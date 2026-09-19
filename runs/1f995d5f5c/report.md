### arm=weak, n=6, game=dollar, N=10, w=0.01, x_on=True, role=False, mode=square

programs 1852, classes 46, states 182, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 2.30e-04
mean payoff 0.2135, efficient 0.5000, deadweight loss 0.2865, mean bits in support 2.79

| pi | state |
|---|---|
| 0.3335 | mono {C:1} |
| 0.3262 | mono {D:1} |
| 0.3111 | mono {X:1} |
| 0.0076 | mono {or(X,X):1} |
| 0.0075 | mono {and(X,X):1} |
| 0.0037 | mono {THEM(ME):1} |
| 0.0037 | mono {THEM(THEM):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 3.25e-02 -> mono {D:1}   via D (3.25e-02, rho=9.87e-02 k*=10)
    - 3.10e-02 -> mono {X:1}   via X (3.10e-02, rho=9.92e-02 k*=10)
    - 7.51e-04 -> mono {or(X,X):1}   via or(X,X) (7.51e-04, rho=9.95e-02 k*=10)
    - 7.46e-04 -> mono {and(X,X):1}   via and(X,X) (7.46e-04, rho=9.89e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {D:1}
    - 3.31e-02 -> mono {C:1}   via C (3.31e-02, rho=1.01e-01 k*=10)
    - 3.13e-02 -> mono {X:1}   via X (3.13e-02, rho=1.00e-01 k*=10)
    - 7.57e-04 -> mono {or(X,X):1}   via or(X,X) (7.57e-04, rho=1.00e-01 k*=10)
    - 7.54e-04 -> mono {and(X,X):1}   via and(X,X) (7.54e-04, rho=1.00e-01 k*=10)
    - 3.72e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.72e-04, rho=1.01e-01 k*=10)
    - 3.69e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.69e-04, rho=1.01e-01 k*=10)
- mono {X:1}
    - 3.31e-02 -> mono {C:1}   via C (3.31e-02, rho=1.01e-01 k*=10)
    - 3.28e-02 -> mono {D:1}   via D (3.28e-02, rho=9.97e-02 k*=10)
    - 7.56e-04 -> mono {or(X,X):1}   via or(X,X) (7.56e-04, rho=1.00e-01 k*=10)
    - 7.53e-04 -> mono {and(X,X):1}   via and(X,X) (7.53e-04, rho=9.98e-02 k*=10)
    - 3.71e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.71e-04, rho=1.00e-01 k*=10)
    - 3.68e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.68e-04, rho=1.00e-01 k*=10)
- mono {or(X,X):1}
    - 3.30e-02 -> mono {C:1}   via C (3.30e-02, rho=1.00e-01 k*=10)
    - 3.26e-02 -> mono {D:1}   via D (3.26e-02, rho=9.93e-02 k*=10)
    - 3.11e-02 -> mono {X:1}   via X (3.11e-02, rho=9.97e-02 k*=10)
    - 7.50e-04 -> mono {and(X,X):1}   via and(X,X) (7.50e-04, rho=9.94e-02 k*=10)
    - 3.70e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.70e-04, rho=1.00e-01 k*=10)
    - 3.68e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.68e-04, rho=1.00e-01 k*=10)
- mono {and(X,X):1}
    - 3.31e-02 -> mono {C:1}   via C (3.31e-02, rho=1.01e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=9.99e-02 k*=10)
    - 3.13e-02 -> mono {X:1}   via X (3.13e-02, rho=1.00e-01 k*=10)
    - 7.57e-04 -> mono {or(X,X):1}   via or(X,X) (7.57e-04, rho=1.00e-01 k*=10)
    - 3.72e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.72e-04, rho=1.01e-01 k*=10)
    - 3.69e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.69e-04, rho=1.01e-01 k*=10)
- mono {THEM(ME):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 3.25e-02 -> mono {D:1}   via D (3.25e-02, rho=9.87e-02 k*=10)
    - 3.09e-02 -> mono {X:1}   via X (3.09e-02, rho=9.90e-02 k*=10)
    - 7.50e-04 -> mono {or(X,X):1}   via or(X,X) (7.50e-04, rho=9.94e-02 k*=10)
    - 7.45e-04 -> mono {and(X,X):1}   via and(X,X) (7.45e-04, rho=9.88e-02 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 3.25e-02 -> mono {D:1}   via D (3.25e-02, rho=9.87e-02 k*=10)
    - 3.09e-02 -> mono {X:1}   via X (3.09e-02, rho=9.90e-02 k*=10)
    - 7.50e-04 -> mono {or(X,X):1}   via or(X,X) (7.50e-04, rho=9.94e-02 k*=10)
    - 7.45e-04 -> mono {and(X,X):1}   via and(X,X) (7.45e-04, rho=9.88e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
