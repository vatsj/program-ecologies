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

## 2. Deviations from the spec and choices, each stated

(Filled in as the run proceeds.)
