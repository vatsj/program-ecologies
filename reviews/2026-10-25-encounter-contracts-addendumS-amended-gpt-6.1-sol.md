# Review of `specs/2026-10-25-encounter-contracts.md` by gpt-6.1-sol

## 1. Errors or unsound mechanisms

- **The escape-bound amendment does not justify the stated limit.** “Before each migrant an island’s state is its within-island limit” conflicts with using “classes identified from holdouts” and “an escape-rate upper bound propagated into the share dynamics.” Any positive spontaneous escape rate dominates migration as migration → 0, however small its finite-window upper bound. **Fix:** certify closure from transition support, or report finite-migration dynamics over an explicit range of migration/escape-rate ratios. Do not treat provisional classes as states of the limiting chain.

- **Closure alone does not justify invariant-distribution averaging.** “Only a verified closed recurrent class is collapsed to one state” with “migrant transitions averaged over its invariant distribution” additionally requires mixing before migration. Closure verification and a 5,000-generation holdout establish neither mixing nor convergence from the founding state. **Fix:** distinguish hitting probabilities into recurrent classes from their internal stationary laws; verify mixing or explicitly use randomized-time sampling with a convergence diagnostic.

## 2. Design flaws or confounds

- **BR is not a best-response dynamics control.** It changes acceptance using worst pure equilibria, but executes installed contracts under ordinary program responses. Thus differences combine responder rationality, equilibrium conservatism, and acceptance/execution mismatch. Proposal-level logging diagnoses these differences but does not remove them. **Fix:** call this a *robust-acceptance diagnostic*; add a small execution-consistent BR cell with an explicit equilibrium-selection rule.

- **The “quiet” prediction retains selection by the outcome being predicted.** Settlement requires that “no contract formed in that window fires on path.” Fresh windows reduce reuse of observations, but quiet-window selection still preferentially samples low-hazard configurations. **Fix:** estimate firing hazards from fixed-age, unselected post-anneal snapshots too; report time to settlement and never-settled mass.

- **Outcome-class shares cannot establish population-level Pareto efficiency.** Heterogeneous islands can have efficient encounter outcomes but inefficient expected slot-payoff vectors, or conversely. **Fix:** define the efficiency target explicitly and report encounter efficiency and expected-payoff-vector dominance separately from V\* membership.

## 3. Predictions likely wrong

- **Prediction 8’s silent-halves mechanism is generally wrong.** On a monomorphic program island, the founding key remains on path despite contract installation: keys use override-free play. Both halves therefore fire immediately whenever their holders encounter residents, even without meeting each other. I predict successful S conversions disproportionately use immediately firing singleton-compatible fills, not two silently drifting halves.

- **Prediction 7’s ordering has no monotonicity basis.** Restricting writes changes both beneficial and harmful reachable transitions; exposed hooks may also attract exploitation. I predict H can outperform H-top by blocking destabilizing contracts, or underperform H-inert through harmful accepted installations. Hook frequency need not increase.

## 4. Missing controls or cheap additions

- Include eviction recency/order, bundle provenance, and any mutable evaluator state in configuration snapshots and replay tests. Identical fills with different eviction histories need not have identical transition laws.
- For each sampled full configuration, run paired migrant/no-migrant branches with common random numbers; estimate the migrant’s incremental conversion probability.
- Stratify establishment by whether each signer’s fill already improves fitness **without any other signer present**. This directly separates coordination from independently advantageous plasticity.

## 5. Alternative explanations not ruled out

- Apparent coverage may be long transients or symmetry-preserving initial conditions, rather than stable coexistence.
- Apparent contract-mediated improvement may arise from ongoing targeted mutation and inherited individual plasticity, rather than coalitional coordination.
- B’s benefit may reflect altered commitment prevalence and responder behaviour, not merely relief of dilution.
