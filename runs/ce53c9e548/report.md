### arm=weak, n=5, game=demand_norole, N=100, w=1.0, x_on=True, role=False, mode=square

programs 450, classes 30, states 913, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 9.02e-04
mean payoff 0.3998, efficient 0.5000, deadweight loss 0.1002, mean bits in support 4.38

| pi | state |
|---|---|
| 0.1359 | poly {C:0.33, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0695 | poly {C:0.34, D:0.01, X:0.63, and(X,X):0.01, or(X,X):0.01} |
| 0.0510 | poly {D:0.33, not(THEM(ME)):0.01, not(THEM(THEM)):0.66} |
| 0.0472 | poly {D:0.33, not(THEM(ME)):0.66, not(THEM(THEM)):0.01} |
| 0.0422 | poly {C:0.62, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0284 | poly {C:0.65, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01} |
| 0.0235 | poly {D:0.33, not(THEM(THEM)):0.67} |
| 0.0230 | poly {D:0.33, not(THEM(ME)):0.67} |
| 0.0205 | poly {C:0.34, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0204 | poly {C:0.33, D:0.01, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |
| 0.0203 | poly {C:0.34, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01} |
| 0.0193 | poly {C:0.33, D:0.01, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {C:0.33, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 2.29e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.29e-05, rho=6.21e-03 k*=100)
    - 2.29e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.29e-05, rho=6.21e-03 k*=100)
    - 2.10e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (2.10e-05, rho=3.05e-02 k*=66)
    - 2.10e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (2.10e-05, rho=3.05e-02 k*=66)
    - 4.75e-06 -> mono {THEM(^C):1}   via THEM(^C) (4.75e-06, rho=6.21e-03 k*=100)
    - 3.75e-06 -> poly {C:0.43, D:0.34, not(THEM(^D)):0.22, or(THEM(ME),C):0.01}   via not(THEM(^D)) (3.75e-06, rho=4.92e-02 k*=22)
- poly {C:0.34, D:0.01, X:0.63, and(X,X):0.01, or(X,X):0.01}
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.35, D:0.01, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 2.34e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.34e-05, rho=6.36e-03 k*=100)
- poly {D:0.33, not(THEM(ME)):0.01, not(THEM(THEM)):0.66}
    - 2.40e-04 -> mono {X:1}   via X (2.40e-04, rho=7.63e-04 k*=100)
    - 1.52e-04 -> poly {D:0.33, not(THEM(ME)):0.01, not(THEM(THEM)):0.65, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 4.03e-05 -> mono {C:1}   via C (4.03e-05, rho=1.22e-04 k*=100)
    - 1.59e-05 -> mono {not(THEM(THEM)):1}   via THEM(ME) (7.64e-06, rho=3.81e-03 k*=45), THEM(THEM) (7.64e-06, rho=3.81e-03 k*=45), and(THEM(ME),D) (1.58e-07, rho=3.81e-03 k*=45), and(THEM(ME),X) (1.58e-07, rho=3.81e-03 k*=45)
    - 6.37e-06 -> poly {D:0.33, not(THEM(ME)):0.01, not(THEM(THEM)):0.44, not(THEM(^D)):0.22}   via not(THEM(^D)) (6.37e-06, rho=8.37e-02 k*=22)
    - 6.27e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (6.27e-06, rho=3.81e-03 k*=45)
- poly {D:0.33, not(THEM(ME)):0.66, not(THEM(THEM)):0.01}
    - 2.40e-04 -> mono {X:1}   via X (2.40e-04, rho=7.63e-04 k*=100)
    - 1.52e-04 -> poly {D:0.33, not(THEM(ME)):0.65, not(THEM(THEM)):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 4.03e-05 -> mono {C:1}   via C (4.03e-05, rho=1.22e-04 k*=100)
    - 1.80e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.80e-05, rho=2.36e-02 k*=100)
    - 1.59e-05 -> mono {not(THEM(ME)):1}   via THEM(ME) (7.64e-06, rho=3.81e-03 k*=45), THEM(THEM) (7.64e-06, rho=3.81e-03 k*=45), and(THEM(ME),D) (1.58e-07, rho=3.81e-03 k*=45), and(THEM(ME),X) (1.58e-07, rho=3.81e-03 k*=45)
    - 6.37e-06 -> poly {D:0.33, not(THEM(ME)):0.44, not(THEM(THEM)):0.01, not(THEM(^D)):0.22}   via not(THEM(^D)) (6.37e-06, rho=8.37e-02 k*=22)
- poly {C:0.62, D:0.3, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 4.49e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (4.49e-05, rho=6.52e-02 k*=66)
    - 4.49e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (4.49e-05, rho=6.52e-02 k*=66)
    - 6.44e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (6.44e-06, rho=1.75e-03 k*=100)
    - 6.44e-06 -> mono {THEM(ME):1}   via THEM(ME) (6.44e-06, rho=1.75e-03 k*=100)
    - 6.13e-06 -> poly {C:0.44, D:0.33, not(THEM(^D)):0.22, or(THEM(ME),C):0.01}   via not(THEM(^D)) (6.13e-06, rho=8.05e-02 k*=22)
    - 5.03e-06 -> poly {D:0.33, not(THEM(^C)):0.67}   via not(THEM(^C)) (5.03e-06, rho=6.61e-02 k*=67)
- poly {C:0.65, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01}
    - 1.52e-04 -> poly {C:0.64, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.64, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.65, D:0.31, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.64, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.65, D:0.31, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 4.69e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (4.69e-05, rho=6.81e-02 k*=67)
- poly {D:0.33, not(THEM(THEM)):0.67}
    - 6.89e-04 -> poly {D:0.33, not(THEM(ME)):0.01, not(THEM(THEM)):0.66}   via not(THEM(ME)) (6.89e-04, rho=1.00e+00 k*=1)
    - 2.40e-04 -> mono {X:1}   via X (2.40e-04, rho=7.63e-04 k*=100)
    - 1.52e-04 -> poly {D:0.33, not(THEM(THEM)):0.66, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 4.03e-05 -> mono {C:1}   via C (4.03e-05, rho=1.22e-04 k*=100)
    - 1.62e-05 -> mono {not(THEM(THEM)):1}   via THEM(ME) (7.76e-06, rho=3.81e-03 k*=45), THEM(THEM) (7.76e-06, rho=3.81e-03 k*=45), and(THEM(ME),D) (1.60e-07, rho=3.81e-03 k*=45), and(THEM(ME),X) (1.60e-07, rho=3.81e-03 k*=45)
    - 6.37e-06 -> poly {D:0.33, not(THEM(THEM)):0.45, not(THEM(^D)):0.22}   via not(THEM(^D)) (6.37e-06, rho=8.37e-02 k*=22)
- poly {D:0.33, not(THEM(ME)):0.67}
    - 6.89e-04 -> poly {D:0.33, not(THEM(ME)):0.66, not(THEM(THEM)):0.01}   via not(THEM(THEM)) (6.89e-04, rho=1.00e+00 k*=1)
    - 2.40e-04 -> mono {X:1}   via X (2.40e-04, rho=7.63e-04 k*=100)
    - 1.52e-04 -> poly {D:0.33, not(THEM(ME)):0.66, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 4.03e-05 -> mono {C:1}   via C (4.03e-05, rho=1.22e-04 k*=100)
    - 1.94e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.94e-05, rho=2.53e-02 k*=100)
    - 1.62e-05 -> mono {not(THEM(ME)):1}   via THEM(ME) (7.76e-06, rho=3.81e-03 k*=45), THEM(THEM) (7.76e-06, rho=3.81e-03 k*=45), and(THEM(ME),D) (1.60e-07, rho=3.81e-03 k*=45), and(THEM(ME),X) (1.60e-07, rho=3.81e-03 k*=45)
- poly {C:0.34, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.58, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 2.27e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.27e-05, rho=6.16e-03 k*=100)
    - 2.27e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.27e-05, rho=6.16e-03 k*=100)
    - 2.12e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (2.12e-05, rho=3.07e-02 k*=66)
    - 2.12e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (2.12e-05, rho=3.07e-02 k*=66)
    - 4.71e-06 -> mono {THEM(^C):1}   via THEM(^C) (4.71e-06, rho=6.16e-03 k*=100)
- poly {C:0.33, D:0.01, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.33, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 2.29e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.29e-05, rho=6.21e-03 k*=100)
    - 2.29e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.29e-05, rho=6.21e-03 k*=100)
    - 2.10e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (2.10e-05, rho=3.04e-02 k*=66)
    - 2.10e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (2.10e-05, rho=3.04e-02 k*=66)
    - 4.75e-06 -> mono {THEM(^C):1}   via THEM(^C) (4.75e-06, rho=6.21e-03 k*=100)
- poly {C:0.34, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01}
    - 1.52e-04 -> poly {C:0.34, D:0.01, X:0.58, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 2.29e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.29e-05, rho=6.21e-03 k*=100)
    - 2.29e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.29e-05, rho=6.21e-03 k*=100)
    - 2.14e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (2.14e-05, rho=3.11e-02 k*=67)
    - 2.14e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (2.14e-05, rho=3.11e-02 k*=67)
    - 4.75e-06 -> mono {THEM(^C):1}   via THEM(^C) (4.75e-06, rho=6.21e-03 k*=100)
- poly {C:0.33, D:0.01, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}
    - 1.52e-04 -> poly {C:0.33, D:0.01, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),C):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 2.29e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.29e-05, rho=6.22e-03 k*=100)
    - 2.29e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.29e-05, rho=6.22e-03 k*=100)
    - 2.09e-05 -> poly {D:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (2.09e-05, rho=3.03e-02 k*=67)
    - 2.09e-05 -> poly {D:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (2.09e-05, rho=3.03e-02 k*=67)
    - 4.76e-06 -> mono {THEM(^C):1}   via THEM(^C) (4.76e-06, rho=6.22e-03 k*=100)
