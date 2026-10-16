#!/bin/zsh
# Counted cells (notes §1.5, §2.4). Sequential drivers, 3 workers each; resumable (rows already written are skipped).
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a0ddabfa59255b1cf
python3 src/annealed_run.py cells --runs 40 --out main --cells an_i_1600 an_iv_1600 an_iiiS_1600 an_i_800 an_iv_800 an_iiiS_800 an_i_400 an_iv_400 an_iiiS_400 an_i_200 an_iv_200 an_iiiS_200 || exit 1
python3 src/annealed_run.py cells --runs 40 --out partF --cells anF_AP_1600_K3 anF_DET_1600_K3 anF_AP_800_K3 anF_DET_800_K3 anF_AP_400_K3 anF_DET_400_K3 anF_AP_200_K3 anF_DET_200_K3 || exit 2
python3 src/annealed_run.py cells --runs 20 --out spon --cells an_ii_1600 an_iiiP_1600 an_ii_800 an_iiiP_800 an_ii_400 an_iiiP_400 an_ii_200 an_iiiP_200 || exit 3
python3 src/annealed_run.py cells --runs 20 --out k1 --cells an_i_800_K1 an_ii_800_K1 an_i_200_K1 an_ii_200_K1 anF_AP_800_K1 anF_DET_800_K1 anF_AP_200_K1 anF_DET_200_K1 an_iiiSnat_400 || exit 4
echo done > runs/annealed/cells.done
