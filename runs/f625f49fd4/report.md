### arm=strong, n=6, game=stag, N=100, w=0.01, x_on=True, role=False, mode=square

programs 1726, classes 21, states 30, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 1.92e-03
mean payoff 3.0584, efficient 4.0000, deadweight loss 0.9416, mean bits in support 2.70

| pi | state |
|---|---|
| 0.5738 | mono {D:1} |
| 0.1175 | poly {C:0.5, X:0.49, or(X,X):0.01} |
| 0.1094 | mono {C:1} |
| 0.0959 | mono {X:1} |
| 0.0876 | poly {C:0.5, X:0.5} |
| 0.0076 | mono {and(X,X):1} |
| 0.0032 | mono {or(X,X):1} |
| 0.0028 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.72e-03 -> mono {X:1}   via X (1.72e-03, rho=5.46e-03 k*=100)
    - 1.40e-03 -> mono {C:1}   via C (1.40e-03, rho=4.22e-03 k*=100)
    - 5.69e-05 -> mono {and(X,X):1}   via and(X,X) (5.69e-05, rho=7.14e-03 k*=100)
    - 3.84e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-05, rho=1.00e-02 k*=100)
    - 3.65e-05 -> mono {or(X,X):1}   via or(X,X) (3.65e-05, rho=4.58e-03 k*=100)
    - 2.94e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (2.94e-06, rho=3.45e-03 k*=100)
- poly {C:0.5, X:0.49, or(X,X):0.01}
    - 4.56e-03 -> mono {D:1}   via D (4.56e-03, rho=1.37e-02 k*=100)
    - 1.22e-03 -> mono {C:1}   via THEM(ME) (4.84e-04, rho=1.26e-01 k*=8), or(X,and(X,X)) (3.01e-04, rho=1.00e+00 k*=1), or(X,or(X,X)) (3.01e-04, rho=1.00e+00 k*=1), or(THEM(ME),C) (6.09e-05, rho=5.00e-01 k*=2)
    - 9.32e-05 -> mono {and(X,X):1}   via and(X,X) (9.32e-05, rho=1.17e-02 k*=100)
    - 5.73e-05 -> mono {X:1}   via not(and(X,THEM(ME))) (2.87e-05, rho=1.00e+00 k*=1), not(and(THEM(ME),X)) (2.87e-05, rho=1.00e+00 k*=1)
    - 1.02e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.02e-05, rho=1.20e-02 k*=100)
    - 3.80e-06 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (3.80e-06, rho=1.26e-02 k*=100)
- mono {C:1}
    - 5.83e-03 -> poly {C:0.5, X:0.5}   via X (5.83e-03, rho=1.85e-02 k*=50)
    - 3.77e-03 -> mono {D:1}   via D (3.77e-03, rho=1.14e-02 k*=100)
    - 8.00e-05 -> mono {and(X,X):1}   via and(X,X) (8.00e-05, rho=1.00e-02 k*=100)
    - 7.40e-05 -> mono {or(X,X):1}   via or(X,X) (7.40e-05, rho=9.27e-03 k*=100)
    - 3.25e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.25e-05, rho=8.45e-03 k*=100)
    - 9.69e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (9.69e-06, rho=1.14e-02 k*=100)
- mono {X:1}
    - 6.10e-03 -> poly {C:0.5, X:0.5}   via C (6.10e-03, rho=1.84e-02 k*=50)
    - 4.78e-03 -> mono {D:1}   via D (4.78e-03, rho=1.44e-02 k*=100)
    - 9.34e-05 -> mono {and(X,X):1}   via and(X,X) (9.34e-05, rho=1.17e-02 k*=100)
    - 7.33e-05 -> mono {or(X,X):1}   via or(X,X) (7.33e-05, rho=9.19e-03 k*=100)
    - 4.15e-05 -> mono {THEM(ME):1}   via THEM(ME) (4.15e-05, rho=1.08e-02 k*=100)
    - 9.20e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (9.20e-06, rho=1.08e-02 k*=100)
- poly {C:0.5, X:0.5}
    - 7.98e-03 -> poly {C:0.5, X:0.49, or(X,X):0.01}   via or(X,X) (7.98e-03, rho=1.00e+00 k*=1)
    - 4.56e-03 -> mono {D:1}   via D (4.56e-03, rho=1.38e-02 k*=100)
    - 9.36e-04 -> mono {C:1}   via THEM(ME) (4.84e-04, rho=1.26e-01 k*=8), or(X,or(X,X)) (3.01e-04, rho=1.00e+00 k*=1), or(THEM(ME),C) (1.22e-04, rho=1.00e+00 k*=1), or(THEM(ME),X) (1.87e-05, rho=2.00e-01 k*=5)
    - 3.58e-04 -> mono {X:1}   via or(X,and(X,X)) (3.01e-04, rho=1.00e+00 k*=1), not(and(X,THEM(ME))) (2.87e-05, rho=1.00e+00 k*=1), not(and(THEM(ME),X)) (2.87e-05, rho=1.00e+00 k*=1)
    - 9.32e-05 -> mono {and(X,X):1}   via and(X,X) (9.32e-05, rho=1.17e-02 k*=100)
    - 1.02e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.02e-05, rho=1.20e-02 k*=100)
- mono {and(X,X):1}
    - 4.33e-03 -> mono {D:1}   via D (4.33e-03, rho=1.31e-02 k*=100)
    - 2.55e-03 -> mono {X:1}   via X (2.55e-03, rho=8.12e-03 k*=100)
    - 2.27e-03 -> mono {C:1}   via C (2.27e-03, rho=6.84e-03 k*=100)
    - 5.69e-05 -> mono {or(X,X):1}   via or(X,X) (5.69e-05, rho=7.14e-03 k*=100)
    - 4.15e-05 -> mono {THEM(ME):1}   via THEM(ME) (4.15e-05, rho=1.08e-02 k*=100)
    - 6.08e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (6.08e-06, rho=7.14e-03 k*=100)
- mono {or(X,X):1}
    - 4.56e-03 -> mono {D:1}   via D (4.56e-03, rho=1.38e-02 k*=100)
    - 3.43e-03 -> mono {C:1}   via C (3.43e-03, rho=1.04e-02 k*=100)
    - 3.28e-03 -> mono {X:1}   via X (3.28e-03, rho=1.04e-02 k*=100)
    - 9.32e-05 -> mono {and(X,X):1}   via and(X,X) (9.32e-05, rho=1.17e-02 k*=100)
    - 3.84e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-05, rho=1.00e-02 k*=100)
    - 1.06e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.06e-05, rho=1.25e-02 k*=100)
- mono {THEM(ME):1}
    - 4.50e-03 -> mono {C:1}   via C (4.50e-03, rho=1.36e-02 k*=100)
    - 3.32e-03 -> mono {D:1}   via D (3.32e-03, rho=1.00e-02 k*=100)
    - 2.67e-03 -> mono {X:1}   via X (2.67e-03, rho=8.51e-03 k*=100)
    - 7.98e-05 -> mono {or(X,X):1}   via or(X,X) (7.98e-05, rho=1.00e-02 k*=100)
    - 6.79e-05 -> mono {and(X,X):1}   via and(X,X) (6.79e-05, rho=8.51e-03 k*=100)
    - 8.51e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.51e-06, rho=1.00e-02 k*=100)
