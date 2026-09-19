### arm=weak, n=5, game=chicken_norole, N=100, x_on=True, role=False, mode=square

programs 450, classes 30, states 16744, terminal classes 17, indeterminate 0, divergence rate 0.0027
mean payoff -0.3331, efficient 0.5000, deadweight loss 0.8331, mean bits in support 9.84
absorption: class 6: 0.982, class 0: 0.001, class 2: 0.001, class 4: 0.016, class 10: 0.000, class 14: 0.000, class 17: 0.000, class 13: 0.000, class 22: 0.000, class 24: 0.000, class 26: 0.000, class 27: 0.000, class 29: 0.000, class 30: 0.000, class 32: 0.000, class 33: 0.000, class 34: 0.000

| pi | state |
|---|---|
| 0.9823 | poly {D:0.19, not(THEM(THEM)):0.66, not(THEM(^D)):0.15} |
| 0.0159 | poly {D:0.19, not(THEM(THEM)):0.65, not(THEM(^D)):0.15, or(THEM(ME),C):0.01} |
| 0.0013 | poly {D:0.19, not(THEM(THEM)):0.64, not(THEM(^D)):0.15, or(THEM(ME),C):0.02} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {D:0.19, not(THEM(THEM)):0.66, not(THEM(^D)):0.15}: absorbing (no exits)
- poly {D:0.19, not(THEM(THEM)):0.65, not(THEM(^D)):0.15, or(THEM(ME),C):0.01}: absorbing (no exits)
- poly {D:0.19, not(THEM(THEM)):0.64, not(THEM(^D)):0.15, or(THEM(ME),C):0.02}: absorbing (no exits)
