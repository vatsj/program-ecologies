# Spec: the scramble lemma, and the absence of D-tying fakers for the prover family (theory), 2026-10-05

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-05-scramble-lemma-gpt-6.1-sol.md`) and revised; changes marked [after review]. Committed before launch. To be run by an Opus subagent. Mostly theory, with static checks.

## Why

"Almost all seeds" (THEORY §3) now has both halves measured for the modal arm at n ≤ 12: establishment is rigorously
positive uniformly in the cutoff, and a co-seeded faker is a bounded discount because it dies in the scramble (RESULTS
"Spoiler-conditioned establishment"). Two statements would turn that into a theorem for this language family:

**Claim A (no dangerous fakers).** For every member x of the prover family P = {FairBot `BOX(THEM(ME))`,
`BOX1(THEM(ME))`, `BOX(THEM(THEM))`, `BOX1(THEM(THEM))`, `BOX(THEM(^C))`, `BOX1(THEM(^C))`}, and at every cutoff n,
every *non-establisher* faker q of x (q defects on x while x cooperates with q, and q does not self-cooperate) is
strictly worse than D in a population of {D, ALLC}: it cooperates with D, or cooperates with ALLC, or both.

**Claim B (the scramble lemma)** [after review: restated]. In a single island seeded iid from μ at size N, a
non-establisher faker q of x has a per-copy probability of surviving to the island's ALLC extinction bounded above by
a function of its integrated fitness deficit *relative to the population mean*, ∫ w·[f̄(t) − f_q(t)] dt, over the
window in which f_q < f̄. Three things sol pointed out, which the proof must handle rather than assume:
- the deficit against D is type-specific: a faker that cooperates with D loses (P − S)·x_D(t) to D, one that cooperates
  with ALLC loses (T − R)·x_A(t), one that does both loses both; other seeded programs can shift the ranking, so the
  deficit is derived against the actual population, with the remainder bounded by its mass;
- losing to D is not subcriticality: a Moran lineage grows at w·(f_q − f̄), and a D-cooperating faker that defects on
  ALLC can be *above* the mean while ALLC is rich. So the bound is on the window after the faker drops below the mean,
  and the exposure before that window is part of the statement;
- the exposure ∫x_A dt is not a deterministic function of N: condition on a seed-composition event E (ALLC share ≥ a₀
  and D share ≥ d₀ at t = 0, which has probability → 1 by concentration), and prove a probabilistic exposure bound
  with its failure probability; the stopping time (ALLC extinction) is correlated with the faker's survival, so bound
  on a fixed-time window inside the scramble, not on the stopping time.

Together with the establishment bound and the two-factor decomposition measured in the spoiler run, A and B give a
per-island bound [after review: as a union bound over seeded lineages, with every quantity defined]:
P(island establishes | E, seed contains a member of P) ≥ ρ_P(N)·[1 − Σ_q K_q·q̄_q·h_q], the sum over seeded faker
lineages, with K_q the seeded copies, q̄_q the per-copy survival bound from B, and h_q the post-scramble harm
(measured ≤ 0.9; to be defined as a conditional probability, not assumed). Multiple faker types and copies enter
through the union bound; establishment–survival dependence is handled by conditioning on E.

## Tasks

1. **Prove Claim A** over the evaluator semantics of `src/modal.py` (linear Kripke chain, levels PA and PA + Con(PA);
   extend to all levels if the argument allows). Expected structure:
   - FairBot and `BOX1(THEM(ME))`: no faker exists at all (unfakeability by soundness; cite the sibling theorem's
     ledger for which steps need Löb). State it as a lemma with its dependency ledger.
   - `BOX(THEM(^C))`, `BOX1(THEM(^C))`: x cooperates with q only if q provably cooperates with ALLC, so every faker
     cooperates with ALLC. One line; check the levels.
   - `BOX(THEM(THEM))`, `BOX1(THEM(THEM))` [after review: sol is right that this case is short]: by soundness of the
     box, x cooperates with q only if q *actually* self-cooperates; a non-establisher that self-cooperates is, by the
     definition of establisher, one that cooperates with D, so every non-establisher faker cooperates with D. Verify
     the box's soundness at the level and world used for the nested call `THEM(THEM)`, which is the one step that could
     fail. Establisher-fakers (e.g. `and(BOX(THEM(THEM)),not(BOX(THEM(^C))))`) exist and are not dangerous for
     cooperative fixation, only for target identity; verify one by evaluator, and note sol's caveat that an
     establisher-faker could in principle sustain a parochial network with inefficient cross-play (the spoiler run
     found cooperative fixation and efficiency to coincide in every cell, so this did not occur at n ≤ 12).
   If any case fails, give the counterexample, check it with the evaluator, and state the largest sub-family for which
   A holds.
2. **Prove or bound Claim B** [after review]. Specify the update rule (the kernel's Moran death-birth with
   f = exp(w·payoff)) and derive the lineage's birth and death rates from the full state; use the first-moment bound
   P(Z_t > 0) ≤ E[Z_t] = exp(∫(b − d) ds) with an explicit clock convention, over the window where the faker is below
   the mean, and state the demographic-rate bounds needed to turn the integrated relative deficit into the exponent.
   Treat the three faker types separately. Give the bound conditional on E, with the exposure bound's failure
   probability, and compare with the measured per-copy survivals 0.014–0.06 (disadvantaged) and 0.05–0.09 (neutral)
   at N = 100 and 400 from RESULTS "Spoiler-conditioned establishment", and with a *neutral-lineage* survival under
   matched seed compositions and the same stopping rule (a cheap simulation), so that selection is separated from
   demographic extinction. Use the recorded scramble trajectories (the spoiler run's frequency logs) to tabulate, per
   faker, its payoff against x, itself, D and ALLC along actual scrambles.
3. **Static checks** (`src/spoiler_conditioned.py build` regenerates the class cache; n ≤ 12): enumerate every
   non-establisher faker of every member of P at n = 12 and verify A exhaustively; count establisher-fakers separately.
4. **State the combined per-island bound** with every constant named, and say which parts are proved, which are
   measured, and which are assumed.

## RE predictions (Fable)

1. **Claim A holds** for all six members at every n, with the FairBot pair by soundness, the probe-readers in one
   line, and the THEM(THEM) pair by a short case analysis. *Falsifier:* a non-establisher faker of a member of P that
   defects on both D and ALLC, found by enumeration or constructed.
2. **Claim B holds as a first-moment bound** of the form q̄ ≤ exp(−∫_{window} w·(f̄ − f_q) dt) up to demographic
   constants, conditional on E, and it is within a factor of 10 of the measured per-copy survivals at N = 100 and 400
   [after review: loosened from 3; sol expects a valid bound to be loose]. The neutral-lineage comparison shows that
   selection, not demographic extinction alone, accounts for at least half of the log-survival deficit. *Falsifier:*
   no bound of that form, or a bound off by more than 100×, or neutral survival equal to the faker's within a factor
   of 1.5.
3. **The combined bound is positive and uniform in n** for the family P [after review: stated in inf units]. P is a
   fixed finite set of programs, so its raw mass under the infinite length prior is a constant; in cut units it
   decreases toward the inf value as n grows, and the bound is stated with the inf-unit mass and the conditional seed
   probabilities under E. *Falsifier:* an n-dependence of the bound that is not through the normalization of μ_P or
   through P(E).

**What it would mean.** If 1–2 hold, "almost all seeds" is a theorem-shaped statement for the prover family of the
modal arm at the per-island level: the chance is bounded below uniformly in the cutoff, conditional on a seed event of
probability → 1. [after review] What stays empirical is the spread step (one established island spreads to all) and
the absence of competition between established islands holding different provers; a uniform per-island chance does
not by itself prove efficient global absorption. Those are the remaining items for DEFERRED 1. If 1 fails for the THEM(THEM) pair, the
family shrinks to FairBot's pair plus the probe-readers, which still carries most of μ_P.

## RS predictions (Jacob)

(Optional.)

## Procedure for the subagent

Work in small steps and make a tool call at least every few minutes; write proof attempts incrementally to
`notes/scramble-lemma.md`. Commit `predictions/2026-10-05-scramble-lemma.md` carrying the RE predictions before the
static checks. At most 3 workers; do not edit RESULTS.md, REJECTED.md, THEORY.md, CLAUDE.md or DEFERRED.md; do not
touch `runs/d8dcd7ee9a/row.json`; hand back the proofs with dependency ledgers, draft RESULTS, REJECTED, THEORY and
DEFERRED text, at most 5 lines on what matters, and the branch (from `git branch --show-current`) and commits.
