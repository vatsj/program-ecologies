# Rivals under the bounded prover K: does incompleteness remove the bridge-less obstruction? (`src/rivals_under_k.py`)

Spec `specs/2026-10-05-rivals-under-k.md` (reviewed by gpt-6.1-sol); predictions `predictions/2026-10-05-rivals-under-k.md`. Modal language L_8 (610 canonical sources) under the free box (GL+Def table) and under K at global budget b (guard at the reader's own budget; `runs/k-at-n8/kval_n8_b*.npy`). PD, w = 0.3, ε = 0, iid length-prior seeds at n = 8 drawn at source level and lumped by each arm's classes (paired seeds across arms), complete island graph, N = 200, I = 64, generation = I·N births, horizon 10⁵ (continuation 3·10⁵). **Finite-cutoff (n = 8), finite-horizon evidence about the bridge-less obstruction relative to FairBot's pair; not a large-population or large-cutoff conclusion; incompatible non-A networks beyond the static graph, longer bridge paths and larger cutoffs are untested here.** Intervals: Wilson 95% over runs (runs are the independent units); one-sided 95% upper bounds Clopper–Pearson (≈ 3/n at zero events); hazards exact Poisson, 3/exposure at zero losses; resolution times right-censored (Kaplan–Meier); q_est by run bootstrap over paired seeds.

**What ran.** Everything in the spec's priority order that the screening left runnable: the static screening (free, K b = 16, 4, 54) with the lumping validity check and the free reproduction; the m = 0 calibration (free, K b = 16, K b = 4; 120 runs each); (a) the matched natural arms, 3,000 runs each: free at its calibrated boundary mN = 1.091 (= the common mN), K b = 16 at its calibrated 1.200 and at the common 1.091; (b) the positive control (PrudentBot under K b = 16, dense, 100 runs); (c) forced P\* under K b = 16 with the inert-D and iid controls, and forced P\* under the free box as a reference beyond the spec, 100 runs each with paired m = 0 references; (e) the continuation of all 8 separated natural runs to 3·10⁵. **(d) did not run:** the screening found no direct-bridge-less rival of A under K at b = 16. Beyond the spec (declared in the predictions): a K b = 4 natural cell at its calibrated mN = 1.091, **stopped at 50 runs** (declared 1,000; the complete prefix of reps 0–49, so no selection by run length; stopped when the machine load reached 35–45 on 10 cores and separated K b = 4 runs took several minutes each; §7).

## 1. Static screening (n = 8; free, K b = 16, and K b = 4, 54 for budget sensitivity)

**Checks.** Free reproduction: the class table built from the GL+Def table equals `modal.build(8)` (the n = 8 free table `seeds_in_n` uses): 471 classes, names equal, payoffs equal, max |Δμ| 4.4e-15. Lumping validity (behavioural class = identical directed row and column; checked exhaustively, every arm): 
free 471 classes, 0 member violations, mass error 1.7e-18, seed-draw max |z| 2.5, 610 sources tested, mismatches 0; K b = 16 476 classes, 0 member violations, mass error 3.5e-18, seed-draw max |z| 2.6, 610 sources tested, mismatches 0; K b = 4 83 classes, 0 member violations, mass error 2.2e-17, seed-draw max |z| 2.0, 610 sources tested, mismatches 0; K b = 54 255 classes, 0 member violations, mass error 5.6e-17, seed-draw max |z| 2.8, 610 sources tested, mismatches 0. The establisher, rival and direct-bridge tests (existence and mass) were compared between lumped and source-level tables on **all 610 sources** (the spec's 1,000-source sample exceeds the language).

| arm | classes | establishers (μ cut) | rivals (full / half) | rival μ cut [raw] | direct-bridge-less: n, share of rival μ [raw μ] | hard share | no mediator path ≤ 3 (establisher / cooperative graph) | A-faked share | P\* family share | fixation at N = 200: zero / < 10⁻¹² / positive | at N = 400 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| free | 471 | 96 (0.0242) | 12 (6 / 6) | 1.8e-05 [1.4e-05] | 2, **0.221** [3.1e-06] | 0.221 | 0.000 / 0.000 | 0.147 | 0.221 | 0 / 0 / 12 | 0 / 12 / 0 |
| K b = 16 | 476 | 93 (0.0242) | 2 (0 / 2) | 2.7e-06 [2.1e-06] | 0, **0.000** [0] | 0.000 | 0.000 / 0.000 | 0.000 | 0.000 | 0 / 0 / 2 | 0 / 2 / 0 |
| K b = 54 | 255 | 52 (0.0242) | 2 (0 / 2) | 2.7e-06 [2.1e-06] | 0, **0.000** [0] | 0.000 | 0.000 / 0.000 | 0.000 | 0.000 | 0 / 0 / 2 | 0 / 2 / 0 |
| K b = 4 | 83 | 25 (0.0281) | 18 (5 / 13) | 0.0168 [0.0128] | 18, **1.000** [0.0128] | 0.906 | 0.091 / 0.091 | 0.094 | 0.000 | 0 / 0 / 18 | 0 / 18 / 0 |

Rivals of A = {FairBot, `BOX1(THEM(ME))`} (cut μ; bridges = cooperative classes mutually cooperating with FairBot, `BOX1(THEM(ME))` and R; path = shortest path to A in the establisher mutual-cooperation graph):

| arm | rival | μ | full | P\* family | direct bridges (μ, heaviest) | mediators | A-faked | path | ρ(R→A_j), ρ(A_j→R) at N = 200 |
|---|---|---|---|---|---|---|---|---|---|
| free | `BOX1(THEM(^not(BOX(THEM(ME)))))` | 3.8e-06 | yes |  | 45 (5.2e-03, `BOX1(THEM(THEM))`) | 0 |  | 2 | 7.2e-09, 7.2e-09, 7.2e-09, 7.2e-09 |
| free | `BOX1(THEM(^not(BOX(THEM(THEM)))))` | 3.8e-06 | yes |  | 45 (5.2e-03, `BOX1(THEM(THEM))`) | 0 |  | 2 | 7.2e-09, 7.2e-09, 7.2e-09, 7.2e-09 |
| free | `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 2.7e-06 | yes | yes | 0 (0, `–`) | 0 |  | 3 | 7.2e-09, 7.2e-09, 7.2e-09, 7.2e-09 |
| free | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 1.4e-06 | half |  | 12 (5.1e-03, `BOX(THEM(THEM))`) | 0 |  | 1 | 7.2e-09, 7.2e-09 |
| free | `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` | 1.4e-06 | half |  | 13 (5.1e-03, `BOX(THEM(THEM))`) | 6 |  | 1 | 7.2e-09, 7.2e-09 |
| free | `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 1.4e-06 | yes | yes | 0 (0, `–`) | 0 |  | 3 | 7.2e-09, 7.2e-09, 7.2e-09, 7.2e-09 |
| free | `not(BOXD1(THEM(^not(BOX(THEM(ME))))))` | 6.8e-07 | half |  | 30 (5.2e-05, `or(BOX(THEM(ME)),not(BOX(THEM(THEM))))`) | 53 | yes | 2 | 7.2e-09, 7.2e-09 |
| free | `not(BOXD1(THEM(^not(BOX(THEM(THEM))))))` | 6.8e-07 | half |  | 28 (4.6e-05, `or(BOX(THEM(ME)),not(BOX(THEM(THEM))))`) | 53 | yes | 2 | 7.2e-09, 7.2e-09 |
| free | `not(BOXD1(THEM(^not(BOX1(THEM(ME))))))` | 6.8e-07 | half |  | 32 (5.5e-05, `or(BOX(THEM(ME)),not(BOX(THEM(THEM))))`) | 53 | yes | 2 | 7.2e-09, 7.2e-09 |
| free | `not(BOXD1(THEM(^not(BOX1(THEM(THEM))))))` | 6.8e-07 | half |  | 30 (4.9e-05, `or(BOX(THEM(ME)),not(BOX(THEM(THEM))))`) | 53 | yes | 2 | 7.2e-09, 7.2e-09 |
| free | `BOX1(THEM(^not(BOX(THEM(^C)))))` | 6.8e-07 | yes |  | 45 (5.2e-03, `BOX1(THEM(THEM))`) | 0 |  | 2 | 7.2e-09, 7.2e-09, 7.2e-09, 7.2e-09 |
| free | `BOX1(THEM(^not(BOX(THEM(^D)))))` | 6.8e-07 | yes |  | 45 (5.2e-03, `BOX1(THEM(THEM))`) | 0 |  | 2 | 7.2e-09, 7.2e-09, 7.2e-09, 7.2e-09 |
| K b = 16 | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 1.4e-06 | half |  | 9 (5.1e-03, `BOX(THEM(THEM))`) | 0 |  | 1 | 7.2e-09, 7.2e-09 |
| K b = 16 | `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` | 1.4e-06 | half |  | 17 (5.1e-03, `BOX(THEM(THEM))`) | 10 |  | 1 | 7.2e-09, 7.2e-09 |
| K b = 54 | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 1.4e-06 | half |  | 12 (5.1e-03, `BOX(THEM(THEM))`) | 0 |  | 1 | 7.2e-09, 7.2e-09 |
| K b = 54 | `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` | 1.4e-06 | half |  | 13 (5.1e-03, `BOX(THEM(THEM))`) | 4 |  | 1 | 7.2e-09, 7.2e-09 |
| K b = 4 | `BOX(THEM(ME))` | 5.0e-03 | half |  | 0 (0, `–`) | 0 |  | 0 | 7.2e-09, 7.2e-09 |
| K b = 4 | `BOX(THEM(THEM))` | 5.0e-03 | half |  | 0 (0, `–`) | 0 |  | 1 | 7.2e-09, 7.2e-09 |
| K b = 4 | `BOX1(THEM(ME))` | 5.0e-03 | half |  | 0 (0, `–`) | 0 |  | 0 | 7.2e-09, 7.2e-09 |
| K b = 4 | `BOX(THEM(^C))` | 1.5e-03 | half |  | 0 (0, `–`) | 0 | yes | None | 7.2e-09, 7.2e-09 |
| K b = 4 | `BOX(THEM(^BOX(THEM(ME))))` | 3.1e-05 | half |  | 0 (0, `–`) | 0 |  | 1 | 7.2e-09, 7.2e-09 |
| K b = 4 | `BOX(THEM(^BOX(THEM(THEM))))` | 3.1e-05 | half |  | 0 (0, `–`) | 0 | yes | 2 | 7.2e-09, 7.2e-09 |
| K b = 4 | `or(BOX(THEM(ME)),BOX(THEM(THEM)))` | 1.5e-05 | half |  | 0 (0, `–`) | 0 |  | 1 | 7.2e-09, 7.2e-09 |
| K b = 4 | `or(BOX(THEM(ME)),BOX1(THEM(ME)))` | 7.6e-06 | yes |  | 0 (0, `–`) | 0 |  | 2 | 7.2e-09, 7.2e-09, 7.2e-09, 7.2e-09 |
| K b = 4 | `not(or(BOXD(THEM(ME)),BOX1(THEM(THEM))))` | 5.5e-06 | yes |  | 0 (0, `–`) | 0 |  | 2 | 7.2e-09, 7.2e-09, 7.2e-09, 7.2e-09 |
| K b = 4 | `not(or(BOX(THEM(THEM)),BOXD(THEM(ME))))` | 5.5e-06 | half |  | 0 (0, `–`) | 0 | yes | 3 | 7.2e-09, 7.2e-09 |
| K b = 4 | `or(BOX(THEM(ME)),BOX(THEM(^C)))` | 1.4e-06 | half |  | 0 (0, `–`) | 0 | yes | 2 | 7.2e-09, 7.2e-09 |
| K b = 4 | `or(BOX(THEM(ME)),BOX(THEM(^D)))` | 1.4e-06 | yes |  | 0 (0, `–`) | 0 |  | 2 | 7.2e-09, 7.2e-09, 7.2e-09, 7.2e-09 |
| K b = 4 | `or(BOX(THEM(ME)),BOX1(THEM(^C)))` | 1.4e-06 | yes |  | 0 (0, `–`) | 0 |  | 2 | 7.2e-09, 7.2e-09, 7.2e-09, 7.2e-09 |
| K b = 4 | `or(BOX(THEM(ME)),BOX1(THEM(^D)))` | 1.4e-06 | yes |  | 0 (0, `–`) | 0 |  | 2 | 7.2e-09, 7.2e-09, 7.2e-09, 7.2e-09 |
| K b = 4 | `or(BOX(THEM(THEM)),BOX(THEM(^C)))` | 1.4e-06 | half |  | 0 (0, `–`) | 0 |  | 1 | 7.2e-09, 7.2e-09 |
| K b = 4 | `or(BOX(THEM(THEM)),BOX(THEM(^D)))` | 1.4e-06 | half |  | 0 (0, `–`) | 0 |  | 1 | 7.2e-09, 7.2e-09 |
| K b = 4 | `or(BOX(THEM(THEM)),BOX1(THEM(^C)))` | 1.4e-06 | half |  | 0 (0, `–`) | 0 |  | 1 | 7.2e-09, 7.2e-09 |
| K b = 4 | `or(BOX(THEM(THEM)),BOX1(THEM(^D)))` | 1.4e-06 | half |  | 0 (0, `–`) | 0 |  | 1 | 7.2e-09, 7.2e-09 |

**Compatibility / bridge graph** (nodes: establishers and A; edges: mutual cooperation):

| arm | nodes | components (largest) | A's component μ / establisher μ | FairBot and `BOX1(THEM(ME))` connected | path length to A: count | by μ | mutually-defecting establisher pairs (n, μ²-mass) |
|---|---|---|---|---|---|---|---|
| free | 96 | 1 (96) | 0.0242 / 0.0242 | yes | 0: 2, 1: 70, 2: 22, 3: 2 | 0: 0.0102, 1: 0.0138, 2: 2.7e-04, 3: 4.1e-06 | 324, 2.2e-07 |
| K b = 16 | 93 | 1 (93) | 0.0242 / 0.0242 | yes | 0: 2, 1: 57, 2: 34 | 0: 0.0101, 1: 0.0135, 2: 5.3e-04 | 133, 3.5e-08 |
| K b = 54 | 52 | 1 (52) | 0.0242 / 0.0242 | yes | 0: 2, 1: 33, 2: 17 | 0: 0.0102, 1: 0.0134, 2: 5.3e-04 | 18, 2.0e-08 |
| K b = 4 | 25 | 4 (22, 1, 1, 1) | 0.0164 / 0.0281 | **no** | -1: 2, 0: 2, 1: 9, 2: 11, 3: 1 | -1: 6.6e-03, 0: 0.0101, 1: 5.1e-03, 2: 6.3e-03, 3: 5.5e-06 | 87, 6.8e-05 |

(path −1 = not connected to A.) **New rivals under K by source identity** (a canonical source that is a rival of A under K's table and not under the free table):

| arm | new rivals: n, cut μ (bridge-less μ) | lost (rival under free, not under K): n, cut μ | kept |
|---|---|---|---|
| K b = 16 | 0, 0 (0) | 11, 1.6e-05 | 2 |
| K b = 4 | 25, 0.0168 (0.0168) | 13, 1.8e-05 | 0 |
| K b = 54 | 0, 0 (0) | 11, 1.6e-05 | 2 |

Lost at b = 16 (sources): `BOX1(THEM(^not(BOX(THEM(ME)))))` (3.8e-06), `BOX1(THEM(^not(BOX(THEM(THEM)))))` (3.8e-06), `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` (1.4e-06), `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` (1.4e-06), `and(BOX1(THEM(THEM)),not(BOX(THEM(THEM))))` (1.4e-06), `not(BOXD1(THEM(^not(BOX(THEM(ME))))))` (6.8e-07), `not(BOXD1(THEM(^not(BOX(THEM(THEM))))))` (6.8e-07), `not(BOXD1(THEM(^not(BOX1(THEM(ME))))))` (6.8e-07), `not(BOXD1(THEM(^not(BOX1(THEM(THEM))))))` (6.8e-07), `BOX1(THEM(^not(BOX(THEM(^C)))))` (6.8e-07), `BOX1(THEM(^not(BOX(THEM(^D)))))` (6.8e-07). New at b = 4: `BOX(THEM(ME))` (5.0e-03), `BOX(THEM(THEM))` (5.0e-03), `BOX1(THEM(ME))` (5.0e-03), `BOX(THEM(^C))` (1.5e-03), `BOX(THEM(^BOX(THEM(ME))))` (3.1e-05), `BOX(THEM(^BOX(THEM(THEM))))` (3.1e-05), `or(BOX(THEM(ME)),BOX(THEM(THEM)))` (7.6e-06), `or(BOX(THEM(ME)),BOX1(THEM(ME)))` (7.6e-06), `or(BOX(THEM(THEM)),BOX1(THEM(ME)))` (7.6e-06), `not(or(BOX(THEM(THEM)),BOXD(THEM(ME))))` (1.4e-06), …

**P\* under each table** (`and(BOX1(THEM(ME)),not(BOX(THEM(ME))))`):

| arm | class | self-play | vs FairBot (P\*, FB) | vs `BOX1(THEM(ME))` | row = D's row | column ≠ D's in | prey μ not D's (establishers: n, μ) | D's prey not P\*'s μ |
|---|---|---|---|---|---|---|---|---|
| free | `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` (2 members) | C | DD | DD | no | 150 classes | 0.0108 (27, 5.1e-03) | 0.0178 |
| K b = 16 | `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` (1 members) | D | DD | DD | yes | 175 classes | 5.8e-03 (40, 8.1e-05) | 0.0138 |
| K b = 54 | `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` (1 members) | D | DD | DD | yes | 76 classes | 5.8e-03 (20, 8.1e-05) | 0.0138 |
| K b = 4 | `and(BOX(THEM(ME)),BOXD(THEM(ME)))` (66 members) | D | DD | DD | yes | 25 classes | 6.2e-03 (6, 6.2e-03) | 0.0273 |

**b = 4 supplement** (A is split there): rivals of each member alone.

| arm | reference | rivals | rival μ | direct-bridge-less share | hard share |
|---|---|---|---|---|---|
| free | `BOX(THEM(ME))` | 10 | 1.6e-05 | 0.259 | 0.259 |
| free | `BOX1(THEM(ME))` | 8 | 1.6e-05 | 0.259 | 0.259 |
| K b = 16 | `BOX(THEM(ME))` | 0 | 0 | 0.000 | 0.000 |
| K b = 16 | `BOX1(THEM(ME))` | 2 | 2.7e-06 | 0.000 | 0.000 |
| K b = 4 | `BOX(THEM(ME))` | 7 | 5.1e-03 | 0.997 | 0.997 |
| K b = 4 | `BOX1(THEM(ME))` | 16 | 0.0117 | 1.000 | 1.000 |
| K b = 54 | `BOX(THEM(ME))` | 0 | 0 | 0.000 | 0.000 |
| K b = 54 | `BOX1(THEM(ME))` | 2 | 2.7e-06 | 0.000 | 0.000 |

**Budget profile** (exploratory static, computed after the predictions and the runs, no prediction attached; the K tables at b = 3–54 from `src/k_at_n8.py`): rivals of A under K by budget.

| b | classes | establishers (μ) | FairBot, `BOX1(THEM(ME))` self-cooperate / mutually cooperate | rivals | rival μ | direct-bridge-less μ (share) | hard share | establisher-graph components | new rivals by source: n, μ (bridge-less μ) | heaviest rivals |
|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 22 | 7 (0.0133) | yes/no / **no** | 5 | 0.0102 | 0.0102 (1.000) | 1.000 | 4 | 6, 0.0102 (0.0102) | `BOX(THEM(ME))`, `BOX(THEM(THEM))`, `BOX(THEM(^BOX(THEM(ME))))` |
| 4 | 83 | 25 (0.0281) | yes/yes / **no** | 18 | 0.0168 | 0.0168 (1.000) | 0.906 | 4 | 25, 0.0168 (0.0168) | `BOX(THEM(ME))`, `BOX(THEM(THEM))`, `BOX1(THEM(ME))` |
| 6 | 248 | 59 (0.0244) | yes/yes / yes | 13 | 2.9e-04 | 2.9e-04 (1.000) | 0.221 | 4 | 13, 2.9e-04 (2.9e-04) | `not(BOXD1(THEM(^D)))`, `BOX(THEM(^BOX(THEM(THEM))))`, `and(BOX(THEM(ME)),BOX(THEM(THEM)))` |
| 8 | 371 | 76 (0.0244) | yes/yes / yes | 8 | 3.7e-04 | 7.6e-06 (0.020) | 0.020 | 2 | 8, 3.7e-04 (7.6e-06) | `not(BOXD1(THEM(^D)))`, `BOX(THEM(^BOX(THEM(THEM))))`, `BOX(THEM(^BOX1(THEM(THEM))))` |
| 12 | 491 | 104 (0.0242) | yes/yes / yes | 4 | 1.8e-05 | 0 (0.000) | 0.000 | 1 | 2, 1.5e-05 (0) | `and(BOX(THEM(ME)),BOX(THEM(THEM)))`, `and(BOX(THEM(THEM)),BOX1(THEM(ME)))`, `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` |
| 16 | 476 | 93 (0.0242) | yes/yes / yes | 2 | 2.7e-06 | 0 (0.000) | 0.000 | 1 | 0, 0 (0) | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))`, `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` |
| 24 | 321 | 69 (0.0242) | yes/yes / yes | 2 | 2.7e-06 | 0 (0.000) | 0.000 | 1 | 0, 0 (0) | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))`, `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` |
| 32 | 284 | 64 (0.0242) | yes/yes / yes | 2 | 2.7e-06 | 0 (0.000) | 0.000 | 1 | 0, 0 (0) | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))`, `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` |
| 54 | 255 | 52 (0.0242) | yes/yes / yes | 2 | 2.7e-06 | 0 (0.000) | 0.000 | 1 | 0, 0 (0) | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))`, `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` |

