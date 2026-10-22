# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/prud-results-draft.md` by gemini-4-argon

- **Draft sentence:** "Realized exposure was within 2% of the schedule (6,658 and 19,954 arrivals against 6,656 and 19,968)."
  - **Evidence:** `runs/prudence-verdicts.md` (S7) and `runs/prudence.md` (Delivered exposure, 0–39): maximum deviation is 1.91% on replicates 0–19, but reaches 3.25% on the 40-run extension (6,872 against 6,656 at A52).
  - **Correction:** Specify "within 2% on the 20 main runs [3.25% on 40]" (or state that the 6,658 and 19,954 means are for replicates 0–19 [6,666 and 19,966 on 40]).

- **Draft sentence:** "Prediction 1 (G rises by at least 0.1 at A52 in L) failed, with its falsifier."
  - **Evidence:** `predictions/2026-10-21-prudence-world-k.md` (Scoring conventions) and `runs/prudence-verdicts.md` (RE 1): Prediction 1 ("PrudentBot's share") is scored primarily on (a) the frozen target network T (which fell by −0.153 in L and −0.101 in K) and (b) PrudentBot's own tree (−0.011 in L, −0.020 in K), with G (prudent target) added by the subagent as (c). Furthermore, in K, G rose by +0.012 [+0.025], so the falsifier ("no rise in either world") only fired unconditionally on T and PB's own tree, not on G.
  - **Correction:** State that Prediction 1 failed on all three measures—the primary target network T (−0.153 in L, −0.101 in K), PrudentBot's own tree (−0.011, −0.020), and G—with its falsifier firing on T and PB's own tree.

- **Draft sentence:** "Standing certified suckers average only 0.014–0.044 of the population in the arrival arms. Where prudent and unguarded target members are both present, the prudent ones do not out-earn the unguarded (−0.01 to −0.04 in every arm, A0 included)."
  - **Evidence:** `runs/prudence.md` (Deviations v, Reading of the post-hoc table): Both of these metrics come from the post-hoc script `src/prudence_extra.py` (`runs/prudence-extra.json`), and the 0.014–0.044 range is across the 40-run cells (and omits SD52's 0.010; on the 20-run main table, residence over the 10,000-generation tail is 0.003–0.059 of the population, or 0.017–0.059 excluding SD52).
  - **Correction:** Label these figures as post-hoc (on 40 runs), and include SD52 (0.010–0.044) or specify non-depleted arrival arms.

- **Draft sentence:** "Only 0.02–0.09 of the tail-end prudent share descends from arrivals: the gain comes from residents (prediction S6 failed)."
  - **Evidence:** `runs/prudence-verdicts.md` (S6) and `runs/prudence.md` (Ancestry tables): 0.02–0.09 (specifically 0.000–0.087 across all arrival arms, 0.022–0.087 in A52/A156) is the 40-run extension range. On the 20 scored runs, the arrival-descended fraction is 0.00–0.13 (0.04 in L A52, 0.00 in L A156, 0.07 in K A52, 0.13 in K A156).
  - **Correction:** Report the 20-run scored values with 40-run values in brackets: "0.00–0.13 [0.02–0.09]".

- **Draft sentence:** "Off-target FairBot residence rises with the tail in K (16 of 20 pairs, p = 0.012); prediction 2 failed."
  - **Evidence:** `runs/prudence-verdicts.md` (RE 2): Off-target residence also rose in L on the sign test (17 of 20 pairs up, p = 0.003 [33 of 40, p < 0.001]; mean +0.245 [−0.001]).
  - **Correction:** Mention L alongside K (e.g., "rises at A52 over A0 in 16 of 20 pairs in K, p = 0.012, and 17 of 20 in L, p = 0.003").
