# K with the 4-rule, and a frozen classifier for what a sound bounded prover loses

Spec `specs/2026-10-05-k-four.md`; predictions `predictions/2026-10-05-k-four.md`; notes `notes/k-four.md` (§1: encoding, cost recurrence, soundness proof; Lemmas V, V′, G). Code: the `four` option of `src/bounded_k.py`, everything else `src/k_four.py`. Raw rows in `runs/k-four/`. ε → 0 chain numbers are at the stated N; the lottery is ε = 0 at (N, I) = (100, 64). K+4 = the spec's literal rule; K+4m = its monotone closure (cases i–iv); X-arm = guard read one budget up (exploratory, not in the spec).

## 0. Reproduction with the option off

| n | b | identical to the published K table | soundness violations |
|---|---|---|---|
| 8 | 4 | True | 0 |
| 8 | 8 | True | 0 |
| 8 | 16 | True | 0 |
| 6 | 4 | True | 0 |
| 6 | 16 | True | 0 |
| 6 | 40 | True | 0 |

## 1.a K+4 tables at n = 6

| b | rule | time (s) | soundness: violations / checked | plays ≠ free | plays ≠ K | μ²-weight of changed plays | self-cooperators | restored cooperators | restored exploiters | drift-closed components |
|---|---|---|---|---|---|---|---|---|---|---|
| 4 | K+4 | 0 | 0 / 130 | 872 | 0 | 0.00e+00 | 24 | 0 | 0 | 0 |
| 4 | K+4m | 0 | 0 / 130 | 872 | 0 | 0.00e+00 | 24 | 0 | 0 | 0 |
| 16 | K+4 | 1 | 0 / 1031 | 304 | 0 | 0.00e+00 | 25 | 0 | 0 | 0 |
| 16 | K+4m | 1 | 0 / 1031 | 304 | 0 | 0.00e+00 | 25 | 0 | 0 | 0 |
| 40 | K+4 | 1 | 0 / 1032 | 304 | 0 | 0.00e+00 | 25 | 0 | 0 | 0 |
| 40 | K+4m | 1 | 0 / 1032 | 304 | 0 | 0.00e+00 | 25 | 0 | 0 | 0 |


## 1.b K+4 tables at n = 8

| b | rule | time (s) | soundness: violations / checked | plays ≠ free | plays ≠ K | μ²-weight of changed plays | self-cooperators | restored cooperators | restored exploiters | drift-closed components |
|---|---|---|---|---|---|---|---|---|---|---|
| 4 | K+4m | 136 | 0 / 1275 | 82243 | 0 | 0.00e+00 | 261 | 0 | 0 | 0 |
| 8 | K+4m | 313 | 0 / 18297 | 59485 | 864 | 3.03e-06 | 284 | 1 | 28 | 0 |
| 12 | K+4m | 383 | 0 / 59414 | 43990 | 482 | 3.66e-07 | 287 | 0 | 0 | 0 |
| 16 | K+4 | 291 | 0 / 78340 | 37860 | 0 | 0.00e+00 | 286 | 0 | 0 | 0 |
| 16 | K+4m | 540 | 0 / 78727 | 37710 | 150 | 3.55e-09 | 286 | 0 | 1 | 0 |
| 24 | K+4m | 1168 | 0 / 90588 | 34439 | 57 | 3.69e-09 | 287 | 0 | 1 | 0 |
| 32 | K+4m | 1373 | 0 / 92234 | 34179 | 14 | 1.29e-10 | 287 | 0 | 0 | 0 |
| 54 | K+4 | 581 | 0 / 93019 | 34042 | 0 | 0.00e+00 | 287 | 0 | 0 | 0 |
| 54 | K+4m | 1334 | 0 / 93019 | 34042 | 0 | 0.00e+00 | 287 | 0 | 0 | 0 |

- b = 8, mono: changed plays vs K (reader, opponent, K, new): `BOX(THEM(ME))` vs `BOX(THEM(^BOX1(THEM(ME))))` 0→1; `BOX(THEM(ME))` vs `BOX1(THEM(^BOX(THEM(^C))))` 0→1; `BOX(THEM(ME))` vs `and(BOX(THEM(ME)),BOX(THEM(^C)))` 0→1; `BOX(THEM(THEM))` vs `BOX(THEM(^BOX1(THEM(ME))))` 0→1; `BOX(THEM(THEM))` vs `BOX(THEM(^BOX1(THEM(THEM))))` 0→1; `BOXD(THEM(ME))` vs `not(BOX(THEM(^D)))` 0→1; `BOX1(THEM(ME))` vs `or(BOX(THEM(THEM)),BOXD(THEM(ME)))` 0→1; `BOX1(THEM(ME))` vs `or(BOX(THEM(THEM)),BOXD(THEM(THEM)))` 0→1; `BOX1(THEM(ME))` vs `or(BOX(THEM(THEM)),BOXD1(THEM(ME)))` 0→1; `BOX1(THEM(ME))` vs `or(BOX(THEM(THEM)),BOXD1(THEM(THEM)))` 0→1; `BOX1(THEM(ME))` vs `or(BOX(THEM(THEM)),not(BOX(THEM(ME))))` 0→1; `BOX1(THEM(ME))` vs `or(BOX(THEM(THEM)),not(BOXD(THEM(ME))))` 0→1
  - classes K 371 → 389; splits: BOXD(THEM(^BOXD(THEM(THEM)))) (n 45, μ 3.19e-04, into 3); BOX1(THEM(^BOXD(THEM(ME)))) (n 4, μ 7.08e-05, into 3); BOX1(THEM(^BOXD1(THEM(ME)))) (n 13, μ 8.63e-05, into 2); not(BOXD(THEM(^BOXD(THEM(THEM))))) (n 15, μ 1.96e-05, into 3); not(BOX1(THEM(^BOXD(THEM(ME))))) (n 4, μ 8.95e-06, into 3); not(BOX1(THEM(^BOXD1(THEM(ME))))) (n 7, μ 1.10e-05, into 2); merges: BOXD(THEM(^BOX1(THEM(^C)))) (n 3, μ 1.34e-05, from 2); not(BOXD(THEM(^BOX(THEM(^D))))) (n 3, μ 2.05e-06, from 2)
  - restored exploiters: `or(BOX(THEM(ME)),BOX1(THEM(ME)))` → `BOX(THEM(^BOX1(THEM(THEM))))`, `BOX(THEM(^BOX1(THEM(ME))))`; `BOX(THEM(ME))` → `BOX1(THEM(^BOX1(THEM(THEM))))`; `BOX(THEM(^BOX(THEM(ME))))` → `BOX1(THEM(^BOX1(THEM(THEM))))`; `BOX(THEM(^BOX(THEM(THEM))))` → `BOX1(THEM(^BOX1(THEM(THEM))))`; `or(BOX(THEM(ME)),BOX(THEM(THEM)))` → `BOX1(THEM(^BOX1(THEM(THEM))))`; `or(BOX(THEM(THEM)),BOXD(THEM(ME)))` → `BOX1(THEM(^BOX1(THEM(THEM))))`, `BOX1(THEM(^BOX1(THEM(ME))))`; `or(BOX(THEM(THEM)),BOXD(THEM(THEM)))` → `BOX1(THEM(^BOX1(THEM(THEM))))`, `BOX1(THEM(^BOX1(THEM(ME))))`; `or(BOX(THEM(THEM)),BOX1(THEM(ME)))` → `BOX1(THEM(^BOX1(THEM(THEM))))`; `or(BOX(THEM(THEM)),BOXD1(THEM(ME)))` → `BOX1(THEM(^BOX1(THEM(THEM))))`, `BOX1(THEM(^BOX1(THEM(ME))))`; `or(BOX(THEM(THEM)),BOXD1(THEM(THEM)))` → `BOX1(THEM(^BOX1(THEM(THEM))))`, `BOX1(THEM(^BOX1(THEM(ME))))`
  - restored cooperators: `BOX1(THEM(^BOX(THEM(^C))))`
