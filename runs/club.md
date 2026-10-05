# The closed club: oracle benchmark for semantic self-recognition (specs/2026-10-04-club.md)

Predictions: `predictions/2026-10-04-club.md` (committed 3e20554 before any evaluation). Debugging runs: `runs/club_debug.md`. Code: `src/club.py` (language, evaluator, F), `src/club_static.py`, `src/club_lattice.py`, `src/club_maximal.py`, `src/club_chain.py`, this report `src/club_report.py`.

`CLUB(THEM)` is a global semantic oracle over the finite universe L_n, not a proof procedure. Nothing here is a realizability result.

## 1. Fixed points of the joint operator F

F(K) = {x : x(x) = C under P_K and x plays C against no program of L_n outside K}. F(K) ⊆ K for every K (prediction S1, a proof), so iteration from any start decreases to a fixed point and cycles cannot occur.

### Spec starts at n = 6, 7 (full set, empty set, 20 random sets with inclusion 1/2)

| grammar | n | universe | distinct fixed points (spec starts) | all fixed points found (+20 random subsets of K*) | |K*| from full set | cycles | union of found = fixed | all found ⊆ K* | monotonicity violations (50 random nested pairs) |
|---|---|---|---|---|---|---|---|---|---|
| full | 6 | 72 | 2 | 2 | 1 | none | True | True | 0 |
| full | 7 | 248 | 17 | 23 | 5 | none | True | True | 0 |
| pos | 6 | 67 | 2 | 2 | 1 | none | True | True | 0 |
| pos | 7 | 235 | 14 | 24 | 5 | none | True | True | 0 |

K* at n = 7: `CLUB(THEM)`, `and(BOX(THEM(ME)),CLUB(THEM))`, `and(BOX(THEM(THEM)),CLUB(THEM))`, `and(BOX1(THEM(ME)),CLUB(THEM))`, `and(BOX1(THEM(THEM)),CLUB(THEM))`.

### Every subset of K* is a fixed point (`runs/club_lattice.json`)

| grammar | n | |K*| | subsets that are fixed points | monotonicity violations (200 random nested pairs) |
|---|---|---|---|---|
| full | 6 | 1 | 2 of 2 | 0 |
| full | 7 | 5 | 32 of 32 | 0 |
| full | 8 | 9 | 512 of 512 | 50 |
| pos | 6 | 1 | 2 of 2 | 0 |
| pos | 7 | 5 | 32 of 32 | 0 |
| pos | 8 | 9 | 512 of 512 | 53 |

Membership of a guarded program `and(CLUB(THEM),ψ)` is self-fulfilling: in K it cooperates with itself (when ψ holds of it), out of K it defects on itself. So the fixed points below K* form the full Boolean lattice, and "the club" is one choice among 2^|K*|; the greatest-fixed-point rule picks all-in.

### The limit from the full set is not the greatest fixed point at n ≥ 8 (`runs/club_maximal.json`)

F is not monotone at n = 8 (25% of random nested pairs). A program such as `and(CLUB(THEM),BOXD(THEM(^D)))` (cooperate with members that provably defect on D) self-cooperates when D is outside K and defects on itself while D is still inside; starting from the full set it is removed at step 1 and never returns. Starts from the set G of guarded programs, and greedy ascent (add any single program, re-iterate, keep strict growth), find:

| grammar | n | guarded programs | |K| from full set | from G | ascended maximum | missed by the full-set start | unguarded members | incomparable fixed points met in ascent |
|---|---|---|---|---|---|---|---|---|
| full | 6 | 1 | 1 | 1 | 1 | — | 0 | 0 |
| full | 7 | 9 | 5 | 5 | 5 | — | 0 | 0 |
| full | 8 | 25 | 9 | 13 | 13 | `and(CLUB(THEM),BOXD(THEM(^C)))`, `and(CLUB(THEM),BOXD(THEM(^D)))`, `and(CLUB(THEM),BOXD1(THEM(^C)))`, `and(CLUB(THEM),BOXD1(THEM(^D)))` | 0 | 0 |
| full | 9 | 33 | 13 | 17 | 17 | `and(CLUB(THEM),BOXD(THEM(^C)))`, `and(CLUB(THEM),BOXD(THEM(^D)))`, `and(CLUB(THEM),BOXD1(THEM(^C)))`, `and(CLUB(THEM),BOXD1(THEM(^D)))` | 0 | 0 |
| pos | 6 | 1 | 1 | 1 | 1 | — | 0 | 0 |
| pos | 7 | 9 | 5 | 5 | 5 | — | 0 | 0 |
| pos | 8 | 25 | 9 | 13 | 13 | `and(CLUB(THEM),BOXD(THEM(^C)))`, `and(CLUB(THEM),BOXD(THEM(^D)))`, `and(CLUB(THEM),BOXD1(THEM(^C)))`, `and(CLUB(THEM),BOXD1(THEM(^D)))` | 0 | 0 |
| pos | 9 | 33 | 13 | 17 | 17 | `and(CLUB(THEM),BOXD(THEM(^C)))`, `and(CLUB(THEM),BOXD(THEM(^D)))`, `and(CLUB(THEM),BOXD1(THEM(^C)))`, `and(CLUB(THEM),BOXD1(THEM(^D)))` | 0 | 0 |

