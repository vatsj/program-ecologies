# Review of `specs/2026-10-16-annealed-mutation.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes

- **Mutation exposure is not successful-colonization exposure.** The formulas assume arrivals meet established, eligible residents and have time to fix. Annealing delivers half its arrivals by generation 50, overlapping founding/regrowth; constant rain encounters different residents and leaves less follow-up for late arrivals. Increasing \(N\) can also lengthen fixation, making incomplete drift look suppressed. **Fix:** log arrival time, resident state, lineage fate and unresolved lineages; add a mutation-free chase and compare cohorts at matched follow-up. Distinguish founding effects from post-establishment effects.

- **The cure prediction is not numerically justified.** At \(N=800,\Lambda_0=0.03\), there are only \(N\Lambda_N=12\) arrivals per island. The proposed formula gives \(1-e^{-3.12\mu_{\rm pred}}\); reaching 0.8 requires \(\mu_{\rm pred}\ge0.516\). **Fix:** compute the applicable predator prior mass before launching, stratified by rival type. If this threshold is not met, revise the prediction or increase exposure.

- **A fourfold size range cannot establish the scaling limit.** “Within a factor 2” around the predicted twofold decline includes no decline. Fixed \(I=16\) also cannot establish drift-free behavior along growing-island paths: aggregate drift scales approximately as \(I\Lambda_N\), not just \(\Lambda_N\). **Fix:** frame this as a finite-size diagnostic, specify a slope/effect-size criterion, and explicitly restrict conclusions to fixed \(I\). Preserve at least one larger-\(N\) diagnostic if affordable.

- **Predictions and falsifiers leave unregistered gray zones.** Examples include cure probabilities between 0.5 and 0.8, drift-free fractions between 0.2 and 0.5, and identity comparisons not covered by the stated falsifier. **Fix:** distinguish supported, contradicted and inconclusive outcomes in advance. Define arm (iv) separately for both founder regimes.

### 2. Predictions likely wrong

- **“Only \(\Lambda\) matters” is unlikely.** Neutrality, predator fitness and susceptible-resident abundance change during establishment. I predict schedule-dependent outcomes, without a defensible direction before measuring those state-conditioned hazards. Overlapping intervals would not establish equivalence; register an equivalence margin.

- **The ≥0.8 cure prediction is likely too high** unless predators comprise over half the applicable arrival prior, or migration/secondary spread amplifies direct injections. My direct-injection prediction is the formula above, using measured eligible mass rather than an assumed constant.

- **Identity abundance need not exceed baseline at every \(N\).** Rain can both feed identity through shadows and disrupt its establishment indirectly. I predict heterogeneous effects across founder regimes, not pointwise monotonicity.

### 3. Missing controls / cheap additions

- Add delayed annealing beginning after establishment, preferably from saved resident snapshots shared across schedules.
- Run cheap single-arrival assays on frozen target/rival residents at each \(N\), estimating neutral fixation, predator establishment and completion times independently.
- Report cures per initially eligible rival, separating direct injected ancestry from migrant-mediated cures.
- Pair schedules using the same founder identities/order, not merely the same random seed. Test discrete schedule normalization and actual arrival counts.

### 4. Alternative explanations not ruled out

Apparent drift suppression could reflect censoring, changed resident composition or fewer neutral opportunities. Apparent cure improvement could reflect changing rival composition or migration calibration rather than more predator trials. Sponsorship could act through founding priority rather than prevention of shadow-mediated invasion.

### 5. Beyond this experiment

nothing material