- b = 12, mono: changed plays vs K (reader, opponent, K, new): `BOXD(THEM(ME))` vs `not(BOX(THEM(^not(BOX1(THEM(ME))))))` 0→1; `BOX1(THEM(ME))` vs `BOX(THEM(^BOX(THEM(THEM))))` 0→1; `BOX1(THEM(ME))` vs `and(BOX(THEM(ME)),BOX(THEM(THEM)))` 0→1; `BOX1(THEM(ME))` vs `BOX(THEM(^BOX(THEM(^C))))` 0→1; `BOX1(THEM(ME))` vs `and(BOX(THEM(THEM)),BOX(THEM(^C)))` 0→1; `BOX1(THEM(ME))` vs `and(BOX1(THEM(THEM)),BOX(THEM(^C)))` 0→1; `not(BOX(THEM(ME)))` vs `BOXD(THEM(^BOXD1(THEM(ME))))` 1→0; `not(BOX(THEM(ME)))` vs `BOXD(THEM(^BOXD(THEM(^C))))` 1→0; `not(BOX(THEM(ME)))` vs `BOXD(THEM(^BOX1(THEM(^D))))` 1→0; `BOX(THEM(^BOX(THEM(THEM))))` vs `BOX1(THEM(^BOX1(THEM(^C))))` 0→1; `BOX(THEM(^BOXD(THEM(ME))))` vs `BOX(THEM(^not(BOX(THEM(^D)))))` 0→1; `BOX(THEM(^BOX1(THEM(ME))))` vs `BOX1(THEM(^BOX(THEM(THEM))))` 0→1
  - classes K 491 → 498; splits: BOX1(THEM(THEM)) (n 2, μ 5.05e-03, into 2); BOXD1(THEM(ME)) (n 2, μ 5.05e-03, into 2); not(BOX1(THEM(ME))) (n 2, μ 1.30e-03, into 2); not(BOX1(THEM(THEM))) (n 2, μ 1.30e-03, into 2); BOXD(THEM(^BOXD1(THEM(^C)))) (n 3, μ 1.34e-05, into 2); not(BOXD(THEM(^not(BOX(THEM(THEM)))))) (n 2, μ 1.36e-06, into 2); merges: BOX(THEM(^BOX1(THEM(ME)))) (n 2, μ 6.19e-05, from 2)
- b = 16, mono: changed plays vs K (reader, opponent, K, new): `BOX(THEM(^BOX(THEM(THEM))))` vs `and(BOX(THEM(ME)),BOX(THEM(^C)))` 0→1; `BOX(THEM(^BOX1(THEM(ME))))` vs `and(BOX(THEM(ME)),BOX(THEM(THEM)))` 0→1; `BOX(THEM(^BOX1(THEM(ME))))` vs `and(BOX(THEM(ME)),BOX1(THEM(ME)))` 0→1; `BOX(THEM(^BOX1(THEM(ME))))` vs `and(BOX(THEM(ME)),BOX1(THEM(THEM)))` 0→1; `BOX(THEM(^BOX1(THEM(ME))))` vs `and(BOX(THEM(ME)),BOX(THEM(^C)))` 0→1; `BOX(THEM(^BOX1(THEM(THEM))))` vs `and(BOX(THEM(ME)),BOX(THEM(THEM)))` 0→1; `BOX1(THEM(^BOX(THEM(THEM))))` vs `and(BOX(THEM(ME)),BOX(THEM(^C)))` 0→1; `BOX1(THEM(^BOX1(THEM(THEM))))` vs `and(BOX(THEM(ME)),BOX(THEM(THEM)))` 0→1; `BOX1(THEM(^BOXD1(THEM(ME))))` vs `BOX(THEM(^not(BOX1(THEM(^D)))))` 0→1; `BOX1(THEM(^BOXD1(THEM(ME))))` vs `BOX1(THEM(^not(BOX(THEM(^D)))))` 0→1; `BOX1(THEM(^BOXD1(THEM(THEM))))` vs `BOX(THEM(^not(BOXD(THEM(^D)))))` 0→1; `BOXD1(THEM(^BOXD(THEM(THEM))))` vs `not(BOX(THEM(^not(BOXD1(THEM(ME))))))` 0→1
  - classes K 476 → 474; splits: BOX(THEM(^BOX1(THEM(ME)))) (n 2, μ 6.19e-05, into 2); not(BOX(THEM(^BOX1(THEM(ME))))) (n 2, μ 7.59e-06, into 2); and(BOXD(THEM(ME)),not(BOX(THEM(ME)))) (n 2, μ 2.73e-06, into 2); and(BOXD(THEM(ME)),not(BOX(THEM(THEM)))) (n 2, μ 2.73e-06, into 2); and(BOXD(THEM(THEM)),not(BOX(THEM(ME)))) (n 2, μ 2.73e-06, into 2); merges: BOXD(THEM(^BOXD(THEM(THEM)))) (n 2, μ 6.19e-05, from 2); BOXD(THEM(^BOXD1(THEM(THEM)))) (n 2, μ 6.19e-05, from 2); BOX1(THEM(^BOXD(THEM(THEM)))) (n 2, μ 6.19e-05, from 2); not(BOXD(THEM(^BOXD(THEM(THEM))))) (n 2, μ 7.59e-06, from 2); not(BOX1(THEM(^BOXD(THEM(THEM))))) (n 2, μ 7.59e-06, from 2); not(BOXD(THEM(^BOX(THEM(^C))))) (n 2, μ 1.36e-06, from 2)
  - restored exploiters: `and(BOX(THEM(ME)),BOX(THEM(THEM)))` → `BOX1(THEM(^BOX1(THEM(THEM))))`
