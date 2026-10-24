# Spec: mixed actions in two-role games: the inspection game and Basic Endgame in poker, 2026-10-23

Status: draft by the RE; reviewed by gemini-4-argon (folded [after review]), then gpt-6.1-sol (`--mode amended`, folded [after second review]); to be run
by a Sonnet subagent. Queue items 55 and 56. The RS (2026-10-23): "inspection game sgtm", and Basic Endgame from
C. Ferguson and T. Ferguson, "The endgame in poker" (the RS supplied the paper). Follows RESULTS "Rock–paper–scissors
and mixed actions" and "Rock–paper–scissors with a compute price", and DEFERRED 16. REJECTED.md checked: nothing on
either game; the priced RPS results set the conventions reused here and re-open nothing.

## Why

In RPS a reader can at best match the coin: the coin earns the value against everyone, so selection never strictly
favours a reader over it, and the priced lottery was held by the free coin `X`. These two games are where seeing the
other side's randomization can be worth more than flipping blind.

1. **Inspection (non-zero-sum).** An inspector inspects with some probability; an inspectee complies or cheats. In
   the mixed Nash equilibrium both randomize and the inspector does badly. An inspector whose inspection probability
   is visible and just high enough to deter does much better (the Stackelberg commitment value). Source code makes
   every inspector's probability visible, so reading inspectees should select committed inspectors: the prediction is
   the commitment outcome, not Nash.
2. **Basic Endgame (zero-sum, hidden information).** Player I sees a card that wins with probability P; II does not.
   I bets or checks; after a bet, II calls or folds. A reader of I's source sees I's bluffing rate but not the card,
   a third kind of thing a reader cannot see besides how a coin lands. The paper's closed form gives the target.

## Games

**Inspection.** Inspector: inspect (I) or not (N). Inspectee: comply (C) or cheat (K). Payoffs (inspector, inspectee):
(I, C) = (−1, 0); (I, K) = (−1, −3); (N, C) = (0, 0); (N, K) = (−4, +1). Inspection costs h = 1, undetected cheating
costs the inspector L = 4, cheating gains g = 1 and a caught cheat pays f = 3. Mixed Nash: inspect with probability
p* = g/(g + f) = 1/4, cheat with probability q* = h/L = 1/4; payoffs (−1, 0). Commitment: an inspector visibly
inspecting with p > 1/4 makes cheating strictly worse than complying, so a best-responding inspectee complies and the
inspector earns −p. On the dyadic grid a grammar of size n can express, the commitment target is the smallest
expressible p > 1/4, against Nash −1. [After review] Fair binary coins reach denominators 2 at size ≤ 3, 4 at size 5,
8 at size 7 and 16 at size 9, so at n = 6 the only blind probability above 1/4 is 1/2 (`X`), which cannot separate
commitment from `X`'s prior mass. The inspection grammar therefore runs at **n = 8**, where p = 3/8 exists (payoff
−0.375, commitment) beside p = 1/2 (−0.5, the one-node coin). At exactly
p = 1/4 a reader is indifferent and breaks the tie by its own coin (as `cr` does in RPS).

