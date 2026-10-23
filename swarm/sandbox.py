"""Sandbox lifecycle for the swarm harness: a fixed image (4 vCPU, 8 GB), a non-root `agent` user, keys in a 600 file."""
import sys, os, shlex; sys.path.insert(0, os.path.dirname(__file__))
from common import load_env
from daytona import Daytona, DaytonaConfig, Image, CreateSandboxFromImageParams, Resources
IMAGE = (Image.debian_slim("3.11")
         .pip_install(["numpy==1.26.4", "scipy==1.13.1", "sympy==1.13.3", "networkx==3.3"])
         .run_commands("apt-get update && apt-get install -y --no-install-recommends curl ca-certificates git ripgrep procps "
                       "&& curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && apt-get install -y nodejs "
                       "&& rm -rf /var/lib/apt/lists/*",
                       "npm install -g @anthropic-ai/claude-code @openai/codex @google/gemini-cli && npm cache clean --force",
                       "useradd -m -s /bin/bash agent && mkdir -p /work && chown agent:agent /work"))
MODELS = {"opus": "claude-opus-5-5", "sonnet": "claude-sonnet-5-5", "sol": "gpt-6.1-sol", "argon": "gemini-4-argon"}
import re as _re
def family(name):
    """Agent names may carry a suffix (sonnet2); the model is the name without trailing digits."""
    return _re.sub(r"\d+$", "", name)
class Box:
    def __init__(self, label="swarm"):
        self.keys = load_env()
        self.d = Daytona(DaytonaConfig(api_key=self.keys["DAYTONA_API_KEY"]))
        self.sb = self.d.create(CreateSandboxFromImageParams(image=IMAGE, resources=Resources(cpu=4, memory=8, disk=10),
                                labels={"purpose": label}, auto_delete_interval=120), timeout=1800,
                                on_snapshot_create_logs=lambda l: None)
        envfile = "\n".join(f"export {k}={shlex.quote(self.keys[k])}" for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY"))
        envfile += "\nexport DISABLE_TELEMETRY=1 GEMINI_TELEMETRY_ENABLED=false GEMINI_CLI_TRUST_WORKSPACE=true CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1\n"
        self.sb.fs.upload_file(envfile.encode(), "/home/agent/.agent_env")
        self.root("chown agent:agent /home/agent/.agent_env && chmod 600 /home/agent/.agent_env")
        self.agent("printenv OPENAI_API_KEY | codex login --with-api-key >/dev/null 2>&1; echo codex-login:$?")
    def root(self, cmd, t=600):
        return self.sb.process.exec(cmd, timeout=t)
    def agent(self, cmd, t=600, cwd="/work"):
        inner = f"source ~/.agent_env; cd {cwd}; {cmd}"
        return self.sb.process.exec(f"su - agent -c {shlex.quote(inner)}", timeout=t)
    def put(self, local, remote):
        self.sb.fs.upload_file(open(local, "rb").read(), remote); self.root(f"chown agent:agent {remote}")
    def get(self, remote):
        try: return self.sb.fs.download_file(remote).decode(errors="replace")
        except Exception: return None
    def close(self):
        self.sb.delete()
def cli_resume(name, prompt, session=None):
    q = shlex.quote(prompt); m = family(name)
    if m in ("opus", "sonnet"):
        sess = f"--resume {session}" if session else "-c"
        return f"claude {sess} -p {q} --model {MODELS[m]} --permission-mode bypassPermissions --output-format stream-json --verbose"
    if m == "sol":
        return (f"codex exec resume --last --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox --json "
                f"-m {MODELS['sol']} {q}")
    if m == "argon":
        return f"gemini -m {MODELS['argon']} --skip-trust --yolo --output-format stream-json --resume latest -p {q}"
def cli(name, prompt, json_out=True, session=None):
    q = shlex.quote(prompt); m = family(name)
    if m in ("opus", "sonnet"):
        sess = f" --session-id {session}" if session else ""
        return f"claude -p {q} --model {MODELS[m]}{sess} --permission-mode bypassPermissions --output-format stream-json --verbose"
    if m == "sol":
        return f"codex exec --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox --json -m {MODELS['sol']} {q}"
    if m == "argon":
        return f"gemini -m {MODELS['argon']} --skip-trust --yolo --output-format stream-json -p {q}"
