# Review of `specs/2026-10-14-founding-legibility.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **L1 conflates timely legibility with extra production and a free information endowment.** Founders receive an island-wide pass before selection; ordinary production may encounter different sets or exhaust a different budget. Specify candidate enumeration, total/per-set fuel, certificate cap, and cost accounting. Add a matched pass whose outputs are withheld until after the first selection event. Compute all founding lists from the same frozen, empty-list snapshot; otherwise founder order can bootstrap certificates.
- **L2 is not demonstrably semantics-preserving.** A failure may depend on current certificates, opponent state, search order, or fuel. An inherited negative cache can suppress a later successful production. Cache only failures proved invariant under the relevant changes; otherwise invalidate on state/budget changes. Separate `NONE` from timeout, and replay sampled cached failures against descendants.
- **The proposed interpretation of failure is invalid.** L1 ≤ 0.1 does not establish a language limitation: founding coverage, verification fuel, or subsequent certificate loss could still bind. Require a manipulation check: which naturally founded coalitions become executable and fair at generation 0, and whether certificates survive through their first encounters.
- **The experiment cannot identify a large-population conclusion.** Two sizes, finite horizons, and 12 larger-size runs estimate finite-time establishment, not limiting efficiency. Label claims accordingly. Distinguish fairness from Pareto efficiency and report both.

## 2. Predictions likely wrong

- **Prediction 1’s ≥ 0.3 is too optimistic.** The ideal-table result of 0/20 already suggests removing execution/legibility obstacles is insufficient, unless that control had a materially different founding rule. My prediction: L1 improves early militant survival but need not reach 0.3 persistence. Reconcile the ideal-table control before assigning causality.
- **Prediction 2’s dynamic neutrality is unjustified.** If failures are state-dependent, permanent caching changes reachable certificate states. My prediction: neutrality only for an invariant-failure cache; the proposed unrestricted mark may change persistence in either direction.
- **Prediction 3 lacks monotonicity.** More fuel can enable rival strategies as well as fair coalitions. My prediction: isolated-coalition success improves with fuel; ecological persistence has no guaranteed ordering.
- **Prediction 6’s gate rationale is incomplete.** In `(D*, T₁, T₁)`, each T₁ still has an identical-source partner. A distinct boss does not by itself establish that the required three-party production passes the gate. Resolve this by a deterministic gate-and-production trace before running 40 assays.

## 3. Missing controls / cheap additions

- Add **natural founding at 3·10⁶**: otherwise L3 cannot identify a fuel-by-legibility interaction.
- Preserve the **sham comparison** ahead of secondary scaling if identity separation is a central claim.
- Record generation-0 certificate coverage, first-encounter strike/work decisions, and militant lineage survival. Unconditional-worker share at generation 50 alone is not a direct mechanism test.
- Report total and tail costs, including founding, not just median encounter cost.
- Predefine persistence, establishment windows, and terminal evaluation windows. Ensure stored baselines have matching horizons.
- Forty runs cannot credibly establish equivalence within 0.05 near low persistence; twelve runs are weak for the size comparison. Report intervals and “inconclusive,” not “no effect.”

## 4. Alternative explanations not ruled out

Extra founding search, rare complete-coalition availability, certificate retention, altered rival legibility, and finite-horizon basin selection can explain L1 effects. The size effect may reflect slower establishment rather than lower eventual success.

## 5. Beyond this experiment

Nothing material.
