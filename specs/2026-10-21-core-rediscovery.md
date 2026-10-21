# Spec: rediscovering the core: first-price package auctions on islands, with the losing bid as a threat, 2026-10-21

Status: draft by the RE; reviewed by gpt-6.1-sol, then gemini-4-argon (`--mode amended`), both folded [after review]; to be run by
a Sonnet subagent. Stage 1 of the RS's program (2026-10-21: "the relevant program for us is trying to rediscover this
core notion in our machinery"; "sgtm" to the staged plan). Theory: `notes/coalition-proof-auctions.md` §1–3; the rule
being rediscovered: the minimum-revenue core (bidder-optimal) and its Vickrey-nearest selection. Companion run (rules
imposed; rings versus police): `specs/2026-10-21-coalition-proof-auctions.md`. REJECTED.md checked: nothing re-opened.

## Why

With a best-offer seller, first-price outcomes are always in the core *with respect to the bids*: the seller never takes
less from the winners than a losing bidder offers. They are in the core *with respect to the true values* only if the
losing bidder keeps bidding near its value. A loser's bid is free: it loses whatever it bids below the winners' total,
so its bid is a costless threat, the unconditional shadow of the PD in auction form. Static theory (Bernheim–Whinston;
the pure Nash equilibria of the constant-bid game) puts first-price at the bidder-optimal core, because a loser facing
underbidding winners outbids them. The ε = 0 seed lottery has no outbidding mutant unless one was founded, so the
losing bid can drift down and the winners' price with it. The run asks which happens, what restores the core (re-
injection, a prudent loser), and how the winners split the core payment (the Vickrey-nearest split is justified only
by private-value incentives, so the RE expects no preference for it under complete information). [After review:] the
losing bid can also drift *up*. A losing overbid is free too, and the pure Nash equilibria of the unrestricted
constant game span the whole true-value core (revenue 20 to 30 in the threshold instance), not only its bidder-optimal
edge. The bidder-optimal edge is Bernheim–Whinston's refinement, and it reappears among ordinary Nash equilibria only
once weakly dominated overbids are excluded. So the run measures where the losing bid settles: below the core
(erosion), inside it, and where inside.

## Design

**Instances** (Ausubel–Milgrom roles; P bids on AB, A on A, B on B; complete information; integer grid 0..40):
- *threshold* (P, A, B) = (20, 15, 15): A and B should win; the minimum-revenue core charges them 20 in total;
  Vickrey-nearest payments 10 and 10.
- *asymmetric* (20, 16, 12): minimum-revenue core total 20; core bounds on surplus u_A ≤ 8, u_B ≤ 8, u_A + u_B ≤ 8;
  Vickrey-nearest payments 12 and 8.
- *collusion* (20, 5, 5): P should win; the minimum-revenue core charges P 10 (the two losers' values); two
  independent losing threats instead of one.

**Bid spaces** [after review]: *unrestricted* (0..40) and *no-overbid* (each role's bids capped at its value; the
weakly dominated overbids removed), both in every cell of Stage 1a.

**Seller.** First-price, best offer: the allocation with the highest reported revenue; revenue ties broken uniformly at
random; winners pay their bids.

**Programs.**
- *Stage 1a, constants:* a program is an integer bid on 0..40.
- *Stage 1b, the responder* [after review: made role-specific, capped and terminating; **run in the no-overbid space
  only**, after the second review, so the responder's default never wins at a loss]: `PRU(c)` reads the other
  roles' programs, which here is the same as seeing their bids, so source access and response capability coincide in
  this game (stated, not tested). It plays the bid that maximizes its expected payoff against the others' resolved
  bids, over the whole grid and counting the seller's random tie (so tying can beat outbidding by one tick near its
  value), with ties in expected payoff broken toward the lower bid. It plays that bid when the expected payoff is
  strictly positive, and otherwise its default c ≤ its value [after second review]. Zero bids are handled
  explicitly. Losing as a loser, it never pays and never wins at a loss. It
  is the PrudentBot of the auction for whichever role is losing: it wins exactly when the other side underbids.
  *Evaluator:* constants resolve first. `PRU` programs then best-reply in the role order P, A, B to the bids resolved
  so far, with unresolved responders at their defaults. A second pass follows. If it changes nothing the profile is
  resolved; otherwise the triple is recorded as cycling and the second-pass bids are used. An order-sensitivity
  diagnostic reruns 1b's primary cell with the order B, A, P, and 1b is also run on the asymmetric instance, to check
  that the order does not bias the split [after second review].
**Priors.** Uniform over constants (U); in 1b, uniform over constants plus `PRU` with total mass m ∈ {0.05, 0.2} per
role, its default uniform over the grid.

**Dynamics.** The repo's fixed-role island seed lottery (reuse the fixed-role chicken or social organization game
island kernel, import only): one population per role per island, N = 100, 64 islands, w = 0.3, random role triples per
encounter. Run 5,000 generations; the constant-rain arm runs 20,000 generations, since 5,000 is only a few neutral turnover times
under rain [after second review]. Outcomes are reported at that fixed horizon for **every** island, censored ones included, and
absorption statistics are given separately for the mutation-free arms [after review]. A small N sweep, N ∈ {50, 100,
200}, is run in the primary cell (constants, threshold instance, ε = 0, both bid spaces). Re-injection arms:
- ε = 0 (primary);
- an annealed tail, delivering A ∈ {1, 3} fresh founders per 100 programs per role over t₀ = N/2, with the repo's
  annealed schedule;
