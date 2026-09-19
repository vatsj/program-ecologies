### arm=weak, n=6, game=pd, N=10, w=0.01, x_on=True, role=False, mode=square

programs 1852, classes 48, states 119, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 1.57e-06
mean payoff -0.5229, efficient 0.0000, deadweight loss 0.5229, mean bits in support 2.79

| pi | state |
|---|---|
| 0.3472 | mono {D:1} |
| 0.3121 | mono {X:1} |
| 0.3112 | mono {C:1} |
| 0.0077 | mono {and(X,X):1} |
| 0.0073 | mono {or(X,X):1} |
| 0.0036 | mono {THEM(ME):1} |
| 0.0036 | mono {THEM(THEM):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.11e-02 -> mono {C:1}   via C (3.11e-02, rho=9.45e-02 k*=10)
    - 3.04e-02 -> mono {X:1}   via X (3.04e-02, rho=9.72e-02 k*=10)
    - 7.44e-04 -> mono {and(X,X):1}   via and(X,X) (7.44e-04, rho=9.86e-02 k*=10)
    - 7.23e-04 -> mono {or(X,X):1}   via or(X,X) (7.23e-04, rho=9.59e-02 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {X:1}
    - 3.38e-02 -> mono {D:1}   via D (3.38e-02, rho=1.03e-01 k*=10)
    - 3.20e-02 -> mono {C:1}   via C (3.20e-02, rho=9.73e-02 k*=10)
    - 7.65e-04 -> mono {and(X,X):1}   via and(X,X) (7.65e-04, rho=1.01e-01 k*=10)
    - 7.44e-04 -> mono {or(X,X):1}   via or(X,X) (7.44e-04, rho=9.86e-02 k*=10)
    - 3.65e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.65e-04, rho=9.93e-02 k*=10)
    - 3.64e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.64e-04, rho=9.93e-02 k*=10)
- mono {C:1}
    - 3.47e-02 -> mono {D:1}   via D (3.47e-02, rho=1.06e-01 k*=10)
    - 3.21e-02 -> mono {X:1}   via X (3.21e-02, rho=1.03e-01 k*=10)
    - 7.86e-04 -> mono {and(X,X):1}   via and(X,X) (7.86e-04, rho=1.04e-01 k*=10)
    - 7.65e-04 -> mono {or(X,X):1}   via or(X,X) (7.65e-04, rho=1.01e-01 k*=10)
    - 3.63e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.63e-04, rho=9.87e-02 k*=10)
    - 3.62e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.62e-04, rho=9.87e-02 k*=10)
- mono {and(X,X):1}
    - 3.34e-02 -> mono {D:1}   via D (3.34e-02, rho=1.01e-01 k*=10)
    - 3.15e-02 -> mono {C:1}   via C (3.15e-02, rho=9.59e-02 k*=10)
    - 3.08e-02 -> mono {X:1}   via X (3.08e-02, rho=9.86e-02 k*=10)
    - 7.33e-04 -> mono {or(X,X):1}   via or(X,X) (7.33e-04, rho=9.73e-02 k*=10)
    - 3.67e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.67e-04, rho=9.97e-02 k*=10)
    - 3.65e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.65e-04, rho=9.97e-02 k*=10)
- mono {or(X,X):1}
    - 3.43e-02 -> mono {D:1}   via D (3.43e-02, rho=1.04e-01 k*=10)
    - 3.24e-02 -> mono {C:1}   via C (3.24e-02, rho=9.86e-02 k*=10)
    - 3.17e-02 -> mono {X:1}   via X (3.17e-02, rho=1.01e-01 k*=10)
    - 7.75e-04 -> mono {and(X,X):1}   via and(X,X) (7.75e-04, rho=1.03e-01 k*=10)
    - 3.64e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.64e-04, rho=9.90e-02 k*=10)
    - 3.63e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.63e-04, rho=9.90e-02 k*=10)
- mono {THEM(ME):1}
    - 3.38e-02 -> mono {C:1}   via C (3.38e-02, rho=1.03e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 3.17e-02 -> mono {X:1}   via X (3.17e-02, rho=1.01e-01 k*=10)
    - 7.69e-04 -> mono {or(X,X):1}   via or(X,X) (7.69e-04, rho=1.02e-01 k*=10)
    - 7.59e-04 -> mono {and(X,X):1}   via and(X,X) (7.59e-04, rho=1.01e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 3.38e-02 -> mono {C:1}   via C (3.38e-02, rho=1.03e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 3.17e-02 -> mono {X:1}   via X (3.17e-02, rho=1.01e-01 k*=10)
    - 7.69e-04 -> mono {or(X,X):1}   via or(X,X) (7.69e-04, rho=1.02e-01 k*=10)
    - 7.59e-04 -> mono {and(X,X):1}   via and(X,X) (7.59e-04, rho=1.01e-01 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=1.00e-01 k*=10)
