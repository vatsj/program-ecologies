# Predictions: the pair-worth-a game on islands (queue 72), 2026-11-01

Spec `specs/2026-11-01-pair-worth.md` (a7758a7), reviews `reviews/2026-11-01-pair-worth-*.md`, notes `notes/pair-worth.md`.
Written by the engineer before any counted cell; the static numbers below are computed (`src/pair_worth_static.py`,
`runs/pair_worth/static.json`). The main tail dose is Lambda = 10 (queue 71 had not reported). Scoring is against the
spec's verdict rules. Verdict vocabulary: held / failed / unresolved. A falsifier that is met is a failure, reported as
one.

## Static numbers (design 1)

Strict coalitions-map dominance (x dominates y if some coalition S with x(S) <= v(S) has x_i > y_i for all i in S);
weak: weakly better for all, strictly for one. Vectors are payoff vectors on the grid; "efficient" means the sum is the
grand worth; ring = strictly undominated efficient vectors outside the core proper; undominated wasteful = strictly
undominated vectors of sum < 1 (wasteful grand splits and pair vectors).

| game (grid) | vectors | core proper | strict undominated | = core + ring + undominated wasteful | weak undominated | stable set, strict | stable set, weak |
|---|---|---|---|---|---|---|---|
| G1/3 (6ths) | 84 | 19 | 55 | 19 + 6 + 30 | 19 (= core) | unique, = the 55 (externally stable) | unique, = the 19 |
| G2/3 (6ths) | 84 | 1 | 13 | 1 + 9 + 3 | 1 (= core) | unique, 13 | unique, 4 (core + 3 ring) |
| Glove (6ths) | 84 | 1 | 5 | 1 + 3 + 1 | 1 (= core) | unique, 13 (core 1, ring 3, other efficient 6, wasteful 3) | unique, 4 |
| G5/6 (12ths) | 455 | 0 | 0 | | 0 | unique, 15 vectors (12 efficient + 3 at (5,5,0) perms) | none |
| G2/3' (24ths) | 2,925 | 1 | 13 | 1 + 9 + 3 | 1 (= core) | not searched (MILP at 2,925 vectors skipped) | |
| Glove' (24ths) | 2,925 | 1 | 5 | 1 + 3 + 1 | 1 (= core) | | |

Findings from the static table:

- **The Theory tab's grid claim does not hold on 24ths.** "Strict undominated = core proper at a = 2/3 and in the glove
  market" is a continuum fact; on every grid the one-tick ring (9 vectors at a = 2/3, 3 in the glove market) and the
  wasteful undominated vectors are strictly undominated, so the count does not fall with the grid (13 and 5 at 6ths and
  at 24ths; only the distance to the core shrinks). Only weak dominance returns the core proper (1 vector) at both grids.
  This undercuts the stated static rationale of RE 4's transfer clause; the prediction is kept as registered and scored.
- G1/3: the strict stable set (55) contains, besides the 19 core points, 6 ring points ((5,1,0) permutations) and 30
  undominated wasteful vectors; **most of them are wasteful grand splits**, reachable by three constants naming ALL.
  The RS's target (the core proper) is the weak-dominance stable set; ring and wasteful vectors are scored separately.
