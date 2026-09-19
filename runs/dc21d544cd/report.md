### arm=strong, n=6, game=stag, N=10, w=0.01, x_on=True, role=False, mode=square

programs 1726, classes 21, states 30, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 1.77e-02
mean payoff 3.0725, efficient 4.0000, deadweight loss 0.9275, mean bits in support 2.74

| pi | state |
|---|---|
| 0.3548 | mono {D:1} |
| 0.3268 | poly {C:0.5, X:0.5} |
| 0.1265 | mono {C:1} |
| 0.1097 | mono {X:1} |
| 0.0648 | poly {C:0.5, X:0.4, or(X,X):0.1} |
| 0.0081 | mono {and(X,X):1} |
| 0.0046 | mono {or(X,X):1} |
| 0.0023 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.06e-02 -> mono {C:1}   via C (3.06e-02, rho=9.22e-02 k*=10)
    - 2.98e-02 -> mono {X:1}   via X (2.98e-02, rho=9.48e-02 k*=10)
    - 7.74e-04 -> mono {and(X,X):1}   via and(X,X) (7.74e-04, rho=9.71e-02 k*=10)
    - 7.43e-04 -> mono {or(X,X):1}   via or(X,X) (7.43e-04, rho=9.32e-02 k*=10)
    - 3.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-04, rho=1.00e-01 k*=10)
    - 7.75e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.75e-05, rho=9.10e-02 k*=10)
- poly {C:0.5, X:0.5}
    - 3.45e-02 -> mono {D:1}   via D (3.45e-02, rho=1.04e-01 k*=10)
    - 7.98e-03 -> poly {C:0.5, X:0.4, or(X,X):0.1}   via or(X,X) (7.98e-03, rho=1.00e+00 k*=1)
    - 2.46e-03 -> mono {C:1}   via THEM(ME) (1.92e-03, rho=5.01e-01 k*=2), or(X,or(X,X)) (3.01e-04, rho=1.00e+00 k*=1), or(THEM(ME),C) (1.22e-04, rho=1.00e+00 k*=1), or(THEM(ME),X) (9.32e-05, rho=1.00e+00 k*=1)
    - 8.14e-04 -> mono {and(X,X):1}   via and(X,X) (8.14e-04, rho=1.02e-01 k*=10)
    - 3.58e-04 -> mono {X:1}   via or(X,and(X,X)) (3.01e-04, rho=1.00e+00 k*=1), not(and(X,THEM(ME))) (2.87e-05, rho=1.00e+00 k*=1), not(and(THEM(ME),X)) (2.87e-05, rho=1.00e+00 k*=1)
    - 8.72e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.72e-05, rho=1.02e-01 k*=10)
- mono {C:1}
    - 6.27e-02 -> poly {C:0.5, X:0.5}   via X (6.27e-02, rho=1.99e-01 k*=5)
    - 3.41e-02 -> mono {D:1}   via D (3.41e-02, rho=1.03e-01 k*=10)
    - 8.06e-04 -> mono {and(X,X):1}   via and(X,X) (8.06e-04, rho=1.01e-01 k*=10)
    - 7.95e-04 -> mono {or(X,X):1}   via or(X,X) (7.95e-04, rho=9.97e-02 k*=10)
    - 3.79e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.79e-04, rho=9.87e-02 k*=10)
    - 8.75e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.75e-05, rho=1.03e-01 k*=10)
- mono {X:1}
    - 6.57e-02 -> poly {C:0.5, X:0.5}   via C (6.57e-02, rho=1.98e-01 k*=5)
    - 3.45e-02 -> mono {D:1}   via D (3.45e-02, rho=1.04e-01 k*=10)
    - 8.11e-04 -> mono {and(X,X):1}   via and(X,X) (8.11e-04, rho=1.02e-01 k*=10)
    - 7.90e-04 -> mono {or(X,X):1}   via or(X,X) (7.90e-04, rho=9.90e-02 k*=10)
    - 3.86e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.86e-04, rho=1.01e-01 k*=10)
    - 8.57e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.57e-05, rho=1.01e-01 k*=10)
- poly {C:0.5, X:0.4, or(X,X):0.1}
    - 3.45e-02 -> mono {D:1}   via D (3.45e-02, rho=1.04e-01 k*=10)
    - 4.69e-03 -> mono {C:1}   via THEM(ME) (3.84e-03, rho=1.00e+00 k*=1), or(X,and(X,X)) (3.01e-04, rho=1.00e+00 k*=1), or(X,or(X,X)) (3.01e-04, rho=1.00e+00 k*=1), or(THEM(ME),C) (1.22e-04, rho=1.00e+00 k*=1)
    - 8.14e-04 -> mono {and(X,X):1}   via and(X,X) (8.14e-04, rho=1.02e-01 k*=10)
    - 8.73e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.73e-05, rho=1.02e-01 k*=10)
    - 5.73e-05 -> mono {X:1}   via not(and(X,THEM(ME))) (2.87e-05, rho=1.00e+00 k*=1), not(and(THEM(ME),X)) (2.87e-05, rho=1.00e+00 k*=1)
    - 3.10e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (3.10e-05, rho=1.03e-01 k*=10)
- mono {and(X,X):1}
    - 3.40e-02 -> mono {D:1}   via D (3.40e-02, rho=1.03e-01 k*=10)
    - 3.18e-02 -> mono {C:1}   via C (3.18e-02, rho=9.60e-02 k*=10)
    - 3.08e-02 -> mono {X:1}   via X (3.08e-02, rho=9.80e-02 k*=10)
    - 7.71e-04 -> mono {or(X,X):1}   via or(X,X) (7.71e-04, rho=9.67e-02 k*=10)
    - 3.86e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.86e-04, rho=1.01e-01 k*=10)
    - 8.23e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.23e-05, rho=9.67e-02 k*=10)
- mono {or(X,X):1}
    - 3.45e-02 -> mono {D:1}   via D (3.45e-02, rho=1.04e-01 k*=10)
    - 3.31e-02 -> mono {C:1}   via C (3.31e-02, rho=1.00e-01 k*=10)
    - 3.16e-02 -> mono {X:1}   via X (3.16e-02, rho=1.01e-01 k*=10)
    - 8.14e-04 -> mono {and(X,X):1}   via and(X,X) (8.14e-04, rho=1.02e-01 k*=10)
    - 3.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-04, rho=1.00e-01 k*=10)
    - 8.74e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.74e-05, rho=1.03e-01 k*=10)
- mono {THEM(ME):1}
    - 3.40e-02 -> mono {C:1}   via C (3.40e-02, rho=1.03e-01 k*=10)
    - 3.32e-02 -> mono {D:1}   via D (3.32e-02, rho=1.00e-01 k*=10)
    - 3.10e-02 -> mono {X:1}   via X (3.10e-02, rho=9.87e-02 k*=10)
    - 7.98e-04 -> mono {or(X,X):1}   via or(X,X) (7.98e-04, rho=1.00e-01 k*=10)
    - 7.87e-04 -> mono {and(X,X):1}   via and(X,X) (7.87e-04, rho=9.87e-02 k*=10)
    - 8.51e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.51e-05, rho=1.00e-01 k*=10)