One maximal fixed point was found at every n (no incomparable fixed point met). The chain uses K_max, the largest found, as the spec defines the club as the largest such set. Every member at every n is guarded.

## 2. Sanity: the base language

| n | |K| |
|---|---|
| 6 | 0 |
| 7 | 0 |
| 8 | 0 |
| 9 | 0 |

## 3. Composition of K

### At the limit from the full set (first scored pass)

| grammar | n | canons | programs | behavioural classes | μ(K) | μ(`CLUB(THEM)`) | share of self-coop classes | within-K components (largest) | singletons only | suckerable members (μ) | neutral entrants into all-club-FairBot outside K | excluded unsuckerable μ (×μ(K)) | excluded suckerable μ | old-sense universality |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| full | 6 | 1 | 10 | 1 | 0.00465 | 0.00465 | 0.037 | 1 (1) | True | 0 (0) | 0 | 0.00938 (×2.02) | 0.4863 | 0 |
| full | 7 | 5 | 69 | 1 | 0.00480 | 0.00480 | 0.011 | 1 (1) | True | 0 (0) | 0 | 0.00964 (×2.01) | 0.4859 | 0 |
| full | 8 | 9 | 173 | 7 | 0.00482 | 0.00479 | 0.023 | 3 (3) | False | 5 (0.0048) | 0 | 0.00969 (×2.01) | 0.4857 | 0 |
| full | 9 | 13 | 1056 | 10 | 0.00488 | 0.00483 | 0.020 | 1 (10) | False | 7 (0.0048) | 0 | 0.00980 (×2.01) | 0.4855 | 0 |
| pos | 6 | 1 | 10 | 1 | 0.00465 | 0.00465 | 0.050 | 1 (1) | True | 0 (0) | 0 | 0.00946 (×2.03) | 0.4856 | 0 |
| pos | 7 | 5 | 69 | 1 | 0.00481 | 0.00481 | 0.012 | 1 (1) | True | 0 (0) | 0 | 0.00967 (×2.01) | 0.4852 | 0 |
| pos | 8 | 9 | 173 | 7 | 0.00483 | 0.00479 | 0.027 | 3 (3) | False | 5 (0.0048) | 0 | 0.00973 (×2.02) | 0.4849 | 0 |
| pos | 9 | 13 | 1056 | 10 | 0.00489 | 0.00484 | 0.023 | 1 (10) | False | 7 (0.0049) | 0 | 0.00984 (×2.01) | 0.4847 | 0 |

### At K_max (the chain's fixed point)

| grammar | n | canons | programs | behavioural classes | μ(K) | μ(`CLUB(THEM)`) | share of self-coop classes | within-K components (largest) | singletons only | suckerable members (μ) | neutral entrants into all-club-FairBot outside K | excluded unsuckerable μ (×μ(K)) | excluded suckerable μ | old-sense universality |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| full | 6 | 1 | 10 | 1 | 0.00465 | 0.00465 | 0.037 | 1 (1) | True | 0 (0) | 0 | 0.00938 (×2.02) | 0.4863 | 0 |
| full | 7 | 5 | 69 | 1 | 0.00480 | 0.00480 | 0.011 | 1 (1) | True | 0 (0) | 0 | 0.00964 (×2.01) | 0.4859 | 0 |
| full | 8 | 13 | 181 | 7 | 0.00483 | 0.00479 | 0.023 | 3 (3) | False | 5 (0.0048) | 0 | 0.00969 (×2.01) | 0.4857 | 0 |
| full | 9 | 17 | 1072 | 10 | 0.00488 | 0.00484 | 0.020 | 1 (10) | False | 7 (0.0049) | 0 | 0.00980 (×2.01) | 0.4855 | 0 |
| pos | 6 | 1 | 10 | 1 | 0.00465 | 0.00465 | 0.050 | 1 (1) | True | 0 (0) | 0 | 0.00946 (×2.03) | 0.4856 | 0 |
| pos | 7 | 5 | 69 | 1 | 0.00481 | 0.00481 | 0.012 | 1 (1) | True | 0 (0) | 0 | 0.00967 (×2.01) | 0.4852 | 0 |
| pos | 8 | 13 | 181 | 7 | 0.00483 | 0.00480 | 0.027 | 3 (3) | False | 5 (0.0048) | 0 | 0.00973 (×2.01) | 0.4849 | 0 |
| pos | 9 | 17 | 1072 | 10 | 0.00489 | 0.00484 | 0.023 | 1 (10) | False | 7 (0.0049) | 0 | 0.00984 (×2.01) | 0.4847 | 0 |

**Members at n = 8 (K_max)**, by μ:

