### arm=weak, n=5, game=demand, N=10, w=1.0, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 53, states 1041, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 3.51e-02
mean payoff 0.4213, efficient 0.5000, deadweight loss 0.0787, mean bits in support 3.46

| pi | state |
|---|---|
| 0.3274 | mono {ROLE:1} |
| 0.1302 | poly {High:0.3, Low:0.6, X:0.1} |
| 0.1281 | poly {High:0.1, Low:0.4, X:0.5} |
| 0.0816 | mono {not(ROLE):1} |
| 0.0629 | mono {X:1} |
| 0.0380 | mono {High:1} |
| 0.0367 | mono {Low:1} |
| 0.0243 | poly {Low:0.3, X:0.7} |
| 0.0223 | poly {High:0.3, Low:0.7} |
| 0.0205 | poly {Low:0.4, X:0.6} |
| 0.0181 | poly {High:0.1, Low:0.4, X:0.4, and(X,X):0.1} |
| 0.0161 | poly {High:0.3, Low:0.5, X:0.1, or(X,X):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 1.52e-02 -> mono {Low:1}   via Low (1.52e-02, rho=6.12e-02 k*=10)
    - 1.52e-02 -> mono {X:1}   via X (1.52e-02, rho=6.58e-02 k*=10)
    - 1.05e-02 -> mono {High:1}   via High (1.05e-02, rho=4.22e-02 k*=10)
    - 3.10e-03 -> mono {not(ROLE):1}   via not(ROLE) (3.10e-03, rho=6.52e-02 k*=10)
    - 4.95e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (4.95e-04, rho=7.90e-02 k*=10)
    - 4.18e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (4.18e-04, rho=6.68e-02 k*=10)
- poly {High:0.3, Low:0.6, X:0.1}
    - 2.27e-02 -> mono {ROLE:1}   via ROLE (2.27e-02, rho=1.19e-01 k*=10)
    - 5.65e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.65e-03, rho=1.19e-01 k*=10)
    - 3.86e-03 -> poly {High:0.3, Low:0.5, X:0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {High:0.2, Low:0.6, X:0.1, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.48e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.48e-04, rho=1.04e-01 k*=10)
- poly {High:0.1, Low:0.4, X:0.5}
    - 2.27e-02 -> mono {ROLE:1}   via ROLE (2.27e-02, rho=1.19e-01 k*=10)
    - 5.65e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.65e-03, rho=1.19e-01 k*=10)
    - 3.86e-03 -> poly {High:0.1, Low:0.4, X:0.4, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {High:0.1, Low:0.4, X:0.4, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.48e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.48e-04, rho=1.04e-01 k*=10)
- mono {not(ROLE):1}
    - 1.52e-02 -> mono {Low:1}   via Low (1.52e-02, rho=6.12e-02 k*=10)
    - 1.52e-02 -> mono {X:1}   via X (1.52e-02, rho=6.58e-02 k*=10)
    - 1.24e-02 -> mono {ROLE:1}   via ROLE (1.24e-02, rho=6.52e-02 k*=10)
    - 1.05e-02 -> mono {High:1}   via High (1.05e-02, rho=4.22e-02 k*=10)
    - 4.03e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (4.03e-04, rho=6.43e-02 k*=10)
    - 3.41e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (3.41e-04, rho=5.45e-02 k*=10)
- mono {X:1}
    - 8.53e-02 -> poly {Low:0.3, X:0.7}   via Low (8.53e-02, rho=3.43e-01 k*=3)
    - 2.28e-02 -> mono {ROLE:1}   via ROLE (2.28e-02, rho=1.20e-01 k*=10)
    - 1.68e-02 -> mono {High:1}   via High (1.68e-02, rho=6.74e-02 k*=10)
    - 5.69e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.69e-03, rho=1.20e-01 k*=10)
    - 6.74e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.74e-04, rho=1.08e-01 k*=10)
    - 5.80e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (5.80e-04, rho=9.27e-02 k*=10)
- mono {High:1}
    - 6.48e-02 -> poly {High:0.3, Low:0.7}   via Low (6.48e-02, rho=2.60e-01 k*=7)
    - 3.83e-02 -> mono {X:1}   via X (3.83e-02, rho=1.66e-01 k*=10)
    - 3.60e-02 -> mono {ROLE:1}   via ROLE (3.60e-02, rho=1.89e-01 k*=10)
    - 8.99e-03 -> mono {not(ROLE):1}   via not(ROLE) (8.99e-03, rho=1.89e-01 k*=10)
    - 1.21e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.21e-03, rho=1.93e-01 k*=10)
    - 8.85e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (8.85e-04, rho=1.41e-01 k*=10)
