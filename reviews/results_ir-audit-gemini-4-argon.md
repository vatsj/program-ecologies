# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/results_ir.md` by gemini-4-argon

**1. Overstatement of `target (V*)` under locking arms at mN = 0.1**
- **Draft:** "Rejecting every play-changing immigrant on member islands by fiat meets the target in 0.03 / 0.95 / 1.00 of runs, and freezing the pivot's partner choice in 0.00 / 0.88 / 0.88; at mN = 0.01 waste islands are never cleared. A locking guard (the spec's candidates) can do no better."
- **Evidence:** In `runs/immigrant-rejection.md` ("Coverage at generation 10,000"), those numbers are for `target (as stated)` (efficient modal outcome). For `target (V*)` (every island on a fair pair and all three present)—which `predictions/2026-10-25-immigrant-rejection.md` defines alongside `target (as stated)` as the RS's target—FI achieves `0.00 / 0.03 / 1.00` and FP achieves `0.00 / 0.05 / 0.88` (whereas gV and gKRw achieve `1.00` at mN = 0.1).
- **Correction:** Specify that 0.03 / 0.95 / 1.00 and 0.00 / 0.88 / 0.88 are for `target (as stated)`, and report the `target (V*)` shares alongside them (`0.00 / 0.03 / 1.00` for FI and `0.00 / 0.05 / 0.88` for FP).

**2. Unverified numbers for proposal acceptance counts**
- **Draft:** "The farsighted guard with weak consent, gKRw, accepts all nine fair-to-fair contracts at the fair pairs and no other contract there... The strict farsighted guard gKR, which accepts two of the nine..."
- **Evidence:** The counts "all nine" and "two of the nine" (along with "36 of the 90 proposals" in `notes/immigrant-rejection.md` §3) do not appear in the tables or text of `runs/immigrant-rejection.md`.
- **Correction:** Either add the guard proposal-acceptance counts to `runs/immigrant-rejection.md` or cite the code/table inspection where they are verified.
