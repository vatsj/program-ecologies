# Predictions: the scramble lemma and Claim A (no dangerous fakers for the prover family) (2026-10-05)

Spec: `specs/2026-10-05-scramble-lemma.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-05-scramble-lemma-gpt-6.1-sol.md`).
Mostly theory with static checks (n ≤ 12) and one cheap simulation (neutral-lineage control). Committed before the
static checks and the simulation. Proofs go to `notes/scramble-lemma.md`; numbers to `runs/scramble-lemma.{md,json}`.

Prover family P = {FairBot `BOX(THEM(ME))`, `BOX1(THEM(ME))`, `BOX(THEM(THEM))`, `BOX1(THEM(THEM))`,
`BOX(THEM(^C))`, `BOX1(THEM(^C))`}. A *faker* q of x: q defects on x while x cooperates with q. A *non-establisher*:
q does not both defect on D and self-cooperate.

## RE predictions (Fable, copied from the spec)

1. **Claim A holds** for all six members at every n, with the FairBot pair by soundness, the probe-readers in one
   line, and the THEM(THEM) pair by a short case analysis. *Falsifier:* a non-establisher faker of a member of P that
   defects on both D and ALLC, found by enumeration or constructed.
2. **Claim B holds as a first-moment bound** of the form q̄ ≤ exp(−∫_{window} w·(f̄ − f_q) dt) up to demographic
   constants, conditional on E, and it is within a factor of 10 of the measured per-copy survivals at N = 100 and 400.
   The neutral-lineage comparison shows that selection, not demographic extinction alone, accounts for at least half
   of the log-survival deficit. *Falsifier:* no bound of that form, or a bound off by more than 100×, or neutral
   survival equal to the faker's within a factor of 1.5.
3. **The combined bound is positive and uniform in n** for the family P, stated in inf units: P is a fixed finite set,
   its raw mass under the infinite length prior is a constant, and the bound is stated with the inf-unit mass and the
   conditional seed probabilities under E. *Falsifier:* an n-dependence of the bound that is not through the
   normalization of μ_P or through P(E).

## RE notes added by the executing subagent before the checks

- Sol's review predicts the THEM(THEM) case is either vacuous (no non-establisher fakers at all, if the box is sound
  for actual self-cooperation) or exposes a level/world mismatch. The static data already show non-establisher fakers
  of `BOX1(THEM(THEM))` that self-cooperate and cooperate with D (e.g. `not(BOX(THEM(ME)))`), so the case is not
  vacuous; Claim A for this pair rests on "self-cooperating non-establisher ⇒ cooperates with D", which is the
  definition, provided soundness gives actual self-cooperation. Checked exhaustively at n = 12.
- Expected looseness of B: the first-moment bound ignores the drift-free extinction of a rare lineage, so it should be
  an upper bound that is loose by the neutral survival factor unless the neutral factor is put in by hand.

## What would change the plan

If A fails for a member, report the counterexample (evaluator-checked) and state the largest sub-family for which A
holds. If B has no bound of the stated form, report the obstruction.
