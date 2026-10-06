# Predictions: solver audit of the published ε→0 chains, with independent deep-state discovery (2026-10-05)

Spec `specs/2026-10-05-solver-audit.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-05-solver-audit-gpt-6.1-sol.md`;
where the spec's [after review] text and the review differ, the spec is the resolution). New code
`src/solver_audit.py`, `src/chain_log.py`, tests `tests/test_solver_deep.py`. Committed before any counted run (no
re-solve, discovery, rate check, control or twin number was computed before this commit; only class-table load
times and class counts were looked at: dollar5 n = 5 `norole` 78 classes, `role` 140; dollar3 n = 5 `norole` 45,
`role` 80; modal dollar n = 7 205; modal PD n = 9 863; weak PD L_6 112 (abm cache)).

## Cells and the published numbers they are checked against

| cell | published chain | published headline |
|---|---|---|
| dollar5 `norole` N = 10³ / 10⁴ / 3·10⁴ | `dollar_partitions.onepop_chain` (θ = 10⁻⁷, eager) | P(efficient) 0.9995 / 0.4135 / 0.4132; 1/2–1/2 0.9990 / 0.0004 / 0.0000 |
| dollar5 `role` N = 10³ / 10⁴ / 3·10⁴ | same | P(efficient) 0.9995 / 0.9682 / 0.4620; 1/2–1/2 0.6928 / 0.8062 / 0.0740 |
| dollar3 `norole` N = 10³ / 10⁴ / 3·10⁴ | same | P(efficient) 0.9959 / 0.6251 / – ; 1/2–1/2 0.9853 / 0.0000 / – |
| dollar3 `role` N = 10³ / 10⁴ / 3·10⁴ | same | P(efficient) 0.9992 / 0.9858 / – ; 1/2–1/2 0.1568 / 0.7882 / 0.817 (text) |
| PD modal n = 9, w = 0.3, N = 10⁴ / 3·10⁴ | `modal_limN.cell` (θ = 10⁻⁶, eager) | P(C,C) 0.622 / 0.727 |
| PD weak L_6 (`ROLE`), w = 0.3, N = 10⁴ | `limN` / `run.run_cell` (θ = 10⁻⁶, eager) | P(C,C) 0.0073 |
| PD priced n = 6 atoms, n = 8 atoms, n = 8 lazy, c = 0.01, N = 10⁴ | `priced_limN.cell` (θ = 10⁻⁶, `eager_poly=False`) | P(C,C) 0.0150 / 0.0158 / 0.9985 |
| PD K b = 16 at n = 8, N = 10⁴ | `k_at_n8.chain_cell` (θ = 10⁻⁶, `eager_poly=False`) | P(C,C) 0.671 |
| three-player dollar modalPA, N = 10³ | `dollar3_chain.Chain3` (core + ring, log-scaled GTH) | grand .0161, fair pair .366, unfair pair .615 |
| union QUORUM, c = 0.5, N = 10³ | `union_chain.UChain` | fair .003, intermediate .013, zero wage .48 |
| positive control: modal dollar n = 7, N = 10⁴ | lazy θ = 10⁻⁷ / seeded log-domain | 0.445 / 0.653 |
| negative controls: exhaustive {C, FairBot} and {D, C, FairBot} (modal PD), N = 10⁴ | – | all solvers agree to 10⁻⁶ |

Where a published row was produced with a different w or n than listed, the audit uses the published row's
parameters and says so.

## Operational definitions (from the spec)

- Candidate recurrent support: ≤ 3 classes whose restricted replicator (`chain.replicator`) has a rest point with
  every member > 10⁻⁶ that is internally stable by the Jacobian (all eigenvalues of the replicator Jacobian on the
  simplex's tangent space with real part < 0; zero eigenvalues = neutral, reported as not internally stable; cycles
  reported as indeterminate).
- Deep: every outside class has invasion fitness (payoff against the resident mix) below the resident mean by more
  than 10⁻⁹. Non-deep: some outside class within 10⁻⁹ or above. The repo's older `modal_dollar.deep_states`
  (which also admits first-order-neutral mutants with a second-order frequency penalty) is reported alongside as
  "deep with penalty", never substituted.
