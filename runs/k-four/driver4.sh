#!/bin/zsh
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-acf58b05299993510
while pgrep -f "driver[23].sh" > /dev/null; do sleep 15; done
mv runs/k-four/misclass_n8_K16.json runs/k-four/misclass_n8_K16_v0.json
python3 src/k_four.py misclass --n 8 --label K@16 --also_tp --workers 3 > runs/k-four/misclass_n8.log 2>&1
echo DRIVER4 DONE >> runs/k-four/misclass_n8.log
