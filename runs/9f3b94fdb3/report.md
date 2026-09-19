### arm=weak, n=6, game=exchange, N=100, w=0.01, x_on=True, role=False, mode=square

programs 1852, classes 48, states 409, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 1.47e-05
mean payoff 0.6774, efficient 2.0000, deadweight loss 1.3226, mean bits in support 2.77

| pi | state |
|---|---|
| 0.5005 | mono {D:1} |
| 0.2880 | mono {X:1} |
| 0.1853 | mono {C:1} |
| 0.0089 | mono {and(X,X):1} |
| 0.0054 | mono {or(X,X):1} |
| 0.0024 | mono {THEM(ME):1} |
| 0.0024 | mono {THEM(THEM):1} |
| 0.0015 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.40e-03 -> mono {X:1}   via X (2.40e-03, rho=7.67e-03 k*=100)
    - 1.90e-03 -> mono {C:1}   via C (1.90e-03, rho=5.77e-03 k*=100)
    - 6.62e-05 -> mono {and(X,X):1}   via and(X,X) (6.62e-05, rho=8.78e-03 k*=100)
    - 5.03e-05 -> mono {or(X,X):1}   via or(X,X) (5.03e-05, rho=6.67e-03 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
- mono {X:1}
    - 4.19e-03 -> mono {D:1}   via D (4.19e-03, rho=1.27e-02 k*=100)
    - 2.53e-03 -> mono {C:1}   via C (2.53e-03, rho=7.69e-03 k*=100)
    - 8.53e-05 -> mono {and(X,X):1}   via and(X,X) (8.53e-05, rho=1.13e-02 k*=100)
    - 6.63e-05 -> mono {or(X,X):1}   via or(X,X) (6.63e-05, rho=8.79e-03 k*=100)
    - 3.11e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.11e-05, rho=8.41e-03 k*=100)
    - 3.08e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.08e-05, rho=8.41e-03 k*=100)
- mono {C:1}
    - 5.21e-03 -> mono {D:1}   via D (5.21e-03, rho=1.58e-02 k*=100)
    - 3.97e-03 -> mono {X:1}   via X (3.97e-03, rho=1.27e-02 k*=100)
    - 1.07e-04 -> mono {and(X,X):1}   via and(X,X) (1.07e-04, rho=1.42e-02 k*=100)
    - 8.52e-05 -> mono {or(X,X):1}   via or(X,X) (8.52e-05, rho=1.13e-02 k*=100)
    - 2.56e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.56e-05, rho=6.93e-03 k*=100)
    - 2.54e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.54e-05, rho=6.93e-03 k*=100)
- mono {and(X,X):1}
    - 3.72e-03 -> mono {D:1}   via D (3.72e-03, rho=1.13e-02 k*=100)
    - 2.74e-03 -> mono {X:1}   via X (2.74e-03, rho=8.79e-03 k*=100)
    - 2.20e-03 -> mono {C:1}   via C (2.20e-03, rho=6.68e-03 k*=100)
    - 5.79e-05 -> mono {or(X,X):1}   via or(X,X) (5.79e-05, rho=7.68e-03 k*=100)
    - 3.39e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.39e-05, rho=9.19e-03 k*=100)
    - 3.37e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.37e-05, rho=9.19e-03 k*=100)
- mono {or(X,X):1}
    - 4.69e-03 -> mono {D:1}   via D (4.69e-03, rho=1.42e-02 k*=100)
    - 3.53e-03 -> mono {X:1}   via X (3.53e-03, rho=1.13e-02 k*=100)
    - 2.89e-03 -> mono {C:1}   via C (2.89e-03, rho=8.80e-03 k*=100)
    - 9.60e-05 -> mono {and(X,X):1}   via and(X,X) (9.60e-05, rho=1.27e-02 k*=100)
    - 2.83e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.83e-05, rho=7.65e-03 k*=100)
    - 2.81e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.81e-05, rho=7.65e-03 k*=100)
- mono {THEM(ME):1}
    - 6.00e-03 -> mono {C:1}   via C (6.00e-03, rho=1.82e-02 k*=100)
    - 4.27e-03 -> mono {X:1}   via X (4.27e-03, rho=1.37e-02 k*=100)
    - 3.29e-03 -> mono {D:1}   via D (3.29e-03, rho=1.00e-02 k*=100)
    - 1.20e-04 -> mono {or(X,X):1}   via or(X,X) (1.20e-04, rho=1.58e-02 k*=100)
    - 8.85e-05 -> mono {and(X,X):1}   via and(X,X) (8.85e-05, rho=1.17e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
- mono {THEM(THEM):1}
    - 6.00e-03 -> mono {C:1}   via C (6.00e-03, rho=1.82e-02 k*=100)
    - 4.27e-03 -> mono {X:1}   via X (4.27e-03, rho=1.37e-02 k*=100)
    - 3.29e-03 -> mono {D:1}   via D (3.29e-03, rho=1.00e-02 k*=100)
    - 1.20e-04 -> mono {or(X,X):1}   via or(X,X) (1.20e-04, rho=1.58e-02 k*=100)
    - 8.85e-05 -> mono {and(X,X):1}   via and(X,X) (8.85e-05, rho=1.17e-02 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 2.24e-03 -> mono {X:1}   via X (2.24e-03, rho=7.17e-03 k*=100)
    - 1.65e-03 -> mono {D:1}   via D (1.65e-03, rho=5.02e-03 k*=100)
    - 6.41e-05 -> mono {or(X,X):1}   via or(X,X) (6.41e-05, rho=8.49e-03 k*=100)
    - 4.54e-05 -> mono {and(X,X):1}   via and(X,X) (4.54e-05, rho=6.02e-03 k*=100)
    - 2.56e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.56e-05, rho=6.93e-03 k*=100)
