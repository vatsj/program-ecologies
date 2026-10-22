import sys, os, time; sys.path.insert(0, os.path.dirname(__file__))
from sandbox import Box, cli
t0 = time.time(); b = Box("swarm-smoke"); print(f"sandbox up in {time.time()-t0:.0f}s")
try:
    print(b.root("nproc; cat /sys/fs/cgroup/cpu.max; claude --version; codex --version; gemini --version").result)
    print(b.agent("whoami; ls -la ~/.agent_env | cut -c1-30; codex login status 2>&1 | head -2").result)
    for m in ("opus", "sol", "argon"):
        t1 = time.time()
        r = b.agent(cli(m, f"Write the single word OK into a file named ok_{m}.txt in the current directory, then reply DONE.") + " 2>&1 | tail -c 400", 300)
        print(f"== {m} ({time.time()-t1:.0f}s, exit {r.exit_code}): {r.result.strip()[-400:]}")
    print(b.agent("ls; cat ok_*.txt").result)
finally:
    b.close(); print("deleted")
