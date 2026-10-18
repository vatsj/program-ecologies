#!/bin/zsh
# Counted cells, in order (each driver uses <= 3 worker processes; resumable: finished rows are skipped).
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a896af328ecd32dc2
python3 src/detectors_run.py cells --part A --reps 100 --workers 3 > runs/detectors/cells_A.log 2>&1 || exit 1
python3 src/detectors_run.py cells --part B --reps 20 --workers 3 > runs/detectors/cells_B.log 2>&1 || exit 2
python3 src/detectors_run.py cells --part C --reps 20 --workers 3 > runs/detectors/cells_C.log 2>&1 || exit 3
python3 src/detectors_run.py cells --part R --reps 20 --workers 3 > runs/detectors/cells_R.log 2>&1 || exit 4
echo done > runs/detectors/batch.done
