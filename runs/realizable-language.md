# Run: the realizable language L_T, milestone 1 (2026-10-06)

Spec `specs/2026-10-06-realizable-language.md` (reviewed by gpt-6.1-sol); predictions
`predictions/2026-10-06-realizable-language.md` (frozen terms, committed before any code); notes
`notes/realizable-language.md` (§1, the gate, committed before any table; §2, the hand-checked FairBot space). Code:
`src/lt.py` (language, evaluator, K_T, prover, soundness checker), `src/lt_check.py` (independent evaluator, witness
replay, brute-force prover), `src/lt_run.py` (driver, 3 workers), `src/lt_report.py` (tables), `tests/test_lt.py`.
Raw per-task JSON in `runs/realizable_language/`; summary JSON `runs/realizable-language.json`.

**What was run.** The eleven frozen programs (C, D, FB, FB1, PB, G, P\*, SF_k with k = b, SC, Vlet, Vwrap) at every
b ∈ {2, …, 64}: every ordered pair under primitive-assisted charging (prove = 1 step, K = 10⁶) and search-charged
charging (prove = W node expansions, charged to the global K and every enclosing sim fuel) at K ∈ {10⁴, 10⁵, 10⁶};
the same cells in the JLöb-disabled calculus K_T⁻; the FairBot copy/distinct-budget grid {4, 8, 16, 32}² in both
semantics plus the full {2..40}² under primitive-assisted charging; an SF k sweep {5, …, 1000} against itself and
FB_{16,32,64}; audits (soundness checker on every found box and every witness sequent, independent replay of every
witness, independent evaluator on every play trace, independent brute-force prover at b ≤ 8, Mem enlarged to the
whole root closure at b ∈ {16, 25, 32}).

**Implementation notes decided before any table.** (i) The search's lower-bound rule (notes §1.6): a failed
expansion stores the minimum over rule instances of their lower bounds; exact, changes only W. (ii) Timeout of a
prove call under search-charged charging ends the play (⊥) when the global counter is the first exhausted, or makes
the outermost exhausted sim return TO. **After the run** (notes §1.7 amended, marked): merges occur in root closures
(max 1, SF simulating PB and P\*); the completeness argument was rewritten (Lemma U) so as not to depend on them, and
the two empirical checks (brute force, Mem = whole closure) agree on every query.

**Realizability caveat.** The primitive-assisted arm runs the exhaustive search in the host and charges one step:
it is the idealization the calculus describes, not an internalized prover. The search-charged arm charges the
host search's node count to the program, which is the realizability test of that idealization, but the search
still runs in Python, not as an L_T term; milestone 3 (the prover as code) is what makes the budget the program's
own step count and the checker's source visible. Box truth is "a K_T derivation exists within b sequents", a
decidable syntactic fact for this finite catalogue; K_T is a sound bounded calculus for the evaluation of these
terms, not a bounded PA prover.

## 1. Self-cooperation thresholds (primitive-assisted)

b\* = first b ∈ {2..64} with (C, C) against a copy; "stable" = (C, C) at every larger b on the grid. Certified minimal size and Λ of the self-play formula at b\*; W = search work at b\*.

| program | b\* | stable | minimal size at b\* | Λ | W at b\* | certified lower bound if none |
|---|---|---|---|---|---|---|
| C | 2 | True | — | — | — |  |
| D | none ≤ 64 | — | — | — | — |  |
| FB | 8 | True | 8 | 1 | 378 |  |
| FB1 | 13 | True | 13 | 1 | 10560 |  |
| PB | 25 | True | 25 | 1 | 365656 |  |
| G | 2 | True | None | None | 5 |  |
| P* | none ≤ 64 | — | — | — | — | > 64 (refuted at every b ≤ 64) |
| SF | none ≤ 64 | — | — | — | — | > 64 (refuted at every b ≤ 64) |
| SC | 2 | True | — | — | — |  |
| Vlet | 9 | True | 9 | 1 | 765 |  |
| Vwrap | 11 | True | 11 | 1 | 3057 |  |

## 2. First b of mutual cooperation, every unordered pair (primitive-assisted)