| class | μ | canons | programs | suckerable (by) | mutual with `CLUB(THEM)` | mates in K |
|---|---|---|---|---|---|---|
| `CLUB(THEM)` | 0.00479 | 5 | 165 | yes (`and(CLUB(THEM),not(BOX(THEM(ME))))`) | True | 2 |
| `and(BOX(THEM(ME)),CLUB(THEM))` | 2.16e-05 | 3 | 6 | no | True | 2 |
| `and(BOX1(THEM(THEM)),CLUB(THEM))` | 7.2e-06 | 1 | 2 | yes (`and(CLUB(THEM),not(BOX(THEM(ME))))`) | True | 2 |
| `and(CLUB(THEM),not(BOX(THEM(ME))))` | 1.3e-06 | 1 | 2 | yes (`and(BOX(THEM(ME)),CLUB(THEM))`) | False | 1 |
| `and(CLUB(THEM),not(BOX(THEM(THEM))))` | 1.3e-06 | 1 | 2 | yes (`and(CLUB(THEM),not(BOX1(THEM(ME))))`) | False | 1 |
| `and(CLUB(THEM),not(BOX1(THEM(ME))))` | 1.3e-06 | 1 | 2 | yes (`and(BOX(THEM(ME)),CLUB(THEM))`) | False | 1 |
| `and(CLUB(THEM),not(BOX1(THEM(THEM))))` | 1.3e-06 | 1 | 2 | no | False | 1 |

Within-K mutual-cooperation components: {`CLUB(THEM)`, `and(BOX(THEM(ME)),CLUB(THEM))`, `and(BOX1(THEM(THEM)),CLUB(THEM))`} (complete); {`and(CLUB(THEM),not(BOX(THEM(ME))))`, `and(CLUB(THEM),not(BOX(THEM(THEM))))`} (complete); {`and(CLUB(THEM),not(BOX1(THEM(ME))))`, `and(CLUB(THEM),not(BOX1(THEM(THEM))))`} (complete).

Excluded unsuckerable classes (top): `BOX1(THEM(ME))` 0.0048, `BOX(THEM(ME))` 0.0048, `and(BOX(THEM(ME)),BOX(THEM(THEM)))` 1.4e-05, `and(BOX(THEM(THEM)),BOX1(THEM(ME)))` 7.2e-06, `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))` 7.2e-06, `and(BOX(THEM(ME)),BOX(THEM(^C)))` 3.9e-06.

P*-block (mutual cooperators of P* that do not cooperate with FairBot) in the same language: 46 classes, μ 0.0030. FairBot's component: 292 classes, μ 0.0307.

**Members at n = 9 (K_max)**, by μ:

| class | μ | canons | programs | suckerable (by) | mutual with `CLUB(THEM)` | mates in K |
|---|---|---|---|---|---|---|
| `CLUB(THEM)` | 0.00484 | 5 | 920 | yes (`and(CLUB(THEM),not(BOX(THEM(ME))))`) | True | 5 |
| `and(BOX(THEM(ME)),CLUB(THEM))` | 2.07e-05 | 2 | 64 | no | True | 3 |
| `and(BOX1(THEM(ME)),CLUB(THEM))` | 1.04e-05 | 1 | 32 | no | True | 4 |
| `and(BOX1(THEM(THEM)),CLUB(THEM))` | 1.04e-05 | 1 | 32 | yes (`and(CLUB(THEM),not(BOX(THEM(ME))))`) | True | 4 |
| `and(CLUB(THEM),not(BOX(THEM(ME))))` | 1.5e-06 | 1 | 4 | yes (`and(BOX(THEM(ME)),CLUB(THEM))`) | False | 3 |
| `and(CLUB(THEM),not(BOX(THEM(THEM))))` | 1.5e-06 | 1 | 4 | yes (`and(CLUB(THEM),not(BOX1(THEM(ME))))`) | False | 3 |
| `and(CLUB(THEM),not(BOX1(THEM(ME))))` | 1.5e-06 | 1 | 4 | yes (`and(BOX(THEM(ME)),CLUB(THEM))`) | False | 2 |
| `and(CLUB(THEM),not(BOX1(THEM(THEM))))` | 1.5e-06 | 1 | 4 | no | False | 2 |
| `and(CLUB(THEM),not(BOX(THEM(^C))))` | 4.3e-07 | 2 | 4 | yes (`and(BOX(THEM(ME)),CLUB(THEM))`) | True | 6 |
| `and(CLUB(THEM),not(BOX1(THEM(^C))))` | 4.3e-07 | 2 | 4 | yes (`and(BOX(THEM(ME)),CLUB(THEM))`) | True | 6 |

Within-K mutual-cooperation components: {`CLUB(THEM)`, `and(BOX(THEM(ME)),CLUB(THEM))`, `and(BOX1(THEM(ME)),CLUB(THEM))`, `and(BOX1(THEM(THEM)),CLUB(THEM))`, `and(CLUB(THEM),not(BOX(THEM(ME))))`, `and(CLUB(THEM),not(BOX(THEM(THEM))))`, `and(CLUB(THEM),not(BOX1(THEM(ME))))`, `and(CLUB(THEM),not(BOX1(THEM(THEM))))`}.

