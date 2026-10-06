# Mixed-budget populations under K: do budget soft cliques become bridge-less rivals when budgets vary? (`src/mixed_budgets.py`)

Spec `specs/2026-10-05-mixed-budgets.md` (reviewed by gpt-6.1-sol); predictions `predictions/2026-10-05-mixed-budgets.md`. Modal language L_8 under the sound bounded calculus K; genotypes (source, budget) with budget in B = {4, 8, 16} (C and D unbudgeted); plays from the K tables and the cross-budget blocks (`runs/k-at-n8/`, guard at the reader's own budget). PD, w = 0.3, ε = 0, complete island graph, N = 200, I = 64, horizon 10⁵, generation = I·N births. Seeds: iid canonical sources from the length prior, a budget per non-constant individual by inverse CDF of one shared uniform (so every prior sees the same sources and monotonically coupled budgets: paired seeds across priors), lumped by the catalogue's behavioural classes. **Finite-horizon incidence at n = 8; not large-population universality or permanent isolation.** Intervals are exact (Clopper–Pearson) with runs as the units; hazards are events per exposure with a 97.5% Poisson upper bound; resolution times are right-censored (Kaplan–Meier).

## 1. The budgeted catalogue

**Catalogue.** 1826 genotypes (C, D and 608 non-constant sources at each of b = 4, 8, 16), 1027 behavioural classes (identical directed rows and columns). Soundness checks of the K closures behind each block: 16: 0 bad of 78340; 4: 0 bad of 1275; 4×16: 0 bad of 37893; 4×8: 0 bad of 16249; 8: 0 bad of 17474; 8×16: 0 bad of 97215.

**Lumping validity.** Member rows/columns identical in every class (0 violations); masses preserved under every prior (max error 0); genotype-level seed draws lumped versus class-level draws agree in first moments (max |z| 3.3 over priors, 500 islands each); establisher, incompatibility and pairwise-bridge tests at genotype level against the class tests on all 1785 incompatible genotype pairs: mismatches {'est': 0}.

**The budget grid on the catalogue** (row program's play, column program's play; C = cooperates):

| pair | 4 vs 4 | 4 vs 8 | 4 vs 16 | 8 vs 4 | 8 vs 8 | 8 vs 16 | 16 vs 4 | 16 vs 8 | 16 vs 16 |
|---|---|---|---|---|---|---|---|---|---|
| `BOX(THEM(ME))` vs `BOX(THEM(ME))` | CC | CC | CC | CC | CC | CC | CC | CC | CC |
| `BOX1(THEM(ME))` vs `BOX1(THEM(ME))` | CC | DD | DD | DD | CC | CC | DD | CC | CC |
| `BOX(THEM(ME))` vs `BOX1(THEM(ME))` | DD | DD | DD | DD | CC | CC | DD | CC | CC |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` vs `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | DD | DD | DD | DD | DD | DD | DD | DD | CC |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` vs `BOX(THEM(ME))` | DD | DD | DD | DD | DD | DD | DD | DD | CC |
| `BOX(THEM(THEM))` vs `BOX1(THEM(ME))` | DD | DD | DD | CD | CC | CC | CD | CC | CC |
| `BOX1(THEM(THEM))` vs `BOX1(THEM(ME))` | CD | DD | DD | CD | CC | CC | CD | CD | CC |

**Induced class tables** (classes of positive mass; establisher = self-cooperates, defects on D, not all-C):

| prior (b = 4, 8, 16) | classes | establishers | establisher μ (cut) [raw] | establisher μ by budget 4 / 8 / 16 |
|---|---|---|---|---|
| cheap-heavy (0.6, 0.3, 0.1) | 1027 | 219 | 0.0266 [0.0203] | 0.0168 / 0.0073 / 0.0024 |
| uniform (0.33, 0.33, 0.33) | 1027 | 219 | 0.0255 [0.0195] | 0.0094 / 0.0081 / 0.0081 |
| above-threshold (0, 0.5, 0.5) | 910 | 187 | 0.0243 [0.0185] | 0.0000 / 0.0122 / 0.0121 |
| homogeneous b = 4 (1, 0, 0) | 138 | 35 | 0.0281 [0.0214] | 0.0281 / 0.0000 / 0.0000 |
| homogeneous b = 8 (0, 1, 0) | 395 | 77 | 0.0244 [0.0186] | 0.0000 / 0.0244 / 0.0000 |
| homogeneous b = 16 (0, 0, 1) | 520 | 110 | 0.0242 [0.0185] | 0.0000 / 0.0000 / 0.0242 |

## 2. Static screening: incompatible pairs of budgeted establishers

Unit: an incompatible pair = two establisher classes of positive mass that mutually defect. Pairwise bridge = a cooperative class of positive mass under the prior mutually cooperating with both (exhaustive); structural bridge = any cooperative class of the catalogue; mediator path = shortest path in the establisher mutual-cooperation graph of the prior's support. Pair mass = product of the two class masses (cut); co-seeding = P(both on one island of N = 200), summed over pairs.

| prior | establishers | components (sizes) | incompatible: n, mass [raw] | bridged: n, mass | **direct-bridge-less**: n, mass [raw], co-seed sum (max) | structurally bridge-less: n, mass | no path ≤ 3: n, mass | disconnected: n, mass | budget copies of one source: n (bridge-less n) |
|---|---|---|---|---|---|---|---|---|---|
| cheap-heavy | 219 | 3 (217, 1, 1) | 1659, 5.9e-05 [3.4e-05] | 1310, 2.5e-05 | **349, 3.4e-05** [2.0e-05], 0.834 (0.206) | 349, 3.4e-05 | 159, 3.4e-05 | 151, 3.4e-05 | 15 (3) |
| uniform | 219 | 3 (217, 1, 1) | 1659, 4.0e-05 [2.3e-05] | 1310, 2.1e-05 | **349, 1.8e-05** [1.1e-05], 0.533 (0.0814) | 349, 1.8e-05 | 159, 1.8e-05 | 151, 1.8e-05 | 15 (3) |
| above-threshold | 187 | 2 (186, 1) | 739, 1.5e-06 [9.0e-07] | 672, 1.5e-06 | **67, 6.4e-08** [3.8e-08], 0.00206 (0.0003) | 67, 6.4e-08 | 67, 6.4e-08 | 67, 6.4e-08 | 7 (1) |
| homogeneous b = 4 | 35 | 4 (32, 1, 1, 1) | 112, 6.8e-05 [3.9e-05] | 20, 1.2e-07 | **92, 6.8e-05** [3.9e-05], 1.17 (0.404) | 75, 5.9e-05 | 57, 6.7e-05 | 45, 6.7e-05 | 0 (0) |
| homogeneous b = 8 | 77 | 2 (76, 1) | 113, 3.7e-06 [2.1e-06] | 83, 3.5e-06 | **30, 1.4e-07** [8.2e-08], 0.00377 (0.000962) | 30, 1.4e-07 | 30, 1.4e-07 | 30, 1.4e-07 | 0 (0) |
| homogeneous b = 16 | 110 | 1 (110) | 150, 3.5e-08 [2.0e-08] | 150, 3.5e-08 | **0, 0** [0], 0 (0) | 0, 0 | 0, 0 | 0, 0 | 0 (0) |

Direct-bridge-less pair mass, cheap-heavy / above-threshold: 528.
cheap-heavy: `BOX1(THEM(ME))`@4's class is a member of 65 direct-bridge-less pairs carrying 0.995 of the bridge-less mass; 80 bridge-less pairs (mass 3.4e-05) have a FairBot or `BOX1(THEM(ME))` copy as a member.
uniform: `BOX1(THEM(ME))`@4's class is a member of 65 direct-bridge-less pairs carrying 0.994 of the bridge-less mass; 80 bridge-less pairs (mass 1.8e-05) have a FairBot or `BOX1(THEM(ME))` copy as a member.
above-threshold: `BOX1(THEM(ME))`@4's class is a member of 0 direct-bridge-less pairs carrying 0.000 of the bridge-less mass; 4 bridge-less pairs (mass 3.8e-08) have a FairBot or `BOX1(THEM(ME))` copy as a member.
homogeneous b = 4: `BOX1(THEM(ME))`@4's class is a member of 18 direct-bridge-less pairs carrying 0.876 of the bridge-less mass; 20 bridge-less pairs (mass 5.9e-05) have a FairBot or `BOX1(THEM(ME))` copy as a member.
homogeneous b = 8: `BOX1(THEM(ME))`@4's class is a member of 0 direct-bridge-less pairs carrying 0.000 of the bridge-less mass; 2 bridge-less pairs (mass 7.7e-08) have a FairBot or `BOX1(THEM(ME))` copy as a member.

**Core programs: do their budget copies share an establisher component?** (component index per budget; "—" = not an establisher at that budget)

| program | prior | b = 4 | b = 8 | b = 16 | 4–8 | 4–16 | 8–16 |
|---|---|---|---|---|---|---|---|
| `BOX(THEM(ME))` | cheap-heavy | 0 | 0 | 0 | yes | yes | yes |
| `BOX1(THEM(ME))` | cheap-heavy | 1 | 0 | 0 | no | no | yes |
| `BOX(THEM(THEM))` | cheap-heavy | 0 | 0 | 0 | yes | yes | yes |
| `BOX1(THEM(THEM))` | cheap-heavy | 0 | 0 | 0 | yes | yes | yes |
| `BOX(THEM(^C))` | cheap-heavy | 0 | 0 | 0 | yes | yes | yes |
| `BOX1(THEM(^C))` | cheap-heavy | — | 0 | 0 | no | no | yes |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | cheap-heavy | — | — | 0 | no | no | no |
| `BOX(THEM(ME))` | uniform | 0 | 0 | 0 | yes | yes | yes |
| `BOX1(THEM(ME))` | uniform | 1 | 0 | 0 | no | no | yes |
| `BOX(THEM(THEM))` | uniform | 0 | 0 | 0 | yes | yes | yes |
| `BOX1(THEM(THEM))` | uniform | 0 | 0 | 0 | yes | yes | yes |
| `BOX(THEM(^C))` | uniform | 0 | 0 | 0 | yes | yes | yes |
| `BOX1(THEM(^C))` | uniform | — | 0 | 0 | no | no | yes |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | uniform | — | — | 0 | no | no | no |
| `BOX(THEM(ME))` | above-threshold | — | 0 | 0 | no | no | yes |
| `BOX1(THEM(ME))` | above-threshold | — | 0 | 0 | no | no | yes |
| `BOX(THEM(THEM))` | above-threshold | — | 0 | 0 | no | no | yes |
| `BOX1(THEM(THEM))` | above-threshold | — | 0 | 0 | no | no | yes |
| `BOX(THEM(^C))` | above-threshold | — | 0 | 0 | no | no | yes |
| `BOX1(THEM(^C))` | above-threshold | — | 0 | 0 | no | no | yes |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | above-threshold | — | — | 0 | no | no | no |

**Incompatible-pair list, cheap-heavy** (heaviest direct-bridge-less pairs, then heaviest bridged pairs; budgets in class names; path = mediator path length, – = none):

| pair | pair mass | co-seed | bridges (n, mass, heaviest) | structural bridges | path | same component | budget copies of |
|---|---|---|---|---|---|---|---|
| `BOX(THEM(ME))@4` × `BOX1(THEM(ME))@4` | 9.2e-06 | 0.206 | 0, 0, – | 0 | – | no | – |
| `BOX(THEM(THEM))@4` × `BOX1(THEM(ME))@4` | 9.2e-06 | 0.206 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX(THEM(ME))@8` | 4.6e-06 | 0.118 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX1(THEM(ME))@8` | 4.6e-06 | 0.118 | 0, 0, – | 0 | – | no | `BOX1(THEM(ME))` |
| `BOX1(THEM(ME))@4` × `BOX(THEM(^C))@4` | 2.8e-06 | 0.0761 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX(THEM(ME))@16` | 1.5e-06 | 0.0435 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX1(THEM(ME))@16` | 1.5e-06 | 0.0435 | 0, 0, – | 0 | – | no | `BOX1(THEM(ME))` |
| `BOX(THEM(^C))@4` × `not(BOXD1(THEM(^D)))@8` | 6.3e-08 | 0.00227 | 0, 0, – | 0 | 3 | yes | – |
| `BOX1(THEM(ME))@4` × `BOX(THEM(^BOX(THEM(ME))))@4` | 5.6e-08 | 0.00168 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX(THEM(^BOX(THEM(THEM))))@4` | 5.6e-08 | 0.00168 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX(THEM(^BOX(THEM(ME))))@8` | 2.8e-08 | 0.00084 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX(THEM(^BOX(THEM(THEM))))@8` | 2.8e-08 | 0.00084 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX(THEM(^BOX1(THEM(ME))))@8` | 2.8e-08 | 0.00084 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX(THEM(^BOX1(THEM(THEM))))@8` | 2.8e-08 | 0.00084 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX1(THEM(^BOX(THEM(ME))))@8` | 2.8e-08 | 0.00084 | 0, 0, – | 0 | – | no | – |
| `BOX(THEM(ME))@4` × `BOX1(THEM(ME))@8` | 4.6e-06 | 0.118 | 6, 4.0e-03, `BOX(THEM(ME))@8` | 6 | 2 | yes | – |
| `BOX(THEM(THEM))@4` × `BOX1(THEM(ME))@8` | 4.6e-06 | 0.118 | 53, 4.1e-03, `BOX(THEM(ME))@8` | 53 | 2 | yes | – |
| `BOX1(THEM(THEM))@4` × `BOX1(THEM(ME))@8` | 4.6e-06 | 0.118 | 4, 4.0e-03, `BOX(THEM(ME))@8` | 4 | 2 | yes | – |
| `BOX1(THEM(THEM))@4` × `BOX(THEM(^C))@4` | 2.8e-06 | 0.0761 | 4, 4.0e-03, `BOX(THEM(ME))@8` | 4 | 2 | yes | – |
| `BOX(THEM(ME))@4` × `BOX1(THEM(ME))@16` | 1.5e-06 | 0.0435 | 6, 4.0e-03, `BOX(THEM(ME))@8` | 6 | 2 | yes | – |
| `BOX(THEM(THEM))@4` × `BOX1(THEM(ME))@16` | 1.5e-06 | 0.0435 | 93, 4.1e-03, `BOX(THEM(ME))@8` | 93 | 2 | yes | – |
| `BOX1(THEM(THEM))@4` × `BOX1(THEM(ME))@16` | 1.5e-06 | 0.0435 | 4, 4.0e-03, `BOX(THEM(ME))@8` | 4 | 2 | yes | – |
| `BOX1(THEM(ME))@8` × `BOX(THEM(^C))@4` | 1.4e-06 | 0.0437 | 8, 4.7e-03, `BOX(THEM(ME))@8` | 8 | 2 | yes | – |
| `BOX1(THEM(ME))@16` × `BOX(THEM(^C))@4` | 4.6e-07 | 0.0161 | 10, 4.7e-03, `BOX(THEM(ME))@8` | 10 | 2 | yes | – |
| `BOX(THEM(ME))@4` × `not(BOXD1(THEM(^D)))@8` | 2.1e-07 | 0.00614 | 2, 4.1e-06, `or(BOX(THEM(THEM)),not(BOXD(THEM(ME))))@4` | 2 | 2 | yes | – |

**Incompatible-pair list, above-threshold** (heaviest direct-bridge-less pairs, then heaviest bridged pairs; budgets in class names; path = mediator path length, – = none):

| pair | pair mass | co-seed | bridges (n, mass, heaviest) | structural bridges | path | same component | budget copies of |
|---|---|---|---|---|---|---|---|
| `BOX(THEM(ME))@8` × `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` | 9.6e-09 | 0.0003 | 0, 0, – | 0 | – | no | – |
| `BOX(THEM(THEM))@8` × `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` | 9.6e-09 | 0.0003 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@8` × `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` | 9.6e-09 | 0.0003 | 0, 0, – | 0 | – | no | – |
| `BOX(THEM(ME))@16` × `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` | 9.6e-09 | 0.0003 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@16` × `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` | 9.6e-09 | 0.0003 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(THEM))@16` × `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` | 9.6e-09 | 0.0003 | 0, 0, – | 0 | – | no | – |
| `BOX(THEM(^C))@8` × `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` | 2.9e-09 | 0.000107 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(^C))@8` × `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` | 2.9e-09 | 0.000107 | 0, 0, – | 0 | – | no | – |
| `BOX(THEM(^BOX(THEM(ME))))@8` × `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` | 5.9e-11 | 2.33e-06 | 0, 0, – | 0 | – | no | – |
| `BOX(THEM(^BOX(THEM(THEM))))@8` × `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` | 5.9e-11 | 2.33e-06 | 0, 0, – | 0 | – | no | – |
| `BOX(THEM(^BOX1(THEM(ME))))@8` × `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` | 5.9e-11 | 2.33e-06 | 0, 0, – | 0 | – | no | – |
| `BOX(THEM(^BOX1(THEM(THEM))))@8` × `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` | 5.9e-11 | 2.33e-06 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(^BOX(THEM(ME))))@8` × `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` | 5.9e-11 | 2.33e-06 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(^BOX(THEM(THEM))))@8` × `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` | 5.9e-11 | 2.33e-06 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(^BOX1(THEM(ME))))@8` × `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` | 5.9e-11 | 2.33e-06 | 0, 0, – | 0 | – | no | – |
| `BOX(THEM(ME))@8` × `not(BOXD1(THEM(^D)))@8` | 2.9e-07 | 0.00888 | 60, 4.4e-05, `or(BOX1(THEM(ME)),not(BOXD(THEM(ME))))@8` | 64 | 2 | yes | – |
| `BOX(THEM(THEM))@8` × `not(BOXD1(THEM(^D)))@8` | 2.9e-07 | 0.00888 | 65, 4.8e-05, `or(BOX1(THEM(ME)),not(BOXD(THEM(ME))))@8` | 68 | 2 | yes | – |
| `BOX(THEM(^C))@8` × `not(BOXD1(THEM(^D)))@8` | 8.7e-08 | 0.00318 | 56, 4.2e-05, `or(BOX1(THEM(ME)),not(BOXD(THEM(ME))))@8` | 65 | 2 | yes | – |
| `BOX(THEM(ME))@8` × `BOX1(THEM(^BOX1(THEM(THEM))))@8` | 3.9e-08 | 0.00122 | 10, 4.1e-03, `BOX(THEM(THEM))@16` | 10 | 2 | yes | – |
| `BOX1(THEM(ME))@8` × `BOX(THEM(^BOX(THEM(THEM))))@8` | 3.9e-08 | 0.00122 | 67, 0.0143, `BOX(THEM(ME))@8` | 67 | 2 | yes | – |
| `BOX1(THEM(ME))@8` × `BOX(THEM(^BOX1(THEM(THEM))))@8` | 3.9e-08 | 0.00122 | 19, 6.6e-03, `BOX(THEM(ME))@16` | 19 | 2 | yes | – |
| `BOX1(THEM(ME))@8` × `BOX1(THEM(^BOX(THEM(THEM))))@8` | 3.9e-08 | 0.00122 | 49, 9.2e-03, `BOX(THEM(ME))@8` | 49 | 2 | yes | – |
| `BOX1(THEM(ME))@8` × `BOX1(THEM(^BOX1(THEM(THEM))))@8` | 3.9e-08 | 0.00122 | 10, 4.1e-03, `BOX(THEM(THEM))@16` | 10 | 2 | yes | – |
| `BOX1(THEM(ME))@8` × `BOX(THEM(^BOX1(THEM(THEM))))@16` | 3.9e-08 | 0.00122 | 65, 9.2e-03, `BOX(THEM(ME))@16` | 65 | 2 | yes | – |
| `BOX1(THEM(ME))@8` × `BOX1(THEM(^BOX1(THEM(THEM))))@16` | 3.9e-08 | 0.00122 | 65, 9.2e-03, `BOX(THEM(ME))@16` | 65 | 2 | yes | – |

