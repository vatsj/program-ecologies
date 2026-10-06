#!/bin/zsh
# Scaling panel, second launch (machine load ~28 on 10 cores): B1 cells to the spec's 40 runs, P* cells capped at 12.
cd "$(dirname "$0")/.."
python3 src/bridgeless_rivals.py run --exp scale --procs 3 --rival 'BOX1(THEM(^not(BOX(THEM(ME)))))' > runs/log_bridgeless_scale_b1.txt 2>&1 || echo "FAILED scale b1" >> runs/log_bridgeless_status.txt
echo "done scale b1 $(date)" >> runs/log_bridgeless_status.txt
python3 src/bridgeless_rivals.py run --exp scale --procs 3 --maxreps 12 --rival 'and(BOX1(THEM(ME)),not(BOX(THEM(ME))))' > runs/log_bridgeless_scale_pstar.txt 2>&1 || echo "FAILED scale pstar" >> runs/log_bridgeless_status.txt
echo "done scale pstar $(date)" >> runs/log_bridgeless_status.txt
