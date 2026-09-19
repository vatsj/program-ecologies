### arm=weak, n=6, game=dollar, N=100, w=0.1, x_on=True, role=False, mode=square

programs 1852, classes 46, states 154, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 2.04e-05
mean payoff 0.4164, efficient 0.5000, deadweight loss 0.0836, mean bits in support 2.81

| pi | state |
|---|---|
| 0.7753 | mono {C:1} |
| 0.1227 | mono {X:1} |
| 0.0697 | mono {D:1} |
| 0.0087 | mono {THEM(ME):1} |
| 0.0086 | mono {THEM(THEM):1} |
| 0.0063 | mono {or(X,X):1} |
| 0.0021 | mono {THEM(^C):1} |
| 0.0019 | mono {and(X,X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 1.02e-03 -> mono {X:1}   via X (1.02e-03, rho=3.27e-03 k*=100)
    - 5.32e-04 -> mono {D:1}   via D (5.32e-04, rho=1.62e-03 k*=100)
    - 4.20e-05 -> mono {or(X,X):1}   via or(X,X) (4.20e-05, rho=5.58e-03 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 1.62e-05 -> mono {and(X,X):1}   via and(X,X) (1.62e-05, rho=2.14e-03 k*=100)
- mono {X:1}
    - 6.42e-03 -> mono {C:1}   via C (6.42e-03, rho=1.95e-02 k*=100)
    - 2.16e-03 -> mono {D:1}   via D (2.16e-03, rho=6.55e-03 k*=100)
    - 1.05e-04 -> mono {or(X,X):1}   via or(X,X) (1.05e-04, rho=1.39e-02 k*=100)
    - 5.92e-05 -> mono {THEM(ME):1}   via THEM(ME) (5.92e-05, rho=1.60e-02 k*=100)
    - 5.88e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (5.88e-05, rho=1.60e-02 k*=100)
    - 5.80e-05 -> mono {and(X,X):1}   via and(X,X) (5.80e-05, rho=7.70e-03 k*=100)
- mono {D:1}
    - 5.92e-03 -> mono {C:1}   via C (5.92e-03, rho=1.80e-02 k*=100)
    - 3.77e-03 -> mono {X:1}   via X (3.77e-03, rho=1.21e-02 k*=100)
    - 1.10e-04 -> mono {or(X,X):1}   via or(X,X) (1.10e-04, rho=1.46e-02 k*=100)
    - 7.93e-05 -> mono {and(X,X):1}   via and(X,X) (7.93e-05, rho=1.05e-02 k*=100)
    - 6.65e-05 -> mono {THEM(ME):1}   via THEM(ME) (6.65e-05, rho=1.80e-02 k*=100)
    - 6.60e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (6.60e-05, rho=1.80e-02 k*=100)
- mono {THEM(ME):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 8.34e-04 -> mono {X:1}   via X (8.34e-04, rho=2.67e-03 k*=100)
    - 5.32e-04 -> mono {D:1}   via D (5.32e-04, rho=1.62e-03 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 3.62e-05 -> mono {or(X,X):1}   via or(X,X) (3.62e-05, rho=4.80e-03 k*=100)
    - 1.39e-05 -> mono {and(X,X):1}   via and(X,X) (1.39e-05, rho=1.84e-03 k*=100)
- mono {THEM(THEM):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 8.34e-04 -> mono {X:1}   via X (8.34e-04, rho=2.67e-03 k*=100)
    - 5.32e-04 -> mono {D:1}   via D (5.32e-04, rho=1.62e-03 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.62e-05 -> mono {or(X,X):1}   via or(X,X) (3.62e-05, rho=4.80e-03 k*=100)
    - 1.39e-05 -> mono {and(X,X):1}   via and(X,X) (1.39e-05, rho=1.84e-03 k*=100)
- mono {or(X,X):1}
    - 5.15e-03 -> mono {C:1}   via C (5.15e-03, rho=1.56e-02 k*=100)
    - 2.05e-03 -> mono {X:1}   via X (2.05e-03, rho=6.55e-03 k*=100)
    - 1.23e-03 -> mono {D:1}   via D (1.23e-03, rho=3.73e-03 k*=100)
    - 4.99e-05 -> mono {THEM(ME):1}   via THEM(ME) (4.99e-05, rho=1.35e-02 k*=100)
    - 4.95e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (4.95e-05, rho=1.35e-02 k*=100)
    - 3.51e-05 -> mono {and(X,X):1}   via and(X,X) (3.51e-05, rho=4.66e-03 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 8.34e-04 -> mono {X:1}   via X (8.34e-04, rho=2.67e-03 k*=100)
    - 5.32e-04 -> mono {D:1}   via D (5.32e-04, rho=1.62e-03 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 3.62e-05 -> mono {or(X,X):1}   via or(X,X) (3.62e-05, rho=4.80e-03 k*=100)
- mono {and(X,X):1}
    - 6.68e-03 -> mono {C:1}   via C (6.68e-03, rho=2.03e-02 k*=100)
    - 3.79e-03 -> mono {X:1}   via X (3.79e-03, rho=1.21e-02 k*=100)
    - 2.97e-03 -> mono {D:1}   via D (2.97e-03, rho=9.02e-03 k*=100)
    - 1.18e-04 -> mono {or(X,X):1}   via or(X,X) (1.18e-04, rho=1.56e-02 k*=100)
    - 6.47e-05 -> mono {THEM(ME):1}   via THEM(ME) (6.47e-05, rho=1.75e-02 k*=100)
    - 6.42e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (6.42e-05, rho=1.75e-02 k*=100)
