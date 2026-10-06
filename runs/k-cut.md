# K with cut and distribution under a box (K_c): runs, 2026-10-05/06

Spec `specs/2026-10-05-k-cut.md`; predictions `predictions/2026-10-05-k-cut.md` (commit 818ec64, before any counted
table); notes `notes/k-cut.md`; code `src/k_cut.py` and the `cut` option of `src/bounded_k.py`; tests
`tests/test_k_cut.py` (5 pass); machine-readable `runs/k-cut.json`, per-cell files in `runs/k-cut/`.

## 0. What ran, and what did not

Ran, in the spec's priority order: notes §1 (definition, soundness, Theorem D0, Lemma C, extension-model certificates);
the option in its own commit with the K tables reproduced exactly when off; tables at n = 6 (b = 4, 16, 40) and n = 8
(b = 4, 8, 16, 24, 54); structural certificates for the named family at every b from 4 to 200 (four arms); family
sweeps (K, K_c every b 4–54; K_c + 4m, K and K_c at g = 1, K_c + 4m at g = 1 on b ∈ {4, 8, 10, 11, 12, 16, 24, 32}, 53–54);
seeded log-domain chains for K, K_c (b = 16, 54), free, and the factorial cells; the 2×2 graft; the lottery; and the
exploratory long-guard arm (K_c4, guard at 2b + 8) on the family at b ∈ {4, 8, 12, 14, 16} with a long-guard 2×2 graft.

Not run / changed: (i) the **full K_c closure at n = 8** exhausted memory (≈ 50 GB compressed at b = 54 before it was
killed); the n = 8 tables are **targeted** (K closure + certificates + K_c search on the uncertified misses only), exact
by Corollary T and identical to the full closure at n = 6 (all three budgets). (ii) **General contextual cut is not
searched**; cut is searched in Lemma C's form (lemma cuts on Dist hypotheses' contents). Searched sizes are upper
bounds on K_c's; structural claims come from certificates, which cover contextual cut at every size. (iii) The
**cross-budget catalogue {4, 16}** under K_c was not computed (a full cross-budget K_c closure); the leak claim rests on
fixed-b leak tests and K at n = 8's proposition (each fixed-b graph is an induced subgraph of the catalogue's and the
suckering pairs survive). (iv) Long-guard arm: no full n = 8 table (a K_c4 closure at cap 2b + 8 does not fit); family
sweep stopped at b = 16; its chain is a graft of family plays into K's table (descriptive). (v) 3-type deep-state
seeding (C(476, 3) candidates) did not finish in 45 CPU-minutes; chains seed every monomorphic and 2-type deep state
(0 found) and expand by relative inflow to 10⁻¹².

