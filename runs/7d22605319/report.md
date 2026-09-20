### arm=weak, n=5, game=demand_norole, N=10, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 450, classes 30, states 764, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 6.68e-03
mean payoff 0.3941, efficient 0.5000, deadweight loss 0.1059, mean bits in support 4.35

| pi | state |
|---|---|
| 0.2109 | poly {High:0.1, Low:0.4, X:0.3, and(X,X):0.1, or(X,X):0.1} |
| 0.1804 | poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1} |
| 0.0369 | poly {High:0.1, Low:0.4, X:0.5} |
| 0.0336 | poly {High:0.3, Low:0.6, X:0.1} |
| 0.0311 | poly {High:0.1, Low:0.4, X:0.4, and(X,X):0.1} |
| 0.0278 | poly {High:0.1, Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1} |
| 0.0271 | poly {High:0.3, Low:0.5, X:0.1, or(X,X):0.1} |
| 0.0271 | poly {High:0.2, Low:0.6, X:0.1, and(X,X):0.1} |
| 0.0245 | poly {High:0.1, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1} |
| 0.0237 | poly {High:0.1, Low:0.3, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1} |
| 0.0237 | poly {High:0.1, Low:0.3, X:0.3, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Low):0.1} |
| 0.0237 | poly {High:0.1, Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {High:0.1, Low:0.4, X:0.3, and(X,X):0.1, or(X,X):0.1}
    - 3.59e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.59e-04, rho=9.74e-02 k*=10)
    - 3.59e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.59e-04, rho=9.74e-02 k*=10)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.3, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1}
    - 3.54e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.54e-04, rho=9.62e-02 k*=10)
    - 3.54e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.54e-04, rho=9.62e-02 k*=10)
    - 1.52e-04 -> poly {High:0.2, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.2, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.4, X:0.5}
    - 6.74e-03 -> poly {High:0.1, Low:0.4, X:0.4, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {High:0.1, Low:0.4, X:0.4, and(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.60e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.60e-04, rho=9.77e-02 k*=10)
    - 3.60e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.60e-04, rho=9.77e-02 k*=10)
    - 1.52e-04 -> poly {Low:0.4, X:0.6}   via and(THEM(ME),X) (7.61e-05, rho=1.00e+00 k*=1), and(THEM(THEM),X) (7.61e-05, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.5, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.3, Low:0.6, X:0.1}
    - 6.74e-03 -> poly {High:0.3, Low:0.5, X:0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {High:0.2, Low:0.6, X:0.1, and(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.51e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.51e-04, rho=9.53e-02 k*=10)
    - 3.51e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.51e-04, rho=9.53e-02 k*=10)
    - 1.52e-04 -> poly {High:0.3, Low:0.5, X:0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.3, Low:0.5, X:0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.4, X:0.4, and(X,X):0.1}
    - 6.74e-03 -> poly {High:0.1, Low:0.4, X:0.3, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.59e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.59e-04, rho=9.76e-02 k*=10)
    - 3.59e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.59e-04, rho=9.76e-02 k*=10)
    - 1.52e-04 -> poly {Low:0.5, X:0.3, and(X,X):0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.3, and(X,X):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.3, and(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}
    - 3.59e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.59e-04, rho=9.74e-02 k*=10)
    - 3.59e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.59e-04, rho=9.74e-02 k*=10)
    - 1.52e-04 -> poly {Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.3, Low:0.5, X:0.1, or(X,X):0.1}
    - 6.74e-03 -> poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.53e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.53e-04, rho=9.58e-02 k*=10)
    - 3.53e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.53e-04, rho=9.58e-02 k*=10)
    - 1.52e-04 -> poly {High:0.3, Low:0.4, X:0.1, or(X,X):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.2, Low:0.5, X:0.1, or(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.2, Low:0.5, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.2, Low:0.6, X:0.1, and(X,X):0.1}
    - 6.74e-03 -> poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.53e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.53e-04, rho=9.58e-02 k*=10)
    - 3.53e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.53e-04, rho=9.58e-02 k*=10)
    - 1.52e-04 -> poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.2, Low:0.5, X:0.1, and(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.6, X:0.1, and(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}
    - 3.56e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.56e-04, rho=9.68e-02 k*=10)
    - 3.56e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.56e-04, rho=9.68e-02 k*=10)
    - 1.52e-04 -> poly {Low:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.3, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}
    - 3.60e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.60e-04, rho=9.77e-02 k*=10)
    - 3.60e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.60e-04, rho=9.77e-02 k*=10)
    - 1.52e-04 -> poly {High:0.1, Low:0.2, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.3, X:0.3, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Low):0.1}
    - 3.59e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.59e-04, rho=9.74e-02 k*=10)
    - 3.59e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.59e-04, rho=9.74e-02 k*=10)
    - 1.52e-04 -> poly {High:0.1, Low:0.2, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),Low):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(THEM(ME),Low):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(THEM(ME),Low):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(THEM(ME),Low):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {High:0.1, Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1}
    - 3.58e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.58e-04, rho=9.72e-02 k*=10)
    - 3.58e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.58e-04, rho=9.72e-02 k*=10)
    - 1.52e-04 -> poly {Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Low:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,and(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.3, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(THEM(ME),Low):0.1}   via or(THEM(ME),Low) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {High:0.1, Low:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
