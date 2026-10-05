# Almost all seeds: cutoff sensitivity in n (2026-10-05)

Spec `specs/2026-10-05-seeds-in-n.md`; predictions `predictions/2026-10-05-seeds-in-n.md` (committed before the runs); code `src/seeds_in_n.py`, `src/seeds_in_n_report.py`. Modal arm (all box kinds), PD, w = 0.3, ε = 0, iid seeding from the length prior at cutoff n, complete island graph, mN = 1 (a generation = I·N births), checks every 20 generations, common generation budget 10⁵ in every cell. Paired RNG seeds across n (the multinomial draw differs, so intervals are unpaired). Wilson 95% intervals throughout. Raw rows: `runs/seeds-in-n.json`.

## Static prior masses

| n | classes | μ(ALLC) | μ(D) | μ(self-cooperators) | μ(core = unfakeable) | μ(FairBot) | μ(fakeable self-coop) | μ(D-entering self-coop) | core classes / self-cooperators |
|---|---|---|---|---|---|---|---|---|---|
| 6 | 51 | 0.469 | 0.469 | 0.0284 | 0.0149 | 0.0050 | 0.0135 | 0.0229 | 3 / 17 |
| 7 | 172 | 0.468 | 0.468 | 0.0297 | 0.0102 | 0.0051 | 0.0196 | 0.0238 | 5 / 78 |
| 8 | 471 | 0.466 | 0.466 | 0.0306 | 0.0102 | 0.0051 | 0.0204 | 0.0242 | 9 / 236 |
| 9 | 863 | 0.466 | 0.466 | 0.0313 | 0.0104 | 0.0051 | 0.0210 | 0.0246 | 13 / 404 |

D-entering = a self-cooperator whose single copy fixes on an all-D island of 100 with probability > 10⁻³ (all of them have ρ = 0.0421 there).

## Censoring

Administrative censoring (cells stopped for time): none. Dynamically unresolved runs (reached 10⁵ generations without certification): 1 of 1920. Largest single-run wall time 63.9 s; total run exposure 586040 generations.

## Per-island chance p(N, n) (no-migration control, 100 runs × 4 islands per cell)

| n | N | islands | efficient [95%] | defecting | other | not frozen | P(eff \| no core seed) | P(eff \| ≥ 1 core seed) | islands with ≥ 1 core seed |
|---|---|---|---|---|---|---|---|---|---|
| 6 | 100 | 400 | 0.083 [0.059, 0.114] | 0.917 | 0.000 | 0 runs | 0.03 [0.01, 0.09] | 0.10 [0.07, 0.14] | 0.76 |
| 6 | 400 | 400 | 0.158 [0.125, 0.196] | 0.843 | 0.000 | 0 runs | - | 0.16 [0.13, 0.20] | 1.00 |
| 6 | 1600 | 400 | 0.383 [0.336, 0.431] | 0.618 | 0.000 | 0 runs | - | 0.38 [0.34, 0.43] | 1.00 |
| 7 | 100 | 400 | 0.090 [0.066, 0.122] | 0.910 | 0.000 | 0 runs | 0.06 [0.03, 0.11] | 0.11 [0.08, 0.15] | 0.62 |
| 7 | 400 | 400 | 0.198 [0.161, 0.239] | 0.802 | 0.000 | 0 runs | 0.14 [0.03, 0.51] | 0.20 [0.16, 0.24] | 0.98 |
| 7 | 1600 | 400 | 0.427 [0.380, 0.476] | 0.573 | 0.000 | 0 runs | - | 0.43 [0.38, 0.48] | 1.00 |
| 8 | 100 | 400 | 0.092 [0.068, 0.125] | 0.907 | 0.000 | 0 runs | 0.07 [0.03, 0.12] | 0.10 [0.07, 0.15] | 0.69 |
| 8 | 400 | 400 | 0.195 [0.159, 0.237] | 0.805 | 0.000 | 0 runs | 0.00 [0.00, 0.35] | 0.20 [0.16, 0.24] | 0.98 |
| 8 | 1600 | 400 | 0.427 [0.380, 0.476] | 0.573 | 0.000 | 0 runs | - | 0.43 [0.38, 0.48] | 1.00 |
| 9 | 100 | 400 | 0.090 [0.066, 0.122] | 0.910 | 0.000 | 0 runs | 0.06 [0.03, 0.11] | 0.11 [0.08, 0.15] | 0.65 |
| 9 | 400 | 400 | 0.185 [0.150, 0.226] | 0.812 | 0.003 | 1 runs | 0.25 [0.07, 0.59] | 0.18 [0.15, 0.23] | 0.98 |
| 9 | 1600 | 400 | 0.412 [0.365, 0.461] | 0.588 | 0.000 | 0 runs | - | 0.41 [0.37, 0.46] | 1.00 |

Predictor p ≈ a·μ·√N. Fits through the origin; residual = (observed − predicted)/predicted; "in CI" = the prediction lies in the observed Wilson interval.

| μ used | fit on | a | n=6 N=100 | n=6 N=400 | n=6 N=1600 | n=7 N=100 | n=7 N=400 | n=7 N=1600 | n=8 N=100 | n=8 N=400 | n=8 N=1600 | n=9 N=100 | n=9 N=400 | n=9 N=1600 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| μ_core | p(100, 6) | 0.555 | +0% | -5% | +16% (out) | +59% (out) | +75% (out) | +89% (out) | +63% (out) | +71% (out) | +88% (out) | +57% (out) | +61% (out) | +79% (out) |
| μ_core | n = 6, all N | 0.618 | -10% | -14% | +4% | +43% (out) | +57% (out) | +70% (out) | +46% (out) | +54% (out) | +69% (out) | +41% (out) | +45% (out) | +61% (out) |
| μ_est | p(100, 6) | 0.361 | +0% | -5% | +16% (out) | +5% | +15% | +25% (out) | +6% | +12% | +22% (out) | +1% | +4% | +16% (out) |
| μ_est | n = 6, all N | 0.401 | -10% | -14% | +4% | -6% | +3% | +12% | -5% | +0% | +10% | -9% | -6% | +4% |

