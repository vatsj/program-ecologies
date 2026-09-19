### arm=strong, n=7, game=pd, N=10, w=0.1, x_on=True, role=False, mode=sparse

programs 8770, classes 44, states 349, terminal classes 1, indeterminate 0, divergence rate 0.0058, flow into polymorphic targets 1.16e-06
mean payoff -0.6861, efficient 0.0000, deadweight loss 0.6861, mean bits in support 2.73

| pi | state |
|---|---|
| 0.5329 | mono {D:1} |
| 0.2774 | mono {X:1} |
| 0.1676 | mono {C:1} |
| 0.0102 | mono {and(X,X):1} |
| 0.0057 | mono {or(X,X):1} |
| 0.0032 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.27e-02 -> mono {X:1}   via X (2.27e-02, rho=7.26e-02 k*=10)
    - 1.70e-02 -> mono {C:1}   via C (1.70e-02, rho=5.13e-02 k*=10)
    - 7.32e-04 -> mono {and(X,X):1}   via and(X,X) (7.32e-04, rho=8.55e-02 k*=10)
    - 5.24e-04 -> mono {or(X,X):1}   via or(X,X) (5.24e-04, rho=6.12e-02 k*=10)
    - 3.90e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.90e-04, rho=1.00e-01 k*=10)
    - 3.99e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (3.99e-05, rho=9.26e-02 k*=10)
- mono {X:1}
    - 4.36e-02 -> mono {D:1}   via D (4.36e-02, rho=1.32e-01 k*=10)
    - 2.45e-02 -> mono {C:1}   via C (2.45e-02, rho=7.39e-02 k*=10)
    - 9.86e-04 -> mono {and(X,X):1}   via and(X,X) (9.86e-04, rho=1.15e-01 k*=10)
    - 7.39e-04 -> mono {or(X,X):1}   via or(X,X) (7.39e-04, rho=8.62e-02 k*=10)
    - 3.62e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.62e-04, rho=9.29e-02 k*=10)
    - 7.95e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.95e-05, rho=9.29e-02 k*=10)
- mono {C:1}
    - 5.45e-02 -> mono {D:1}   via D (5.45e-02, rho=1.64e-01 k*=10)
    - 4.06e-02 -> mono {X:1}   via X (4.06e-02, rho=1.30e-01 k*=10)
    - 1.26e-03 -> mono {and(X,X):1}   via and(X,X) (1.26e-03, rho=1.47e-01 k*=10)
    - 9.80e-04 -> mono {or(X,X):1}   via or(X,X) (9.80e-04, rho=1.14e-01 k*=10)
    - 3.36e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.36e-04, rho=8.64e-02 k*=10)
    - 1.41e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.41e-04, rho=1.64e-01 k*=10)
- mono {and(X,X):1}
    - 3.83e-02 -> mono {D:1}   via D (3.83e-02, rho=1.16e-01 k*=10)
    - 2.68e-02 -> mono {X:1}   via X (2.68e-02, rho=8.59e-02 k*=10)
    - 2.06e-02 -> mono {C:1}   via C (2.06e-02, rho=6.21e-02 k*=10)
    - 6.27e-04 -> mono {or(X,X):1}   via or(X,X) (6.27e-04, rho=7.32e-02 k*=10)
    - 3.75e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.75e-04, rho=9.64e-02 k*=10)
    - 5.46e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (5.46e-05, rho=6.39e-02 k*=10)
- mono {or(X,X):1}
    - 4.90e-02 -> mono {D:1}   via D (4.90e-02, rho=1.48e-01 k*=10)
    - 3.58e-02 -> mono {X:1}   via X (3.58e-02, rho=1.15e-01 k*=10)
    - 2.87e-02 -> mono {C:1}   via C (2.87e-02, rho=8.66e-02 k*=10)
    - 1.12e-03 -> mono {and(X,X):1}   via and(X,X) (1.12e-03, rho=1.31e-01 k*=10)
    - 3.49e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.49e-04, rho=8.96e-02 k*=10)
    - 1.09e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.09e-04, rho=1.27e-01 k*=10)
- mono {THEM(ME):1}
    - 4.33e-02 -> mono {C:1}   via C (4.33e-02, rho=1.31e-01 k*=10)
    - 3.59e-02 -> mono {X:1}   via X (3.59e-02, rho=1.15e-01 k*=10)
    - 3.31e-02 -> mono {D:1}   via D (3.31e-02, rho=1.00e-01 k*=10)
    - 1.05e-03 -> mono {or(X,X):1}   via or(X,X) (1.05e-03, rho=1.23e-01 k*=10)
    - 9.21e-04 -> mono {and(X,X):1}   via and(X,X) (9.21e-04, rho=1.07e-01 k*=10)
    - 8.55e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.55e-05, rho=1.00e-01 k*=10)
