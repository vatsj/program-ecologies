# Predictions: mixed actions in two-role games, the inspection game and Basic Endgame, 2026-10-23

Spec `specs/2026-10-23-two-role-mixed.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in amended mode; both folded). Hand
derivations: `notes/mixed2.md` §1 (committed before any code). Written and committed before any code runs and before any
counted cell. Chain numbers are ε→0 chain quantities (π over pairs of monomorphic role classes), lottery numbers are
ε = 0 seed-lottery statistics at finite (N, I, horizon), never π. Scoring: held / failed / partial / not scored, each
with the number, in `runs/mixed2.md` and `.json`.

## The RS's statements (2026-10-23; quoted in the spec)

* "I suspect we're gonna need strong notions of mixed actions to recover equilibria in adversarial games." (the standing
  hypothesis, RS 2026-10-23, from the RPS spec).
* "inspection game sgtm" (the RS, 2026-10-23), and Basic Endgame from C. Ferguson and T. Ferguson, "The endgame in poker"
  (the RS supplied the paper).

The RE's reading of the inspection statement: the game is a test of whether source reading selects the *commitment*
outcome (a visibly committed inspector, a complying reader) over Nash, not of whether the mixed equilibrium is recovered;
Basic Endgame is the test of the RS's hypothesis proper (is the equilibrium of a zero-sum game with hidden information
recovered, and by what).

## Scoring conventions fixed here (engineer, before any code), so no threshold can move afterwards

* **Cells.** Inspection at n = 8, Endgame at n = 7, D = 12, w = 0.3, length prior in bits (`notes/rps.md` §2), arms blind /
  sample / exact / matched (`sr`), plus `sr_4` and `sr_16` in the inspection exact family (the operator `cr` replaced by
  `sr_k` in both roles). Prices c in {0, 0.01}. The blind arm has no reading and pays nothing, so it is one cell per game.
  Endgame I keeps `card` in every arm.
* **Chain.** ε → 0 chain over pairs of monomorphic role classes (two-population constant selection, Moran fixation with
  fitness exp(w·net payoff), mutation to a role chosen with probability 1/2 from that role's prior), N in {10², 10³, 10⁴},
  closure-seeded exploration, log-domain GTH. Cycles (below) are reported as indeterminate and their mass is not a
  stationary claim. The chain is a diagnostic.
* **Cycle / indeterminate.** A closed communicating class of the graph of weakly improving single-mutant moves
  (Δ >= 0 for the mutant) that contains a strictly improving move inside it is a *cycle class*; a closed class with only
  neutral moves is a *drift set*; a singleton is a *rest point*. The chain's mass on cycle classes is reported as
  `pi_cycle`; "indeterminate" means `pi_cycle` >= 0.5.
* **Lottery.** ε = 0 islands, N = 100 per role, I = 64, mN = 1, 40 runs, complete graph, horizon 2,000 (verdicts) with the
  mean over generations 1,500–2,000 (every 10) reported beside, runs 0–9 continued to 10,000 (runs fixed in advance),
  founders drawn per slot from the length prior with common random numbers across arms (paired on size and quantile),
  run-clustered 95% bootstrap intervals (4,000 resamples of runs), paired contrasts across arms and prices. Size panel
  (400, 16), 20 runs, inspection exact arm at c = 0 and c = 0.01. Statistics are island means, then run means.
* **Payoffs in verdicts.** Mean inspector (resp. player I) payoff is the **game payoff** (gross of the compute price), the
  quantity the commitment and Nash references are stated in; the net payoff (gross minus the program's own price) is
  reported beside it. Exploitability is net (the exploiter's game payoff minus its own price), gross reported beside.
* **Readers.** A *reader* class is a class whose representative (smallest size, then id) contains an application;
  *exact reader*: contains `cr`; *sampling reader*: contains `if` or `sr`. The behavioural "reads" share (action
  distribution varies across the island's opposing classes by more than 10⁻⁶ in total variation) is reported beside it.
  The class of `C` (resp. `X`) is the class whose representative is that atom. *Inspector mass at p*: the share of
  inspector population mass whose probability of inspecting against the island's inspectee population is within 5·10⁻³
  of p. *Committed* inspector: p > 1/4 + 5·10⁻³.
* **Two-arm and conjunctive rules.** A prediction with sub-claims is *held* if all sub-claims hold, *failed* if the stated
  falsifier trips, *partial* otherwise ("not scored" only when a required cell did not complete). Where a prediction names
  a counter-prediction, the counter-prediction gets its own held/failed line by the rule stated with it below.

## Predictions (the RE's, verbatim from the spec; falsifiers in brackets)

1. *Statics.* The hand table in the notes (Nash, the commitment grid, Endgame's equilibrium) matches the evaluator.
   [Corrected after second review] In Endgame the equilibrium mixers satisfy the minimax inequalities: each earns at
   least the value against every opponent program, with equality against the opponent's equilibrium-support
   strategies (II's coin gains strictly when I checks a winner) [any mismatch].
   *Scoring:* held iff (a) every entry of the notes' two payoff tables, the effective-q formulas, the depths and the
   dyadic grid matches the evaluator to 10⁻⁹; (b) over the whole n = 7 table, `EQ` (the class of
   `card BET (coin X CHECK)`) earns >= −10⁻⁹ against every II program, and II's `X` earns >= −10⁻⁹ against every I
   program, with the stated equalities (EQ vs every non-forfeiting II program equals 0 within 10⁻⁹; `X` strictly
   positive against `CHECK` and `XI`). Failed on any mismatch beyond 10⁻⁹.
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
   *Scoring (lottery, generation 2,000, exact arm, island means then run means):* part (a), c = 0: held iff reader share
   (inspectees) >= 0.5 and inspector mass at 3/8 > inspector mass at 1/2 and mean inspector payoff > −0.6; failed iff
   reader share < 0.3 or mean inspector payoff < −0.8; partial otherwise. Part (b), c = 0.01: held iff the paired
   (run-by-run) mean inspector payoff at c = 0.01 is below the c = 0 value by >= 0.1 (point estimate); failed iff it is
   not lower (difference >= 0); partial otherwise. The prediction is held iff (a) and (b) held, failed iff both are
   failed, partial otherwise. *gpt-6.1-sol:* held iff the run-to-run standard deviation of the c = 0 reader share is
   >= 0.2 or the continuation (runs 0–9) inspector payoff at 10,000 generations is lower than at 2,000 by >= 0.1.
   *gemini-4-argon:* held iff at c = 0.01 the inspectee reader share < 0.5 and the mean inspector payoff < −0.5. The
   mass at the commitment point 5/16 (the smallest grid point above 1/4 at n = 8, `notes/mixed2.md` §1.1) is reported
   beside the 3/8 and 1/2 masses and is not part of the verdict.
3. *Inspection, blind arm:* no commitment can be read, so the inspector payoff stays near Nash or below (mean ≤ −0.8)
   and the chain is indeterminate (two-population cycling) [mean above −0.5].
   *Scoring:* lottery, blind arm (one cell, price irrelevant), generation 2,000 mean inspector payoff: held iff <= −0.8
   and the chain at N = 10⁴ has `pi_cycle` >= 0.5; failed iff the lottery mean is > −0.5; partial otherwise.
4. *Inspection, sample vs exact:* [revised after second review] a one-draw responder cannot tell 3/8 from 1/4, and k
   draws tell them apart only noisily, so the commitment payoff is graded in the responder's information: at c = 0 the
   mean inspector payoff orders exact ≥ sr_16 ≥ sr_4 ≥ matched (sr), and exact − matched ≥ 0.2 [exact − matched ≤ 0].
   *Counter-prediction (gpt-6.1-sol), registered:* the advantage is graded by sample budget, and a gap of 0.2 is not
   justified. *Counter-prediction (gemini-4-argon), registered:* the
   compliance shadow makes exact − matched near 0.
   *Scoring (lottery, c = 0, generation 2,000, paired by founder run, point estimates plus run-clustered interval for the
   gap):* held iff the point estimates satisfy exact >= sr_16 >= sr_4 >= matched and exact − matched >= 0.2; failed iff
   exact − matched <= 0; partial otherwise. *gpt-6.1-sol:* held iff exact − matched < 0.2 and matched <= sr_4 <= sr_16 <=
   exact at the point estimates (graded, small). *gemini-4-argon:* held iff |exact − matched| < 0.1.
5. *Endgame, exact arm, c = 0.01, lottery:* the mass-weighted bluff probability is within 0.1 of 1/4 and the call
   probability within 0.1 of 1/2 on at least 0.6 of islands; the realized value is within 0.1 of 0 [either within-0.1
   share below 0.3].
   *Scoring (generation 2,000):* per island, the bluff probability is I's population mean of P(bet | loser) against that
   island's II population, the call probability II's population mean of P(call | acting); the value is I's mean game
   payoff on the island. Held iff the share of islands with both within 0.1 is >= 0.6 and the run-mean realized value is
   within 0.1 of 0; failed iff the share of islands with the bluff within 0.1 is < 0.3 or the share with the call within
   0.1 is < 0.3; partial otherwise.
6. *Endgame, who mixes:* as in RPS, coin programs at the equilibrium rates (`card BET (coin (coin BET CHECK) CHECK)`
   for I, `X` for II) hold most of the mass, and II's exact readers do not beat them [readers hold more than half of
   II's mass]. Low confidence: unlike RPS, II's exact reader computes a posterior that a coin cannot.
   *Scoring (lottery, exact arm, c = 0.01, generation 2,000, run means):* held iff the class of `EQ` holds more than 0.5
   of I's mass, the class of `X` more than 0.5 of II's mass, and II's reader classes together hold <= 0.5; failed iff II's
   reader classes together hold > 0.5; partial otherwise. Matched and c = 0 reported beside.

The RE's confidence (spec): 1 high; 2 low; 3 medium; 4 low; 5 medium; 6 low.

## Hand predictions of the engineer (from `notes/mixed2.md` §1; checked by the tests, not scored as RE verdicts)

* The inspection table of §1.1: Nash (1/4, 1/4) with payoffs (−1, 0); commitment −p at visible p > 1/4, −7/4 at exactly 1/4
  against a coin-tie-breaking reader; the smallest grid point above 1/4 at n = 8 is 5/16 (size 7), then 3/8 (size 5).
* The Endgame table of §1.2: U_I(w, l, q) = −1/3 + (2/3) w q + (4/3) l (1 − 2q), equilibrium (w, l, q) = (1, 1/4, 1/2),
  value 0; reader entries as tabulated (e.g. `HON` against `RII` −1/9, `BET` against `SRII` −1/3, `EXP` against `X` 0).
* Mutual forfeits pay (−4, −3) in inspection and (−3, −3) in Endgame and cost 12 levels each; `sr(THEM(ME))` is
  behaviourally the one-sample conditional program in inspection.
* In the blind inspection arm the monomorphic-pair chain has the strict best-response cycle (I, C) → (N, C) → (N, K) →
  (I, K) → (I, C) among constants; no monomorphic pair of the blind arm is a rest point of weak improvement, so the
  chain's recurrent mass sits on cycle classes or drift sets.
