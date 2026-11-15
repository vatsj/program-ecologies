# Review of `notes/follower-core-RESULTS-draft.md` by gemini-4-carbon

1. **Draft sentence:** `"In public goods, linear-quadratic games and differentiated Bertrand it is empty at 0.67–0.71 of the points with a leader core (0.58 for linear-quadratic)."`
   - **Evidence:** Among points with a leader core, the follower core is empty at `224 / 332 = 0.67` in differentiated Bertrand, `1,224 / 1,735 = 0.71` in public goods, and `889 / 1,545 = 0.58` in linear-quadratic games. Listing linear-quadratic inside `0.67–0.71` contradicts the parenthetical.
   - **Correction:** Change the range to `0.58–0.71`, or write `"In differentiated Bertrand and public goods it is empty at 0.67 and 0.71 of the points with a leader core, and at 0.58 in linear-quadratic games."`

2. **Draft sentence:** `"F4: the share clause is false (mixed-sign points are 0.56 of all, not < 0.2); the rate clause holds (0.73 empty against 0.001)."`
   - **Evidence:** Prediction F4 does not condition on leader-core existence (`"Points with mixed-sign FMA ... are < 20% of all points, and the intersection is empty at a higher rate there than elsewhere"`). Across all points, the joint core is empty at `2,851 / 3,850 = 0.74` on mixed-sign points vs `132 / 2,991 = 0.044` elsewhere. The draft's `0.73` (`2,740 / 3,739`) vs `0.001` (`2 / 2,861 = 0.0007`) conditions on a leader core existing.
   - **Correction:** Report the unconditional rates (`0.74 empty against 0.044`), or state explicitly that `0.73 against 0.001` is conditioned on points with a leader core.

3. **Draft sentence:** `"F1 falsified: plain Cournot keeps the leader verdict at 0.98, but Cournot with capacities at 0.63 and public goods at 0.20."`
   - **Evidence:** Prediction F1 states `"both = leader core in verdict"` and `src/follower_core.py` stores `tu_core`'s three-way `'verdict'` (`empty`, `nonempty`, `tight`). Exact verdict agreement (`both == leader`) is `201 / 332 = 0.61` in `cournot_cap` and `310 / 1,820 = 0.17` in `pg`, because 9 `cournot_cap` points and 52 `pg` points narrow from `nonempty` to `tight`. The draft's `0.63` (`210 / 332`) and `0.20` (`362 / 1,820`) collapse `nonempty` and `tight` into binary existence. (F1 is falsified either way.)
   - **Correction:** Specify `"keeps the leader existence verdict"` or report the exact three-way verdict rates (`0.61` and `0.17`).

4. **Draft sentence:** `"F2 holds (follower empty at 224 of 332 differentiated-Bertrand points and 889 of 1,545 linear-quadratic points with a leader core)."`
   - **Evidence:** Prediction F2 restricts LQ to `"LQ points with FMA < 0 somewhere"` where the leader core is nonempty. Excluding the 11 `"lead"` and 5 `"none"` LQ points with a leader core gives `889 of 1,529` (`0.581`), not `1,545`. (F2 holds either way.)
   - **Correction:** Replace `889 of 1,545 linear-quadratic points with a leader core` with `889 of 1,529 linear-quadratic points with FMA < 0 somewhere and a nonempty leader core`.

5. **Draft sentence:** `"(2,859 of 2,861; the two exceptions are panel points where every coalition prefers following)"`
   - **Evidence:** In `src/follower_core.py`, `sign == "follow"` means `FMA <= TOL * sc` for every proper coalition and `FMA < -TOL * sc` for at least one—some coalitions may have `FMA = 0` rather than strictly preferring to follow.
   - **Correction:** Change `"where every coalition prefers following"` to `"where no coalition gains by leading (and at least one gains by following)"`.
