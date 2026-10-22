# Rediscovering the core, stage 2: the run (engineer, 2026-10-21)

Spec `specs/2026-10-21-core-stage2.md`; stage 1 notes `notes/core-rediscovery.md` (its 11 choices are followed unless §2 says
otherwise); predictions `predictions/2026-10-21-core-stage2.md` (committed before any code); verdicts `runs/core-stage2.md`.
Code: `src/core_stage2.py` (programs, checker, resolvers, kernel), `src/core_stage2_run.py` (statics, registry, driver),
`src/core_stage2_report.py` (tables, verdicts); tests `tests/test_core_stage2.py`. Outputs `runs/core_stage2/`.

## 1. Hand predictions (engineer, before the statics were run)

No pilot was run. Before these were written I had checked only that the numba tensor and the pure-python resolver agree on every
triple (two instances), which is a test of the code, not a look at any result.

**1.1 Follower bids.** A follower with d = 10δ facing a requirement R bids (dR + 5) // 10 (half rounds up), raised to 1, capped at
its value. Against `TX(20)` (R = 21) the bids for δ = 0.1..0.9 are 2, 4, 6, 8, 11, 13, 15, 17, 19, capped at the item value.

**1.2 Statics, threshold (20, 15, 15), `TX(20)`.** `TX` wins whenever T <= 19 (it bids T + 1, inefficient), ties with the items at
T = 20 (a 50/50 revenue lottery), loses at T >= 21. Complementary pairs (A, B): (0.1, 0.9) T = 17 and (0.2, 0.8) T = 19 give a `TX`
win; (0.3, 0.7) and (0.4, 0.6) T = 21; (0.5, 0.5) T = 22; mirrors the same. So the efficient complementary outcomes have revenue
21, 21, 22 (1, 1, 2 ticks above the minimum 20): within two ticks, prediction 1 holds. Asymmetric (20, 16, 12): efficient
complementary revenues 21, 22, 21 and ties at T = 20; the extreme pairs are `TX` wins (B's cap at 12 clamps δ_B >= 0.6).
Skew (14, 16, 8), `TX(14)`, R = 15: A's follower bids 2, 3, 5, 6, 8, 9, 11, 12, 14, B's the same capped at 8
(2, 3, 5, 6, 8, 8, 8, 8, 8). Complementary pairs (A, B): (0.9, 0.1) T = 16, (0.8, 0.2) T = 15, (0.7, 0.3) T = 16,
(0.6, 0.4) T = 15, (0.5, 0.5) T = 16, then (0.4, 0.6) T = 14 (a tie), (0.3, 0.7), (0.2, 0.8), (0.1, 0.9) `TX` wins. So efficient
complementary revenues 15 or 16 (one or two ticks above the minimum 14): prediction 1 holds with the maximum exactly at the
two-tick limit, so the skew instance is the one place the falsifier could bite (a revenue of 17 would fire it).

**1.3 The skew static map.** Of the 81 (δ_A, δ_B) pairs, 35 have T >= 15 (items win outright), more with ties at T = 14; B's
cap puts 45 of the 81 pairs at b_B = 8 (five of nine δ_B values). No pair reproduces the Vickrey-nearest payments (10, 4) exactly
(B has no bid of 4), nor the equal-payment point (7, 7) (A has no bid of 7 either); the equal-surplus point (11, 3) is reachable at
(δ_A, δ_B) = (0.7, 0.2) at T = 14 (a tie). So exact matches to the three references will be rare under the follower grid and the
split classes will mostly be "other", with distances reported. The prior-weighted split distribution (uniform δ) will put the bulk of
the item-winning pairs at b_B = 8 and A paying 8..14.

**1.4 Dynamics (partly informed by the statics above and by stage 1).**
* `TX(t)` weakly dominates the constant t in role P: against T < t it pays T + 1 where the constant pays t; against T >= t the two
  bid alike. So in the scramble the selection pressure is toward high t. I expect P's end threat well above the prior mean (about
  10.25) on most islands in the primary cell, a shift of 5..9 ticks, and the matched-constants control to shift less but not by less
  than half (constants are selected on the same pressure through the item bids). That is a deliberate disagreement with the RE's
  "at most half"; I put 0.35 on the RE's reading.
* The core fraction in the primary cell (ε = 0, m = 0.5): I expect it above the RE's 0.2..0.6 band, around 0.6..0.8, because followers
  re-price against a high fixed threat (T near t + 1) and a constants-only item pair does not have to be exploited. Probability that
  it lands inside 0.2..0.6: 0.4.
* Prediction 3: I expect the shadow to hold. A follower pair whose bids sum above t is never overbid by `TX`, so `TX` wins 0 of
  the encounters on qualifying islands; I put 0.8 on "under 1%".
* Rain: I expect rain to help (>= 0.8 core) only if the cell is not dominated by arrivals of low-δ followers; unsure. The safe-follower
  control I expect to fall (0.6 or lower, 0.6 confidence).
* The order-free check will pass trivially: the tensors are bit-identical.

## 2. Deviations from the spec and choices, each stated

(filled in as the run proceeds; see below)
