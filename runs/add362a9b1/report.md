### arm=weak, n=6, game=stag, N=10, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 46, states 81, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 3.70e-07
mean payoff 3.0154, efficient 4.0000, deadweight loss 0.9846, mean bits in support 2.68

| pi | state |
|---|---|
| 0.9754 | mono {Hare:1} |
| 0.0112 | mono {Stag:1} |
| 0.0054 | mono {THEM(^Stag):1} |
| 0.0021 | mono {X:1} |
| 0.0017 | mono {THEM(ME):1} |
| 0.0017 | mono {THEM(THEM):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Hare:1}
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
    - 1.89e-04 -> mono {THEM(^Stag):1}   via THEM(^Stag) (1.89e-04, rho=2.08e-01 k*=10)
    - 9.10e-05 -> mono {THEM(^Hare):1}   via THEM(^Hare) (9.10e-05, rho=1.00e-01 k*=10)
    - 3.53e-05 -> mono {THEM(^X):1}   via THEM(^X) (3.53e-05, rho=4.00e-02 k*=10)
    - 2.29e-05 -> mono {and(THEM(ME),Hare):1}   via and(THEM(ME),Hare) (2.29e-05, rho=1.00e-01 k*=10)
- mono {Stag:1}
    - 4.73e-02 -> mono {Hare:1}   via Hare (4.73e-02, rho=1.44e-01 k*=10)
    - 2.91e-02 -> mono {X:1}   via X (2.91e-02, rho=9.33e-02 k*=10)
    - 9.18e-04 -> mono {and(X,X):1}   via and(X,X) (9.18e-04, rho=1.22e-01 k*=10)
    - 5.59e-04 -> mono {or(X,X):1}   via or(X,X) (5.59e-04, rho=7.41e-02 k*=10)
    - 1.14e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.14e-04, rho=1.44e-01 k*=10)
    - 1.14e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.14e-04, rho=1.44e-01 k*=10)
- mono {THEM(^Stag):1}
    - 3.29e-02 -> mono {Stag:1}   via Stag (3.29e-02, rho=1.00e-01 k*=10)
    - 1.25e-03 -> mono {Hare:1}   via Hare (1.25e-03, rho=3.81e-03 k*=10)
    - 1.87e-04 -> mono {X:1}   via X (1.87e-04, rho=6.00e-04 k*=10)
    - 1.31e-04 -> mono {THEM(^Hare):1}   via THEM(^Hare) (1.31e-04, rho=1.44e-01 k*=10)
    - 8.24e-05 -> mono {THEM(^X):1}   via THEM(^X) (8.24e-05, rho=9.33e-02 k*=10)
    - 3.61e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.61e-05, rho=9.79e-03 k*=10)
- mono {X:1}
    - 1.66e-01 -> mono {Hare:1}   via Hare (1.66e-01, rho=5.03e-01 k*=10)
    - 6.85e-03 -> mono {Stag:1}   via Stag (6.85e-03, rho=2.08e-02 k*=10)
    - 2.30e-03 -> mono {and(X,X):1}   via and(X,X) (2.30e-03, rho=3.05e-01 k*=10)
    - 5.98e-04 -> mono {THEM(ME):1}   via THEM(ME) (5.98e-04, rho=1.62e-01 k*=10)
    - 5.94e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (5.94e-04, rho=1.62e-01 k*=10)
    - 2.30e-04 -> mono {or(X,X):1}   via or(X,X) (2.30e-04, rho=3.06e-02 k*=10)
- mono {THEM(ME):1}
    - 1.76e-01 -> mono {Stag:1}   via Stag (1.76e-01, rho=5.34e-01 k*=10)
    - 3.29e-02 -> mono {Hare:1}   via Hare (3.29e-02, rho=1.00e-01 k*=10)
    - 6.85e-03 -> mono {X:1}   via X (6.85e-03, rho=2.19e-02 k*=10)
    - 7.54e-04 -> mono {or(X,X):1}   via or(X,X) (7.54e-04, rho=1.00e-01 k*=10)
    - 4.86e-04 -> mono {THEM(^Stag):1}   via THEM(^Stag) (4.86e-04, rho=5.34e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 1.76e-01 -> mono {Stag:1}   via Stag (1.76e-01, rho=5.34e-01 k*=10)
    - 3.29e-02 -> mono {Hare:1}   via Hare (3.29e-02, rho=1.00e-01 k*=10)
    - 6.85e-03 -> mono {X:1}   via X (6.85e-03, rho=2.19e-02 k*=10)
    - 7.54e-04 -> mono {or(X,X):1}   via or(X,X) (7.54e-04, rho=1.00e-01 k*=10)
    - 4.86e-04 -> mono {THEM(^Stag):1}   via THEM(^Stag) (4.86e-04, rho=5.34e-01 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
