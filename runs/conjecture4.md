# Conjecture 4: static map at n = 6–13 and the sibling check

Written by `src/conj4_report.py` from `runs/conjecture4.json` (`src/moat_static_big.py`) and `src/conj4.py`. Spec `specs/2026-10-04-conjecture4.md`; predictions `predictions/2026-10-04-conjecture4.md`; proof `notes/conjecture4.md`. Free modal arm, PD, boxes at PA and PA + Con(PA) (`modal.build`). Masses normalized over L_n unless marked unnormalized. n ≤ 11 reproduce `runs/drift_closure_static.json` exactly (class counts, frontier names, μ and leak to machine precision).

## Per n

| n | programs | canonical functions | classes | worlds | self-cooperating | suckerable self-coop. | components of G | closed | max drift distance | unsuckerable | FairBot leak/μ | min leak/μ (class) | time (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 1020 | 66 | 51 | 7 | 18 | 15 | 1 | 0 | 1 | 3 | 96.2788 | 96.2788 (`BOX(THEM(ME))`) | 3 |
| 8 | 19544 | 610 | 471 | 7 | 237 | 228 | 1 | 0 | 1 | 9 | 94.4377 | 94.4377 (`BOX(THEM(ME))`) | 0 |
| 9 | 89842 | 1210 | 863 | 9 | 405 | 392 | 1 | 0 | 1 | 13 | 93.4604 | 93.4604 (`BOX(THEM(ME))`) | 0 |
| 10 | 410644 | 2626 | 1752 | 10 | 764 | 749 | 1 | 0 | 1 | 15 | 93.1199 | 93.1199 (`BOX(THEM(ME))`) | 0 |
| 11 | 1935718 | 8322 | 5545 | 11 | 2520 | 2482 | 1 | 0 | 1 | 38 | 92.6832 | 92.6832 (`BOX(THEM(ME))`) | 6 |
| 12 | 9151856 | 22690 | 13514 | 13 | 6286 | 6201 | 1 | 0 | 1 | 85 | 92.4527 | 92.4527 (`BOX(THEM(ME))`) | 54 |
| 13 | 43982810 | 51234 | 27189 | 14 | 12310 | 12180 | 1 | 0 | 1 | 130 | 92.2175 | 92.2175 (`BOX(THEM(ME))`) | 388 |

**FairBot against the runner-up** (leak/μ):

| n | FairBot | runner-up | runner-up / FairBot − 1 |
|---|---|---|---|
| 6 | 96.27876 | 96.27876 (`BOX(THEM(THEM))`) | 0.00e+00 |
| 8 | 94.43770 | 94.46653 (`BOX1(THEM(ME))`) | 3.05e-04 |
| 9 | 93.46045 | 93.49384 (`BOX1(THEM(ME))`) | 3.57e-04 |
| 10 | 93.11986 | 93.14418 (`BOX1(THEM(ME))`) | 2.61e-04 |
| 11 | 92.68319 | 92.70761 (`BOX1(THEM(ME))`) | 2.64e-04 |
| 12 | 92.45273 | 92.47264 (`BOX1(THEM(ME))`) | 2.15e-04 |
| 13 | 92.21750 | 92.23642 (`BOX1(THEM(ME))`) | 2.05e-04 |

## Shells of FairBot's direct leak (n = 13; unnormalized mass, and contribution to leak/μ)

Shell s = programs of size exactly s. Shell s has total prior mass 1/(2s²). Leak membership is evaluated at cutoff n = 13. The contribution to leak/μ divides by FairBot's unnormalized class mass.

| s | shell mass 1/(2s²) | leak mass in shell | fraction of shell | FairBot-class mass in shell | Δ(leak/μ) | ratio to shell s−1 |
|---|---|---|---|---|---|---|
| 1 | 0.5 | 0.25 | 0.5000 | 0 | 61.348 |  |
| 2 | 0.125 | 0.0625 | 0.5000 | 0 | 15.337 | 0.250 |
| 3 | 0.05556 | 0.0216 | 0.3889 | 0.00309 | 5.302 | 0.346 |
| 4 | 0.03125 | 0.01116 | 0.3571 | 0 | 2.739 | 0.517 |
| 5 | 0.02 | 0.008416 | 0.4208 | 0.000495 | 2.065 | 0.754 |
| 6 | 0.01389 | 0.005508 | 0.3966 | 9.21e-05 | 1.352 | 0.654 |
| 7 | 0.0102 | 0.004262 | 0.4177 | 0.000154 | 1.046 | 0.774 |
| 8 | 0.007812 | 0.003211 | 0.4109 | 5.52e-05 | 0.788 | 0.753 |
| 9 | 0.006173 | 0.002592 | 0.4199 | 6.83e-05 | 0.636 | 0.807 |
| 10 | 0.005 | 0.002089 | 0.4177 | 3.71e-05 | 0.513 | 0.806 |
| 11 | 0.004132 | 0.001742 | 0.4216 | 3.76e-05 | 0.428 | 0.834 |
| 12 | 0.003472 | 0.001463 | 0.4213 | 2.59e-05 | 0.359 | 0.840 |
| 13 | 0.002959 | 0.001252 | 0.4233 | 2.39e-05 | 0.307 | 0.856 |

**FairBot's leak by shell at each cutoff** (unnormalized leak mass in shell s, evaluated at cutoff n):

| n | s=3 | s=4 | s=5 | s=6 | s=7 | s=8 | s=9 | s=10 | s=11 | s=12 | s=13 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 0.0185 | 0.0112 | 0.00792 | 0.00536 |  |  |  |  |  |  |  |
| 8 | 0.0216 | 0.0112 | 0.00842 | 0.00549 | 0.00426 | 0.00321 |  |  |  |  |  |
| 9 | 0.0216 | 0.0112 | 0.00842 | 0.00549 | 0.00426 | 0.00321 | 0.00259 |  |  |  |  |
| 10 | 0.0216 | 0.0112 | 0.00842 | 0.00551 | 0.00426 | 0.00321 | 0.00259 | 0.00209 |  |  |  |
| 11 | 0.0216 | 0.0112 | 0.00842 | 0.00551 | 0.00426 | 0.00321 | 0.00259 | 0.00209 | 0.00174 |  |  |
| 12 | 0.0216 | 0.0112 | 0.00842 | 0.00551 | 0.00426 | 0.00321 | 0.00259 | 0.00209 | 0.00174 | 0.00146 |  |
| 13 | 0.0216 | 0.0112 | 0.00842 | 0.00551 | 0.00426 | 0.00321 | 0.00259 | 0.00209 | 0.00174 | 0.00146 | 0.00125 |

## Program counts and prior mass by size and box-nesting depth (n = 13)

| size | programs | depth 0 | depth 1 | depth 2 | depth 3 | depth 4 |
|---|---|---|---|---|---|---|
| 1 | 2 | 2 | 0 | 0 | 0 | 0 |
| 2 | 2 | 2 | 0 | 0 | 0 | 0 |
| 3 | 18 | 10 | 8 | 0 | 0 | 0 |
| 4 | 42 | 26 | 16 | 0 | 0 | 0 |
| 5 | 202 | 114 | 88 | 0 | 0 | 0 |
| 6 | 754 | 402 | 320 | 32 | 0 | 0 |
| 7 | 3522 | 1722 | 1704 | 96 | 0 | 0 |
| 8 | 15002 | 6890 | 7408 | 704 | 0 | 0 |
| 9 | 70298 | 29794 | 37368 | 3008 | 128 | 0 |
| 10 | 320802 | 126626 | 175136 | 18528 | 512 | 0 |
| 11 | 1525074 | 556778 | 873800 | 90144 | 4352 | 0 |
| 12 | 7216138 | 2446138 | 4243408 | 504576 | 21504 | 512 |
| 13 | 34830954 | 10930130 | 21173144 | 2581376 | 143744 | 2560 |

Prior mass by box-nesting depth (normalized over L_13): depth 0: 0.9048, depth 1: 0.0919, depth 2: 0.0032, depth 3: 0.0001, depth 4: 0.0000.

## Unsuckerable classes, n = 6 (3)

| class | μ | direct leak | leak/μ | closure leak | universality | coop FB | coop ALLC | top leaks |
|---|---|---|---|---|---|---|---|---|
| `BOX(THEM(ME))` | 4.951e-03 | 4.767e-01 | 96.279 | 0.483 | 0.795 | True | True | `C`, `BOX1(THEM(THEM))` |
| `BOX(THEM(THEM))` | 4.951e-03 | 4.767e-01 | 96.279 | 0.483 | 0.795 | True | True | `C`, `BOX1(THEM(THEM))` |
| `BOX1(THEM(ME))` | 4.951e-03 | 4.768e-01 | 96.311 | 0.483 | 0.800 | True | True | `C`, `BOX1(THEM(THEM))` |

## Unsuckerable classes, n = 8 (9)

| class | μ | direct leak | leak/μ | closure leak | universality | coop FB | coop ALLC | top leaks |
|---|---|---|---|---|---|---|---|---|
| `BOX(THEM(ME))` | 5.084e-03 | 4.801e-01 | 94.438 | 0.487 | 0.779 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX1(THEM(ME))` | 5.085e-03 | 4.803e-01 | 94.467 | 0.487 | 0.788 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 2.728e-06 | 3.106e-03 | 1138.6 | 0.487 | 0.102 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 1.364e-06 | 3.122e-03 | 2289.3 | 0.487 | 0.102 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 1.364e-06 | 5.078e-03 | 3723.4 | 0.487 | 0.334 | True | False | `BOX(THEM(THEM))`, `or(BOX(THEM(ME)),BOX(THEM(THEM)))` |
| `BOX(THEM(^BOX(THEM(THEM))))` | 3.094e-05 | 4.801e-01 | 15517 | 0.487 | 0.779 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(THEM)))` | 2.276e-05 | 4.801e-01 | 21091 | 0.487 | 0.779 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))` | 7.587e-06 | 4.801e-01 | 63274 | 0.487 | 0.779 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^C)))` | 4.091e-06 | 4.801e-01 | 1.1734e+05 | 0.487 | 0.778 | True | True | `C`, `BOX(THEM(THEM))` |

