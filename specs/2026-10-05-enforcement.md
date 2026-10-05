# Spec: incentive-compatible enforcement in the union game, and the unfakeable-polarity pact, 2026-10-05

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-05-enforcement-gpt-6.1-sol.md`) and revised; changes marked
[after review]. To be run by an Opus subagent. Queue item 5
(CLAUDE.md); sol's "beyond this experiment" note on the union spec and DEFERRED 10. Mostly cheap: static tables and
the reduced canonical chain, with two full-chain cells.

## Why

The union game (RESULTS "The union game") found that under the length prior the boss takes almost everything, that
the prior and not the institution decides the fair share (0.31 under a uniform prior over the named programs, 0.001
under the length prior), that the quorum is FairBot's handshake on strikes, and that a strike pact's wage check has
the fakeable polarity: "strike iff provably low" is fooled by a boss that pays fair only at the bottom world. Sol's
follow-up: in that game both repression and collective withdrawal are *committed program policies* with no
within-encounter incentive check, so the result says nothing about which institution survives when enforcement has
to pay for itself. The RS's normative interest (2026-10-04) is exactly that "our setup renders a whole bunch of
threats difficult to enforce". Two questions, then:

1. **Which side's commitment carries the fair share?** Ablate commitment on each side separately: whose threat is
   doing the work in the 0.31, and what happens to the wage when a side's enforcement must be ex-post rational.
2. **Does the unfakeable polarity carry a pact?** The RE's re-reading of the polarity dilemma: the sucker polarity is
   "strike iff □(low)", which fails against a boss whose low wage is *unprovable* (the legibility shield of RESULTS
   "The symmetric gate", transposed). The other polarity, "strike iff ¬□(fair) ∧ □(other strikes)", strikes against
   every boss whose fairness is unprovable, and by Lemma 0 (box soundness at the stable world) no boss can be judged
   fair while paying low. Its only error is self-harming (striking against a fair boss that is illegible), not
   exploitable. The union run's claim that this polarity "cannot carry a strike pact" was made for the set-atom
   grammar, where negated wage boxes broke the militant's provability; it needs a direct check.
   [after review] Sol's objection, that soundness excludes false fairness certificates but does not make two union⁻
   workers able to prove each other's strikes, is right, and the RE's hand evaluation on the Kripke chain shows why:
   every box is vacuously true at world 0, so ¬□(fair) is *false* at world 0, no union⁻ strikes there, and a level-0
   handshake □(other strikes), which needs strikes at every earlier world, can never become true. With a level-1
   handshake □₁(other strikes) (worlds ≥ 1 only, the PrudentBot device) the pact does start against a constant
   low-paying boss (strike from world 1 on), but against the bottom-world wage faker (fair at world 0, low after)
   ¬□(fair) becomes true only at world 2, by which time the level-1 handshake needs a strike at world 1 that did not
   happen. So in the two-level language the unfakeable polarity's pact is defeated by the same faker, through the
   handshake rather than the wage check, and pushing the handshake up a level only moves the faker up a world (the
   sibling theorem's regress). Part A is therefore a static check of this derivation, not a chain experiment.

## Design

**Game and language** as in `specs/2026-10-05-union.md` and `src/union*.py`: boss slot (s ∈ {0, 1/4, 1/2}, whack
policy h ∈ {strike targeting, none, source targeting}, cost c per whack, striker's loss L = 1), two worker slots,
fixed roles, separate populations; c ∈ {0.1, 0.5}; w = 0.3.

**Part A: the unfakeable-polarity union (static only) [after review].**
- Worker programs: `militant⁻` = `if(not(BOX(s = 1/2)), strike, work)`; `union⁻₀` = `if(and(not(BOX(s = 1/2)),
  BOX(OTHER = strike)), strike, work)`; `union⁻₁` = the same with `BOX1(OTHER = strike)`; and the BOX1 wage-check
  twins of each. If the grammar's set atoms cannot express the negated single-wage box, add it as an atom for this
  static part only and say so.
- Tabulate, with the box truth values world by world: union⁻ₗ/union⁻ₗ, union⁻ₗ/militant⁻, and mixed BOX/BOX1 pairs
  against the constant-low, constant-intermediate and constant-fair bosses and against the wage-faker classes of
  the union run (bosses fair only at the bottom world, and any fair-until-world-1 class at n = 6). Record actions
  and the relevant box values at each world until stabilization.
- Confirm by evaluator over every boss class at n = 6 that no boss is judged fair (□fair true at the stable world)
  while paying low there (0 counterexamples required, dependency on Lemma 0 stated; this tests implementation
  consistency at n = 6, not unfakeability throughout the language), and count the fair bosses that are struck with
  their μ mass.
- No chain runs in Part A unless the static tables contradict the derivation above (then one reduced-chain cell
  under each prior, c = 0.5, N = 10³, with a fixed-mass substitution of union⁻₁ for union, masses frozen).

**Part B: the commitment ablation (reduced chain, both priors) [after review: extensive form, box referents and
best responses specified].**

*Extensive form of one encounter.* Stage 1: the boss's wage s is committed (program output; it stays committed in
every arm, so RR is "both enforcement moves uncommitted", not "nothing committed"). Stage 2: the workers' strike/work
and the boss's whack policy are each either committed (program output) or ex-post rational, per arm. *Box referents:*
every box refers to **implemented actions**, after any override. The override is applied inside the evaluator at
each world (a program's value at world n is its recommendation, then the best response given the other slots' values
at that world and the full payoff table including L, c and the pool), so values stay per-world, boxes stay "true at
every earlier world", monotonicity and stabilization are unchanged, and Lemma 0's soundness argument goes through
unchanged; the subagent must re-run the box audit on the modified evaluator (0 violations required). *Best
responses* are computed from the complete payoff table conditional on this timing, never from a verbal shortcut:
a worker's deviation payoff includes the loss L if the boss's (committed or rational) policy would whack it, and
source-targeted whacking of workers who work. *Tie-breaking:* indifference resolves to the program's committed
recommendation; the exact boundary 1 − s = c (s = 1/2, c = 1/2) is included and declared as "whack" for the
rational boss (and reported both ways).

Arms, each run **with and without the replacement pool** (2 × 2 × 2 = 8 cells per prior and c) [after review: the
pool changes the economy, so it is crossed with commitment rather than tied to RC]:
- (CC) both enforcement moves committed: the union run's game;
- (RC) boss's whack is ex-post rational: it whacks a striker only if whacking raises its payoff in this encounter;
  without the pool this never holds at c > 0, with the pool it holds iff 1 − s ≥ c, where the **replacement pool**
  means a whacked striker is replaced by an outside scab whose product 1 − s the boss recovers;
- (CR) workers' strike is ex-post rational;
- (RR) both ex-post rational.
Report, per cell: the fair / intermediate / zero-wage / strike / repression shares, worker and boss mean payoffs,
realized total surplus and payoff-vector dominance (repression costs and replacement product included), support and
transitions; strike incidence separately from repression conditional on a strike; and for each committed threat its
payoff advantage over the feasible deviation (not only how often a noncredible threat is executed). Grammar masses
are frozen across arms (the arms change the evaluator, not the language).

**Part C (one full-chain cell, cheap only if Part A's code makes it so):** (RC with pool) on the full language at the
length prior, c = 0.5, N = 10³, to see whether incentive-compatible repression changes the full-chain picture.

## Required outputs

`runs/enforcement.md` and `.json` (every table with support and transitions; static tables as a section), code in
`src/union_enforcement.py` (extending `src/union*.py`), a predictions file from the spec committed before any
counted run, and the usual hand-back (draft RESULTS, REJECTED, THEORY §9.9 and §9.11 edits, DEFERRED 6 and 10
edits, NOTATION, ≤ 5 lines on what matters, branch from `git branch --show-current`, commits). ≤ 3 workers; the
three-player solver's log-scaled GTH as in `src/dollar3*.py` / `src/union_chain.py`.

## RE predictions (with falsifiers)

1. **No polarity in the two-level language carries a pact against every low-paying boss** [after review: replaces
   the RE's first draft, which conflated soundness with pact activation]. union⁻₀ pairs never strike (¬□fair is
   false at world 0); union⁻₁ pairs strike against every *constant* low-paying boss and work against the
   bottom-world wage faker; no boss class is judged fair while paying low at the stable world (0 counterexamples);
   and the self-harming errors (fair bosses struck by militant⁻) have μ mass < 0.05 of the boss language.
   *Falsifier:* a union⁻ variant that strikes against every low-paying class including the fakers, or a boss judged
   fair while paying low.
2. **Commitment ablation under the uniform prior, c = 0.5, no pool: the workers' commitment carries the fair share,
   the boss's does not.** (CR) and (RR) give fair ≤ 0.05 and zero wage ≥ 0.8; (RC) is within 0.05 of (CC) on every
   share. *Falsifier:* (CR) fair ≥ 0.2, or (RC) differing from (CC) by ≥ 0.15 on the fair share.
3. **The pool suppresses the wage through restored production, in both CC and RC alike** [after review: sol's
   reading; the RE's "free of the commitment cost" rationale was wrong, since rational repression still pays c when
   executed]. With the pool, fair falls by ≥ 0.1 relative to the matched no-pool arm in both (CC) and (RC), and
   (RC with pool) is within 0.05 of (CC with pool); repression conditional on a strike rises with the pool while
   strike incidence falls. *Falsifier:* the pool not lowering fair in (CC), or (RC) and (CC) with pool differing by
   ≥ 0.15.
4. **Under the length prior every cell gives zero wage ≥ 0.95:** no commitment structure or pool rescues the
   workers from the prior. *Falsifier:* any cell with fair ≥ 0.1 under the length prior.
5. **Part C:** the full-chain (RC with pool) cell has repression conditional on a strike ≥ 0.5 and fair ≤ 0.01.
   *Falsifier:* repression conditional on a strike < 0.2.

The RS is invited to add predictions; the uncertain one is 3's "within 0.05" clause (whether avoiding unprofitable
executions is worth anything once the pool exists).