Slope of log p on log N (N = 100, 400, 1,600): n = 6: 0.55; n = 7: 0.56; n = 8: 0.55; n = 9: 0.55.

Mean absolute relative residual at n = 7–9 (a fitted on p(100, 6)): μ_core 71%, μ_est 12%.

## Run-level outcomes with migration (mN = 1)

CF / CS / MS / UN = certified frozen / certified separated / metastable / unresolved. Predicted = 1 − (1 − p(N, n))^I with the measured per-island p.

| n | N | I | runs | CF / CS / MS / UN | efficient / defecting / other | efficient fraction [95%] | predicted 1−(1−p)^I | median freeze gen | median first certified coop island | median first certified core island | mean final P(C,C) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 100 | 4 | 20 | 20 / 0 / 0 / 0 | 7 / 13 / 0 | 0.35 [0.18, 0.57] | 0.29 | 40 | 80 (7 runs) | 120 (4 runs) | 0.350 |
| 7 | 100 | 4 | 20 | 20 / 0 / 0 / 0 | 5 / 15 / 0 | 0.25 [0.11, 0.47] | 0.31 | 40 | 80 (5 runs) | 100 (2 runs) | 0.250 |
| 8 | 100 | 4 | 20 | 20 / 0 / 0 / 0 | 5 / 15 / 0 | 0.25 [0.11, 0.47] | 0.32 | 40 | 40 (5 runs) | 50 (2 runs) | 0.250 |
| 9 | 100 | 4 | 20 | 20 / 0 / 0 / 0 | 4 / 16 / 0 | 0.20 [0.08, 0.42] | 0.31 | 40 | 50 (4 runs) | 100 (1 runs) | 0.200 |
| 6 | 400 | 4 | 20 | 20 / 0 / 0 / 0 | 7 / 13 / 0 | 0.35 [0.18, 0.57] | 0.50 | 60 | 80 (7 runs) | 140 (5 runs) | 0.350 |
| 7 | 400 | 4 | 20 | 20 / 0 / 0 / 0 | 8 / 12 / 0 | 0.40 [0.22, 0.61] | 0.59 | 70 | 130 (8 runs) | 90 (4 runs) | 0.400 |
| 8 | 400 | 4 | 20 | 20 / 0 / 0 / 0 | 11 / 9 / 0 | 0.55 [0.34, 0.74] | 0.58 | 190 | 160 (11 runs) | 170 (6 runs) | 0.550 |
| 9 | 400 | 4 | 20 | 20 / 0 / 0 / 0 | 8 / 12 / 0 | 0.40 [0.22, 0.61] | 0.56 | 60 | 130 (8 runs) | 160 (3 runs) | 0.400 |
| 6 | 1600 | 4 | 40 | 40 / 0 / 0 / 0 | 31 / 9 / 0 | 0.78 [0.62, 0.88] | 0.85 | 360 | 160 (31 runs) | 200 (22 runs) | 0.775 |
| 7 | 1600 | 4 | 40 | 40 / 0 / 0 / 0 | 34 / 6 / 0 | 0.85 [0.71, 0.93] | 0.89 | 320 | 160 (34 runs) | 160 (13 runs) | 0.850 |
| 8 | 1600 | 4 | 40 | 40 / 0 / 0 / 0 | 34 / 6 / 0 | 0.85 [0.71, 0.93] | 0.89 | 330 | 140 (34 runs) | 260 (13 runs) | 0.850 |
| 9 | 1600 | 4 | 40 | 40 / 0 / 0 / 0 | 32 / 8 / 0 | 0.80 [0.65, 0.90] | 0.88 | 320 | 150 (32 runs) | 180 (12 runs) | 0.800 |
| 6 | 100 | 64 | 20 | 20 / 0 / 0 / 0 | 20 / 0 / 0 | 1.00 [0.84, 1.00] | 1.00 | 250 | 60 (20 runs) | 60 (19 runs) | 1.000 |
| 7 | 100 | 64 | 20 | 20 / 0 / 0 / 0 | 20 / 0 / 0 | 1.00 [0.84, 1.00] | 1.00 | 250 | 60 (20 runs) | 80 (17 runs) | 1.000 |
| 8 | 100 | 64 | 20 | 20 / 0 / 0 / 0 | 20 / 0 / 0 | 1.00 [0.84, 1.00] | 1.00 | 250 | 60 (20 runs) | 90 (18 runs) | 1.000 |
| 9 | 100 | 64 | 20 | 20 / 0 / 0 / 0 | 20 / 0 / 0 | 1.00 [0.84, 1.00] | 1.00 | 260 | 60 (20 runs) | 80 (20 runs) | 1.000 |
| 6 | 100 | 256 | 40 | 40 / 0 / 0 / 0 | 40 / 0 / 0 | 1.00 [0.91, 1.00] | 1.00 | 280 | 40 (40 runs) | 40 (40 runs) | 1.000 |
| 7 | 100 | 256 | 40 | 40 / 0 / 0 / 0 | 40 / 0 / 0 | 1.00 [0.91, 1.00] | 1.00 | 280 | 40 (40 runs) | 60 (40 runs) | 1.000 |
| 8 | 100 | 256 | 40 | 40 / 0 / 0 / 0 | 40 / 0 / 0 | 1.00 [0.91, 1.00] | 1.00 | 280 | 40 (40 runs) | 60 (40 runs) | 1.000 |
| 9 | 100 | 256 | 40 | 38 / 2 / 0 / 0 | 40 / 0 / 0 | 1.00 [0.91, 1.00] | 1.00 | 280 | 40 (40 runs) | 40 (40 runs) | 1.000 |
| 6 | 400 | 16 | 20 | 20 / 0 / 0 / 0 | 18 / 2 / 0 | 0.90 [0.70, 0.97] | 0.94 | 370 | 100 (18 runs) | 120 (16 runs) | 0.900 |
| 7 | 400 | 16 | 20 | 20 / 0 / 0 / 0 | 18 / 2 / 0 | 0.90 [0.70, 0.97] | 0.97 | 360 | 100 (18 runs) | 100 (16 runs) | 0.900 |
| 8 | 400 | 16 | 20 | 20 / 0 / 0 / 0 | 20 / 0 / 0 | 1.00 [0.84, 1.00] | 0.97 | 360 | 100 (20 runs) | 120 (11 runs) | 1.000 |
| 9 | 400 | 16 | 20 | 20 / 0 / 0 / 0 | 19 / 1 / 0 | 0.95 [0.76, 0.99] | 0.96 | 360 | 100 (19 runs) | 140 (9 runs) | 0.950 |

