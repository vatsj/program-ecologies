# Almost all seeds? Persistence without mutation along N >> I and I >> N (2026-10-04)

Spec `specs/2026-10-04-almost-all-seeds.md`; predictions `predictions/2026-10-04-almost-all-seeds.md`; code `src/almost_all_seeds.py`. PD, w = 0.3. Raw rows: `runs/almost-all-seeds.json` (static, islands, assays).

## Object 1: replicator from x0 = prior

"first" = the integrator's endpoint (`chain.replicator`, shares below 1e-9 pruned). "closed" = after re-injecting every class with positive growth rate at 1e-6 and re-integrating until none has (the true flow keeps positive coordinates positive). Persistence, neutral classes, perturbations and tolerance checks refer to the closed endpoint. Support = classes with share >= 1e-6.

| arm | n | prior | first P(C,C) | first max growth (class) | rounds | closed P(C,C) | persistent | support size | top support | neutral extinct classes | perturbations recovered | tolerance x10 and /10 same | residual |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| modal | 6 | length | 1.0000 | 0  | 0 | 1.0000 | yes | 7 | `BOX1(THEM(THEM))` 0.23; `BOX(THEM(THEM))` 0.22; `BOX(THEM(ME))` 0.22 | 1 | 7/7 | yes | 0e+00 |
| modal | 6 | base 2 | 1.0000 | 0  | 0 | 1.0000 | yes | 8 | `BOX(THEM(THEM))` 0.21; `BOX(THEM(ME))` 0.21; `BOX1(THEM(ME))` 0.20 | 0 | 5/5 | yes | 0e+00 |
| modal | 6 | base 4 | 1.0000 | 0  | 0 | 1.0000 | yes | 8 | `BOX(THEM(THEM))` 0.22; `BOX1(THEM(THEM))` 0.22; `BOX(THEM(ME))` 0.22 | 0 | 5/5 | yes | 0e+00 |
| modal | 6 | base 8 | 1.0000 | 0  | 0 | 1.0000 | yes | 7 | `BOX1(THEM(THEM))` 0.24; `BOX(THEM(THEM))` 0.23; `BOX(THEM(ME))` 0.23 | 1 | 7/7 | yes | 0e+00 |
| modal | 6 | temper 0.5 | 1.0000 | 0  | 0 | 1.0000 | yes | 8 | `BOX(THEM(THEM))` 0.21; `BOX(THEM(ME))` 0.21; `BOX1(THEM(ME))` 0.20 | 0 | 5/5 | yes | 0e+00 |
| modal | 6 | temper 2 | 1.0000 | 0  | 0 | 1.0000 | yes | 7 | `BOX1(THEM(THEM))` 0.25; `BOX(THEM(THEM))` 0.24; `BOX(THEM(ME))` 0.24 | 1 | 7/7 | yes | 0e+00 |
| modal | 6 | uniform-programs | 1.0000 | 0  | 0 | 1.0000 | yes | 8 | `BOX(THEM(THEM))` 0.22; `BOX(THEM(ME))` 0.21; `BOX1(THEM(ME))` 0.20 | 0 | 5/5 | yes | 0e+00 |
| modal | 6 | uniform-classes | 1.0000 | 0  | 0 | 1.0000 | yes | 8 | `BOX(THEM(THEM))` 0.21; `BOX(THEM(ME))` 0.19; `BOX1(THEM(ME))` 0.18 | 0 | 5/5 | yes | 0e+00 |
| modal | 7 | length | 1.0000 | 0  | 0 | 1.0000 | yes | 22 | `BOX1(THEM(THEM))` 0.23; `BOX(THEM(ME))` 0.22; `BOX1(THEM(ME))` 0.22 | 17 | 23/23 | yes | 0e+00 |
| modal | 7 | base 2 | 1.0000 | 0  | 0 | 1.0000 | yes | 23 | `BOX1(THEM(THEM))` 0.21; `BOX(THEM(ME))` 0.20; `BOX1(THEM(ME))` 0.20 | 16 | 22/22 | yes | 0e+00 |
| modal | 7 | base 4 | 1.0000 | 0  | 0 | 1.0000 | yes | 23 | `BOX1(THEM(THEM))` 0.22; `BOX(THEM(ME))` 0.21; `BOX(THEM(THEM))` 0.21 | 16 | 22/22 | yes | 0e+00 |
| modal | 7 | base 8 | 1.0000 | 0  | 0 | 1.0000 | yes | 22 | `BOX1(THEM(THEM))` 0.24; `BOX(THEM(ME))` 0.23; `BOX(THEM(THEM))` 0.23 | 17 | 23/23 | yes | 0e+00 |
| modal | 7 | temper 0.5 | 1.0000 | 0  | 0 | 1.0000 | yes | 23 | `BOX1(THEM(THEM))` 0.21; `BOX(THEM(ME))` 0.20; `BOX1(THEM(ME))` 0.20 | 16 | 22/22 | yes | 0e+00 |
| modal | 7 | temper 2 | 1.0000 | 0  | 0 | 1.0000 | yes | 12 | `BOX1(THEM(THEM))` 0.25; `BOX(THEM(ME))` 0.24; `BOX(THEM(THEM))` 0.24 | 27 | 33/33 | yes | 0e+00 |
| modal | 7 | uniform-programs | 1.0000 | 0  | 0 | 1.0000 | yes | 23 | `BOX1(THEM(THEM))` 0.21; `BOX(THEM(ME))` 0.20; `BOX1(THEM(ME))` 0.19 | 16 | 22/22 | yes | 0e+00 |
| modal | 7 | uniform-classes | 1.0000 | 0  | 0 | 1.0000 | yes | 39 | `and(BOX(THEM(ME)),BOX(THEM(THEM)))` 0.06; `BOX(THEM(^BOX(THEM(THEM))))` 0.05; `BOX(THEM(^BOX1(THEM(ME))))` 0.05 | 0 | 5/5 | yes | 0e+00 |
| modal | 8 | length | 1.0000 | 0.11 `or(BOXD(THEM(ME)),BOX(THEM(^D)))` | 1 | 1.0000 | yes | 50 | `BOX(THEM(ME))` 0.28; `BOX1(THEM(ME))` 0.28; `BOX1(THEM(THEM))` 0.18 | 53 | 46/46 | yes | 0e+00 |
| modal | 8 | base 2 | 1.0000 | 0  | 0 | 1.0000 | yes | 51 | `BOX(THEM(ME))` 0.24; `BOX1(THEM(ME))` 0.23; `BOX1(THEM(THEM))` 0.15 | 52 | 46/46 | yes | 0e+00 |
| modal | 8 | base 4 | 1.0000 | 0  | 0 | 1.0000 | yes | 51 | `BOX(THEM(ME))` 0.27; `BOX1(THEM(ME))` 0.27; `BOX1(THEM(THEM))` 0.16 | 52 | 46/46 | yes | 0e+00 |
| modal | 8 | base 8 | 1.0000 | 0.07 `or(BOXD(THEM(ME)),BOX(THEM(^D)))` | 1 | 1.0000 | yes | 50 | `BOX(THEM(ME))` 0.27; `BOX1(THEM(ME))` 0.27; `BOX1(THEM(THEM))` 0.20 | 53 | 46/46 | yes | 0e+00 |
| modal | 8 | temper 0.5 | 1.0000 | 0  | 0 | 1.0000 | yes | 51 | `BOX(THEM(ME))` 0.25; `BOX1(THEM(ME))` 0.24; `BOX1(THEM(THEM))` 0.15 | 52 | 46/46 | yes | 0e+00 |
| modal | 8 | temper 2 | 1.0000 | 0.032 `or(BOXD(THEM(ME)),BOX(THEM(^D)))` | 1 | 1.0000 | yes | 12 | `BOX(THEM(ME))` 0.26; `BOX1(THEM(ME))` 0.26; `BOX1(THEM(THEM))` 0.23 | 91 | 46/46 | yes | 0e+00 |
| modal | 8 | uniform-programs | 1.0000 | 0  | 0 | 1.0000 | yes | 51 | `BOX(THEM(ME))` 0.22; `BOX1(THEM(ME))` 0.22; `BOX1(THEM(THEM))` 0.15 | 52 | 46/46 | yes | 0e+00 |
| modal | 8 | uniform-classes | 1.0000 | 0  | 0 | 1.0000 | yes | 103 | `and(BOX(THEM(ME)),BOX(THEM(THEM)))` 0.07; `and(BOX(THEM(ME)),BOX(THEM(^C)))` 0.06; `BOX(THEM(^BOX(THEM(THEM))))` 0.06 | 0 | 5/5 | yes | 0e+00 |
| modal | 9 | length | 1.0000 | 0.11 `or(BOXD(THEM(ME)),BOX(THEM(^D)))` | 1 | 1.0000 | yes | 82 | `BOX(THEM(ME))` 0.28; `BOX1(THEM(ME))` 0.28; `BOX1(THEM(THEM))` 0.17 | 80 | 46/46 | yes | 0e+00 |
| modal | 9 | base 2 | 1.0000 | 0  | 0 | 1.0000 | yes | 83 | `BOX(THEM(ME))` 0.25; `BOX1(THEM(ME))` 0.24; `BOX1(THEM(THEM))` 0.15 | 79 | 46/46 | yes | 0e+00 |
| modal | 9 | base 4 | 1.0000 | 0  | 0 | 1.0000 | yes | 83 | `BOX(THEM(ME))` 0.27; `BOX1(THEM(ME))` 0.27; `BOX1(THEM(THEM))` 0.16 | 79 | 46/46 | yes | 0e+00 |
| modal | 9 | base 8 | 1.0000 | 0.071 `or(BOXD(THEM(ME)),BOX(THEM(^D)))` | 1 | 1.0000 | yes | 79 | `BOX(THEM(ME))` 0.27; `BOX1(THEM(ME))` 0.27; `BOX1(THEM(THEM))` 0.20 | 83 | 46/46 | yes | 0e+00 |
| modal | 9 | temper 0.5 | 1.0000 | 0  | 0 | 1.0000 | yes | 83 | `BOX(THEM(ME))` 0.25; `BOX1(THEM(ME))` 0.25; `BOX1(THEM(THEM))` 0.15 | 79 | 46/46 | yes | 0e+00 |
| modal | 9 | temper 2 | 1.0000 | 0.032 `or(BOXD(THEM(ME)),BOX(THEM(^D)))` | 1 | 1.0000 | yes | 12 | `BOX(THEM(ME))` 0.26; `BOX1(THEM(ME))` 0.26; `BOX1(THEM(THEM))` 0.23 | 150 | 46/46 | yes | 0e+00 |
| modal | 9 | uniform-programs | 1.0000 | 0  | 0 | 1.0000 | yes | 83 | `BOX(THEM(ME))` 0.25; `BOX1(THEM(ME))` 0.24; `BOX1(THEM(THEM))` 0.15 | 79 | 46/46 | yes | 0e+00 |
| modal | 9 | uniform-classes | 1.0000 | 0  | 0 | 1.0000 | yes | 162 | `and(BOX(THEM(ME)),BOX(THEM(THEM)))` 0.06; `and(BOX(THEM(ME)),BOX(THEM(^C)))` 0.05; `BOX(THEM(^BOX(THEM(THEM))))` 0.05 | 0 | 5/5 | yes | 0e+00 |
| W0 | 6 | length | 0.0000 | 0.78 `C` | 1 | 0.0000 | yes | 5 | `D` 0.84; `THEM(^D)` 0.11; `THEM(ME)` 0.03 | 0 | 5/5 | yes | 0e+00 |
| W0 | 6 | base 2 | 0.0000 | 0.52 `C` | 1 | 0.0000 | yes | 5 | `D` 0.77; `THEM(^D)` 0.15; `THEM(ME)` 0.05 | 0 | 5/5 | yes | 1e-16 |
| W0 | 6 | base 4 | 0.0000 | 1.1 `C` | 1 | 0.0000 | yes | 5 | `D` 0.90; `THEM(^D)` 0.06; `THEM(ME)` 0.03 | 0 | 5/5 | yes | 0e+00 |
| W0 | 6 | base 8 | 0.0000 | 1.2 `C` | 1 | 0.0000 | yes | 5 | `D` 0.92; `THEM(^D)` 0.05; `THEM(ME)` 0.02 | 0 | 5/5 | yes | 0e+00 |
| W0 | 6 | temper 0.5 | 0.0000 | 0.59 `C` | 1 | 0.0000 | yes | 5 | `D` 0.79; `THEM(^D)` 0.13; `THEM(ME)` 0.04 | 0 | 5/5 | yes | 0e+00 |
| W0 | 6 | temper 2 | 0.0000 | 0  | 0 | 0.0000 | yes | 4 | `D` 0.70; `THEM(^D)` 0.26; `THEM(ME)` 0.02 | 1 | 7/7 | yes | 0e+00 |
| W0 | 6 | uniform-programs | 0.0000 | 0.0078 `not(THEM(^C))` | 1 | 0.0000 | yes | 5 | `D` 0.62; `THEM(^D)` 0.27; `THEM(ME)` 0.05 | 1 | 7/7 | yes | 2e-16 |
| W0 | 6 | uniform-classes | 0.0000 | -1.1e-16  | 0 | 0.0000 | yes | 5 | `D` 0.70; `THEM(^D)` 0.17; `and(THEM(ME),D)` 0.09 | 0 | 5/5 | yes | 1e-16 |
| W0 | 7 | length | 0.0000 | 1.9 `C` | 3 | 0.0000 | yes | 3 | `D` 0.70; `THEM(^D)` 0.30; `THEM(^THEM(^D))` 0.00 | 5 | 11/11 | yes | 0e+00 |
| W0 | 7 | base 2 | 0.0000 | 1.8 `C` | 3 | 0.0000 | yes | 3 | `D` 0.69; `THEM(^D)` 0.31; `THEM(^THEM(^D))` 0.00 | 5 | 11/11 | yes | 0e+00 |
| W0 | 7 | base 4 | 0.0000 | 1.9 `C` | 3 | 0.0000 | yes | 3 | `D` 0.70; `THEM(^D)` 0.30; `THEM(^THEM(^D))` 0.00 | 5 | 11/11 | yes | 1e-16 |
| W0 | 7 | base 8 | 0.0000 | 1.9 `C` | 3 | 0.0000 | yes | 3 | `D` 0.70; `THEM(^D)` 0.30; `THEM(^THEM(^D))` 0.00 | 5 | 11/11 | yes | 0e+00 |
| W0 | 7 | temper 0.5 | 0.0000 | 1.8 `C` | 3 | 0.0000 | yes | 3 | `D` 0.69; `THEM(^D)` 0.30; `THEM(^THEM(^D))` 0.00 | 5 | 11/11 | yes | 0e+00 |
| W0 | 7 | temper 2 | 0.0000 | 0.00015 `THEM(^THEM(^C))` | 14 | 0.0000 | yes | 6 | `D` 0.99; `and(THEM(ME),D)` 0.01; `THEM(^D)` 0.00 | 2 | 8/8 | yes | 2e-16 |
| W0 | 7 | uniform-programs | 0.0000 | 1.8 `C` | 3 | 0.0000 | yes | 6 | `D` 0.75; `THEM(^D)` 0.25; `THEM(^THEM(^D))` 0.00 | 2 | 8/8 | yes | 0e+00 |
| W0 | 7 | uniform-classes | 0.0000 | 2.2e-16  | 0 | 0.0000 | yes | 8 | `D` 0.66; `THEM(^D)` 0.20; `THEM(^THEM(^D))` 0.08 | 0 | 5/5 | yes | 2e-16 |
| L6R | 6 | length | 0.0000 | 0.22 `not(THEM(ME))` | 1 | 0.0000 | yes | 21 | `D` 0.71; `THEM(^D)` 0.23; `THEM(ME)` 0.03 | 0 | 5/5 | yes | 1e-16 |
| L6R | 6 | base 2 | 0.0000 | -1.1e-16  | 0 | 0.0000 | yes | 21 | `D` 0.64; `THEM(^D)` 0.26; `THEM(THEM)` 0.03 | 0 | 5/5 | yes | 1e-16 |
| L6R | 6 | base 4 | 0.0000 | 0.26 `not(THEM(ME))` | 1 | 0.0000 | yes | 21 | `D` 0.71; `THEM(^D)` 0.21; `THEM(ME)` 0.03 | 0 | 5/5 | yes | 1e-16 |
| L6R | 6 | base 8 | 0.0000 | 0.84 `C` | 1 | 0.0000 | yes | 21 | `D` 0.85; `THEM(^D)` 0.11; `THEM(ME)` 0.03 | 0 | 5/5 | yes | 2e-16 |
| L6R | 6 | temper 0.5 | 0.0000 | 0.068 `not(THEM(^C))` | 1 | 0.0000 | yes | 21 | `D` 0.65; `THEM(^D)` 0.26; `THEM(ME)` 0.03 | 0 | 5/5 | yes | 0e+00 |
| L6R | 6 | temper 2 | 0.0000 | -2.2e-16  | 0 | 0.0000 | yes | 6 | `D` 0.89; `THEM(^D)` 0.09; `THEM(THEM)` 0.01 | 15 | 21/21 | yes | 2e-16 |
| L6R | 6 | uniform-programs | 0.0000 | 0  | 0 | 0.0000 | yes | 21 | `D` 0.74; `THEM(^D)` 0.19; `THEM(THEM)` 0.02 | 0 | 5/5 | yes | 0e+00 |
| L6R | 6 | uniform-classes | 0.0000 | 0.07 `not(THEM(^C))` | 1 | 0.0000 | yes | 21 | `D` 0.33; `and(X,THEM(^D))` 0.17; `and(X,THEM(ME))` 0.12 | 0 | 5/5 | yes | 2e-16 |