- mono {Low:1}
    - 9.82e-02 -> poly {High:0.3, Low:0.7}   via High (9.82e-02, rho=3.94e-01 k*=3)
    - 4.08e-02 -> poly {Low:0.3, X:0.7}   via X (4.08e-02, rho=1.76e-01 k*=7)
    - 2.87e-02 -> mono {ROLE:1}   via ROLE (2.87e-02, rho=1.51e-01 k*=10)
    - 7.15e-03 -> mono {not(ROLE):1}   via not(ROLE) (7.15e-03, rho=1.51e-01 k*=10)
    - 1.56e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.56e-03, rho=2.50e-01 k*=5)
    - 1.16e-03 -> poly {Low:0.6, and(X,X):0.4}   via and(X,X) (1.16e-03, rho=2.99e-01 k*=4)
- poly {Low:0.3, X:0.7}
    - 2.49e-01 -> poly {Low:0.4, X:0.6}   via High (2.49e-01, rho=1.00e+00 k*=1)
    - 2.27e-02 -> mono {ROLE:1}   via ROLE (2.27e-02, rho=1.19e-01 k*=10)
    - 5.65e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.65e-03, rho=1.19e-01 k*=10)
    - 3.86e-03 -> poly {Low:0.3, X:0.6, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {Low:0.4, X:0.5, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
- poly {High:0.3, Low:0.7}
    - 2.31e-01 -> poly {High:0.3, Low:0.6, X:0.1}   via X (2.31e-01, rho=1.00e+00 k*=1)
    - 2.30e-02 -> mono {ROLE:1}   via ROLE (2.30e-02, rho=1.21e-01 k*=10)
    - 5.72e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.72e-03, rho=1.21e-01 k*=10)
    - 3.86e-03 -> poly {High:0.3, Low:0.6, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {High:0.3, Low:0.6, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.27e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.27e-03, rho=2.03e-01 k*=5)
- poly {Low:0.4, X:0.6}
    - 2.49e-01 -> poly {High:0.1, Low:0.4, X:0.5}   via High (2.49e-01, rho=1.00e+00 k*=1)
    - 2.30e-02 -> mono {ROLE:1}   via ROLE (2.30e-02, rho=1.21e-01 k*=10)
    - 6.70e-03 -> poly {Low:0.3, X:0.7}   via THEM(ME) (2.18e-03, rho=1.00e+00 k*=1), THEM(THEM) (2.18e-03, rho=1.00e+00 k*=1), THEM(^High) (4.39e-04, rho=1.00e+00 k*=1), THEM(^Low) (4.39e-04, rho=1.00e+00 k*=1)
    - 5.72e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.72e-03, rho=1.21e-01 k*=10)
    - 3.86e-03 -> poly {Low:0.3, X:0.6, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {Low:0.4, X:0.5, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.4, X:0.4, and(X,X):0.1}
    - 2.26e-02 -> mono {ROLE:1}   via ROLE (2.26e-02, rho=1.19e-01 k*=10)
    - 5.63e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.63e-03, rho=1.19e-01 k*=10)
    - 3.86e-03 -> poly {High:0.1, Low:0.4, X:0.3, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.24e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.24e-03, rho=1.98e-01 k*=5)
    - 6.49e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.49e-04, rho=1.04e-01 k*=10)
    - 3.48e-04 -> poly {Low:0.5, not(or(X,ROLE)):0.5}   via not(or(X,ROLE)) (3.48e-04, rho=1.98e-01 k*=5)
- poly {High:0.3, Low:0.5, X:0.1, or(X,X):0.1}
    - 2.26e-02 -> mono {ROLE:1}   via ROLE (2.26e-02, rho=1.19e-01 k*=10)
    - 5.63e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.63e-03, rho=1.19e-01 k*=10)
    - 3.86e-03 -> poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.24e-03 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.24e-03, rho=1.98e-01 k*=5)
    - 6.49e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.49e-04, rho=1.04e-01 k*=10)
    - 3.48e-04 -> poly {Low:0.5, not(or(X,ROLE)):0.5}   via not(or(X,ROLE)) (3.48e-04, rho=1.98e-01 k*=5)
