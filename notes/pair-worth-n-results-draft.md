## The pair-worth easy case along N: with migration, reader arms reach the core on 0.94–1.00 of islands at N = 400–800 while constants fall back to pairs; without migration coordination is rare; and 98% of core islands sit on the seven core points where every share lies between 1/6 and 1/2 (2026-11-04)

Spec `specs/2026-11-03-pair-worth-n.md` (queue 73; the RS approved the run on 2026-11-03; reviewed by gemini-4-argon then gpt-6.1-sol, folded). Predictions `predictions/2026-11-03-pair-worth-n.md` were committed before any counted cell. They were not fully outcome-blind: one pipeline smoke run of C+F and C+B\*₄ (N = 100, run 0) and a smoke run of the assays preceded them and are disclosed there. The assays were rerun with fresh seeds after the file was committed. Notes are in `notes/pair-worth-n.md` (§3 lists every deviation). Report `runs/pair-worth-n.md` and `.json`; rows `runs/pair_worth_n/rows.jsonl.gz`; static numbers `runs/pair_worth_n/static.json`; assays `runs/pair_worth_n/assays.json`. The coverage supplement (RE, after the run) is `src/pair_worth_n_coverage.py` → `runs/pair_worth_n/coverage.json`. Run by a Sonnet subagent: all 900 jobs (2,200 records), nothing cut, 33 kernel core-hours.

*Question and design.* Queue 72 found the RS's easy-case conjecture failing at N = 100 in the arm registered for it. The game was G⅓ (pair worth ⅓, sixths). The conjecture: every island ends in the core, and every core point appears. Bids on all 28 grand splits (C+B\*) put 0.25 of islands in the core, constants 0.53, and grand constants that read no one (C+G) 0.80. The exploratory rows at N = 200 and 400 had bids at 0.80–0.85. Two readings were tested:
- H_supply: bids coordinate only when three slots hold a bid on the same split.
- H_N: selection against drift.

Queue 73 reran the easy case at N = 100–800. Design:
- I = 64, w = 0.3, annealed tail Λ = 10 (and Λ = 0 at N ≤ 200), mN ∈ {1, 0}, cut at 100·N generations plus a 20·N tail-free chase.
- Arms: C, C+B\*, C+B (19 core splits), C+G, and a new flexible bid F. F plays grand with share σ_i iff it can prove both others play grand with demands summing to at most 1 − σ_i. It reads at level 0, so three feasible F's play the grand coalition by Löb (V6, exhaustive, 0 mismatches). Then come the level-1 exclusion handshakes, then a constant. F is seeded with the same per-slot marginal as G and B\*.
- Controls: F₄ (own share ≤ 4/6), F⁻ (no handshakes), fixed-count inoculation C+B\*ₖ (exactly k bid copies per slot on one split per island), a dose panel, invasion assays and a longer chase.
- Founders and tails are shared across arms. Runs: 20–59 for C, C+B\*, C+G at N = 200 and 400 (40 runs); 20–39 for the other new cells there; 0–59 at N = 100; 20–29 at N = 800.

*Validations.* V1 and V2 reproduce stored queue-72 rows exactly. V6 (F against direct modal evaluation, 4.7·10⁶ triples, plus an independent chain on 9,811) has 0 mismatches and catches a mutated F. V7 (common random numbers) and V8 pass.

**1. Core share against N** (Λ = 10, mN = 1, δ = 0.05):

| arm | N = 100 | 200 | 400 | 800 |
|---|---|---|---|---|
| C | 0.53 | 0.76 | 0.37 | 0.23 |
| C+B\* | 0.25 | 0.58 | 0.94 | 1.00 |
| C+B (19 core splits) | 0.17 | 0.90 | 1.00 | – |
| C+G | 0.65 | 0.90 | 0.66 | 0.53 |
| C+F | 0.82 | 1.00 | 1.00 | – |

- Constants peak at N = 200 and then fall back onto pair outcomes: C's dominated-wasteful share is 0.63 at N = 400 and 0.77 at 800.
- Readers rise, reaching 1.00 at N = 400 (C+B, C+F, 20 runs each) and N = 800 (C+B\*, 10 runs).
- Paired contrasts at N = 400: C+B\* − C = +0.57 [0.47, 0.67] and C+G − C+B\* = −0.29 [−0.39, −0.17]. At N = 100 and 200 the sign is the other way (+0.40 and +0.33).
- C+F beats C+G at every N: +0.17 [0.02, 0.32], +0.10, +0.32 [0.19, 0.47].
- These are endpoint shares on finite schedules, not limits. At N = 400, C+B\* is at 0.94 [0.87, 1.00]; C+F is already at 1.00 at N = 200.
- A longer chase (60·N, 5 runs, N = 400) leaves C+G at 0.46 → 0.51 and C+B\* at 1.00.
- The tail-free reference (Λ = 0) has the same ordering at N = 100 and 200, with some cells lower at N = 200: C+B 0.65 (0.90 with the tail), F⁻ 0.86, F₄ 0.97, against F 1.00.
- The exploratory N = 200 value for C+B\* did not replicate: 0.80 on runs 0–19, 0.58 on runs 20–59.

