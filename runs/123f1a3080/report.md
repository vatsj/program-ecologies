### arm=weak, n=5, game=demand, N=10, w=0.1, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 53, states 1062, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 3.81e-02
mean payoff 0.3845, efficient 0.5000, deadweight loss 0.1155, mean bits in support 3.44

| pi | state |
|---|---|
| 0.2024 | mono {ROLE:1} |
| 0.1715 | poly {High:0.3, Low:0.6, X:0.1} |
| 0.1455 | poly {High:0.1, Low:0.4, X:0.5} |
| 0.0893 | mono {High:1} |
| 0.0639 | mono {X:1} |
| 0.0505 | mono {not(ROLE):1} |
| 0.0435 | mono {Low:1} |
| 0.0265 | poly {High:0.3, Low:0.7} |
| 0.0244 | poly {Low:0.3, X:0.7} |
| 0.0236 | poly {High:0.3, Low:0.5, X:0.1, or(X,X):0.1} |
| 0.0236 | poly {High:0.2, Low:0.6, X:0.1, and(X,X):0.1} |
| 0.0225 | poly {High:0.1, Low:0.4, X:0.4, and(X,X):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 2.38e-02 -> mono {Low:1}   via Low (2.38e-02, rho=9.56e-02 k*=10)
    - 2.31e-02 -> mono {High:1}   via High (2.31e-02, rho=9.27e-02 k*=10)
    - 2.22e-02 -> mono {X:1}   via X (2.22e-02, rho=9.61e-02 k*=10)
    - 4.56e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.56e-03, rho=9.61e-02 k*=10)
    - 6.12e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.12e-04, rho=9.78e-02 k*=10)
    - 6.03e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.03e-04, rho=9.63e-02 k*=10)
- poly {High:0.3, Low:0.6, X:0.1}
    - 1.94e-02 -> mono {ROLE:1}   via ROLE (1.94e-02, rho=1.02e-01 k*=10)
    - 4.84e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.84e-03, rho=1.02e-01 k*=10)
    - 3.86e-03 -> poly {High:0.3, Low:0.5, X:0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {High:0.2, Low:0.6, X:0.1, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.28e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.28e-04, rho=1.00e-01 k*=10)
- poly {High:0.1, Low:0.4, X:0.5}
    - 1.94e-02 -> mono {ROLE:1}   via ROLE (1.94e-02, rho=1.02e-01 k*=10)
    - 4.84e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.84e-03, rho=1.02e-01 k*=10)
    - 3.86e-03 -> poly {High:0.1, Low:0.4, X:0.4, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {High:0.1, Low:0.4, X:0.4, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.28e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.28e-04, rho=1.00e-01 k*=10)
- mono {High:1}
    - 3.80e-02 -> poly {High:0.3, Low:0.7}   via Low (3.80e-02, rho=1.53e-01 k*=7)
    - 2.44e-02 -> mono {X:1}   via X (2.44e-02, rho=1.06e-01 k*=10)
    - 2.05e-02 -> mono {ROLE:1}   via ROLE (2.05e-02, rho=1.08e-01 k*=10)
    - 5.11e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.11e-03, rho=1.08e-01 k*=10)
    - 6.73e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.73e-04, rho=1.07e-01 k*=10)
    - 6.50e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.50e-04, rho=1.04e-01 k*=10)
- mono {X:1}
    - 8.32e-02 -> poly {Low:0.3, X:0.7}   via Low (8.32e-02, rho=3.34e-01 k*=3)
    - 2.40e-02 -> mono {High:1}   via High (2.40e-02, rho=9.65e-02 k*=10)
    - 1.94e-02 -> mono {ROLE:1}   via ROLE (1.94e-02, rho=1.02e-01 k*=10)
    - 4.84e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.84e-03, rho=1.02e-01 k*=10)
    - 6.31e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.31e-04, rho=1.01e-01 k*=10)
    - 6.21e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.21e-04, rho=9.93e-02 k*=10)
