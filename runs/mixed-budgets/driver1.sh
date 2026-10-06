#!/bin/sh
# priority order: homogeneous controls, then (a) cheap-heavy and above-threshold at the common mN
cd "$(dirname "$0")/../.."
python3 src/mixed_budgets.py run --exp hom --reps 300 --procs 3 > runs/mixed-budgets/hom.log 2>&1
python3 src/mixed_budgets.py run --exp nat --priors cheap above --reps 3000 --procs 3 > runs/mixed-budgets/nat.log 2>&1
echo done > runs/mixed-budgets/driver1.done