**Incompatible-pair list, uniform** (heaviest direct-bridge-less pairs, then heaviest bridged pairs; budgets in class names; path = mediator path length, – = none):

| pair | pair mass | co-seed | bridges (n, mass, heaviest) | structural bridges | path | same component | budget copies of |
|---|---|---|---|---|---|---|---|
| `BOX(THEM(ME))@4` × `BOX1(THEM(ME))@4` | 2.8e-06 | 0.0814 | 0, 0, – | 0 | – | no | – |
| `BOX(THEM(THEM))@4` × `BOX1(THEM(ME))@4` | 2.8e-06 | 0.0814 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX(THEM(ME))@8` | 2.8e-06 | 0.0814 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX1(THEM(ME))@8` | 2.8e-06 | 0.0814 | 0, 0, – | 0 | – | no | `BOX1(THEM(ME))` |
| `BOX1(THEM(ME))@4` × `BOX(THEM(ME))@16` | 2.8e-06 | 0.0814 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX1(THEM(ME))@16` | 2.8e-06 | 0.0814 | 0, 0, – | 0 | – | no | `BOX1(THEM(ME))` |
| `BOX1(THEM(ME))@4` × `BOX(THEM(^C))@4` | 8.6e-07 | 0.0276 | 0, 0, – | 0 | – | no | – |
| `BOX(THEM(^C))@4` × `not(BOXD1(THEM(^D)))@8` | 3.9e-08 | 0.00145 | 0, 0, – | 0 | 3 | yes | – |
| `BOX1(THEM(ME))@4` × `BOX(THEM(^BOX(THEM(ME))))@4` | 1.7e-08 | 0.000586 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX(THEM(^BOX(THEM(THEM))))@4` | 1.7e-08 | 0.000586 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX(THEM(^BOX(THEM(ME))))@8` | 1.7e-08 | 0.000586 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX(THEM(^BOX(THEM(THEM))))@8` | 1.7e-08 | 0.000586 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX(THEM(^BOX1(THEM(ME))))@8` | 1.7e-08 | 0.000586 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX(THEM(^BOX1(THEM(THEM))))@8` | 1.7e-08 | 0.000586 | 0, 0, – | 0 | – | no | – |
| `BOX1(THEM(ME))@4` × `BOX1(THEM(^BOX(THEM(ME))))@8` | 1.7e-08 | 0.000586 | 0, 0, – | 0 | – | no | – |
| `BOX(THEM(ME))@4` × `BOX1(THEM(ME))@8` | 2.8e-06 | 0.0814 | 6, 6.7e-03, `BOX(THEM(ME))@8` | 6 | 2 | yes | – |
| `BOX(THEM(ME))@4` × `BOX1(THEM(ME))@16` | 2.8e-06 | 0.0814 | 6, 6.7e-03, `BOX(THEM(ME))@8` | 6 | 2 | yes | – |
| `BOX(THEM(THEM))@4` × `BOX1(THEM(ME))@8` | 2.8e-06 | 0.0814 | 53, 6.8e-03, `BOX(THEM(ME))@8` | 53 | 2 | yes | – |
| `BOX(THEM(THEM))@4` × `BOX1(THEM(ME))@16` | 2.8e-06 | 0.0814 | 93, 6.9e-03, `BOX(THEM(ME))@8` | 93 | 2 | yes | – |
| `BOX1(THEM(THEM))@4` × `BOX1(THEM(ME))@8` | 2.8e-06 | 0.0814 | 4, 6.7e-03, `BOX(THEM(ME))@8` | 4 | 2 | yes | – |
| `BOX1(THEM(THEM))@4` × `BOX1(THEM(ME))@16` | 2.8e-06 | 0.0814 | 4, 6.7e-03, `BOX(THEM(ME))@8` | 4 | 2 | yes | – |
| `BOX1(THEM(THEM))@4` × `BOX(THEM(^C))@4` | 8.6e-07 | 0.0276 | 4, 6.7e-03, `BOX(THEM(ME))@8` | 4 | 2 | yes | – |
| `BOX1(THEM(ME))@8` × `BOX(THEM(^C))@4` | 8.6e-07 | 0.0276 | 8, 7.8e-03, `BOX(THEM(ME))@8` | 8 | 2 | yes | – |
| `BOX1(THEM(ME))@16` × `BOX(THEM(^C))@4` | 8.6e-07 | 0.0276 | 10, 7.8e-03, `BOX(THEM(ME))@8` | 10 | 2 | yes | – |
| `BOX(THEM(ME))@4` × `not(BOXD1(THEM(^D)))@8` | 1.3e-07 | 0.00428 | 2, 2.3e-06, `or(BOX(THEM(THEM)),not(BOXD(THEM(ME))))@4` | 2 | 2 | yes | – |

