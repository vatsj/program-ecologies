# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/hooksw2-results-draft.md` by gemini-4-argon

- **Draft:** "**Union game** (shares of islands; under mN = 1 all islands of a run end alike):" and the table's missing column.
  **Evidence:** In `runs/hooks-w2.md`, `union-M` has fair 0.000, intermediate (¼) 0.808, zero wage 0.136, and `scab split` 0.056 (and `union-C` has 0.000, 0.891, 0.091, and `scab split` 0.019). Because 0.808, 0.136, and 0.056 are not multiples of 1/40 = 0.025 (40 runs × 16 islands = 640 islands; e.g., 517/640 = 0.8078, 87/640 = 0.1359, 36/640 = 0.05625), not all 16 islands of a run end alike in `union-M` and `union-C`, and the three table columns do not sum to 1 (0.95 and 0.98).
  **Correction:** Change the parenthetical to note that in `union-C-role`, `bw-only-C`, and `myopic-ref` all islands of a run end alike, and either add the `scab split` column (0.056 for `union-M`, 0.019 for `union-C`) or note the omitted scab-split remainder.

- **Draft:** "*Partial:* RE 4's 'no raise against a constant boss' (680 of 161,864 acceptances, 0.42%, untraced), A5, A8, B3, B4, B7."
  **Evidence:** In `runs/hooks-w2-verdicts.md`, A5, B3, and B7 have multi-clause verdicts where **a stated falsifier fired** on the failing clause:
  - A5: "sucker clause **held**; survival clause **failed, falsifier fired** as worded (the survival I defined was contract-origin)" (0.000 vs falsifier ≤ 0.25).
  - B3: "fair clause **held**; mechanism clauses **partial/failed** (... pooled execution under 10⁻², the falsifier's second clause fires)" (0.005 vs falsifier ≤ 10⁻²).
  - B7: "M clause **held**; (C) clause **failed, falsifier fired**" (ratio 0.17× in `union-C-role` vs falsifier ≤ 1.5).
  - B4's execution clause also failed by a wide margin (0.205 and 0.366 vs ≤ 0.05).
  **Correction:** Explicitly state in the Verdicts list that on A5 (contract survival 0.000), B3 (pooled execution 0.005), and B7 (`union-C-role` adoption ratio 0.17×), one clause held while the other failed with its falsifier firing, and that B4's low-execution clause failed (0.21 and 0.37 vs ≤ 0.05).

- **Draft:** "*Disclosures:* ..."
  **Evidence:** `notes/hooks-w2.md` §2.3 item 5 discloses a structural property of `union-C-role` omitted from the draft: "Role-scope fills are per slot (key = the holder's slot, Part W's role semantics); a fill copied between the two worker slots does not apply in the other slot (a Part W property)."
  **Correction:** Add to Disclosures or the union-game design that role-scope fills are keyed per worker slot, so fills copied across worker slots are inert.
