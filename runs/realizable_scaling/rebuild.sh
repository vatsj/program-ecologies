#!/bin/zsh
# Rebuild the untracked cached tables (milestone 5 static, provenance static/osv/sets) with the stored code;
# nothing new is computed. Tracked summary files overwritten by these commands are compared and restored afterwards.
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-abbd4be19f0352379
python3 src/lt_genes_run.py static --workers 3 > runs/realizable_scaling/rebuild_m5_static.log 2>&1 || exit 1
python3 src/provenance_run.py static --workers 3 > runs/realizable_scaling/rebuild_pv_static.log 2>&1 || exit 2
python3 src/provenance_run.py osv --workers 3 > runs/realizable_scaling/rebuild_pv_osv.log 2>&1 || exit 3
python3 src/provenance_run.py sets > runs/realizable_scaling/rebuild_pv_sets.log 2>&1 || exit 4
echo done > runs/realizable_scaling/rebuild.done
