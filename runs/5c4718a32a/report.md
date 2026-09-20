### arm=weak, n=5, game=demand_norole, N=100, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 450, classes 30, states 748, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 9.67e-04
mean payoff 0.3991, efficient 0.5000, deadweight loss 0.1009, mean bits in support 3.23

| pi | state |
|---|---|
| 0.1155 | poly {High:0.01, Low:0.33, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01} |
| 0.0970 | poly {High:0.3, Low:0.62, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01} |
| 0.0709 | poly {High:0.01, Low:0.34, X:0.63, and(X,X):0.01, or(X,X):0.01} |
| 0.0527 | poly {High:0.32, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01} |
| 0.0190 | poly {High:0.01, Low:0.34, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(THEM(ME),Low):0.01} |
| 0.0190 | poly {High:0.01, Low:0.33, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01} |
| 0.0188 | poly {High:0.01, Low:0.34, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01} |
| 0.0180 | poly {High:0.01, Low:0.33, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01} |
| 0.0151 | poly {High:0.01, Low:0.35, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01} |
| 0.0151 | poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01} |
| 0.0148 | poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01} |
| 0.0147 | poly {High:0.3, Low:0.63, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {High:0.01, Low:0.33, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}
    - 3.46e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.46e-05, rho=9.39e-03 k*=100)
    - 3.46e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.46e-05, rho=9.39e-03 k*=100)
    - 1.17e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.17e-05, rho=1.69e-02 k*=66)
    - 1.17e-05 -> poly {High:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.17e-05, rho=1.69e-02 k*=66)
    - 7.18e-06 -> mono {THEM(^Low):1}   via THEM(^Low) (7.18e-06, rho=9.39e-03 k*=100)
    - 6.60e-06 -> mono {THEM(^X):1}   via THEM(^X) (6.60e-06, rho=8.63e-03 k*=100)
- poly {High:0.3, Low:0.62, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}
    - 2.99e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.99e-05, rho=8.11e-03 k*=100)
    - 2.99e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.99e-05, rho=8.11e-03 k*=100)
    - 1.36e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.36e-05, rho=1.97e-02 k*=66)
    - 1.36e-05 -> poly {High:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.36e-05, rho=1.97e-02 k*=66)
    - 6.20e-06 -> mono {THEM(^Low):1}   via THEM(^Low) (6.20e-06, rho=8.11e-03 k*=100)
    - 5.71e-06 -> mono {THEM(^X):1}   via THEM(^X) (5.71e-06, rho=7.47e-03 k*=100)
- poly {High:0.01, Low:0.34, X:0.63, and(X,X):0.01, or(X,X):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.35, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.47e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.47e-05, rho=9.42e-03 k*=100)
- poly {High:0.32, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01}
    - 1.52e-04 -> poly {High:0.32, Low:0.64, X:0.01, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.32, Low:0.64, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.31, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.32, Low:0.64, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.31, Low:0.65, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 2.97e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.97e-05, rho=8.05e-03 k*=100)
- poly {High:0.01, Low:0.34, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.58, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.45e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.45e-05, rho=9.38e-03 k*=100)
    - 3.45e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.45e-05, rho=9.38e-03 k*=100)
    - 1.15e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.15e-05, rho=1.67e-02 k*=67)
    - 1.15e-05 -> poly {High:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.15e-05, rho=1.67e-02 k*=67)
    - 7.17e-06 -> mono {THEM(^Low):1}   via THEM(^Low) (7.17e-06, rho=9.38e-03 k*=100)
- poly {High:0.01, Low:0.33, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.33, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.46e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.46e-05, rho=9.39e-03 k*=100)
    - 3.46e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.46e-05, rho=9.39e-03 k*=100)
    - 1.15e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.15e-05, rho=1.67e-02 k*=67)
    - 1.15e-05 -> poly {High:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.15e-05, rho=1.67e-02 k*=67)
    - 7.18e-06 -> mono {THEM(^Low):1}   via THEM(^Low) (7.18e-06, rho=9.39e-03 k*=100)
- poly {High:0.01, Low:0.34, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.58, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.46e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.46e-05, rho=9.39e-03 k*=100)
    - 3.46e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.46e-05, rho=9.39e-03 k*=100)
    - 1.16e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.16e-05, rho=1.68e-02 k*=67)
    - 1.16e-05 -> poly {High:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.16e-05, rho=1.68e-02 k*=67)
    - 7.18e-06 -> mono {THEM(^Low):1}   via THEM(^Low) (7.18e-06, rho=9.39e-03 k*=100)
- poly {High:0.01, Low:0.33, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.33, X:0.59, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.46e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.46e-05, rho=9.39e-03 k*=100)
    - 3.46e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.46e-05, rho=9.39e-03 k*=100)
    - 1.15e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.15e-05, rho=1.67e-02 k*=67)
    - 1.15e-05 -> poly {High:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.15e-05, rho=1.67e-02 k*=67)
    - 7.18e-06 -> mono {THEM(^Low):1}   via THEM(^Low) (7.18e-06, rho=9.39e-03 k*=100)
- poly {High:0.01, Low:0.35, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.35, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.35, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.35, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.45e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.45e-05, rho=9.38e-03 k*=100)
    - 3.45e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.45e-05, rho=9.38e-03 k*=100)
- poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.33, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.61, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.61, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.47e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.47e-05, rho=9.41e-03 k*=100)
    - 3.47e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.47e-05, rho=9.41e-03 k*=100)
- poly {High:0.01, Low:0.34, X:0.62, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.61, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.34, X:0.61, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.01, Low:0.35, X:0.6, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, and(X,or(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.47e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.47e-05, rho=9.41e-03 k*=100)
    - 3.47e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.47e-05, rho=9.41e-03 k*=100)
- poly {High:0.3, Low:0.63, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01}
    - 1.52e-04 -> poly {High:0.3, Low:0.62, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01, or(X,and(X,X)):0.01, and(X,or(X,X)):0.01, or(X,or(X,X)):0.01, or(THEM(ME),Low):0.01}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 2.99e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.99e-05, rho=8.11e-03 k*=100)
    - 2.99e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.99e-05, rho=8.11e-03 k*=100)
    - 1.35e-05 -> poly {High:0.33, not(THEM(THEM)):0.67}   via not(THEM(THEM)) (1.35e-05, rho=1.96e-02 k*=67)
    - 1.35e-05 -> poly {High:0.33, not(THEM(ME)):0.67}   via not(THEM(ME)) (1.35e-05, rho=1.96e-02 k*=67)
    - 6.20e-06 -> mono {THEM(^Low):1}   via THEM(^Low) (6.20e-06, rho=8.11e-03 k*=100)
