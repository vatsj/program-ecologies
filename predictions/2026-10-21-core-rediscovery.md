# Predictions: rediscovering the core, 2026-10-21

Spec `specs/2026-10-21-core-rediscovery.md` (reviewed by gpt-6.1-sol, then gemini-4-argon in amended mode, both folded).
Theory `notes/coalition-proof-auctions.md` §1–3. The predictions below are the spec's, verbatim, with the falsifier in
brackets. Written and committed before any code and any counted cell. All island numbers are eps = 0 (or stated
re-injection) seed-lottery statistics at finite (N, I, horizon), never pi. Scoring: held / failed / partial, with the
number, in `runs/core-rediscovery.md`.

Scoring conventions fixed here (engineer, before any code), so no threshold can move afterwards:
* "Revenue" is the seller's expected revenue on the island's encounter distribution (mean over the island's population
  shares, counting the seller's random revenue tie). "Eroded" is revenue more than one tick below the minimum-revenue
  core (revenue < min-revenue − 1). "In the core" is: the island's mean payoff vector (seller revenue and bidder
  payoffs) is efficient, individually rational and satisfies every true-value core inequality, to 1e-6. "At the
  minimum-revenue edge" is in the core with revenue at most min-revenue + 1.
* Fractions are over (run, island) pairs pooled across the 40 runs × 64 islands of a cell, with the run-level spread
  also reported. The "end" is the fixed horizon (5,000 generations; 20,000 for constant rain), censored islands
  included.
* Prediction 6's "chance baseline" is the share of the grid's bidder-optimal-edge split points (revenue within one tick
  of the minimum, individually rational, in the core) that lie within one tick per winner of the Vickrey-nearest point.
* Predictions with a conjunction are scored partial when one part holds.

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
   second review, which pointed out that `PRU` is neutral against constants once an island is in the core.
   *Counter-prediction (gemini-4-argon), registered:* core islands exceed 50%, but `PRU` holds the losing role on fewer
   than 40% of them; its effect is weeding out underbidding winners early, so that high-bidding constants survive.
6. *The split is not Vickrey-nearest:* in the asymmetric instance, among islands in the core on the bidder-optimal
   edge, the frequency at the Vickrey-nearest split is within a factor of 2 of its chance baseline from the grid
   enumeration [above twice the baseline].
7. *Outbidder injection:* the injected outbidder establishes in at least 80% of eroded islands and restores revenue to
   the core on those [below 50%].

Reported without a prediction: the collusion instance against the threshold instance (the reviewer noted they differ in
more than the number of threats), and migration (its sign depends on the weighting).

Engineer's scoring notes (recorded before any run, not predictions): "primary cell" is the threshold instance, constants
only, U prior, eps = 0, no migration, N = 100, 64 islands, w = 0.3, 40 runs. Prediction 3's "end-state encounters" is
the encounter-weighted efficiency of the island's end state, pooled over islands. Prediction 5's "holds the losing
role" is: `PRU` is above half of the P population on the island (threshold instance; the losing role is P). Prediction
7 is scored on the threshold instance in the no-overbid space and, separately, in the unrestricted space; "restores
revenue to the core" is the island's end revenue in the core after 5,000 further generations.
