#!/bin/sh
# Remaining cells after the drop-order step 2 (notes §2 addendum): C-donor at (400, 64) mN = 1 and dense donors at
# N = 400 dropped; C-donor (400, 64) calibrated kept. Resumable (the driver skips finished (cell, replicate) pairs).
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-abbd4be19f0352379
R="python3 src/realizable_scaling_run.py"
$R lottery --workers 3 --out cdon --noext --cells \
  rs_Cdon_100_64_cal rs_Cdon_200_64_m1 rs_Cdon_200_64_cal rs_Cdon_100_128_cal rs_Cdon_100_256_cal \
  rs_Cdon_50_64_m1 rs_Cdon_50_64_cal rs_Cdon_100_32_cal rs_Cdon_200_128_m1 rs_Cdon_200_128_cal rs_Cdon_50_32_m1 rs_Cdon_50_32_cal \
  >> runs/realizable_scaling/lottery_cdon.log 2>&1 || exit 4
$R lottery --workers 3 --out cdense --noext --cells rs_Cdense_200_64_m1 rs_Cdense_200_64_cal >> runs/realizable_scaling/lottery_cdense.log 2>&1 || exit 5
$R lottery --workers 3 --out cdon400 --noext --cells rs_Cdon_400_64_cal >> runs/realizable_scaling/lottery_cdon400.log 2>&1 || exit 6
echo all > runs/realizable_scaling/batches.done
