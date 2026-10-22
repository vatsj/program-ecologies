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

1. **Pilot.** One run each of four primary cells (threshold, no-overbid ε = 0; the same with the annealed tail and with migration;
   threshold, unrestricted, rain) was run once to time the kernel and debug the pipeline after §1 and the statics were written and
   committed; outputs were not kept. Its end-state lines were seen (threat about 13, revenue about 14 in the primary cell). The
   registered predictions, the scoring conventions and §1 were fixed earlier and none was changed.
2. **The kernel is a copy, not an import.** `core_auction.sim` has no arrivals schedule, no counts history and no fixation or
   first-tested records, so `core_stage2.sim2` copies its event loop (same fitness, victim, migration conventions, 3NI events per
   generation) and takes the arrivals from a precomputed schedule. It calls stage 1's `_stats`, `_payoff_of`, `_fit`, `_tri`,
   `outcome` and `flags` by import. No existing file was edited.
3. **Arrivals are drawn from a schedule, not event by event.** For rain and the annealed tail the number of arrivals in a generation
   is Binomial(3IN, ε_g), each arrival has a uniformly chosen event slot, island and role, a uniform that picks the arriving
   program through the role's cdf, and a uniform that picks the victim; an arrival replaces the selection event in its slot. This
   is the same law as stage 1's per-event mutation. The point is pairing: the full rain, (iv), (iv″) and (iv′) share the arrival
   slots, islands, roles and victim uniforms (the seed is keyed on instance, space, m, N and run, not on the control), and the
   founding states are paired by the founding prior (full prior for (iv), (iv′), (iv″)). The selection randomness is not paired
   (it diverges once the states differ). In (iv) and (iv″) the child is the same uniform mapped through a follower-only (δ >= 0.5)
   cdf in the item roles; the P-role child is identical to the full rain's.
4. **Follower rounding in integers.** The bid is (dR + 5) // 10 with d = 10δ and R = t + 1 (or c + 1), then raised to 1 and capped at
   the item's value. This is ⌊δR + ½⌋ without floating point.
5. **The checker's domain.** A program source is a function of the winners' total T alone; the checker compares it with the stated
   policy at every T in 0..80, the whole domain (two bids on 0..40), so the check is complete. Followers read the certified threat
   from this check (cached once per t). False claims are rejected in the tests; the priors contain only true claims, as the spec
   says, so the checker is exercised by the tests and by the construction of every `TX(t)`, not by an adversary in the population.
6. **Winners' total with zero bids.** T = bA + bB as submitted; a follower bids at least 1, so T = 0 arises only from two constant 0
   item programs, and `TX` then bids 1.
7. **`XPRUWIN` is P(TX wins)** in this module (stage 1: any responder's wins). Stage 1's `pru` share rows therefore read the TX share
   of P and the follower shares of A and B. P(P wins) is a separate channel.
8. **Tested.** A P program is *tested* in an island when, at a generation boundary, it wins an encounter against some pair of present
   item programs with positive probability. It is checked at every generation boundary (every fifth in the rain cells) from the
   island's current item populations; `first_tested` is the first such generation. A program's flag persists if the program leaves
   and returns. A win at an interior event that is not visible at a boundary is not counted.
9. **Item fixation.** `t_fix_items` is the first generation boundary at which A and B are both single-program. Pre and post
   `txwin` means are averaged over the sampled generations before and after it (the sample grid is coarse after 2,000).
10. **Qualifying islands (prediction 3)** are decided on the end state of the island (all three roles fixed, P on `TX(t)`, both items
    on followers, T > t), and the TX win rate is the end-state probability (and its post-fixation time average); at ε = 0 an
    island that is fixed in all roles is static from then on.
11. **Reverse-order dynamic check.** The first three runs of every cell are rerun with the tensor built under the reverse order
    (TX first, fresh item evaluations). The tensors are bit-identical for all 202,500 triples per instance (statics), so identity of
    the final counts is implied; it is recorded as `order_match` per cell.
12. **Process.** Worker count 1 (three sibling drivers alive at launch).
