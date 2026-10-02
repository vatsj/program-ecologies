# Review of `predictions/2026-10-01-rival-networks.md` by gpt-6-astra

## 1. Design flaws/confounds and fixes

- **R2 cannot support the claimed spatial stationary distribution.** Labels are not lumpable: invasion changes the resident genotype, not merely its label, and subsequent exits need not resemble the representative’s. Well-mixed agreement neither validates spatial lumping nor bounds its error by 0.08. **Fix:** expand residents around likely stationary support, especially fakeable FB members and P* shadows; report sensitivity to representative choice and rate uncertainty. Otherwise call R2 a representative-model result, not a spatial reversal.

- **Censoring and adaptive stopping compromise R1 inference.** Excluding unresolved trials preferentially removes long-lived lineages. Ordinary Wilson intervals are not generally valid under success-dependent stopping. Twenty continuations poorly estimate fixation probabilities; zero observed transitions can create artificial absorbing classes in R2. **Fix:** retain censoring bounds, use fixed trial counts or sequentially valid intervals, and propagate unresolved/rare-rate uncertainty into stationary-mass bounds.

- **The proposed order-of-limits conclusion is unsupported.** R2 estimates rare-mutation equilibrium; R4 measures finite-time invasion from selected initial conditions. Different winners do not establish noncommuting limits. **Fix:** describe this as mutation-dependent invasion versus rare-mutation occupancy. An order-of-limits claim needs specified observables and scaling in \(N,\varepsilon,t\).

- **MD fraction is not total welfare loss.** With these payoffs, unilateral cooperation has mean payoff −0.5, versus −1 for DD. Per-capita interaction-welfare loss relative to CC is
  \[
  f_{DD}+\tfrac12(f_{CD}+f_{DC}),
  \]
  plus separately reported compute costs. **Fix:** record all action outcomes; retain MD as one component and \(P(C,C)\) as the dilemma statistic.

## 2. Predictions likely wrong

- **The ALLC threshold is not a spatial death-birth invasion criterion.** It compares cross-edge payoffs, whereas reproduction compares competitors’ complete neighbourhood payoffs through exponential fitness. Bulk ALLC share need not equal exposure at the front; ALLC and FB are not interchangeable competitors. I predict no universal reversal threshold in bulk \(x\). Measure interface-conditioned composition and actual replacement drift.

- **“Finite \(\varepsilon\) reverses the border” is too unconditional.** Mutation also supplies P* shadows and other programs capable of disrupting P* domains. Two successful split-start runs would not establish ALLC causation. I expect substantially more composition- and initial-condition dependence than verdicts 17–19 allow.

- **R2’s cost-independent \(188/N\) law is overconfident.** It assumes the entire relevant traffic is effectively D→FB→ALLC→D. Free entry and one free exit do not make the stationary distribution cost-independent. Predict cost-dependent corrections, potentially changes of dominant support.

- **The \(O(1/\text{side})\) border bound need not survive mutation.** It describes a few macroscopic interfaces, not a nucleating mosaic. At fixed mutation rate, interface density can remain positive as size grows.

## 3. Missing controls / cheap additions

- Validate selected **nonneutral** blocks against exact small-graph calculations, including whether payoffs are evaluated before or after death.
- Compare with a complete graph using the **same update rule**; well-mixed birth-death rates are not automatically a death-birth control.
- Add mutation-free FB/ALLC–P* fronts with controlled ALLC placement, and targeted ALLC-input suppression.
- Add several smaller-system seeds and mutation rates before expensive large runs.

## 4. Alternative explanations

- Apparent coexistence may be slow coarsening or metastability.
- Network dominance may reflect prior multiplicity and exact-copy pricing subsidies rather than reasoning ability.
- Hypercube trends combine increasing population, degree, and changing interface geometry.

## 5. Beyond this experiment

Nothing material.
