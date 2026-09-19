### arm=weak, n=5, game=chicken, N=10, x_on=True, role=True, mode=square

programs 902, classes 53, states 3147, terminal classes 2, indeterminate 0, divergence rate 0.0010
mean payoff 0.5000, efficient 0.5000, deadweight loss 0.0000, mean bits in support 3.03
absorption: class 0: 0.000, class 1: 1.000

| pi | state |
|---|---|
| 0.9849 | mono {ROLE:1} |
| 0.0141 | mono {not(ROLE):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 3.64e-05 -> neutral {ROLE:0.9, not(THEM(^ROLE)):0.1}   via not(THEM(^ROLE)) (3.64e-05)
- mono {not(ROLE):1}
    - 3.64e-05 -> neutral {not(ROLE):0.9, not(THEM(^ROLE)):0.1}   via not(THEM(^ROLE)) (3.64e-05)
