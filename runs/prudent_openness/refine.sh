#!/bin/zsh
# Refinement of the second curve (notes §1.11): its 10,000 crossing fell between 2e-3 and 5e-3 (2.5x apart), so two
# points at the geometric thirds.  Waits for the panel.
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a41a30946fb51d29e
while pgrep -f "prudent_openness_run.py lottery" >/dev/null || pgrep -f "panel.sh" >/dev/null; do sleep 15; done
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
n=$(ps -eo command | grep -c "[s]og_realizable_run\|[f]ixed_role_chicken_run")
w=$((10 - n)); if [ $w -gt 3 ]; then w=3; fi; if [ $w -lt 1 ]; then w=1; fi
echo "workers $w"
python3 src/prudent_openness_run.py lottery --cells scanBm_0.002714 scanBm_0.003684 --runs 40 --workers $w --out main
echo "refine done"; date
