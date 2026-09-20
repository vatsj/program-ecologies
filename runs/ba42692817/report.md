### arm=weak, n=5, game=demand_norole, N=100, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 450, classes 30, states 737, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 9.41e-04
mean payoff 0.3996, efficient 0.5000, deadweight loss 0.1004, mean bits in support 3.34

| pi | state |
|---|---|
| 0.1355 | poly {High:0.01, Low:0.33, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01} |
| 0.0945 | poly {High:0.3, Low:0.62, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01} |
| 0.0721 | poly {High:0.01, Low:0.34, X:0.63, and(X,X):0.01, or(X,X):0.01} |
| 0.0424 | poly {High:0.32, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01} |
| 0.0208 | poly {High:0.01, Low:0.34, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(THEM(ME),Low):0.01} |
| 0.0208 | poly {High:0.01, Low:0.33, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01} |
| 0.0205 | poly {High:0.01, Low:0.34, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01} |
| 0.0197 | poly {High:0.01, Low:0.33, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01} |
| 0.0158 | poly {High:0.01, Low:0.33, X:0.6, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01} |
| 0.0155 | poly {High:0.01, Low:0.35, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01} |
| 0.0155 | poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01} |
| 0.0152 | poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {High:0.01, Low:0.33, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}
    - 3.04e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.04e-05, rho=8.25e-03 k*=100)
    - 3.04e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.04e-05, rho=8.25e-03 k*=100)
    - 1.44e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.44e-05, rho=2.09e-02 k*=66)
    - 1.44e-05 -> poly {High:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.44e-05, rho=2.09e-02 k*=66)
    - 6.31e-06 -> mono {THEM(^Low):1}   via THEM(^Low) (6.31e-06, rho=8.25e-03 k*=100)
    - 4.85e-06 -> mono {THEM(^X):1}   via THEM(^X) (4.85e-06, rho=6.34e-03 k*=100)
- poly {High:0.3, Low:0.62, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}
    - 2.19e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (2.19e-05, rho=3.17e-02 k*=66)
    - 2.19e-05 -> poly {High:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (2.19e-05, rho=3.17e-02 k*=66)
    - 1.92e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (1.92e-05, rho=5.21e-03 k*=100)
    - 1.92e-05 -> mono {THEM(ME):1}   via THEM(ME) (1.92e-05, rho=5.21e-03 k*=100)
    - 4.49e-06 -> poly {High:0.33, Low:0.44, not(THEM(^High)):0.22, or(THEM(ME),Low):0.01}   via not(THEM(^High)) (4.49e-06, rho=5.90e-02 k*=22)
    - 3.98e-06 -> mono {THEM(^Low):1}   via THEM(^Low) (3.98e-06, rho=5.21e-03 k*=100)
- poly {High:0.01, Low:0.34, X:0.63, and(X,X):0.01, or(X,X):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.35, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.07e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.07e-05, rho=8.33e-03 k*=100)
- poly {High:0.32, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01}
    - 1.52e-04 -> poly {High:0.32, Low:0.64, X:0.01, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.32, Low:0.64, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.31, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.32, Low:0.64, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.31, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 2.23e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (2.23e-05, rho=3.24e-02 k*=67)
- poly {High:0.01, Low:0.34, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.58, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.03e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.03e-05, rho=8.22e-03 k*=100)
    - 3.03e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.03e-05, rho=8.22e-03 k*=100)
    - 1.43e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.43e-05, rho=2.08e-02 k*=67)
    - 1.43e-05 -> poly {High:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.43e-05, rho=2.08e-02 k*=67)
    - 6.29e-06 -> mono {THEM(^Low):1}   via THEM(^Low) (6.29e-06, rho=8.22e-03 k*=100)
- poly {High:0.01, Low:0.33, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.33, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.04e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.04e-05, rho=8.25e-03 k*=100)
    - 3.04e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.04e-05, rho=8.25e-03 k*=100)
    - 1.42e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.42e-05, rho=2.07e-02 k*=67)
    - 1.42e-05 -> poly {High:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.42e-05, rho=2.07e-02 k*=67)
    - 6.31e-06 -> mono {THEM(^Low):1}   via THEM(^Low) (6.31e-06, rho=8.25e-03 k*=100)
- poly {High:0.01, Low:0.34, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.58, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.04e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.04e-05, rho=8.25e-03 k*=100)
    - 3.04e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.04e-05, rho=8.25e-03 k*=100)
    - 1.44e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.44e-05, rho=2.10e-02 k*=67)
    - 1.44e-05 -> poly {High:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.44e-05, rho=2.10e-02 k*=67)
    - 6.31e-06 -> mono {THEM(^Low):1}   via THEM(^Low) (6.31e-06, rho=8.25e-03 k*=100)
- poly {High:0.01, Low:0.33, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.33, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.04e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.04e-05, rho=8.26e-03 k*=100)
    - 3.04e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.04e-05, rho=8.26e-03 k*=100)
    - 1.42e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.42e-05, rho=2.07e-02 k*=67)
    - 1.42e-05 -> poly {High:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.42e-05, rho=2.07e-02 k*=67)
    - 6.31e-06 -> mono {THEM(^Low):1}   via THEM(^Low) (6.31e-06, rho=8.26e-03 k*=100)
- poly {High:0.01, Low:0.33, X:0.6, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.33, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.05e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.05e-05, rho=8.29e-03 k*=100)
    - 3.05e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.05e-05, rho=8.29e-03 k*=100)
    - 1.43e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.43e-05, rho=2.08e-02 k*=66)
    - 1.43e-05 -> poly {High:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.43e-05, rho=2.08e-02 k*=66)
    - 6.34e-06 -> mono {THEM(^Low):1}   via THEM(^Low) (6.34e-06, rho=8.29e-03 k*=100)
- poly {High:0.01, Low:0.35, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.35, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.35, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.35, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.03e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.03e-05, rho=8.23e-03 k*=100)
    - 3.03e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.03e-05, rho=8.23e-03 k*=100)
- poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.33, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.61, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.61, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.07e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.07e-05, rho=8.33e-03 k*=100)
    - 3.07e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.07e-05, rho=8.33e-03 k*=100)
- poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.61, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.35, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.07e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.07e-05, rho=8.33e-03 k*=100)
    - 3.07e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.07e-05, rho=8.33e-03 k*=100)