Entry: first b with (C, C), "s" if stable above it; "—" none on the grid.

| | C | D | FB | FB1 | PB | G | P* | SF | SC | Vlet | Vwrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | 2s | — | 3s | 4s | — | 2 | — | 2s | 2s | 3s | 3s |
| D | — | — | — | — | — | — | — | — | — | — | — |
| FB | 3s | — | 8s | 20s | 29s | — | — | 14s | 6s | 13s | 15s |
| FB1 | 4s | — | 20s | 13s | — | — | — | 19s | 7s | 21s | 23s |
| PB | — | — | 29s | — | 25s | — | — | 32s | — | 31s | 35s |
| G | 2 | — | — | — | — | 2s | — | 5s | 2 | — | — |
| P* | — | — | — | — | — | — | — | — | — | — | — |
| SF | 2s | — | 14s | 19s | 32s | 5s | — | — | 5s | 15s | 17s |
| SC | 2s | — | 6s | 7s | — | 2 | — | 5s | 2s | 6s | 6s |
| Vlet | 3s | — | 13s | 21s | 31s | — | — | 15s | 6s | 9s | 15s |
| Vwrap | 3s | — | 15s | 23s | 35s | — | — | 17s | 6s | 15s | 11s |

### Play of the row program against the column program at b = 8 (primitive-assisted; ⊥ = timeout/other)

| row \ col | C | D | FB | FB1 | PB | G | P* | SF | SC | Vlet | Vwrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | C | C | C | C | C | C | C | C | C | C | C |
| D | D | D | D | D | D | D | D | D | D | D | D |
| FB | C | D | C | D | D | D | D | D | C | D | D |
| FB1 | C | D | D | D | D | D | D | D | C | D | D |
| PB | D | D | D | D | D | D | D | D | D | D | D |
| G | D | C | C | C | C | C | C | C | D | C | C |
| P* | D | D | D | D | D | D | D | D | D | D | D |
| SF | C | D | D | D | D | C | D | D | C | D | D |
| SC | C | C | C | C | C | C | C | C | C | C | C |
| Vlet | C | D | D | D | D | D | D | D | C | D | D |
| Vwrap | C | D | D | D | D | D | D | D | C | D | D |

### Play of the row program against the column program at b = 16 (primitive-assisted; ⊥ = timeout/other)

| row \ col | C | D | FB | FB1 | PB | G | P* | SF | SC | Vlet | Vwrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | C | C | C | C | C | C | C | C | C | C | C |
| D | D | D | D | D | D | D | D | D | D | D | D |
| FB | C | D | C | D | D | D | D | C | C | C | C |
| FB1 | C | D | D | C | D | D | D | D | C | D | D |
| PB | D | D | D | D | D | D | D | D | D | D | D |
| G | D | C | C | C | C | C | C | C | D | C | C |
| P* | D | D | D | D | D | D | D | D | D | D | D |
| SF | C | D | C | D | D | C | D | D | C | C | D |
| SC | C | C | C | C | C | C | C | C | C | C | C |
| Vlet | C | D | C | D | D | D | D | C | C | C | C |
| Vwrap | C | D | C | D | D | D | D | D | C | C | C |

### Play of the row program against the column program at b = 25 (primitive-assisted; ⊥ = timeout/other)

| row \ col | C | D | FB | FB1 | PB | G | P* | SF | SC | Vlet | Vwrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | C | C | C | C | C | C | C | C | C | C | C |
| D | D | D | D | D | D | D | D | D | D | D | D |
| FB | C | D | C | C | D | D | D | C | C | C | C |
| FB1 | C | D | C | C | D | D | D | C | C | C | C |
| PB | D | D | D | D | C | D | D | D | D | D | D |
| G | D | C | C | C | C | C | C | C | D | C | C |
| P* | D | D | D | D | D | D | D | D | D | D | D |
| SF | C | D | C | C | D | C | D | D | C | C | C |
| SC | C | C | C | C | C | C | C | C | C | C | C |
| Vlet | C | D | C | C | D | D | D | C | C | C | C |
| Vwrap | C | D | C | C | D | D | D | C | C | C | C |

