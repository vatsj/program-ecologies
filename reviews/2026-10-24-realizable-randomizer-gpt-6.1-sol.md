# Review of `specs/2026-10-24-realizable-randomizer.md` by gpt-6.1-sol

### 1. Design flaws/confounds → fixes

- **The probability semantics are not defined for adaptive execution.** \(M\) can depend on earlier digits, branching, nested simulations and proof checks; repeated reads of one digit are not independent draws. Specify a finite random decision tree with randomness indexed by invocation and tape position. Compute probabilities by weighted leaves or a fixed padded assignment space—not a trace-dependent denominator. Separate tape length \(m\) from total randomness consumed across invocations.

- **Count certificates need stronger binding and replay semantics.** Bind each certificate to both sources, checker version, fuel budget and evaluation context. Explicitly replay supplied tape assignments rather than drawing fresh randomness during checking. Require coverage, uniqueness and correct weights. Prevent checking from certifying a larger-budget or differently charged execution than actual play. Named-pair agreement is a regression test, not a soundness argument; add adaptive/nested adversarial cases.

- **“No-prover (simulators only)” and the prior are ambiguous.** Does this retain constants and mixers? Removing templates and renormalizing changes founders’ abundances, potentially explaining the lottery result. Freeze the complete grammar, lengths, certificate encoding/production costs and inherited evaluator conventions. Add a matched-prior capability-disabled comparison.

- **The evolutionary object needs specification.** State whether selection uses exact expected payoffs or sampled encounters. Exact tables remove reproductive payoff variance; these need not produce the same finite-population lottery. Fix horizon summaries, efficiency thresholds and censoring rules before running. \(N=100\) alone cannot establish large-population persistence; label this a transfer test and retain one larger-\(N\) check.

### 2. Predictions likely wrong

- **Prediction 1 is too broad.** A quote-hash program is deterministic, but one bounded simulation need not predict it successfully under recursion and real charging. Conversely, a fresh sample cannot predict a uniform tape mixer’s realized action, but can predict a biased mixer better than chance. Predict exact exploitation only for explicitly terminating hash fixtures under matched execution semantics.

- **Prediction 2’s pseudo-random exploitability bound is unsupported.** Deterministic individuals can form an aggregate RPS equilibrium, and grammar-limited exploiters may be too costly. Individual predictability does not imply population exploitability ≥0.3. I predict predictable individuals but potentially low aggregate exploitability; report both.

- **Predictions 5–6 do not follow from enumeration complexity.** A one-bit inspector can certify \(p=1/2\) using two assignments; \(m=3\) does not force eight assignments. Responsive proof search may be substantially dearer. Predict route costs from the hand table before imposing a ratio or survival ordering.

- **Prediction 3’s explanation misattributes effects at \(c=0\).** Steps then matter through fuel exhaustion, not direct fitness charges. Predict a budget-dependent gap, not necessarily reduced efficiency whenever search takes longer.

### 3. Missing controls/cheap additions

- Hand-check inspectee compliance: its payoff difference is \(4p-1\), so compliance requires \(p>1/4\), with indifference at equality. Include below/equal/above-threshold certificates.
- Add malformed certificates, duplicate/omitted assignments, repeated tape reads and branch-dependent simulation tests.
- Report raw game payoff separately from compute-adjusted payoff; fix \(c\) while varying fuel once. Otherwise recalibrating \(cK=0.12\) confounds more computation with cheaper computation.
- Cluster uncertainty by run, not by island; extend unresolved runs rather than calling horizon occupancy absorption.

### 4. Alternative explanations not ruled out

Template abundance, certificate bulk, source-length changes affecting hashes, fuel-induced forfeits, and transient founding advantages could explain arm differences without any advantage from private randomness or sound probability reasoning.

### 5. Beyond this experiment

Nothing material.
