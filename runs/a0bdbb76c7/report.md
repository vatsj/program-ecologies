### arm=weak, n=5, game=demand, N=100, w=0.1, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 53, states 1063, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 4.50e-03
mean payoff 0.4308, efficient 0.5000, deadweight loss 0.0692, mean bits in support 3.45

| pi | state |
|---|---|
| 0.3564 | mono {ROLE:1} |
| 0.0889 | mono {not(ROLE):1} |
| 0.0634 | mono {X:1} |
| 0.0567 | poly {High:0.01, Low:0.34, X:0.65} |
| 0.0563 | poly {High:0.01, Low:0.34, X:0.63, and(X,X):0.01, or(X,X):0.01} |
| 0.0552 | poly {High:0.32, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01} |
| 0.0481 | poly {High:0.33, Low:0.66, X:0.01} |
| 0.0382 | mono {Low:1} |
| 0.0295 | poly {High:0.01, Low:0.34, X:0.64, or(X,X):0.01} |
| 0.0261 | mono {High:1} |
| 0.0261 | poly {High:0.32, Low:0.66, X:0.01, and(X,X):0.01} |
| 0.0254 | poly {High:0.33, Low:0.65, X:0.01, or(X,X):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 1.46e-03 -> mono {Low:1}   via Low (1.46e-03, rho=5.85e-03 k*=100)
    - 1.38e-03 -> mono {X:1}   via X (1.38e-03, rho=5.99e-03 k*=100)
    - 8.03e-04 -> mono {High:1}   via High (8.03e-04, rho=3.22e-03 k*=100)
    - 2.84e-04 -> mono {not(ROLE):1}   via not(ROLE) (2.84e-04, rho=5.98e-03 k*=100)
    - 4.84e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (4.84e-05, rho=7.73e-03 k*=100)
    - 3.69e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (3.69e-05, rho=5.90e-03 k*=100)
- mono {not(ROLE):1}
    - 1.46e-03 -> mono {Low:1}   via Low (1.46e-03, rho=5.85e-03 k*=100)
    - 1.38e-03 -> mono {X:1}   via X (1.38e-03, rho=5.99e-03 k*=100)
    - 1.14e-03 -> mono {ROLE:1}   via ROLE (1.14e-03, rho=5.98e-03 k*=100)
    - 8.03e-04 -> mono {High:1}   via High (8.03e-04, rho=3.22e-03 k*=100)
    - 3.77e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (3.77e-05, rho=6.02e-03 k*=100)
    - 2.88e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.88e-05, rho=4.61e-03 k*=100)
- mono {X:1}
    - 7.95e-03 -> poly {Low:0.33, X:0.67}   via Low (7.95e-03, rho=3.19e-02 k*=33)
    - 2.38e-03 -> mono {ROLE:1}   via ROLE (2.38e-03, rho=1.25e-02 k*=100)
    - 1.43e-03 -> mono {High:1}   via High (1.43e-03, rho=5.76e-03 k*=100)
    - 5.93e-04 -> mono {not(ROLE):1}   via not(ROLE) (5.93e-04, rho=1.25e-02 k*=100)
    - 7.04e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.04e-05, rho=1.12e-02 k*=100)
    - 6.08e-05 -> poly {X:0.33, or(X,X):0.67}   via or(X,X) (6.08e-05, rho=1.57e-02 k*=67)
- poly {High:0.01, Low:0.34, X:0.65}
    - 3.86e-03 -> poly {High:0.01, Low:0.34, X:0.64, or(X,X):0.01}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {High:0.01, Low:0.34, X:0.64, and(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.33e-03 -> mono {ROLE:1}   via ROLE (2.33e-03, rho=1.22e-02 k*=100)
    - 5.80e-04 -> mono {not(ROLE):1}   via not(ROLE) (5.80e-04, rho=1.22e-02 k*=100)
    - 2.19e-04 -> poly {High:0.01, Low:0.35, X:0.64}   via and(X,and(X,ROLE)) (2.19e-04, rho=1.00e+00 k*=1)
    - 1.22e-04 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.22e-04, rho=1.95e-02 k*=50)
- poly {High:0.01, Low:0.34, X:0.63, and(X,X):0.01, or(X,X):0.01}
    - 2.33e-03 -> mono {ROLE:1}   via ROLE (2.33e-03, rho=1.22e-02 k*=100)
    - 5.80e-04 -> mono {not(ROLE):1}   via not(ROLE) (5.80e-04, rho=1.22e-02 k*=100)
    - 1.46e-04 -> poly {High:0.01, Low:0.35, X:0.62, and(X,X):0.01, or(X,X):0.01}   via and(X,or(X,ROLE)) (1.46e-04, rho=1.00e+00 k*=1)
    - 1.22e-04 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.22e-04, rho=1.95e-02 k*=50)
    - 7.29e-05 -> poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
