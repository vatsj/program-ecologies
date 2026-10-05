# A path in (N, I, mN): independent nucleation and rival resolution (`src/island_path.py`)

Spec `specs/2026-10-05-island-path.md`; predictions `predictions/2026-10-05-island-path.md`. Modal arm, n = 9, PD, w = 0.3, ε = 0, iid length-prior seeds, complete island graph, generation = I·N births, horizon 10⁵ generations. Finite-horizon lottery and hazard results, not π. Every run is in every denominator; intervals are Wilson 95% over runs (islands within a run are not independent), exact Poisson for hazards, run-pair bootstrap for q.

## 0. Calibration, statics, validation

| N | nucleating islands (m = 0, I = 16, 120 runs) | p | T_nuc median [95%] | 5 / 25 / 75 / 95% | boundary mN |
|---|---|---|---|---|---|
| 100 | 166 / 1920 | 0.086 | 45 [40, 45] | 25 / 35 / 50 / 70 | 0.667 |
| 200 | 251 / 1920 | 0.131 | 55 [50, 55] | 35 / 45 / 65 / 85 | 1.091 |
| 400 | 344 / 1920 | 0.179 | 70 [65, 75] | 45 / 60 / 90 / 125 | 1.714 |

T_nuc ∝ N^0.32. Checks every 5 generations (the resolution of T_nuc).

**Statics** (exact formula; 10⁴ simulated runs per cell, 116 of 120 inside the 95% interval). P(fix) of k invaders arriving at once on one island:

| invader → resident | N | k = 1 | k = 10 | k = 30 | k = 60 |
|---|---|---|---|---|---|
| A → B3 | 100 | 1.85e-05 (0) | 0.000871 (8) | 0.0596 (572) | 0.782 (7813) |
| A → B3 | 200 | 7.22e-09 (0) | 3.66e-07 (0) | 6.05e-05 (0) | 0.014 (147) |
| A → B3 | 400 | 1.56e-15 (0) | 8.2e-14 (0) | 2.16e-11 (0) | 2.83e-08 (0) |
| B3 → A | 100 | 1.85e-05 (0) | 0.000871 (11) | 0.0596 (572) | 0.782 (7789) |
| B3 → A | 200 | 7.22e-09 (0) | 3.66e-07 (0) | 6.05e-05 (0) | 0.014 (124) |
| B3 → A | 400 | 1.56e-15 (0) | 8.2e-14 (0) | 2.16e-11 (0) | 2.83e-08 (0) |
| A → B1 | 100 | 1.85e-05 (0) | 0.000871 (9) | 0.0596 (601) | 0.782 (7885) |
| A → B1 | 200 | 7.22e-09 (0) | 3.66e-07 (0) | 6.05e-05 (0) | 0.014 (122) |
| A → B1 | 400 | 1.56e-15 (0) | 8.2e-14 (0) | 2.16e-11 (0) | 2.83e-08 (0) |
| bridge → A | 100 | 0.01 (81) | 0.1 (934) | 0.3 (3067) | 0.6 (5995) |
| bridge → A | 200 | 0.005 (53) | 0.05 (482) | 0.15 (1507) | 0.3 (3023) |
| bridge → A | 400 | 0.0025 (22) | 0.025 (254) | 0.075 (735) | 0.15 (1467) |
| A → bridge | 100 | 0.01 (114) | 0.1 (1009) | 0.3 (2957) | 0.6 (5913) |
| A → bridge | 200 | 0.005 (56) | 0.05 (527) | 0.15 (1557) | 0.3 (3030) |
| A → bridge | 400 | 0.0025 (22) | 0.025 (234) | 0.075 (743) | 0.15 (1428) |
| bridge → B1 | 100 | 0.01 (99) | 0.1 (1011) | 0.3 (2967) | 0.6 (6068) |
| bridge → B1 | 200 | 0.005 (52) | 0.05 (531) | 0.15 (1499) | 0.3 (3107) |
| bridge → B1 | 400 | 0.0025 (32) | 0.025 (262) | 0.075 (700) | 0.15 (1539) |
| B1 → bridge | 100 | 0.01 (108) | 0.1 (1005) | 0.3 (2996) | 0.6 (5928) |
| B1 → bridge | 200 | 0.005 (51) | 0.05 (507) | 0.15 (1518) | 0.3 (2980) |
| B1 → bridge | 400 | 0.0025 (16) | 0.025 (243) | 0.075 (773) | 0.15 (1517) |
| B3 → bridge | 100 | 0.269 (2689) | 0.962 (9595) | 1 (10000) | 1 (10000) |
| B3 → bridge | 200 | 0.264 (2598) | 0.957 (9544) | 1 (9998) | 1 (10000) |
| B3 → bridge | 400 | 0.262 (2537) | 0.954 (9512) | 1 (9999) | 1 (10000) |
| bridge → B3 | 100 | 7.71e-21 (0) | 3.56e-18 (0) | 2.18e-13 (0) | 3.48e-07 (0) |
| bridge → B3 | 200 | 2.17e-40 (0) | 1.03e-37 (0) | 1.03e-32 (0) | 1.05e-25 (0) |
| bridge → B3 | 400 | 1.76e-79 (0) | 8.48e-77 (0) | 1.08e-71 (0) | 2.81e-64 (0) |

