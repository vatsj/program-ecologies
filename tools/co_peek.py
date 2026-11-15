#!/usr/bin/env python3
"""Queue 79: per running sandbox, finished rows and their summed job walls by N (seconds), to project the remaining cost.

    python3 tools/co_peek.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daytona_run as DR   # noqa: E402
from daytona import Daytona  # noqa: E402

CMD = (r"""cd %s && python3 -c "
import glob, json, collections
w = collections.Counter(); n = collections.Counter()
for f in glob.glob('runs/co_rows/*/rows_*.jsonl'):
    for l in open(f):
        try: r = json.loads(l)
        except Exception: continue
        k = '%%d%%s' %% (r['N'], 'L' if r['long'] else '') + ('i' if r['I'] == 256 else '')
        w[k] += r['job_wall']; n[k] += 1
print(dict(n), {k: round(v / n[k]) for k, v in w.items()})
" """ % DR.REMOTE)

if __name__ == '__main__':
    d = Daytona()
    for s in DR._ours(d):
        try:
            r = s.process.exec(CMD, timeout=120)
            print(s.id[:8], r.result.strip())
        except Exception as e:
            print(s.id[:8], 'error', repr(e)[:80])
