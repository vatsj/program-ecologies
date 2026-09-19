### arm=weak, n=7, game=pd, N=10, w=0.01, x_on=True, role=False, mode=sparse

programs 9426, classes 105, states 851, terminal classes 1, indeterminate 0, divergence rate 0.0131, flow into polymorphic targets 4.54e-06
mean payoff -0.5231, efficient 0.0000, deadweight loss 0.5231, mean bits in support 2.81

| pi | state |
|---|---|
| 0.3469 | mono {D:1} |
| 0.3110 | mono {C:1} |
| 0.3102 | mono {X:1} |
| 0.0083 | mono {and(X,X):1} |
| 0.0079 | mono {or(X,X):1} |
| 0.0073 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.11e-02 -> mono {C:1}   via C (3.11e-02, rho=9.45e-02 k*=10)
    - 3.02e-02 -> mono {X:1}   via X (3.02e-02, rho=9.72e-02 k*=10)
    - 7.98e-04 -> mono {and(X,X):1}   via and(X,X) (7.98e-04, rho=9.86e-02 k*=10)
    - 7.75e-04 -> mono {or(X,X):1}   via or(X,X) (7.75e-04, rho=9.59e-02 k*=10)
    - 7.46e-04 -> mono {THEM(ME):1}   via THEM(ME) (7.46e-04, rho=1.00e-01 k*=10)
    - 9.60e-05 -> mono {THEM(^C):1}   via THEM(^C) (9.60e-05, rho=1.01e-01 k*=10)
- mono {C:1}
    - 3.47e-02 -> mono {D:1}   via D (3.47e-02, rho=1.06e-01 k*=10)
    - 3.19e-02 -> mono {X:1}   via X (3.19e-02, rho=1.03e-01 k*=10)
    - 8.43e-04 -> mono {and(X,X):1}   via and(X,X) (8.43e-04, rho=1.04e-01 k*=10)
    - 8.20e-04 -> mono {or(X,X):1}   via or(X,X) (8.20e-04, rho=1.01e-01 k*=10)
    - 7.36e-04 -> mono {THEM(ME):1}   via THEM(ME) (7.36e-04, rho=9.87e-02 k*=10)
    - 9.48e-05 -> mono {THEM(^C):1}   via THEM(^C) (9.48e-05, rho=1.00e-01 k*=10)
- mono {X:1}
    - 3.38e-02 -> mono {D:1}   via D (3.38e-02, rho=1.03e-01 k*=10)
    - 3.20e-02 -> mono {C:1}   via C (3.20e-02, rho=9.73e-02 k*=10)
    - 8.20e-04 -> mono {and(X,X):1}   via and(X,X) (8.20e-04, rho=1.01e-01 k*=10)
    - 7.98e-04 -> mono {or(X,X):1}   via or(X,X) (7.98e-04, rho=9.86e-02 k*=10)
    - 7.41e-04 -> mono {THEM(ME):1}   via THEM(ME) (7.41e-04, rho=9.93e-02 k*=10)
    - 9.54e-05 -> mono {THEM(^C):1}   via THEM(^C) (9.54e-05, rho=1.01e-01 k*=10)
- mono {and(X,X):1}
    - 3.33e-02 -> mono {D:1}   via D (3.33e-02, rho=1.01e-01 k*=10)
    - 3.15e-02 -> mono {C:1}   via C (3.15e-02, rho=9.59e-02 k*=10)
    - 3.06e-02 -> mono {X:1}   via X (3.06e-02, rho=9.86e-02 k*=10)
    - 7.86e-04 -> mono {or(X,X):1}   via or(X,X) (7.86e-04, rho=9.73e-02 k*=10)
    - 7.44e-04 -> mono {THEM(ME):1}   via THEM(ME) (7.44e-04, rho=9.97e-02 k*=10)
    - 9.57e-05 -> mono {THEM(^C):1}   via THEM(^C) (9.57e-05, rho=1.01e-01 k*=10)
- mono {or(X,X):1}
    - 3.42e-02 -> mono {D:1}   via D (3.42e-02, rho=1.04e-01 k*=10)
    - 3.24e-02 -> mono {C:1}   via C (3.24e-02, rho=9.86e-02 k*=10)
    - 3.15e-02 -> mono {X:1}   via X (3.15e-02, rho=1.01e-01 k*=10)
    - 8.31e-04 -> mono {and(X,X):1}   via and(X,X) (8.31e-04, rho=1.03e-01 k*=10)
    - 7.39e-04 -> mono {THEM(ME):1}   via THEM(ME) (7.39e-04, rho=9.90e-02 k*=10)
    - 9.51e-05 -> mono {THEM(^C):1}   via THEM(^C) (9.51e-05, rho=1.00e-01 k*=10)
- mono {THEM(ME):1}
    - 3.38e-02 -> mono {C:1}   via C (3.38e-02, rho=1.03e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 3.15e-02 -> mono {X:1}   via X (3.15e-02, rho=1.01e-01 k*=10)
    - 8.25e-04 -> mono {or(X,X):1}   via or(X,X) (8.25e-04, rho=1.02e-01 k*=10)
    - 8.14e-04 -> mono {and(X,X):1}   via and(X,X) (8.14e-04, rho=1.01e-01 k*=10)
    - 9.73e-05 -> mono {THEM(^C):1}   via THEM(^C) (9.73e-05, rho=1.03e-01 k*=10)
