### arm=weak, n=5, game=chicken, N=10, w=0.01, x_on=True, role=True, mode=square

programs 902, classes 53, states 725, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 4.23e-02
mean payoff -1.1309, efficient 0.5000, deadweight loss 1.6309, mean bits in support 3.39

| pi | state |
|---|---|
| 0.2198 | mono {ROLE:1} |
| 0.1645 | poly {C:0.8, D:0.1, X:0.1} |
| 0.1197 | poly {C:0.7, D:0.1, X:0.2} |
| 0.0951 | mono {X:1} |
| 0.0887 | mono {D:1} |
| 0.0401 | poly {C:0.7, D:0.1, X:0.1, and(X,X):0.1} |
| 0.0348 | mono {not(ROLE):1} |
| 0.0307 | mono {C:1} |
| 0.0267 | poly {C:0.8, D:0.2} |
| 0.0220 | poly {C:0.7, D:0.1, X:0.1, or(X,X):0.1} |
| 0.0208 | poly {C:0.6, X:0.4} |
| 0.0180 | poly {C:0.7, X:0.3} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 2.37e-02 -> mono {C:1}   via C (2.37e-02, rho=9.53e-02 k*=10)
    - 2.15e-02 -> mono {X:1}   via X (2.15e-02, rho=9.28e-02 k*=10)
    - 2.07e-02 -> mono {D:1}   via D (2.07e-02, rho=8.30e-02 k*=10)
    - 8.80e-03 -> poly {ROLE:0.5, not(ROLE):0.5}   via not(ROLE) (8.80e-03, rho=1.85e-01 k*=5)
    - 6.11e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.11e-04, rho=9.76e-02 k*=10)
    - 5.72e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (5.72e-04, rho=9.15e-02 k*=10)
- poly {C:0.8, D:0.1, X:0.1}
    - 1.96e-02 -> mono {ROLE:1}   via ROLE (1.96e-02, rho=1.03e-01 k*=10)
    - 4.89e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.89e-03, rho=1.03e-01 k*=10)
    - 3.86e-03 -> poly {C:0.7, D:0.1, X:0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.7, D:0.1, X:0.1, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.09e-03 -> poly {C:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.09e-03, rho=3.34e-01 k*=3)
    - 6.33e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.33e-04, rho=1.01e-01 k*=10)
- poly {C:0.7, D:0.1, X:0.2}
    - 1.95e-02 -> mono {ROLE:1}   via ROLE (1.95e-02, rho=1.03e-01 k*=10)
    - 4.87e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.87e-03, rho=1.03e-01 k*=10)
    - 3.86e-03 -> poly {C:0.6, D:0.1, X:0.2, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.7, D:0.1, X:0.1, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.09e-03 -> poly {C:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.09e-03, rho=3.33e-01 k*=3)
    - 6.32e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.32e-04, rho=1.01e-01 k*=10)
- mono {X:1}
    - 4.25e-02 -> poly {C:0.6, X:0.4}   via C (4.25e-02, rho=1.71e-01 k*=6)
    - 2.24e-02 -> mono {D:1}   via D (2.24e-02, rho=8.98e-02 k*=10)
    - 1.98e-02 -> mono {ROLE:1}   via ROLE (1.98e-02, rho=1.04e-01 k*=10)
    - 4.93e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.93e-03, rho=1.04e-01 k*=10)
    - 6.46e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.46e-04, rho=1.03e-01 k*=10)
    - 6.06e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.06e-04, rho=9.68e-02 k*=10)
- mono {D:1}
    - 3.75e-02 -> poly {C:0.8, D:0.2}   via C (3.75e-02, rho=1.50e-01 k*=8)
    - 2.67e-02 -> mono {X:1}   via X (2.67e-02, rho=1.15e-01 k*=10)
    - 2.27e-02 -> mono {ROLE:1}   via ROLE (2.27e-02, rho=1.19e-01 k*=10)
    - 5.66e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.66e-03, rho=1.19e-01 k*=10)
    - 7.56e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.56e-04, rho=1.21e-01 k*=10)
    - 6.86e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.86e-04, rho=1.10e-01 k*=10)
- poly {C:0.7, D:0.1, X:0.1, and(X,X):0.1}
    - 1.95e-02 -> mono {ROLE:1}   via ROLE (1.95e-02, rho=1.02e-01 k*=10)
    - 4.87e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.87e-03, rho=1.02e-01 k*=10)
    - 3.86e-03 -> poly {C:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.08e-03 -> poly {C:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.08e-03, rho=3.33e-01 k*=3)
    - 6.32e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.32e-04, rho=1.01e-01 k*=10)
    - 5.85e-04 -> poly {C:0.7, not(or(X,ROLE)):0.3}   via not(or(X,ROLE)) (5.85e-04, rho=3.33e-01 k*=3)