Extinction order under the length prior (fixed-step integration, no pruning; time to share < 1e-6):

| arm | n | ALLC extinct at t | D extinct at t | cooperative family >= 0.99 at t | ALLC first |
|---|---|---|---|---|---|
| modal | 6 | 14.7 | 58.0 | 48.8 | True |
| modal | 7 | 14.7 | 56.6 | 47.4 | True |
| modal | 8 | 14.8 | 55.9 | 46.6 | True |
| modal | 9 | 14.8 | 55.2 | 46.0 | True |
| W0 | 6 | 14.3 | never (t <= 4000) | never (t <= 4000) | True |
| W0 | 7 | 14.3 | 186.5 | 277.4 | True |
| L6R | 6 | 14.0 | never (t <= 4000) | never (t <= 4000) | True |

Basin lines, x0 = (1 - t) * length prior + t * uniform (closed endpoints): P(C,C) at t = 0, 0.25, 0.5, 0.75, 1.

| arm | n | uniform over | P(C,C) along t | largest t with every t' <= t efficient |
|---|---|---|---|---|
| modal | 6 | classes | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 1.0 |
| modal | 6 | programs | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 1.0 |
| modal | 7 | classes | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 1.0 |
| modal | 7 | programs | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 1.0 |
| modal | 8 | classes | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 1.0 |
| modal | 8 | programs | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 1.0 |
| modal | 9 | classes | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 1.0 |
| modal | 9 | programs | 1.00 / 1.00 / 1.00 / 1.00 / 1.00 | 1.0 |
| W0 | 6 | classes | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | none |
| W0 | 6 | programs | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | none |
| W0 | 7 | classes | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | none |
| W0 | 7 | programs | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | none |
| L6R | 6 | classes | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | none |
| L6R | 6 | programs | 0.00 / 0.00 / 0.00 / 0.00 / 0.00 | none |

