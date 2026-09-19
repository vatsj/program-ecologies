### arm=weak, n=6, game=dollar, N=10, w=1.0, x_on=True, role=False, mode=square

programs 1852, classes 46, states 182, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 2.36e-04
mean payoff 0.3653, efficient 0.5000, deadweight loss 0.1347, mean bits in support 2.81

| pi | state |
|---|---|
| 0.6578 | mono {C:1} |
| 0.1902 | mono {X:1} |
| 0.1185 | mono {D:1} |
| 0.0079 | mono {or(X,X):1} |
| 0.0075 | mono {THEM(ME):1} |
| 0.0074 | mono {THEM(THEM):1} |
| 0.0032 | mono {and(X,X):1} |
| 0.0018 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 1.55e-02 -> mono {X:1}   via X (1.55e-02, rho=4.95e-02 k*=10)
    - 9.03e-03 -> mono {D:1}   via D (9.03e-03, rho=2.74e-02 k*=10)
    - 5.33e-04 -> mono {or(X,X):1}   via or(X,X) (5.33e-04, rho=7.06e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
    - 2.69e-04 -> mono {and(X,X):1}   via and(X,X) (2.69e-04, rho=3.57e-02 k*=10)
- mono {X:1}
    - 5.23e-02 -> mono {C:1}   via C (5.23e-02, rho=1.59e-01 k*=10)
    - 2.36e-02 -> mono {D:1}   via D (2.36e-02, rho=7.17e-02 k*=10)
    - 9.52e-04 -> mono {or(X,X):1}   via or(X,X) (9.52e-04, rho=1.26e-01 k*=10)
    - 6.18e-04 -> mono {and(X,X):1}   via and(X,X) (6.18e-04, rho=8.19e-02 k*=10)
    - 5.17e-04 -> mono {THEM(ME):1}   via THEM(ME) (5.17e-04, rho=1.40e-01 k*=10)
    - 5.14e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (5.14e-04, rho=1.40e-01 k*=10)
- mono {D:1}
    - 5.16e-02 -> mono {C:1}   via C (5.16e-02, rho=1.57e-01 k*=10)
    - 3.63e-02 -> mono {X:1}   via X (3.63e-02, rho=1.16e-01 k*=10)
    - 1.01e-03 -> mono {or(X,X):1}   via or(X,X) (1.01e-03, rho=1.34e-01 k*=10)
    - 7.85e-04 -> mono {and(X,X):1}   via and(X,X) (7.85e-04, rho=1.04e-01 k*=10)
    - 5.79e-04 -> mono {THEM(ME):1}   via THEM(ME) (5.79e-04, rho=1.57e-01 k*=10)
    - 5.75e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (5.75e-04, rho=1.57e-01 k*=10)
- mono {or(X,X):1}
    - 4.37e-02 -> mono {C:1}   via C (4.37e-02, rho=1.33e-01 k*=10)
    - 2.34e-02 -> mono {X:1}   via X (2.34e-02, rho=7.48e-02 k*=10)
    - 1.57e-02 -> mono {D:1}   via D (1.57e-02, rho=4.77e-02 k*=10)
    - 4.49e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.49e-04, rho=1.22e-01 k*=10)
    - 4.46e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (4.46e-04, rho=1.22e-01 k*=10)
    - 4.36e-04 -> mono {and(X,X):1}   via and(X,X) (4.36e-04, rho=5.78e-02 k*=10)
- mono {THEM(ME):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 1.30e-02 -> mono {X:1}   via X (1.30e-02, rho=4.17e-02 k*=10)
    - 9.03e-03 -> mono {D:1}   via D (9.03e-03, rho=2.74e-02 k*=10)
    - 4.80e-04 -> mono {or(X,X):1}   via or(X,X) (4.80e-04, rho=6.36e-02 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
    - 2.32e-04 -> mono {and(X,X):1}   via and(X,X) (2.32e-04, rho=3.07e-02 k*=10)
- mono {THEM(THEM):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 1.30e-02 -> mono {X:1}   via X (1.30e-02, rho=4.17e-02 k*=10)
    - 9.03e-03 -> mono {D:1}   via D (9.03e-03, rho=2.74e-02 k*=10)
    - 4.80e-04 -> mono {or(X,X):1}   via or(X,X) (4.80e-04, rho=6.36e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 2.32e-04 -> mono {and(X,X):1}   via and(X,X) (2.32e-04, rho=3.07e-02 k*=10)
- mono {and(X,X):1}
    - 5.56e-02 -> mono {C:1}   via C (5.56e-02, rho=1.69e-01 k*=10)
    - 3.63e-02 -> mono {X:1}   via X (3.63e-02, rho=1.16e-01 k*=10)
    - 3.03e-02 -> mono {D:1}   via D (3.03e-02, rho=9.20e-02 k*=10)
    - 1.06e-03 -> mono {or(X,X):1}   via or(X,X) (1.06e-03, rho=1.40e-01 k*=10)
    - 5.63e-04 -> mono {THEM(ME):1}   via THEM(ME) (5.63e-04, rho=1.52e-01 k*=10)
    - 5.59e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (5.59e-04, rho=1.52e-01 k*=10)
- mono {THEM(^C):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 1.30e-02 -> mono {X:1}   via X (1.30e-02, rho=4.17e-02 k*=10)
    - 9.03e-03 -> mono {D:1}   via D (9.03e-03, rho=2.74e-02 k*=10)
    - 4.80e-04 -> mono {or(X,X):1}   via or(X,X) (4.80e-04, rho=6.36e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