## Unsuckerable classes, n = 9 (13)

| class | μ | direct leak | leak/μ | closure leak | universality | coop FB | coop ALLC | top leaks |
|---|---|---|---|---|---|---|---|---|
| `BOX(THEM(ME))` | 5.131e-03 | 4.796e-01 | 93.46 | 0.487 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX1(THEM(ME))` | 5.133e-03 | 4.799e-01 | 93.494 | 0.487 | 0.784 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 3.162e-06 | 3.210e-03 | 1015.2 | 0.487 | 0.103 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 1.809e-06 | 3.234e-03 | 1787.8 | 0.487 | 0.103 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 1.581e-06 | 5.135e-03 | 3248 | 0.487 | 0.330 | True | False | `BOX(THEM(THEM))`, `or(BOX(THEM(ME)),BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOX(THEM(THEM)))` | 3.284e-05 | 4.796e-01 | 14602 | 0.487 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX(THEM(^BOX(THEM(THEM))))` | 3.160e-05 | 4.796e-01 | 15176 | 0.487 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^D))))` | 2.281e-07 | 8.362e-03 | 36657 | 0.487 | 0.267 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))` | 1.095e-05 | 4.796e-01 | 43806 | 0.487 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^C)))` | 4.743e-06 | 4.796e-01 | 1.0112e+05 | 0.487 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX(THEM(^BOX(THEM(^BOX1(THEM(ME))))))` | 2.281e-07 | 4.796e-01 | 2.1024e+06 | 0.487 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX(THEM(^BOX(THEM(^BOX(THEM(THEM))))))` | 1.141e-07 | 4.796e-01 | 4.2049e+06 | 0.487 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX1(THEM(^BOX1(THEM(^BOX1(THEM(THEM))))))` | 1.141e-07 | 4.799e-01 | 4.2077e+06 | 0.487 | 0.784 | True | True | `C`, `BOX(THEM(THEM))` |

## Unsuckerable classes, n = 10 (15)