### Play of the row program against the column program at b = 32 (primitive-assisted; ⊥ = timeout/other)

| row \ col | C | D | FB | FB1 | PB | G | P* | SF | SC | Vlet | Vwrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | C | C | C | C | C | C | C | C | C | C | C |
| D | D | D | D | D | D | D | D | D | D | D | D |
| FB | C | D | C | C | C | D | D | C | C | C | C |
| FB1 | C | D | C | C | D | D | D | C | C | C | C |
| PB | D | D | C | D | C | D | D | C | D | C | D |
| G | D | C | C | C | C | C | C | C | D | C | C |
| P* | D | D | D | D | D | D | D | D | D | D | D |
| SF | C | D | C | C | C | C | D | D | C | C | C |
| SC | C | C | C | C | C | C | C | C | C | C | C |
| Vlet | C | D | C | C | C | D | D | C | C | C | C |
| Vwrap | C | D | C | C | D | D | D | C | C | C | C |

### Play of the row program against the column program at b = 64 (primitive-assisted; ⊥ = timeout/other)

| row \ col | C | D | FB | FB1 | PB | G | P* | SF | SC | Vlet | Vwrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C | C | C | C | C | C | C | C | C | C | C | C |
| D | D | D | D | D | D | D | D | D | D | D | D |
| FB | C | D | C | C | C | D | D | C | C | C | C |
| FB1 | C | D | C | C | D | D | D | C | C | C | C |
| PB | D | D | C | D | C | D | D | C | D | C | C |
| G | D | C | C | C | C | C | C | C | D | C | C |
| P* | D | D | D | D | D | D | D | D | D | D | D |
| SF | C | D | C | C | C | C | D | D | C | C | C |
| SC | C | C | C | C | C | C | C | C | C | C | C |
| Vlet | C | D | C | C | C | D | D | C | C | C | C |
| Vwrap | C | D | C | C | C | D | D | C | C | C | C |

### Certified minimal derivation size (Λ) of each found box of the row program against the column program, b = 64

Entry per prove call in order (PB and P\* make two); "r" refuted; empty: no prove call.

| row \ col | C | D | FB | FB1 | PB | G | P* | SF | SC | Vlet | Vwrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C |  |  |  |  |  |  |  |  |  |  |  |
| D |  |  |  |  |  |  |  |  |  |  |  |
| FB | 3(0) | r | 8(1) | 20(1) | 29(1) | r | r | 14(1) | 6(0) | 13(1) | 15(1) |
| FB1 | 4(0) | r | 13(1) | 13(1) | r | r | r | 19(1) | 7(0) | 14(1) | 16(1) |
| PB | 3(0) / r | r | 29(1) / 9(0) | r | 25(1) / 9(0) | r | r | 32(1) / 10(0) | 6(0) / r | 31(1) / 10(0) | 35(1) / 12(0) |
| G | 3(0) | r | r | r | r | r | r | r | 6(0) | r | r |
| P* | 4(0) / 3(0) | r | r | r | r | r | r | r | 7(0) / 6(0) | r | r |
| SF |  |  | 14(1) | 19(1) | 32(1) / 10(0) | r | r |  |  | 15(1) | 17(1) |
| SC |  |  |  |  |  |  |  |  |  |  |  |
| Vlet | 3(0) | r | 12(1) | 21(1) | 30(1) | r | r | 15(1) | 6(0) | 9(1) | 15(1) |
| Vwrap | 3(0) | r | 13(1) | 23(1) | 33(1) | r | r | 17(1) | 6(0) | 14(1) | 11(1) |

## 3. Exploitation cells: the row program plays C, the column program plays D or ⊥

