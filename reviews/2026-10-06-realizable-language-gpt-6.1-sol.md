# Review of `specs/2026-10-06-realizable-language.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes

- **The soundness argument does not yet establish the central claim.** Replacing modal unfolding with arbitrary computation does not automatically preserve JLöb’s witness construction. In particular, deriving a cooperative return is insufficient if the actual proof search times out under global \(K\). **Fix:** state the complete evaluation, box and JLöb rules, then construct an executable witness with explicit proof-size and runtime bounds. Gate the experiment on this theorem; replay checks validate implementation, not rule soundness.

- **Proof-search cost is underspecified.** Does `prove_b` consume one evaluator step, or steps proportional to its actual search? The former remains a computational subsidy; the latter can change cooperation into timeout-defection. “Choose \(K\) large enough” needs a demonstrated bound across the entire grid. **Fix:** specify charging semantics, report search work and timeout counts, and run multiple \(K\) values. Distinguish primitive-assisted realizability from an internalized prover.

- **Finite proof size does not guarantee finite search with the proposed syntax.** Formula labels contain arbitrary sources, budgets and JLöb sets; bounding rule-node count alone leaves infinitely many candidates. Negative `prove_b` results also require exhaustive search, not merely failed heuristic search. **Fix:** specify finite candidate generation with a completeness proof, or charge total encoded proof length. Report minimality only when exhaustive lower-budget searches are certified.

- **Several agents are not executable specifications.** PrudentBot’s “appropriate level,” P*’s unindexed consistency guard, and the sloppy checker’s candidate derivations are unresolved. `plays(...,D)` also conflates explicit D with timeout unless defined carefully. **Fix:** freeze exact terms, guard budgets, candidate generators and timeout semantics before predictions.

### 2. Predictions likely wrong

- **Prediction 3’s mutual defection against the Gödel faker is wrong under the stated semantics.** If FairBot defects, a sound prover cannot prove that it cooperates, so the terminating faker returns C. Indeed mutual defection is impossible for this pair under soundness and completed searches. **Prediction:** likely `(FairBot D, faker C)`; soundness alone does not establish FairBot’s defection.

- **The numeric thresholds and constant-overhead proof claim are unsupported.** Source encoding, quotation, evaluation and witness construction can dominate modal proof-node costs. Critch’s asymptotic result does not supply \(b^*\le32\) for this calculus. **Prediction:** thresholds are representation-dependent and may exceed 64.

- **The distinct-budget minimum-threshold law is not automatic.** Proof costs can depend on both encoded budgets and source lengths. **Prediction:** no exploitation follows from soundness and successful execution, but compatibility need not depend solely on the minimum budget.

- **Prediction 5’s “iff” is too strong.** An always-accepting sloppy checker can cooperate before sound FairBot has sufficient budget to certify it. **Prediction:** sound FairBot can defect against a cooperating sloppy checker.

### 3. Missing controls / cheap additions

- Run an otherwise identical **JLöb-disabled** calculus.
- Test harmless wrappers, renamed representations and syntactically distinct equivalent FairBots: separate copy recognition from general cooperation.
- Include tiny hand-enumerated exhaustive proof spaces and an independently implemented evaluator/checker.
- Separate “proof found,” “proof search completed without proof,” and “execution timed out.”
- Keep milestone 2 gated on these audits; pairwise cooperation alone says nothing about population selection or large-\(N\) efficiency.

### 4. Alternative explanations not ruled out

Apparent success could reflect a cooperation shortcut embedded in JLöb, free host-language search, source-specific recognition, or shared bugs between prover and replay checker—not executable bounded Löbian reasoning.

### 5. Beyond this experiment

nothing material
