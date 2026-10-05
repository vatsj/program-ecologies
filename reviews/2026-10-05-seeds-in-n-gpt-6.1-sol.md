# Review of `specs/2026-10-05-seeds-in-n.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **Finite cutoffs cannot establish uniformity in n.** Flat core mass at n = 7–9 neither bounds its infinite-language mass nor bounds survival against later entrants. Fix: describe this as a local cutoff-sensitivity test; reserve uniformity claims for a theorem or tail bound covering all larger n. Separate uniformity in n from the path in (N, I) needed for “almost all seeds.”
- **“Unfakeable” does not imply stochastic persistence.** No strict invasion of a monomorphic resident excludes neither neutral replacement nor losses from mixed populations or migration. Losing a core island would not, by itself, contradict soundness or identify a strict invader. Fix: distinguish monomorphic strict invasion, neutral drift, and mixed-state displacement; reconstruct payoff/transition evidence for each observed loss.
- **The replication cannot resolve several declared thresholds.** With 40/40 efficient runs, the two-sided 95% Wilson lower bound is approximately 0.912—not 0.97. The no-migration controls provide only 160 islands per cell, with roughly eight successes when p ≈ 0.05; ±25% changes are poorly resolved. Fix: predeclare inconclusive outcomes, increase inexpensive no-migration replication, and use uncertainty-aware tests rather than point-estimate falsifiers.
- **Runtime censoring is not dynamical non-resolution.** Stopping expensive cells can selectively remove high-n or slow trajectories. Fix: report administrative censoring separately, completed generations and exposure; predeclare a common generation budget and record partial trajectories.
- **Specify the actual limiting object.** Explicitly state ε = 0, migration sampling/rate normalization as I changes, and the certification rule. Complete-graph enlargement can change effective connectivity as well as the number of seed opportunities.

## 2. Predictions likely wrong

- **Prediction 2:** \(1-(1-p)^I\) assumes independent successful nucleation and effectively guaranteed spread thereafter. No-migration p measures neither under migration. Predict departures in either direction; estimate establishment and subsequent spread separately.
- **Prediction 3:** “Never lost” and “every loss-containing run succeeds” are stronger than unfakeability warrants. Predict occasional core displacement is possible through drift or mixed-state transitions, without a soundness failure.
- **Prediction 5:** Global ALLC extinction is an extreme statistic over islands. Even unchanged local extinction distributions generally produce longer global extinction times as I grows. Predict an I dependence; compare island-level extinction distributions first.
- **Prediction 4:** “Cheapest” needs a defined mechanism in a free-oracle arm. Prior mass, cross-play compatibility, and establishment probability could determine winners instead. Predict composition tracks those quantities, not description length alone.

## 3. Missing controls / cheap additions

- Add no-migration controls at N = 1,600 to test the √N predictor rather than extrapolate it.
- At one representative cell, impose a migration-free establishment phase, then enable migration: directly test nucleation versus spread.
- Log initial core counts, identities, and time to first certified core island; condition outcomes on these.
- Report support, transition structure, and \(P(C,C)\), including unresolved runs—not only terminal labels.
- Fit the predictor with calibration uncertainty and acknowledge saturation at p ≤ 1.

## 4. Alternative explanations not ruled out

Flat outcomes could reflect FairBot’s stable prior mass alone, rather than the entire core. Larger-I success could arise from migration-assisted rescue rather than independent lotteries. Frozen composition could reflect founder effects. Finite-horizon certification could conceal slow leakage. None establishes persistence with realizable, resource-bounded proof search.

## 5. Beyond this experiment

Nothing material.
