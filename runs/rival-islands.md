# Rival networks across islands, and the mN rule (`src/rival_islands.py`)

Spec `specs/2026-10-05-rival-islands.md`; predictions `predictions/2026-10-05-rival-islands.md`. Modal arm, PD, w = 0.3, eps = 0, complete island graph, uniform replacement; generation = I*N births; horizon 1e5; migration continues after certification. Every run is in every denominator.

## 1. Static

| N | rho(DD migrant) | rho(D into FairBot) | rho(establisher into all-D) | P(fix) from k = 5 / 10 / 20 / 40 DD migrants at once |
|---|---|---|---|---|
| 100 | 1.85e-05 | 1.74e-08 | 0.0421 | 0.00018 / 0.00087 / 0.0097 / 0.22 |
| 200 | 7.22e-09 | 3.79e-15 | 0.0300 | 7.1e-08 / 3.7e-07 / 5.6e-06 / 0.00049 |
| 400 | 1.56e-15 | 2.53e-28 | 0.0214 | 1.5e-14 / 8.2e-14 / 1.5e-12 / 2.7e-10 |

n = 9: 770 mutually-defecting establisher pairs, pair mass 3e-07; rivals of the FairBot pair (cooperative, mutually defecting with FairBot or `BOX1(THEM(ME))`): establisher mass 2.43e-05 over 20 classes; expected rival establisher seeds per run at N = 100: I = 64: 0.16, I = 256: 0.62, I = 1024: 2.49.

| x | y | mu_x | mu_y | co-seed N = 100 |
|---|---|---|---|---|
| `BOX1(THEM(ME))` | `BOX1(THEM(^not(BOX(THEM(ME)))))` | 0.00513 | 5.36e-06 | 2.14e-04 |
| `BOX1(THEM(ME))` | `BOX1(THEM(^not(BOX(THEM(THEM)))))` | 0.00513 | 5.36e-06 | 2.14e-04 |
| `BOX(THEM(ME))` | `BOX1(THEM(^not(BOX(THEM(ME)))))` | 0.00513 | 5.36e-06 | 2.14e-04 |
| `BOX(THEM(ME))` | `BOX1(THEM(^not(BOX(THEM(THEM)))))` | 0.00513 | 5.36e-06 | 2.14e-04 |
| `BOX1(THEM(ME))` | `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 0.00513 | 3.16e-06 | 1.26e-04 |
| `BOX(THEM(ME))` | `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 0.00513 | 3.16e-06 | 1.26e-04 |
| `BOX(THEM(THEM))` | `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 0.0051 | 3.16e-06 | 1.26e-04 |
| `BOX1(THEM(ME))` | `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 0.00513 | 1.81e-06 | 7.22e-05 |

n = 12: 283091 mutually-defecting establisher pairs, pair mass 5.38e-07; rivals of the FairBot pair (cooperative, mutually defecting with FairBot or `BOX1(THEM(ME))`): establisher mass 4.14e-05 over 443 classes; expected rival establisher seeds per run at N = 100: I = 64: 0.26, I = 256: 1.06, I = 1024: 4.24.

| x | y | mu_x | mu_y | co-seed N = 100 |
|---|---|---|---|---|
| `BOX1(THEM(ME))` | `BOX1(THEM(^not(BOX(THEM(ME)))))` | 0.00518 | 6.46e-06 | 2.60e-04 |
| `BOX1(THEM(ME))` | `BOX1(THEM(^not(BOX(THEM(THEM)))))` | 0.00518 | 6.46e-06 | 2.59e-04 |
| `BOX(THEM(ME))` | `BOX1(THEM(^not(BOX(THEM(ME)))))` | 0.00518 | 6.46e-06 | 2.60e-04 |
| `BOX(THEM(ME))` | `BOX1(THEM(^not(BOX(THEM(THEM)))))` | 0.00518 | 6.46e-06 | 2.59e-04 |
| `BOX1(THEM(ME))` | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 0.00518 | 3.15e-06 | 1.27e-04 |
| `BOX1(THEM(ME))` | `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` | 0.00518 | 3.13e-06 | 1.26e-04 |
| `BOX1(THEM(ME))` | `and(BOX1(THEM(THEM)),not(BOX(THEM(THEM))))` | 0.00518 | 3.03e-06 | 1.22e-04 |
| `BOX(THEM(ME))` | `and(BOX1(THEM(THEM)),not(BOX(THEM(THEM))))` | 0.00518 | 3.03e-06 | 1.22e-04 |

Item-2 pairs (n = 9), network masses under the length prior (tag 1 = A's network, 2 = B's, 3 = bridge):

