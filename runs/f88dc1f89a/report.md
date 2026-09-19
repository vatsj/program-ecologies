### arm=weak, n=6, game=stag, N=10, w=1.0, x_on=True, role=False, mode=square

programs 1852, classes 46, states 109, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 2.58e-03
mean payoff 2.9959, efficient 4.0000, deadweight loss 1.0041, mean bits in support 2.71

| pi | state |
|---|---|
| 0.9070 | mono {D:1} |
| 0.0335 | mono {X:1} |
| 0.0275 | poly {C:0.5, X:0.5} |
| 0.0129 | mono {C:1} |
| 0.0042 | mono {and(X,X):1} |
| 0.0032 | mono {THEM(ME):1} |
| 0.0032 | mono {THEM(THEM):1} |
| 0.0026 | poly {C:0.5, X:0.4, or(X,X):0.1} |
| 0.0019 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 4.37e-03 -> mono {X:1}   via X (4.37e-03, rho=1.40e-02 k*=10)
    - 7.63e-04 -> mono {C:1}   via C (7.63e-04, rho=2.32e-03 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
    - 2.91e-04 -> mono {and(X,X):1}   via and(X,X) (2.91e-04, rho=3.85e-02 k*=10)
    - 1.19e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.19e-04, rho=1.31e-01 k*=10)
- mono {X:1}
    - 7.57e-02 -> mono {D:1}   via D (7.57e-02, rho=2.30e-01 k*=10)
    - 4.83e-02 -> poly {C:0.5, X:0.5}   via C (4.83e-02, rho=1.47e-01 k*=5)
    - 1.16e-03 -> mono {and(X,X):1}   via and(X,X) (1.16e-03, rho=1.54e-01 k*=10)
    - 5.55e-04 -> mono {or(X,X):1}   via or(X,X) (5.55e-04, rho=7.36e-02 k*=10)
    - 4.37e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.37e-04, rho=1.18e-01 k*=10)
    - 4.34e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (4.34e-04, rho=1.18e-01 k*=10)
- poly {C:0.5, X:0.5}
    - 7.01e-02 -> mono {D:1}   via D (7.01e-02, rho=2.13e-01 k*=10)
    - 7.54e-03 -> poly {C:0.5, X:0.4, or(X,X):0.1}   via or(X,X) (7.54e-03, rho=1.00e+00 k*=1)
    - 6.15e-03 -> mono {C:1}   via THEM(ME) (1.90e-03, rho=5.13e-01 k*=2), THEM(THEM) (1.88e-03, rho=5.13e-01 k*=2), THEM(^X) (8.83e-04, rho=1.00e+00 k*=1), THEM(^D) (4.67e-04, rho=5.13e-01 k*=2)
    - 1.21e-03 -> mono {and(X,X):1}   via and(X,X) (1.21e-03, rho=1.61e-01 k*=10)
    - 4.69e-04 -> mono {X:1}   via or(X,and(X,X)) (2.82e-04, rho=1.00e+00 k*=1), not(THEM(^X)) (8.01e-05, rho=1.00e+00 k*=1), not(and(X,THEM(ME))) (2.66e-05, rho=1.00e+00 k*=1), not(and(X,THEM(THEM))) (2.66e-05, rho=1.00e+00 k*=1)
    - 1.30e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.30e-04, rho=1.63e-01 k*=10)
- mono {C:1}
    - 5.81e-02 -> poly {C:0.5, X:0.5}   via X (5.81e-02, rho=1.86e-01 k*=5)
    - 5.11e-02 -> mono {D:1}   via D (5.11e-02, rho=1.55e-01 k*=10)
    - 9.54e-04 -> mono {and(X,X):1}   via and(X,X) (9.54e-04, rho=1.26e-01 k*=10)
    - 7.09e-04 -> mono {or(X,X):1}   via or(X,X) (7.09e-04, rho=9.40e-02 k*=10)
    - 2.67e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.67e-04, rho=7.23e-02 k*=10)
    - 2.65e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.65e-04, rho=7.23e-02 k*=10)
- mono {and(X,X):1}
    - 6.08e-02 -> mono {D:1}   via D (6.08e-02, rho=1.85e-01 k*=10)
    - 1.60e-02 -> mono {X:1}   via X (1.60e-02, rho=5.13e-02 k*=10)
    - 7.18e-03 -> mono {C:1}   via C (7.18e-03, rho=2.18e-02 k*=10)
    - 4.37e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.37e-04, rho=1.18e-01 k*=10)
    - 4.34e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (4.34e-04, rho=1.18e-01 k*=10)
    - 2.29e-04 -> mono {or(X,X):1}   via or(X,X) (2.29e-04, rho=3.04e-02 k*=10)
- mono {THEM(ME):1}
    - 5.59e-02 -> mono {C:1}   via C (5.59e-02, rho=1.70e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 2.14e-02 -> mono {X:1}   via X (2.14e-02, rho=6.84e-02 k*=10)
    - 7.54e-04 -> mono {or(X,X):1}   via or(X,X) (7.54e-04, rho=1.00e-01 k*=10)
    - 5.16e-04 -> mono {and(X,X):1}   via and(X,X) (5.16e-04, rho=6.84e-02 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 5.59e-02 -> mono {C:1}   via C (5.59e-02, rho=1.70e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 2.14e-02 -> mono {X:1}   via X (2.14e-02, rho=6.84e-02 k*=10)
    - 7.54e-04 -> mono {or(X,X):1}   via or(X,X) (7.54e-04, rho=1.00e-01 k*=10)
    - 5.16e-04 -> mono {and(X,X):1}   via and(X,X) (5.16e-04, rho=6.84e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
- poly {C:0.5, X:0.4, or(X,X):0.1}
    - 6.87e-02 -> mono {D:1}   via D (6.87e-02, rho=2.09e-01 k*=10)
    - 1.05e-02 -> mono {C:1}   via THEM(ME) (3.69e-03, rho=1.00e+00 k*=1), THEM(THEM) (3.67e-03, rho=1.00e+00 k*=1), THEM(^D) (9.10e-04, rho=1.00e+00 k*=1), THEM(^X) (8.83e-04, rho=1.00e+00 k*=1)
    - 1.20e-03 -> mono {and(X,X):1}   via and(X,X) (1.20e-03, rho=1.59e-01 k*=10)
    - 1.86e-04 -> mono {X:1}   via not(THEM(^X)) (8.01e-05, rho=1.00e+00 k*=1), not(and(X,THEM(ME))) (2.66e-05, rho=1.00e+00 k*=1), not(and(X,THEM(THEM))) (2.66e-05, rho=1.00e+00 k*=1), not(and(THEM(ME),X)) (2.66e-05, rho=1.00e+00 k*=1)
    - 1.32e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.32e-04, rho=1.66e-01 k*=10)
    - 1.32e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.32e-04, rho=1.66e-01 k*=10)
- mono {THEM(^C):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 1.70e-02 -> mono {D:1}   via D (1.70e-02, rho=5.17e-02 k*=10)
    - 1.02e-02 -> mono {X:1}   via X (1.02e-02, rho=3.28e-02 k*=10)
    - 3.90e-04 -> mono {or(X,X):1}   via or(X,X) (3.90e-04, rho=5.17e-02 k*=10)
    - 2.67e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.67e-04, rho=7.23e-02 k*=10)
    - 2.65e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.65e-04, rho=7.23e-02 k*=10)
