#!/bin/zsh
# sequential driver (<= 3 workers at any time)
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-acf58b05299993510
while pgrep -f "k_four.py ktables --n 8 --four mono" > /dev/null; do sleep 15; done
python3 src/k_four.py ktables --n 6 --four mono --budgets 4 16 40 --workers 3 > runs/k-four/ktables_n6.log 2>&1
python3 src/k_four.py ktables --n 6 --four lit --budgets 4 16 40 --workers 3 >> runs/k-four/ktables_n6.log 2>&1
python3 src/k_four.py ktables --n 6 --four K --budgets 4 16 40 --workers 3 >> runs/k-four/ktables_n6.log 2>&1
python3 src/k_four.py static --n 6 --budgets 4 16 40 > runs/k-four/static_n6.log 2>&1
python3 src/k_four.py static --n 8 --budgets 4 8 12 16 24 32 54 > runs/k-four/static_n8.log 2>&1
python3 src/k_four.py chain --budgets 16 54 --workers 3 > runs/k-four/chain.log 2>&1
python3 src/k_four.py sweep --configs K/0 mono/0 K/1 mono/1 --workers 3 > runs/k-four/sweep.log 2>&1
python3 src/k_four.py ktables --n 8 --four lit --budgets 16 54 --workers 2 > runs/k-four/ktables_lit.log 2>&1
echo DRIVER1 DONE >> runs/k-four/chain.log