(simulated fixations of 10⁴ in parentheses.) Classes: A = `BOX1(THEM(ME))`, B1 = `BOX1(THEM(^not(BOX(THEM(ME)))))`, B3 = `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))`, bridge = `BOX1(THEM(THEM))`. B3 → A equals A → B3 and B1 ↔ A equals B3 ↔ A (same symmetric coordination game).

**Validation.** k = 1 path draw-for-draw identical to the ca3cc7f kernel (48/48, `tests/check_rival_kernel_identity.py`). Against an unskipped reference with the same stopping rule (N = 50, I = 4, identical initial states, independent streams, 1,000 runs per side per cell): z-scores of kernel − reference:

| preset | pair | k | mN | gens | both-present ref / kern | z(both) | z(B count) | z(coop count) | z(n_est) | z(n_local) | z(P(C,C)) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AB | 2 | 1 | 1 | 1000 | 0.011 / 0.021 | 1.78 | -0.37 | -0.42 | 0.58 | -0.85 | -1.22 |
| AB | 2 | 1 | 3 | 100 | 0.054 / 0.069 | 1.40 | 0.84 | -0.74 | -1.29 | 0.45 | -0.79 |
| AB | 2 | 5 | 1 | 1000 | 0.004 / 0.004 | 0.00 | 1.09 | -0.90 | -0.82 | 1.64 | -0.93 |
| AB | 2 | 5 | 3 | 100 | 0.040 / 0.066 | 2.60 | 0.65 | 1.37 | 0.87 | -2.70 | -1.16 |
| AB | 2 | 10 | 1 | 1000 | 0.001 / 0.000 | -1.00 | 0.20 | -0.91 | -0.91 | -0.38 | -0.88 |
| AB | 2 | 10 | 3 | 100 | 0.046 / 0.041 | -0.55 | -0.95 | -0.53 | -1.34 | -0.86 | 0.26 |
| AB | 0 | 1 | 1 | 1000 | 0.010 / 0.016 | 1.18 | -0.32 | 1.86 | 1.47 | 0.21 | -0.52 |
| AB | 0 | 1 | 3 | 100 | 0.043 / 0.049 | 0.64 | 2.06 | 2.30 | 0.83 | 0.82 | 1.02 |
| AB | 0 | 5 | 1 | 1000 | 0.003 / 0.005 | 0.71 | -0.62 | -0.22 | -0.09 | 0.00 | 0.42 |
| AB | 0 | 5 | 3 | 100 | 0.035 / 0.035 | 0.00 | -0.84 | 1.36 | 0.76 | -0.54 | -0.26 |
| AB | 0 | 10 | 1 | 1000 | 0.001 / 0.000 | -1.00 | -0.15 | -2.20 | -1.45 | -0.28 | -1.09 |
| AB | 0 | 10 | 3 | 100 | 0.029 / 0.017 | -1.79 | -0.33 | 1.39 | 1.62 | -0.45 | 1.13 |
| iid | None | 1 | 1 | 1000 | 0.000 / 0.000 | 0.00 | 0.00 | 0.79 | 0.83 | 0.44 | 0.76 |
| iid | None | 1 | 3 | 100 | 0.000 / 0.000 | 0.00 | 0.00 | -0.25 | -0.23 | 0.61 | -0.27 |
| iid | None | 5 | 1 | 1000 | 0.000 / 0.000 | 0.00 | 0.00 | -1.05 | -1.08 | -1.19 | -1.00 |
| iid | None | 5 | 3 | 100 | 0.000 / 0.000 | 0.00 | 0.00 | 0.71 | 0.63 | -0.91 | 0.68 |
| iid | None | 10 | 1 | 1000 | 0.000 / 0.000 | 0.00 | 0.00 | -1.07 | -1.10 | -1.32 | -1.06 |
| iid | None | 10 | 3 | 100 | 0.000 / 0.000 | 0.00 | 0.00 | 0.70 | 0.73 | 0.94 | 0.74 |

max |z| = 2.70 over 117 nonzero statistics; 5 exceed 2 (≈ 5.3 expected under the null). Default kernel vs `seeds_in_n._run`: (100, 4, mN 1) efficient 0.285 vs 0.310 (600 runs each); (100, 16, mN 0.1) efficient 0.753 vs 0.807 (300 runs each).

## 1. The boundary path (pre-seeded A on island 0, B on island 1, rest iid; 40 runs per cell)

Both = A and B each hold ≥ 1 island at the horizon or stop (holder rule). Hazard = separation losses per minority-island-generation (exposure ∫ min(held_A, held_B) dt). Reference = mN·ρ_DD(N) per recipient island-generation. Invasions summed over runs (strong-holder changes; 2>1 = an island held by B taken by A; 2>3 by the bridge; 2>0 by an untagged class).

