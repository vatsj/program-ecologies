#!/bin/zsh
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a7781c6388595da18
for p in B D A C N; do
  python3 src/world_k_run.py cells --part $p --workers 3 >> runs/world_k/cells_$p.log 2>&1
done
echo BATCH_DONE >> runs/world_k/batch.log
