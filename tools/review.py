"""Send an experiment brief to an external reviewer model and save the review.
OpenAI models read OPENAI_API_KEY, Gemini models (name starting with "gemini") read GEMINI_API_KEY,
both from .env (gitignored).

    python3 tools/review.py specs/<file>.md --context CLAUDE.md --model gpt-6.1-sol
    python3 tools/review.py specs/<file>.md --context CLAUDE.md --model gemini-4-argon
Writes reviews/<brief-stem>-<model>.md.

Modes (RS, 2026-10-17; two reviews before a run and two after, each pair sequential: one model, fold, then the
other, alternating which goes first):
    (default) spec   the first pre-run review of a draft spec -> reviews/<stem>-<model>.md
    --mode amended   the second pre-run review: a full review of the spec with the first review folded in, which also
                     checks the folded amendments for errors and inconsistencies -> reviews/<stem>-amended-<model>.md
    --mode audit     a draft RESULTS section (the brief argument) checked against run files passed as --context
                     -> reviews/<stem>-audit-<model>.md
"""
import argparse, json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SYSTEM = """You are a critical research collaborator reviewing an experiment brief before it is run.
The project studies evolutionary dynamics over populations of programs that can read or reason about
each other (open-source game theory), with the goal of characterizing when selection reaches Pareto-
efficient outcomes in the large-population limit. Be concrete and brief. Report, in order of importance:
1. Design flaws or confounds that would make the result uninterpretable, and the fix.
2. Predictions you think are wrong, with the reason and your own prediction.
3. Missing controls or cheap additions that would sharpen the conclusion.
4. Alternative explanations the brief does not rule out.
5. Ideas that matter for the research program beyond this experiment (only if genuinely new).
Say "nothing material" for any empty category. Under 600 words. No preamble."""


AMENDED = """You are a critical research collaborator giving the second review of an experiment brief before it is run.
The first reviewer's points have been folded in (marked [after review] or in an amendments section). The project studies
evolutionary dynamics over populations of programs that read or reason about each other (open-source game theory),
with the goal of characterizing when selection reaches Pareto-efficient outcomes in the large-population limit. Be
concrete and brief. Report, in order of importance:
1. Errors, contradictions or unsound mechanisms that the folded amendments introduced or left (quote the conflicting
   sentences), and the fix.
2. Design flaws or confounds that would make the result uninterpretable, and the fix.
3. Predictions you think are wrong, with the reason and your own prediction.
4. Missing controls or cheap additions that would sharpen the conclusion.
5. Alternative explanations the brief does not rule out.
Say "nothing material" for any empty category. Under 600 words. No preamble."""

AUDIT = """You are auditing a draft results section against the run files it summarizes, before it is committed to an
append-only research record. The project studies evolutionary dynamics over populations of programs that read or reason
about each other. Check: every number in the draft against the run files; every verdict against the stated prediction
and falsifier; claims in the reading that the data do not support or that overstate them (finite-size claims stated as
limits, post-hoc results stated as tested, correlations stated as mechanisms); disclosed deviations that change what a
verdict means; and anything material in the run files that the draft omits. Report each problem with the draft sentence,
the evidence, and the correction. If there is nothing material, say "nothing material". Under 500 words. No preamble."""

def _req(url, key, body=None):
    req = urllib.request.Request(url, data=body, headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def call(model, system, user, key, poll=15, max_wait=3600):
    """Background-mode request, polled until done (long reasoning drops plain connections)."""
    import time
    body = json.dumps({"model": model, "background": True,
                       "input": [{"role": "system", "content": system}, {"role": "user", "content": user}]}).encode()
    d = _req("https://api.openai.com/v1/responses", key, body)
    rid, t0 = d["id"], time.time()
    while d.get("status") in ("queued", "in_progress") and time.time() - t0 < max_wait:
        time.sleep(poll)
        try:
            d = _req("https://api.openai.com/v1/responses/" + rid, key)
        except Exception as e:          # transient network error: keep polling
            print("poll error:", e, file=sys.stderr)
    if d.get("status") != "completed":
        return "REVIEW FAILED: status %s %s" % (d.get("status"), json.dumps(d.get("error") or d.get("incomplete_details"))[:500])
    out = []
    for item in d.get("output", []):
        for c in item.get("content", []) or []:
            if c.get("type") in ("output_text", "text"):
                out.append(c.get("text", ""))
    return "\n".join(out).strip() or json.dumps(d)[:2000]


def call_gemini(model, system, user, key, max_wait=3600):
    """Gemini backend (google-genai): one synchronous generate call with a long timeout."""
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=key, http_options=types.HttpOptions(timeout=max_wait * 1000))
    r = client.models.generate_content(model=model, contents=user,
                                       config=types.GenerateContentConfig(system_instruction=system))
    text = (r.text or "").strip()
    return text or "REVIEW FAILED: empty response %s" % str(r)[:500]


def load_env():
    p = os.path.join(ROOT, ".env")
    if os.path.exists(p):
        for line in open(p):
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                os.environ.setdefault(k, v.strip().strip('"').strip("'"))


def main(a):
    load_env()
    gemini = a.model.startswith("gemini")
    key = os.environ.get("GEMINI_API_KEY" if gemini else "OPENAI_API_KEY")
    if not key:
        sys.exit(("GEMINI_API_KEY" if gemini else "OPENAI_API_KEY") + " not set")
    brief = open(a.brief).read()
    ctx = "".join("\n\n--- context: %s ---\n%s" % (c, open(c).read()) for c in a.context)
    note = ("\n\nNOTE: " + a.note) if a.note else ""
    system = {"spec": SYSTEM, "amended": AMENDED, "audit": AUDIT}[a.mode]
    head = {"spec": "Experiment brief", "amended": "Amended experiment brief", "audit": "Draft results section"}[a.mode]
    user = head + ":\n\n" + brief + note + ctx
    text = call_gemini(a.model, system, user, key) if gemini else call(a.model, system, user, key)
    stem = os.path.splitext(os.path.basename(a.brief))[0]
    tag = "" if a.mode == "spec" else a.mode + "-"
    out = os.path.join(ROOT, "reviews", "%s-%s%s.md" % (stem, tag, a.model))
    open(out, "w").write("# Review of `%s` by %s\n\n%s\n" % (a.brief, a.model, text))
    print(out); print(text)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("brief")
    ap.add_argument("--context", nargs="*", default=[])
    ap.add_argument("--model", default="gpt-6-astra")
    ap.add_argument("--note", default="")
    ap.add_argument("--mode", choices=["spec", "amended", "audit"], default="spec")
    main(ap.parse_args())
