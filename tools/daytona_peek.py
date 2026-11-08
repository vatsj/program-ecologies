#!/usr/bin/env python3
"""Count finished rows in a running sandbox: python3 tools/daytona_peek.py SANDBOX_ID RELATIVE_ROWS_DIR"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daytona_run as DR   # noqa: E402
from daytona import Daytona  # noqa: E402

if __name__ == '__main__':
    d = Daytona()
    for s in DR._ours(d):
        if len(sys.argv) > 1 and not s.id.startswith(sys.argv[1]) and sys.argv[1] != 'all':
            continue
        try:
            r = s.process.exec(f'cat {DR.REMOTE}/{sys.argv[2]}/rows_*.jsonl 2>/dev/null | wc -l; tail -n 1 /tmp/job.log 2>/dev/null | cut -c1-120', timeout=60)
            print(s.id[:8], r.result.strip().replace('\n', ' | '))
        except Exception as e:
            print(s.id[:8], 'error', repr(e)[:80])