| pair | mu_A | mu_B | A net | B net | bridge | fakers of B | fakers of A |
|---|---|---|---|---|---|---|---|
| 1: `BOX1(THEM(ME))` x `BOX1(THEM(^not(BOX(THEM(ME)))))` | 0.00513 | 5.36e-06 | 0.0193 | 0.00031 | 0.0053 | 0.0182 | 0 |
| 2: `BOX1(THEM(ME))` x `BOX1(THEM(^not(BOX(THEM(THEM)))))` | 0.00513 | 5.36e-06 | 0.0193 | 0.000321 | 0.0053 | 0.008 | 0 |
| 3: `BOX1(THEM(ME))` x `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 0.00513 | 3.16e-06 | 0.0246 | 0.00321 | 8.15e-06 | 0 | 0 |

## 2. Separated seed (n = 9, N = 100; islands 0, 1 all-A, all-B; the rest iid)

Categories at the horizon or stop (from island holders): both / A only / B only / neither / unresolved. Hazard = first network extinctions per generation at risk (exact Poisson 95%). KM = survival of both networks.

| pair | I | mN | runs | both | A only | B only | neither | unres. | first-loss hazard [95%] | KM S(1e2) / S(1e3) / S(1e4) / S(1e5) | median loss gen | A majority | B majority | bridge-held at end | cf cross P(C,C) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 16 | 0.1 | 40 | 32 | 3 | 5 | 0 | 0 | 2.4e-06 [1e-06, 4.7e-06] | 1.00 / 0.97 / 0.88 / 0.80 | 7691 | 24 | 15 | 0.09 | 0.722 |
| 1 | 16 | 1 | 40 | 0 | 20 | 20 | 0 | 0 | 7.8e-05 [5.6e-05, 0.00011] | 0.97 / 0.67 / 0.45 / 0.00 | 7587 | 20 | 20 | 0.14 | 1.000 |
| 1 | 16 | 10 | 40 | 0 | 26 | 13 | 1 | 0 | 0.012 [0.0089, 0.017] | 0.17 / 0.00 / 0.00 / 0.00 | 76 | 26 | 13 | 0.07 | 1.000 |
| 1 | 64 | 0.1 | 40 | 21 | 10 | 9 | 0 | 0 | 7.9e-06 [4.7e-06, 1.2e-05] | 1.00 / 0.95 / 0.88 / 0.52 | 14758 | 18 | 21 | 0.26 | 0.773 |
| 1 | 64 | 1 | 40 | 0 | 22 | 18 | 0 | 0 | 0.00013 [9.5e-05, 0.00018] | 1.00 / 0.80 / 0.30 / 0.00 | 1362 | 22 | 18 | 0.51 | 1.000 |
| 1 | 64 | 10 | 40 | 0 | 28 | 10 | 2 | 0 | 0.0077 [0.0055, 0.01] | 0.80 / 0.00 / 0.00 / 0.00 | 108 | 28 | 10 | 0.21 | 1.000 |
| 1 | 256 | 0.1 | 40 | 4 | 21 | 15 | 0 | 0 | 2e-05 [1.4e-05, 2.7e-05] | 0.97 / 0.97 / 0.92 / 0.10 | 39038 | 24 | 16 | 0.62 | 0.984 |
| 1 | 256 | 1 | 40 | 0 | 32 | 8 | 0 | 0 | 0.00066 [0.00047, 0.0009] | 1.00 / 0.82 / 0.02 / 0.00 | 1244 | 32 | 8 | 0.61 | 1.000 |
| 1 | 256 | 10 | 40 | 0 | 34 | 5 | 1 | 0 | 0.0057 [0.0041, 0.0078] | 0.90 / 0.00 / 0.00 / 0.00 | 155 | 34 | 5 | 0.45 | 1.000 |
| 2 | 16 | 0.1 | 40 | 36 | 3 | 1 | 0 | 0 | 1.1e-06 [3e-07, 2.8e-06] | 1.00 / 1.00 / 0.95 / 0.90 | 10175 | 23 | 16 | 0.04 | 0.672 |
| 2 | 16 | 1 | 40 | 0 | 22 | 18 | 0 | 0 | 0.0001 [7.1e-05, 0.00014] | 0.97 / 0.82 / 0.42 / 0.00 | 6764 | 22 | 18 | 0.07 | 1.000 |
| 2 | 16 | 10 | 40 | 0 | 22 | 17 | 1 | 0 | 0.013 [0.0096, 0.018] | 0.10 / 0.00 / 0.00 / 0.00 | 73 | 22 | 17 | 0.06 | 1.000 |
| 2 | 64 | 0.1 | 40 | 22 | 10 | 8 | 0 | 0 | 7e-06 [4.1e-06, 1.1e-05] | 1.00 / 0.97 / 0.85 / 0.55 | 13985 | 22 | 17 | 0.27 | 0.839 |
| 2 | 64 | 1 | 40 | 0 | 25 | 13 | 2 | 0 | 0.00029 [0.00021, 0.00039] | 1.00 / 0.57 / 0.10 / 0.00 | 1119 | 25 | 13 | 0.50 | 1.000 |
| 2 | 64 | 10 | 40 | 0 | 26 | 12 | 2 | 0 | 0.0079 [0.0057, 0.011] | 0.80 / 0.00 / 0.00 / 0.00 | 118 | 26 | 12 | 0.23 | 1.000 |
| 2 | 256 | 0.1 | 40 | 2 | 23 | 14 | 0 | 1 | 2e-05 [1.4e-05, 2.8e-05] | 1.00 / 1.00 / 0.95 / 0.05 | 44096 | 25 | 15 | 0.61 | 0.975 |
| 2 | 256 | 1 | 40 | 0 | 35 | 5 | 0 | 0 | 0.00075 [0.00054, 0.001] | 1.00 / 0.67 / 0.00 / 0.00 | 1227 | 35 | 5 | 0.71 | 1.000 |
| 2 | 256 | 10 | 40 | 0 | 28 | 9 | 3 | 0 | 0.0049 [0.0035, 0.0067] | 1.00 / 0.00 / 0.00 / 0.00 | 168 | 28 | 9 | 0.43 | 1.000 |
| 3 | 16 | 0.1 | 40 | 38 | 1 | 1 | 0 | 0 | 5.1e-07 [6.2e-08, 1.8e-06] | 1.00 / 1.00 / 1.00 / 0.95 | 53698 | 18 | 20 | 0.00 | 0.646 |
| 3 | 16 | 1 | 40 | 0 | 25 | 15 | 0 | 0 | 7.1e-05 [5.1e-05, 9.7e-05] | 1.00 / 1.00 / 0.47 / 0.00 | 9635 | 25 | 15 | 0.00 | 1.000 |
| 3 | 16 | 10 | 40 | 0 | 18 | 22 | 0 | 0 | 0.014 [0.01, 0.02] | 0.05 / 0.00 / 0.00 / 0.00 | 67 | 18 | 22 | 0.00 | 1.000 |
| 3 | 64 | 0.1 | 40 | 40 | 0 | 0 | 0 | 0 | 0 [0, 9.2e-07] | 1.00 / 1.00 / 1.00 / 1.00 | - | 34 | 6 | 0.00 | 0.669 |
| 3 | 64 | 1 | 40 | 0 | 33 | 7 | 0 | 0 | 5.2e-05 [3.7e-05, 7e-05] | 1.00 / 1.00 / 0.85 / 0.00 | 18236 | 33 | 7 | 0.00 | 1.000 |
| 3 | 64 | 10 | 40 | 0 | 21 | 19 | 0 | 0 | 0.0089 [0.0064, 0.012] | 0.72 / 0.00 / 0.00 / 0.00 | 109 | 21 | 19 | 0.00 | 1.000 |
| 3 | 256 | 0.1 | 40 | 40 | 0 | 0 | 0 | 0 | 0 [0, 9.2e-07] | 1.00 / 1.00 / 1.00 / 1.00 | - | 38 | 2 | 0.00 | 0.645 |
| 3 | 256 | 1 | 40 | 0 | 40 | 0 | 0 | 0 | 4.5e-05 [3.2e-05, 6.1e-05] | 1.00 / 1.00 / 1.00 / 0.00 | 21553 | 40 | 0 | 0.00 | 1.000 |
| 3 | 256 | 10 | 40 | 0 | 36 | 4 | 0 | 0 | 0.008 [0.0057, 0.011] | 0.90 / 0.00 / 0.00 / 0.00 | 125 | 36 | 4 | 0.00 | 1.000 |

Nucleation and ancestry in the background islands (means per run): established locally by A's network / B's / bridge / other; established by immigrants (any network); never established; first immigrant-founded establishment (median gen); run-level: network with more local establishments before it (incl. its pre-seeded island) holds the majority.

| pair | I | mN | local A / B / bridge / other | immigrant A / B / bridge | none | first imm. est. | predicted-majority right / wrong / tie |
|---|---|---|---|---|---|---|---|
| 1 | 16 | 0.1 | 0.9 / 0.00 / 0.3 / 0.0 | 6.9 / 5.25 / 0.6 | 0.0 | 135 | 15 / 7 / 18 |
| 1 | 16 | 1 | 0.5 / 0.00 / 0.2 / 0.0 | 6.3 / 5.90 / 1.1 | 0.0 | 58 | 5 / 3 / 32 |
| 1 | 16 | 10 | 0.0 / 0.00 / 0.0 / 0.0 | 8.0 / 4.05 / 1.1 | 0.9 | 60 | 0 / 0 / 40 |
| 1 | 64 | 0.1 | 4.5 / 0.00 / 1.2 / 0.0 | 28.6 / 19.68 / 8.0 | 0.0 | 82 | 17 / 21 / 2 |
| 1 | 64 | 1 | 2.8 / 0.00 / 1.0 / 0.0 | 28.5 / 21.05 / 8.7 | 0.0 | 55 | 12 / 11 / 17 |
| 1 | 64 | 10 | 0.0 / 0.00 / 0.0 / 0.0 | 36.2 / 12.90 / 12.9 | 0.0 | 80 | 0 / 0 / 40 |
| 1 | 256 | 0.1 | 17.5 / 0.05 / 5.0 / 0.2 | 148.2 / 36.18 / 46.3 | 0.0 | 58 | 22 / 16 / 2 |
| 1 | 256 | 1 | 14.4 / 0.00 / 3.6 / 0.1 | 143.3 / 44.50 / 46.9 | 0.0 | 48 | 28 / 6 / 6 |
| 1 | 256 | 10 | 0.0 / 0.00 / 0.0 / 0.0 | 148.5 / 2.83 / 102.6 | 0.0 | 85 | 0 / 0 / 40 |
| 2 | 16 | 0.1 | 0.8 / 0.00 / 0.2 / 0.0 | 7.0 / 5.55 / 0.5 | 0.0 | 105 | 11 / 9 / 20 |
| 2 | 16 | 1 | 0.7 / 0.00 / 0.2 / 0.0 | 6.4 / 6.25 / 0.5 | 0.0 | 60 | 6 / 5 / 29 |
| 2 | 16 | 10 | 0.0 / 0.00 / 0.0 / 0.0 | 6.6 / 5.47 / 0.7 | 1.2 | 60 | 0 / 0 / 40 |
| 2 | 64 | 0.1 | 3.8 / 0.03 / 1.2 / 0.1 | 31.6 / 17.07 / 7.8 | 0.0 | 82 | 22 / 18 / 0 |
| 2 | 64 | 1 | 3.4 / 0.00 / 1.2 / 0.0 | 33.0 / 15.15 / 9.2 | 0.0 | 58 | 18 / 7 / 15 |
| 2 | 64 | 10 | 0.0 / 0.00 / 0.0 / 0.0 | 35.0 / 13.63 / 13.4 | 0.0 | 78 | 0 / 0 / 40 |
| 2 | 256 | 0.1 | 16.9 / 0.00 / 4.3 / 0.2 | 153.3 / 33.25 / 45.4 | 0.0 | 60 | 25 / 15 / 0 |
| 2 | 256 | 1 | 13.0 / 0.03 / 4.1 / 0.0 | 139.7 / 46.50 / 50.6 | 0.0 | 45 | 27 / 4 / 9 |
| 2 | 256 | 10 | 0.0 / 0.00 / 0.0 / 0.0 | 135.5 / 19.60 / 98.9 | 0.0 | 85 | 0 / 0 / 40 |
| 3 | 16 | 0.1 | 1.0 / 0.00 / 0.0 / 0.0 | 6.6 / 6.35 / 0.0 | 0.0 | 100 | 10 / 16 / 14 |
| 3 | 16 | 1 | 0.8 / 0.00 / 0.0 / 0.0 | 7.5 / 5.67 / 0.0 | 0.0 | 60 | 15 / 2 / 23 |
| 3 | 16 | 10 | 0.0 / 0.00 / 0.0 / 0.0 | 6.3 / 7.70 / 0.0 | 0.0 | 60 | 0 / 0 / 40 |
| 3 | 64 | 0.1 | 5.6 / 0.00 / 0.0 / 0.0 | 42.2 / 14.20 / 0.0 | 0.0 | 72 | 31 / 6 / 3 |
| 3 | 64 | 1 | 4.3 / 0.00 / 0.0 / 0.0 | 42.2 / 15.45 / 0.0 | 0.0 | 52 | 24 / 5 / 11 |
| 3 | 64 | 10 | 0.0 / 0.00 / 0.0 / 0.0 | 32.6 / 29.45 / 0.0 | 0.0 | 85 | 0 / 0 / 40 |
| 3 | 256 | 0.1 | 24.0 / 0.03 / 0.0 / 0.1 | 200.9 / 28.82 / 0.0 | 0.0 | 60 | 35 / 2 / 3 |
| 3 | 256 | 1 | 17.6 / 0.05 / 0.0 / 0.0 | 203.2 / 32.72 / 0.0 | 0.0 | 45 | 35 / 0 / 5 |
| 3 | 256 | 10 | 0.0 / 0.00 / 0.0 / 0.0 | 228.6 / 25.40 / 0.0 | 0.0 | 85 | 0 / 0 / 40 |

## Controls

**m = 0 (A and B pre-seeded, iid background):** local establishment per background island, by network.

| pair | I | runs | p(A net) | p(B net) | p(bridge) | p(other coop) | p(none) |
|---|---|---|---|---|---|---|---|
| 1 | 16 | 40 | 0.0643 | 0.00000 | 0.0196 | 0.0000 | 0.916 |
| 1 | 64 | 40 | 0.0681 | 0.00000 | 0.0198 | 0.0004 | 0.912 |
| 1 | 256 | 40 | 0.0708 | 0.00020 | 0.0187 | 0.0017 | 0.909 |
| 2 | 16 | 40 | 0.0732 | 0.00000 | 0.0250 | 0.0018 | 0.900 |
| 2 | 64 | 40 | 0.0738 | 0.00040 | 0.0173 | 0.0008 | 0.908 |
| 2 | 256 | 40 | 0.0702 | 0.00000 | 0.0174 | 0.0009 | 0.912 |
| 3 | 16 | 40 | 0.0696 | 0.00000 | 0.0000 | 0.0000 | 0.930 |
| 3 | 64 | 40 | 0.0992 | 0.00000 | 0.0000 | 0.0008 | 0.900 |
| 3 | 256 | 40 | 0.0885 | 0.00000 | 0.0000 | 0.0009 | 0.911 |

**Prediction 2.** Predicted A share from the m = 0 measured local-establishment rates, (1 + E_A)/(2 + E_A + E_B), against the observed fraction of runs with an A majority; Spearman over cells = 0.70. Pooled: A majority 719 / 1080 = 0.67, B majority 343 (0.32), ties 18. Run level: the network with more local establishments before the first immigrant-founded island held the majority in 358 of 511 decided runs (0.70); 569 runs undecided (equal counts).

| pair | I | mN | predicted A share | observed A-majority fraction |
|---|---|---|---|---|
| 1 | 16 | 0.1 | 0.655 | 0.60 |
| 1 | 16 | 1 | 0.655 | 0.50 |
| 1 | 16 | 10 | 0.655 | 0.65 |
| 1 | 64 | 0.1 | 0.839 | 0.45 |
| 1 | 64 | 1 | 0.839 | 0.55 |
| 1 | 64 | 10 | 0.839 | 0.70 |
| 1 | 256 | 0.1 | 0.948 | 0.60 |
| 1 | 256 | 1 | 0.948 | 0.80 |
| 1 | 256 | 10 | 0.948 | 0.85 |
| 2 | 16 | 0.1 | 0.669 | 0.57 |
| 2 | 16 | 1 | 0.669 | 0.55 |
| 2 | 16 | 10 | 0.669 | 0.55 |
| 2 | 64 | 0.1 | 0.845 | 0.55 |
| 2 | 64 | 1 | 0.845 | 0.62 |
| 2 | 64 | 10 | 0.845 | 0.65 |
| 2 | 256 | 0.1 | 0.950 | 0.62 |
| 2 | 256 | 1 | 0.950 | 0.88 |
| 2 | 256 | 10 | 0.950 | 0.70 |
| 3 | 16 | 0.1 | 0.664 | 0.45 |
| 3 | 16 | 1 | 0.664 | 0.62 |
| 3 | 16 | 10 | 0.664 | 0.45 |
| 3 | 64 | 0.1 | 0.877 | 0.85 |
| 3 | 64 | 1 | 0.877 | 0.82 |
| 3 | 64 | 10 | 0.877 | 0.53 |
| 3 | 256 | 0.1 | 0.959 | 0.95 |
| 3 | 256 | 1 | 0.959 | 1.00 |
| 3 | 256 | 10 | 0.959 | 0.90 |

Per pair: pair 1: A 228, B 126, tie 6 of 360; pair 2: A 228, B 122, tie 10 of 360; pair 3: A 263, B 95, tie 2 of 360

**A only pre-seeded (pair 1 tags).**

| I | mN | runs | A-network-held islands at end (mean share) | bridge-held | rival (any) locally established, runs | rival separation at end | ever separated | efficient |
|---|---|---|---|---|---|---|---|---|
| 16 | 0.1 | 40 | 0.86 | 0.14 | 0 | 0 | 0 | 40 |
| 16 | 1 | 40 | 0.90 | 0.10 | 0 | 0 | 0 | 40 |
| 16 | 10 | 40 | 0.97 | 0.00 | 0 | 0 | 0 | 39 |
| 64 | 0.1 | 40 | 0.85 | 0.15 | 0 | 0 | 0 | 40 |
| 64 | 1 | 40 | 0.89 | 0.11 | 0 | 0 | 0 | 40 |
| 64 | 10 | 40 | 0.94 | 0.03 | 0 | 0 | 0 | 39 |
| 256 | 0.1 | 40 | 0.77 | 0.22 | 1 | 1 | 1 | 39 |
| 256 | 1 | 40 | 0.80 | 0.20 | 1 | 0 | 2 | 40 |
| 256 | 10 | 40 | 0.96 | 0.04 | 0 | 0 | 0 | 40 |

**two homogeneous networks, half/half, no background.**

| N | I | mN | runs | both | A only | B only | neither | first-loss hazard [95%] | KM S(1e2)/S(1e3)/S(1e4)/S(1e5) | median loss | rival separation at end | A majority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 16 | 0.1 | 40 | 40 | 0 | 0 | 0 | 0 [0, 9.2e-07] | 1.00 / 1.00 / 1.00 / 1.00 | - | 40 | 17 |
| 100 | 16 | 1 | 40 | 0 | 25 | 15 | 0 | 4.4e-05 [3.1e-05, 6e-05] | 1.00 / 1.00 / 0.95 / 0.00 | 22657 | 0 | 25 |
| 100 | 16 | 10 | 40 | 0 | 20 | 20 | 0 | 0.013 [0.0094, 0.018] | 0.10 / 0.00 / 0.00 / 0.00 | 74 | 0 | 20 |
| 100 | 64 | 0.1 | 40 | 40 | 0 | 0 | 0 | 0 [0, 9.2e-07] | 1.00 / 1.00 / 1.00 / 1.00 | - | 40 | 17 |
| 100 | 64 | 1 | 40 | 0 | 20 | 20 | 0 | 2.7e-05 [1.9e-05, 3.6e-05] | 1.00 / 1.00 / 1.00 / 0.00 | 36165 | 0 | 20 |
| 200 | 64 | 1 | 40 | 40 | 0 | 0 | 0 | 0 [0, 9.2e-07] | 1.00 / 1.00 / 1.00 / 1.00 | - | 40 | 3 |
| 100 | 64 | 10 | 40 | 0 | 22 | 18 | 0 | 0.01 [0.0074, 0.014] | 0.45 / 0.00 / 0.00 / 0.00 | 99 | 0 | 22 |
| 200 | 64 | 10 | 40 | 0 | 19 | 21 | 0 | 0.0019 [0.0013, 0.0025] | 1.00 / 0.02 / 0.00 / 0.00 | 506 | 0 | 19 |
| 100 | 256 | 0.1 | 40 | 40 | 0 | 0 | 0 | 0 [0, 9.2e-07] | 1.00 / 1.00 / 1.00 / 1.00 | - | 40 | 22 |
| 100 | 256 | 1 | 40 | 0 | 20 | 20 | 0 | 2e-05 [1.5e-05, 2.8e-05] | 1.00 / 1.00 / 1.00 / 0.00 | 44441 | 0 | 20 |
| 100 | 256 | 10 | 40 | 0 | 19 | 21 | 0 | 0.0088 [0.0063, 0.012] | 0.82 / 0.00 / 0.00 / 0.00 | 115 | 0 | 19 |

**one all-B island among I - 1 all-A, no background.**

| N | I | mN | runs | both | A only | B only | neither | first-loss hazard [95%] | KM S(1e2)/S(1e3)/S(1e4)/S(1e5) | median loss | rival separation at end | A majority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 16 | 0.1 | 40 | 33 | 7 | 0 | 0 | 1.9e-06 [7.6e-07, 3.9e-06] | 1.00 / 1.00 / 1.00 / 0.82 | 63648 | 33 | 40 |
| 100 | 16 | 1 | 40 | 0 | 40 | 0 | 0 | 0.00026 [0.00019, 0.00036] | 0.97 / 0.72 / 0.07 / 0.00 | 2245 | 0 | 40 |
| 100 | 16 | 10 | 40 | 0 | 40 | 0 | 0 | 0.038 [0.027, 0.051] | 0.00 / 0.00 / 0.00 / 0.00 | 26 | 0 | 40 |
| 100 | 64 | 0.1 | 40 | 38 | 2 | 0 | 0 | 5.1e-07 [6.1e-08, 1.8e-06] | 1.00 / 1.00 / 1.00 / 0.95 | 78082 | 35 | 40 |
| 100 | 64 | 1 | 40 | 0 | 40 | 0 | 0 | 0.00027 [0.00019, 0.00036] | 0.97 / 0.82 / 0.10 / 0.00 | 2784 | 0 | 40 |
| 200 | 64 | 1 | 40 | 39 | 1 | 0 | 0 | 2.6e-07 [6.5e-09, 1.4e-06] | 1.00 / 1.00 / 1.00 / 0.97 | 17288 | 32 | 40 |
| 100 | 64 | 10 | 40 | 0 | 40 | 0 | 0 | 0.036 [0.026, 0.049] | 0.00 / 0.00 / 0.00 / 0.00 | 27 | 0 | 40 |
| 200 | 64 | 10 | 40 | 0 | 40 | 0 | 0 | 0.019 [0.013, 0.026] | 0.02 / 0.00 / 0.00 / 0.00 | 50 | 0 | 40 |
| 100 | 256 | 0.1 | 40 | 36 | 4 | 0 | 0 | 1.1e-06 [2.9e-07, 2.7e-06] | 1.00 / 1.00 / 0.97 / 0.90 | 23041 | 35 | 40 |
| 100 | 256 | 1 | 40 | 0 | 40 | 0 | 0 | 0.00034 [0.00024, 0.00047] | 1.00 / 0.72 / 0.02 / 0.00 | 1923 | 0 | 40 |
| 100 | 256 | 10 | 40 | 0 | 40 | 0 | 0 | 0.038 [0.027, 0.051] | 0.00 / 0.00 / 0.00 / 0.00 | 27 | 0 | 40 |

S1 check (one all-B island among I - 1 all-A): hazard of losing B vs the single-migrant prediction mN·rho_DD(100) = 1.85e-05·mN.

| N | I | mN | B losses / runs | hazard of B loss [95%] | predicted mN·rho_DD(N) | ratio | B ever held > 1 island |
|---|---|---|---|---|---|---|---|
| 100 | 16 | 0.1 | 7 / 40 | 1.9e-06 [7.6e-07, 3.9e-06] | 1.9e-06 | 1.03 | 5 |
| 100 | 16 | 1 | 40 / 40 | 0.00026 [0.00019, 0.00036] | 1.9e-05 | 14.1 | 3 |
| 100 | 16 | 10 | 40 / 40 | 0.038 [0.027, 0.051] | 0.00019 | 203 | 0 |
| 100 | 64 | 0.1 | 2 / 40 | 5.1e-07 [6.1e-08, 1.8e-06] | 1.9e-06 | 0.273 | 9 |
| 100 | 64 | 1 | 40 / 40 | 0.00027 [0.00019, 0.00036] | 1.9e-05 | 14.4 | 2 |
| 200 | 64 | 1 | 1 / 40 | 2.6e-07 [6.5e-09, 1.4e-06] | 7.2e-09 | 35.3 | 0 |
| 100 | 64 | 10 | 40 / 40 | 0.036 [0.026, 0.049] | 0.00019 | 194 | 0 |
| 200 | 64 | 10 | 40 / 40 | 0.019 [0.013, 0.026] | 7.2e-08 | 2.61e+05 | 0 |
| 100 | 256 | 0.1 | 4 / 40 | 1.1e-06 [2.9e-07, 2.7e-06] | 1.9e-06 | 0.576 | 7 |
| 100 | 256 | 1 | 40 / 40 | 0.00034 [0.00024, 0.00047] | 1.9e-05 | 18.5 | 1 |
| 100 | 256 | 10 | 40 / 40 | 0.038 [0.027, 0.051] | 0.00019 | 204 | 0 |

## 3. Natural separation (iid seeds only, N = 100)

Separated = at the end, two certified islands whose cooperative holders mutually defect. p_B = local establishments by a rival of the FairBot pair per island, measured in these runs; predicted = 1 - (1 - p_B)^I.

| n | I | mN | runs | separated at end [95%] | ever separated | p_B (per island) | predicted | rival seeded runs | efficient | unresolved | composition of separated runs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 9 | 64 | 0.1 | 300 | 0.00 [0.00, 0.02] | 2 | 1.04e-04 | 0.007 | 2 | 297 | 0 | BOX1(THEM(ME)):34 + BOX1(THEM(^not(BOX(THEM(ME))))):27 (1) |
| 9 | 64 | 1 | 300 | 0.00 [0.00, 0.01] | 2 | 5.21e-05 | 0.003 | 2 | 299 | 0 |  |
| 9 | 256 | 0.1 | 300 | 0.00 [0.00, 0.02] | 8 | 1.04e-04 | 0.026 | 8 | 300 | 0 | BOX1(THEM(ME)):210 + and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):42 (1) |
| 9 | 256 | 1 | 300 | 0.00 [0.00, 0.01] | 9 | 1.04e-04 | 0.026 | 9 | 300 | 0 |  |
| 9 | 1024 | 0.1 | 300 | 0.03 [0.02, 0.06] | 35 | 1.01e-04 | 0.098 | 30 | 300 | 0 | BOX1(THEM(^C)):862 + and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):147 (1); BOX(THEM(THEM)):826 + and(BOX1(THEM(ME)),not(BOX(THEM(THEM)))):186 (1); BOX1(THEM(ME)):803 + and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):209 (1) |
| 9 | 1024 | 1 | 300 | 0.00 [0.00, 0.01] | 25 | 6.84e-05 | 0.068 | 25 | 300 | 0 |  |
| 12 | 64 | 0.1 | 300 | 0.01 [0.00, 0.03] | 4 | 2.08e-04 | 0.013 | 4 | 299 | 0 | and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):40 + BOX1(THEM(ME)):24 (1); BOX(THEM(ME)):36 + and(BOX1(THEM(ME)),not(BOX(THEM(THEM)))):27 (1); BOX1(THEM(ME)):61 + and(BOX1(THEM(THEM)),not(BOX(THEM(THEM)))):3 (1) |
| 12 | 64 | 1 | 300 | 0.00 [0.00, 0.01] | 6 | 2.60e-04 | 0.017 | 6 | 299 | 0 |  |
| 12 | 256 | 0.1 | 300 | 0.02 [0.01, 0.05] | 21 | 2.73e-04 | 0.068 | 21 | 300 | 0 | BOX1(THEM(ME)):254 + BOX1(THEM(^not(BOX(THEM(ME))))):2 (1); BOX1(THEM(ME)):216 + and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):37 (1); BOX1(THEM(ME)):166 + and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):82 (1) |
| 12 | 256 | 1 | 300 | 0.00 [0.00, 0.01] | 15 | 1.43e-04 | 0.036 | 15 | 300 | 0 |  |
| 12 | 1024 | 0.1 | 100 | 0.09 [0.05, 0.16] | 20 | 1.95e-04 | 0.181 | 18 | 100 | 0 | BOX1(THEM(ME)):798 + and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):209 (1); BOX1(THEM(ME)):754 + and(BOX1(THEM(THEM)),not(BOX(THEM(THEM)))):248 (1); BOX1(THEM(ME)):946 + and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):71 (1) |
| 12 | 1024 | 1 | 300 | 0.00 [0.00, 0.01] | 50 | 1.33e-04 | 0.128 | 49 | 300 | 0 |  |

## 4. The mN rule (n = 9)

m = 0 reference, N = 100: per-island establishment p = 0.103 (640 islands), T_nuc (median establishment gen) = 45.
m = 0 reference, N = 400: per-island establishment p = 0.181 (640 islands), T_nuc (median establishment gen) = 70.

| N | I | mN | x = mN·T_nuc/N | runs | efficient [95%] | reference 1-(1-p)^I | fall | local-ancestry est. per island | ICC of local est. | arrivals before est. (mean) | replacement fraction at est. (mean) | median est. gen |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 16 | 0.03 | 0.013 | 40 | 0.82 [0.68, 0.91] | 0.825 | -0.00 | 0.091 | -0.010 | 61.0 | 0.890 | 1845 |
| 100 | 16 | 0.1 | 0.045 | 40 | 0.82 [0.68, 0.91] | 0.825 | -0.00 | 0.080 | -0.006 | 81.5 | 0.904 | 698 |
| 100 | 16 | 0.3 | 0.135 | 40 | 0.80 [0.65, 0.90] | 0.825 | +0.02 | 0.089 | -0.006 | 78.3 | 0.889 | 265 |
| 100 | 16 | 1 | 0.450 | 40 | 0.88 [0.74, 0.95] | 0.825 | -0.05 | 0.077 | -0.026 | 147.9 | 0.916 | 150 |
| 100 | 16 | 3 | 1.350 | 40 | 0.72 [0.57, 0.84] | 0.825 | +0.10 | 0.025 | 0.002 | 314.1 | 0.967 | 100 |
| 100 | 16 | 10 | 4.500 | 40 | 0.65 [0.50, 0.78] | 0.825 | +0.17 | 0.000 | nan | 913.9 | 1.000 | 85 |
| 100 | 64 | 0.03 | 0.013 | 40 | 1.00 [0.91, 1.00] | 0.999 | -0.00 | 0.096 | -0.003 | 60.8 | 0.904 | 1918 |
| 100 | 64 | 0.1 | 0.045 | 40 | 0.97 [0.87, 1.00] | 0.999 | +0.02 | 0.088 | 0.001 | 68.6 | 0.912 | 660 |
| 100 | 64 | 0.3 | 0.135 | 40 | 1.00 [0.91, 1.00] | 0.999 | -0.00 | 0.082 | -0.002 | 87.7 | 0.918 | 290 |
| 100 | 64 | 1 | 0.450 | 40 | 1.00 [0.91, 1.00] | 0.999 | -0.00 | 0.076 | 0.003 | 148.6 | 0.928 | 150 |
| 100 | 64 | 3 | 1.350 | 40 | 1.00 [0.91, 1.00] | 0.999 | -0.00 | 0.020 | -0.001 | 334.2 | 0.981 | 110 |
| 100 | 64 | 10 | 4.500 | 40 | 1.00 [0.91, 1.00] | 0.999 | -0.00 | 0.000 | nan | 1160.2 | 1.000 | 105 |
| 100 | 256 | 0.03 | 0.013 | 40 | 1.00 [0.91, 1.00] | 1.000 | -0.00 | 0.089 | 0.000 | 61.5 | 0.911 | 1980 |
| 100 | 256 | 0.1 | 0.045 | 40 | 0.97 [0.87, 1.00] | 1.000 | +0.02 | 0.094 | 0.001 | 64.4 | 0.906 | 625 |
| 100 | 256 | 0.3 | 0.135 | 40 | 1.00 [0.91, 1.00] | 1.000 | -0.00 | 0.089 | -0.000 | 82.6 | 0.911 | 275 |
| 100 | 256 | 1 | 0.450 | 40 | 1.00 [0.91, 1.00] | 1.000 | -0.00 | 0.075 | 0.001 | 144.1 | 0.928 | 145 |
| 100 | 256 | 3 | 1.350 | 40 | 1.00 [0.91, 1.00] | 1.000 | -0.00 | 0.026 | 0.001 | 317.5 | 0.977 | 105 |
| 100 | 256 | 10 | 4.500 | 40 | 1.00 [0.91, 1.00] | 1.000 | -0.00 | 0.000 | nan | 996.0 | 1.000 | 100 |
| 400 | 16 | 0.03 | 0.005 | 40 | 0.95 [0.83, 0.99] | 0.959 | +0.01 | 0.177 | -0.024 | 90.2 | 0.814 | 2625 |
| 400 | 16 | 0.1 | 0.018 | 40 | 0.90 [0.77, 0.96] | 0.959 | +0.06 | 0.178 | 0.007 | 93.3 | 0.802 | 715 |
| 400 | 16 | 0.3 | 0.052 | 40 | 0.97 [0.87, 1.00] | 0.959 | -0.02 | 0.158 | -0.015 | 129.8 | 0.839 | 410 |
| 400 | 16 | 1 | 0.175 | 40 | 0.95 [0.83, 0.99] | 0.959 | +0.01 | 0.167 | 0.026 | 204.8 | 0.830 | 200 |
| 400 | 16 | 3 | 0.525 | 40 | 0.93 [0.80, 0.97] | 0.959 | +0.03 | 0.139 | -0.012 | 473.2 | 0.875 | 155 |
| 400 | 16 | 10 | 1.750 | 40 | 0.95 [0.83, 0.99] | 0.959 | +0.01 | 0.023 | -0.004 | 1321.5 | 0.965 | 120 |
| 400 | 64 | 0.03 | 0.005 | 40 | 1.00 [0.91, 1.00] | 1.000 | -0.00 | 0.190 | -0.009 | 80.4 | 0.810 | 2350 |
| 400 | 64 | 0.1 | 0.018 | 40 | 1.00 [0.91, 1.00] | 1.000 | -0.00 | 0.192 | 0.002 | 93.3 | 0.809 | 855 |
| 400 | 64 | 0.3 | 0.052 | 40 | 1.00 [0.91, 1.00] | 1.000 | -0.00 | 0.179 | 0.002 | 125.0 | 0.823 | 395 |
| 400 | 64 | 1 | 0.175 | 40 | 1.00 [0.91, 1.00] | 1.000 | -0.00 | 0.173 | 0.001 | 208.3 | 0.833 | 210 |
| 400 | 64 | 3 | 0.525 | 40 | 1.00 [0.91, 1.00] | 1.000 | -0.00 | 0.137 | -0.004 | 455.2 | 0.884 | 150 |
| 400 | 64 | 10 | 1.750 | 40 | 1.00 [0.91, 1.00] | 1.000 | -0.00 | 0.023 | 0.002 | 1263.9 | 0.969 | 120 |

Local nucleation under migration (islands whose winner is local-ancestry). q = local-establishment rate per island / m = 0 p_N; arrival exposure and replacement fraction averaged over the locally-founded islands only.

| N | I | mN | x | mN·T_nuc (expected arrivals) | q | arrivals before local est. (mean) | replacement fraction at local est. (mean) | median local est. gen |
|---|---|---|---|---|---|---|---|---|
| 100 | 16 | 0.03 | 0.013 | 1.3 | 0.88 | 1.5 | 0.000 | 45 |
| 100 | 16 | 0.1 | 0.045 | 4.5 | 0.77 | 4.8 | 0.002 | 45 |
| 100 | 16 | 0.3 | 0.135 | 13.5 | 0.86 | 15.3 | 0.003 | 50 |
| 100 | 16 | 1 | 0.450 | 45.0 | 0.74 | 60.6 | 0.052 | 55 |
| 100 | 16 | 3 | 1.350 | 135.0 | 0.24 | 230.4 | 0.231 | 80 |
| 100 | 16 | 10 | 4.500 | 450.0 | 0.00 | nan | nan | - |
| 100 | 64 | 0.03 | 0.013 | 1.3 | 0.94 | 1.5 | 0.000 | 45 |
| 100 | 64 | 0.1 | 0.045 | 4.5 | 0.86 | 4.6 | 0.001 | 45 |
| 100 | 64 | 0.3 | 0.135 | 13.5 | 0.80 | 14.5 | 0.009 | 45 |
| 100 | 64 | 1 | 0.450 | 45.0 | 0.73 | 63.7 | 0.054 | 60 |
| 100 | 64 | 3 | 1.350 | 135.0 | 0.19 | 262.0 | 0.275 | 90 |
| 100 | 64 | 10 | 4.500 | 450.0 | 0.00 | nan | nan | - |
| 100 | 256 | 0.03 | 0.013 | 1.3 | 0.87 | 1.3 | 0.001 | 40 |
| 100 | 256 | 0.1 | 0.045 | 4.5 | 0.91 | 4.6 | 0.005 | 45 |
| 100 | 256 | 0.3 | 0.135 | 13.5 | 0.87 | 14.9 | 0.008 | 45 |
| 100 | 256 | 1 | 0.450 | 45.0 | 0.73 | 67.3 | 0.052 | 65 |
| 100 | 256 | 3 | 1.350 | 135.0 | 0.25 | 270.3 | 0.301 | 90 |
| 100 | 256 | 10 | 4.500 | 450.0 | 0.00 | nan | nan | - |
| 400 | 16 | 0.03 | 0.005 | 2.1 | 0.97 | 2.3 | 0.001 | 70 |
| 400 | 16 | 0.1 | 0.018 | 7.0 | 0.98 | 8.1 | 0.000 | 72 |
| 400 | 16 | 0.3 | 0.052 | 21.0 | 0.87 | 24.3 | 0.008 | 75 |
| 400 | 16 | 1 | 0.175 | 70.0 | 0.92 | 86.5 | 0.037 | 80 |
| 400 | 16 | 3 | 0.525 | 210.0 | 0.77 | 391.5 | 0.206 | 130 |
| 400 | 16 | 10 | 1.750 | 700.0 | 0.13 | 1069.9 | 0.446 | 105 |
| 400 | 64 | 0.03 | 0.005 | 2.1 | 1.05 | 2.3 | 0.001 | 70 |
| 400 | 64 | 0.1 | 0.018 | 7.0 | 1.06 | 7.6 | 0.005 | 70 |
| 400 | 64 | 0.3 | 0.052 | 21.0 | 0.98 | 24.0 | 0.011 | 75 |
| 400 | 64 | 1 | 0.175 | 70.0 | 0.95 | 92.5 | 0.040 | 90 |
| 400 | 64 | 3 | 0.525 | 210.0 | 0.75 | 383.1 | 0.213 | 125 |
| 400 | 64 | 10 | 1.750 | 700.0 | 0.13 | 1126.7 | 0.432 | 110 |

Crossing of q = 1/2 (log-linear interpolation of q pooled over I at each (N, mN)) under each candidate control:

| N | mN·T_nuc/N at q = 1/2 | expected arrivals mN·T_nuc at q = 1/2 | measured arrivals before local est. at q = 1/2 | m = mN/N at q = 1/2 |
|---|---|---|---|---|
| 100 | 0.75 | 75 | 127 | 0.0166 |
| 400 | 0.86 | 345 | 597 | 0.0123 |

Collapse test: P(efficient) = R0 * sigmoid(a + b log c) for control c, pooled over all (N, I) cells; deviance (lower is better):

- mN·T_nuc/N: deviance 387.8 (a 6.70, b 0.36)
- arrival exposure: deviance 385.3 (a -15.81, b 4.92)
- replacement fraction: deviance 388.5 (a 5.92, b 1.23)

## 5. Merge test

| source | merges | clean two-type | larger won (clean) | minority won (clean) | mixed/unresolved | median gens to freeze (clean) | median larger share (clean) | near-ties (share < 0.6) |
|---|---|---|---|---|---|---|---|---|
| ctrl A | 1 | 1 | 1 | 0 | 0 | 35 | 0.680 | 0 |
| ctrl halfAB | 160 | 160 | 131 | 29 | 0 | 50 | 0.514 | 151 |
| ctrl minorB | 146 | 146 | 146 | 0 | 0 | 20 | 0.984 | 0 |
| nat iid | 31 | 30 | 30 | 0 | 0 | 40 | 0.793 | 2 |
| sep AB | 236 | 235 | 227 | 8 | 0 | 30 | 0.748 | 47 |

## Verdicts (predictions/2026-10-05-rival-islands.md)

| # | prediction | outcome |
|---|---|---|
| 1 | separation long-lived: hazard < 1e-5 at mN <= 1; both present >= 0.8 at mN <= 1, >= 0.5 at mN = 10 | **Failed, falsifier fired.** Both present at the horizon in 0/40 runs in every mN = 1 and mN = 10 cell; at mN = 0.1, 2/40 to 40/40. First-loss hazard 5e-5 to 7.5e-4 at mN = 1, 5e-3 to 1.4e-2 at mN = 10. "Lifetimes shorten with flux" held, strongly superlinearly |
| 2 | majority set at nucleation; A (FairBot family) majority >= 0.8; falsifier: B majority > 0.3 or Spearman < 0.3 | **Failed, falsifier fired narrowly** (B majority 343/1,080 = 0.32). A majority 0.67; run-level nucleation rule right in 358/511 decided runs (0.70; 569 undecided). Spearman with measured rates 0.70 (that clause held) |
| 3 | natural separation 0.01-0.05 at (100, 256) n = 9, higher at n = 12 and at I = 1,024, consistent with 1 - (1 - p_B)^I, flat in mN <= 1; falsifier: a fall from 256 to 1,024 | **Falsifier not fired; most clauses failed.** Growth in I and n held at mN = 0.1. The band failed (1/300 = 0.003). 1 - (1 - p_B)^I predicts *ever separated* (35/300 vs 0.098; 20/100 vs 0.18), not separated at the horizon (outside the interval at 4 of 6 mN = 0.1 cells). Flatness in mN failed: 0/300 at mN = 1 in every cell |
| 4 | efficient fraction flat while mN·T_nuc/N < 0.1 and falls once > 1; ICC < 0.1 in the flat region; falsifier: a fall > 0.2 while < 0.1 | **Held on the falsifier, the flat clause and ICC** (max fall 0.06; abs(ICC) < 0.03). **Fall clause partly held:** run-level efficiency falls only where independent trials leave room ((100, 16): -0.10 at x = 1.35, -0.17 at x = 4.5; (400, 16) none at x = 1.75; I >= 64 at the ceiling). Island-level local nucleation q has the predicted shape: q = 1/2 at x = 0.75 (N = 100) and 0.86 (N = 400) |
| 5 | larger network wins >= 0.9 of clean two-type merges; falsifier: minority > 0.3 | **Held.** 535/572 clean merges (0.935); 372/372 at larger share >= 0.6; minority wins only near ties (share <= 0.56). All resolved within 115 generations |
| S1 | minority-island hazard = mN·rho_DD(100) within x3 | **Failed** at mN >= 1 (14-18x faster at mN = 1, ~200x at mN = 10); held at mN = 0.1 (ratio 0.27-1.03) |
| S2 | at mN = 10 one network lost within 1e3 generations in >= 0.8 of runs | **Held** (item 2: 360/360; control c: all) |
| S3 | losses dominated by nucleation; both present >= 0.8 at mN = 0.1 in every item-2 cell | **Failed** (415 of 485 losses at mN <= 1 after generation 1e3; pairs 1-2 at I = 64, 256: 2-22 of 40) |
| S4 | N = 200: no loss at mN = 1; at mN = 10 half/half loses >= 0.5, minority <= 0.2 | **Failed on two clauses** (minority preset: 1/40 lost at mN = 1 and 40/40 at mN = 10). The central contrast held: at mN = 1 the hazard falls ~1,000x from N = 100 to 200 |

## Deviations and definitions applied after seeing data

- *Unresolved* at the horizon is assigned by holders, as predeclared: an island held by a class outside the tagged networks. The kernel's
  own "unresolved" status (some island not locally frozen at the last check) is almost always transient migrants and is not used.
- Item 4: the efficient fraction is at its ceiling for I >= 64, so the island-level local-nucleation rate q (relative to m = 0) and its
  q = 1/2 crossing were added as the informative response; the predeclared logistic collapse on the run-level efficient fraction is
  reported but is uninformative (deviances 385-389).
- Item 4's arrival exposure and replacement fraction are reported over locally founded islands (the islands whose nucleation is being
  diluted); means over all established islands are dominated by colonized islands (replacement ~0.9 at every mN).
- The N = 200 control cells (addendum S4) were added after partial item-2 data, predeclared in a committed addendum before they ran.

