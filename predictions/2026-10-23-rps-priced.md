# Predictions: rock-paper-scissors with a compute price, 2026-10-23

Spec `specs/2026-10-23-rps-priced.md` (reviewed by gpt-6.1-sol, then gemini-4-argon in amended mode; both folded). Hand
derivations: `notes/rps-priced.md` §1 (committed before any code). Written and committed before any code runs and before
any counted cell. Chain numbers are ε→0 chain quantities (π, closure-complete over the explored states), lottery numbers
are ε = 0 seed-lottery statistics at finite (N, I, horizon), never π. Scoring: held / failed / partial / not scored, each
with the number, in `runs/rps-priced.md` and `.json`.

## The RS's statement (2026-10-23, quoted in the spec)

"there's an old thread that considers compute costs nontrivial, so I'd lean against [counting mutual non-termination as a
free tie]. I'd call this a failure that shows a need for a random-action primitive … Opponents can see the coin and
simulate the flip, but they can't actually predict how the opponent flip will land."

The RE's reply, accepted by the RS ("go with your default price"): the coin primitive was already present (`X`, `coin`);
what failed is that non-play was free; the default price is a cost per application level, so a forfeit costs the whole cap.
Scored on the same reading (I) as the unpriced run (individual programs mix and the programs that hold the population are
unexploitable), on the **net** exploitability: it holds, per price c, if in the stochastic arms (sample, exact) at N = 10^4
(chain) and on the lottery the population's net in-population program exploitability is at most 0.05 and the
individual-mixing share is at least 0.8; it fails if net exploitability exceeds 0.15 or mixing falls below 0.5 in every
stochastic arm; partial otherwise. The primary c is 0.01; the others are reported. Readings (W) and (M) are reported.

## Scoring conventions fixed here (engineer, before any code), so no threshold can move afterwards

* **Cells.** Grammar n = 6, D = 12, w = 0.3, length prior (bits), as in the unpriced run. Arms pure, sample, sample-matched
  ("matched"), exact, each priced by the **depth price** (`notes/rps-priced.md` §1.0): `U_c = U - c H`, H the expected
  application depth of the paying program's root evaluation (a coin counts the branch taken, a `cr` the deepest branch).
  Price panel c in {0.001, 0.01, 0.05}; c = 0 is the stored unpriced run. Controls at c = 0.01: **forfeit-only**
  (charge c D P(forfeit)), **depth panel** (c D = 0.12 at D = 8 and 16, i.e. c = 0.015 and 0.0075, sample and exact arms),
  exact-br priced at c = 0.01, and the **work price** (c per application executed, all branches of a `cr`) at c = 0.01 in
  the sample and exact arms. Classes are recomputed from the priced payoff rows and columns of each cell.
* **Chain.** `LogChain`, closure-seeded exploration plus multi-start replicator searches (support up to 6), twin-expanded
  distribution, N in {100, 1000, 10^4, 10^5}, log theta sensitivity at N = 10^4 (two further values), lumped versus
  twin-expanded at N = 10^4. Any unresolved cycle or attractor is reported as indeterminate and not given stationary weight.
* **Lottery.** ε = 0, founders iid from the length prior at the program level with the unpriced run's seeds (paired, run by
  run), mapped to the priced classes after seeding; complete island graph, (N, I) = (100, 64), mN = 1, w = 0.3, 40 runs,
  generation 2,000 is the primary reading; runs are carried to 10,000 generations and the rule of the spec is applied:
  an island's **support** is its set of classes with share >= 0.05; it is **resolved** when its support has not changed over
  the last 500 generations (a stable polymorphism counts as resolved), **cycling** when its support revisits an earlier
  support within that window (indeterminate, not extended), otherwise **unresolved**; the 10,000-generation statistics are
  reported for runs with any unresolved island. Size cell (400, 16), 20 runs, at c = 0.01. All contrasts are paired by
  founder run and use run-clustered 95% bootstrap intervals (4,000 resamples of runs).
