# Review of `specs/2026-10-13-stable-sets-on-islands.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **The proposed weak dominance destroys the symmetric stable set.** Under standard majority feasibility, \((1/2,1/2,0)\) weakly improves coalition \(\{1,2\}\) over \((1/2,0,1/2)\), strictly improving player 2. Thus the three equal pairs are not internally stable under that relation. **Fix:** compute and name the solutions separately for strict-majority dominance and commitment/credible-response dominance; do not assume either inherits the classical stable sets.

- **“Discriminatory elements” are misidentified.** In the classical majority game, a discriminatory stable set fixes one player’s payoff at \(c\), while the others divide \(1-c\). For \(c=1/6\), these are generally three-positive-payoff allocations, not pairs excluding that player. “Unequal pairs” also cannot automatically be labeled dominated interlopers: dominance is not exclusion from every stable set. **Fix:** classify exact payoff vectors by computed set membership, allowing overlaps.

- **Credible-response dominance may not be an outcome-level relation.** Identical realized divisions can arise from programs with different off-path responses. Best replies can also be multiple. **Fix:** specify admissible commitments, feasibility, response tie-breaking, and whether improvement must hold for all or some best replies. Either establish outcome invariance or define dominance on policy profiles.

- **The dynamic object is underspecified.** Mutation rate, fitness mapping, migration topology/weighting, and generation units are missing. At zero mutation, missing founder types cannot reappear; with mutation, horizon support is not absorption or stationary support. **Fix:** register these explicitly and use common observation horizons; treat unresolved dwell times as censored. Add a small \(N\)-scaling panel before making large-population claims.

## 2. Predictions likely wrong

- **Prediction 4 contradicts internal stability.** Direct dominance arrows between members of one stable set cannot exist. Transitions through outsiders may occur, but are not direct external-stability moves. Nor does absence of dominance prevent migration-driven consensus: the supplied chicken results already show bridge-mediated merging. **Prediction:** switches depend on accessible intermediate programs; consensus remains possible. Trace the intermediate invasion sequence.

- **Prediction 2 overinterprets symmetry.** A symmetric prior implies a role-symmetric distribution across runs, not selection of the symmetric stable set within each run. Randomly selected discriminatory sets can collectively preserve symmetry. A small-demand seed also need not produce the classical fixed-\(c\) line. **Prediction:** role symmetry is more robust than symmetric-set selection.

- **Prediction 1 uses the wrong occupancy baseline.** The formula assumes every island lands uniformly on the three members. With total member probability \(q\), coverage is
  \[
  1-3(1-q/3)^{64}+3(1-2q/3)^{64}-(1-q)^{64}.
  \]
  **Prediction:** coverage can be nearly certain even when member occupancy is modest, making it a weak test.

## 3. Missing controls/cheap additions

- Matched modal/weak grammars, demand marginals, and prior masses; uniform demands changes more than symmetry.
- Forced seeds at each candidate member and selected outsiders; measure local entry, exit, and residence times.
- Report efficiency, exact payoff support, and time-window frequencies alongside modal classifications.
- Report **all** stable sets containing observed support. Subset membership need not identify a unique selected set.

## 4. Alternative explanations not ruled out

Founder availability, basin volume, risk dominance, neutral bridges, finite-population drift, and grammar-specific accessibility can explain coverage without stable-set dominance governing selection. The cited myopic-dynamics result requires checking its assumptions against Moran program evolution.

## 5. Beyond this experiment

nothing material