Excluded unsuckerable classes (top): `BOX1(THEM(ME))` 0.0049, `BOX(THEM(ME))` 0.0049, `and(BOX(THEM(ME)),BOX(THEM(THEM)))` 2.1e-05, `and(BOX(THEM(THEM)),BOX1(THEM(ME)))` 1e-05, `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))` 1e-05, `and(BOX(THEM(ME)),BOX(THEM(^C)))` 4.5e-06.

P*-block (mutual cooperators of P* that do not cooperate with FairBot) in the same language: 81 classes, μ 0.0031. FairBot's component: 496 classes, μ 0.0314.

### Cutoff dependence (K_max, members tracked by source string)

| n → n+1 | members at n | dropped | new members (examples) |
|---|---|---|---|
| 6 → 7 | 1 | 0 | 4 (`and(BOX(THEM(ME)),CLUB(THEM))`, `and(BOX1(THEM(ME)),CLUB(THEM))`, `and(BOX(THEM(THEM)),CLUB(THEM))`, `and(BOX1(THEM(THEM)),CLUB(THEM))`) |
| 7 → 8 | 5 | 0 | 8 (`and(CLUB(THEM),BOXD(THEM(^C)))`, `and(CLUB(THEM),BOXD(THEM(^D)))`, `and(CLUB(THEM),BOXD1(THEM(^C)))`, `and(CLUB(THEM),BOXD1(THEM(^D)))`) |
| 8 → 9 | 13 | 0 | 4 (`and(CLUB(THEM),not(BOX(THEM(^C))))`, `and(CLUB(THEM),not(BOX(THEM(^D))))`, `and(CLUB(THEM),not(BOX1(THEM(^C))))`, `and(CLUB(THEM),not(BOX1(THEM(^D))))`) |

## 4. The ε→0 chain (PD, w = 0.3, `eager_poly=False`, θ = 10⁻⁶) and controls

π(K): the chain's mass on states made only of K classes (club: K_max; clique: the clique; free: none). GTH: the log-domain monomorphic embedded chain (single-mutant fixation, no polymorphic routes). Residuals: ‖πP − π‖₁ for the linear chain; max relative balance error for GTH.

