### arm=weak, n=6, game=stag, N=10, w=0.01, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 46, states 81, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 8.21e-07
mean payoff 3.1601, efficient 4.0000, deadweight loss 0.8399, mean bits in support 2.79

| pi | state |
|---|---|
| 0.3515 | mono {Hare:1} |
| 0.3153 | mono {Stag:1} |
| 0.3038 | mono {X:1} |
| 0.0076 | mono {and(X,X):1} |
| 0.0072 | mono {or(X,X):1} |
| 0.0037 | mono {THEM(ME):1} |
| 0.0036 | mono {THEM(THEM):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Hare:1}
    - 3.03e-02 -> mono {Stag:1}   via Stag (3.03e-02, rho=9.21e-02 k*=10)
    - 2.96e-02 -> mono {X:1}   via X (2.96e-02, rho=9.47e-02 k*=10)
    - 7.31e-04 -> mono {and(X,X):1}   via and(X,X) (7.31e-04, rho=9.70e-02 k*=10)
    - 7.02e-04 -> mono {or(X,X):1}   via or(X,X) (7.02e-04, rho=9.31e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {Stag:1}
    - 3.38e-02 -> mono {Hare:1}   via Hare (3.38e-02, rho=1.03e-01 k*=10)
    - 3.13e-02 -> mono {X:1}   via X (3.13e-02, rho=1.00e-01 k*=10)
    - 7.63e-04 -> mono {and(X,X):1}   via and(X,X) (7.63e-04, rho=1.01e-01 k*=10)
    - 7.52e-04 -> mono {or(X,X):1}   via or(X,X) (7.52e-04, rho=9.97e-02 k*=10)
    - 3.64e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.64e-04, rho=9.87e-02 k*=10)
    - 3.62e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.62e-04, rho=9.87e-02 k*=10)
- mono {X:1}
    - 3.42e-02 -> mono {Hare:1}   via Hare (3.42e-02, rho=1.04e-01 k*=10)
    - 3.24e-02 -> mono {Stag:1}   via Stag (3.24e-02, rho=9.86e-02 k*=10)
    - 7.67e-04 -> mono {and(X,X):1}   via and(X,X) (7.67e-04, rho=1.02e-01 k*=10)
    - 7.46e-04 -> mono {or(X,X):1}   via or(X,X) (7.46e-04, rho=9.90e-02 k*=10)
    - 3.72e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.72e-04, rho=1.01e-01 k*=10)
    - 3.69e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.69e-04, rho=1.01e-01 k*=10)
- mono {and(X,X):1}
    - 3.38e-02 -> mono {Hare:1}   via Hare (3.38e-02, rho=1.03e-01 k*=10)
    - 3.16e-02 -> mono {Stag:1}   via Stag (3.16e-02, rho=9.59e-02 k*=10)
    - 3.06e-02 -> mono {X:1}   via X (3.06e-02, rho=9.80e-02 k*=10)
    - 7.29e-04 -> mono {or(X,X):1}   via or(X,X) (7.29e-04, rho=9.66e-02 k*=10)
    - 3.72e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.72e-04, rho=1.01e-01 k*=10)
    - 3.69e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.69e-04, rho=1.01e-01 k*=10)
- mono {or(X,X):1}
    - 3.43e-02 -> mono {Hare:1}   via Hare (3.43e-02, rho=1.04e-01 k*=10)
    - 3.29e-02 -> mono {Stag:1}   via Stag (3.29e-02, rho=1.00e-01 k*=10)
    - 3.15e-02 -> mono {X:1}   via X (3.15e-02, rho=1.01e-01 k*=10)
    - 7.70e-04 -> mono {and(X,X):1}   via and(X,X) (7.70e-04, rho=1.02e-01 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(ME):1}
    - 3.38e-02 -> mono {Stag:1}   via Stag (3.38e-02, rho=1.03e-01 k*=10)
    - 3.29e-02 -> mono {Hare:1}   via Hare (3.29e-02, rho=1.00e-01 k*=10)
    - 3.08e-02 -> mono {X:1}   via X (3.08e-02, rho=9.87e-02 k*=10)
    - 7.54e-04 -> mono {or(X,X):1}   via or(X,X) (7.54e-04, rho=1.00e-01 k*=10)
    - 7.44e-04 -> mono {and(X,X):1}   via and(X,X) (7.44e-04, rho=9.87e-02 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 3.38e-02 -> mono {Stag:1}   via Stag (3.38e-02, rho=1.03e-01 k*=10)
    - 3.29e-02 -> mono {Hare:1}   via Hare (3.29e-02, rho=1.00e-01 k*=10)
    - 3.08e-02 -> mono {X:1}   via X (3.08e-02, rho=9.87e-02 k*=10)
    - 7.54e-04 -> mono {or(X,X):1}   via or(X,X) (7.54e-04, rho=1.00e-01 k*=10)
    - 7.44e-04 -> mono {and(X,X):1}   via and(X,X) (7.44e-04, rho=9.87e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
