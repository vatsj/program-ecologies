#!/bin/zsh
# The scaling panel (notes §1.11): waits for the main lottery, then runs the bracketing scan points at three (N, I).
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a41a30946fb51d29e
while pgrep -f "prudent_openness_run.py lottery" >/dev/null; do sleep 15; done
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
n=$(ps -eo command | grep -c "[s]og_realizable_run\|[f]ixed_role_chicken_run")
w=$((10 - n)); if [ $w -gt 3 ]; then w=3; fi; if [ $w -lt 1 ]; then w=1; fi
echo "workers $w"
python3 src/prudent_openness_run.py lottery --cells scanA_3 scanA_4 --N 50 --I 64 --runs 40 --workers $w --out panel
python3 src/prudent_openness_run.py lottery --cells scanA_3 scanA_4 --N 100 --I 32 --runs 40 --workers $w --out panel
python3 src/prudent_openness_run.py lottery --cells scanA_3 scanA_4 --N 100 --I 128 --runs 40 --workers $w --out panel
echo "panel done"; date