**Basic Endgame** (the paper's §1) with a = 1, b = 2 (pot limit), P = 1/3. The all-strategies-active case applies
(P < (2a + b)/(2a + 2b) = 2/3). I always bets a winning card (the paper's convention; a program that checks a winner is
allowed and is dominated). [After review] The equilibrium bluffer `card BET (coin (coin BET CHECK) CHECK)` has 7 nodes, so
Endgame runs at **n = 7** for both roles. With a losing card I bluffs with probability π = (b/(2a + b))·P/(1 − P) = 1/4; II folds with
probability b/(2a + b) = 1/2; the value is 2aP(2a + 2b)/(2a + b) − a = 0. These are dyadic, so fair coins can express
the equilibrium exactly. Payoffs to I: check with a winner +a, with a loser −a; bet and fold +a; bet and call ±(a + b).

## Programs

Fixed roles, one population per role. Each role's grammar is RPS's (constants, `X`, `coin A A`, application, `↑`) with
role-specific constants and three additions:
- **constants:** inspector {I, N}, inspectee {C, K}; Endgame I {BET, CHECK}, II {CALL, FOLD}. `X` is the fair coin over
  the role's two actions.
- **`card A B`** (Endgame I only): A if the card wins, else B.
- **`if Q = α then A else B`**: Q is an application (the opponent's simulated action against me), α a constant of the
  opponent's role. When II simulates I, the simulation draws a fresh card from P, independent of the real card.
- **`cr`** (exact arms): the exact best response to the opponent's exact action distribution against me, with ties
  broken by the reader's own coin. For Endgame II it uses the joint distribution of I's card and action (the posterior
  that a bet is a bluff); for Endgame I it best-responds card by card; for the inspection roles it best-responds to the
  opponent's probability. [After review] `cr` consumes one depth level and computes the opponent's exact distribution
  on the remaining budget D − d; at d = D it forfeits (paying c·D). [After second review] A depth-sensitive opponent can
  behave differently with less budget than in its own root evaluation, so `cr` is a *bounded* exact counter: the
  report compares, for every nested-reader pair in the support and every cap-boundary program, the distribution `cr`
  computed with the opponent's actual distribution, and counts disagreements. If the opponent never bets (P(BET) = 0), Endgame II's
  posterior is undefined and II is payoff-indifferent, so `cr` breaks the tie with its own coin. `cr` is charged only
  when evaluated.

**Non-termination and price** (RESULTS "Rock–paper–scissors with a compute price"): depth cap D = 12; the depth price c
per application level, so a forfeit pays c·D; a forfeit plays the forfeiting role's worst action against the
realized opponent action. Main price c = 0.01; [after review] **c = 0 is a required control**, not a reference: at
c > 0 a reading follower pays to comply where the constant C complies for free, so c = 0 separates "reading cannot
sustain commitment" from "the price taxes the reader".

**Arms:** *sample* (coins, simulation), *exact* (sample plus `cr`), *matched* (exact with `cr` replaced by a simulating
counterpart of the same size), *blind* (constants and coins only, no application: no program reads; [after second
review] Endgame I keeps `card` in every arm, so blind removes only reading of the opponent, not private information).
n = 8 for inspection and n = 7 for Endgame (above), the repo's length prior.
[After second review] **The matched counterpart is `sr`**, a one-node unary operator like `cr`: it draws one simulated
opponent action (fresh coins and card) and plays the pure best response to that draw, charged one depth level as `cr`
is. Its prior weight and size equal `cr`'s by construction; the report audits this after class reduction, and reports
the work each `cr` evaluation performs (exact enumeration is a subsidy). **Sampling responders** `sr_k`, k ∈ {4, 16}
(best response to the empirical distribution of k independent simulated draws, ties by own coin, charged k levels),
run as inspectee controls in the inspection exact arm.

## Objects

1. **The ε → 0 chain** over pairs of monomorphic role classes (the fixed-role chain used for the union game and the
   auctions), `chain_log.LogChain` with closure-seeded exploration and replicator attractor search, w = 0.3,
   N ∈ {10², 10³, 10⁴}; any cycle or unresolved attractor is indeterminate (THEORY §5). Two-population matching-pennies
   dynamics cycle around the mixed equilibrium, so cycles are expected in the blind arm.
2. **The ε = 0 seed lottery:** N = 100 per role, 64 islands, mN = 1, 40 runs, horizon 2,000 with continuation of runs
   0–9 (fixed in advance) to 10,000, paired founders across arms, run-clustered intervals. Verdicts use generation
   2,000, with the mean over generations 1,500–2,000 reported beside it. [After second review] Size panel: (400, 16),
   20 runs, inspection exact arm at c = 0 and c = 0.01; otherwise conclusions are limited to N = 100.

## Statistics

- **Inspection:** the inspector population's inspection probability (mass-weighted distribution, and the share above,
  at and below 1/4); the inspectee's cheat probability; the share of inspectees that read (`cr` or `if`); mean payoffs
  of both roles against the Nash (−1, 0) and commitment (−p_min, 0) references; [after review] inspector mass at
  p = 3/8 (commitment) against p = 1/2 (`X`, prior mass), and the share of compliant constants among inspectees.
- **Endgame:** I's bluff probability with a losing card, II's call probability, both against (1/4, 1/2); the value
  realized against 0; exploitability of each role's population (the best payoff any program of the opposite role's
  grammar earns against it, net of its own cost).
- Both: individual mixing, cost paid, forfeits, the named classes' shares, support and transitions (CLAUDE.md rule 4).
- [After second review] Pairwise invasion rates along the predicted inspection ladder (reader → C → N → K → back),
  measured as transitions, not inferred from shares; encounter-conditioned action distributions and action
  correlations (marginals cannot identify equilibrium among source-responsive programs); Endgame I's winner-betting
  rate.
- [After second review] These games test commitment and exploitability, not Pareto efficiency: (N, C) = (0, 0)
  dominates the commitment payoff (−3/8, 0) in inspection, and Endgame is zero-sum.

