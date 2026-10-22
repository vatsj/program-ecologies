import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from sandbox import Box
b=Box("swarm-probe")
try:
    print(b.agent("claude --help 2>&1 | grep -iE -- '--continue|--resume|-c,' | head -4; echo ---; codex exec --help 2>&1 | grep -iE 'resume' | head -5; codex exec resume --help 2>&1 | head -12; echo ---; gemini --help 2>&1 | grep -iE 'resume|session' | head -6").result)
finally:
    b.close()
