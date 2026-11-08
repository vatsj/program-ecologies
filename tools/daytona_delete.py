#!/usr/bin/env python3
"""Delete named Daytona sandboxes of this project (queue 75; `daytona_run.py cleanup` deletes all of them).

    python3 tools/daytona_delete.py ID [ID ...]
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daytona_run as DR   # noqa: E402  (patches the proxy on import)
from daytona import Daytona  # noqa: E402

if __name__ == '__main__':
    d = Daytona()
    ids = set(sys.argv[1:])
    for s in DR._ours(d):
        if s.id in ids:
            d.delete(s)
            DR._log('deleted', s.id)