- b = 24, mono: changed plays vs K (reader, opponent, K, new): `BOX(THEM(^BOX(THEM(THEM))))` vs `and(BOX(THEM(ME)),BOX1(THEM(ME)))` 0→1; `BOX(THEM(^BOX1(THEM(ME))))` vs `and(BOX(THEM(ME)),BOX1(THEM(ME)))` 0→1; `BOX(THEM(^BOX1(THEM(THEM))))` vs `and(BOX(THEM(ME)),BOX1(THEM(ME)))` 0→1; `BOX(THEM(^BOX1(THEM(THEM))))` vs `and(BOX1(THEM(ME)),BOX(THEM(^C)))` 0→1; `BOXD(THEM(^BOXD1(THEM(ME))))` vs `not(and(BOX(THEM(ME)),BOX1(THEM(ME))))` 0→1; `BOX1(THEM(^BOX(THEM(THEM))))` vs `and(BOX(THEM(ME)),BOX1(THEM(ME)))` 0→1; `BOX1(THEM(^BOX(THEM(THEM))))` vs `and(BOX(THEM(ME)),BOX1(THEM(^C)))` 0→1; `BOX1(THEM(^BOX1(THEM(THEM))))` vs `and(BOX(THEM(ME)),BOX1(THEM(ME)))` 0→1; `not(BOX(THEM(^BOX(THEM(THEM)))))` vs `and(BOX(THEM(ME)),BOX1(THEM(ME)))` 1→0; `not(BOX(THEM(^BOX1(THEM(ME)))))` vs `and(BOX(THEM(ME)),BOX1(THEM(ME)))` 1→0; `not(BOX(THEM(^BOX1(THEM(THEM)))))` vs `and(BOX(THEM(ME)),BOX1(THEM(ME)))` 1→0; `not(BOX(THEM(^BOX1(THEM(THEM)))))` vs `and(BOX1(THEM(ME)),BOX(THEM(^C)))` 1→0
  - classes K 321 → 319; splits: BOXD(THEM(^BOXD(THEM(^C)))) (n 4, μ 1.79e-05, into 2); merges: BOXD(THEM(ME)) (n 7, μ 1.02e-02, from 2); not(BOXD(THEM(^BOXD(THEM(ME))))) (n 4, μ 1.52e-05, from 2); not(BOXD(THEM(^BOXD(THEM(THEM))))) (n 2, μ 7.59e-06, from 2)
  - restored exploiters: `and(BOX1(THEM(ME)),BOX(THEM(^C)))` → `BOX(THEM(^BOX1(THEM(THEM))))`
- b = 32, mono: changed plays vs K (reader, opponent, K, new): `and(BOX(THEM(ME)),BOX1(THEM(ME)))` vs `BOX1(THEM(^BOX1(THEM(^C))))` 0→1; `BOXD(THEM(^BOXD(THEM(^C))))` vs `not(and(BOX(THEM(ME)),BOX1(THEM(ME))))` 0→1; `BOXD(THEM(^BOXD1(THEM(^C))))` vs `not(and(BOX(THEM(ME)),BOX1(THEM(ME))))` 0→1; `BOXD1(THEM(^BOXD(THEM(^C))))` vs `not(and(BOX(THEM(ME)),BOX1(THEM(ME))))` 0→1; `BOXD1(THEM(^BOXD1(THEM(^C))))` vs `not(and(BOX(THEM(ME)),BOX1(THEM(ME))))` 0→1; `not(and(BOX(THEM(ME)),BOX1(THEM(ME))))` vs `BOXD(THEM(^BOXD1(THEM(ME))))` 1→0; `not(and(BOX(THEM(ME)),BOX1(THEM(ME))))` vs `BOXD(THEM(^BOXD(THEM(^C))))` 1→0; `not(and(BOX(THEM(ME)),BOX1(THEM(ME))))` vs `BOXD(THEM(^BOXD1(THEM(^C))))` 1→0; `not(and(BOX(THEM(ME)),BOX1(THEM(ME))))` vs `BOXD1(THEM(^BOXD(THEM(^C))))` 1→0; `not(and(BOX(THEM(ME)),BOX1(THEM(ME))))` vs `BOXD1(THEM(^BOXD1(THEM(^C))))` 1→0; `not(BOXD(THEM(^BOXD(THEM(^C)))))` vs `not(and(BOX(THEM(ME)),BOX1(THEM(ME))))` 1→0; `not(BOXD(THEM(^BOXD1(THEM(^C)))))` vs `not(and(BOX(THEM(ME)),BOX1(THEM(ME))))` 1→0
  - classes K 284 → 283; splits: none; merges: BOXD(THEM(ME)) (n 7, μ 1.02e-02, from 2)

Named self-play in K+4m at n = 8 (1 = C): b = 4: 00111110; b = 8: 00111110; b = 12: 01111110; b = 16: 01111110; b = 24: 01111110; b = 32: 01111110; b = 54: 01111110
(order: `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))`, `and(BOX(THEM(ME)),BOXD1(THEM(^D)))`, `BOX(THEM(ME))`, `BOX1(THEM(ME))`, `BOX(THEM(THEM))`, `BOX1(THEM(THEM))`, `C`, `D`)

## 2. Dense sweeps on the named family (b = 4…40)

Family: 33 programs (the five Con/4-axiom cooperators, PrudentBot, FairBot, `BOX1(THEM(ME))`, `BOX(THEM(THEM))`, `BOX1(THEM(THEM))`, C, D, the 21 Gödel-sentence fakers and their free-arm victims). b\* = first b at which the program self-cooperates; witness = the exact minimal sizes T of its self-play atom contents at b\* (each witnessed by a derivation; at b\* − 1 at least one exceeds the budget).

