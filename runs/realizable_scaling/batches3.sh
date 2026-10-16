#!/bin/sh
# After the C-donor driver (pid 35233) ends: dense donors on the calibrated arm only at (200, 64), then C-donor
# (400, 64) calibrated with 10 replicates (notes §2, second addendum: budget).
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-abbd4be19f0352379
while kill -0 35233 2>/dev/null; do sleep 20; done
R="python3 src/realizable_scaling_run.py"
$R lottery --workers 3 --out cdense --noext --cells rs_Cdense_200_64_cal >> runs/realizable_scaling/lottery_cdense.log 2>&1 || exit 5
$R lottery --workers 3 --out cdon400 --noext --runs 10 --cells rs_Cdon_400_64_cal >> runs/realizable_scaling/lottery_cdon400.log 2>&1 || exit 6
echo all > runs/realizable_scaling/batches.done
