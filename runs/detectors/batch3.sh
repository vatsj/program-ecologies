#!/bin/zsh
# Part C's last job (Cff_KGs_e0 rep 6, after a pool stall: notes §2.7), the reference, then the post-hoc jobs.
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a896af328ecd32dc2
python3 src/detectors_run.py cells --part C --reps 20 --workers 1 --cap Cff_KGh_e0:0 > runs/detectors/cells_C3.log 2>&1 &
python3 src/detectors_run.py cells --part R --reps 20 --workers 2 > runs/detectors/cells_R.log 2>&1
wait
python3 src/detectors_report.py posthoc > runs/detectors/posthoc.log 2>&1 || exit 5
echo done > runs/detectors/batch.done
