# Review of `notes/ev-monotonicity-RESULTS-draft.md` by gemini-4-argon

1. **Unrecorded mean-field and composition claims in the `runs/ev-monotonicity.md` summary:**
   - *Draft:* "F0 holds 0.97 of islands by 5·10³ events... before F0 returns by ~5·10⁴. At 10⁴ events the top triples of the unequal state (pool 0) are a bully in slot 0 against an accommodating constant in slot 2, (⅔, 0, ⅓)."
   - *Draft:* "b = 1/24: the mean-field limit depends on the founding pool, one pool ends on a fair pair (F1, not F0) and two on unequal pairs (pool-mean V\* ⅓ at convergence)..."
   - *Evidence:* `runs/ev-monotonicity.md` does not record the 5·10³ or 5·10⁴ mean-field checkpoints, the pool-0 top triple composition at 10⁴ events, or which specific pair (F1 vs F0) won in pool 0 under b = 1/24 (the table shows `F0 = 0.333333` and `F1 = 0.000000` at `end`, which contradicts "F1, not F0" unless the table columns in `runs/ev-monotonicity.md` are mislabeled or symmetrized).
   - *Correction:* Verify against `runs/ev-monotonicity.json` why the markdown table reports `F0 = 0.333333, F1 = 0.000000` at convergence for b = 1/24 while the text says "F1, not F0", and either correct the text ("F0" instead of "F1, not F0") or fix `runs/ev-monotonicity.md` and add the missing checkpoints/triple details to the markdown run report.

2. **Overstatement in Reading ("every b tested down to 1/12"):**
   - *Draft:* "...a bonus on one pair selects it in the mean field at every b tested down to 1/12..."
   - *Evidence:* b = 1/24 was also tested (exploratory) and did not select the bonused pair across all pools. Phrasing as "every b tested down to 1/12" is true by truncation, but easily misread alongside the b = 1/24 failure.
   - *Correction:* State explicitly "at b ∈ {1/12, 1/8, 1/6} (failing at 1/24)".
