# Review of `specs/2026-10-25-pricing-rules.md` by gpt-6.1-sol

## 1. Errors, contradictions, unsound mechanisms

- **Scoring reverses the RPS criterion.** Target: “population exploitability ≤ 0.1”; amendment: “met if the interval lies above the threshold, failed if below.” That would reward exploitability. **Fix:** specify directions separately: RPS exploitability’s upper confidence bound ≤0.1; inspection and PD lower bounds ≥ their thresholds. Operationalize “uniform mixer, or guarded mixers, hold” separately from aggregate exploitability.

- **Cache accounting remains underspecified.** B says “a reader pays a given read once,” but also “later executions … are free, including their subtree.” When a cached ancestor executes a previously unseen descendant, does that descendant become cached despite nobody paying? Likewise, what happens when a first execution is interrupted? **Fix:** define cache insertion, nested-hit precedence, partial execution and first-payer rules; add corresponding tests for B and B-own. Otherwise free ancestor execution can silently prewarm unrelated keys.

- **Falsifiers do not match claims.** “RPS simulators lose to `U` at every P_fail ≥ 0.1” is not falsified solely by “`U` below 0.5 at P_fail = 0.1.” Conversely, absence of a statistically certified adjacent pair need not falsify A’s joint-band prediction: results may be undetermined. **Fix:** distinguish pairwise mechanism tests, ecological targets and inconclusive outcomes.

## 2. Design flaws or confounds

- **Stored stochastic records may not support faithful repricing.** Per-pair mean steps/timeouts need not reproduce selection under random tapes, nested events, nonlinear fitness transformations or evolving certificates. **Fix:** audit whether records preserve the required joint payoff–cost distribution; validate replay against online execution at one nonzero price per game before relying on tables.

- **Power is poorly matched to the headline.** With 20 PD runs, an observed 0.75 success rate cannot certify exceeding 0.7; approximately 19/20 successes are needed with common two-sided interval methods. Requiring every game to pass further reduces power. **Fix:** specify interval methods and anticipated power; allow preregistered expansion for undetermined cells. Report point-estimate overlap separately from certified overlap, and discrete adjacent levels rather than a continuous “band.”

- **B-own does not isolate memoization alone.** It changes ownership, inheritance, migration and exposure to first-payment barriers simultaneously. **Fix:** characterize B versus B-own as different subsidy institutions, not a clean memoization decomposition.

## 3. Predictions likely wrong

- **Prediction 6’s ordering is unjustified.** More subsidy does not monotonically improve ecological outcomes, and inherited memos can favor established lineages differently from island caches. **Prediction:** no universal F–B-own–B ordering; rank reversals are plausible during establishment and migration.

- **A’s reliable joint band is doubtful.** Successful bounded reads remain free, while PD root production/retries retain fuel constraints and forfeiture risks. **Prediction:** A suppresses timeout-heavy RPS strategies without necessarily delivering the RPS target; PD remains closer to its unpriced baseline than under F.

## 4. Missing controls or cheap additions

- Test cache-order dependence by permuting encounter evaluation order under identical founders.
- Log cumulative charges by lineage and phase: founding, production, establishment, maintenance.
- At one price, separate true timeouts from bounded default returns with matched computational effort; otherwise the bounded-simulator control changes both semantics and pricing.

## 5. Alternative explanations

Apparent robustness could reflect free successful computation, first-payer selection, cache saturation or the chosen stopping horizon—not a generally suitable compute price. Larger geometry alone does not separate these; report phase-resolved outcomes and cache saturation versus time.
