### arm=weak, n=6, game=pd, N=100, w=0.01, x_on=True, role=False, mode=square

programs 1852, classes 48, states 118, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 1.29e-07
mean payoff -0.6631, efficient 0.0000, deadweight loss 0.6631, mean bits in support 2.77

| pi | state |
|---|---|
| 0.5011 | mono {D:1} |
| 0.2880 | mono {X:1} |
| 0.1841 | mono {C:1} |
| 0.0089 | mono {and(X,X):1} |
| 0.0054 | mono {or(X,X):1} |
| 0.0029 | mono {THEM(ME):1} |
| 0.0029 | mono {THEM(THEM):1} |
| 0.0012 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.39e-03 -> mono {X:1}   via X (2.39e-03, rho=7.67e-03 k*=100)
    - 1.89e-03 -> mono {C:1}   via C (1.89e-03, rho=5.75e-03 k*=100)
    - 6.62e-05 -> mono {and(X,X):1}   via and(X,X) (6.62e-05, rho=8.78e-03 k*=100)
    - 5.02e-05 -> mono {or(X,X):1}   via or(X,X) (5.02e-05, rho=6.66e-03 k*=100)
    - 3.68e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
- mono {X:1}
    - 4.19e-03 -> mono {D:1}   via D (4.19e-03, rho=1.28e-02 k*=100)
    - 2.53e-03 -> mono {C:1}   via C (2.53e-03, rho=7.68e-03 k*=100)
    - 8.54e-05 -> mono {and(X,X):1}   via and(X,X) (8.54e-05, rho=1.13e-02 k*=100)
    - 6.63e-05 -> mono {or(X,X):1}   via or(X,X) (6.63e-05, rho=8.78e-03 k*=100)
    - 3.38e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.38e-05, rho=9.19e-03 k*=100)
    - 3.37e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.37e-05, rho=9.19e-03 k*=100)
- mono {C:1}
    - 5.22e-03 -> mono {D:1}   via D (5.22e-03, rho=1.59e-02 k*=100)
    - 3.98e-03 -> mono {X:1}   via X (3.98e-03, rho=1.27e-02 k*=100)
    - 1.08e-04 -> mono {and(X,X):1}   via and(X,X) (1.08e-04, rho=1.43e-02 k*=100)
    - 8.53e-05 -> mono {or(X,X):1}   via or(X,X) (8.53e-05, rho=1.13e-02 k*=100)
    - 3.09e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.09e-05, rho=8.39e-03 k*=100)
    - 3.08e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.08e-05, rho=8.39e-03 k*=100)
- mono {and(X,X):1}
    - 3.73e-03 -> mono {D:1}   via D (3.73e-03, rho=1.13e-02 k*=100)
    - 2.74e-03 -> mono {X:1}   via X (2.74e-03, rho=8.78e-03 k*=100)
    - 2.19e-03 -> mono {C:1}   via C (2.19e-03, rho=6.67e-03 k*=100)
    - 5.79e-05 -> mono {or(X,X):1}   via or(X,X) (5.79e-05, rho=7.67e-03 k*=100)
    - 3.53e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.53e-05, rho=9.59e-03 k*=100)
    - 3.52e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.52e-05, rho=9.59e-03 k*=100)
- mono {or(X,X):1}
    - 4.69e-03 -> mono {D:1}   via D (4.69e-03, rho=1.43e-02 k*=100)
    - 3.54e-03 -> mono {X:1}   via X (3.54e-03, rho=1.13e-02 k*=100)
    - 2.89e-03 -> mono {C:1}   via C (2.89e-03, rho=8.79e-03 k*=100)
    - 9.61e-05 -> mono {and(X,X):1}   via and(X,X) (9.61e-05, rho=1.27e-02 k*=100)
    - 3.23e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.23e-05, rho=8.79e-03 k*=100)
    - 3.22e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.22e-05, rho=8.79e-03 k*=100)
- mono {THEM(ME):1}
    - 4.51e-03 -> mono {C:1}   via C (4.51e-03, rho=1.37e-02 k*=100)
    - 3.67e-03 -> mono {X:1}   via X (3.67e-03, rho=1.18e-02 k*=100)
    - 3.29e-03 -> mono {D:1}   via D (3.29e-03, rho=1.00e-02 k*=100)
    - 9.59e-05 -> mono {or(X,X):1}   via or(X,X) (9.59e-05, rho=1.27e-02 k*=100)
    - 8.18e-05 -> mono {and(X,X):1}   via and(X,X) (8.18e-05, rho=1.09e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
- mono {THEM(THEM):1}
    - 4.51e-03 -> mono {C:1}   via C (4.51e-03, rho=1.37e-02 k*=100)
    - 3.67e-03 -> mono {X:1}   via X (3.67e-03, rho=1.18e-02 k*=100)
    - 3.29e-03 -> mono {D:1}   via D (3.29e-03, rho=1.00e-02 k*=100)
    - 9.59e-05 -> mono {or(X,X):1}   via or(X,X) (9.59e-05, rho=1.27e-02 k*=100)
    - 8.18e-05 -> mono {and(X,X):1}   via and(X,X) (8.18e-05, rho=1.09e-02 k*=100)
    - 3.68e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-05, rho=1.00e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 2.64e-03 -> mono {X:1}   via X (2.64e-03, rho=8.47e-03 k*=100)
    - 2.34e-03 -> mono {D:1}   via D (2.34e-03, rho=7.12e-03 k*=100)
    - 6.94e-05 -> mono {or(X,X):1}   via or(X,X) (6.94e-05, rho=9.21e-03 k*=100)
    - 5.86e-05 -> mono {and(X,X):1}   via and(X,X) (5.86e-05, rho=7.77e-03 k*=100)
    - 3.09e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.09e-05, rho=8.39e-03 k*=100)