**Secondary: rivals of A₁₆ = {FairBot@16, `BOX1(THEM(ME))`@16}** (establishers of positive mass mutually defecting with either member):

| prior | rivals | rival mass | direct-bridge-less mass (share) | heaviest rivals |
|---|---|---|---|---|
| cheap-heavy | 34 | 0.0132 | 3.0e-03 (0.231) | `BOX(THEM(ME))@4` (3.0e-03, 5 bridges), `BOX(THEM(THEM))@4` (3.0e-03, 92 bridges), `BOX1(THEM(ME))@4` (3.0e-03, 0 bridges), `BOX1(THEM(THEM))@4` (3.0e-03, 3 bridges) |
| uniform | 34 | 7.3e-03 | 1.7e-03 (0.23) | `BOX(THEM(ME))@4` (1.7e-03, 5 bridges), `BOX(THEM(THEM))@4` (1.7e-03, 92 bridges), `BOX1(THEM(ME))@4` (1.7e-03, 0 bridges), `BOX1(THEM(THEM))@4` (1.7e-03, 3 bridges) |
| above-threshold | 10 | 8.9e-05 | 3.8e-06 (0.0428) | `BOX(THEM(^BOX(THEM(THEM))))@8` (1.5e-05, 146 bridges), `BOX(THEM(^BOX1(THEM(ME))))@8` (1.5e-05, 60 bridges), `BOX(THEM(^BOX1(THEM(THEM))))@8` (1.5e-05, 59 bridges), `BOX1(THEM(^BOX(THEM(THEM))))@8` (1.5e-05, 107 bridges) |

