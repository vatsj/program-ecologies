### arm=weak, n=6, game=pd, N=30000, w=0.3, x_on=True, role=True, mode=square, fmap=exp

programs 3994, classes 112, states 506, terminal classes 1, indeterminate 0, divergence rate 0.0006, flow into polymorphic targets 1.53e-08
mean payoff -0.9955, efficient 0.0000, deadweight loss 0.9955, mean bits in support 3.05

| pi | state |
|---|---|
| 0.9945 | mono {D:1} |
| 0.0044 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.30e-06 -> mono {THEM(^C):1}   via THEM(^C) (1.30e-06, rho=2.52e-03 k*=30000)
    - 8.75e-07 -> mono {THEM(^X):1}   via THEM(^X) (8.75e-07, rho=1.78e-03 k*=30000)
    - 8.33e-07 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (8.33e-07, rho=1.78e-03 k*=30000)
    - 7.23e-08 -> mono {THEM(ME):1}   via THEM(ME) (7.23e-08, rho=3.33e-05 k*=30000)
    - 7.21e-08 -> mono {THEM(THEM):1}   via THEM(THEM) (7.21e-08, rho=3.33e-05 k*=30000)
    - 6.37e-08 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (6.37e-08, rho=1.78e-03 k*=30000)
- mono {THEM(^C):1}
    - 1.34e-04 -> mono {THEM(^D):1}   via THEM(^D) (1.34e-04, rho=2.59e-01 k*=30000)
    - 6.84e-05 -> mono {THEM(^X):1}   via THEM(^X) (6.84e-05, rho=1.39e-01 k*=30000)
    - 6.51e-05 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (6.51e-05, rho=1.39e-01 k*=30000)
    - 8.31e-06 -> mono {C:1}   via C (8.31e-06, rho=3.33e-05 k*=30000)
    - 4.98e-06 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (4.98e-06, rho=1.39e-01 k*=30000)
    - 3.36e-06 -> mono {or(ROLE,THEM(^D)):1}   via or(ROLE,THEM(^D)) (3.36e-06, rho=1.39e-01 k*=30000)
