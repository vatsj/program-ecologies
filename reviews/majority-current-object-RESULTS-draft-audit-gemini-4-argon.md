# Review of `notes/majority-current-object-RESULTS-draft.md` by gemini-4-argon

1. **Draft:** "...the majority-triple version is reported beside it and has the same cell mean in every cell..." (also in *Caveats*: "`modal` and the majority-triple series have identical cell means")
**Evidence:** In `runs/majority-current-object.md` (Key table), `V*` is reported to 3 decimal places while `V* (maj. triple)` is rounded to 2 decimal places. Even at 2 decimal places, they differ in `T | main | 400 | 0 | 0.1` (`V*` 0.997, `V* (maj. triple)` 1.00) and `T | main | 400 | 100 | 1` (`V*` 0.999, `V* (maj. triple)` 1.00).
**Correction:** Change "has the same cell mean in every cell" and "have identical cell means" to "have cell means within 0.01 in every cell (agreeing to two decimal places in all but two cells)".

2. **Draft:** "The readers carry T: T − T0 at Λ = 100 is +0.18 [0.05, 0.30] at N = 100, +0.28 [0.13, 0.43] at N = 200, +0.74 [0.55, 0.90] at N = 400..."
**Evidence:** `runs/majority-current-object.md` (Paired contrasts on V*) reports: `T-T0|N100|mN1|lam100: 0.175 [0.075, 0.300]`, `T-T0|N200|mN1|lam100: 0.275 [0.150, 0.425]`, and `T-T0|N400|mN1|lam100: 0.742 [0.537, 0.901]`.
**Correction:** Update the bootstrap intervals to `[0.08, 0.30]` (or `[0.075, 0.300]`) at N = 100, `[0.15, 0.43]` (or `[0.150, 0.425]`) at N = 200, and `[0.54, 0.90]` at N = 400.

3. **Draft:** "D1 − main: +0.075 [−0.025, 0.175] at N = 100, +0.275 [0.10, 0.45] at N = 200 (at mN = 0.1: −0.02 and +0.10, intervals include 0). D3 − main: +0.18 [0.05, 0.33], +0.50 [0.35, 0.65]."
**Evidence:** `runs/majority-current-object.md` (Paired contrasts on V*) reports `D1-main|N100|mN1|lam100: 0.075 [-0.025, 0.200]` (though the prediction table row for RE 8 lists `[-0.025, 0.175]`) and `D3-main|N100|mN1|lam100: 0.175 [0.050, 0.300]`.
**Correction:** Change the D3 − main interval at N = 100 to `[0.05, 0.30]` (and reconcile the D1 − main upper bound at N = 100 between `0.175` and `0.200`).

4. **Draft:** "At mN = 1 no class transitions occur in the 20N chase in any M, L or T cell (closed populations: F exit rate and entry rate to F both 0.000)..."
**Evidence:** `runs/majority-current-object.md` (Transition structure) reports non-zero chase transition rates at mN = 1 for `L | main | 200 | 100 | 1 | chase | d25` (`F exit` 0.001) and `M | main | 200 | 0 | 1 | chase | d25` (`entry to F` 0.001), as well as in the `M | D4` cells at N = 200 (`F exit` 0.005 / 0.004, `entry to F` 0.002 / 0.001).
**Correction:** Specify "under the `dq` debounce in main cells (and ≤ 0.001 under `d25`; ≤ 0.009 in D4 at N = 200)" instead of claiming no class transitions occur in any cell.

5. **Draft:** "(a) In the current object at these sizes arm T meets the stable-set target at mN = 1 in every run and cell..."
**Evidence:** In `T | main | 400 | 100 | 1`, `V*` is 0.999 and 1 of 20 runs is mixed (63 fair islands, 1 unequal island), as the draft notes in Section 1.
**Correction:** Change "in every run and cell" to "in every cell (and every run except one island of one run at N = 400, Λ = 100)".
