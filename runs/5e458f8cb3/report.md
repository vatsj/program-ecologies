### arm=weak, n=5, game=demand, N=100, w=0.3, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 53, states 1061, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 1.79e-03
mean payoff 0.4800, efficient 0.5000, deadweight loss 0.0200, mean bits in support 3.46

| pi | state |
|---|---|
| 0.6528 | mono {ROLE:1} |
| 0.1626 | mono {not(ROLE):1} |
| 0.0292 | mono {X:1} |
| 0.0259 | poly {High:0.01, Low:0.34, X:0.65} |
| 0.0173 | poly {High:0.01, Low:0.34, X:0.63, and(X,X):0.01, or(X,X):0.01} |
| 0.0143 | poly {High:0.33, Low:0.66, X:0.01} |
| 0.0119 | mono {Low:1} |
| 0.0118 | poly {High:0.01, Low:0.34, X:0.64, or(X,X):0.01} |
| 0.0113 | poly {High:0.32, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01} |
| 0.0077 | poly {High:0.01, Low:0.35, X:0.63, and(X,X):0.01} |
| 0.0069 | poly {High:0.32, Low:0.66, X:0.01, and(X,X):0.01} |
| 0.0067 | poly {High:0.33, Low:0.65, X:0.01, or(X,X):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 4.42e-04 -> mono {X:1}   via X (4.42e-04, rho=1.91e-03 k*=100)
    - 3.97e-04 -> mono {Low:1}   via Low (3.97e-04, rho=1.60e-03 k*=100)
    - 9.01e-05 -> mono {not(ROLE):1}   via not(ROLE) (9.01e-05, rho=1.90e-03 k*=100)
    - 4.13e-05 -> mono {High:1}   via High (4.13e-05, rho=1.66e-04 k*=100)
    - 2.72e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.72e-05, rho=4.34e-03 k*=100)
    - 1.03e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.03e-05, rho=1.65e-03 k*=100)
- mono {not(ROLE):1}
    - 4.42e-04 -> mono {X:1}   via X (4.42e-04, rho=1.91e-03 k*=100)
    - 3.97e-04 -> mono {Low:1}   via Low (3.97e-04, rho=1.60e-03 k*=100)
    - 3.61e-04 -> mono {ROLE:1}   via ROLE (3.61e-04, rho=1.90e-03 k*=100)
    - 4.13e-05 -> mono {High:1}   via High (4.13e-05, rho=1.66e-04 k*=100)
    - 1.27e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.27e-05, rho=2.02e-03 k*=100)
    - 9.02e-06 -> mono {or(X,X):1}   via or(X,X) (9.02e-06, rho=2.34e-03 k*=100)
- mono {X:1}
    - 8.81e-03 -> poly {Low:0.33, X:0.67}   via Low (8.81e-03, rho=3.54e-02 k*=33)
    - 3.30e-03 -> mono {ROLE:1}   via ROLE (3.30e-03, rho=1.73e-02 k*=100)
    - 8.23e-04 -> mono {not(ROLE):1}   via not(ROLE) (8.23e-04, rho=1.73e-02 k*=100)
    - 3.21e-04 -> mono {High:1}   via High (3.21e-04, rho=1.29e-03 k*=100)
    - 8.78e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (8.78e-05, rho=1.40e-02 k*=100)
    - 6.74e-05 -> poly {X:0.33, or(X,X):0.67}   via or(X,X) (6.74e-05, rho=1.74e-02 k*=67)
- poly {High:0.01, Low:0.34, X:0.65}
    - 3.86e-03 -> poly {High:0.01, Low:0.34, X:0.64, or(X,X):0.01}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {High:0.01, Low:0.34, X:0.64, and(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.16e-03 -> mono {ROLE:1}   via ROLE (3.16e-03, rho=1.66e-02 k*=100)
    - 7.88e-04 -> mono {not(ROLE):1}   via not(ROLE) (7.88e-04, rho=1.66e-02 k*=100)
    - 2.19e-04 -> poly {High:0.01, Low:0.35, X:0.64}   via and(X,and(X,ROLE)) (2.19e-04, rho=1.00e+00 k*=1)
    - 1.16e-04 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.16e-04, rho=1.85e-02 k*=50)
- poly {High:0.01, Low:0.34, X:0.63, and(X,X):0.01, or(X,X):0.01}
    - 3.16e-03 -> mono {ROLE:1}   via ROLE (3.16e-03, rho=1.66e-02 k*=100)
    - 7.88e-04 -> mono {not(ROLE):1}   via not(ROLE) (7.88e-04, rho=1.66e-02 k*=100)
    - 1.46e-04 -> poly {High:0.01, Low:0.35, X:0.62, and(X,X):0.01, or(X,X):0.01}   via and(X,or(X,ROLE)) (1.46e-04, rho=1.00e+00 k*=1)
    - 1.16e-04 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.16e-04, rho=1.85e-02 k*=50)
    - 7.29e-05 -> poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
