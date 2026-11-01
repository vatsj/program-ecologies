# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/results_ub.md` by gemini-4-argon

- **Draft:** `| the 16 fair-reader programs per slot | 0.4875 | U at every scanned u down to 0.1 |` (and in Reading: "Removing them alone sends M unequal from every scanned start.")
  - **Evidence:** In `runs/unequal-basin.md`, the tilt scan table for `M0 | 3 | auto | fam:fair-reader` has `range = [0.3, 0.9]` and scanned values `0.3:U, 0.4:U, 0.5:U, 0.6:U, 0.7:Ue, 0.8:Ue, 0.9:Ue`. No scan down to 0.1 is in the run report.
  - **Correction:** Change `down to 0.1` to `down to 0.3` (or commit the 0.1–0.2 scan rows to `runs/unequal-basin.md`).

- **Draft:** `Lumping is exact where it merges (111 programs to 45 classes, field to 10⁻¹⁸).`
  - **Evidence:** `runs/unequal-basin.md` validation `v2` reports `L-all-action: 111 -> 45 classes, field diff 4.8e-20; ... M-all-action: 111 -> 42 classes, field diff 2.7e-18`.
  - **Correction:** Change `45 classes` to `45 (L) and 42 (M) classes`.

- **Draft:** `Object P against a fresh Monte Carlo of the full dynamics from the same law: within 0.0011 (L) and 0.0025 (M) to 3,000 events.`
  - **Evidence:** `runs/unequal-basin.md` validation table shows `v3-L0-m3-core` and `v3-M0-m3-core` have `max |ODE - MC(m)| 0.0011` and `0.0025`, while `max |ODE - MC(full)|` is `n/a` (only `v3-L0-m1` reports `MC(full)`, at `0.0018`).
  - **Correction:** Clarify whether the `0.0011` and `0.0025` comparisons for `m3-core` were against the matched-truncation MC or full-dynamics MC, and update `runs/unequal-basin.md` if they were against full dynamics.

- **Draft:** (Omission in §2 table and text)
  - **Evidence:** `runs/unequal-basin.md` ("u* and the tilt scans" and "One pool (support sensitivity) and the raw unsymmetrized pool law") and `notes/unequal-basin.md` (§2.3) report two material results that the draft omits: (1) the "victims" (`orb:0.0`, ⅓-constants) knockout gives `u* = none` in L, and in M gives a non-monotone regime (`U` for `u ∈ [0.5625, 0.8375]`, returning to `F` at `0.85` and `0.9`), while the draft's caveats mention "the 'victims removed' knockout" without it appearing in the text or table; (2) the raw unsymmetrized pool-0 law (`raw`) ends at `U = 1.0000` even from L's natural start (`0.9997 F` when symmetrized), showing that single-pool sampling asymmetry suffices to send L's natural start to an unequal orientation.
  - **Correction:** Add the `orb:0.0` (⅓-constants removed) row to the §2 table and note the raw unsymmetrized pool-0 natural-start result in §1 or §4.