## Object 2: eps = 0 islands, iid seeding from mu

Complete island graph, mN = 1 (one migrant per island per generation; a generation = I*N births), horizon 1e5 generations, checks every 20. Categories: CF = certified, outcome-frozen (all surviving classes pairwise payoff-identical); CS = certified, separated (islands monomorphic, every cross-island migrant strictly disadvantaged); MS = metastable (monomorphic at horizon, some neutral or advantaged migrant); UN = unresolved. Efficient = mean island P(C,C) >= 0.95 at stop. Eff fraction = efficient (CF/CS/MS) / runs, Wilson 95%. P(no R), P(no unfakeable coop), P(faker) are per-island seed probabilities from mu, times I.

### Modal arm (n = 6, all box kinds)

mu(R = `BOX(THEM(ME))`) = 0.0050; mu(unfakeable cooperative family) = 0.0149; mu(fakers of R) = 0.0000.

| N | I | mN | runs | CF / CS / MS / UN | efficient / defecting / other | eff fraction [95%] | mean final P(C,C) | median stop gen | P(no R) * I | P(no unfakeable coop) * I | P(faker) * I | islands seeded with R / faker | top frozen classes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 4 | 1 | 40 | 40 / 0 / 0 / 0 | 10 / 30 / 0 | 0.25 [0.14, 0.40] | 0.250 | 40 | 2.4 | 0.9 | 0 | 0.39 / 0.00 | `D` 0.74; `BOX1(THEM(ME))` 0.09; `BOX(THEM(ME))` 0.08 |
| 400 | 4 | 1 | 20 | 20 / 0 / 0 / 0 | 9 / 11 / 0 | 0.45 [0.26, 0.66] | 0.450 | 70 | 0.55 | 0.01 | 0 | 0.80 / 0.00 | `D` 0.54; `BOX(THEM(THEM))` 0.20; `BOX(THEM(ME))` 0.13 |
| 1600 | 4 | 1 | 20 | 20 / 0 / 0 / 0 | 16 / 4 / 0 | 0.80 [0.58, 0.92] | 0.800 | 290 | 0.0014 | 1.6e-10 | 0 | 1.00 / 0.00 | `BOX(THEM(THEM))` 0.28; `BOX1(THEM(THEM))` 0.22; `D` 0.20 |
| 6400 | 4 | 1 | 40 | 40 / 0 / 0 / 0 | 40 / 0 / 0 | 1.00 [0.91, 1.00] | 1.000 | 480 | 6.4e-14 | 1e-41 | 0 | 1.00 / 0.00 | `BOX(THEM(ME))` 0.26; `BOX1(THEM(THEM))` 0.24; `BOX(THEM(THEM))` 0.21 |
| 100 | 16 | 1 | 20 | 20 / 0 / 0 / 0 | 15 / 5 / 0 | 0.75 [0.53, 0.89] | 0.750 | 220 | 9.7 | 3.6 | 0 | 0.42 / 0.00 | `BOX(THEM(THEM))` 0.25; `D` 0.25; `BOX1(THEM(THEM))` 0.22 |
| 100 | 64 | 1 | 20 | 20 / 0 / 0 / 0 | 20 / 0 / 0 | 1.00 [0.84, 1.00] | 1.000 | 270 | 39 | 14 | 0 | 0.39 / 0.00 | `BOX(THEM(THEM))` 0.28; `BOX(THEM(ME))` 0.25; `BOX1(THEM(ME))` 0.24 |
| 100 | 256 | 1 | 40 | 40 / 0 / 0 / 0 | 40 / 0 / 0 | 1.00 [0.91, 1.00] | 1.000 | 280 | 1.6e+02 | 57 | 0 | 0.39 / 0.00 | `BOX(THEM(ME))` 0.24; `BOX1(THEM(THEM))` 0.23; `BOX(THEM(THEM))` 0.22 |
| 200 | 8 | 1 | 20 | 20 / 0 / 0 / 0 | 14 / 6 / 0 | 0.70 [0.48, 0.85] | 0.700 | 180 | 3 | 0.4 | 0 | 0.66 / 0.00 | `D` 0.30; `BOX1(THEM(ME))` 0.28; `BOX(THEM(THEM))` 0.14 |
| 400 | 16 | 1 | 20 | 20 / 0 / 0 / 0 | 20 / 0 / 0 | 1.00 [0.84, 1.00] | 1.000 | 360 | 2.2 | 0.04 | 0 | 0.88 / 0.00 | `BOX(THEM(ME))` 0.27; `BOX1(THEM(ME))` 0.26; `BOX(THEM(THEM))` 0.24 |
| 800 | 32 | 1 | 20 | 20 / 0 / 0 / 0 | 20 / 0 / 0 | 1.00 [0.84, 1.00] | 1.000 | 490 | 0.6 | 0.0002 | 0 | 0.98 / 0.00 | `BOX(THEM(THEM))` 0.30; `BOX1(THEM(THEM))` 0.24; `BOX1(THEM(ME))` 0.21 |
| 400 | 4 | 0 | 20 | 20 / 0 / 0 / 0 | 0 / 0 / 0 | (per island below) | 0.138 | 60 | 0.55 | 0.01 | 0 | 0.85 / 0.00 | `D` 0.86; `BOX(THEM(ME))` 0.04; `BOX(THEM(THEM))` 0.04 |
| 100 | 64 | 0 | 20 | 20 / 0 / 0 / 0 | 0 / 0 / 0 | (per island below) | 0.074 | 80 | 39 | 14 | 0 | 0.36 / 0.00 | `D` 0.92; `BOX1(THEM(THEM))` 0.02; `BOX(THEM(THEM))` 0.02 |