- G5/6: strict dominance has no undominated vector; there is a unique strict stable set on twelfths (15 vectors) and none
  under weak dominance (the Theory tab's "15 on twelfths" is the strict one).
- The core points of G1/3: 10 with every share positive, 9 with a zero share: (4,2,0), (3,3,0) and permutations.

Length-prior mass under R's grammar (n <= 6, atoms BOX(THEM_j = a), 2 * nact atoms): the level-1 spelling (what is run) is
outside the modalPA grammar (mass 0); the as-written level-0 spellings have sizes B0 = 20, K0 = 30 and A0 = 40 (G1/3), 120
(G5/6) nodes and, for one spelling, log10 prior mass -15.1 / -22.1 / -29.2 at G1/3 (-16.1 / -23.7 / -91.6 at G5/6), against a
dose of 10^-2 per slot: the families are seeded, not drawn.

## The RS's conjecture (easy case)

In G1/3 every island ends in the core proper and every core point appears with positive probability. Operationalised:
C+B* at Lambda = 10 and mN = 1: core proper >= 0.95 of islands at the end; and at mN = 0 every one of the 19 core points
has island frequency >= 1/76 by run-clustered simultaneous 95% intervals (fails on a point with upper bound < 1/76).

**Engineer's expectation: fails on the first clause.** The strict stable set of this grid includes the 6 ring points and
30 undominated wasteful vectors; bids on all 28 splits (B*) and the undominated wasteful grand coalitions reached by
constants are not removed by strict dominance, so core proper is expected at about 0.5-0.85 at mN = 1, with core + ring +
undominated wasteful >= 0.9 (the strict stable set). The second clause (coverage at mN = 0) is expected to hold for the
10 points with every share positive and to be marginal for the 9 zero-share points.

## RE predictions 1-11 (as in the spec; thresholds unchanged) with the engineer's expectation

| # | statement (abridged) | expectation |
|---|---|---|
| 1 | G1/3 C: core proper < 0.8 at mN = 1, both tails | holds (confident) |
| 2 | C+B* core proper >= 0.8, >= 0.2 above C, dominated grand <= 0.05; C+B >= 0.9; C+G >= 0.15 below C+B* | uncertain; the >= 0.9 for C+B is the fragile clause (undominated wasteful and ring outcomes take the rest) |
| 3 | tail raises core proper by >= 0.05 in C+B, < 0.05 in C | uncertain |
| 4 | ring: C+B <= 0.05, C >= 0.02; transfers lower non-core undominated share by >= 0.05 | clause 1 likely fails (ring points are strictly undominated, 6 of the 55), clause 3 likely fails (static: the ring does not shrink with the grid) |
| 5 | middle case: G2/3 C+B core + ring >= 0.7, core >= 0.3; glove R share >= 5/6, islands on (1,0,0) or (5/6,1/6,0) >= 0.7, (1,0,0) alone in [0.3,0.8] | uncertain; glove R share clause likely holds |
| 6 | G5/6 C: pair islands >= 0.7 | likely holds |
| 7 | G5/6 C+B: grand >= 0.6, >= 0.3 above C | holds if the repaired fallback works as hand-checked (V4) |
| 8 | G5/6 C+B+K: grand occupancy in [0.15, 0.85], >= 1 switch per island per 10^4 generations in the tail, structure >= 0.6 | see E3 below: likely fails on structure and possibly on occupancy |
| 9 | C+A within 0.05 of C | uncertain (A accepts pair offers; may help pair islands, not grand) |
| 10 | R within 0.1 of C | likely holds |
| 11 | invasion assays: (i) B in a pair slot fixes at 1/N, with B in both pair slots a B in the excluded slot fixes at >= 3/N; (ii) blocker on a B^3 island fixes at 1/N, with K^2 the third bid is lost, a matching grand constant fixes at 1/N | (i) pair-slot neutrality holds when the island's pair split is not the exclusion split; (ii) fails for K (E1 below) |

Reviewer counter-predictions (scored as the spec states): gpt-6.1-sol: grand states long-lived not absorbing (escape
hazards of 2b); G5/6 switching depends strongly on residual family supply, recurrent cycling unestablished (chase switch
rate against the tail's). gemini-4-argon: G1/3 C+B core proper >= 0.9 but pooled coverage at mN = 1 <= 15/19 with the
zero-share points missing, while mN = 0 shows all 19.

## The engineer's own predictions (derived from the equations before any run; see notes 1.3)

E1. **The blocker is not neutral on a bid island and is slot-asymmetric.** With the repaired (level-1) handshakes, K
in slot 0 or 1 on a B^3 island pairs with the lowest-indexed other slot (its first handshake line) and breaks the grand
coalition: K in slot 0 pairs with the slot-1 bid, K in slot 1 with the slot-0 bid, K in slot 2 is paired with nobody (slots
0 and 1 pair, K falls to its fallback c). At G5/6 equal split a K in slot 0 or 1 gains 5/12 against 4/12 (selected, one
copy), a K in slot 2 loses (selected against); a single blocker in slots 0 or 1 therefore fixes with probability
greater than 2/N (RE 11(ii) falsified), in slot 2 below 0.5/N. Equations: notes 1.4 and V4.
E2. **The as-written level-0 bid has no working fallback** (hand-derived and prototyped before the notes were written;
validated by V4). Arms with level-0 bids (CB0, CBs0) are within 0.05 of C on core / grand share at G1/3 and G5/6.
E3. **G5/6 C+B+K does not cycle between grand and pair on the stated structure.** Blockers in slots 0 and 1 are selected on
entry; the grand state is destroyed by a single K and restored only when bids refill; the "neutral blocker then selected
second blocker" structure (RE 8) is not the mechanism; the structure criterion (bid or blocker present in two slots
before the switch, >= 0.6 of switches) is expected to hold only trivially (families present in >= 1 individual are
common under the tail) and the grand occupancy over 200-10,000 to be below 0.5.
E4. **Bids do not remove the strict ring.** G1/3 C+B*: ring islands >= 0.05 at mN = 0 (the six (5,1,0) permutations are
in every strict stable set, and bids on them are as stable as bids on core points).
E5. **Zero-share core points are under-represented**, as argon predicts: pooled coverage at mN = 0 of the 9 zero-share core
points is below that of the 10 positive-share points by a factor of 2 or more per point.

Falsifiers: each of E1-E5 fails if the stated inequality is reversed in the corresponding measured quantity.
