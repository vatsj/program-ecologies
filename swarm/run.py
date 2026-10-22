"""Run one problem over the nonempty subsets of {opus, sol, argon}: one Daytona sandbox per (condition, replicate),
agents launched concurrently in a shared /work with an append-only board; equal wall-clock per condition (v1)."""
import sys, os, json, time, argparse, itertools, threading, traceback
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(__file__))
from sandbox import Box, cli
HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = ("opus", "sol", "argon")
def prompt(me, others, minutes):
    team = (f"You are working together with {', '.join(others)}, other AI agents running at the same time in this "
            f"machine. Coordinate through /work/board.md: append (never rewrite) short dated entries prefixed "
            f"'[{me}]' saying what you are doing, what you found, and what you need. Read the board often. "
            if others else "You are working alone. ")
    return (f"You are the agent '{me}'. Solve the problem in /work/problem.md. {team}"
            f"You have about {minutes} minutes of wall-clock time; budget it. Use the shell and Python freely for "
            f"experiments in /work. Write the final answer to /work/answer.md"
            + (" (one shared file: agree on its content via the board). When you consider answer.md final, append "
               f"'[{me}] FINAL' to the board." if others else ".")
            + " Do not stop early while there is useful work left; stop when the answer is complete.")
def one(problem, cond, rep, minutes, out):
    tag = f"{'+'.join(cond)}-r{rep}"; d = os.path.join(out, tag); os.makedirs(d, exist_ok=True)
    meta = {"condition": cond, "replicate": rep, "minutes": minutes, "start": time.time()}
    b = None
    try:
        for attempt in range(60):
            try:
                b = Box(f"swarm-{problem}"); break
            except Exception as e:
                if "limit" in str(e).lower() and attempt < 59: time.sleep(60); continue
                raise
        b.put(os.path.join(HERE, "problems", problem + ".md"), "/work/problem.md")
        b.agent("touch board.md; mkdir -p logs")
        res = {}
        def go(m):
            others = [x for x in cond if x != m]
            c = f"timeout {minutes*60} {cli(m, prompt(m, others, minutes))} > logs/{m}.out 2> logs/{m}.err; echo $?"
            t0 = time.time(); r = b.agent(c, t=minutes*60 + 300)
            res[m] = {"exit": r.result.strip()[-20:], "seconds": round(time.time() - t0)}
        ths = [threading.Thread(target=go, args=(m,)) for m in cond]
        [t.start() for t in ths]; [t.join() for t in ths]
        meta["agents"] = res
        for f in ["answer.md", "board.md"] + [f"logs/{m}.out" for m in cond] + [f"logs/{m}.err" for m in cond]:
            txt = b.get("/work/" + f)
            if txt is not None:
                p = os.path.join(d, f.replace("logs/", "")); open(p, "w").write(txt)
        meta["files"] = b.agent("ls -la /work | head -40").result
    except Exception:
        meta["error"] = traceback.format_exc()[-2000:]
    finally:
        meta["end"] = time.time()
        if b: 
            try: b.close()
            except Exception: pass
        json.dump(meta, open(os.path.join(d, "meta.json"), "w"), indent=1)
        print(f"{tag} done in {meta['end']-meta['start']:.0f}s {'ERROR' if 'error' in meta else ''}", flush=True)
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("problem"); ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--minutes", type=int, default=15); ap.add_argument("--parallel", type=int, default=7)
    ap.add_argument("--only", default=None, help="comma list of conditions like opus,opus+sol")
    a = ap.parse_args()
    conds = [c for k in (1, 2, 3) for c in itertools.combinations(NAMES, k)]
    if a.only: conds = [tuple(x.split("+")) for x in a.only.split(",")]
    out = os.path.join(HERE, "runs", a.problem); os.makedirs(out, exist_ok=True)
    jobs = [(c, r) for r in range(a.reps) for c in conds]
    with ThreadPoolExecutor(a.parallel) as ex:
        for c, r in jobs: ex.submit(one, a.problem, c, r, a.minutes, out)
    open(os.path.join(out, "ALL_DONE"), "w").write(time.ctime())
