# Review of `specs/2026-10-14-farsighted-refusal.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **A few initializations do not enumerate equilibria.** Failure to find a V\*-absorbing fixed point cannot falsify prediction 2; initialization-dependent convergence is not an equilibrium-selection justification. **Fix:** distinguish certified solutions from search coverage. Use policy enumeration with pruning or a constraint solver to certify nonexistence; otherwise report “not found.” Freeze the default-selection algorithm before static computation.

- **The discounted process is underspecified.** Does δ advance on every contract draw, every dominating proposal, or only installed contracts? Are status-quo payoffs accrued during refusals? These choices change the incentives fundamentally. **Fix:** write the Bellman equations, reward timing, self-loops, and consent counterfactual explicitly. Discounting only installed moves risks making refusal stop the economic clock.

- **gKR-read remains self-referential.** Reading current frequencies does not determine the consent probabilities of readers whose decisions depend on those same probabilities. Monomorphic equality also requires matching equilibrium-selection conventions. **Fix:** specify a joint mixed-composition fixed point, its selection rule, and behavior on nonexistence/nonconvergence. Alternatively, use explicitly lagged policies and label that a different model.

- **“Stationary V\* mass” is not unique for an absorbing chain.** The union of recurrent classes also does not establish reachability from seeded island states. **Fix:** report each recurrent class, initial-condition-dependent absorption probabilities, and hitting-time distributions. Separate static contract-chain conclusions from ecological dynamics, where migration and play reproduction can invalidate the 20-state closure.

- **Realizability is not established by host-side value iteration.** Reading island-wide frequencies is an information-access assumption; host operations are not evaluator steps. **Fix:** specify executable access, numerical precision, fuel, and failure behavior. Otherwise call this an idealized oracle experiment, with a separate implementation benchmark.

## 2. Predictions likely wrong

- **2: the Anesi analogue is too strong.** Majority bargaining results do not automatically transfer to uniform contract proposals restricted to immediate dominance and strict, tie-refusing consent. My prediction: equilibrium existence and recurrent sets will be protocol-sensitive; V\* recovery is possible but not justified by the cited analogy.

- **5–6: recovery does not imply evolutionary spread or coexistence.** gKR evaluates a counterfactual monomorphic population; mixed populations can make its refusals costly or ineffective. Neutrality within established islands does not establish neutrality during formation. My prediction: trajectories depend strongly on initial outcome–guard associations; no robust coexistence conclusion at 2,000.

- **7: reading need not increase realized fitness.** Better continuation estimates optimize discounted consent, not reproductive success. Readers can also accept moves that undermine the collective refusal convention. My prediction: no systematic advantage without a measured mechanism.

## 3. Missing controls / cheap additions

- Forced starts at every outcome, especially outside V\*, to separate recovery from persistence.
- Matched guard placements across slots and islands; include rare-invasion starts, not only ½ mixtures.
- A precomputed lookup-table clone of each KR policy: isolates source reading from policy behavior.
- Exact rational policy evaluation and consent-margin reporting; near-zero margins at δ = 0.99 can flip recurrent classes.
- Separate predictive falsifiers from gaps such as occupancy 0.7–0.9 and cost 10⁵–10⁶.

## 4. Alternative explanations not ruled out

Generic transition suppression; favorable basin sizes; arbitrary equilibrium selection; guard–play linkage; payoff-weighted migration favoring incumbent distributions rather than farsightedness.

## 5. Beyond this experiment

Test whether one executable equilibrium-selection convention remains well-defined under heterogeneous reader composition. That compositional property—not monomorphic recovery alone—is necessary for treating KR consent as a heritable source-reading program.
