#!/usr/bin/env python3
"""Run an experiment command in a Daytona sandbox (2026-11-06).

Cloud sessions cannot reach Modal (its client is gRPC-only and the sandbox proxy
carries HTTPS only), so remote compute goes through Daytona's REST API.

    python3 tools/daytona_run.py run --cpus 4 --out runs/foo -- python3 src/foo.py --args
    python3 tools/daytona_run.py list | cleanup

`run` ships `git archive HEAD` (commit first: uncommitted edits are not sent,
`--dirty` adds the tracked working-tree diff), runs the command from the repo root
inside a `python:3.11-slim` sandbox after `pip install -r requirements.txt` (the
pinned environment the published runs used; about a minute; this account may not
build snapshots), streams nothing, polls until it exits,
then downloads `--out` (a repo-relative directory) back into the local checkout
and deletes the sandbox. Exit code is the command's. Sandboxes are labelled
`program-ecologies` so `cleanup` can remove strays.

`nproc` inside a sandbox reports the host's cores, not the quota: the job sees
DAYTONA_CPUS and thread caps (NUMBA_NUM_THREADS, OMP_NUM_THREADS, ...) set to --cpus;
size worker pools from DAYTONA_CPUS.

Keys: DAYTONA_API_KEY from the environment; never printed.
"""
import argparse, importlib, io, os, subprocess, sys, tarfile, time

IMAGE = "python:3.11-slim"
LABEL = {"project": "program-ecologies"}
REMOTE = "/home/daytona/repo"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _patch_proxy():
    """The SDK's generated clients ignore HTTPS_PROXY; set it (and the CA) explicitly."""
    px = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if not px:
        return
    ca = "/root/.ccr/ca-bundle.crt"
    for mod in ("daytona_api_client.configuration", "daytona_toolbox_api_client.configuration",
                "daytona_analytics_api_client.configuration"):
        try:
            C = importlib.import_module(mod).Configuration
        except ImportError:
            continue
        orig = C.__init__

        def init(self, *a, _o=orig, **k):
            _o(self, *a, **k)
            self.proxy = px
            if os.path.exists(ca):
                self.ssl_ca_cert = ca
        C.__init__ = init


_patch_proxy()
from daytona import (CreateSandboxFromImageParams, Daytona, Resources,  # noqa: E402
                     SessionExecuteRequest)


def _log(*a):
    print("[daytona]", *a, file=sys.stderr, flush=True)


def _archive(dirty):
    tar = subprocess.run(["git", "archive", "--format=tar", "HEAD"], cwd=ROOT, check=True,
                         capture_output=True).stdout
    if not dirty:
        return tar
    buf = io.BytesIO(tar)
    changed = subprocess.run(["git", "diff", "--name-only", "HEAD"], cwd=ROOT, check=True,
                             capture_output=True, text=True).stdout.split()
    out = io.BytesIO()
    with tarfile.open(fileobj=buf) as src, tarfile.open(fileobj=out, mode="w") as dst:
        for m in src.getmembers():
            if m.name not in changed:
                dst.addfile(m, src.extractfile(m) if m.isfile() else None)
        for f in changed:
            if os.path.exists(os.path.join(ROOT, f)):
                dst.add(os.path.join(ROOT, f), arcname=f)
    return out.getvalue()


