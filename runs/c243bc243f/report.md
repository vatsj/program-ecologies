### arm=weak, n=6, game=stag, N=10, w=0.01, x_on=True, role=False, mode=square

programs 1852, classes 46, states 109, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 1.84e-02
mean payoff 3.0862, efficient 4.0000, deadweight loss 0.9138, mean bits in support 2.78

| pi | state |
|---|---|
| 0.3519 | mono {D:1} |
| 0.3220 | poly {C:0.5, X:0.5} |
| 0.1404 | mono {C:1} |
| 0.1103 | mono {X:1} |
| 0.0527 | poly {C:0.5, X:0.4, or(X,X):0.1} |
| 0.0076 | mono {and(X,X):1} |
| 0.0045 | mono {or(X,X):1} |
| 0.0023 | mono {THEM(ME):1} |
| 0.0023 | mono {THEM(THEM):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.03e-02 -> mono {C:1}   via C (3.03e-02, rho=9.22e-02 k*=10)
    - 2.96e-02 -> mono {X:1}   via X (2.96e-02, rho=9.48e-02 k*=10)
    - 7.32e-04 -> mono {and(X,X):1}   via and(X,X) (7.32e-04, rho=9.71e-02 k*=10)
    - 7.03e-04 -> mono {or(X,X):1}   via or(X,X) (7.03e-04, rho=9.32e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- poly {C:0.5, X:0.5}
    - 3.42e-02 -> mono {D:1}   via D (3.42e-02, rho=1.04e-01 k*=10)
    - 7.54e-03 -> poly {C:0.5, X:0.4, or(X,X):0.1}   via or(X,X) (7.54e-03, rho=1.00e+00 k*=1)
    - 6.03e-03 -> mono {C:1}   via THEM(ME) (1.85e-03, rho=5.01e-01 k*=2), THEM(THEM) (1.83e-03, rho=5.01e-01 k*=2), THEM(^X) (8.83e-04, rho=1.00e+00 k*=1), THEM(^D) (4.56e-04, rho=5.01e-01 k*=2)
    - 7.70e-04 -> mono {and(X,X):1}   via and(X,X) (7.70e-04, rho=1.02e-01 k*=10)
    - 4.69e-04 -> mono {X:1}   via or(X,and(X,X)) (2.82e-04, rho=1.00e+00 k*=1), not(THEM(^X)) (8.01e-05, rho=1.00e+00 k*=1), not(and(X,THEM(ME))) (2.66e-05, rho=1.00e+00 k*=1), not(and(X,THEM(THEM))) (2.66e-05, rho=1.00e+00 k*=1)
    - 9.57e-05 -> mono {THEM(^C):1}   via THEM(^C) (9.57e-05, rho=3.34e-01 k*=3)
- mono {C:1}
    - 6.23e-02 -> poly {C:0.5, X:0.5}   via X (6.23e-02, rho=1.99e-01 k*=5)
    - 3.38e-02 -> mono {D:1}   via D (3.38e-02, rho=1.03e-01 k*=10)
    - 7.62e-04 -> mono {and(X,X):1}   via and(X,X) (7.62e-04, rho=1.01e-01 k*=10)
    - 7.52e-04 -> mono {or(X,X):1}   via or(X,X) (7.52e-04, rho=9.97e-02 k*=10)
    - 3.65e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.65e-04, rho=9.87e-02 k*=10)
    - 3.62e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.62e-04, rho=9.87e-02 k*=10)
- mono {X:1}
    - 6.51e-02 -> poly {C:0.5, X:0.5}   via C (6.51e-02, rho=1.98e-01 k*=5)
    - 3.42e-02 -> mono {D:1}   via D (3.42e-02, rho=1.04e-01 k*=10)
    - 7.67e-04 -> mono {and(X,X):1}   via and(X,X) (7.67e-04, rho=1.02e-01 k*=10)
    - 7.47e-04 -> mono {or(X,X):1}   via or(X,X) (7.47e-04, rho=9.90e-02 k*=10)
    - 3.72e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.72e-04, rho=1.01e-01 k*=10)
    - 3.69e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.69e-04, rho=1.01e-01 k*=10)
- poly {C:0.5, X:0.4, or(X,X):0.1}
    - 3.42e-02 -> mono {D:1}   via D (3.42e-02, rho=1.04e-01 k*=10)
    - 1.05e-02 -> mono {C:1}   via THEM(ME) (3.69e-03, rho=1.00e+00 k*=1), THEM(THEM) (3.67e-03, rho=1.00e+00 k*=1), THEM(^D) (9.10e-04, rho=1.00e+00 k*=1), THEM(^X) (8.83e-04, rho=1.00e+00 k*=1)
    - 7.69e-04 -> mono {and(X,X):1}   via and(X,X) (7.69e-04, rho=1.02e-01 k*=10)
    - 1.86e-04 -> mono {X:1}   via not(THEM(^X)) (8.01e-05, rho=1.00e+00 k*=1), not(and(X,THEM(ME))) (2.66e-05, rho=1.00e+00 k*=1), not(and(X,THEM(THEM))) (2.66e-05, rho=1.00e+00 k*=1), not(and(THEM(ME),X)) (2.66e-05, rho=1.00e+00 k*=1)
    - 8.50e-05 -> mono {THEM(^C):1}   via THEM(^C) (8.50e-05, rho=3.34e-01 k*=3)
    - 8.15e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (8.15e-05, rho=1.02e-01 k*=10)
- mono {and(X,X):1}
    - 3.38e-02 -> mono {D:1}   via D (3.38e-02, rho=1.03e-01 k*=10)
    - 3.16e-02 -> mono {C:1}   via C (3.16e-02, rho=9.60e-02 k*=10)
    - 3.06e-02 -> mono {X:1}   via X (3.06e-02, rho=9.80e-02 k*=10)
    - 7.29e-04 -> mono {or(X,X):1}   via or(X,X) (7.29e-04, rho=9.67e-02 k*=10)
    - 3.72e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.72e-04, rho=1.01e-01 k*=10)
    - 3.69e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.69e-04, rho=1.01e-01 k*=10)
- mono {or(X,X):1}
    - 3.42e-02 -> mono {D:1}   via D (3.42e-02, rho=1.04e-01 k*=10)
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 3.15e-02 -> mono {X:1}   via X (3.15e-02, rho=1.01e-01 k*=10)
    - 7.70e-04 -> mono {and(X,X):1}   via and(X,X) (7.70e-04, rho=1.02e-01 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(ME):1}
    - 3.37e-02 -> mono {C:1}   via C (3.37e-02, rho=1.03e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 3.08e-02 -> mono {X:1}   via X (3.08e-02, rho=9.87e-02 k*=10)
    - 7.54e-04 -> mono {or(X,X):1}   via or(X,X) (7.54e-04, rho=1.00e-01 k*=10)
    - 7.44e-04 -> mono {and(X,X):1}   via and(X,X) (7.44e-04, rho=9.87e-02 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 3.37e-02 -> mono {C:1}   via C (3.37e-02, rho=1.03e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 3.08e-02 -> mono {X:1}   via X (3.08e-02, rho=9.87e-02 k*=10)
    - 7.54e-04 -> mono {or(X,X):1}   via or(X,X) (7.54e-04, rho=1.00e-01 k*=10)
    - 7.44e-04 -> mono {and(X,X):1}   via and(X,X) (7.44e-04, rho=9.87e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
