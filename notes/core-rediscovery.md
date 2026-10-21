# Rediscovering the core: the run (engineer, 2026-10-21)

Spec `specs/2026-10-21-core-rediscovery.md`; theory `notes/coalition-proof-auctions.md` §1–3; predictions
`predictions/2026-10-21-core-rediscovery.md` (committed before any code); verdicts `runs/core-rediscovery.md`. Code:
`src/core_auction.py` (seller, instances, evaluator, statics, island kernel), `src/core_auction_run.py` (driver),
`src/core_auction_report.py` (tables, verdicts); tests `tests/test_core_auction.py`. Outputs `runs/core_auction/`.

## 1. Hand predictions (engineer, before the statics were run)

Derived by hand from the seller's rule (best offer, revenue ties at random, a zero bid is no bid). A pilot of the kernel
(one run of the two primary cells at one seed, to time it; not counted, not kept) had been run before these were
written; it showed revenue about 16–17 in the threshold instance, so my expectation of erosion in §1.4 is not
independent of it.

**1.1 Instance cores** (true values; payoff of bidder i is v_i − payment; seller payoff is revenue):
* threshold (20, 15, 15): w(N) = 30; bounds u_P ≤ 0, u_A ≤ 10, u_B ≤ 10, u_A + u_B ≤ 10; the bidders' payoffs sum to
  at most 10, so the minimum-revenue core charges the winners 20 in total (revenue range 20..30). VCG payments (5, 5),
  Vickrey-nearest (10, 10).
* asymmetric (20, 16, 12): w(N) = 28; u_A ≤ 8, u_B ≤ 8, u_A + u_B ≤ 8, so revenue 20..28; VCG (8, 4); Vickrey-nearest
  (12, 8) (surcharge 8 split 4 + 4).
* collusion (20, 5, 5): w(N) = 20; u_P ≤ 10, losers' bounds 0, so P pays 10..20; VCG price 10, Vickrey-nearest 10.

**1.2 Pure Nash equilibria of the constant-bid game, threshold, efficient allocation.** P (value 20) must not gain by
bidding the item total (a tie pays ½(20 − t) with t = bA + bB, so t ≥ 20), and A must not gain by lowering its bid until
it just wins (that cheaper win is available unless bP ≥ t − 1), while a tie at bP = t − 1 after A's one-tick drop pays
½(16 − bA), which beats 15 − bA only if bA = 15. So the efficient equilibria have bP = t − 1 exactly with
bA, bB ≤ 14 (the tie lowers a bid of 15 by a tick for 0.5), i.e. revenue 20..28, not 20..30. Unrestricted: revenue
covers 20..28 (the whole core except its top two ticks, a grid-tie effect). No-overbid (bP ≤ 20): t ≤ bP + 1 ≤ 21,
revenue 20..21. Asymmetric: bA ≤ 15, bB ≤ 11, so unrestricted revenue 20..26, no-overbid 20..21; the splits span the
whole edge (every (bA, bB) with the right sum), so Nash makes no choice among them.

**1.3 Collusion instance (P wins).** P outbids the losers by one tick (bP = bA + bB + 1) up to total 18 and ties
above; neither loser can win profitably alone while bP ≥ bB + 5 (a tie at bP − bB would pay ½(5 − x)), i.e. bA, bB ≥ 4.
At bA = bB = 4, bP = 9: an efficient equilibrium with revenue **9, one tick below the core's minimum 10** (the losers
could win only jointly). So I expect prediction 1's "nothing below the core" to fail by one tick in the collusion
instance and to hold in the threshold and asymmetric instances. In the no-overbid space the losers are capped at 5, so
bP is 9..11.

**1.4 Island dynamics (expectation, partly informed by the pilot).** Erosion in the threshold instance at ε = 0:
high P bids lose and cost nothing, but P's low bids win against underbidding winners, so P's population is pulled to
bids just above the winners' total; the winners are pulled down to just beat P. The result is a revenue near, and mostly
below, 20 (the pilot: 16–17), with the efficient allocation played in roughly 0.8 of encounters because P wins when
the winners' total falls below P's bid.

**1.5 The skew control (post hoc, written before the skew cells finished).** After the spec cells showed that runs reaching the
core under migration all land on one split (threshold (10, 10), asymmetric (12, 8): 20 of 20 and 15 of 15 core-reaching runs
in the no-overbid space), I noticed that in the AM family with v_P above both item values the two winners' VCG surpluses are
equal (both are w(N) − v_P), so the Vickrey-nearest split and the equal-surplus (Nash-product) split coincide in the spec's
instances and the run cannot tell them apart. I added one instance, `skew` = (v_P, v_A, v_B) = (14, 16, 8), where they differ:
core u_A ≤ 10, u_B ≤ 8, u_A + u_B ≤ 10, min revenue 14; VCG payments (6, 0); Vickrey-nearest payments (10, 4), surpluses
(6, 4); equal surplus (5, 5), payments (11, 3); equal payments (7, 7), surpluses (9, 1), also in the core. Hand statics: efficient Nash revenue 14..22 unrestricted (b_P = total − 1,
b_A ≤ 15, b_B ≤ 7), 14..15 no-overbid. My prediction before the skew cells: under migration the core-reaching runs land on
the **equal-surplus (5, 5)** point (risk-dominance reading of a Nash demand game between A and B, as in the divide-the-dollar
lottery), not on the Vickrey-nearest (6, 4); probability 0.55 equal surplus, 0.30 Vickrey-nearest, 0.15 other. Not a registered
prediction; it is outside the spec and scored only as a control.

