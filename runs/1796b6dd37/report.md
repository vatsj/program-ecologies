### arm=weak, n=6, game=pd, N=3000, w=0.3, x_on=True, role=True, mode=square, fmap=exp

programs 3994, classes 112, states 507, terminal classes 1, indeterminate 0, divergence rate 0.0006, flow into polymorphic targets 4.81e-08
mean payoff -0.9887, efficient 0.0000, deadweight loss 0.9887, mean bits in support 3.11

| pi | state |
|---|---|
| 0.9872 | mono {D:1} |
| 0.0110 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 4.08e-06 -> mono {THEM(^C):1}   via THEM(^C) (4.08e-06, rho=7.92e-03 k*=3000)
    - 2.76e-06 -> mono {THEM(^X):1}   via THEM(^X) (2.76e-06, rho=5.61e-03 k*=3000)
    - 2.62e-06 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (2.62e-06, rho=5.61e-03 k*=3000)
    - 7.23e-07 -> mono {THEM(ME):1}   via THEM(ME) (7.23e-07, rho=3.33e-04 k*=3000)
    - 7.21e-07 -> mono {THEM(THEM):1}   via THEM(THEM) (7.21e-07, rho=3.33e-04 k*=3000)
    - 2.01e-07 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (2.01e-07, rho=5.61e-03 k*=3000)
- mono {THEM(^C):1}
    - 1.34e-04 -> mono {THEM(^D):1}   via THEM(^D) (1.34e-04, rho=2.59e-01 k*=3000)
    - 8.31e-05 -> mono {C:1}   via C (8.31e-05, rho=3.33e-04 k*=3000)
    - 6.85e-05 -> mono {THEM(^X):1}   via THEM(^X) (6.85e-05, rho=1.39e-01 k*=3000)
    - 6.52e-05 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (6.52e-05, rho=1.39e-01 k*=3000)
    - 4.98e-06 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (4.98e-06, rho=1.39e-01 k*=3000)
    - 3.36e-06 -> mono {or(ROLE,THEM(^D)):1}   via or(ROLE,THEM(^D)) (3.36e-06, rho=1.40e-01 k*=3000)
