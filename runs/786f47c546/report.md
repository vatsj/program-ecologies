### arm=weak, n=5, game=chicken_norole, N=10, x_on=True, role=False, mode=square

programs 450, classes 30, states 1755, terminal classes 2, indeterminate 0, divergence rate 0.0027
mean payoff -0.2700, efficient 0.5000, deadweight loss 0.7700, mean bits in support 9.92
absorption: class 0: 0.706, class 5: 0.294

| pi | state |
|---|---|
| 0.7059 | poly {D:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.5, not(THEM(^D)):0.1, or(THEM(ME),C):0.1} |
| 0.2941 | poly {D:0.2, not(THEM(ME)):0.5, not(THEM(THEM)):0.1, not(THEM(^D)):0.1, or(THEM(ME),C):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {D:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.5, not(THEM(^D)):0.1, or(THEM(ME),C):0.1}: absorbing (no exits)
- poly {D:0.2, not(THEM(ME)):0.5, not(THEM(THEM)):0.1, not(THEM(^D)):0.1, or(THEM(ME),C):0.1}: absorbing (no exits)
