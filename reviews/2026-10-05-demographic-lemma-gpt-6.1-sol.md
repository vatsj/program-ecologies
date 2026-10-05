# Review of `specs/2026-10-05-demographic-lemma.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes

- **Payoff neutrality is not fitness neutrality.** Even with zero remainder, a prover’s payoff equals the mean payoff, but \(e^{w\pi_q}\neq\overline{e^{w\pi}}\). At \(x_A=x_D=1/2\), its relative fitness is \(1/\cosh(0.15)<1\). Thus the claimed martingale already fails at \(x_o=0\). **Fix:** derive drift using mean exponential fitness; bound its integrated effect separately from remainder effects.

- **Lemma D needs a precise cap convention.** “Size stays below \(K\)” cannot mean conditioning on that future event while retaining the proposed unconditional bound. An unrestricted neutral Moran lineage eventually survives with probability \(k_0/N\), contradicting a bound tending to zero. **Fix:** prove a bound for a process killed upon reaching \(K\), then add the probability of hitting \(K\) for actual survival. State clock conventions explicitly. Conditioning on an endogenous background path does not automatically produce an independent branching process.

- **The stopping-time bound is not implied by the fixed-time lemma.** Survival-dependent \(\tau\) cannot simply replace \(T\) inside an expectation; this is not merely a Jensen gap. **Fix:** retain deterministic-time guarantees, or derive a valid stopped-process inequality. Separate ALLC extinction, freeze, and administrative censoring.

- **Task 2 assumes the dependence structure it needs to prove.** Rare lineages need not be exchangeable, and conditional negative association is unestablished. The defined event-level \(r_q\) also differs from a per-founder dependence correction. Moreover, replacing actual conditional survival probabilities by upper envelopes does not justify the stated covariance formula. **Fix:** write an exact per-founder conditional union bound first; identify each additional assumption before converting it into a fixation bound involving \(\tilde\rho\) and \(h_q\). Measured \(r_q\) yields a confidence-qualified empirical bound, not a theorem.

- **Establishment events are not independent trials.** Compatible copies jointly create frequency-dependent advantage; scramble survivors have a broad size distribution. \(E[k_\tau]\) alone does not determine \(E[u_{k_\tau}]\). **Fix:** predict establishment from the measured post-scramble state distribution and the appropriate multi-type fixation function.

### 2. Predictions likely wrong

- **The saturation formula is structurally wrong for a compatible pooled family.** With initial frequency \(\mu_{\rm est}\), the diffusion instead gives
  \[
  u(\mu_{\rm est})\approx
  \frac{\operatorname{erf}(\mu_{\rm est}\sqrt{Nc/2})}
       {\operatorname{erf}(\sqrt{Nc/2})}.
  \]
  Its small-probability expansion agrees with the proposed square-root law, but saturation differs: approximately **0.69**, rather than **0.56**, at \(N=6400\), before scramble losses and spoilers. Prediction: square-root scaling can hold locally without validating independent-founder saturation.

- **\(r_q\ge1\) and positivity in every cell are unsupported.** Competition can produce negative association; shared favorable backgrounds can produce substantial positive association. Prediction: no universal interval without controlling background duration and lineage interactions.

- **\(E[k_\tau]\approx1\) is not guaranteed.** Exponential-fitness curvature produces systematic loss even without a remainder; its magnitude depends on scramble duration.

### 3. Missing controls/cheap additions

- Benchmark direct D-sea simulations against the **exact finite-\(N\) birth–death fixation formula**, including self-interaction conventions.
- Save \(k_\tau\), cap crossings, background exposure, and censoring reason; compare \(E[u_{k_\tau}]\) with \(u_1E[k_\tau]\).
- Distinguish “any compatible family fixes” from “this labelled target fixes.”

### 4. Alternative explanations

Apparent \(N^{1/2}\) scaling could reflect frequency-dependent escape while concealing scramble losses, survivor clustering, or changing family composition. Four-island success near one poorly discriminates competing single-island formulas.

### 5. Beyond this experiment

nothing material
