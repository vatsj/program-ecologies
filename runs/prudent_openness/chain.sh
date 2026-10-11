#!/bin/zsh
# Part 3 (notes §1.12): waits for the lottery cells, then the panel baseline (added), then the reduced-support chain, twin drift on and off.
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a41a30946fb51d29e
while pgrep -f "prudent_openness_run.py lottery" >/dev/null || pgrep -f "panel.sh" >/dev/null || pgrep -f "refine.sh" >/dev/null; do sleep 15; done
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PO_MAX_STATES=4000
n=$(ps -eo command | grep -c "[s]og_realizable_run\|[f]ixed_role_chicken_run")
w=$((10 - n)); if [ $w -gt 3 ]; then w=3; fi; if [ $w -lt 1 ]; then w=1; fi
echo "workers $w"
# added after the panel, not preregistered: the clique-free baseline (m = 0) at the three panel (N, I)
python3 src/prudent_openness_run.py lottery --cells scanA_0 --N 50 --I 64 --runs 40 --workers $w --out panel
python3 src/prudent_openness_run.py lottery --cells scanA_0 --N 100 --I 32 --runs 40 --workers $w --out panel
python3 src/prudent_openness_run.py lottery --cells scanA_0 --N 100 --I 128 --runs 40 --workers $w --out panel
python3 src/prudent_openness_run.py chain --N 1000 10000 --theta 1e-8 --twins 1 0 --workers $w
echo "chain done"; date