**Incident.** A mistyped `pkill -f "multiprocessing.spawn" -P 1` (BSD pkill read `-P 1` as extra patterns) killed every
process whose command line contained "multiprocessing.spawn" or "1" at ≈ 00:00 on 10-06, including this run's b = 8
table (rerun) and **workers of sibling experiments** (e.g. `src/mixed_budgets.py`'s pool was respawned). Siblings
running at that time should be checked.

## 1. Proved (notes §1)

- **Theorem D0.** Contextual cut does not give distribution under a box: □_a P[C,C], □_c(P[C,C] → ⊥) ⊢ □_d ⊥ is not
  derivable in K + Cut (+ 4m) at any d (extension model). So Dist is a primitive rule; its soundness needs cut.
- **K_c = K + Cut + UnfId + Dist_k (k ≤ 3)**, Dist: from A_1..A_k ⊢ B infer Γ, □_{a_i}A_i ⊢ □_d B, Δ when
  d ≥ s + Σa_i + k. **Lemma C** (witness composition by k cuts); **Lemma W** survives cut with UnfId; **soundness** by
  size induction (cut: classical; Dist: Lemma C, no induction hypothesis; JLöb with cut/Dist inside premises unchanged).
  The spec's a + c + 1 is a + c + 5 for atomic A, B (a + c when ⊢ A → B ends in →R).
- **Theorem E / Lemmas E1, E2.** Extension models certify structural failure at every size. At guard offsets 0 and 1 no
  rule of this class can reach □_{b+g}⊥ from a budget-b hypothesis (outputs land at ≥ b + 2); without a 4-rule no
  margin helps P\* (Lemma E2). **Corollary P:** P\*, P2, P12b, P\*1b (and PB2 at g = 0; at g = 1 without 4m) and the
  Gödel/Con-sentence readings are underivable in K_c at every b. P\* and the Gödel fakers need the guard at ≥ 2b + 7 /
  2b + 6 and Dist⁺ (the bounded K4 rule).

## 2. Option off, hand checks, tests

`runs/k-cut/repro.json`: n = 8 b = 4, 8, 16 and n = 6 b = 4, 16, 40 identical to the published K tables (0 differing
plays, 0 soundness violations). Hand example (A = P[FB_5, D], B = P[D, D]): □_a A ∧ □_c(A → B) → □_d B derivable iff
d ≥ a + c + 5, size 6, one Dist node; never in K. Tests: distribution boundary, Theorem D0's model, K ⊆ K_c (sizes
never larger; K's extracted derivations pass the K_c checker), named certificates at b = 16, 30 (g = 0, 1; with and
without 4m), the n = 6 b = 16 table with the checker, Lemma C replay and the prune on every sequent of every extracted
derivation (GL-valid).

## 3. Tables

| n | b | K_c plays ≠ K | toward free | μ² of changes | GL-true atom contents: K-derived / certified structural / uncertified (searched) / newly derived by K_c | provable fraction (atoms, μ) | soundness | checker (goals, Dist nodes, witnesses replayed) |
|---|---|---|---|---|---|---|---|---|
| 6 | 4 | 0 | — | 0 | 72 / 252 / 367 / 0 | 0.123 / 0.973 | 0 / 169 | 72, 0, 0 |
| 6 | 16, 40 | 0 | — | 0 | 439 / 252 / 0 / 0 | 0.694 / 0.992 | 0 / 1,184 | 439, 94–98, 47–49 |
| 8 | 4 | 0 | — | 0 | 589 / 31,491 / 27,902 / 0 | 0.042 / 0.970 | 0 / 1,479 | — |
| 8 | 8 | 0 | — | 0 | 6,140 / 31,491 / 22,351 / 0 | 0.341 / 0.989 | 0 / 12,373 | — |
| 8 | 16 | 197 | 195 | 2.3·10⁻⁸ | 24,469 / 31,491 / 4,022 / 322 | 0.587 / 0.992 | 0 / 12,422 | 322, 657, 328 |
| 8 | 24 | 182 | 179 | 5.4·10⁻⁹ | 27,964 / 31,491 / 527 / 218 | 0.618 / 0.992 | 0 / 3,367 | 218, 568, 282 |
| 8 | 54 | **2** | 2 | 2.1·10⁻¹¹ | 28,487 / 31,491 / 4 / **4** | 0.6206 / 0.9917 | 0 / 20 | 4, 24, 8 |

(GL-true contents at n = 8: 59,982; atoms 143,269. K's b = 54 provable fraction is 88,904 atoms; K_c's 88,908.)
At b = 16, 195 of the 197 changed plays are K's own plays at b = 32 and 54 (acceleration); at b = 24, 179 of 182.
Leak test: 0 closed components at every fixed b (self-cooperators 261 / 286 / 287 at b = 4 / 16 / 24, 54).
Behavioural classes: b = 16 476 → 478 (two splits, μ 7·10⁻⁵); b = 54 255 → 253 (one merge of the BOXD readers, μ 0.010,
caused by the two changed plays). **Restored cooperators (self-cooperating in K_c, not K): none at any b. Restored
exploiters against the fixed panel: none. Against supported self-cooperators:** b = 16, `and(BOX(THEM(ME)),BOX1(THEM(THEM)))`
and `and(BOX(THEM(THEM)),BOX1(THEM(ME)))` now strictly invade `BOX(THEM(^BOX(THEM(THEM))))` (the probe reader's
cooperation is accelerated, theirs is not); b = 24, `and(BOX1(THEM(ME)),BOX(THEM(^C)))` the same reader.

