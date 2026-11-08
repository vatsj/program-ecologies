#!/usr/bin/env python3
"""Recover the outputs of an orphaned `daytona_run.py run` sandbox (its client died): wait for /tmp/job.exit, then fetch
the repo-relative OUT directory and delete the sandbox.

    python3 tools/daytona_fetch.py SANDBOX_ID OUT_DIR [--poll 60]
"""
import io, os, sys, tarfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daytona_run as DR   # noqa: E402
from daytona import Daytona  # noqa: E402

if __name__ == '__main__':
    sid, out = sys.argv[1], sys.argv[2].strip('/')
    poll = int(sys.argv[sys.argv.index('--poll') + 1]) if '--poll' in sys.argv else 60
    d = Daytona()
    sb = [s for s in DR._ours(d) if s.id == sid][0]
    while True:
        try:
            done = sb.process.exec('cat /tmp/job.exit 2>/dev/null || true', timeout=60).result.strip()
        except Exception as e:           # transient gateway errors
            DR._log('poll error', repr(e)[:100]); time.sleep(poll); continue
        if done:
            break
        time.sleep(poll)
    sb.process.exec(f'cd {DR.REMOTE} && tar -cf /tmp/out.tar {out} 2>/dev/null || true', timeout=600)
    data = sb.fs.download_file('/tmp/out.tar')
    if data:
        with tarfile.open(fileobj=io.BytesIO(data)) as t:
            t.extractall(DR.ROOT, filter='data')
        DR._log('fetched', out, 'exit', done)
    d.delete(sb)
