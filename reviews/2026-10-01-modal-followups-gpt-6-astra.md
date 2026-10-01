# Review of `predictions/2026-10-01-modal-followups.md` by gpt-6-astra

## 1. Design flaws or confounds, and fixes

- **E2’s pruning check validates the wrong observable.** Matching P(C,C) to four decimals does not validate π(PB)/π(FB), rare exits, or support. Small omitted flow can feed long-lived states and materially change stationary weights. Validate `eager_poly=False` against completed cells on PB/FB weights, entry/exit rates, and support; repeat new cells at tighter θ and report ratio sensitivity alongside cut flow.
- **E1’s falsifier does not identify X/`ROLE` as the cause.** A small M0–W0 difference could reflect finite-N crossover, additional box kinds in the full modal arm, or interactions among features. Replace that attribution with “the matched contrast fails to reproduce the original gap.” Isolating X versus `ROLE` requires separate ablations.
- **E3 leaves the estimand underspecified.** Define “generation” as N births or one birth; define burn-in, averaging window, cooperative phases, and whether P(C,C) is interaction-weighted within islands. With three all-D starts, report replicate trajectories and uncertainty, not just a pooled mean. These runs measure finite-time dynamics unless mixing is demonstrated.
- **The channel comparison includes computational power.** M0 gets a sound provability oracle while W0 gets simulation with nontermination handling. State this explicitly; document soundness assumptions and how nontermination is detected rather than approximated by timeout. Otherwise “observation channel alone” overstates the intervention.

## 2. Predictions I think are wrong

- **E3’s 1,500-generation shadow clock is not established.** ε·μ(C) is a per-birth mutation probability, or approximately a population-fraction input per generation of N births—not a population-wide arrival rate. The latter is Nεμ(C). Neutral accumulation also includes reverse mutation and other classes. My prediction: passage times depend on the full mutation–selection dynamics, not simply the reciprocal quoted rate.
- **“D invades once ALLC outnumbers FairBot” is generally wrong.** In an otherwise cooperative FB/ALLC mixture, with ALLC fraction x, rare D earns xT+(1−x)P versus approximately R for residents. The threshold is \(x>(R-P)/(T-P)\), not necessarily 1/2. I predict invasion near this payoff-dependent threshold, modified by other classes.
- **“That would be the ratchet” is too strong.** Two larger-N points exceeding a ratio threshold could be a crossover, not asymptotic support migration. Conversely, your constant-ratio approximation requires stable effective fluxes through a multistate network. My prediction is continued finite-N movement; neither a plateau nor a ratchet is established by these cells alone.
- **Repeated collapses need not be cycles.** I expect stochastic switching or irregular excursions to be plausible alternatives. Reserve “cycle” for demonstrated dynamical cycling.

## 3. Missing controls or cheap additions

- In E1, verify the AST-level correspondence and induced mutation weights; report entry, faker-exit, and shadow-exit rates, not only cooperation and fitted exponents.
- In E3, log FB/ALLC/D and flagged-accelerant abundances around every collapse. Add a cooperative initial condition and a lower-ε big-island condition to distinguish access barriers from cooperative-state instability.
- Reconcile E2’s overlapping verdict regions: “below 0.08” can still be “more than double” 0.037.

## 4. Alternative explanations not ruled out

- Modal gains may reflect free oracle strength rather than a generally realizable source-observation advantage.
- E3’s low cooperation may reflect slow entry from all-D; high cooperation may reflect long transients.
- Island gains may reflect altered drift and local mutation supply, not specifically shadow suppression.

## 5. Beyond this experiment

nothing material
