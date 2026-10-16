#!/bin/sh
# Remaining batches after the injection driver (pid 26897) ends (notes §2.4 order; batches.sh was stopped after B3
# to free a worker for a diagnostic replay, and the injection driver restarted with 2 workers; resumable).
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a4a0f6a7072bc2408
while kill -0 26897 2>/dev/null; do sleep 20; done
R="python3 src/removing_rivals_run.py"
L=runs/removing_rivals
$R triples --workers 3 >> $L/triples.log 2>&1 || exit 5
$R branch --workers 3 --out main >> $L/branch.log 2>&1 || exit 6
$R lottery --workers 3 --out B --cells rr_rain001_200_64 rr_rain001_200_128 rr_rain01_200_64 rr_rain01_200_128 >> $L/lottery_B.log 2>&1 || exit 7
$R lottery --workers 3 --out B --cells rr_rain1_200_64 rr_rain1_200_128 >> $L/lottery_B.log 2>&1 || exit 8
echo all > $L/batches.done
