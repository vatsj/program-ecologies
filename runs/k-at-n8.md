# K at n = 8, lemma sharing, and non-per-match budget prices

Spec `specs/2026-10-05-k-at-n8.md`; predictions `predictions/2026-10-05-k-at-n8.md`. Code `src/k_at_n8.py` (with the GL-erasure prune hook in `src/bounded_k.py` and analytic cut / DAG measures in `src/gl_proofs.py`). Raw rows: `runs/k-at-n8-*.json`, `runs/k-at-n8/kmeta_n8_b*.json`. ε → 0 chain numbers are at the stated N; lottery numbers are ε = 0 at (N, I) = (100, 64). Prices are imposed schedules (verification events are not counted).

## 1. K play tables at n = 8 (every class of L_8 at a global budget b)

GL-erasure prune: a box content whose budget-erased form is not a GL+Def theorem is never searched (K ⊢ A implies GL+Def ⊢ erase(A)); validated by reproducing the n = 6 K tables exactly at b = 4 and 16 (and the unpruned n = 6 closure derives no formula the prune rejects, b = 16 and 40), and by agreement with four unpruned cross-budget n = 6 cells.

| b | box contents (GL-live) | passes | time (s) | soundness violations / checked | plays ≠ free | plays changed vs previous b | self-cooperators | GL-true atoms K-true: count | μ-weighted | drift-closed components |
|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 260656 (59982) | 3 | 135 | 0 / 497 | 84435 | — | 229 | 881 / 143269 = 0.006 | 0.7244 | 0 (of 1 components) |
| 4 | 260656 (59982) | 3 | 134 | 0 / 1275 | 82243 | 2754 | 261 | 6011 / 143269 = 0.042 | 0.9703 | 0 (of 1 components) |
| 6 | 260656 (59982) | 4 | 193 | 0 / 5730 | 71026 | 12275 | 278 | 28853 / 143269 = 0.201 | 0.9828 | 0 (of 1 components) |
| 8 | 260656 (59982) | 4 | 287 | 0 / 17474 | 60319 | 11371 | 283 | 48903 / 143269 = 0.341 | 0.9887 | 0 (of 1 components) |
| 12 | 260656 (59982) | 4 | 329 | 0 / 58568 | 44470 | 16165 | 287 | 74236 / 143269 = 0.518 | 0.9914 | 0 (of 1 components) |
| 16 | 260656 (59982) | 4 | 423 | 0 / 78340 | 37860 | 6822 | 286 | 83716 / 143269 = 0.584 | 0.9917 | 0 (of 1 components) |
| 24 | 260656 (59982) | 5 | 660 | 0 / 90444 | 34496 | 3394 | 287 | 88318 / 143269 = 0.616 | 0.9917 | 0 (of 1 components) |
| 32 | 260656 (59982) | 5 | 745 | 0 / 92196 | 34193 | 309 | 287 | 88711 / 143269 = 0.619 | 0.9917 | 0 (of 1 components) |
| 54 | 260656 (59982) | 5 | 804 | 0 / 93019 | 34042 | 151 | 287 | 88904 / 143269 = 0.621 | 0.9917 | 0 (of 1 components) |

Free arm: 287 self-cooperators, 0 drift-closed components. The table changes at every tested step; from 32 to 54 it changes in 151 plays with μ-weight 1.1·10⁻⁹ (unchanged over the tested budgets in μ-weight only, not in count). Max JLöb candidate set |U| after pruning: 3: 16, 4: 16, 6: 16, 8: 16, 12: 16, 16: 16, 24: 16, 32: 16, 54: 16.

**GL atoms K never proves (b = 54).** 54365 of 143269 GL-true atoms (0.379 by count, 0.0083 μ-weighted) stay unproved; 608 of 610 readers have at least one (their μ: 0.067). Largest: `and(BOX(THEM(ME)),not(BOX1(THEM(ME))))` (284); `or(BOXD1(THEM(ME)),not(BOXD(THEM(ME))))` (258); `or(BOXD1(THEM(THEM)),not(BOXD1(THEM(ME))))` (233); `and(BOXD1(THEM(ME)),not(BOX1(THEM(ME))))` (226); `or(BOXD1(THEM(ME)),not(BOXD1(THEM(THEM))))` (226).

**Named classes in L_8: self-play by b** (1 = C), and the number of opponents whose play against them differs from the free arm (row / column):

| class | free | b=3 | b=4 | b=6 | b=8 | b=12 | b=16 | b=24 | b=32 | b=54 | row/col ≠ free at b = 16 | at b = 54 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BOX(THEM(ME))` | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 24 / 39 | 24 / 39 |
| `BOX1(THEM(ME))` | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 66 / 16 | 66 / 16 |
| `BOX(THEM(THEM))` | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 12 / 41 | 8 / 39 |
| `BOX1(THEM(THEM))` | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 55 / 20 | 54 / 18 |
| `BOX(THEM(^C))` | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 8 / 39 | 8 / 39 |
| `BOX1(THEM(^C))` | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 58 / 16 | 58 / 16 |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 10 / 47 | 0 / 39 |
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 46 / 106 | 46 / 102 |
| `not(BOX(THEM(ME)))` | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 56 / 78 | 55 / 77 |
| `not(BOX(THEM(THEM)))` | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 12 / 76 | 8 / 76 |
| `BOX1(THEM(^not(BOX(THEM(ME)))))` | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 105 / 94 | 101 / 94 |
| `C` | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 / 0 | 0 / 0 |
| `D` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 / 0 | 0 / 0 |

**Named family beyond L_8** (K closure on the family alone, pruned by `src/conj4.py`'s trace evaluator; 0 soundness violations at every b; budgets [3, 4, 6, 8, 9, 10, 11, 12, 16, 24, 32, 54]): self-play by b.

| program | b=3 | b=4 | b=6 | b=8 | b=9 | b=10 | b=11 | b=12 | b=16 | b=24 | b=32 | b=54 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `BOX(THEM(ME))` | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| `BOX1(THEM(ME))` | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 |
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^C))))` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `and(and(BOX1(THEM(ME)),not(BOX(THEM(^C)))),BOXD2(THEM(^D)))` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `and(and(BOX1(THEM(ME)),not(BOX(THEM(ME)))),BOXD2(THEM(^D)))` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `and(BOX(THEM(ME)),BOXD2(THEM(^D)))` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `BOX(THEM(THEM))` | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| `BOX1(THEM(THEM))` | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| `BOX(THEM(^C))` | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| `BOX1(THEM(^C))` | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

