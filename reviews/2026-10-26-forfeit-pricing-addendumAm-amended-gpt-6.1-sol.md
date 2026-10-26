# Review of `specs/2026-10-26-forfeit-pricing.md` by gpt-6.1-sol

## 1. Errors, contradictions, unsound mechanisms

- **Pure security actions do not imply equivalent forfeit outcomes.** “A_m differs from A_f’s game outcome only where the security strategy is mixed” conflicts with A_f’s “in addition to the game’s own forfeit payoff.” Replacing forfeiture with inspect, comply or defect generally changes both players’ payoffs unless the existing forfeit table implements precisely those actions. **Fix:** publish unilateral and mutual-forfeit payoff tables for each game; establish equivalence entry by entry or treat inspection/PD as substantively different treatments.

- **Prediction 2 lacks its promised controls.** “A_f equals the concurrent A … in each score (paired…)” includes “inspection and the PD,” but PD receives only A_f cells. **Fix:** add paired contemporary PD A controls, or restrict the equivalence prediction to RPS/inspection. Prediction 6’s historical comparison cannot supply pairing.

- **The remaining exactness claim is too strong.** “‘Exact’ means exact for deterministic opponents that finish within that fuel.” Deterministic opponents can branch on nested read timeouts: reduced fuel can change their returned action even when they finish successfully. **Fix:** call these uncapped shared-fuel simulations throughout; claim agreement only where execution is budget-invariant, and measure actual-versus-simulated disagreement among completed deterministic simulations.

## 2. Design flaws/confounds

- **Fallback-conditioned exploitability is not policy exploitability.** “Non-fallback mixing 0 and exploitability 1 by convention” assigns maximal exploitability to a policy whose actual fallback action is uniform. Conversely, conditioning on completion can hide opponent-dependent failures. **Fix:** report actual-policy exploitability, including fallback actions, separately from completion-conditioned diagnostics. Mark zero-completion conditional quantities undefined; keep fallback rates and charges explicit.

- **Outcome-dependent extensions compromise matched comparisons.** Only “unresolved or high-forfeit cells” extend to generation 4,000. **Fix:** retain generation 2,000 as the primary endpoint; extend all members of any selected matched comparison and label extension results secondary.

- **Inference is underspecified.** Confidence level, equivalence procedure, aggregation across levels and the meaning of “above 0.05 by upper bound” are unstated. An upper bound above a threshold establishes uncertainty, not excess. **Fix:** preregister interval procedures and distinguish demonstrated failure from failure to demonstrate equivalence.

## 3. Predictions likely wrong

- **9:** Charging fallback more than a coin does not establish dominance of the whole program. Readers can profit on successful executions while occasionally falling back. I predict persistent fallback is possible at 0.1, especially with X; its rate depends on the successful-play advantage.

- **10:** A_m removes the +1 reward for causing an opponent’s unilateral forfeiture and improves the forfeiter’s payoff. That changes selection, not merely measurement. I expect the largest A_m/A_f differences where reader-induced failures are common; identical classifications across every cell are doubtful.

- **11:** The stated “worst case” ignores earlier capped-read charges and possible exploitation on completed plays. I expect an improved *failure branch* under A_m, but no robust twofold population-mass effect.

## 4. Missing controls / cheap additions

- Test A_m’s fallback independence, mutual fallback, nested-timeout accounting, reservation exhaustion and payoff tables directly.
- Report successful-play advantage versus failure loss for each simulator class.
- Preserve prediction-linked cells in the cut order, or mark affected predictions untested.

## 5. Alternative explanations not ruled out

Apparent success may reflect selection of free coins rather than useful source reasoning; apparent X effects may reflect budget-sensitive action changes rather than better prediction; apparent persistence may be slow transient sorting. Existing diagnostics help, but endpoint classifications alone cannot distinguish these mechanisms.
