# Proof length: GLS+Def on the free arm, and the bounded calculus K

Spec `specs/2026-10-05-proof-length.md`; predictions `predictions/2026-10-05-proof-length.md`; calculi, soundness and hand-checked derivations in `notes/proof-length.md`. Raw rows: `runs/proof-length-partA.json`, `runs/proof-length-grid.json`, `runs/proof-length-karm-*.json`, `runs/proof-length-priced.json`.

## Part A: GLS+Def on the free arm

### Audit and certification

| set | pairs | disagreements | provable roots | certified | neither at level 0 | neither at level 1 | search time per pair (mean / max s) |
|---|---|---|---|---|---|---|---|
| n6 | 4356 | 0 | 3308 | 3308 (1.000) | 3230 | 2174 | 0.0005 / 0.05 |
| n8_family | 289 | 0 | 348 | 348 (1.000) | 143 | 87 | 0.0008 / 0.03 |
| n8_sample | 5000 | 0 | 9732 | 9732 (1.000) | 175 | 93 | 0.0000 / 0.04 |
| n8_uniform | 5000 | 0 | 4224 | 4224 (1.000) | 3432 | 2344 | 0.0041 / 0.70 |
| n8_mce | 8256 | 0 | 12093 | 12093 (1.000) | 2585 | 1834 | 0.0084 / 8.36 |
| ladder | 784 | 0 | 1040 | 1040 (1.000) | 321 | 207 | 0.1639 / 15.32 |

Audit: hc[0] ⇔ ⊢ P, hd[0] ⇔ P ⊢, hc[1] ⇔ ⊢ ¬□⊥ → P, hd[1] ⇔ ⊢ ¬□⊥ → ¬P against the evaluator's tables (n = 6, 8) or `src/conj4.py`'s trace (ladder, siblings and fakers, levels ≤ 2). Certified = minimal size certified by iterative deepening.

### Distributions of minimal sizes and Löb counts

| set | root | n provable | size: min / median / mean / max | Λ: min / median / max | DAG/tree (mean) | height (mean) |
|---|---|---|---|---|---|---|
| n6 | C0 | 779 | 2 / 10 / 9.3 / 17 | 0 / 3 / 5 | 1.000 | 9.3 |
| n6 | D0 | 347 | 2 / 9 / 8.5 / 20 | 0 / 2 / 5 | 1.000 | 8.5 |
| n6 | C1 | 1043 | 3 / 9 / 9.9 / 18 | 0 / 2 / 5 | 1.000 | 9.9 |
| n6 | D1 | 1139 | 4 / 9 / 9.4 / 22 | 0 / 2 / 5 | 1.000 | 9.4 |
| n8_sample | C0 | 2482 | 2 / 2 / 2.2 / 11 | 0 / 0 / 3 | 1.000 | 2.2 |
| n8_sample | D0 | 2343 | 2 / 2 / 2.1 / 16 | 0 / 0 / 3 | 1.000 | 2.1 |
| n8_sample | C1 | 2498 | 3 / 3 / 3.2 / 12 | 0 / 0 / 3 | 1.000 | 3.2 |
| n8_sample | D1 | 2409 | 4 / 4 / 4.2 / 18 | 0 / 0 / 3 | 1.000 | 4.2 |
| n8_uniform | C0 | 982 | 2 / 12 / 13.1 / 68 | 0 / 2 / 17 | 0.999 | 11.6 |
| n8_uniform | D0 | 586 | 2 / 13 / 14.2 / 78 | 0 / 3 / 16 | 0.999 | 12.7 |
| n8_uniform | C1 | 1374 | 3 / 12 / 13.2 / 69 | 0 / 2 / 17 | 0.999 | 11.8 |
| n8_uniform | D1 | 1282 | 4 / 11 / 13.5 / 80 | 0 / 2 / 16 | 0.999 | 12.3 |
| n8_mce | C0 | 5671 | 4 / 11 / 13.6 / 70 | 1 / 3 / 20 | 0.994 | 10.7 |
| n8_mce | C1 | 6422 | 5 / 12 / 14.0 / 71 | 1 / 3 / 20 | 0.995 | 11.4 |

