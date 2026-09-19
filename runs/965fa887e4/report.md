### arm=strong, n=6, game=stag, N=10, w=1.0, x_on=True, role=False, mode=square

programs 1726, classes 21, states 30, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 2.36e-03
mean payoff 2.9905, efficient 4.0000, deadweight loss 1.0095, mean bits in support 2.65

| pi | state |
|---|---|
| 0.9196 | mono {D:1} |
| 0.0331 | mono {X:1} |
| 0.0259 | poly {C:0.5, X:0.5} |
| 0.0092 | mono {C:1} |
| 0.0044 | mono {and(X,X):1} |
| 0.0033 | mono {THEM(ME):1} |
| 0.0027 | poly {C:0.5, X:0.4, or(X,X):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 4.40e-03 -> mono {X:1}   via X (4.40e-03, rho=1.40e-02 k*=10)
    - 7.69e-04 -> mono {C:1}   via C (7.69e-04, rho=2.32e-03 k*=10)
    - 3.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-04, rho=1.00e-01 k*=10)
    - 3.08e-04 -> mono {and(X,X):1}   via and(X,X) (3.08e-04, rho=3.85e-02 k*=10)
    - 4.49e-05 -> mono {or(X,X):1}   via or(X,X) (4.49e-05, rho=5.63e-03 k*=10)
    - 1.91e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.91e-05, rho=6.35e-02 k*=10)
- mono {X:1}
    - 7.63e-02 -> mono {D:1}   via D (7.63e-02, rho=2.30e-01 k*=10)
    - 4.87e-02 -> poly {C:0.5, X:0.5}   via C (4.87e-02, rho=1.47e-01 k*=5)
    - 1.23e-03 -> mono {and(X,X):1}   via and(X,X) (1.23e-03, rho=1.54e-01 k*=10)
    - 5.87e-04 -> mono {or(X,X):1}   via or(X,X) (5.87e-04, rho=7.36e-02 k*=10)
    - 4.54e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.54e-04, rho=1.18e-01 k*=10)
    - 1.01e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.01e-04, rho=1.18e-01 k*=10)
- poly {C:0.5, X:0.5}
    - 7.07e-02 -> mono {D:1}   via D (7.07e-02, rho=2.13e-01 k*=10)
    - 7.98e-03 -> poly {C:0.5, X:0.4, or(X,X):0.1}   via or(X,X) (7.98e-03, rho=1.00e+00 k*=1)
    - 2.51e-03 -> mono {C:1}   via THEM(ME) (1.97e-03, rho=5.13e-01 k*=2), or(X,or(X,X)) (3.01e-04, rho=1.00e+00 k*=1), or(THEM(ME),C) (1.22e-04, rho=1.00e+00 k*=1), or(THEM(ME),X) (9.32e-05, rho=1.00e+00 k*=1)
    - 1.28e-03 -> mono {and(X,X):1}   via and(X,X) (1.28e-03, rho=1.61e-01 k*=10)
    - 3.58e-04 -> mono {X:1}   via or(X,and(X,X)) (3.01e-04, rho=1.00e+00 k*=1), not(and(X,THEM(ME))) (2.87e-05, rho=1.00e+00 k*=1), not(and(THEM(ME),X)) (2.87e-05, rho=1.00e+00 k*=1)
    - 1.39e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.39e-04, rho=1.63e-01 k*=10)
- mono {C:1}
    - 5.84e-02 -> poly {C:0.5, X:0.5}   via X (5.84e-02, rho=1.86e-01 k*=5)
    - 5.15e-02 -> mono {D:1}   via D (5.15e-02, rho=1.55e-01 k*=10)
    - 1.01e-03 -> mono {and(X,X):1}   via and(X,X) (1.01e-03, rho=1.26e-01 k*=10)
    - 7.50e-04 -> mono {or(X,X):1}   via or(X,X) (7.50e-04, rho=9.40e-02 k*=10)
    - 2.77e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.77e-04, rho=7.23e-02 k*=10)
    - 1.32e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.32e-04, rho=1.55e-01 k*=10)
- mono {and(X,X):1}
    - 6.13e-02 -> mono {D:1}   via D (6.13e-02, rho=1.85e-01 k*=10)
    - 1.61e-02 -> mono {X:1}   via X (1.61e-02, rho=5.13e-02 k*=10)
    - 7.23e-03 -> mono {C:1}   via C (7.23e-03, rho=2.18e-02 k*=10)
    - 4.54e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.54e-04, rho=1.18e-01 k*=10)
    - 2.42e-04 -> mono {or(X,X):1}   via or(X,X) (2.42e-04, rho=3.04e-02 k*=10)
    - 4.18e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (4.18e-05, rho=1.39e-01 k*=10)
- mono {THEM(ME):1}
    - 5.64e-02 -> mono {C:1}   via C (5.64e-02, rho=1.70e-01 k*=10)
    - 3.32e-02 -> mono {D:1}   via D (3.32e-02, rho=1.00e-01 k*=10)
    - 2.15e-02 -> mono {X:1}   via X (2.15e-02, rho=6.84e-02 k*=10)
    - 7.98e-04 -> mono {or(X,X):1}   via or(X,X) (7.98e-04, rho=1.00e-01 k*=10)
    - 5.46e-04 -> mono {and(X,X):1}   via and(X,X) (5.46e-04, rho=6.84e-02 k*=10)
    - 8.51e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.51e-05, rho=1.00e-01 k*=10)
- poly {C:0.5, X:0.4, or(X,X):0.1}
    - 6.92e-02 -> mono {D:1}   via D (6.92e-02, rho=2.09e-01 k*=10)
    - 4.69e-03 -> mono {C:1}   via THEM(ME) (3.84e-03, rho=1.00e+00 k*=1), or(X,and(X,X)) (3.01e-04, rho=1.00e+00 k*=1), or(X,or(X,X)) (3.01e-04, rho=1.00e+00 k*=1), or(THEM(ME),C) (1.22e-04, rho=1.00e+00 k*=1)
    - 1.27e-03 -> mono {and(X,X):1}   via and(X,X) (1.27e-03, rho=1.59e-01 k*=10)
    - 1.41e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.41e-04, rho=1.66e-01 k*=10)
    - 5.73e-05 -> mono {X:1}   via not(and(X,THEM(ME))) (2.87e-05, rho=1.00e+00 k*=1), not(and(THEM(ME),X)) (2.87e-05, rho=1.00e+00 k*=1)
    - 5.52e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (5.52e-05, rho=1.83e-01 k*=10)