- mono {not(ROLE):1}
    - 3.53e-02 -> poly {ROLE:0.5, not(ROLE):0.5}   via ROLE (3.53e-02, rho=1.85e-01 k*=5)
    - 2.37e-02 -> mono {C:1}   via C (2.37e-02, rho=9.53e-02 k*=10)
    - 2.15e-02 -> mono {X:1}   via X (2.15e-02, rho=9.28e-02 k*=10)
    - 2.07e-02 -> mono {D:1}   via D (2.07e-02, rho=8.30e-02 k*=10)
    - 5.89e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (5.89e-04, rho=9.40e-02 k*=10)
    - 5.50e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (5.50e-04, rho=8.80e-02 k*=10)
- mono {C:1}
    - 1.26e-01 -> poly {C:0.8, D:0.2}   via D (1.26e-01, rho=5.05e-01 k*=2)
    - 5.86e-02 -> poly {C:0.6, X:0.4}   via X (5.86e-02, rho=2.53e-01 k*=4)
    - 2.00e-02 -> mono {ROLE:1}   via ROLE (2.00e-02, rho=1.05e-01 k*=10)
    - 4.98e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.98e-03, rho=1.05e-01 k*=10)
    - 2.11e-03 -> poly {C:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.11e-03, rho=3.38e-01 k*=3)
    - 1.95e-03 -> poly {C:0.8, and(X,X):0.2}   via and(X,X) (1.95e-03, rho=5.04e-01 k*=2)
- poly {C:0.8, D:0.2}
    - 2.31e-01 -> poly {C:0.8, D:0.1, X:0.1}   via X (2.31e-01, rho=1.00e+00 k*=1)
    - 1.95e-02 -> mono {ROLE:1}   via ROLE (1.95e-02, rho=1.03e-01 k*=10)
    - 4.87e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.87e-03, rho=1.03e-01 k*=10)
    - 3.86e-03 -> poly {C:0.7, D:0.2, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.8, D:0.1, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.09e-03 -> poly {C:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.09e-03, rho=3.33e-01 k*=3)
- poly {C:0.7, D:0.1, X:0.1, or(X,X):0.1}
    - 1.96e-02 -> mono {ROLE:1}   via ROLE (1.96e-02, rho=1.03e-01 k*=10)
    - 4.88e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.88e-03, rho=1.03e-01 k*=10)
    - 3.86e-03 -> poly {C:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.09e-03 -> poly {C:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.09e-03, rho=3.34e-01 k*=3)
    - 6.32e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.32e-04, rho=1.01e-01 k*=10)
    - 5.86e-04 -> poly {C:0.7, not(or(X,ROLE)):0.3}   via not(or(X,ROLE)) (5.86e-04, rho=3.34e-01 k*=3)
- poly {C:0.6, X:0.4}
    - 2.53e-01 -> poly {C:0.7, X:0.3}   via D (2.49e-01, rho=1.00e+00 k*=1), and(X,X) (3.86e-03, rho=1.00e+00 k*=1), and(X,and(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
    - 1.95e-02 -> mono {ROLE:1}   via ROLE (1.95e-02, rho=1.03e-01 k*=10)
    - 4.87e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.87e-03, rho=1.03e-01 k*=10)
    - 3.86e-03 -> poly {C:0.6, X:0.3, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.09e-03 -> poly {C:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.09e-03, rho=3.33e-01 k*=3)
    - 6.32e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.32e-04, rho=1.01e-01 k*=10)
- poly {C:0.7, X:0.3}
    - 2.49e-01 -> poly {C:0.7, D:0.1, X:0.2}   via D (2.49e-01, rho=1.00e+00 k*=1)
    - 1.96e-02 -> mono {ROLE:1}   via ROLE (1.96e-02, rho=1.03e-01 k*=10)
    - 6.55e-03 -> poly {C:0.6, X:0.4}   via THEM(ME) (2.18e-03, rho=1.00e+00 k*=1), THEM(THEM) (2.18e-03, rho=1.00e+00 k*=1), THEM(^C) (4.39e-04, rho=1.00e+00 k*=1), THEM(^D) (4.39e-04, rho=1.00e+00 k*=1)
    - 4.89e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.89e-03, rho=1.03e-01 k*=10)
    - 3.86e-03 -> poly {C:0.6, X:0.3, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.7, X:0.2, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
