### arm=weak, n=5, game=demand, N=10, w=0.3, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 53, states 1062, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 3.79e-02
mean payoff 0.3935, efficient 0.5000, deadweight loss 0.1065, mean bits in support 3.44

| pi | state |
|---|---|
| 0.2277 | mono {ROLE:1} |
| 0.1640 | poly {High:0.3, Low:0.6, X:0.1} |
| 0.1431 | poly {High:0.1, Low:0.4, X:0.5} |
| 0.0749 | mono {High:1} |
| 0.0644 | mono {X:1} |
| 0.0568 | mono {not(ROLE):1} |
| 0.0425 | mono {Low:1} |
| 0.0259 | poly {High:0.3, Low:0.7} |
| 0.0247 | poly {Low:0.3, X:0.7} |
| 0.0220 | poly {High:0.3, Low:0.5, X:0.1, or(X,X):0.1} |
| 0.0220 | poly {High:0.2, Low:0.6, X:0.1, and(X,X):0.1} |
| 0.0217 | poly {High:0.1, Low:0.4, X:0.4, and(X,X):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 2.17e-02 -> mono {Low:1}   via Low (2.17e-02, rho=8.70e-02 k*=10)
    - 2.05e-02 -> mono {X:1}   via X (2.05e-02, rho=8.85e-02 k*=10)
    - 1.97e-02 -> mono {High:1}   via High (1.97e-02, rho=7.90e-02 k*=10)
    - 4.20e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.20e-03, rho=8.85e-02 k*=10)
    - 5.84e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (5.84e-04, rho=9.34e-02 k*=10)
    - 5.58e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (5.58e-04, rho=8.91e-02 k*=10)
- poly {High:0.3, Low:0.6, X:0.1}
    - 2.01e-02 -> mono {ROLE:1}   via ROLE (2.01e-02, rho=1.06e-01 k*=10)
    - 5.02e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.02e-03, rho=1.06e-01 k*=10)
    - 3.86e-03 -> poly {High:0.3, Low:0.5, X:0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {High:0.2, Low:0.6, X:0.1, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.33e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.33e-04, rho=1.01e-01 k*=10)
- poly {High:0.1, Low:0.4, X:0.5}
    - 2.01e-02 -> mono {ROLE:1}   via ROLE (2.01e-02, rho=1.06e-01 k*=10)
    - 5.02e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.02e-03, rho=1.06e-01 k*=10)
    - 3.86e-03 -> poly {High:0.1, Low:0.4, X:0.4, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {High:0.1, Low:0.4, X:0.4, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.33e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.33e-04, rho=1.01e-01 k*=10)
- mono {High:1}
    - 4.32e-02 -> poly {High:0.3, Low:0.7}   via Low (4.32e-02, rho=1.73e-01 k*=7)
    - 2.72e-02 -> mono {X:1}   via X (2.72e-02, rho=1.17e-01 k*=10)
    - 2.36e-02 -> mono {ROLE:1}   via ROLE (2.36e-02, rho=1.24e-01 k*=10)
    - 5.89e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.89e-03, rho=1.24e-01 k*=10)
    - 7.73e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.73e-04, rho=1.24e-01 k*=10)
    - 6.99e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.99e-04, rho=1.12e-01 k*=10)
- mono {X:1}
    - 8.37e-02 -> poly {Low:0.3, X:0.7}   via Low (8.37e-02, rho=3.36e-01 k*=3)
    - 2.23e-02 -> mono {High:1}   via High (2.23e-02, rho=8.97e-02 k*=10)
    - 2.02e-02 -> mono {ROLE:1}   via ROLE (2.02e-02, rho=1.06e-01 k*=10)
    - 5.03e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.03e-03, rho=1.06e-01 k*=10)
    - 6.40e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.40e-04, rho=1.02e-01 k*=10)
    - 6.12e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.12e-04, rho=9.78e-02 k*=10)