Pooled over n = 6–9 (predicted interval from the Wilson interval of the pooled p): (100, 4): observed 0.26 [0.18, 0.37], predicted 0.31 [0.27, 0.35]; (400, 4): observed 0.42 [0.32, 0.53], predicted 0.56 [0.52, 0.60]; (1600, 4): observed 0.82 [0.75, 0.87], predicted 0.88 [0.86, 0.90]; (400, 16): observed 0.94 [0.86, 0.97], predicted 0.96 [0.94, 0.97].

Outcome conditioned on the seed (I = 4 cells, pooled over n): efficient fraction by the number of islands seeded with ≥ 1 core program.

| N | 0 islands | 1 | 2 | 3–4 |
|---|---|---|---|---|
| 100 | 0/1 | 3/13 | 4/20 | 14/46 |
| 400 | - | - | - | 34/80 |
| 1600 | - | - | - | 131/160 |

Core programs alive (summed over islands) at global ALLC extinction, efficient vs defecting runs, I = 4 (pooled over n): N = 100: efficient median 0, defecting median 0, defecting runs with 0 core left 54/59; N = 400: efficient median 35, defecting median 0, defecting runs with 0 core left 15/46; N = 1600: efficient median 77, defecting median 26, defecting runs with 0 core left 0/29 (the last count uses all self-cooperators).

## Nucleation-then-spread control, (100, 64), migration off for the first 2,000 generations

| n | runs | certified coop islands at switch: mean [min, max] | of which core-only: mean | frozen non-coop islands: mean | unfrozen islands at switch: mean | runs with 0 certified coop islands | efficient after [95%] | P(eff \| ≥ 1 certified coop island) | predicted P(≥ 1) = 1−(1−p)^64 | median stop gen |
|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 40 | 5.4 [2, 9] | 3.3 | 58.6 | 0.0 | 0 (+0 stopped before the switch: -) | 1.00 [0.91, 1.00] | 1.00 [0.91, 1.00] | 0.996 | 2230 |
| 9 | 40 | 5.7 [2, 9] | 2.5 | 58.3 | 0.0 | 0 (+0 stopped before the switch: -) | 1.00 [0.91, 1.00] | 1.00 [0.91, 1.00] | 0.998 | 2220 |

Per-island establishment by the switch (certified coop islands / 64) against the no-migration p(100, n): n = 6: 0.084 vs 0.083; n = 9: 0.089 vs 0.090.

## Cooperative islands lost (≥ 90% → < 50% self-cooperators), mN = 1 cells

| n | losses before / after global ALLC extinction | per run (after) [runs] | held by core / fakeable self-coop (after) | strict invasions of monomorphic islands (core-held) | neutral replacements | against selection | mixed-island displacements | runs with losses: efficient |
|---|---|---|---|---|---|---|---|---|
| 6 | 2 / 25 | 0.156 [160] | 3 / 22 | 1 (0) | 0 | 0 | 26 | 1.00 [0.77, 1.00] |
| 7 | 5 / 173 | 1.081 [160] | 5 / 168 | 10 (0) | 0 | 0 | 168 | 1.00 [0.80, 1.00] |
| 8 | 4 / 113 | 0.706 [160] | 3 / 110 | 15 (0) | 0 | 0 | 102 | 1.00 [0.82, 1.00] |
| 9 | 4 / 75 | 0.469 [160] | 1 / 74 | 7 (0) | 0 | 0 | 72 | 1.00 [0.74, 1.00] |

Held class → taker, after global ALLC extinction (all n; count by n = 6/7/8/9):

