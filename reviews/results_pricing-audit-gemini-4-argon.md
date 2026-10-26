# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/results_pricing.md` by gemini-4-argon

1. **PD timeouts per play under Rule A**
* **Draft:** "In the PD and inspection, A changes little against the zero price (PD timeouts are about 0.016 per play)."
* **Evidence:** In `runs/pricing-rules.md`, 0.016 is the `timeouts/play` in *inspection* at A 0.1 (`0.016 [0.004, 0.031]`). In the *PD* detail table, `timeouts/play` under A is `0.0000` at 0.01 and 10, `0.0002 [0.0000, 0.0006]` at 0.1, and `0.0000 [0.0000, 0.0001]` at 1.
* **Correction:** Change "(PD timeouts are about 0.016 per play)" to "(PD timeouts are ≤ 0.0002 per play; inspection timeouts at A 0.1 are 0.016)".

2. **Simulator share in RPS under B and B-own**
* **Draft:** "*Amortizing (B, B-own) keeps the PD and gives RPS back to the simulators* (0.55–0.63 of the lottery against 0.88 at the sampled zero price): free repeated reads are what lets simulators beat the coin."
* **Evidence:** In `runs/pricing-rules.md` (RPS detail), at the sampled zero price (`Zs 0`), the simulator share is `0.699 [0.599, 0.794]` (0.880 is the exact-kernel `F 0.0001` simulator share; `Z 0` is 0.845). Across `B` and `Bo` from $10^{-5}$ to $10^{-2}$, the simulator share ranges from `0.327` (`Bo 0.01`) to `0.688` (`B 1e-05`), or `0.552–0.688` across $10^{-5}\dots 10^{-3}$.
* **Correction:** Replace "(0.55–0.63 of the lottery against 0.88 at the sampled zero price)" with "(0.55–0.69 of the lottery at $10^{-5}\dots 10^{-3}$, and 0.33–0.41 at $10^{-2}$, against 0.70 at the sampled zero price)".

3. **Comparison of B-own and B in RPS and inspection**
* **Draft:** "The owned memo is not between F and B: it equals B within 0.02 in RPS and inspection..."
* **Evidence:** In `runs/pricing-rules.md`, `Bo` and `B` differ by up to 0.066 in RPS (`0.262` vs `0.328` at $10^{-2}$) and by up to 0.274 in inspection (`0.600` vs `0.874` at $10^{-5}$, `0.702` vs `0.622` at $10^{-4}$, `1.000` vs `0.899` at $10^{-2}$). Even restricted to the panel levels $10^{-4}$ and $10^{-3}$, inspection at $10^{-4}$ differs by 0.080 (`0.702` vs `0.622`).
* **Correction:** Change "it equals B within 0.02 in RPS and inspection" to "at the panel levels ($10^{-4}, 10^{-3}$) it is within 0.02 of B in RPS and 0.08 in inspection (and differs by up to 0.07 in RPS and 0.27 in inspection across all four levels)".

4. **Unsubstantiated program shares in RPS under Rule A**
* **Draft:** "...and the islands are held by the counted-probability reader `PRR` (0.911 of islands) at 0.1 and by the prover `PB` (0.49) at 1: readers whose reads finish pay nothing."
* **Evidence:** Neither `PRR` (0.911) nor `PB` (0.49) appears in `runs/pricing-rules.md`, `notes/pricing-rules.md`, or `predictions/2026-10-25-pricing-rules.md` (in `runs/pricing-rules.md`, 0.911 appears only as the fraction of simulating inspectors in inspection at A 1).
* **Correction:** Verify that 0.911 and 0.49 come from `runs/pricing-rules.json` / `runs/pricing_rules/` and add them to `runs/pricing-rules.md`, or remove the specific program-share numbers from the draft.
