# Review of `notes/pair-worth-n-results-draft.md` by gemini-4-argon

1. **Draft:** "Three of them, (3, 3, 0), (4, 2, 0) and (2, 0, 4), never occur."
**Evidence:** In `runs/pair_worth_n/coverage.json` (`pooled["1.0"]["by_point"]`), four core points have count 0: `(0, 4, 2): 0`, `(2, 0, 4): 0`, `(3, 3, 0): 0`, and `(4, 2, 0): 0`.
**Correction:** Change to "Four of them, (0, 4, 2), (2, 0, 4), (3, 3, 0) and (4, 2, 0), never occur."

2. **Draft:** "The equal split dominates (0.37–0.72 of core islands at N ≥ 400)."
**Evidence:** In `runs/pair_worth_n/coverage.json`, the equal-split share (`eq_split_share`) at $N \ge 400$ ($mN = 1$) is below 0.37 in multiple arms: at $N = 400$, C is 0.30, C+B is 0.27, $\text{C+B}^*_4$ is 0.27, $\text{C+B}^*$ ($\delta = 0.0125$) is 0.30, $\text{C+B}^*$ ($\delta = 0.15$) is 0.34, and $\text{C+B}^*$ ($\delta = 0.5$) is 0.22; at $N = 800$, C is 0.16 and C+G is 0.23. (The 0.37–0.72 range holds only across the four $\delta = 0.05$ cells C+B\*, C+F, C+G at $N = 400$ and C+B\* at $N = 800$.)
**Correction:** Change the overall $N \ge 400$, $\delta = 0.05$ range to "0.16–0.72 of core islands at N ≥ 400 (0.27–0.72 in the δ = 0.05 reader and grand-constant arms at N = 400, and 0.23–0.72 at N = 800)."

3. **Draft:** "Consensus at N ≥ 400 is 0.03–0.28."
**Evidence:** In `runs/pair-worth-n.md` ("End class shares, delta = 0.05, Lambda = 10, mN = 1"), consensus at $N = 800$ is 0.00 for both C and C+G (and 0.10 for C+B\*). The 0.03–0.28 range applies only to $N = 400$.
**Correction:** Change to "Consensus at N ≥ 400 is 0.00–0.28 (0.03–0.28 at N = 400, 0.00–0.10 at N = 800)."
