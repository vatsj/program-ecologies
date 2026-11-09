#!/bin/bash
# Queue 76 step 2: R2 exhaustive enumeration (s0 = 5, 4 shards) then Monte Carlo (4 x 1.5e6 draws) in one 4-CPU sandbox.
cd "$(dirname "$0")/.."
mkdir -p runs/lt_prior_br/e_R2
for k in 0 1 2 3; do
  python3 src/lt_prior_br.py enum R2 5 $k 4 runs/lt_prior_br/e_R2/enum_R2_s5_${k}of4.json > runs/lt_prior_br/e_R2/enum_$k.log 2>&1 &
done
wait
for k in 0 1 2 3; do
  python3 src/lt_prior_br.py mc R2 1500000 $((300 + k)) runs/lt_prior_br/e_R2/mc_R2_$((300 + k)).json 5 > runs/lt_prior_br/e_R2/mc_$k.log 2>&1 &
done
wait
