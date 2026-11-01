# Review of `specs/2026-11-01-annealed-tail-dollar3.md` by gemini-4-argon

1. **Design flaws or confounds**
- **Two-step tail rescue vs. migrant amplification (confound in Cell 3 & Prediction 2):** On a settled U ratchet ($10^{-17}$ offering constants), a single tail arrival of an offering constant into the excluded slot $E$ fixes neutrally ($1/N$), creating an unrescued U state with an offering $E$. To complete $U \to V^*$, slot $Lw$ needs a $(2, 1/2)$ constant. If $Lw$'s $(2, 1/2)$ is also depleted in the donor marginal $q(x)$, the rescue requires *two* tail arrivals on the *same* island (scaling as $(\Lambda/N)^2$), unless the first rescued islands immediately amplify $(2, 1/2)$ in the migrant pool $q(x)$. 
  *Fix:* In the attribution (Cell 5) and late-tail (Cell 3) outputs, report the donor marginal mass $q(x)$ of $(2, 1/2)$ and offering constants at $t_s = 10^6$, and decompose $U \to V^*$ rescue steps into `(tail E, migrant Lw)` vs. `(tail E, tail Lw)`.
- **Convergence horizon at large $t_0$ and $\Lambda$:** The endpoint criterion requires $\int_t^\infty \varepsilon(s)ds = \Lambda/(1 + (t-t_s)/t_0) < 10^{-6}$. For $\Lambda = 300, t_0 = 10^4$, this forces $t > 3 \cdot 10^{12}$ events, which may cause stiffness or step-size artifacts in `integrate_be` and hides when the flip actually occurs.
  *Fix:* Record class shares at fixed milestones ($t = 10^4, 10^5, 10^6, 10^7$) in addition to the asymptotic endpoint, and cap the integration horizon at $t - t_s = 10^8$ if the tail integral criterion is the only thing preventing termination (or lower the tail-integral threshold to $10^{-4}$ per island, since fixation is $1/N = 10^{-2}$).
- **Symmetry enforcement:** Queue 70's `notes/unequal-basin.md` (§2.3) found that unsymmetrized pool-0 goes to $U = 1.0$ while the $S_3$-symmetrized start goes to $V^* = 0.9997$. The brief does not state whether the ODE and prior $p$ are $S_3$-symmetrized at every step.
  *Fix:* Specify explicitly that both $x(0)$ and $p$ are $S_3$-symmetrized (or that `sym=True` is passed to `field`).

2. **Predictions I think are wrong**
- **Prediction 5 (Removing Trojan bullies from the tail lowers $\Lambda^*$ by $\ge 2\times$):** Likely wrong. In the prior $p$, Trojan bullies have mass $3.7 \cdot 10^{-5}$ per slot, whereas offering constants have mass $\approx 2/9 \approx 0.22$. In the *tail*, constants outnumber bullies by $6,000:1$. The bullies do their damage via the *founding start* and *migrant* amplification ($q(x)$), not via tail re-supply. Removing them from $p$ while keeping the founding law unchanged will move $\Lambda^*$ by $< 1\%$. 
  *My prediction:* Tail ablation (a) changes $\Lambda^*$ by less than $1.05\times$; tail ablation (b) (removing $1/3$-demanding constant victims, prior mass $0.108$) lowers $\Lambda^*$ by $\ge 1.5\times$.
- **Prediction 6 ($\Lambda^*(400)/\Lambda^*(100) \in [2.5, 6]$ at $t_0 = 10^2$):** Likely wrong (ratio will be smaller). At $t_0 = 10^2$, the system is in the middle of the mean-field scramble near the basin boundary $u^*$, not trapped in a settled ratchet. Moreover, as $N$ increases from 100 to 400, deleterious moves ($\Delta = -1/6$, which feed $V^* \to U$ via constant victims at rate $e^{-wN/6}$) are suppressed from $3.5 \cdot 10^{-4}$ to $6 \cdot 10^{-10}$, stabilizing $V^*$ in the migrant field. Thus less tail mass is needed to tip the boundary than strict $1/N$ neutral scaling implies.
  *My prediction:* $\Lambda^*(400)/\Lambda^*(100) < 2.5$ for the early tail ($t_0 = 10^2$), whereas the *late* tail ($t_s = 10^6$) will obey $\propto N$ scaling.

3. **Missing controls or cheap additions**
- **Constants-only tail ablation:** Add a fourth ablation in Cell 5 where the tail $p$ is restricted to the 9 constants only. Zero extra code, directly tests whether conditional programs in the tail do anything at all.
- **Full-core check for the tail:** In Object P, 96% of conditionals in $p$ are outside the 48-core and become null tail events. Run a single point ($M$ natural, $t_0 = 10^2, \Lambda = \Lambda^*$) on the $m = 1$ full-conditional object (316k states) to verify that the $2.3\%$ blocked conditional tail mass does not contain a surprise predator.

4. **Alternative explanations the brief does not rule out**
- **Basin-boundary shift vs. ratchet cure:** At $t_0 = 1$ and $10^2$, the tail acts *before* the unequal ratchet settles (which takes $\sim 10^4$ events). If $\Lambda^*$ is small at $t_0 \le 10^2$, it may simply be shifting the effective initial condition $u(0)$ from $0.429$ across the $u^* = 0.425$ boundary (a $0.4\%$ nudge), rather than "rescuing" depleted offerers from a ratchet. Cell 3 (late tail) is the only true test of ratchet rescue; the brief should frame Cell 2 ($t_0 \le 10^2$) as a boundary-perturbation test and Cell 3 as the ratchet-rescue test.

5. **Ideas that matter for the research program**
- Nothing material.
