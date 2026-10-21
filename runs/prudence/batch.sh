#!/bin/bash
# Prudence run: counted cells (replicates 0-19, spec) then the declared precision extension (replicates 20-39).
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a39ef5a00bf34e011
python3 -u src/prudence_run.py cells --reps 20 --out main --workers 3 > runs/prudence/main.log 2>&1
python3 -u src/prudence_run.py cells --rep0 20 --reps 20 --out ext --workers 3 > runs/prudence/ext.log 2>&1
echo done > runs/prudence/batch.done