| pair | N | I | mN | both [95%] | A only | B only | neither | all islands one tag | B islands at end (mean) | losses / exposure | hazard [95%] | ref. mN·ρ_DD | KM S(10²/10³/10⁴/10⁵) | median loss gen | island P(C,C) | cf cross P(C,C) | worker-h |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P* | 100 | 16 | 0.667 | 0.10 [0.04, 0.23] | 29 | 7 | 0 | 36 | 3.3 | 36 / 6.2e+06 | 5.8e-06 [4.1e-06, 8e-06] | 1.2e-05 | 1.00 / 1.00 / 0.95 / 0.10 | 32750 | 0.999 ± 0.001 | 0.974 ± 0.028 | 0.02 |
| P* | 100 | 64 | 0.667 | 0.10 [0.04, 0.23] | 30 | 6 | 0 | 36 | 9.7 | 36 / 1.83e+07 | 2e-06 [1.4e-06, 2.7e-06] | 1.2e-05 | 1.00 / 1.00 / 1.00 / 0.10 | 50250 | 1.000 ± 0.000 | 0.996 ± 0.004 | 0.06 |
| P* | 200 | 16 | 1.091 | 1.00 [0.91, 1.00] | 0 | 0 | 0 | 0 | 5.8 | 0 / 1.91e+07 | 0 [0, 1.9e-07] | 7.9e-09 | 1.00 / 1.00 / 1.00 / 1.00 | – | 0.981 ± 0.003 | 0.619 ± 0.036 | 0.15 |
| P* | 200 | 64 | 1.091 | 1.00 [0.91, 1.00] | 0 | 0 | 0 | 0 | 20.4 | 0 / 7.56e+07 | 0 [0, 4.9e-08] | 7.9e-09 | 1.00 / 1.00 / 1.00 / 1.00 | – | 0.983 ± 0.002 | 0.614 ± 0.033 | 0.75 |
| P* | 400 | 16 | 1.714 | 1.00 [0.91, 1.00] | 0 | 0 | 0 | 0 | 6.4 | 0 / 1.96e+07 | 0 [0, 1.9e-07] | 2.7e-15 | 1.00 / 1.00 / 1.00 / 1.00 | – | 0.987 ± 0.002 | 0.612 ± 0.039 | 0.44 |
| P* | 400 | 64 | 1.714 | 1.00 [0.91, 1.00] | 0 | 0 | 0 | 0 | 16.9 | 0 / 6.65e+07 | 0 [0, 5.5e-08] | 2.7e-15 | 1.00 / 1.00 / 1.00 / 1.00 | – | 0.988 ± 0.001 | 0.646 ± 0.038 | 1.59 |
| bridge | 100 | 16 | 0.667 | 0.07 [0.03, 0.20] | 20 | 17 | 0 | 29 | 5.7 | 37 / 5.2e+06 | 7.1e-06 [5e-06, 9.8e-06] | 1.2e-05 | 0.95 / 0.80 / 0.67 / 0.07 | 34800 | 0.999 ± 0.001 | 0.989 ± 0.013 | 0.02 |
| bridge | 100 | 64 | 0.667 | 0.10 [0.04, 0.23] | 21 | 15 | 0 | 8 | 15.2 | 36 / 9.51e+06 | 3.8e-06 [2.7e-06, 5.2e-06] | 1.2e-05 | 0.95 / 0.80 / 0.30 / 0.10 | 1450 | 1.000 ± 0.000 | 0.995 ± 0.005 | 0.03 |
| bridge | 200 | 16 | 1.091 | 0.65 [0.50, 0.78] | 10 | 4 | 0 | 1 | 5.3 | 15 / 1.34e+07 | 1.1e-06 [6.3e-07, 1.9e-06] | 7.9e-09 | 0.95 / 0.67 / 0.62 / 0.62 | 455 | 0.987 ± 0.004 | 0.728 ± 0.066 | 0.12 |
| bridge | 200 | 64 | 1.091 | 0.15 [0.07, 0.29] | 23 | 11 | 0 | 3 | 8.4 | 34 / 1.18e+07 | 2.9e-06 [2e-06, 4e-06] | 7.9e-09 | 0.97 / 0.65 / 0.15 / 0.15 | 1128 | 0.998 ± 0.002 | 0.942 ± 0.045 | 0.13 |
| bridge | 400 | 16 | 1.714 | 0.50 [0.35, 0.65] | 9 | 7 | 4 | 5 | 5.1 | 22 / 1e+07 | 2.2e-06 [1.4e-06, 3.3e-06] | 2.7e-15 | 0.92 / 0.60 / 0.45 / 0.45 | 718 | 0.992 ± 0.003 | 0.788 ± 0.070 | 0.22 |
| bridge | 400 | 64 | 1.714 | 0.12 [0.05, 0.26] | 22 | 12 | 1 | 1 | 6.9 | 35 / 1.19e+07 | 2.9e-06 [2.1e-06, 4.1e-06] | 2.7e-15 | 0.97 / 0.72 / 0.12 / 0.12 | 1165 | 0.998 ± 0.002 | 0.945 ± 0.046 | 0.24 |