### Cost table: the prover family, the ladder, fakers

| program | |x| | depth | L_C (self) | Λ | L_C¹ (self) | Λ¹ | L_read(x→x) | vs D: L_D¹ | vs ALLC: L_out |
|---|---|---|---|---|---|---|---|---|---|
| `BOX(THEM(ME))` | 3 | 1 | 4 | 1 | 5 | 1 | 3 | 7 | 4 (lvl 0) |
| `BOX1(THEM(ME))` | 3 | 1 | 5 | 1 | 6 | 1 | 4 | ∞ | 5 (lvl 0) |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 8 | 1 | 24 | 5 | 25 | 5 | 22 | 8 | ∞ |
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 8 | 1 | ∞ | — | 22 | 3 | 12 | ∞ | 6 (lvl 0) |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^C))))` | 9 | 1 | ∞ | — | 24 | 5 | 13 | ∞ | 6 (lvl 0) |
| `and(and(BOX1(THEM(ME)),not(BOX(THEM(^C)))),BOXD2(THEM(^D)))` | 14 | 1 | ∞ | — | 54 | 9 | 41 | ∞ | 7 (lvl 0) |
| `and(and(BOX1(THEM(ME)),not(BOX(THEM(ME)))),BOXD2(THEM(^D)))` | 13 | 1 | ∞ | — | 52 | 7 | 40 | ∞ | 7 (lvl 0) |
| `and(BOX(THEM(ME)),BOXD2(THEM(^D)))` | 8 | 1 | 24 | 5 | 25 | 5 | 22 | 8 | ∞ |
| `BOX(THEM(THEM))` | 3 | 1 | 4 | 1 | 5 | 1 | 3 | 7 | 4 (lvl 0) |
| `BOX1(THEM(THEM))` | 3 | 1 | 5 | 1 | 6 | 1 | 4 | ∞ | 5 (lvl 0) |
| `BOX(THEM(^C))` | 4 | 1 | 6 | 2 | 7 | 2 | 5 | 7 | 4 (lvl 0) |
| `BOX1(THEM(^C))` | 4 | 1 | 8 | 2 | 9 | 2 | 7 | ∞ | 5 (lvl 0) |
| `BOX1(THEM(^D))` | 4 | 1 | ∞ | — | ∞ | — | 0 | ∞ | 5 (lvl 0) |
| `BOX2(THEM(^D))` | 4 | 1 | ∞ | — | ∞ | — | 0 | ∞ | 5 (lvl 0) |

### Siblings: L(x → sibling) / L(x → x)

y = or(x, ψ_K) (`src/conj4.py`). L_read sums the minimal sizes of x's true atoms against the opponent; L_out is the minimal size of x's actual outcome (level 0, else level 1).

| x | K | L_read(x→x) | L_read(x→y) | ratio | diff | L_out(x→x) | L_out(x→y) | ratio | y cooperates with x (L_out(y→x)) |
|---|---|---|---|---|---|---|---|---|---|
| `BOX(THEM(ME))` | 1 | 3 | 6 | 2.00 | 3 | 4 (lvl 0) | 7 (lvl 0) | 1.75 | 8 (lvl 0) |
| `BOX1(THEM(ME))` | 2 | 4 | 8 | 2.00 | 4 | 5 (lvl 0) | 9 (lvl 0) | 1.80 | 10 (lvl 0) |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 1 | 22 | 51 | 2.32 | 29 | 24 (lvl 0) | 53 (lvl 0) | 2.21 | 46 (lvl 0) |
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 2 | 12 | 31 | 2.58 | 19 | 22 (lvl 1) | 47 (lvl 1) | 2.14 | 43 (lvl 1) |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^C))))` | 2 | 13 | 31 | 2.38 | 18 | 24 (lvl 1) | 47 (lvl 1) | 1.96 | 43 (lvl 1) |
| `and(and(BOX1(THEM(ME)),not(BOX(THEM(^C)))),BOXD2(THEM(^D)))` | 2 | 41 | 90 | 2.20 | 49 | 54 (lvl 1) | 108 (lvl 1) | 2.00 | 96 (lvl 1) |
| `and(and(BOX1(THEM(ME)),not(BOX(THEM(ME)))),BOXD2(THEM(^D)))` | 2 | 40 | 90 | 2.25 | 50 | 52 (lvl 1) | 108 (lvl 1) | 2.08 | 96 (lvl 1) |
| `and(BOX(THEM(ME)),BOXD2(THEM(^D)))` | 1 | 22 | 51 | 2.32 | 29 | 24 (lvl 0) | 53 (lvl 0) | 2.21 | 46 (lvl 0) |
| `BOX(THEM(THEM))` | 1 | 3 | 4 | 1.33 | 1 | 4 (lvl 0) | 5 (lvl 0) | 1.25 | 5 (lvl 0) |
| `BOX1(THEM(THEM))` | 2 | 4 | 5 | 1.25 | 1 | 5 (lvl 0) | 6 (lvl 0) | 1.20 | 6 (lvl 0) |
| `BOX(THEM(^C))` | 1 | 5 | 6 | 1.20 | 1 | 6 (lvl 0) | 7 (lvl 0) | 1.17 | 7 (lvl 0) |
| `BOX1(THEM(^C))` | 2 | 7 | 8 | 1.14 | 1 | 8 (lvl 0) | 9 (lvl 0) | 1.12 | 9 (lvl 0) |