- mono {not(ROLE):1}
    - 2.38e-02 -> mono {Low:1}   via Low (2.38e-02, rho=9.56e-02 k*=10)
    - 2.31e-02 -> mono {High:1}   via High (2.31e-02, rho=9.27e-02 k*=10)
    - 2.22e-02 -> mono {X:1}   via X (2.22e-02, rho=9.61e-02 k*=10)
    - 1.83e-02 -> mono {ROLE:1}   via ROLE (1.83e-02, rho=9.61e-02 k*=10)
    - 6.00e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.00e-04, rho=9.58e-02 k*=10)
    - 5.91e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (5.91e-04, rho=9.44e-02 k*=10)
- mono {Low:1}
    - 8.45e-02 -> poly {High:0.3, Low:0.7}   via High (8.45e-02, rho=3.39e-01 k*=3)
    - 3.38e-02 -> poly {Low:0.3, X:0.7}   via X (3.38e-02, rho=1.46e-01 k*=7)
    - 1.99e-02 -> mono {ROLE:1}   via ROLE (1.99e-02, rho=1.05e-01 k*=10)
    - 4.97e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.97e-03, rho=1.05e-01 k*=10)
    - 1.28e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.28e-03, rho=2.05e-01 k*=5)
    - 9.84e-04 -> poly {Low:0.6, and(X,X):0.4}   via and(X,X) (9.84e-04, rho=2.55e-01 k*=4)
- poly {High:0.3, Low:0.7}
    - 2.31e-01 -> poly {High:0.3, Low:0.6, X:0.1}   via X (2.31e-01, rho=1.00e+00 k*=1)
    - 1.94e-02 -> mono {ROLE:1}   via ROLE (1.94e-02, rho=1.02e-01 k*=10)
    - 4.85e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.85e-03, rho=1.02e-01 k*=10)
    - 3.86e-03 -> poly {High:0.3, Low:0.6, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {High:0.3, Low:0.6, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
- poly {Low:0.3, X:0.7}
    - 2.49e-01 -> poly {Low:0.4, X:0.6}   via High (2.49e-01, rho=1.00e+00 k*=1)
    - 1.94e-02 -> mono {ROLE:1}   via ROLE (1.94e-02, rho=1.02e-01 k*=10)
    - 4.84e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.84e-03, rho=1.02e-01 k*=10)
    - 3.86e-03 -> poly {Low:0.3, X:0.6, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {Low:0.4, X:0.5, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
- poly {High:0.3, Low:0.5, X:0.1, or(X,X):0.1}
    - 1.94e-02 -> mono {ROLE:1}   via ROLE (1.94e-02, rho=1.02e-01 k*=10)
    - 4.84e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.84e-03, rho=1.02e-01 k*=10)
    - 3.86e-03 -> poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.28e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.28e-04, rho=1.00e-01 k*=10)
    - 3.51e-04 -> poly {Low:0.5, not(or(X,ROLE)):0.5}   via not(or(X,ROLE)) (3.51e-04, rho=2.00e-01 k*=5)
- poly {High:0.2, Low:0.6, X:0.1, and(X,X):0.1}
    - 1.94e-02 -> mono {ROLE:1}   via ROLE (1.94e-02, rho=1.02e-01 k*=10)
    - 4.84e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.84e-03, rho=1.02e-01 k*=10)
    - 3.86e-03 -> poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.28e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.28e-04, rho=1.00e-01 k*=10)
    - 3.52e-04 -> poly {Low:0.5, not(or(X,ROLE)):0.5}   via not(or(X,ROLE)) (3.52e-04, rho=2.00e-01 k*=5)
- poly {High:0.1, Low:0.4, X:0.4, and(X,X):0.1}
    - 1.94e-02 -> mono {ROLE:1}   via ROLE (1.94e-02, rho=1.02e-01 k*=10)
    - 4.84e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.84e-03, rho=1.02e-01 k*=10)
    - 3.86e-03 -> poly {High:0.1, Low:0.4, X:0.3, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.28e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.28e-04, rho=1.00e-01 k*=10)
    - 3.51e-04 -> poly {Low:0.5, not(or(X,ROLE)):0.5}   via not(or(X,ROLE)) (3.51e-04, rho=2.00e-01 k*=5)