No-migration control (mN = 0), per island: (N 400, I 4) 80 islands: efficient 0.14 [0.08, 0.23], defecting 0.86, other 0.00; (N 100, I 64) 1280 islands: efficient 0.07 [0.06, 0.09], defecting 0.93, other 0.00.

Mechanism (modal, mN = 1): global ALLC extinction generation; cooperative islands (>= 90% in cooperative classes other than ALLC) that fell below 50%, before / after global ALLC extinction.

| N | I | ALLC extinct: median / max gen | runs with ALLC never extinct | coop islands lost before / after |
|---|---|---|---|---|
| 100 | 4 | 40 / 40 | 0 | 0 / 0 |
| 400 | 4 | 40 / 60 | 0 | 0 / 0 |
| 1600 | 4 | 40 / 60 | 0 | 0 / 0 |
| 6400 | 4 | 40 / 60 | 0 | 0 / 2 |
| 100 | 16 | 40 / 60 | 0 | 0 / 0 |
| 100 | 64 | 40 / 80 | 0 | 0 / 3 |
| 100 | 256 | 60 / 100 | 1 | 1 / 59 |
| 200 | 8 | 40 / 60 | 0 | 0 / 0 |
| 400 | 16 | 40 / 60 | 0 | 0 / 0 |
| 800 | 32 | 40 / 260 | 0 | 0 / 4 |