| arm | n | N | classes | P(C,C) | π(K) | π(K), GTH | log(1 − π(K)), GTH | top K state (π) | log exit rate out of K | cheapest exit (log ρ) | log entry flux into K from all-D | hitting time all-D → K | terminal | polymorphic π | residual lin / GTH | s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| club | 6 | 100 | 66 | 0.9989 | 0.998702 | 0.998702 | -6.6 | `CLUB(THEM)` (0.999) | -15.00 | `BOX(THEM(ME))` -10.90 | -8.54 | 4.12e+03 | 1 | 0.0e+00 | 5e-16 / 2e-14 | 1 |
| club | 6 | 1000 | 66 | 1.0000 | 1.000000 | 1.000000 | -74.4 | `CLUB(THEM)` (1.000) | -83.69 | `BOX(THEM(ME))` -79.55 | -9.67 | 9.36e+03 | 1 | 0.0e+00 | 9e-20 / 9e-14 | 1 |
| club | 6 | 10000 | 66 | 1.0000 | 1.000000 | 1.000000 | -749.1 | `CLUB(THEM)` (1.000) | -759.84 | `BOX(THEM(ME))` -755.70 | -10.81 | 3.52e+04 | 1 | 0.0e+00 | 1e-19 / 0e+00 | 1 |
| club | 6 | 100000 | 66 | 1.0000 | 1.000000 | 1.000000 | -7498.3 | `CLUB(THEM)` (1.000) | -7510.99 | `BOX(THEM(ME))` -7506.86 | -11.96 | 2.13e+05 | 1 | 0.0e+00 | 2e-17 / 9e-13 | 4 |
| club | 8 | 100 | 581 | 0.9988 | 0.998443 | 0.998443 | -6.5 | `and(CLUB(THEM),not(BOX1(THEM(THEM))))` (0.410) | -14.74 | `BOX1(THEM(ME))` -10.90 | -8.50 | 3.98e+03 | 1 | 0.0e+00 | 3e-15 / 8e-14 | 44 |
| club | 8 | 1000 | 581 | 1.0000 | 1.000000 | 1.000000 | -74.3 | `and(CLUB(THEM),not(BOX1(THEM(THEM))))` (0.995) | -83.26 | `BOX1(THEM(ME))` -79.55 | -9.63 | 9.25e+03 | 1 | 0.0e+00 | 3e-17 / 3e-13 | 45 |
| club | 8 | 10000 | 581 | 1.0000 | 1.000000 | 1.000000 | -749.0 | `and(CLUB(THEM),not(BOX1(THEM(THEM))))` (0.999) | -759.42 | `BOX1(THEM(ME))` -755.70 | -10.77 | 3.61e+04 | 1 | 0.0e+00 | 2e-16 / 6e-14 | 60 |
| club | 8 | 100000 | 581 | 1.0000 | 1.000000 | 1.000000 | -7498.2 | `and(CLUB(THEM),not(BOX1(THEM(THEM))))` (0.999) | -7510.57 | `BOX1(THEM(ME))` -7506.86 | -11.92 | 2.25e+05 | 1 | 0.0e+00 | 1e-16 / 4e-13 | 246 |
| clique | 6 | 100 | 53 | 0.9990 | 0.998809 | 0.998809 | -6.7 | `CLIQUE_1` (0.999) | -15.04 | `BOX(THEM(ME))` -10.90 | -8.49 | 3.91e+03 | 1 | 0.0e+00 | 2e-16 / 1e-14 | 0 |
| clique | 6 | 1000 | 53 | 1.0000 | 1.000000 | 1.000000 | -74.5 | `CLIQUE_1` (1.000) | -83.72 | `BOX(THEM(ME))` -79.55 | -9.62 | 8.96e+03 | 1 | 0.0e+00 | 7e-20 / 7e-14 | 0 |
| clique | 6 | 10000 | 53 | 1.0000 | 1.000000 | 1.000000 | -749.1 | `CLIQUE_1` (1.000) | -759.88 | `BOX(THEM(ME))` -755.70 | -10.76 | 3.43e+04 | 1 | 0.0e+00 | 2e-19 / 1e-13 | 1 |
| clique | 6 | 100000 | 53 | 1.0000 | 1.000000 | 1.000000 | -7498.3 | `CLIQUE_1` (1.000) | -7511.03 | `BOX(THEM(ME))` -7506.86 | -11.91 | 2.12e+05 | 1 | 0.0e+00 | 2e-17 / 9e-13 | 2 |
| clique | 8 | 100 | 485 | 0.9990 | 0.998752 | 0.998752 | -6.7 | `CLIQUE_1` (0.999) | -14.97 | `BOX1(THEM(ME))` -10.90 | -8.46 | 3.81e+03 | 1 | 0.0e+00 | 2e-15 / 9e-14 | 30 |
| clique | 8 | 1000 | 485 | 1.0000 | 1.000000 | 1.000000 | -74.4 | `CLIQUE_1` (1.000) | -83.65 | `BOX1(THEM(ME))` -79.55 | -9.59 | 8.94e+03 | 1 | 0.0e+00 | 9e-21 / 3e-13 | 32 |
| clique | 8 | 10000 | 485 | 1.0000 | 1.000000 | 1.000000 | -749.0 | `CLIQUE_1` (1.000) | -759.80 | `BOX1(THEM(ME))` -755.70 | -10.73 | 3.58e+04 | 1 | 0.0e+00 | 5e-17 / 5e-13 | 45 |
| clique | 8 | 100000 | 485 | 1.0000 | 1.000000 | 1.000000 | -7498.1 | `CLIQUE_1` (1.000) | -7510.95 | `BOX1(THEM(ME))` -7506.86 | -11.88 | 2.3e+05 | 1 | 0.0e+00 | 1e-16 / 9e-12 | 175 |
| free | 6 | 100 | 51 | 0.1693 | — | — | — | — | — | — | — | — | 1 | 0.0e+00 | 8e-16 / 1e-14 | 0 |
| free | 6 | 1000 | 51 | 0.3453 | — | — | — | — | — | — | — | — | 1 | 0.0e+00 | 3e-16 / 1e-14 | 0 |
| free | 6 | 10000 | 51 | 0.5869 | — | — | — | — | — | — | — | — | 1 | 0.0e+00 | 2e-16 / 1e-14 | 0 |
| free | 6 | 100000 | 51 | 0.8137 | — | — | — | — | — | — | — | — | 1 | 0.0e+00 | 2e-16 / 1e-14 | 2 |
| free | 8 | 100 | 471 | 0.1821 | — | — | — | — | — | — | — | — | 1 | 0.0e+00 | 1e-15 / 1e-13 | 29 |
| free | 8 | 1000 | 471 | 0.3707 | — | — | — | — | — | — | — | — | 1 | 0.0e+00 | 7e-16 / 9e-14 | 29 |
| free | 8 | 10000 | 471 | 0.6172 | — | — | — | — | — | — | — | — | 1 | 0.0e+00 | 3e-15 / 7e-14 | 40 |
| free | 8 | 100000 | 471 | 0.8135 | — | — | — | — | — | — | — | — | 1 | 0.0e+00 | 1e-15 / 7e-14 | 161 |

### Exits from the top K state, per mutation event (log domain, single-mutant fixation; last column: transition weights in the linear chain)

