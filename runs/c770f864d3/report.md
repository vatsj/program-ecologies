### arm=weak, n=5, game=demand, N=10, w=0.1, x_on=True, role=True, mode=square

programs 902, classes 53, states 1173, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 4.27e-02
mean payoff 0.3841, efficient 0.5000, deadweight loss 0.1159, mean bits in support 3.41

| pi | state |
|---|---|
| 0.2168 | mono {ROLE:1} |
| 0.1699 | poly {C:0.6, D:0.3, X:0.1} |
| 0.1444 | poly {C:0.4, D:0.1, X:0.5} |
| 0.0886 | mono {D:1} |
| 0.0633 | mono {X:1} |
| 0.0433 | mono {C:1} |
| 0.0335 | mono {not(ROLE):1} |
| 0.0262 | poly {C:0.7, D:0.3} |
| 0.0242 | poly {C:0.3, X:0.7} |
| 0.0234 | poly {C:0.5, D:0.3, X:0.1, or(X,X):0.1} |
| 0.0234 | poly {C:0.6, D:0.2, X:0.1, and(X,X):0.1} |
| 0.0224 | poly {C:0.4, D:0.1, X:0.4, and(X,X):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 2.38e-02 -> mono {C:1}   via C (2.38e-02, rho=9.57e-02 k*=10)
    - 2.31e-02 -> mono {D:1}   via D (2.31e-02, rho=9.29e-02 k*=10)
    - 2.23e-02 -> mono {X:1}   via X (2.23e-02, rho=9.62e-02 k*=10)
    - 9.14e-03 -> poly {ROLE:0.5, not(ROLE):0.5}   via not(ROLE) (9.14e-03, rho=1.92e-01 k*=5)
    - 6.13e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.13e-04, rho=9.79e-02 k*=10)
    - 6.04e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.04e-04, rho=9.64e-02 k*=10)
- poly {C:0.6, D:0.3, X:0.1}
    - 1.94e-02 -> mono {ROLE:1}   via ROLE (1.94e-02, rho=1.02e-01 k*=10)
    - 4.84e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.84e-03, rho=1.02e-01 k*=10)
    - 3.86e-03 -> poly {C:0.5, D:0.3, X:0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.6, D:0.2, X:0.1, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.28e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.28e-04, rho=1.00e-01 k*=10)
- poly {C:0.4, D:0.1, X:0.5}
    - 1.94e-02 -> mono {ROLE:1}   via ROLE (1.94e-02, rho=1.02e-01 k*=10)
    - 4.84e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.84e-03, rho=1.02e-01 k*=10)
    - 3.86e-03 -> poly {C:0.4, D:0.1, X:0.4, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.4, D:0.1, X:0.4, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.28e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.28e-04, rho=1.00e-01 k*=10)
- mono {D:1}
    - 3.79e-02 -> poly {C:0.7, D:0.3}   via C (3.79e-02, rho=1.52e-01 k*=7)
    - 2.44e-02 -> mono {X:1}   via X (2.44e-02, rho=1.06e-01 k*=10)
    - 2.05e-02 -> mono {ROLE:1}   via ROLE (2.05e-02, rho=1.08e-01 k*=10)
    - 5.11e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.11e-03, rho=1.08e-01 k*=10)
    - 6.71e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.71e-04, rho=1.07e-01 k*=10)
    - 6.49e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.49e-04, rho=1.04e-01 k*=10)
- mono {X:1}
    - 8.32e-02 -> poly {C:0.3, X:0.7}   via C (8.32e-02, rho=3.34e-01 k*=3)
    - 2.40e-02 -> mono {D:1}   via D (2.40e-02, rho=9.66e-02 k*=10)
    - 1.94e-02 -> mono {ROLE:1}   via ROLE (1.94e-02, rho=1.02e-01 k*=10)
    - 4.84e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.84e-03, rho=1.02e-01 k*=10)
    - 6.30e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.30e-04, rho=1.01e-01 k*=10)
    - 6.21e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.21e-04, rho=9.93e-02 k*=10)
