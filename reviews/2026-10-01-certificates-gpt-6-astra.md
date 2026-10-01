# Review of `predictions/2026-10-01-certificates.md` by gpt-6-astra

### 1. Design flaws/confounds and fixes

- **Thresholding changes the stationary object.** At finite N, exponentially small clique exits remain relevant to stationary weights. Deleting them and taking an absorption lottery computes a different object. Payoff-symmetric transitions between pure cliques do **not** establish that absorption weights equal stationary weights: paths through other states matter, and absorption depends on initialization. Small dropped stationary flow does not bound stationary-distribution error. **Fix:** solve the unthresholded generator in log/high precision, or derive an effective inter-clique chain. Report the lottery separately as metastable behavior.

- **Finite grids cannot establish lim_N efficiency.** Four N values at two syntax cutoffs establish finite-size behavior, not convergence to P(C,C)=1. A rare longer program with N-independent invasion can reverse the apparent trend. **Fix:** state the order of ε, N, and syntax-cutoff limits; restrict conclusions to each finite language unless accompanied by an asymptotic argument controlling all relevant entry/exit channels.

- **“lfp/gfp” is misleading with negation.** Seeded iteration of a nonmonotone system need not select its least/greatest fixed point; oscillation need not mean no fixed point exists. Locally replacing oscillating coordinates by D can also invalidate equations for settled dependents. **Fix:** specify synchronous updates, dependency closure, cycle detection, and fallback propagation. Call the full evaluators D-seeded/C-seeded iteration, reserving lfp/gfp for monotone systems. Test fixed-point consistency wherever the mirror argument is invoked.

- **The contrast does not isolate only fixed-point choice.** PA provability and stable-value truth are different operators, not alternative selections from one common equation system. Modal fixed-point uniqueness is uniqueness up to provable equivalence, not a blanket unique Boolean valuation. **Fix:** frame this as a comparison of semantic regimes; isolate individual mechanisms with targeted ablations.

### 2. Predictions I think are wrong

- **“gfp cooperation is universal” is already contradicted by the three stated exceptions.** A connected cooperation graph can contain many mutually defecting pairs. I predict connected but incomplete cooperation. Rename this “broad compatibility” and report pairwise coverage rather than connectivity alone.

- **Verdict 8 is stronger than the mirror theorem.** The theorem protects FairBot, but the falsifier quantifies over *any* resident whose cooperation depends on a positive loop. Nothing supplied excludes loop-supported exploitation of compound residents. I predict FairBot remains protected; the broader claim is unresolved and needs exhaustive edge classification.

- **Failure of verdict 7 would not imply a negligible probe-faker channel.** A substantial channel can be offset by different entry rates, class masses, or routing elsewhere. I predict its causal contribution will differ from the raw gfp–Löb gap.

### 3. Missing controls or cheap additions

- Suppress only the identified probe-faker transitions, keeping mutation weights and all other rates fixed; recompute π as a mechanism diagnostic.
- Report μ- and π-weighted mutual-cooperation coverage, worst cross-pair outcomes, and clique completeness.
- Separate theorem checks, already-computed static estimates, and genuinely uncomputed predictions. Reproducing a fixation-chain estimate is validation, not independent confirmation.
- Run threshold-sensitivity checks and exhaustive small-language fixed-point enumeration, including nonmonotone systems with both cycles and fixed points.

### 4. Alternative explanations not ruled out

- Tag dominance reflects authenticated commitment plus the syntax prior’s overwhelming preference for one clique—not generally effective certificate reasoning.
- The gfp–Löb gap may reflect semantic class aggregation, mutation routing, or negation fallback, not principally probe protection.
- Apparent efficiency may be metastable trapping rather than stationary selection.

### 5. Beyond this experiment

Nothing material.
