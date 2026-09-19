### arm=weak, n=5, game=demand_norole, N=100, w=0.1, x_on=True, role=False, mode=square

programs 450, classes 30, states 762, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 9.57e-04
mean payoff 0.3990, efficient 0.5000, deadweight loss 0.1010, mean bits in support 3.23

| pi | state |
|---|---|
| 0.1147 | poly {C:0.33, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0989 | poly {C:0.62, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0707 | poly {C:0.34, D:0.01, X:0.63, and(X,X):0.01, or(X,X):0.01} |
| 0.0528 | poly {C:0.65, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01} |
| 0.0189 | poly {C:0.34, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0188 | poly {C:0.33, D:0.01, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0187 | poly {C:0.34, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01} |
| 0.0179 | poly {C:0.33, D:0.01, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0151 | poly {C:0.35, D:0.01, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01} |
| 0.0151 | poly {C:0.34, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01} |
| 0.0148 | poly {C:0.63, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0148 | poly {C:0.62, D:0.31, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {C:0.33, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 3.46e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.46e-05, rho=9.41e-03 k*=100)
    - 3.46e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.46e-05, rho=9.41e-03 k*=100)
    - 1.16e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.16e-05, rho=1.69e-02 k*=66)
    - 1.16e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.16e-05, rho=1.69e-02 k*=66)
    - 7.20e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.20e-06, rho=9.41e-03 k*=100)
    - 6.64e-06 -> mono {THEM(^X):1}   via THEM(^X) (6.64e-06, rho=8.68e-03 k*=100)
- poly {C:0.62, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 3.01e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.01e-05, rho=8.17e-03 k*=100)
    - 3.01e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.01e-05, rho=8.17e-03 k*=100)
    - 1.34e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.34e-05, rho=1.95e-02 k*=66)
    - 1.34e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.34e-05, rho=1.95e-02 k*=66)
    - 6.25e-06 -> mono {THEM(^C):1}   via THEM(^C) (6.25e-06, rho=8.17e-03 k*=100)
    - 5.77e-06 -> mono {THEM(^X):1}   via THEM(^X) (5.77e-06, rho=7.54e-03 k*=100)
- poly {C:0.34, D:0.01, X:0.63, and(X,X):0.01, or(X,X):0.01}
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.35, D:0.01, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.47e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.47e-05, rho=9.44e-03 k*=100)
- poly {C:0.65, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01}
    - 1.52e-04 -> poly {C:0.64, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.64, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.65, D:0.31, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.64, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.65, D:0.31, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 2.99e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.99e-05, rho=8.11e-03 k*=100)
- poly {C:0.34, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.58, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.46e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.46e-05, rho=9.40e-03 k*=100)
    - 3.46e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.46e-05, rho=9.40e-03 k*=100)
    - 1.16e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.16e-05, rho=1.69e-02 k*=66)
    - 1.16e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.16e-05, rho=1.69e-02 k*=66)
    - 7.19e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.19e-06, rho=9.40e-03 k*=100)
- poly {C:0.33, D:0.01, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.33, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.46e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.46e-05, rho=9.41e-03 k*=100)
    - 3.46e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.46e-05, rho=9.41e-03 k*=100)
    - 1.16e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.16e-05, rho=1.69e-02 k*=66)
    - 1.16e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.16e-05, rho=1.69e-02 k*=66)
    - 7.20e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.20e-06, rho=9.41e-03 k*=100)
- poly {C:0.34, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01}
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.58, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.46e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.46e-05, rho=9.41e-03 k*=100)
    - 3.46e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.46e-05, rho=9.41e-03 k*=100)
    - 1.15e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.15e-05, rho=1.67e-02 k*=67)
    - 1.15e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.15e-05, rho=1.67e-02 k*=67)
    - 7.20e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.20e-06, rho=9.41e-03 k*=100)
- poly {C:0.33, D:0.01, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.33, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.46e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.46e-05, rho=9.41e-03 k*=100)
    - 3.46e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.46e-05, rho=9.41e-03 k*=100)
    - 1.15e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.15e-05, rho=1.66e-02 k*=67)
    - 1.15e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.15e-05, rho=1.66e-02 k*=67)
    - 7.20e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.20e-06, rho=9.41e-03 k*=100)
- poly {C:0.35, D:0.01, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.35, D:0.01, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.35, D:0.01, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.35, D:0.01, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.46e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.46e-05, rho=9.40e-03 k*=100)
    - 3.46e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.46e-05, rho=9.40e-03 k*=100)
- poly {C:0.34, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}
    - 1.52e-04 -> poly {C:0.33, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.61, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.61, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.47e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.47e-05, rho=9.44e-03 k*=100)
    - 3.47e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.47e-05, rho=9.44e-03 k*=100)
- poly {C:0.63, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.62, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.00e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.00e-05, rho=8.16e-03 k*=100)
    - 3.00e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.00e-05, rho=8.16e-03 k*=100)
    - 1.34e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.34e-05, rho=1.95e-02 k*=66)
    - 1.34e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.34e-05, rho=1.95e-02 k*=66)
    - 6.24e-06 -> mono {THEM(^C):1}   via THEM(^C) (6.24e-06, rho=8.16e-03 k*=100)
- poly {C:0.62, D:0.31, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.62, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.00e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.00e-05, rho=8.16e-03 k*=100)
    - 3.00e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.00e-05, rho=8.16e-03 k*=100)
    - 1.34e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.34e-05, rho=1.95e-02 k*=66)
    - 1.34e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.34e-05, rho=1.95e-02 k*=66)
    - 6.24e-06 -> mono {THEM(^C):1}   via THEM(^C) (6.24e-06, rho=8.16e-03 k*=100)
