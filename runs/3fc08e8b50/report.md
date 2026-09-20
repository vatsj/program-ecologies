### arm=weak, n=5, game=demand_norole, N=10, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 450, classes 30, states 760, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 6.50e-03
mean payoff 0.3951, efficient 0.5000, deadweight loss 0.1049, mean bits in support 4.40

| pi | state |
|---|---|
| 0.2221 | poly {High:0.1, Low:0.4, X:0.3, and(X,X):0.1, or(X,X):0.1} |
| 0.1659 | poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1} |
| 0.0376 | poly {High:0.1, Low:0.4, X:0.5} |
| 0.0318 | poly {High:0.1, Low:0.4, X:0.4, and(X,X):0.1} |
| 0.0302 | poly {High:0.1, Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1} |
| 0.0295 | poly {High:0.3, Low:0.6, X:0.1} |
| 0.0258 | poly {High:0.1, Low:0.3, X:0.3, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Low):0.1} |
| 0.0256 | poly {High:0.1, Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1} |
| 0.0256 | poly {High:0.1, Low:0.3, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1} |
| 0.0240 | poly {High:0.3, Low:0.5, X:0.1, or(X,X):0.1} |
| 0.0240 | poly {High:0.2, Low:0.6, X:0.1, and(X,X):0.1} |
| 0.0233 | poly {High:0.1, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {High:0.1, Low:0.4, X:0.3, and(X,X):0.1, or(X,X):0.1}
    - 3.37e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.37e-04, rho=9.15e-02 k*=10)
    - 3.37e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.37e-04, rho=9.15e-02 k*=10)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.3, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1}
    - 3.23e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.23e-04, rho=8.78e-02 k*=10)
    - 3.23e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.23e-04, rho=8.78e-02 k*=10)
    - 1.52e-04 -> poly {High:0.2, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.2, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.4, X:0.5}
    - 6.74e-03 -> poly {High:0.1, Low:0.4, X:0.4, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {High:0.1, Low:0.4, X:0.4, and(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.40e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.40e-04, rho=9.24e-02 k*=10)
    - 3.40e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.40e-04, rho=9.24e-02 k*=10)
    - 1.52e-04 -> poly {Low:0.4, X:0.6}   via and(THEM(ME),X) (7.61e-05, rho=1.00e+00 k*=1), and(THEM(THEM),X) (7.61e-05, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.5, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.4, X:0.4, and(X,X):0.1}
    - 6.74e-03 -> poly {High:0.1, Low:0.4, X:0.3, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.39e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.39e-04, rho=9.21e-02 k*=10)
    - 3.39e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.39e-04, rho=9.21e-02 k*=10)
    - 1.52e-04 -> poly {Low:0.5, X:0.3, and(X,X):0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.3, and(X,X):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.3, and(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}
    - 3.37e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.37e-04, rho=9.14e-02 k*=10)
    - 3.37e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.37e-04, rho=9.14e-02 k*=10)
    - 1.52e-04 -> poly {Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.3, Low:0.6, X:0.1}
    - 6.74e-03 -> poly {High:0.3, Low:0.5, X:0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {High:0.2, Low:0.6, X:0.1, and(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.13e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.13e-04, rho=8.50e-02 k*=10)
    - 3.13e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.13e-04, rho=8.50e-02 k*=10)
    - 1.52e-04 -> poly {High:0.3, Low:0.5, X:0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.3, Low:0.5, X:0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.3, X:0.3, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Low):0.1}
    - 3.37e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.37e-04, rho=9.15e-02 k*=10)
    - 3.37e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.37e-04, rho=9.15e-02 k*=10)
    - 1.52e-04 -> poly {High:0.1, Low:0.2, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),Low):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(THEM(ME),Low):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(THEM(ME),Low):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(THEM(ME),Low):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1}
    - 3.34e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.34e-04, rho=9.08e-02 k*=10)
    - 3.34e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.34e-04, rho=9.08e-02 k*=10)
    - 1.52e-04 -> poly {Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,and(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.3, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}
    - 3.40e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.40e-04, rho=9.24e-02 k*=10)
    - 3.40e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.40e-04, rho=9.24e-02 k*=10)
    - 1.52e-04 -> poly {High:0.1, Low:0.2, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.3, Low:0.5, X:0.1, or(X,X):0.1}
    - 6.74e-03 -> poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.19e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.19e-04, rho=8.65e-02 k*=10)
    - 3.19e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.19e-04, rho=8.65e-02 k*=10)
    - 1.52e-04 -> poly {High:0.3, Low:0.4, X:0.1, or(X,X):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.2, Low:0.5, X:0.1, or(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.2, Low:0.5, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.2, Low:0.6, X:0.1, and(X,X):0.1}
    - 6.74e-03 -> poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.18e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.18e-04, rho=8.64e-02 k*=10)
    - 3.18e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.18e-04, rho=8.64e-02 k*=10)
    - 1.52e-04 -> poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.6, X:0.1, and(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}
    - 3.30e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.30e-04, rho=8.96e-02 k*=10)
    - 3.30e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.30e-04, rho=8.96e-02 k*=10)
    - 1.52e-04 -> poly {Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