Siblings y = or(x, ψ_K) at b = 54: x → y / y → x / y suckered by z = BOX_K(THEM(^D)) (y → z = C, z → y = D): `BOX(THEM(ME))` 1/1/yes; `BOX1(THEM(ME))` 1/1/yes; `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` 1/1/yes; `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` 0/1/yes; `and(BOX1(THEM(ME)),not(BOX(THEM(^C))))` 0/1/yes; `and(and(BOX1(THEM(ME)),not(BOX(THEM(^C))` 0/1/yes; `and(and(BOX1(THEM(ME)),not(BOX(THEM(ME))` 0/1/yes; `and(BOX(THEM(ME)),BOXD2(THEM(^D)))` 0/0/yes; `BOX(THEM(THEM))` 1/1/yes; `BOX1(THEM(THEM))` 1/1/yes; `BOX(THEM(^C))` 1/1/yes; `BOX1(THEM(^C))` 1/1/yes

**Leak test on the cross-budget catalogue.** No component is drift-closed at any fixed b, so none is closed in the catalogue of every class at every budget (each fixed-b graph is an induced subgraph of the catalogue's; suckering pairs survive; predictions, design choice 4). Computed check at n = 6 on the priced catalogue (budgets {2, 3, 4, 6, 10, 16}, 386 genotypes): 128 self-cooperators in 1 component(s), 0 closed. Computed at n = 8 on the catalogue over b ∈ {4, 16} (every class at both budgets, cross-budget plays by a pruned K closure with 0 soundness violations in 37,893 checked formulas): 1218 genotypes, 546 self-cooperators in 1 component(s), 0 closed.

## 2. The lim_N chain at n = 8 (PD, w = 0.3)

| arm | P(C,C) N = 10³ | 10⁴ | 3·10⁴ | π(all-D) 3·10⁴ | π on self-cooperating states 3·10⁴ | top state (π, 3·10⁴) | top exit 10³ / 10⁴ / 3·10⁴ | exit slope | strict share | ALLC share | odds slope | entry from all-D: N·ρ | terminal / indeterminate / cut flow |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| free | 0.3707 | 0.6172 | 0.7246 | 0.275 | 0.725 | `BOX(THEM(ME))` (0.226) | 4.85e-04 / 4.85e-05 / 1.62e-05 | -1.00 | 0.000 | 0.96 | 0.44 | 43.5 | 1 / 0 / 2e-07 |
| K b=4 | 0.4138 | 0.6789 | 0.7736 | 0.226 | 0.774 | `BOX(THEM(ME))` (0.301) | 4.72e-04 / 4.72e-05 / 1.57e-05 | -1.00 | 0.000 | 0.99 | 0.47 | 43.5 | 1 / 0 / 0e+00 |
| K b=8 | 0.3967 | 0.6622 | 0.7623 | 0.238 | 0.762 | `BOX1(THEM(ME))` (0.218) | 4.85e-04 / 4.83e-05 / 1.61e-05 | -1.00 | 0.004 | 0.96 | 0.47 | 43.5 | 1 / 0 / 1e-07 |
| K b=16 | 0.3920 | 0.6710 | 0.7909 | 0.209 | 0.791 | `BOX(THEM(ME))` (0.173) | 4.85e-04 / 4.85e-05 / 1.62e-05 | -1.00 | 0.000 | 0.96 | 0.52 | 43.5 | 1 / 0 / 2e-07 |
| K b=54 | 0.3920 | 0.6709 | 0.7911 | 0.209 | 0.791 | `BOX(THEM(ME))` (0.174) | 4.85e-04 / 4.85e-05 / 1.62e-05 | -1.00 | 0.000 | 0.96 | 0.52 | 43.5 | 1 / 0 / 2e-07 |
| faker-removal control | 0.3922 | 0.6710 | 0.7912 | 0.209 | 0.791 | `BOX(THEM(ME))` (0.174) | 4.87e-04 / 4.87e-05 / 1.62e-05 | -1.00 | 0.000 | 0.96 | 0.52 | 43.5 | 1 / 0 / 2e-07 |

Faker-removal control: the free n = 8 table with 37 classes deleted (μ 0.0029), identified as in the predictions (strict free-arm invaders of a supported self-cooperator whose invasion K at b = 16 removes; 21 of them Gödel sentences, i.e. self-cooperating with no level-0 proof). K b = 16 − free at N = 10⁴: +0.0537; control − free: +0.0538; share explained 1.00.

Support at N = 3·10⁴ (π ≥ 10⁻³):

- free: {D:1} 0.275, {BOX(THEM(ME)):1} 0.226, {BOX1(THEM(ME)):1} 0.225, {BOX(THEM(THEM)):1} 0.171, {and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):1} 0.053, {and(BOX1(THEM(ME)),not(BOX(THEM(THEM)))):1} 0.026, {and(BOX(THEM(ME)),BOXD1(THEM(^D))):1} 0.008, {BOX1(THEM(THEM)):1} 0.005
- K b=4: {BOX(THEM(ME)):1} 0.301, {BOX1(THEM(ME)):1} 0.275, {D:1} 0.226, {BOX(THEM(THEM)):1} 0.162, {or(BOX(THEM(ME)),BOX1(THEM(ME))):1} 0.021, {or(BOX(THEM(ME)),BOX1(THEM(^C))):1} 0.004, {or(BOX(THEM(ME)),BOX(THEM(^D))):1} 0.004, {or(BOX(THEM(ME)),BOX1(THEM(^D))):1} 0.004
- K b=8: {D:1} 0.238, {BOX1(THEM(ME)):1} 0.218, {BOX1(THEM(THEM)):1} 0.197, {BOX(THEM(ME)):1} 0.195, {BOX(THEM(THEM)):1} 0.122, {and(BOX1(THEM(ME)),BOX1(THEM(THEM))):1} 0.025, {BOX(THEM(^C)):1} 0.001
- K b=16: {D:1} 0.209, {BOX(THEM(ME)):1} 0.173, {BOX1(THEM(ME)):1} 0.171, {and(BOX(THEM(ME)),BOXD1(THEM(^D))):1} 0.148, {BOX(THEM(THEM)):1} 0.147, {BOX1(THEM(THEM)):1} 0.138, {and(BOX(THEM(ME)),BOX1(THEM(^C))):1} 0.003, {BOX(THEM(^BOX1(THEM(ME)))):1} 0.002
- K b=54: {D:1} 0.209, {BOX(THEM(ME)):1} 0.174, {BOX1(THEM(ME)):1} 0.173, {and(BOX(THEM(ME)),BOXD1(THEM(^D))):1} 0.149, {BOX(THEM(THEM)):1} 0.147, {BOX1(THEM(THEM)):1} 0.141, {BOX(THEM(^BOX1(THEM(ME)))):1} 0.002, {BOX(THEM(^BOX(THEM(THEM)))):1} 0.001
- faker-removal control: {D:1} 0.209, {BOX(THEM(ME)):1} 0.174, {BOX1(THEM(ME)):1} 0.171, {and(BOX(THEM(ME)),BOXD1(THEM(^D))):1} 0.149, {BOX(THEM(THEM)):1} 0.147, {BOX1(THEM(THEM)):1} 0.141, {BOX(THEM(^BOX1(THEM(ME)))):1} 0.002, {BOX(THEM(^BOX(THEM(THEM)))):1} 0.001

