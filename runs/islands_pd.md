# Island model: pd, weak L_6, I = 64 islands of N = 100, w = 0.3, no mutation

Second-half statistics over a 2e5-generation horizon (frozen runs: the frozen state for the remainder). P(C,C) is P(C,C). DWL = 0 - island mean payoff. "island-time DWL>0.1" is the fraction of island-samples with deadweight loss above 0.1. Outcome at freeze: coop = all surviving pairs (C,C); defect = all pairs (D,D); other = any other frozen outcome; live = not frozen at the horizon.

| graph | mN | seeding | runs | P(C,C) mean ± sd | payoff | island-time DWL>0.1 | frozen (median gen) | coop / defect / other / live | R extinct | ALLC share at gen 1000 | ALLC extinct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| complete | 0.1 | programs | 20 | 0.315 ± 0.415 | -0.487 | 0.750 | 20 (2580) | 5 / 5 / 10 / 0 | 15 | 0.0000 | 20 |
| complete | 0.1 | prior | 20 | 0.388 ± 0.429 | -0.450 | 0.700 | 20 (2650) | 6 / 5 / 9 / 0 | 14 | 0.0000 | 20 |
| complete | 0.1 | hostile | 20 | 0.200 ± 0.348 | -0.581 | 0.850 | 20 (2680) | 3 / 5 / 12 / 0 | 17 | 0.0000 | 20 |
| complete | 0.1 | clustered | 20 | 0.188 ± 0.315 | -0.650 | 0.900 | 20 (2250) | 2 / 9 / 9 / 0 | 18 | 0.0000 | 20 |
| complete | 1 | programs | 20 | 0.228 ± 0.351 | -0.650 | 0.850 | 20 (370) | 3 / 9 / 8 / 0 | 17 | 0.0000 | 20 |
| complete | 1 | prior | 20 | 0.244 ± 0.396 | -0.637 | 0.800 | 20 (380) | 4 / 9 / 7 / 0 | 16 | 0.0000 | 20 |
| complete | 1 | hostile | 20 | 0.215 ± 0.354 | -0.600 | 0.850 | 20 (380) | 3 / 6 / 11 / 0 | 17 | 0.0000 | 20 |
| complete | 1 | clustered | 20 | 0.062 ± 0.092 | -0.762 | 1.000 | 20 (470) | 0 / 8 / 12 / 0 | 20 | 0.0000 | 20 |
| ring | 0.1 | programs | 20 | 0.294 ± 0.377 | -0.475 | 0.800 | 20 (14250) | 4 / 3 / 13 / 0 | 16 | 0.0000 | 20 |
| ring | 0.1 | prior | 20 | 0.403 ± 0.419 | -0.438 | 0.700 | 20 (13060) | 6 / 4 / 10 / 0 | 14 | 0.0000 | 20 |
| ring | 0.1 | hostile | 20 | 0.234 ± 0.337 | -0.500 | 0.850 | 20 (16630) | 3 / 2 / 15 / 0 | 17 | 0.0000 | 20 |
| ring | 0.1 | clustered | 20 | 0.204 ± 0.320 | -0.613 | 0.900 | 20 (19060) | 2 / 6 / 12 / 0 | 18 | 0.0071 | 20 |
| ring | 1 | programs | 20 | 0.285 ± 0.340 | -0.450 | 0.850 | 20 (1860) | 3 / 1 / 16 / 0 | 17 | 0.0000 | 20 |
| ring | 1 | prior | 20 | 0.171 ± 0.353 | -0.738 | 0.850 | 20 (1370) | 3 / 12 / 5 / 0 | 17 | 0.0000 | 20 |
| ring | 1 | hostile | 20 | 0.432 ± 0.435 | -0.412 | 0.650 | 20 (2030) | 7 / 4 / 9 / 0 | 13 | 0.0000 | 20 |
| ring | 1 | clustered | 20 | 0.166 ± 0.318 | -0.694 | 0.900 | 20 (2090) | 2 / 9 / 9 / 0 | 18 | 0.0000 | 20 |

## Dominant classes (share of second-half island-time with a class above 1/2; top 4 per cell)

