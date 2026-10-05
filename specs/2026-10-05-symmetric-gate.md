# Spec: the symmetric gate, does carrying a contract confer an advantage without the sucker fringe? 2026-10-05

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-05-symmetric-gate-gpt-6.1-sol.md`) and revised; changes marked [after review]. Committed before launch. To be run by an Opus subagent.

[after review] These are trajectory and lottery outcomes at finite sizes, not π; the window, mutation, migration and seed counts are stated per object.

## Why

RESULTS "Prover-carrier seed at b = 0" found that a 1–3% seed of prover carriers establishes where only constants are
legible from source, but the carriers' early advantage (≈ 0.01 per generation at every frequency) comes from a *sucker
fringe*: non-carrier provers whose atoms are answered by the carrier's contract, so they cooperate with the carrier,
while the carrier cannot read them and defects. That is a one-sided rule in the kernel: a contract-less program reads a
carrier's contract freely, but is itself read from source through the gate. Before the result is read as "carrying is
heritable legibility", the asymmetry must be removed.

## The two rules

- **Asymmetric (as run):** any program's box about a carrier is answered from the carrier's contract at zero cost; a
  box about a non-carrier is answered from source through the gate (b = 0: constants only).
- **Symmetric:** a box about a carrier is answered from the contract only if the *reader* is itself a carrier (readers
  that carry nothing have no checker, so they read everyone through the gate). Non-carriers then see carriers as
  illegible, and the fringe cannot cooperate with carriers through their contracts.
- **Intermediate** (for the mechanism) [after review: one stochastic model, specified]: *quenched per source class*.
  Each non-carrier source class is assigned once, by a fixed seed, to "reads contracts" with probability q ∈ {0.25,
  0.5}; the assignment persists for the whole run and across cells. "Reader" is always the executing program; nested
  boxes inside a read are evaluated under the executing program's access. Reciprocal and nested queries (a
  non-carrier's box about a carrier's box about it) are unit-tested under each rule.

## Design

`src/prover_carrier_seed.py` kernel (bit-identical to `contracts_abm`), n = 8 sources, b = 0, PD, w = 0.3, s = 0,
σ = 0 (swapping was inert in outcome). Mix seeds as before.
1. **Static diagnostics** for each rule, on an *identical frozen background* [after review]: the carrier–carrier,
   carrier–non-carrier and non-carrier–non-carrier action and payoff tables, with the component that changes between
   rules identified; rare-carrier growth at 10⁻³ in the μ background, after ALLC's extinction, and at the ε = 10⁻³
   equilibrium; the deterministic invasion threshold (the frequency at which the carrier's growth rate crosses 0) kept
   separate from the finite-population *establishment* threshold (the seed frequency giving establishment probability
   0.5, from the runs); the fringe's mass and its contribution to growth, measured by setting the fringe's cooperation
   with carriers to D while holding every other action and the composition fixed. Exact payoff-table equality, not
   trajectory similarity, verifies the b = ∞ baseline.
   [after review] **Definitions.** *Established:* carriers ≥ 50% of the population for at least 1,000 consecutive
   generations within the window. *Extinct:* zero carriers; at s = 0 this is absorbing, since mutation can only drop
   contracts (the kernel never creates one), so a run stops there. *Censored:* neither by the window's end.
2. **Finite ε** (ε = 10⁻³, 2·10⁴ generations with the second half as the window; **20 seeds per cell** [after review],
   N = 6,400, plus N = 25,600 at f₀ = 0.01 under the asymmetric and symmetric rules, 10 seeds): f₀ ∈ {0.003, 0.01,
   0.03, 0.1} × rule ∈ {asymmetric, symmetric, q = 0.5, q = 0.25}, paired on identical seeds, with Wilson intervals and
   paired differences. Report established / extinct / censored, carrier trajectories, time to 50%, final composition,
   carrier–carrier P(C,C), and population P(C,C) in the second half (separately: established carriers can coexist with
   a mutation-fed shadow).
3. **ε = 0 twins** of every cell (20 seeds).
4. **Lottery** (ε = 0, mN = 1, b = 0): (100, 64) with k ∈ {1, 3} carriers per island, 40 runs per rule [after review:
   k = 3 added]. Plus a **pure-carrier invasion challenge**: an all-carrier island of N = 100 receiving one D, one ALLC
   and one non-carrier FairBot, each in 100 runs, under each rule, to show what established carriers resist.
5. **Baseline:** b = ∞ with the symmetric rule (contracts irrelevant), to confirm the rule changes nothing where source
   is readable.

## RE predictions (Fable)

1. **The symmetric rule removes the frequency-independent advantage, leaving only the linear one** [after review:
   sol is right that the earlier claim of f* > 0 did not follow]. After the scramble the background mutually defects
   (P) and carriers mutually cooperate (R), so a carrier at frequency f earns P + f·(R − P) against the background's
   P: the deterministic invasion threshold is 0, but the advantage vanishes as f → 0 (≈ w·f·(R − P) ≈ 3·10⁻⁴ per
   generation at f = 10⁻³), about 30× below the asymmetric rule's frequency-independent +0.010, which came from the
   fringe. Prediction: symmetric rare-carrier growth at 10⁻³ after the scramble is in [0, +0.002]; the fringe-to-D
   intervention on the asymmetric rule reproduces the symmetric growth within 0.002. *Falsifier:* symmetric growth at
   10⁻³ above +0.005, or the intervention leaving growth above +0.005.
2. **Establishment under the symmetric rule is drift-limited and needs a larger seed.** With only the linear
   advantage, the establishment threshold (seed frequency for probability 0.5) moves from ≈ 0.01 to 0.03–0.1: success
   at f₀ = 0.01 falls from ≈ 0.5 to below 0.2, at f₀ = 0.03 to 0.2–0.6, and at f₀ = 0.1 stays ≥ 0.8. [after review]
   These are bets from the linear-advantage picture, not from a birth–death calculation; the paired differences with
   intervals are the test. *Falsifier:* symmetric success at f₀ = 0.01 above 0.4, or at f₀ = 0.1 below 0.6.
3. **The advantage is dosed by q, on the frozen background.** Rare-carrier growth after the scramble is monotone in
   q, with q = 0.5 within 0.003 of the asymmetric value; success at f₀ = 0.01 is monotone in q as a point estimate,
   but [after review] full-run establishment need not be, since access also changes which exploitable classes persist;
   a non-monotone full-run ordering is reported, not scored. *Falsifier:* frozen-background growth non-monotone in q.
4. **Once established, carriers hold under either rule:** carrier–carrier P(C,C) = 1.00 and population P(C,C) ≥ 0.9
   in every established run (the mutation-fed ALLC shadow, ≈ 0.27 of the population before, is not counted against
   this), and no established run collapses within the window. *Falsifier:* a collapse, or population P(C,C) below 0.8
   in an established run.
5. **The lottery at (100, 64) with k = 1 falls under the symmetric rule** from 0.925 to 0.3–0.7, because a lone
   carrier has no fringe to feed on and its advantage is linear in its own frequency; with k = 3 it is ≥ 0.8 under
   both rules. *Falsifier:* symmetric k = 1 above 0.85, or symmetric k = 3 below 0.5.

**What it would mean.** If 1–2 hold, carrying a proof is an advantage *among carriers* and against unconditional
cooperators only; it does not let a carrier exploit anyone, and a carrier seed establishes by the same mechanism as a
FairBot seed in the free arm, by reaching the frequency at which carriers meet. "Carrying is heritable legibility" then
means exactly that: carriers are legible to each other and to nobody else. If 1 fails and carriers still grow from
rare under the symmetric rule, there is a second advantage to find (ALLC exploitation is excluded by construction;
check the static table). If 2 fails toward the asymmetric values, the fringe was not the mechanism and the static
diagnostics are wrong.

## RS predictions (Jacob)

(Optional.)

## Procedure for the subagent

Follow CLAUDE.md discipline. Commit `predictions/2026-10-05-symmetric-gate.md` carrying the RE predictions before any
run; the static diagnostics come after that commit and before the runs. At most 3 workers; measure one run's time
first and predeclare any reduction; stop cells projected beyond 2 hours and say so; do not edit RESULTS.md, REJECTED.md,
THEORY.md, CLAUDE.md, DEFERRED.md or NOTATION.md; do not touch `runs/d8dcd7ee9a/row.json`; hand back draft RESULTS,
REJECTED, THEORY and DEFERRED text, at most 5 lines on what matters, and the branch (`git branch --show-current`) and
commits.
