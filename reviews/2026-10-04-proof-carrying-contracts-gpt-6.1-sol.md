# Review of `specs/2026-10-04-proof-carrying-contracts.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **Validity and execution are not yet jointly defined.** Source-reading \(p\) is evaluated against source in the validity test, but against contracts during play. These need not yield identical actions. “Every assignment of valid contracts” also makes validity recursively dependent on itself, potentially vacuous. **Fix:** specify one evaluator for \((p,c)\), including absent contracts, and an explicit semantics for the mutually dependent validity relation. Exhaustively test certified implications against actual pairwise play, including mixed certified/uncertified encounters.

- **The guarantee is ambiguously an implication or an exact policy.** “Whenever pre holds…” permits unconstrained behavior otherwise; “agrees with guaranteed play” sounds like equality everywhere. This distinction determines validity breadth and whether one contract can certify heterogeneous sources. **Fix:** formalize the guarantee, its unspecified cases, and exactly which deductions readers may make.

- **Contract-free populations cannot generate contracts at \(s=0\).** Swapping and inheritance preserve their absence. Thus the all-D/no-contract start cannot satisfy prediction 3, regardless of \(\sigma\); neither can the \(s=0\) lottery as specified. **Fix:** independently vary initial carrier frequency, including zero and a small positive seed. Define how source mutation handles an invalid inherited contract.

- **Breadth is not isolated from donor fitness or supply.** Payoff-weighted donors, search’s unspecified choice among valid contracts, source frequencies, and replacement rules all affect contract success. **Fix:** preregister the search distribution and replacement order; add uniform-donor swapping and matched initial contract frequencies.

- **The proposed objects do not establish a large-population conclusion.** One finite-\(\epsilon\) population and a small lottery grid cannot identify limiting efficiency. **Fix:** label results finite-size mechanisms; add an \(N\)-scaling path with specified initialization and island coupling. Report support and transitions, not merely second-half averages.

## 2. Predictions likely wrong

- **Prediction 2:** swapping selects donor abundance × donor fitness × compatibility with current newborns, not static \(\mu\)-breadth alone. My prediction: any breadth advantage is population-dependent; FairBot dominance is not guaranteed. Verify that P* is expressible at source \(n=6\), given the reported \(n\ge8\) result.
- **Predictions 3 and 5:** swapping cannot restore cooperation without an initial carrier. With carriers, restoration additionally requires compatible recipients and carrier persistence. I predict strong seed-frequency dependence.
- **Prediction 4:** unchanged ALLC-contract load does not follow from an unavoidable mutation leak. Transmission can alter label frequencies, and ALLC sources may carry other valid guarantees. I predict source-ALLC and contract-ALLC loads can diverge and depend on \(\sigma\).
- **Prediction 1:** certification need not recover the source oracle if contracts reveal less information or change responses. Predict recovery only for behaviorally matched, sufficiently expressive certification.

## 3. Missing controls / cheap additions

- Compare certified play with an unbounded reader **using the same contract evaluator**, alongside the source-oracle baseline.
- Report the full source–contract compatibility matrix, joint frequencies, accepted/rejected swaps, and acceptance rates by contract.
- Include neutral label transmission to distinguish behavioral effects from copying dynamics.
- Increase lottery replication: 20 trials give roughly ±0.20 uncertainty near probability 0.5, inadequate for a 0.15 equivalence claim. Align falsifiers with the stated margins.
- Record censoring explicitly; runtime-based cell exclusion may preferentially remove complex networks.

## 4. Alternative explanations not ruled out

Cooperation could reflect free oracle evaluation, altered information semantics, or favorable initialization rather than proof portability. Contract dominance could reflect payoff-biased copying or search supply rather than breadth. Apparent endpoints could be metastable.

## 5. Beyond this experiment

Nothing material.