**2. It is N with migration, not local supply.**
- Supply is never scarce. Every island has a compatible efficient grand support at founding, and constants alone supply thousands of grand triples.
- Named supply does not predict establishment. Islands with a same-split bid support at founding establish a grand state at 0.65, those without at 0.63 (N = 200, mN = 1). The ROC area of the support statistics is 0.50 at mN = 0.
- At matched T = 0.16 the cells separate by N:

  | N | δ | core − C |
  |---|---|---|
  | 100 | 0.05 | −0.28 |
  | 200 | 0.025 | −0.06 |
  | 400 | 0.0125 | +0.29 [0.06, 0.53] (core 0.68) |

- With the count held fixed, k = 4 bid copies per slot give core 0.20 / 0.63 / 0.77 at N = 100 / 200 / 400. With k = 1: 0.20 / 0.57 / 0.46.
- Without migration coordination is rare at every N tested: core 0.02–0.12, null 0.48–0.86, the rest mostly pairs, with small ring and undominated-wasteful shares. The k-inoculations give 0.02–0.07. Small differences remain (C+F 0.07 against C 0.04 at N = 200; C+G 0.12 against C 0.07 at N = 400).
- Dose is non-monotone at N = 400: 0.68 / 1.00 / 0.85 / 0.70 at δ = 0.0125 / 0.05 / 0.15 / 0.5. δ = 0.5 against 0.05 is −0.30 [−0.50, −0.10], with the pair share +0.30.

**3. Exits.**
- The ε-free assays agree with neutrality. A matching grand constant on a homogeneous B\*³ core island fixes at 1/N (9 cells, |z| ≤ 1.35). One of 18 neutral G³ cells is at |z| = 2.24. Pair offers and B\*(σ′) entrants have exact N·p ≤ 0.035.
- The raw tail exit hazards fall faster than 1/N:
  - C+G: 7.5·10⁻⁵, 3.0·10⁻⁵, 5.1·10⁻⁶ per in-core island-generation at N = 100 / 200 / 400 (log–log slope −1.94 [−2.17, −1.74]);
  - C+B\*: 2.2·10⁻⁴, 2.7·10⁻⁵ at N = 200 / 400.
- Most exit and entry events at mN = 1 trace to migrant lineages. These are finite-schedule rates, not ε-free.

**4. Who holds the core.**
- C+G core islands are held by grand constants in every slot.
- C+B\* at N = 400: a reader is in the majority on 1,923 of 2,411 core islands.
- C+F at N = 400: F holds 2,011 of 3,840 majority slots and grand constants the rest.
- No island at mN = 1 holds any of the 9 non-core grand splits (efficient-dominated share exactly 0 in every mN = 1 cell). At mN = 0 it is at most 0.006 of islands. F₄ equals F at N = 200 with the tail.
- With the tail, the pair fallback matters at N = 100 (C+F − C+F⁻ = +0.30 [0.05, 0.55]) and not at N = 200 (0.00). Tail-free at N = 200, F⁻ is 0.86 against F's 1.00.

**5. Which core points (RE supplement, `coverage.json`).**
- Pooled over all 1,210 mN = 1 records, 53,030 of 54,163 core islands (0.98) sit on the seven core points where every share lies between 1/6 and 1/2: the equal split, 30,143 islands, and the six permutations of (1, 2, 3)/6, 2,101–5,638 each.
- The other twelve core points hold 1,133 islands together: those where someone gets 0 (0–128 each) and the permutations of (4, 1, 1)/6 (165–329). Four of them, (0, 4, 2), (2, 0, 4), (3, 3, 0) and (4, 2, 0), never occur.
- At N = 400 the equal split is 0.37 (C+B\*), 0.49 (C+F) and 0.54 (C+G) of core islands, and 6–9 distinct modal points occur across the 20–40 runs. It is not always the most common point: in C+B at N = 400, (2, 3, 1)/6 has 381 islands against the equal split's 349.
- (4, 1, 1)-type islands are rare but persist: 11 in C+B\* at N = 800.
- At mN = 0 the few core islands (2,725) spread over all 19 points. Zero-share points occur at about a third of the equal split's frequency, as in queue 72, and 16 of 19 points have simultaneous upper bounds below 1/76 at N = 400.