| graph | mN | seeding | classes (self P(C,C), self payoff): share |
|---|---|---|---|
| complete | 0.1 | programs | `THEM(^ROLE)` (0.00, -0.50): 0.291; `THEM(^C)` (1.00, 0.00): 0.250; `THEM(^X)` (0.25, -0.50): 0.159; `D` (0.00, -1.00): 0.116 |
| complete | 0.1 | prior | `THEM(^C)` (1.00, 0.00): 0.300; `THEM(^ROLE)` (0.00, -0.50): 0.200; `D` (0.00, -1.00): 0.198; `THEM(^X)` (0.25, -0.50): 0.150 |
| complete | 0.1 | hostile | `THEM(^ROLE)` (0.00, -0.50): 0.282; `THEM(^X)` (0.25, -0.50): 0.198; `THEM(^C)` (1.00, 0.00): 0.150; `D` (0.00, -1.00): 0.112 |
| complete | 0.1 | clustered | `D` (0.00, -1.00): 0.239; `THEM(^ROLE)` (0.00, -0.50): 0.200; `THEM(^X)` (0.25, -0.50): 0.150; `THEM(^C)` (1.00, 0.00): 0.100 |
| complete | 1 | programs | `D` (0.00, -1.00): 0.237; `THEM(^X)` (0.25, -0.50): 0.166; `THEM(^C)` (1.00, 0.00): 0.150; `THEM(^D)` (0.00, -1.00): 0.109 |
| complete | 1 | prior | `D` (0.00, -1.00): 0.219; `THEM(^C)` (1.00, 0.00): 0.200; `THEM(^ROLE)` (0.00, -0.50): 0.142; `THEM(^D)` (0.00, -1.00): 0.131 |
| complete | 1 | hostile | `THEM(^ROLE)` (0.00, -0.50): 0.207; `D` (0.00, -1.00): 0.163; `THEM(^C)` (1.00, 0.00): 0.150; `THEM(^X)` (0.25, -0.50): 0.143 |
| complete | 1 | clustered | `THEM(^X)` (0.25, -0.50): 0.201; `D` (0.00, -1.00): 0.166; `THEM(^ROLE)` (0.00, -0.50): 0.148; `THEM(^and(X,ROLE))` (0.00, -0.75): 0.100 |
| ring | 0.1 | programs | `THEM(^X)` (0.25, -0.50): 0.277; `THEM(^ROLE)` (0.00, -0.50): 0.273; `THEM(^C)` (1.00, 0.00): 0.200; `D` (0.00, -1.00): 0.097 |
| ring | 0.1 | prior | `THEM(^C)` (1.00, 0.00): 0.300; `THEM(^X)` (0.25, -0.50): 0.200; `D` (0.00, -1.00): 0.159; `THEM(^ROLE)` (0.00, -0.50): 0.150 |
| ring | 0.1 | hostile | `THEM(^X)` (0.25, -0.50): 0.325; `THEM(^ROLE)` (0.00, -0.50): 0.298; `THEM(^C)` (1.00, 0.00): 0.150; `D` (0.00, -1.00): 0.099 |
| ring | 0.1 | clustered | `D` (0.00, -1.00): 0.227; `THEM(^ROLE)` (0.00, -0.50): 0.200; `THEM(^or(X,ROLE))` (0.50, -0.25): 0.150; `THEM(^C)` (1.00, 0.00): 0.100 |
| ring | 1 | programs | `THEM(^X)` (0.25, -0.50): 0.312; `THEM(^ROLE)` (0.00, -0.50): 0.288; `THEM(^C)` (1.00, 0.00): 0.150; `THEM(^and(X,ROLE))` (0.00, -0.75): 0.050 |
| ring | 1 | prior | `D` (0.00, -1.00): 0.505; `THEM(^C)` (1.00, 0.00): 0.150; `THEM(^ROLE)` (0.00, -0.50): 0.127; `THEM(^D)` (0.00, -1.00): 0.084 |
| ring | 1 | hostile | `THEM(^C)` (1.00, 0.00): 0.350; `THEM(^X)` (0.25, -0.50): 0.227; `THEM(^ROLE)` (0.00, -0.50): 0.173; `THEM(^D)` (0.00, -1.00): 0.120 |
| ring | 1 | clustered | `D` (0.00, -1.00): 0.341; `THEM(^or(X,ROLE))` (0.50, -0.25): 0.100; `THEM(^ROLE)` (0.00, -0.50): 0.100; `THEM(^C)` (1.00, 0.00): 0.100 |

## Exits from `THEM(^C)` islands (pooled over all runs)

Island dominant-class changes out of `THEM(^C)`, sampled every 20 generations: to a faker (a class earning more against `THEM(^C)` than it earns against itself) 1901, to an on-path-identical shadow 0, to anything else 457. Shadow islands later taken by a class exploiting the shadow: 945; other exits from shadow islands: 5.

Destinations: `THEM(^ROLE)` 595, `THEM(^X)` 592, `and(X,THEM(^D))` 266, `THEM(^D)` 218, `THEM(^or(X,ROLE))` 192, `and(ROLE,THEM(^D))` 115, `THEM(^or(X,X))` 99, `THEM(^and(X,ROLE))` 99, `or(ROLE,THEM(^D))` 45, `THEM(^and(X,X))` 40.
