# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/results_mw.md` by gemini-4-argon

- **Draft:** "Larger islands stretch both timescales: at N = 200 the best share is 0.70 (mN = 0.1), still with no V\* islands."
  - **Evidence:** In `runs/migration-window.md` §2 (baseline, N = 200), the Kaplan–Meier waste-cleared medians are 4,499 / 1,764 / 674 / 390 at mN = 0.03 / 0.1 / 0.3 / 1, which are *shorter* than the N = 100 medians (8,432 / 2,685 / 1,394 / 746). Only coverage-lost medians are stretched (e.g., >20,000 / 7,340 / 1,663 at N = 200 vs. 11,063 / 3,213 / 685 at N = 100). Also, `F/U/G/W/D @10k` at N = 200, mN = 0.1 is `0.59/0.40/0.00/0.00/0.00` (59% of islands are on fair pairs, V\*); it is `V*@10k` (the share of *runs* meeting the V\* target) that is 0.00.
  - **Correction:** Change to: "Larger islands shorten waste clearance and stretch coverage loss: at N = 200 the best share is 0.70 (mN = 0.1), still with 0 runs meeting the V\* target."

- **Draft:** "Coverage is lost mostly by member-to-member flips (2:1 to 5:1 over member-to-unequal at mN ≥ 0.03)."
  - **Evidence:** In `runs/migration-window.md` §3 (P2 `transitions_from_member`), at mN = 1, `Fk_to_Fj` is 12,963 and `F_to_U` is 917, a ratio of 14.1:1. (At mN = 0.03, 0.1, 0.3 the ratios are 1.8:1, 2.0:1, and 4.8:1.)
  - **Correction:** Change "2:1 to 5:1" to "1.8:1 to 14:1" (or specify "at mN ∈ {0.03, 0.1, 0.3}, and 14:1 at mN = 1").

- **Draft:** "Its coverage-lost median is about 18,300 / 5,800 / 2,200 / 500 generations at mN = 0.01 / 0.03 / 0.1 / 1, roughly 1/mN..."
  - **Evidence:** `runs/migration-window.md` §2 (U-gKR(0.99), N = 100) also reports an uncensored KM coverage-lost median of 957 at mN = 0.3, which is omitted from the sequence.
  - **Correction:** Include mN = 0.3: "...about 18,300 / 5,800 / 2,200 / 960 / 500 generations at mN = 0.01 / 0.03 / 0.1 / 0.3 / 1..."

- **Draft:** "gemini-4-argon's counter-prediction on 2 held on the ratio but not on its mechanism; its counter-prediction on 4 held."
  - **Evidence:** Under the pre-registered scoring rule in `predictions/2026-10-24-migration-window.md`, Gemini's counter-prediction on 4 is scored as: "guard share ≤ baseline share at mN ∈ {0.1, 0.3}, guard above the baseline at mN ≤ 0.03." At mN = 0.03, the guard share is 0.175 and the baseline share is 0.200 (`diff_at_0_03: -0.025` in P4 JSON), so the guard is *below* the baseline at mN = 0.03 (holding only at mN ≤ 0.01).
  - **Correction:** State that Gemini's counter-prediction on 4 held at mN ∈ {0.1, 0.3} and mN ≤ 0.01, but missed at mN = 0.03 (where the guard is slightly below baseline, 0.175 vs. 0.20).

- **Draft:** "Components do not rescue the unguarded lottery."
  - **Evidence:** In `runs/migration-window.md` §4 & §6, `C16-base-N200-m0.1/C4` (64 islands in 4 components of 16) achieves `ts@10k = 0.90` and `ts@20k = 0.80`, and `C8` achieves `0.80` at 10k and `1.00` at 20k—listed as near misses to the RS's ≥0.9 target at both snapshots, and substantially above the single-component baseline at mN = 0.1, N = 200 (0.70 at 10k, 0.50 at 20k). The draft omits the mN = 0.1 component panel entirely.
  - **Correction:** Qualify "at mN = 1" or note that at mN = 0.1, N = 200, C = 4 and C = 8 reach 0.90 / 0.80 and 0.80 / 1.00 at 10k / 20k (near misses to the RS target, still with 0 on the V\* target).