## 3. Calibration (m = 0, N = 200, I = 16, 120 runs per prior)

| prior | T_nuc (median [95% bootstrap]) | quartiles | per-island nucleation p | boundary mN = 0.3·N/T_nuc |
|---|---|---|---|---|
| cheap-heavy | 60 [55, 60] | 45 / 60 / 70 | 0.131 (252 / 1920) | 1.000 |
| above-threshold | 55 [55, 60] | 45 / 55 / 70 | 0.115 (220 / 1920) | 1.091 |
| uniform | 55 [55, 60] | 45 / 55 / 65 | 0.128 (245 / 1920) | 1.091 |
| homogeneous b = 4 | 55 [55, 60] | 50 / 55 / 70 | 0.139 (267 / 1920) | 1.091 |
| homogeneous b = 8 | 55 [55, 60] | 45 / 55 / 65 | 0.127 (243 / 1920) | 1.091 |
| homogeneous b = 16 | 55 [50, 55] | 45 / 55 / 65 | 0.116 (222 / 1920) | 1.091 |

Checks are every 5 generations, so T_nuc is resolved to 5.

## 4. Natural runs (N = 200, I = 64, horizon 10⁵): homogeneous controls, common mN, calibrated mN

| cell | prior | mN | x = mN·T_nuc/N | runs | ever separated [95%] | **separated at the horizon** [95%] | with `BOX1(THEM(ME))`@4 | bridge-less (prior) / structural | budget copies | island P(C,C), certified (min) | run-level efficient | all-D runs | cf cross P(C,C): separated / all | worker-hours |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| homogeneous | homogeneous b = 4 | 1.091 | 0.300 | 150 | 126/150 = 0.840 [0.771, 0.895] | **122/150 = 0.813 [0.742, 0.872]** | 121 | 121 / 121 | 0 | 0.9925 (0.982) | 0.930 | 0 | 0.654 / 0.718 | 1.77 |
| homogeneous | homogeneous b = 8 | 1.091 | 0.300 | 300 | 8/300 = 0.027 [0.012, 0.052] | **1/300 = 0.003 [0.000, 0.018]** | 0 | 1 / 1 | 0 | 1.0000 (0.986) | 1.000 | 0 | 0.518 / 0.998 | 0.04 |
| homogeneous | homogeneous b = 16 | 1.091 | 0.300 | 300 | 0/300 = 0.000 [0.000, 0.012] | **0/300 = 0.000 [0.000, 0.012]** | 0 | 0 / 0 | 0 | 1.0000 (1.000) | 1.000 | 0 | – / 1.000 | 0.03 |
| common mN | cheap-heavy | 1.091 | 0.327 | 3000 | 2486/3000 = 0.829 [0.815, 0.842] | **2048/3000 = 0.683 [0.666, 0.699]** | 1931 | 1935 / 1935 | 98 | 0.9931 (0.979) | 0.935 | 2 | 0.61 / 0.733 | 31.37 |
| common mN | above-threshold | 1.091 | 0.300 | 3000 | 87/3000 = 0.029 [0.023, 0.036] | **6/3000 = 0.002 [0.001, 0.004]** | 0 | 6 / 6 | 0 | 1.0000 (0.987) | 1.000 | 0 | 0.531 / 0.999 | 0.38 |

