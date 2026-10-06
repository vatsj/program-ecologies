#!/bin/zsh
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-acf58b05299993510
while pgrep -f "driver2.sh" > /dev/null; do sleep 15; done
python3 src/k_four.py posthoc --workers 3 > runs/k-four/posthoc.log 2>&1
echo DRIVER3 DONE >> runs/k-four/posthoc.log
