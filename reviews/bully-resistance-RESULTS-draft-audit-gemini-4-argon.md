# Review of `notes/bully-resistance-RESULTS-draft.md` by gemini-4-argon

- **Draft sentence:** "`Predictions predictions/2026-11-08-bully-resistance.md` were committed before step 0's assays and before any counted step-2 mass or step-3 cell (addenda for the step-0 and step-2 pilots, for the partial look at the main grid before E10 and the decomposition were written, and for the F+O arm, all before the cells they concern)."
  **Evidence:** `predictions/2026-11-08-bully-resistance.md` discloses that the Step 1 gates (51-program table) were run and read before the predictions file was committed, and that E2, E3, and E4 were written using those gate results (e.g., E2 explicitly cites `Because P_z is self-incompatible... (gate)`).
  **Correction:** Disclose in the provenance sentence (and in Verdicts for E2–E4) that the Step 1 gate table was built and read before the initial predictions commit and informed E2–E4.

- **Draft sentence:** "`P_z` and `O` give the same pattern in UB (median 10^-8 to 10^-13)."
  **Evidence:** `runs/bully-resistance.md` Step 0 table reports UB class medians of `4.3e-08` (`Pz`) and `1.4e-10` (`O`). `4.4e-13` is the pair-slot-only median for `Pz`, not the UB class median.
  **Correction:** Change to `(class medians 4e-8 and 1e-10; pair-slot medians 4e-13 and 1e-10, unpaired slot 1)`.

- **Draft sentence:** "...at N = 200 beta = 3 at most 0.45-0.55 at 3.10^-4)."
  **Evidence:** `runs/bully-resistance.md` Step 3 table for `N = 200, I = 64, beta = 3.0` at `delta = 0.0003` has `F = 0.30`, `FO = 0.36`, `PO = 0.40`, `P = 0.45`, `O = 0.45`, `FPO = 0.55` (and at `N = 200, beta = 3.0` variants, `Po = 0.60`).
  **Correction:** Change `0.45-0.55` to `0.30-0.55 across main arms (0.60 for variant Po)`.

- **Draft sentence:** "...at beta = 0 the idealized table lifts O to 1.00 and F to 0.80 / 1.00 and leaves P at 0.60 / 0.75 (strategic self-incompatibility)."
  **Evidence:** `runs/bully-resistance.md` idealized uncapped table at `beta = 0.0` (for `delta = 0.01 / 0.1`) gives `O` as `0.85 / 1.00` (against `0.65 / 0.95` charged capped).
  **Correction:** Change `lifts O to 1.00` to `lifts O to 0.85 / 1.00`.

- **Draft sentence:** "E4 holds on the profile table (opener 2.0 against 1.0 timed-out reads, P 1.36; not scorable from end-state charges)..."
  **Evidence:** `predictions/2026-11-08-bully-resistance.md` defines E4 strictly on dynamics: `In the beta = 0 control the mean A_f charge per reader per generation at delta = 0.1, N = 200 is at least 1.4 times larger for O than for the firm readers, and P's is within 1.25 times the firm readers'.` Furthermore, the profile numbers `2.0`, `1.0`, and `1.36` were already known from the pre-prediction Step 1 pilot (`predictions/2026-11-08-bully-resistance.md`, Pilot runs).
  **Correction:** Score E4 as **unscorable / indeterminate** (or falsified) as registered because snapshot per-capita charges rounded to `0.000`, and note the profile-table ratio only as the pre-registered pilot observation rather than a passed test.