| held | taker | mechanism | held class | n = 6 / 7 / 8 / 9 |
|---|---|---|---|---|
| `BOX1(THEM(^C))` | `BOX(THEM(^D))` | displacement from a mixed island | fakeable | 4 / 99 / 31 / 23 |
| `BOX(THEM(^C))` | `BOX(THEM(^D))` | displacement from a mixed island | fakeable | 9 / 43 / 14 / 9 |
| `BOX1(THEM(^C))` | `BOX1(THEM(^D))` | displacement from a mixed island | fakeable | 3 / 11 / 25 / 4 |
| `BOX(THEM(^C))` | `BOX1(THEM(^D))` | displacement from a mixed island | fakeable | 5 / 3 / 14 / 9 |
| `BOX1(THEM(^C))` | `BOX(THEM(^D))` | strict invasion of a monomorphic island | fakeable | 0 / 7 / 5 / 3 |
| `BOX(THEM(^C))` | `BOX1(THEM(^BOXD1(THEM(^C))))` | displacement from a mixed island | fakeable | 0 / 0 / 0 / 12 |
| `BOX1(THEM(^C))` | `BOX1(THEM(^D))` | strict invasion of a monomorphic island | fakeable | 0 / 1 / 8 / 0 |
| `BOX1(THEM(^C))` | `BOX1(THEM(^BOXD1(THEM(^C))))` | displacement from a mixed island | fakeable | 0 / 0 / 0 / 8 |
| `BOX1(THEM(ME))` | `BOX(THEM(^D))` | displacement from a mixed island | core | 1 / 2 / 2 / 1 |
| `BOX(THEM(ME))` | `BOX(THEM(^D))` | displacement from a mixed island | core | 1 / 3 / 0 / 0 |
| `BOX(THEM(^C))` | `BOX1(THEM(^D))` | strict invasion of a monomorphic island | fakeable | 1 / 1 / 1 / 0 |
| `BOX1(THEM(THEM))` | `BOX1(THEM(^D))` | displacement from a mixed island | fakeable | 0 / 1 / 2 / 0 |
| `BOX(THEM(^C))` | `BOX(THEM(^D))` | strict invasion of a monomorphic island | fakeable | 0 / 1 / 0 / 2 |
| `BOX(THEM(^C))` | `BOX1(THEM(^BOXD1(THEM(ME))))` | displacement from a mixed island | fakeable | 0 / 0 / 3 / 0 |
| `BOX(THEM(^C))` | `BOX(THEM(^BOXD(THEM(THEM))))` | displacement from a mixed island | fakeable | 0 / 0 / 2 / 0 |
| `BOX1(THEM(THEM))` | `BOX(THEM(^D))` | displacement from a mixed island | fakeable | 0 / 0 / 2 / 0 |
| `BOX(THEM(^C))` | `BOX(THEM(^not(BOX1(THEM(ME)))))` | displacement from a mixed island | fakeable | 0 / 0 / 0 / 2 |
| `BOX(THEM(ME))` | `D` | displacement from a mixed island | core | 1 / 0 / 0 / 0 |
| `BOX(THEM(THEM))` | `BOX(THEM(^D))` | displacement from a mixed island | fakeable | 0 / 1 / 0 / 0 |
| `BOX(THEM(ME))` | `BOX1(THEM(^D))` | displacement from a mixed island | core | 0 / 0 / 1 / 0 |
| `BOX(THEM(^C))` | `BOX(THEM(^BOXD(THEM(THEM))))` | strict invasion of a monomorphic island | fakeable | 0 / 0 / 1 / 0 |
| `BOX1(THEM(^C))` | `BOX(THEM(^BOXD1(THEM(THEM))))` | displacement from a mixed island | fakeable | 0 / 0 / 1 / 0 |
| `BOX1(THEM(THEM))` | `BOX1(THEM(^BOXD1(THEM(ME))))` | displacement from a mixed island | fakeable | 0 / 0 / 1 / 0 |
| `BOX1(THEM(^C))` | `BOX1(THEM(^BOXD1(THEM(^C))))` | strict invasion of a monomorphic island | fakeable | 0 / 0 / 0 / 1 |
| `BOX(THEM(^C))` | `BOX1(THEM(^BOXD1(THEM(^C))))` | strict invasion of a monomorphic island | fakeable | 0 / 0 / 0 / 1 |

Before global ALLC extinction (all n): `BOX(THEM(^C))` → `BOX(THEM(^D))` (displacement from a mixed island) 4, `BOX1(THEM(^C))` → `BOX(THEM(^D))` (displacement from a mixed island) 3, `BOX(THEM(^C))` → `BOX1(THEM(^D))` (displacement from a mixed island) 3, `not(BOX(THEM(THEM)))` → `D` (displacement from a mixed island) 1, `BOX(THEM(ME))` → `C` (displacement from a mixed island) 1, `not(BOXD1(THEM(^BOX(THEM(ME)))))` → `BOX(THEM(ME))` (displacement from a mixed island) 1, `BOX(THEM(THEM))` → `C` (displacement from a mixed island) 1, `not(BOXD(THEM(^C)))` → `BOX(THEM(^D))` (displacement from a mixed island) 1.

Core-held losses (13; first 25): n 6 gen 200 (snapshot gen 180) `BOX1(THEM(ME))` → `BOX(THEM(^D))`, displacement from a mixed island, residents 3, ALLC in snapshot False, snapshot `BOX1(THEM(ME))` 58, `BOX1(THEM(^C))` 38, `BOX(THEM(^D))` 2, `BOX(THEM(THEM))` 2; n 6 gen 160 (snapshot gen 140) `BOX(THEM(ME))` → `D`, displacement from a mixed island, residents 2, ALLC in snapshot False, snapshot `BOX(THEM(ME))` 94, `BOX(THEM(THEM))` 5, `D` 1; n 6 gen 180 (snapshot gen 160) `BOX(THEM(ME))` → `C`, displacement from a mixed island, residents 5, ALLC in snapshot False, snapshot `BOX(THEM(ME))` 66, `BOX1(THEM(ME))` 15, `BOX(THEM(THEM))` 12, `BOX1(THEM(^C))` 4; n 6 gen 200 (snapshot gen 160) `BOX(THEM(ME))` → `BOX(THEM(^D))`, displacement from a mixed island, residents 5, ALLC in snapshot False, snapshot `BOX(THEM(ME))` 60, `BOX(THEM(^C))` 23, `BOX1(THEM(ME))` 13, `BOX1(THEM(THEM))` 2; n 7 gen 220 (snapshot gen 180) `BOX(THEM(ME))` → `BOX(THEM(^D))`, displacement from a mixed island, residents 3, ALLC in snapshot False, snapshot `BOX(THEM(ME))` 55, `BOX(THEM(THEM))` 24, `BOX(THEM(^C))` 21; n 7 gen 240 (snapshot gen 220) `BOX(THEM(ME))` → `BOX(THEM(^D))`, displacement from a mixed island, residents 5, ALLC in snapshot False, snapshot `BOX(THEM(ME))` 35, `BOX(THEM(^C))` 31, `BOX1(THEM(ME))` 13, `BOX1(THEM(^C))` 8; n 7 gen 160 (snapshot gen 120) `BOX1(THEM(ME))` → `BOX(THEM(^D))`, displacement from a mixed island, residents 3, ALLC in snapshot False, snapshot `BOX1(THEM(ME))` 55, `BOX1(THEM(^C))` 44, `D` 1; n 7 gen 180 (snapshot gen 140) `BOX1(THEM(ME))` → `BOX(THEM(^D))`, displacement from a mixed island, residents 3, ALLC in snapshot False, snapshot `BOX1(THEM(ME))` 52, `BOX1(THEM(^C))` 46, `D` 2; n 7 gen 200 (snapshot gen 160) `BOX(THEM(ME))` → `BOX(THEM(^D))`, displacement from a mixed island, residents 4, ALLC in snapshot False, snapshot `BOX(THEM(ME))` 50, `BOX(THEM(^C))` 46, `D` 3, `BOX1(THEM(^C))` 1; n 8 gen 220 (snapshot gen 180) `BOX1(THEM(ME))` → `BOX(THEM(^D))`, displacement from a mixed island, residents 2, ALLC in snapshot False, snapshot `BOX1(THEM(ME))` 57, `BOX1(THEM(^C))` 43; n 8 gen 240 (snapshot gen 220) `BOX1(THEM(ME))` → `BOX(THEM(^D))`, displacement from a mixed island, residents 4, ALLC in snapshot False, snapshot `BOX1(THEM(ME))` 57, `BOX1(THEM(^C))` 36, `BOX(THEM(ME))` 6, `BOX1(THEM(THEM))` 1; n 8 gen 240 (snapshot gen 200) `BOX(THEM(ME))` → `BOX1(THEM(^D))`, displacement from a mixed island, residents 3, ALLC in snapshot False, snapshot `BOX(THEM(ME))` 44, `BOX1(THEM(^C))` 37, `BOX(THEM(THEM))` 13, `BOX1(THEM(^D))` 6; n 9 gen 460 (snapshot gen 420) `BOX1(THEM(ME))` → `BOX(THEM(^D))`, displacement from a mixed island, residents 4, ALLC in snapshot False, snapshot `BOX1(THEM(ME))` 67, `BOX(THEM(^C))` 21, `BOX(THEM(^D))` 7, `BOX1(THEM(^C))` 4


