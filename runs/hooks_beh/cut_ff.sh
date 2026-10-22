#!/bin/sh
# Cost cut declared in notes 2.3: stop ff-beh-max after 6 completed runs (about 50 minutes each), kill the batch (children by pid,
# then the parent) and let run_all.sh go on to the next batch.
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a775c6f491a2cf348 || exit 1
until [ "$(grep -c '^ff-beh-max rep' runs/hooks_beh/run_all.log)" -ge 6 ]; do sleep 60; done
PARENT=$(pgrep -f "hooks_beh_run.py batch ff-beh-max" | head -1)
for c in $(pgrep -P "$PARENT"); do kill "$c"; done
sleep 2
kill "$PARENT"
echo "cut at $(date)"
