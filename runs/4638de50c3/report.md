### arm=weak, n=6, game=dollar, N=10, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 46, states 108, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 4.48e-06
mean payoff 0.3914, efficient 0.5000, deadweight loss 0.1086, mean bits in support 2.83

| pi | state |
|---|---|
| 0.7161 | mono {Half:1} |
| 0.1518 | mono {X:1} |
| 0.0969 | mono {Greedy:1} |
| 0.0080 | mono {THEM(ME):1} |
| 0.0080 | mono {THEM(THEM):1} |
| 0.0068 | mono {or(X,X):1} |
| 0.0025 | mono {and(X,X):1} |
| 0.0020 | mono {THEM(^Half):1} |
| 0.0017 | mono {not(THEM(THEM)):1} |
| 0.0017 | mono {not(THEM(ME)):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Half:1}
    - 1.22e-02 -> mono {X:1}   via X (1.22e-02, rho=3.90e-02 k*=10)
    - 7.21e-03 -> mono {Greedy:1}   via Greedy (7.21e-03, rho=2.19e-02 k*=10)
    - 4.59e-04 -> mono {or(X,X):1}   via or(X,X) (4.59e-04, rho=6.09e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
    - 2.08e-04 -> mono {and(X,X):1}   via and(X,X) (2.08e-04, rho=2.76e-02 k*=10)
- mono {X:1}
    - 5.75e-02 -> mono {Half:1}   via Half (5.75e-02, rho=1.75e-01 k*=10)
    - 2.33e-02 -> mono {Greedy:1}   via Greedy (2.33e-02, rho=7.07e-02 k*=10)
    - 9.90e-04 -> mono {or(X,X):1}   via or(X,X) (9.90e-04, rho=1.31e-01 k*=10)
    - 6.08e-04 -> mono {and(X,X):1}   via and(X,X) (6.08e-04, rho=8.06e-02 k*=10)
    - 5.46e-04 -> mono {THEM(ME):1}   via THEM(ME) (5.46e-04, rho=1.48e-01 k*=10)
    - 5.42e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (5.42e-04, rho=1.48e-01 k*=10)
- mono {Greedy:1}
    - 5.33e-02 -> mono {Half:1}   via Half (5.33e-02, rho=1.62e-01 k*=10)
    - 3.64e-02 -> mono {X:1}   via X (3.64e-02, rho=1.17e-01 k*=10)
    - 1.03e-03 -> mono {or(X,X):1}   via or(X,X) (1.03e-03, rho=1.36e-01 k*=10)
    - 7.86e-04 -> mono {and(X,X):1}   via and(X,X) (7.86e-04, rho=1.04e-01 k*=10)
    - 5.98e-04 -> mono {THEM(ME):1}   via THEM(ME) (5.98e-04, rho=1.62e-01 k*=10)
    - 5.94e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (5.94e-04, rho=1.62e-01 k*=10)
- mono {THEM(ME):1}
    - 3.29e-02 -> mono {Half:1}   via Half (3.29e-02, rho=1.00e-01 k*=10)
    - 1.03e-02 -> mono {X:1}   via X (1.03e-02, rho=3.30e-02 k*=10)
    - 7.21e-03 -> mono {Greedy:1}   via Greedy (7.21e-03, rho=2.19e-02 k*=10)
    - 4.05e-04 -> mono {or(X,X):1}   via or(X,X) (4.05e-04, rho=5.36e-02 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
    - 1.83e-04 -> mono {and(X,X):1}   via and(X,X) (1.83e-04, rho=2.43e-02 k*=10)
- mono {THEM(THEM):1}
    - 3.29e-02 -> mono {Half:1}   via Half (3.29e-02, rho=1.00e-01 k*=10)
    - 1.03e-02 -> mono {X:1}   via X (1.03e-02, rho=3.30e-02 k*=10)
    - 7.21e-03 -> mono {Greedy:1}   via Greedy (7.21e-03, rho=2.19e-02 k*=10)
    - 4.05e-04 -> mono {or(X,X):1}   via or(X,X) (4.05e-04, rho=5.36e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 1.83e-04 -> mono {and(X,X):1}   via and(X,X) (1.83e-04, rho=2.43e-02 k*=10)
- mono {or(X,X):1}
    - 4.80e-02 -> mono {Half:1}   via Half (4.80e-02, rho=1.46e-01 k*=10)
    - 2.19e-02 -> mono {X:1}   via X (2.19e-02, rho=7.03e-02 k*=10)
    - 1.46e-02 -> mono {Greedy:1}   via Greedy (1.46e-02, rho=4.43e-02 k*=10)
    - 4.75e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.75e-04, rho=1.29e-01 k*=10)
    - 4.72e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (4.72e-04, rho=1.29e-01 k*=10)
    - 4.01e-04 -> mono {and(X,X):1}   via and(X,X) (4.01e-04, rho=5.31e-02 k*=10)
- mono {and(X,X):1}
    - 5.91e-02 -> mono {Half:1}   via Half (5.91e-02, rho=1.80e-01 k*=10)
    - 3.66e-02 -> mono {X:1}   via X (3.66e-02, rho=1.17e-01 k*=10)
    - 3.02e-02 -> mono {Greedy:1}   via Greedy (3.02e-02, rho=9.19e-02 k*=10)
    - 1.09e-03 -> mono {or(X,X):1}   via or(X,X) (1.09e-03, rho=1.44e-01 k*=10)
    - 5.85e-04 -> mono {THEM(ME):1}   via THEM(ME) (5.85e-04, rho=1.59e-01 k*=10)
    - 5.81e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (5.81e-04, rho=1.59e-01 k*=10)
- mono {THEM(^Half):1}
    - 3.29e-02 -> mono {Half:1}   via Half (3.29e-02, rho=1.00e-01 k*=10)
    - 1.03e-02 -> mono {X:1}   via X (1.03e-02, rho=3.30e-02 k*=10)
    - 7.21e-03 -> mono {Greedy:1}   via Greedy (7.21e-03, rho=2.19e-02 k*=10)
    - 4.05e-04 -> mono {or(X,X):1}   via or(X,X) (4.05e-04, rho=5.36e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {not(THEM(THEM)):1}
    - 1.57e-02 -> mono {Half:1}   via Half (1.57e-02, rho=4.77e-02 k*=10)
    - 1.03e-02 -> mono {X:1}   via X (1.03e-02, rho=3.30e-02 k*=10)
    - 7.21e-03 -> mono {Greedy:1}   via Greedy (7.21e-03, rho=2.19e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
    - 3.09e-04 -> mono {or(X,X):1}   via or(X,X) (3.09e-04, rho=4.10e-02 k*=10)
- mono {not(THEM(ME)):1}
    - 1.57e-02 -> mono {Half:1}   via Half (1.57e-02, rho=4.77e-02 k*=10)
    - 1.03e-02 -> mono {X:1}   via X (1.03e-02, rho=3.30e-02 k*=10)
    - 7.21e-03 -> mono {Greedy:1}   via Greedy (7.21e-03, rho=2.19e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
    - 3.09e-04 -> mono {or(X,X):1}   via or(X,X) (3.09e-04, rho=4.10e-02 k*=10)
