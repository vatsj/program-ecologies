# Queue 73 drafts for the RE (RESULTS, REJECTED, THEORY, NOTATION)

Source: `runs/pair-worth-n.md` / `.json` (all tables), `predictions/2026-11-03-pair-worth-n.md`, `notes/pair-worth-n.md`. Branch `worktree-agent-a4dc6762bd84f2b1b`. All 900 jobs ran, nothing cut.

## 1. RESULTS draft: "The pair-worth easy case along N: constants stop coordinating, readers start"

**Question and design (reminder).** Queue 72 left the RS's easy-case conjecture (G1/3: every island in the core, every core point appearing) failed at N = 100 in the registered
arm C+B* (bids on all 28 grand splits): core 0.25 of islands against 0.53 for constants, and bids did not improve with dose. At N = 200-400 the exploratory rows showed bids at
0.80-0.85. Two readings: H_supply (bids coordinate only when three slots hold a bid on the same split; expected same-split triples T = 28 (dN/28)^3 = 0.16 / 1.3 / 10 at
N = 100 / 200 / 400) and H_N (selection against drift). Queue 73 reran the easy case at N = 100-800 (I = 64, mN = 1 and 0, annealed tail Lambda = 10, w = 0.3), with C+B*, C+B,
C+G (grand constants), a new flexible bid F (grand if the others' grand demands are feasible, else the exclusion handshakes; seeded with the same marginals as B*), C+F4, C+F-
(F without handshakes), fixed-count inoculation C+B*_k (exactly k copies per slot on one split per island), a dose panel, ten invasion assays and a longer chase. Founders
and tails shared across arms; 40 runs (20-59) for C, C+B*, C+G at N = 200 and 400, 20 runs for new cells, 60 at N = 100, 10 at N = 800. 33 kernel core-hours.

**Static supply (before any run).** The grand coalition is never scarce: constants alone supply 2,600 efficient grand triples per island at N = 100 and every island has a compatible efficient
support at founding. What differs is the *named* supply: same-split B* triples 0.16 / 1.3 / 10 / 82 (N = 100-800, d = 0.05) against 73 / 585 / 4,700 / 37,000 feasible F or G triples.

**Core share, Lambda = 10, mN = 1, d = 0.05** (runs: N = 100 0-59; N = 200, 400 20-59 for C, C+B*, C+G, 20-39 otherwise; N = 800 20-29):

| arm | N = 100 | 200 | 400 | 800 |
|---|---|---|---|---|
| C | 0.53 | 0.76 | 0.37 | 0.23 |
| C+B* | 0.25 | 0.58 | 0.94 | 1.00 |
| C+B (19 core splits) | 0.17 | 0.90 | 1.00 | - |
| C+G | 0.65 | 0.90 | 0.66 | 0.53 |
| C+F | 0.82 | 1.00 | 1.00 | - |
| C+F4 / C+F- | - / 0.65 | 1.00 / 1.00 | - | - |

Findings.
1. **Constants coordinate worse as N grows past 200, readers better.** C falls 0.76 -> 0.37 -> 0.23 and C+G 0.90 -> 0.66 -> 0.53 from N = 200 to 800 (the rest of the islands sit
   on pair outcomes: weak drift keeps pairs); C+B* rises 0.25 -> 0.58 -> 0.94 -> 1.00 and C+B, C+F reach 1.00 at N = 400. Paired at N = 400: C+B* - C = +0.57 [0.47, 0.67],
   C+G - C+B* = -0.29 [-0.40, -0.17]: the reading premium is positive and large at N = 400, the opposite of N = 100 (C+G - C+B* = +0.40) and N = 200 (+0.33).
2. **The RS's conjecture, core clause, is met at N >= 400 at mN = 1** (C+B 1.00, C+F 1.00 over 20 runs; C+B* 0.94 [0.87, 1.00] over 40, 1.00 at N = 800), **the coverage clause is not**:
   at mN = 0 every arm ends mostly null (C+B* N = 400: core 0.06, null 0.50, pair 0.41); 16 of 19 core points have a simultaneous upper bound below 1/76. The reading advantage is a migration phenomenon.
3. **It is not local supply.** The share of islands with a named same-split support at founding (0.13 / 0.59 / 0.99 at N = 100 / 200 / 400 for d = 0.05; the T-based count was 0.116 / 0.537 / 0.982) predicts nothing:
   establishment (a grand state held 25 generations) is 0.65 with a named support against 0.63 without at N = 200, mN = 1; ROC area of the support's minimum abundance or count of compatible triples is
   0.50 at mN = 0. At matched T = 0.16 the cells separate by N, not T: C+B* d = 0.0125 at N = 400 is +0.29 [0.06, 0.53] over C (0.68), at N = 200 d = 0.025 -0.06 (0.70 vs 0.76), at N = 100 d = 0.05 -0.28.
   Fixed-count inoculation says the same: k = 4 copies per slot give core 0.20 / 0.63 / 0.77 at N = 100 / 200 / 400 (k = 1: 0.20 / 0.57 / 0.46), +0.57 from N = 100 to 400 with the count held fixed. At mN = 0 inoculation gives 0.02-0.06.
   So the gain is H_N plus migration (selection against drift, with islands that establish seeding the others), with bids as the program that exploits it; the T arithmetic of the spec is not the lever.
4. **Dose is non-monotone at N = 400** (core 0.68 / 1.00 / 0.85 / 0.70 at d = 0.0125 / 0.05 / 0.15 / 0.5; d = 0.5 minus d = 0.05 -0.30 [-0.50, -0.10], pair share +0.30) and flat-to-falling at N = 100 and 200.
5. **F is a constant with a fallback only at N >= 200**: C+F - C+G = +0.17 [0.02, 0.32] at N = 100, +0.10 at N = 200, +0.32 [0.19, 0.47] at N = 400 (a reading premium, not equality). Against equality bids C+F - C+B* = +0.57 at N = 100.
   The fallback matters at N = 100 only (C+F - C+F- = +0.30 [0.05, 0.55]; identical at N = 200). F4 = F. No efficient-dominated islands in any arm (0.00): the 9 non-core splits are never held.
6. **Exits are neutral-looking drift at the assay level and finite-schedule fast at the raw level.** Assays (ε-free): a matching grand constant fixes at 1/N in every B*^3 cell (|z| <= 1.35 over 9 cells; one G^3 identity cell at |z| = 2.24 of 18 neutral G^3 cells);
   pair offers and B*(sigma') entrants have N p <= 0.035 (exact) and 0.10 (MC). Raw tail exit hazards per in-core island-generation: C+G 7.5e-5 / 3.0e-5 / 5.1e-6 at N = 100 / 200 / 400 (log-log slope -1.94 [-2.17, -1.74]), C+B* 2.2e-4 / 2.7e-5
   at N = 200 / 400 (slope -3.0 [-5.5, -1.1]): steeper than 1/N (a selection effect of the larger population), and almost all events at mN = 1 trace to migrant lineages (e.g. C+B* N = 400: 1,484 migrant, 843 resident, 2 arrival exits).
7. **Who holds the core.** C+G islands: grand constants in all three majorities (100%). C+B* N = 400: 2,411 core islands, readers in the majority in 1,923; at d = 0.5 reading majorities everywhere (896/896). C+F: F in 2,011 of 3,840 majority slots at N = 400.
8. Longer chase (60 N, 5 runs at N = 400): C+B* 1.00 -> 1.00; C+G 0.46 -> 0.51 (same founders): no relaxation to the core for constants. N = 800 (10 runs): C 0.23, C+B* 1.00, C+G 0.53.
9. Tail-free reference (Lambda = 0) agrees at N = 100 and 200 (C+F 0.86, C+B* 0.24, C 0.57, C+G 0.75 at N = 100): the result is not a property of the tail.

**Verdicts.** held: RE2, RE7, argon (i), sol (iii) (both arms' intervals exclude -1), sol (v) (trivially: support has no predictive value), E3. failed: RS conjecture (core clause met, coverage clause fails), RE1 (d = 0.0125 clause: +0.29 over C), RE3, RE4, RE5,
RE6, RE8, argon (ii), sol (iv), E1 (N = 200: 0.594 against 0.537, by 0.057), E2. No prediction was unscored.

Caveats. Core share at mN = 1 is run-level (islands synchronize; consensus 0.03-0.28 at N >= 400 for C and C+B*, so runs are not at one outcome but islands within a run are correlated). N = 800 has 10 runs. Exit and entry rates are finite-schedule rates with the 200-generation ancestry window. F and G are the same-feasibility coordination families the stored machinery can express; the free modal oracle (Löb) makes F's grand line sound by construction (V6), so "reading beats constants" is a statement about the DSL arm.

## 2. REJECTED draft (added 2026-11-04; queue 73)

- **RE 1 ("supply, not N or dose, is the lever for bids").** Failed on the d = 0.0125 clause: C+B* at N = 400 with T = 0.16 is 0.68, +0.29 [0.06, 0.53] over C (the H_N reading, argon's metapopulation reading); the N = 400 d = 0.05 clause (0.94, +0.57) and the N = 200 d = 0.025 clause (-0.06) held. Founding named support does not predict establishment (ROC 0.50, establishment 0.65 vs 0.63).
- **RE 3 ("constants coordinate better than bids at every N; C+G >= 0.8 at N = 400").** Failed: C+G - C+B* = +0.33 at N = 200, -0.29 [-0.40, -0.17] at N = 400 (a reading premium); C+G is 0.66 at N = 400.
- **RE 4 ("a flexible bid is a constant with a fallback").** Failed: |C+F - C+G| = 0.17 at N = 100 and 0.32 at N = 400 (> 0.15); C+F - C+B* = +0.57 at N = 100 held.
- **RE 5 ("local supply is enough without migration at N = 400").** Failed: mN = 0 core 0.06 (C+B*) and 0.12 (C+G), null 0.50 / 0.64.
- **RE 6 ("no arm reaches core >= 0.95 at N = 400").** Failed: C+B and C+F 1.00 [1.00, 1.00] over 20 runs; C+B* 0.94.
- **RE 8 ("fixed count isolates N").** Failed: C+B*_4 core 0.77 at N = 400 against 0.20 at N = 100 (+0.57): the count does not carry the gain, N does (H_N).
- **The RS's conjecture re-scored.** Core clause met at N >= 400 by readers (C+B, C+F 1.00; C+B* 0.94); coverage clause failed (mN = 0: 16 of 19 core points below 1/76, total core share 0.065).
- **gemini-4-argon (ii)** (C+F has an efficient-dominated share > 0.15): failed, 0.00 at every N. **gpt-6.1-sol (iv)** (C+F differs from C+G through a pair excess): failed, C+F has fewer pair islands than C+G at N = 100 (-0.19) and N = 200 (-0.10), and the F- control shows the fallback *raises* the core at N = 100.
- **Engineer E1** (named support share within 0.05 of the Poisson count 0.116 / 0.537 / 0.982): failed at N = 200 (0.594), by 0.057 (N = 100 0.129, N = 400 0.991 within). **E2** (the pair fallback does not change the core share): failed at N = 100 (+0.30 [0.05, 0.55]), 0.00 at N = 200.
- **Spec's design points.** "T = 28 n_sigma^3 as the supply that bids need" (design 1(c), the matched-T cells): rejected as the operative quantity; the grand coalition is never scarce (static) and founding support is non-predictive. "Lambda in {0, 10} at N = 400 and 800": not run (Lambda = 10 only; the cost table assumed it).
- Nothing re-opened by this run that REJECTED already holds: the queue-72 entry on the easy-case conjecture is re-opened at N >= 400 (and was allowed to be: larger N and a menu-free bid).

## 3. THEORY draft (only if the RE accepts the moves)

- The easy-case selection claim should read: on the grid, with the free modal oracle and migration (mN = 1, I = 64), reading programs (equality bids, flexible bids) put every island in the core proper from N >= 400, constants do not (core falls with N past 200); without migration the ecology does not reach the core at any N tested (core <= 0.12, mostly null or pair); coverage of all 19 core points at mN = 0 fails. The operative variable is N with migration, not the founding supply of a named coordination device.
- "Reading never beats constants in the easy case" (queue 72's reading) is a small-N finding (N <= 200); at N >= 400 it reverses (+0.29 to +0.57 paired).

## 4. NOTATION draft

- **Pair-worth along N (queue 73):** **F(sigma_i; c)** — flexible grand bid: plays (ALL, sigma_i) at level 0 iff some feasible pair (a, b), a + b <= 1 - sigma_i, of the others' grand demands is provable, then the level-1 exclusion handshakes, then c; **F4** — F with sigma_i <= 4/6 (renormalized weights); **F- (`CFm`)** — F without handshakes; **B\*_k (`CBk1`, `CBk4`)** — fixed-count inoculation: C founders plus exactly k copies per slot of B\*(sigma; c) on one split per island; **T** — expected same-split triples on an island at founding, 28 n_sigma^3; **n_sigma** — delta N / 28, expected bids per slot per split; **supply** — the founding statistics: any compatible grand support, named-only efficient support, minimum abundance of the best support, count of compatible triples; **establishment** — first generation an island's modal outcome is a grand kind held 25 generations; **finite-schedule transition rate** — debounced core entries/exits per island-generation at risk, tail and chase separately, ancestry by what reached 10% of a slot in the previous 200 generations (arrival / migrant / resident); **assay (cell F)** — single-island, no-tail, no-migration fixation probabilities of one introduced program, MC and exact. Codes in the repo: `CF`, `CF4`, `CFm`, `CBk1`, `CBk4`.