| class | μ | direct leak | leak/μ | closure leak | universality | coop FB | coop ALLC | top leaks |
|---|---|---|---|---|---|---|---|---|
| `BOX(THEM(ME))` | 5.146e-03 | 4.792e-01 | 93.12 | 0.487 | 0.769 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX1(THEM(ME))` | 5.149e-03 | 4.796e-01 | 93.144 | 0.487 | 0.780 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 4.670e-06 | 3.310e-03 | 708.82 | 0.487 | 0.104 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 2.335e-06 | 3.346e-03 | 1433 | 0.487 | 0.105 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 2.375e-06 | 5.194e-03 | 2186.6 | 0.487 | 0.326 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^C))))` | 3.071e-07 | 3.346e-03 | 10896 | 0.487 | 0.105 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOX(THEM(THEM)))` | 3.432e-05 | 4.792e-01 | 13963 | 0.487 | 0.769 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^D))))` | 3.071e-07 | 8.486e-03 | 27634 | 0.487 | 0.267 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))` | 1.144e-05 | 4.792e-01 | 41888 | 0.487 | 0.769 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^C)))` | 7.126e-06 | 4.792e-01 | 67250 | 0.487 | 0.769 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX1(THEM(ME)))))` | 2.414e-07 | 4.792e-01 | 1.9854e+06 | 0.487 | 0.769 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX(THEM(THEM)))))` | 2.414e-07 | 4.792e-01 | 1.9855e+06 | 0.487 | 0.769 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX(THEM(^BOX(THEM(^BOX(THEM(THEM))))))` | 1.133e-07 | 4.792e-01 | 4.2289e+06 | 0.487 | 0.769 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(^BOX(THEM(ME)))))` | 8.046e-08 | 4.796e-01 | 5.9607e+06 | 0.487 | 0.780 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(^BOX1(THEM(THEM)))))` | 8.046e-08 | 4.796e-01 | 5.9607e+06 | 0.487 | 0.780 | True | True | `C`, `BOX(THEM(THEM))` |

## Unsuckerable classes, n = 11 (38)

| class | μ | direct leak | leak/μ | closure leak | universality | coop FB | coop ALLC | top leaks |
|---|---|---|---|---|---|---|---|---|
| `BOX(THEM(ME))` | 5.167e-03 | 4.789e-01 | 92.683 | 0.486 | 0.766 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX1(THEM(ME))` | 5.170e-03 | 4.793e-01 | 92.708 | 0.486 | 0.778 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 2.594e-06 | 3.381e-03 | 1303.3 | 0.486 | 0.105 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(THEM)),not(BOX(THEM(THEM))))` | 2.594e-06 | 3.381e-03 | 1303.3 | 0.486 | 0.105 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 2.594e-06 | 3.425e-03 | 1320.2 | 0.486 | 0.106 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 2.648e-06 | 5.224e-03 | 1972.7 | 0.486 | 0.323 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^C))))` | 4.794e-07 | 3.425e-03 | 7144 | 0.486 | 0.106 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOX(THEM(THEM)))` | 3.936e-05 | 4.789e-01 | 12168 | 0.486 | 0.766 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^D))))` | 4.794e-07 | 8.587e-03 | 17912 | 0.486 | 0.266 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))` | 1.302e-05 | 4.789e-01 | 36774 | 0.486 | 0.766 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^C)))` | 7.944e-06 | 4.789e-01 | 60288 | 0.486 | 0.766 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD(THEM(ME))))))` | 1.391e-08 | 5.215e-03 | 3.7485e+05 | 0.486 | 0.323 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX1(THEM(THEM))))))` | 6.956e-09 | 3.429e-03 | 4.9301e+05 | 0.486 | 0.107 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX(THEM(ME))))))` | 6.956e-09 | 3.444e-03 | 4.9516e+05 | 0.486 | 0.107 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX(THEM(THEM))))))` | 6.956e-09 | 3.444e-03 | 4.9516e+05 | 0.486 | 0.107 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX1(THEM(ME))))))` | 6.956e-09 | 3.445e-03 | 4.9523e+05 | 0.486 | 0.107 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX1(THEM(ME))))))` | 6.956e-09 | 5.196e-03 | 7.4702e+05 | 0.486 | 0.322 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX(THEM(ME))))))` | 6.956e-09 | 5.203e-03 | 7.4793e+05 | 0.486 | 0.323 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD1(THEM(THEM))))))` | 6.956e-09 | 5.209e-03 | 7.4879e+05 | 0.486 | 0.323 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX1(THEM(THEM))))))` | 6.956e-09 | 5.209e-03 | 7.4881e+05 | 0.486 | 0.323 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX(THEM(THEM))))))` | 6.956e-09 | 5.215e-03 | 7.4972e+05 | 0.486 | 0.323 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD1(THEM(ME))))))` | 6.956e-09 | 5.221e-03 | 7.5057e+05 | 0.486 | 0.323 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD(THEM(ME))))))` | 6.956e-09 | 8.632e-03 | 1.2409e+06 | 0.486 | 0.268 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD(THEM(THEM))))))` | 6.956e-09 | 8.639e-03 | 1.242e+06 | 0.486 | 0.268 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD1(THEM(ME))))))` | 6.956e-09 | 8.683e-03 | 1.2482e+06 | 0.486 | 0.269 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD1(THEM(THEM))))))` | 6.956e-09 | 8.690e-03 | 1.2493e+06 | 0.486 | 0.270 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX1(THEM(ME)))))` | 2.610e-07 | 4.789e-01 | 1.8352e+06 | 0.486 | 0.766 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX(THEM(THEM)))))` | 2.401e-07 | 4.789e-01 | 1.9948e+06 | 0.486 | 0.766 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX(THEM(^BOX(THEM(^BOX(THEM(THEM))))))` | 1.649e-07 | 4.789e-01 | 2.9045e+06 | 0.486 | 0.766 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(^BOX(THEM(ME)))))` | 8.699e-08 | 4.793e-01 | 5.51e+06 | 0.486 | 0.778 | True | True | `C`, `BOX(THEM(THEM))` |
| `or(BOX(THEM(ME)),and(BOXD(THEM(ME)),BOX1(THEM(ME))))` | 8.348e-08 | 4.789e-01 | 5.7372e+06 | 0.486 | 0.766 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(^BOX1(THEM(THEM)))))` | 8.003e-08 | 4.793e-01 | 5.989e+06 | 0.486 | 0.778 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX(THEM(THEM)),BOXD(THEM(ME))))` | 5.565e-08 | 4.789e-01 | 8.6057e+06 | 0.486 | 0.766 | True | True | `C`, `BOX(THEM(THEM))` |
| `or(BOX(THEM(ME)),and(BOXD(THEM(THEM)),BOX1(THEM(ME))))` | 5.565e-08 | 4.789e-01 | 8.6058e+06 | 0.486 | 0.766 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX(THEM(^C)))))` | 4.174e-08 | 4.789e-01 | 1.1474e+07 | 0.486 | 0.766 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX(THEM(THEM)),BOXD(THEM(THEM))))` | 2.783e-08 | 4.789e-01 | 1.7212e+07 | 0.486 | 0.766 | True | True | `C`, `BOX(THEM(THEM))` |
| `or(BOX(THEM(ME)),and(BOX1(THEM(ME)),BOX1(THEM(THEM))))` | 2.783e-08 | 4.789e-01 | 1.7212e+07 | 0.486 | 0.766 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOXD(THEM(THEM)),BOX1(THEM(THEM))))` | 2.783e-08 | 4.789e-01 | 1.7212e+07 | 0.486 | 0.766 | True | True | `C`, `BOX(THEM(THEM))` |

## Unsuckerable classes, n = 12 (85)

