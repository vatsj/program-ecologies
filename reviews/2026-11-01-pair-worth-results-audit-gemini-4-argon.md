# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/results_pw.md` by gemini-4-argon

1. **Result 1 — Confidence interval mismatch.**
- *Draft:* "G1/3, C+B* (bids on all 28 splits, dose 0.05), Lambda 10, mN 1: core proper 0.25 [0.05, 0.45] of islands (20 runs..."
- *Evidence:* `runs/pair-worth.md` End class shares table for `CBs, 100, 0.05, 10, 1` gives `0.25 [0.10, 0.45]` (also in the RE2 verdict row).
- *Correction:* Change `[0.05, 0.45]` to `[0.10, 0.45]` (or reconcile the `RS conjecture` verdict row in `runs/pair-worth.md` if `[0.050, 0.450]` was a typo there).

2. **Result 2 — High-dose C+B* core and pair shares.**
- *Draft:* "Raising the dose with 28 splits does not help (0.30: 0.18; 0.50: 0.05 core, pair 0.95)..."
- *Evidence:* `runs/pair-worth.md` for `CBs, 100, 0.5, 10, 1` gives `core 0.09 [0.00, 0.22]` and `pair (kind) 0.91 [0.79, 1.00]` (`dom-waste 0.91 [0.78, 1.00]`).
- *Correction:* Change `0.50: 0.05 core, pair 0.95` to `0.50: 0.09 core, pair 0.91`.

3. **Result 2 — Level-0 bids vs C interval.**
- *Draft:* "Level-0 bids (no working fallback) are not distinguishable from C at 20 runs (0.15 vs 0.45 at mN 1, interval includes 0)."
- *Evidence:* `runs/pair-worth.md` E2 verdict row gives `pw13 CB0 - C -0.300 [-0.550, 0.000]` and `pw13 CBs0 - C -0.200 [-0.500, 0.100]`. At Lambda 10, mN 1, `CB0` is 0.15 (paired interval touches 0.000 at the boundary), while `CBs0` is 0.25 (interval `[-0.500, 0.100]` crosses 0).
- *Correction:* Specify both arms: `(CB0 0.15, CB*0 0.25 vs C 0.45 at mN 1; paired intervals [-0.55, 0.00] and [-0.50, 0.10] include 0)`.

4. **Result 4 & Predictions scored — Ring appearance and transfer effect in the glove market.**
- *Draft:* "Ring islands 0.00-0.01 in every cell; on the 24ths grid (G2/3', glove') the end states are the same as on sixths." and "RE4 failed (no ring in either arm, transfers change nothing)".
- *Evidence:* In `runs/pair-worth.md`, Glove (sixths) has ring share `0.05`–`0.53` in C and `0.06`–`0.74` in CB (as Result 5 itself notes: `0.55 in C+B`). On 24ths (`Glove'`), the ring share drops to `0.00` across all cells (moving from `0.55` ring / `0.45` eff-dom in CB at mN 1 on sixths to `0.00` ring / `1.00` eff-dom on 24ths).
- *Correction:* Qualify Result 4 to state that ring islands are `0.00-0.01` in G1/3 and G2/3 (where RE4 is scored), whereas in the glove market the Bertrand ring `(5/6, 1/6, 0)` reaches `0.05-0.74` on sixths and disappears (`0.00`, shifting into dominated efficient splits) on 24ths.

5. **Result 5 — Glove end-state shares and Bertrand ring in arm C.**
- *Draft:* "...islands end on dominated efficient splits (0.95) or the ring (0.55 in C+B); (1,0,0) never, the core is unreachable, and the Bertrand ring (5/6,1/6,0) appears in C+B only (0.55 [0.35, 0.75])."
- *Evidence:* `runs/pair-worth.md` (Glove, Lambda 10, mN 1) shows C has `eff-dom 0.95` and `ring 0.05 [0.00, 0.15]` (and at mN 0.1, C has `ring 0.53 [0.35, 0.73]`), while CB at mN 1 has `eff-dom 0.45 [0.25, 0.65]` and `ring 0.55 [0.35, 0.75]`. The RE5 verdict row explicitly records `(5/6,1/6,0) 0.050 [0.000, 0.150]` for glove C.
- *Correction:* Change to "...at mN 1 islands end on dominated efficient splits (0.95 in C, 0.45 in C+B) or the Bertrand ring (5/6,1/6,0) (0.05 [0.00, 0.15] in C, 0.55 [0.35, 0.75] in C+B; 0.53 and 0.69 at mN = 0.1); (1,0,0) never, and the core is unreachable."

6. **Result 6 — G5/6 CB N = 200 exception and high-dose arm label.**
- *Draft:* "G5/6 C, C+B, C+B+K, C+B2, C+G, C+A, R, R+B: 1.00 of islands end in a pair at mN 1 and 0.1, with and without the tail; grand-split islands appear only at mN = 0 and only at a high dose (0.37 at dose 0.3, 0.72 at dose 0.5 for the equal-split bid)."
- *Evidence:* In `runs/pair-worth.md` (G5/6), `CB, 200, 0.05, 10, 1` has `pair 0.95 [0.85, 1.00]` and `grand-eff 0.05 [0.00, 0.15]` (and several `mN = 0.1` cells at N = 100 are `0.98`–`0.99` pair with `0.01`–`0.02` grand-eff). Also, `0.37` and `0.72` at mN = 0 are for arm `CB` (core-or-equal bids), not `CBe`.
- *Correction:* Specify "at N = 100, 0.98–1.00 of islands end in a pair at mN 1 and 0.1 (1.00 in every mN = 1 cell; 0.95 at N = 200, C+B, Lambda 10)" and change "for the equal-split bid" to "in C+B".

7. **Result 7 — Ambiguous K^2 invasion description.**
- *Draft:* "K^2 with a third slot: the third bid is lost only when the third slot is slot 2 (0.85/N); with the third slot 0 or 1 the bid is paired with a blocker and is selected (4.8/N)."
- *Evidence:* In `runs/pair-worth.md` Invasion assays `(iii)`, `0.85/N` is for a *bid invading a constant* in slot 2 (`K in slots [0, 1], constant in slot 2: B invades slot 2`), whereas a constant G invading a resident bid in slot 2 is `0.75/N` (exact `1.00/N`, neutral drift). In slots 0 or 1, `4.8/N` (exact `4.91/N`) at G1/3 is both the fixation of constant G invading resident B *and* of B invading resident constant (at G5/6, B invading constant is `10.65/N` and `11.25/N`, exact `11.75/N`, while G invading B is `0.25/N` and `0.10/N`, exact `0.23/N`).
- *Correction:* Clarify the game and direction of invasion: "With K^2 in the other two slots: when the remaining slot is slot 2, B and G are mutually neutral (0.75–0.85/N, exact 1.00); when it is slot 0 or 1, B pairs with a blocker (payoff 1/6 at G1/3, 5/12 at G5/6), so B invades a non-grand constant at 4.75–4.80/N at G1/3 (exact 4.91) and 10.65–11.25/N at G5/6 (exact 11.75), while G invades B at 4.50–4.80/N at G1/3 (getting 2/6) but only 0.10–0.25/N at G5/6."
