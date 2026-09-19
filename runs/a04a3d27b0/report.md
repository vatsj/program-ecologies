### arm=weak, n=6, game=stag, N=100, w=0.1, x_on=True, role=False, mode=square

programs 1852, classes 46, states 111, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 6.66e-05
mean payoff 3.0191, efficient 4.0000, deadweight loss 0.9809, mean bits in support 2.68

| pi | state |
|---|---|
| 0.9707 | mono {D:1} |
| 0.0140 | mono {C:1} |
| 0.0055 | mono {THEM(^C):1} |
| 0.0023 | poly {C:0.5, X:0.5} |
| 0.0016 | mono {THEM(ME):1} |
| 0.0015 | mono {THEM(THEM):1} |
| 0.0013 | poly {C:0.5, X:0.49, or(X,X):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 1.98e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.98e-05, rho=2.17e-02 k*=100)
    - 9.10e-06 -> mono {THEM(^D):1}   via THEM(^D) (9.10e-06, rho=1.00e-02 k*=100)
    - 5.41e-06 -> mono {X:1}   via X (5.41e-06, rho=1.73e-05 k*=100)
    - 3.91e-06 -> mono {THEM(^X):1}   via THEM(^X) (3.91e-06, rho=4.43e-03 k*=100)
- mono {C:1}
    - 3.40e-03 -> poly {C:0.5, X:0.5}   via X (3.40e-03, rho=1.09e-02 k*=50)
    - 3.29e-03 -> mono {D:1}   via D (3.29e-03, rho=1.00e-02 k*=100)
    - 5.78e-05 -> mono {and(X,X):1}   via and(X,X) (5.78e-05, rho=7.67e-03 k*=100)
    - 4.13e-05 -> mono {or(X,X):1}   via or(X,X) (4.13e-05, rho=5.48e-03 k*=100)
    - 9.10e-06 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-06, rho=1.00e-02 k*=100)
    - 7.97e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (7.97e-06, rho=1.00e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 1.81e-04 -> mono {D:1}   via D (1.81e-04, rho=5.50e-04 k*=100)
    - 2.92e-05 -> mono {X:1}   via X (2.92e-05, rho=9.34e-05 k*=100)
    - 9.63e-06 -> poly {THEM(^C):0.5, THEM(^X):0.5}   via THEM(^X) (9.63e-06, rho=1.09e-02 k*=50)
    - 9.11e-06 -> mono {THEM(^D):1}   via THEM(^D) (9.11e-06, rho=1.00e-02 k*=100)
    - 5.92e-06 -> mono {THEM(ME):1}   via THEM(ME) (5.92e-06, rho=1.60e-03 k*=100)
- poly {C:0.5, X:0.5}
    - 1.11e-02 -> mono {D:1}   via D (1.11e-02, rho=3.37e-02 k*=100)
    - 7.54e-03 -> poly {C:0.5, X:0.49, or(X,X):0.01}   via or(X,X) (7.54e-03, rho=1.00e+00 k*=1)
    - 1.88e-03 -> mono {C:1}   via THEM(ME) (4.91e-04, rho=1.33e-01 k*=8), THEM(THEM) (4.88e-04, rho=1.33e-01 k*=8), or(X,or(X,X)) (2.82e-04, rho=1.00e+00 k*=1), THEM(^X) (1.33e-04, rho=1.51e-01 k*=7)
    - 4.76e-04 -> mono {X:1}   via or(X,and(X,X)) (2.82e-04, rho=1.00e+00 k*=1), not(THEM(^X)) (8.79e-05, rho=1.00e+00 k*=1), not(and(X,THEM(ME))) (2.66e-05, rho=1.00e+00 k*=1), not(and(X,THEM(THEM))) (2.66e-05, rho=1.00e+00 k*=1)
    - 1.73e-04 -> mono {and(X,X):1}   via and(X,X) (1.73e-04, rho=2.29e-02 k*=100)
    - 1.64e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.64e-05, rho=2.06e-02 k*=100)
- mono {THEM(ME):1}
    - 1.90e-02 -> mono {C:1}   via C (1.90e-02, rho=5.78e-02 k*=100)
    - 3.29e-03 -> mono {D:1}   via D (3.29e-03, rho=1.00e-02 k*=100)
    - 7.44e-04 -> mono {X:1}   via X (7.44e-04, rho=2.38e-03 k*=100)
    - 7.54e-05 -> mono {or(X,X):1}   via or(X,X) (7.54e-05, rho=1.00e-02 k*=100)
    - 5.26e-05 -> mono {THEM(^C):1}   via THEM(^C) (5.26e-05, rho=5.78e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
- mono {THEM(THEM):1}
    - 1.90e-02 -> mono {C:1}   via C (1.90e-02, rho=5.78e-02 k*=100)
    - 3.29e-03 -> mono {D:1}   via D (3.29e-03, rho=1.00e-02 k*=100)
    - 7.44e-04 -> mono {X:1}   via X (7.44e-04, rho=2.38e-03 k*=100)
    - 7.54e-05 -> mono {or(X,X):1}   via or(X,X) (7.54e-05, rho=1.00e-02 k*=100)
    - 5.26e-05 -> mono {THEM(^C):1}   via THEM(^C) (5.26e-05, rho=5.78e-02 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
- poly {C:0.5, X:0.49, or(X,X):0.01}
    - 1.10e-02 -> mono {D:1}   via D (1.10e-02, rho=3.35e-02 k*=100)
    - 2.18e-03 -> mono {C:1}   via THEM(ME) (4.91e-04, rho=1.33e-01 k*=8), THEM(THEM) (4.87e-04, rho=1.33e-01 k*=8), or(X,and(X,X)) (2.82e-04, rho=1.00e+00 k*=1), or(X,or(X,X)) (2.82e-04, rho=1.00e+00 k*=1)
    - 1.94e-04 -> mono {X:1}   via not(THEM(^X)) (8.79e-05, rho=1.00e+00 k*=1), not(and(X,THEM(ME))) (2.66e-05, rho=1.00e+00 k*=1), not(and(X,THEM(THEM))) (2.66e-05, rho=1.00e+00 k*=1), not(and(THEM(ME),X)) (2.66e-05, rho=1.00e+00 k*=1)
    - 1.72e-04 -> mono {and(X,X):1}   via and(X,X) (1.72e-04, rho=2.28e-02 k*=100)
    - 1.64e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.64e-05, rho=2.06e-02 k*=100)
    - 1.64e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.64e-05, rho=2.06e-02 k*=100)
