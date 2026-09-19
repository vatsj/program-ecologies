### arm=weak, n=6, game=dollar, N=10, w=0.1, x_on=True, role=False, mode=square

programs 1852, classes 46, states 182, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 2.37e-04
mean payoff 0.2299, efficient 0.5000, deadweight loss 0.2701, mean bits in support 2.79

| pi | state |
|---|---|
| 0.3678 | mono {C:1} |
| 0.3015 | mono {D:1} |
| 0.3009 | mono {X:1} |
| 0.0077 | mono {or(X,X):1} |
| 0.0070 | mono {and(X,X):1} |
| 0.0041 | mono {THEM(ME):1} |
| 0.0041 | mono {THEM(THEM):1} |
| 0.0010 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 2.88e-02 -> mono {D:1}   via D (2.88e-02, rho=8.75e-02 k*=10)
    - 2.88e-02 -> mono {X:1}   via X (2.88e-02, rho=9.21e-02 k*=10)
    - 7.21e-04 -> mono {or(X,X):1}   via or(X,X) (7.21e-04, rho=9.57e-02 k*=10)
    - 6.74e-04 -> mono {and(X,X):1}   via and(X,X) (6.74e-04, rho=8.94e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {D:1}
    - 3.51e-02 -> mono {C:1}   via C (3.51e-02, rho=1.07e-01 k*=10)
    - 3.18e-02 -> mono {X:1}   via X (3.18e-02, rho=1.02e-01 k*=10)
    - 7.82e-04 -> mono {or(X,X):1}   via or(X,X) (7.82e-04, rho=1.04e-01 k*=10)
    - 7.57e-04 -> mono {and(X,X):1}   via and(X,X) (7.57e-04, rho=1.00e-01 k*=10)
    - 3.94e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.94e-04, rho=1.07e-01 k*=10)
    - 3.91e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.91e-04, rho=1.07e-01 k*=10)
- mono {X:1}
    - 3.51e-02 -> mono {C:1}   via C (3.51e-02, rho=1.07e-01 k*=10)
    - 3.18e-02 -> mono {D:1}   via D (3.18e-02, rho=9.67e-02 k*=10)
    - 7.76e-04 -> mono {or(X,X):1}   via or(X,X) (7.76e-04, rho=1.03e-01 k*=10)
    - 7.39e-04 -> mono {and(X,X):1}   via and(X,X) (7.39e-04, rho=9.79e-02 k*=10)
    - 3.87e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.87e-04, rho=1.05e-01 k*=10)
    - 3.85e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.85e-04, rho=1.05e-01 k*=10)
- mono {or(X,X):1}
    - 3.42e-02 -> mono {C:1}   via C (3.42e-02, rho=1.04e-01 k*=10)
    - 3.05e-02 -> mono {D:1}   via D (3.05e-02, rho=9.28e-02 k*=10)
    - 3.02e-02 -> mono {X:1}   via X (3.02e-02, rho=9.68e-02 k*=10)
    - 7.12e-04 -> mono {and(X,X):1}   via and(X,X) (7.12e-04, rho=9.44e-02 k*=10)
    - 3.80e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.80e-04, rho=1.03e-01 k*=10)
    - 3.77e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.77e-04, rho=1.03e-01 k*=10)
- mono {and(X,X):1}
    - 3.53e-02 -> mono {C:1}   via C (3.53e-02, rho=1.07e-01 k*=10)
    - 3.26e-02 -> mono {D:1}   via D (3.26e-02, rho=9.92e-02 k*=10)
    - 3.18e-02 -> mono {X:1}   via X (3.18e-02, rho=1.02e-01 k*=10)
    - 7.85e-04 -> mono {or(X,X):1}   via or(X,X) (7.85e-04, rho=1.04e-01 k*=10)
    - 3.92e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.92e-04, rho=1.06e-01 k*=10)
    - 3.89e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.89e-04, rho=1.06e-01 k*=10)
- mono {THEM(ME):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 2.88e-02 -> mono {D:1}   via D (2.88e-02, rho=8.75e-02 k*=10)
    - 2.83e-02 -> mono {X:1}   via X (2.83e-02, rho=9.06e-02 k*=10)
    - 7.13e-04 -> mono {or(X,X):1}   via or(X,X) (7.13e-04, rho=9.45e-02 k*=10)
    - 6.66e-04 -> mono {and(X,X):1}   via and(X,X) (6.66e-04, rho=8.83e-02 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 2.88e-02 -> mono {D:1}   via D (2.88e-02, rho=8.75e-02 k*=10)
    - 2.83e-02 -> mono {X:1}   via X (2.83e-02, rho=9.06e-02 k*=10)
    - 7.13e-04 -> mono {or(X,X):1}   via or(X,X) (7.13e-04, rho=9.45e-02 k*=10)
    - 6.66e-04 -> mono {and(X,X):1}   via and(X,X) (6.66e-04, rho=8.83e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
- mono {THEM(^C):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 2.88e-02 -> mono {D:1}   via D (2.88e-02, rho=8.75e-02 k*=10)
    - 2.83e-02 -> mono {X:1}   via X (2.83e-02, rho=9.06e-02 k*=10)
    - 7.13e-04 -> mono {or(X,X):1}   via or(X,X) (7.13e-04, rho=9.45e-02 k*=10)
    - 6.66e-04 -> mono {and(X,X):1}   via and(X,X) (6.66e-04, rho=8.83e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
