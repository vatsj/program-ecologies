#!/bin/sh
# twin drift as a labelled intervention (spec item 4): twin-expanded stationary distribution at N = 1e4 and 1e5, and the
# untwinned re-solve at 1e5 for comparison; closure-seeded, log threshold 1e-14 (1e-20 for the modal dollar cell)
cd "$(dirname "$0")/../.."
for c in dollar3-norole dollar5-norole dollar3-role dollar5-role; do
  python3 src/solver_audit.py cell --cell $c --N 10000 100000 --theta 1e-14 --closure 6000 --twins --tag _final > runs/solver_audit/${c}_twins.log 2>&1
  python3 src/solver_audit.py cell --cell $c --N 100000 --theta 1e-14 --closure 6000 --tag _final > runs/solver_audit/${c}_1e5.log 2>&1
done
python3 src/solver_audit.py cell --cell modal-dollar7 --N 10000 100000 --theta 1e-20 --closure 6000 --twins --tag _final > runs/solver_audit/modal-dollar7_twins.log 2>&1
python3 src/solver_audit.py cell --cell modal-dollar7 --N 100000 --theta 1e-20 --closure 6000 --tag _final > runs/solver_audit/modal-dollar7_1e5.log 2>&1
