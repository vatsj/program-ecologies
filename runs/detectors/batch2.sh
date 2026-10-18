#!/bin/zsh
# Resume Part C (Cff_KGh_e0 closed at its finished replicates, notes §2.7) and the reference, then the post-hoc jobs.
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a896af328ecd32dc2
python3 src/detectors_run.py cells --part C --reps 20 --workers 3 --cap Cff_KGh_e0:0 > runs/detectors/cells_C2.log 2>&1 || exit 3
python3 src/detectors_run.py cells --part R --reps 20 --workers 3 > runs/detectors/cells_R.log 2>&1 || exit 4
python3 src/detectors_report.py posthoc > runs/detectors/posthoc.log 2>&1 || exit 5
echo done > runs/detectors/batch.done