| program | b\* K | b\* K, guard +1 | b\* K+4m | b\* K+4m, guard +1 |
|---|---|---|---|---|
| `and(BOX(THEM(ME)),BOXD2(THEM(^D)))` | never (≤ 54) | never (≤ 54) | never (≤ 54) | 11 [T = 11, 6] |
| `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | never (≤ 54) | never (≤ 54) | never (≤ 54) | never (≤ 54) |
| `and(BOX1(THEM(ME)),not(BOX(THEM(^C))))` | never (≤ 54) | never (≤ 54) | never (≤ 54) | never (≤ 54) |
| `and(and(BOX1(THEM(ME)),not(BOX(THEM(^C)))),BOXD2(THEM(^D)))` | never (≤ 54) | never (≤ 54) | never (≤ 54) | never (≤ 54) |
| `and(and(BOX1(THEM(ME)),not(BOX(THEM(ME)))),BOXD2(THEM(^D)))` | never (≤ 54) | never (≤ 54) | never (≤ 54) | never (≤ 54) |
| `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 11 [T = 11, 6] | 11 [T = 11, 6] | 11 [T = 11, 6] | 11 [T = 11, 6] |
| `BOX(THEM(ME))` | 4 [T = 3] | 4 [T = 3] | 4 [T = 3] | 4 [T = 3] |
| `BOX1(THEM(ME))` | 4 [T = 4] | 4 [T = 4] | 4 [T = 4] | 4 [T = 4] |
| `BOX(THEM(THEM))` | 4 [T = 3] | 4 [T = 3] | 4 [T = 3] | 4 [T = 3] |
| `BOX1(THEM(THEM))` | 4 [T = 4] | 4 [T = 4] | 4 [T = 4] | 4 [T = 4] |
| `C` | 4 [T = ] | 4 [T = ] | 4 [T = ] | 4 [T = ] |
| `D` | never (≤ 54) | never (≤ 54) | never (≤ 54) | never (≤ 54) |

Gödel sentences re-armed (strictly invading a free-arm victim in the family table), max over b: K/0: 0; K/1: 0; K+4m/0: 0; K+4m/1: 0

Soundness over all sweep cells: 0 violations / 38235 checked formulas.

## 3. Cross-budget catalogue at n = 8 under K+4m (b ∈ [4, 16])

1218 genotypes, 546 self-cooperators in 1 component(s), 0 closed. Plays changed against K's published cross-budget blocks: 4_16: 126 (`BOX(THEM(ME))` vs `BOX(THEM(^C))` 0→1; `BOX(THEM(ME))` vs `or(BOX(THEM(ME)),BOX(THEM(THEM)))` 0→1; `BOX(THEM(ME))` vs `or(BOX(THEM(ME)),BOXD(THEM(ME)))` 0→1; `BOX(THEM(ME))` vs `or(BOX(THEM(ME)),BOXD(THEM(THEM)))` 0→1; `BOX(THEM(ME))` vs `or(BOX(THEM(ME)),BOX1(THEM(ME)))` 0→1; `BOX(THEM(ME))` vs `or(BOX(THEM(ME)),BOX1(THEM(THEM)))` 0→1); 16_4: 248 (`BOX(THEM(ME))` vs `BOX1(THEM(ME))` 0→1; `BOX(THEM(ME))` vs `BOX(THEM(^BOX(THEM(THEM))))` 0→1; `BOX(THEM(ME))` vs `BOX1(THEM(^BOX(THEM(ME))))` 0→1; `BOX(THEM(ME))` vs `BOX1(THEM(^BOX1(THEM(ME))))` 0→1; `BOX(THEM(^BOX(THEM(ME))))` vs `BOX1(THEM(ME))` 0→1; `BOX(THEM(^BOX(THEM(ME))))` vs `BOX(THEM(^BOX(THEM(THEM))))` 0→1).

## 4. The lim_N chain at n = 8 (PD, w = 0.3)

| arm | P(C,C) N = 10³ | 10⁴ | 3·10⁴ | π(all-D) 3·10⁴ | top state (π) 3·10⁴ | top exit 10³ / 10⁴ / 3·10⁴ | exit slope | strict share | ALLC share | entry N·ρ 10³ / 10⁴ / 3·10⁴ | classes | terminal / indeterminate / cut |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K b=16 | 0.3920 | 0.6710 | 0.7909 | 0.209 | `BOX(THEM(ME))` (0.173) | 4.85e-04 / 4.85e-05 / 1.62e-05 | -1.00 | 0.000 | 0.96 | 13.6 / 43.5 / 75.5 | 476 | 1 / 0 / 1e-08 |
| free | 0.3707 | 0.6172 | 0.7246 | 0.275 | `BOX(THEM(ME))` (0.226) | 4.85e-04 / 4.85e-05 / 1.62e-05 | -1.00 | 0.000 | 0.96 | 13.6 / 43.5 / 75.5 | 471 | 1 / 0 / 3e-08 |
| K b=54 | 0.3920 | 0.6709 | 0.7911 | 0.209 | `BOX(THEM(ME))` (0.174) | 4.85e-04 / 4.85e-05 / 1.62e-05 | -1.00 | 0.000 | 0.96 | 13.6 / 43.5 / 75.5 | 255 | 1 / 0 / 1e-08 |
| K4m b=54 g=0 | 0.3920 | 0.6709 | 0.7911 | 0.209 | `BOX(THEM(ME))` (0.174) | 4.85e-04 / 4.85e-05 / 1.62e-05 | -1.00 | 0.000 | 0.96 | 13.6 / 43.5 / 75.5 | 255 | 1 / 0 / 1e-08 |
| K4m b=16 g=0 | 0.3920 | 0.6710 | 0.7909 | 0.209 | `BOX(THEM(ME))` (0.173) | 4.85e-04 / 4.85e-05 / 1.62e-05 | -1.00 | 0.000 | 0.96 | 13.6 / 43.5 / 75.5 | 474 | 1 / 0 / 1e-08 |
| K4m b=16 g=1 | — | 0.6710 | — | 0.329 | `BOX(THEM(ME))` (0.157) | 4.85e-05 | — | 0.000 | 0.96 | 43.5 | 474 | 1 / 0 / 3e-08 |
| K b=16 g=1 | — | 0.6710 | — | 0.329 | `BOX(THEM(ME))` (0.157) | 4.85e-05 | — | 0.000 | 0.96 | 43.5 | 476 | 1 / 0 / 3e-08 |