### Comparison with the stabilization proxy v(x, y) = k(y)·(1 + settle(y, x))

| n | pairs with v > 0 | Spearman(v, L_read) | Spearman(v, L_out) over finite (n) | Spearman(v, L_read) among pairs with true atoms |
|---|---|---|---|---|
| 6 | 4224 | -0.220 | 0.045 (2082) | 0.064 (930) |
| 8, mu-sample | 85 | -0.069 | -0.052 (78) | -0.567 (8) |
| 8, uniform sample | 4957 | -0.137 | 0.103 (2630) | -0.165 (1678) |
| 8, all sets (union) | 13359 | -0.342 | -0.072 (9137) | -0.185 (7300) |

Largest rank disagreements at n = 8 (pairs with v > 0 and at least one true atom):

| x | y | v | L_read | rank v | rank L |
|---|---|---|---|---|---|
| `and(BOX1(THEM(THEM)),not(BOX(THEM(ME))))` | `or(BOX1(THEM(ME)),not(BOXD(THEM(ME))))` | 10 | 5 | 1.00 | 0.05 |
| `and(BOX1(THEM(THEM)),not(BOX(THEM(ME))))` | `or(BOX1(THEM(ME)),not(BOXD1(THEM(ME))))` | 10 | 5 | 1.00 | 0.05 |
| `and(BOX(THEM(THEM)),BOXD1(THEM(THEM)))` | `or(BOX(THEM(ME)),not(BOX1(THEM(THEM))))` | 8 | 4 | 0.96 | 0.02 |
| `and(BOX(THEM(THEM)),BOX(THEM(^D)))` | `or(BOX(THEM(THEM)),BOX(THEM(^C)))` | 8 | 4 | 0.96 | 0.02 |
| `or(BOXD1(THEM(ME)),not(BOX(THEM(THEM))))` | `or(BOX(THEM(THEM)),BOXD1(THEM(THEM)))` | 8 | 4 | 0.96 | 0.02 |
| `and(BOX(THEM(THEM)),BOXD1(THEM(THEM)))` | `or(BOX(THEM(THEM)),BOX1(THEM(ME)))` | 8 | 4 | 0.96 | 0.02 |
| `or(BOX(THEM(ME)),BOX1(THEM(^D)))` | `or(BOX(THEM(ME)),BOX1(THEM(^D)))` | 8 | 4 | 0.96 | 0.02 |
| `or(BOX(THEM(THEM)),BOX1(THEM(^D)))` | `or(BOX(THEM(ME)),BOX(THEM(^D)))` | 8 | 4 | 0.96 | 0.02 |

