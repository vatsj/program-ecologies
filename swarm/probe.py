import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from common import load_env
from daytona import Daytona, DaytonaConfig, CreateSandboxFromSnapshotParams
keys=load_env(); d=Daytona(DaytonaConfig(api_key=keys["DAYTONA_API_KEY"]))
sb=d.create(CreateSandboxFromSnapshotParams(language="python", auto_delete_interval=60), timeout=180)
try:
    r=lambda c,t=900: print(sb.process.exec(c,timeout=t).result[-2500:])
    r("whoami; echo $SHELL; npm config get prefix; ls -ld $(npm config get prefix)/lib/node_modules; cat /sys/fs/cgroup/cpu.max 2>/dev/null; cat /sys/fs/cgroup/memory.max 2>/dev/null")
    r("npm install -g @anthropic-ai/claude-code@latest @openai/codex@latest @google/gemini-cli@latest 2>&1 | tail -25; echo EXIT:$?")
    r("claude --version; codex --version; gemini --version")
finally:
    sb.delete()