**prim:** C exploited by D (D) at 63 b, C exploited by FB (D) at 1 b, C exploited by FB1 (D) at 2 b, C exploited by G (D) at 62 b, C exploited by P* (D) at 63 b, C exploited by PB (D) at 63 b, C exploited by Vlet (D) at 1 b, C exploited by Vwrap (D) at 1 b, G exploited by D (D) at 63 b, G exploited by FB (D) at 63 b, G exploited by FB1 (D) at 63 b, G exploited by P* (D) at 63 b, G exploited by PB (D) at 63 b, G exploited by SF (D) at 3 b, G exploited by Vlet (D) at 63 b, G exploited by Vwrap (D) at 63 b, SC exploited by D (D) at 63 b, SC exploited by FB (D) at 4 b, SC exploited by FB1 (D) at 5 b, SC exploited by G (D) at 59 b, SC exploited by P* (D) at 63 b, SC exploited by PB (D) at 63 b, SC exploited by SF (D) at 3 b, SC exploited by Vlet (D) at 4 b, SC exploited by Vwrap (D) at 4 b.

**search_10000:** C exploited by D (D) at 63 b, C exploited by FB (D) at 1 b, C exploited by FB1 (D) at 2 b, C exploited by G (D) at 62 b, C exploited by P* (D) at 63 b, C exploited by PB (D) at 63 b, C exploited by Vlet (D) at 1 b, C exploited by Vwrap (D) at 1 b, G exploited by D (D) at 63 b, G exploited by FB (D) at 15 b, G exploited by FB1 (D) at 8 b, G exploited by P* (⊥) at 1 b, G exploited by P* (D) at 7 b, G exploited by PB (D) at 6 b, G exploited by SF (D) at 9 b, G exploited by Vlet (D) at 12 b, G exploited by Vwrap (D) at 9 b, SC exploited by D (D) at 63 b, SC exploited by FB (D) at 4 b, SC exploited by FB1 (D) at 5 b, SC exploited by G (D) at 59 b, SC exploited by P* (D) at 63 b, SC exploited by PB (D) at 63 b, SC exploited by SF (D) at 3 b, SC exploited by Vlet (D) at 4 b, SC exploited by Vwrap (D) at 4 b.

**search_100000:** C exploited by D (D) at 63 b, C exploited by FB (D) at 1 b, C exploited by FB1 (D) at 2 b, C exploited by G (D) at 62 b, C exploited by P* (D) at 63 b, C exploited by PB (D) at 63 b, C exploited by Vlet (D) at 1 b, C exploited by Vwrap (D) at 1 b, FB exploited by SF (D) at 51 b, FB1 exploited by Vwrap (⊥) at 42 b, G exploited by D (D) at 63 b, G exploited by FB (D) at 63 b, G exploited by FB1 (D) at 32 b, G exploited by P* (⊥) at 5 b, G exploited by P* (D) at 19 b, G exploited by PB (D) at 14 b, G exploited by SF (D) at 63 b, G exploited by Vlet (D) at 63 b, G exploited by Vwrap (D) at 63 b, SC exploited by D (D) at 63 b, SC exploited by FB (D) at 4 b, SC exploited by FB1 (D) at 5 b, SC exploited by G (D) at 59 b, SC exploited by P* (D) at 63 b, SC exploited by PB (D) at 63 b, SC exploited by SF (D) at 3 b, SC exploited by Vlet (D) at 4 b, SC exploited by Vwrap (D) at 4 b, Vlet exploited by SF (D) at 50 b, Vwrap exploited by SF (D) at 48 b.

**search_1000000:** C exploited by D (D) at 63 b, C exploited by FB (D) at 1 b, C exploited by FB1 (D) at 2 b, C exploited by G (D) at 62 b, C exploited by P* (D) at 63 b, C exploited by PB (D) at 63 b, C exploited by Vlet (D) at 1 b, C exploited by Vwrap (D) at 1 b, FB exploited by SF (D) at 51 b, FB1 exploited by SF (D) at 46 b, G exploited by D (D) at 63 b, G exploited by FB (D) at 63 b, G exploited by FB1 (D) at 63 b, G exploited by P* (D) at 63 b, G exploited by PB (D) at 63 b, G exploited by SF (D) at 63 b, G exploited by Vlet (D) at 63 b, G exploited by Vwrap (D) at 63 b, PB exploited by SF (D) at 33 b, SC exploited by D (D) at 63 b, SC exploited by FB (D) at 4 b, SC exploited by FB1 (D) at 5 b, SC exploited by G (D) at 59 b, SC exploited by P* (D) at 63 b, SC exploited by PB (D) at 63 b, SC exploited by SF (D) at 3 b, SC exploited by Vlet (D) at 4 b, SC exploited by Vwrap (D) at 4 b, Vlet exploited by SF (D) at 50 b, Vwrap exploited by SF (D) at 48 b.