Top-state exits at N = 10⁴ (mutant → destination, weight per mutation event, N·ρ, payoff differences mutant-vs-resident / resident-vs-mutant / mutant-vs-itself):

- free, top `BOX(THEM(ME))`: `C` 4.7e-05 N·ρ 1.00 Δ 0/0/0; `BOX1(THEM(ME))` 5.1e-07 N·ρ 1.00 Δ 0/0/0; `BOX(THEM(THEM))` 5.1e-07 N·ρ 1.00 Δ 0/0/0
- K b=4, top `BOX(THEM(ME))`: `C` 4.7e-05 N·ρ 1.00 Δ 0/0/0; `BOX(THEM(THEM))` 5.0e-07 N·ρ 1.00 Δ 0/0/0; `BOX(THEM(^BOX(THEM(ME))))` 3.1e-09 N·ρ 1.00 Δ 0/0/0
- K b=8, top `BOX1(THEM(ME))`: `C` 4.7e-05 N·ρ 1.00 Δ 0/0/0; `BOX(THEM(ME))` 5.0e-07 N·ρ 1.00 Δ 0/0/0; `BOX(THEM(THEM))` 5.0e-07 N·ρ 1.00 Δ 0/0/0
- K b=16, top `BOX(THEM(ME))`: `C` 4.7e-05 N·ρ 1.00 Δ 0/0/0; `BOX1(THEM(ME))` 5.1e-07 N·ρ 1.00 Δ 0/0/0; `BOX(THEM(THEM))` 5.0e-07 N·ρ 1.00 Δ 0/0/0
- K b=54, top `BOX1(THEM(ME))`: `C` 4.7e-05 N·ρ 1.00 Δ 0/0/0; `BOX(THEM(ME))` 5.1e-07 N·ρ 1.00 Δ 0/0/0; `BOX1(THEM(THEM))` 5.1e-07 N·ρ 1.00 Δ 0/0/0
- faker-removal control, top `BOX(THEM(ME))`: `C` 4.7e-05 N·ρ 1.00 Δ 0/0/0; `BOX1(THEM(ME))` 5.1e-07 N·ρ 1.00 Δ 0/0/0; `BOX1(THEM(THEM))` 5.1e-07 N·ρ 1.00 Δ 0/0/0

**ε = 0 lottery at n = 8**, (N, I) = (100, 64), mN = 1, 20 paired seeds, success = every island ends held by cooperators (outcome "efficient"), unresolved censored: free 20/20 [0.84, 1.00]; K b=4 20/20 [0.84, 1.00]; K b=16 20/20 [0.84, 1.00]

## 3. Lemma sharing: the cost table in four columns

Tree = number of sequents of the minimal derivation; DAG = distinct sequents of that derivation (exact identity), with the subsumption variant (a sequent weakening an already certified one is a free reference) after the slash; cut = analytic cut on reachable boxed formulas and their contents. DAG numbers are upper bounds on the minimal DAG over all derivations. [lb, ub] = cut search aborted (300k expansions): certified lower bound, upper bound from the cut-free minimum. Λ in parentheses.

