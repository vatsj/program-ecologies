#!/bin/zsh
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-acf58b05299993510
while pgrep -f "driver1.sh" > /dev/null; do sleep 15; done
python3 src/k_four.py classify --n 8 --labels K@16 K4m@16 --workers 3 > runs/k-four/classify_n8b.log 2>&1
python3 src/k_four.py misclass --n 8 --label K@16 --also_tp --workers 3 > runs/k-four/misclass_n8.log 2>&1
python3 src/k_four.py partc --b 16 --workers 3 > runs/k-four/partc.log 2>&1
python3 src/k_four.py n6res > runs/k-four/n6res.log 2>&1
python3 src/k_four.py classify --n 6 --labels K@16 K4m@16 --workers 3 > runs/k-four/classify_n6.log 2>&1
python3 src/k_four.py lottery --b 16 --workers 3 > runs/k-four/lottery.log 2>&1
python3 src/k_four.py catalogue --budgets 4 16 --workers 1 > runs/k-four/catalogue.log 2>&1
python3 src/k_four.py ktables --n 8 --four K --goff 1 --budgets 16 54 --workers 2 > runs/k-four/ktables_g1.log 2>&1
python3 src/k_four.py ktables --n 8 --four mono --goff 1 --budgets 16 54 --workers 2 >> runs/k-four/ktables_g1.log 2>&1
python3 src/k_four.py static --n 8 --goff 1 --budgets 16 54 > runs/k-four/static_g1.log 2>&1
python3 src/k_four.py chain --budgets 16 --Ns 10000 --goff 1 --workers 2 > runs/k-four/chain_g1.log 2>&1
echo DRIVER2 DONE >> runs/k-four/chain_g1.log
