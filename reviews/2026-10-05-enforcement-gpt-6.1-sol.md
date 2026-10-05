# Review of `specs/2026-10-05-enforcement.md` by gpt-6.1-sol

### 1. Design flaws or confounds, and fixes

- **The ablations leave source semantics and timing unspecified.** Do boxes refer to program recommendations or implemented actions after best-response overrides? If recommendations, workers can “prove” a strike that never occurs; if implemented actions, Part A’s soundness argument must be re-established for the modified evaluator. Define the extensive form, information sets, tie-breaking, and box referents explicitly. RR is not fully uncommitted: wages apparently remain committed.
- **Worker best responses omit repression.** At zero wage, striking is not indifferent if it triggers loss \(L\); source-targeted repression may also affect working. Compute best responses from the complete payoff table, conditional on the specified timing—not simply “0 against \(s\).”
- **RC-with-pool changes the economy, not just commitment.** Outside replacement labor adds productive capacity and weakens withdrawal independently of enforcement credibility. Cross pool availability with CC/RC, keeping replacement timing and costs identical. Otherwise a lower wage cannot be attributed to incentive compatibility.
- **Grammar expansion changes the mutation prior.** Adding an atom or named strategies can change existing masses and multiplicities. Separate a fixed-mass strategy substitution from an expanded-language run; report old and new masses. Include BOX1 twins consistently in static and chain comparisons.
- **Neither fair-wage share nor two finite \(N\) values establishes large-population Pareto efficiency.** Report realized total surplus and payoff-vector dominance, including repression costs and replacement workers. Use transition-rate scaling or an analytic reduced-chain limit before making asymptotic claims.

### 2. Predictions likely wrong

- **Prediction 1 conflates soundness with pact activation.** Soundness excludes false fairness certification; it does not establish that two union⁻ workers can prove each other’s strikes. The negated fairness condition may itself be unavailable inside the proof system. My prediction: militant⁻ rejects uncertified fairness, but universal union⁻ quorum activation fails unless an additional derivability argument succeeds. Test this first.
- **Prediction 3’s “free of the commitment cost” rationale is wrong.** Rational repression still pays \(c\) whenever executed. Its advantage is avoiding unprofitable executions, not eliminating costs. With replacements, I expect wage suppression mainly from restored production; the sign relative to matched CC-with-pool is unclear.
- **Prediction 2’s ≥0.4 uniform-prior claim lacks a mechanism sufficient for that magnitude.** Removing one exit need not improve stationary weight when neutral scab exits or new entry barriers bind. I predict no robust ≥0.1 gain without evidence from entry/exit rates.

### 3. Missing controls or cheap additions

- First tabulate union⁻/union⁻, union⁻/militant⁻, and mixed BOX/BOX1 pairs against constant-low and constant-fair bosses; record both actions and relevant box truth values.
- Freeze prior masses while replacing union with union⁻; separately test adding militant⁻ alone.
- Include exact-boundary cases \(1-s=c\), especially \(s=1/2,c=1/2\), with declared tie-breaking.
- Report each threat’s payoff advantage over its feasible deviation, not only the frequency of “noncredible” executions.
- Separate suppression through reduced strike incidence from increased repression conditional on a strike.

### 4. Alternative explanations not ruled out

Fairness changes could reflect prior renormalization, syntax multiplicity, proof-system strength, or finite-\(N\) neutral drift rather than unfakeability. Apparent credible-enforcement effects could instead reflect replacement technology or elimination of costly repression. Zero observed counterexamples at \(n=6\) tests implementation consistency, not unfakeability throughout the language.

### 5. Beyond this experiment

nothing material
