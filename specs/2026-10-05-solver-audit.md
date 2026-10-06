# Spec: solver audit of the published ε→0 chains, with independent deep-state discovery, 2026-10-05

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-05-solver-audit-gpt-6.1-sol.md`) and revised; changes marked
[after review]. To be run by an Opus subagent. Follow-up to the methods finding of RESULTS "The modal arm on
two-player divide-the-dollar" (IMPLEMENTATION §4 solver caveat). Corrective: no new science unless a published
number changes, and every discrepancy is reported, not only the large ones.

## Why

The modal-dollar run found that the repo's lazy linear-domain chain (`eager_poly=False`, exploration threshold θ)
is not trustworthy once *deep polymorphisms* exist (recurrent mixed states every exit of which is deleterious):
their flows underflow and the stationary answer moves with θ (0.44 against 0.75 at θ = 10⁻⁷ against 10⁻⁹ for the
same arm), while a seeded log-domain chain converged. Published results used the lazy chain in settings where deep
polymorphisms exist (RESULTS "Divide-the-dollar partitions", whose headline is that a greedy S5–accommodator
polymorphism, itself a deep state, absorbs π), and the PD chains (`src/chain.py`, `src/modal_limN.py`) have never
been checked against a deep-state definition. [after review] θ-insensitivity does not establish correctness (both
thresholds can omit the same trap), and a census of the *solved* chain gated by its own π cannot find the states it
suppresses. So every listed cell is re-solved unconditionally, state discovery is independent of any published π,
and the audit's conclusions are limited to what the discovery enumerates.

## Definitions [after review: operational]

- **Candidate recurrent support:** a set of ≤ 3 behavioural classes whose restricted replicator dynamics
  (`chain.replicator`) has an internally stable rest point with every member above 10⁻⁶ (internal stability tested
  by the Jacobian at the rest point; cycles reported separately as indeterminate).
- **Deep:** a candidate support at whose rest point *every* admissible outside mutant (every class in the catalogue
  not in the support) has invasion fitness below the resident mean by more than the neutrality tolerance 10⁻⁹ in
  payoff. **Non-deep:** at least one outside mutant neutral or advantageous. ("Bistable" is not used unless shown.)
- **Twin:** a class outside the support whose payoffs against every support member and against itself equal a
  member's; **twin drift** is the replacement of that member by its twin, modelled as a complete transition with
  rate μ(twin)·(1/(x_r N))·(the neutral fixation of a mutant inside a resident subpopulation of share x_r), stated
  as such.
- Mutation-prior weights and class multiplicities are identical in every solver (the same `mu` vector and class
  table; no re-aggregation).

## Design

1. **Independent state discovery** for every cell below: enumerate candidate recurrent supports from the class
   tables alone (all singletons; all pairs and triples among the K_c classes with the largest μ and all classes in
   any published support, with K_c chosen so the enumeration fits and reported; the enumeration's coverage stated as
   a limit on the conclusions), classify each as deep or non-deep with the full list of outside mutants and their
   invasion fitnesses, and compare the deep set with the published chain's recurrent states.
2. **Three separated checks** [after review], each on identical rates:
   - *state discovery:* the published chain's explored set against the enumerated candidate set (missed deep states
     counted, with their μ and their best-path weight from the published support);
   - *transition rates:* every rate between enumerated supports recomputed in the log domain and compared with the
     published solver's rates (max relative error; underflowed rates counted);
   - *stationary solver:* the published chain's generator, re-solved in log-domain GTH, and the lazy linear solve of
     the same generator, with stationary residuals, precision sensitivity (double against `mpmath` at 50 digits on a
     small exhaustive instance, see 5) and rate-level agreement.
   Then the **full re-solve** on the enumerated state space (every enumerated support expanded, log-domain GTH):
   published number, re-solved number, difference, support and transition structure under both. Every discrepancy is
   reported; a difference ≥ 0.05 on P(efficient), P(C,C) or a headline partition share is a correction recorded as
   an addendum to the published section (append-only), with the mechanism.
3. **Cells** (all unconditional): divide-the-dollar one-population `norole` and `role` at N = 10³, 10⁴, 3·10⁴, both
   games; the three-player dollar modalPA at N = 10³; the union game QUORUM arm at c = 0.5, N = 10³; the PD modal arm
   at N = 10⁴ and 3·10⁴ (`src/modal_limN.py`); the PD weak arm at N = 10⁴; the priced arm c = 0.01 at N = 10⁴; the
   bounded K arm b = 16 at N = 10⁴. **Controls** [after review]: the modal-dollar n = 7 cell at N = 10⁴ as the
   positive control (the lazy solve must fail and the log-domain solve must reproduce 0.653), and an exhaustive
   two-class PD cell with no deep state as the negative control (every solver must agree to 10⁻⁶).
4. **Twin drift as a labelled intervention, after the solver comparison** [after review]: for every deep state found
   in a dollar cell, add the twin transitions and compute the **twin-expanded stationary distribution** (not only
   best paths; best-path exponents kept as diagnostics), at N = 10⁴ and 10⁵; report whether the absorbing state's
   identity or weight changes.
5. **Regression tests** (`tests/test_solver_deep.py`) [after review: two failure modes]: (i) a hand-built chain with
   one deep polymorphism whose flows underflow in double precision, where the lazy linear solve is wrong and the
   log-domain solve matches `mpmath`; (ii) a hand-built chain in which the lazy exploration never reaches a deep
   state reachable only through a sub-threshold flow, where the enumeration finds it.

≤ 3 workers; priority 5 → 3's controls → dollar cells (1–2) → PD cells → union and three-player → 4.

## Required outputs

`runs/solver-audit.md` and `.json`, `src/solver_audit.py` and `src/chain_log.py` (the generalized seeded log-domain
solver; no edits to `src/chain.py` except a bug fix in its own commit), the tests, a predictions file from the spec
committed before any counted run, and the usual hand-back (draft RESULTS addenda for every corrected section,
REJECTED entries, THEORY/IMPLEMENTATION edits, NOTATION, ≤ 5 lines, branch from `git branch --show-current`,
commits).

## RE predictions (with falsifiers) [after review: tolerances and falsifiers aligned; confidence lowered]

1. **The PD cells have no deep state** under the operational definition within the enumeration's coverage, and
   their published numbers re-solve within 0.01. *Falsifier:* a PD cell with a deep state of μ-weighted candidate
   mass ≥ 10⁻³, or a published P(C,C) moving by ≥ 0.01. (Between: none; the two clauses are exact.)
2. **The dollar one-population cells have deep states and their headline survives in identity but not necessarily
   in weight** (sol's point adopted): the greedy polymorphism remains the absorbing state at N ≥ 10⁴ (`norole`) and
   ≥ 3·10⁴ (`role`), and P(efficient) changes by less than 0.1 in every cell. *Falsifier:* the absorbing state's
   identity changes, or any dollar P(efficient) changes by ≥ 0.1. (No gap.)
3. **The union and three-player cells re-solve within 0.02 on every headline share**, after the three checks pass.
   *Falsifier:* a headline share moving by ≥ 0.02.
4. **Twin drift changes a best-path exponent in every dollar deep state but changes the absorbing state's identity
   at N = 10⁴ in none**; the RE allows that a twin differing off-support can expose a new exit (sol's point) and
   predicts its stationary effect stays below 0.05. *Falsifier:* a different absorbing state at N = 10⁴ under twin
   moves, or a twin-expanded P(efficient) differing by ≥ 0.05.
5. **Both regression tests fail the lazy chain and pass the log-domain chain**, and the positive control reproduces
   the modal-dollar failure. *Falsifier:* the lazy chain passing test (ii), or the positive control not failing.

The RS is invited to add predictions; the uncertain one is 2's weight clause.
