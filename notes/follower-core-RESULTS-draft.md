## The follower-value core and the joint core: no coalition deviating before or after the others (2026-11-15; aside)

Asked by the RS ("is there a follower-value core?"; "I'm most interested in cases whether the cores intersect, meaning no coalition would deviate before OR after the others"; "provisionally an aside"). Predictions `predictions/2026-11-15-follower-core.md` (committed before the computation; light path as queue 77, no spec review). Script `src/follower_core.py`, output `runs/follower-core.json`. A static recomputation from the stored sweep `runs/core-existence-sweep.json` (RESULTS "The leader-value core: where it exists"), no ecology and no new game solving.

*Objects.* v(S) is S's leader value (S commits, the others reply as individuals in Nash equilibrium). v_F(S) = v(S) − FMA(S) is S's payoff at the complement's leader outcome, as stored. Three transferable-utility cores per point, by the sweep's `tu_core`: **leader** (v), **follower** (v_F), and **joint** (max(v, v_F) on every proper coalition, the grand value unchanged). The joint core is the intersection of the other two. Scope: TU only, the stored selection per point, and the 6,841 grid and panel points with FMA stored for every proper coalition. The exchange family (1,000 points) has no FMA stored, so trading games are not covered.

*Counts* (points with a nonempty or tight leader core; share of those with a nonempty or tight joint core; follower core empty among them):

| family | points | leader core exists | joint core exists | share | follower core empty |
|---|---|---|---|---|---|
| Cournot | 2,023 | 1,924 | 1,892 | 0.98 | 0 |
| Cournot (NTU grid, TU values) | 363 | 339 | 332 | 0.98 | 0 |
| Cournot with capacities | 332 | 332 | 210 | 0.63 | 119 |
| homogeneous Bertrand | 363 | 363 | 363 | 1.00 | 0 |
| public goods | 1,820 | 1,735 | 277 | 0.16 | 1,224 |
| linear-quadratic | 1,560 | 1,545 | 654 | 0.42 | 889 |
| differentiated Bertrand | 332 | 332 | 108 | 0.33 | 224 |
| panel | 48 | 30 | 22 | 0.73 | 6 |
| pooled | 6,841 | 6,600 | 3,858 | 0.58 | 2,462 |

- **Joint-core failure is associated with a first-mover advantage whose sign is mixed across coalitions** (neither necessary nor sufficient). 3,850 points (0.56) have some coalition that gains by leading and another that gains by following. Among those with a leader core the joint core exists at 0.27 (999 of 3,739). At almost every other point with a leader core it exists (2,859 of 2,861; the two exceptions are panel points where no coalition gains by leading and at least one gains by following).
- **Two existing cores can be disjoint.** Of the 6,600 points with a leader core, 4,138 also have a follower core, and at 280 of those the intersection is empty: 234 public goods, 32 Cournot, 7 Cournot on the NTU grid, 3 Cournot with capacities, 2 linear-quadratic, 2 panel. The other 2,462 joint failures have no follower core to begin with.
- **The follower core alone is the weaker demand where every coalition gains by leading and the stronger one where none does; with mixed signs neither contains the other in general.** In plain Cournot and homogeneous Bertrand it is never empty where the leader core exists, and it exists at all 99 + 24 Cournot points where the leader core is empty. In differentiated Bertrand and public goods it is empty at 0.67 and 0.71 of the points with a leader core, and at 0.58 in linear-quadratic games.
- **Public goods are the sharpest case.** The leader core exists at 0.95 of points and the joint core at 0.16 of those. At mixed-sign points the sign follows coalition size (tabulated from the stored FMA, post hoc): in public goods at n = 5, singletons gain by following in 4,284 cases against 580 by leading, and four-player coalitions gain by leading in all 4,899 signed cases; in differentiated Bertrand singletons always gain by following and coalitions of n − 1 always by leading; linear-quadratic games and Cournot with capacities show the same pattern. Free-riding as the reason small coalitions prefer to follow is an untested hypothesis; no coalition-level infeasibility certificate was computed.
- **Catalogue.** PD: all three exist. Chicken, hawk–dove (hd3, hd6) and `dollar5`: leader empty, follower nonempty, joint empty. `dollar3`: leader and joint empty under both selections, follower empty under pessimistic selection and nonempty under optimistic. SOG, pessimistic: leader nonempty, follower empty, joint empty; optimistic: all three tight.

*Verdicts.* F1 falsified: on the registered three-way verdict, agreement is 1,991 of 2,023 in plain Cournot, 356 of 363 on the NTU grid, 201 of 332 with capacities and 310 of 1,820 in public goods (binary existence, supplementary: 0.98, 0.98, 0.63, 0.20). F2 holds (follower empty at 224 of 332 differentiated-Bertrand points and 889 of the 1,529 linear-quadratic points with FMA < 0 somewhere and a leader core). F3 fails, falsifier not fired (0.58 against a predicted ≥ 0.8). F4: the share clause is false (mixed-sign points are 0.56 of all, not < 0.2); the rate clause holds (the joint core is empty at 0.74 of mixed-sign points against 0.044 elsewhere; 0.73 against 0.001 among points with a leader core). F5 falsified for the SOG under pessimistic selection (joint empty); the other catalogue entries as predicted.

*Caveats.* TU only; the NTU joint core is not computed. Individual followers and each point's stored selection only. v_F is read off the complement's leader outcome with ties as stored. The sign classes use the sweep's tolerance. Nothing here is about the ecology.
