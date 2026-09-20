### arm=weak, n=5, game=demand_norole, N=100, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 450, classes 30, states 792, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 8.21e-04
mean payoff 0.4000, efficient 0.5000, deadweight loss 0.1000, mean bits in support 5.64

| pi | state |
|---|---|
| 0.1628 | poly {High:0.33, not(THEM(ME)):0.01, not(THEM(THEM)):0.66} |
| 0.1327 | poly {High:0.33, not(THEM(ME)):0.66, not(THEM(THEM)):0.01} |
| 0.1075 | poly {High:0.01, Low:0.33, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01} |
| 0.0541 | poly {High:0.01, Low:0.34, X:0.63, and(X,X):0.01, or(X,X):0.01} |
| 0.0256 | poly {High:0.33, not(THEM(THEM)):0.67} |
| 0.0249 | poly {High:0.33, not(THEM(ME)):0.67} |
| 0.0180 | poly {High:0.32, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01} |
| 0.0168 | mono {and(THEM(THEM),High):1} |
| 0.0167 | mono {and(THEM(ME),High):1} |
| 0.0159 | poly {High:0.01, Low:0.34, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(THEM(ME),Low):0.01} |
| 0.0159 | poly {High:0.01, Low:0.33, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01} |
| 0.0153 | poly {High:0.01, Low:0.34, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {High:0.33, not(THEM(ME)):0.01, not(THEM(THEM)):0.66}
    - 1.52e-04 -> poly {High:0.33, not(THEM(ME)):0.01, not(THEM(THEM)):0.65, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 8.93e-05 -> mono {X:1}   via X (8.93e-05, rho=2.83e-04 k*=100)
    - 8.10e-06 -> poly {High:0.33, not(THEM(ME)):0.01, not(THEM(THEM)):0.44, not(THEM(^High)):0.22}   via not(THEM(^High)) (8.10e-06, rho=1.06e-01 k*=22)
    - 2.85e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (2.85e-06, rho=7.75e-04 k*=100)
    - 2.85e-06 -> mono {THEM(ME):1}   via THEM(ME) (2.85e-06, rho=7.75e-04 k*=100)
    - 2.50e-06 -> mono {Low:1}   via Low (2.50e-06, rho=7.59e-06 k*=100)
- poly {High:0.33, not(THEM(ME)):0.66, not(THEM(THEM)):0.01}
    - 1.52e-04 -> poly {High:0.33, not(THEM(ME)):0.65, not(THEM(THEM)):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 8.93e-05 -> mono {X:1}   via X (8.93e-05, rho=2.83e-04 k*=100)
    - 2.08e-05 -> mono {THEM(^Low):1}   via THEM(^Low) (2.08e-05, rho=2.72e-02 k*=100)
    - 8.10e-06 -> poly {High:0.33, not(THEM(ME)):0.44, not(THEM(THEM)):0.01, not(THEM(^High)):0.22}   via not(THEM(^High)) (8.10e-06, rho=1.06e-01 k*=22)
    - 2.85e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (2.85e-06, rho=7.75e-04 k*=100)
    - 2.85e-06 -> mono {THEM(ME):1}   via THEM(ME) (2.85e-06, rho=7.75e-04 k*=100)
- poly {High:0.01, Low:0.33, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}
    - 2.65e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (2.65e-05, rho=3.84e-02 k*=66)
    - 2.65e-05 -> poly {High:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (2.65e-05, rho=3.84e-02 k*=66)
    - 1.89e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (1.89e-05, rho=5.13e-03 k*=100)
    - 1.89e-05 -> mono {THEM(ME):1}   via THEM(ME) (1.89e-05, rho=5.13e-03 k*=100)
    - 3.92e-06 -> mono {THEM(^Low):1}   via THEM(^Low) (3.92e-06, rho=5.13e-03 k*=100)
    - 3.88e-06 -> poly {High:0.34, Low:0.43, not(THEM(^High)):0.22, or(THEM(ME),Low):0.01}   via not(THEM(^High)) (3.88e-06, rho=5.09e-02 k*=22)
- poly {High:0.01, Low:0.34, X:0.63, and(X,X):0.01, or(X,X):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.35, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 2.66e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (2.66e-05, rho=3.86e-02 k*=67)
- poly {High:0.33, not(THEM(THEM)):0.67}
    - 6.89e-04 -> poly {High:0.33, not(THEM(ME)):0.01, not(THEM(THEM)):0.66}   via not(THEM(ME)) (6.89e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.33, not(THEM(THEM)):0.66, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 8.93e-05 -> mono {X:1}   via X (8.93e-05, rho=2.83e-04 k*=100)
    - 8.10e-06 -> poly {High:0.33, not(THEM(THEM)):0.45, not(THEM(^High)):0.22}   via not(THEM(^High)) (8.10e-06, rho=1.06e-01 k*=22)
    - 2.85e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (2.85e-06, rho=7.75e-04 k*=100)
    - 2.85e-06 -> mono {THEM(ME):1}   via THEM(ME) (2.85e-06, rho=7.75e-04 k*=100)
- poly {High:0.33, not(THEM(ME)):0.67}
    - 6.89e-04 -> poly {High:0.33, not(THEM(ME)):0.66, not(THEM(THEM)):0.01}   via not(THEM(THEM)) (6.89e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.33, not(THEM(ME)):0.66, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 8.93e-05 -> mono {X:1}   via X (8.93e-05, rho=2.83e-04 k*=100)
    - 2.28e-05 -> mono {THEM(^Low):1}   via THEM(^Low) (2.28e-05, rho=2.98e-02 k*=100)
    - 8.10e-06 -> poly {High:0.33, not(THEM(ME)):0.45, not(THEM(^High)):0.22}   via not(THEM(^High)) (8.10e-06, rho=1.06e-01 k*=22)
    - 2.85e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (2.85e-06, rho=7.75e-04 k*=100)
- poly {High:0.32, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01}
    - 1.52e-04 -> poly {High:0.32, Low:0.64, X:0.01, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.32, Low:0.64, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.31, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.32, Low:0.64, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.31, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 7.14e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (7.14e-05, rho=1.04e-01 k*=67)
- mono {and(THEM(THEM),High):1}
    - 3.68e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.68e-05, rho=1.00e-02 k*=100)
    - 3.68e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-05, rho=1.00e-02 k*=100)
    - 6.89e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (6.89e-06, rho=1.00e-02 k*=100)
    - 6.89e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (6.89e-06, rho=1.00e-02 k*=100)
    - 2.66e-06 -> mono {X:1}   via X (2.66e-06, rho=8.45e-06 k*=100)
    - 2.58e-06 -> mono {Low:1}   via Low (2.58e-06, rho=7.84e-06 k*=100)
- mono {and(THEM(ME),High):1}
    - 3.68e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.68e-05, rho=1.00e-02 k*=100)
    - 3.68e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-05, rho=1.00e-02 k*=100)
    - 6.89e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (6.89e-06, rho=1.00e-02 k*=100)
    - 6.89e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (6.89e-06, rho=1.00e-02 k*=100)
    - 2.66e-06 -> mono {X:1}   via X (2.66e-06, rho=8.45e-06 k*=100)
    - 2.58e-06 -> mono {Low:1}   via Low (2.58e-06, rho=7.84e-06 k*=100)
- poly {High:0.01, Low:0.34, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.58, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 2.66e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (2.66e-05, rho=3.86e-02 k*=67)
    - 2.66e-05 -> poly {High:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (2.66e-05, rho=3.86e-02 k*=67)
    - 1.87e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (1.87e-05, rho=5.07e-03 k*=100)
    - 1.87e-05 -> mono {THEM(ME):1}   via THEM(ME) (1.87e-05, rho=5.07e-03 k*=100)
    - 3.90e-06 -> poly {High:0.34, Low:0.43, not(THEM(^High)):0.22, or(THEM(ME),Low):0.01}   via not(THEM(^High)) (3.90e-06, rho=5.12e-02 k*=22)
- poly {High:0.01, Low:0.33, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.33, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 2.63e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (2.63e-05, rho=3.82e-02 k*=67)
    - 2.63e-05 -> poly {High:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (2.63e-05, rho=3.82e-02 k*=67)
    - 1.89e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (1.89e-05, rho=5.13e-03 k*=100)
    - 1.89e-05 -> mono {THEM(ME):1}   via THEM(ME) (1.89e-05, rho=5.13e-03 k*=100)
    - 3.93e-06 -> mono {THEM(^Low):1}   via THEM(^Low) (3.93e-06, rho=5.13e-03 k*=100)
- poly {High:0.01, Low:0.34, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.58, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 2.73e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (2.73e-05, rho=3.96e-02 k*=67)
    - 2.73e-05 -> poly {High:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (2.73e-05, rho=3.96e-02 k*=67)
    - 1.89e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (1.89e-05, rho=5.13e-03 k*=100)
    - 1.89e-05 -> mono {THEM(ME):1}   via THEM(ME) (1.89e-05, rho=5.13e-03 k*=100)
    - 3.92e-06 -> mono {THEM(^Low):1}   via THEM(^Low) (3.92e-06, rho=5.13e-03 k*=100)
