# Review of `specs/2026-11-23-tiered-best-response.md` by gpt-6.1-sol

## 1. Errors, contradictions, unsound mechanisms

- **The prior statistic does not test lexicographic tier 3.** “Finally, to the mutation prior” conflicts with “Prior regret: the same with the replacement drawn from the arm’s tail law,” which optimizes over all native equivalents. A migrant-optimal resident can legitimately sacrifice prior payoff. **Fix:** compute prior regret within the migrant-payoff maximizers in E; report unconditional prior regret separately. Score tier 3 only where earlier tiers hold.

- **Tester lifetime is undefined upon establishment.** “T_q the mean copy-generations of a single q” lacks a stopping rule when q fixes. Meanwhile, “a tester lineage that reaches half of its slot ends the replicate, which is discarded” conditions fixation estimates on avoiding precisely the feedback being tested. **Fix:** distinguish transient occupation until extinction/establishment from establishment probability. Retain threshold-hit replicates as a competing outcome; do not compare the retained subset directly with unconditional P10 fixation.

- **Snapshots cannot identify RE 9’s mechanisms.** “Save … at 25%, 50%, 75% and 100%” cannot establish that a program “held the island from 25% on,” or distinguish intervening replacement, takeover, and return. Routes also overlap unless explicitly ordered. **Fix:** log majority transitions and lineage/source-island provenance; define mutually exclusive routes, including unresolved cases. Otherwise label RE 9 a snapshot description, not a mechanism test.

## 2. Design flaws or confounds

- **Majority profiles are not native populations.** At the permitted 0.8 threshold, minorities can generate selection stronger than the proposed migrant bias; discarded minority migrants also distort exposure. Payoff equivalence at the majority profile does not imply native neutrality. **Fix:** save full composition and realized migrant identities; calculate native payoff differences against actual encounter distributions. Add a near-monomorphic sensitivity analysis.

- **Dose comparisons condition on treatment outcomes.** Migration changes which worlds remain diverse, which islands settle, and which equivalence classes survive. Conditional zero-regret shares can improve without any within-island adaptation. **Fix:** report unconditional joint outcomes and fixed-baseline-profile assays alongside the conditional statistics; pair founder seeds across doses.

- **Founder presence is not arrival opportunity.** The supply control excludes later tail arrivals and includes founders that disappeared before relevant profiles formed. **Fix:** record arrivals into each island while the relevant native profile exists, with counts and time available for fixation.

## 3. Predictions likely wrong

- **RE 1’s numerical precision is unrealistic.** At σ = −3, the formula gives Nρ ≈ 0.157; N = 400 and 10⁵ replicates yield only about 39 fixations, approximately 16% relative sampling error. **Prediction:** some points miss 10% through noise alone. Use exact finite-N benchmarks and binomial intervals, or adaptive replication.

- **RE 8 lacks a monotonicity basis.** Endogenous migrant composition, turnover, and conditioning on diversity can increase regret. **Prediction:** nonmonotone trajectories in some arms; preregister paired changes and exposure changes rather than universal nonincrease.

## 4. Missing controls or cheap additions

Add frozen-native, exogenous-tester assays for selected real profiles, directly testing assumption A. Define zero-regret numerical tolerance, empty-control handling, bootstrap weighting, and “inconclusive” verdicts. Score migrant claims separately where native regret is zero.

## 5. Alternative explanations not ruled out

Low regret may reflect founding abundance, catalogue geometry, colonization, or selective survival rather than threat refinement. T-weighting may identify dangerous, establishing migrants rather than a stationary tester field. Finite-horizon catalogue-relative success would establish neither large-population lexicographic best response nor Pareto efficiency.