def cmd_run(d, a):
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True,
                          text=True).stdout.strip()
    command = " ".join(a.command)
    _log(f"HEAD {head}{' +dirty' if a.dirty else ''}: {command}")
    sb = d.create(CreateSandboxFromImageParams(image=IMAGE, labels=LABEL,
                                               resources=Resources(cpu=a.cpus, memory=a.memory, disk=a.disk),
                                               auto_stop_interval=0, auto_delete_interval=a.ttl),
                  timeout=600)
    _log("sandbox", sb.id)
    code = 1
    try:
        sb.fs.upload_file(_archive(a.dirty), "/tmp/repo.tar")
        r = sb.process.exec(f"mkdir -p {REMOTE} && tar -xf /tmp/repo.tar -C {REMOTE} && "
                            f"pip install -q --root-user-action=ignore -r {REMOTE}/requirements.txt 2>&1 | tail -3",
                            timeout=900)
        if r.exit_code:
            _log("setup failed:", r.result)
            return 1
        caps = " ".join(f"{v}={a.cpus}" for v in ("DAYTONA_CPUS", "NUMBA_NUM_THREADS", "OMP_NUM_THREADS",
                                                    "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"))
        sess = "job"
        sb.process.create_session(sess)
        sb.process.execute_session_command(sess, SessionExecuteRequest(
            command=f"cd {REMOTE} && export {caps} && ({command}) > /tmp/job.log 2>&1; echo $? > /tmp/job.exit",
            run_async=True))
        t0 = time.time()
        while True:
            time.sleep(a.poll)
            done = sb.process.exec("cat /tmp/job.exit 2>/dev/null || true", timeout=60).result.strip()
            if done:
                code = int(done)
                break
            if a.timeout and time.time() - t0 > a.timeout:
                _log("timeout; collecting partial outputs")
                break
        log = sb.fs.download_file("/tmp/job.log")
        os.makedirs(a.logdir, exist_ok=True)
        lp = os.path.join(a.logdir, f"{sb.id}.log")
        open(lp, "wb").write(log)
        sys.stdout.write(log.decode(errors="replace")[-a.tail:])
        _log(f"exit {code} after {time.time() - t0:.0f}s; log {lp}")
        for out in a.out or []:
            rel = out.strip("/")
            sb.process.exec(f"cd {REMOTE} && tar -cf /tmp/out.tar {rel} 2>/dev/null || true", timeout=600)
            data = sb.fs.download_file("/tmp/out.tar")
            if data:
                with tarfile.open(fileobj=io.BytesIO(data)) as t:
                    t.extractall(ROOT, filter="data")
                _log("fetched", rel)
    finally:
        if a.keep:
            _log("kept sandbox", sb.id)
        else:
            d.delete(sb)
    return code


def _ours(d):
    return [s for s in d.list() if (getattr(s, "labels", None) or {}).get("project") == LABEL["project"]]


def cmd_list(d, a):
    for s in _ours(d):
        print(s.id, s.state, getattr(s, "created_at", ""))
    return 0


def cmd_cleanup(d, a):
    for s in _ours(d):
        d.delete(s)
        _log("deleted", s.id)
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    r = sp.add_parser("run")
    r.add_argument("--cpus", type=int, default=4)
    r.add_argument("--memory", type=int, default=8, help="GiB")
    r.add_argument("--disk", type=int, default=10, help="GiB")
    r.add_argument("--out", action="append", help="repo-relative directory to fetch back (repeatable)")
    r.add_argument("--dirty", action="store_true", help="also ship uncommitted tracked edits")
    r.add_argument("--poll", type=float, default=20)
    r.add_argument("--timeout", type=float, default=0, help="seconds; 0 = none")
    r.add_argument("--ttl", type=int, default=60, help="minutes a stopped sandbox lives before auto-delete")
    r.add_argument("--keep", action="store_true")
    r.add_argument("--tail", type=int, default=4000)
    r.add_argument("--logdir", default=os.path.join(ROOT, "runs", "_daytona_logs"))
    r.add_argument("command", nargs=argparse.REMAINDER)
    sp.add_parser("list")
    sp.add_parser("cleanup")
    a = p.parse_args()
    if a.cmd == "run":
        if a.command and a.command[0] == "--":
            a.command = a.command[1:]
        if not a.command:
            p.error("run needs a command after --")
    d = Daytona()
    sys.exit({"run": cmd_run, "list": cmd_list, "cleanup": cmd_cleanup}[a.cmd](d, a))


if __name__ == "__main__":
    main()
