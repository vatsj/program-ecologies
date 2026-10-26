# Review of `specs/2026-10-25-failure-pricing-confirmation.md` by gpt-6.1-sol

1. **Errors, contradictions, unsound mechanisms**
   - “This run confirms or refutes the default” conflicts with “the PD is met or undetermined with a point estimate ≥ 0.75.” Undetermined is not confirmation, and the default’s prediction still permits cost-blind PD success. **Fix:** distinguish confirmed / refuted / unresolved; require all three cost-aware primary targets to be met for confirmation.
   - “Charges per play below 0.01 of the range” is not tested by “[A’s cost-inclusive count drops by more than 2 runs at any level].” The scoring cutoff is **0.1**, ten times larger; substantial violations of the prediction can leave counts unchanged. **Fix:** register a separate charge statistic and falsifier at 0.01, specifying whether it concerns every run or a population summary.
   - “To test whether the band survives normalizing the charge by stakes” specifies only one normalized price per game. One point cannot establish a band. **Fix:** call this a normalized-point control, or test normalized 0.03/0.1/0.3.
   - Prediction 3 includes inspection and PD, but its bracketed falsifier mentions only RPS. Prediction 4 predicts failure at both 1 and 10 but its falsifier mentions only 1. **Fix:** make falsifiers cover every stated component.

2. **Design flaws or confounds**
   - No operational definition of “inspection net of timeout charges” is provided. Charges can change both the feasible Pareto frontier and which outcomes count as efficient. **Fix:** freeze the net payoff vectors, comparison set, and efficiency criterion before runs.
   - “Up to 10,000 generations” leaves PD stopping unspecified. Stopping at first universal-open state can misclassify transient success; final-generation charges can miss recurrent costly episodes. **Fix:** fix stopping rules, retain censored runs, and require persistence over a prespecified terminal window.
   - The geometries change island size and island count simultaneously, holding total population fixed. They cannot identify large-population behavior or an island-size effect. **Fix:** restrict conclusions to these geometries; add a crossed geometry if scaling is claimed.
   - Fresh indices alone do not guarantee independent founders or uncontaminated caches. **Fix:** document seed derivation, hash imported caches/code, and verify caches are semantic accelerators rather than price-dependent payoff tables.

3. **Predictions likely wrong**
   - Inspection being “met” at (100,64) looks optimistic. If its success probability is near the reported 0.65 at the other geometry, 40 runs will usually leave the 95% interval straddling 0.60. **My prediction:** undetermined unless the smaller-island geometry substantially improves success.
   - Tiny terminal PD charges do not imply negligible evolutionary cost: failure pricing can eliminate useful founders during the scramble. **My prediction:** terminal charges may be tiny despite substantial early-charge effects on which network establishes.

4. **Missing controls or cheap additions**
   - Report paired price-minus-zero differences with intervals, using matched fresh founder sets where feasible.
   - Log timeout counts by program, stage, and nesting depth; explicitly test who pays for nested failed reads and whether caching changes charges.
   - Verify stored rows contain sufficient encounter/charge information for retrospective scoring; otherwise mark scores unavailable.
   - Report support and transition summaries, not only modal-program identities.

5. **Alternative explanations**
   - Success may reflect free successful verification plus punitive failure handling, not a general compute price.
   - The apparent joint band may be specific to fuel/depth caps, grammar, founder prior, or world-K semantics.
   - Low terminal costs may reflect selection having already removed costly readers, rather than intrinsically inexpensive cooperation.
