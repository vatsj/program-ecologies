#!/bin/sh
# After the main queue (runs/hooks_beh/batch.done): the inert-hooks reference at this geometry (a counted reference cell, added
# after seeing that plain provers win many beh-max islands), then diagnostic re-runs (not counted).  One process at a time.
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a775c6f491a2cf348 || exit 1
until [ -f runs/hooks_beh/batch.done ]; do sleep 120; done
PRUD=/Users/jstav/code/program-ecologies/.claude/worktrees/agent-a39ef5a00bf34e011/runs/prudence/batch.done
if [ -f "$PRUD" ]; then P=3; else P=1; fi
python3 src/hooks_beh_run.py batch inert --procs $P
for r in 0 1 2; do
  python3 tools/beh_diag.py beh-max $r 200 runs/hooks_beh/diag_beh-max_${r}_200.md > /dev/null 2>&1
  python3 tools/beh_diag.py beh-max $r 500 runs/hooks_beh/diag_beh-max_${r}_500.md > /dev/null 2>&1
done
touch runs/hooks_beh/after.done
