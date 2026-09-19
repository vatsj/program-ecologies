### arm=weak, n=6, game=exchange, N=10, w=0.1, x_on=True, role=False, mode=square

programs 1852, classes 48, states 399, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 1.41e-04
mean payoff 0.6488, efficient 2.0000, deadweight loss 1.3512, mean bits in support 2.77

| pi | state |
|---|---|
| 0.5185 | mono {D:1} |
| 0.2793 | mono {X:1} |
| 0.1757 | mono {C:1} |
| 0.0089 | mono {and(X,X):1} |
| 0.0052 | mono {or(X,X):1} |
| 0.0027 | mono {THEM(ME):1} |
| 0.0027 | mono {THEM(THEM):1} |
| 0.0013 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.29e-02 -> mono {X:1}   via X (2.29e-02, rho=7.34e-02 k*=10)
    - 1.75e-02 -> mono {C:1}   via C (1.75e-02, rho=5.32e-02 k*=10)
    - 6.48e-04 -> mono {and(X,X):1}   via and(X,X) (6.48e-04, rho=8.59e-02 k*=10)
    - 4.72e-04 -> mono {or(X,X):1}   via or(X,X) (4.72e-04, rho=6.26e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {X:1}
    - 4.28e-02 -> mono {D:1}   via D (4.28e-02, rho=1.30e-01 k*=10)
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=7.56e-02 k*=10)
    - 8.62e-04 -> mono {and(X,X):1}   via and(X,X) (8.62e-04, rho=1.14e-01 k*=10)
    - 6.57e-04 -> mono {or(X,X):1}   via or(X,X) (6.57e-04, rho=8.71e-02 k*=10)
    - 3.24e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.24e-04, rho=8.76e-02 k*=10)
    - 3.21e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.21e-04, rho=8.76e-02 k*=10)
- mono {C:1}
    - 5.25e-02 -> mono {D:1}   via D (5.25e-02, rho=1.60e-01 k*=10)
    - 3.98e-02 -> mono {X:1}   via X (3.98e-02, rho=1.27e-01 k*=10)
    - 1.08e-03 -> mono {and(X,X):1}   via and(X,X) (1.08e-03, rho=1.43e-01 k*=10)
    - 8.53e-04 -> mono {or(X,X):1}   via or(X,X) (8.53e-04, rho=1.13e-01 k*=10)
    - 2.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.84e-04, rho=7.70e-02 k*=10)
    - 2.82e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.82e-04, rho=7.70e-02 k*=10)
- mono {and(X,X):1}
    - 3.79e-02 -> mono {D:1}   via D (3.79e-02, rho=1.15e-01 k*=10)
    - 2.70e-02 -> mono {X:1}   via X (2.70e-02, rho=8.65e-02 k*=10)
    - 2.11e-02 -> mono {C:1}   via C (2.11e-02, rho=6.40e-02 k*=10)
    - 5.62e-04 -> mono {or(X,X):1}   via or(X,X) (5.62e-04, rho=7.45e-02 k*=10)
    - 3.46e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.46e-04, rho=9.36e-02 k*=10)
    - 3.43e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.43e-04, rho=9.36e-02 k*=10)
- mono {or(X,X):1}
    - 4.77e-02 -> mono {D:1}   via D (4.77e-02, rho=1.45e-01 k*=10)
    - 3.55e-02 -> mono {X:1}   via X (3.55e-02, rho=1.14e-01 k*=10)
    - 2.88e-02 -> mono {C:1}   via C (2.88e-02, rho=8.76e-02 k*=10)
    - 9.71e-04 -> mono {and(X,X):1}   via and(X,X) (9.71e-04, rho=1.29e-01 k*=10)
    - 3.03e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.03e-04, rho=8.21e-02 k*=10)
    - 3.01e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.01e-04, rho=8.21e-02 k*=10)
- mono {THEM(ME):1}
    - 5.12e-02 -> mono {C:1}   via C (5.12e-02, rho=1.56e-01 k*=10)
    - 3.98e-02 -> mono {X:1}   via X (3.98e-02, rho=1.27e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 1.07e-03 -> mono {or(X,X):1}   via or(X,X) (1.07e-03, rho=1.42e-01 k*=10)
    - 8.56e-04 -> mono {and(X,X):1}   via and(X,X) (8.56e-04, rho=1.14e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 5.12e-02 -> mono {C:1}   via C (5.12e-02, rho=1.56e-01 k*=10)
    - 3.98e-02 -> mono {X:1}   via X (3.98e-02, rho=1.27e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 1.07e-03 -> mono {or(X,X):1}   via or(X,X) (1.07e-03, rho=1.42e-01 k*=10)
    - 8.56e-04 -> mono {and(X,X):1}   via and(X,X) (8.56e-04, rho=1.14e-01 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
- mono {THEM(^C):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 2.45e-02 -> mono {X:1}   via X (2.45e-02, rho=7.85e-02 k*=10)
    - 1.94e-02 -> mono {D:1}   via D (1.94e-02, rho=5.89e-02 k*=10)
    - 6.72e-04 -> mono {or(X,X):1}   via or(X,X) (6.72e-04, rho=8.91e-02 k*=10)
    - 5.16e-04 -> mono {and(X,X):1}   via and(X,X) (5.16e-04, rho=6.84e-02 k*=10)
    - 2.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.84e-04, rho=7.70e-02 k*=10)