- K b=16, support at 3·10⁴: mono {D:1} 0.209, mono {BOX(THEM(ME)):1} 0.173, mono {BOX1(THEM(ME)):1} 0.171, mono {and(BOX(THEM(ME)),BOXD1(THEM(^D))):1} 0.148, mono {BOX(THEM(THEM)):1} 0.147, mono {BOX1(THEM(THEM)):1} 0.138, mono {and(BOX(THEM(ME)),BOX1(THEM(^C))):1} 0.003, mono {BOX(THEM(^BOX1(THEM(ME)))):1} 0.002
- free, support at 3·10⁴: mono {D:1} 0.275, mono {BOX(THEM(ME)):1} 0.226, mono {BOX1(THEM(ME)):1} 0.225, mono {BOX(THEM(THEM)):1} 0.171, mono {and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):1} 0.053, mono {and(BOX1(THEM(ME)),not(BOX(THEM(THEM)))):1} 0.026, mono {and(BOX(THEM(ME)),BOXD1(THEM(^D))):1} 0.008, mono {BOX1(THEM(THEM)):1} 0.005
- K b=54, support at 3·10⁴: mono {D:1} 0.209, mono {BOX(THEM(ME)):1} 0.174, mono {BOX1(THEM(ME)):1} 0.173, mono {and(BOX(THEM(ME)),BOXD1(THEM(^D))):1} 0.149, mono {BOX(THEM(THEM)):1} 0.147, mono {BOX1(THEM(THEM)):1} 0.141, mono {BOX(THEM(^BOX1(THEM(ME)))):1} 0.002, mono {BOX(THEM(^BOX(THEM(THEM)))):1} 0.001
- K4m b=54 g=0, support at 3·10⁴: mono {D:1} 0.209, mono {BOX(THEM(ME)):1} 0.174, mono {BOX1(THEM(ME)):1} 0.173, mono {and(BOX(THEM(ME)),BOXD1(THEM(^D))):1} 0.149, mono {BOX(THEM(THEM)):1} 0.147, mono {BOX1(THEM(THEM)):1} 0.141, mono {BOX(THEM(^BOX1(THEM(ME)))):1} 0.002, mono {BOX(THEM(^BOX(THEM(THEM)))):1} 0.001
- K4m b=16 g=0, support at 3·10⁴: mono {D:1} 0.209, mono {BOX(THEM(ME)):1} 0.173, mono {BOX1(THEM(ME)):1} 0.171, mono {and(BOX(THEM(ME)),BOXD1(THEM(^D))):1} 0.148, mono {BOX(THEM(THEM)):1} 0.147, mono {BOX1(THEM(THEM)):1} 0.138, mono {and(BOX(THEM(ME)),BOX1(THEM(^C))):1} 0.003, mono {BOX(THEM(^BOX1(THEM(ME)))):1} 0.001

- K b=16, top `BOX(THEM(ME))` exits at 10⁴: `C` 4.7e-05 N·ρ 1.00 Δ 0/0/0; `BOX1(THEM(ME))` 5.1e-07 N·ρ 1.00 Δ 0/0/0; `BOX(THEM(THEM))` 5.0e-07 N·ρ 1.00 Δ 0/0/0
- free, top `BOX(THEM(ME))` exits at 10⁴: `C` 4.7e-05 N·ρ 1.00 Δ 0/0/0; `BOX1(THEM(ME))` 5.1e-07 N·ρ 1.00 Δ 0/0/0; `BOX(THEM(THEM))` 5.1e-07 N·ρ 1.00 Δ 0/0/0
- K b=54, top `BOX1(THEM(ME))` exits at 10⁴: `C` 4.7e-05 N·ρ 1.00 Δ 0/0/0; `BOX(THEM(ME))` 5.1e-07 N·ρ 1.00 Δ 0/0/0; `BOX1(THEM(THEM))` 5.1e-07 N·ρ 1.00 Δ 0/0/0
- K4m b=54 g=0, top `BOX1(THEM(ME))` exits at 10⁴: `C` 4.7e-05 N·ρ 1.00 Δ 0/0/0; `BOX(THEM(ME))` 5.1e-07 N·ρ 1.00 Δ 0/0/0; `BOX1(THEM(THEM))` 5.1e-07 N·ρ 1.00 Δ 0/0/0
- K4m b=16 g=0, top `BOX(THEM(ME))` exits at 10⁴: `C` 4.7e-05 N·ρ 1.00 Δ 0/0/0; `BOX1(THEM(ME))` 5.1e-07 N·ρ 1.00 Δ 0/0/0; `BOX(THEM(THEM))` 5.0e-07 N·ρ 1.00 Δ 0/0/0
- K4m b=16 g=1, top `BOX(THEM(ME))` exits at 10⁴: `C` 4.7e-05 N·ρ 1.00 Δ 0/0/0; `BOX1(THEM(ME))` 5.1e-07 N·ρ 1.00 Δ 0/0/0; `BOX(THEM(THEM))` 5.0e-07 N·ρ 1.00 Δ 0/0/0
- K b=16 g=1, top `BOX(THEM(ME))` exits at 10⁴: `C` 4.7e-05 N·ρ 1.00 Δ 0/0/0; `BOX1(THEM(ME))` 5.1e-07 N·ρ 1.00 Δ 0/0/0; `BOX(THEM(THEM))` 5.0e-07 N·ρ 1.00 Δ 0/0/0

## 5. The frozen classifier

C_spec (primary) and C_pair (secondary) as frozen in commit 6001721; positive = disarmed (invasion gone). Pair level is primary.

| n | label | classifier | level | TP | FP | FN | TN | precision | recall |
|---|---|---|---|---|---|---|---|---|---|
| 8 | K@16 | flag_spec | pair | 31 | 0 | 43 | 334 | 1.00 | 0.42 |
| 8 | K@16 | flag_spec | class | 16 | 0 | 21 | 52 | 1.00 | 0.43 |
| 8 | K@16 | flag_pair | pair | 48 | 0 | 26 | 334 | 1.00 | 0.65 |
| 8 | K@16 | flag_pair | class | 23 | 0 | 14 | 52 | 1.00 | 0.62 |
| 8 | K@16 | spec.flagG | pair | 24 | 0 | 50 | 334 | 1.00 | 0.32 |
| 8 | K@16 | spec.flagC | pair | 15 | 0 | 59 | 334 | 1.00 | 0.20 |
| 8 | K4m@16 | flag_spec | pair | 31 | 0 | 43 | 334 | 1.00 | 0.42 |
| 8 | K4m@16 | flag_spec | class | 16 | 0 | 21 | 52 | 1.00 | 0.43 |
| 8 | K4m@16 | flag_pair | pair | 48 | 0 | 26 | 334 | 1.00 | 0.65 |
| 8 | K4m@16 | flag_pair | class | 23 | 0 | 14 | 52 | 1.00 | 0.62 |
| 8 | K4m@16 | spec.flagG | pair | 24 | 0 | 50 | 334 | 1.00 | 0.32 |
| 8 | K4m@16 | spec.flagC | pair | 15 | 0 | 59 | 334 | 1.00 | 0.20 |

n = 8: 408 eligible pairs; 272 without a proof of the invader's play at level ≤ 2; 0 uncertified.

