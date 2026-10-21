#!/bin/bash
# Hooks W2: all counted cells and the registered diagnostics, one batch at a time (3 workers each), then the report.
# Launch: nohup bash runs/hooks_w2/run_all.sh > runs/hooks_w2/run_all.log 2>&1 &
# Rows land in runs/hooks_w2/CELL.json and runs/hooks_w2/sog-CELL.json (resumable: a rerun skips finished runs).
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-ad03b37f615da20c7 || exit 1
echo "start $(date)"
python3 src/hooks_w2_run.py batch lineage-max,open-max,open-contract,open-history --procs 3 > runs/hooks_w2/batch_pd.log 2>&1
echo "pd done $(date)"
python3 src/hooks_w2_sog_run.py batch myopic-ref,union-M,union-C,bw-only-C,union-C-role --procs 3 > runs/hooks_w2/batch_sog.log 2>&1
echo "sog done $(date)"
python3 src/hooks_w2_run.py batch ff-lineage-max,ff-open-max --procs 3 > runs/hooks_w2/batch_ff.log 2>&1
echo "ff done $(date)"
python3 src/hooks_w2_run.py batch open-max-nocontract-strict,open-writes-only,open-grudge-only,open-thanks-only --procs 3 > runs/hooks_w2/batch_diag.log 2>&1
echo "diag done $(date)"
python3 src/hooks_w2_report.py > runs/hooks_w2/report.log 2>&1
echo "report done $(date)"
