# Review of `specs/2026-10-26-forfeit-pricing.md` by gpt-6.1-sol

### 1. Errors / unsound mechanisms

- **“Exact” remains unjustified.** “Opponents have the option to simulate an opponent EXACTLY” conflicts with “the fixed steps of its own response are reserved before the rest of the fuel is passed to `run`.” The simulated opponent receives less fuel than its actual root invocation; budget-sensitive readers can therefore behave differently. Private tapes also prevent predicting the actual randomized action. **Fix:** call this *uncapped, shared-fuel simulation*, specifying precisely which execution it reproduces. Test a deterministic opponent that finishes at its actual root budget but fails at the simulator’s reduced budget.

- **Response reservation is incomplete.** The amendment guarantees response fuel for RPS `SIMX`, but not `SIMX_I` or `SIMX_E`. A successful simulation could leave either inspection simulator unable to answer. **Fix:** reserve all response/return overhead in every simulator; test exact boundary budgets.

- **Failure accounting needs an execution boundary.** “P_fail per timed-out read call and P_fail per forfeit” plus “One failure, one charge” does not specify whether failures inside simulated executions count, or whether a root may incur earlier capped-read charges and then a forfeit charge. **Fix:** define a trace-based accounting rule, including nested simulation, attribution, and multiple distinct failures. Add tests beyond the single uncapped exhaustion case.

### 2. Design flaws / confounds

- **X changes both capability and initialization.** “Each splits its capped counterpart’s template mass equally with it” preserves constants’ mass, but halves capped-simulator abundance. Any X effect could reflect reduced capped seeding rather than useful exact simulation. **Fix:** add a sham-split control using behaviorally identical capped templates, preserving the same template bookkeeping.

- **Historical comparisons cannot establish equivalence.** “A_f equals A within noise” and the PD’s “within 3 runs” use fresh, independent runs without a justified equivalence margin or power calculation. At intermediate success probabilities, differences exceeding three successes among 40 can readily arise without a treatment effect. **Fix:** use concurrent paired-seed A controls at the principal levels; report run-clustered confidence intervals and preregister meaningful equivalence margins.

- **One size and one horizon do not identify a large-population or limiting outcome.** **Fix:** label this a finite-size mechanism test. Require support and transition diagnostics; extend selected unresolved/high-forfeit cells in time before interpreting persistence as selection’s endpoint.

### 3. Predictions likely wrong

- **Prediction 5:** reading a compliant constant supplies no advantage over the already successful, uncharged capped reader. I favor the registered counter-prediction: `SIMX_I` has no positive selective advantage there and is disadvantaged against expensive opponents. Its modal frequency remains prior- and drift-dependent, not necessarily below 0.1.

- **Prediction 6:** “within 3 runs” is too sharp even if the PD is causally unaffected. I predict negligible expected change, but potentially a formal falsification from sampling noise alone.

### 4. Missing controls / cheap additions

- Report **paired payoff differences** between capped and uncapped simulators against each opponent class, including charge totals and actual-versus-simulated actions.
- Test recursive reader pairs across several nearby fuel budgets; recursion thresholds can manufacture apparent advantages.
- Report exact-simulator population mass alongside modal-island frequency, and uncertainty clustered by run.

### 5. Alternative explanations not ruled out

Reduced forfeiting could arise from removal of reader lineages, not improved reasoning. Better RPS scores could be carried entirely by free randomizers. Inspection changes could reflect seeding or recursion-budget thresholds rather than informational gains from uncapped simulation.
