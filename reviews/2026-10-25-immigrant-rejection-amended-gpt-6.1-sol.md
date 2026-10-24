# Review of `specs/2026-10-25-immigrant-rejection.md` by gpt-6.1-sol

## 1. Errors, contradictions, unsound mechanisms

- **The Step 0 gate reverses prediction 1.** It says: “if it falsifies prediction 1 (**gV acts mainly through contract refusal**)”; prediction 1 instead says “through the refusal bit carried by residents, **not by blocking member-to-member contracts**.” Its bracketed falsifier agrees with the latter. **Fix:** make the gate explicitly test immigrant selection versus contract refusal versus tie blocking, with preregistered attribution criteria. Resolve this before coding.

- **A switching penalty does not automatically establish the claimed value ordering.** “The KR recursion is solved with a switching cost ε … so the current pair has a strictly higher value” requires a state-dependent recursion tracking the incumbent coalition and all subsequent switching costs. Symmetry of the original values alone is insufficient. **Fix:** specify that recursion, whose utility pays the cost, discount normalization, and tie fallback. Test ε = 0 against the original transition kernel, not merely noisy lifetime estimates.

## 2. Design flaws and confounds

- **Heritable programs have unspecified mutable-state semantics.** Loyalty and conformity depend on personal histories, but initialization, reproduction, migration, exclusion, and encounter ordering are undefined. Inheriting a parent’s partner memory can act as an island-level coordination mechanism rather than personal loyalty. **Fix:** define the state machine and distinguish inherited versus reset memory; specify whether “partner” means role, source, or individual.

- **“For their own reasons” is not tested by adding a switching preference.** A utility penalty manufactures an incentive absent from the original game. **Fix:** label this a preference-modification arm; compare with a direct status-quo tie rule and, separately, a switching cost actually charged in evolutionary payoffs.

- **The spread amendment does not identify selection.** “Trait frequency is conditioned on the island’s member stability” conditions on an outcome the trait may cause, introducing selection bias. **Fix:** use paired, randomized trait introductions into identical resident states, measuring relative reproductive success and establishment against inert controls.

- **The panel cannot establish large-population persistence.** Two population sizes and a fixed 20,000-generation horizon distinguish neither reduced transition rates nor permanent protection. **Fix:** report censored survival curves and member-transition hazards; describe conclusions as finite-time unless an invariant or scaling argument supports more.

## 3. Predictions likely wrong

- **Conformity matching gV at every migration rate is unlikely.** Sampling one encounter supplies copying, not rejection: it can amplify an immigrant-associated outcome and produce voter-like coarsening. I predict improved local coordination but eventual coverage loss in a connected component.

- **Coverage preservation does not imply trait spread.** A stabilizer can benefit noncarriers equally and remain neutral, or incur encounter costs. I predict some effective stabilizers will fail to increase when rare.

- **The k = 5 rationale is incomplete.** One encounter cannot reverse a settled five-encounter majority, but repeated encounters and exclusion can; longer memory also delays establishment. I predict a persistence–adaptation tradeoff, not uniformly better performance.

## 4. Missing controls or cheap additions

- Add **both diagnostic freezes together**: offer drift and pivot switching may interact, so separate freezes cannot allocate “how much” each contributes.
- Use paired seeds, confidence intervals, and explicit censoring rules; 20–40 runs cannot reliably certify “within 0.1.”
- Test rare inert invaders into stabilized islands and reciprocal rare stabilizer invasion.

## 5. Alternative explanations not ruled out

Coverage may reflect seeded diversity frozen by hysteresis, slower mixing, inherited correlation, or altered preferences—not selected immigrant rejection. Track establishment from uncoordinated seeds separately from maintenance of pre-established coverage.
