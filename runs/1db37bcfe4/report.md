### arm=weak, n=6, game=pd, N=30000, w=0.1, x_on=True, role=True, mode=square, fmap=exp

programs 3994, classes 112, states 506, terminal classes 1, indeterminate 0, divergence rate 0.0006, flow into polymorphic targets 8.82e-09
mean payoff -0.9931, efficient 0.0000, deadweight loss 0.9931, mean bits in support 3.07

| pi | state |
|---|---|
| 0.9920 | mono {D:1} |
| 0.0068 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 7.50e-07 -> mono {THEM(^C):1}   via THEM(^C) (7.50e-07, rho=1.45e-03 k*=30000)
    - 5.06e-07 -> mono {THEM(^X):1}   via THEM(^X) (5.06e-07, rho=1.03e-03 k*=30000)
    - 4.81e-07 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (4.81e-07, rho=1.03e-03 k*=30000)
    - 7.23e-08 -> mono {THEM(ME):1}   via THEM(ME) (7.23e-08, rho=3.33e-05 k*=30000)
    - 7.21e-08 -> mono {THEM(THEM):1}   via THEM(THEM) (7.21e-08, rho=3.33e-05 k*=30000)
    - 3.68e-08 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (3.68e-08, rho=1.03e-03 k*=30000)
- mono {THEM(^C):1}
    - 4.91e-05 -> mono {THEM(^D):1}   via THEM(^D) (4.91e-05, rho=9.52e-02 k*=30000)
    - 2.40e-05 -> mono {THEM(^X):1}   via THEM(^X) (2.40e-05, rho=4.88e-02 k*=30000)
    - 2.28e-05 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (2.28e-05, rho=4.88e-02 k*=30000)
    - 8.31e-06 -> mono {C:1}   via C (8.31e-06, rho=3.33e-05 k*=30000)
    - 1.74e-06 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (1.74e-06, rho=4.88e-02 k*=30000)
    - 1.18e-06 -> mono {or(ROLE,THEM(^D)):1}   via or(ROLE,THEM(^D)) (1.18e-06, rho=4.88e-02 k*=30000)
