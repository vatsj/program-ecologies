### arm=weak, n=6, game=pd, N=3000, w=0.1, x_on=True, role=True, mode=square, fmap=exp

programs 3994, classes 112, states 479, terminal classes 1, indeterminate 0, divergence rate 0.0006, flow into polymorphic targets 2.63e-08
mean payoff -0.9868, efficient 0.0000, deadweight loss 0.9868, mean bits in support 3.14

| pi | state |
|---|---|
| 0.9849 | mono {D:1} |
| 0.0126 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.36e-06 -> mono {THEM(^C):1}   via THEM(^C) (2.36e-06, rho=4.59e-03 k*=3000)
    - 1.60e-06 -> mono {THEM(^X):1}   via THEM(^X) (1.60e-06, rho=3.25e-03 k*=3000)
    - 1.52e-06 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (1.52e-06, rho=3.25e-03 k*=3000)
    - 7.23e-07 -> mono {THEM(ME):1}   via THEM(ME) (7.23e-07, rho=3.33e-04 k*=3000)
    - 7.21e-07 -> mono {THEM(THEM):1}   via THEM(THEM) (7.21e-07, rho=3.33e-04 k*=3000)
    - 1.72e-07 -> mono {THEM(^D):1}   via THEM(^D) (1.72e-07, rho=3.33e-04 k*=3000)
- mono {THEM(^C):1}
    - 8.31e-05 -> mono {C:1}   via C (8.31e-05, rho=3.33e-04 k*=3000)
    - 4.91e-05 -> mono {THEM(^D):1}   via THEM(^D) (4.91e-05, rho=9.52e-02 k*=3000)
    - 2.40e-05 -> mono {THEM(^X):1}   via THEM(^X) (2.40e-05, rho=4.88e-02 k*=3000)
    - 2.28e-05 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (2.28e-05, rho=4.88e-02 k*=3000)
    - 1.75e-06 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (1.75e-06, rho=4.88e-02 k*=3000)
    - 1.18e-06 -> mono {or(ROLE,THEM(^D)):1}   via or(ROLE,THEM(^D)) (1.18e-06, rho=4.91e-02 k*=3000)
