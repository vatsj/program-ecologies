### arm=weak, n=6, game=pd, N=10000, w=0.1, x_on=True, role=True, mode=square, fmap=exp

programs 3994, classes 112, states 508, terminal classes 1, indeterminate 0, divergence rate 0.0006, flow into polymorphic targets 1.51e-08
mean payoff -0.9896, efficient 0.0000, deadweight loss 0.9896, mean bits in support 3.11

| pi | state |
|---|---|
| 0.9882 | mono {D:1} |
| 0.0101 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.30e-06 -> mono {THEM(^C):1}   via THEM(^C) (1.30e-06, rho=2.52e-03 k*=10000)
    - 8.75e-07 -> mono {THEM(^X):1}   via THEM(^X) (8.75e-07, rho=1.78e-03 k*=10000)
    - 8.33e-07 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (8.33e-07, rho=1.78e-03 k*=10000)
    - 2.17e-07 -> mono {THEM(ME):1}   via THEM(ME) (2.17e-07, rho=1.00e-04 k*=10000)
    - 2.16e-07 -> mono {THEM(THEM):1}   via THEM(THEM) (2.16e-07, rho=1.00e-04 k*=10000)
    - 6.37e-08 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (6.37e-08, rho=1.78e-03 k*=10000)
- mono {THEM(^C):1}
    - 4.91e-05 -> mono {THEM(^D):1}   via THEM(^D) (4.91e-05, rho=9.52e-02 k*=10000)
    - 2.49e-05 -> mono {C:1}   via C (2.49e-05, rho=1.00e-04 k*=10000)
    - 2.40e-05 -> mono {THEM(^X):1}   via THEM(^X) (2.40e-05, rho=4.88e-02 k*=10000)
    - 2.28e-05 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (2.28e-05, rho=4.88e-02 k*=10000)
    - 1.74e-06 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (1.74e-06, rho=4.88e-02 k*=10000)
    - 1.18e-06 -> mono {or(ROLE,THEM(^D)):1}   via or(ROLE,THEM(^D)) (1.18e-06, rho=4.89e-02 k*=10000)
