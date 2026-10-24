# Review of `specs/2026-10-24-inspection-shadow.md` by gpt-6.1-sol

1. **Errors / unsound mechanisms**
   - “Identify the efficient states (both mean payoffs ≥ −0.05)” conflicts with “the largest exit from the efficient set is neutral drift of `N` … followed by strict invasion of `K`.” At c = 0, replacing `cr` with its payoff twin `N` against `C` preserves both payoffs: that drift remains **inside** the efficient set. **Fix:** distinguish loss of responsive enforcement from loss of payoff efficiency; measure both first-passage events and their connecting paths.
   - “The branching ratio … into the efficient set … decides whether a 1/N exit is fatal in the limit” is insufficient. Return probabilities alone omit excursion durations and trapping times. **Fix:** compute return-time distributions or mean first-passage times and occupation rewards, including committed/mixing detours.
   - “Decompose the stationary flow … record each exit’s rate and its slope” conflates stationary flux, π(s)q(s,t), with conditional escape rate q(s,t). Only the latter directly tests neutral 1/N fixation. **Fix:** report per-mutant fixation probabilities, prior-weighted transition rates, conditional set-exit hazards, and stationary flux separately.
   - The unqualified “`N` is a payoff twin” must be rechecked at c = 0.01. **Fix:** tabulate actual charged costs against `C`; if reading incurs cost, classify `N`’s advantage as selection, not neutral drift.

2. **Design flaws / confounds**
   - “Whole-space chain” is not established merely by using the “twin-expanded distribution.” The concurrent audit follows a capped/full discrepancy of −0.009 versus −0.47. **Fix:** require log-domain solving, closure-seeded exploration, support-convergence diagnostics, and cross-checks with the audit before interpreting stationary weights or slopes.
   - The size path simultaneously changes N, island count, migration exposure per individual, and observation horizon. Constant NI does not isolate population-size effects. **Fix:** add one crossed cell, e.g. (400, 64), and report trajectories at common t and t/N. Describe remaining results as path effects, not N effects.
   - “Prior mass … multiplied by 10” leaves normalization and affected seed/mutation distributions unspecified. **Fix:** specify exact normalized priors, donor mass, and whether the change affects founders, mutation, or both; match the `C` control’s reallocation exactly.

3. **Predictions likely wrong**
   - Prediction 1 is wrong literally: neutral `N` replacement is not an efficiency exit. I predict shadow accumulation precedes an efficiency exit caused by `K` or another exploiter.
   - “P(efficient) does not go to 1” does not follow from odds slope <0.5 over three finite sizes. Odds growing as N^0.2 still imply convergence to 1. I predict rising efficiency if escapes scale as 1/N and return times remain bounded; otherwise the return-time scaling determines the answer. Register finite-range and asymptotic claims separately.

4. **Missing controls / cheap additions**
   - Start paired populations at (`cr`,`C`) and (`N`,`C`); measure shadow fixation, cheater establishment, and recovery directly.
   - Add separate founder-only and mutation-only prudent-class boosts.
   - Preregister intermediate verdicts: predictions with ≥0.1 effects currently leave small positive effects unclassified.

5. **Alternative explanations not ruled out**
   - Rain may rescue enforcement through persistent polymorphism rather than shadow pruning.
   - Boosted readers may help through unrelated off-path behavior or founder abundance.
   - Payoff-threshold efficiency may include forfeit artifacts; report action frequencies and forfeits separately.
