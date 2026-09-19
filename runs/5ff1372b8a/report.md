### arm=weak, n=5, game=demand_norole, N=100, w=0.01, x_on=True, role=False, mode=square

programs 450, classes 30, states 756, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 9.88e-04
mean payoff 0.3972, efficient 0.5000, deadweight loss 0.1028, mean bits in support 3.19

| pi | state |
|---|---|
| 0.1020 | poly {C:0.33, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0974 | poly {C:0.62, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0670 | poly {C:0.34, D:0.01, X:0.63, and(X,X):0.01, or(X,X):0.01} |
| 0.0631 | poly {C:0.65, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01} |
| 0.0172 | poly {C:0.34, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0171 | poly {C:0.33, D:0.01, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0166 | poly {C:0.34, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01} |
| 0.0163 | poly {C:0.33, D:0.01, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0160 | poly {C:0.63, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0160 | poly {C:0.62, D:0.31, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0158 | poly {C:0.63, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0158 | poly {C:0.63, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {C:0.33, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 3.66e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.66e-05, rho=9.94e-03 k*=100)
    - 3.66e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.66e-05, rho=9.94e-03 k*=100)
    - 1.06e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.06e-05, rho=1.53e-02 k*=66)
    - 1.06e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.06e-05, rho=1.53e-02 k*=66)
    - 7.60e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.60e-06, rho=9.94e-03 k*=100)
    - 7.54e-06 -> mono {THEM(^X):1}   via THEM(^X) (7.54e-06, rho=9.86e-03 k*=100)
- poly {C:0.62, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 3.61e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.61e-05, rho=9.80e-03 k*=100)
    - 3.61e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.61e-05, rho=9.80e-03 k*=100)
    - 1.07e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.07e-05, rho=1.56e-02 k*=66)
    - 1.07e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.07e-05, rho=1.56e-02 k*=66)
    - 7.49e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.49e-06, rho=9.80e-03 k*=100)
    - 7.43e-06 -> mono {THEM(^X):1}   via THEM(^X) (7.43e-06, rho=9.72e-03 k*=100)
- poly {C:0.34, D:0.01, X:0.63, and(X,X):0.01, or(X,X):0.01}
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.35, D:0.01, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.66e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.66e-05, rho=9.94e-03 k*=100)
- poly {C:0.65, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01}
    - 1.52e-04 -> poly {C:0.64, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.64, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.65, D:0.31, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.64, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.65, D:0.31, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.60e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.60e-05, rho=9.79e-03 k*=100)
- poly {C:0.34, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.58, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.66e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.66e-05, rho=9.94e-03 k*=100)
    - 3.66e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.66e-05, rho=9.94e-03 k*=100)
    - 1.06e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.06e-05, rho=1.53e-02 k*=66)
    - 1.06e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.06e-05, rho=1.53e-02 k*=66)
    - 7.60e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.60e-06, rho=9.94e-03 k*=100)
- poly {C:0.33, D:0.01, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.33, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.66e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.66e-05, rho=9.94e-03 k*=100)
    - 3.66e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.66e-05, rho=9.94e-03 k*=100)
    - 1.06e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.06e-05, rho=1.53e-02 k*=66)
    - 1.06e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.06e-05, rho=1.53e-02 k*=66)
    - 7.60e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.60e-06, rho=9.94e-03 k*=100)
- poly {C:0.34, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01}
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.58, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.66e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.66e-05, rho=9.94e-03 k*=100)
    - 3.66e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.66e-05, rho=9.94e-03 k*=100)
    - 1.04e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.04e-05, rho=1.51e-02 k*=67)
    - 1.04e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.04e-05, rho=1.51e-02 k*=67)
    - 7.60e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.60e-06, rho=9.94e-03 k*=100)
- poly {C:0.33, D:0.01, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.33, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.66e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.66e-05, rho=9.94e-03 k*=100)
    - 3.66e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.66e-05, rho=9.94e-03 k*=100)
    - 1.04e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.04e-05, rho=1.51e-02 k*=67)
    - 1.04e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.04e-05, rho=1.51e-02 k*=67)
    - 7.60e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.60e-06, rho=9.94e-03 k*=100)
- poly {C:0.63, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.62, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.61e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.61e-05, rho=9.80e-03 k*=100)
    - 3.61e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.61e-05, rho=9.80e-03 k*=100)
    - 1.07e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.07e-05, rho=1.56e-02 k*=66)
    - 1.07e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.07e-05, rho=1.56e-02 k*=66)
    - 7.49e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.49e-06, rho=9.80e-03 k*=100)
- poly {C:0.62, D:0.31, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.62, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.61e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.61e-05, rho=9.80e-03 k*=100)
    - 3.61e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.61e-05, rho=9.80e-03 k*=100)
    - 1.07e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.07e-05, rho=1.56e-02 k*=66)
    - 1.07e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.07e-05, rho=1.56e-02 k*=66)
    - 7.49e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.49e-06, rho=9.80e-03 k*=100)
- poly {C:0.63, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.62, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.61e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.61e-05, rho=9.80e-03 k*=100)
    - 3.61e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.61e-05, rho=9.80e-03 k*=100)
    - 1.07e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.07e-05, rho=1.56e-02 k*=66)
    - 1.07e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.07e-05, rho=1.56e-02 k*=66)
    - 7.49e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.49e-06, rho=9.80e-03 k*=100)
- poly {C:0.63, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.62, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.61e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.61e-05, rho=9.80e-03 k*=100)
    - 3.61e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.61e-05, rho=9.80e-03 k*=100)
    - 1.06e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.06e-05, rho=1.53e-02 k*=67)
    - 1.06e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.06e-05, rho=1.53e-02 k*=67)
    - 7.49e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.49e-06, rho=9.80e-03 k*=100)