| program | root | tree / no cut (Λ) | tree / cut (Λ) | DAG / no cut: exact / subsumption | DAG / cut: exact / subsumption |
|---|---|---|---|---|---|
| `BOX(THEM(ME))` | C0 | 4 (1) | 4 (1) | 4 / 4 | 4 / 4 |
| `BOX(THEM(ME))` | C1 | 5 (1) | 5 (1) | 5 / 5 | 5 / 5 |
| `BOX(THEM(THEM))` | C0 | 4 (1) | 4 (1) | 4 / 4 | 4 / 4 |
| `BOX(THEM(THEM))` | C1 | 5 (1) | 5 (1) | 5 / 5 | 5 / 5 |
| `BOX1(THEM(ME))` | C0 | 5 (1) | 5 (1) | 5 / 5 | 5 / 5 |
| `BOX1(THEM(ME))` | C1 | 6 (1) | 6 (1) | 6 / 6 | 6 / 6 |
| `BOX1(THEM(THEM))` | C0 | 5 (1) | 5 (1) | 5 / 5 | 5 / 5 |
| `BOX1(THEM(THEM))` | C1 | 6 (1) | 6 (1) | 6 / 6 | 6 / 6 |
| `BOX(THEM(^C))` | C0 | 6 (2) | 6 (2) | 6 / 6 | 6 / 6 |
| `BOX(THEM(^C))` | C1 | 7 (2) | 7 (2) | 7 / 7 | 7 / 7 |
| `BOX1(THEM(^C))` | C0 | 8 (2) | 8 (2) | 8 / 8 | 8 / 8 |
| `BOX1(THEM(^C))` | C1 | 9 (2) | 9 (2) | 9 / 9 | 9 / 9 |
| `not(BOX(THEM(ME)))` | C1 | 8 (1) | 8 (1) | 8 / 8 | 8 / 8 |
| `BOX(THEM(^BOX(THEM(ME))))` | C0 | 6 (2) | 6 (2) | 6 / 6 | 6 / 6 |
| `BOX(THEM(^BOX(THEM(ME))))` | C1 | 7 (2) | 7 (2) | 7 / 7 | 7 / 7 |
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | C1 | 22 (3) | 22 (3) | 22 / 16 | 22 / 16 |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | C0 | 24 (5) | 18 (3) | 24 / 15 | 18 / 17 |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | C1 | 25 (5) | 19 (3) | 25 / 16 | 19 / 18 |
| `and(BOX(THEM(ME)),BOXD2(THEM(^D)))` | C0 | 24 (5) | 18 (3) | 24 / 15 | 18 / 17 |
| `and(BOX(THEM(ME)),BOXD2(THEM(^D)))` | C1 | 25 (5) | 19 (3) | 25 / 16 | 19 / 18 |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^C))))` | C1 | 24 (5) | 24 (5) | 24 / 17 | 24 / 17 |
| `and(and(BOX1(THEM(ME)),not(BOX(THEM(ME)))),BOXD2(THEM(^D)))` | C1 | 52 (7) | [23, 52] (7) | 52 / 32 | [23, 52] / [23, 32] |
| `and(and(BOX1(THEM(ME)),not(BOX(THEM(^C)))),BOXD2(THEM(^D)))` | C1 | 54 (9) | [16, 54] (9) | 54 / 33 | [16, 54] / [16, 33] |

**Sibling ratios** L(x → y)/L(x → x), y = or(x, ψ_K), under each measure: L_read (sum over x's true atoms) and L_out (x's cooperation proof, level 0 else 1). * = some cut search uncertified (upper bound from the cut-free minimum).

| x | L_read: tree | tree/cut | DAG exact | DAG subs | L_out: tree | tree/cut | DAG exact | DAG subs |
|---|---|---|---|---|---|---|---|---|
| `BOX(THEM(ME))` | 6/3 = 2.00 | 6/3 = 2.00 | 6/3 = 2.00 | 6/3 = 2.00 | 7/4 = 1.75 | 7/4 = 1.75 | 7/4 = 1.75 | 7/4 = 1.75 |
| `BOX1(THEM(ME))` | 8/4 = 2.00 | 8/4 = 2.00 | 8/4 = 2.00 | 8/4 = 2.00 | 9/5 = 1.80 | 9/5 = 1.80 | 9/5 = 1.80 | 9/5 = 1.80 |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 51/22 = 2.32 | 51/22 = 2.32* | 51/22 = 2.32 | 49/22 = 2.23 | 53/24 = 2.21 | 53/18 = 2.94* | 53/24 = 2.21 | 35/15 = 2.33 |
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 31/12 = 2.58 | 31/12 = 2.58* | 31/12 = 2.58 | 31/12 = 2.58 | 47/22 = 2.14 | 47/22 = 2.14* | 47/22 = 2.14 | 35/16 = 2.19 |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^C))))` | 31/13 = 2.38 | 31/13 = 2.38* | 31/13 = 2.38 | 31/13 = 2.38 | 47/24 = 1.96 | 47/24 = 1.96* | 47/24 = 1.96 | 35/17 = 2.06 |
| `and(and(BOX1(THEM(ME)),not(BOX(THEM(^C)))),BOXD2(THEM(^D)))` | 90/41 = 2.20 | 90/41 = 2.20* | 90/41 = 2.20 | 88/41 = 2.15 | 108/54 = 2.00 | 108/54 = 2.00* | 108/54 = 2.00 | 73/33 = 2.21 |
| `and(and(BOX1(THEM(ME)),not(BOX(THEM(ME)))),BOXD2(THEM(^D)))` | 90/40 = 2.25 | 90/40 = 2.25* | 90/40 = 2.25 | 88/40 = 2.20 | 108/52 = 2.08 | 108/52 = 2.08* | 108/52 = 2.08 | 73/32 = 2.28 |
| `and(BOX(THEM(ME)),BOXD2(THEM(^D)))` | 51/22 = 2.32 | 51/22 = 2.32* | 51/22 = 2.32 | 51/22 = 2.32 | 53/24 = 2.21 | 53/18 = 2.94* | 53/24 = 2.21 | 36/15 = 2.40 |
| `BOX(THEM(THEM))` | 4/3 = 1.33 | 4/3 = 1.33 | 4/3 = 1.33 | 4/3 = 1.33 | 5/4 = 1.25 | 5/4 = 1.25 | 5/4 = 1.25 | 5/4 = 1.25 |
| `BOX1(THEM(THEM))` | 5/4 = 1.25 | 5/4 = 1.25 | 5/4 = 1.25 | 5/4 = 1.25 | 6/5 = 1.20 | 6/5 = 1.20 | 6/5 = 1.20 | 6/5 = 1.20 |
| `BOX(THEM(^C))` | 6/5 = 1.20 | 6/5 = 1.20 | 6/5 = 1.20 | 6/5 = 1.20 | 7/6 = 1.17 | 7/6 = 1.17 | 7/6 = 1.17 | 7/6 = 1.17 |
| `BOX1(THEM(^C))` | 8/7 = 1.14 | 8/7 = 1.14 | 8/7 = 1.14 | 8/7 = 1.14 | 9/8 = 1.12 | 9/8 = 1.12 | 9/8 = 1.12 | 9/8 = 1.12 |