Who took those islands (the 13 runs with losses re-run with a loss log, `runs/almost-all-seeds-losses.json`; 13 of 13 reproduced exactly; all 13 ended efficient): `BOX1(THEM(^D))` 49 (after ALLC extinct), `BOX(THEM(^D))` 19 (after ALLC extinct), `BOX1(THEM(^D))` 1 (before). These probe-fakers (D against everything but ALLC) exploit only the fakeable cooperative classes in the cooperative set (`BOX(THEM(^C))`, `BOX1(THEM(^C))` and `not(...)` forms), not FairBot, `BOX(THEM(THEM))` or `BOX1(THEM(ME))`.

### W0 (weak, no X, no `ROLE`, n = 6)

mu(R = `THEM(^C)`) = 0.0020; mu(unfakeable cooperative family) = 0.0000; mu(fakers of R) = 0.0020.

| N | I | mN | runs | CF / CS / MS / UN | efficient / defecting / other | eff fraction [95%] | mean final P(C,C) | median stop gen | P(no R) * I | P(no unfakeable coop) * I | P(faker) * I | islands seeded with R / faker | top frozen classes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 4 | 1 | 40 | 40 / 0 / 0 / 0 | 1 / 39 / 0 | 0.03 [0.00, 0.13] | 0.025 | 20 | 3.3 | 4 | 0.72 | 0.16 / 0.21 | `D` 0.96; `THEM(^C)` 0.03; `THEM(THEM)` 0.01 |
| 400 | 4 | 1 | 20 | 20 / 0 / 0 / 0 | 0 / 20 / 0 | 0.00 [0.00, 0.16] | 0.000 | 40 | 1.8 | 4 | 2.2 | 0.62 / 0.54 | `D` 0.96; `THEM(^D)` 0.01; `THEM(THEM)` 0.01 |
| 1600 | 4 | 1 | 20 | 20 / 0 / 0 / 0 | 3 / 17 / 0 | 0.15 [0.05, 0.36] | 0.150 | 40 | 0.17 | 4 | 3.8 | 0.97 / 0.93 | `D` 0.84; `THEM(^C)` 0.15; `THEM(ME)` 0.01 |
| 6400 | 4 | 1 | 40 | 40 / 0 / 0 / 0 | 10 / 30 / 0 | 0.25 [0.14, 0.40] | 0.250 | 60 | 1.2e-05 | 4 | 4 | 1.00 / 1.00 | `D` 0.71; `THEM(^C)` 0.25; `THEM(^D)` 0.03 |
| 100 | 16 | 1 | 20 | 20 / 0 / 0 / 0 | 4 / 16 / 0 | 0.20 [0.08, 0.42] | 0.200 | 40 | 13 | 16 | 2.9 | 0.17 / 0.14 | `D` 0.79; `THEM(^C)` 0.20; `THEM(THEM)` 0.00 |
| 100 | 64 | 1 | 20 | 20 / 0 / 0 / 0 | 8 / 12 / 0 | 0.40 [0.22, 0.61] | 0.400 | 150 | 52 | 64 | 12 | 0.17 / 0.17 | `D` 0.53; `THEM(^C)` 0.40; `THEM(^D)` 0.07 |
| 100 | 256 | 1 | 40 | 40 / 0 / 0 / 0 | 22 / 18 / 0 | 0.55 [0.40, 0.69] | 0.550 | 360 | 2.1e+02 | 2.6e+02 | 46 | 0.18 / 0.18 | `THEM(^C)` 0.55; `THEM(^D)` 0.23; `D` 0.22 |
| 200 | 8 | 1 | 20 | 20 / 0 / 0 / 0 | 3 / 17 / 0 | 0.15 [0.05, 0.36] | 0.150 | 40 | 5.4 | 8 | 2.6 | 0.35 / 0.39 | `D` 0.84; `THEM(^C)` 0.15; `THEM(ME)` 0.01 |
| 400 | 16 | 1 | 20 | 20 / 0 / 0 / 0 | 3 / 17 / 0 | 0.15 [0.05, 0.36] | 0.150 | 40 | 7.2 | 16 | 8.8 | 0.58 / 0.55 | `D` 0.83; `THEM(^C)` 0.15; `THEM(ME)` 0.01 |
| 800 | 32 | 1 | 20 | 20 / 0 / 0 / 0 | 4 / 16 / 0 | 0.20 [0.08, 0.42] | 0.200 | 70 | 6.6 | 32 | 25 | 0.80 / 0.80 | `D` 0.75; `THEM(^C)` 0.20; `THEM(^D)` 0.04 |
| 400 | 4 | 0 | 20 | 20 / 0 / 0 / 0 | 0 / 0 / 0 | (per island below) | 0.013 | 40 | 1.8 | 4 | 2.2 | 0.62 / 0.56 | `D` 0.97; `THEM(^C)` 0.01; `THEM(^D)` 0.01 |
| 100 | 64 | 0 | 20 | 20 / 0 / 0 / 0 | 0 / 0 / 0 | (per island below) | 0.005 | 40 | 52 | 64 | 12 | 0.17 / 0.18 | `D` 0.99; `THEM(THEM)` 0.00; `THEM(ME)` 0.00 |