**Invasions by direction** (summed over the 40 runs of each cell):

| pair | N | I | 2>1 | 2>3 | 2>0 | 1>2 | 3>2 | 1>3 | 3>1 | 1>0 | 0>1 | 0>2 | 0>3 | B-island losses: replacement / absorption / capture |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P* | 100 | 16 | 225 | 0 | 0 | 115 | 0 | 0 | 0 | 2 | 309 | 187 | 0 | 225 / 0 / 0 |
| P* | 100 | 64 | 756 | 0 | 0 | 414 | 0 | 0 | 0 | 3 | 1636 | 673 | 0 | 756 / 0 / 0 |
| P* | 200 | 16 | 2 | 0 | 0 | 28 | 0 | 0 | 0 | 0 | 331 | 157 | 0 | 2 / 0 / 0 |
| P* | 200 | 64 | 10 | 0 | 0 | 199 | 0 | 0 | 0 | 11 | 1704 | 574 | 0 | 10 / 0 / 0 |
| P* | 400 | 16 | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 301 | 199 | 0 | – |
| P* | 400 | 64 | 0 | 0 | 0 | 98 | 0 | 0 | 0 | 20 | 1767 | 519 | 0 | – |
| bridge | 100 | 16 | 157 | 55 | 0 | 128 | 44 | 28 | 13 | 2 | 266 | 219 | 28 | 157 / 55 / 0 |
| bridge | 100 | 64 | 234 | 1223 | 1 | 499 | 871 | 1470 | 1092 | 1 | 1252 | 658 | 383 | 234 / 1223 / 1 |
| bridge | 200 | 16 | 5 | 63 | 6 | 15 | 18 | 53 | 24 | 2 | 253 | 191 | 45 | 5 / 63 / 6 |
| bridge | 200 | 64 | 16 | 852 | 39 | 149 | 412 | 1144 | 674 | 2 | 1229 | 621 | 448 | 16 / 852 / 39 |
| bridge | 400 | 16 | 2 | 68 | 6 | 15 | 27 | 78 | 13 | 0 | 259 | 190 | 56 | 2 / 68 / 6 |
| bridge | 400 | 64 | 11 | 684 | 44 | 148 | 156 | 737 | 227 | 0 | 1130 | 627 | 530 | 11 / 684 / 44 |

**q on the path** (iid ancestry-tagged runs vs the m = 0 reference with the same initial states):

| N | I | mN | x = mN·T_nuc/N | runs | q (holder form) [95%] | q_est (local establishment) [95%] | m = 0 local holders | island P(C,C) | cf cross P(C,C) | worker-h |
|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 16 | 0.667 | 0.30 | 120 | 0.90 [0.73, 1.12] | 0.92 [0.74, 1.14] | 166 | 0.783 ± 0.074 | 0.783 ± 0.074 | 0.00 |
| 100 | 64 | 0.667 | 0.30 | 40 | 0.86 [0.69, 1.04] | 0.89 [0.72, 1.07] | 221 | 0.975 ± 0.049 | 0.975 ± 0.049 | 0.00 |
| 200 | 16 | 1.091 | 0.30 | 120 | 0.90 [0.75, 1.06] | 0.90 [0.76, 1.06] | 251 | 0.875 ± 0.059 | 0.875 ± 0.059 | 0.00 |
| 200 | 64 | 1.091 | 0.30 | 40 | 0.83 [0.73, 0.95] | 0.84 [0.74, 0.94] | 358 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.00 |
| 400 | 16 | 1.714 | 0.30 | 120 | 0.97 [0.84, 1.12] | 0.97 [0.84, 1.12] | 344 | 0.958 ± 0.036 | 0.955 ± 0.036 | 0.02 |
| 400 | 64 | 1.714 | 0.30 | 40 | 0.82 [0.72, 0.92] | 0.84 [0.75, 0.93] | 482 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.01 |

## 3. Natural separation along the path (iid only)

Ever = two certified islands with mutually-defecting cooperative holders at some check; horizon = at the end. Bridge share = islands at the end held by classes mutually cooperating with both members of the first separated pair (ever-separated runs). Colonization time = first immigrant-founded establishment − first establishment; rival interval = first establishment of a holder mutually defecting with an earlier holder − first establishment.