## 2. Deviations from the spec and choices, each stated

1. **Seller details the spec left open.** A zero bid is "no bid": it cannot win, so allocations {A, B} need both bids at least 1,
   and an all-zero profile is no sale (zero payoffs). Allocations considered are {P}, {A, B}, {A}, {B}; the singleton item
   allocations matter only when the other item bid is zero. Ties are uniform over the revenue-maximal allocations, and every
   payoff and statistic is the expectation over that lottery (the island kernel uses expected payoffs, as `auction_islands.sim3`
   does).
2. **A new island kernel.** The spec says to import the repo's fixed-role island kernel. `auction_islands.sim3` has its program count
   compiled in as K = 4, so `core_auction.sim` re-implements the same conventions (three populations per island; one island
   and one role per event; child drawn in the own island or, with probability m, a uniformly chosen other island, by exp(w ·
   expected payoff); uniform victim; 3NI events per generation; expectation over independent draws from the two other
   roles' island populations), for up to 82 programs per role, with payoffs updated incrementally on present programs and
   a test that the incremental payoffs equal a recomputation. No file in `src/` was edited.
3. **The annealed schedule** is the repo's (`eps_n_annealed`, `delivered`, `ONSET` = 200 from `src/annealed.py`), loaded from the
   source by the AST because importing `annealed.py` runs module-level code that needs run data a fresh worktree lacks
   (`runs/provenance/static`). Horizon = the run length (5,000), so the tail delivers A·4,800/4,850 founders per role per island;
   founders are drawn from the cell's prior (uniform over constants, plus PRU mass in the 1b arms) and replace a uniformly chosen
   program. Constant rain is εN = 0.05 per role per island per generation from generation 0, 20,000 generations (the
   annealed arms run 5,000).
4. **Per-role migration**: mN = 1 (m = 0.01 per event, the stored rule at N = 100), each role's child drawn independently in a
   uniformly chosen other island by that role's own fitness (the kernel's convention); there is no between-island selection
   on island totals. 5,000 generations, no stopping at global freezing. Migration cells are reported without a prediction.
5. **PRU**: its bid set in the no-overbid space is 0..value (so it never overbids), its default c is uniform on the same set;
   mass m per role is split uniformly over defaults; the resolution is as in the spec. 1b is run only in the no-overbid space.
6. **Island statistics** are encounter-weighted means over the island's present program triples. "In the core" is evaluated on
   the island's mean payoff vector and mean revenue (the spec's "realized vector"), with the encounter-level core probability
   also stored (`core_enc`). Polymorphic islands (migration, rain) therefore average over encounters; at ε = 0 without
   migration every island is fixed at the horizon (`fixed` = 1.00 in every such cell), so the two coincide there.
7. **Reading of prediction 3's second sentence.** The bracket "[below 60%]" is read as the falsifier for the efficiency share
   (below 60% of end-state encounters efficient); "mostly a transfer from the seller" is scored separately as the transfer
   share of the revenue shortfall, (bidders' total payoff above the core maximum)/(minimum revenue − revenue), pooled over eroded
   islands, with "mostly" read as above 0.5.
8. **Outbidder injection** is run in the four 1a cells with item winners (threshold and asymmetric, both spaces), after the
   main run, into every eroded island: 5 uniformly chosen P programs are replaced by the constant (modal A bid + modal B bid +
   1), capped at P's bid cap; 5,000 further generations at ε = 0; establishment is the injected program holding at least half of P
   at the end (fixation is reported too); the control continues the same eroded islands without injection. Not run in the
   collusion instance (no single profitable outbidder: the losers would need a joint deviation).
9. **Founding states are already eroded in the no-overbid space** (the uniform mixture's revenue is about 16.6 against a core
   minimum of 20), so "time to first erosion" is generation 0 for every island there; in the unrestricted space the founding mix
   overpays (mean revenue 41.8, random overbids win) and the time to first erosion is meaningful (median 2 generations after the
   start among islands that were not eroded at generation 0). Erosion statistics at the end are therefore not a drift away from
   a core start; they compare the end state with the core.
10. **Prediction 6 and the numbers behind it**: the baseline is the grid enumeration (5/17 = 0.294 in the asymmetric instance,
    both spaces); the ε = 0 asymmetric cells have very few islands on the bidder-optimal edge (0.3% of islands), so I added
    ten-times-the-runs cells (`*_x10`, 400 runs) for a usable count. They are post hoc and reported beside the 40-run cells.
11. **Post-hoc extras, not in the spec**: the `skew` instance (§1.5), the order-free responder (`1b_*_sim`: every PRU best-replies
    once, simultaneously, to the profile with the PRU programs at their defaults), re-injection arms on the asymmetric and
    collusion instances and on the responder prior, migration on every instance, and the x10 cells. Also the static order
    diagnostic (`order_static.json`: share of triples whose resolved bids differ between P,A,B and B,A,P, and the cycling share).
12. **The pilot** (§1) is disclosed there. The statics were run before any island cell and committed; hand predictions §1.1–1.3
    matched them exactly.
13. **Seeds**: founders per (instance, space, PRU mass, N) and run index, so founders are paired across arms of a prior;
    dynamics seeds per (cell, run). Cells are deterministic given the seeds.
14. **Process**: worker count 1 until the `runs/hooks_w2` chain was gone, then at most 3 (2 + 1 in the second and third batches); one
    process per chunk of runs (a pool with `maxtasksperchild=1` when more than one worker); the tensors are rebuilt in each task.
