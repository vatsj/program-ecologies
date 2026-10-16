#!/bin/sh
# Budget (notes §2.5, second addendum): after the B2 driver (pid 63529) ends, B2 at eps N = 1; the slow B1 checkpoint
# rs_prop_400_64_cal 9 is dropped.
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a4a0f6a7072bc2408
while kill -0 63529 2>/dev/null; do sleep 20; done
python3 src/removing_rivals_run.py lottery --workers 3 --out B --cells rr_rain1_200_64 rr_rain1_200_128 >> runs/removing_rivals/lottery_B.log 2>&1 || exit 8
echo all > runs/removing_rivals/batches.done