* **Net exploitability** is the primary exploitability and the one that binds Predictions 2, 3, 5, 7: the in-population
  program exploitability `e(x) = max_k (U_c x)_k` over all classes k of the arm's own grammar (the exploiter's game payoff
  minus its own cost). **Gross** exploitability (the best game payoff alone) is reported beside it; at c = 0 the two are
  equal. **Individual (statewise) exploitability** is `sum_p x_p max_k U_c[k, p]`, the resident-weighted exploitability of
  each resident program on its own; it differs from the population exploitability when the population is a mixture.
  Exploiter-set control (the exact grammar's classes held fixed for the matched arm) is reported as in the unpriced run.
* **Individual mixing** (`mix_pop`), **forfeited plays** (`forfeit_plays`), **self-play forfeit**, resident regret, action
  exploitability: exactly as in `predictions/2026-10-23-rps.md`, computed on the priced classes' action distributions.
  **Cost paid**: the population mean of `c H` over ordered pairs (price units), plus the aggregate net payoff `x' U_c x`
  (game payoffs sum to zero, so it is minus the cost).
* **Reader** = a class whose representative contains an application; **guarded reader** = a class whose representative
  contains both a `coin` and an application; **X** = the class of the representative `X`. "Individual mixing islands" in
  Prediction 2 is read as the island-mean of `mix_pop`, the statistic the unpriced numbers (0.22 / 0.25) quote.
* **Two-arm verdicts.** Where a prediction is about the sample and the exact arm, each arm gets a verdict by the
  prediction's own thresholds; the prediction is **held** if both are held, **failed** if both are failed, **partial**
  otherwise. Where a prediction has conjunctive sub-claims that split, **partial**. "Not scored" only when the cell
  did not complete.
* Cells that fail to complete are reported as such; no verdict is scored on an incomplete cell.

## Predictions (the RE's, verbatim from the spec; falsifiers in brackets)

1. *Statics.* Under any c > 0, `X` invades, and dominates at every frequency of the two-type contest, every class
   whose self-play forfeits with positive probability (`X` pays 0 and earns at least 0 against everyone, +p_f against
   a program that forfeits against it with probability p_f; the reader pays at least c·D·p_f in self-play) [a
   forfeiting class that `X` does not dominate].
   *Scoring:* checked on every program of the n = 6 table (sample, matched, exact, exact-br arms, depth price, each c of the
   panel, tolerance 1e-9): X's priced payoff against every program is >= 0, X pays 0, and for every program r with
   self-play forfeit probability p_f > 0 the fitness difference X - r is linear in the frequency x of X, so dominance at
   every x in [0,1) is the two endpoints: `U_c(X, r) > U_c(r, r)` (invasion) and `U_c(X, X) >= U_c(r, X)`.
2. *Lottery, c = 0.01, sample and exact arms.* Forfeited plays ≤ 0.1 (unpriced 0.69 / 0.52); islands with individual
   mixing ≥ 0.6 (unpriced 0.22 / 0.25); islands with exploitability ≤ 0.05 ≥ 0.6 (unpriced 0.58 / 0.25) [forfeits
   ≥ 0.3, or mixing islands < 0.4].
   *Scoring (per arm, generation 2,000, primary cell):* held if forfeited plays <= 0.1, island-mean `mix_pop` >= 0.6 and
   the share of islands with **net** exploitability <= 0.05 is >= 0.6; failed if forfeited plays >= 0.3 or mixing < 0.4
   (the falsifier); partial otherwise. Two-arm rule above.
3. *Chain, c = 0.01, N = 10⁴.* Exploitability ≤ 0.1 and mixing ≥ 0.6 in sample and exact (unpriced: 0.29 / 0.31 and
   0.43 / 0.31) [exploitability > 0.2 or mixing < 0.4]. The approach is fast: by N = 10³ the chain is within 0.1 of its
   N = 10⁵ values [it is not]. *Counter-prediction (gpt-6.1-sol), registered:* forfeits respond sooner than
   individual-mixing mass; free constants and `X` stay neutral with each other and entry rates still bind, so
   convergence by N = 10³ is far from secure.
   *Scoring (per arm; chain π-weighted):* level: held if **net** exploitability <= 0.1 and mixing >= 0.6 at N = 10^4;
   failed if net exploitability > 0.2 or mixing < 0.4; partial otherwise. Speed: held if |value(10^3) - value(10^5)| <= 0.1
   for both net exploitability and mixing; failed otherwise. The arm's verdict is held if level and speed are both held, failed if the level falsifier trips, partial otherwise (including speed failed with the level held). Two-arm rule above. Counter-prediction (gpt) scored as: in at least
   one of the two arms the N = 10^3 vs 10^5 distance of mixing exceeds 0.1 while the distance of the self-play forfeit
   share is smaller than the mixing distance.
4. *Dose.* c = 0.001 lies between unpriced and c = 0.01 on forfeits and mixing; c = 0.05 is at least as mixed as
   c = 0.01 [non-monotone in c on forfeits]. *Counter-prediction (gpt-6.1-sol), registered:* forfeits decline
   reliably but individual mixing need not be monotone, because a higher price also removes readers that exploit
   constants and can favour population-level mixtures of constants.
   *Scoring (lottery primary cell, sample and exact arms, forfeited plays and island-mean `mix_pop`, paired by founder run
   across c in {0, 0.001, 0.01, 0.05}; chain N = 10^4 reported alongside):* (a) the c = 0.001 point estimate lies weakly
   between the c = 0 and c = 0.01 values on both statistics; (b) mixing(0.05) >= mixing(0.01) (point estimate);
   (c) forfeits are monotone: no step of the sequence c = 0, 0.001, 0.01, 0.05 has a paired run-clustered interval for the
   rise entirely above 0. Held if (a), (b), (c) hold; failed if (c) fails (the falsifier); partial if (c) holds and (a) or
   (b) fails. Two-arm rule above. Counter-prediction (gpt) scored: (c) holds in both arms and in at least one arm the
   mixing sequence has a step down whose paired interval is entirely below 0.
5. *Pure arm.* With no coin, the price removes the readers' free tie, but no program mixes: islands hold constants and
   readers, and statewise (individual) program exploitability stays ≥ 0.3 at every c [≤ 0.1 at any c]. [Revised after
   review] A balanced polymorphism of constants can have zero population exploitability; population exploitability is
   reported without a prediction.
   *Scoring:* the lottery, c in {0.001, 0.01, 0.05}, island-mean **net individual (statewise) exploitability** at generation
   2,000 (own-grammar exploiters; may be negative in the pure arm, which has no `X`). Held if >= 0.3 at all three c; failed
   if <= 0.1 at any c; partial otherwise. The chain at N = 10^4 and the population exploitability and the mixing share
   (which must be 0) are reported beside it.
6. *Who mixes.* At c = 0.01 the coin `X` holds more lottery mass than every source-reading class combined [readers
   hold more]. Low confidence: guarded readers also beat constants, and the chain at c = 0 gave them more mass than
   `X` at large N. *Counter-prediction (gemini-4-argon), registered:* a coin-guarded reader pays about c to read a
   constant and earns +½ to +1 against the constant-heavy founding scramble while avoiding most self-forfeits, so
   guarded readers hold more lottery mass than `X` at c = 0.01; `X` dominates only at c = 0.05 or in the large-N
   chain.
   *Scoring (lottery, generation 2,000, island-mean class shares, then runs; sample and exact arms, matched reported):* held
   if the X class's share exceeds the combined share of all reader classes; failed if the readers' combined share exceeds it.
   Two-arm rule above. Counter-prediction (gemini): held if the combined guarded-reader share exceeds the X share in both
   arms at c = 0.01. The c = 0.05 lottery and the large-N chain (N = 10^5, X share vs guarded share) are reported to
   check the counter-prediction's second clause.
7. *Exact reading.* Exact − matched exploitability is not negative at c = 0.01 in either object [negative, with a
   run-clustered interval excluding 0]. Low confidence.
   *Scoring (net exploitability, own-grammar exploiters; exploiter-set control reported):* lottery: paired exact minus
   matched island-mean (40 runs, run-clustered interval) at generation 2,000; chain: the difference at N = 10^4 (the chain
   has no run interval, so a point difference below -0.01 counts as negative). Held if the lottery interval does not lie
   entirely below 0 and the chain difference is >= -0.01; failed if the lottery interval lies entirely below 0 (the
   falsifier); partial if only the chain point difference is below -0.01.

The RE's confidence (spec): 1 high; 2 medium; 3 medium-low (speed low); 4 medium; 5 medium; 6 low; 7 low.

## Hand predictions of the engineer (from `notes/rps-priced.md` §1; checked by the tests, not scored as RE verdicts)

* The cost table of §1.2 and the priced payoffs of §1.3 for the eleven named programs (e.g. N against a constant 0.99,
  N against N -0.12, GN against N -0.011875, N against GN -0.037344 at c = 0.01).
* Work price equals depth price on the whole n = 6 table in every arm (no body has two applications); the work-price
  sensitivity is informative only at n >= 7 for exact reading of a two-application coin.
* At c > 0 the unpriced stationarity argument pi(X) = mu(X) fails in the direction pi(X) >= mu(X).
* The eleven-class toy chain at c = 0.01: pi mass on X is at least 0.8 at N = 10^4 and the guarded readers hold less than
  0.1; at N = 100 pi is more spread. The toy two-type contests reproduce `chain.Chain`.