- constant rain at εN = 0.05 per role per generation.

Migration off (primary). As a secondary arm, the stored mN rule applied **per role**: each role's emigrants are chosen
independently, weighted by that role's own payoff [after second review: whole-island weighting by summed bidder
payoffs would select against seller revenue by construction]. 40 runs per cell, paired founders across arms.

**Statics, committed before the dynamics.** All pure Nash equilibria of the three-role constant-bid game in each
instance and bid space, their full payoff vectors checked against every true-value core inequality, their revenue
against the minimum-revenue core, and their splits. Also the grid points within one tick of the Vickrey-nearest point,
so the split statistic has a stated chance baseline.

**Caveat on the unrestricted arm** [after second review]: the grid gives the losing bid more room below the core
(0..19) than inside it (20..30), and a quarter of P's uniform prior starts at bids that block the items entirely. So
erosion rates are compared across bid spaces only alongside the founders' bid distributions.

**Controls** [after review]: (i) *outbidder injection*: into eroded end states (revenue below the core), inject 5
copies of the profitable outbidder (P bidding the item total plus one) and measure establishment and downstream
revenue; (ii) founder coverage per island (the highest and lowest founding bid of each role).

**Outputs.**
- *Per island at the end:* the realized seller-and-bidder payoff vector checked against every true-value core
  inequality, with efficiency, individual rationality and revenue reported separately [after review]; revenue relative
  to the minimum-revenue core; whether the efficient allocation is played
  (an evaluation); the winners' split along the core frontier; the losing role's surviving bids.
- *Time series:* the losing bid's maximum and median; revenue; time to first erosion (revenue below the core by more
  than one tick); for `PRU`, its share and whether it was ever tested (won a contest).
- *Per cell:* the fraction of islands within one tick of the minimum-revenue core; the fraction at the Vickrey-nearest
  split (within one tick per winner); efficiency; drift and selected fixations of the losing role's bid.

## Predictions (the RE's; falsifiers in brackets)

1. *Statics* [rewritten after review: the first draft claimed the bidder-optimal edge for ordinary Nash, and the
   reviewer's counterexample (24, 12, 13), with revenue 25, refutes it]: in the unrestricted bid space the efficient
   pure Nash equilibria's revenues cover the whole true-value core (20..30 in the threshold instance) and nothing
   below it. In the no-overbid space they lie within two ticks of the minimum-revenue core [an efficient equilibrium
   below the core in either space, or more than two ticks above its minimum in the no-overbid space].
2. *Erosion at ε = 0 (constants, threshold instance, both bid spaces):* at least 50% of islands end with revenue more
   than one tick below the minimum-revenue core; in the unrestricted space the rest end mostly inside the core, spread
   over it rather than at its minimum [below 30% eroded].
3. *Efficiency:* the efficient allocation is played in at least 75% of end-state encounters in the threshold and
   collusion instances. The erosion is mostly a transfer from the seller [below 60%; lowered after review, which
   expects package wins from item bidders' coordination failures].
4. *Re-injection:* with the annealed tail at A = 3, at least 60% of islands end within the core [below 40%]. The
   reviewer expects transient restoration; the time-average of the in-core fraction is reported beside the endpoint.
5. *The responder (1b):* at ε = 0 with m = 0.2, at least 50% of islands end in the core [below 30%]. Revised after the
   second review, which pointed out that `PRU` is neutral against constants once an island is in the core. *Counter-
   prediction (gemini-4-argon), registered:* core islands exceed 50%, but `PRU` holds the losing role on fewer than 40%
   of them; its effect is weeding out underbidding winners early, so that high-bidding constants survive.
6. *The split is not Vickrey-nearest:* in the asymmetric instance, among islands in the core on the bidder-optimal
   edge, the frequency at the Vickrey-nearest split is within a factor of 2 of its chance baseline from the grid
   enumeration [above twice the baseline].
7. *Outbidder injection:* the injected outbidder establishes in at least 80% of eroded islands and restores revenue to
   the core on those [below 50%].

Reported without a prediction [after review]: the collusion instance against the threshold instance (the reviewer
noted they differ in more than the number of threats), and migration (its sign depends on the weighting).

## Required outputs

`src/core_auction.py` (+ `_run.py`, `_report.py`), `tests/test_core_auction.py` (the instance cores and Vickrey-nearest
points by hand; best-offer resolution; `PRU` resolution against constants; the statics), `notes/core-rediscovery.md`
(§1 hand predictions; §2 deviations), `predictions/2026-10-21-core-rediscovery.md` committed before any counted cell,
`runs/core_auction/` (summary JSON and small CSVs only), and a verdict file `runs/core-rediscovery.md`. Hand back draft
paragraphs for RESULTS ("Rediscovering the core"), REJECTED, THEORY and NOTATION; do not edit the shared docs.

**Scale guard.** ≤ 3 workers, launched only when a sibling run has finished (check `ps`); one job per process.
**Waiting:** watch short commands; for long batches wait on one background command that exits at completion, or end the
turn with outputs on disk; never poll periodically.
