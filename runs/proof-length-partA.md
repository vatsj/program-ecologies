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

