# Island model: chicken_norole, weak L_6 without ROLE, I = 64 islands of N = 100, w = 0.3, no mutation

Second-half statistics over a 2e5-generation horizon (frozen runs: the frozen state for the remainder). P(C,C) is P(Swerve,Swerve). DWL = 0.5 - island mean payoff. "island-time DWL>0.1" is the fraction of island-samples with deadweight loss above 0.1. Outcome at freeze: coop = all surviving pairs (C,C); defect = all pairs (D,D); other = any other frozen outcome; live = not frozen at the horizon.

| graph | mN | seeding | runs | P(C,C) mean ± sd | payoff | island-time DWL>0.1 | frozen (median gen) | coop / defect / other / live | R extinct | ALLC share at gen 1000 | ALLC extinct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| complete | 0.1 | programs | 20 | 0.670 ± 0.191 | -0.216 | 1.000 | 0 (-) | 0 / 0 / 0 / 20 | 16 | 0.0000 | 20 |
| complete | 0.1 | hostile | 20 | 0.702 ± 0.101 | -0.184 | 1.000 | 0 (-) | 0 / 0 / 0 / 20 | 20 | 0.0000 | 20 |
| complete | 0.1 | clustered | 20 | 0.806 ± 0.198 | -0.127 | 1.000 | 5 (24860) | 5 / 0 / 0 / 15 | 6 | 0.0005 | 20 |
| complete | 1 | programs | 20 | 0.486 ± 0.133 | -0.343 | 1.000 | 1 (1500) | 1 / 0 / 0 / 19 | 19 | 0.0000 | 20 |
| complete | 1 | hostile | 20 | 0.575 ± 0.107 | -0.271 | 1.000 | 0 (-) | 0 / 0 / 0 / 20 | 20 | 0.0000 | 20 |
| complete | 1 | clustered | 20 | 0.784 ± 0.183 | -0.142 | 1.000 | 4 (1180) | 4 / 0 / 0 / 16 | 11 | 0.0000 | 20 |
| ring | 0.1 | programs | 20 | 0.686 ± 0.167 | -0.202 | 1.000 | 0 (-) | 0 / 0 / 0 / 20 | 17 | 0.0009 | 20 |
| ring | 0.1 | hostile | 20 | 0.720 ± 0.107 | -0.173 | 1.000 | 0 (-) | 0 / 0 / 0 / 20 | 20 | 0.0021 | 20 |
| ring | 0.1 | clustered | 20 | 0.751 ± 0.170 | -0.159 | 1.000 | 2 (32110) | 2 / 0 / 0 / 18 | 12 | 0.4102 | 20 |
| ring | 1 | programs | 20 | 0.470 ± 0.081 | -0.353 | 1.000 | 0 (-) | 0 / 0 / 0 / 20 | 20 | 0.0000 | 20 |
| ring | 1 | hostile | 20 | 0.551 ± 0.139 | -0.292 | 1.000 | 1 (13820) | 1 / 0 / 0 / 19 | 19 | 0.0000 | 20 |
| ring | 1 | clustered | 20 | 0.747 ± 0.158 | -0.159 | 1.000 | 4 (12540) | 4 / 0 / 0 / 16 | 12 | 0.0140 | 20 |

## Dominant classes (share of second-half island-time with a class above 1/2; top 4 per cell)

