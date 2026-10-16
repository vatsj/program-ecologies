#!/bin/sh
# The counted cells, in the order of notes §2 (one driver at a time, 3 workers). Resumable: each driver skips
# (cell, replicate) pairs already in its output file.
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-abbd4be19f0352379
R="python3 src/realizable_scaling_run.py"
$R lottery --workers 3 --out main --cells \
  rs_Snon_100_64_cal rs_Snon_200_64_cal rs_Snon_400_64_cal rs_Snon_100_128_cal rs_Snon_200_128_cal rs_Snon_100_256_cal \
  rs_prop_100_64_cal rs_prop_200_64_cal rs_prop_100_128_cal rs_prop_200_128_cal C >> runs/realizable_scaling/lottery_main.log 2>&1 || exit 1
$R lottery --workers 3 --out srest --cells \
  rs_Snon_50_64_m1 rs_Snon_50_64_cal rs_Snon_200_64_m1 rs_Snon_400_64_m1 rs_Snon_100_32_cal rs_Snon_50_32_m1 rs_Snon_50_32_cal rs_Snon_200_128_m1 \
  rs_abl_50_64_m1 rs_abl_50_64_cal rs_abl_100_64_cal rs_abl_200_64_m1 rs_abl_200_64_cal rs_abl_400_64_m1 rs_abl_400_64_cal \
  rs_abl_100_32_cal rs_abl_100_128_cal rs_abl_100_256_cal rs_abl_50_32_m1 rs_abl_50_32_cal rs_abl_200_128_m1 rs_abl_200_128_cal \
  rs_prop_50_64_cal rs_prop_400_64_cal rs_prop_100_32_cal rs_prop_100_256_cal rs_prop_50_32_cal >> runs/realizable_scaling/lottery_srest.log 2>&1 || exit 2
$R calib --runs 10 --gens 150 --workers 3 --cells rs_Cdon_400_64_m0 >> runs/realizable_scaling/calib_cdon.log 2>&1 || exit 3
$R lottery --workers 3 --out cdon --noext --cells \
  rs_Cdon_100_64_cal rs_Cdon_200_64_m1 rs_Cdon_200_64_cal rs_Cdon_400_64_m1 rs_Cdon_400_64_cal rs_Cdon_100_128_cal rs_Cdon_100_256_cal \
  rs_Cdon_50_64_m1 rs_Cdon_50_64_cal rs_Cdon_100_32_cal rs_Cdon_200_128_m1 rs_Cdon_200_128_cal rs_Cdon_50_32_m1 rs_Cdon_50_32_cal \
  >> runs/realizable_scaling/lottery_cdon.log 2>&1 || exit 4
$R lottery --workers 3 --out cdense --noext --cells D >> runs/realizable_scaling/lottery_cdense.log 2>&1 || exit 5
echo all > runs/realizable_scaling/batches.done
