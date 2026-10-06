## 6. What ran, what did not

Ran to completion:
- catalogue, soundness and lumping checks;
- static screening under all six priors;
- m = 0 calibration for all six priors;
- homogeneous controls: b = 4 (150 runs), b = 8 (300), b = 16 (300);
- (a) natural runs at the common mN = 1.091: cheap-heavy and above-threshold, 3,000 runs each, paired seeds.

**Did not run** (the session's compute ran out; the coordinator asked for the report on the finished data):
- (b) the forced bridge-less and forced bridged pairs, with their inert-defector and iid controls;
- (a) the calibrated cells (cheap-heavy at mN = 1.000; the other priors' boundaries equal the common mN) and the uniform prior;
- (c) the scaling panel.

The forced pairs remain as declared in the predictions addendum.

## 7. Verdicts

| # | prediction | outcome |
|---|---|---|
| RE 1 | named pair (`BOX1(THEM(ME))`@4, @16) incompatible and direct-bridge-less; cheap-heavy / above-threshold bridge-less mass ≥ 10×; core at ≥ 8 one component | **held**: no structural bridge, ratio ≈ 530, FairBot and `BOX1(THEM(ME))` at 8 and 16 in one component. The above-threshold prior does keep 67 light bridge-less pairs (6.4·10⁻⁸), as RE 1 allowed. |
| RE 2 | cheap-heavy natural horizon separation > above-threshold at the common mN (point ≥ 5 vs ≤ 2) | **held**: 2,048/3,000 = 0.683 [0.666, 0.699] against 6/3,000 = 0.002 [0.001, 0.004]; paired 2,043 cheap-only vs 1 above-only. The above-threshold count exceeds the RE's point expectation of ≤ 2; that is not a falsifier. |
| RE 3 | horizon − first-checkpoint composition distance ≥ 0.1 under cheap-heavy, toward higher budgets | **failed, falsifier fired (narrowly)**: ΔTV = +0.0299 [+0.026, +0.034] against the 0.03 falsifier. The interval straddles 0.03. The direction is the RE's: mean holder budget +0.32 [+0.28, +0.36] budget units, +0.51 in unseparated runs. The pooled-over-runs TV *falls* (0.186 → 0.136), so the distance statistic does not capture the shift well. |
| RE 4 | bridged forced pair resolves with a bridge, separates without; bridge-less separation persists on the scaling panel | **not tested** (cells did not run). Indirect natural evidence (not a substitute): among cheap-heavy runs whose first separation was a bridged pair, all 382 with the bridge alive at the horizon resolved, and 481 of 512 with the bridge dead ended separated. |
| RE 5 | island P(C,C) ≥ 0.97 every cell; homogeneous b = 4 ≈ 0.8, b = 16 ≈ 0 separated | **held** on the cells that ran: island P(C,C) over certified islands ≥ 0.992 per cell (lowest run 0.979); b = 4 0.813 [0.742, 0.872]; b = 16 0/300 (one-sided 95% ≤ 0.010). |
| S1 | ≥ 0.8 of cheap-heavy bridge-less mass on `BOX1(THEM(ME))`@4; above-threshold mass < 10⁻⁸ with no FairBot/`BOX1(THEM(ME))` copy | **failed, falsifier fired**: share 0.995 held, mass 6.4·10⁻⁸ grey, but 4 above-threshold bridge-less pairs contain FairBot or `BOX1(THEM(ME))` at 8 or 16, against the b = 8 soft clique `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))`@8. |
| S2 | cheap-heavy ≥ 0.3 separated, ≥ 0.7 of them with `BOX1(THEM(ME))`@4; above-threshold ≤ 3/3,000 | **held on two clauses, grey on one**: 0.683; share 1,931/2,048 = 0.943; above-threshold 6/3,000 is between 3 and the falsifier's 10. Overall inconclusive by the grey clause. |
| S3 | under cheap-heavy, mean holder budget does not rise by > 0.5 units and TV change < 0.1 (direction: falls or stays) | **held on its numbers** (+0.32 units, ΔTV +0.030); **the stated direction was wrong**: holder budgets rise, and in unseparated runs by +0.51. |
| S4 | homogeneous b = 4 in [0.65, 0.92], b = 8 ≤ 0.01, b = 16 ≤ 0.005 | **held** (0.813; 1/300; 0/300) |
| S5, S6 | forced pairs | **not tested** |
| S7 | island P(C,C) ≥ 0.98 per cell; run-level efficient fraction ≥ 0.95; cf cross P(C,C) of separated cheap-heavy runs in [0.4, 0.85] | **inconclusive**: island P(C,C) 0.992–1.000 held; cf cross 0.61 held; run-level 0.935 (cheap-heavy) and 0.930 (b = 4) are between the claim (0.95) and the falsifier (0.9). |
| S8 | T_nuc 45–65 under every prior; calibrated cheap-heavy separation within 0.1 of common | **calibration clause held** (55–60); separation clause **not tested** |

## 8. Reading

- **Mixed budgets do not split FairBot; they split `BOX1(THEM(ME))`.**
  - FairBot cooperates with itself at every pair of budgets in {4, 8, 16}.
  - `BOX1(THEM(ME))`@4 cooperates with nothing outside itself, so no program at any budget bridges it.
  - Under cheap-heavy it carries 0.995 of the bridge-less pair mass and is a member of 0.943 of the 2,048 horizon separations.
- **The obstruction is dynamic as well as static.**
  - 0.683 of cheap-heavy runs end separated, against 0.002 under above-threshold (paired, same seeds) and 0.813 in the homogeneous b = 4 control.
  - Every island stays efficient (island P(C,C) ≥ 0.99). What is lost is the cross-island counterfactual (0.61 in separated runs).
- **Bridged incompatibilities resolve iff the bridge survives**, as in the free box and in K at a single budget.
  - Cheap-heavy first separations with a living bridge: 382 of 382 resolved.
  - With the bridge dead: 481 of 512 ended separated.
  - The 113 horizon separations of bridged pairs are all dead-bridge runs.
- **Above the copy thresholds the residue is one b = 8 soft clique.**
  - `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))`@8 is in all 6 above-threshold horizon separations and the 1 b = 8 separation.
  - The b = 16 control has none.
- **Holder budgets drift upward after founding, slowly.** The mean holder budget rises +0.32 budget units (+0.51 where no rival survives). Compatibility selects the copies that cooperate with more partners. The composition distance moves only 0.03, so selection after founding is weak at this horizon.
- *Scope:* finite-horizon incidence at n = 8, N = 200, I = 64, horizon 10⁵. The forced cells, calibrated cells, uniform prior and scaling panel did not run.