| 6 | K@16 | flag_spec | pair | 1 | 0 | 2 | 20 | 1.00 | 0.33 |
| 6 | K@16 | flag_spec | class | 1 | 0 | 2 | 10 | 1.00 | 0.33 |
| 6 | K@16 | flag_pair | pair | 2 | 0 | 1 | 20 | 1.00 | 0.67 |
| 6 | K@16 | flag_pair | class | 2 | 0 | 1 | 10 | 1.00 | 0.67 |
| 6 | K@16 | spec.flagG | pair | 1 | 0 | 2 | 20 | 1.00 | 0.33 |
| 6 | K@16 | spec.flagC | pair | 0 | 0 | 3 | 20 | — | 0.00 |
| 6 | K4m@16 | flag_spec | pair | 1 | 0 | 2 | 20 | 1.00 | 0.33 |
| 6 | K4m@16 | flag_spec | class | 1 | 0 | 2 | 10 | 1.00 | 0.33 |
| 6 | K4m@16 | flag_pair | pair | 2 | 0 | 1 | 20 | 1.00 | 0.67 |
| 6 | K4m@16 | flag_pair | class | 2 | 0 | 1 | 10 | 1.00 | 0.67 |
| 6 | K4m@16 | spec.flagG | pair | 1 | 0 | 2 | 20 | 1.00 | 0.33 |
| 6 | K4m@16 | spec.flagC | pair | 0 | 0 | 3 | 20 | — | 0.00 |

n = 6: 23 eligible pairs; 18 without a proof of the invader's play at level ≤ 2; 0 uncertified.

Post-hoc variants (declared after seeing the frozen result; descriptive only): maxlev6|K@16|flag_spec: {'tp': 31, 'fp': 21, 'fn': 43, 'tn': 313, 'precision': 0.5961538461538461, 'recall': 0.4189189189189189, 'n': 408}; maxlev6|K@16|flag_pair: {'tp': 48, 'fp': 21, 'fn': 26, 'tn': 313, 'precision': 0.6956521739130435, 'recall': 0.6486486486486487, 'n': 408}; maxlev6|K4m@16|flag_spec: {'tp': 31, 'fp': 21, 'fn': 43, 'tn': 313, 'precision': 0.5961538461538461, 'recall': 0.4189189189189189, 'n': 408}; maxlev6|K4m@16|flag_pair: {'tp': 48, 'fp': 21, 'fn': 26, 'tn': 313, 'precision': 0.6956521739130435, 'recall': 0.6486486486486487, 'n': 408}; maxlev6|no_root: 0

**Misclassified and true-positive pairs, label K16** (FN: disarmed, not flagged; FP: flagged, not disarmed; TP: both). Lost atoms: GL-true atoms of z vs x, x vs z, x vs x that are K-false at b = 16, with GL length L and the first budget ≤ 2L + 10 at which K proves them (structural if none). Alternative: minimal size of a GL derivation of z's play with no used trigger, searched to twice the minimum.

