# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/results_fp.md` by gemini-4-argon

1. **Draft:** "Extras outside the spec: concurrent A at 10, A+X at 0.3 and 0.03, A_m with and without X at 1 in inspection, and a supplement of 80 more runs in 12 inspection cells..."
**Evidence:** Neither `A+X` at 0.3 nor `A+X` at 0.03 was run (see `runs/forfeit-pricing.md` "Cells present": `A+X` is only at 0.1 and 1). Also, `A_m` without X at 1 in inspection was required by the spec's addendum ("inspection at 0.1 and 1 without X"). The actual extras listed in `notes/forfeit-pricing.md` §2.9 and `runs/forfeit-pricing.md` are: concurrent A at 10, `A_m + X` in RPS at every level (though already listed in the spec addendum), and `A_m + X` at 0.1 and 1 in inspection.
**Correction:** Replace "A+X at 0.3 and 0.03, A_m with and without X at 1 in inspection" with "A_m+X at 0.1 and 1 in inspection".

2. **Draft:** "RPS under A_f is met by mixing at every level from 0.03 to 10 (gross exploitability 0.000 and forfeits 0.000 through 1; forfeits 0.001 at 10)..."
**Evidence:** In the band table (`runs/forfeit-pricing.md`), `Af@0.03` has `e_gross` = `0.031 [0.002, 0.085]` (and `Af@10` has `0.017`). `e_gross` is `0.000` only at 0.1, 0.3, and 1.
**Correction:** Change to "(gross exploitability 0.031 at 0.03, 0.000 from 0.1 through 1, and 0.017 at 10; forfeits 0.000 through 1 and 0.001 at 10)".

3. **Draft:** "`SIMX_I` is selected at every price under A_f (mass 0.37–0.73, modal 0.37–0.72)..."
**Evidence:** At the primary endpoint (generation 2,000, 40 runs), `SIMX_I` mass under `Af+X` ranges from `0.36729` (at 0.1) to `0.71832` (at 10), which rounds to `0.37–0.72`. (`0.728` is the 120-run supplementary mass at 10).
**Correction:** Change "mass 0.37–0.73" to "mass 0.37–0.72".

4. **Draft:** "...and the engineer's E2 (the guarded reader, not the coin, carries the high end), E5–E9 and E12."
**Evidence:** Prediction `E11` ("A_f is confirmed at 0.03, 0.1, 0.3 and 1, and confirmed or unresolved at 10 [refuted at any of 0.03-1, or confirmed label differs at 0.1]") was registered in `predictions/2026-10-26-forfeit-pricing.md`, omitted from the `runs/forfeit-pricing.md` verdict table, and omitted from the draft. Because `A_f` is registered as `unresolved` at every level (including 0.1), `E11`'s falsifier ("confirmed label differs at 0.1") triggered.
**Correction:** Add `E11` to the failed engineer predictions in the draft (and note its omission from the run report table).

5. **Draft:** "The RS's sponsorship worry is real under A_m at low prices: forfeits turn into referee coin draws (0.10–0.21 of plays) and the free coin takes the high end."
**Evidence:** Under `A_m`, the free coin (`U`) is modal on `0.35` (at 0.03), `0.64` (at 0.1), `0.83` (at 0.3), `0.42` (at 1), and `0.04` (at 10, where `PRR` is `0.93`). `U` takes the middle/moderate prices (0.1–0.3, and splits 1), not the high end (10).
**Correction:** Change "takes the high end" to "takes the middle of the band (0.1–0.3, and nearly half of 1)".