**Paired horizon separation** (same source seeds and budget uniforms): nat cheap-heavy vs nat above-threshold: 3000 common reps, both 5, first only 2043, second only 1; hom homogeneous b = 4 vs nat cheap-heavy: 150 common reps, both 79, first only 43, second only 20.

**Separated pairs at the horizon** (first listed pair of each separated run) and per-separation tracking:

| cell | prior | heaviest separated pairs (runs) | first-separation fate | resolved / censored | resolution hazard per separated-run-generation [upper] | KM P(still separated) at 10² / 10³ / 10⁴ / 5·10⁴ after first separation (follow-up ends at 10⁵ − first separation) |
|---|---|---|---|---|---|---|
| hom | homogeneous b = 4 | `BOX(THEM(ME))@4 | BOX1(THEM(ME))@4` 68; `BOX(THEM(THEM))@4 | BOX1(THEM(ME))@4` 51; `BOX(THEM(^C))@4 | BOX1(THEM(ME))@4` 2; `BOX(THEM(ME))@4 | or(BOX(THEM(ME)),BOX(THEM(^D)))@4` 1 | bridge-less, separated at end 121, bridge-less, resolved 4, bridged, not seeded, dead, separated at end 1 | 4 / 122 | 3.2e-07 [8.2e-07] | 0.99 / 0.99 / 0.99 / 0.99 |
| hom | homogeneous b = 8 | `BOX(THEM(ME))@8 | and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` 1 | bridged, seeded, alive, resolved 2, bridged, seeded, dead, resolved 4, bridged, not seeded, dead, resolved 1, bridge-less, separated at end 1 | 7 / 1 | 6.9e-05 [1.4e-04] | 0.38 / 0.12 / 0.12 / 0.12 |
| nat | cheap-heavy | `BOX(THEM(ME))@4 | BOX1(THEM(ME))@4` 1021; `BOX(THEM(THEM))@4 | BOX1(THEM(ME))@4` 641; `BOX(THEM(ME))@8 | BOX1(THEM(ME))@4` 123; `BOX1(THEM(ME))@4 | BOX1(THEM(ME))@8` 82 | bridge-less, separated at end 1561, bridged, seeded, dead, separated at end 481, bridged, seeded, alive, resolved 382, bridged, seeded, dead, resolved 31, bridge-less, resolved 22, bridged, not seeded, dead, separated at end 6, bridged, not seeded, dead, resolved 3 | 438 / 2048 | 2.1e-06 [2.3e-06] | 0.99 / 0.93 / 0.83 / 0.83 |
| nat | above-threshold | `BOX1(THEM(ME))@8 | and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` 3; `BOX(THEM(THEM))@8 | and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` 2; `BOX1(THEM(ME))@16 | and(BOX1(THEM(ME)),BOX1(THEM(THEM)))@8` 1 | bridged, seeded, alive, resolved 39, bridged, seeded, dead, resolved 40, bridge-less, separated at end 6, bridge-less, resolved 1, bridged, not seeded, dead, resolved 1 | 81 / 6 | 1.1e-04 [1.4e-04] | 0.56 / 0.24 / 0.08 / 0.08 |

