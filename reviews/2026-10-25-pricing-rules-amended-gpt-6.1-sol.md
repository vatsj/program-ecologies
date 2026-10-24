# Review of `specs/2026-10-25-pricing-rules.md` by gpt-6.1-sol

## 1. Errors, contradictions, unsound mechanisms

- **F+A’s timeout charge is ambiguous.** “Every step costs c, and a timed-out read is charged as if it had run to the cap, c·K.” Does this replace the read’s step charge or supplement it? Supplementing charges twice for a read already consuming K. **Fix:** specify an explicit ledger formula, including nested calls, their local caps, and whether child steps count toward ancestor charges. Test partial-cap and nested timeouts.
- **B is not yet an executable accounting rule.** “Every step costs c, but a reader pays a given read once per island lifetime” conflicts with “stores the cost only … against a fresh tape”: stochastic executions have different costs and timeout statuses. **Fix:** define first-execution charging versus some fixed expected charge; exempt precisely the cached subtree, without double-counting it as root steps. Specify cache ownership, migration, certificate changes, and island resets.
- **Prediction 2’s falsifier is incomplete.** “At least two adjacent P_fail levels” is not falsified only by “[none]”; one successful level, or two nonadjacent levels, also falsifies it. **Fix:** use “no adjacent pair meets all three targets.”

## 2. Design flaws or confounds

- **Cross-game price robustness depends on arbitrary units.** A common numeric price depends on payoff scales; F and F+A additionally depend on evaluator steps and game-specific K. A’s equal penalty does not imply equal timeout severity. **Fix:** report raw prices alongside prices normalized by game stakes, and tabulate fuel caps and timeout frequencies. Describe the result as robustness under these conventions, not an intrinsic ranking of cost notions.
- **Static records may be insufficient.** Pair/route totals do not establish the nested-call counts needed for A or unambiguous F+A accounting. PD production changes certificates and subsequent encounters. **Fix:** audit record sufficiency before launch; obtain fresh event traces where needed. Explicitly price production, retries, and checking—or state their exemptions.
- **Joint-band verdicts are too noisy and potentially incomplete.** Twenty PD runs poorly resolve a 0.7 threshold; budget cuts can remove cells necessary to establish a joint band. **Fix:** preregister confidence intervals and an “undetermined” category; preserve one complete cross-game panel before optional cells. Static invasion flips do not establish lottery success between sampled prices.
- This is a fixed-geometry seed-lottery comparison, not evidence of large-population convergence. **Fix:** bound claims accordingly; add one larger geometry for any apparent winning level.

## 3. Predictions likely wrong

- **A’s RPS mechanism is overstated.** Mutual simulation timing out does not show every relevant simulator loses to U: readers may finish against U, exploit constants, or use bounded reads without timeout. Nor does U ≥ 0.5 establish exploitability ≤ 0.1. **Prediction:** timeout-heavy simulators decline, but residual successful readers can prevent the RPS target; derive pairwise margins before predicting a joint band.
- **B’s pointwise U ordering is unjustified.** Subsidizing reads changes a frequency-dependent ecology, including predators of simulators. **Prediction:** B lowers repeated-read costs, but U’s population share need not be monotone relative to F.

## 4. Missing controls or cheap additions

- Add timeout-free bounded simulators and a matched constant per-read toll.
- For B, log cache hits, first-charge payer, and cumulative charges; compare cold versus prewarmed caches.
- Report support, transition structure, non-play, gross payoffs, net payoffs, and PD P(C,C), not only winner labels.

## 5. Alternative explanations

Apparent success could reflect free successful computation, cache-incumbency subsidies, founder composition, arbitrary payoff/fuel calibration, or finite-time delayed collapse—not selection favoring efficient reasoning.
