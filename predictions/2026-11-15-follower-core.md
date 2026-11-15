# Predictions: the follower-value core and its intersection with the leader-value core, 2026-11-15

Aside (RS, 2026-11-15: "I'm most interested in cases whether the cores intersect, meaning no coalition would deviate
before OR after the others"; "provisionally an aside"). Static, from the stored sweep `runs/core-existence-sweep.json`
(RESULTS "The leader-value core: where it exists"): v_F(S) = v(S) − FMA(S), the payoff S gets at the complement's
leader outcome. Three TU cores per point by the sweep's own `tu_core`: leader (v), follower (v_F), and **both**
(max(v, v_F) on proper coalitions, the grand value unchanged). Script `src/follower_core.py`. Light path as queue 77
(no spec review). Scope: TU only; individual followers; points where FMA is stored for every proper coalition (the
exchange family has none stored, so the RS's trading worry is not tested here).

Identities, not predictions: if FMA ≥ 0 for every coalition, both = leader; if ≤ 0 for every coalition, both = follower.

- **F1.** In Cournot (all variants) and public goods, both = leader core in verdict at ≥ 95% of points (first-mover
  advantage is the rule). Falsifier: < 80%.
- **F2.** In the complements families (differentiated Bertrand, LQ points with FMA < 0 somewhere), the follower core is
  empty at ≥ 5% of the points where the leader core is nonempty. Falsifier: at none.
- **F3.** Pooled over all points with a nonempty leader core, the intersection is nonempty at ≥ 80%. Falsifier: < 50%.
- **F4.** Points with mixed-sign FMA (some coalition gains by leading, another by following) are < 20% of all points,
  and the intersection is empty at a higher rate there than elsewhere. Falsifier: the rate is not higher.
- **F5.** Catalogue: the PD and the SOG keep their leader verdicts for the intersection; chicken, hawk–dove and the
  dollar games stay empty.