Post-ALLC losses held by a fakeable self-cooperator and taken by a probe-faker (a class, not itself a self-cooperator, that strictly invades some fakeable self-cooperator's monomorphic world): n = 6: 0.88 [0.70, 0.96]; n = 7: 0.97 [0.93, 0.99]; n = 8: 0.97 [0.92, 0.99]; n = 9: 0.99 [0.93, 1.00].

Post-ALLC losses per run by cell (mean; bootstrap 95% over runs):

| N | I | n = 6 | n = 7 | n = 8 | n = 9 |
|---|---|---|---|---|---|
| 100 | 4 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 400 | 4 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 1600 | 4 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| 100 | 64 | 0.15 [0.00, 0.40] | 0.45 [0.00, 1.35] | 2.35 [0.00, 5.75] | 0.10 [0.00, 0.30] |
| 100 | 256 | 0.55 [0.23, 0.95] | 4.10 [0.75, 8.38] | 1.60 [0.45, 3.35] | 1.82 [0.17, 4.20] |
| 400 | 16 | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.10 [0.00, 0.30] | 0.00 [0.00, 0.00] |

Nucleation-control runs (reported separately): 23 losses, `BOX(THEM(^C))` → `BOX1(THEM(^D))` (displacement from a mixed island), `BOX(THEM(^C))` → `BOX1(THEM(^D))` (displacement from a mixed island), `BOX(THEM(^C))` → `BOX1(THEM(^D))` (displacement from a mixed island), `BOX(THEM(^C))` → `BOX1(THEM(^D))` (displacement from a mixed island), `BOX(THEM(THEM))` → `BOX1(THEM(^D))` (displacement from a mixed island), `BOX(THEM(^C))` → `BOX1(THEM(^D))` (displacement from a mixed island), `BOX(THEM(THEM))` → `C` (neutral replacement), `BOX(THEM(^C))` → `BOX1(THEM(^D))` (strict invasion of a monomorphic island).
## Frozen efficient states: who holds the islands

Island holder = largest class on the island at the stop. Shares over islands of efficient runs (mN = 1, all cells pooled) and over efficient islands of the no-migration control. E_k = μ_k·ρ_k(D, 100). Spearman ρ over all self-cooperators.

Intervals are run-cluster bootstrap 95% (islands within a run are not independent; no-migration islands are, so Wilson and bootstrap agree there). TV = total-variation distance between the holder distribution and E_k normalized.

| n | sample | runs / islands | FairBot + `BOX1(THEM(ME))` | fakeable self-coop | `BOX(THEM(THEM))` + `BOX1(THEM(THEM))` | Spearman (all self-coop) | Spearman (D-entering only) | TV to E_k | top holders (share) | E_k-predicted shares (top) |
|---|---|---|---|---|---|---|---|---|---|---|
| 6 | migration | 123 / 11988 | 0.43 [0.38, 0.48] | 0.33 [0.29, 0.38] | 0.48 [0.43, 0.54] | 0.85 | 0.82 | 0.07 | `BOX1(THEM(THEM))` 0.24; `BOX(THEM(THEM))` 0.24; `BOX(THEM(ME))` 0.23; `BOX1(THEM(ME))` 0.20; `BOX(THEM(^C))` 0.04; `BOX1(THEM(^C))` 0.04 | `BOX(THEM(ME))` 0.22; `BOX(THEM(THEM))` 0.22; `BOX1(THEM(ME))` 0.22; `BOX1(THEM(THEM))` 0.21 |
| 6 | no migration | 300 / 249 | 0.43 [0.36, 0.50] | 0.36 [0.30, 0.41] | 0.44 [0.37, 0.51] | 0.85 | 0.83 | 0.03 | `BOX1(THEM(THEM))` 0.23; `BOX1(THEM(ME))` 0.22; `BOX(THEM(ME))` 0.21; `BOX(THEM(THEM))` 0.21; `BOX(THEM(^C))` 0.06; `BOX1(THEM(^C))` 0.06 | `BOX(THEM(ME))` 0.22; `BOX(THEM(THEM))` 0.22; `BOX1(THEM(ME))` 0.22; `BOX1(THEM(THEM))` 0.21 |
| 7 | migration | 125 / 11996 | 0.46 [0.42, 0.50] | 0.54 [0.50, 0.58] | 0.42 [0.38, 0.46] | 0.64 | 0.78 | 0.06 | `BOX(THEM(THEM))` 0.24; `BOX1(THEM(ME))` 0.23; `BOX(THEM(ME))` 0.23; `BOX1(THEM(THEM))` 0.18; `BOX1(THEM(^C))` 0.06; `BOX(THEM(^C))` 0.06 | `BOX(THEM(ME))` 0.21; `BOX1(THEM(ME))` 0.21; `BOX(THEM(THEM))` 0.21; `BOX1(THEM(THEM))` 0.21 |
| 7 | no migration | 300 / 286 | 0.47 [0.41, 0.52] | 0.53 [0.48, 0.59] | 0.40 [0.34, 0.45] | 0.64 | 0.84 | 0.07 | `BOX1(THEM(ME))` 0.23; `BOX(THEM(ME))` 0.23; `BOX(THEM(THEM))` 0.20; `BOX1(THEM(THEM))` 0.19; `BOX(THEM(^C))` 0.08; `BOX1(THEM(^C))` 0.03 | `BOX(THEM(ME))` 0.21; `BOX1(THEM(ME))` 0.21; `BOX(THEM(THEM))` 0.21; `BOX1(THEM(THEM))` 0.21 |
| 8 | migration | 130 / 12040 | 0.41 [0.37, 0.45] | 0.59 [0.55, 0.62] | 0.47 [0.43, 0.51] | 0.40 | 0.54 | 0.08 | `BOX1(THEM(THEM))` 0.24; `BOX1(THEM(ME))` 0.23; `BOX(THEM(THEM))` 0.23; `BOX(THEM(ME))` 0.18; `BOX1(THEM(^C))` 0.06; `BOX(THEM(^C))` 0.05 | `BOX1(THEM(ME))` 0.21; `BOX(THEM(ME))` 0.21; `BOX(THEM(THEM))` 0.21; `BOX1(THEM(THEM))` 0.21 |
| 8 | no migration | 300 / 286 | 0.40 [0.34, 0.46] | 0.60 [0.54, 0.66] | 0.44 [0.38, 0.50] | 0.39 | 0.48 | 0.07 | `BOX(THEM(THEM))` 0.26; `BOX1(THEM(ME))` 0.20; `BOX(THEM(ME))` 0.20; `BOX1(THEM(THEM))` 0.18; `BOX(THEM(^C))` 0.06; `BOX1(THEM(^C))` 0.06 | `BOX1(THEM(ME))` 0.21; `BOX(THEM(ME))` 0.21; `BOX(THEM(THEM))` 0.21; `BOX1(THEM(THEM))` 0.21 |
| 9 | migration | 123 / 12000 | 0.49 [0.43, 0.54] | 0.51 [0.45, 0.56] | 0.39 [0.34, 0.44] | 0.33 | 0.48 | 0.08 | `BOX1(THEM(ME))` 0.28; `BOX(THEM(ME))` 0.20; `BOX(THEM(THEM))` 0.20; `BOX1(THEM(THEM))` 0.20; `BOX1(THEM(^C))` 0.06; `BOX(THEM(^C))` 0.05 | `BOX1(THEM(ME))` 0.21; `BOX(THEM(ME))` 0.21; `BOX(THEM(THEM))` 0.21; `BOX1(THEM(THEM))` 0.21 |
| 9 | no migration | 300 / 275 | 0.39 [0.33, 0.45] | 0.60 [0.54, 0.66] | 0.48 [0.42, 0.54] | 0.29 | 0.40 | 0.08 | `BOX(THEM(THEM))` 0.25; `BOX1(THEM(THEM))` 0.23; `BOX1(THEM(ME))` 0.21; `BOX(THEM(ME))` 0.18; `BOX(THEM(^C))` 0.05; `BOX1(THEM(^C))` 0.05 | `BOX1(THEM(ME))` 0.21; `BOX(THEM(ME))` 0.21; `BOX(THEM(THEM))` 0.21; `BOX1(THEM(THEM))` 0.21 |

## ALLC extinction

Island level: exact generation (birth resolution) at which each island's ALLC count first reaches 0, pooled over runs. Global: the generation at which the last ALLC dies.

| n | N | I | mN | island median [IQR] | island 90th pct | global median / max | ALLC re-entries per run |
|---|---|---|---|---|---|---|---|
| 6 | 100 | 4 | 1 | 13.9 [11.0, 18.2] | 22.4 | 20.3 / 64.8 | 0.7 |
| 7 | 100 | 4 | 1 | 13.4 [11.1, 17.7] | 22.4 | 21.3 / 64.8 | 0.8 |
| 8 | 100 | 4 | 1 | 13.7 [11.2, 16.8] | 21.0 | 19.1 / 62.1 | 1.0 |
| 9 | 100 | 4 | 1 | 14.0 [11.3, 19.1] | 23.2 | 21.9 / 38.8 | 0.8 |
| 6 | 100 | 64 | 1 | 13.6 [10.6, 17.0] | 21.7 | 36.6 / 109.5 | 10.6 |
| 7 | 100 | 64 | 1 | 13.7 [10.5, 17.2] | 21.9 | 35.3 / 174.3 | 11.8 |
| 8 | 100 | 64 | 1 | 13.3 [10.6, 17.2] | 21.6 | 40.8 / 164.9 | 12.0 |
| 9 | 100 | 64 | 1 | 13.6 [10.4, 17.2] | 21.9 | 35.1 / 112.0 | 12.7 |
| 6 | 100 | 256 | 1 | 13.6 [10.6, 17.3] | 21.7 | 48.3 / 110.2 | 46.8 |
| 7 | 100 | 256 | 1 | 13.5 [10.5, 17.3] | 21.7 | 48.0 / 117.9 | 48.0 |
| 8 | 100 | 256 | 1 | 13.6 [10.6, 17.4] | 21.9 | 62.9 / 242.2 | 48.4 |
| 9 | 100 | 256 | 1 | 13.5 [10.5, 17.3] | 21.6 | 50.2 / 153.1 | 45.2 |
| 6 | 400 | 4 | 1 | 18.7 [15.2, 22.4] | 25.6 | 23.5 / 30.1 | 0.1 |
| 7 | 400 | 4 | 1 | 19.2 [15.6, 21.9] | 25.6 | 23.1 / 41.8 | 0.1 |
| 8 | 400 | 4 | 1 | 19.6 [16.0, 22.5] | 25.2 | 24.5 / 200.6 | 1.9 |
| 9 | 400 | 4 | 1 | 19.2 [15.8, 22.5] | 25.6 | 23.5 / 41.8 | 0.2 |
| 6 | 400 | 16 | 1 | 18.6 [15.8, 22.2] | 25.9 | 30.9 / 52.4 | 0.5 |
| 7 | 400 | 16 | 1 | 18.8 [15.7, 22.2] | 26.1 | 28.3 / 47.2 | 0.5 |
| 8 | 400 | 16 | 1 | 19.2 [16.1, 22.4] | 26.3 | 32.2 / 49.1 | 0.4 |
| 9 | 400 | 16 | 1 | 18.7 [15.8, 22.2] | 26.9 | 31.1 / 139.6 | 0.9 |
| 6 | 1600 | 4 | 1 | 24.0 [21.7, 28.2] | 33.1 | 31.4 / 47.9 | 0.1 |
| 7 | 1600 | 4 | 1 | 24.0 [21.3, 28.4] | 33.6 | 32.6 / 47.9 | 0.1 |
| 8 | 1600 | 4 | 1 | 25.0 [21.7, 27.6] | 30.8 | 29.7 / 57.3 | 0.0 |
| 9 | 1600 | 4 | 1 | 24.2 [22.0, 28.5] | 33.6 | 32.3 / 47.9 | 0.1 |
| 6 | 100 | 64 | 1, T0 2000 | 13.4 [10.5, 17.4] | 21.9 | 33.5 / 2028.1 | 0.8 |
| 9 | 100 | 64 | 1, T0 2000 | 13.4 [10.4, 17.4] | 22.4 | 34.7 / 2033.0 | 1.6 |
| 6 | 100 | 4 | 0 | 13.8 [10.3, 18.1] | 22.5 | 19.8 / 54.9 | 0.0 |
| 7 | 100 | 4 | 0 | 13.8 [9.9, 18.2] | 22.6 | 20.7 / 49.6 | 0.0 |
| 8 | 100 | 4 | 0 | 13.4 [10.3, 16.9] | 21.3 | 18.9 / 52.8 | 0.0 |
| 9 | 100 | 4 | 0 | 14.1 [10.2, 18.3] | 22.6 | 20.9 / 54.9 | 0.0 |
| 6 | 400 | 4 | 0 | 19.0 [15.9, 22.6] | 26.4 | 24.4 / 36.1 | 0.0 |
| 7 | 400 | 4 | 0 | 18.9 [15.8, 22.7] | 26.7 | 24.9 / 48.5 | 0.0 |
| 8 | 400 | 4 | 0 | 19.7 [15.8, 22.9] | 26.9 | 25.4 / 66.9 | 0.0 |
| 9 | 400 | 4 | 0 | 19.2 [15.9, 22.7] | 26.6 | 24.5 / 46.9 | 0.0 |
| 6 | 1600 | 4 | 0 | 24.0 [21.5, 28.1] | 32.7 | 30.9 / 64.5 | 0.0 |
| 7 | 1600 | 4 | 0 | 24.2 [21.5, 28.1] | 32.7 | 30.9 / 51.4 | 0.0 |
| 8 | 1600 | 4 | 0 | 24.9 [21.9, 28.4] | 32.1 | 30.2 / 50.5 | 0.0 |
| 9 | 1600 | 4 | 0 | 24.3 [21.6, 28.4] | 33.1 | 31.1 / 51.4 | 0.0 |

Ratio of island-level medians n = 9 / n = 6: (100, 4, 1) 1.01; (100, 64, 1) 1.00; (100, 256, 1) 1.00; (400, 4, 1) 1.03; (400, 16, 1) 1.00; (1600, 4, 1) 1.01; (100, 4, 0) 1.02; (400, 4, 0) 1.01; (1600, 4, 0) 1.01.

## Unresolved and metastable runs

- n 9 (400, 4, mN 0) rep 94: unresolved, P(C,C) 0.625, support `D` 400, `BOX1(THEM(^C))` 400, `BOX(THEM(^C))` 400, `not(BOXD(THEM(THEM)))` 211, `BOX1(THEM(^BOX1(THEM(^D))))` 189; non-identical pairs [['D', 'BOX1(THEM(^C))'], ['D', 'BOX(THEM(^C))'], ['D', 'not(BOXD(THEM(THEM)))'], ['D', 'BOX1(THEM(^BOX1(THEM(^D))))']]

No-migration runs with some island unfrozen at the horizon: 1 (n 9 N 400 rep 94).

## Verdicts against `predictions/2026-10-05-seeds-in-n.md`

Held = the claimed quantity's interval lies inside the claim; failed = outside, or a falsifier fired; inconclusive = an interval straddles the boundary.

| # | prediction | outcome |
|---|---|---|
| 1 | p(100, n) 0.07–0.08 at n = 6, 0.045–0.06 at n = 7–9, tracking μ_core; no further fall 7 → 9 | **Failed (the step); falsifier not fired.** p(100, n) = 0.083 / 0.090 / 0.092 / 0.090. n = 6 range inconclusive ([0.059, 0.114] spans it); n = 7–9 range failed (every interval lies above 0.06); the μ_core predictor misses by +57% to +89% in all nine n ≥ 7 cells, outside every interval. "No further fall from 7 to 9" held (0.090 vs 0.090). |
| 2 | I = 4 ranges at n ≥ 7; ≥ 0.95 at I = 64, 256; ≈ 1 − (1 − p)^I | **Inconclusive at I = 4** (every interval straddles a range boundary; N = 1,600 point estimates 0.80–0.85 sit above 0.55–0.75). **Held at I ≥ 64** (20/20 and 40/40 at every n). Falsifiers not fired. The approximation **fails at (400, 4)** pooled over n: 0.42 [0.32, 0.53] observed against 0.56 [0.52, 0.60]; at (1,600, 4) 0.82 [0.75, 0.87] against 0.88 [0.86, 0.90]; it holds at N = 100 and at I = 16. |
| 3 | post-ALLC losses ≥ 0.9 fakeable-held and probe-faker-taken; no strict invasion of a core island; losses grow with n; runs with losses ≥ 0.95 efficient | **Held on the falsifier and the mechanism:** 0 strict invasions of a monomorphic core island; all 13 core-held losses are displacements from mixed islands: 11 by a probe-faker growing on a fakeable co-resident (`BOX(THEM(^C))` / `BOX1(THEM(^C))`, present in every one of the 11 snapshots), 1 by ALLC before its global extinction, and 1 by D against selection (birth-level replay, `python3 src/seeds_in_n.py replay`: 17 D migrants in 20 generations from a still mostly-D archipelago, then drift at w = 0.3, where D's disadvantage against FairBot is a fitness ratio of only e^0.3 ≈ 1.35; the run still froze efficient). Fakeable-and-probe-faker share 0.97–0.99 at n = 7–9 (held), 0.88 [0.70, 0.96] at n = 6 (inconclusive). "Grows with n" **inconclusive**: 0.16 / 1.08 / 0.71 / 0.47 losses per run, not monotone, concentrated in a few I = 64 and 256 runs, per-cell bootstrap intervals overlapping. Runs with losses: 100% efficient at every n (Wilson lower bounds 0.74–0.82). |
| 4 | FairBot + `BOX1(THEM(ME))` hold ≥ 0.6 of frozen efficient islands; fakeable share falls with n; shares track μ × establishment | **Failed, falsifier fired:** FairBot + `BOX1(THEM(ME))` hold 0.41–0.49 at every n (0.43 at n = 6 too); the fakeable share at n = 9 is 0.51 [0.45, 0.56] (> 0.3) and rises with n (0.33 → 0.51), because `BOX(THEM(THEM))` moves from the core to the fakeable set at n = 7 and keeps its share. The tracking claim holds in substance: the total-variation distance between island shares and normalized μ_k ρ_k(D) is 0.03–0.08 at every n (the four D-entering provers at ≈ 0.21 each, observed 0.18–0.28); the predeclared Spearman is 0.33 at n = 9 (0.29 without migration), at the 0.3 line, dragged by hundreds of zero-share, near-zero-mass classes. |
| 5 | island-level ALLC extinction median 15–60 at every n, N; n = 9 within ×1.5 of n = 6; global grows with I | **Partly.** n-independence held (n = 9 / n = 6 ratio of island medians 1.00–1.03 in all nine cells); global time grows with I (medians 20 / 35–41 / 48–63 at N = 100, I = 4 / 64 / 256). The range **failed at N = 100** (island medians 13.3–14.1); 18.6–25.0 at N = 400 and 1,600, inside. Falsifier (> 120) not fired. |
| S1 | no step at n = 7: p(100, 7) > 0.06, n = 7–9 within ±25% of n = 6 | **Held** (0.090; +8% to +11%). |
| S2 | μ_est (D-entering self-cooperators) predicts within ±25% at n = 7–9; μ_core does worse | **Held:** μ_est residuals +1% to +24.6% (fit on p(100, 6)); μ_core +57% to +89%; mean absolute 12% vs 71%. Part of the N = 1,600 residual is the exponent (slope of log p on log N is 0.55 at every n), not n. |
| S3 | `BOX(THEM(THEM))` + `BOX1(THEM(THEM))` share at n = 9 within the n = 6 interval | **Failed narrowly** on the predeclared (migration) sample: 0.39 [0.34, 0.44] vs 0.48 [0.42, 0.53]. Within on the no-migration sample (0.48 vs 0.44 [0.38, 0.50]). |
| S4 | post-ALLC losses per run at n = 9 within ×1.5 of n = 6; "grows with n" inconclusive | **Failed** on the factor (point ratio 3.0); the inconclusive part held. |

Other findings:
- *Establishment, then spread.* With migration off to generation 2,000 at (100, 64), 5.4 (n = 6) and 5.7 (n = 9) of 64 islands per run were certified cooperative at the switch (per island 0.084 / 0.089, equal to the no-migration p of 0.083 / 0.090), at least 2 in every run; after the switch 80 of 80 runs froze efficient (1.00 [0.95, 1.00]). At I = 64 the only stochastic step is establishment.
- *Where the defecting runs lose.* At N = 100, 54 of 59 defecting I = 4 runs had no self-cooperator left when the last ALLC died. At N = 1,600, 0 of 29 had lost them all; the defecting runs still had a median 26 core programs at ALLC extinction (efficient runs: 77), so the loss is a failure to nucleate from a minority after ALLC is gone, not a wipe-out in the scramble.
- *Small I with mN = 1.* At I = 4 the run-level chance sits between independent islands and one well-mixed island of 4N (N = 400: independent 0.56, observed 0.42, p(1,600) = 0.41). One migrant per generation partly merges four islands during nucleation. Untested hypothesis.
- *The one unresolved run* (n = 9, (400, 4), no migration) holds a stable anti-coordination pair on one island, `not(BOXD(THEM(THEM)))` 211 and `BOX1(THEM(^BOX1(THEM(^D))))` 189: each defects on its own class and cooperates with the other (payoff −1 against self, 0 against the other), island P(C,C) ≈ 0.5, alive at 10⁵ generations. An interior rest point, not a cycle. Dynamically unresolved, not administratively censored.