Sound readers (FB, FB1, PB, Vlet, Vwrap) on the C side under primitive-assisted charging: 0 cells.


## 4. Prove outcomes: found / refuted / timeout (every prove call of every cell, all b)

| semantics | found | refuted | timeout | of which inside a sim | plays ⊥ |
|---|---|---|---|---|---|
| prim | 2649 | 3064 | 0 | 0 | 0 |
| search_10000 | 1233 | 1130 | 3144 | 416 | 2728 |
| search_100000 | 1854 | 1889 | 1764 | 416 | 1348 |
| search_1000000 | 2388 | 2735 | 557 | 416 | 141 |
| ctrl_prim | 962 | 4545 | 0 | 0 | 0 |
| ctrl_search_10000 | 962 | 4129 | 416 | 416 | 0 |
| ctrl_search_100000 | 962 | 4129 | 416 | 416 | 0 |
| ctrl_search_1000000 | 962 | 4129 | 416 | 416 | 0 |

## 5. Search work W and the K at which outcomes stabilize (search-charged)

Distinct prove queries: 2388 found, 2876 refuted. Max W of a found box: 861842 (b = 64, `plays(SF,PB,C)@64`). Max W of a refutation: 4211754 (b = 64, `(~[64]F -> plays(PB,P*,C))@64`). Found boxes with W > 10⁴ / 10⁵ / 10⁶: 982 / 361 / 0. Refutations with W > 10⁴ / 10⁵ / 10⁶: 1746 / 987 / 141.

| W band | found | refuted |
|---|---|---|
| [0, 100) | 493 | 219 |
| [100, 1000) | 582 | 513 |
| [1000, 10000) | 331 | 398 |
| [10000, 100000) | 621 | 759 |
| [100000, 1e+06) | 361 | 846 |
| [1e+06, 1e+09) | 0 | 141 |

Cells (all b, 7623) by the smallest tested K from which the search-charged play no longer changes: K = 10000: 5036, K = 100000: 1380, K = 1e+06: 1207. At K = 10⁶ the search-charged play equals the primitive-assisted play in 7194 cells and differs in 429.

Cells differing at K = 10⁶ (pair, prim → search, number of b): FB1|PB D→⊥ (32), P*|FB1 D→⊥ (7), P*|PB D→⊥ (46), P*|SF D→⊥ (3), PB|FB1 D→⊥ (29), PB|P* D→⊥ (24), SF|FB C→D (51), SF|FB1 C→D (46), SF|G C→D (60), SF|PB C→D (33), SF|Vlet C→D (50), SF|Vwrap C→D (48).


### Self-cooperation thresholds under search-charged charging

| program | b\* at K = 10000 | b\* at K = 100000 | b\* at K = 1e+06 |
|---|---|---|---|
| C | 2 | 2 | 2 |
| D | none | none | none |
| FB | 8 | 8 | 8 |
| FB1 | none | 13 | 13 |
| PB | none | none | 25 |
| G | 2 | 2 | 2 |
| P* | none | none | none |
| SF | none | none | none |
| SC | 2 | 2 | 2 |
| Vlet | 9 | 9 | 9 |
| Vwrap | 11 | 11 | 11 |

## 6. JLöb-disabled control K_T⁻ (every cell recomputed)

Mutual cooperation cells (unordered pairs, number of b): C–C (63), C–FB (62), C–FB1 (61), C–G (1), C–SC (63), C–SF (63), C–Vlet (62), C–Vwrap (62), FB–SC (59), FB1–SC (58), G–G (63), G–SC (4), G–SF (60), SC–SC (63), SC–SF (60), SC–Vlet (59), SC–Vwrap (59).

Mutual cooperation between two programs both outside {C, SC}: G–G (63), G–SF (60).