### The cost of cooperation among mutually cooperating establisher pairs

**n8_mce** (6422 ordered pairs with a C proof; 0.12 need level 1):

- linear: L_C = 6.16 + 0.49·(|x|+|y|) (se 0.05), residual sd / mean = 0.58; Spearman(L_C, |x|+|y|) = 0.084, Spearman(L_C, depth) = 0.094
- quadratic term -0.175, 95% CI [-0.217, -0.133]; AIC linear 26086.1, quadratic 26021.2 (prefers quadratic)
- Λ > depth + 1 in 2411 pairs; Λ ≥ depth + 3 in 1478 pairs; max Λ − depth = 18; FairBot–FairBot (L, Λ) = (4, 1)
- DAG/tree size ratio of the minimal derivations: 0.995; mean residual by level: {0: 0.42625739967864457, 1: -3.2187825746702052}
- by nesting depth: d=1: n 3512, mean L 13.5, mean Λ 3.11, max Λ 17, d=2: n 2910, mean L 12.9, mean Λ 3.38, max Λ 20

**n6** (208 ordered pairs with a C proof; 0.03 need level 1):

- linear: L_C = 3.64 + 0.58·(|x|+|y|) (se 0.08), residual sd / mean = 0.23; Spearman(L_C, |x|+|y|) = 0.408, Spearman(L_C, depth) = 0.364
- quadratic term -0.037, 95% CI [-0.117, 0.043]; AIC linear 326.4, quadratic 327.5 (prefers linear)
- Λ > depth + 1 in 69 pairs; Λ ≥ depth + 3 in 12 pairs; max Λ − depth = 3; FairBot–FairBot (L, Λ) = (4, 1)
- DAG/tree size ratio of the minimal derivations: 1.000; mean residual by level: {0: 0.015312582740898317, 1: -0.5155236189436684}
- by nesting depth: d=1: n 40, mean L 7.5, mean Λ 2.12, max Λ 3, d=2: n 168, mean L 9.7, mean Λ 3.13, max Λ 5


## Part B: the bounded calculus K

### Run 1: budget grid, b ∈ {2..40}²

| pair | (C, D) cells | copy threshold (b_x = b_y) | distinct-budget rule | soundness violations / checked |
|---|---|---|---|---|
| `BOX(THEM(ME))` vs `BOX(THEM(ME))` | 0 | 3 | min(b_x, b_y) ≥ 4 | 0 / 8106 |
| `BOX1(THEM(ME))` vs `BOX1(THEM(ME))` | 0 | 4 | min(b_x, b_y) ≥ 7 | 0 / 9124 |
| `BOX(THEM(ME))` vs `BOX1(THEM(ME))` | 0 | — | b_x ≥ 6 and b_y ≥ 5 | 0 / 8820 |

Payoffs per cell follow from the play (PD: both C → 0 each, both D → −1 each); no cell is (C, D), so no budget is exploited.

### Run 2: the n = 6 arm, every class at a global budget b (ε → 0 chain, w = 0.3; ε = 0 lottery)

K soundness: 0 violations in 34679 checked K-derived formulas over b = 1..40. Plays differing from the free arm by b: 1: 994, 2: 978, 3: 934, 4: 872, 6: 630, 10: 356, 16: 304, 40: 304.

