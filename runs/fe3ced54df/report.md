### arm=weak, n=6, game=stag, N=10, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 46, states 81, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 4.42e-07
mean payoff 3.0142, efficient 4.0000, deadweight loss 0.9858, mean bits in support 2.70

| pi | state |
|---|---|
| 0.8912 | mono {Hare:1} |
| 0.0523 | mono {X:1} |
| 0.0403 | mono {Stag:1} |
| 0.0038 | mono {and(X,X):1} |
| 0.0030 | mono {THEM(ME):1} |
| 0.0030 | mono {THEM(THEM):1} |
| 0.0022 | mono {THEM(^Stag):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Hare:1}
    - 4.31e-03 -> mono {X:1}   via X (4.31e-03, rho=1.38e-02 k*=10)
    - 1.82e-03 -> mono {Stag:1}   via Stag (1.82e-03, rho=5.52e-03 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
    - 2.62e-04 -> mono {and(X,X):1}   via and(X,X) (2.62e-04, rho=3.48e-02 k*=10)
    - 1.26e-04 -> mono {THEM(^Stag):1}   via THEM(^Stag) (1.26e-04, rho=1.39e-01 k*=10)
- mono {X:1}
    - 7.85e-02 -> mono {Hare:1}   via Hare (7.85e-02, rho=2.39e-01 k*=10)
    - 2.12e-02 -> mono {Stag:1}   via Stag (2.12e-02, rho=6.43e-02 k*=10)
    - 1.18e-03 -> mono {and(X,X):1}   via and(X,X) (1.18e-03, rho=1.57e-01 k*=10)
    - 5.44e-04 -> mono {or(X,X):1}   via or(X,X) (5.44e-04, rho=7.21e-02 k*=10)
    - 4.42e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.42e-04, rho=1.20e-01 k*=10)
    - 4.39e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (4.39e-04, rho=1.20e-01 k*=10)
- mono {Stag:1}
    - 4.92e-02 -> mono {Hare:1}   via Hare (4.92e-02, rho=1.50e-01 k*=10)
    - 3.15e-02 -> mono {X:1}   via X (3.15e-02, rho=1.01e-01 k*=10)
    - 9.26e-04 -> mono {and(X,X):1}   via and(X,X) (9.26e-04, rho=1.23e-01 k*=10)
    - 6.90e-04 -> mono {or(X,X):1}   via or(X,X) (6.90e-04, rho=9.16e-02 k*=10)
    - 2.27e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.27e-04, rho=6.14e-02 k*=10)
    - 2.25e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.25e-04, rho=6.14e-02 k*=10)
- mono {and(X,X):1}
    - 6.42e-02 -> mono {Hare:1}   via Hare (6.42e-02, rho=1.95e-01 k*=10)
    - 1.59e-02 -> mono {X:1}   via X (1.59e-02, rho=5.09e-02 k*=10)
    - 8.36e-03 -> mono {Stag:1}   via Stag (8.36e-03, rho=2.54e-02 k*=10)
    - 4.42e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.42e-04, rho=1.20e-01 k*=10)
    - 4.39e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (4.39e-04, rho=1.20e-01 k*=10)
    - 2.38e-04 -> mono {or(X,X):1}   via or(X,X) (2.38e-04, rho=3.15e-02 k*=10)
- mono {THEM(ME):1}
    - 6.71e-02 -> mono {Stag:1}   via Stag (6.71e-02, rho=2.04e-01 k*=10)
    - 3.29e-02 -> mono {Hare:1}   via Hare (3.29e-02, rho=1.00e-01 k*=10)
    - 2.05e-02 -> mono {X:1}   via X (2.05e-02, rho=6.58e-02 k*=10)
    - 7.54e-04 -> mono {or(X,X):1}   via or(X,X) (7.54e-04, rho=1.00e-01 k*=10)
    - 4.96e-04 -> mono {and(X,X):1}   via and(X,X) (4.96e-04, rho=6.58e-02 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 6.71e-02 -> mono {Stag:1}   via Stag (6.71e-02, rho=2.04e-01 k*=10)
    - 3.29e-02 -> mono {Hare:1}   via Hare (3.29e-02, rho=1.00e-01 k*=10)
    - 2.05e-02 -> mono {X:1}   via X (2.05e-02, rho=6.58e-02 k*=10)
    - 7.54e-04 -> mono {or(X,X):1}   via or(X,X) (7.54e-04, rho=1.00e-01 k*=10)
    - 4.96e-04 -> mono {and(X,X):1}   via and(X,X) (4.96e-04, rho=6.58e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
- mono {THEM(^Stag):1}
    - 3.29e-02 -> mono {Stag:1}   via Stag (3.29e-02, rho=1.00e-01 k*=10)
    - 1.38e-02 -> mono {Hare:1}   via Hare (1.38e-02, rho=4.18e-02 k*=10)
    - 8.08e-03 -> mono {X:1}   via X (8.08e-03, rho=2.59e-02 k*=10)
    - 3.15e-04 -> mono {or(X,X):1}   via or(X,X) (3.15e-04, rho=4.18e-02 k*=10)
    - 2.27e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.27e-04, rho=6.14e-02 k*=10)
    - 2.25e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.25e-04, rho=6.14e-02 k*=10)
