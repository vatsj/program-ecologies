# Review of `predictions/2026-09-30-modal-arm.md` by gpt-6-astra

### 1. Design flaws/confounds and fixes

- **The falsifiers do not test limiting efficiency.** A finite-N peak can precede eventual convergence to 1; increasing cooperation through N = 30,000 does not establish that convergence. A strict FairBot invader would refute unfakeability, not necessarily efficiency supported by other programs. **Fix:** separate finite-range predictions, the unfakeability claim, and the asymptotic efficiency conjecture.
- **Local FairBot rates do not determine stationary mass.** The two-state approximation omits indirect entries, cooperative intermediates, and other metastable sets. An accessible, unfakeable efficient state alone does not establish stationary concentration there. **Fix:** report the full transition structure and aggregate stationary flows across cooperative/noncooperative states; identify competing slow traps and their N-scaling.
- **The limiting object needs explicit specification.** State the replacement rule, payoff/self-interaction convention, mutation proposal, truncation/renormalization, and whether π comes from the ε→0 monomorphic chain. “Per-mutant rates” and per-generation rates differ. **Fix:** define the order of limits; do not extrapolate fixed-n results to an unbounded program population.
- **Evaluator agreement validates implementation, not the advertised provability interpretation.** Agreement with recursion on the same linear frames does not independently establish that the two-box semantics implements PA and PA + Con(PA). Guarded uniqueness alone does not establish that equivalence either. **Fix:** supply the applicable soundness/equivalence argument, including cross-level self-reference, and a certified stabilization criterion.

### 2. Predictions likely wrong

- **“Every exit … is by a neutral mutant” is too strong at finite N.** Under standard stochastic replacement, deleterious mutants can fix. Also, equal payoff when rare does not imply neutrality throughout fixation. **Prediction:** strict advantageous invasion is absent, but deleterious substitution flow is positive; genuinely neutral substitutions may dominate asymptotically.
- **PrudentBot’s small μ does not imply negligible π.** Stationary weight depends on incoming flow and residence time. Its smaller exploitable shadow mass could compensate partly for rare direct introduction. **Prediction:** direct introduction is rare; its stationary weight remains undetermined without outgoing rates and indirect entries. Likewise, ±20% agreement across n is unsupported by these static facts.
- **The crossover arithmetic is optimistic.** Using the quoted ratio \(r(30{,}000)=0.8\) and \(r\propto\sqrt N\), 90% cooperation requires \(r=9\), hence \(N\approx3.8\times10^6\), even under the two-state approximation—not approximately \(10^6\).
- **“Free proof search is an upper bound” is unjustified.** Enlarging capabilities need not monotonically improve evolutionary efficiency, and this grammar also removes capabilities. Treat it as a distinct idealized arm, not a bound.

### 3. Missing controls/cheap additions

- Report stationary inflow/outflow by destination class, including deleterious substitutions; compare the two-state estimate directly with computed π.
- Check fixation calculations independently for ALLC, FairBot, and PrudentBot, including payoff differences across mutant frequencies.
- Remove second-level boxes at matched truncation/prior conventions to isolate their contribution. Report how truncation changes total prior mass on shared behaviors.
- Report stationary residuals and numerical precision checks: rare transitions can control π.
- Label these as post-hoc diagnostics; preserve the committed predictions unchanged.

### 4. Alternative explanations not ruled out

Increasing cooperation could reflect finite-range redistribution among traps, truncation-dependent mutation mass, or grammar-specific accessibility—not the proposed characterization. Weak/modal differences also combine provability with removal of simulation and randomness.

### 5. Beyond this experiment

Nothing material.
