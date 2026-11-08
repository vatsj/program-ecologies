#!/bin/bash
# Queue 76 step 2: R2 Monte Carlo from the prior (4 x 1.5e6 draws; the exhaustive part, s0 = 4, was run locally: runs/lt_prior_br/e_R2/enum_R2_s4_0of1.json).
cd "$(dirname "$0")/.."
mkdir -p runs/lt_prior_br/e_R2
for k in 0 1 2 3; do
  python3 src/lt_prior_br.py mc R2 1500000 $((300 + k)) runs/lt_prior_br/e_R2/mc_R2_$((300 + k)).json 4 > runs/lt_prior_br/e_R2/mc_$k.log 2>&1 &
done
wait