| graph | mN | seeding | classes (self P(C,C), self payoff): share |
|---|---|---|---|
| complete | 0.1 | programs | `not(THEM(ME))` (1.00, 0.00): 0.387; `not(THEM(THEM))` (1.00, 0.00): 0.261; `THEM(^Swerve)` (1.00, 0.00): 0.122; `not(and(THEM(THEM),X))` (1.00, 0.00): 0.100 |
| complete | 0.1 | hostile | `not(THEM(ME))` (1.00, 0.00): 0.583; `not(THEM(THEM))` (1.00, 0.00): 0.408; `not(or(X,THEM(ME)))` (0.11, -4.22): 0.007 |
| complete | 0.1 | clustered | `THEM(^Swerve)` (1.00, 0.00): 0.375; `not(THEM(THEM))` (1.00, 0.00): 0.217; `not(and(THEM(ME),X))` (1.00, 0.00): 0.140; `not(THEM(ME))` (1.00, 0.00): 0.100 |
| complete | 1 | programs | `not(THEM(ME))` (1.00, 0.00): 0.373; `not(THEM(THEM))` (1.00, 0.00): 0.343; `not(and(THEM(THEM),X))` (1.00, 0.00): 0.098; `not(and(THEM(ME),X))` (1.00, 0.00): 0.095 |
| complete | 1 | hostile | `not(THEM(THEM))` (1.00, 0.00): 0.494; `not(THEM(ME))` (1.00, 0.00): 0.393; `or(THEM(ME),Swerve)` (1.00, 0.00): 0.050; `not(and(THEM(THEM),X))` (1.00, 0.00): 0.050 |
| complete | 1 | clustered | `THEM(^Swerve)` (1.00, 0.00): 0.298; `not(THEM(THEM))` (1.00, 0.00): 0.270; `or(THEM(ME),Swerve)` (1.00, 0.00): 0.175; `not(and(THEM(THEM),X))` (1.00, 0.00): 0.134 |
| ring | 0.1 | programs | `not(THEM(ME))` (1.00, 0.00): 0.603; `not(THEM(THEM))` (1.00, 0.00): 0.229; `THEM(^Swerve)` (1.00, 0.00): 0.085; `or(THEM(ME),Swerve)` (1.00, 0.00): 0.026 |
| ring | 0.1 | hostile | `not(THEM(ME))` (1.00, 0.00): 0.565; `not(THEM(THEM))` (1.00, 0.00): 0.276; `not(and(THEM(ME),X))` (1.00, 0.00): 0.104; `not(and(THEM(THEM),X))` (1.00, 0.00): 0.044 |
| ring | 0.1 | clustered | `not(and(THEM(ME),X))` (1.00, 0.00): 0.444; `not(and(THEM(THEM),X))` (1.00, 0.00): 0.286; `not(or(THEM(ME),X))` (1.00, 0.00): 0.087; `THEM(^Swerve)` (1.00, 0.00): 0.073 |
| ring | 1 | programs | `not(THEM(ME))` (1.00, 0.00): 0.618; `not(THEM(THEM))` (1.00, 0.00): 0.246; `not(and(THEM(ME),X))` (1.00, 0.00): 0.046; `or(THEM(ME),Swerve)` (1.00, 0.00): 0.046 |
| ring | 1 | hostile | `not(THEM(ME))` (1.00, 0.00): 0.443; `not(THEM(THEM))` (1.00, 0.00): 0.387; `THEM(^Swerve)` (1.00, 0.00): 0.050; `not(and(THEM(ME),X))` (1.00, 0.00): 0.049 |
| ring | 1 | clustered | `not(and(THEM(THEM),X))` (1.00, 0.00): 0.309; `not(and(THEM(ME),X))` (1.00, 0.00): 0.258; `THEM(^Swerve)` (1.00, 0.00): 0.131; `not(or(THEM(ME),X))` (1.00, 0.00): 0.112 |

## Exits from `THEM(^Swerve)` islands (pooled over all runs)

Island dominant-class changes out of `THEM(^Swerve)`, sampled every 20 generations: to a faker (a class earning more against `THEM(^Swerve)` than it earns against itself) 10007, to an on-path-identical shadow 2416, to anything else 297. Shadow islands later taken by a class exploiting the shadow: 416330; other exits from shadow islands: 16692.

Destinations: `THEM(^X)` 9966, `or(THEM(ME),Swerve)` 1205, `THEM(ME)` 888, `not(and(THEM(ME),X))` 266, `THEM(THEM)` 252, `or(X,THEM(^X))` 41, `Swerve` 29, `or(THEM(THEM),X)` 27, `or(X,X)` 19, `or(THEM(ME),X)` 15.