| arm | n | N | top state | strict in K | neutral in K | weak in K | deleterious in K | deleterious out of K | linear chain: kinds with nonzero weight |
|---|---|---|---|---|---|---|---|---|---|
| club | 6 | 100 | `CLUB(THEM)` | — | — | — | — | -15.00 | deleterious_out 3.1e-07 |
| club | 6 | 1000 | `CLUB(THEM)` | — | — | — | — | -83.69 | deleterious_out 4.5e-37 |
| club | 6 | 10000 | `CLUB(THEM)` | — | — | — | — | -759.84 | — |
| club | 6 | 100000 | `CLUB(THEM)` | — | — | — | — | -7510.99 | — |
| club | 8 | 100 | `and(CLUB(THEM),not(BOX1(THEM(THEM))))` | — | -18.16 | — | -21.35 | -14.59 | deleterious_out 4.6e-07, deleterious_in 5.3e-10, neutral_in 1.3e-08 |
| club | 8 | 1000 | `and(CLUB(THEM),not(BOX1(THEM(THEM))))` | — | -20.46 | — | -90.01 | -83.26 | deleterious_out 6.9e-37, deleterious_in 8.1e-40, neutral_in 1.3e-09 |
| club | 8 | 10000 | `and(CLUB(THEM),not(BOX1(THEM(THEM))))` | — | -22.77 | — | -766.16 | -759.42 | neutral_in 1.3e-10 |
| club | 8 | 100000 | `and(CLUB(THEM),not(BOX1(THEM(THEM))))` | — | -25.07 | — | -7517.31 | -7510.57 | neutral_in 1.3e-11 |
| clique | 6 | 100 | `CLIQUE_1` | — | — | — | — | -15.04 | deleterious_out 2.9e-07 |
| clique | 6 | 1000 | `CLIQUE_1` | — | — | — | — | -83.72 | deleterious_out 4.4e-37 |
| clique | 6 | 10000 | `CLIQUE_1` | — | — | — | — | -759.88 | — |
| clique | 6 | 100000 | `CLIQUE_1` | — | — | — | — | -7511.03 | — |
| clique | 8 | 100 | `CLIQUE_1` | — | — | — | — | -14.97 | deleterious_out 3.2e-07 |
| clique | 8 | 1000 | `CLIQUE_1` | — | — | — | — | -83.65 | deleterious_out 4.7e-37 |
| clique | 8 | 10000 | `CLIQUE_1` | — | — | — | — | -759.80 | — |
| clique | 8 | 100000 | `CLIQUE_1` | — | — | — | — | -7510.95 | — |

### Fitted exit and residence slopes

| arm | n | d log(exit out of K)/dN, N ∈ [10³, 10⁵] | log-log slope of exit out of K, N ∈ [10², 10³] | d log(1−π(K))/dN, N ∈ [10³, 10⁵] |
|---|---|---|---|---|
| club | 6 | -0.07502 | -29.8 | -0.07499 |
| club | 8 | -0.07502 | -29.8 | -0.07499 |
| clique | 6 | -0.07502 | -29.8 | -0.07499 |
| clique | 8 | -0.07502 | -29.8 | -0.07499 |

w/4 = 0.075: the cheapest exit out of K is a symmetric coordination with a non-member self-cooperator (FairBot), whose fixation is e^(−wN/4 + O(log N)).

### Entry from all-D

| arm | n | N | payoff (u(x,x), u(x,D), u(D,x), u(D,D)) of club-FairBot / FairBot / `CLUB(THEM)` | log ρ(club-FairBot) | log ρ(FairBot) | log ρ(`CLUB(THEM)`) | |difference| | K members entering neutrally |
|---|---|---|---|---|---|---|---|---|
| club | 6 | 100 | — / (0.0, -1.0, -1.0, -1.0) / (0.0, -1.0, -1.0, -1.0) | — (merged with `CLUB(THEM)`) | -3.168685 | -3.168685 | 0.0e+00 | 1 |
| club | 6 | 1000 | — / (0.0, -1.0, -1.0, -1.0) / (0.0, -1.0, -1.0, -1.0) | — (merged with `CLUB(THEM)`) | -4.294924 | -4.294924 | 0.0e+00 | 1 |
| club | 6 | 10000 | — / (0.0, -1.0, -1.0, -1.0) / (0.0, -1.0, -1.0, -1.0) | — (merged with `CLUB(THEM)`) | -5.437263 | -5.437263 | 0.0e+00 | 1 |
| club | 6 | 100000 | — / (0.0, -1.0, -1.0, -1.0) / (0.0, -1.0, -1.0, -1.0) | — (merged with `CLUB(THEM)`) | -6.585617 | -6.585617 | 0.0e+00 | 1 |
| club | 8 | 100 | (0.0, -1.0, -1.0, -1.0) / (0.0, -1.0, -1.0, -1.0) / (0.0, -1.0, -1.0, -1.0) | -3.168685 | -3.168685 | -3.168685 | 0.0e+00 | 7 |
| club | 8 | 1000 | (0.0, -1.0, -1.0, -1.0) / (0.0, -1.0, -1.0, -1.0) / (0.0, -1.0, -1.0, -1.0) | -4.294924 | -4.294924 | -4.294924 | 0.0e+00 | 7 |
| club | 8 | 10000 | (0.0, -1.0, -1.0, -1.0) / (0.0, -1.0, -1.0, -1.0) / (0.0, -1.0, -1.0, -1.0) | -5.437263 | -5.437263 | -5.437263 | 0.0e+00 | 7 |
| club | 8 | 100000 | (0.0, -1.0, -1.0, -1.0) / (0.0, -1.0, -1.0, -1.0) / (0.0, -1.0, -1.0, -1.0) | -6.585617 | -6.585617 | -6.585617 | 0.0e+00 | 7 |

