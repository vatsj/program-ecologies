# Review of `specs/2026-10-24-zero-tolerance.md` by gemini-4-argon

**1. Design flaws or confounds**

* **Bounded-read exploiters still kill `zt(THEM(ME))`.** The Why section notes `cr(THEM(ME))` is eroded by *two* channels: light cheaters ($q < 1/4$) and bounded-read exploiters (inspectees that read the inspector, exhausting the recursion/step depth so `THEM(ME)` returns the un-inspected default, then cheat). `zt(THEM(ME))` changes the threshold from $q \ge 1/4$ to $q > 0$, which fixes light cheaters, but it uses the *exact same* bounded read `THEM(ME)`. Any bounded-read exploiter that returned $q=0$ to `cr` will return $q=0$ to `zt` and still strictly invade at $N \ge 10^4$. 
* **Confused rationale for `sr_k` and bounded reads.** The brief says `sr_k`'s read "cannot be gamed through the bounded-read path that `cr` exposes." Why? Each of the $k$ simulated draws of the inspectee against `ME` still requires evaluating the inspectee's source on `sr_k`. If the inspectee reads the inspector, this still hits the depth/step bound and triggers the default action on every draw. Furthermore, because `sr_k` is itself a stochastic program, you must specify whether an inspectee reading `sr_k` sees its exact mixed distribution or a single draw, and how the evaluator computes the expected payoff matrix for stochastic-vs-stochastic pairs without Monte Carlo noise creating false strict invasions at $N=10^5$.
* **Unmatched prior in `ZT+SR`.** If each added program gets the mass of `cr`, then `ZT+SR` (adding `zt` + three `sr_k`, or specify which `sr_k`) adds $2\times$ or $4\times$ the mass, confounding program mechanism with prior weight compared to the $1\times$ control. *Fix:* Split the added mass across the programs in `ZT+SR`, or add a $2\times$/$4\times$ `cr` control.
* **Charging `sr_k` at $c = 0.01$.** Charging `sr_16` 16 levels ($0.16$ payoff penalty) against compliant inspectees creates a massive entry barrier and an immediate strict-invasion ladder for unconditional `N` (shadow) or `cr` (which pays $0.01$ and gets the same on-path payoff against compliant inspectees). Specify whether `sr_k` uses short-circuit evaluation (stopping at the first draw that cheats, paying $<k$ levels on average against cheaters, though still $k$ levels on-path against compliant inspectees).

**2. Predictions I think are wrong**

* **Prediction 1 ($\pi(E) \ge 0.3$ in ZT at $N=10^5$) is likely wrong.** Because `zt` does not close the bounded-read exploiter exit, and at $N=10^5$ any remaining strict exit ($O(1)$ fixation vs $O(1/N)$ drift) dominates the stationary distribution, bounded-read exploiters will still drain $R$. I predict the light-cheater exit hazard drops $>10\times$, but the bounded-read exit absorbs the flow and $\pi(E)$ stays below $0.10$ (falsifying Pred 1) unless bounded-read exploiters were a negligible fraction of the $0.3\%$ compared to light cheaters.
* **Prediction 2's reasoning is flawed.** In the $\varepsilon \to 0$ chain, the cost `zt` pays against light cheaters *on the invasion path* does not directly lower $\pi(E)$ once light cheaters are blocked from fixing (their fixation probability becomes exponentially small in $N$). $\pi(E)$ stays below $0.811$ because of the *unclosed bounded-read exit*, not because of transient payoffs against failed invaders.

**3. Missing controls or cheap additions**

* **Partial ablation references.** From the existing `inspection_shadow` data (zero new compute), compute the chain with *only* light cheaters removed, and *only* bounded-read exploiters removed. This immediately tells you the ceiling for a mechanism that only fixes light cheaters (`zt`).
* **Define $R$ per arm.** Explicitly state that the $R$ (responsive inspector) set in the exit decomposition is expanded to include `zt` and `sr_k` in their respective arms.

**4. Alternative explanations**

* If `ZT+SR` outperforms `ZT` and `SR` alone, it could be simply because `zt` and `sr_k` act as mutual reinforcement (increasing total responsive-inspector prior mass), rather than complementary defense against the two exit channels.

**5. Ideas beyond this experiment**

* Nothing material.
