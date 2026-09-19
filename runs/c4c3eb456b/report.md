### arm=weak, n=5, game=demand, N=100, w=0.01, x_on=True, role=True, mode=square

programs 902, classes 53, states 1235, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 6.21e-03
mean payoff 0.3875, efficient 0.5000, deadweight loss 0.1125, mean bits in support 3.40

| pi | state |
|---|---|
| 0.2041 | mono {ROLE:1} |
| 0.0862 | poly {C:0.65, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01} |
| 0.0853 | mono {D:1} |
| 0.0736 | poly {C:0.34, D:0.01, X:0.63, and(X,X):0.01, or(X,X):0.01} |
| 0.0671 | mono {X:1} |
| 0.0614 | poly {C:0.66, D:0.33, X:0.01} |
| 0.0518 | mono {not(ROLE):1} |
| 0.0455 | mono {C:1} |
| 0.0415 | poly {C:0.34, D:0.01, X:0.65} |
| 0.0355 | poly {C:0.66, D:0.32, X:0.01, and(X,X):0.01} |
| 0.0344 | poly {C:0.65, D:0.33, X:0.01, or(X,X):0.01} |
| 0.0333 | poly {C:0.34, D:0.01, X:0.64, or(X,X):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 2.37e-03 -> mono {C:1}   via C (2.37e-03, rho=9.52e-03 k*=100)
    - 2.26e-03 -> mono {D:1}   via D (2.26e-03, rho=9.06e-03 k*=100)
    - 2.20e-03 -> mono {X:1}   via X (2.20e-03, rho=9.52e-03 k*=100)
    - 9.04e-04 -> poly {ROLE:0.5, not(ROLE):0.5}   via not(ROLE) (9.04e-04, rho=1.90e-02 k*=50)
    - 6.11e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.11e-05, rho=9.76e-03 k*=100)
    - 5.96e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (5.96e-05, rho=9.52e-03 k*=100)
- poly {C:0.65, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01}
    - 1.95e-03 -> mono {ROLE:1}   via ROLE (1.95e-03, rho=1.02e-02 k*=100)
    - 4.85e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.85e-04, rho=1.02e-02 k*=100)
    - 1.25e-04 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-04, rho=2.00e-02 k*=50)
    - 7.29e-05 -> poly {C:0.64, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {C:0.64, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {C:0.65, D:0.31, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
- mono {D:1}
    - 4.05e-03 -> poly {C:0.67, D:0.33}   via C (4.05e-03, rho=1.63e-02 k*=67)
    - 2.49e-03 -> mono {X:1}   via X (2.49e-03, rho=1.07e-02 k*=100)
    - 2.10e-03 -> mono {ROLE:1}   via ROLE (2.10e-03, rho=1.10e-02 k*=100)
    - 5.23e-04 -> mono {not(ROLE):1}   via not(ROLE) (5.23e-04, rho=1.10e-02 k*=100)
    - 6.89e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.89e-05, rho=1.10e-02 k*=100)
    - 6.57e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.57e-05, rho=1.05e-02 k*=100)
- poly {C:0.34, D:0.01, X:0.63, and(X,X):0.01, or(X,X):0.01}
    - 1.95e-03 -> mono {ROLE:1}   via ROLE (1.95e-03, rho=1.02e-02 k*=100)
    - 4.85e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.85e-04, rho=1.02e-02 k*=100)
    - 2.19e-04 -> poly {C:0.35, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01}   via and(X,and(X,ROLE)) (2.19e-04, rho=1.00e+00 k*=1)
    - 1.25e-04 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-04, rho=2.00e-02 k*=50)
    - 7.29e-05 -> poly {C:0.34, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {C:0.34, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
- mono {X:1}
    - 7.58e-03 -> poly {C:0.33, X:0.67}   via C (7.58e-03, rho=3.05e-02 k*=33)
    - 2.37e-03 -> mono {D:1}   via D (2.37e-03, rho=9.52e-03 k*=100)
    - 1.95e-03 -> mono {ROLE:1}   via ROLE (1.95e-03, rho=1.02e-02 k*=100)
    - 4.87e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.87e-04, rho=1.02e-02 k*=100)
    - 6.33e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.33e-05, rho=1.01e-02 k*=100)
    - 6.18e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.18e-05, rho=9.88e-03 k*=100)
