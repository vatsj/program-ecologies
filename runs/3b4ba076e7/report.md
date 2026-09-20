### arm=weak, n=6, game=dollar, N=100, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 46, states 80, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 2.66e-08
mean payoff 0.4195, efficient 0.5000, deadweight loss 0.0805, mean bits in support 2.84

| pi | state |
|---|---|
| 0.7794 | mono {Half:1} |
| 0.1179 | mono {X:1} |
| 0.0673 | mono {Greedy:1} |
| 0.0087 | mono {THEM(ME):1} |
| 0.0087 | mono {THEM(THEM):1} |
| 0.0061 | mono {or(X,X):1} |
| 0.0022 | mono {THEM(^Half):1} |
| 0.0019 | mono {not(THEM(ME)):1} |
| 0.0019 | mono {not(THEM(THEM)):1} |
| 0.0018 | mono {and(X,X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Half:1}
    - 9.83e-04 -> mono {X:1}   via X (9.83e-04, rho=3.15e-03 k*=100)
    - 5.13e-04 -> mono {Greedy:1}   via Greedy (5.13e-04, rho=1.56e-03 k*=100)
    - 4.10e-05 -> mono {or(X,X):1}   via or(X,X) (4.10e-05, rho=5.44e-03 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 1.55e-05 -> mono {and(X,X):1}   via and(X,X) (1.55e-05, rho=2.06e-03 k*=100)
- mono {X:1}
    - 6.50e-03 -> mono {Half:1}   via Half (6.50e-03, rho=1.98e-02 k*=100)
    - 2.15e-03 -> mono {Greedy:1}   via Greedy (2.15e-03, rho=6.54e-03 k*=100)
    - 1.05e-04 -> mono {or(X,X):1}   via or(X,X) (1.05e-04, rho=1.39e-02 k*=100)
    - 5.96e-05 -> mono {THEM(ME):1}   via THEM(ME) (5.96e-05, rho=1.61e-02 k*=100)
    - 5.92e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (5.92e-05, rho=1.61e-02 k*=100)
    - 5.79e-05 -> mono {and(X,X):1}   via and(X,X) (5.79e-05, rho=7.68e-03 k*=100)
- mono {Greedy:1}
    - 5.95e-03 -> mono {Half:1}   via Half (5.95e-03, rho=1.81e-02 k*=100)
    - 3.77e-03 -> mono {X:1}   via X (3.77e-03, rho=1.21e-02 k*=100)
    - 1.10e-04 -> mono {or(X,X):1}   via or(X,X) (1.10e-04, rho=1.46e-02 k*=100)
    - 7.93e-05 -> mono {and(X,X):1}   via and(X,X) (7.93e-05, rho=1.05e-02 k*=100)
    - 6.68e-05 -> mono {THEM(ME):1}   via THEM(ME) (6.68e-05, rho=1.81e-02 k*=100)
    - 6.63e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (6.63e-05, rho=1.81e-02 k*=100)
- mono {THEM(ME):1}
    - 3.29e-03 -> mono {Half:1}   via Half (3.29e-03, rho=1.00e-02 k*=100)
    - 8.03e-04 -> mono {X:1}   via X (8.03e-04, rho=2.57e-03 k*=100)
    - 5.13e-04 -> mono {Greedy:1}   via Greedy (5.13e-04, rho=1.56e-03 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 3.52e-05 -> mono {or(X,X):1}   via or(X,X) (3.52e-05, rho=4.66e-03 k*=100)
    - 1.34e-05 -> mono {and(X,X):1}   via and(X,X) (1.34e-05, rho=1.77e-03 k*=100)
- mono {THEM(THEM):1}
    - 3.29e-03 -> mono {Half:1}   via Half (3.29e-03, rho=1.00e-02 k*=100)
    - 8.03e-04 -> mono {X:1}   via X (8.03e-04, rho=2.57e-03 k*=100)
    - 5.13e-04 -> mono {Greedy:1}   via Greedy (5.13e-04, rho=1.56e-03 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.52e-05 -> mono {or(X,X):1}   via or(X,X) (3.52e-05, rho=4.66e-03 k*=100)
    - 1.34e-05 -> mono {and(X,X):1}   via and(X,X) (1.34e-05, rho=1.77e-03 k*=100)
- mono {or(X,X):1}
    - 5.22e-03 -> mono {Half:1}   via Half (5.22e-03, rho=1.59e-02 k*=100)
    - 2.03e-03 -> mono {X:1}   via X (2.03e-03, rho=6.49e-03 k*=100)
    - 1.21e-03 -> mono {Greedy:1}   via Greedy (1.21e-03, rho=3.69e-03 k*=100)
    - 5.03e-05 -> mono {THEM(ME):1}   via THEM(ME) (5.03e-05, rho=1.36e-02 k*=100)
    - 4.99e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (4.99e-05, rho=1.36e-02 k*=100)
    - 3.47e-05 -> mono {and(X,X):1}   via and(X,X) (3.47e-05, rho=4.60e-03 k*=100)
- mono {THEM(^Half):1}
    - 3.29e-03 -> mono {Half:1}   via Half (3.29e-03, rho=1.00e-02 k*=100)
    - 8.03e-04 -> mono {X:1}   via X (8.03e-04, rho=2.57e-03 k*=100)
    - 5.13e-04 -> mono {Greedy:1}   via Greedy (5.13e-04, rho=1.56e-03 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 3.52e-05 -> mono {or(X,X):1}   via or(X,X) (3.52e-05, rho=4.66e-03 k*=100)
- mono {not(THEM(ME)):1}
    - 1.36e-03 -> mono {Half:1}   via Half (1.36e-03, rho=4.14e-03 k*=100)
    - 8.03e-04 -> mono {X:1}   via X (8.03e-04, rho=2.57e-03 k*=100)
    - 5.13e-04 -> mono {Greedy:1}   via Greedy (5.13e-04, rho=1.56e-03 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 2.55e-05 -> mono {or(X,X):1}   via or(X,X) (2.55e-05, rho=3.38e-03 k*=100)
- mono {not(THEM(THEM)):1}
    - 1.36e-03 -> mono {Half:1}   via Half (1.36e-03, rho=4.14e-03 k*=100)
    - 8.03e-04 -> mono {X:1}   via X (8.03e-04, rho=2.57e-03 k*=100)
    - 5.13e-04 -> mono {Greedy:1}   via Greedy (5.13e-04, rho=1.56e-03 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 2.55e-05 -> mono {or(X,X):1}   via or(X,X) (2.55e-05, rho=3.38e-03 k*=100)
- mono {and(X,X):1}
    - 6.74e-03 -> mono {Half:1}   via Half (6.74e-03, rho=2.05e-02 k*=100)
    - 3.80e-03 -> mono {X:1}   via X (3.80e-03, rho=1.22e-02 k*=100)
    - 2.97e-03 -> mono {Greedy:1}   via Greedy (2.97e-03, rho=9.02e-03 k*=100)
    - 1.18e-04 -> mono {or(X,X):1}   via or(X,X) (1.18e-04, rho=1.57e-02 k*=100)
    - 6.50e-05 -> mono {THEM(ME):1}   via THEM(ME) (6.50e-05, rho=1.76e-02 k*=100)
    - 6.45e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (6.45e-05, rho=1.76e-02 k*=100)
