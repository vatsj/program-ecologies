### arm=strong, n=6, game=stag, N=10, x_on=True, role=False, mode=square

programs 1726, classes 21, states 235, terminal classes 2, indeterminate 0, divergence rate 0.0004
mean payoff 4.0000, efficient 4.0000, deadweight loss 0.0000, mean bits in support 3.34
absorption: class 0: 0.659, class 1: 0.341

| pi | state |
|---|---|
| 0.6589 | poly {C:0.9, THEM(ME):9.94e-09, or(X,THEM(ME)):0.1} |
| 0.3406 | mono {C:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {C:0.9, THEM(ME):9.94e-09, or(X,THEM(ME)):0.1}: absorbing (no exits)
- mono {C:1}
    - 9.32e-05 -> neutral {C:0.9, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (9.32e-05)