Cells where the control changes the primitive-assisted play (row vs column, full → control, number of b): FB vs FB C→D (57), FB vs FB1 C→D (45), FB vs PB C→D (36), FB vs SF C→D (51), FB vs Vlet C→D (52), FB vs Vwrap C→D (50), FB1 vs FB C→D (45), FB1 vs FB1 C→D (52), FB1 vs SF C→D (46), FB1 vs Vlet C→D (44), FB1 vs Vwrap C→D (42), PB vs FB C→D (36), PB vs PB C→D (40), PB vs SF C→D (33), PB vs Vlet C→D (34), PB vs Vwrap C→D (30), SF vs FB C→D (51), SF vs FB1 C→D (46), SF vs PB C→D (33), SF vs Vlet C→D (50), SF vs Vwrap C→D (48), Vlet vs FB C→D (52), Vlet vs FB1 C→D (44), Vlet vs PB C→D (34), Vlet vs SF C→D (50), Vlet vs Vlet C→D (56), Vlet vs Vwrap C→D (50), Vwrap vs FB C→D (50), Vwrap vs FB1 C→D (42), Vwrap vs PB C→D (30), Vwrap vs SF C→D (48), Vwrap vs Vlet C→D (50), Vwrap vs Vwrap C→D (54).


## 7. Audits

- Soundness checker: 4213 found boxes and 43491 witness sequents evaluated in the standard model (full calculus and control); **0 violations**.
- Independent replay (`src/lt_check.py`): 6327 witnesses, 68683 nodes, 43339 evaluation steps re-derived by the independent evaluator, 2504 JLöb instances; **0 failures**.
- Independent evaluator on every play trace (both charging semantics, every K, full calculus and control under primitive-assisted): 246045 steps; **0 disagreements**.
- Merges (states with two deterministic predecessors) in any root closure: max 2 (allowed by Lemma U, notes §1.7 as amended). Largest root closure 57 formulas. Searches stopped by the work limit 5·10⁷: 0.
- Independent brute-force prover (no lower bounds; members = whole closure) at b ∈ [2, 3, 4, 5, 6, 7, 8, 9]: 636 / 636 prove queries agree on found/refuted and the minimal size; control 636 / 636.
- Mem enlarged to every atom and box content of the root closure, b ∈ [16, 25, 32]: 248 / 248 prove queries agree.

## 8. FairBot budgets: copies vs distinct budgets

