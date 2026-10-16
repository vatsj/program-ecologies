# Review of `specs/2026-10-16-pangaea.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes

- **Geometry is confounded with certificate-production intensity.** With \(r=N/2\), increasing island size also increases production encounters per individual per generation. A Pangaea victory could reflect repaired production coverage rather than selection favoring openness. **Fix:** retain the specified path, but add a fixed-\(r\) comparison spanning an island cell and Pangaea; report production attempts, successful certificates, and coverage through establishment.

- **The proposed cap validation does not establish equivalence.** “No change beyond run-level uncertainty” with 20 runs can hide substantial effects, and agreement at \(N=3{,}200\) need not transfer to \(12{,}800\). **Fix:** prespecify equivalence margins for establishment probabilities, times, and coverage. Validate an endpoint subset against uncapped runs or an exact accelerated implementation. Otherwise describe capped Pangaea as a different production regime.

- **Twenty runs cannot substantiate the registered reliability claims.** Even 20/20 successes gives a one-sided 95% lower confidence bound of only about 0.86, not 0.95. Prediction thresholds and falsifiers also leave unexplained gaps. **Fix:** label these as predictive point thresholds, report exact binomial intervals, and predeclare pass/fail/inconclusive regions. Increase replication adaptively only under a registered rule.

- **Finite-horizon endpoints do not identify the large-population lottery.** Two Pangaea sizes cannot distinguish vanishing failure probability from a persistent tail; 2,000 generations may represent different stages across cells. **Fix:** report unresolved trajectories separately from losses, and define establishment/absorption criteria independent of the reporting horizon. Restrict conclusions to tested sizes unless supported analytically.

### 2. Predictions likely wrong

- **“Strictly fitter at every frequency,” hence zero scramble failures, is unjustified.** Without self-interaction, a singleton prudent cooperator gets no own-kind benefit; advantage may vanish after unconditional cooperators disappear. Actual certification state can further invalidate the ideal payoff comparison. Selection advantage also does not imply survival in a finite Moran population. **Prediction:** Pangaea improves establishment, but all-defect remains possible. Derive fitness differences from executable, time-dependent states—not only ideal family tables.

- **Monotonicity and the specified crossing are overconfident.** Pooling suppresses local clique nucleation, but larger islands also change drift, production, migration, and certificate spread. **Prediction:** lower clique success overall toward Pangaea; neither strict monotonicity nor the proposed crossing is presently warranted.

- **A universal winner need not be PrudentBot’s network.** Majority resolution selects among surviving compatible basins, not necessarily the designated target. **Prediction:** target success will depend strongly on early certificate coverage and surviving bridge copies.

### 3. Missing controls/cheap additions

- Draw one global founder multiset per replicate and randomly partition it across geometries; record individual identity multiplicities, not just total TwinD copies.
- Run deterministic frequency dynamics for the exact seed families with certificates saturated, alongside actual production. This separates payoff selection from verification access.
- Report \(P(C,C)\), compatibility of occupied holders, target-network share, and absorption status separately.
- Record early extinction of prudent founders, bridges, and individual clique identities; aggregate TwinD mass hides the relevant frequency dependence.
- Distinguish one donor’s demographic extinction from failure of certificate dissemination.

### 4. Alternative explanations not ruled out

Pangaea success could result from faster production, reduced loss of rare bridges, or pooled founder survival—not openness’s superior growth. Target dominance could reflect initial abundance rather than a unique selective advantage.

### 5. Beyond this experiment

Nothing material.