- mono {not(ROLE):1}
    - 2.17e-02 -> mono {Low:1}   via Low (2.17e-02, rho=8.70e-02 k*=10)
    - 2.05e-02 -> mono {X:1}   via X (2.05e-02, rho=8.85e-02 k*=10)
    - 1.97e-02 -> mono {High:1}   via High (1.97e-02, rho=7.90e-02 k*=10)
    - 1.68e-02 -> mono {ROLE:1}   via ROLE (1.68e-02, rho=8.85e-02 k*=10)
    - 5.50e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (5.50e-04, rho=8.79e-02 k*=10)
    - 5.25e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (5.25e-04, rho=8.39e-02 k*=10)
- mono {Low:1}
    - 8.75e-02 -> poly {High:0.3, Low:0.7}   via High (8.75e-02, rho=3.51e-01 k*=3)
    - 3.53e-02 -> poly {Low:0.3, X:0.7}   via X (3.53e-02, rho=1.52e-01 k*=7)
    - 2.17e-02 -> mono {ROLE:1}   via ROLE (2.17e-02, rho=1.14e-01 k*=10)
    - 5.42e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.42e-03, rho=1.14e-01 k*=10)
    - 1.34e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.34e-03, rho=2.14e-01 k*=5)
    - 1.02e-03 -> poly {Low:0.6, and(X,X):0.4}   via and(X,X) (1.02e-03, rho=2.64e-01 k*=4)
- poly {High:0.3, Low:0.7}
    - 2.31e-01 -> poly {High:0.3, Low:0.6, X:0.1}   via X (2.31e-01, rho=1.00e+00 k*=1)
    - 2.02e-02 -> mono {ROLE:1}   via ROLE (2.02e-02, rho=1.06e-01 k*=10)
    - 5.04e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.04e-03, rho=1.06e-01 k*=10)
    - 3.86e-03 -> poly {High:0.3, Low:0.6, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {High:0.3, Low:0.6, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.26e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.26e-03, rho=2.01e-01 k*=5)
- poly {Low:0.3, X:0.7}
    - 2.49e-01 -> poly {Low:0.4, X:0.6}   via High (2.49e-01, rho=1.00e+00 k*=1)
    - 2.01e-02 -> mono {ROLE:1}   via ROLE (2.01e-02, rho=1.06e-01 k*=10)
    - 5.02e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.02e-03, rho=1.06e-01 k*=10)
    - 3.86e-03 -> poly {Low:0.3, X:0.6, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {Low:0.4, X:0.5, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
- poly {High:0.3, Low:0.5, X:0.1, or(X,X):0.1}
    - 2.01e-02 -> mono {ROLE:1}   via ROLE (2.01e-02, rho=1.06e-01 k*=10)
    - 5.02e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.02e-03, rho=1.06e-01 k*=10)
    - 3.86e-03 -> poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=1.99e-01 k*=5)
    - 6.33e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.33e-04, rho=1.01e-01 k*=10)
    - 3.50e-04 -> poly {Low:0.5, not(or(X,ROLE)):0.5}   via not(or(X,ROLE)) (3.50e-04, rho=1.99e-01 k*=5)
- poly {High:0.2, Low:0.6, X:0.1, and(X,X):0.1}
    - 2.02e-02 -> mono {ROLE:1}   via ROLE (2.02e-02, rho=1.06e-01 k*=10)
    - 5.03e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.03e-03, rho=1.06e-01 k*=10)
    - 3.86e-03 -> poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.33e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.33e-04, rho=1.01e-01 k*=10)
    - 3.52e-04 -> poly {Low:0.5, not(or(X,ROLE)):0.5}   via not(or(X,ROLE)) (3.52e-04, rho=2.00e-01 k*=5)
- poly {High:0.1, Low:0.4, X:0.4, and(X,X):0.1}
    - 2.01e-02 -> mono {ROLE:1}   via ROLE (2.01e-02, rho=1.06e-01 k*=10)
    - 5.02e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.02e-03, rho=1.06e-01 k*=10)
    - 3.86e-03 -> poly {High:0.1, Low:0.4, X:0.3, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=1.99e-01 k*=5)
    - 6.33e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.33e-04, rho=1.01e-01 k*=10)
    - 3.50e-04 -> poly {Low:0.5, not(or(X,ROLE)):0.5}   via not(or(X,ROLE)) (3.50e-04, rho=1.99e-01 k*=5)
