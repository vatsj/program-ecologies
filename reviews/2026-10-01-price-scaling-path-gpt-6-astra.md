# Review of `predictions/2026-10-01-price-scaling-path.md` by gpt-6-astra

## 1. Design flaws/confounds and fixes

- **Excluding cells with >1% polymorphic mass is outcome-dependent censoring near the proposed boundary.** Establish whether this mass is numerical error or genuine recurrent structure. Audit fixation calculations in log space, transition cutoffs, stationary residuals, and communicating classes. Rerun suspect cells at higher precision. Unresolved cells make that path’s verdict indeterminate, not eligible for silent exclusion.
- **Finite-range monotonicity cannot falsify an asymptotic efficiency conjecture.** Crossovers can violate every listed “falsifier” while preserving D; increasing cooperation need not converge to one. Label these tests of the finite-size predictor. Report local slopes and exact-rate crossover diagnostics separately from conclusions about the limit.
- **The free-arm extrapolation mixes odds and probabilities.** The predictor section calls 0.80/0.87 *odds*, whereas verdict 6 calls them P(C,C). Those odds imply probabilities 0.444/0.465 in a two-outcome reduction. Define precisely whether “odds” means P(C,C)/(1−P(C,C)) or cooperative/D stationary mass; mixed outcomes make these different. Correct this before freezing predictions.
- **Two representative edges need not control the full chain.** Agreement at one fixed price does not establish validity along shrinking-price paths or at n=8. Include mutation-weighted aggregate fluxes between cooperative, ALLC, and defective classes, and compare their scaling with the representative-edge predictor.

## 2. Predictions likely wrong

- **“A neutral lineage reaches about √N copies” is not a typical-lineage statement.** Starting at one copy, neutral gambler’s ruin gives Pr(reach k before extinction)=1/k. Most lineages disappear quickly. The √N scale instead arises from the fixation integral under frequency-dependent selection: accumulated selection becomes order one there. I expect the same threshold under the stated payoff structure, but not for the proposed neutral-lineage reason.
- **“Only α>1 converges to the free arm itself” conflates odds ratios with outcomes.** At α=1, a constant odds penalty still allows both arms’ P(C,C) to approach one. I predict convergence in cooperation probability under the conjectured free-arm asymptotics, but not relative-odds equivalence.
- **The generalized threshold α>1−β needs another condition.** If the stated entry barrier remains applicable, it also requires controlling Nc². For β>1/2, α>1−β can hold while α<1/2 and entry is exponentially suppressed. Keep β=1/2 as the asymptotic claim; treat 0.56 only as a provisional finite-window slope crossover.

## 3. Missing controls/cheap additions

- Add one α>1 path to test the claimed relative-odds convergence.
- Add α≈0.55–0.6 to probe the proposed finite-size crossover; the current grid cannot locate it.
- Use newly measured free-arm cells in a separately labelled, updated predictor; retain the original extrapolated predictions for scoring.
- Add diagnostic chains separately removing entry costs and the ALLC cost advantage. Strict exits being numerous does not establish that they cause the stationary decline.

## 4. Alternative explanations not ruled out

- Changing dominance among prover families, mutation-target multiplicities, or return routes could mimic the fitted exponent.
- Numerical loss of exponentially small rates could create apparent terminal classes or cooperation plateaus.
- n=6 fixes the program repertoire and makes atoms identical to depth pricing. Agreement at one n=8 path would not establish robustness to richer programs or pricing definitions.
- Continuity of the ε→0 stationary chain at c=0 requires justification if recurrent classes change; continuity of individual rates alone is insufficient.

## 5. Beyond this experiment

Nothing material.
