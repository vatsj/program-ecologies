# Review of `specs/2026-10-24-exploration-audit.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **The triage excludes other exploration failures.** Payoff-twin networks are one demonstrated mechanism, not a necessary condition: rare gateways and deep polymorphic traps can also defeat capped exploration. **Fix:** audit every restricted chain; use twins to prioritize, not determine eligibility. Mark unaudited cells unresolved.

- **“Complete monomorphic solve” is not a complete chain solve.** Stored polymorphisms plus a multi-start search capped at support six cannot certify completeness—the earlier audit already establishes this concern. **Fix:** label these “monomorphic-complete, polymorphism-search-limited”; record search coverage, test every retained state against all admissible invaders, and distinguish certified completeness from empirical stability. Clarify that “closure complete” earns exclusion only if closure is over all permitted transitions.

- **The proposed comparison changes more than exploration.** Switching solver, adding polymorphisms, and twin-expanding can each change the stationary distribution. Reproducing the published baseline does not isolate these effects. **Fix:** stage comparisons: baseline → enlarged exploration with unchanged construction → polymorphic additions → twin expansion. Validate solver equivalence on identical state sets and rates.

- **Jump-chain stationary weights require holding-time correction.** GTH on the embedded jump chain does not directly yield evolutionary-time occupancy. **Fix:** explicitly recover occupancy using exit rates; handle absorbing/reducible classes and initial-condition dependence separately. Cross-check against the original transition matrix on small instances.

- **The large-space rerun is underspecified and cannot establish convergence.** Raising caps leaves top-k restrictions untouched; two nested truncations can agree while both miss the same drain. **Fix:** specify enlargement of every active restriction, including invader sets and rounds. Call agreement “stable under this enlargement,” not converged; retain an unresolved status absent stronger coverage evidence.

## 2. Predictions likely wrong

- **Prediction 2’s justification is weak.** Small class tables and closure seeding do not guarantee discovery of neutral-network exits or polymorphic traps. I predict corrections will track missing transition structure more reliably than one-population versus two-role classification. Also define the denominator and metric: “most” and “more than a third” are not complementary falsifiers, and 0.02 is not comparable across payoffs, probabilities, and slopes.

- **Prediction 4 overstates what a change would mean.** Direct lottery outputs should remain unchanged, but a headline combining lottery and chain evidence may legitimately change. That would not necessarily be an audit error. Predict unchanged lottery measurements, while permitting revised interpretations.

## 3. Missing controls or cheap additions

- Include the known mixed2 failure as a positive control and a small complete-chain case as a negative control.
- Record mutation-prior mass, twin multiplicities, state counts, SCCs/recurrent classes, and newly opened escape paths—not just added states and scalar weights.
- On tractable cases, compare several caps and exploration seeds against the complete reference.
- Freeze code revision, evaluator, prior, population size, seeds, and numeric tolerances.
- Replace the 50,000-state feasibility rule with measured transition count and memory estimates; a dense matrix alone is approximately 20 GB.

## 4. Alternative explanations not ruled out

A discrepancy could reflect changed twin weighting, invader renormalization, numerical underflow, or different polymorphism discovery rather than exploration alone. Conversely, unchanged aggregate payoffs can conceal substantially different support and transitions. The staged controls above distinguish these possibilities.

## 5. Beyond this experiment

nothing material
