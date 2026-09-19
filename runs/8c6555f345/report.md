### arm=weak, n=5, game=chicken_norole, N=10, w=0.01, x_on=True, role=False, mode=square

programs 450, classes 30, states 517, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 1.66e-02
mean payoff -0.1866, efficient 0.5000, deadweight loss 0.6866, mean bits in support 4.21

| pi | state |
|---|---|
| 0.4438 | poly {C:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1} |
| 0.1048 | poly {C:0.7, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1} |
| 0.0619 | poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1} |
| 0.0601 | poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1} |
| 0.0474 | poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),C):0.1} |
| 0.0359 | poly {C:0.7, D:0.1, X:0.1, and(X,X):0.1} |
| 0.0277 | poly {C:0.7, D:0.1, X:0.1, or(X,X):0.1} |
| 0.0233 | poly {C:0.8, D:0.1, X:0.1} |
| 0.0232 | poly {C:0.7, D:0.1, X:0.2} |
| 0.0195 | poly {C:0.6, D:0.1, X:0.2, or(X,X):0.1} |
| 0.0137 | poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),C):0.1} |
| 0.0135 | poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(THEM(ME),C):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {C:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}
    - 8.13e-03 -> poly {C:0.6, X:0.2, and(X,X):0.1, or(X,X):0.1}   via THEM(ME) (3.68e-03, rho=1.00e+00 k*=1), THEM(THEM) (3.68e-03, rho=1.00e+00 k*=1), THEM(^C) (7.65e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.7, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.7, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1}
    - 9.20e-03 -> poly {C:0.6, X:0.2, or(X,X):0.1, and(X,or(X,X)):0.1}   via THEM(ME) (3.68e-03, rho=1.00e+00 k*=1), THEM(THEM) (3.68e-03, rho=1.00e+00 k*=1), THEM(^C) (7.65e-04, rho=1.00e+00 k*=1), THEM(^X) (7.65e-04, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 9.17e-04 -> poly {C:0.6, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.2}   via THEM(^D) (7.65e-04, rho=1.00e+00 k*=1), and(X,THEM(ME)) (7.61e-05, rho=1.00e+00 k*=1), and(X,THEM(THEM)) (7.61e-05, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.2, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, X:0.1, or(X,X):0.1, or(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}
    - 3.64e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.64e-04, rho=9.92e-02 k*=10)
    - 3.64e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.64e-04, rho=9.92e-02 k*=10)
    - 1.52e-04 -> poly {C:0.6, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1}
    - 3.66e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.66e-04, rho=9.93e-02 k*=10)
    - 3.66e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.66e-04, rho=9.93e-02 k*=10)
    - 1.52e-04 -> poly {C:0.6, X:0.1, or(X,X):0.1, or(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),C):0.1}
    - 3.65e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.65e-04, rho=9.92e-02 k*=10)
    - 3.65e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.65e-04, rho=9.92e-02 k*=10)
    - 1.52e-04 -> poly {C:0.6, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(THEM(ME),C):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(THEM(ME),C):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.7, D:0.1, X:0.1, and(X,X):0.1}
    - 6.74e-03 -> poly {C:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 7.97e-04 -> mono {C:1}   via THEM(ME) (3.61e-04, rho=1.96e-01 k*=5), THEM(THEM) (3.61e-04, rho=1.96e-01 k*=5), THEM(^C) (7.50e-05, rho=1.96e-01 k*=5)
    - 3.62e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.62e-04, rho=1.96e-01 k*=5)
    - 3.62e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.62e-04, rho=1.96e-01 k*=5)
    - 1.52e-04 -> poly {C:0.8, X:0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.7, X:0.1, and(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.7, D:0.1, X:0.1, or(X,X):0.1}
    - 6.74e-03 -> poly {C:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.63e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.63e-04, rho=9.87e-02 k*=10)
    - 3.63e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.63e-04, rho=9.87e-02 k*=10)
    - 1.52e-04 -> poly {C:0.7, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.7, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, D:0.1, X:0.1, or(X,X):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.8, D:0.1, X:0.1}
    - 6.74e-03 -> poly {C:0.7, D:0.1, X:0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {C:0.7, D:0.1, X:0.1, and(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 8.10e-04 -> mono {C:1}   via THEM(ME) (3.67e-04, rho=1.97e-01 k*=5), THEM(THEM) (3.67e-04, rho=1.97e-01 k*=5), THEM(^C) (7.62e-05, rho=1.97e-01 k*=5)
    - 3.58e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.58e-04, rho=1.97e-01 k*=5)
    - 3.58e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.58e-04, rho=1.97e-01 k*=5)
    - 1.52e-04 -> poly {C:0.7, D:0.1, X:0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.7, D:0.1, X:0.2}
    - 6.74e-03 -> poly {C:0.6, D:0.1, X:0.2, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {C:0.7, D:0.1, X:0.1, and(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 8.05e-04 -> mono {C:1}   via THEM(ME) (3.65e-04, rho=1.97e-01 k*=5), THEM(THEM) (3.65e-04, rho=1.97e-01 k*=5), THEM(^C) (7.58e-05, rho=1.97e-01 k*=5)
    - 3.60e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.60e-04, rho=1.97e-01 k*=5)
    - 3.60e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.60e-04, rho=1.97e-01 k*=5)
    - 1.52e-04 -> poly {C:0.6, D:0.1, X:0.2, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.6, D:0.1, X:0.2, or(X,X):0.1}
    - 6.74e-03 -> poly {C:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.64e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.64e-04, rho=9.89e-02 k*=10)
    - 3.64e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.64e-04, rho=9.89e-02 k*=10)
    - 1.52e-04 -> poly {C:0.7, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.7, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, D:0.1, X:0.2, or(X,X):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),C):0.1}
    - 3.64e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.64e-04, rho=9.92e-02 k*=10)
    - 3.64e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.64e-04, rho=9.92e-02 k*=10)
    - 1.52e-04 -> poly {C:0.5, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 7.61e-05 -> poly {C:0.6, and(X,X):0.2, not(THEM(^D)):0.1, or(THEM(ME),C):0.1}   via not(THEM(^D)) (7.61e-05, rho=1.00e+00 k*=1)
- poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(THEM(ME),C):0.1}
    - 3.66e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.66e-04, rho=9.93e-02 k*=10)
    - 3.66e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.66e-04, rho=9.93e-02 k*=10)
    - 1.52e-04 -> poly {C:0.5, X:0.1, or(X,X):0.1, or(X,and(X,X)):0.1, and(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,and(X,X)):0.1, or(THEM(ME),C):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 7.61e-05 -> poly {C:0.6, and(X,X):0.2, not(THEM(^D)):0.1, or(THEM(ME),C):0.1}   via not(THEM(^D)) (7.61e-05, rho=1.00e+00 k*=1)
