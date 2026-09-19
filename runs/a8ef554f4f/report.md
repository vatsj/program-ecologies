### arm=strong, n=6, game=pd, N=1000, w=0.01, x_on=True, role=False, mode=square

programs 1726, classes 21, states 25, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 1.46e-11
mean payoff -0.9953, efficient 0.0000, deadweight loss 0.9953, mean bits in support 2.61

| pi | state |
|---|---|
| 0.9885 | mono {D:1} |
| 0.0072 | mono {X:1} |
| 0.0020 | mono {and(X,X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.02e-05 -> mono {X:1}   via X (1.02e-05, rho=3.26e-05 k*=1000)
    - 3.84e-06 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-06, rho=1.00e-03 k*=1000)
    - 1.75e-06 -> mono {and(X,X):1}   via and(X,X) (1.75e-06, rho=2.19e-04 k*=1000)
    - 1.50e-07 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.50e-07, rho=4.98e-04 k*=1000)
    - 1.41e-07 -> mono {C:1}   via C (1.41e-07, rho=4.25e-07 k*=1000)
    - 1.22e-07 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.22e-07, rho=1.00e-03 k*=1000)
- mono {X:1}
    - 1.68e-03 -> mono {D:1}   via D (1.68e-03, rho=5.05e-03 k*=1000)
    - 2.18e-05 -> mono {and(X,X):1}   via and(X,X) (2.18e-05, rho=2.74e-03 k*=1000)
    - 1.10e-05 -> mono {C:1}   via C (1.10e-05, rho=3.33e-05 k*=1000)
    - 1.77e-06 -> mono {or(X,X):1}   via or(X,X) (1.77e-06, rho=2.21e-04 k*=1000)
    - 1.22e-06 -> mono {THEM(ME):1}   via THEM(ME) (1.22e-06, rho=3.18e-04 k*=1000)
    - 1.16e-06 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.16e-06, rho=3.86e-03 k*=1000)
- mono {and(X,X):1}
    - 9.09e-04 -> mono {D:1}   via D (9.09e-04, rho=2.74e-03 k*=1000)
    - 6.93e-05 -> mono {X:1}   via X (6.93e-05, rho=2.20e-04 k*=1000)
    - 2.34e-06 -> mono {THEM(ME):1}   via THEM(ME) (2.34e-06, rho=6.10e-04 k*=1000)
    - 1.32e-06 -> mono {C:1}   via C (1.32e-06, rho=3.99e-06 k*=1000)
    - 5.30e-07 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (5.30e-07, rho=1.76e-03 k*=1000)
    - 3.34e-07 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (3.34e-07, rho=2.74e-03 k*=1000)
