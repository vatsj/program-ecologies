# Review of `specs/2026-10-25-encounter-contracts.md` by gemini-4-argon

1. **Errors, contradictions or unsound mechanisms**

* **Arm H hook-tag indexing:** The brief states: *"The weak `dollar3` grammar gains the leaf `HOOK(t, a₀)` (tag t ∈ {0, 1}, default a₀ one of the nine actions)... A contract is a set of fills, one per member, each written into a hook that member reaches in the genesis encounter, keyed by the situation as in R and carrying the proposed action"*, while earlier defining: *"An individual carries at most one fill per key"*. If a program reaches `HOOK(0, ...)` in one branch and `HOOK(1, ...)` in another, or reaches both, is the fill table indexed by `(t, p)` or just `p`? If indexed only by `p`, the tag `t ∈ {0, 1}` is vestigial. **Fix:** Specify that in arm H, fills are keyed by `(t, p)` (with at most one fill per `(t, p)` and the cap of 8 applying across all `(t, p)` entries), and if an evaluation reaches both `t=0` and `t=1` in the genesis encounter, specify which tag gets written (e.g., the last hook evaluated, which produces the stage-1 action).
* **Two-responder mutual simulation in Stage 2:** *"a responder re-runs its program with every simulation atom of a carrier replaced by that carrier's fill... and with non-carrier opponents simulated as in stage 1."* When $|S|=1$, there are two uncommitted responders. If responder $j$ simulates responder $k$, $j$ sees $k$'s *stage-1* action, even if $k$ also changes its action in stage 2 in response to $S$'s fill. This is well-defined (one ply of response to carriers only), but if $j$'s simulation of $k$ recursively runs $k$'s simulation of carrier $i$, does that nested simulation see $i$'s stage-1 action or $i$'s fill? **Fix:** Clarify whether the substitution of carrier $i$'s fill applies at all simulation depths or only depth-1 atoms (and confirm Replay tests check the $|S|=1$ two-responder case under this exact rule).
* **Spontaneous transitions in the rare-migration jump chain:** *"the rare-migration jump chain with islands relaxed to their attractors... any class change during holdouts is a spontaneous (genesis-driven) transition, counted and included in the dynamics explicitly"*. In the $m \to 0$ limit, inter-arrival times between migrants are infinite relative to within-island timescales. If an island has a positive spontaneous transition rate per generation, it transitions infinitely often between migrants, making a per-migrant jump chain ill-defined unless spontaneous transitions have absorbed before migrants arrive. **Fix:** Specify how spontaneous transitions enter the $I \to \infty$ pool ODE/jump chain (e.g., whether holdout transitions just trigger continued relaxation until a genuinely genesis-stable attractor is reached, or if the pool dynamics run at a fixed ratio of migrant rate to generation rate).

2. **Design flaws or confounds**

* **Single-migrant arrival in the jump chain:** Under rare migration, a single migrant enters one slot at frequency $1/N=0.01$. Before it fixes or dies by drift/selection (~10–100 generations), its encounter share is ~0.01, so at $\nu=0.1$ a genesis event involving that migrant occurs with probability $\approx 1 - (0.999)^T < 0.1$ before extinction. Thus $\alpha$ and $\kappa$ in arm R confound "contracts cannot form against migrants" with "$\nu=0.1$ rarely samples the migrant before drift eliminates it." **Fix:** The $\nu=1$ sensitivity is critical here; do *not* put $\nu=1$ second in the cut order, or ensure migrant-encounter genesis is measured conditionally.

3. **Predictions you think are wrong**

* **Prediction 4 ($\alpha > 0$ under R):** I side with the registered counter-prediction. A third-pair transition on a settled fair island (say $\{1,2\}$) requires slots 1 and 3 to coordinate on $\{1,3\}$. Even if a migrant triggers genesis for $S=\{1,3\}$, only the two specific individuals drawn acquire the fill. In subsequent encounters with the other $N-1$ residents of slot 1 or 3, the carrier plays the $\{1,3\}$ fill alone, gets 0 instead of 1/2 (for slot 1), and is selected against. **My prediction:** $\alpha$'s interval includes 0 under R, and is positive only under B (matched broadcasting).

4. **Missing controls or cheap additions**

* **Record $|\text{NE}|=0$ vs $|\text{NE}|>1$ in BR:** Log separately how often BR rejects a proposal because no pure NE exists among two responders versus because one of multiple pure NEs fails the Pareto test.

5. **Alternative explanations**

* Nothing material.
