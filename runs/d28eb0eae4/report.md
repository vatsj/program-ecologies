### arm=weak, n=6, game=pd, N=30000, w=1.0, x_on=True, role=True, mode=square, fmap=exp

programs 3994, classes 112, states 506, terminal classes 1, indeterminate 0, divergence rate 0.0006, flow into polymorphic targets 2.87e-08
mean payoff -0.9968, efficient 0.0000, deadweight loss 0.9968, mean bits in support 3.04

| pi | state |
|---|---|
| 0.9959 | mono {D:1} |
| 0.0031 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.36e-06 -> mono {THEM(^C):1}   via THEM(^C) (2.36e-06, rho=4.59e-03 k*=30000)
    - 1.60e-06 -> mono {THEM(^X):1}   via THEM(^X) (1.60e-06, rho=3.25e-03 k*=30000)
    - 1.52e-06 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (1.52e-06, rho=3.25e-03 k*=30000)
    - 1.16e-07 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (1.16e-07, rho=3.25e-03 k*=30000)
    - 7.23e-08 -> mono {THEM(ME):1}   via THEM(ME) (7.23e-08, rho=3.33e-05 k*=30000)
    - 7.21e-08 -> mono {THEM(THEM):1}   via THEM(THEM) (7.21e-08, rho=3.33e-05 k*=30000)
- mono {THEM(^C):1}
    - 3.26e-04 -> mono {THEM(^D):1}   via THEM(^D) (3.26e-04, rho=6.32e-01 k*=30000)
    - 1.93e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.93e-04, rho=3.93e-01 k*=30000)
    - 1.84e-04 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (1.84e-04, rho=3.93e-01 k*=30000)
    - 1.41e-05 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (1.41e-05, rho=3.93e-01 k*=30000)
    - 9.48e-06 -> mono {or(ROLE,THEM(^D)):1}   via or(ROLE,THEM(^D)) (9.48e-06, rho=3.94e-01 k*=30000)
    - 8.31e-06 -> mono {C:1}   via C (8.31e-06, rho=3.33e-05 k*=30000)
