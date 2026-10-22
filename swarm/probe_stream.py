import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from sandbox import Box, MODELS
b=Box("swarm-probe")
try:
    r=b.agent(f"gemini -m {MODELS['argon']} --skip-trust --yolo --output-format stream-json -p 'Run the shell command: echo hi > x.txt, then reply DONE.' 2>/dev/null | tail -c 1500",300)
    print("GEMINI:", r.result[-1500:])
    r=b.agent("claude -p 'Run: echo hi > y.txt then reply DONE' --model " + MODELS['opus'] + " --permission-mode bypassPermissions --output-format stream-json --verbose 2>/dev/null > c.jsonl; python3 -c \"import json;[print(json.loads(l).get('type'), json.loads(l).get('message',{}).get('usage') if isinstance(json.loads(l).get('message'),dict) else json.loads(l).get('usage')) for l in open('c.jsonl')]\"",300)
    print("CLAUDE:", r.result[-1200:])
finally:
    b.close()
