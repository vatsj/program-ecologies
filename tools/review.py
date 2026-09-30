"""Send an experiment brief to an external reviewer model (OpenAI API) and
save the review.  Reads OPENAI_API_KEY from .env (gitignored).

    python3 tools/review.py predictions/2026-09-30-modal-arm.md --context CLAUDE.md --model gpt-6-astra
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


def call(model, system, user, key):
    body = json.dumps({"model": model, "input": [{"role": "system", "content": system}, {"role": "user", "content": user}]}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/responses", data=body,
                                 headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        d = json.load(r)
    out = []
    for item in d.get("output", []):
        for c in item.get("content", []) or []:
            if c.get("type") in ("output_text", "text"):
                out.append(c.get("text", ""))
    return "\n".join(out).strip() or json.dumps(d)[:2000]


def load_env():
    p = os.path.join(ROOT, ".env")
    if os.path.exists(p):
        for line in open(p):
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                os.environ.setdefault(k, v.strip().strip('"').strip("'"))


def main(a):
    load_env()
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY not set")
    brief = open(a.brief).read()
    ctx = "".join("\n\n--- context: %s ---\n%s" % (c, open(c).read()) for c in a.context)
    note = ("\n\nNOTE: " + a.note) if a.note else ""
    text = call(a.model, SYSTEM, "Experiment brief:\n\n" + brief + note + ctx, key)
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