| N | I | mN | runs | ever separated [95%] | horizon separated [95%] | separations surviving | bridge share (ever-sep. runs) | runs with a rival establishment | rival before first immigrant island | median colonization time | median rival interval | island P(C,C) | cf cross P(C,C) | worker-h |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 64 | 0.667 | 300 | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.01] | 0 / 2 | 0.11 | 2 | 1 / 2 | 25 | 28 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.02 |
| 100 | 256 | 0.667 | 300 | 0.03 [0.02, 0.06] | 0.00 [0.00, 0.01] | 0 / 10 | 0.29 | 10 | 3 / 10 | 20 | 20 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.14 |
| 200 | 64 | 1.091 | 300 | 0.01 [0.01, 0.03] | 0.00 [0.00, 0.01] | 0 / 4 | 0.70 | 4 | 2 / 4 | 32 | 48 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.04 |
| 200 | 256 | 1.091 | 100 | 0.01 [0.00, 0.05] | 0.00 [0.00, 0.04] | 0 / 1 | 0.80 | 1 | 0 / 1 | 20 | 40 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.05 |

Separated pairs (first separated pair in ever-separated runs; horizon pairs marked):

- (100, 64): BOX1(THEM(ME)) × BOX1(THEM(^not(BOX(THEM(THEM))))) (1); and(BOX1(THEM(ME)),not(BOX(THEM(ME)))) × BOX1(THEM(ME)) (1); at the horizon: none
- (100, 256): BOX1(THEM(ME)) × and(BOX(THEM(THEM)),BOXD1(THEM(^D))) (2); BOX(THEM(THEM)) × and(BOX1(THEM(ME)),not(BOX(THEM(ME)))) (2); BOX1(THEM(^BOX(THEM(THEM)))) × BOX1(THEM(^not(BOX(THEM(ME))))) (1); BOX(THEM(^BOX1(THEM(ME)))) × and(BOX1(THEM(ME)),not(BOX(THEM(ME)))) (1); BOX(THEM(ME)) × BOX1(THEM(^not(BOX(THEM(ME))))) (1); BOX1(THEM(ME)) × BOX1(THEM(^not(BOX(THEM(THEM))))) (1); BOX(THEM(ME)) × and(BOX1(THEM(ME)),not(BOX(THEM(ME)))) (1); BOX1(THEM(ME)) × BOX1(THEM(^not(BOX(THEM(ME))))) (1); at the horizon: none
- (200, 64): BOX1(THEM(ME)) × BOX1(THEM(^not(BOX(THEM(THEM))))) (2); BOX1(THEM(ME)) × BOX1(THEM(^not(BOX(THEM(ME))))) (1); BOX1(THEM(^not(BOX(THEM(ME))))) × BOX(THEM(ME)) (1); at the horizon: none
- (200, 256): BOX1(THEM(^not(BOX(THEM(ME))))) × BOX(THEM(ME)) (1); at the horizon: none

## 2. Propagule migration (I = 16, boundary flux mN, mN/k propagule events per island-generation; 40 runs per cell)

k = 1 rows are the path cells at I = 16 (same initial states). Reference = (mN/k)·P_k(N), P_k the static A → B probability for k at once.

