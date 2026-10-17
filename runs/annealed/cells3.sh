#!/bin/zsh
# The last batch of cells2.sh (its shell was stopped while one slow eps = 0 run held a worker): K = 1 cells and the
# native-r control, 2 workers while the sponsored driver finishes its last run.
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a0ddabfa59255b1cf
python3 src/annealed_run.py cells --runs 20 --out k1 --workers 2 --cells an_i_800_K1 an_ii_800_K1 an_i_200_K1 an_ii_200_K1 anF_AP_800_K1 anF_DET_800_K1 anF_AP_200_K1 anF_DET_200_K1 an_iiiSnat_400 || exit 4
while kill -0 30290 2>/dev/null; do sleep 30; done
echo done > runs/annealed/cells.done
