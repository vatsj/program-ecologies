# Review of `specs/2026-10-14-realizable-scaling.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes

- **The endpoints do not identify an efficiency limit.** P2 holds N = 100 fixed: increasing I need not improve a typical island, and can reduce P(every island efficient). A fraction ≥0.95 is not evidence that this probability approaches 1. Separate mean island efficiency, a randomly sampled island’s failure probability, and all-island success. State finite-size conclusions; reserve convergence claims for growing-N paths with an explicit failure-rate scaling hypothesis.

- **Seeded abundance is confounded with geometry.** At fixed prior, copies grow with NI; an across-cell exponential fit cannot establish that copies alone determine universality. Add a small crossed panel: hold seeded TwinD counts at 0, 4, 8, and 16 across selected geometries, preserving total population. Estimate the clique-free baseline separately; a cell whose baseline is below 0.5 has no absolute 50% crossing.

- **The mass-matched ablation changes two things:** it removes cliques and strengthens their prudent-open competitor. It does not isolate identity abundance. Add a replacement control allocating removed mass proportionally among existing nonidentity types, and paired seed-level substitutions. Describe the current ablation as a joint intervention.

- **Finite horizons confound failure with slow resolution.** Specify “main cells” before launch; the extension/drop rules are currently ambiguous. Measure time in consistent generations or events per individual, report right-censored resolution times, and distinguish unresolved from demonstrably absorbing patchworks. A 10,000-step endpoint cannot establish permanence.

### 2. Predictions likely wrong

- **Prediction 1’s P2 improvement is unsupported.** With fixed local N, I primarily changes coverage and connectivity, not local founding quality. My prediction: mean efficient-island fraction roughly plateaus along P2; all-island success can decline unless migration repairs failures sufficiently rapidly.

- **Prediction 4 is untenable as a blanket donor prediction.** C-donor already achieves 20/20 in a reported size cell; a universal-run probability ≥0.85 leaves less than 0.2 improvement available. Predict little detectable donor gain where the fixed-migration arm is near ceiling, and gains only for bridged, migration-limited failures. Bridge-less rivals should not be rescued merely by raising migration.

- **Prediction 5 likely fails.** Existing evidence already makes the threshold geometry-dependent, including a clique-free baseline below 0.5. My prediction: establishment per seeded copy and baseline-adjusted identity failure vary with N and I; raw counts will not collapse universally.

### 3. Missing controls/cheap additions

- Pair seeds across migration and rule arms; deduplicate overlapping path cells and the identical N = 100 migration settings.
- Calibrate T_nuc using independent runs under the realizable machinery, with a predefined measurement and tuning rule; verify x separately by rule.
- Record clique establishment **per copy**, occupied islands, copies per occupied island, surviving bridges, and minted versus seeded identity lineages.
- Preregister confidence intervals and treatment contrasts. Twenty runs cannot resolve modest probability differences reliably; even 20/20 leaves substantial uncertainty about near-certain success.

### 4. Alternative explanations not ruled out

Donor success may reflect guaranteed local certificate access rather than superior scaling. Declining universality may arise from more opportunities for any local failure, not a global abundance threshold. Ablation gains may reflect competitor reinforcement. Migration may change founding composition rather than resolve established rivals.

### 5. Beyond this experiment

Formulate the path claim through the island failure rate q(N): all-island success requires control of joint failure dependence and, sufficiently, I(N)q(N) → 0. This makes the admissible geometry an explicit research target rather than an extrapolation from endpoint efficiency.
