"""Build the standard swarm sandbox snapshot: Python 3.11 + numpy/scipy/sympy/networkx, Node 22, the three agent CLIs; 4 vCPU, 8 GB."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__))
from common import load_env
from daytona import Daytona, DaytonaConfig, Image, CreateSnapshotParams, Resources
NAME = "swarm-agents-v1"
keys = load_env(); d = Daytona(DaytonaConfig(api_key=keys["DAYTONA_API_KEY"]))
try:
    s = d.snapshot.get(NAME); print("exists:", s.name, s.state); sys.exit(0)
except Exception:
    pass
img = (Image.debian_slim("3.11")
       .pip_install(["numpy==1.26.4", "scipy==1.13.1", "sympy==1.13.3", "networkx==3.3"])
       .run_commands("apt-get update && apt-get install -y --no-install-recommends curl ca-certificates git ripgrep procps "
                     "&& curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && apt-get install -y nodejs "
                     "&& rm -rf /var/lib/apt/lists/*",
                     "npm install -g @anthropic-ai/claude-code @openai/codex @google/gemini-cli && npm cache clean --force",
                     "useradd -m -s /bin/bash agent || true")
       .workdir("/home/agent"))
snap = d.snapshot.create(CreateSnapshotParams(name=NAME, image=img, resources=Resources(cpu=4, memory=8, disk=10)),
                         on_logs=lambda l: print(l.rstrip()[-160:]) if any(k in l for k in ("Step", "ERROR", "error", "added", "Successfully")) else None,
                         timeout=1800)
print("built:", snap.name, snap.state)
