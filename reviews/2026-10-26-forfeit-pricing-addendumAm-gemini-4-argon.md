# Review of `specs/2026-10-26-forfeit-pricing.md` by gemini-4-argon

### 1. Errors, contradictions or unsound mechanisms

- **Mutual forfeit payoff in RPS is underspecified and likely contradicts zero-sum structure:** The brief states *"the game's own forfeit payoff (RPS: −1 against any action) is part of the game and stays"* and *"in RPS a forfeiter... loses the play (−1 against any action, its pure security level), and its opponent gains +1."* It does not state the base game payoff when **both** players forfeit (e.g., `SIMX` vs `SIMX`, or mutual prover non-play—the very 0.50–0.63 forfeit regime that motivated this experiment). If a forfeiter gets −1 against *any* outcome including another forfeit, mutual forfeit yields (−1, −1) before `P_fail`; if it is a tie, it yields (0, 0) before `P_fail`.
  - **Fix:** Explicitly state the base payoff for mutual forfeit in RPS, inspection, and PD before `P_fail` is deducted (presumably (0, 0) in RPS, and the existing mutual-forfeit table in inspection/PD), and require `notes/forfeit-pricing.md` §1 to include the mutual-forfeit cells in the hand table.

- **Undefined division-by-zero edge case in `A_m` statistics:** The Addendum states *"individual mixing, by-mixing and the coin share are computed on non-fallback plays."* If an island or run has 100% fallback plays (or 0 non-fallback plays for a given program), these statistics are undefined (0/0), which could break the equivalence and classification checks in Prediction 10.
  - **Fix:** Specify the convention when non-fallback plays equal zero (e.g., non-fallback mixing = 0, exploitability = 1).

- **Missing baseline for Prediction 2 at `P_fail = 0.03`:** Prediction 2 claims *"At 0.03 and 0.1, A_f equals the concurrent A within an equivalence margin of 0.05... (paired, run-clustered intervals)"*, but the **Cells** section only schedules *"Concurrent A cells (no X) on the same fresh founders at 0.1, 0.3 and 1"*. There is no concurrent `A` cell at 0.03 to pair with.
  - **Fix:** Either add a concurrent `A` cell at 0.03 or restrict the paired equivalence test in Prediction 2 to 0.1 (using the confirmation run for 0.03).

### 2. Design flaws or confounds

- **Asymmetric `A_m` cell matrix vs Prediction 10:** The Addendum schedules `A_m` in RPS *"with and without X"*, so Prediction 10 (*"A_m's classification equals A_f's at every level"*) is ambiguous between the no-`X` and with-`X` arms, and `A_m` in inspection is only run at 0.1 and 1 without specifying whether `X` is included.
  - **Fix:** State whether `A_m` in inspection is with or without `X` (or both), and state in Prediction 10 that the comparison is matched by arm (`A_m` vs `A_f` without `X`, and `A_m + X` vs `A_f + X`).

### 3. Predictions I think are wrong

- **Prediction 5 (and I side with the registered counter-prediction):** `SIMX_I` will not reach 0.10 modal share of inspector slots for functional reasons. Because `SIM_I` already reads constants within its cap for free, `SIMX_I` has zero payoff advantage over `SIM_I` against constants, while suffering strictly worse payoffs (via root exhaustion and forfeit) against deep or recursive inspectees. With half the prior mass of original `SIM_I`, `SIMX_I` will at best neutral-drift against `SIM_I` on constant-inspectee islands and lose elsewhere, landing below 0.10.
- **Prediction 11:** Expecting `SIMX` population mass under `A_m` to be *at least twice* its `A_f` mass at 0.1 is dubious if both are near the selection/mutation floor. Under `A_m`, `SIMX` still loses strictly to constants/coins against mixers (paying `P_fail` or getting 50% wrong on fresh tape draws) and pays `P_fail` on mutual recursion. When two quantities are driven near zero by selection (< 0.01 mass), their ratio is dominated by founder noise rather than the −1 vs 0 fallback difference.

### 4. Missing controls or cheap additions

- Report `X-sham` population mass and modal share directly alongside `SIMX` / `SIMX_I` / `SIMX_E` in the main summary table at 0.1 and 1, so Prediction 5 and 11 can be immediately benchmarked against neutral template-splitting drift.

### 5. Alternative explanations

- Nothing material.