### Support (π ≥ 10⁻⁴) and networks

- club n=6 N=100: mono {CLUB(THEM):1} 0.9987; mono {D:1} 0.0011; blocks 1, rival share 0.000
- club n=6 N=1000: mono {CLUB(THEM):1} 1.0000; blocks 1, rival share 0.000
- club n=6 N=10000: mono {CLUB(THEM):1} 1.0000; blocks 1, rival share 0.000
- club n=6 N=100000: mono {CLUB(THEM):1} 1.0000; blocks 1, rival share 0.000
- club n=8 N=100: mono {and(CLUB(THEM),not(BOX1(THEM(THEM)))):1} 0.4099; mono {CLUB(THEM):1} 0.4058; mono {and(CLUB(THEM),not(BOX(THEM(THEM)))):1} 0.1289; mono {and(CLUB(THEM),not(BOX1(THEM(ME)))):1} 0.0242; mono {and(CLUB(THEM),not(BOX(THEM(ME)))):1} 0.0208; blocks 3, rival share 0.565
- club n=8 N=1000: mono {and(CLUB(THEM),not(BOX1(THEM(THEM)))):1} 0.9951; mono {CLUB(THEM):1} 0.0024; mono {and(CLUB(THEM),not(BOX(THEM(THEM)))):1} 0.0013; mono {and(BOX(THEM(ME)),CLUB(THEM)):1} 0.0006; mono {and(CLUB(THEM),not(BOX1(THEM(ME)))):1} 0.0003; blocks 3, rival share 0.004
- club n=8 N=10000: mono {and(CLUB(THEM),not(BOX1(THEM(THEM)))):1} 0.9989; mono {and(BOX(THEM(ME)),CLUB(THEM)):1} 0.0006; mono {CLUB(THEM):1} 0.0002; mono {and(CLUB(THEM),not(BOX(THEM(THEM)))):1} 0.0001; blocks 1, rival share 0.000
- club n=8 N=100000: mono {and(CLUB(THEM),not(BOX1(THEM(THEM)))):1} 0.9994; mono {and(BOX(THEM(ME)),CLUB(THEM)):1} 0.0006; blocks 1, rival share 0.000
- clique n=6 N=100: mono {CLIQUE_1:1} 0.9988; mono {D:1} 0.0010; blocks 1, rival share 0.000
- clique n=6 N=1000: mono {CLIQUE_1:1} 1.0000; blocks 1, rival share 0.000
- clique n=6 N=10000: mono {CLIQUE_1:1} 1.0000; blocks 1, rival share 0.000
- clique n=6 N=100000: mono {CLIQUE_1:1} 1.0000; blocks 1, rival share 0.000
- clique n=8 N=100: mono {CLIQUE_1:1} 0.9988; mono {D:1} 0.0010; blocks 1, rival share 0.000
- clique n=8 N=1000: mono {CLIQUE_1:1} 1.0000; blocks 1, rival share 0.000
- clique n=8 N=10000: mono {CLIQUE_1:1} 1.0000; blocks 1, rival share 0.000
- clique n=8 N=100000: mono {CLIQUE_1:1} 1.0000; blocks 1, rival share 0.000
- free n=6 N=100: mono {D:1} 0.8299; mono {BOX(THEM(THEM)):1} 0.0372; mono {BOX(THEM(ME)):1} 0.0372; mono {BOX1(THEM(ME)):1} 0.0371; mono {BOX1(THEM(THEM)):1} 0.0322; blocks 1, rival share 0.000
- free n=6 N=1000: mono {D:1} 0.6545; mono {BOX(THEM(THEM)):1} 0.0945; mono {BOX(THEM(ME)):1} 0.0945; mono {BOX1(THEM(ME)):1} 0.0941; mono {BOX1(THEM(THEM)):1} 0.0393; blocks 1, rival share 0.000
- free n=6 N=10000: mono {D:1} 0.4130; mono {BOX(THEM(THEM)):1} 0.1894; mono {BOX(THEM(ME)):1} 0.1893; mono {BOX1(THEM(ME)):1} 0.1886; mono {BOX1(THEM(THEM)):1} 0.0127; blocks 1, rival share 0.000
- free n=6 N=100000: mono {BOX(THEM(THEM)):1} 0.2706; mono {BOX(THEM(ME)):1} 0.2706; mono {BOX1(THEM(ME)):1} 0.2695; mono {D:1} 0.1863; mono {BOX1(THEM(THEM)):1} 0.0019; blocks 1, rival share 0.000
- free n=8 N=100: mono {D:1} 0.8166; mono {BOX(THEM(ME)):1} 0.0379; mono {BOX1(THEM(ME)):1} 0.0378; mono {BOX(THEM(THEM)):1} 0.0377; mono {BOX1(THEM(THEM)):1} 0.0326; blocks 2, rival share 0.034
- free n=8 N=1000: mono {D:1} 0.6288; mono {BOX(THEM(ME)):1} 0.0940; mono {BOX1(THEM(ME)):1} 0.0935; mono {BOX(THEM(THEM)):1} 0.0925; mono {BOX1(THEM(THEM)):1} 0.0370; blocks 2, rival share 0.067
- free n=8 N=10000: mono {D:1} 0.3826; mono {BOX(THEM(ME)):1} 0.1816; mono {BOX1(THEM(ME)):1} 0.1804; mono {BOX(THEM(THEM)):1} 0.1633; mono {and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):1} 0.0410; blocks 2, rival share 0.100
- free n=8 N=100000: mono {BOX(THEM(ME)):1} 0.2791; mono {BOX1(THEM(ME)):1} 0.2773; mono {D:1} 0.1864; mono {BOX(THEM(THEM)):1} 0.1353; mono {and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):1} 0.0675; blocks 2, rival share 0.125

