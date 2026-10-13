"""Send an experiment brief to an external reviewer model and save the review.
OpenAI models read OPENAI_API_KEY, Gemini models (name starting with "gemini") read GEMINI_API_KEY,
both from .env (gitignored).

    python3 tools/review.py specs/<file>.md --context CLAUDE.md --model gpt-6.1-sol
    python3 tools/review.py specs/<file>.md --context CLAUDE.md --model gemini-4-argon
Writes reviews/<brief-stem>-<model>.md.
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
    user = "Experiment brief:\n\n" + brief + note + ctx
    text = call_gemini(a.model, SYSTEM, user, key) if gemini else call(a.model, SYSTEM, user, key)
    stem = os.path.splitext(os.path.basename(a.brief))[0]
    out = os.path.join(ROOT, "reviews", "%s-%s.md" % (stem, a.model))
    open(out, "w").write("# Review of `%s` by %s\n\n%s\n" % (a.brief, a.model, text))
    print(out); print(text)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("brief")
    ap.add_argument("--context", nargs="*", default=[])
    ap.add_argument("--model", default="gpt-6-astra")
    ap.add_argument("--note", default="")
    main(ap.parse_args())
