# Review of `specs/2026-10-21-prudence-world-k.md` by gemini-4-argon

**1. Errors, contradictions or unsound mechanisms**

* **Contradiction in the sucker-depleted control across worlds:** Amendment 2 defines the control as: *"arrivals drawn from the prior with unconditional and certified cooperators removed and the rest renormalized, at the same rate."* However, the brief’s "Why" states that in world L, the TwinD family are identity cliques, while in world K they become *"certified unconditional cooperators"*. If "certified cooperators" means the TwinD family, removing them in both worlds removes identity cliques in world L (altering the rival/predator arrival rate) while removing suckers in world K. Conversely, if "certified cooperators" is evaluated behaviourally per world, the renormalized arrival distributions for non-suckers will differ in mass between K and L, breaking the *"paired fresh-founder sequences"* design.
  * **Fix:** Define the excluded set syntactically as the union of unconditional cooperators and the TwinD family in *both* worlds, or introduce a third control removing only uncertified unconditional cooperators so the K-vs-L difference on the TwinD family is isolated without confounding identity-clique arrivals in L.
* **Drop order contradiction:** The Design section states *"Drop order: A = 156 in world L, then the chase"*, while Amendment 4 says *"The chase is kept (never dropped)"* and Amendment 5 revises the drop order.
  * **Fix:** Delete the stale drop-order sentence from the Design section so the subagent does not follow it by mistake.
* **Undefined denominator in Prediction 3:** Prediction 3 compares *"the premium per sucker encounter"* between K and L. In K, certified suckers are not exploited by PrudentBot, so they survive longer in the population than in L, inflating the encounter count with certified suckers and mechanically depressing the per-encounter average even if per-capita selection per *arriving* sucker were unchanged.
  * **Fix:** Specify whether the denominator of "sucker encounter" in Prediction 3's falsifier is *all* suckers (certified + uncertified) or *uncertainties only*, and tie the primary falsifier to the static/fixed-list edge (Amendment 3) or per-arriving-founder exposure rather than the endogenous encounter-weighted average.

**2. Design flaws or confounds**

* **Delayed schedule decay ($t_0 = 6,400$ vs horizon $10,000$):** Setting $t_0 = N/2 = 6,400$ for the merged population means the arrival rate at the end of the 10,000-generation tail is still $(1 + 10000/6400)^{-2} \approx 15\%$ of its initial peak, and over $39\%$ of the infinite-horizon integral occurs *after* $t = 10,000$. Because Amendment 1 normalizes the schedule so the delivered integral over the 10,000 window equals $A$, this is more like a heavy sustained rain that abruptly cuts off at $t = 10,000$ than an annealed tail.
  * **Fix:** Either shorten $t_0$ (e.g., $t_0 = 1,000$ or $2,000$) so the tail actually anneals before the chase, or explicitly relabel the schedule as a slowly tapering rain truncated at $10,000$.

**3. Predictions you think are wrong**

* **Prediction 4 (Universal-open $\ge 0.9$ at every $A$ in both worlds):** Likely wrong at $A = 156$ in world L (as gpt-6.1-sol also noted). In "Annealed mutation", a single fit identity arrival could take a whole run through an identity-exploitable target holder. At $A = 156$ per 100 programs ($19,968$ total arrivals across the merged population), identity cliques will be repeatedly injected alongside uncertified target drift variants. I predict universal-open in world L at $A = 156$ falls below $0.85$.

**4. Missing controls or cheap additions**

* **Pre-merge vs post-merge state logging:** Log the exact population composition at $t = 200$ (immediately at the merge, before the tail starts). Without this, you cannot separate how much of PrudentBot's terminal share came from the island-scramble prudence premium ($t \le 200$) versus the post-merge tail ($t > 200$).

**5. Alternative explanations**

* **Anti-punisher / predator pruning vs sucker exploitation:** Under a re-injection tail, defectors and anti-punishers also arrive continuously. If uncertified FairBot variants are more vulnerable to arriving defectors/rivals than PrudentBot is, PrudentBot's share will rise and off-target residence will fall due to *defensive resilience against arriving predators*, not the *offensive prudence premium* from eating arriving suckers. The sucker-depleted control (Amendment 2) rules this out *only if*Prediction 1 and 2 are explicitly evaluated against the sucker-depleted control at $A = 52$, not just against $A = 0$. Make that comparison part of the falsifier.
