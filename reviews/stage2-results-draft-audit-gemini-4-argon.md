# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/stage2-results-draft.md` by gemini-4-argon

**1. Conflation of fixed-`TX` threat mean with overall P threat mean.**
- *Draft:* "The threat is untested from then on, and its level freezes where the scramble left it: a mean of 13.3, against a prior mean of 10.25 (shift +2.61; prediction 2 claimed at least 3)."
- *Evidence:* In `runs/core-stage2.md` §2 and `table_cells.csv` (`p_threshold_no-overbid_zero_m50`), the overall end mean threat across all P programs is 12.86 (which gives the +2.61 shift against the 10.25 prior mean: $12.86 - 10.25 = 2.61$). The 13.28 (13.3) figure is the mean $t$ among fixed `TX(t)` islands only (74% of islands).
- *Correction:* State that the overall mean threat is 12.86 (shift +2.61 against the 10.25 prior, 13.3 on islands where `TX` fixed).

**2. Omission of intermediate $t=17$ value in a claimed step-function sequence.**
- *Draft:* "With followers fixed, the core is reached only when the frozen threat is high: 0.000 for every t ≤ 16, then 0.42 at t = 18, 0.986 at 19 and 1.000 at 20."
- *Evidence:* `runs/core-stage2.md` §2 reports: "0.000 for every t ≤ 16, 0.034 at t = 17, 0.42 at t = 18, 0.986 at t = 19, 1.000 at t = 20".
- *Correction:* Insert "0.034 at t = 17," before "0.42 at t = 18".

**3. Inverted metric convention (reporting `core_enc` as `core` without brackets) in the follower-mass sweep.**
- *Draft:* "Core is the island-mean fraction, with the encounter-level fraction (the spec's primary) in brackets where it differs. ... Post-hoc follower-mass sweep at ε = 0: core 0.605, 0.559, 0.487, 0.395 and 0.251 at item follower mass 0.01, 0.02, 0.05, 0.10 and 0.20."
- *Evidence:* In `table_cells.csv` (`x_fol*_zero`), 0.605, 0.559, 0.487, 0.395, and 0.251 are the encounter-level fractions (`core_enc`). The island-mean fractions (`core`) are 0.576, 0.532, 0.471, 0.383, and 0.247, which differ by up to 0.029.
- *Correction:* Follow the stated convention: "core 0.576 (0.605), 0.532 (0.559), 0.471 (0.487), 0.383 (0.395) and 0.247 (0.251)".

**4. Omitted bracketed `core_enc` values where they differ from island-mean `core` under rain.**
- *Draft:* "Follower-only rain gave 0.086, safe-follower rain 0.102, P-only rain 0.098 and item-only rain 0.064."
- *Evidence:* In `table_cells.csv` (`iv_threshold_m50`, `ivb_threshold_m50`, `ivp_P_threshold_m50`, `ivp_items_threshold_m50`), `core_enc` differs from `core` in all four cells: 0.105, 0.117, 0.117, and 0.068.
- *Correction:* Add the bracketed encounter-level fractions: "0.086 (0.105), safe-follower rain 0.102 (0.117), P-only rain 0.098 (0.117) and item-only rain 0.064 (0.068)".