- FN: 43 pairs; lost atoms structural in 43, some finite-budget in 0, no lost GL-true atom in 0; untriggered derivation within 2× in 35 (for an FN the minimal derivation is itself untriggered; the 8 without one have no proof at level ≤ 2).
- TP: 31 pairs; lost atoms structural in 31, some finite-budget in 0, no lost GL-true atom in 0; untriggered derivation within 2× in 6.

  - FN `BOX(THEM(^not(BOX(THEM(ME)))))` vs `BOX(THEM(^BOX1(THEM(THEM))))`: min [11, 3], untriggered [11, 3]; lost xz L=12 structural (≤ 34)
  - FN `BOX1(THEM(^not(BOX(THEM(ME)))))` vs `BOX(THEM(^BOX1(THEM(THEM))))`: min [14, 3], untriggered [14, 3]; lost xz L=13 structural (≤ 36)
  - FN `BOX(THEM(^not(BOX(THEM(THEM)))))` vs `BOX(THEM(^BOX1(THEM(THEM))))`: min [11, 3], untriggered [11, 3]; lost xz L=12 structural (≤ 34)
  - FN `BOX1(THEM(^not(BOX(THEM(THEM)))))` vs `BOX(THEM(^BOX1(THEM(THEM))))`: min [14, 3], untriggered [14, 3]; lost xz L=13 structural (≤ 36)
  - FN `BOX(THEM(^not(BOX(THEM(^D)))))` vs `BOX(THEM(^BOX1(THEM(THEM))))`: min [11, 3], untriggered [11, 3]; lost xz L=13 structural (≤ 36)
  - FN `BOX(THEM(^not(BOX(THEM(^C)))))` vs `BOX(THEM(^BOX1(THEM(THEM))))`: min [11, 3], untriggered [11, 3]; lost xz L=13 structural (≤ 36)
  - FN `BOX1(THEM(^not(BOX(THEM(^D)))))` vs `BOX(THEM(^BOX1(THEM(THEM))))`: min [14, 3], untriggered [14, 3]; lost xz L=14 structural (≤ 38)
  - FN `BOX1(THEM(^not(BOX(THEM(^C)))))` vs `BOX(THEM(^BOX1(THEM(THEM))))`: min [14, 3], untriggered [14, 3]; lost xz L=14 structural (≤ 38)
  - FN `BOX(THEM(^not(BOX(THEM(ME)))))` vs `BOX1(THEM(^BOX1(THEM(THEM))))`: min None, untriggered None; lost xz L=13 structural (≤ 36)
  - FN `BOX(THEM(^not(BOX(THEM(THEM)))))` vs `BOX1(THEM(^BOX1(THEM(THEM))))`: min None, untriggered None; lost xz L=13 structural (≤ 36)
  - FN `BOX1(THEM(^not(BOX(THEM(ME)))))` vs `BOX1(THEM(^BOX1(THEM(THEM))))`: min None, untriggered None; lost xz L=14 structural (≤ 38)
  - FN `BOX1(THEM(^not(BOX(THEM(THEM)))))` vs `BOX1(THEM(^BOX1(THEM(THEM))))`: min None, untriggered None; lost xz L=14 structural (≤ 38)
  - FN `BOX(THEM(^not(BOX(THEM(^D)))))` vs `BOX1(THEM(^BOX1(THEM(THEM))))`: min None, untriggered None; lost xz L=14 structural (≤ 38)
  - FN `BOX1(THEM(^not(BOX(THEM(^D)))))` vs `BOX1(THEM(^BOX1(THEM(THEM))))`: min None, untriggered None; lost xz L=15 structural (≤ 40)
  - FN `not(BOX(THEM(THEM)))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [6, 1], untriggered [6, 1]; lost xz L=8 structural (≤ 26)
  - FN `BOX(THEM(^not(BOX(THEM(^C)))))` vs `BOX1(THEM(^BOX1(THEM(THEM))))`: min None, untriggered None; lost xz L=14 structural (≤ 38)
  - FN `BOX1(THEM(^not(BOX(THEM(^C)))))` vs `BOX1(THEM(^BOX1(THEM(THEM))))`: min None, untriggered None; lost xz L=15 structural (≤ 40)
  - FN `not(BOX(THEM(^BOX(THEM(ME)))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [8, 2], untriggered [8, 2]; lost xz L=9 structural (≤ 28)
  - FN `not(BOX(THEM(^C)))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [8, 2], untriggered [8, 2]; lost xz L=9 structural (≤ 28)
  - FN `not(BOX(THEM(^BOX(THEM(THEM)))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [8, 2], untriggered [8, 2]; lost xz L=9 structural (≤ 28)
  - FN `not(or(BOX(THEM(ME)),BOX(THEM(THEM))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [7, 1], untriggered [7, 1]; lost zx L=18 structural (≤ 46), xz L=15 structural (≤ 40)
  - FN `not(BOX(THEM(^BOX(THEM(^C)))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [12, 4], untriggered [12, 4]; lost xz L=9 structural (≤ 28)
  - FN `not(BOX(THEM(^BOX1(THEM(^C)))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [14, 4], untriggered [14, 4]; lost xz L=9 structural (≤ 28)
  - FN `BOX(THEM(^not(BOXD(THEM(ME)))))` vs `BOX(THEM(^BOX1(THEM(ME))))`: min [11, 3], untriggered [11, 3]; lost xz L=11 structural (≤ 32)
  - FN `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [11, 2], untriggered [11, 2]; lost zx L=15 structural (≤ 40), zx L=14 structural (≤ 38), xz L=22 structural (≤ 54)
  - FN `BOX(THEM(^not(BOXD(THEM(THEM)))))` vs `BOX(THEM(^BOX1(THEM(ME))))`: min [11, 3], untriggered [11, 3]; lost xz L=13 structural (≤ 36)
  - FN `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [7, 1], untriggered [7, 1]; lost zx L=15 structural (≤ 40), xz L=22 structural (≤ 54)
  - FN `BOX1(THEM(^not(BOXD(THEM(THEM)))))` vs `BOX(THEM(^BOX1(THEM(ME))))`: min [14, 3], untriggered [14, 3]; lost xz L=14 structural (≤ 38)
  - FN `BOX1(THEM(^not(BOXD(THEM(ME)))))` vs `BOX(THEM(^BOX1(THEM(ME))))`: min [14, 3], untriggered [14, 3]; lost xz L=13 structural (≤ 36)
  - FN `BOX(THEM(^not(BOXD(THEM(^C)))))` vs `BOX(THEM(^BOX1(THEM(ME))))`: min [11, 3], untriggered [11, 3]; lost xz L=13 structural (≤ 36)
  - FN `BOX(THEM(^not(BOXD(THEM(^D)))))` vs `BOX(THEM(^BOX1(THEM(ME))))`: min [11, 3], untriggered [11, 3]; lost xz L=13 structural (≤ 36)
  - FN `not(BOX(THEM(THEM)))` vs `BOX1(THEM(THEM))`: min [7, 2], untriggered [7, 2]; lost xz L=8 structural (≤ 26)
  - FN `not(BOX(THEM(^C)))` vs `BOX1(THEM(THEM))`: min [8, 2], untriggered [8, 2]; lost xz L=9 structural (≤ 28)
  - FN `BOX1(THEM(^not(BOXD(THEM(^C)))))` vs `BOX(THEM(^BOX1(THEM(ME))))`: min [14, 3], untriggered [14, 3]; lost xz L=14 structural (≤ 38)
  - FN `BOX1(THEM(^not(BOXD(THEM(^D)))))` vs `BOX(THEM(^BOX1(THEM(ME))))`: min [14, 3], untriggered [14, 3]; lost xz L=14 structural (≤ 38)
  - FN `not(BOX(THEM(^BOX(THEM(ME)))))` vs `BOX1(THEM(THEM))`: min [10, 3], untriggered [10, 3]; lost xz L=9 structural (≤ 28)
  - FN `not(BOX(THEM(^BOX(THEM(THEM)))))` vs `BOX1(THEM(THEM))`: min [10, 3], untriggered [10, 3]; lost xz L=9 structural (≤ 28)
  - FN `not(BOX(THEM(^BOX1(THEM(THEM)))))` vs `BOX1(THEM(THEM))`: min [7, 2], untriggered [7, 2]; lost xz L=9 structural (≤ 28)
  - FN `not(or(BOX(THEM(ME)),BOX(THEM(THEM))))` vs `BOX1(THEM(THEM))`: min [8, 2], untriggered [8, 2]; lost zx L=17 structural (≤ 44), xz L=15 structural (≤ 40)
  - FN `not(BOX(THEM(^BOX1(THEM(^C)))))` vs `BOX1(THEM(THEM))`: min [14, 4], untriggered [14, 4]; lost xz L=9 structural (≤ 28)
  - FN `not(BOX(THEM(^BOX(THEM(^C)))))` vs `BOX1(THEM(THEM))`: min [12, 4], untriggered [12, 4]; lost xz L=9 structural (≤ 28)
  - FN `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` vs `BOX1(THEM(THEM))`: min [10, 2], untriggered [10, 2]; lost zx L=14 structural (≤ 38), zx L=13 structural (≤ 36), xz L=22 structural (≤ 54)
  - FN `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))` vs `BOX1(THEM(THEM))`: min [8, 2], untriggered [8, 2]; lost zx L=14 structural (≤ 38), xz L=22 structural (≤ 54)
  - TP `BOX1(THEM(^not(BOX(THEM(ME)))))` vs `and(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [14, 2], untriggered None; lost xz L=13 structural (≤ 36), xz L=14 structural (≤ 38)
  - TP `BOX1(THEM(^not(BOX(THEM(THEM)))))` vs `and(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [14, 2], untriggered None; lost xz L=13 structural (≤ 36), xz L=14 structural (≤ 38)
  - TP `not(BOX(THEM(ME)))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [14, 3], untriggered None; lost zx L=11 structural (≤ 32), xz L=8 structural (≤ 26)
  - TP `BOX1(THEM(^not(BOX(THEM(^C)))))` vs `and(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [15, 3], untriggered None; lost xz L=14 structural (≤ 38), xz L=15 structural (≤ 40)
  - TP `not(BOX(THEM(^BOX1(THEM(THEM)))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [9, 2], untriggered [10, 3]; lost xz L=9 structural (≤ 28)
  - TP `not(BOX(THEM(^BOX1(THEM(ME)))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [9, 2], untriggered [10, 3]; lost xz L=9 structural (≤ 28)
  - TP `BOX1(THEM(^not(BOX(THEM(^D)))))` vs `and(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [15, 3], untriggered None; lost xz L=14 structural (≤ 38), xz L=15 structural (≤ 40)
  - TP `not(and(BOX(THEM(ME)),BOX(THEM(THEM))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [22, 4], untriggered None; lost zx L=14 structural (≤ 38), xz L=11 structural (≤ 32)
  - TP `not(and(BOX(THEM(ME)),BOX1(THEM(THEM))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [23, 4], untriggered None; lost zx L=14 structural (≤ 38), xz L=11 structural (≤ 32)
  - TP `not(and(BOX(THEM(ME)),BOX1(THEM(ME))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [34, 6], untriggered None; lost zx L=14 structural (≤ 38), zx L=15 structural (≤ 40), xz L=11 structural (≤ 32)
  - TP `not(and(BOX(THEM(THEM)),BOX1(THEM(THEM))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [12, 2], untriggered [15, 3]; lost xz L=11 structural (≤ 32)
  - TP `not(and(BOX(THEM(THEM)),BOX1(THEM(ME))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [23, 4], untriggered None; lost zx L=15 structural (≤ 40), xz L=11 structural (≤ 32)
  - TP `not(BOX(THEM(^not(BOX(THEM(THEM))))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [14, 3], untriggered None; lost zx L=11 structural (≤ 32), xz L=9 structural (≤ 28)
  - TP `not(BOX(THEM(^not(BOX(THEM(ME))))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [14, 3], untriggered None; lost zx L=11 structural (≤ 32), xz L=9 structural (≤ 28)
  - TP `not(BOX(THEM(ME)))` vs `BOX1(THEM(THEM))`: min [13, 3], untriggered None; lost zx L=10 structural (≤ 30), xz L=8 structural (≤ 26)
  - TP `not(BOX(THEM(^BOX1(THEM(ME)))))` vs `BOX1(THEM(THEM))`: min [8, 2], untriggered [9, 2]; lost xz L=9 structural (≤ 28)
  - TP `not(and(BOX(THEM(ME)),BOX(THEM(THEM))))` vs `BOX1(THEM(THEM))`: min [22, 5], untriggered None; lost zx L=13 structural (≤ 36), xz L=11 structural (≤ 32)
  - TP `and(BOX1(THEM(THEM)),not(BOX(THEM(THEM))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [7, 1], untriggered [7, 1]; lost xz L=22 structural (≤ 54)
  - TP `not(and(BOX(THEM(ME)),BOX1(THEM(ME))))` vs `BOX1(THEM(THEM))`: min [32, 6], untriggered None; lost zx L=13 structural (≤ 36), zx L=14 structural (≤ 38), xz L=11 structural (≤ 32)
  - TP `not(and(BOX(THEM(THEM)),BOX1(THEM(ME))))` vs `BOX1(THEM(THEM))`: min [23, 5], untriggered None; lost zx L=14 structural (≤ 38), xz L=11 structural (≤ 32)
  - TP `not(and(BOX(THEM(ME)),BOX1(THEM(THEM))))` vs `BOX1(THEM(THEM))`: min [21, 4], untriggered None; lost zx L=13 structural (≤ 36), xz L=11 structural (≤ 32)
  - TP `and(BOX1(THEM(THEM)),not(BOX(THEM(ME))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: min [18, 3], untriggered None; lost zx L=14 structural (≤ 38), xz L=22 structural (≤ 54)
  - TP `not(and(BOX(THEM(THEM)),BOX1(THEM(THEM))))` vs `BOX1(THEM(THEM))`: min [12, 3], untriggered None; lost xz L=11 structural (≤ 32)
  - TP `not(BOX(THEM(^not(BOX(THEM(THEM))))))` vs `BOX1(THEM(THEM))`: min [13, 3], untriggered None; lost zx L=10 structural (≤ 30), xz L=9 structural (≤ 28)
  - TP `not(BOX(THEM(^not(BOX(THEM(ME))))))` vs `BOX1(THEM(THEM))`: min [13, 3], untriggered None; lost zx L=10 structural (≤ 30), xz L=9 structural (≤ 28)
  - TP `BOX1(THEM(^not(BOX(THEM(ME)))))` vs `BOX(THEM(THEM))`: min [13, 2], untriggered None; lost xz L=13 structural (≤ 36)
  - TP `and(BOX1(THEM(THEM)),not(BOX(THEM(THEM))))` vs `BOX1(THEM(THEM))`: min [6, 1], untriggered [8, 2]; lost xz L=22 structural (≤ 54)
  - TP `BOX1(THEM(^not(BOX(THEM(THEM)))))` vs `BOX(THEM(THEM))`: min [13, 2], untriggered None; lost xz L=13 structural (≤ 36)
  - TP `and(BOX1(THEM(THEM)),not(BOX(THEM(ME))))` vs `BOX1(THEM(THEM))`: min [17, 3], untriggered None; lost zx L=13 structural (≤ 36), xz L=22 structural (≤ 54)
  - TP `BOX1(THEM(^not(BOX(THEM(^D)))))` vs `BOX(THEM(THEM))`: min [14, 3], untriggered None; lost xz L=14 structural (≤ 38)
  - TP `BOX1(THEM(^not(BOX(THEM(^C)))))` vs `BOX(THEM(THEM))`: min [14, 3], untriggered None; lost xz L=14 structural (≤ 38)

## 6. Part C: matched table interventions (n = 8, N = 10⁴, b = 16)

| arm | P(C,C) | − free | − K | − K+4m | top state |
|---|---|---|---|---|---|
| free | 0.6172 | +0.0000 | -0.0537 | -0.0537 |  |
| K b=16 | 0.6710 | +0.0537 | +0.0000 | -0.0000 |  |
| K4m b=16 | 0.6710 | +0.0537 | +0.0000 | +0.0000 |  |
| C(iii) K + restored exploiters | 0.6710 | +0.0537 | -0.0000 | -0.0000 | `BOX(THEM(ME))` |
| C(i) free minus C_spec-flagged | 0.6384 | +0.0212 | -0.0326 | -0.0326 | `BOX(THEM(ME))` |
| C(ii) K + restored cooperators | 0.6710 | +0.0537 | +0.0000 | -0.0000 | `BOX(THEM(ME))` |

Recovered share of the K − free gap by (i): 0.394 (gap 0.0537). Flagged classes deleted: 16 (μ 0.0013).

## 7. Lottery

K+4m b = 16, (100, 64), mN = 1, 20 paired seeds: efficient 20/20 (unresolved 0).

