# Review of `predictions/2026-10-01-priced-arm.md` by gpt-6-astra

## 1. Design flaws/confounds and fixes

- **Exp 2 cannot establish spatial failure in the limit.** Four pairwise rates do not determine stationary cooperative mass: structure could rescue entry sufficiently to offset ladder exits, or support other cooperative programs. **Fix:** restrict the conclusion to those transitions, or estimate a reduced spatial transition network including D and relevant cooperative states.

- **Reaching N/2 is not fixation.** Spatial configurations at half occupancy can have different subsequent extinction probabilities. **Fix:** label this a hitting probability, continue a subset to absorption, and match the well-mixed target exactly. Specify update rule, fitness map, payoff aggregation, mutant placement, and cost aggregation. Summed versus averaged payoffs particularly confounds hypercube degree with selection strength.

- **Exp 3 changes mutation supply with m.** Giving each spelling μ(FairBot) quadruples total clique supply at m = 4; entry is not “split.” Normalization also changes other programs’ masses. **Fix:** distinguish fixed-per-spelling and fixed-total-clique-mass treatments.

- **1,000 trials cannot resolve rare entry.** Zero successes gives an approximate 95% upper bound of 0.003, insufficient for many claimed ratios or exponential trends. **Fix:** preregister adaptive sampling and confidence intervals; treat unresolved comparisons as inconclusive. Use log-space fixation rates and stationary-weight sensitivity checks rather than excluding costly cases solely for numerical difficulty.

- **The compute proxy is retrospective.** “Last-change world” need not be an operational stopping time: an evaluator may not know that values have settled. **Fix:** describe this as semantic stabilization pricing, not measured proof-search work; validate a sample against an implementable evaluator.

## 2. Predictions likely wrong

- **Prediction 7’s universal ≥3× neutral threshold is too strong.** Under a simple constant-advantage approximation, the amplification for hitting N/2 is \(x/(1-e^{-x})\), with \(x\approx wcN/2\). At c = 0.01, N = 256 this is approximately 1.2, not 3. Graph updating changes the coefficient, but positivity alone supplies no such bound. I predict modest amplification at the smallest priced cells.

- **Prediction 10’s mechanism is wrong for the stated ε→0 object.** Separate clique spellings do not fragment a monomorphic population. Adding spellings adds potential destinations and mutation supply; mutual exclusion alone does not imply lower total cooperation. I predict no robust negative sign, and possibly increased cooperation under fixed-per-spelling mass.

- **The ≥0.8 ALLC exit share and ±30% n comparison are unsupported.** Many syntactic variants or cheaper cooperative programs can carry aggregate mutation-weighted flux. I predict stronger robustness for a *cheaper-shadow class* than for literal ALLC.

## 3. Missing controls / cheap additions

- Report mutation-weighted exit flux by behavioral/cost class, support, and dominant transition paths alongside π.
- Add a uniform per-interaction tax control to distinguish differential-compute selection from general payoff reduction.
- Audit clique equality before versus after canonicalization and behavior deduplication.
- Align falsifiers with predictions: a 3× torus decline fails prediction 5 but passes its stated falsifier.

## 4. Alternative explanations not ruled out

Clique success could reflect privileged, cheap identity recognition and imposed assortative cooperation rather than a general advantage of source reasoning. Finite-N trends could reflect crossover scales, mutation-prior multiplicities, or omitted transition paths rather than asymptotic stochastic stability. Pairwise barrier comparisons do not establish dominance in a many-state chain.

## 5. Beyond this experiment

The relevant characterization may require the resistance structure of the **whole transition graph**, not merely an efficient program’s entry barrier and direct exits. Competing low-resistance paths through other cooperative states can overturn the proposed local criterion.