| pair | N | k | k/N | both [95%] | A only | B only | B islands at end | losses / exposure | hazard [95%] | ref. (mN/k)·P_k | KM S(10²/10³/10⁴/10⁵) | 2>1 / 1>2 / 2>3 / 2>0 | island P(C,C) | cf cross P(C,C) | worker-h |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P* | 200 | 1 | 0.005 | 1.00 [0.91, 1.00] | 0 | 0 | 5.8 | 0 / 1.91e+07 | 0 [0, 1.9e-07] | 7.9e-09 | 1.00 / 1.00 / 1.00 / 1.00 | 2 / 28 / 0 / 0 | 0.981 ± 0.003 | 0.619 ± 0.036 | 0.15 |
| P* | 200 | 10 | 0.050 | 0.97 [0.87, 1.00] | 1 | 0 | 7.9 | 1 / 2e+07 | 5e-08 [1.3e-09, 2.8e-07] | 4e-08 | 1.00 / 1.00 / 1.00 / 0.97 | 11 / 28 / 0 / 0 | 0.980 ± 0.004 | 0.614 ± 0.038 | 0.10 |
| P* | 200 | 30 | 0.150 | 0.00 [0.00, 0.09] | 27 | 13 | 5.2 | 40 / 2.84e+06 | 1.4e-05 [1e-05, 1.9e-05] | 2.2e-06 | 1.00 / 0.95 / 0.72 / 0.00 | 120 / 115 / 0 / 0 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.01 |
| P* | 400 | 1 | 0.003 | 1.00 [0.91, 1.00] | 0 | 0 | 6.4 | 0 / 1.96e+07 | 0 [0, 1.9e-07] | 2.7e-15 | 1.00 / 1.00 / 1.00 / 1.00 | 0 / 7 / 0 / 0 | 0.987 ± 0.002 | 0.612 ± 0.039 | 0.44 |
| P* | 400 | 10 | 0.025 | 1.00 [0.91, 1.00] | 0 | 0 | 7.3 | 0 / 1.97e+07 | 0 [0, 1.9e-07] | 1.4e-14 | 1.00 / 1.00 / 1.00 / 1.00 | 0 / 15 / 0 / 0 | 0.985 ± 0.002 | 0.604 ± 0.034 | 0.45 |
| P* | 400 | 30 | 0.075 | 1.00 [0.91, 1.00] | 0 | 0 | 6.2 | 0 / 1.97e+07 | 0 [0, 1.9e-07] | 1.2e-12 | 1.00 / 1.00 / 1.00 / 1.00 | 0 / 25 / 0 / 0 | 0.985 ± 0.002 | 0.611 ± 0.036 | 0.22 |
| P* | 400 | 60 | 0.150 | 0.82 [0.68, 0.91] | 4 | 3 | 6.7 | 7 / 1.48e+07 | 4.7e-07 [1.9e-07, 9.7e-07] | 8.1e-10 | 1.00 / 1.00 / 0.97 / 0.82 | 42 / 78 / 0 / 0 | 0.990 ± 0.003 | 0.733 ± 0.054 | 0.12 |
| bridge | 200 | 1 | 0.005 | 0.65 [0.50, 0.78] | 10 | 4 | 5.3 | 15 / 1.34e+07 | 1.1e-06 [6.3e-07, 1.9e-06] | 7.9e-09 | 0.95 / 0.67 / 0.62 / 0.62 | 5 / 15 / 63 / 6 | 0.987 ± 0.004 | 0.728 ± 0.066 | 0.12 |
| bridge | 200 | 10 | 0.050 | 0.72 [0.57, 0.84] | 4 | 6 | 6.3 | 11 / 1.16e+07 | 9.5e-07 [4.7e-07, 1.7e-06] | 4e-08 | 0.95 / 0.80 / 0.75 / 0.72 | 10 / 32 / 44 / 10 | 0.989 ± 0.003 | 0.759 ± 0.055 | 0.07 |
| bridge | 200 | 30 | 0.150 | 0.00 [0.00, 0.09] | 28 | 11 | 3.5 | 40 / 2.2e+06 | 1.8e-05 [1.3e-05, 2.5e-05] | 2.2e-06 | 0.92 / 0.65 / 0.55 / 0.00 | 99 / 92 / 50 / 13 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.01 |
| bridge | 400 | 1 | 0.003 | 0.50 [0.35, 0.65] | 9 | 7 | 5.1 | 22 / 1e+07 | 2.2e-06 [1.4e-06, 3.3e-06] | 2.7e-15 | 0.92 / 0.60 / 0.45 / 0.45 | 2 / 15 / 68 / 6 | 0.992 ± 0.003 | 0.788 ± 0.070 | 0.22 |
| bridge | 400 | 10 | 0.025 | 0.40 [0.26, 0.55] | 12 | 10 | 4.8 | 24 / 9.33e+06 | 2.6e-06 [1.6e-06, 3.8e-06] | 1.4e-14 | 0.95 / 0.50 / 0.40 / 0.40 | 0 / 21 / 88 / 17 | 0.995 ± 0.002 | 0.825 ± 0.070 | 0.14 |
| bridge | 400 | 30 | 0.075 | 0.53 [0.37, 0.67] | 12 | 5 | 5.2 | 20 / 9.54e+06 | 2.1e-06 [1.3e-06, 3.2e-06] | 1.2e-12 | 0.95 / 0.70 / 0.50 / 0.50 | 3 / 34 / 78 / 12 | 0.990 ± 0.004 | 0.798 ± 0.065 | 0.10 |
| bridge | 400 | 60 | 0.150 | 0.42 [0.29, 0.58] | 12 | 9 | 4.7 | 23 / 7.18e+06 | 3.2e-06 [2e-06, 4.8e-06] | 8.1e-10 | 0.95 / 0.60 / 0.50 / 0.42 | 23 / 68 / 63 / 2 | 0.996 ± 0.002 | 0.866 ± 0.055 | 0.06 |

**q under propagules** (iid, I = 16, 120 runs per cell, paired m = 0 reference; Δq against k = 1 on the same initial states):

| N | k | q (holder form) [95%] | Δq vs k = 1 [95%] | q_est [95%] | island P(C,C) | cf cross P(C,C) |
|---|---|---|---|---|---|---|
| 200 | 1 | 0.90 [0.75, 1.06] | – | 0.90 [0.76, 1.06] | 0.875 ± 0.059 | 0.875 ± 0.059 |
| 200 | 10 | 0.82 [0.67, 1.00] | -0.08 [-0.24, +0.08] | 0.82 [0.68, 1.00] | 0.842 ± 0.066 | 0.840 ± 0.066 |
| 200 | 30 | 0.92 [0.78, 1.10] | +0.03 [-0.14, +0.19] | 0.93 [0.78, 1.10] | 0.917 ± 0.050 | 0.917 ± 0.050 |
| 400 | 1 | 0.97 [0.84, 1.12] | – | 0.97 [0.84, 1.12] | 0.958 ± 0.036 | 0.955 ± 0.036 |
| 400 | 10 | 0.94 [0.82, 1.09] | -0.03 [-0.16, +0.10] | 0.97 [0.85, 1.11] | 0.975 ± 0.028 | 0.975 ± 0.028 |
| 400 | 30 | 0.92 [0.82, 1.04] | -0.06 [-0.20, +0.08] | 0.92 [0.82, 1.04] | 0.967 ± 0.032 | 0.967 ± 0.032 |
| 400 | 60 | 0.88 [0.76, 1.02] | -0.10 [-0.23, +0.04] | 0.89 [0.77, 1.04] | 0.950 ± 0.039 | 0.949 ± 0.039 |