- Twin: an outside class whose payoffs against every support member and against itself equal a member's; twin drift
  = replacement of that member by the twin at rate μ(twin)·(1/(x_r N)), a complete transition, labelled as an
  intervention and added only after the solver comparison on identical rates.
- The same `mu` vector and class table in every solver of a cell.

## RE predictions (copied verbatim from the spec)

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

## Subagent predictions

- **S1 (the failure mechanism is the linear stationary routine, not the rates).** In at least one published dollar
  one-population cell at N ≥ 10⁴, the linear solve (`Chain.stationary`) treats a class as numerically closed (its
  `near_closed` path, or a 1 − P_ii that rounds to 0) although the log-domain generator on the same explored set is
  irreducible; there the published π is an absorption lottery from the seed weights, not a stationary
  distribution. *Falsifier:* no dollar cell at N ≥ 10⁴ has a near-closed class in the published solve.
- **S2 (at least one correction).** At least one dollar one-population cell moves by ≥ 0.05 on P(efficient) or on
  its 1/2–1/2 share. *Falsifier:* every dollar cell within 0.05 on both.
- **S3 (PD cells are numerically sound).** Modal (10⁴, 3·10⁴), weak (10⁴), K b = 16 (10⁴) and priced atoms n = 6
  (10⁴) re-solve within 0.005 in P(C,C); priced lazy n = 8 within 0.01. *Falsifier:* a larger move in any of them.
- **S4 (RE 1's first clause fails on price, not on provers).** Under atom pricing at c = 0.01 all-D is deep (every
  prover pays the price against D; constants lose), so a PD cell has a deep state of mass ≫ 10⁻³; the free modal,
  weak and K b = 16 cells have no deep state of candidate mass ≥ 10⁻³. *Falsifier:* all-D non-deep under atom
  pricing, or a deep state of mass ≥ 10⁻³ in the free modal, weak or K cell.
- **S5 (twin identity at 10⁵).** In every dollar cell where twin moves are added, the twin-expanded stationary
  distribution has the same top state (up to twin relabelling) at N = 10⁵ as at N = 10⁴. *Falsifier:* a different
  top state.
- **S6 (fixed-role chains are clean).** In the union and three-player cells there is no internally stable
  polymorphic candidate (constant selection within a slot), no deep monomorphic triple in the enumeration lies
  outside the published explored set with re-solved π ≥ 10⁻⁴, and no headline share moves by ≥ 0.005 (stricter
  than RE 3). *Falsifier:* a move ≥ 0.005, or such a missed deep triple.
- **S7 (precision).** On the small exhaustive instance (the modal-dollar reduced subsystem {S3, S5, A5} at
  N = 10⁴, every state expanded) log-domain GTH agrees with `mpmath` at 50 digits to 10⁻⁹ in every log π_i,
  including components below 10⁻³⁰⁰. *Falsifier:* a larger disagreement.
- **S8 (discovery is not where the errors are).** In every dollar cell, every deep candidate carrying ≥ 10⁻³ of
  the re-solved π is in the published chain's explored set; the published errors, where any, come from the
  stationary solve. *Falsifier:* a deep state outside the published explored set with re-solved π ≥ 10⁻³.

## Verdict rules

- A prediction **holds** if every clause holds; **fails** if a clause fails; **falsifier fired** if its stated
  falsifier condition is met (a failure with the falsifier not fired is reported as "failed, falsifier not fired").
- Tolerances are absolute differences in the stated statistic (P(efficient), P(C,C), headline share), published
  number to re-solved number on the full re-solve; the solver check on identical rates is reported separately and
  does not enter a verdict except S1 and S7.
- A published number that moves by ≥ 0.05 on P(efficient), P(C,C) or a headline partition share is a correction:
  an addendum paragraph is drafted for its RESULTS section (append-only).
- Every conclusion is limited to the enumeration's coverage, stated per cell (K_c and whether triples are
  exhaustive).
