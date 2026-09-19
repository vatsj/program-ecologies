### arm=weak, n=6, game=dollar, N=100, w=0.01, x_on=True, role=False, mode=square

programs 1852, classes 46, states 154, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 2.29e-05
mean payoff 0.2346, efficient 0.5000, deadweight loss 0.2654, mean bits in support 2.79

| pi | state |
|---|---|
| 0.3779 | mono {C:1} |
| 0.2978 | mono {X:1} |
| 0.2949 | mono {D:1} |
| 0.0078 | mono {or(X,X):1} |
| 0.0069 | mono {and(X,X):1} |
| 0.0042 | mono {THEM(ME):1} |
| 0.0042 | mono {THEM(THEM):1} |
| 0.0010 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 2.82e-03 -> mono {X:1}   via X (2.82e-03, rho=9.02e-03 k*=100)
    - 2.79e-03 -> mono {D:1}   via D (2.79e-03, rho=8.47e-03 k*=100)
    - 7.13e-05 -> mono {or(X,X):1}   via or(X,X) (7.13e-05, rho=9.45e-03 k*=100)
    - 6.56e-05 -> mono {and(X,X):1}   via and(X,X) (6.56e-05, rho=8.70e-03 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
- mono {X:1}
    - 3.56e-03 -> mono {C:1}   via C (3.56e-03, rho=1.08e-02 k*=100)
    - 3.16e-03 -> mono {D:1}   via D (3.16e-03, rho=9.60e-03 k*=100)
    - 7.81e-05 -> mono {or(X,X):1}   via or(X,X) (7.81e-05, rho=1.04e-02 k*=100)
    - 7.35e-05 -> mono {and(X,X):1}   via and(X,X) (7.35e-05, rho=9.75e-03 k*=100)
    - 3.92e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.92e-05, rho=1.06e-02 k*=100)
    - 3.89e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.89e-05, rho=1.06e-02 k*=100)
- mono {D:1}
    - 3.56e-03 -> mono {C:1}   via C (3.56e-03, rho=1.08e-02 k*=100)
    - 3.19e-03 -> mono {X:1}   via X (3.19e-03, rho=1.02e-02 k*=100)
    - 7.89e-05 -> mono {or(X,X):1}   via or(X,X) (7.89e-05, rho=1.05e-02 k*=100)
    - 7.58e-05 -> mono {and(X,X):1}   via and(X,X) (7.58e-05, rho=1.01e-02 k*=100)
    - 4.00e-05 -> mono {THEM(ME):1}   via THEM(ME) (4.00e-05, rho=1.08e-02 k*=100)
    - 3.97e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.97e-05, rho=1.08e-02 k*=100)
- mono {or(X,X):1}
    - 3.46e-03 -> mono {C:1}   via C (3.46e-03, rho=1.05e-02 k*=100)
    - 3.00e-03 -> mono {X:1}   via X (3.00e-03, rho=9.60e-03 k*=100)
    - 3.00e-03 -> mono {D:1}   via D (3.00e-03, rho=9.12e-03 k*=100)
    - 7.02e-05 -> mono {and(X,X):1}   via and(X,X) (7.02e-05, rho=9.31e-03 k*=100)
    - 3.82e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.82e-05, rho=1.04e-02 k*=100)
    - 3.80e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.80e-05, rho=1.04e-02 k*=100)
- mono {and(X,X):1}
    - 3.60e-03 -> mono {C:1}   via C (3.60e-03, rho=1.09e-02 k*=100)
    - 3.26e-03 -> mono {D:1}   via D (3.26e-03, rho=9.90e-03 k*=100)
    - 3.19e-03 -> mono {X:1}   via X (3.19e-03, rho=1.02e-02 k*=100)
    - 7.93e-05 -> mono {or(X,X):1}   via or(X,X) (7.93e-05, rho=1.05e-02 k*=100)
    - 3.98e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.98e-05, rho=1.08e-02 k*=100)
    - 3.95e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.95e-05, rho=1.08e-02 k*=100)
- mono {THEM(ME):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 2.79e-03 -> mono {D:1}   via D (2.79e-03, rho=8.47e-03 k*=100)
    - 2.76e-03 -> mono {X:1}   via X (2.76e-03, rho=8.84e-03 k*=100)
    - 7.02e-05 -> mono {or(X,X):1}   via or(X,X) (7.02e-05, rho=9.31e-03 k*=100)
    - 6.46e-05 -> mono {and(X,X):1}   via and(X,X) (6.46e-05, rho=8.56e-03 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
- mono {THEM(THEM):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 2.79e-03 -> mono {D:1}   via D (2.79e-03, rho=8.47e-03 k*=100)
    - 2.76e-03 -> mono {X:1}   via X (2.76e-03, rho=8.84e-03 k*=100)
    - 7.02e-05 -> mono {or(X,X):1}   via or(X,X) (7.02e-05, rho=9.31e-03 k*=100)
    - 6.46e-05 -> mono {and(X,X):1}   via and(X,X) (6.46e-05, rho=8.56e-03 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 2.79e-03 -> mono {D:1}   via D (2.79e-03, rho=8.47e-03 k*=100)
    - 2.76e-03 -> mono {X:1}   via X (2.76e-03, rho=8.84e-03 k*=100)
    - 7.02e-05 -> mono {or(X,X):1}   via or(X,X) (7.02e-05, rho=9.31e-03 k*=100)
    - 6.46e-05 -> mono {and(X,X):1}   via and(X,X) (6.46e-05, rho=8.56e-03 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
