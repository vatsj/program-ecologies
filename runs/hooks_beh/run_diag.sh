#!/bin/sh
# Diagnostics (not counted cells): deterministic re-runs of counted runs to dump signature histograms and common types.
# Waits for the main queue (runs/hooks_beh/batch.done) so the worker rule is kept; one process at a time.
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a775c6f491a2cf348 || exit 1
until [ -f runs/hooks_beh/batch.done ]; do sleep 120; done
for r in 0 1 2; do
  python3 tools/beh_diag.py beh-max $r 200 runs/hooks_beh/diag_beh-max_${r}_200.md > /dev/null 2>&1
  python3 tools/beh_diag.py beh-max $r 500 runs/hooks_beh/diag_beh-max_${r}_500.md > /dev/null 2>&1
done
touch runs/hooks_beh/diag.done
