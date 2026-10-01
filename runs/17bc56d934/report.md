### arm=weak, n=6, game=pd, N=10000, w=0.3, x_on=True, role=True, mode=square, fmap=exp

programs 3994, classes 112, states 508, terminal classes 1, indeterminate 0, divergence rate 0.0006, flow into polymorphic targets 2.67e-08
mean payoff -0.9926, efficient 0.0000, deadweight loss 0.9926, mean bits in support 3.08

| pi | state |
|---|---|
| 0.9915 | mono {D:1} |
| 0.0072 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.24e-06 -> mono {THEM(^C):1}   via THEM(^C) (2.24e-06, rho=4.35e-03 k*=10000)
    - 1.51e-06 -> mono {THEM(^X):1}   via THEM(^X) (1.51e-06, rho=3.08e-03 k*=10000)
    - 1.44e-06 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (1.44e-06, rho=3.08e-03 k*=10000)
    - 2.17e-07 -> mono {THEM(ME):1}   via THEM(ME) (2.17e-07, rho=1.00e-04 k*=10000)
    - 2.16e-07 -> mono {THEM(THEM):1}   via THEM(THEM) (2.16e-07, rho=1.00e-04 k*=10000)
    - 1.10e-07 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (1.10e-07, rho=3.08e-03 k*=10000)
- mono {THEM(^C):1}
    - 1.34e-04 -> mono {THEM(^D):1}   via THEM(^D) (1.34e-04, rho=2.59e-01 k*=10000)
    - 6.85e-05 -> mono {THEM(^X):1}   via THEM(^X) (6.85e-05, rho=1.39e-01 k*=10000)
    - 6.52e-05 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (6.52e-05, rho=1.39e-01 k*=10000)
    - 2.49e-05 -> mono {C:1}   via C (2.49e-05, rho=1.00e-04 k*=10000)
    - 4.98e-06 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (4.98e-06, rho=1.39e-01 k*=10000)
    - 3.36e-06 -> mono {or(ROLE,THEM(^D)):1}   via or(ROLE,THEM(^D)) (3.36e-06, rho=1.39e-01 k*=10000)
