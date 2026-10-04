# Review of `specs/2026-10-04-three-player-dollar.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes
- **Three-player program semantics are underspecified.** A binary opponent cannot be called as `THEM_j(ME)` without specifying its other argument, argument ordering, and slot identities. Likewise, `BOX(THEM_j plays a)` needs a fully specified encounter. Define these semantics, recursion/divergence handling, and modal consistency before enumeration; test all slot permutations.
- **The dictatorship statistic is vacuous under symmetry.** With a permutation-invariant grammar, prior, and unique stationary distribution, every slot’s mean share equals expected total payout/3, hence is ≤1/3. Rotating dictators and egalitarian outcomes can therefore score identically. Add encounter-level maximum share, inequality, exclusion probability, and coalition persistence.
- **“Genuine limit cycle” is undefined for this object.** A finite irreducible mutation–fixation chain has a stationary distribution, even with cyclic probability currents. Specify whether Rule 4 concerns currents, metastable transition sequences, or a deterministic limiting process. Report π and directed currents rather than suppressing the stationary result.
- **The limits and mutation clock need specification.** Explicitly take ε→0 at fixed N before studying N→∞; distinguish the monomorphic embedded chain from the full polymorphic process. Define mutation per birth versus per generation and slot-selection probabilities. At N=100, ε=10⁻³ need not ensure isolated fixation events.
- **Language truncation is central, not incidental.** An existential neutral-bridge claim can fail simply because the bridge exceeds n. Freeze matched grammars/priors and budget rules in advance; state conclusions as language-relative. Commit predictions before inspecting invasion tables, which already reveal predicted outcomes.

### 2. Predictions likely wrong
- **Prediction 4:** symmetry predicts exactly efficiency/3, not [0.33, 0.42]. Values above 1/3 indicate asymmetry or error, not evidence of dictatorship.
- **Prediction 5:** a 1/N exit does not imply stationary mass cannot rise with N; stationary weights depend on entry rates and competing exits. I predict its direction is unresolved until those rates are compared.
- **Predictions 1–2:** empty-core reasoning does not establish neutral program bridges or cyclic evolutionary accessibility. Coalition deviations require coordinated action and may face unilateral barriers. Expect some language-dependent trapped or metastable networks, not necessarily rotation.
- **Prediction 3:** the pivot’s alternatives require coordination between the excluded player and the low-paid player. Their preference alone does not cap pivot rents. Fair-versus-unfair pair mass is unresolved.

### 3. Missing controls/cheap additions
- Run the nine constant actions alone as a baseline for ordinary bargaining coordination.
- Verify relabeling invariance of payoffs, mutation rates, and π.
- Report grand-coalition entry and exit rates separately, neutral-bridge prior mass, stationary currents, and mixing-time estimates.
- Since opponents’ populations are fixed during fixation, check whether mutant/resident payoffs are frequency-independent; if so, use exact Moran formulas and analytical large-N rates.
- Replicate finite-ε trajectories with uncertainty intervals; one run per initialization cannot establish dwell times.

### 4. Alternative explanations
Pair dominance could reflect shorter encodings, greater behavioral multiplicity, or unilateral coordination barriers—not a failure of “democracy.” Modal success could reflect oracle semantics rather than realizable source reasoning. Rising grand-coalition mass would **not** establish drift-closure: declining but nonzero exits can produce that result.

### 5. Beyond this experiment
Nothing material.
