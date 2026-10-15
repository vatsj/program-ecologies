# Review of `specs/2026-10-14-core-existence-sweep.md` by gemini-4-argon

### 1. Design flaws or confounds

* **TU vs. NTU conflation in $v(S)$ and Bondareva–Shapley.** The brief defines $v(S)$ as a scalar ("S's leader value") and applies Bondareva–Shapley balancedness, which assumes transferable utility (side-payments). Yet blocking is defined via $x_S$ (a vector in NTU space), and the sweep restricts outcomes $x$ to physical action profiles without side-payments. Under asymmetric costs (Cournot, Bertrand), a coalition $S$ cannot freely transfer profits through quantities or prices alone, and the NTU blocking set $V(S)$ is not a half-space $\sum_{i\in S} u_i \ge v(S)$. 
  * *Fix:* Explicitly compute both the **NTU leader-value core** (no side-payments; $S$ blocks $x$ if there is $a_S$ such that every $i \in S$ strictly improves under $N \setminus S$'s credible response) and the **TU leader-value core** (with side-payments, via Bondareva–Shapley on $\max_{a_S} \sum_{i\in S} u_i$). Keep them strictly separate in the table and predictions.
* **Non-uniqueness of the complement's credible response.** When $|N \setminus S| \ge 2$ (e.g., $n=4, |S|=1$ or $2$), the subgame among $N \setminus S$ after $S$ commits can have multiple Nash equilibria (especially in supermodular games or capacity-constrained Cournot). "The" credible best response is ill-defined.
  * *Fix:* Specify the selection rule for $N \setminus S$'s equilibrium in the spec before running: pessimistic (minimax over $N \setminus S$'s NE, matching $\text{val}(S)$), optimistic, or Pareto-best for $N \setminus S$.
* **Grid-discretization artifacts in continuous NTU games.** Evaluating continuous Cournot, Bertrand, and Cobb–Douglas allocation games on coarse grids will re-introduce the exact indivisibility artifacts the brief aims to eliminate (creating phantom first-mover advantages or hiding small blocking deviations).
  * *Fix:* Use closed-form analytical reactions for quadratic Cournot/Bertrand and exact KKT/root-finding (`scipy.optimize`) for concave public goods and CES/Cobb–Douglas, reserving grids only for verification.

### 2. Predictions that are wrong

* **Prediction 3 (Concave public goods: nonempty).** *Why it is wrong:* Voluntary contribution to a concave public good has strategic substitutes in contributions (as the brief itself notes). A coalition $S$ leading by free-riding ($g_S = 0$) forces the complement $N \setminus S$ to move down its reaction curve and increase contributions $g_{N\setminus S}$, giving $S$ a strict first-mover advantage. In symmetric 3-player concave public goods, the sum of singletons' leader payoffs when free-riding typically exceeds the grand coalition's optimal total payoff, making the TU (and symmetric NTU) core **empty**. (Even Chander–Tulkens's $\gamma$-core requires convexity/superadditivity conditions that fail when free-riding extracts large complement responses). *My prediction:* Empty in a large share of the concave public goods parameter grid (and thus consistent with Prediction 6, whereas Prediction 3 contradicts Prediction 6).
* **Prediction 1 (Cournot $n \ge 3$: empty at *every* cost profile).** *Why it is wrong:* Under strongly asymmetric costs (or tight capacity limits), high-cost firms are near-inactive or capped, collapsing the effective game to $n \le 2$ or limiting $S$'s ability to over-produce profitably. *My prediction:* Nonempty in the corners of the asymmetric-cost and capacity-constrained grids (especially for the NTU core without side-payments).

### 3. Missing controls or cheap additions

* **Compare against the standard $\gamma$-core (simultaneous Nash among $N \setminus S$ vs. sequential leader-follower).**Wait—in a two-stage move where $S$ commits as a bloc and $N \setminus S$ responds simultaneously, the credible response of $N \setminus S$ *is* the $\gamma$-core reaction if $S$ has no post-response move. If $v(S)$ is identical to the Chander–Tulkens $\gamma$-characteristic function, state that identity explicitly and benchmark against known $\gamma$-core existence theorems (e.g., Helm 2001).

### 4. Alternative explanations

* **Failure of balancedness from coalition-size returns, not FMA.** In symmetric games where coalitions of size $k$ act as a single merged player (Cournot mergers), the core can be empty or nonempty due to the curvature of the payoff function in $k$ (the Salant–Switzer–Reynolds merger paradox) rather than sequential first-mover advantage. Separating simultaneous-partition payoffs from sequential-leader payoffs immediately rules this out.

### 5. Ideas that matter for the research program

* Nothing material.
