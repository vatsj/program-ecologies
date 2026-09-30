# Regret witnesses (predictions in `predictions/2026-09-30-regret-witnesses.md`)

r(q) = u(q, σ) − u(σ, σ); a state is no-regret iff max r ≤ 1e-9. Top witnesses with positive regret listed.

| game | state | payoff u(σ,σ) | max regret | top witnesses |
|---|---|---|---|---|
| PD | all-`D` | -1.000 | 0.000 | — |
| PD | all-`THEM(^C)` | 0.000 | 1.000 | `THEM(^D)` 1.000, `THEM(^and(X,ROLE))` 0.750, `THEM(^and(X,X))` 0.750, `THEM(^X)` 0.500 |
| PD | all-`X` | -0.500 | 0.500 | `D` 0.500, `and(THEM(THEM),D)` 0.500, `and(THEM(ME),D)` 0.500, `not(or(X,or(X,ROLE)))` 0.375 |
| PD | all-`ROLE` | -0.500 | 0.500 | `D` 0.500, `and(ROLE,THEM(THEM))` 0.500, `and(ROLE,THEM(^X))` 0.500, `and(THEM(ME),ROLE)` 0.500 |
| PD | all-`THEM(^C)`: regret of the shadow `C` | | 0.000 | |
| PD islands | frozen coop (56 runs) | | 0 no-regret; max regret median 1.000, max 1.000 | `THEM(^D)` ×56 |
| PD islands | frozen defect (97 runs) | | 38 no-regret; max regret median 0.013, max 1.992 | `not(THEM(ME))` ×23, `THEM(^C)` ×12, `not(THEM(^C))` ×11, `not(or(THEM(ME),ROLE))` ×6; exploitable-by-`not(THEM(^C))` share: max 0.33 in no-regret runs, min 0.00 in positive-regret runs |
| PD islands | frozen other (167 runs) | | 0 no-regret; max regret median 0.750, max 1.250 | `not(and(THEM(ME),ROLE))` ×55, `C` ×44, `or(ROLE,THEM(^D))` ×37, `not(and(ROLE,THEM(ME)))` ×11 |
| Chicken+ROLE | all-`ROLE` | 0.500 | 0.000 | — |
| Chicken+ROLE | all-`not(ROLE)` | 0.500 | 0.000 | — |
| Chicken+ROLE | all-`THEM(^ROLE)` | 0.500 | 0.500 | `not(and(THEM(ME),ROLE))` 0.500, `or(ROLE,THEM(^Straight))` 0.500, `not(and(ROLE,THEM(ME)))` 0.500 |
| Chicken+ROLE | all-`not(or(THEM(THEM),X))` | 0.000 | 0.000 | — |
| Chicken+ROLE | all-`not(or(THEM(ME),X))` | 0.000 | 0.000 | — |
| Chicken+ROLE | all-`THEM(ME)` | 0.000 | 0.000 | — |
| Chicken no ROLE | mixed-eq state: `not(THEM(ME))` 9/11 + Straight 2/11 | -0.182 | 1.636 | `not(THEM(^Straight))` 1.636, `not(or(X,THEM(ME)))` 0.818 |
| Chicken no ROLE | three-class cool state (0.659/0.195/0.146) | -0.340 | 0.003 | `not(THEM(^Straight))` 0.003, `Straight` 0.000 |
| Chicken no ROLE | two-class state `not(THEM(ME))` 0.627 + `not(or(X,THEM(ME)))` 0.372 | -0.352 | 0.164 | `not(THEM(^Straight))` 0.164, `Straight` 0.118, `and(X,THEM(^Swerve))` 0.118, `THEM(^Swerve)` 0.118 |
| Chicken no ROLE | all-`not(THEM(ME))` (frozen mutual Swerve) | 0.000 | 2.000 | `Straight` 2.000, `not(THEM(^Straight))` 2.000, `THEM(^Swerve)` 2.000, `and(X,THEM(^Swerve))` 2.000 |
