#!/bin/zsh
# Remaining batches of cells.sh (whose shell was stopped while one slow run of the first batch held a worker):
# Part F with 2 workers while the first driver finishes, then the rest with 3 once it has exited.
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a0ddabfa59255b1cf
python3 src/annealed_run.py cells --runs 40 --out partF --workers 2 --cells anF_AP_1600_K3 anF_DET_1600_K3 anF_AP_800_K3 anF_DET_800_K3 anF_AP_400_K3 anF_DET_400_K3 anF_AP_200_K3 anF_DET_200_K3 || exit 2
while kill -0 79786 2>/dev/null; do sleep 30; done
python3 src/annealed_run.py cells --runs 20 --out spon --cells an_ii_1600 an_iiiP_1600 an_ii_800 an_iiiP_800 an_ii_400 an_iiiP_400 an_ii_200 an_iiiP_200 || exit 3
python3 src/annealed_run.py cells --runs 20 --out k1 --cells an_i_800_K1 an_ii_800_K1 an_i_200_K1 an_ii_200_K1 anF_AP_800_K1 anF_DET_800_K1 anF_AP_200_K1 anF_DET_200_K1 an_iiiSnat_400 || exit 4
echo done > runs/annealed/cells.done
