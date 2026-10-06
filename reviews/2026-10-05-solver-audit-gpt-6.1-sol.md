# Review of `specs/2026-10-05-solver-audit.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **The audit’s trigger is circular.** A census of the *solved, pruned chain*, gated by its estimated π mass, can miss precisely the deep states whose mass the solver suppresses. θ-insensitivity also does not establish correctness: both thresholds can omit the same trap. **Fix:** enumerate candidate recurrent supports independently of published π, or certify exploration completeness. Re-solve every listed cell unconditionally; if enumeration is incomplete, explicitly limit the audit’s conclusions.

- **Log-domain arithmetic does not validate the chain construction.** Expanding every *known* deep state can still omit supports, transitions, or indirect exit routes. **Fix:** separate state-discovery, transition-rate, and stationary-solver checks. Validate a small exhaustive instance against an independent arbitrary-precision calculation. Report unexplored-state counts or bounds, not just convergence.

- **Twin drift risks changing the model during a solver audit.** If previously omitted twin transitions are restored only after the numerical correction, differences conflate arithmetic, exploration, and transition-model changes. **Fix:** compare old versus new solver on identical rates first; then add twins as a separately labelled intervention. Preserve mutation-prior weights and class multiplicities; specify whether \(1/(x_rN)\) is a conditional fixation probability or the complete transition rate.

- **The classification needs an operational definition.** “Some outside mutant neutral or advantageous” does not establish bistability; internal instability and cycles are separate possibilities. **Fix:** test resident-support stability and classify all admissible outside mutants using stated invasion criteria and neutrality tolerances. Call non-deep mixtures “non-deep,” unless bistability is independently demonstrated.

## 2. Predictions likely wrong

- **Prediction 2’s confidence is unjustified.** Finding the dominant-looking trap does not guarantee its stationary weight: a missed rare exit or competing trap can change occupancy by order one. **My prediction:** dollar corrections will be larger than PD corrections, but trap identity and the ±0.1 bound are genuinely unresolved; neither should be the default verdict.

- **Prediction 3’s rationale is insufficient.** Constant-size supports and promoted-state GTH do not ensure complete transitions or numerically accurate rates. **My prediction:** agreement is plausible, but should follow validation rather than support size.

- **Prediction 4 is too strong.** Payoff identity on the resident support need not imply identical interactions with outsiders. Twin drift can expose a qualitatively different exit. **My prediction:** identity changes are possible wherever twins differ off-support.

The prediction tolerances and falsifiers also leave gaps: e.g. a 0.15 dollar change violates “within 0.1” without satisfying the ≥0.2 falsifier. Align them.

## 3. Missing controls / cheap additions

- Include a previously demonstrated failing modal-dollar cell as a positive control and an exhaustive no-deep-state cell as a negative control.
- Test both **underflow** and **missed-state exploration**; one hand-built numerical example cannot pin both failures.
- Report precision sensitivity, stationary residuals, and rate-level agreement. Small residuals alone are insufficient for nearly reducible chains.
- Report every discrepancy, not only ≥0.05 corrections.
- Twin-path maxima are not stationary weights. Compute the twin-expanded stationary distribution; retain best-path exponents as diagnostics.

## 4. Alternative explanations not ruled out

Changes could arise from mutation-prior aggregation, payoff/class-table translation, mixed-state discretization, or omitted transitions rather than deep-state underflow. Finite-\(N\) agreement also does not certify earlier \(\lim_N\) claims; that requires rate scaling or asymptotic resistance analysis.

## 5. Beyond this experiment

nothing material
