### arm=weak, n=6, game=stag, N=10, w=0.1, x_on=True, role=False, mode=square

programs 1852, classes 46, states 109, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 1.41e-02
mean payoff 3.0497, efficient 4.0000, deadweight loss 0.9503, mean bits in support 2.76

| pi | state |
|---|---|
| 0.5331 | mono {D:1} |
| 0.2103 | poly {C:0.5, X:0.5} |
| 0.1034 | mono {X:1} |
| 0.1022 | mono {C:1} |
| 0.0284 | poly {C:0.5, X:0.4, or(X,X):0.1} |
| 0.0077 | mono {and(X,X):1} |
| 0.0033 | mono {or(X,X):1} |
| 0.0027 | mono {THEM(ME):1} |
| 0.0027 | mono {THEM(THEM):1} |
| 0.0012 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.96e-02 -> mono {X:1}   via X (1.96e-02, rho=6.27e-02 k*=10)
    - 1.57e-02 -> mono {C:1}   via C (1.57e-02, rho=4.77e-02 k*=10)
    - 5.87e-04 -> mono {and(X,X):1}   via and(X,X) (5.87e-04, rho=7.78e-02 k*=10)
    - 4.01e-04 -> mono {or(X,X):1}   via or(X,X) (4.01e-04, rho=5.31e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- poly {C:0.5, X:0.5}
    - 4.40e-02 -> mono {D:1}   via D (4.40e-02, rho=1.34e-01 k*=10)
    - 7.54e-03 -> poly {C:0.5, X:0.4, or(X,X):0.1}   via or(X,X) (7.54e-03, rho=1.00e+00 k*=1)
    - 6.06e-03 -> mono {C:1}   via THEM(ME) (1.86e-03, rho=5.04e-01 k*=2), THEM(THEM) (1.85e-03, rho=5.04e-01 k*=2), THEM(^X) (8.83e-04, rho=1.00e+00 k*=1), THEM(^D) (4.59e-04, rho=5.04e-01 k*=2)
    - 8.82e-04 -> mono {and(X,X):1}   via and(X,X) (8.82e-04, rho=1.17e-01 k*=10)
    - 4.69e-04 -> mono {X:1}   via or(X,and(X,X)) (2.82e-04, rho=1.00e+00 k*=1), not(THEM(^X)) (8.01e-05, rho=1.00e+00 k*=1), not(and(X,THEM(ME))) (2.66e-05, rho=1.00e+00 k*=1), not(and(X,THEM(THEM))) (2.66e-05, rho=1.00e+00 k*=1)
    - 9.72e-05 -> mono {THEM(^C):1}   via THEM(^C) (9.72e-05, rho=3.39e-01 k*=3)
- mono {X:1}
    - 6.06e-02 -> poly {C:0.5, X:0.5}   via C (6.06e-02, rho=1.84e-01 k*=5)
    - 4.43e-02 -> mono {D:1}   via D (4.43e-02, rho=1.35e-01 k*=10)
    - 8.61e-04 -> mono {and(X,X):1}   via and(X,X) (8.61e-04, rho=1.14e-01 k*=10)
    - 6.93e-04 -> mono {or(X,X):1}   via or(X,X) (6.93e-04, rho=9.19e-02 k*=10)
    - 3.89e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.89e-04, rho=1.05e-01 k*=10)
    - 3.86e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.86e-04, rho=1.05e-01 k*=10)
- mono {C:1}
    - 6.10e-02 -> poly {C:0.5, X:0.5}   via X (6.10e-02, rho=1.95e-01 k*=5)
    - 3.98e-02 -> mono {D:1}   via D (3.98e-02, rho=1.21e-01 k*=10)
    - 8.19e-04 -> mono {and(X,X):1}   via and(X,X) (8.19e-04, rho=1.09e-01 k*=10)
    - 7.38e-04 -> mono {or(X,X):1}   via or(X,X) (7.38e-04, rho=9.79e-02 k*=10)
    - 3.33e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.33e-04, rho=9.03e-02 k*=10)
    - 3.31e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.31e-04, rho=9.03e-02 k*=10)
