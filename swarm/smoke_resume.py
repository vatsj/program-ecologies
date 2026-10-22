import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from sandbox import Box, cli, cli_resume
b=Box("swarm-smoke")
try:
    for m in ("opus","sol","argon"):
        r1=b.agent(cli(m,"Remember the secret word BANANA. Reply only OK.")+" > /dev/null 2>&1; echo first:$?", 300)
        r2=b.agent(cli_resume(m,f"What was the secret word? Write it alone into the file word_{m}.txt.")+" > /dev/null 2>&1; echo resume:$?", 300)
        print(m, r1.result.strip(), r2.result.strip(), "->", (b.get(f"/work/word_{m}.txt") or "MISSING").strip())
finally:
    b.close()