No-migration control (mN = 0), per island: (N 400, I 4) 80 islands: efficient 0.01 [0.00, 0.07], defecting 0.99, other 0.00; (N 100, I 64) 1280 islands: efficient 0.00 [0.00, 0.01], defecting 1.00, other 0.00.

### Weak L_6 with X and `ROLE`

mu(R = `THEM(^C)`) = 0.0005; mu(unfakeable cooperative family) = 0.0000; mu(fakers of R) = 0.0016.

| N | I | mN | runs | CF / CS / MS / UN | efficient / defecting / other | eff fraction [95%] | mean final P(C,C) | median stop gen | P(no R) * I | P(no unfakeable coop) * I | P(faker) * I | islands seeded with R / faker | top frozen classes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 4 | 1 | 40 | 40 / 0 / 0 / 0 | 0 / 40 / 0 | 0.00 [0.00, 0.09] | 0.000 | 60 | 3.8 | 4 | 0.6 | 0.02 / 0.12 | `D` 0.99; `THEM(ME)` 0.01 |
| 400 | 4 | 1 | 20 | 20 / 0 / 0 / 0 | 0 / 19 / 1 | 0.00 [0.00, 0.16] | 0.013 | 60 | 3.3 | 3.9 | 1.9 | 0.14 / 0.55 | `D` 0.95; `THEM(^X)` 0.05; `THEM(ME)` 0.00 |
| 1600 | 4 | 1 | 20 | 20 / 0 / 0 / 0 | 1 / 19 / 0 | 0.05 [0.01, 0.24] | 0.050 | 80 | 1.8 | 3.7 | 3.7 | 0.56 / 0.97 | `D` 0.94; `THEM(^C)` 0.05; `THEM(ME)` 0.00 |
| 6400 | 4 | 1 | 40 | 40 / 0 / 0 / 0 | 4 / 32 / 4 | 0.10 [0.04, 0.23] | 0.107 | 120 | 0.15 | 3.1 | 4 | 0.97 / 1.00 | `D` 0.78; `THEM(^C)` 0.10; `THEM(^ROLE)` 0.05 |
| 100 | 16 | 1 | 20 | 20 / 0 / 0 / 0 | 1 / 19 / 0 | 0.05 [0.01, 0.24] | 0.050 | 70 | 15 | 16 | 2.4 | 0.08 / 0.16 | `D` 0.94; `THEM(^C)` 0.05; `and(THEM(ME),X)` 0.00 |
| 100 | 64 | 1 | 20 | 20 / 0 / 0 / 0 | 2 / 17 / 1 | 0.10 [0.03, 0.30] | 0.100 | 100 | 61 | 64 | 9.6 | 0.04 / 0.15 | `D` 0.84; `THEM(^C)` 0.10; `THEM(^ROLE)` 0.05 |
| 100 | 256 | 1 | 40 | 40 / 0 / 0 / 0 | 6 / 20 / 14 | 0.15 [0.07, 0.29] | 0.193 | 370 | 2.4e+02 | 2.5e+02 | 38 | 0.05 / 0.15 | `D` 0.48; `THEM(^X)` 0.16; `THEM(^ROLE)` 0.16 |
| 200 | 8 | 1 | 20 | 20 / 0 / 0 / 0 | 0 / 20 / 0 | 0.00 [0.00, 0.16] | 0.000 | 60 | 7.2 | 7.9 | 2.2 | 0.11 / 0.21 | `D` 0.99; `THEM(THEM)` 0.01; `THEM(ME)` 0.00 |
| 400 | 16 | 1 | 20 | 20 / 0 / 0 / 0 | 1 / 19 / 0 | 0.05 [0.01, 0.24] | 0.050 | 80 | 13 | 16 | 7.6 | 0.17 / 0.48 | `D` 0.94; `THEM(^C)` 0.05; `and(THEM(THEM),D)` 0.00 |
| 800 | 32 | 1 | 20 | 20 / 0 / 0 / 0 | 1 / 13 / 6 | 0.05 [0.01, 0.24] | 0.103 | 100 | 21 | 31 | 23 | 0.36 / 0.72 | `D` 0.63; `THEM(^ROLE)` 0.15; `THEM(^X)` 0.10 |
| 400 | 4 | 0 | 20 | 20 / 0 / 0 / 0 | 0 / 0 / 0 | (per island below) | 0.000 | 60 | 3.3 | 3.9 | 1.9 | 0.25 / 0.54 | `D` 1.00; `THEM(ME)` 0.00; `and(X,THEM(THEM))` 0.00 |
| 100 | 64 | 0 | 20 | 20 / 0 / 0 / 0 | 0 / 0 / 0 | (per island below) | 0.004 | 80 | 61 | 64 | 9.6 | 0.05 / 0.13 | `D` 0.96; `X` 0.01; `ROLE` 0.01 |