- poly {C:0.5, X:0.4, or(X,X):0.1}
    - 4.37e-02 -> mono {D:1}   via D (4.37e-02, rho=1.33e-01 k*=10)
    - 1.05e-02 -> mono {C:1}   via THEM(ME) (3.69e-03, rho=1.00e+00 k*=1), THEM(THEM) (3.67e-03, rho=1.00e+00 k*=1), THEM(^D) (9.10e-04, rho=1.00e+00 k*=1), THEM(^X) (8.83e-04, rho=1.00e+00 k*=1)
    - 8.79e-04 -> mono {and(X,X):1}   via and(X,X) (8.79e-04, rho=1.17e-01 k*=10)
    - 1.86e-04 -> mono {X:1}   via not(THEM(^X)) (8.01e-05, rho=1.00e+00 k*=1), not(and(X,THEM(ME))) (2.66e-05, rho=1.00e+00 k*=1), not(and(X,THEM(THEM))) (2.66e-05, rho=1.00e+00 k*=1), not(and(THEM(ME),X)) (2.66e-05, rho=1.00e+00 k*=1)
    - 9.56e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (9.56e-05, rho=1.20e-01 k*=10)
    - 9.56e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (9.56e-05, rho=1.20e-01 k*=10)
- mono {and(X,X):1}
    - 4.03e-02 -> mono {D:1}   via D (4.03e-02, rho=1.23e-01 k*=10)
    - 2.64e-02 -> mono {X:1}   via X (2.64e-02, rho=8.44e-02 k*=10)
    - 2.31e-02 -> mono {C:1}   via C (2.31e-02, rho=7.02e-02 k*=10)
    - 5.65e-04 -> mono {or(X,X):1}   via or(X,X) (5.65e-04, rho=7.49e-02 k*=10)
    - 3.89e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.89e-04, rho=1.05e-01 k*=10)
    - 3.86e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.86e-04, rho=1.05e-01 k*=10)
- mono {or(X,X):1}
    - 4.40e-02 -> mono {D:1}   via D (4.40e-02, rho=1.34e-01 k*=10)
    - 3.30e-02 -> mono {X:1}   via X (3.30e-02, rho=1.06e-01 k*=10)
    - 3.28e-02 -> mono {C:1}   via C (3.28e-02, rho=9.96e-02 k*=10)
    - 8.82e-04 -> mono {and(X,X):1}   via and(X,X) (8.82e-04, rho=1.17e-01 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(ME):1}
    - 3.98e-02 -> mono {C:1}   via C (3.98e-02, rho=1.21e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 2.81e-02 -> mono {X:1}   via X (2.81e-02, rho=8.99e-02 k*=10)
    - 7.54e-04 -> mono {or(X,X):1}   via or(X,X) (7.54e-04, rho=1.00e-01 k*=10)
    - 6.78e-04 -> mono {and(X,X):1}   via and(X,X) (6.78e-04, rho=8.99e-02 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 3.98e-02 -> mono {C:1}   via C (3.98e-02, rho=1.21e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 2.81e-02 -> mono {X:1}   via X (2.81e-02, rho=8.99e-02 k*=10)
    - 7.54e-04 -> mono {or(X,X):1}   via or(X,X) (7.54e-04, rho=1.00e-01 k*=10)
    - 6.78e-04 -> mono {and(X,X):1}   via and(X,X) (6.78e-04, rho=8.99e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
- mono {THEM(^C):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 2.68e-02 -> mono {D:1}   via D (2.68e-02, rho=8.15e-02 k*=10)
    - 2.27e-02 -> mono {X:1}   via X (2.27e-02, rho=7.27e-02 k*=10)
    - 6.15e-04 -> mono {or(X,X):1}   via or(X,X) (6.15e-04, rho=8.15e-02 k*=10)
    - 5.48e-04 -> mono {and(X,X):1}   via and(X,X) (5.48e-04, rho=7.27e-02 k*=10)
    - 3.33e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.33e-04, rho=9.03e-02 k*=10)