- mono {C:1}
    - 8.44e-02 -> poly {C:0.7, D:0.3}   via D (8.44e-02, rho=3.39e-01 k*=3)
    - 3.37e-02 -> poly {C:0.3, X:0.7}   via X (3.37e-02, rho=1.46e-01 k*=7)
    - 1.99e-02 -> mono {ROLE:1}   via ROLE (1.99e-02, rho=1.04e-01 k*=10)
    - 4.96e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.96e-03, rho=1.04e-01 k*=10)
    - 1.28e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.28e-03, rho=2.04e-01 k*=5)
    - 9.83e-04 -> poly {C:0.6, and(X,X):0.4}   via and(X,X) (9.83e-04, rho=2.55e-01 k*=4)
- mono {not(ROLE):1}
    - 3.66e-02 -> poly {ROLE:0.5, not(ROLE):0.5}   via ROLE (3.66e-02, rho=1.92e-01 k*=5)
    - 2.38e-02 -> mono {C:1}   via C (2.38e-02, rho=9.57e-02 k*=10)
    - 2.31e-02 -> mono {D:1}   via D (2.31e-02, rho=9.29e-02 k*=10)
    - 2.23e-02 -> mono {X:1}   via X (2.23e-02, rho=9.62e-02 k*=10)
    - 6.01e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.01e-04, rho=9.60e-02 k*=10)
    - 5.92e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (5.92e-04, rho=9.46e-02 k*=10)
- poly {C:0.7, D:0.3}
    - 2.31e-01 -> poly {C:0.6, D:0.3, X:0.1}   via X (2.31e-01, rho=1.00e+00 k*=1)
    - 1.94e-02 -> mono {ROLE:1}   via ROLE (1.94e-02, rho=1.02e-01 k*=10)
    - 4.84e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.84e-03, rho=1.02e-01 k*=10)
    - 3.86e-03 -> poly {C:0.6, D:0.3, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.6, D:0.3, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
- poly {C:0.3, X:0.7}
    - 2.49e-01 -> poly {C:0.4, X:0.6}   via D (2.49e-01, rho=1.00e+00 k*=1)
    - 1.94e-02 -> mono {ROLE:1}   via ROLE (1.94e-02, rho=1.02e-01 k*=10)
    - 4.84e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.84e-03, rho=1.02e-01 k*=10)
    - 3.86e-03 -> poly {C:0.3, X:0.6, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.4, X:0.5, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
- poly {C:0.5, D:0.3, X:0.1, or(X,X):0.1}
    - 1.94e-02 -> mono {ROLE:1}   via ROLE (1.94e-02, rho=1.02e-01 k*=10)
    - 4.84e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.84e-03, rho=1.02e-01 k*=10)
    - 3.86e-03 -> poly {C:0.5, D:0.2, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.28e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.28e-04, rho=1.00e-01 k*=10)
    - 3.51e-04 -> poly {C:0.5, not(or(X,ROLE)):0.5}   via not(or(X,ROLE)) (3.51e-04, rho=2.00e-01 k*=5)
- poly {C:0.6, D:0.2, X:0.1, and(X,X):0.1}
    - 1.94e-02 -> mono {ROLE:1}   via ROLE (1.94e-02, rho=1.02e-01 k*=10)
    - 4.84e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.84e-03, rho=1.02e-01 k*=10)
    - 3.86e-03 -> poly {C:0.5, D:0.2, X:0.1, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.28e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.28e-04, rho=1.00e-01 k*=10)
    - 3.52e-04 -> poly {C:0.5, not(or(X,ROLE)):0.5}   via not(or(X,ROLE)) (3.52e-04, rho=2.00e-01 k*=5)
- poly {C:0.4, D:0.1, X:0.4, and(X,X):0.1}
    - 1.94e-02 -> mono {ROLE:1}   via ROLE (1.94e-02, rho=1.02e-01 k*=10)
    - 4.84e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.84e-03, rho=1.02e-01 k*=10)
    - 3.86e-03 -> poly {C:0.4, D:0.1, X:0.3, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.28e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.28e-04, rho=1.00e-01 k*=10)
    - 3.51e-04 -> poly {C:0.5, not(or(X,ROLE)):0.5}   via not(or(X,ROLE)) (3.51e-04, rho=2.00e-01 k*=5)