No-migration control (mN = 0), per island: (N 400, I 4) 80 islands: efficient 0.00 [0.00, 0.05], defecting 1.00, other 0.00; (N 100, I 64) 1280 islands: efficient 0.00 [0.00, 0.00], defecting 0.97, other 0.03.

## Control (b): single-migrant fixation assays (isolated island, two types)

| arm | migrant -> resident | N | reps | fixations | rho Monte Carlo [95%] | rho exact |
|---|---|---|---|---|---|---|
| modal | `BOX(THEM(ME))` -> all-`D` | 100 | 20000 | 877 | 4.39e-02 [4.11e-02, 4.68e-02] | 4.206e-02 |
| modal | `D` -> all-`BOX(THEM(ME))` | 100 | 20000 | 0 | 0.00e+00 [0.00e+00, 1.92e-04] | 1.737e-08 |
| modal | `BOX(THEM(ME))` -> all-`D` | 400 | 50000 | 1064 | 2.13e-02 [2.01e-02, 2.26e-02] | 2.141e-02 |
| modal | `D` -> all-`BOX(THEM(ME))` | 400 | 20000 | 0 | 0.00e+00 [0.00e+00, 1.92e-04] | 2.530e-28 |
| modal | `BOX(THEM(ME))` -> all-`D` | 1600 | 100000 | 1040 | 1.04e-02 [9.79e-03, 1.10e-02] | 1.081e-02 |
| modal | `D` -> all-`BOX(THEM(ME))` | 1600 | 20000 | 0 | 0.00e+00 [0.00e+00, 1.92e-04] | 8.579e-107 |
| W0 | `THEM(^C)` -> all-`D` | 100 | 20000 | 782 | 3.91e-02 [3.65e-02, 4.19e-02] | 4.206e-02 |
| W0 | `D` -> all-`THEM(^C)` | 100 | 20000 | 0 | 0.00e+00 [0.00e+00, 1.92e-04] | 1.737e-08 |
| W0 | `THEM(^D)` -> all-`THEM(^C)` | 100 | 20000 | 5238 | 2.62e-01 [2.56e-01, 2.68e-01] | 2.637e-01 |
| W0 | `THEM(^C)` -> all-`THEM(^D)` | 100 | 20000 | 0 | 0.00e+00 [0.00e+00, 1.92e-04] | 1.828e-14 |
| W0 | `THEM(^C)` -> all-`D` | 400 | 50000 | 1064 | 2.13e-02 [2.01e-02, 2.26e-02] | 2.141e-02 |
| W0 | `D` -> all-`THEM(^C)` | 400 | 20000 | 0 | 0.00e+00 [0.00e+00, 1.92e-04] | 2.530e-28 |
| W0 | `THEM(^D)` -> all-`THEM(^C)` | 400 | 20000 | 5174 | 2.59e-01 [2.53e-01, 2.65e-01] | 2.603e-01 |
| W0 | `THEM(^C)` -> all-`THEM(^D)` | 400 | 20000 | 0 | 0.00e+00 [0.00e+00, 1.92e-04] | 1.479e-53 |
| W0 | `THEM(^C)` -> all-`D` | 1600 | 100000 | 1065 | 1.06e-02 [1.00e-02, 1.13e-02] | 1.081e-02 |
| W0 | `D` -> all-`THEM(^C)` | 1600 | 20000 | 0 | 0.00e+00 [0.00e+00, 1.92e-04] | 8.579e-107 |
| W0 | `THEM(^D)` -> all-`THEM(^C)` | 1600 | 20000 | 5148 | 2.57e-01 [2.51e-01, 2.64e-01] | 2.595e-01 |
| W0 | `THEM(^C)` -> all-`THEM(^D)` | 1600 | 20000 | 0 | 0.00e+00 [0.00e+00, 1.92e-04] | 6.644e-210 |

