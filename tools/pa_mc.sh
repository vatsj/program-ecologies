#!/bin/bash
# Queue 78 step 1: Monte Carlo from the prior with the extended members (59), 4 shards in parallel.  usage: bash tools/pa_mc.sh mcR1|mcR0
M=${1#mc}
OUT=runs/patient_accepter/$1
mkdir -p $OUT
if [ "$M" = "R1" ]; then N=1500000; else N=3000000; fi
for s in 0 1 2 3; do
  python3 src/patient_accepter_prior.py mc $M $N $((7800 + s)) $OUT/mc_${M}_$((7800 + s)).json 6 > $OUT/mc_$s.log 2>&1 &
done
wait