**Bracketed cut minima re-run with 5·10⁶ expansions** (`src/k_at_n8_certify.py`): `and(and(BOX1(THEM(ME)),not(BOX(THEM(ME)))),BO` vs self, C1: cut 42 (Λ 5), DAG exact 42 / subsumption 34, certified; `and(and(BOX1(THEM(ME)),not(BOX(THEM(^C)))),BO` vs self, C1: still uncertified, lower bound 22 (cut-free 54); `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` vs its sibling, C0: still uncertified, lower bound 19 (cut-free 53). Rows not listed were not reached before the run was stopped.

**Cut search certification (n = 6, every pair).** Iterative deepening with analytic cut against Knuth's algorithm on the normal-form graph with cut: 2733 roots compared (3998 of 4356 pairs fit), 0 mismatches; against the all-orders graph with cut on a 1-in-10 sample of pairs: 135 roots (298 pairs fit), 0 mismatches; 0 cut searches uncertified. 2197 s.

At n = 6 (3308 provable roots): cut shortens 0, exact DAG 0, subsumption DAG 0; max saving 0 (cut) and 0 (subsumption).

**Scaling on the n = 8 mutually cooperating establisher pairs** (8256 of 8256 ordered pairs cut-free; the cut measures on a uniform random sample of 200, cut search capped at 10⁵ expansions, uncertified rows dropped; cost of cooperation = C0 if provable else C1; descriptive only: a dependent sample, so a quadratic interval containing 0 is not evidence of linearity):

| measure | n (uncertified dropped) | mean | slope in |x|+|y| (se) | residual sd / mean | quadratic term [95%] |
|---|---|---|---|---|---|
| tree/no cut | 6422 (0) | 13.18 | 0.487 (0.052) | 0.58 | -0.175 [-0.217, -0.133] |
| DAG exact/no cut | 6422 (0) | 13.08 | 0.480 (0.051) | 0.57 | -0.172 [-0.213, -0.131] |
| DAG subsumption/no cut | 6422 (0) | 12.61 | 0.408 (0.044) | 0.51 | -0.166 [-0.202, -0.131] |
| tree/no cut [random sample] | 152 (0) | 12.74 | 0.480 (0.306) | 0.57 | -0.188 [-0.494, 0.119] |
| tree/cut [random sample] | 126 (26) | 10.40 | 0.293 (0.122) | 0.27 | -0.019 [-0.143, 0.105] |
| DAG exact/no cut [random sample] | 152 (0) | 12.61 | 0.501 (0.301) | 0.57 | -0.199 [-0.501, 0.103] |
| DAG exact/cut [random sample] | 126 (26) | 10.35 | 0.301 (0.121) | 0.27 | -0.009 [-0.132, 0.114] |
| DAG subsumption/no cut [random sample] | 152 (0) | 12.19 | 0.404 (0.274) | 0.53 | -0.207 [-0.480, 0.067] |
| DAG subsumption/cut [random sample] | 126 (26) | 10.30 | 0.297 (0.119) | 0.26 | -0.012 [-0.133, 0.109] |

The cut rows drop the 26 uncertified pairs, which are the long proofs (mean cut-free size 23.2), so their fits are not comparable with the cut-free rows. Paired on the 126 certified pairs: mean size 10.60 cut-free, 10.40 with cut (shorter in 6, max saving 7), 10.33 subsumption DAG (shorter in 6). Over all 6422 pairs with a cooperation proof, the subsumption DAG is shorter than the tree in 758 and exact identity in 204.

## 4. Prices in K (n = 6, per-program budgets {2, 3, 4, 6, 10, 16}, μ split equally, N = 10⁴ unless stated; imposed schedules)