**Budget composition of cooperative holders** (island-weighted, one vote per holding island, each vote the holder's expected budget composition on that island; first checkpoint = first check after every island is established, horizon = 10⁵ or the stop of a frozen run; TV against the prior over {4, 8, 16}; mean over runs with both checkpoints, bootstrap 95%):

| cell | prior | runs with both | first checkpoint (median gen) | composition 4 / 8 / 16 at first | at horizon | TV first → horizon | ΔTV [95%] | mean budget first → horizon | Δ budget [95%] | unseparated runs: mean budget first → horizon |
|---|---|---|---|---|---|---|---|---|---|---|
| hom | homogeneous b = 4 | 150 | 328 | 1.000 / 0.000 / 0.000 | 1.000 / 0.000 / 0.000 | 0.000 → 0.000 | +0.000 [+0.000, +0.000] | 4.00 → 4.00 | +0.00 [+0.00, +0.00] | 4.00 → 4.00 (28) |
| hom | homogeneous b = 8 | 299 | 305 | 0.000 / 1.000 / 0.000 | 0.000 / 1.000 / 0.000 | 0.000 → 0.000 | +0.000 [+0.000, +0.000] | 8.00 → 8.00 | +0.00 [+0.00, +0.00] | 8.00 → 8.00 (298) |
| hom | homogeneous b = 16 | 298 | 300 | 0.000 / 0.000 / 1.000 | 0.000 / 0.000 / 1.000 | 0.000 → 0.000 | +0.000 [+0.000, +0.000] | 16.00 → 16.00 | +0.00 [+0.00, +0.00] | 16.00 → 16.00 (298) |
| nat | cheap-heavy | 2992 | 325 | 0.786 / 0.161 / 0.054 | 0.736 / 0.196 / 0.069 | 0.284 → 0.314 | +0.030 [+0.026, +0.034] | 5.29 → 5.61 | +0.32 [+0.28, +0.36] | 5.91 → 6.42 (944) |
| nat | above-threshold | 2986 | 295 | 0.000 / 0.587 / 0.413 | 0.000 / 0.586 / 0.414 | 0.202 → 0.202 | -0.000 [-0.001, +0.001] | 11.31 → 11.31 | +0.00 [-0.00, +0.01] | 11.31 → 11.31 (2980) |

## 6. What ran, what did not

Ran to completion:
- catalogue, soundness and lumping checks;
- static screening under all six priors;
- m = 0 calibration for all six priors;
- homogeneous controls: b = 4 (150 runs), b = 8 (300), b = 16 (300);
- (a) natural runs at the common mN = 1.091: cheap-heavy and above-threshold, 3,000 runs each, paired seeds.

**Did not run** (the session's compute ran out; the coordinator asked for the report on the finished data):
- (b) the forced bridge-less and forced bridged pairs, with their inert-defector and iid controls;
- (a) the calibrated cells (cheap-heavy at mN = 1.000; the other priors' boundaries equal the common mN) and the uniform prior;
- (c) the scaling panel.

The forced pairs remain as declared in the predictions addendum.

## 7. Verdicts

| # | prediction | outcome |
|---|---|---|
| RE 1 | named pair (`BOX1(THEM(ME))`@4, @16) incompatible and direct-bridge-less; cheap-heavy / above-threshold bridge-less mass ≥ 10×; core at ≥ 8 one component | **held**: no structural bridge, ratio ≈ 530, FairBot and `BOX1(THEM(ME))` at 8 and 16 in one component. The above-threshold prior does keep 67 light bridge-less pairs (6.4·10⁻⁸), as RE 1 allowed. |
| RE 2 | cheap-heavy natural horizon separation > above-threshold at the common mN (point ≥ 5 vs ≤ 2) | **held**: 2,048/3,000 = 0.683 [0.666, 0.699] against 6/3,000 = 0.002 [0.001, 0.004]; paired 2,043 cheap-only vs 1 above-only. The above-threshold count exceeds the RE's point expectation of ≤ 2; that is not a falsifier. |
| RE 3 | horizon − first-checkpoint composition distance ≥ 0.1 under cheap-heavy, toward higher budgets | **failed, falsifier fired (narrowly)**: ΔTV = +0.0299 [+0.026, +0.034] against the 0.03 falsifier. The interval straddles 0.03. The direction is the RE's: mean holder budget +0.32 [+0.28, +0.36] budget units, +0.51 in unseparated runs. The pooled-over-runs TV *falls* (0.186 → 0.136), so the distance statistic does not capture the shift well. |
| RE 4 | bridged forced pair resolves with a bridge, separates without; bridge-less separation persists on the scaling panel | **not tested** (cells did not run). Indirect natural evidence (not a substitute): among cheap-heavy runs whose first separation was a bridged pair, all 382 with the bridge alive at the horizon resolved, and 481 of 512 with the bridge dead ended separated. |
| RE 5 | island P(C,C) ≥ 0.97 every cell; homogeneous b = 4 ≈ 0.8, b = 16 ≈ 0 separated | **held** on the cells that ran: island P(C,C) over certified islands ≥ 0.992 per cell (lowest run 0.979); b = 4 0.813 [0.742, 0.872]; b = 16 0/300 (one-sided 95% ≤ 0.010). |
| S1 | ≥ 0.8 of cheap-heavy bridge-less mass on `BOX1(THEM(ME))`@4; above-threshold mass < 10⁻⁸ with no FairBot/`BOX1(THEM(ME))` copy | **failed, falsifier fired**: share 0.995 held, mass 6.4·10⁻⁸ grey, but 4 above-threshold bridge-less pairs contain FairBot or `BOX1(THEM(ME))` at 8 or 16, against the b = 8 soft clique `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))`@8. |
| S2 | cheap-heavy ≥ 0.3 separated, ≥ 0.7 of them with `BOX1(THEM(ME))`@4; above-threshold ≤ 3/3,000 | **held on two clauses, grey on one**: 0.683; share 1,931/2,048 = 0.943; above-threshold 6/3,000 is between 3 and the falsifier's 10. Overall inconclusive by the grey clause. |
| S3 | under cheap-heavy, mean holder budget does not rise by > 0.5 units and TV change < 0.1 (direction: falls or stays) | **held on its numbers** (+0.32 units, ΔTV +0.030); **the stated direction was wrong**: holder budgets rise, and in unseparated runs by +0.51. |
| S4 | homogeneous b = 4 in [0.65, 0.92], b = 8 ≤ 0.01, b = 16 ≤ 0.005 | **held** (0.813; 1/300; 0/300) |
| S5, S6 | forced pairs | **not tested** |
| S7 | island P(C,C) ≥ 0.98 per cell; run-level efficient fraction ≥ 0.95; cf cross P(C,C) of separated cheap-heavy runs in [0.4, 0.85] | **inconclusive**: island P(C,C) 0.992–1.000 held; cf cross 0.61 held; run-level 0.935 (cheap-heavy) and 0.930 (b = 4) are between the claim (0.95) and the falsifier (0.9). |
| S8 | T_nuc 45–65 under every prior; calibrated cheap-heavy separation within 0.1 of common | **calibration clause held** (55–60); separation clause **not tested** |

## 8. Reading

- **Mixed budgets do not split FairBot; they split `BOX1(THEM(ME))`.**
  - FairBot cooperates with itself at every pair of budgets in {4, 8, 16}.
  - `BOX1(THEM(ME))`@4 cooperates with nothing outside itself, so no program at any budget bridges it.
  - Under cheap-heavy it carries 0.995 of the bridge-less pair mass and is a member of 0.943 of the 2,048 horizon separations.
- **The obstruction is dynamic as well as static.**
  - 0.683 of cheap-heavy runs end separated, against 0.002 under above-threshold (paired, same seeds) and 0.813 in the homogeneous b = 4 control.
  - Every island stays efficient (island P(C,C) ≥ 0.99). What is lost is the cross-island counterfactual (0.61 in separated runs).
- **Bridged incompatibilities resolve iff the bridge survives**, as in the free box and in K at a single budget.
  - Cheap-heavy first separations with a living bridge: 382 of 382 resolved.
  - With the bridge dead: 481 of 512 ended separated.
  - The 113 horizon separations of bridged pairs are all dead-bridge runs.
- **Above the copy thresholds the residue is one b = 8 soft clique.**
  - `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))`@8 is in all 6 above-threshold horizon separations and the 1 b = 8 separation.
  - The b = 16 control has none.
- **Holder budgets drift upward after founding, slowly.** The mean holder budget rises +0.32 budget units (+0.51 where no rival survives). Compatibility selects the copies that cooperate with more partners. The composition distance moves only 0.03, so selection after founding is weak at this horizon.
- *Scope:* finite-horizon incidence at n = 8, N = 200, I = 64, horizon 10⁵. The forced cells, calibrated cells, uniform prior and scaling panel did not run.

