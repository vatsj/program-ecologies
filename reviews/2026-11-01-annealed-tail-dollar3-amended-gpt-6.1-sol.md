# Review of `specs/2026-11-01-annealed-tail-dollar3.md` by gpt-6.1-sol

1. **Errors / unsound mechanisms**
- The amendment says “one completed by migrants from already-rescued islands [scales] as Λ.” This does not follow: if those migrants are themselves generated at order Λ, completing another rescue can remain order Λ². Conversely, a pre-existing donor supply permits linear rescue. **Fix:** distinguish baseline from tail-generated migrant supply; estimate small-Λ scaling rather than assigning it from event labels. Tracking `(tail E, migrant Lw)` requires lineage-tagged intermediate states, not ordinary transition-flux totals.
- “Both directions start with a neutral step” conflicts with the listed alternative “a victim enters at −⅙.” The notes also identify deleterious concessions out of U. Neither direction’s complete rate necessarily scales as 1/N, especially at N = 100. **Fix:** enumerate competing paths and calculate their rates separately; restrict the neutral-bottleneck claim to demonstrated dominant paths.
- Prediction 5 requires “removing the victims lowers [Λ*] by at least 1.5×,” but the ablation design requests only “ablation endpoints” at one Λ. **Fix:** bracket ablated thresholds, or replace threshold predictions with endpoint contrasts.

2. **Design flaws / confounds**
- **The amended full-conditional check changes two things:** “m = 3 on … 48-conditional core” versus “m = 1 … over every conditional.” The notes already report that m = 1 has 15% blocked flux at an unequal endpoint. Agreement cannot validate omitted predators; disagreement cannot identify their cause. **Fix:** compare matched-core m = 1 and full-conditional m = 1, alongside object P, then use full-library Monte Carlo near the relevant late-tail outcome.
- **Finite-horizon classifications are not the stated time limit.** At Λ = 300, t₀ = 10⁴, the cap leaves about 0.03 arrivals per island, not 10⁻⁴. Small remaining forcing can still cross a nearby separatrix; small residuals also do not establish asymptotic absorption. **Fix:** call capped results censored, not endpoints; continue tail-free from the cap and test sensitivity to administering the remaining dose. Report unresolved Λ* brackets.
- **N scaling changes the migrant dynamics as well as tail fixation.** Founding held fixed does not hold the basin boundary or relaxation time fixed. **Fix:** obtain the Λ = 0 outcome and boundary distance at every N; include a late-tail comparison and a fixed-dose single-island neutral-entry assay.

3. **Predictions likely wrong**
- The inference “97.6% constants … boundary … 0.69” therefore “tail … toward V*” substitutes a founding-basin threshold for a perturbation response around a different resident distribution. **Prediction:** early M-natural rescue is substantially easier than deep-U rescue; the constants percentage alone will not predict the latter.
- Λ*(N) ∝ N is unsupported for the early tail because both basin geometry and competing deleterious paths change. **Prediction:** no clean proportional scaling across these three N values.
- Monotonicity is not guaranteed when arrivals supply both rescue and exploitation. Prediction 1’s falsifier also misses decreases that remain above 0.1004. **Fix:** score every adjacent-grid decrease separately.

4. **Missing controls / cheap additions**
- Add matched-dose, unrenormalized ablations, assigning removed mass to null events; otherwise victim removal increases every remaining family’s dose.
- Check timestep/tolerance convergence near Λ*, particularly for the stiff backward-Euler phase.
- Test tiny asymmetric perturbations at representative rescued outcomes; enforced symmetry cannot demonstrate robustness or the across-world lottery.

5. **Alternative explanations**
- Apparent rescue may reflect numerical deletion of rare donors, truncation-blocked exploitation, or schedule-dependent basin crossing rather than durable repair of the ratchet.
