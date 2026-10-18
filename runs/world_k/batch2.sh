#!/bin/zsh
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a7781c6388595da18
until grep -q BATCH_DONE runs/world_k/batch.log; do sleep 60; done
python3 src/world_k_run.py cells --part D --workers 3 >> runs/world_k/cells_D.log 2>&1
echo BATCH2_DONE >> runs/world_k/batch2.log
