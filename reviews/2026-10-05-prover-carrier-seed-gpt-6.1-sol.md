# Review of `specs/2026-10-05-prover-carrier-seed.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes

- **“Establisher” does not establish invasion fitness or mutual compatibility.** Establishing a contract against a resident may differ from recognizing heterogeneous carriers’ contracts. If cooperation requires carrier–carrier encounters, its benefit vanishes with seed frequency; an established cooperative majority says little about invasion. **Fix:** before long runs, compute the seeded types’ pairwise action/payoff matrix, including interactions with the μ background, and their frequency-dependent reproductive advantage. Test a homogeneous FairBot-carrier seed alongside the mixture.

- **Mutation and transmission rules are underspecified.** Does source mutation erase a contract, inherit an invalid contract, or automatically validate/reissue one? Can mutation create carriers despite s = 0? These choices can determine extinction or sustained presence. **Fix:** specify the birth/mutation/swap transition rules; report carrier creation, loss, validation rejection, and transfer counts separately.

- **The conclusions exceed the measured object.** Success at one N and finite ε establishes neither large-population efficiency nor spread “to every program that can carry it.” Failure need not mean drift: deterministic negative invasion fitness or incompatibility could explain it. **Fix:** label this an invasion/establishment experiment; distinguish lineage expansion from contract acquisition across source classes. Add a modest N sweep and deterministic invasion diagnostics.

- **The island lottery is not sufficiently specified.** Define migration, selection, absorption/efficiency criteria, stopping time, and whether N is per island. With k fixed per island, increasing I also increases total seeded copies; it does not isolate an island-number mechanism. **Fix:** include a fixed-total-carrier comparison, record placement, and report censored runs rather than treating timeouts as failures.

### 2. Predictions likely wrong

- **Prediction 1 is too confident.** A conditional cooperator may be neutral or disadvantaged when rare in a mostly defecting background. Tens of carriers are not necessarily beyond an establishment barrier. My prediction: success depends strongly on compatibility and initial frequency; a threshold or long neutral waiting period is plausible, rather than reliable takeover from 1%.
- **Prediction 2 lacks a quantitative basis.** Rare valid swaps can matter over 10⁵ generations, especially after inheritance expands the compatible population. My prediction: negligible effects only if measured successful-transfer rates are negligible on the establishment timescale.
- **Prediction 4’s numerical probabilities are unsupported.** More islands increase seeded opportunities but may also increase opportunities for spoilers. My prediction: the direction of the I effect depends on migration and competing absorption hazards, not simply carrier presence.

### 3. Missing controls / cheap additions

- Add ε = 0 well-mixed runs to separate seed invasion from mutation-supported cooperation.
- Preserve the same source multiset and initial placement between carrier/non-carrier controls; toggle only the contract.
- Report lineage ancestry, source frequencies, and carrier-conditional P(C,C), not just aggregate carrier prevalence.
- Estimate early growth, extinction probability, and conditional establishment time. Five runs cannot sharply characterize a drift lottery; increase replicates for inexpensive boundary cells.
- Define “generation,” censoring, and success windows prospectively; reconcile prediction thresholds with their much weaker falsifiers.

### 4. Alternative explanations not ruled out

Carrier enrichment could select a particular prover clique rather than transmissible legibility. Cooperation could require a mutation-maintained defector fringe. Apparent stability could be metastability before shadow invasion. Cross-kernel semantic differences could explain discrepancies between ABM and lottery results.

### 5. Ideas beyond this experiment

nothing material
