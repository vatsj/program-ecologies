# Review of `specs/2026-10-05-proof-length.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **GL does not decide both actions by theoremhood.** “Cooperate iff GL proves \(p^*\)” does not imply “defect iff GL proves \(\neg p^*\).” For example, neither \(\Box\bot\) nor its negation is a GL theorem. **Fix:** distinguish C-proofs, D-proofs, and non-theorems; report \(L_D=\infty\) when appropriate. Specify precisely which evaluator outcome corresponds to theoremhood before requiring zero disagreements.

- **Fixed-point proof length is not the cost of establishing cooperation.** FairBot’s fixed point can be represented by \(\top\), whose proof is trivial; the Löb work resides in proving the fixed-point equivalence. Equivalent fixed-point representatives can have very different lengths. **Fix:** freeze the construction and charge for the fixed-point certificate, its verification, and the outcome derivation. Report formula-symbol size as well as proof nodes. Otherwise “FairBot requires one Löb step” measures an arbitrary representation.

- **BOX1 is not justified by the proposed GL encoding.** An ordinary propositional atom has unrestricted valuations; GL cannot enforce “true only at world 0.” Restricting valuations changes the semantics and requires a corresponding calculus. **Fix:** first audit the one-box fragment; separately specify and validate the two-level logic. Do not classify every surviving disagreement as an implementation bug.

- **The bounded arm lacks a defined proof target.** Unbounded GL lengths used to gate bounded play are an external lookup intervention. Recomputing lengths from gated play instead requires a formal semantics and proofs referring to the budgeted programs; these are not automatically GL fixed points. **Fix:** separate these experiments. For the realizability claim, define bounded proof search operationally, including what the prover proves, termination, and any fixed-point selection.

- **A found proof is not necessarily a shortest proof.** Depth truncation can miss a shorter, deeper proof; terminating theorem search does not certify minimality. **Fix:** use exhaustive proof-size search for certified minima. Else report upper bounds from found proofs and certified lower bounds separately. Do not regress censored observations as exact lengths.

## 2. Predictions likely wrong

- **Prediction 3:** Exact slopes and \(\Lambda=\text{depth}+1\) are representation-dependent, not GL invariants. Prediction: simplification will collapse some nested programs’ costs, while duplicated formulas inflate others; no universal slope or Löb-count identity.
- **Prediction 4:** A FairBot threshold cannot exclude cheaper conditional programs, and covering P’s lengths does not restore interactions with all outsiders. Prediction: multiple thresholds; agreement with the free arm requires covering every relevant queried theorem.
- **Prediction 5:** Unequal budgets destroy the unbounded symmetry argument; symmetric underlying programs do not establish symmetric bounded outcomes. Asymmetry remains plausible. Pricing also penalizes cooperation relative to zero-budget defectors, so concentration at the smallest cooperative budget is not assured.

## 3. Missing controls / cheap additions

- Hand-check ALLC, ALLD, FairBot, \(\Box\bot\), nested boxes, and asymmetric budgets.
- Compare raw versus simplified fixed points; tree versus shared-DAG symbol costs; proof length versus search effort.
- Match masking by opponent/type and cooperation status, not only aggregate fraction.
- Report uncertainty for 20-run lotteries and label finite-\(N\) trends separately from large-population claims.

## 4. Alternative explanations not ruled out

Observed thresholds or closure could reflect compiler normalization, proof-search heuristics, circular-solver selection, or truncation of cheap escape programs. Budget pricing could select low advertised capacity rather than low actual computational cost.

## 5. Beyond this experiment

Nothing material.
