#!/bin/sh
# The counted cells in the order of notes §2.4 (one driver at a time, 3 workers). Resumable: each driver skips
# finished (cell, replicate) pairs.
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a4a0f6a7072bc2408
R="python3 src/removing_rivals_run.py"
L=runs/removing_rivals
$R lottery --workers 3 --out A --cells rr_spon_200_64 rr_spon_400_64 rr_spon_200_128 rr_spon_100_256 rr_pbe_200_64 rr_pbe_200_128 >> $L/lottery_A.log 2>&1 || exit 1
$R lottery --workers 3 --out base --cells rs_Snon_100_256_cal >> $L/lottery_base.log 2>&1 || exit 2
$R lottery --workers 3 --out B --cells rr_sponrain01_200_64 rr_sponrain01_200_128 >> $L/lottery_B.log 2>&1 || exit 3
$R inject --workers 3 >> $L/inject.log 2>&1 || exit 4
$R triples --workers 3 >> $L/triples.log 2>&1 || exit 5
$R branch --workers 3 --out main >> $L/branch.log 2>&1 || exit 6
$R lottery --workers 3 --out B --cells rr_rain001_200_64 rr_rain001_200_128 rr_rain01_200_64 rr_rain01_200_128 >> $L/lottery_B.log 2>&1 || exit 7
$R lottery --workers 3 --out B --cells rr_rain1_200_64 rr_rain1_200_128 >> $L/lottery_B.log 2>&1 || exit 8
echo all > $L/batches.done