### Top out-of-K destinations from the top state (log rate per mutation event)

- club n=6 N=100: `BOX(THEM(ME))` -16.26; `BOX1(THEM(ME))` -16.26; `BOX(THEM(^C))` -17.51
- club n=6 N=1000: `BOX(THEM(ME))` -84.92; `BOX1(THEM(ME))` -84.92; `BOX(THEM(^C))` -86.17
- club n=6 N=10000: `BOX(THEM(ME))` -761.07; `BOX1(THEM(ME))` -761.07; `BOX(THEM(^C))` -762.32
- club n=6 N=100000: `BOX(THEM(ME))` -7512.22; `BOX1(THEM(ME))` -7512.22; `BOX(THEM(^C))` -7513.47
- club n=8 N=100: `BOX1(THEM(ME))` -16.23; `BOX(THEM(ME))` -16.23; `BOX(THEM(THEM))` -16.24
- club n=8 N=1000: `BOX1(THEM(ME))` -84.89; `BOX(THEM(ME))` -84.89; `BOX(THEM(THEM))` -84.89
- club n=8 N=10000: `BOX1(THEM(ME))` -761.04; `BOX(THEM(ME))` -761.04; `BOX(THEM(THEM))` -761.04
- club n=8 N=100000: `BOX1(THEM(ME))` -7512.19; `BOX(THEM(ME))` -7512.19; `BOX(THEM(THEM))` -7512.20
- clique n=6 N=100: `BOX(THEM(ME))` -16.21; `BOX1(THEM(ME))` -16.21; `BOX(THEM(^C))` -17.49
- clique n=6 N=1000: `BOX(THEM(ME))` -84.87; `BOX1(THEM(ME))` -84.87; `BOX(THEM(^C))` -86.15
- clique n=6 N=10000: `BOX(THEM(ME))` -761.02; `BOX1(THEM(ME))` -761.02; `BOX(THEM(^C))` -762.30
- clique n=6 N=100000: `BOX(THEM(ME))` -7512.17; `BOX1(THEM(ME))` -7512.17; `BOX(THEM(^C))` -7513.45
- clique n=8 N=100: `BOX1(THEM(ME))` -16.18; `BOX(THEM(ME))` -16.18; `BOX1(THEM(^C))` -17.38
- clique n=8 N=1000: `BOX1(THEM(ME))` -84.84; `BOX(THEM(ME))` -84.84; `BOX1(THEM(^C))` -86.04
- clique n=8 N=10000: `BOX1(THEM(ME))` -760.99; `BOX(THEM(ME))` -760.99; `BOX1(THEM(^C))` -762.19
- clique n=8 N=100000: `BOX1(THEM(ME))` -7512.14; `BOX(THEM(ME))` -7512.14; `BOX1(THEM(^C))` -7513.34

## 5. Extra diagnostic (not predicted): the chain on a smaller fixed point

K' = K_max at n = 8 without the four member-exploiting `and(CLUB(THEM),not(BOX...))` members and the four BOXD-guarded ones (which behave as `CLUB(THEM)`): `CLUB(THEM)`, `and(BOX(THEM(ME)),CLUB(THEM))`, `and(BOX(THEM(THEM)),CLUB(THEM))`, `and(BOX1(THEM(ME)),CLUB(THEM))`, `and(BOX1(THEM(THEM)),CLUB(THEM))`. K' is a fixed point (every subset of K* is). Its five members are behaviourally one class, `CLUB(THEM)`.

| N | P(C,C) | π(K') | top state (π) | hitting time all-D → K' |
|---|---|---|---|---|
| 100 | 0.9989 | 0.998649 | `CLUB(THEM)` (0.999) | 3.98e+03 |
| 1000 | 1.0000 | 1.000000 | `CLUB(THEM)` (1.000) | 9.27e+03 |
| 10000 | 1.0000 | 1.000000 | `CLUB(THEM)` (1.000) | 3.65e+04 |

At K_max the stationary mass sits on `and(CLUB(THEM),not(BOX1(THEM(THEM))))` (μ 1.3·10⁻⁶), the unsuckerable end of a within-club faker ladder; at K' it sits on `CLUB(THEM)`. Which member holds the club is decided by the fixed-point selection, not by the dynamics.
