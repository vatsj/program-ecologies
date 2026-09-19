### arm=weak, n=5, game=chicken_norole, N=100, w=0.01, x_on=True, role=False, mode=square

programs 450, classes 30, states 891, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 8.21e-04
mean payoff -0.1952, efficient 0.5000, deadweight loss 0.6952, mean bits in support 3.25

| pi | state |
|---|---|
| 0.1055 | poly {C:0.77, D:0.15, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0698 | poly {C:0.64, D:0.01, X:0.28, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0540 | poly {C:0.8, D:0.17, X:0.01, and(X,X):0.01, or(X,X):0.01} |
| 0.0465 | poly {C:0.63, D:0.01, X:0.29, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0335 | poly {C:0.64, D:0.01, X:0.33, and(X,X):0.01, or(X,X):0.01} |
| 0.0332 | poly {C:0.65, D:0.01, X:0.32, and(X,X):0.01, or(X,X):0.01} |
| 0.0180 | poly {C:0.64, D:0.01, X:0.29, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0180 | poly {C:0.64, D:0.01, X:0.29, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0180 | poly {C:0.63, D:0.01, X:0.3, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0180 | poly {C:0.63, D:0.01, X:0.3, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0155 | poly {C:0.77, D:0.16, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0155 | poly {C:0.78, D:0.15, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {C:0.77, D:0.15, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 2.93e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.93e-05, rho=7.98e-03 k*=100)
    - 2.93e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.93e-05, rho=7.98e-03 k*=100)
    - 1.35e-05 -> poly {D:0.18, not(THEM(THEM)):0.81, or(THEM(ME),C):0.01}   via not(THEM(THEM)) (1.35e-05, rho=1.95e-02 k*=81)
    - 1.35e-05 -> poly {D:0.18, not(THEM(ME)):0.81, or(THEM(ME),C):0.01}   via not(THEM(ME)) (1.35e-05, rho=1.95e-02 k*=81)
    - 6.09e-06 -> mono {THEM(^C):1}   via THEM(^C) (6.09e-06, rho=7.98e-03 k*=100)
    - 5.45e-06 -> poly {C:0.65, D:0.19, not(THEM(^D)):0.15, or(THEM(ME),C):0.01}   via not(THEM(^D)) (5.45e-06, rho=7.15e-02 k*=15)
- poly {C:0.64, D:0.01, X:0.28, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 3.34e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.34e-05, rho=9.10e-03 k*=100)
    - 3.34e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.34e-05, rho=9.10e-03 k*=100)
    - 1.19e-05 -> poly {D:0.18, not(THEM(THEM)):0.81, or(THEM(ME),C):0.01}   via not(THEM(THEM)) (1.19e-05, rho=1.73e-02 k*=81)
    - 1.19e-05 -> poly {D:0.18, not(THEM(ME)):0.81, or(THEM(ME),C):0.01}   via not(THEM(ME)) (1.19e-05, rho=1.73e-02 k*=81)
    - 6.94e-06 -> mono {THEM(^C):1}   via THEM(^C) (6.94e-06, rho=9.10e-03 k*=100)
    - 5.20e-06 -> poly {C:0.65, D:0.19, not(THEM(^D)):0.15, or(THEM(ME),C):0.01}   via not(THEM(^D)) (5.20e-06, rho=6.83e-02 k*=15)
- poly {C:0.8, D:0.17, X:0.01, and(X,X):0.01, or(X,X):0.01}
    - 1.52e-04 -> poly {C:0.79, D:0.17, X:0.01, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.79, D:0.17, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.8, D:0.16, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.8, D:0.16, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.8, D:0.16, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 2.90e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.90e-05, rho=7.87e-03 k*=100)
- poly {C:0.63, D:0.01, X:0.29, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 3.34e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.34e-05, rho=9.11e-03 k*=100)
    - 3.34e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.34e-05, rho=9.11e-03 k*=100)
    - 1.18e-05 -> poly {D:0.18, not(THEM(THEM)):0.81, or(THEM(ME),C):0.01}   via not(THEM(THEM)) (1.18e-05, rho=1.72e-02 k*=81)
    - 1.18e-05 -> poly {D:0.18, not(THEM(ME)):0.81, or(THEM(ME),C):0.01}   via not(THEM(ME)) (1.18e-05, rho=1.72e-02 k*=81)
    - 6.94e-06 -> mono {THEM(^C):1}   via THEM(^C) (6.94e-06, rho=9.11e-03 k*=100)
    - 5.19e-06 -> poly {C:0.65, D:0.19, not(THEM(^D)):0.15, or(THEM(ME),C):0.01}   via not(THEM(^D)) (5.19e-06, rho=6.82e-02 k*=15)
- poly {C:0.64, D:0.01, X:0.33, and(X,X):0.01, or(X,X):0.01}
    - 1.52e-04 -> poly {C:0.64, D:0.01, X:0.32, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.64, D:0.01, X:0.32, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.65, D:0.01, X:0.31, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.64, D:0.01, X:0.32, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.65, D:0.01, X:0.31, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.37e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.37e-05, rho=9.16e-03 k*=100)
- poly {C:0.65, D:0.01, X:0.32, and(X,X):0.01, or(X,X):0.01}
    - 1.52e-04 -> poly {C:0.64, D:0.01, X:0.32, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.64, D:0.01, X:0.32, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.65, D:0.01, X:0.31, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.64, D:0.01, X:0.32, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.65, D:0.01, X:0.31, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.37e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.37e-05, rho=9.15e-03 k*=100)
- poly {C:0.64, D:0.01, X:0.29, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.64, D:0.01, X:0.28, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.35e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.35e-05, rho=9.10e-03 k*=100)
    - 3.35e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.35e-05, rho=9.10e-03 k*=100)
    - 1.18e-05 -> poly {D:0.18, not(THEM(THEM)):0.81, or(THEM(ME),C):0.01}   via not(THEM(THEM)) (1.18e-05, rho=1.72e-02 k*=81)
    - 1.18e-05 -> poly {D:0.18, not(THEM(ME)):0.81, or(THEM(ME),C):0.01}   via not(THEM(ME)) (1.18e-05, rho=1.72e-02 k*=81)
    - 6.96e-06 -> mono {THEM(^C):1}   via THEM(^C) (6.96e-06, rho=9.10e-03 k*=100)
- poly {C:0.64, D:0.01, X:0.29, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.64, D:0.01, X:0.28, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.34e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.34e-05, rho=9.09e-03 k*=100)
    - 3.34e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.34e-05, rho=9.09e-03 k*=100)
    - 1.19e-05 -> poly {D:0.18, not(THEM(THEM)):0.81, or(THEM(ME),C):0.01}   via not(THEM(THEM)) (1.19e-05, rho=1.73e-02 k*=81)
    - 1.19e-05 -> poly {D:0.18, not(THEM(ME)):0.81, or(THEM(ME),C):0.01}   via not(THEM(ME)) (1.19e-05, rho=1.73e-02 k*=81)
    - 6.93e-06 -> mono {THEM(^C):1}   via THEM(^C) (6.93e-06, rho=9.09e-03 k*=100)
- poly {C:0.63, D:0.01, X:0.3, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.63, D:0.01, X:0.29, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.35e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.35e-05, rho=9.12e-03 k*=100)
    - 3.35e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.35e-05, rho=9.12e-03 k*=100)
    - 1.18e-05 -> poly {D:0.18, not(THEM(THEM)):0.81, or(THEM(ME),C):0.01}   via not(THEM(THEM)) (1.18e-05, rho=1.72e-02 k*=81)
    - 1.18e-05 -> poly {D:0.18, not(THEM(ME)):0.81, or(THEM(ME),C):0.01}   via not(THEM(ME)) (1.18e-05, rho=1.72e-02 k*=81)
    - 6.95e-06 -> mono {THEM(^C):1}   via THEM(^C) (6.95e-06, rho=9.12e-03 k*=100)
- poly {C:0.63, D:0.01, X:0.3, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.63, D:0.01, X:0.29, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.36e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.36e-05, rho=9.16e-03 k*=100)
    - 3.36e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.36e-05, rho=9.16e-03 k*=100)
    - 1.18e-05 -> poly {D:0.18, not(THEM(THEM)):0.81, or(THEM(ME),C):0.01}   via not(THEM(THEM)) (1.18e-05, rho=1.71e-02 k*=81)
    - 1.18e-05 -> poly {D:0.18, not(THEM(ME)):0.81, or(THEM(ME),C):0.01}   via not(THEM(ME)) (1.18e-05, rho=1.71e-02 k*=81)
    - 6.98e-06 -> mono {THEM(^C):1}   via THEM(^C) (6.98e-06, rho=9.16e-03 k*=100)
- poly {C:0.77, D:0.16, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.77, D:0.15, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 2.92e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.92e-05, rho=7.96e-03 k*=100)
    - 2.92e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.92e-05, rho=7.96e-03 k*=100)
    - 1.35e-05 -> poly {D:0.18, not(THEM(THEM)):0.81, or(THEM(ME),C):0.01}   via not(THEM(THEM)) (1.35e-05, rho=1.96e-02 k*=81)
    - 1.35e-05 -> poly {D:0.18, not(THEM(ME)):0.81, or(THEM(ME),C):0.01}   via not(THEM(ME)) (1.35e-05, rho=1.96e-02 k*=81)
    - 6.07e-06 -> mono {THEM(^C):1}   via THEM(^C) (6.07e-06, rho=7.96e-03 k*=100)
- poly {C:0.78, D:0.15, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.77, D:0.15, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 2.92e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.92e-05, rho=7.97e-03 k*=100)
    - 2.92e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.92e-05, rho=7.97e-03 k*=100)
    - 1.35e-05 -> poly {D:0.18, not(THEM(THEM)):0.81, or(THEM(ME),C):0.01}   via not(THEM(THEM)) (1.35e-05, rho=1.96e-02 k*=81)
    - 1.35e-05 -> poly {D:0.18, not(THEM(ME)):0.81, or(THEM(ME),C):0.01}   via not(THEM(ME)) (1.35e-05, rho=1.96e-02 k*=81)
    - 6.07e-06 -> mono {THEM(^C):1}   via THEM(^C) (6.07e-06, rho=7.97e-03 k*=100)
