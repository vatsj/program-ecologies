import sys, os, time; sys.path.insert(0, os.path.dirname(__file__))
from common import load_env
from daytona import Daytona, DaytonaConfig, Image, CreateSandboxFromImageParams, Resources
keys=load_env(); d=Daytona(DaytonaConfig(api_key=keys["DAYTONA_API_KEY"]))
img=(Image.debian_slim("3.11").pip_install(["numpy==1.26.4","scipy==1.13.1","sympy==1.13.3","networkx==3.3"])
     .run_commands("apt-get update && apt-get install -y --no-install-recommends curl ca-certificates git ripgrep procps && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && apt-get install -y nodejs && rm -rf /var/lib/apt/lists/*",
                   "npm install -g @anthropic-ai/claude-code @openai/codex @google/gemini-cli && npm cache clean --force"))
t0=time.time()
sb=d.create(CreateSandboxFromImageParams(image=img, resources=Resources(cpu=4, memory=8, disk=10), auto_delete_interval=60),
            timeout=1800, on_snapshot_create_logs=lambda l: None)
print("created in", round(time.time()-t0), "s", sb.id)
try:
    print(sb.process.exec("whoami; nproc; cat /sys/fs/cgroup/cpu.max; cat /sys/fs/cgroup/memory.max; claude --version; codex --version; gemini --version; python3 -c 'import numpy,scipy;print(numpy.__version__,scipy.__version__)'", timeout=120).result)
finally:
    sb.delete()
