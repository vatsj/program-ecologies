### arm=weak, n=7, game=pd, N=100, w=0.01, x_on=True, role=False, mode=sparse

programs 9426, classes 105, states 671, terminal classes 1, indeterminate 0, divergence rate 0.0118, flow into polymorphic targets 3.11e-07
mean payoff -0.6632, efficient 0.0000, deadweight loss 0.6632, mean bits in support 2.78

| pi | state |
|---|---|
| 0.5011 | mono {D:1} |
| 0.2864 | mono {X:1} |
| 0.1842 | mono {C:1} |
| 0.0096 | mono {and(X,X):1} |
| 0.0060 | mono {THEM(ME):1} |
| 0.0058 | mono {or(X,X):1} |
| 0.0012 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.38e-03 -> mono {X:1}   via X (2.38e-03, rho=7.67e-03 k*=100)
    - 1.89e-03 -> mono {C:1}   via C (1.89e-03, rho=5.75e-03 k*=100)
    - 7.46e-05 -> mono {THEM(ME):1}   via THEM(ME) (7.46e-05, rho=1.00e-02 k*=100)
    - 7.10e-05 -> mono {and(X,X):1}   via and(X,X) (7.10e-05, rho=8.78e-03 k*=100)
    - 5.38e-05 -> mono {or(X,X):1}   via or(X,X) (5.38e-05, rho=6.66e-03 k*=100)
    - 1.11e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.11e-05, rho=1.17e-02 k*=100)
- mono {X:1}
    - 4.19e-03 -> mono {D:1}   via D (4.19e-03, rho=1.28e-02 k*=100)
    - 2.52e-03 -> mono {C:1}   via C (2.52e-03, rho=7.68e-03 k*=100)
    - 9.16e-05 -> mono {and(X,X):1}   via and(X,X) (9.16e-05, rho=1.13e-02 k*=100)
    - 7.10e-05 -> mono {or(X,X):1}   via or(X,X) (7.10e-05, rho=8.78e-03 k*=100)
    - 6.85e-05 -> mono {THEM(ME):1}   via THEM(ME) (6.85e-05, rho=9.19e-03 k*=100)
    - 1.03e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.03e-05, rho=1.08e-02 k*=100)
- mono {C:1}
    - 5.22e-03 -> mono {D:1}   via D (5.22e-03, rho=1.59e-02 k*=100)
    - 3.95e-03 -> mono {X:1}   via X (3.95e-03, rho=1.27e-02 k*=100)
    - 1.15e-04 -> mono {and(X,X):1}   via and(X,X) (1.15e-04, rho=1.43e-02 k*=100)
    - 9.15e-05 -> mono {or(X,X):1}   via or(X,X) (9.15e-05, rho=1.13e-02 k*=100)
    - 6.26e-05 -> mono {THEM(ME):1}   via THEM(ME) (6.26e-05, rho=8.39e-03 k*=100)
    - 1.27e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.27e-05, rho=1.59e-02 k*=100)
- mono {and(X,X):1}
    - 3.72e-03 -> mono {D:1}   via D (3.72e-03, rho=1.13e-02 k*=100)
    - 2.73e-03 -> mono {X:1}   via X (2.73e-03, rho=8.78e-03 k*=100)
    - 2.19e-03 -> mono {C:1}   via C (2.19e-03, rho=6.67e-03 k*=100)
    - 7.16e-05 -> mono {THEM(ME):1}   via THEM(ME) (7.16e-05, rho=9.59e-03 k*=100)
    - 6.20e-05 -> mono {or(X,X):1}   via or(X,X) (6.20e-05, rho=7.67e-03 k*=100)
    - 1.07e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.07e-05, rho=1.12e-02 k*=100)
- mono {THEM(ME):1}
    - 4.51e-03 -> mono {C:1}   via C (4.51e-03, rho=1.37e-02 k*=100)
    - 3.65e-03 -> mono {X:1}   via X (3.65e-03, rho=1.18e-02 k*=100)
    - 3.29e-03 -> mono {D:1}   via D (3.29e-03, rho=1.00e-02 k*=100)
    - 1.03e-04 -> mono {or(X,X):1}   via or(X,X) (1.03e-04, rho=1.27e-02 k*=100)
    - 8.77e-05 -> mono {and(X,X):1}   via and(X,X) (8.77e-05, rho=1.09e-02 k*=100)
    - 1.30e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.30e-05, rho=1.37e-02 k*=100)
- mono {or(X,X):1}
    - 4.69e-03 -> mono {D:1}   via D (4.69e-03, rho=1.43e-02 k*=100)
    - 3.51e-03 -> mono {X:1}   via X (3.51e-03, rho=1.13e-02 k*=100)
    - 2.89e-03 -> mono {C:1}   via C (2.89e-03, rho=8.79e-03 k*=100)
    - 1.03e-04 -> mono {and(X,X):1}   via and(X,X) (1.03e-04, rho=1.27e-02 k*=100)
    - 6.56e-05 -> mono {THEM(ME):1}   via THEM(ME) (6.56e-05, rho=8.79e-03 k*=100)
    - 9.87e-06 -> mono {THEM(^C):1}   via THEM(^C) (9.87e-06, rho=1.04e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 2.63e-03 -> mono {X:1}   via X (2.63e-03, rho=8.47e-03 k*=100)
    - 2.34e-03 -> mono {D:1}   via D (2.34e-03, rho=7.12e-03 k*=100)
    - 7.45e-05 -> mono {or(X,X):1}   via or(X,X) (7.45e-05, rho=9.21e-03 k*=100)
    - 6.28e-05 -> mono {and(X,X):1}   via and(X,X) (6.28e-05, rho=7.77e-03 k*=100)
    - 6.26e-05 -> mono {THEM(ME):1}   via THEM(ME) (6.26e-05, rho=8.39e-03 k*=100)
