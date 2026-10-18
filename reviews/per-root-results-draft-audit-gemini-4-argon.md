# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/per-root-results-draft.md` by gemini-4-argon

1. **S5 verdict vs. scoring conventions**
- *Draft:* `S1, S5, S6, S8, S12, S14, D1, D2 held` (Verdicts table).
- *Evidence:* `predictions/2026-10-16-per-root-production.md` states: "a paired contrast whose bootstrap interval spans both the predicted effect and zero is inconclusive" and S5 predicts "R0 + alternatives ≤ 0.05 on both stream sets, and the interaction (R2 − R1) − (R0+alt − R0) > 0." In `runs/per-root.md`, `R0alt_i|dev` is `0.053` (> 0.05), and the interaction 95% CIs are `[-0.15, 0.32]` (dev) and `[-0.10, 0.50]` (conf), both spanning zero.
- *Correction:* Score S5 as **inconclusive** (the confirmation point estimate held, but the dev level was 0.053 and the interaction CIs span zero).

2. **RE 1 verdict on the full confirmation set (streams 20–59)**
- *Draft:* `RE 1 | R2 within 0.1 of H-full on the paired streams, zero wage ≤ 0.05 | held (0.402 vs 0.398 on 20–39; zero wage 0)` (Verdicts table).
- *Evidence:* `predictions/2026-10-16-per-root-production.md` defines `"confirmation" = streams 20–59 (stored H-full 0.299)` and states for RE 1: "supported iff |R2 − H-full| ≤ 0.1 and R2 zero wage ≤ 0.05 on the confirmation streams... inconclusive otherwise". On streams 20–59, `R2_i` is 0.426 and `Hfull_i` is 0.299, so `|R2 − H-full| = 0.127 > 0.10` (`runs/per-root.md`, `runs/per_root/verdicts.md`).
- *Correction:* Note in the RE 1 outcome that it **held on 20–39** (`Δ +0.004`), while on the full 20–59 confirmation set R2 exceeded H-full by `+0.127` (0.426 vs 0.299, outside the ±0.1 band in the positive direction).

3. **20,000-generation extension claim**
- *Draft:* `and states at 20,000 equal those at 10,000.` (Mechanism, bullet 4).
- *Evidence:* `runs/per-root.md` (`Extensions to 20,000`) shows `R2_i_ext20k: {3: (1.0, 1.0), 5: (0.78, 0.8), 9: (1.0, 1.0), 14: (1.0, 1.0), 15: (1.0, 1.0)}` (only 5 streams run, and stream 5 changes from 0.78 to 0.80).
- *Correction:* Change to "and fair shares at 20,000 match those at 10,000 (within 0.02 on the 5 extended streams)."

4. **Fair-bosses extinction denominator in R0**
- *Draft:* `under R0 the count falls to 3–5 islands and 2–5 of 20 runs lose them.` (Mechanism, bullet 1).
- *Evidence:* `runs/per-root.md` (`Fair bosses`) reports `R0_i|dev: ... extinct by 200 in 2/5 runs`, `R0_i|conf: ... 2/20 runs`, `R0_3|dev: ... 5/20 runs` (while the predictions addendum notes `5/18` for R0 at 3·10⁶), `R0_6|dev: ... 2/20 runs`. Furthermore, `R0_i|dev` falls to `0.0` islands by generation 1,000, not 3–5.
- *Correction:* Specify "falls to 2.5–5.2 islands at generation 200 (0 by generation 1,000 in `R0_i` dev) and 2/5 (`R0_i` dev) or 2–5 of 20 runs lose them by generation 200."

5. **Whole-encounter step mismatches omitted in validation bullet**
- *Draft:* `Whole encounters executed by the term with R2 lists: plays 450/450 and productions 1,882/1,882 match, with 0 of 856 accepted checks unsound across appends and evictions.` (Validation and audit, bullet 3).
- *Evidence:* `runs/per_root/verdicts.md` (S12) notes that while plays match 450/450, exact step equality of plays failed on 8/450 encounters (median 1 step, from the parent's per-row-class approximation), and the cost model's median error is 0.22%.
- *Correction:* Add "(steps match on 442/450 plays, median diff 1 step; cost model median error 0.22%)" to the bullet.
