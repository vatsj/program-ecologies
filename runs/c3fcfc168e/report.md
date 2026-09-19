### arm=weak, n=6, game=exchange, N=10, w=1.0, x_on=True, role=False, mode=square

programs 1852, classes 48, states 373, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 7.84e-05
mean payoff 0.0373, efficient 2.0000, deadweight loss 1.9627, mean bits in support 2.69

| pi | state |
|---|---|
| 0.9670 | mono {D:1} |
| 0.0156 | mono {X:1} |
| 0.0051 | mono {THEM(^C):1} |
| 0.0040 | mono {C:1} |
| 0.0020 | mono {and(X,X):1} |
| 0.0015 | mono {THEM(^X):1} |
| 0.0011 | mono {THEM(ME):1} |
| 0.0011 | mono {THEM(THEM):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.07e-03 -> mono {X:1}   via X (1.07e-03, rho=3.44e-03 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
    - 2.25e-04 -> mono {THEM(^C):1}   via THEM(^C) (2.25e-04, rho=2.47e-01 k*=10)
    - 1.74e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.74e-04, rho=1.96e-01 k*=10)
    - 1.46e-04 -> mono {and(X,X):1}   via and(X,X) (1.46e-04, rho=1.94e-02 k*=10)
- mono {X:1}
    - 1.03e-01 -> mono {D:1}   via D (1.03e-01, rho=3.13e-01 k*=10)
    - 6.37e-03 -> mono {C:1}   via C (6.37e-03, rho=1.94e-02 k*=10)
    - 1.48e-03 -> mono {and(X,X):1}   via and(X,X) (1.48e-03, rho=1.96e-01 k*=10)
    - 3.40e-04 -> mono {or(X,X):1}   via or(X,X) (3.40e-04, rho=4.51e-02 k*=10)
    - 1.43e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.43e-04, rho=1.57e-01 k*=10)
    - 1.18e-04 -> mono {THEM(ME):1}   via THEM(ME) (1.18e-04, rho=3.19e-02 k*=10)
- mono {THEM(^C):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 8.57e-03 -> mono {X:1}   via X (8.57e-03, rho=2.74e-02 k*=10)
    - 4.44e-04 -> mono {or(X,X):1}   via or(X,X) (4.44e-04, rho=5.89e-02 k*=10)
    - 4.18e-04 -> mono {D:1}   via D (4.18e-04, rho=1.27e-03 k*=10)
    - 3.50e-04 -> mono {THEM(^D):1}   via THEM(^D) (3.50e-04, rho=3.85e-01 k*=10)
    - 2.07e-04 -> mono {THEM(^X):1}   via THEM(^X) (2.07e-04, rho=2.34e-01 k*=10)
- mono {C:1}
    - 1.27e-01 -> mono {D:1}   via D (1.27e-01, rho=3.85e-01 k*=10)
    - 7.32e-02 -> mono {X:1}   via X (7.32e-02, rho=2.34e-01 k*=10)
    - 2.36e-03 -> mono {and(X,X):1}   via and(X,X) (2.36e-03, rho=3.13e-01 k*=10)
    - 1.20e-03 -> mono {or(X,X):1}   via or(X,X) (1.20e-03, rho=1.60e-01 k*=10)
    - 3.06e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (3.06e-04, rho=3.85e-01 k*=10)
    - 3.06e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (3.06e-04, rho=3.85e-01 k*=10)
- mono {and(X,X):1}
    - 7.71e-02 -> mono {D:1}   via D (7.71e-02, rho=2.34e-01 k*=10)
    - 1.07e-02 -> mono {X:1}   via X (1.07e-02, rho=3.41e-02 k*=10)
    - 1.13e-03 -> mono {C:1}   via C (1.13e-03, rho=3.44e-03 k*=10)
    - 1.97e-04 -> mono {THEM(ME):1}   via THEM(ME) (1.97e-04, rho=5.35e-02 k*=10)
    - 1.96e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (1.96e-04, rho=5.35e-02 k*=10)
    - 1.79e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.79e-04, rho=1.96e-01 k*=10)
- mono {THEM(^X):1}
    - 7.89e-02 -> mono {C:1}   via C (7.89e-02, rho=2.40e-01 k*=10)
    - 3.12e-02 -> mono {X:1}   via X (3.12e-02, rho=1.00e-01 k*=10)
    - 2.84e-03 -> mono {D:1}   via D (2.84e-03, rho=8.63e-03 k*=10)
    - 1.28e-03 -> mono {or(X,X):1}   via or(X,X) (1.28e-03, rho=1.70e-01 k*=10)
    - 3.15e-04 -> mono {and(X,X):1}   via and(X,X) (3.15e-04, rho=4.17e-02 k*=10)
    - 2.85e-04 -> mono {THEM(^D):1}   via THEM(^D) (2.85e-04, rho=3.13e-01 k*=10)
- mono {THEM(ME):1}
    - 1.68e-01 -> mono {C:1}   via C (1.68e-01, rho=5.11e-01 k*=10)
    - 1.12e-01 -> mono {X:1}   via X (1.12e-01, rho=3.58e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 3.37e-03 -> mono {or(X,X):1}   via or(X,X) (3.37e-03, rho=4.46e-01 k*=10)
    - 1.81e-03 -> mono {and(X,X):1}   via and(X,X) (1.81e-03, rho=2.40e-01 k*=10)
    - 4.65e-04 -> mono {THEM(^C):1}   via THEM(^C) (4.65e-04, rho=5.11e-01 k*=10)
- mono {THEM(THEM):1}
    - 1.68e-01 -> mono {C:1}   via C (1.68e-01, rho=5.11e-01 k*=10)
    - 1.12e-01 -> mono {X:1}   via X (1.12e-01, rho=3.58e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 3.37e-03 -> mono {or(X,X):1}   via or(X,X) (3.37e-03, rho=4.46e-01 k*=10)
    - 1.81e-03 -> mono {and(X,X):1}   via and(X,X) (1.81e-03, rho=2.40e-01 k*=10)
    - 4.65e-04 -> mono {THEM(^C):1}   via THEM(^C) (4.65e-04, rho=5.11e-01 k*=10)
