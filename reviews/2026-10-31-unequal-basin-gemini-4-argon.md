# Review of `specs/2026-10-31-unequal-basin.md` by gemini-4-argon

### 1. Design flaws or confounds

* **Behavioural lumping breaks under `P_fail = 0.1` in Arm L.** The spec merges $y, y'$ if they produce the same joint action code across the support. In the weak evaluator, a divergent root plays `(ALL, 2/3)`, which is also a valid constant action. At $P_{\text{fail}} = 0.1$, a program that returns `(ALL, 2/3)` by converging has a different payoff than one that diverges to `(ALL, 2/3)`, violating payoff equivalence within lumped classes.
  * *Fix:* Define lumping equivalence on `(joint_action_code, divergence_vector)` across all partner pairs in the support.
* **Lumping on raw pools breaks S₃ projection.** If you lump on the raw post-anneal pool before S₃-symmetrizing, the post-anneal supports of slots 0, 1, 2 may differ slightly by sampling noise, yielding non-isomorphic quotient spaces across slots and breaking S₃-equivariance (V6).
  * *Fix:* Take the S₃-union of the slot supports (or S₃-symmetrize the pool law) *before* computing the behavioural equivalence classes.
* **Sparse adaptive ODE (fallback 2) destroys the premise of Question 1.** Q1 asks whether the stored bistability was an artefact of Monte Carlo support collapse, relying on the exact ODE to keep every program at positive mass. If class counts exceed 80 and you fall back to $\theta$-pruning, you re-introduce support truncation (which the solver audit proved can manufacture or hide traps).
  * *Fix:* Do not use $\theta$-pruning. Even at $C \approx 300$ classes per slot, $C^3 = 2.7 \times 10^7$ floats is 216 MB. Vectorize the dense tensor contraction (or keep the full support and prune only the *Evaluation of the RHS* for donor pairs with $q_s(y) < 10^{-15}$, never zeroing out resident triple states $x$).

### 2. Predictions I think are wrong

* **Prediction 5 (Mechanism: the excluded slot).** You predict the decisive classes sit in the excluded slot and block rescue by refusing to offer $\frac{1}{2}$ to the low demander. I predict this is wrong (or secondary). In an unequal pair $(2/3, 1/3, 0)$, the excluded player gets $0$; refusing to form a $(1/2, 1/2)$ pair with the $1/3$-earner leaves the excluded slot at $0$, so an incoming constant offering $\frac{1}{2}$ to the $1/3$-earner will still invade the excluded slot whenever the $1/3$-earner is willing to switch. The binding obstruction must sit in the **pair slots**: specifically, a conditional low-demander (accommodator) that demands $\frac{1}{3}$ against a $\frac{2}{3}$-demander and *does not* switch to the excluded slot unless the excluded slot already demands $\frac{1}{2}$ directed at it, or a high-demander that punishes defection.

### 3. Missing controls or cheap additions

* **Pairwise synergy in data-driven attribution (Q2).** If the unequal basin is held by a complementary pair (e.g., an A1 bully in the high slot and an A1 accommodator in the low slot), removing one behaviour class at a time from the top 20 may show $\Delta u^* \approx 0$ if multiple classes play the partner role. Add a cheap check: remove the top *k* classes jointly ($k \in \{1, 2, 5, 10, 20\}$) to find the minimal knockout set, and test removing all top-20 classes sitting in *pair* roles vs *excluded* roles.
* **No-refounding control for syntactic ablations (Q2).** Syntactic ablations refound the pools (30 min/pool), confounding seed-scramble dynamics with migration-ODE dynamics. Also run the syntactic family ablations directly on the un-ablated post-anneal start law (zeroing the family and moving mass to constants, just like the data-driven attribution). It costs zero pool-building time and cleanly separates founding effects from ODE basin effects.

### 4. Alternative explanations not ruled out

* **Within-class tilt distortion.** The U-tilt rescales the whole U class to $u$ while keeping within-U frequencies from the post-anneal law. If conditional programs are heavily overrepresented inside U at $t=0$ relative to constants (because conditionals coordinate on unequal splits more easily during the founding scramble), tilting U to $0.6$ artificially inflates the marginal donor share $q_s$ of conditionals. The basin at $u^*$ might be an artefact of donor-marginal inflation rather than intrinsic stability of U triples.
  * *Check:* In the static analysis (Q3), verify whether the U endpoint is self-sustaining under its own marginals vs dependent on transient founder weights.

### 5. Ideas beyond this experiment

* Nothing material.
