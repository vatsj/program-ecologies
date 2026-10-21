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
(6, 4); equal surplus (5, 5), payments (11, 3); equal payments (7, 7), surpluses (9, 1) [not in the core: u_A + u_B = 10, ok;
(9, 1) is in the core, it is the equal-payment point]. Hand statics: efficient Nash revenue 14..22 unrestricted (b_P = total − 1,
b_A ≤ 15, b_B ≤ 7), 14..15 no-overbid. My prediction before the skew cells: under migration the core-reaching runs land on
the **equal-surplus (5, 5)** point (risk-dominance reading of a Nash demand game between A and B, as in the divide-the-dollar
lottery), not on the Vickrey-nearest (6, 4); probability 0.55 equal surplus, 0.30 Vickrey-nearest, 0.15 other. Not a registered
prediction; it is outside the spec and scored only as a control.

## 2. Deviations from the spec and choices, each stated

(Filled in as the run proceeds.)