| arm | P(C,C) N = 10³ | 10⁴ | 3·10⁴ | π(all-D) at 3·10⁴ | top cooperative state (π) | its exit rate 10³ / 10⁴ / 3·10⁴ (strict share) | indeterminate | cut flow |
|---|---|---|---|---|---|---|---|---|
| free | 0.3453 | 0.5869 | 0.7068 | 0.293 | `BOX(THEM(THEM))` (0.233) | 4.9e-04 / 4.9e-05 / 1.6e-05 (0.00) | 0 | 7.7e-09 |
| K b=2 | 0.0001 | 0.0000 | 0.0000 | 1.000 | `not(BOX(THEM(ME)))` (0.000) | 1.4e-01 / 1.3e-01 / 1.3e-01 (1.00) | 0 | 0.0e+00 |
| K b=3 | 0.2337 | 0.4903 | 0.6251 | 0.350 | `BOX(THEM(THEM))` (0.314) | 4.7e-04 / 4.7e-05 / 1.6e-05 (0.00) | 0 | 0.0e+00 |
| K b=4 | 0.4043 | 0.6822 | 0.7882 | 0.212 | `BOX(THEM(ME))` (0.270) | 4.7e-04 / 4.7e-05 / 1.6e-05 (0.00) | 0 | 0.0e+00 |
| K b=6 | 0.3922 | 0.6709 | 0.7795 | 0.221 | `BOX1(THEM(ME))` (0.587) | 4.7e-04 / 4.7e-05 / 1.6e-05 (0.00) | 0 | 2.7e-09 |
| K b=10 | 0.3797 | 0.6495 | 0.7616 | 0.238 | `BOX1(THEM(ME))` (0.192) | 4.9e-04 / 4.9e-05 / 1.6e-05 (0.00) | 0 | 6.1e-09 |
| K b=16 | 0.3797 | 0.6495 | 0.7616 | 0.238 | `BOX1(THEM(ME))` (0.379) | 4.8e-04 / 4.8e-05 / 1.6e-05 (0.00) | 0 | 6.3e-09 |
| control b=2 | 0.0120 | 0.0038 | 0.0019 | 0.996 | `not(BOX(THEM(ME)))` (0.001) | 4.9e-03 / 4.5e-03 / 4.5e-03 (1.00) | 0 | 2.5e-06 |
| control b=3 | 0.1381 | 0.0675 | 0.0415 | 0.950 | `BOX(THEM(THEM))` (0.019) | 1.8e-03 / 1.3e-03 / 1.3e-03 (0.99) | 0 | 1.8e-07 |
| control b=4 | 0.1210 | 0.1296 | 0.0967 | 0.903 | `BOX(THEM(ME))` (0.092) | 5.8e-04 / 1.5e-04 / 1.2e-04 (0.87) | 0 | 1.1e-07 |
| control b=6 | 0.1442 | 0.0860 | 0.0551 | 0.945 | `BOX1(THEM(ME))` (0.036) | 8.0e-04 / 3.6e-04 / 3.3e-04 (0.95) | 0 | 1.0e-07 |
| control b=10 | 0.2232 | 0.3499 | 0.4621 | 0.538 | `BOX(THEM(THEM))` (0.437) | 4.8e-04 / 4.8e-05 / 1.6e-05 (0.00) | 0 | 2.5e-08 |
| control b=16 | 0.2857 | 0.4748 | 0.5787 | 0.421 | `BOX1(THEM(ME))` (0.325) | 4.9e-04 / 4.9e-05 / 1.6e-05 (0.00) | 0 | 1.5e-08 |

Support at N = 3·10⁴ (π ≥ 10⁻³): free: mono {D:1} 0.293, mono {BOX(THEM(THEM)):1} 0.233, mono {BOX(THEM(ME)):1} 0.233, mono {BOX1(THEM(ME)):1} 0.232, mono {BOX1(THEM(THEM)):1} 0.005; K b=3: mono {D:1} 0.350, mono {BOX(THEM(THEM)):1} 0.314, mono {BOX(THEM(ME)):1} 0.311, mono {BOXD1(THEM(ME)):1} 0.025; K b=6: mono {BOX1(THEM(ME)):1} 0.587, mono {D:1} 0.221, mono {BOX(THEM(ME)):1} 0.186, mono {BOX1(THEM(THEM)):1} 0.002, mono {BOX(THEM(THEM)):1} 0.002; K b=16: mono {BOX1(THEM(ME)):1} 0.379, mono {D:1} 0.238, mono {BOX(THEM(THEM)):1} 0.190, mono {BOX(THEM(ME)):1} 0.190, mono {BOX(THEM(^C)):1} 0.001

