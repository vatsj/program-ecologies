### arm=strong, n=6, game=stag, N=10, w=0.1, x_on=True, role=False, mode=square

programs 1726, classes 21, states 30, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 1.37e-02
mean payoff 3.0400, efficient 4.0000, deadweight loss 0.9600, mean bits in support 2.72

| pi | state |
|---|---|
| 0.5391 | mono {D:1} |
| 0.2136 | poly {C:0.5, X:0.5} |
| 0.1033 | mono {X:1} |
| 0.0933 | mono {C:1} |
| 0.0341 | poly {C:0.5, X:0.4, or(X,X):0.1} |
| 0.0082 | mono {and(X,X):1} |
| 0.0034 | mono {or(X,X):1} |
| 0.0028 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.97e-02 -> mono {X:1}   via X (1.97e-02, rho=6.27e-02 k*=10)
    - 1.58e-02 -> mono {C:1}   via C (1.58e-02, rho=4.77e-02 k*=10)
    - 6.21e-04 -> mono {and(X,X):1}   via and(X,X) (6.21e-04, rho=7.78e-02 k*=10)
    - 4.24e-04 -> mono {or(X,X):1}   via or(X,X) (4.24e-04, rho=5.31e-02 k*=10)
    - 3.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-04, rho=1.00e-01 k*=10)
    - 3.51e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (3.51e-05, rho=4.13e-02 k*=10)
- poly {C:0.5, X:0.5}
    - 4.44e-02 -> mono {D:1}   via D (4.44e-02, rho=1.34e-01 k*=10)
    - 7.98e-03 -> poly {C:0.5, X:0.4, or(X,X):0.1}   via or(X,X) (7.98e-03, rho=1.00e+00 k*=1)
    - 2.47e-03 -> mono {C:1}   via THEM(ME) (1.94e-03, rho=5.04e-01 k*=2), or(X,or(X,X)) (3.01e-04, rho=1.00e+00 k*=1), or(THEM(ME),C) (1.22e-04, rho=1.00e+00 k*=1), or(THEM(ME),X) (9.32e-05, rho=1.00e+00 k*=1)
    - 9.33e-04 -> mono {and(X,X):1}   via and(X,X) (9.33e-04, rho=1.17e-01 k*=10)
    - 3.58e-04 -> mono {X:1}   via or(X,and(X,X)) (3.01e-04, rho=1.00e+00 k*=1), not(and(X,THEM(ME))) (2.87e-05, rho=1.00e+00 k*=1), not(and(THEM(ME),X)) (2.87e-05, rho=1.00e+00 k*=1)
    - 1.01e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.01e-04, rho=1.19e-01 k*=10)
- mono {X:1}
    - 6.11e-02 -> poly {C:0.5, X:0.5}   via C (6.11e-02, rho=1.84e-01 k*=5)
    - 4.46e-02 -> mono {D:1}   via D (4.46e-02, rho=1.35e-01 k*=10)
    - 9.11e-04 -> mono {and(X,X):1}   via and(X,X) (9.11e-04, rho=1.14e-01 k*=10)
    - 7.33e-04 -> mono {or(X,X):1}   via or(X,X) (7.33e-04, rho=9.19e-02 k*=10)
    - 4.04e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.04e-04, rho=1.05e-01 k*=10)
    - 8.96e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.96e-05, rho=1.05e-01 k*=10)
- mono {C:1}
    - 6.13e-02 -> poly {C:0.5, X:0.5}   via X (6.13e-02, rho=1.95e-01 k*=5)
    - 4.01e-02 -> mono {D:1}   via D (4.01e-02, rho=1.21e-01 k*=10)
    - 8.67e-04 -> mono {and(X,X):1}   via and(X,X) (8.67e-04, rho=1.09e-01 k*=10)
    - 7.81e-04 -> mono {or(X,X):1}   via or(X,X) (7.81e-04, rho=9.79e-02 k*=10)
    - 3.47e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.47e-04, rho=9.03e-02 k*=10)
    - 1.03e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.03e-04, rho=1.21e-01 k*=10)
- poly {C:0.5, X:0.4, or(X,X):0.1}
    - 4.41e-02 -> mono {D:1}   via D (4.41e-02, rho=1.33e-01 k*=10)
    - 4.69e-03 -> mono {C:1}   via THEM(ME) (3.84e-03, rho=1.00e+00 k*=1), or(X,and(X,X)) (3.01e-04, rho=1.00e+00 k*=1), or(X,or(X,X)) (3.01e-04, rho=1.00e+00 k*=1), or(THEM(ME),C) (1.22e-04, rho=1.00e+00 k*=1)
    - 9.30e-04 -> mono {and(X,X):1}   via and(X,X) (9.30e-04, rho=1.17e-01 k*=10)
    - 1.02e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.02e-04, rho=1.20e-01 k*=10)
    - 5.73e-05 -> mono {X:1}   via not(and(X,THEM(ME))) (2.87e-05, rho=1.00e+00 k*=1), not(and(THEM(ME),X)) (2.87e-05, rho=1.00e+00 k*=1)
    - 3.74e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (3.74e-05, rho=1.24e-01 k*=10)
- mono {and(X,X):1}
    - 4.06e-02 -> mono {D:1}   via D (4.06e-02, rho=1.23e-01 k*=10)
    - 2.65e-02 -> mono {X:1}   via X (2.65e-02, rho=8.44e-02 k*=10)
    - 2.33e-02 -> mono {C:1}   via C (2.33e-02, rho=7.02e-02 k*=10)
    - 5.97e-04 -> mono {or(X,X):1}   via or(X,X) (5.97e-04, rho=7.49e-02 k*=10)
    - 4.04e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.04e-04, rho=1.05e-01 k*=10)
    - 6.37e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (6.37e-05, rho=7.49e-02 k*=10)
- mono {or(X,X):1}
    - 4.44e-02 -> mono {D:1}   via D (4.44e-02, rho=1.34e-01 k*=10)
    - 3.32e-02 -> mono {X:1}   via X (3.32e-02, rho=1.06e-01 k*=10)
    - 3.30e-02 -> mono {C:1}   via C (3.30e-02, rho=9.96e-02 k*=10)
    - 9.33e-04 -> mono {and(X,X):1}   via and(X,X) (9.33e-04, rho=1.17e-01 k*=10)
    - 3.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-04, rho=1.00e-01 k*=10)
    - 1.04e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.04e-04, rho=1.22e-01 k*=10)
- mono {THEM(ME):1}
    - 4.01e-02 -> mono {C:1}   via C (4.01e-02, rho=1.21e-01 k*=10)
    - 3.32e-02 -> mono {D:1}   via D (3.32e-02, rho=1.00e-01 k*=10)
    - 2.83e-02 -> mono {X:1}   via X (2.83e-02, rho=8.99e-02 k*=10)
    - 7.98e-04 -> mono {or(X,X):1}   via or(X,X) (7.98e-04, rho=1.00e-01 k*=10)
    - 7.17e-04 -> mono {and(X,X):1}   via and(X,X) (7.17e-04, rho=8.99e-02 k*=10)
    - 8.51e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.51e-05, rho=1.00e-01 k*=10)
