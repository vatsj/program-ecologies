### arm=weak, n=6, game=exchange, N=10, w=0.01, x_on=True, role=False, mode=square

programs 1852, classes 48, states 399, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 1.54e-04
mean payoff 0.9512, efficient 2.0000, deadweight loss 1.0488, mean bits in support 2.79

| pi | state |
|---|---|
| 0.3486 | mono {D:1} |
| 0.3116 | mono {X:1} |
| 0.3096 | mono {C:1} |
| 0.0078 | mono {and(X,X):1} |
| 0.0073 | mono {or(X,X):1} |
| 0.0036 | mono {THEM(ME):1} |
| 0.0035 | mono {THEM(THEM):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.10e-02 -> mono {C:1}   via C (3.10e-02, rho=9.41e-02 k*=10)
    - 3.03e-02 -> mono {X:1}   via X (3.03e-02, rho=9.70e-02 k*=10)
    - 7.43e-04 -> mono {and(X,X):1}   via and(X,X) (7.43e-04, rho=9.85e-02 k*=10)
    - 7.21e-04 -> mono {or(X,X):1}   via or(X,X) (7.21e-04, rho=9.56e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {X:1}
    - 3.39e-02 -> mono {D:1}   via D (3.39e-02, rho=1.03e-01 k*=10)
    - 3.19e-02 -> mono {C:1}   via C (3.19e-02, rho=9.71e-02 k*=10)
    - 7.65e-04 -> mono {and(X,X):1}   via and(X,X) (7.65e-04, rho=1.01e-01 k*=10)
    - 7.43e-04 -> mono {or(X,X):1}   via or(X,X) (7.43e-04, rho=9.85e-02 k*=10)
    - 3.64e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.64e-04, rho=9.87e-02 k*=10)
    - 3.62e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.62e-04, rho=9.87e-02 k*=10)
- mono {C:1}
    - 3.49e-02 -> mono {D:1}   via D (3.49e-02, rho=1.06e-01 k*=10)
    - 3.22e-02 -> mono {X:1}   via X (3.22e-02, rho=1.03e-01 k*=10)
    - 7.88e-04 -> mono {and(X,X):1}   via and(X,X) (7.88e-04, rho=1.04e-01 k*=10)
    - 7.65e-04 -> mono {or(X,X):1}   via or(X,X) (7.65e-04, rho=1.01e-01 k*=10)
    - 3.60e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.60e-04, rho=9.74e-02 k*=10)
    - 3.57e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.57e-04, rho=9.74e-02 k*=10)
- mono {and(X,X):1}
    - 3.34e-02 -> mono {D:1}   via D (3.34e-02, rho=1.02e-01 k*=10)
    - 3.14e-02 -> mono {C:1}   via C (3.14e-02, rho=9.56e-02 k*=10)
    - 3.08e-02 -> mono {X:1}   via X (3.08e-02, rho=9.85e-02 k*=10)
    - 7.32e-04 -> mono {or(X,X):1}   via or(X,X) (7.32e-04, rho=9.70e-02 k*=10)
    - 3.67e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.67e-04, rho=9.93e-02 k*=10)
    - 3.64e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.64e-04, rho=9.93e-02 k*=10)
- mono {or(X,X):1}
    - 3.44e-02 -> mono {D:1}   via D (3.44e-02, rho=1.05e-01 k*=10)
    - 3.24e-02 -> mono {C:1}   via C (3.24e-02, rho=9.85e-02 k*=10)
    - 3.17e-02 -> mono {X:1}   via X (3.17e-02, rho=1.01e-01 k*=10)
    - 7.77e-04 -> mono {and(X,X):1}   via and(X,X) (7.77e-04, rho=1.03e-01 k*=10)
    - 3.62e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.62e-04, rho=9.80e-02 k*=10)
    - 3.59e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.59e-04, rho=9.80e-02 k*=10)
- mono {THEM(ME):1}
    - 3.47e-02 -> mono {C:1}   via C (3.47e-02, rho=1.05e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 3.21e-02 -> mono {X:1}   via X (3.21e-02, rho=1.03e-01 k*=10)
    - 7.84e-04 -> mono {or(X,X):1}   via or(X,X) (7.84e-04, rho=1.04e-01 k*=10)
    - 7.64e-04 -> mono {and(X,X):1}   via and(X,X) (7.64e-04, rho=1.01e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 3.47e-02 -> mono {C:1}   via C (3.47e-02, rho=1.05e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 3.21e-02 -> mono {X:1}   via X (3.21e-02, rho=1.03e-01 k*=10)
    - 7.84e-04 -> mono {or(X,X):1}   via or(X,X) (7.84e-04, rho=1.04e-01 k*=10)
    - 7.64e-04 -> mono {and(X,X):1}   via and(X,X) (7.64e-04, rho=1.01e-01 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