- poly {High:0.33, Low:0.66, X:0.01}
    - 3.86e-03 -> poly {High:0.33, Low:0.65, X:0.01, or(X,X):0.01}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {High:0.32, Low:0.66, X:0.01, and(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.16e-03 -> mono {ROLE:1}   via ROLE (3.16e-03, rho=1.66e-02 k*=100)
    - 7.88e-04 -> mono {not(ROLE):1}   via not(ROLE) (7.88e-04, rho=1.66e-02 k*=100)
    - 1.16e-04 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.16e-04, rho=1.85e-02 k*=50)
    - 7.29e-05 -> poly {High:0.33, Low:0.65, X:0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (7.29e-05, rho=1.00e+00 k*=1)
- mono {Low:1}
    - 1.39e-02 -> poly {High:0.33, Low:0.67}   via High (1.39e-02, rho=5.57e-02 k*=33)
    - 6.40e-03 -> poly {Low:0.33, X:0.67}   via X (6.40e-03, rho=2.76e-02 k*=67)
    - 5.92e-03 -> mono {ROLE:1}   via ROLE (5.92e-03, rho=3.11e-02 k*=100)
    - 1.48e-03 -> mono {not(ROLE):1}   via not(ROLE) (1.48e-03, rho=3.11e-02 k*=100)
    - 2.48e-04 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (2.48e-04, rho=3.96e-02 k*=50)
    - 1.62e-04 -> poly {Low:0.56, and(X,X):0.44}   via and(X,X) (1.62e-04, rho=4.18e-02 k*=44)
- poly {High:0.01, Low:0.34, X:0.64, or(X,X):0.01}
    - 3.86e-03 -> poly {High:0.01, Low:0.34, X:0.63, and(X,X):0.01, or(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.16e-03 -> mono {ROLE:1}   via ROLE (3.16e-03, rho=1.66e-02 k*=100)
    - 7.89e-04 -> mono {not(ROLE):1}   via not(ROLE) (7.89e-04, rho=1.66e-02 k*=100)
    - 2.19e-04 -> poly {High:0.02, Low:0.34, X:0.63, or(X,X):0.01}   via and(X,and(X,ROLE)) (2.19e-04, rho=1.00e+00 k*=1)
    - 1.16e-04 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.16e-04, rho=1.86e-02 k*=50)
    - 7.29e-05 -> poly {High:0.01, Low:0.33, X:0.64, or(X,X):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (7.29e-05, rho=1.00e+00 k*=1)
- poly {High:0.32, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01}
    - 3.16e-03 -> mono {ROLE:1}   via ROLE (3.16e-03, rho=1.66e-02 k*=100)
    - 7.88e-04 -> mono {not(ROLE):1}   via not(ROLE) (7.88e-04, rho=1.66e-02 k*=100)
    - 1.16e-04 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.16e-04, rho=1.85e-02 k*=50)
    - 7.29e-05 -> poly {High:0.32, Low:0.64, X:0.01, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {High:0.32, Low:0.64, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {High:0.31, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
- poly {High:0.01, Low:0.35, X:0.63, and(X,X):0.01}
    - 3.86e-03 -> poly {High:0.01, Low:0.35, X:0.62, and(X,X):0.01, or(X,X):0.01}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.16e-03 -> mono {ROLE:1}   via ROLE (3.16e-03, rho=1.66e-02 k*=100)
    - 7.89e-04 -> mono {not(ROLE):1}   via not(ROLE) (7.89e-04, rho=1.66e-02 k*=100)
    - 1.16e-04 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.16e-04, rho=1.86e-02 k*=50)
    - 7.29e-05 -> poly {High:0.01, Low:0.34, X:0.63, and(X,X):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {High:0.01, Low:0.34, X:0.63, and(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
- poly {High:0.32, Low:0.66, X:0.01, and(X,X):0.01}
    - 3.86e-03 -> poly {High:0.32, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.16e-03 -> mono {ROLE:1}   via ROLE (3.16e-03, rho=1.66e-02 k*=100)
    - 7.89e-04 -> mono {not(ROLE):1}   via not(ROLE) (7.89e-04, rho=1.66e-02 k*=100)
    - 1.16e-04 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.16e-04, rho=1.86e-02 k*=50)
    - 7.29e-05 -> poly {High:0.32, Low:0.65, X:0.01, and(X,X):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {High:0.32, Low:0.65, X:0.01, and(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
- poly {High:0.33, Low:0.65, X:0.01, or(X,X):0.01}
    - 3.86e-03 -> poly {High:0.32, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.16e-03 -> mono {ROLE:1}   via ROLE (3.16e-03, rho=1.66e-02 k*=100)
    - 7.87e-04 -> mono {not(ROLE):1}   via not(ROLE) (7.87e-04, rho=1.66e-02 k*=100)
    - 2.19e-04 -> poly {High:0.32, Low:0.65, X:0.01, or(X,X):0.02}   via or(X,or(X,ROLE)) (2.19e-04, rho=1.00e+00 k*=1)
    - 1.15e-04 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.15e-04, rho=1.85e-02 k*=50)
    - 7.29e-05 -> poly {High:0.33, Low:0.64, X:0.01, or(X,X):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (7.29e-05, rho=1.00e+00 k*=1)
