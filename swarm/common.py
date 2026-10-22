"""Shared helpers for the swarm harness. Keys are read from .env and passed per command; never printed or stored."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load_env():
    env = {}
    for line in open(os.path.join(ROOT, ".env")):
        m = re.match(r"^([A-Z_][A-Z0-9_]*)=(.*)$", line.strip())
        if m: env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return env
ALLOW = ("api.anthropic.com,statsig.anthropic.com,api.openai.com,chatgpt.com,generativelanguage.googleapis.com,"
         "oauth2.googleapis.com,registry.npmjs.org,pypi.org,files.pythonhosted.org,github.com,objects.githubusercontent.com")
INSTALL = "npm install -g --silent @anthropic-ai/claude-code @openai/codex @google/gemini-cli >/tmp/npm.log 2>&1; echo npm:$?"
def agent_env(keys):
    return {"ANTHROPIC_API_KEY": keys["ANTHROPIC_API_KEY"], "OPENAI_API_KEY": keys["OPENAI_API_KEY"],
            "GEMINI_API_KEY": keys["GEMINI_API_KEY"], "DISABLE_TELEMETRY": "1", "GEMINI_TELEMETRY_ENABLED": "false",
            "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"}