Primitive-assisted, then search-charged at K = 10⁴ / 10⁵ / 10⁶ (row FB_x, column FB_y; the row's play):

| x \ y | 4 | 8 | 16 | 32 |
|---|---|---|---|---|
| 4 | D / D D D | D / D D D | D / D D D | D / D D D |
| 8 | D / D D D | C / C C C | D / D D D | D / D D D |
| 16 | D / D D D | D / D D D | C / C C C | C / C C C |
| 32 | D / ⊥ D D | D / ⊥ D D | C / C C C | C / C C C |

Full grid {2..40}², primitive-assisted: cells violating "C iff (x = y ≥ 8) or (x ≠ y and min(x, y) ≥ 12)": 0; asymmetric cells: 0.

(C, not-C) cells on the {4, 8, 16, 32}² grid: none.


## 9. Simulation FairBot: k sweep

Row program's play: primitive-assisted / search-charged at K = 10⁴, 10⁵, 10⁶ (prove outcomes f/r/t).

| k | SF|SF | SF|FB16 | FB16|SF | SF|FB32 | FB32|SF | SF|FB64 | FB64|SF |
|---|---|---|---|---|---|---|---|
| 5 | D / D D D | C:f / D:t D:t D:t | C:f / ⊥:t C:f C:f | C:f / D:t D:t D:t | C:f / ⊥:t C:f C:f | C:f / D:t D:t D:t | C:f / ⊥:t C:f C:f |
| 10 | D / D D D | C:f / D:t D:t D:t | C:f / ⊥:t C:f C:f | C:f / D:t D:t D:t | C:f / ⊥:t C:f C:f | C:f / D:t D:t D:t | C:f / ⊥:t C:f C:f |
| 20 | D / D D D | C:f / D:t D:t D:t | C:f / ⊥:t C:f C:f | C:f / D:t D:t D:t | C:f / ⊥:t C:f C:f | C:f / D:t D:t D:t | C:f / ⊥:t C:f C:f |
| 64 | D / D D D | C:f / D:t D:t D:t | C:f / ⊥:t C:f C:f | C:f / D:t D:t D:t | C:f / ⊥:t C:f C:f | C:f / D:t D:t D:t | C:f / ⊥:t C:f C:f |
| 200 | D / D D D | C:f / D:t D:t D:t | C:f / ⊥:t C:f C:f | C:f / D:t D:t D:t | C:f / ⊥:t C:f C:f | C:f / D:t D:t D:t | C:f / ⊥:t C:f C:f |
| 1000 | D / D D D | C:f / D:t D:t D:t | C:f / ⊥:t C:f C:f | C:f / D:t D:t D:t | C:f / ⊥:t C:f C:f | C:f / D:t D:t D:t | C:f / ⊥:t C:f C:f |

## 10. Verdicts

| # | prediction | outcome |
|---|---|---|
| RE 1 | K_T sound, witness executable (every found box found by the search-charged arm within K = 10⁶), FB self-cooperates from a finite threshold with Λ = 1 | **held**: §1 proved (notes); 0 violations over 4,213 found boxes and 43,491 witness sequents; 6,327 witnesses replayed independently, 0 failures; max W of a found box 861,842 < 10⁶ (none above 10⁶); b\*(FB) = 8, Λ = 1. Caveat: inside a simulation the sim fuel, not K, is the binding budget (§9) |
| RE 2 | no (C, D) on the FairBot grid under completed searches; copies no higher than distinct budgets; min-rule guessed | **held**: no (C, not-C) cell on {4, 8, 16, 32}² in any semantics (one (D, ⊥) at K = 10⁴: FB_32's refutation of FB_4 times out); copies 8 < distinct 12; min-rule exact on all of {2..40}², symmetric. Between distinct *sources* the rule is a max of the two readers' proof sizes (FB–FB1 20, FB–PB 29), so source length enters, as the RE allowed |
| RE 3 | FB and FB1 defect on G, G cooperates; G's victim, if any, a level-1 reader; SF pair (D, D) or ⊥ at every k; P\* never self-cooperates | **partly**: FB, FB1, PB, Vlet, Vwrap defect on G at every b and G cooperates (suckered, not disarmed); SF–SF (D, D) at every k with no timeout; P\* defects on everything at every b ≤ 64. Falsifier not fired. The victim clause is not borne out: G's only victims are the unconditional cooperators C (62 b) and SC (59 b); the level-1 reader FB1 is not one |
| RE 4 | PB self-cooperates at a finite threshold, Λ ≤ 5, ≤ 8× FB's | **held**: b\*(PB) = 25, minimal size 25, Λ = 1; 3.1× FB's |
| RE 5 | SC exploited by G; FB may defect on SC while it cooperates; K_T⁻ shows no cooperation between conditional programs; harmless variants within +4 of FB's threshold | **failed, falsifier fired** (literal control clause): K_T⁻ has mutual cooperation FB–SC, FB1–SC, Vlet–SC, Vwrap–SC, SF–SC (proofs by evaluation of an extensional constant), G–G (63 b) and G–SF (60 b) (cooperation by refutation and by simulating a refuter); **no Löbian cooperation**: every prover–prover cell is (D, D) in K_T⁻. SC exploited by G at 59 b (held); FB defects on SC at b = 2–5 while SC cooperates (held). Variants: FB–Vlet 13 (+5), FB–Vwrap 15 (+7) over b\*(FB) = 8, so "+4" failed, but neither exceeds 2× = 16 |
| S1 | b\*(FB) = 8, Λ = 1, minimal size 8 | **held** |
| S2 | distinct FB budgets iff min ≥ 12, symmetric | **held** (0 violations, 0 asymmetric cells on {2..40}²) |
| S3 | b\*(FB1) = 13; b\*(PB) = 25 ± 3, Λ = 1; ratio ∈ [2.5, 4] | **held** (13; 25, Λ 1; 3.1) |
| S4 | G plays C against FB, FB1, PB, P\*, G, SF; D against SC from b = 6 and C from b = 3; P\* D against everything | **held** |
| S5 | SF–SF (D, D), no timeout; SF–FB mutual under primitive-assisted iff b ≥ 14 and k ≥ 5; under search-charged FB C, SF D | **held**: SF–FB from b = 14 (k = b) and from k = 5 in the sweep; under search-charged SF defects on FB at every b ≥ 14 and every k ≤ 10³ (the inner search, W = 16,356, exceeds the sim fuel), while FB cooperates (K ≥ 10⁵) |
| S6 | Vlet 9, Vwrap 11; FB–Vlet 13, FB–Vwrap 15, Vlet–Vwrap 16 ± 1 | **held** (9, 11, 13, 15, 15) |
| S7 | K_T⁻: no mutual cooperation between two programs outside {C, SC} | **failed, falsifier fired**: G–G and G–SF cooperate in K_T⁻ (I missed that a Gödel sentence cooperates on every refutation, including against itself and against a simulator of itself); no prover–prover cooperation |
| S8 | 0 violations, 0 evaluator disagreements, every witness replays | **held** (also: brute-force prover 636/636 and control 636/636 at b ≤ 9; Mem = whole closure 248/248 at b ∈ {16, 25, 32}) |
| S9 | every found box has W < 10⁴; some refutation needs W > 10⁴ | **failed, falsifier fired**: 982 found boxes have W > 10⁴ (361 above 10⁵); FB1 self-cooperates under search-charged charging only from K = 10⁵ and PB only at K = 10⁶. The second clause held (1,746 refutations above 10⁴; 141 above 10⁶) |
| S10 | SC C everywhere; PB defects on SC; FB cooperates with SC from b = 6 | **held** |

## 11. Reading

- **Critch's bounded Löb runs in our own Turing-complete evaluator.** FairBot written as a λ-term that calls a
  bounded prover for "my opponent plays C against me" cooperates with its copy from b = 8 (one JLöb, 8 sequents:
  three evaluation steps, the prove step's box obligation discharged by BoxEq from the Löb hypothesis), with distinct
  budgets iff min ≥ 12, symmetric, never exploited when searches complete. K's structure transfers exactly with the
  evaluation steps added to the costs (K: 3/4; here 8/12).
- **Soundness, not syntax, carries cooperation.** Distinct-source cooperators (a let-variant, a wrapper, FB1, PB,
  even a bounded simulator) cooperate with FairBot at thresholds set by the two proof sizes (13–35); the JLöb-disabled
  control kills every one of these and nothing else.
- **The Gödel sentence is suckered, and bounded Gödel II transfers.** No reader certifies G's cooperation, so every
  sound reader defects on G while G cooperates: G is the sucker, not a faker, and exploits only the unconditional
  cooperators C and SC. P\* never cooperates. PrudentBot never cooperates with the level-1 reader FB1: certifying that FB1
  punishes D needs distribution under a box, the Con-dependent loss of K again.
- **The idealization leaks exactly where a program simulates a prover.** Under search-charged charging a sound
  reader proves that SF cooperates (true of the idealized evaluation, where the inner prove costs one step) while the
  real SF cannot afford FairBot's inner search inside its fuel and defects: FB, FB1, PB, Vlet and Vwrap are exploited
  by SF at K = 10⁶ on 33–51 budgets. The calculus cannot charge searches inside sims (the charge would refer to
  itself, notes §1.6). This is what milestone 3 must face: with the prover as code, the simulated search costs real
  steps, and a reader's proof about a simulator must account for them.
- **Search cost is mostly refutation cost.** Found boxes need W ≤ 8.6·10⁵; refutations among prudent readers reach
  4.2·10⁶ and leave 141 plays ⊥ at K = 10⁶. FB is stable from K = 10⁴; FB1 needs 10⁵, PB 10⁶. A realizable prudent
  reader pays most of its budget proving that it should defect.
- *Realizability caveat.* The search runs in the host in both arms; search-charged charging bills the host's node
  count to the program. The programs cooperate by calling a primitive; milestone 3 replaces it by L_T code.
