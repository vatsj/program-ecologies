import sys, os, uuid; sys.path.insert(0, os.path.dirname(__file__))
from sandbox import Box, cli, cli_resume
b=Box("swarm-smoke")
try:
    s1,s2=str(uuid.uuid4()),str(uuid.uuid4())
    b.agent(cli("sonnet","Remember the secret word APPLE. Reply only OK.",session=s1)+" >/dev/null 2>&1",300)
    b.agent(cli("sonnet2","Remember the secret word PLUM. Reply only OK.",session=s2)+" >/dev/null 2>&1",300)
    b.agent(cli_resume("sonnet","Write your secret word alone into w1.txt.",session=s1)+" >/dev/null 2>&1",300)
    b.agent(cli_resume("sonnet2","Write your secret word alone into w2.txt.",session=s2)+" >/dev/null 2>&1",300)
    print("sonnet ->",(b.get("/work/w1.txt") or "MISSING").strip(),"| sonnet2 ->",(b.get("/work/w2.txt") or "MISSING").strip())
finally:
    b.close()
