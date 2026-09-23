# Island model: chicken, weak L_6, I = 64 islands of N = 100, w = 0.3, no mutation

Second-half statistics over a 2e5-generation horizon (frozen runs: the frozen state for the remainder). P(C,C) is P(Swerve,Swerve). DWL = 0.5 - island mean payoff. "island-time DWL>0.1" is the fraction of island-samples with deadweight loss above 0.1. Outcome at freeze: coop = all surviving pairs (C,C); defect = all pairs (D,D); other = any other frozen outcome; live = not frozen at the horizon.

| graph | mN | seeding | runs | P(C,C) mean ± sd | payoff | island-time DWL>0.1 | frozen (median gen) | coop / defect / other / live | R extinct | ALLC share at gen 1000 | ALLC extinct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| complete | 0.1 | programs | 20 | 0.029 ± 0.049 | 0.480 | 0.072 | 1 (23680) | 0 / 0 / 1 / 19 | 20 | 0.0000 | 20 |
| complete | 0.1 | hostile | 20 | 0.150 ± 0.324 | 0.421 | 0.181 | 4 (16630) | 0 / 0 / 4 / 16 | 20 | 0.0000 | 20 |
| complete | 0.1 | clustered | 20 | 0.040 ± 0.055 | 0.473 | 0.092 | 0 (-) | 0 / 0 / 0 / 20 | 17 | 0.0000 | 20 |
| complete | 1 | programs | 20 | 0.104 ± 0.296 | 0.409 | 0.325 | 7 (820) | 1 / 0 / 6 / 13 | 19 | 0.0000 | 20 |
| complete | 1 | hostile | 20 | 0.053 ± 0.217 | 0.411 | 0.327 | 5 (900) | 0 / 0 / 5 / 15 | 19 | 0.0000 | 20 |
| complete | 1 | clustered | 20 | 0.127 ± 0.255 | 0.380 | 0.414 | 2 (1240) | 0 / 0 / 2 / 18 | 12 | 0.0000 | 20 |
| ring | 0.1 | programs | 20 | 0.021 ± 0.021 | 0.487 | 0.050 | 0 (-) | 0 / 0 / 0 / 20 | 20 | 0.0007 | 20 |
| ring | 0.1 | hostile | 20 | 0.027 ± 0.031 | 0.485 | 0.056 | 0 (-) | 0 / 0 / 0 / 20 | 20 | 0.0026 | 20 |
| ring | 0.1 | clustered | 20 | 0.162 ± 0.166 | 0.418 | 0.242 | 1 (18760) | 0 / 0 / 1 / 19 | 15 | 0.2783 | 20 |
| ring | 1 | programs | 20 | 0.070 ± 0.202 | 0.432 | 0.222 | 1 (3660) | 0 / 0 / 1 / 19 | 20 | 0.0000 | 20 |
| ring | 1 | hostile | 20 | 0.056 ± 0.137 | 0.453 | 0.147 | 1 (87580) | 0 / 0 / 1 / 19 | 20 | 0.0000 | 20 |
| ring | 1 | clustered | 20 | 0.166 ± 0.252 | 0.394 | 0.302 | 0 (-) | 0 / 0 / 0 / 20 | 18 | 0.0034 | 20 |

## Dominant classes (share of second-half island-time with a class above 1/2; top 4 per cell)

