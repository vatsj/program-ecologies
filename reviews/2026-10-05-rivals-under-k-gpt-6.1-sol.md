# Review of `specs/2026-10-05-rivals-under-k.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes

- **The proposed conclusion exceeds the object tested.** Absence of bridge-less rivals relative to A at n = 8 does not establish metapopulation universality: incompatible non-A networks, longer bridge paths, missing bridges in realized seeds, and larger cutoffs remain untested. **Fix:** characterize the full establisher compatibility/bridge graph; label the lottery result finite-cutoff, finite-horizon evidence, not a large-population conclusion.
- **Arm-specific migration calibration confounds calculus with dynamics.** Different calibrated mN values can change separation and resolution independently of bridge structure. **Fix:** retain the calibrated comparison but add a common-mN comparison; report nucleation times and the dimensionless boundary coordinate for both arms.
- **Payoff-identity lumping needs a K-specific validity check.** Reproducing the free cache validates pipeline compatibility, not the new quotient. **Fix:** verify identical directed interaction rows/columns within each lump, preserved source masses and seed probabilities, and agreement between lumped and source-level establishment/bridge tests. Define “new rival” by source identity across arms, not arm-specific class IDs.
- **“Bridge-less” and “permanent” need separate operational definitions.** Failure to find a pairwise bridge is not absence of multistep mediation; finite-N fixation probabilities can be positive but astronomically small. **Fix:** distinguish direct bridges, mediator paths, zero transitions, and transitions below a numerical threshold. State the limiting object supporting permanence.

### 2. Predictions likely wrong

- **Prediction 2 is overconfident.** Removing P* does not determine replacement-rival mass, bridge survival, or establishment rates. Moreover, ≤2/3,000 is an observed-count threshold, not a fivefold rate bound: with two events, the one-sided 95% upper rate is about 0.0021. **My prediction:** fewer P*-associated separations, but no defensible fivefold reduction before screening; surviving separations may still be bridge-less.
- **Prediction 3 conflates self-defection with extinction.** A self-defecting lineage can drift among defectors, exploit cooperators, or alter founder demography. Its disappearance and unchanged q_est do not follow from P*(P*) = D. **My prediction:** no *cooperative P* establishment*, but possible transient survival or effects on establishment. Define lineage establishment separately from cooperative establishment.
- **The stated mechanism is inconsistent with the supplied latest results.** Those attribute related failures to bounded self-consistency and say the literal 4-rule is vacuous, rather than simply missing distribution. **Prediction:** P* loses self-cooperation at the tested budgets, but this does not certify “at every budget.” Use audited derivations, not that extrapolation.

### 3. Missing controls/cheap additions

- Add a **forced bridged-rival positive control** under K to verify that the reused mediator/holder machinery resolves a known rivalry.
- For forced P*, specify whether founders are added or replaced; match founder count and replacement with an inert-defector control.
- Report binomial intervals, island-clustered uncertainty, bridge presence at seeding, and right-censored resolution times. A longer-horizon continuation of unresolved runs is cheap.
- Prioritize both matched natural arms before optional forced cells; the current stop order risks losing the main comparison.

### 4. Alternative explanations not ruled out

Lower separation could reflect reduced rival establishment, increased A mass, slower nucleation, altered migration, or horizon censoring—not improved bridge connectivity. High island P(C,C) can coexist with permanently incompatible islands. Budget effects can reflect which programs enter the establisher set rather than improved mediation.

### 5. Beyond this experiment

nothing material