modal, R into all-D: slope of log rho on log N over N = 100, 400, 1600: exact -0.490, Monte Carlo -0.519.

W0, R into all-D: slope of log rho on log N over N = 100, 400, 1600: exact -0.490, Monte Carlo -0.469.

## Notes (hand-written, 2026-10-04)

**Budget.** The timing runs at (N, I) = (6,400, 4) took 0–2 s per run (one per arm, kept as rep 0). No horizon cut: every
cell ran at the declared 1e5-generation horizon. All 897 island runs (and all 120 no-migration runs) were certified
outcome-frozen well before the horizon (median stop at generation 20–490); there were no certified-separated, metastable or
unresolved runs. W0 at n = 8 could not be evaluated: the square evaluation of 11,462 programs was killed by the system
(exit 137, memory). W0 n = 9 and L_7 with `ROLE` were not attempted (see the predictions file).

**Pruned endpoints vs the flow.** `chain.replicator` prunes shares below 1e-9. At modal n = 8, 9 under the length, base-8 and
tempered-2 priors the pruned endpoint had a positive-growth class, `or(BOXD(THEM(ME)),BOX(THEM(^D)))` (rate 0.03–0.11),
which cooperates with ALLC and so exploits the probe-reading provers `BOX(THEM(^C))`, `BOX1(THEM(^C))`. One closure round
(re-inject at 1e-6) lets it in; it shrinks `BOX(THEM(^C))` and dies out again, and the closed endpoint is efficient and
persistent. In the weak arms the pruned endpoints had positive-growth classes such as ALLC (fed by the sucker `THEM(^D)`)
and `not(THEM(ME))`; closure leaves P(C,C) at 0. A no-pruning fixed-step integration (`flowcheck`,
`runs/almost-all-seeds-flow.txt`) confirms P(C,C) = 0 at t = 2e4 in every weak cell, but W0 n = 7 passes close to
cooperation on the way: P(C,C) is 0.85 (base 2), 0.91 (base 4) and 0.62 (uniform over programs) at t = 100, then collapses
to all-D. The "D extinct" time for W0 n = 7 in the extinction-order table is that transient (D falls below 1e-6 and
comes back); it is not an extinction. In the modal arm at n = 8 the no-pruning flow agrees with the closed endpoint under the length and base-8 priors (P(C,C) = 1.000 from t = 100). Under the tempered-2 prior it is still at P(C,C) = 0.000 at t = 3,000: D holds 0.996 and the prover family about 0.003, growing at rate 3.6e-3. The closed endpoint (efficient) is where this flow goes, but slowly: squaring the prior leaves the provers with so little mass after the ALLC phase that a finite island would likely lose them by drift. This is the thin-margin case, not uniform-over-programs.

**W0 on islands is not the replicator.** The replicator from mu is all-D in W0 at every prior, but the eps = 0 island
lottery ends all-`THEM(^C)` in up to 55% of runs. Two-type assays explain the race: `THEM(^C)` enters an all-D island
exactly like FairBot (rho 0.042 / 0.021 / 0.011 at N = 100 / 400 / 1,600, slope -0.49), while its faker `THEM(^D)` is
neutral against D and gains only on `THEM(^C)` islands (rho(THEM(^D) -> all-THEM(^C)) = 0.26 at every N). Without
mutation the faker is a finite stock that drifts on D islands; when every faker lineage is lost before it reaches a
`THEM(^C)` island, the metapopulation freezes at all-`THEM(^C)`, which nothing remaining can invade. In W0 mu(fakers) =
mu(R) = 0.002; in L_6 with `ROLE` the fakers carry 3x R's mass over 13 classes, and the old I-sweep
(`runs/islands_count.md`) seeded uniform over programs, which gives fakers far more weight.

**Cooperative-island losses (modal).** All 69 logged losses were to `BOX(THEM(^D))` / `BOX1(THEM(^D))`, which defect against
everything except ALLC-like cooperators and so exploit the probe-reading cooperative classes. These invaders earn no more against FairBot, `BOX(THEM(THEM))` or
`BOX1(THEM(ME))` than those earn against themselves. Every run with a loss still froze efficient.
