# Review of `specs/2026-11-16-script-checked-offers.md` by gpt-6.1-sol

## 1. Errors, contradictions, unsound mechanisms

- **The amended requirement semantics still need an executable definition.** “Eligibility is mutual by construction” does not follow merely from parameterizing `S_off`: recognition must inspect the partner’s *own* requirement, not require an identical `S_off(d; R)` statement. “Pc⁺ … whose requirement is S_off and S_nx” also conflicts with “R is ∅ … or {S_nx}.” **Fix:** define one Boolean eligibility predicate explicitly, including reciprocal offer directions and both requirement sets; use it verbatim in statements, code and proofs. Rewrite Pc⁺’s requirement consistently as `{S_nx}`.

- **An invalid rejection gate.** “A program that passes S_off toward d but names someone else when d is eligible” need not violate `S_off`, which promises naming only “if d is my preferred member of E.” **Fix:** require that d is eligible **and preferred**, or the purported forger may correctly be accepted.

- **Exact full-check costs do not establish fuel equivalence.** S1 is “charged the exact S0 step count,” while soundness includes “fuel exhaustion.” An atomic cached check must also reproduce interruption when the remaining fuel is insufficient; charging its completed cost afterward is insufficient. Moreover, fuel is sized using “worst accepted cost,” excluding potentially expensive rejections. **Fix:** specify interrupted-check semantics and bound all encountered checks, including rejections; test residual budgets immediately below and above each check’s cost.

## 2. Design flaws or confounds

- **RE 1 is registered after its outcome is known.** Gates precede prediction commitment, but RE 1 predicts existence, soundness and spelling completeness—the gates themselves. **Fix:** commit engineering predictions before construction/gates; distinguish subsequent dynamics predictions conditional on passing.

- **Mass lower bounds cannot establish the proposed scarcity conclusion.** Step 1 promises “exact-member lower bounds only,” whereas RE 10 asserts that the “simplest script carriers” are extremely rare and competitive “only if” scripts are uncharged. A few witnesses establish neither minimality nor family-mass upper bounds. **Fix:** score witness ratios only; reserve minimality/scarcity claims for a bounded exhaustive search or proven size lower bound.

- **Fallback matching does not ensure historical matching.** The new two-fallback pool differs from queue 79’s sixteen. V2 must reproduce the historical catalogue/law separately; A1–K comparisons must use the same restricted pool. Specify both configurations explicitly.

## 3. Predictions likely wrong

- **RE 8’s global Bc exclusion is unsupported.** Pc⁺ refuses Bc, but Oc⁺ and Rc⁺ retain empty requirements, and Bc pairs with itself. Thus prudence excludes Bc from *Pc⁺ partnerships*, not fair islands generally. **Prediction:** Bc remains substantial, potentially dominant, among fair-pair holders, especially at low δ; its fall below 0.1 is unlikely without broader adoption of the requirement.

## 4. Missing controls or cheap additions

- Report Bc occupancy separately for **paired versus excluded slots**, and conditional on the other holder’s family. Otherwise “excludes the bully” conflates refusal with displacement.
- Add the omitted `(Pc⁺, Oc)` and `(Pc⁺, Rc)` tests: these should fail eligibility without `S_nx`, unlike their certified-plus counterparts.
- Include a three-carrier competing-offer gate, not just pointing pairs beside non-carriers.
- Preserve N-scaling as exploratory if budget cuts remove it; finite thresholds at N ≤ 400 do not establish a large-population result.

## 5. Alternative explanations not ruled out

- Any prudence penalty could reflect lost compatibility/network connectivity rather than a fitness disadvantage of no-exploit reasoning itself.
- Cross-spelling success demonstrates robustness across the selected transformations, not independence from a restricted proof convention or an abundant founder subsidy.