**The b = 54 restoration** (structural for K: not derived at b = 54, 80, 120, 200): x = `and(BOXD(THEM(ME)),BOXD1(THEM(ME)))`
vs y = `not(and(BOX(THEM(ME)),BOX1(THEM(ME))))` flips to x C, y D. Minimal K_c derivation (size 17): JLöb over
S = {¬P[y,x], P[x,y]} at b′ = 17; inside, □_17 P[x,y] ⊢ □_54(¬□_54⊥ → P[x,y]) by Dist from P ⊢ ¬□⊥ → P (2 sequents)
— weakening of a box's content, which K's BoxEq lacks. Distribution restores monotonicity under a box, not Con
reasoning.

## 4. Named family: b\* and structural status

| program | K b\* [witness] | K_c | K_c + 4m | K, g = 1 | K_c, g = 1 | K_c + 4m, g = 1 | certificate b = 4…200 |
|---|---|---|---|---|---|---|---|
| FairBot, `BOX1(THEM(ME))`, `BOX(THEM(THEM))`, `BOX1(THEM(THEM))` | ≤ 4 [3, 4, 3, 4] | same | same | same | same | same | — |
| PrudentBot | 11 [11, 6] | 11 [11, 6] | 11 | 11 | 11 | 11 | — |
| PB2 | never | never | never | never | never | **11** | structural except K_c + 4m at g = 1 |
| P\*, P2, P12b, P\*1b | never | never | never | never | never | never | structural, 197/197 budgets, all four arms |

Gödel (21) and Con-set (16) classes strictly invading a fixed-panel victim or one of their free-arm victims: **0 in
every counted and g ≤ 1 arm at every swept b** (K_c: every b 4–54). Soundness: 0 violations in 29,383 (K_c sweep) /
24,084 (K) checked formulas; 297 named witnesses independently checked, 0 mismatches.

## 5. Chains (ε → 0, PD, w = 0.3, n = 8; seeded log-domain GTH)

| arm | N = 10³ | N = 10⁴ | N = 3·10⁴ | π(all-D) 3·10⁴ | top state | top exit (N·exit, kind) | entry D → top (N·ρ) |
|---|---|---|---|---|---|---|---|
| free | — | 0.61725 | — | — | FairBot 0.182 (10⁴) | 0.485, neutral → C | 43.5 |
| K b = 16 | 0.392043 | 0.670960 | 0.790923 | 0.209 | FairBot 0.173 | 0.485, neutral → C | 13.6 / 43.5 / 75.5 |
| K_c b = 16 | 0.392046 | 0.670962 | 0.790923 | 0.209 | FairBot 0.173 | same | same |
| K b = 54 | — | 0.670936 | — | — | `BOX1(THEM(ME))` 0.158 | same | 43.5 |
| K_c b = 54 | 0.392048 | 0.670936 | 0.791120 | 0.209 | `BOX1(THEM(ME))` 0.158 (10⁴) | same | same |

K_c − K: +2.5·10⁻⁶ / +1.9·10⁻⁶ / +7·10⁻⁷ at b = 16; 0 to 9 digits at b = 54. Exit per event × N = 0.485 at every N
(slope −1, neutral drift into ALLC, 0.96 of exit mass to C); entry N·ρ ∝ N^0.5. Support at 3·10⁴ (K_c b = 16): D 0.209,
FairBot 0.173, `BOX1(THEM(ME))` 0.171, PrudentBot 0.148, `BOX(THEM(THEM))` 0.147, `BOX1(THEM(THEM))` 0.138. **Audit:**
residual ‖πQ‖₁/‖π·out‖₁ ≤ 1.8·10⁻¹⁴; seeded and lazy linear chains agree to ≤ 2.5·10⁻⁶ (the seeded chain expands
67–440 states the lazy one does not, carrying π ≤ 2.4·10⁻⁶; the lazy one has none the seeded one lacks); no 2-type deep
state exists (so twin drift has nothing to act on); dominant exit and entry fixation probabilities recomputed by an
independent mpmath Moran sum agree with the chain to |Δρ| ≤ 10⁻¹⁸. Published lazy numbers reproduced (free 0.617, K
0.392 / 0.671 / 0.791).

