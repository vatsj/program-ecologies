# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/results_churn.md` by gemini-4-argon

- **Draft:** `## Churn among the fair pairs in the primary object: with flexible readers seeded, islands churn without contracts or a veto (4–21× the baseline's flips)...` (and in Reading: `with flexible readers seeded at about 9%, islands change pair 4–21× as often as without them`)
  **Evidence:** In `runs/churn-primary.md`, the ratio to B6w at mN = 1 is `2.76` for `Emin-hi-m`, `3.24` for `Emin-lo-m`, `3.64` for `Emin-lo-w`, `3.68` for `Emin-main-m`, `3.93` for `Emin-hi-w`, and `3.99` for `T-lo`. Furthermore, the `21×` figure is from `T-hi` (`21.04`), where flexible readers are seeded at `16%` (`0.160`), not `9%`; at the `9%` doses (lo and main), the maximum ratio is `11.0×` (`T-main` at mN = 0.01).
  **Correction:** Change `4–21×` to `2.8–21×` (or `3.7–21×` if restricted to the table's subset), and in the Reading change `with flexible readers seeded at about 9%, islands change pair 4–21×` to `with flexible readers seeded at 9–16%, islands change pair 2.8–21× (3.2–11× at the 9% doses)`.

- **Draft:** `Of the flips with readers seeded, 83–92% occur on islands where a reader is the dominant class of some slot (baseline 1–9%).`
  **Evidence:** In `runs/churn-primary.md` (`routes (redirect / resident / reader)`), the reader-route share in `Emin-main-w` is `7852 / 10807 = 72.7%` at mN = 0.1 and `23660 / 34658 = 68.3%` at mN = 1, and in `Emin-hi-w` is `8347 / 12240 = 68.2%` at mN = 0.1 and `23386 / 33829 = 69.1%` at mN = 1. The `83–92%` range only holds at mN = 0.01 (or in the modal and T arms).
  **Correction:** Change `83–92%` to `68–92%` (or specify `83–92% in the modal and T arms, 68–87% in E-min weak`).

- **Draft:** `At mN = 1 consensus on one pair is reached in 0.80–0.90 of runs with readers, against 0.95 for the baseline.`
  **Evidence:** In `runs/churn-primary.md`, consensus at mN = 1 for `Emin-hi-w` is `0.72`.
  **Correction:** Change `0.80–0.90` to `0.72–0.90` (or specify `0.80–0.90 in the main and lo doses, 0.72–0.90 across all doses`).

- **Draft:** `What the readers do deliver is the efficiency half of the RS's target: at mN ≥ 0.1, 0.97–1.00 of islands sit on a fair pair (baseline 0.56–0.82), without a veto.`
  **Evidence:** In `runs/churn-primary.md` (and the draft's own table), V\* share at mN = 0.1 is `0.89` in `Emin-main-w`, `0.93` in `Emin-lo-w`, and `0.96` in `Emin-lo-m` (and `0.70` in baseline `B6m` at mN = 1).
  **Correction:** Change `0.97–1.00` to `0.89–1.00`.

- **Draft:** `Single immigrants switch an island in 0.07–0.1% of injections over all slots...`
  **Evidence:** In `runs/churn-primary.md` (Probe table and notes §2.2 item 14), the excluded-slot taker configurations (`P-dm-taker-a-single` and `P-dw-taker-a-single`) are single-immigrant injections and switch at `0.8%` (`77 / 10200`) and `0.5%` (`46 / 10200`).
  **Correction:** Clarify that `0.07–0.1%` is for the `const`, `switch`, and `two` configurations, while the excluded-slot `taker` configuration switches at `0.5–0.8%`.

- **Draft:** `Ablations at 0.03 each (post hoc): switchers alone 4.2× and two-partner readers alone 3.6× at mN = 0.1...`
  **Evidence:** In `runs/churn-primary.md`, `4.2×` (`4.22`) and `3.6×` (`3.59`) are for E-min modal only; the T ablations at mN = 0.1 are `4.0×` (`3.99` for `T-abS`) and `3.8×` (`3.78` for `T-abD`).
  **Correction:** Specify that `4.2×` and `3.6×` are in E-min modal (and add `4.0×` and `3.8×` in T).
