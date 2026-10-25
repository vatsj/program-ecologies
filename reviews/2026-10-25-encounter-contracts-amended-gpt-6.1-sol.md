# Review of `specs/2026-10-25-encounter-contracts.md` by gpt-6.1-sol

## 1. Errors, contradictions, unsound mechanisms

- **The amended stopping rule does not establish a rare-migration jump chain.** “Genesis keeps running during relaxation” conflicts with treating islands as relaxed attractors merely because behaviour “has been fixed for 500 generations.” Silent contracts can change future responses to migrants; later genesis can also cause spontaneous switches. Behavioural stationarity is not stationarity of the transition-relevant state. **Fix:** retain program-and-contract microstates, test no-migrant switching over extended holdouts, and establish within-class equilibration. If genesis causes persistent class transitions, include those transitions explicitly rather than attributing everything to migration.

- **BR is inconsistent with commitment and has an undefined case.** Genesis says complement carriers “play their fills (they are committed),” whereas BR says “the complement plays a pure best reply.” Also, “every such reply” vacuously accepts improvements if the remaining game has no pure Nash equilibrium. **Fix:** hold committed complement members fixed; best-respond only with uncommitted members. Specify a non-vacuous fallback for no pure equilibrium, or verify exhaustively that this case cannot occur.

## 2. Design flaws or confounds

- **Outcome classes are not sufficient pool states.** Two fair-pair islands can have different programs, reservoirs, and migrant responses. A pool dynamics estimated from class-averaged rates need not remain valid as hidden composition changes. **Fix:** propagate richer island states, or demonstrate approximately invariant within-class conditional distributions and rates across starts and time.

- **N = 100 cannot characterize the large-population claim.** Fixed per-island ν supplies only O(1) proposals per generation while installation affects O(1/N) of each signing slot. Encounter coordination also changes with N. **Fix:** add at least a small N panel, explicitly separating fixed-ν scaling from fixed per-individual proposal exposure.

- **B does not isolate dilution alone.** Random recipients may have different programs and encounter contexts from the tested signers, so their contracts need not benefit them. “Instead of the two signers” also ignores singleton and grand coalitions. **Fix:** retain all original signers, broadcast to matched copies as the primary amplification control, and report unmatched broadcasting separately.

## 3. Predictions likely wrong

- **Prediction 5:** non-best-reply program responses do not imply a ≥0.05 efficiency-share difference. Acceptance can remain unchanged; conversely, BR’s worst-equilibrium acceptance rule can create differences without the proposed mechanism. **My prediction:** substantial encounter-level response differences can coexist with small aggregate differences; the numerical threshold is unsupported.

- **Prediction 6:** all three fair pairs remaining positive does not follow from symmetry or positive conversion rates. Symmetric nonlinear pool dynamics can have unstable interior coexistence and attracting boundary states. **My prediction:** coverage will depend on invasion rates and initial composition, not symmetry alone.

## 4. Missing controls or cheap additions

- Compute an **exhaustive improving-contract oracle** on reported settled states. Random genesis failing to discover a deviation is not contract-stability.
- Separate the settling window from an independent holdout when testing “go quiet”; the current stopping condition partly selects quiet windows.
- Add post-installation replay tests: accepted genesis must reproduce its predicted outcome, including existing complement contracts, replacements, multiple responders, and grand coalitions.
- Predefine contract caps and eviction rules; report cap sensitivity, not just whether caps bind.
- Preserve tilted starts before optional reference arms: they directly test coexistence and basin dependence.

## 5. Alternative explanations

Apparent efficiency could reflect preferential sampling of quiet states, exogenous payoff-filtered innovation rather than evolutionary spread, or reservoir/history composition rather than outcome-class dynamics. Observed third-pair transitions could be spontaneous genesis events coinciding with migrant windows. Matched no-migrant windows and contract-lineage attribution are needed.