| class | μ | direct leak | leak/μ | closure leak | universality | coop FB | coop ALLC | top leaks |
|---|---|---|---|---|---|---|---|---|
| `BOX(THEM(ME))` | 5.177e-03 | 4.787e-01 | 92.453 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX1(THEM(ME))` | 5.181e-03 | 4.791e-01 | 92.473 | 0.486 | 0.775 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(THEM)),not(BOX(THEM(THEM))))` | 3.028e-06 | 3.444e-03 | 1137.4 | 0.486 | 0.106 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 3.013e-06 | 3.444e-03 | 1142.9 | 0.486 | 0.106 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 3.020e-06 | 3.496e-03 | 1157.5 | 0.486 | 0.107 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 3.151e-06 | 5.243e-03 | 1663.6 | 0.486 | 0.321 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^C))))` | 5.707e-07 | 3.496e-03 | 6125.9 | 0.486 | 0.107 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOX(THEM(THEM)))` | 4.072e-05 | 4.787e-01 | 11754 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^D))))` | 5.707e-07 | 8.667e-03 | 15186 | 0.486 | 0.266 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))` | 1.352e-05 | 4.787e-01 | 35404 | 0.486 | 0.764 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^C)))` | 9.393e-06 | 4.787e-01 | 50959 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD(THEM(ME))))))` | 1.508e-08 | 5.233e-03 | 3.4698e+05 | 0.486 | 0.320 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX1(THEM(THEM))))))` | 8.155e-09 | 3.502e-03 | 4.2943e+05 | 0.486 | 0.108 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX(THEM(ME))))))` | 8.155e-09 | 3.518e-03 | 4.3139e+05 | 0.486 | 0.108 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX(THEM(THEM))))))` | 8.155e-09 | 3.518e-03 | 4.3139e+05 | 0.486 | 0.108 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX1(THEM(ME))))))` | 8.155e-09 | 3.519e-03 | 4.3145e+05 | 0.486 | 0.108 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD1(THEM(ME))))))` | 8.155e-09 | 5.240e-03 | 6.4252e+05 | 0.486 | 0.321 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX1(THEM(ME))))))` | 6.925e-09 | 5.211e-03 | 7.5243e+05 | 0.486 | 0.320 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX(THEM(ME))))))` | 6.925e-09 | 5.218e-03 | 7.535e+05 | 0.486 | 0.320 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD1(THEM(THEM))))))` | 6.925e-09 | 5.225e-03 | 7.5451e+05 | 0.486 | 0.320 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX1(THEM(THEM))))))` | 6.925e-09 | 5.226e-03 | 7.5455e+05 | 0.486 | 0.320 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX(THEM(THEM))))))` | 6.925e-09 | 5.233e-03 | 7.5563e+05 | 0.486 | 0.320 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD(THEM(ME))))))` | 8.155e-09 | 8.718e-03 | 1.0691e+06 | 0.486 | 0.268 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD(THEM(THEM))))))` | 8.155e-09 | 8.727e-03 | 1.0701e+06 | 0.486 | 0.268 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD1(THEM(ME))))))` | 8.155e-09 | 8.775e-03 | 1.076e+06 | 0.486 | 0.269 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD1(THEM(THEM))))))` | 8.155e-09 | 8.783e-03 | 1.077e+06 | 0.486 | 0.270 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX(THEM(THEM)))))` | 3.866e-07 | 4.787e-01 | 1.2381e+06 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX1(THEM(THEM)))))` | 1.933e-07 | 4.787e-01 | 2.4762e+06 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX1(THEM(ME)))))` | 1.933e-07 | 4.787e-01 | 2.4762e+06 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX(THEM(^BOX(THEM(^BOX(THEM(THEM))))))` | 1.715e-07 | 4.787e-01 | 2.7904e+06 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOX(THEM(THEM)))))))` | 1.230e-09 | 3.445e-03 | 2.8011e+06 | 0.486 | 0.106 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOX(THEM(ME)))))))` | 1.230e-09 | 3.446e-03 | 2.8022e+06 | 0.486 | 0.106 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX(THEM(^C))))))` | 1.230e-09 | 3.518e-03 | 2.8605e+06 | 0.486 | 0.108 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX1(THEM(^C))))))` | 1.230e-09 | 3.519e-03 | 2.861e+06 | 0.486 | 0.108 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(^BOX(THEM(ME)))))` | 1.370e-07 | 4.791e-01 | 3.4961e+06 | 0.486 | 0.775 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(^BOX1(THEM(THEM)))))` | 1.289e-07 | 4.791e-01 | 3.7174e+06 | 0.486 | 0.775 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD1(THEM(^C))))))` | 1.230e-09 | 5.211e-03 | 4.2368e+06 | 0.486 | 0.320 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX1(THEM(^D))))))` | 1.230e-09 | 5.211e-03 | 4.237e+06 | 0.486 | 0.320 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD(THEM(^C))))))` | 1.230e-09 | 5.218e-03 | 4.2428e+06 | 0.486 | 0.320 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX(THEM(^D))))))` | 1.230e-09 | 5.218e-03 | 4.2431e+06 | 0.486 | 0.320 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX1(THEM(^C))))))` | 1.230e-09 | 5.226e-03 | 4.2489e+06 | 0.486 | 0.320 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `or(BOX(THEM(ME)),and(BOXD(THEM(ME)),BOX1(THEM(ME))))` | 1.126e-07 | 4.787e-01 | 4.2501e+06 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX(THEM(^C))))))` | 1.230e-09 | 5.233e-03 | 4.255e+06 | 0.486 | 0.320 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOX1(THEM(THEM)))))))` | 1.230e-09 | 8.703e-03 | 7.0762e+06 | 0.486 | 0.267 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOX1(THEM(ME)))))))` | 1.230e-09 | 8.704e-03 | 7.0776e+06 | 0.486 | 0.267 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD(THEM(^C))))))` | 1.230e-09 | 8.710e-03 | 7.0822e+06 | 0.486 | 0.267 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOXD(THEM(ME)))))))` | 1.230e-09 | 8.713e-03 | 7.0849e+06 | 0.486 | 0.267 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOXD(THEM(THEM)))))))` | 1.230e-09 | 8.713e-03 | 7.0849e+06 | 0.486 | 0.267 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD(THEM(^D))))))` | 1.230e-09 | 8.727e-03 | 7.0956e+06 | 0.486 | 0.268 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOXD1(THEM(ME)))))))` | 1.230e-09 | 8.741e-03 | 7.1071e+06 | 0.486 | 0.268 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOXD1(THEM(THEM)))))))` | 1.230e-09 | 8.741e-03 | 7.1075e+06 | 0.486 | 0.268 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX1(THEM(^D))))))` | 1.230e-09 | 8.764e-03 | 7.1257e+06 | 0.486 | 0.269 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD1(THEM(^C))))))` | 1.230e-09 | 8.767e-03 | 7.1284e+06 | 0.486 | 0.269 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX(THEM(^D))))))` | 1.230e-09 | 8.778e-03 | 7.1371e+06 | 0.486 | 0.269 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD1(THEM(^D))))))` | 1.230e-09 | 8.783e-03 | 7.1418e+06 | 0.486 | 0.270 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),or(BOX(THEM(THEM)),BOXD(THEM(ME))))` | 6.278e-08 | 4.787e-01 | 7.624e+06 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `or(BOX(THEM(ME)),and(BOXD(THEM(THEM)),BOX1(THEM(ME))))` | 6.032e-08 | 4.787e-01 | 7.9349e+06 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),and(BOX(THEM(THEM)),BOX(THEM(^C))))` | 5.165e-08 | 4.787e-01 | 9.2666e+06 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX(THEM(^C)))))` | 4.893e-08 | 4.787e-01 | 9.7823e+06 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `or(BOX(THEM(ME)),and(BOX1(THEM(ME)),BOX1(THEM(THEM))))` | 3.016e-08 | 4.787e-01 | 1.587e+07 | 0.486 | 0.764 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX(THEM(THEM)),BOXD(THEM(THEM))))` | 2.770e-08 | 4.787e-01 | 1.7279e+07 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOXD(THEM(THEM)),BOX1(THEM(THEM))))` | 2.770e-08 | 4.787e-01 | 1.728e+07 | 0.486 | 0.764 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX1(THEM(^C)))))` | 2.447e-08 | 4.787e-01 | 1.9564e+07 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `or(BOX(THEM(ME)),and(BOX1(THEM(ME)),not(BOXD(THEM(ME)))))` | 1.476e-08 | 4.791e-01 | 3.246e+07 | 0.486 | 0.776 | True | True | `C`, `BOX(THEM(THEM))` |
| `or(BOX(THEM(ME)),and(BOX1(THEM(ME)),not(BOXD(THEM(THEM)))))` | 1.476e-08 | 4.791e-01 | 3.246e+07 | 0.486 | 0.776 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),or(BOX(THEM(THEM)),BOX(THEM(^C))))` | 1.230e-08 | 4.787e-01 | 3.892e+07 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),or(BOX(THEM(THEM)),BOX(THEM(^D))))` | 1.230e-08 | 4.787e-01 | 3.892e+07 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOXD(THEM(ME)),not(BOXD(THEM(THEM)))))` | 1.230e-08 | 4.791e-01 | 3.8952e+07 | 0.486 | 0.775 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(and(BOX(THEM(ME)),BOXD(THEM(ME)))))` | 9.839e-09 | 4.749e-01 | 4.8265e+07 | 0.486 | 0.487 | False | True | `C`, `BOX1(THEM(THEM))` |
| `or(BOX(THEM(ME)),and(BOX1(THEM(ME)),BOXD(THEM(^D))))` | 9.839e-09 | 4.790e-01 | 4.8687e+07 | 0.486 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(and(BOX(THEM(ME)),BOXD1(THEM(ME)))))` | 7.379e-09 | 4.730e-01 | 6.4102e+07 | 0.486 | 0.271 | False | True | `C`, `BOX1(THEM(THEM))` |
| `or(BOX(THEM(ME)),and(BOX1(THEM(ME)),not(BOX1(THEM(THEM)))))` | 7.379e-09 | 4.790e-01 | 6.4919e+07 | 0.486 | 0.775 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),or(BOX(THEM(THEM)),BOXD1(THEM(^D))))` | 4.919e-09 | 4.787e-01 | 9.73e+07 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `or(BOX(THEM(ME)),and(BOX1(THEM(ME)),BOX1(THEM(^D))))` | 4.919e-09 | 4.787e-01 | 9.7303e+07 | 0.486 | 0.764 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX1(THEM(THEM)),BOX(THEM(^D))))` | 4.919e-09 | 4.787e-01 | 9.7303e+07 | 0.486 | 0.764 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX(THEM(THEM)),not(BOX(THEM(ME)))))` | 4.919e-09 | 4.791e-01 | 9.738e+07 | 0.486 | 0.775 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(and(BOX(THEM(ME)),BOXD1(THEM(THEM)))))` | 2.460e-09 | 4.730e-01 | 1.9231e+08 | 0.486 | 0.271 | False | True | `C`, `BOX1(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX(THEM(THEM)),BOX1(THEM(^D))))` | 2.460e-09 | 4.787e-01 | 1.9461e+08 | 0.486 | 0.764 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX(THEM(THEM)),BOXD(THEM(^D))))` | 2.460e-09 | 4.790e-01 | 1.9475e+08 | 0.486 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX(THEM(THEM)),BOXD1(THEM(^D))))` | 2.460e-09 | 4.790e-01 | 1.9475e+08 | 0.486 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX1(THEM(THEM)),BOXD(THEM(^D))))` | 2.460e-09 | 4.790e-01 | 1.9475e+08 | 0.486 | 0.775 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX1(THEM(THEM)),BOXD1(THEM(^D))))` | 2.460e-09 | 4.790e-01 | 1.9475e+08 | 0.486 | 0.775 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX(THEM(^BOX(THEM(^BOX(THEM(^BOX1(THEM(ME))))))))` | 1.230e-09 | 4.787e-01 | 3.892e+08 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX(THEM(^BOX(THEM(^BOX(THEM(^BOX(THEM(THEM))))))))` | 6.149e-10 | 4.787e-01 | 7.784e+08 | 0.486 | 0.763 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX1(THEM(^BOX1(THEM(^BOX1(THEM(^BOX1(THEM(THEM))))))))` | 6.149e-10 | 4.791e-01 | 7.7904e+08 | 0.486 | 0.775 | True | True | `C`, `BOX(THEM(THEM))` |