## 6. The 2×2 restoration design (b = 16, N = 10⁴) and the guard × calculus factorial

Frozen sets: R_coop = ∅, R_expl (fixed panel) = ∅. All four hybrid tables are K's table (checked entrywise): P(C,C)
0.670960 in every cell; both main effects and the interaction are 0. **The design is degenerate.**
Factorial at b = 16, N = 10⁴: K g = 0 0.670960, K g = 1 0.670960, K_c g = 0 0.670962, K_c g = 1 0.670962 (g = 1 changes
no play of L_8 in either calculus); interaction 0.000000.

## 7. Lottery (ε = 0, (N, I) = (100, 64), mN = 1, 20 paired seeds)

K_c b = 16: 20/20 efficient, Wilson [0.84, 1.00], 0 censored (as K and free in "K at n = 8").

## 8. Exploratory: the long-guard arm (K_c4, guard read at 2b + 8)

Family sweep (named + panel + 37 disarmed classes + their free-arm victims; 0 soundness violations in every cell):

| b | P\* | P2 | PB2 | PrudentBot | P12b, P\*1b | Gödel classes invading a free-arm victim (of 21) | Con-set classes (of 16) | Gödel / Con invading the fixed panel |
|---|---|---|---|---|---|---|---|---|
| 4, 8 | D | D | D | D | D | 0, 1 | 0 | 0 / 0 |
| 12 | **C [12]** | D | C [12, 7] | C | D | 8 | 3 | 0 / 0 |
| 14 | C | **C [13]** | C | C | D | 13 | 7 | 0 / 2 |
| 16 | C | C | C | C | D | **15** | **12** | 0 / 3 |

K at the same long guard (K_L, no Dist⁺) restores nothing at b = 4–16: the margin alone does nothing; distribution with
the 4-rule under the margin does it. The fixed panel (FairBot, `BOX1(THEM(ME))`, PrudentBot, P\*, `BOX(THEM(THEM))`)
contains none of the Gödel sentences' free-arm victims (`BOX1(THEM(THEM))`, `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`),
so panel counts understate the restoration.

**Long-guard 2×2 (b = 16, N = 10⁴; descriptive graft).** Donor: the long-guard family table at b = 16 restricted to the
49 family members in L_8 (256 plays differ from K's), grafted into K's n = 8 table (family vs non-family plays stay K's).
R_coop = 7 classes (P\*, its `THEM`-variants `and(BOX1(…)),not(BOX(THEM(THEM))))` etc., and three `BOX1(THEM(^not(…)))`
readers); R_expl = 27 classes (Gödel sentences and P\*-type conjunctions invading `BOX1(THEM(THEM))` and
`or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`, probe readers).

| cell | P(C,C) | π(all-D) | top state | top exit |
|---|---|---|---|---|
| neither (K) | 0.6710 | 0.329 | FairBot 0.157 | 0.485/N neutral → C |
| cooperators only | **0.8177** | 0.182 | **P\* 0.220** (and its THEM-variant 0.218) | 0.0015/N, neutral → Gödel sentences |
| exploiters only | 0.5927 | 0.407 | FairBot 0.193 | 0.485/N |
| both | 0.6318 | 0.368 | FairBot 0.174 (P\* 0.047) | 0.485/N |
| all 256 family plays | 0.6318 | 0.368 | same | same |

Main effects: cooperators +0.147, exploiters −0.078; **interaction −0.108** (|interaction| = 2.8 × the smaller main
effect). With its fakers, completeness lands between K (0.671) and free (0.617); without them it would beat K by 0.15,
with P\* nearly absorbing (exit 0.0015/N, all neutral into Gödel sentences).