## 4. The bridge test (N = 100, I = 16, pair 1 tags; 40 runs per cell)

Shares are of the 16 islands at the horizon or stop (holder rule). Per-migrant invasion probability = strong-holder changes x → y-held / migrant individuals of tag x arriving on islands strongly held by y (static neutral value 1/N = 0.01).

| preset | mN | bridge share [95%] | A-net share | B share | bridge majority (> 8 islands) [95%] | bridge holds every island | B present at end | bridge share at 10² / 10³ / 10⁴ / 10⁵ | P(inv) bridge→A-held | A→bridge-held | bridge→B-held | B→bridge-held | island P(C,C) | cf cross P(C,C) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A, B, bridge | 0.1 | 0.442 ± 0.118 | 0.28 | 0.28 | 0.42 [0.29, 0.58] | 2 | 25 | 0.10 / 0.33 / 0.43 / 0.44 | 0.0104 (215/20612) | 0.0087 (177/20375) | 0.0105 (208/19854) | 0.0085 (165/19324) | 0.999 ± 0.001 | 0.916 ± 0.045 |
| A, A, bridge | 0.1 | 0.302 ± 0.069 | 0.70 | 0.00 | 0.15 [0.07, 0.29] | 0 | 0 | 0.10 / 0.27 / 0.30 / 0.30 | 0.0102 (64/6302) | 0.0110 (69/6250) | – | – | 1.000 ± 0.000 | 1.000 ± 0.000 |
| bridge alone | 0.1 | 0.519 ± 0.128 | 0.48 | 0.00 | 0.42 [0.29, 0.58] | 13 | 0 | 0.09 / 0.42 / 0.52 / 0.52 | 0.0096 (31/3234) | 0.0117 (38/3259) | – | – | 1.000 ± 0.000 | 1.000 ± 0.000 |
| A, B, bridge | 1 | 0.619 ± 0.103 | 0.23 | 0.15 | 0.65 [0.50, 0.78] | 6 | 16 | 0.26 / 0.62 / 0.62 / 0.62 | 0.0072 (149/20611) | 0.0035 (69/19791) | 0.0068 (135/19758) | 0.0033 (61/18295) | 1.000 ± 0.000 | 1.000 ± 0.000 |
| A, A, bridge | 1 | 0.295 ± 0.062 | 0.70 | 0.00 | 0.12 [0.05, 0.26] | 0 | 0 | 0.25 / 0.30 / 0.30 / 0.30 | 0.0019 (16/8443) | 0.0025 (17/6877) | – | – | 1.000 ± 0.000 | 1.000 ± 0.000 |
| bridge alone | 1 | 0.619 ± 0.111 | 0.38 | 0.00 | 0.57 [0.42, 0.71] | 11 | 0 | 0.36 / 0.62 / 0.62 / 0.62 | 0.0037 (18/4911) | 0.0036 (21/5759) | – | – | 1.000 ± 0.000 | 1.000 ± 0.000 |

## Merge test (N = 200 runs of cells 1–2 ending with both present; conditional on survival)

| source | merges | clean two-type | larger won (clean) | minority won (clean) | median gens to freeze | median larger share |
|---|---|---|---|---|---|---|
| path | 112 | 112 | 110 | 2 | 35 | 0.690 |
| prop | 68 | 68 | 65 | 3 | 30 | 0.747 |

## Bridge survival in pair-1 runs (added in analysis, not predeclared)

Every pair-1 run (path and propagule cells) that ends with both A and B present has lost the bridge class's last copy,
and early: median bridge extinction at generation 9–58, i.e. during the scramble. Runs ending both-present / runs with
the bridge extinct: (100, 16) 3 / 32; (100, 64) 4 / 12; (200, 16) 26 / 27; (200, 64) 6 / 9; (400, 16) 20 / 21;
(400, 64) 5 / 5 (40 runs per cell; at k = 10, 30, 60 on I = 16 the same pattern, 0 exceptions). A surviving bridge
absorbed B in every run in which it survived the scramble (2>3 is 63–1,223 events per cell against 2–234 replacements
2>1). At N = 100 coordination flips resolve rivals even without the bridge.

## Propagule stacking (added in analysis)

At (400, 60) the pair-3 hazard is 4.7·10⁻⁷ per minority-island-generation against the single-propagule reference
8.1·10⁻¹⁰ (×580); at (200, 30), 1.4·10⁻⁵ against 2.2·10⁻⁶ (×6). Two propagules arriving within the decay time of the
first act as one of size 2k: P(fix) from 120 of 400 at once is 9.6·10⁻⁴ (from 60, 2.8·10⁻⁸), from 60 of 200, 0.014.
Arrival intervals per island are k/mN = 35 generations at (400, 60) and 27 at (200, 30).

