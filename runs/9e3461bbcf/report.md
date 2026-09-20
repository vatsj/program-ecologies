### arm=weak, n=6, game=stag, N=10, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 46, states 81, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 6.80e-07
mean payoff 3.0850, efficient 4.0000, deadweight loss 0.9150, mean bits in support 2.76

| pi | state |
|---|---|
| 0.5701 | mono {Hare:1} |
| 0.2113 | mono {X:1} |
| 0.1934 | mono {Stag:1} |
| 0.0074 | mono {and(X,X):1} |
| 0.0043 | mono {or(X,X):1} |
| 0.0035 | mono {THEM(ME):1} |
| 0.0034 | mono {THEM(THEM):1} |
| 0.0013 | mono {THEM(^Stag):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Hare:1}
    - 1.74e-02 -> mono {X:1}   via X (1.74e-02, rho=5.56e-02 k*=10)
    - 1.36e-02 -> mono {Stag:1}   via Stag (1.36e-02, rho=4.14e-02 k*=10)
    - 5.47e-04 -> mono {and(X,X):1}   via and(X,X) (5.47e-04, rho=7.26e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
    - 3.47e-04 -> mono {or(X,X):1}   via or(X,X) (3.47e-04, rho=4.61e-02 k*=10)
- mono {X:1}
    - 4.73e-02 -> mono {Hare:1}   via Hare (4.73e-02, rho=1.44e-01 k*=10)
    - 2.85e-02 -> mono {Stag:1}   via Stag (2.85e-02, rho=8.66e-02 k*=10)
    - 8.88e-04 -> mono {and(X,X):1}   via and(X,X) (8.88e-04, rho=1.18e-01 k*=10)
    - 6.78e-04 -> mono {or(X,X):1}   via or(X,X) (6.78e-04, rho=9.00e-02 k*=10)
    - 3.94e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.94e-04, rho=1.07e-01 k*=10)
    - 3.91e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.91e-04, rho=1.07e-01 k*=10)
- mono {Stag:1}
    - 4.09e-02 -> mono {Hare:1}   via Hare (4.09e-02, rho=1.24e-01 k*=10)
    - 3.14e-02 -> mono {X:1}   via X (3.14e-02, rho=1.01e-01 k*=10)
    - 8.30e-04 -> mono {and(X,X):1}   via and(X,X) (8.30e-04, rho=1.10e-01 k*=10)
    - 7.32e-04 -> mono {or(X,X):1}   via or(X,X) (7.32e-04, rho=9.71e-02 k*=10)
    - 3.20e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.20e-04, rho=8.67e-02 k*=10)
    - 3.18e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.18e-04, rho=8.67e-02 k*=10)
- mono {and(X,X):1}
    - 4.24e-02 -> mono {Hare:1}   via Hare (4.24e-02, rho=1.29e-01 k*=10)
    - 2.53e-02 -> mono {X:1}   via X (2.53e-02, rho=8.10e-02 k*=10)
    - 2.14e-02 -> mono {Stag:1}   via Stag (2.14e-02, rho=6.51e-02 k*=10)
    - 5.28e-04 -> mono {or(X,X):1}   via or(X,X) (5.28e-04, rho=7.00e-02 k*=10)
    - 3.94e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.94e-04, rho=1.07e-01 k*=10)
    - 3.91e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.91e-04, rho=1.07e-01 k*=10)
- mono {or(X,X):1}
    - 4.67e-02 -> mono {Hare:1}   via Hare (4.67e-02, rho=1.42e-01 k*=10)
    - 3.35e-02 -> mono {X:1}   via X (3.35e-02, rho=1.07e-01 k*=10)
    - 3.28e-02 -> mono {Stag:1}   via Stag (3.28e-02, rho=9.96e-02 k*=10)
    - 9.14e-04 -> mono {and(X,X):1}   via and(X,X) (9.14e-04, rho=1.21e-01 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(ME):1}
    - 4.26e-02 -> mono {Stag:1}   via Stag (4.26e-02, rho=1.29e-01 k*=10)
    - 3.29e-02 -> mono {Hare:1}   via Hare (3.29e-02, rho=1.00e-01 k*=10)
    - 2.73e-02 -> mono {X:1}   via X (2.73e-02, rho=8.73e-02 k*=10)
    - 7.54e-04 -> mono {or(X,X):1}   via or(X,X) (7.54e-04, rho=1.00e-01 k*=10)
    - 6.59e-04 -> mono {and(X,X):1}   via and(X,X) (6.59e-04, rho=8.73e-02 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 4.26e-02 -> mono {Stag:1}   via Stag (4.26e-02, rho=1.29e-01 k*=10)
    - 3.29e-02 -> mono {Hare:1}   via Hare (3.29e-02, rho=1.00e-01 k*=10)
    - 2.73e-02 -> mono {X:1}   via X (2.73e-02, rho=8.73e-02 k*=10)
    - 7.54e-04 -> mono {or(X,X):1}   via or(X,X) (7.54e-04, rho=1.00e-01 k*=10)
    - 6.59e-04 -> mono {and(X,X):1}   via and(X,X) (6.59e-04, rho=8.73e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
- mono {THEM(^Stag):1}
    - 3.29e-02 -> mono {Stag:1}   via Stag (3.29e-02, rho=1.00e-01 k*=10)
    - 2.50e-02 -> mono {Hare:1}   via Hare (2.50e-02, rho=7.59e-02 k*=10)
    - 2.05e-02 -> mono {X:1}   via X (2.05e-02, rho=6.58e-02 k*=10)
    - 5.73e-04 -> mono {or(X,X):1}   via or(X,X) (5.73e-04, rho=7.59e-02 k*=10)
    - 4.96e-04 -> mono {and(X,X):1}   via and(X,X) (4.96e-04, rho=6.58e-02 k*=10)
    - 3.20e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.20e-04, rho=8.67e-02 k*=10)