Control = the free table with plays flipped at random, matched to the K arm stratum by stratum (opponent class × free play × reader has boxes).

Leak test (drift-closed components among self-cooperators, n = 6): b=1: 0, b=2: 0, b=3: 0, b=4: 0, b=5: 0, b=6: 0, b=7: 0, b=8: 0, b=9: 0, b=10: 0, b=11: 0, b=12: 0, b=13: 0, b=14: 0, b=15: 0, b=16: 0, b=17: 0, b=18: 0, b=19: 0, b=20: 0, b=21: 0, b=22: 0, b=23: 0, b=24: 0, b=25: 0, b=26: 0, b=27: 0, b=28: 0, b=29: 0, b=30: 0, b=31: 0, b=32: 0, b=33: 0, b=34: 0, b=35: 0, b=36: 0, b=37: 0, b=38: 0, b=39: 0, b=40: 0; free: 0.

ε = 0 lottery, n = 6, mN = 1, 20 paired seeds per cell (seeding as `src/bounded_lottery.py`), efficient fraction with Wilson 95%:

| arm | (N, I) = (100, 4) | (100, 64) |
|---|---|---|
| free | 6/20 = 0.30 [0.15, 0.52] | 20/20 = 1.00 [0.84, 1.00] |
| K b=2 | 0/20 = 0.00 [0.00, 0.16] | 0/20 = 0.00 [0.00, 0.16] |
| K b=3 | 2/20 = 0.10 [0.03, 0.30] | 16/20 = 0.80 [0.58, 0.92] |
| K b=4 | 5/20 = 0.25 [0.11, 0.47] | 20/20 = 1.00 [0.84, 1.00] |
| K b=6 | 4/20 = 0.20 [0.08, 0.42] | 20/20 = 1.00 [0.84, 1.00] |
| K b=10 | 6/20 = 0.30 [0.15, 0.52] | 20/20 = 1.00 [0.84, 1.00] |
| K b=16 | 5/20 = 0.25 [0.11, 0.47] | 20/20 = 1.00 [0.84, 1.00] |

### Run 3: per-program budgets with a price c·b per match (budgets {2, 3, 4, 6, 10, 16}, μ split equally across budgets, N = 10⁴)

| c | P(C,C) | π(all-D) | π(all-ALLC) | π by budget (0 = constants) | π on self-cooperating monomorphic states | top cooperative state (π) | its exit (strict) | top destinations |
|---|---|---|---|---|---|---|---|---|
| 0 | 0.5984 | 0.391 | 0.000 | 0: 0.391, 2: 0.008, 3: 0.151, 4: 0.201, 6: 0.117, 10: 0.066, 16: 0.065 | 0.598 | `BOX(THEM(ME))@3` (0.138) | 4.7e-05 (0.0e+00) | C neutral 4.7e-05; BOX(THEM(THEM))@3 neutral 8.2e-08; BOX(THEM(^BOX(THEM(ME))))@3 neutral 4.1e-10 |
| 0.01 | 0.0004 | 1.000 | 0.000 | 0: 1.000, 2: 0.000, 3: 0.000, 4: 0.000, 6: 0.000, 10: 0.000, 16: 0.000 | 0.000 | `BOX(THEM(ME))@3` (0.000) | 4.2e-03 (4.2e-03) | C strict 4.2e-03; BOX(THEM(THEM))@3 neutral 8.2e-08; BOX(THEM(^BOX(THEM(ME))))@3 neutral 4.1e-10 |
| 0.1 | 0.0000 | 1.000 | 0.000 | 0: 1.000, 2: 0.000, 3: 0.000, 4: 0.000, 6: 0.000, 10: 0.000, 16: 0.000 | 0.000 | `BOX(THEM(^BOX(THEM(ME))))@4` (0.000) | 5.3e-02 (5.3e-02) | C strict 5.3e-02; BOX(THEM(ME))@4 neutral 8.2e-08; BOX(THEM(THEM))@4 neutral 8.2e-08 |

