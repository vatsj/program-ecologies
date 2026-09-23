# Spatial structure: death-birth Moran, pd, weak n=6 with ROLE (112 classes), w=0.3, burn-in 10000 generations, 300000 sampled (300000 at 128), 5 seeds

| graph | side | N | epsN | P(C,C) | P(exploit) | mean payoff | duty cycle | collapses | pre-collapse ALLC (mean ± sd) | THEM(^C) | ALLC | D | THEM(^D) | trace |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lattice | 128 | 16384 | 1 | 0.7567 ± 0.1182 | 0.0897 ± 0.0622 | -0.1984 ± 0.0909 | 0.5198 ± 0.2696 | 93 | 0.109 ± 0.092 | 0.4589 ± 0.2409 | 0.1901 ± 0.0443 | 0.1383 ± 0.0623 | 0.0022 ± 0.0014 | runs/spatial/trace_128_epsN1_mix128.png |

Snapshots: runs/spatial/snap_128_epsN1_seed5_mix128.png, runs/spatial/snap_128_epsN1_seed6_mix128.png, runs/spatial/snap_128_epsN1_seed7_mix128.png, runs/spatial/snap_128_epsN1_seed8_mix128.png, runs/spatial/snap_128_epsN1_seed9_mix128.png

| side | epsN | seed | P(C,C) | third 1: dominant class (share), P(C,C) | third 2 | third 3 |
|---|---|---|---|---|---|---|
| 128 | 1 | 5 | 0.679 | `THEM(^X)` (0.38), 0.36 | `THEM(^C)` (0.54), 0.78 | `THEM(^C)` (0.69), 0.90 |
| 128 | 1 | 6 | 0.690 | `D` (0.31), 0.50 | `C` (0.32), 0.70 | `THEM(^C)` (0.64), 0.86 |
| 128 | 1 | 7 | 0.955 | `THEM(^C)` (0.77), 0.93 | `THEM(^C)` (0.77), 0.97 | `THEM(^C)` (0.79), 0.96 |
| 128 | 1 | 8 | 0.826 | `THEM(^C)` (0.57), 0.69 | `THEM(^C)` (0.69), 0.81 | `THEM(^C)` (0.79), 0.98 |
| 128 | 1 | 9 | 0.634 | `THEM(^ROLE)` (0.27), 0.48 | `or(X,THEM(THEM))` (0.50), 0.63 | `THEM(^C)` (0.38), 0.79 |
