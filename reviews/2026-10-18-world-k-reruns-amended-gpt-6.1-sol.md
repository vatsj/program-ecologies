# Review of `specs/2026-10-18-world-k-reruns.md` by gpt-6.1-sol

1. **Errors / unsound mechanisms**
   - **The rain amendment breaks the matched comparison.** “world L rerun beside K on paired founders as the reference” conflicts with “rain under K … against its stored L numbers.” Stored L may differ in production rate, kernel, or stopping schedule. **Fix:** rerun the rain cell in L with identical settings and paired founders; retain historical numbers only as context.
   - **Snapshots cannot identify when conversion occurred.** “contingency table … at generations 200, 2,000 and 10,000” does not support “showing whether K converts L’s identity islands to open ones during establishment or during migration.” Worlds can diverge before generation 200, and corresponding island labels need not represent corresponding lineages. **Fix:** log establishment times, holder transitions, and migrant ancestry; otherwise describe snapshot associations, not conversion mechanisms.
   - **Production units remain ambiguous.** “r = 100 production encounters per Moran event” becomes “constant production per program.” These are not interchangeable without an event convention. **Fix:** specify encounter allocation, eligible producers, replacement sampling, and production opportunities per individual per generation.

2. **Design flaws / confounds**
   - **Twenty runs cannot substantiate the proposed equivalences or rare-event bounds.** Island outcomes within runs are dependent; 20/20 successes still leave substantial uncertainty. “Within 0.1,” “≤ 0.005 per island,” and “indistinguishable (within 1–2 runs)” need different analyses. **Fix:** make runs the independent units, specify confidence level and paired interval method, and label underpowered comparisons inconclusive rather than equivalent. Pre-register run-level aggregation and handling of multiple cells.
   - **The production-rate control does not cover the strongest establishment claim.** Controls stop at N = 3,200, while the prediction concerns N = 6,400 and the counter-prediction includes 12,800. Key coverage depends on distinct partner quotes, not merely encounter count. **Fix:** add a native-rate control at 6,400, or limit the conclusion to constant-budget dynamics; log distinct-key coverage and certificate eviction as well as encounter-weighted matches.
   - Finite horizons cannot establish disappearance of permanent rivals or large-population universality. **Fix:** distinguish unresolved runs from absorbing failures and report resolution-time censoring.

3. **Predictions likely wrong**
   - **Prediction 3’s inference is unjustified:** removing identity holders does not remove copy-count dependence from non-identity rivals, bridge loss, or production coverage. **My prediction:** the identity-associated decline weakens, but some dependence on total founders and geometry remains.
   - **Prediction 5 is too optimistic:** increased μ_net is not increased establishment mass unless the added readers survive predators and obtain useful certificates. **My prediction:** a smaller improvement than the proposed 5/20 to ≤2/20, potentially no detectable change.
   - **Prediction 4 conflates outcome and mechanism:** self-production can alter coverage and self-defection even without minted cliques. **My prediction:** near-ceiling universality may mask reproducible differences in establishment time and founder survival.

4. **Missing controls / cheap additions**
   - Test keyed-certificate rejection against a different quote, acceptance against its production partner, self-play, copying, and eviction—not just agreement with existing tables.
   - Classify identity behavior conditional on reachable certificate inventories; source templates alone need not determine behavior.
   - Report P(C,C), target-network membership, and transition support separately; an “open” label is not itself efficiency.

5. **Alternative explanations not ruled out**
   - K may improve outcomes by suppressing defection generally rather than specifically dissolving identity barriers.
   - Faster resolution, changed cache occupancy, or reduced self-production waste could explain endpoint gains without changing eventual outcomes.
   - The selected grammar and fixed prior may omit alternative identity channels; conclusions should remain grammar-relative.
