#!/bin/sh
# Counted cells of the behavioural-hooks run, one batch at a time; before each batch the worker count is 1 until the prudence
# run's batch.done exists, then 3 (RS process rule).  Resumable (finished runs are skipped).  Writes runs/hooks_beh/batch.done.
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a775c6f491a2cf348 || exit 1
PRUD=/Users/jstav/code/program-ecologies/.claude/worktrees/agent-a39ef5a00bf34e011/runs/prudence/batch.done
run() {
  if [ -f "$PRUD" ]; then P=3; else P=1; fi
  echo "=== $(date '+%H:%M:%S') batch $1 with $P workers"
  python3 src/hooks_beh_run.py batch "$1" --procs $P
}
run M-open-max,M-thanks-only,M-grudge-only
run open-max,M4-early,M4-late
run M3a-thanks-noinherit,M3b-thanks-nocopy,M3c-thanks-neither,M3d-thanks-noevict,M3e-thanks-single
run beh-max
run beh-max-noA,beh-max-hostile
run beh-written-only,M5-sham
run ff-beh-max
run M3a-max-noinherit,M3b-max-nocopy,M3c-max-neither,M3d-max-noevict,M3e-max-single
run beh-max-N200
echo "=== $(date '+%H:%M:%S') all batches finished"
touch runs/hooks_beh/batch.done
