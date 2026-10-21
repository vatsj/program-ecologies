# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/core-results-draft.md` by gemini-4-argon

1. **Draft:** "Fixed-role seed lottery at ε = 0: N = 100 per role, 64 islands, w = 0.3, 40 runs, 5,000 generations. Every island is fixed in the constant-only and sequential-evaluator cells (0.95–0.97 in the order-free cells)."
**Evidence:** In `table_cells.csv`, `ann3_threshold_m20` (a sequential-evaluator cell) has `fixed` = `0.9996`, and all rain and migration constant-only cells have `fixed` between `0.275` and `0.8113`. Only the ε = 0 cells without migration fix every island (`fixed` = 1.00).
**Correction:** Specify that fixation is 1.00 *in the ε = 0 cells without migration* (and 0.9996 in `ann3_threshold_m20`).

2. **Draft:** "The core fraction stays small at N = 50, 100 and 200 (0.3–1.2%)."
**Evidence:** In `table_cells.csv` and `runs/core-rediscovery.md` §2/§6, `1a_threshold_unrestricted` (the N = 100 unrestricted cell) has `core` = `0.002344` (0.2%, as stated earlier in the draft).
**Correction:** Change `(0.3–1.2%)` to `(0.2–1.2%)`.

3. **Draft:** "Necessity is not tested, and rain and migration are ongoing, unabsorbed processes (rain fixes 69–77% of threshold islands, migration 31–52%)." and "These are island means, and migration fixes only 31–52% of islands, so averaging over polymorphic encounters may contribute."
**Evidence:** The first sentence specifies *threshold* islands (where migration `fixed` is `0.3129` and `0.5191`), but the second sentence drops the qualifier inside a paragraph about the `skew` and `asymmetric` instances. Across all migration cells in `table_cells.csv`, `fixed` spans `0.275` (`mig_skew_no-overbid`) to `0.5734` (`mig_collusion_no-overbid`).
**Correction:** In the second sentence, either qualify as "31–52% of threshold islands (28–32% in skew)" or state the full migration range "28–57% of islands".

4. **Draft:** "Per-role migration (post hoc) reaches 18% / 45% in the core in the threshold instance, and 2.5% unrestricted in the asymmetric instance, at revenue 19.1–19.5 and efficiency 0.995 / 0.997."
**Evidence:** In `table_cells.csv` and `runs/core-rediscovery.md` §5, `mig_asymmetric_no-overbid` is also run and reaches `0.3375` (34%) in the core at revenue `19.38` and efficiency `0.9958`, while `mig_asymmetric_unrestricted` (the 2.5% cell) has revenue `18.73`, which is outside the stated `19.1–19.5` range (19.13 and 19.51 are the threshold revenues alone).
**Correction:** Report the asymmetric no-overbid core share (`2.5% / 34% in the asymmetric instance`) and adjust the revenue range to `18.7–19.5` (or attribute `19.1–19.5` and `0.995 / 0.997` specifically to the threshold instance).

5. **Draft:** "With two winners and no binding value cap, the Vickrey-nearest point is always the midpoint of the core's bidder-optimal edge (in skew A's payment ranges over 6..14, midpoint 10)."
**Evidence:** In `runs/core-rediscovery.md` §4 and `notes/core-rediscovery.md` §1.5, for `skew` = (14, 16, 8) with minimum revenue 14, individual rationality caps B's payment at v_B = 8, so A's payment on the bidder-optimal edge is 14 − p_B ∈ [6, 14] in the continuous core, or 6..13 on the integer grid (since a zero bid is no bid, b_B ≥ 1, giving midpoint 9.5 as stated in `runs/core-rediscovery.md` §4: "edge middle 9.5"). Furthermore, this makes B's value cap binding on the core edge (u_B ≥ 0 bounds p_A ≥ 6; A's cap v_A = 16 does not bind since p_A ≤ 14).
**Correction:** Reconcile with `runs/core-rediscovery.md` §4: on the positive-bid integer grid used by the baseline, A's edge payment in `skew` is 6..13 (midpoint 9.5, not 10), and the reason `p_A` is bounded below by 6 is precisely that B's individual-rationality (value) cap binds.