*Predictions* (full table in the report). Held:
- RE 2, RE 7 (the assays), argon (i) and E3.
- Sol (iii), on the arms the verdict scored, C+G and C+B\*. The registration also names C+F; its point slope over N = 100–400 is −1.7 (hazards 1.4·10⁻⁴, 2.7·10⁻⁵, 1.4·10⁻⁵), consistent with the verdict, but no interval was computed.
- Sol (v), only trivially: founding support predicts nothing, so its registered inequality holds at chance.

Failed:
- The RS's conjecture, on its registered coverage clause: C+B\*, N = 400, mN = 0 has 16 of 19 core points with simultaneous upper bounds below 1/76. The core clause (some arm ≥ 0.95 at N = 400, mN = 1) is met by C+B and C+F (1.00, 20 runs each), not by C+B\* (0.94). The mN = 1 coverage supplement (finding 5) is post hoc and not part of the verdict.
- RE 1, on its δ = 0.0125 clause (+0.29 over C, the H_N reading).
- RE 3, RE 4, RE 5 and RE 6. RE 6 failed because readers reach 1.00.
- RE 8: with the count fixed, +0.57 from N = 100 to 400.
- Argon (ii): no efficient-dominated islands.
- Sol (iv): C+F has fewer pairs than C+G, and the fallback raises the core.
- E1 at N = 200 (by 0.057) and E2.

Nothing was unscored. No RS prediction was supplied.

*What it means for the program.*

(a) **Reading pays in proportion to N in the easy case: constants cannot leave a pair, readers can (inferred).** Queue 72's "reading buys nothing a coordination device does not" is a small-N finding and reverses from N = 400. The mechanism is inferred, not tested here:
- A constant cannot express "switch to grand once the others do". Leaving a pair state then needs both pair slots to switch, each switch alone losing its 1/6. That fitness valley deepens with N, which fits constants falling with N and C+G not relaxing in a 3× longer chase.
- A bid in a pair slot is neutral (queue 72 assay: N·p ≈ 1.1). Once two slots bid, a matching grand constant in the excluded slot is selected (≈ 9/N). So readers give a neutral path out of pairs, and neutral steps keep their rate as selection strengthens.
- The direct test would be pair-island assays at N = 200–800.
- F beats G at every N, and F and G have the same named founding supply, so supply volume does not explain F's edge. F⁻ (no fallback) also reaches 1.00 at N = 200 with the tail. Why feasibility-reading beats the grand constants is not established.

(b) **Without migration coordination is rare.** An isolated island has no source of variation besides a thin tail (Λ = 10 arrivals). Founding scrambles mostly end null or in a pair (0.48–0.86 null), and the core is 0.02–0.12 at every N tested. The large reading advantage requires migration, as argon predicted; small differences between arms remain without it.

(c) **At mN = 1 the post-hoc coverage counts are concentrated.** In the reader cells nearly every island is in the core, but 98% of core islands sit on the seven core points where every share lies between 1/6 and 1/2. The equal split is the most common point in most cells but not a majority everywhere: 0.16–0.72 of core islands across the cells at N ≥ 400 (0.37–0.54 in C+B\*, C+F and C+G at N = 400, δ = 0.05; 0.72 in C+B\* at N = 800). Coalitions in which someone gets 0 or someone gets 2/3 are rare (1,133 of 54,163 core islands), not absent. Why the (4, 1, 1) points are rare is not established; a zero-share slot is indifferent between sustaining and breaking the coalition. Under the RS's 2026-10-31 reading of "equally likely" (a lottery across worlds), the points are not equally likely either.

(d) **The easy case meets the RS's core clause in reader cells at large N with migration (C+B and C+F at N = 400; C+B\* at N = 800).** That is the realizable-language question: do readers supplied by a library prior, rather than seeded, do the same? It is not answered here.

*Caveats.*
- At mN = 1 islands within a run are correlated, so intervals are over runs. Consensus at N ≥ 400 is 0.00–0.28 (0.03–0.28 at N = 400, 0.00–0.10 at N = 800).
- N = 800 has 10 runs. Λ = 10 only at N ≥ 400.
- The DSL arm with the free modal oracle; the families are seeded by dose, with no prior over them.
- The new 20-run cells at N ≥ 200 use runs 20–39 (disclosed before launch). Founders use the stored shared-stream CRN scheme (V7 checks pairing).