| graph | mN | seeding | classes (self P(C,C), self payoff): share |
|---|---|---|---|
| complete | 0.1 | programs | `ROLE` (0.00, 0.50): 0.520; `not(ROLE)` (0.00, 0.50): 0.327; `not(THEM(^ROLE))` (0.00, 0.50): 0.049; `not(THEM(^not(ROLE)))` (0.00, 0.50): 0.046 |
| complete | 0.1 | hostile | `ROLE` (0.00, 0.50): 0.459; `not(ROLE)` (0.00, 0.50): 0.192; `not(or(THEM(THEM),X))` (1.00, 0.00): 0.138; `not(THEM(^not(ROLE)))` (0.00, 0.50): 0.083 |
| complete | 0.1 | clustered | `ROLE` (0.00, 0.50): 0.525; `not(ROLE)` (0.00, 0.50): 0.356; `not(or(ROLE,THEM(ME)))` (0.00, 0.50): 0.029; `and(ROLE,not(THEM(ME)))` (0.00, 0.50): 0.029 |
| complete | 1 | programs | `ROLE` (0.00, 0.50): 0.425; `not(or(ROLE,THEM(ME)))` (0.00, 0.50): 0.115; `not(THEM(^ROLE))` (0.00, 0.50): 0.115; `not(or(THEM(THEM),X))` (1.00, 0.00): 0.100 |
| complete | 1 | hostile | `not(THEM(^not(ROLE)))` (0.00, 0.50): 0.220; `ROLE` (0.00, 0.50): 0.217; `not(THEM(^ROLE))` (0.00, 0.50): 0.142; `not(ROLE)` (0.00, 0.50): 0.127 |
| complete | 1 | clustered | `ROLE` (0.00, 0.50): 0.434; `not(ROLE)` (0.00, 0.50): 0.295; `not(or(THEM(ME),X))` (1.00, 0.00): 0.052; `and(ROLE,not(THEM(ME)))` (0.00, 0.50): 0.052 |
| ring | 0.1 | programs | `ROLE` (0.00, 0.50): 0.525; `not(ROLE)` (0.00, 0.50): 0.310; `not(THEM(^not(ROLE)))` (0.00, 0.50): 0.059; `not(THEM(^ROLE))` (0.00, 0.50): 0.027 |
| ring | 0.1 | hostile | `ROLE` (0.00, 0.50): 0.501; `not(ROLE)` (0.00, 0.50): 0.379; `not(THEM(^ROLE))` (0.00, 0.50): 0.036; `not(THEM(^not(ROLE)))` (0.00, 0.50): 0.017 |
| ring | 0.1 | clustered | `ROLE` (0.00, 0.50): 0.536; `or(X,ROLE)` (0.50, 0.25): 0.075; `not(ROLE)` (0.00, 0.50): 0.074; `not(and(X,ROLE))` (0.50, 0.25): 0.062 |
| ring | 1 | programs | `ROLE` (0.00, 0.50): 0.473; `not(ROLE)` (0.00, 0.50): 0.220; `not(THEM(^ROLE))` (0.00, 0.50): 0.065; `not(THEM(^not(ROLE)))` (0.00, 0.50): 0.050 |
| ring | 1 | hostile | `ROLE` (0.00, 0.50): 0.492; `not(ROLE)` (0.00, 0.50): 0.357; `not(THEM(^not(ROLE)))` (0.00, 0.50): 0.050; `and(THEM(THEM),Straight)` (1.00, 0.00): 0.034 |
| ring | 1 | clustered | `ROLE` (0.00, 0.50): 0.515; `not(or(THEM(THEM),X))` (1.00, 0.00): 0.082; `not(and(X,ROLE))` (0.50, 0.25): 0.061; `not(or(ROLE,THEM(ME)))` (0.00, 0.50): 0.058 |

## Exits from `THEM(^Swerve)` islands (pooled over all runs)

Island dominant-class changes out of `THEM(^Swerve)`, sampled every 20 generations: to a faker (a class earning more against `THEM(^Swerve)` than it earns against itself) 1450, to an on-path-identical shadow 41, to anything else 55. Shadow islands later taken by a class exploiting the shadow: 6748; other exits from shadow islands: 187.

Destinations: `THEM(^X)` 1417, `not(and(X,ROLE))` 53, `THEM(^ROLE)` 33, `THEM(THEM)` 25, `THEM(ME)` 9, `Swerve` 5, `or(THEM(ME),Swerve)` 2, `or(X,ROLE)` 1, `or(X,or(X,X))` 1.
