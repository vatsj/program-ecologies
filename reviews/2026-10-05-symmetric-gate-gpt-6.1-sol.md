# Review of `specs/2026-10-05-symmetric-gate.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes

- **The intermediate rule is underspecified.** “Independently per encounter and fixed per source class” describes different stochastic models. Annealed access changes encounter payoffs; quenched class-level access changes which exploitable classes exist. **Fix:** choose and specify the randomization unit, persistence, and treatment of nested boxes. Define whether “reader” means the executing program or the program whose behavior is being proved; test reciprocal and nested queries explicitly.
- **Establishment, extinction, and \(f^*\) are undefined.** At positive mutation, carrier extinction need not be absorbing; crossing 50% need not imply persistence. **Fix:** predeclare hitting thresholds, persistence criteria, censoring, and whether reseeded carriers count. Distinguish deterministic invasion thresholds from frequencies yielding a specified finite-population establishment probability.
- **The mechanistic conclusion overreaches.** Losing establishment after changing access shows that access matters, not uniquely that exploitation of the fringe caused establishment. The rule also alters background–background interactions and subsequent composition. **Fix:** compare payoff matrices on an identical frozen background, then separately measure ecological feedback. The fringe-to-D intervention should hold other actions and composition fixed.
- **Finite windows cannot establish stationary efficiency or large-population behavior.** Report these as trajectory/lottery outcomes, not \(\pi\). Add at least one larger population and state the scaling of mutation, migration, and seed count.

### 2. Predictions likely wrong

- **Prediction 1’s positive deterministic threshold does not follow from its argument.** If the post-scramble background mutually defects and carriers mutually cooperate, then
  \[
  \pi_C=P+f(R-P),\qquad \pi_D=P.
  \]
  Thus selection favors carriers at every positive frequency, though the advantage vanishes as \(f\to0\). Zero linear invasion advantage is not negative growth or a positive \(f^*\). **Prediction:** without costs or cooperative resident payoffs, \(f^*=0\); observed seed thresholds reflect drift and weak frequency-dependent selection. Check the actual payoff matrix before asserting 0.03–0.10.
- **Predictions 2 and 5 consequently lack quantitative support.** A lone carrier’s fate depends on self-exclusion, island replacement, migration, and drift—not simply reaching a proposed threshold. Predict lower symmetric establishment, but not those numerical ranges without a birth–death calculation. The \(k=3\) prediction is also untested by the proposed lottery design.
- **Prediction 3’s ordering is plausible only on a fixed background.** Increasing access can preserve exploitable residents or change competing networks. Frozen-background growth should increase with \(q\) under the claimed mechanism; full-run establishment need not.
- **Prediction 4 conflates conditional cooperation with population efficiency.** Established carriers can coexist with defectors or mutation-generated shadows. Predict high carrier–carrier cooperation, not necessarily population \(P(C,C)\ge0.98\).

### 3. Missing controls / cheap additions

- Add symmetric **\(k=3\)** lottery cells and a pure-carrier invasion challenge with representative defectors/shadows.
- Report carrier–carrier, carrier–noncarrier, and noncarrier–noncarrier action/payoff tables; identify which component changes.
- Include confidence intervals and paired differences. Twenty runs cannot reliably resolve 0.15 differences in success; treat such comparisons as exploratory or allocate more runs.
- Verify the \(b=\infty\) baseline by exact payoff-table equality, not merely similar trajectories.

### 4. Alternative explanations not ruled out

Drift-assisted coordination; early ALLC exploitation before its extinction; carrier-family heterogeneity; background selection under altered access; migration amplification; survivor-conditioned reporting; and finite-window metastability.

### 5. Beyond this experiment

nothing material