## Unsuckerable classes, n = 13 (130)

| class | μ | direct leak | leak/μ | closure leak | universality | coop FB | coop ALLC | top leaks |
|---|---|---|---|---|---|---|---|---|
| `BOX(THEM(ME))` | 5.188e-03 | 4.785e-01 | 92.218 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX1(THEM(ME))` | 5.192e-03 | 4.789e-01 | 92.236 | 0.486 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 3.232e-06 | 3.496e-03 | 1081.9 | 0.486 | 0.106 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 3.240e-06 | 3.556e-03 | 1097.5 | 0.486 | 0.108 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 3.406e-06 | 5.261e-03 | 1544.4 | 0.486 | 0.319 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^C))))` | 6.923e-07 | 3.556e-03 | 5136.4 | 0.486 | 0.108 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOX(THEM(THEM)))` | 4.350e-05 | 4.784e-01 | 11000 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^D))))` | 6.918e-07 | 8.738e-03 | 12629 | 0.486 | 0.266 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))` | 1.440e-05 | 4.785e-01 | 33222 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^C)))` | 1.015e-05 | 4.784e-01 | 47137 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),and(BOX1(THEM(THEM)),not(BOX(THEM(ME)))))` | 1.860e-08 | 3.496e-03 | 1.8802e+05 | 0.486 | 0.106 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX1(THEM(THEM))))))` | 1.332e-08 | 3.563e-03 | 2.6761e+05 | 0.486 | 0.108 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX(THEM(ME))))))` | 1.332e-08 | 3.580e-03 | 2.6889e+05 | 0.486 | 0.109 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX(THEM(THEM))))))` | 1.332e-08 | 3.580e-03 | 2.6889e+05 | 0.486 | 0.109 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX1(THEM(ME))))))` | 1.332e-08 | 3.581e-03 | 2.6893e+05 | 0.486 | 0.109 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX1(THEM(ME))))))` | 1.209e-08 | 5.225e-03 | 4.3219e+05 | 0.486 | 0.318 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX(THEM(ME))))))` | 1.209e-08 | 5.233e-03 | 4.3287e+05 | 0.486 | 0.318 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD1(THEM(THEM))))))` | 1.209e-08 | 5.241e-03 | 4.335e+05 | 0.486 | 0.318 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX1(THEM(THEM))))))` | 1.209e-08 | 5.242e-03 | 4.3353e+05 | 0.486 | 0.318 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD(THEM(THEM))))))` | 1.209e-08 | 5.249e-03 | 4.3419e+05 | 0.486 | 0.319 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD(THEM(ME))))))` | 1.209e-08 | 5.249e-03 | 4.3419e+05 | 0.486 | 0.319 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX(THEM(THEM))))))` | 1.209e-08 | 5.250e-03 | 4.3422e+05 | 0.486 | 0.319 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD1(THEM(ME))))))` | 1.209e-08 | 5.257e-03 | 4.3484e+05 | 0.486 | 0.319 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD(THEM(ME))))))` | 1.332e-08 | 8.795e-03 | 6.6048e+05 | 0.486 | 0.267 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD(THEM(THEM))))))` | 1.332e-08 | 8.803e-03 | 6.6113e+05 | 0.486 | 0.268 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD1(THEM(ME))))))` | 1.332e-08 | 8.857e-03 | 6.6518e+05 | 0.486 | 0.269 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD1(THEM(THEM))))))` | 1.332e-08 | 8.866e-03 | 6.6583e+05 | 0.486 | 0.270 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),and(not(BOX(THEM(ME))),BOXD(THEM(^C))))` | 3.893e-09 | 3.457e-03 | 8.8792e+05 | 0.486 | 0.105 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX(THEM(THEM)))))` | 4.085e-07 | 4.785e-01 | 1.1712e+06 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX(THEM(^C))))))` | 1.658e-09 | 3.580e-03 | 2.1597e+06 | 0.486 | 0.109 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX1(THEM(^C))))))` | 1.658e-09 | 3.581e-03 | 2.1601e+06 | 0.486 | 0.109 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX1(THEM(ME)))))` | 2.049e-07 | 4.784e-01 | 2.335e+06 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX1(THEM(THEM)))))` | 2.036e-07 | 4.784e-01 | 2.3499e+06 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOX(THEM(THEM)))))))` | 1.442e-09 | 3.498e-03 | 2.4267e+06 | 0.486 | 0.107 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOX(THEM(ME)))))))` | 1.442e-09 | 3.500e-03 | 2.4279e+06 | 0.486 | 0.107 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `or(BOX(THEM(ME)),and(BOXD(THEM(ME)),BOX1(THEM(ME))))` | 1.857e-07 | 4.784e-01 | 2.576e+06 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),and(not(BOX(THEM(THEM))),BOXD1(THEM(^C))))` | 1.298e-09 | 3.486e-03 | 2.6859e+06 | 0.486 | 0.106 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD1(THEM(^C))))))` | 1.442e-09 | 5.225e-03 | 3.6246e+06 | 0.486 | 0.318 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX1(THEM(^D))))))` | 1.442e-09 | 5.225e-03 | 3.6249e+06 | 0.486 | 0.318 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD(THEM(^C))))))` | 1.442e-09 | 5.233e-03 | 3.6304e+06 | 0.486 | 0.318 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX(THEM(^D))))))` | 1.442e-09 | 5.234e-03 | 3.6306e+06 | 0.486 | 0.318 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX1(THEM(^C))))))` | 1.442e-09 | 5.242e-03 | 3.6361e+06 | 0.486 | 0.318 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD(THEM(^D))))))` | 1.442e-09 | 5.249e-03 | 3.6416e+06 | 0.486 | 0.319 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX(THEM(^C))))))` | 1.442e-09 | 5.250e-03 | 3.6419e+06 | 0.486 | 0.319 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX(THEM(ME)),BOXD1(THEM(^not(BOXD1(THEM(^D))))))` | 1.442e-09 | 5.257e-03 | 3.6471e+06 | 0.486 | 0.319 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX1(THEM(ME)),or(BOX(THEM(THEM)),BOXD(THEM(ME))))` | 1.071e-07 | 4.784e-01 | 4.4672e+06 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `or(BOX(THEM(ME)),and(BOXD(THEM(THEM)),BOX1(THEM(ME))))` | 1.042e-07 | 4.784e-01 | 4.5908e+06 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD(THEM(^C))))))` | 1.658e-09 | 8.786e-03 | 5.2996e+06 | 0.486 | 0.267 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD(THEM(^D))))))` | 1.658e-09 | 8.803e-03 | 5.3102e+06 | 0.486 | 0.268 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX1(THEM(^D))))))` | 1.658e-09 | 8.845e-03 | 5.3351e+06 | 0.486 | 0.269 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD1(THEM(^C))))))` | 1.658e-09 | 8.848e-03 | 5.3373e+06 | 0.486 | 0.269 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOX(THEM(^D))))))` | 1.658e-09 | 8.859e-03 | 5.3441e+06 | 0.486 | 0.269 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^BOXD1(THEM(^D))))))` | 1.658e-09 | 8.866e-03 | 5.3479e+06 | 0.486 | 0.270 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX(THEM(^C)))))` | 8.119e-08 | 4.785e-01 | 5.893e+06 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),or(not(BOX(THEM(THEM))),BOXD1(THEM(^D))))` | 8.651e-10 | 5.264e-03 | 6.0848e+06 | 0.486 | 0.319 | True | False | `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(THEM))))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOX1(THEM(THEM)))))))` | 1.442e-09 | 8.776e-03 | 6.0882e+06 | 0.486 | 0.267 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOX1(THEM(ME)))))))` | 1.442e-09 | 8.778e-03 | 6.0896e+06 | 0.486 | 0.267 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOXD(THEM(ME)))))))` | 1.442e-09 | 8.789e-03 | 6.0972e+06 | 0.486 | 0.267 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOXD(THEM(THEM)))))))` | 1.442e-09 | 8.789e-03 | 6.0972e+06 | 0.486 | 0.267 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOXD1(THEM(ME)))))))` | 1.442e-09 | 8.819e-03 | 6.1177e+06 | 0.486 | 0.268 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOXD1(THEM(THEM)))))))` | 1.442e-09 | 8.819e-03 | 6.1181e+06 | 0.486 | 0.268 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX(THEM(ME)),or(BOXD1(THEM(ME)),not(BOX(THEM(^D)))))` | 1.730e-09 | 1.061e-02 | 6.1311e+06 | 0.486 | 0.481 | True | False | `BOX(THEM(THEM))`, `BOX1(THEM(THEM))` |
| `and(BOX1(THEM(ME)),and(BOX1(THEM(THEM)),not(BOX(THEM(^D)))))` | 1.298e-09 | 8.738e-03 | 6.733e+06 | 0.486 | 0.266 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(and(BOX(THEM(THEM)),BOX(THEM(^D)))))` | 1.298e-09 | 8.797e-03 | 6.7787e+06 | 0.486 | 0.267 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(^BOX(THEM(ME)))))` | 6.852e-08 | 4.789e-01 | 6.989e+06 | 0.486 | 0.773 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(^BOX(THEM(THEM)))))` | 6.830e-08 | 4.789e-01 | 7.0111e+06 | 0.486 | 0.773 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(^BOX1(THEM(THEM)))))` | 6.808e-08 | 4.789e-01 | 7.0334e+06 | 0.486 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),and(BOX(THEM(THEM)),BOX(THEM(^C))))` | 6.054e-08 | 4.784e-01 | 7.9025e+06 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(or(BOX(THEM(THEM)),BOX(THEM(^D)))))` | 4.326e-10 | 3.496e-03 | 8.0829e+06 | 0.486 | 0.106 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `or(BOX(THEM(ME)),and(BOX1(THEM(ME)),BOX1(THEM(THEM))))` | 5.211e-08 | 4.785e-01 | 9.182e+06 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX(THEM(THEM)),BOXD(THEM(THEM))))` | 4.923e-08 | 4.784e-01 | 9.7194e+06 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOXD(THEM(THEM)),BOX1(THEM(THEM))))` | 4.923e-08 | 4.785e-01 | 9.7198e+06 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX1(THEM(^C)))))` | 4.060e-08 | 4.784e-01 | 1.1786e+07 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOX(THEM(^C)))))))` | 2.163e-10 | 3.498e-03 | 1.6173e+07 | 0.486 | 0.107 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOX(THEM(^D)))))))` | 2.163e-10 | 3.499e-03 | 1.6178e+07 | 0.486 | 0.107 | False | False | `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))` |
| `or(BOX(THEM(ME)),and(BOX1(THEM(ME)),not(BOXD(THEM(ME)))))` | 2.162e-08 | 4.789e-01 | 2.2145e+07 | 0.486 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `or(BOX(THEM(ME)),and(BOX1(THEM(ME)),not(BOXD(THEM(THEM)))))` | 1.903e-08 | 4.789e-01 | 2.5166e+07 | 0.486 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(and(BOX(THEM(ME)),BOXD(THEM(ME)))))` | 1.672e-08 | 4.747e-01 | 2.8384e+07 | 0.486 | 0.487 | False | True | `C`, `BOX1(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOXD(THEM(ME)),not(BOXD(THEM(THEM)))))` | 1.658e-08 | 4.789e-01 | 2.8886e+07 | 0.486 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),or(BOX(THEM(THEM)),BOX(THEM(^C))))` | 1.442e-08 | 4.784e-01 | 3.3191e+07 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),or(BOX(THEM(THEM)),BOX(THEM(^D))))` | 1.442e-08 | 4.785e-01 | 3.3191e+07 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(^BOX(THEM(^C)))))` | 1.353e-08 | 4.789e-01 | 3.5388e+07 | 0.486 | 0.773 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(and(BOX(THEM(ME)),BOXD1(THEM(ME)))))` | 1.254e-08 | 4.728e-01 | 3.7694e+07 | 0.486 | 0.271 | False | True | `C`, `BOX1(THEM(THEM))` |
| `or(BOX(THEM(ME)),and(BOX1(THEM(ME)),BOXD(THEM(^D))))` | 1.240e-08 | 4.788e-01 | 3.8624e+07 | 0.486 | 0.772 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOX1(THEM(^C)))))))` | 2.163e-10 | 8.776e-03 | 4.0576e+07 | 0.486 | 0.267 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOX1(THEM(^D)))))))` | 2.163e-10 | 8.777e-03 | 4.0578e+07 | 0.486 | 0.267 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOXD(THEM(^D)))))))` | 2.163e-10 | 8.789e-03 | 4.0636e+07 | 0.486 | 0.267 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOXD1(THEM(^D)))))))` | 2.163e-10 | 8.819e-03 | 4.0773e+07 | 0.486 | 0.268 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOXD(THEM(^C)))))))` | 2.163e-10 | 8.830e-03 | 4.0824e+07 | 0.486 | 0.268 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^not(BOXD1(THEM(^C)))))))` | 2.163e-10 | 8.852e-03 | 4.0926e+07 | 0.486 | 0.269 | False | False | `BOX1(THEM(THEM))`, `not(BOX(THEM(ME)))` |
| `or(BOX(THEM(ME)),and(BOX1(THEM(ME)),not(BOX1(THEM(THEM)))))` | 8.649e-09 | 4.789e-01 | 5.5365e+07 | 0.486 | 0.773 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX(THEM(THEM)),not(BOX(THEM(ME)))))` | 6.631e-09 | 4.789e-01 | 7.2214e+07 | 0.486 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `or(BOX(THEM(ME)),and(BOX1(THEM(ME)),BOX1(THEM(^D))))` | 6.199e-09 | 4.785e-01 | 7.7189e+07 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),or(BOX(THEM(THEM)),BOXD1(THEM(^D))))` | 5.766e-09 | 4.784e-01 | 8.2977e+07 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX1(THEM(THEM)),BOX(THEM(^D))))` | 5.766e-09 | 4.785e-01 | 8.298e+07 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(and(BOX(THEM(ME)),BOXD1(THEM(THEM)))))` | 3.316e-09 | 4.728e-01 | 1.4259e+08 | 0.486 | 0.271 | False | True | `C`, `BOX1(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX(THEM(THEM)),BOX1(THEM(^D))))` | 2.883e-09 | 4.785e-01 | 1.6596e+08 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX(THEM(THEM)),BOXD(THEM(^D))))` | 2.883e-09 | 4.788e-01 | 1.6609e+08 | 0.486 | 0.772 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX(THEM(THEM)),BOXD1(THEM(^D))))` | 2.883e-09 | 4.788e-01 | 1.6609e+08 | 0.486 | 0.772 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX1(THEM(THEM)),BOXD(THEM(^D))))` | 2.883e-09 | 4.788e-01 | 1.6609e+08 | 0.486 | 0.773 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX1(THEM(THEM)),BOXD1(THEM(^D))))` | 2.883e-09 | 4.788e-01 | 1.6609e+08 | 0.486 | 0.773 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX(THEM(^BOX1(THEM(ME)))))))` | 2.595e-09 | 4.785e-01 | 1.8434e+08 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),or(BOX(THEM(^C)),BOX(THEM(^D))))` | 2.163e-09 | 4.784e-01 | 2.2121e+08 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `or(BOX(THEM(ME)),and(BOX1(THEM(ME)),not(BOXD(THEM(^D)))))` | 2.163e-09 | 4.785e-01 | 2.2123e+08 | 0.486 | 0.762 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX(THEM(^BOX(THEM(THEM)))))))` | 1.947e-09 | 4.785e-01 | 2.4579e+08 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),or(not(BOX(THEM(THEM))),BOX(THEM(^C))))` | 1.730e-09 | 4.784e-01 | 2.7651e+08 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),or(BOX(THEM(THEM)),not(BOX(THEM(^D)))))` | 1.730e-09 | 4.784e-01 | 2.7651e+08 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),or(BOX(THEM(THEM)),not(BOX(THEM(^C)))))` | 1.730e-09 | 4.785e-01 | 2.7651e+08 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),BOX(THEM(^BOX1(THEM(^BOX(THEM(ME)))))))` | 1.298e-09 | 4.784e-01 | 3.6868e+08 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOXD(THEM(ME)),not(BOXD(THEM(^D)))))` | 1.298e-09 | 4.785e-01 | 3.6871e+08 | 0.486 | 0.762 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX(THEM(THEM)),not(BOX(THEM(^D)))))` | 1.298e-09 | 4.789e-01 | 3.69e+08 | 0.486 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(not(BOXD(THEM(THEM))),BOXD(THEM(^D))))` | 1.298e-09 | 4.789e-01 | 3.69e+08 | 0.486 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),or(BOX(THEM(^D)),BOXD1(THEM(^D))))` | 8.651e-10 | 4.712e-01 | 5.4468e+08 | 0.486 | 0.384 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),or(BOX(THEM(^C)),BOXD1(THEM(^D))))` | 8.651e-10 | 4.784e-01 | 5.5303e+08 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX(THEM(ME)),or(BOX(THEM(THEM)),not(BOXD1(THEM(^D)))))` | 8.651e-10 | 4.785e-01 | 5.5303e+08 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `or(BOX(THEM(ME)),and(BOX1(THEM(ME)),not(BOX1(THEM(^C)))))` | 8.651e-10 | 4.785e-01 | 5.5303e+08 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOXD(THEM(THEM)),not(BOXD(THEM(^D)))))` | 8.651e-10 | 4.785e-01 | 5.5307e+08 | 0.486 | 0.762 | True | True | `C`, `BOX(THEM(THEM))` |
| `or(BOX(THEM(ME)),and(BOX1(THEM(ME)),not(BOX1(THEM(^D)))))` | 8.651e-10 | 4.789e-01 | 5.5349e+08 | 0.486 | 0.773 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(^BOX1(THEM(^BOX(THEM(ME)))))))` | 8.651e-10 | 4.789e-01 | 5.5351e+08 | 0.486 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),BOX1(THEM(^BOX1(THEM(^BOX1(THEM(THEM)))))))` | 6.489e-10 | 4.789e-01 | 7.3801e+08 | 0.486 | 0.774 | True | True | `C`, `BOX(THEM(THEM))` |
| `BOX(THEM(^BOX(THEM(^BOX(THEM(^BOX(THEM(THEM))))))))` | 6.126e-10 | 4.785e-01 | 7.81e+08 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOXD1(THEM(ME)),not(BOXD1(THEM(^D)))))` | 4.326e-10 | 4.713e-01 | 1.0896e+09 | 0.486 | 0.385 | False | True | `C`, `BOX1(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOXD1(THEM(THEM)),not(BOXD1(THEM(^D)))))` | 4.326e-10 | 4.713e-01 | 1.0896e+09 | 0.486 | 0.385 | False | True | `C`, `BOX1(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(and(BOX(THEM(ME)),BOXD1(THEM(^C)))))` | 4.326e-10 | 4.727e-01 | 1.0929e+09 | 0.486 | 0.270 | False | True | `C`, `BOX1(THEM(THEM))` |
| `and(BOX1(THEM(ME)),not(and(BOXD1(THEM(THEM)),BOX(THEM(^D)))))` | 4.326e-10 | 4.728e-01 | 1.0929e+09 | 0.486 | 0.271 | False | True | `C`, `BOX1(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX(THEM(THEM)),not(BOX1(THEM(^C)))))` | 4.326e-10 | 4.785e-01 | 1.1061e+09 | 0.486 | 0.761 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX1(THEM(THEM)),not(BOXD1(THEM(^D)))))` | 4.326e-10 | 4.785e-01 | 1.1061e+09 | 0.486 | 0.762 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX(THEM(THEM)),not(BOXD1(THEM(^D)))))` | 4.326e-10 | 4.785e-01 | 1.1061e+09 | 0.486 | 0.762 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(not(BOX1(THEM(THEM))),BOX(THEM(^C))))` | 4.326e-10 | 4.788e-01 | 1.107e+09 | 0.486 | 0.773 | True | True | `C`, `BOX(THEM(THEM))` |
| `and(BOX1(THEM(ME)),or(BOX(THEM(THEM)),not(BOX1(THEM(^D)))))` | 4.326e-10 | 4.788e-01 | 1.107e+09 | 0.486 | 0.773 | True | True | `C`, `BOX(THEM(THEM))` |

## Sibling check (Theorem 1 of `notes/conjecture4.md`)

For every self-cooperating canonical function x of L_n (boxes up to lmax) that defects on D: y = or(x, ψ_K), ψ_K = and(not(BOX_K(THEM(^D))), not(BOXD_K(THEM(^D)))), z = BOX_K(THEM(^D)), K = max settle(P, D) over P in F(x). Checked in `modal_lv` (y, z added to the language): y–x mutual C, y self-C, y cooperates with z, z defects on y. Plus agreement of the independent evaluator in `src/conj4.py` with `modal_lv` on random pairs.

| n / lmax | canonical functions | self-cooperating | cooperate with D | K histogram | failures | pairs compared | disagreements |
|---|---|---|---|---|---|---|---|
| 6 / 1 | 66 | 25 | 9 | K=0: 2, K=1: 5, K=2: 9 | 0 | 3000 | 0 |
| 7 / 1 | 218 | 89 | 41 | K=0: 8, K=1: 16, K=2: 24 | 0 | 3000 | 0 |
| 8 / 1 | 610 | 287 | 169 | K=0: 14, K=1: 44, K=2: 60 | 0 | 3000 | 0 |
| 9 / 1 | 1210 | 551 | 355 | K=0: 26, K=1: 68, K=2: 102 | 0 | 3000 | 0 |
| 10 / 1 | 2626 | 1037 | 590 | K=0: 46, K=1: 140, K=2: 261 | 0 | 3000 | 0 |
| 11 / 1 | 8322 | 3481 | 1932 | K=0: 174, K=1: 470, K=2: 905 | 0 | 3000 | 0 |
| 6 / 2 | 122 | 43 | 13 | K=0: 3, K=1: 5, K=2: 9, K=3: 13 | 0 | 3000 | 0 |
| 7 / 2 | 470 | 190 | 85 | K=0: 15, K=1: 22, K=2: 30, K=3: 38 | 0 | 3000 | 0 |
| 8 / 2 | 1370 | 646 | 379 | K=0: 27, K=1: 63, K=2: 80, K=3: 97 | 0 | 3000 | 0 |
| 9 / 2 | 2870 | 1258 | 793 | K=0: 56, K=1: 96, K=2: 133, K=3: 180 | 0 | 3000 | 0 |
| 9 / 1 | 1210 | 551 | 355 | K=0: 26, K=1: 170 | 0 | 3000 | 0 |
| 10 / 1 | 2626 | 1037 | 590 | K=0: 46, K=1: 401 | 0 | 3000 | 0 |
| 11 / 1 | 8322 | 3481 | 1932 | K=0: 174, K=1: 1375 | 4 | 3000 | 0 |
| 8 / 2 | 1370 | 646 | 379 | K=0: 27, K=1: 63, K=2: 177 | 0 | 3000 | 0 |
| 9 / 2 | 2870 | 1258 | 793 | K=0: 56, K=1: 96, K=2: 313 | 0 | 3000 | 0 |
| 9 / 1 | 1210 | 551 | 355 | K=0: 196 | 0 | 3000 | 0 |
| 10 / 1 | 2626 | 1037 | 590 | K=0: 447 | 0 | 3000 | 0 |
| 11 / 1 | 8322 | 3481 | 1932 | K=0: 1549 | 8 | 3000 | 0 |
| 8 / 2 | 1370 | 646 | 379 | K=0: 267 | 0 | 3000 | 0 |
| 9 / 2 | 2870 | 1258 | 793 | K=0: 465 | 0 | 3000 | 0 |

| x | size | K | sibling y (size) | faker z | ok |
|---|---|---|---|---|---|
| `BOX(THEM(ME))` | 3 | 1 | `or(BOX(THEM(ME)),and(not(BOX1(THEM(^D))),not(BOXD1(THEM(^D)))))` (15) | `BOX1(THEM(^D))` | True |
| `BOX1(THEM(ME))` | 3 | 2 | `or(BOX1(THEM(ME)),and(not(BOX2(THEM(^D))),not(BOXD2(THEM(^D)))))` (15) | `BOX2(THEM(^D))` | True |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 8 | 1 | `or(and(BOX(THEM(ME)),BOXD1(THEM(^D))),and(not(BOX1(THEM(^D))),not(BOXD1(THEM(^D)))))` (20) | `BOX1(THEM(^D))` | True |
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 8 | 2 | `or(and(BOX1(THEM(ME)),not(BOX(THEM(ME)))),and(not(BOX2(THEM(^D))),not(BOXD2(THEM(^D)))))` (20) | `BOX2(THEM(^D))` | True |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^C))))` | 9 | 2 | `or(and(BOX1(THEM(ME)),not(BOX(THEM(^C)))),and(not(BOX2(THEM(^D))),not(BOXD2(THEM(^D)))))` (21) | `BOX2(THEM(^D))` | True |
| `and(and(BOX1(THEM(ME)),not(BOX(THEM(^C)))),BOXD2(THEM(^D)))` | 14 | 2 | `or(and(and(BOX1(THEM(ME)),not(BOX(THEM(^C)))),BOXD2(THEM(^D))),and(not(BOX2(THEM(^D))),not(BOXD2(THEM(^D)))))` (26) | `BOX2(THEM(^D))` | True |
| `and(and(BOX1(THEM(ME)),not(BOX(THEM(ME)))),BOXD2(THEM(^D)))` | 13 | 2 | `or(and(and(BOX1(THEM(ME)),not(BOX(THEM(ME)))),BOXD2(THEM(^D))),and(not(BOX2(THEM(^D))),not(BOXD2(THEM(^D)))))` (25) | `BOX2(THEM(^D))` | True |
| `and(and(BOX2(THEM(ME)),not(BOX1(THEM(^C)))),BOXD2(THEM(^D)))` | 14 | | not self-cooperating | | |
| `and(BOX(THEM(ME)),BOXD2(THEM(^D)))` | 8 | 1 | `or(and(BOX(THEM(ME)),BOXD2(THEM(^D))),and(not(BOX1(THEM(^D))),not(BOXD1(THEM(^D)))))` (20) | `BOX1(THEM(^D))` | True |
| `BOX(THEM(THEM))` | 3 | 1 | `or(BOX(THEM(THEM)),and(not(BOX1(THEM(^D))),not(BOXD1(THEM(^D)))))` (15) | `BOX1(THEM(^D))` | True |
| `C` | 1 | | suckerable by D (distance 0) | | |
