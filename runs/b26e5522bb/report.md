### arm=weak, n=5, game=demand, N=10, x_on=True, role=True, mode=square

programs 902, classes 53, states 2812, terminal classes 2, indeterminate 0, divergence rate 0.0010
mean payoff 0.4997, efficient 0.5000, deadweight loss 0.0003, mean bits in support 3.20
absorption: class 0: 0.000, class 1: 1.000

| pi | state |
|---|---|
| 0.9380 | mono {ROLE:1} |
| 0.0525 | mono {not(ROLE):1} |
| 0.0068 | poly {D:0.2, not(THEM(^ROLE)):0.8} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 3.64e-05 -> neutral {ROLE:0.9, not(THEM(^ROLE)):0.1}   via not(THEM(^ROLE)) (3.64e-05)
- mono {not(ROLE):1}
    - 3.64e-05 -> neutral {not(ROLE):0.9, not(THEM(^ROLE)):0.1}   via not(THEM(^ROLE)) (3.64e-05)
- poly {D:0.2, not(THEM(^ROLE)):0.8}
    - 3.64e-05 -> mono {and(THEM(THEM),ROLE):1}   via and(THEM(THEM),ROLE) (3.64e-05)
    - 3.64e-05 -> mono {and(THEM(THEM),D):1}   via and(THEM(THEM),D) (3.64e-05)
    - 3.64e-05 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (3.64e-05)
    - 7.29e-06 -> poly {D:0.1, not(THEM(^ROLE)):0.8, and(ROLE,THEM(THEM)):0.1}   via and(ROLE,THEM(THEM)) (7.29e-06)