- poly {High:0.32, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01}
    - 2.33e-03 -> mono {ROLE:1}   via ROLE (2.33e-03, rho=1.22e-02 k*=100)
    - 5.80e-04 -> mono {not(ROLE):1}   via not(ROLE) (5.80e-04, rho=1.22e-02 k*=100)
    - 1.22e-04 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.22e-04, rho=1.95e-02 k*=50)
    - 7.29e-05 -> poly {High:0.32, Low:0.64, X:0.01, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {High:0.32, Low:0.64, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {High:0.31, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
- poly {High:0.33, Low:0.66, X:0.01}
    - 3.86e-03 -> poly {High:0.33, Low:0.65, X:0.01, or(X,X):0.01}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {High:0.32, Low:0.66, X:0.01, and(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.33e-03 -> mono {ROLE:1}   via ROLE (2.33e-03, rho=1.22e-02 k*=100)
    - 5.80e-04 -> mono {not(ROLE):1}   via not(ROLE) (5.80e-04, rho=1.22e-02 k*=100)
    - 1.22e-04 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.22e-04, rho=1.95e-02 k*=50)
    - 7.29e-05 -> poly {High:0.33, Low:0.65, X:0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (7.29e-05, rho=1.00e+00 k*=1)
- mono {Low:1}
    - 9.35e-03 -> poly {High:0.33, Low:0.67}   via High (9.35e-03, rho=3.75e-02 k*=33)
    - 4.29e-03 -> poly {Low:0.33, X:0.67}   via X (4.29e-03, rho=1.85e-02 k*=67)
    - 3.00e-03 -> mono {ROLE:1}   via ROLE (3.00e-03, rho=1.57e-02 k*=100)
    - 7.48e-04 -> mono {not(ROLE):1}   via not(ROLE) (7.48e-04, rho=1.57e-02 k*=100)
    - 1.59e-04 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.59e-04, rho=2.55e-02 k*=50)
    - 1.09e-04 -> poly {Low:0.56, and(X,X):0.44}   via and(X,X) (1.09e-04, rho=2.82e-02 k*=44)
- poly {High:0.01, Low:0.34, X:0.64, or(X,X):0.01}
    - 3.86e-03 -> poly {High:0.01, Low:0.34, X:0.63, and(X,X):0.01, or(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.33e-03 -> mono {ROLE:1}   via ROLE (2.33e-03, rho=1.22e-02 k*=100)
    - 5.81e-04 -> mono {not(ROLE):1}   via not(ROLE) (5.81e-04, rho=1.22e-02 k*=100)
    - 2.19e-04 -> poly {High:0.02, Low:0.34, X:0.63, or(X,X):0.01}   via and(X,and(X,ROLE)) (2.19e-04, rho=1.00e+00 k*=1)
    - 1.22e-04 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.22e-04, rho=1.95e-02 k*=50)
    - 7.29e-05 -> poly {High:0.01, Low:0.33, X:0.64, or(X,X):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (7.29e-05, rho=1.00e+00 k*=1)
- mono {High:1}
    - 8.13e-03 -> poly {High:0.33, Low:0.67}   via Low (8.13e-03, rho=3.27e-02 k*=67)
    - 4.49e-03 -> mono {X:1}   via X (4.49e-03, rho=1.94e-02 k*=100)
    - 4.32e-03 -> mono {ROLE:1}   via ROLE (4.32e-03, rho=2.27e-02 k*=100)
    - 1.08e-03 -> mono {not(ROLE):1}   via not(ROLE) (1.08e-03, rho=2.27e-02 k*=100)
    - 1.49e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.49e-04, rho=2.38e-02 k*=100)
    - 9.79e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (9.79e-05, rho=1.56e-02 k*=100)
- poly {High:0.32, Low:0.66, X:0.01, and(X,X):0.01}
    - 3.86e-03 -> poly {High:0.32, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.33e-03 -> mono {ROLE:1}   via ROLE (2.33e-03, rho=1.22e-02 k*=100)
    - 5.81e-04 -> mono {not(ROLE):1}   via not(ROLE) (5.81e-04, rho=1.22e-02 k*=100)
    - 1.22e-04 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.22e-04, rho=1.95e-02 k*=50)
    - 7.29e-05 -> poly {High:0.32, Low:0.65, X:0.01, and(X,X):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {High:0.32, Low:0.65, X:0.01, and(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
- poly {High:0.33, Low:0.65, X:0.01, or(X,X):0.01}
    - 3.86e-03 -> poly {High:0.32, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.33e-03 -> mono {ROLE:1}   via ROLE (2.33e-03, rho=1.22e-02 k*=100)
    - 5.80e-04 -> mono {not(ROLE):1}   via not(ROLE) (5.80e-04, rho=1.22e-02 k*=100)
    - 2.19e-04 -> poly {High:0.32, Low:0.65, X:0.01, or(X,X):0.02}   via or(X,or(X,ROLE)) (2.19e-04, rho=1.00e+00 k*=1)
    - 1.22e-04 -> poly {Low:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.22e-04, rho=1.95e-02 k*=50)
    - 7.29e-05 -> poly {High:0.33, Low:0.64, X:0.01, or(X,X):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (7.29e-05, rho=1.00e+00 k*=1)