- poly {C:0.66, D:0.33, X:0.01}
    - 3.86e-03 -> poly {C:0.65, D:0.33, X:0.01, or(X,X):0.01}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.66, D:0.32, X:0.01, and(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.95e-03 -> mono {ROLE:1}   via ROLE (1.95e-03, rho=1.02e-02 k*=100)
    - 4.85e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.85e-04, rho=1.02e-02 k*=100)
    - 1.25e-04 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-04, rho=2.00e-02 k*=50)
    - 7.29e-05 -> poly {C:0.65, D:0.33, X:0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
- mono {not(ROLE):1}
    - 3.63e-03 -> poly {ROLE:0.5, not(ROLE):0.5}   via ROLE (3.63e-03, rho=1.90e-02 k*=50)
    - 2.37e-03 -> mono {C:1}   via C (2.37e-03, rho=9.52e-03 k*=100)
    - 2.26e-03 -> mono {D:1}   via D (2.26e-03, rho=9.06e-03 k*=100)
    - 2.20e-03 -> mono {X:1}   via X (2.20e-03, rho=9.52e-03 k*=100)
    - 5.96e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (5.96e-05, rho=9.52e-03 k*=100)
    - 5.82e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (5.82e-05, rho=9.29e-03 k*=100)
- mono {C:1}
    - 7.71e-03 -> poly {C:0.67, D:0.33}   via D (7.71e-03, rho=3.10e-02 k*=33)
    - 3.53e-03 -> poly {C:0.33, X:0.67}   via X (3.53e-03, rho=1.53e-02 k*=67)
    - 2.00e-03 -> mono {ROLE:1}   via ROLE (2.00e-03, rho=1.05e-02 k*=100)
    - 4.99e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.99e-04, rho=1.05e-02 k*=100)
    - 1.28e-04 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.28e-04, rho=2.05e-02 k*=50)
    - 8.97e-05 -> poly {C:0.56, and(X,X):0.44}   via and(X,X) (8.97e-05, rho=2.32e-02 k*=44)
- poly {C:0.34, D:0.01, X:0.65}
    - 8.16e-03 -> poly {C:0.35, D:0.01, X:0.64}   via and(X,ROLE) (6.26e-03, rho=1.00e+00 k*=1), not(or(X,ROLE)) (1.76e-03, rho=1.00e+00 k*=1), and(X,or(X,ROLE)) (1.46e-04, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.34, D:0.01, X:0.64, or(X,X):0.01}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.34, D:0.01, X:0.64, and(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.95e-03 -> mono {ROLE:1}   via ROLE (1.95e-03, rho=1.02e-02 k*=100)
    - 4.85e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.85e-04, rho=1.02e-02 k*=100)
    - 7.29e-05 -> poly {C:0.34, D:0.01, X:0.64, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
- poly {C:0.66, D:0.32, X:0.01, and(X,X):0.01}
    - 3.86e-03 -> poly {C:0.65, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.95e-03 -> mono {ROLE:1}   via ROLE (1.95e-03, rho=1.02e-02 k*=100)
    - 4.85e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.85e-04, rho=1.02e-02 k*=100)
    - 1.25e-04 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-04, rho=2.00e-02 k*=50)
    - 7.29e-05 -> poly {C:0.65, D:0.32, X:0.01, and(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {C:0.65, D:0.32, X:0.01, and(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
- poly {C:0.65, D:0.33, X:0.01, or(X,X):0.01}
    - 3.86e-03 -> poly {C:0.65, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.95e-03 -> mono {ROLE:1}   via ROLE (1.95e-03, rho=1.02e-02 k*=100)
    - 4.85e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.85e-04, rho=1.02e-02 k*=100)
    - 2.19e-04 -> poly {C:0.65, D:0.32, X:0.01, or(X,X):0.02}   via or(X,or(X,ROLE)) (2.19e-04, rho=1.00e+00 k*=1)
    - 1.25e-04 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-04, rho=1.99e-02 k*=50)
    - 7.29e-05 -> poly {C:0.64, D:0.33, X:0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
- poly {C:0.34, D:0.01, X:0.64, or(X,X):0.01}
    - 3.86e-03 -> poly {C:0.34, D:0.01, X:0.63, and(X,X):0.01, or(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.95e-03 -> mono {ROLE:1}   via ROLE (1.95e-03, rho=1.02e-02 k*=100)
    - 4.85e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.85e-04, rho=1.02e-02 k*=100)
    - 2.19e-04 -> poly {C:0.34, D:0.02, X:0.63, or(X,X):0.01}   via and(X,and(X,ROLE)) (2.19e-04, rho=1.00e+00 k*=1)
    - 1.25e-04 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-04, rho=2.00e-02 k*=50)
    - 7.29e-05 -> poly {C:0.33, D:0.01, X:0.64, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
