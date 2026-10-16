#!/bin/sh
# Budget step (notes §2.5): B1 restricted to the calibrated arm (the mN = 1 checkpoints already finished are kept as
# extra rows); the slowest checkpoint (rs_prop_400_64_cal 9, ~5,200 s per 10,000 generations at eps = 0) last; then B2.
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a4a0f6a7072bc2408
R="python3 src/removing_rivals_run.py"
L=runs/removing_rivals
CAL="rs_Snon_200_128_cal rs_Snon_200_64_cal rs_Snon_400_64_cal rs_abl_200_128_cal rs_abl_200_64_cal rs_abl_400_64_cal rs_prop_200_128_cal rs_prop_200_64_cal rs_prop_400_64_cal"
$R branch --workers 3 --out main --cells $CAL --skip rs_prop_400_64_cal:9 >> $L/branch.log 2>&1 || exit 6
$R lottery --workers 3 --out B --cells rr_rain001_200_64 rr_rain001_200_128 rr_rain01_200_64 rr_rain01_200_128 >> $L/lottery_B.log 2>&1 || exit 7
$R lottery --workers 3 --out B --cells rr_rain1_200_64 rr_rain1_200_128 >> $L/lottery_B.log 2>&1 || exit 8
$R branch --workers 1 --out main --cells rs_prop_400_64_cal >> $L/branch.log 2>&1 || exit 9
echo all > $L/batches.done
