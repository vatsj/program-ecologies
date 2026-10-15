# Review of `specs/2026-10-14-farsighted-refusal.md` by gemini-4-argon

1. **Design flaws or confounds**
- **Discontinuous value iteration in `gKR(δ)`:** Because the acceptance rule is a step function ($\mathbb{I}[W_i(x) > W_i(y)]$), the Bellman operator on $W$ is discontinuous, so pure strategy fixed points need not exist and standard value iteration will often cycle.
  *Fix:* Specify cycle detection in the static solver; if pure fixed points fail to exist or converge, allow mixed acceptance probabilities at indifference ($W_i(x) = W_i(y)$) or smoothed best responses ($\sigma(\beta(W_i(x) - W_i(y)))$) to find the Markov equilibrium.
- **Ambiguous fixed-point selection in `gKR-read(δ)`:** If `gKR-read` reads another `gKR-read` or `gKR` program, how does it compute the transition matrix? If it merely plugs the island's empirical guard frequencies into a one-shot Bellman solve assuming non-`g0`/`gV` programs use the default `gKR` table, that is just a plug-in policy evaluation, not mutual source-reading. If `gKR-read` copies recursively compute `W`, they face a mutual-simulation regress.
  *Fix:* Explicitly state that `gKR-read` treats all `gKR` and `gKR-read` copies as playing the pre-computed default `gKR` strategy when tallying slot consent probabilities, solving the 20-state linear system $(I - \delta P(\text{freq}))^{-1} r$ for $W$.
- **Payoff vs. play in $W_i$:** On islands, programs play actions, and contracts overwrite actions. In the static 20-state abstraction, $W$ is computed over *outcomes*. On the island, if the population is not yet at a consensus outcome, what is the status quo $y$ in $W_i(x) > W_i(y)$?
  *Fix:* Specify whether $y$ is the island's current modal outcome, mean payoff, or the drawn consenting individual's realized payoff.

2. **Predictions you think are wrong**
- **Prediction 7 (`gKR-read` rises against `gKR` in M-read at $mN = 1$):** Wrong. In a polymorphic island containing *only* `gKR` and `gKR-read` (cell `M-read`), every individual's base behavior is identical (both equal `gKR` on monomorphic islands, and by induction, an island of only `gKR` and `gKR-read` has 100% `gKR` consent probabilities). Thus `gKR-read` and `gKR` make bit-identical consent decisions at every state in `M-read`. Selection between them is strictly neutral (drift).
  *My prediction:* `gKR-read` and `gKR` drift neutrally (50/50 split of runs) in `M-read`. To see `gKR-read` diverge from `gKR`, the cell must include `g0` (i.e., a three-way `gKR-read` vs `gKR` vs `g0` cell).

3. **Missing controls or cheap additions**
- **Add `C3-read` (`gKR-read`, `gKR`, `g0` at $\frac{1}{3}$ each, $mN=1$):** As noted in (2), `M-read` is dynamically vacuous because without `g0` on the island, the empirical transition matrix equals the theoretical `gKR` matrix. `C3-read` is the actual test of whether reading the presence of myopic acceptors (`g0`) and adjusting continuation values outperforms the rigid fixed-point assumption.
- **Static check of the "below $x_i$" variant of `g1` on islands:** If the static check shows the "below $x_i$" variant of `g1` does *not* freeze dominated states (allowing entry into pairs before freezing), add a cheap cell `U-g1-x` at $mN=0$.

4. **Alternative explanations the brief does not rule out**
- **Generalized caution vs. exact $V^*$ targeting:** In `M-gKR`, `gKR` may spread against `g0` under migration simply because *any* guard that lowers the exit rate from pair outcomes reduces destructive churn (the generator's walk), not because `gKR` specifically isolates $V^*$.
  *Fix:* Add a control cell `M-g1` (`g1` vs `g0` at $mN=1$) or compare `M-gKR` against a fixed point of `gKR` whose absorbing set is an unequal held-player pair. If an unequal-absorbing `gKR` spreads against `g0` just as fast as the $V^*$-absorbing `gKR`, selection is rewarding stability, not $V^*$ geometry.

5. **Ideas that matter for the research program**
- Nothing material.
