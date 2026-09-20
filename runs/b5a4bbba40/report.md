### arm=weak, n=5, game=demand_norole, N=10, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 450, classes 30, states 764, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 6.74e-03
mean payoff 0.3935, efficient 0.5000, deadweight loss 0.1065, mean bits in support 4.33

| pi | state |
|---|---|
| 0.2074 | poly {High:0.1, Low:0.4, X:0.3, and(X,X):0.1, or(X,X):0.1} |
| 0.1846 | poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1} |
| 0.0367 | poly {High:0.1, Low:0.4, X:0.5} |
| 0.0349 | poly {High:0.3, Low:0.6, X:0.1} |
| 0.0308 | poly {High:0.1, Low:0.4, X:0.4, and(X,X):0.1} |
| 0.0281 | poly {High:0.3, Low:0.5, X:0.1, or(X,X):0.1} |
| 0.0281 | poly {High:0.2, Low:0.6, X:0.1, and(X,X):0.1} |
| 0.0271 | poly {High:0.1, Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1} |
| 0.0248 | poly {High:0.1, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1} |
| 0.0232 | poly {High:0.1, Low:0.3, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1} |
| 0.0231 | poly {High:0.1, Low:0.3, X:0.3, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Low):0.1} |
| 0.0231 | poly {High:0.1, Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {High:0.1, Low:0.4, X:0.3, and(X,X):0.1, or(X,X):0.1}
    - 3.65e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.65e-04, rho=9.91e-02 k*=10)
    - 3.65e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.65e-04, rho=9.91e-02 k*=10)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.3, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1}
    - 3.63e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.63e-04, rho=9.87e-02 k*=10)
    - 3.63e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.63e-04, rho=9.87e-02 k*=10)
    - 1.52e-04 -> poly {High:0.2, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.2, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.4, X:0.5}
    - 6.74e-03 -> poly {High:0.1, Low:0.4, X:0.4, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {High:0.1, Low:0.4, X:0.4, and(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.65e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.65e-04, rho=9.92e-02 k*=10)
    - 3.65e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.65e-04, rho=9.92e-02 k*=10)
    - 1.52e-04 -> poly {Low:0.4, X:0.6}   via and(THEM(ME),X) (7.61e-05, rho=1.00e+00 k*=1), and(THEM(THEM),X) (7.61e-05, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.5, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.3, Low:0.6, X:0.1}
    - 6.74e-03 -> poly {High:0.3, Low:0.5, X:0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {High:0.2, Low:0.6, X:0.1, and(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.62e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.62e-04, rho=9.84e-02 k*=10)
    - 3.62e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.62e-04, rho=9.84e-02 k*=10)
    - 1.52e-04 -> poly {High:0.3, Low:0.5, X:0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.3, Low:0.5, X:0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.4, X:0.4, and(X,X):0.1}
    - 6.74e-03 -> poly {High:0.1, Low:0.4, X:0.3, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.65e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.65e-04, rho=9.92e-02 k*=10)
    - 3.65e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.65e-04, rho=9.92e-02 k*=10)
    - 1.52e-04 -> poly {Low:0.5, X:0.3, and(X,X):0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.3, and(X,X):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.3, and(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.3, Low:0.5, X:0.1, or(X,X):0.1}
    - 6.74e-03 -> poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.63e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.63e-04, rho=9.86e-02 k*=10)
    - 3.63e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.63e-04, rho=9.86e-02 k*=10)
    - 1.52e-04 -> poly {High:0.3, Low:0.4, X:0.1, or(X,X):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.2, Low:0.5, X:0.1, or(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.2, Low:0.5, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.2, Low:0.6, X:0.1, and(X,X):0.1}
    - 6.74e-03 -> poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.63e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.63e-04, rho=9.86e-02 k*=10)
    - 3.63e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.63e-04, rho=9.86e-02 k*=10)
    - 1.52e-04 -> poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.6, X:0.1, and(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}
    - 3.65e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.65e-04, rho=9.91e-02 k*=10)
    - 3.65e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.65e-04, rho=9.91e-02 k*=10)
    - 1.52e-04 -> poly {Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}
    - 3.64e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.64e-04, rho=9.89e-02 k*=10)
    - 3.64e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.64e-04, rho=9.89e-02 k*=10)
    - 1.52e-04 -> poly {Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.3, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}
    - 3.65e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.65e-04, rho=9.92e-02 k*=10)
    - 3.65e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.65e-04, rho=9.92e-02 k*=10)
    - 1.52e-04 -> poly {High:0.1, Low:0.2, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.3, X:0.3, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Low):0.1}
    - 3.65e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.65e-04, rho=9.91e-02 k*=10)
    - 3.65e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.65e-04, rho=9.91e-02 k*=10)
    - 1.52e-04 -> poly {High:0.1, Low:0.2, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),Low):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(THEM(ME),Low):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(THEM(ME),Low):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(THEM(ME),Low):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1}
    - 3.65e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.65e-04, rho=9.91e-02 k*=10)
    - 3.65e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.65e-04, rho=9.91e-02 k*=10)
    - 1.52e-04 -> poly {Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,and(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
