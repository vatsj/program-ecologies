### arm=weak, n=6, game=pd, N=10, w=0.1, x_on=True, role=False, mode=square

programs 1852, classes 48, states 119, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 1.29e-06
mean payoff -0.6849, efficient 0.0000, deadweight loss 0.6849, mean bits in support 2.77

| pi | state |
|---|---|
| 0.5277 | mono {D:1} |
| 0.2781 | mono {X:1} |
| 0.1675 | mono {C:1} |
| 0.0090 | mono {and(X,X):1} |
| 0.0051 | mono {or(X,X):1} |
| 0.0031 | mono {THEM(ME):1} |
| 0.0030 | mono {THEM(THEM):1} |
| 0.0011 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.27e-02 -> mono {X:1}   via X (2.27e-02, rho=7.26e-02 k*=10)
    - 1.69e-02 -> mono {C:1}   via C (1.69e-02, rho=5.13e-02 k*=10)
    - 6.45e-04 -> mono {and(X,X):1}   via and(X,X) (6.45e-04, rho=8.55e-02 k*=10)
    - 4.62e-04 -> mono {or(X,X):1}   via or(X,X) (4.62e-04, rho=6.12e-02 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {X:1}
    - 4.33e-02 -> mono {D:1}   via D (4.33e-02, rho=1.32e-01 k*=10)
    - 2.43e-02 -> mono {C:1}   via C (2.43e-02, rho=7.39e-02 k*=10)
    - 8.69e-04 -> mono {and(X,X):1}   via and(X,X) (8.69e-04, rho=1.15e-01 k*=10)
    - 6.50e-04 -> mono {or(X,X):1}   via or(X,X) (6.50e-04, rho=8.62e-02 k*=10)
    - 3.42e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.42e-04, rho=9.29e-02 k*=10)
    - 3.41e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.41e-04, rho=9.29e-02 k*=10)
- mono {C:1}
    - 5.40e-02 -> mono {D:1}   via D (5.40e-02, rho=1.64e-01 k*=10)
    - 4.06e-02 -> mono {X:1}   via X (4.06e-02, rho=1.30e-01 k*=10)
    - 1.11e-03 -> mono {and(X,X):1}   via and(X,X) (1.11e-03, rho=1.47e-01 k*=10)
    - 8.63e-04 -> mono {or(X,X):1}   via or(X,X) (8.63e-04, rho=1.14e-01 k*=10)
    - 3.18e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.18e-04, rho=8.64e-02 k*=10)
    - 3.17e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.17e-04, rho=8.64e-02 k*=10)
- mono {and(X,X):1}
    - 3.80e-02 -> mono {D:1}   via D (3.80e-02, rho=1.16e-01 k*=10)
    - 2.68e-02 -> mono {X:1}   via X (2.68e-02, rho=8.59e-02 k*=10)
    - 2.04e-02 -> mono {C:1}   via C (2.04e-02, rho=6.21e-02 k*=10)
    - 5.52e-04 -> mono {or(X,X):1}   via or(X,X) (5.52e-04, rho=7.32e-02 k*=10)
    - 3.55e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.55e-04, rho=9.64e-02 k*=10)
    - 3.53e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.53e-04, rho=9.64e-02 k*=10)
- mono {or(X,X):1}
    - 4.87e-02 -> mono {D:1}   via D (4.87e-02, rho=1.48e-01 k*=10)
    - 3.59e-02 -> mono {X:1}   via X (3.59e-02, rho=1.15e-01 k*=10)
    - 2.85e-02 -> mono {C:1}   via C (2.85e-02, rho=8.66e-02 k*=10)
    - 9.86e-04 -> mono {and(X,X):1}   via and(X,X) (9.86e-04, rho=1.31e-01 k*=10)
    - 3.29e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.29e-04, rho=8.96e-02 k*=10)
    - 3.28e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.28e-04, rho=8.96e-02 k*=10)
- mono {THEM(ME):1}
    - 4.29e-02 -> mono {C:1}   via C (4.29e-02, rho=1.31e-01 k*=10)
    - 3.60e-02 -> mono {X:1}   via X (3.60e-02, rho=1.15e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 9.26e-04 -> mono {or(X,X):1}   via or(X,X) (9.26e-04, rho=1.23e-01 k*=10)
    - 8.11e-04 -> mono {and(X,X):1}   via and(X,X) (8.11e-04, rho=1.07e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 4.29e-02 -> mono {C:1}   via C (4.29e-02, rho=1.31e-01 k*=10)
    - 3.60e-02 -> mono {X:1}   via X (3.60e-02, rho=1.15e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 9.26e-04 -> mono {or(X,X):1}   via or(X,X) (9.26e-04, rho=1.23e-01 k*=10)
    - 8.11e-04 -> mono {and(X,X):1}   via and(X,X) (8.11e-04, rho=1.07e-01 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=1.00e-01 k*=10)
- mono {THEM(^C):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 2.72e-02 -> mono {X:1}   via X (2.72e-02, rho=8.69e-02 k*=10)
    - 2.45e-02 -> mono {D:1}   via D (2.45e-02, rho=7.44e-02 k*=10)
    - 7.04e-04 -> mono {or(X,X):1}   via or(X,X) (7.04e-04, rho=9.34e-02 k*=10)
    - 6.08e-04 -> mono {and(X,X):1}   via and(X,X) (6.08e-04, rho=8.06e-02 k*=10)
    - 3.18e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.18e-04, rho=8.64e-02 k*=10)
