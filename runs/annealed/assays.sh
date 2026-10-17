#!/bin/zsh
# Single-arrival assays (notes §1.5, §2), run before any counted cell. Sequential drivers, 3 workers each.
cd /Users/jstav/code/program-ecologies/.claude/worktrees/agent-a0ddabfa59255b1cf
for N R in 200 10000 400 10000 800 20000 1600 40000; do
  python3 src/annealed_run.py neutral --N $N --sp C --reps $R --chunk 1000 --out neutral_C || exit 1
done
for N R in 200 5000 400 5000 800 10000 1600 20000; do
  python3 src/annealed_run.py neutral --N $N --sp 'if(CHK(them,^D,D),C,D)' --reps $R --chunk 1000 --out neutral_shadow || exit 2
done
for N in 200 400 800 1600; do
  for C in AP DET; do
    python3 src/annealed_run.py predator --N $N --cls $C --reps 400 --chunk 50 --out predator || exit 3
  done
done
echo done > runs/annealed/assays.done
