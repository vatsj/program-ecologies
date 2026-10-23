# Review of `specs/2026-10-23-rps-mixed.md` by gpt-6.1-sol

## 1. Errors, contradictions, unsound mechanisms

- **`br` is no longer a best response.** “`br A`: the exact best response to the distribution of A’s action” conflicts with “`br A` forfeits with probability p_f.” Against certain forfeit, every ordinary action earns +1; propagated forfeit earns 0. **Fix:** rename this a failure-propagating conditional-response operator; separately test genuine best response, which always returns an ordinary action. The amendment deliberately removes a profitable escape from mutual nontermination.

- **The shadow amendment is false.** “`X` is … a neutral shadow of every guarded mixer.” Against constant R, `coin X (next(THEM(ME)))` earns +½, while `X` earns 0, assuming sufficient depth. Their payoff rows differ. **Fix:** distinguish neutrality within a particular resident support from global behavioural equivalence; demonstrate neutrality pairwise rather than asserting it universally.

- **Cap checks cannot establish cap independence.** “D = 11 and D = 13 on the same pairs, so that no payoff depends on the cap’s parity or residue mod 3.” Sampling detects dependence; it does not eliminate it. Moreover, a recursive simulation evaluates the opponent with less remaining depth than its actual root evaluation. **Fix:** specify depth accounting and compare the inferred opponent distribution with its actual distribution. Call `br` exact only about its bounded subevaluation.

## 2. Design flaws or confounds

- **The target statistic conflates two games.** Program exploitability permits opponent-conditioned responses; ordinary RPS exploitability permits a fixed action against a mixture. A uniform population of constants has zero ordinary exploitability but positive reader exploitability. **Fix:** report both, plus each resident’s unilateral program-deviation regret. Define “in-population exploitability” precisely: its parenthesis currently sounds identical to the unrestricted statistic.

- **No large-population lottery inference is possible from N = 100 alone.** The primary object has one geometry and one horizon. **Fix:** add at least one larger N and longer-horizon continuation, or explicitly limit conclusions to finite-population establishment.

- **The matched control matches syntax, not necessarily the implemented prior.** Stripping, deduplication and payoff-row lumping can collapse duplicate `next` constructors differently from `br`. **Fix:** preserve and audit aggregated spelling mass, founder frequencies and twin handling after every reduction.

## 3. Predictions likely wrong

- **Prediction 2:** symmetry guarantees ensemble symmetry under a symmetric sampling law, not uniform action frequencies on each finite trajectory or in every recurrent component. Nonergodic lotteries can break symmetry. Expect substantial island/run asymmetry, with pooled symmetry only within uncertainty. Test relabeling equivariance separately from ecological uniformity.

- **Predictions 4–5:** exact readers need not select individual mixing more strongly. `X` already supplies minimax protection in both stochastic arms, and readers pay recursive-forfeit exposure. Expect substantial mixing in both, with no robust sign for exact minus matched until truncation effects are controlled.

## 4. Missing controls or cheap additions

- Add the constants-only RPS benchmark and a constants-plus-`X` benchmark.
- Exhaustively depth-sweep named classes and all high-mass residents, not merely 1,000 sampled pairs.
- Report confidence intervals clustered by run, not by migrating island.
- In zero-sum RPS every feasible payoff pair is Pareto-efficient; state explicitly that this experiment tests equilibrium/unexploitable play, not Pareto selection.

## 5. Alternative explanations not ruled out

Apparent recovery could reflect cheap `X` founder abundance, selective extinction of capped readers, or pooling symmetry across incompatible islands—not selection for exact source reading. The uniform-default cell additionally builds uniform mixing into the evaluator itself.
