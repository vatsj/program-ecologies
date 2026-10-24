# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/results_mw.md` by gpt-6.1-sol

- **“The V\* version holds too”; “meets the target, the V\* version included, … for 20,000 generations.”** At N = 100, mN = 1, V\* success is 0.85 at 10,000 and 0.825 at 20,000 (§6), below the registered ≥0.9 criterion. Correct: the stated target qualifies at every tested rate; V\* does not. Two qualifying snapshots also do not establish continuous success throughout the horizon.

- **“Larger islands stretch both timescales … still with no V\* islands.”** N = 200 clears waste *faster*: medians 4,499/1,764/674/390 versus 8,432/2,685/1,394/746. Fair islands are abundant; zero refers to runs meeting the all-islands V\* target. Correct both descriptions.

- **“Waste clears in about 270/mN … both times scale roughly as 1/mN”; “lowering migration only slows the same … sequence.”** Clearance median × mN rises from 253 to 746; slope −0.683 misses the registered range. Coverage-loss × mN falls 38%; coincident rescaled trajectories are not demonstrated. Replace the universal trajectory claim with approximate, measure-dependent scaling over uncensored rates.

- **“Coverage is lost mostly by member-to-member flips (2:1 to 5:1 … at mN ≥ 0.03).”** P2’s ratios are 1.83, 2.00, 4.85 and **14.14**. These are all 50-generation-grid transitions, not transitions specifically causing coverage loss. Correct the range and describe transition counts, not an established loss mechanism.

- **“gemini-4-argon’s … counter-prediction on 4 held.”** Its frozen scoring rule requires guard superiority through mN ≤0.03; at 0.03 the difference is −0.025. Correct: mixed/not held under that rule, although the looser verbal prediction largely matches. Its interval [−0.175, 0.15] also warrants distinguishing point-estimate reversal from clear evidence.

- **“Components do not rescue the unguarded lottery.”** This omits strong improvements: N = 200, mN = 0.1, C = 4 reaches 0.90/0.80 at 10k/20k; C = 8 reaches 0.80/1.00. Correct: none qualifies at both snapshots, but components substantially improve stated-target success. Report the contrasting V\* failures.

- **“The target is a property of the guard, not … migration rate.”** Balanced-start baseline controls reach 0.60 at 10k (mN = 0.1) and 0.70 at 20k (0.01). Qualify the conclusion to the tested lottery founders; initialization matters.

- **“Components are independent sub-archipelagos.”** The disclosed implementation also replaces a shared multinomial birth allocation with fixed per-component clocks (notes §1.4). Add this model-level deviation; nesting alone does not disclose it.

- **“0.005 at mN ≤0.03.”** The 0.03 value is 0.006. **“The remaining gap is … immigrant rejection.”** No immigrant-rejection intervention was tested; label this a proposed next hypothesis, not a demonstrated necessary or sufficient remedy.
