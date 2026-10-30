# Review of `specs/2026-10-29-many-islands-t.md` by gpt-6.1-sol

## 1. Errors, contradictions, unsound mechanisms

- **Target and order of limits are conflated.** “Every island lands in the stable set V\*” is operationalized as “share ≥ 0.99”; meanwhile “islands → ∞ before time” is assessed partly through “which pair each world ends on.” A symmetric infinite-population trajectory need never select a single pair, even when finite worlds do. **Fix:** distinguish asymptotic V\* mass, the finite-time 0.99 proxy, and finite-world consensus. Do not call the proxy proof of “every island,” or finite-world consensus the infinite-first limit.

- **Symmetry claim is overstated.** “Each pair is equally likely across worlds by symmetry” does not establish that worlds reach fair consensus. “Any significant deviation is a bug” is also wrong: valid tests have false positives. **Fix:** state equal probabilities *conditional on a rotation-invariant fair-consensus event*, assuming equivariance of the entire implementation. Report non-consensus and unequal endpoints separately; test equivariance directly.

- **The amended attribution is unsound.** Comparing T and DSL tables “so a T-versus-R difference can be traced to the timeout action rather than to fuel” cannot separate these mechanisms: fuel determines whether the fallback executes. **Fix:** cross fallback convention with fuel, holding programs fixed.

- **Fitness units remain ambiguous.** “Payoffs in sixths,” “P_fail is in dollars,” and “Fitness exp(w·(payoff − charge))” require an explicit common unit. **Fix:** specify the conversion and the unit in which w = 0.3 was calibrated; assert numerical fitness ratios on hand cases.

## 2. Design flaws or confounds

- **“Exact ODE” overstates numerical and initialization certainty.** The vector field may be exact, but its initial law is estimated from finite founding pools, and its integration is numerical. Three pools do not automatically supply reliable intervals near basin boundaries. **Fix:** distinguish kernel exactness from sampling/integration error; refine tolerances and pool size near changing verdicts, and propagate founding uncertainty.

- **Charge comparisons mix founding selection with migration selection.** The charge can remove readers before the ODE starts. **Fix:** cross both founding laws with both migration charges, including the A/forfeit-only controls; report founding-mediated versus post-founding effects.

- **A small residual need not imply convergence.** Rare fixation can produce extremely slow transients; boundary equilibria also have infeasible perturbation directions. **Fix:** specify convergence tolerances, horizon-extension rules, and support-aware stability analysis on the simplex tangent space. Report unresolved cases rather than “limits.”

## 3. Predictions likely wrong

- **Prediction 5’s justification is insufficient.** Free reading against constants does not guarantee persistence when resident readers expose migrants to charged recursive encounters. I predict a lower reader marginal and slower conversion under A_f, potentially basin-dependent; I would not confidently predict V\* ≥ 0.95.

- **Prediction 4’s finite-time consensus forecast does not follow from a positive eigenvalue.** Escape time depends on growth rate, initial noise and nonlinear dynamics. Predict consensus only where the measured eigenvalue implies escape within the event budget.

## 4. Missing controls or cheap additions

- Validate rotation-equivariance of payoff, charge and kernel tables exhaustively.
- Stratify injection validation by selection coefficient and timeout pattern; post-anneal sampling can miss rare decisive transitions.
- Add small controlled symmetry-breaking perturbations at several amplitudes; compare growth with the Jacobian.
- Predefine tilt weights exactly and handle absent outcome classes explicitly.

## 5. Alternative explanations not ruled out

Success could reflect the curated finite library, fixed fuel caps, or class-reweighting-induced reader enrichment—not a general property of realizable source readers. Report support/transition structure and qualify conclusions accordingly.