The direct-bridge-less mass under K is 0.010 / 0.017 / 2.9·10⁻⁴ / 7.6·10⁻⁶ / 0 at b = 3 / 4 / 6 / 8 / ≥ 12, against 4.1·10⁻⁶ under the free box. Below b = 7 (`BOX1(THEM(ME))`'s distinct-budget threshold) A itself is split or its readers cannot certify each other's neighbours; at b = 8 the one bridge-less rival is `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))` (a full rival in its own component: a soft clique whose two-box proof does not fit the budget against non-copies). Every bridge-less rival under K at any budget is new by source identity; none is P\*-family.

## 2. Calibration (m = 0, N = 200, I = 16, 120 runs per table)

| table | T_nuc (median, 95% bootstrap) | per-island nucleation p | boundary mN = 0.3·N/T_nuc | quartiles |
|---|---|---|---|---|
| free | 55 [55, 60] | 0.128 (245 / 1920) | 1.091 | 45 / 55 / 70 |
| K b = 16 | 50 [50, 55] | 0.131 (252 / 1920) | 1.200 | 45 / 50 / 70 |
| K b = 4 | 55 [50, 55] | 0.147 (282 / 1920) | 1.091 | 45 / 55 / 70 |

Checks are every 5 generations, so T_nuc is resolved to 5. The dimensionless coordinate x = mN·T_nuc/N for each natural cell is in the next table.

## 3. (a) Natural runs, matched (N = 200, I = 64, horizon 10⁵)

| table | mN | x = mN·T_nuc/N | runs | ever separated [95%] | **separated at the horizon** [95%] (one-sided 95% upper) | A-rival / non-A at the horizon | direct-bridge-less among horizon separations | island P(C,C) mean (min) | run-level efficient [95%] | cf cross P(C,C), separated runs | worker-hours |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K b = 16 | 1.091 | 0.273 | 3000 | 5/3000 = 0.0017 [0.0007, 0.0039] | **0/3000 = 0.0000 [0.0000, 0.0013]** (1.0e-03) | 0 / 0 | 0 | 1.0000 (1.000) | 1.00 [1.00, 1.00] | – | 0.26 |
| K b = 16 | 1.200 | 0.300 | 3000 | 13/3000 = 0.0043 [0.0025, 0.0074] | **0/3000 = 0.0000 [0.0000, 0.0013]** (1.0e-03) | 0 / 0 | 0 | 1.0000 (1.000) | 1.00 [1.00, 1.00] | – | 0.25 |
| K b = 4 | 1.091 | 0.300 | 50 | 40/50 = 0.8000 [0.6696, 0.8876] | **40/50 = 0.8000 [0.6696, 0.8876]** (0.887) | 6 / 34 | 6 | 0.9890 (0.977) | 1.00 [0.93, 1.00] | 0.664 | 0.75 |
| free | 1.091 | 0.300 | 3000 | 20/3000 = 0.0067 [0.0043, 0.0103] | **8/3000 = 0.0027 [0.0014, 0.0053]** (4.8e-03) | 8 / 0 | 7 | 1.0000 (0.977) | 1.00 [1.00, 1.00] | 0.648 | 0.38 |

**Paired at the common mN** (same source-level seeds in both tables): horizon separation K only 0, free only 8, both 0; ever separated K only 4, free only 19, both 1; run-level efficient K only 0, free only 0 (of 3000 paired runs).

Separations by rival (first separation of each ever-separated run; at the horizon):

| table | mN | ever: kinds | ever: A-rivals | horizon: A-rivals | bridge fate (first separation) | resolved / censored | KM P(still separated) at 10² / 10³ / 10⁴ / 10⁵ after first separation | median time to resolution | episodes |
|---|---|---|---|---|---|---|---|---|---|
| K b = 16 | 1.091 | {'A-rival': 4, 'non-A': 1} | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` 2, `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` 2 | – | {'bridged, bridge alive, resolved': 4, 'bridged, bridge dead, resolved': 1} | 5 / 0 | 0.80 / 0.60 / 0.00 / 0.00 | 1.01e+03 | {23: 1, 2: 1, 35: 1, 37: 1, 22: 1} |
| K b = 16 | 1.2 | {'non-A': 4, 'A-rival': 9} | `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` 6, `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` 3 | – | {'bridged, bridge alive, resolved': 11, 'bridged, bridge dead, resolved': 2} | 13 / 0 | 0.85 / 0.31 / 0.00 / 0.00 | 780 | {7: 2, 5: 2, 44: 1, 22: 1, 28: 1, 1: 1, 32: 1, 24: 1, 6: 1, 41: 1, 12: 1} |
| K b = 4 | 1.091 | {'rival-vs-nonA': 34, 'A-rival': 6} | `BOX(THEM(THEM))` 6 | `BOX(THEM(THEM))` 6 | {'no bridge in support, separated at end': 34, 'no bridge in support, resolved': 6} | 6 / 34 | 1.00 / 1.00 / 1.00 / 0.81 | 1.0e+05 | {377: 1, 216: 1, 11: 2, 305: 1, 1: 1, 41: 1, 385: 1, 2: 1, 6: 2, 9: 2, 5: 4, 293: 2, 3: 1, 163: 1, 376: 1, 309: 1, 45: 1, 69: 1, 296: 1, 121: 1, 104: 2, 4: 1, 99: 1, 15: 1, 310: 1, 254: 1, 13: 1, 33: 1, 19: 1, 247: 1, 327: 1, 299: 1} |
| free | 1.091 | {'A-rival': 20} | `BOX1(THEM(^not(BOX(THEM(ME)))))` 4, `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` 4, `BOX1(THEM(^not(BOX(THEM(^C)))))` 1, `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` 3, `BOX1(THEM(^not(BOX(THEM(THEM)))))` 2, `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` 3, `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` 2, `BOX1(THEM(^not(BOX(THEM(^D)))))` 1 | `BOX1(THEM(^not(BOX(THEM(ME)))))` 1, `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` 4, `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` 3 | {'bridged, bridge dead, separated at end': 4, 'no bridge in support, separated at end': 4, 'bridged, bridge alive, resolved': 11, 'bridged, bridge dead, resolved': 1} | 12 / 8 | 1.00 / 0.80 / 0.40 / 0.40 | 1.15e+03 | {383: 1, 6: 2, 25: 2, 24: 1, 54: 1, 133: 1, 5: 2, 10: 1, 15: 1, 8: 1, 381: 1, 45: 1, 13: 1, 11: 1, 18: 1, 28: 1, 26: 1} |

"Separated at the horizon" is read from the final state (certified-cooperative holders, island P(C,C) ≥ 0.95, mutually defecting); the KM, resolution and episode columns use the kernel's per-check flag (two locally frozen, all-cooperative islands with mutually-defecting holders), which flickers under migrant load in the K b = 4 runs. In K b = 4 FairBot and `BOX1(THEM(ME))` mutually defect, so neither is "in A's network" and their separations are classed rival-vs-nonA (§7).

Per-separation tracking (every run ever separated; "first" = first separation, "end" = at the horizon; bridges = cooperative classes in the support mutually cooperating with both holders; A-bridges = the spec's pairwise bridges of (A, R)):

| table | mN | rep | first sep gen | resolved at (−1: separated at the horizon) | when | pair | kind | rival bridge-less | bridge classes | bridge copies / islands at seeding | A-bridge copies at seeding | bridge alive at end | mediations (first gen) | islands held a / b |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K b = 16 | 1.091 | 49 | 55 | 810 | first | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` / `BOX1(THEM(ME))` | A-rival | False | 2 | 146 / 59 | 77 | True | 25 (225) | 8 / 0 |
| K b = 16 | 1.091 | 289 | 125 | 195 | first | `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` / `BOX(THEM(ME))` | A-rival | False | 1 | 87 / 48 | 87 | False | 0 (-1) | 0 / 64 |
| K b = 16 | 1.091 | 515 | 125 | 1135 | first | `BOX1(THEM(ME))` / `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | A-rival | False | 3 | 124 / 53 | 60 | True | 55 (340) | 34 / 0 |
| K b = 16 | 1.091 | 1833 | 60 | 1205 | first | `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` / `BOX1(THEM(^C))` | A-rival | False | 2 | 165 / 60 | 78 | True | 52 (440) | 35 / 0 |
| K b = 16 | 1.091 | 2214 | 65 | 1965 | first | `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))` / `and(BOX(THEM(ME)),BOX(THEM(THEM)))` | non-A | – | 10 | 295 / 64 | – | True | 17 (185) | 0 / 0 |
| K b = 16 | 1.2 | 67 | 125 | 390 | first | `BOX(THEM(THEM))` / `and(BOX1(THEM(ME)),BOX(THEM(^C)))` | non-A | – | 7 | 233 / 64 | – | True | 9 (205) | 9 / 0 |
| K b = 16 | 1.2 | 142 | 150 | 440 | first | `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` / `BOX1(THEM(ME))` | A-rival | False | 2 | 149 / 58 | 75 | True | 10 (265) | 10 / 0 |
| K b = 16 | 1.2 | 530 | 80 | 1015 | first | `BOX1(THEM(ME))` / `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | A-rival | False | 2 | 121 / 55 | 59 | True | 52 (230) | 28 / 0 |
| K b = 16 | 1.2 | 627 | 120 | 1305 | first | `BOX1(THEM(ME))` / `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` | A-rival | False | 3 | 127 / 58 | 71 | True | 33 (200) | 5 / 0 |
| K b = 16 | 1.2 | 756 | 115 | 820 | first | `BOX1(THEM(ME))` / `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | A-rival | False | 2 | 126 / 58 | 59 | True | 45 (290) | 17 / 0 |
| K b = 16 | 1.2 | 1022 | 115 | 120 | first | `BOX1(THEM(ME))` / `BOX(THEM(ME))` | non-A | – | 11 | 181 / 60 | – | False | 0 (-1) | 0 / 64 |
| K b = 16 | 1.2 | 1541 | 125 | 210 | first | `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` / `BOX1(THEM(ME))` | A-rival | False | 5 | 144 / 60 | 67 | False | 1 (210) | 0 / 64 |
| K b = 16 | 1.2 | 1653 | 65 | 1670 | first | `BOX(THEM(THEM))` / `and(BOX1(THEM(ME)),BOX(THEM(^C)))` | non-A | – | 10 | 251 / 62 | – | True | 47 (255) | 7 / 0 |
| K b = 16 | 1.2 | 1976 | 170 | 405 | first | `and(BOX(THEM(ME)),BOX1(THEM(THEM)))` / `BOX(THEM(^BOX(THEM(THEM))))` | non-A | – | 8 | 289 / 63 | – | True | 3 (265) | 3 / 0 |
| K b = 16 | 1.2 | 2517 | 150 | 1365 | first | `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` / `BOX1(THEM(ME))` | A-rival | False | 3 | 142 / 55 | 70 | True | 39 (180) | 5 / 0 |
| K b = 16 | 1.2 | 2662 | 110 | 955 | first | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` / `BOX1(THEM(ME))` | A-rival | False | 2 | 138 / 57 | 66 | True | 43 (250) | 13 / 0 |
| K b = 16 | 1.2 | 2750 | 70 | 1730 | first | `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` / `BOX1(THEM(ME))` | A-rival | False | 2 | 130 / 54 | 56 | True | 65 (215) | 0 / 14 |
| K b = 16 | 1.2 | 2878 | 55 | 835 | first | `BOX1(THEM(^C))` / `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` | A-rival | False | 3 | 124 / 57 | 60 | True | 52 (230) | 0 / 14 |
| free | 1.091 | 182 | 110 | -1 | first | `BOX1(THEM(ME))` / `BOX1(THEM(^not(BOX(THEM(ME)))))` | A-rival | False | 1 | 65 / 41 | 65 | False | 0 (-1) | 4 / 60 |
| free | 1.091 | 182 | 110 | -1 | end | `BOX1(THEM(ME))` / `BOX1(THEM(^not(BOX(THEM(ME)))))` | A-rival | False | 1 | 65 / 41 | 65 | False | 0 (-1) | 4 / 60 |
| free | 1.091 | 145 | 100 | -1 | first | `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` / `BOX(THEM(ME))` | A-rival | True | 0 | 0 / 0 | 0 | False | 0 (-1) | 24 / 40 |
| free | 1.091 | 145 | 100 | -1 | end | `BOX(THEM(ME))` / `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | A-rival | True | 0 | 0 / 0 | 0 | False | 0 (-1) | 40 / 24 |
| free | 1.091 | 296 | 85 | 1090 | first | `BOX1(THEM(^not(BOX(THEM(^C)))))` / `BOX1(THEM(ME))` | A-rival | False | 5 | 69 / 45 | 69 | True | 49 (205) | 17 / 0 |
| free | 1.091 | 515 | 65 | 2175 | first | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` / `BOX1(THEM(ME))` | A-rival | False | 3 | 125 / 53 | 60 | True | 71 (275) | 5 / 0 |
| free | 1.091 | 514 | 95 | 2100 | first | `BOX1(THEM(^not(BOX(THEM(THEM)))))` / `BOX1(THEM(ME))` | A-rival | False | 1 | 58 / 38 | 58 | True | 79 (285) | 34 / 0 |
| free | 1.091 | 527 | 130 | -1 | first | `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` / `BOX1(THEM(ME))` | A-rival | True | 1 | 1 / 1 | 0 | False | 0 (-1) | 12 / 52 |
| free | 1.091 | 527 | 130 | -1 | end | `BOX1(THEM(ME))` / `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | A-rival | True | 1 | 1 / 1 | 0 | False | 0 (-1) | 52 / 12 |
| free | 1.091 | 795 | 100 | 1195 | first | `BOX1(THEM(^not(BOX(THEM(ME)))))` / `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))` | A-rival | False | 1 | 69 / 42 | 69 | True | 26 (345) | 0 / 2 |
| free | 1.091 | 1042 | 95 | 1485 | first | `BOX1(THEM(^not(BOX(THEM(ME)))))` / `BOX1(THEM(ME))` | A-rival | False | 3 | 69 / 46 | 69 | True | 55 (345) | 0 / 2 |
| free | 1.091 | 1275 | 100 | -1 | first | `BOX(THEM(ME))` / `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | A-rival | True | 0 | 0 / 0 | 0 | False | 0 (-1) | 42 / 22 |
| free | 1.091 | 1275 | 100 | -1 | end | `BOX(THEM(ME))` / `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | A-rival | True | 0 | 0 / 0 | 0 | False | 0 (-1) | 42 / 22 |
| free | 1.091 | 1666 | 105 | -1 | first | `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` / `BOX1(THEM(ME))` | A-rival | True | 1 | 1 / 1 | 0 | False | 0 (-1) | 38 / 26 |
| free | 1.091 | 1666 | 105 | -1 | end | `BOX1(THEM(ME))` / `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | A-rival | True | 1 | 1 / 1 | 0 | False | 0 (-1) | 26 / 38 |
| free | 1.091 | 2204 | 75 | 205 | first | `BOX1(THEM(ME))` / `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` | A-rival | False | 2 | 114 / 50 | 67 | False | 0 (-1) | 64 / 0 |
| free | 1.091 | 2296 | 50 | -1 | first | `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` / `BOX1(THEM(ME))` | A-rival | True | 0 | 0 / 0 | 0 | False | 0 (-1) | 5 / 59 |
| free | 1.091 | 2296 | 50 | -1 | end | `BOX1(THEM(ME))` / `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | A-rival | True | 0 | 0 / 0 | 0 | False | 0 (-1) | 59 / 5 |
| free | 1.091 | 2339 | 105 | -1 | first | `BOX1(THEM(ME))` / `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | A-rival | True | 0 | 0 / 0 | 0 | False | 0 (-1) | 48 / 16 |
| free | 1.091 | 2339 | 105 | -1 | end | `BOX1(THEM(ME))` / `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | A-rival | True | 0 | 0 / 0 | 0 | False | 0 (-1) | 48 / 16 |
| free | 1.091 | 2454 | 105 | 385 | first | `BOX1(THEM(^not(BOX(THEM(THEM)))))` / `BOX1(THEM(ME))` | A-rival | False | 7 | 85 / 47 | 85 | True | 5 (275) | 0 / 26 |
| free | 1.091 | 2462 | 130 | 1905 | first | `BOX1(THEM(ME))` / `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | A-rival | False | 2 | 119 / 59 | 61 | True | 63 (230) | 6 / 0 |
| free | 1.091 | 2586 | 105 | 810 | first | `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` / `BOX1(THEM(ME))` | A-rival | False | 3 | 135 / 53 | 64 | True | 34 (335) | 17 / 0 |
| free | 1.091 | 2777 | 95 | 995 | first | `BOX1(THEM(ME))` / `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | A-rival | False | 2 | 128 / 59 | 58 | True | 54 (295) | 0 / 22 |
| free | 1.091 | 2888 | 80 | 1505 | first | `BOX1(THEM(^not(BOX(THEM(ME)))))` / `BOX1(THEM(ME))` | A-rival | False | 5 | 76 / 45 | 75 | True | 76 (385) | 28 / 0 |
| free | 1.091 | 2960 | 140 | 1350 | first | `BOX1(THEM(^not(BOX(THEM(^D)))))` / `BOX1(THEM(ME))` | A-rival | False | 3 | 69 / 43 | 69 | True | 70 (225) | 27 / 0 |
| free | 1.091 | 2970 | 120 | -1 | first | `BOX1(THEM(ME))` / `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | A-rival | True | 1 | 1 / 1 | 0 | False | 0 (-1) | 39 / 25 |
| free | 1.091 | 2970 | 120 | -1 | end | `BOX1(THEM(ME))` / `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | A-rival | True | 1 | 1 / 1 | 0 | False | 0 (-1) | 39 / 25 |

## 4. (b) Positive control: the heaviest bridged rival of A under K b = 16, forced densely

Rival `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` (a half-rival: mutual defection with `BOX1(THEM(ME))`, mutual cooperation with FairBot), one copy per island replacing a uniformly chosen seed; kernel tags for (`BOX1(THEM(ME))`, R): 1 = A's network, 2 = R's, 3 = bridge. mN = 1.200.

| runs | rival established | ever separated | **horizon separated** [95%] | separated with bridge dead / alive | losses (A / R) / exposure, hazard [95%] | R-island losses 2>1 / 2>3 / 2>0 | **mediation-before-loss** [95%] | bridge alive at end | island P(C,C) (min) | KM after separation at 10³ / 10⁴ / 10⁵ |
|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.98 [0.93, 0.99] | 0.97 [0.92, 0.99] | **0.02 [0.01, 0.07]** | 2 / 0 | 95 (72 / 23) / 1.8e+06, 5.2e-05 [4.2e-05, 6.4e-05] | 14 / 2793 / 0 | **0.91 [0.83, 0.95]** | 97 | 0.9998 (0.985) | 0.34 / 0.02 / 0.02 |

## 5. (c) Forced P\* with the inert-defector control (one founder per island, replacing a uniformly chosen seed)

The forced founders are followed as a lineage (a duplicate column of their class, tagged; tags have no dynamic effect). **Cooperative establishment** = an island certified cooperative whose holder is the lineage; **lineage survival** = the lineage present at the horizon in any state. q_est = local establishments / the paired m = 0 reference (same initial states).

| cell | table | mN | runs | cooperative establishment: runs (islands) | holder at the end, certified: runs | **lineage alive at the horizon** [95%] | lineage extinction gen quartiles 25/50/75/90 | max copies (mean) | max islands held (mean) | q_est [95%] | Δq_est vs iid [95%] | Δq_est vs D control | horizon separated | island P(C,C) (min) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| forced D (inert control) | K b = 16 | 1.200 | 100 | 0 (0) | 0 | **0.00 [0.00, 0.04]** | 74.3 / 128 / 190 / 225 | 204.9 | 0.7 | 0.91 [0.83, 0.99] | +0.040 [-0.069, +0.148] | – | 0.00 [0.00, 0.04] | 1.0000 (1.000) |
| iid control | K b = 16 | 1.200 | 100 | – | – | – | – | – | – | 0.86 [0.80, 0.94] | – | – | 0.00 [0.00, 0.04] | 1.0000 (1.000) |
| iid control | free | 1.091 | 100 | – | – | – | – | – | – | 0.91 [0.82, 1.01] | – | – | 0.00 [0.00, 0.04] | 1.0000 (1.000) |
| forced P\* | K b = 16 | 1.200 | 100 | 0 (0) | 0 | **0.00 [0.00, 0.04]** | 86.2 / 144 / 195 / 254 | 202.8 | 0.7 | 0.88 [0.80, 0.96] | +0.013 [-0.100, +0.129] | -0.027 [-0.140, +0.089] | 0.00 [0.00, 0.04] | 1.0000 (1.000) |
| forced P\* | free | 1.091 | 100 | 96 (2597) | 96 | **0.96 [0.90, 0.98]** | alive / alive / alive / alive | 5569.9 | 27.5 | 0.82 [0.77, 0.88] | -0.090 [-0.198, +0.010] | – | 0.96 [0.90, 0.98] | 0.9833 (0.971) |

Paired (same seeds and founder islands): P\* alive and D dead 0, D alive and P\* dead 0, both alive 0, of 100.

## 6. (e) Continuation of every separated, unresolved natural run to 3·10⁵ generations

Same initial state and kernel stream with a longer check schedule (identical up to 10⁵); "matches" = the 10⁵ check row equals the original run's final row.

8 of 8 still separated at 3·10⁵; 0 resolutions in 2.4e+06 separated-run-generations (from first separation; one-sided 95% hazard bound 1.3e-06 per separated run-generation).

| table | mN | rep | matches | status at 3·10⁵ | separated at 3·10⁵ | pairs | worker-hours |
|---|---|---|---|---|---|---|---|
| free | 1.091 | 182 | True | unresolved | 1 | `BOX1(THEM(ME))` / `BOX1(THEM(^not(BOX(THEM(ME)))))` | 0.01 |
| free | 1.091 | 527 | True | unresolved | 1 | `BOX1(THEM(ME))` / `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 0.04 |
| free | 1.091 | 145 | True | unresolved | 1 | `BOX(THEM(ME))` / `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 0.06 |
| free | 1.091 | 1275 | True | unresolved | 1 | `BOX(THEM(ME))` / `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 0.06 |
| free | 1.091 | 2296 | True | unresolved | 1 | `BOX1(THEM(ME))` / `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` | 0.02 |
| free | 1.091 | 1666 | True | unresolved | 1 | `BOX1(THEM(ME))` / `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 0.06 |
| free | 1.091 | 2339 | True | unresolved | 1 | `BOX1(THEM(ME))` / `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 0.05 |
| free | 1.091 | 2970 | True | unresolved | 1 | `BOX1(THEM(ME))` / `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 0.06 |

## 7. Beyond the spec: K at b = 4, natural runs (budget soft cliques)

50 runs at mN = 1.091 (reps 0–49, a complete prefix; declared 1,000): separated at the horizon 0.80 [0.67, 0.89], ever 0.80 [0.67, 0.89]; island P(C,C) 0.9890 (min 0.977); run-level efficient 1.00 [0.93, 1.00]; cf cross-island P(C,C) in separated runs 0.66; 6 of 40 ever-separated runs resolved. Separated holder pairs at the horizon (first listed pair per run):

| pair | runs |
|---|---|
| `BOX(THEM(ME))` / `BOX1(THEM(ME))` | 34 |
| `BOX(THEM(THEM))` / `BOX1(THEM(ME))` | 6 |

## Verdicts

| # | prediction | outcome |
|---|---|---|
| RE 1 | K b = 16 direct-bridge-less hard share < 0.02; no new rival ≥ 10⁻⁶ by source | **held** (share 0.000: the only rivals of A are the bridged PrudentBot pair; 0 new rivals by source identity, 11 free-arm rival sources lost) |
| RE 2 | K natural horizon separation below free at the same mN, none with a direct-bridge-less rival (0–2 vs 4–20) | **held** (common mN 1.091: K 0/3,000 vs free 8/3,000, one-sided 95% upper rate for K 1.0e-03; paired: free-only 8, K-only 0; K at its calibrated mN 1.200: 0; free's 8: 7 P\*-family, 1 B₁ with a dead bridge) |
| RE 3 | forced P\* under K: 0 cooperative establishments; lineage survival ≤ 0.1 and ≤ D control; |Δq_est| ≤ 0.1 vs iid, ≤ 0.05 vs D | **held** (0 cooperative establishments in 100 runs; lineage alive at the horizon 0/100 vs D control 0/100; median extinction generation 144 vs 128; Δq_est vs iid +0.013 [-0.100, +0.129], vs D -0.027 [-0.140, +0.089]; the vs-D clause holds on the point estimate, its interval is ±0.11) |
| RE 4 | direct-bridge-less share under K < 0.05 at b = 4, 16, 54 | **failed, falsifier fired** at b = 4 (share 1.000: FairBot and `BOX1(THEM(ME))` mutually defect at b = 4, so A is not a network and every rival is literally bridge-less; budget soft-clique rivals, μ 0.017, not the P\* family); held at b = 16 (0.000) and 54 (0.000) |
| RE 5 | positive control mediation-before-loss ≥ 0.7; island P(C,C) ≥ 0.97 in every K cell; K run-level efficiency not below free by ≥ 0.05 | **held** (mediation-before-loss 89/98 = 0.91; horizon separation 2/100, both with the bridge dead; island P(C,C) per K cell (mean over runs) ≥ 0.9998, the lowest single run 0.985; run-level efficient fraction 1.000 in K and free) |
| S1 | free natural horizon separations 3–15, ≥ 0.6 P\*-family | **held** (8; 7 of 8 P\*-family = 0.88) |
| S2 | K ≤ 1 horizon separation per cell; every K A-separation with the PrudentBot pair | **held** (0 and 0; ever separated 5 and 13, all resolved; A-rivals among them only the PrudentBot pair; 1 and 4 separations between non-A establishers, all resolved) |
| S3 | T_nuc(K16) within ±20% of free | **held** (50 vs 55 generations, -9%; mN 1.200 vs 1.091) |
| S4 | K b = 4 natural: horizon separation ≥ 0.5, island P(C,C) ≥ 0.97 | **held** (0.80 [0.67, 0.89], 50 runs of the declared 1,000; island P(C,C) 0.9890, min 0.977) |
| S5 | PrudentBot positive control: established ≥ 0.8, separated ≤ 0.05, mediation-before-loss ≥ 0.85 | **held** (98/100, 2/100, 0.91) |
| S6 | P\* lineage under K alive ≤ 0.05, within 0.05 of D; median extinction within ×2 | **held** (0/100 and 0/100; 144 vs 128 generations) |
| S7 | forced P\* under free n = 8: cooperative establishment ≥ 0.9, horizon separated ≥ 0.8 | **held** (96/100 runs with a cooperative P\* establishment, 2597 islands in all; separated 96/100; island P(C,C) 0.983; cf cross P(C,C) 0.59) |
| S8 | natural island P(C,C) ≥ 0.99, run-level efficient ≥ 0.98, |K − free| ≤ 0.01 | **held** (island P(C,C) per cell ≥ 1.0000, the lowest single run 0.977; efficient 3,000/3,000 in all three cells) |
| S9 | ≥ 0.9 of free's separated P\*-family runs still separated at 3·10⁵ | **held** (8 of 8 continued runs separated at 3·10⁵, every trajectory matching its 10⁵ state) |

**Reading.**
- **At b ≥ 12 K removes the bridge-less obstruction at n = 8, and the dynamics follow the statics.** Under the free box 0.221
  of rival mass is direct-bridge-less (P\*, P\*′); under K at b = 16 and 54 the only rivals of FairBot's pair are the
  PrudentBot pair, half-rivals bridged by `BOX(THEM(THEM))` (μ 5·10⁻³), and no source becomes a new rival. Natural horizon
  separation is 8/3,000 under the free box (7 P\*-family, 1 B₁ whose bridge died; all 8 still separated at 3·10⁵) and
  0/3,000 under K at both the common and the calibrated mN (paired: free-only 8, K-only 0; one-sided 95% bound 0.001 per
  run). K's 18 ever-separations all resolved (median ≈ 10³ generations, all within 10⁴), 15 of them with the bridge alive.
- **P\* under K is a defector, not a rival:** forced at one copy per island it never establishes cooperatively, dies as fast
  as an inert D (median 144 vs 128 generations; 0/100 alive in both), and leaves nucleation unchanged (Δq_est +0.01 vs iid,
  −0.03 vs D). The same forcing under the free box gives a permanent cooperative patchwork in 96/100 runs. P\*'s column
  differs from D's (it has prey D lacks, μ 0.006), but this does not show demographically.
- **The bridge machinery works under K:** forced PrudentBot establishes in 98/100 runs, a bridge mediates before loss in
  0.91, and the 2 horizon separations both have a dead bridge, the free arm's pattern.
- **The budget is not innocent.** Below `BOX1(THEM(ME))`'s distinct-budget threshold K creates bridge-less rivals of its
  own, budget soft cliques rather than Gödelian programs: at b = 4 FairBot and `BOX1(THEM(ME))` mutually defect, rival mass
  is 0.017 (900× the free arm's), every rival is bridge-less, and natural runs end separated in 0.80 [0.67, 0.89] at
  (200, 64), every island efficient (island P(C,C) 0.989, cross-island 0.66). Bridge-less mass is 0.017 / 2.9·10⁻⁴ /
  7.6·10⁻⁶ / 0 at b = 4 / 6 / 8 / ≥ 12. So b = 4, the best K budget in the well-mixed chain at N = 10⁴, is the worst arm
  across islands; the obstruction moves from Gödel sentences to budget thresholds and vanishes once the budget clears every
  establisher pair's distinct-budget threshold.
- **Island-level efficiency is untouched everywhere** (run-level efficient fraction 1.00 in every natural cell). *Scope:*
  n = 8, N = 200, I = 64, horizons 10⁵–3·10⁵; K is a sound bounded calculus for the modal fragment with a GL-decidability
  prune; K tables at n ≥ 9 do not exist; longer bridge paths and non-A networks are covered only by the static graph (one
  component at b ≥ 12).