Costs on the reader x@b per match (constants pay nothing): per-match c·b; amortized c·b/N; cache c·b·k/N with k = 2 classes present during a single-mutant invasion (on the chain's transitions this equals amortized at 2c); lazy c·b against non-constant non-copy opponents, copy = (a) identical budgeted program, (b) same source any budget, (c) extensionally identical play.

| schedule | c | N | copy | P(C,C) | π(all-D) | π(all-ALLC) | cooperative π by budget (normalized) | share on 3–4 | top budget share | top state (π) | top exit (strict) | μ on self-cooperating classes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| per-match | 0.01 | 10000 | — | 0.0004 | 1.000 | 0.0000 | 2: 0.000, 3: 0.626, 4: 0.349, 6: 0.018, 10: 0.004, 16: 0.003 | 0.976 | 0.626 | `BOX(THEM(ME))@3` (0.000) | 4.20e-03 (4.20e-03) | 0.0249 |
| amortized | 0 | 10000 | — | 0.5984 | 0.391 | 0.0002 | 2: 0.000, 3: 0.249, 4: 0.336, 6: 0.195, 10: 0.110, 16: 0.109 | 0.585 | 0.336 | `BOX(THEM(ME))@3` (0.138) | 4.70e-05 (0.00e+00) | 0.0249 |
| amortized | 0.01 | 1000 | — | 0.3188 | 0.666 | 0.0013 | 2: 0.000, 3: 0.206, 4: 0.307, 6: 0.207, 10: 0.141, 16: 0.139 | 0.513 | 0.307 | `BOX(THEM(ME))@3` (0.046) | 4.72e-04 (4.71e-04) | 0.0249 |
| amortized | 0.01 | 10000 | — | 0.5961 | 0.393 | 0.0002 | 2: 0.000, 3: 0.250, 4: 0.337, 6: 0.196, 10: 0.109, 16: 0.108 | 0.587 | 0.337 | `BOX(THEM(ME))@3` (0.138) | 4.72e-05 (4.71e-05) | 0.0249 |
| amortized | 0.01 | 30000 | — | 0.7190 | 0.273 | 0.0001 | 2: 0.000, 3: 0.255, 4: 0.341, 6: 0.194, 10: 0.106, 16: 0.104 | 0.596 | 0.341 | `BOX(THEM(ME))@3` (0.178) | 1.57e-05 (1.57e-05) | 0.0249 |
| amortized | 0.1 | 1000 | — | 0.2981 | 0.687 | 0.0013 | 2: 0.000, 3: 0.212, 4: 0.315, 6: 0.209, 10: 0.138, 16: 0.127 | 0.527 | 0.315 | `BOX(THEM(ME))@3` (0.044) | 4.91e-04 (4.90e-04) | 0.0249 |
| amortized | 0.1 | 10000 | — | 0.5762 | 0.413 | 0.0002 | 2: 0.000, 3: 0.258, 4: 0.346, 6: 0.195, 10: 0.105, 16: 0.096 | 0.604 | 0.346 | `BOX(THEM(ME))@3` (0.137) | 4.91e-05 (4.90e-05) | 0.0249 |
| amortized | 0.1 | 30000 | — | 0.7026 | 0.289 | 0.0001 | 2: 0.000, 3: 0.264, 4: 0.350, 6: 0.194, 10: 0.101, 16: 0.092 | 0.613 | 0.350 | `BOX(THEM(ME))@3` (0.180) | 1.64e-05 (1.63e-05) | 0.0249 |
| amortized | 1 | 1000 | — | 0.1659 | 0.822 | 0.0014 | 2: 0.000, 3: 0.249, 4: 0.355, 6: 0.209, 10: 0.114, 16: 0.073 | 0.604 | 0.355 | `BOX(THEM(ME))@3` (0.026) | 7.12e-04 (7.11e-04) | 0.0249 |
| amortized | 1 | 10000 | — | 0.4187 | 0.569 | 0.0003 | 2: 0.000, 3: 0.310, 4: 0.384, 6: 0.180, 10: 0.076, 16: 0.050 | 0.694 | 0.384 | `BOX(THEM(ME))@3` (0.116) | 7.12e-05 (7.11e-05) | 0.0249 |
| amortized | 1 | 30000 | — | 0.5624 | 0.427 | 0.0001 | 2: 0.000, 3: 0.321, 4: 0.388, 6: 0.177, 10: 0.069, 16: 0.045 | 0.709 | 0.388 | `BOX(THEM(ME))@3` (0.173) | 2.37e-05 (2.37e-05) | 0.0249 |
| cache | 0.01 | 10000 | — | 0.5939 | 0.395 | 0.0002 | 2: 0.000, 3: 0.251, 4: 0.338, 6: 0.196, 10: 0.109, 16: 0.106 | 0.589 | 0.338 | `BOX(THEM(ME))@3` (0.138) | 4.74e-05 (4.73e-05) | 0.0249 |
| cache | 0.1 | 10000 | — | 0.5551 | 0.433 | 0.0003 | 2: 0.000, 3: 0.267, 4: 0.354, 6: 0.195, 10: 0.100, 16: 0.085 | 0.621 | 0.354 | `BOX(THEM(ME))@3` (0.136) | 5.13e-05 (5.12e-05) | 0.0249 |
| lazy | 0.01 | 10000 | a | 0.5829 | 0.390 | 0.0002 | 2: 0.000, 3: 0.249, 4: 0.337, 6: 0.194, 10: 0.111, 16: 0.110 | 0.585 | 0.337 | `BOX(THEM(ME))@3` (0.134) | 4.69e-05 (0.00e+00) | 0.0249 |
| lazy | 0.1 | 10000 | a | 0.5756 | 0.389 | 0.0002 | 2: 0.000, 3: 0.264, 4: 0.339, 6: 0.173, 10: 0.111, 16: 0.111 | 0.604 | 0.339 | `BOX(THEM(ME))@3` (0.136) | 4.69e-05 (0.00e+00) | 0.0249 |
| lazy | 0.1 | 10000 | b | 0.5772 | 0.389 | 0.0002 | 2: 0.000, 3: 0.265, 4: 0.338, 6: 0.174, 10: 0.112, 16: 0.111 | 0.603 | 0.338 | `BOX(THEM(ME))@3` (0.137) | 4.69e-05 (0.00e+00) | 0.0249 |
| lazy | 0.1 | 10000 | c | 0.5756 | 0.389 | 0.0002 | 2: 0.000, 3: 0.264, 4: 0.339, 6: 0.173, 10: 0.111, 16: 0.111 | 0.604 | 0.339 | `BOX(THEM(ME))@3` (0.136) | 4.69e-05 (0.00e+00) | 0.0249 |

**Decisive edges** (top cooperative states' exits and their entry from all-D): Δ = mutant's payoff advantage against the resident at the start of invasion, N·Δ, and the fixation ratio ρ/ρ_neutral = N·ρ; the bound column is e^{w·c·b·2} (RE 5).

| schedule | c | N | copy | edge | Δ | N·Δ | N·ρ | e^{2wcb} |
|---|---|---|---|---|---|---|---|---|
| per-match | 0.01 | 10000 | — | `BOX(THEM(ME))@4` → `C` | 0.04 | 400 | 119.283 | 1.024 |
| per-match | 0.01 | 10000 | — | `BOX(THEM(ME))@3` → `C` | 0.03 | 300 | 89.596 | 1.018 |
| per-match | 0.01 | 10000 | — | `BOX(THEM(THEM))@3` → `C` | 0.03 | 300 | 89.596 | 1.018 |
| amortized | 0 | 10000 | — | `BOX(THEM(ME))@3` → `C` | 0 | 0 | 1.000 | 1.000 |
| amortized | 0 | 10000 | — | `BOX(THEM(ME))@4` → `C` | 0 | 0 | 1.000 | 1.000 |
| amortized | 0 | 10000 | — | `BOX1(THEM(ME))@4` → `C` | 0 | 0 | 1.000 | 1.000 |
| amortized | 0.01 | 1000 | — | `BOX1(THEM(ME))@4` → `C` | 4e-05 | 0.04 | 1.006 | 1.024 |
| amortized | 0.01 | 1000 | — | `BOX(THEM(ME))@4` → `C` | 4e-05 | 0.04 | 1.006 | 1.024 |
| amortized | 0.01 | 1000 | — | `BOX(THEM(ME))@3` → `C` | 3e-05 | 0.03 | 1.005 | 1.018 |
| amortized | 0.01 | 10000 | — | `BOX(THEM(ME))@4` → `C` | 4e-06 | 0.04 | 1.006 | 1.024 |
| amortized | 0.01 | 10000 | — | `BOX1(THEM(ME))@4` → `C` | 4e-06 | 0.04 | 1.006 | 1.024 |
| amortized | 0.01 | 10000 | — | `BOX(THEM(ME))@3` → `C` | 3e-06 | 0.03 | 1.005 | 1.018 |
| amortized | 0.01 | 30000 | — | `BOX1(THEM(ME))@4` → `C` | 1.33e-06 | 0.04 | 1.006 | 1.024 |
| amortized | 0.01 | 30000 | — | `BOX(THEM(ME))@4` → `C` | 1.33e-06 | 0.04 | 1.006 | 1.024 |
| amortized | 0.01 | 30000 | — | `BOX(THEM(ME))@3` → `C` | 1e-06 | 0.03 | 1.005 | 1.018 |
| amortized | 0.1 | 1000 | — | `BOX1(THEM(ME))@4` → `C` | 0.0004 | 0.4 | 1.061 | 1.271 |
| amortized | 0.1 | 1000 | — | `BOX(THEM(ME))@4` → `C` | 0.0004 | 0.4 | 1.061 | 1.271 |
| amortized | 0.1 | 1000 | — | `BOX(THEM(ME))@3` → `C` | 0.0003 | 0.3 | 1.046 | 1.197 |
| amortized | 0.1 | 10000 | — | `BOX1(THEM(ME))@4` → `C` | 4e-05 | 0.4 | 1.061 | 1.271 |
| amortized | 0.1 | 10000 | — | `BOX(THEM(ME))@4` → `C` | 4e-05 | 0.4 | 1.061 | 1.271 |
| amortized | 0.1 | 10000 | — | `BOX(THEM(ME))@3` → `C` | 3e-05 | 0.3 | 1.046 | 1.197 |
| amortized | 0.1 | 30000 | — | `BOX1(THEM(ME))@4` → `C` | 1.33e-05 | 0.4 | 1.061 | 1.271 |
| amortized | 0.1 | 30000 | — | `BOX(THEM(ME))@4` → `C` | 1.33e-05 | 0.4 | 1.061 | 1.271 |
| amortized | 0.1 | 30000 | — | `BOX(THEM(ME))@3` → `C` | 1e-05 | 0.3 | 1.046 | 1.197 |
| amortized | 1 | 1000 | — | `BOX(THEM(ME))@4` → `C` | 0.004 | 4 | 1.716 | 11.023 |
| amortized | 1 | 1000 | — | `BOX1(THEM(ME))@4` → `C` | 0.004 | 4 | 1.716 | 11.023 |
| amortized | 1 | 1000 | — | `BOX(THEM(ME))@3` → `C` | 0.003 | 3 | 1.516 | 6.050 |
| amortized | 1 | 10000 | — | `BOX(THEM(ME))@4` → `C` | 0.0004 | 4 | 1.717 | 11.023 |
| amortized | 1 | 10000 | — | `BOX1(THEM(ME))@4` → `C` | 0.0004 | 4 | 1.717 | 11.023 |
| amortized | 1 | 10000 | — | `BOX(THEM(ME))@3` → `C` | 0.0003 | 3 | 1.517 | 6.050 |
| amortized | 1 | 30000 | — | `BOX(THEM(ME))@4` → `C` | 0.000133 | 4 | 1.717 | 11.023 |
| amortized | 1 | 30000 | — | `BOX1(THEM(ME))@4` → `C` | 0.000133 | 4 | 1.717 | 11.023 |
| amortized | 1 | 30000 | — | `BOX(THEM(ME))@3` → `C` | 0.0001 | 3 | 1.517 | 6.050 |
| cache | 0.01 | 10000 | — | `BOX1(THEM(ME))@4` → `C` | 8e-06 | 0.08 | 1.012 | 1.024 |
| cache | 0.01 | 10000 | — | `BOX(THEM(ME))@4` → `C` | 8e-06 | 0.08 | 1.012 | 1.024 |
| cache | 0.01 | 10000 | — | `BOX(THEM(ME))@3` → `C` | 6e-06 | 0.06 | 1.009 | 1.018 |
| cache | 0.1 | 10000 | — | `BOX1(THEM(ME))@4` → `C` | 8e-05 | 0.8 | 1.125 | 1.271 |
| cache | 0.1 | 10000 | — | `BOX(THEM(ME))@4` → `C` | 8e-05 | 0.8 | 1.125 | 1.271 |
| cache | 0.1 | 10000 | — | `BOX(THEM(ME))@3` → `C` | 6e-05 | 0.6 | 1.093 | 1.197 |
| lazy | 0.01 | 10000 | a | `BOX(THEM(ME))@3` → `C` | 0 | 0 | 1.000 | 1.018 |
| lazy | 0.01 | 10000 | a | `BOX(THEM(ME))@4` → `C` | 0 | 0 | 1.000 | 1.024 |
| lazy | 0.01 | 10000 | a | `BOX1(THEM(ME))@4` → `C` | 0 | 0 | 1.000 | 1.024 |
| lazy | 0.1 | 10000 | a | `BOX(THEM(ME))@3` → `C` | 0 | 0 | 1.000 | 1.197 |
| lazy | 0.1 | 10000 | a | `BOX(THEM(ME))@4` → `C` | 0 | 0 | 1.000 | 1.271 |
| lazy | 0.1 | 10000 | a | `BOX1(THEM(ME))@4` → `C` | 0 | 0 | 1.000 | 1.271 |
| lazy | 0.1 | 10000 | b | `BOX(THEM(ME))@3` → `C` | 0 | 0 | 1.000 | 1.197 |
| lazy | 0.1 | 10000 | b | `BOX(THEM(ME))@4` → `C` | 0 | 0 | 1.000 | 1.271 |
| lazy | 0.1 | 10000 | b | `BOX1(THEM(ME))@4` → `C` | 0 | 0 | 1.000 | 1.271 |
| lazy | 0.1 | 10000 | c | `BOX(THEM(ME))@3` → `C` | 0 | 0 | 1.000 | 1.197 |
| lazy | 0.1 | 10000 | c | `BOX(THEM(ME))@4` → `C` | 0 | 0 | 1.000 | 1.271 |
| lazy | 0.1 | 10000 | c | `BOX1(THEM(ME))@4` → `C` | 0 | 0 | 1.000 | 1.271 |

Amortized exit slopes over N = 10³–3·10⁴: c = 0.01: -1.000, c = 0.1: -1.000, c = 1: -1.000.

## 5. Addendum (not in the spec; predictions addendum S10, S11): prices on the n = 8 K catalogue over b ∈ {4, 16}, N = 10⁴

| schedule | c | P(C,C) | π(all-D) | π by budget (0 = constants) | top state (π) | its exit (strict) | support (π ≥ 10⁻³) | terminal / indeterminate |
|---|---|---|---|---|---|---|---|---|
| per-match | 0.01 | 0.0005 | 1.000 | 0: 1.000, 4: 0.000, 16: 0.000 | `BOX(THEM(ME))@4` (0.000) | 5.6e-03 (5.6e-03) | {D:1} 1.000 | 1 / 0 |
| amortized | 0 | 0.6821 | 0.318 | 0: 0.318, 4: 0.512, 16: 0.170 | `BOX1(THEM(ME))@4` (0.217) | 4.7e-05 (0.0e+00) | {D:1} 0.318, {BOX1(THEM(ME))@4:1} 0.217, {BOX(THEM(ME))@4:1} 0.152, {BOX(THEM(THEM))@4:1} 0.133 | 1 / 0 |
| amortized | 0.1 | 0.6596 | 0.340 | 0: 0.340, 4: 0.514, 16: 0.131 | `BOX1(THEM(ME))@4` (0.216) | 5.0e-05 (5.0e-05) | {D:1} 0.340, {BOX1(THEM(ME))@4:1} 0.216, {BOX(THEM(ME))@4:1} 0.153, {BOX(THEM(THEM))@4:1} 0.134 | 1 / 0 |
| lazy | 0.01 | 1.0000 | 0.000 | 0: 0.000, 4: 0.000, 16: 1.000 | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))@16` (1.000) | 4.9e-58 (0.0e+00) | {and(BOX(THEM(ME)),BOXD1(THEM(^D)))@16:1} 1.000 | 1 / 0 |
| lazy | 0.1 | 1.0000 | 0.000 | 0: 0.000, 4: 0.000, 16: 1.000 | `and(BOX(THEM(ME)),BOXD1(THEM(^D)))@16` (1.000) | 0.0e+00 (0.0e+00) | {and(BOX(THEM(ME)),BOXD1(THEM(^D)))@16:1} 1.000 | 1 / 0 |