## Verdicts (predictions/2026-10-05-island-path.md)

| # | prediction | outcome |
|---|---|---|
| RE 1 | N = 100: both ≤ 0.2 (pair 1), ≤ 0.5 (pair 3); N = 200, 400: pair 3 both ≥ 0.8, hazard ≤ 10⁻⁵, q ≥ 0.75 | **Held.** N = 100: pair 1 0.07 / 0.10, pair 3 0.10 / 0.10 (I = 16 / 64). N ≥ 200 pair 3: 40/40 both in all four cells, 0 losses, hazard < 1.9·10⁻⁷ (upper 95%). q = 0.82–0.97 (lower bounds 0.69–0.84; within sampling error of 0.75 at (100, 64), (200, 16)). The headline "resolve only at N = 100" is wrong for pair 1, which resolves at N = 200 and 400 on I = 64 (both 0.15, 0.12) by bridge absorption; no clause covered it |
| RE 2 | both ≤ 0.3 at (200, 30) and (400, 60); ≥ 0.6 at (400, 30); abs(Δq) ≤ 0.3 | **Failed, falsifier fired** (within sampling error): (400, 60) pair 3 both 0.82 [0.68, 0.91] ≥ 0.7. Held: (200, 30) 0.00 [0, 0.09]; (400, 30) 1.00; max abs(Δq) 0.10. k/N is not the scaling variable: at k/N = 0.15 the static probability falls 2,000× from N = 200 to 400 |
| RE 3 | horizon separation < 0.05 at N = 100; grows with I at N = 200, ≥ 0.05 at (200, 256); colonization shorter than the rival interval at N = 100, not at N = 200 | **Failed, falsifier not fired.** Horizon separation 0 in all four cells (0/300, 0/300, 0/300, 0/100). Ever separated 2/300, 10/300 (N = 100); 4/300, 1/100 (N = 200), not growing with I at N = 200. Colonization vs rival interval: 25 vs 28 and 20 vs 20 at N = 100 (10 rival runs at I = 256: not shorter); N = 200 inconclusive (4 and 1 rival runs) |
| RE 4 | bridge share at mN = 1 above the bridge-alone control by ≥ 0.1; majority 0.3–0.6 at mN = 1, ≤ 0.3 at mN = 0.1 | **Failed, falsifier fired**: conflict share 0.619 = bridge-alone 0.619 (not above). Majority 0.65 [0.50, 0.78] at mN = 1 (gap) and 0.42 at mN = 0.1. Against the matched A, A, bridge control the conflict share is +0.32 (0.62 vs 0.30) at mN = 1 and +0.14 at mN = 0.1 |
| S1 | pair 1 both ≤ 0.2 in every path cell; replacement < 0.2 of B-island losses at N ≥ 200 | **Failed, falsifier fired** ((200, 16) both 0.65 ≥ 0.5; (400, 16) 0.50). The mechanism clause held: replacement is 2–16 of 70–910 B-island losses per cell at N ≥ 200, the rest absorption by the bridge (and 6–44 captures) |
| S2 | q ∈ [0.65, 0.95] in every path cell; the three N within 0.15 at each I | **Failed narrowly, falsifier not fired** ((400, 16) q = 0.97, within sampling error); agreement held (I = 16: 0.90 / 0.90 / 0.97; I = 64: 0.86 / 0.83 / 0.82) |
| S3 | pair 3 both ≥ 0.9 at N ≥ 200, B ≥ 3 islands, hazard ≤ 10⁻⁶ | **Held** (1.00; B holds 5.8–20.4 islands; 0 losses) |
| S4 | k/N-matched propagules do not resolve: pair 3 both ≥ 0.85 at every N = 400 cell, ≥ 0.6 at (200, 30); hazard within ×10 of (mN/k)·P_k | **Failed, falsifier not fired**: (200, 30) both 0.00; (400, 60) 0.82; hazard ×6 at (200, 30), ×580 at (400, 60) (stacking) |
| S5 | abs(Δq) ≤ 0.15 at matched flux | **Held** (−0.10 to +0.03; all intervals include 0) |
| S6 | horizon separation ≤ 0.05 at (200, 256), ever ∈ [0.01, 0.12]; more separations survive at N = 200; rival before the first immigrant island in ≥ 0.5 | **Failed, falsifier not fired.** First two clauses held (0/100; 1/100). No separation survived at either N (0/12, 0/5): every N = 200 rival in the sample had a bridge. Rival before the first immigrant-founded island 4/12 (N = 100) and 2/5 (N = 200) |
| S7 | conflict bridge share below bridge-alone, within ±0.15 of A, A, bridge; majority 0.2–0.5 | **Failed, falsifier fired** (conflict exceeds A, A, bridge by 0.32 ≥ 0.2; equal to bridge-alone, not below; majority 0.65 at mN = 1) |

