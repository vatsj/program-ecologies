# Review of `specs/2026-10-25-encounter-contracts.md` by gpt-6.1-sol

## 1. Errors or unsound mechanisms

- **The clock amendment does not resolve the rare-migration limit.** “Spontaneous transitions are kept as rates on the within-island clock (per generation)” conflicts with using “the rare-migration jump chain” while genesis remains active at fixed ν. If migration intensity is m, a positive spontaneous rate g becomes g/m on migration time and diverges as m → 0. Adding the two measured rates without this rescaling defines a different object. **Fix:** specify the two-timescale generator. Before migration, collapse closed within-island recurrent classes and average over their invariant laws; otherwise report finite-m dynamics or explicitly decline the rare-migration limit.

- **Copying is not copying the specified object.** C promises “a whole contract: every member’s fill, keyed as written,” but draws “the set S′ of slots that currently carry fills for p … with one fill per slot drawn by frequency.” This combines unrelated installations, changes the original coalition, and can manufacture a grand-coalition proposal from independent genes. **Fix:** either retain proposal-bundle provenance and copy an actual bundle, or rename C as frequency-weighted recombination. Compare these separately if cheap.

## 2. Design flaws or confounds

- **Observed recurrence cannot verify closure.** “Only a verified closed recurrent class is collapsed” needs an operational verification method. Neither 500 nor 5,000 quiet generations excludes rare exits through silent-contract configurations. **Fix:** require structural closure checking over reachable configurations, including eviction recency, or label empirical classes provisional and propagate escape-rate bounds. Do not publish invariant averages as verified from holdouts alone.

- **BR mixes response rationality, equilibrium ambiguity, and acceptance–execution mismatch.** Its worst-equilibrium acceptance rule differs from R even when the actual responder is already best-replying; accepted proposals then execute under different semantics. Logging this does not isolate the cause. **Fix:** add paired proposal-level comparisons using the actual reply, its best-reply status, the worst-equilibrium verdict, and installed payoffs. Report separate effects of non-best-response behavior and equilibrium conservatism.

- **Selection and formation use different payoff objects.** Encounter improvement can reduce a signer’s expected fitness across other encounters with the same key, especially through replacement and eviction. The requested replay measures this, but the interpretation must make it primary. **Fix:** stratify establishment and conversion by expected-fitness sign, not merely founding-encounter gains.

## 3. Predictions likely wrong

- **Prediction 2’s ≥0.15 improvement is poorly motivated.** Local acceptance supplies neither positive expected selection nor protection against exits from efficient islands. My prediction: gains are heterogeneous, with no robust 0.15 uplift across ν and N; expected-fitness-positive installations, rather than acceptance counts, predict conversions.

- **Prediction 7’s ordering is unjustified.** Restricting writes can block harmful transitions as well as beneficial ones. I expect non-monotone H/H-top efficiency differences and no general enrichment of hooked programs. The registered counter-prediction should replace the proposed monotonic mechanism, not merely accompany it.

## 4. Missing controls or cheap additions

- Make NR non-cuttable: it is the direct control for whether responder evaluation matters.
- Match B on **realized recipients**, not “up to 9”; report recipient count and broadcast-induced payoff changes.
- Estimate α uncertainty across independent source islands/configurations, not by treating all migrant events as independent Bernoulli trials.

## 5. Alternative explanations not ruled out

Higher efficient share could reflect reduced exit rates rather than clearing dominated islands; apparent coverage could be long transients; apparent contract selection could be hitchhiking with successful programs. Report entry/exit decomposition, boundary invasion rates, and contract-ablation replays of successful lineages.
