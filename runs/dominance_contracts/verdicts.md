## Verdicts (scored against `predictions/2026-10-14-dominance-contracts.md`)

Occupancy below is the registered definition (islands classified ≥ 0.95 on a member, the baseline's 0.281 / 0.739);
"modal" is the spec's wording (argmax of the island's encounter distribution), reported because the two part at
mN = 1. **They agree at mN = 0 everywhere.** At mN = 1 contracts keep the islands on different outcomes, so every
migrant is mismatched and selection against it leaves a standing load of 5–25% of encounters: the island's modal play
is unchanged but the 0.95 test fails (other-mixed 0.5–0.95 of islands in the contract cells, 0.03 in the baseline,
where migration builds a consensus and migrants match). Disclosed here, after the run: the modal-play column was
added to the report when the D1 mN = 1 cell showed the split; no prediction was re-scored on it.

| # | prediction | outcome |
|---|---|---|
| **RS** | contracts deviating to dominating outcomes recover the vNM stable set (D1: occupancy ≥ 0.8 and support ⊆ V\* in ≥ 0.5 of runs, at mN = 0 or 1) | **failed at both mN, on both definitions.** mN = 0: 0.338 [0.318, 0.359] at 2,000, 0.315 at 10,000, support 0/40. mN = 1: 0.091 (modal 0.338) at 2,000, 0.084 (modal 0.324) at 10,000, support 0/40 (stable-sets definition 0/40). The occupancy is the exact proposal generator's 1/3. |
| RE 1 | D1 within 0.1 of the walk (0.2–0.4 at mN = 0); support ≤ 0.2; falsifier ≥ 0.6 | **held** (0.338 vs 1/3 at mN = 0; modal 0.338 at mN = 1; registered occupancy at mN = 1 is 0.091, outside the band by the migration load, not by the walk) |
| RE 2 | D1 at mN = 1 below the baseline's 0.74 because contracts break the consensus | **held** (0.091, paired Δ −0.65; modal 0.338 vs 0.843; consensus 0/40 vs 26/40) |
| RE 3 | D2 between the baseline and D1 | **held** (mN = 0: 0.345 [0.325, 0.366] against 0.281 and 0.338, within D1's uncertainty; mN = 1: 0.261 between 0.091 and 0.739; modal 0.679 between 0.338 and 0.843) |
| RE 4 | refusal lost where private (mean < 0.5 in ≥ 0.8 of runs at mN = 0), neutral where public; occupancy rises with the island's bit | **failed.** Public, mN = 0: neutral (change −0.007 [−0.017, 0.003]) and island member time-share rises with the bit (Spearman 0.63; 0.34 with no refusing slot, 1.0 with two or more): held. **Public, mN = 1: the bit rises in 40/40 runs, 0.50 → 0.80 by 10,000 (falsifier fired).** Private, mN = 0: mean < 0.5 in 0.60 of runs (change −0.011): clause failed. **Private, mN = 1: rises in 40/40 runs, 0.50 → 0.96 by 2,000 (falsifier fired).** The r-blind control does not move (−0.008 [−0.053, 0.036]). |
| RE 5 | R2: V\* reachable (contracts-only chain) and ≥ 0.9 occupancy, support ≥ 0.8 of runs | **held at mN = 0** (reachability a theorem of the generator; 1.000 occupancy, support 0.97 at 2,000 and 1.00 at 10,000); **falsifier fired at mN = 1 on the registered classifier** (0.331 / 0.316), read through the hazards: exits from V\* 3.8·10⁻⁵ per member-island-generation, modal occupancy 0.996 / 0.998, support (stable-sets definition) 0.95 / 1.00 of runs, coverage 1.00; the failure is the migration load between islands on different members (consensus 0/40), not leakage |
| RE 6 | D4 within 0.1 of the baseline at mN = 0 | **held** (0.220 vs 0.281, paired Δ −0.061); menus fall from 18.1 contracts to 0.40 by generation 100 and 0.29 by 250 |
| RE 7 (revised) | β\* > 0.5 for every member exit; fixation ≤ 0.05 at β = 0.25; D3 within uncertainty of the baseline; falsifier fixation ≥ 0.2 | **failed in two of three clauses; falsifier not fired.** β\*_static 0.76 (holds), β\*_flow 0.40 (fails); member-exit fixation at β = 0.25 = 0.13 (0.07 when the excluded constant is neutral, ≈ 0.7 when it already offers); D3 at mN = 0 is +0.117 [0.089, 0.144] above the paired baseline |
| Gemini (counter to RE 7) | fixation < 0.05 and D3 identical to the baseline | **failed** (0.13; +0.117) |
| RE 8 (Gemini's alternative, as a test) | if D1(mN = 1) > D1(mN = 0), entries into V\* at mN = 1 are carried by drift and migration | **premise false**: D1(mN = 1) is not above D1(mN = 0) (0.091 vs 0.338; modal 0.338 vs 0.338); 0.986 of entries into V\* at mN = 1 are contract-triggered. (At ν = 0.01, D2 at mN = 1, 0.60 of entries are not contract-triggered.) |
| S1 | D1 mN = 0 within 0.05 of 1/3 at 2,000 and 10,000; unequal 1/2, wasteful 1/6 | **held** (0.338 / 0.315; 0.505 / 0.517; 0.157 / 0.168) |
| S2 | RS fails in D1; mN = 1 occupancy in [0.45, 0.62] | RS clause **held**; the mN = 1 interval **failed** (0.091; modal 0.338); falsifier not fired |
| S3 | contract jumps follow the generator | **held** (member → unequal 1.000 of 62,791 contract jumps at mN = 0; unequal rows 0.333 / 0.334 / 0.333; wasteful 0.252 / 0.499 / 0.249) |
| S4 | same-member return 0.32 ± 0.06 at mN = 0, higher at mN = 1 | first clause **held** (0.326); second **failed** (0.326 at mN = 1) |
| S5 | ≥ 0.4 of entries into V\* not contract-triggered at mN = 1 | **failed, falsifier fired** (0.014) |
| S6 | member-exit fixation ≤ 0.05 at β = 0.25, ≥ 0.5 at 0.5; entries ≥ 3× exits; D3 − baseline ≥ 0.1 | **falsifier fired** (0.13 ≥ 0.1); 0.51 at β = 0.5 held; entries 1.6× exits failed; D3 − baseline +0.117 held |
| S7 | R1-public mN = 0: [0.75, 0.92] at 2,000, ≥ 0.85 at 10,000, support ≤ 0.1, bit change ≤ 0.05, protected islands ≥ 0.9, (0,0,0) ≈ 1/3 | **held** (0.845; 0.915; 0/40; −0.007; protected 1.000, unprotected-by-bits 0.36) |
| S8 | R1-private mN = 0 in [0.55, 0.78]; bit falls ≤ 0.05 at mN = 0, ≥ 0.05 at mN = 1 | first two **held** (0.675; −0.011); **falsifier fired** at mN = 1 (rises +0.46) |
| S9 | R2 ≥ 0.95 at mN = 0, [0.8, 0.95] at mN = 1, hazard ≤ 1/500 | mN = 0 **held** (1.000); **falsifier fired** at mN = 1 on the registered classifier (0.331; modal 0.996); hazard held (3.8·10⁻⁵) |
| S10 | D4 mN = 0 in [0.18, 0.34], menus ≤ 1 | **held** (0.220; 0.29) |
| S11 | D1 mN = 0: efficiency +≥ 0.05, occupancy +≤ 0.08 | **held** (+0.087; +0.057) |
| S12 | D1 mN = 0 within 0.05 of 1/3 at N = 50, 200 | **held** (0.352 / 0.355 at 2,000; 0.317 / 0.310 at 10,000) |
| S13 | no D cell meets the RS thresholds; R2 mN = 0 meets both by 10,000; R1-public meets occupancy, fails support | **held** (R2-0: 1.000, support 1.00; R1pub-0: 0.915, support 0) |
