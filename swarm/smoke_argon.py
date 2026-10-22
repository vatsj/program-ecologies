import sys, os, time; sys.path.insert(0, os.path.dirname(__file__))
from sandbox import Box, cli
b = Box("swarm-smoke")
try:
    r = b.agent(cli("argon", "Write the single word OK into a file named ok_argon.txt in the current directory, then reply DONE.") + " 2>&1 | tail -c 700", 300)
    print(f"exit {r.exit_code}: {r.result.strip()[-700:]}"); print(b.agent("ls; cat ok_argon.txt").result)
finally:
    b.close()