## Predictions (the RE's; falsifiers in brackets)

1. *Statics.* The hand table in the notes (Nash, the commitment grid, Endgame's equilibrium) matches the evaluator.
   [Corrected after second review] In Endgame the equilibrium mixers satisfy the minimax inequalities: each earns at
   least the value against every opponent program, with equality against the opponent's equilibrium-support
   strategies (II's coin gains strictly when I checks a winner) [any mismatch].
2. *Inspection, exact arm, lottery.* [Revised after review: a committed inspector makes the reader's best response
   the pure action C, so the constant C is a shadow of the reader: neutral at c = 0, a strict invader at c > 0. Once
   C replaces the readers, N invades the committed inspectors and K invades N.] At **c = 0**: readers hold at least
   0.5 of the inspectee population, more inspector mass sits at 3/8 than at 1/2, and the mean inspector payoff is
   above −0.6 (Nash −1) [reader share < 0.3, or mean inspector payoff below −0.8]. Low confidence. *Counter-prediction
   (gpt-6.1-sol), registered:* at c = 0 nothing selects readers over their compliant shadow C, so reader share depends
   on founders and the prior, and commitment, if seen, may be a transient. At **c = 0.01**: the compliance
   shadow erodes commitment, so the mean inspector payoff is below the c = 0 value by at least 0.1 [not lower].
   *Counter-prediction (gemini-4-argon), registered:* at c = 0.01 the reader share stays below 0.5 and the inspector
   payoff below −0.5, near −0.7 or cycling; commitment holds only at c = 0 or with 3/8 in the grammar.
3. *Inspection, blind arm:* no commitment can be read, so the inspector payoff stays near Nash or below (mean ≤ −0.8)
   and the chain is indeterminate (two-population cycling) [mean above −0.5].
4. *Inspection, sample vs exact:* [revised after second review] a one-draw responder cannot tell 3/8 from 1/4, and k
   draws tell them apart only noisily, so the commitment payoff is graded in the responder's information: at c = 0 the
   mean inspector payoff orders exact ≥ sr_16 ≥ sr_4 ≥ matched (sr), and exact − matched ≥ 0.2 [exact − matched ≤ 0].
   *Counter-prediction (gpt-6.1-sol), registered:* the advantage is graded by sample budget, and a gap of 0.2 is not
   justified. *Counter-prediction (gemini-4-argon), registered:* the
   compliance shadow makes exact − matched near 0.
5. *Endgame, exact arm, c = 0.01, lottery:* the mass-weighted bluff probability is within 0.1 of 1/4 and the call
   probability within 0.1 of 1/2 on at least 0.6 of islands; the realized value is within 0.1 of 0 [either within-0.1
   share below 0.3].
6. *Endgame, who mixes:* as in RPS, coin programs at the equilibrium rates (`card BET (coin (coin BET CHECK) CHECK)`
   for I, `X` for II) hold most of the mass, and II's exact readers do not beat them [readers hold more than half of
   II's mass]. Low confidence: unlike RPS, II's exact reader computes a posterior that a coin cannot.

## Required outputs

- *Code:* `src/mixed2.py` (role grammars, exact evaluator with hidden cards, price), `src/mixed2_run.py`,
  `src/mixed2_report.py`, reusing `src/rps*.py`, `src/rps_priced*.py`, `src/chain_log.py` and an existing fixed-role
  chain and lottery (look at the auction or union-game modules) by import; no existing file edited.
- *Tests:* `tests/test_mixed2.py`: the hand table for both games, the posterior computation of II's `cr`, the fresh
  card in simulation, the price at c = 0.
- *Notes:* `notes/mixed2.md` (§1 hand table before code; §2 deviations).
- *Predictions:* `predictions/2026-10-23-two-role-mixed.md`, before any counted cell, with the RS's statements first.
- *Runs:* `runs/mixed2/` (small files only), verdicts in `runs/mixed2.md` and `.json`.
- *Hand back* RESULTS, REJECTED, THEORY and NOTATION drafts; do not edit the shared docs.

**Budget and scale guard.** At most 3 workers, capped by memory; one job per process; no `multiprocessing.Pool`.
Waiting: watch short commands; for long batches wait on one background command that exits at completion and also
fires if the log stops changing for 2 hours; never poll periodically. Cut order if needed (disclose): the 10,000
continuation, the size panel, sr_4, the chain at N = 10⁴, the matched arm in Endgame, Endgame at c = 0. Never cut
inspection at c = 0.
