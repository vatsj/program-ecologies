### arm=weak, n=7, game=pd, N=10, w=0.1, x_on=True, role=False, mode=sparse

programs 9426, classes 105, states 843, terminal classes 1, indeterminate 0, divergence rate 0.0131, flow into polymorphic targets 3.53e-06
mean payoff -0.6851, efficient 0.0000, deadweight loss 0.6851, mean bits in support 2.79

| pi | state |
|---|---|
| 0.5273 | mono {D:1} |
| 0.2764 | mono {X:1} |
| 0.1675 | mono {C:1} |
| 0.0096 | mono {and(X,X):1} |
| 0.0062 | mono {THEM(ME):1} |
| 0.0054 | mono {or(X,X):1} |
| 0.0012 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.25e-02 -> mono {X:1}   via X (2.25e-02, rho=7.26e-02 k*=10)
    - 1.69e-02 -> mono {C:1}   via C (1.69e-02, rho=5.13e-02 k*=10)
    - 7.46e-04 -> mono {THEM(ME):1}   via THEM(ME) (7.46e-04, rho=1.00e-01 k*=10)
    - 6.91e-04 -> mono {and(X,X):1}   via and(X,X) (6.91e-04, rho=8.55e-02 k*=10)
    - 4.95e-04 -> mono {or(X,X):1}   via or(X,X) (4.95e-04, rho=6.12e-02 k*=10)
    - 1.08e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.08e-04, rho=1.14e-01 k*=10)
- mono {X:1}
    - 4.33e-02 -> mono {D:1}   via D (4.33e-02, rho=1.32e-01 k*=10)
    - 2.43e-02 -> mono {C:1}   via C (2.43e-02, rho=7.39e-02 k*=10)
    - 9.31e-04 -> mono {and(X,X):1}   via and(X,X) (9.31e-04, rho=1.15e-01 k*=10)
    - 6.97e-04 -> mono {or(X,X):1}   via or(X,X) (6.97e-04, rho=8.62e-02 k*=10)
    - 6.93e-04 -> mono {THEM(ME):1}   via THEM(ME) (6.93e-04, rho=9.29e-02 k*=10)
    - 1.01e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.01e-04, rho=1.07e-01 k*=10)
- mono {C:1}
    - 5.40e-02 -> mono {D:1}   via D (5.40e-02, rho=1.64e-01 k*=10)
    - 4.03e-02 -> mono {X:1}   via X (4.03e-02, rho=1.30e-01 k*=10)
    - 1.19e-03 -> mono {and(X,X):1}   via and(X,X) (1.19e-03, rho=1.47e-01 k*=10)
    - 9.25e-04 -> mono {or(X,X):1}   via or(X,X) (9.25e-04, rho=1.14e-01 k*=10)
    - 6.44e-04 -> mono {THEM(ME):1}   via THEM(ME) (6.44e-04, rho=8.64e-02 k*=10)
    - 1.32e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.32e-04, rho=1.64e-01 k*=10)
- mono {and(X,X):1}
    - 3.80e-02 -> mono {D:1}   via D (3.80e-02, rho=1.16e-01 k*=10)
    - 2.67e-02 -> mono {X:1}   via X (2.67e-02, rho=8.59e-02 k*=10)
    - 2.04e-02 -> mono {C:1}   via C (2.04e-02, rho=6.21e-02 k*=10)
    - 7.19e-04 -> mono {THEM(ME):1}   via THEM(ME) (7.19e-04, rho=9.64e-02 k*=10)
    - 5.92e-04 -> mono {or(X,X):1}   via or(X,X) (5.92e-04, rho=7.32e-02 k*=10)
    - 1.05e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.05e-04, rho=1.11e-01 k*=10)
- mono {THEM(ME):1}
    - 4.29e-02 -> mono {C:1}   via C (4.29e-02, rho=1.31e-01 k*=10)
    - 3.57e-02 -> mono {X:1}   via X (3.57e-02, rho=1.15e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 9.93e-04 -> mono {or(X,X):1}   via or(X,X) (9.93e-04, rho=1.23e-01 k*=10)
    - 8.69e-04 -> mono {and(X,X):1}   via and(X,X) (8.69e-04, rho=1.07e-01 k*=10)
    - 1.24e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.24e-04, rho=1.31e-01 k*=10)
- mono {or(X,X):1}
    - 4.86e-02 -> mono {D:1}   via D (4.86e-02, rho=1.48e-01 k*=10)
    - 3.56e-02 -> mono {X:1}   via X (3.56e-02, rho=1.15e-01 k*=10)
    - 2.85e-02 -> mono {C:1}   via C (2.85e-02, rho=8.66e-02 k*=10)
    - 1.06e-03 -> mono {and(X,X):1}   via and(X,X) (1.06e-03, rho=1.31e-01 k*=10)
    - 6.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (6.68e-04, rho=8.96e-02 k*=10)
    - 1.02e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.02e-04, rho=1.27e-01 k*=10)
- mono {THEM(^C):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 2.70e-02 -> mono {X:1}   via X (2.70e-02, rho=8.69e-02 k*=10)
    - 2.45e-02 -> mono {D:1}   via D (2.45e-02, rho=7.44e-02 k*=10)
    - 7.55e-04 -> mono {or(X,X):1}   via or(X,X) (7.55e-04, rho=9.34e-02 k*=10)
    - 6.52e-04 -> mono {and(X,X):1}   via and(X,X) (6.52e-04, rho=8.06e-02 k*=10)
    - 6.44e-04 -> mono {THEM(ME):1}   via THEM(ME) (6.44e-04, rho=8.64e-02 k*=10)
