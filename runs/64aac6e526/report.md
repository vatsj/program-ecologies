### arm=weak, n=6, game=dollar, N=10, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 46, states 108, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 8.85e-06
mean payoff 0.2690, efficient 0.5000, deadweight loss 0.2310, mean bits in support 2.81

| pi | state |
|---|---|
| 0.4494 | mono {Half:1} |
| 0.2721 | mono {X:1} |
| 0.2466 | mono {Greedy:1} |
| 0.0079 | mono {or(X,X):1} |
| 0.0059 | mono {and(X,X):1} |
| 0.0050 | mono {THEM(ME):1} |
| 0.0050 | mono {THEM(THEM):1} |
| 0.0012 | mono {THEM(^Half):1} |
| 0.0011 | mono {not(THEM(THEM)):1} |
| 0.0011 | mono {not(THEM(ME)):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Half:1}
    - 2.41e-02 -> mono {X:1}   via X (2.41e-02, rho=7.71e-02 k*=10)
    - 2.16e-02 -> mono {Greedy:1}   via Greedy (2.16e-02, rho=6.58e-02 k*=10)
    - 6.55e-04 -> mono {or(X,X):1}   via or(X,X) (6.55e-04, rho=8.68e-02 k*=10)
    - 5.30e-04 -> mono {and(X,X):1}   via and(X,X) (5.30e-04, rho=7.02e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {X:1}
    - 3.98e-02 -> mono {Half:1}   via Half (3.98e-02, rho=1.21e-01 k*=10)
    - 2.97e-02 -> mono {Greedy:1}   via Greedy (2.97e-02, rho=9.04e-02 k*=10)
    - 8.22e-04 -> mono {or(X,X):1}   via or(X,X) (8.22e-04, rho=1.09e-01 k*=10)
    - 7.08e-04 -> mono {and(X,X):1}   via and(X,X) (7.08e-04, rho=9.39e-02 k*=10)
    - 4.24e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.24e-04, rho=1.15e-01 k*=10)
    - 4.21e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (4.21e-04, rho=1.15e-01 k*=10)
- mono {Greedy:1}
    - 3.94e-02 -> mono {Half:1}   via Half (3.94e-02, rho=1.20e-01 k*=10)
    - 3.28e-02 -> mono {X:1}   via X (3.28e-02, rho=1.05e-01 k*=10)
    - 8.39e-04 -> mono {or(X,X):1}   via or(X,X) (8.39e-04, rho=1.11e-01 k*=10)
    - 7.64e-04 -> mono {and(X,X):1}   via and(X,X) (7.64e-04, rho=1.01e-01 k*=10)
    - 4.42e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.42e-04, rho=1.20e-01 k*=10)
    - 4.39e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (4.39e-04, rho=1.20e-01 k*=10)
- mono {or(X,X):1}
    - 3.71e-02 -> mono {Half:1}   via Half (3.71e-02, rho=1.13e-01 k*=10)
    - 2.82e-02 -> mono {X:1}   via X (2.82e-02, rho=9.03e-02 k*=10)
    - 2.61e-02 -> mono {Greedy:1}   via Greedy (2.61e-02, rho=7.94e-02 k*=10)
    - 6.30e-04 -> mono {and(X,X):1}   via and(X,X) (6.30e-04, rho=8.36e-02 k*=10)
    - 4.01e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.01e-04, rho=1.09e-01 k*=10)
    - 3.99e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.99e-04, rho=1.09e-01 k*=10)
- mono {and(X,X):1}
    - 4.05e-02 -> mono {Half:1}   via Half (4.05e-02, rho=1.23e-01 k*=10)
    - 3.28e-02 -> mono {X:1}   via X (3.28e-02, rho=1.05e-01 k*=10)
    - 3.21e-02 -> mono {Greedy:1}   via Greedy (3.21e-02, rho=9.75e-02 k*=10)
    - 8.51e-04 -> mono {or(X,X):1}   via or(X,X) (8.51e-04, rho=1.13e-01 k*=10)
    - 4.38e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.38e-04, rho=1.19e-01 k*=10)
    - 4.35e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (4.35e-04, rho=1.19e-01 k*=10)
- mono {THEM(ME):1}
    - 3.29e-02 -> mono {Half:1}   via Half (3.29e-02, rho=1.00e-01 k*=10)
    - 2.29e-02 -> mono {X:1}   via X (2.29e-02, rho=7.33e-02 k*=10)
    - 2.16e-02 -> mono {Greedy:1}   via Greedy (2.16e-02, rho=6.58e-02 k*=10)
    - 6.31e-04 -> mono {or(X,X):1}   via or(X,X) (6.31e-04, rho=8.36e-02 k*=10)
    - 5.10e-04 -> mono {and(X,X):1}   via and(X,X) (5.10e-04, rho=6.76e-02 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 3.29e-02 -> mono {Half:1}   via Half (3.29e-02, rho=1.00e-01 k*=10)
    - 2.29e-02 -> mono {X:1}   via X (2.29e-02, rho=7.33e-02 k*=10)
    - 2.16e-02 -> mono {Greedy:1}   via Greedy (2.16e-02, rho=6.58e-02 k*=10)
    - 6.31e-04 -> mono {or(X,X):1}   via or(X,X) (6.31e-04, rho=8.36e-02 k*=10)
    - 5.10e-04 -> mono {and(X,X):1}   via and(X,X) (5.10e-04, rho=6.76e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
- mono {THEM(^Half):1}
    - 3.29e-02 -> mono {Half:1}   via Half (3.29e-02, rho=1.00e-01 k*=10)
    - 2.29e-02 -> mono {X:1}   via X (2.29e-02, rho=7.33e-02 k*=10)
    - 2.16e-02 -> mono {Greedy:1}   via Greedy (2.16e-02, rho=6.58e-02 k*=10)
    - 6.31e-04 -> mono {or(X,X):1}   via or(X,X) (6.31e-04, rho=8.36e-02 k*=10)
    - 5.10e-04 -> mono {and(X,X):1}   via and(X,X) (5.10e-04, rho=6.76e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
- mono {not(THEM(THEM)):1}
    - 2.67e-02 -> mono {Half:1}   via Half (2.67e-02, rho=8.13e-02 k*=10)
    - 2.29e-02 -> mono {X:1}   via X (2.29e-02, rho=7.33e-02 k*=10)
    - 2.16e-02 -> mono {Greedy:1}   via Greedy (2.16e-02, rho=6.58e-02 k*=10)
    - 5.84e-04 -> mono {or(X,X):1}   via or(X,X) (5.84e-04, rho=7.74e-02 k*=10)
    - 5.23e-04 -> mono {and(X,X):1}   via and(X,X) (5.23e-04, rho=6.93e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
- mono {not(THEM(ME)):1}
    - 2.67e-02 -> mono {Half:1}   via Half (2.67e-02, rho=8.13e-02 k*=10)
    - 2.29e-02 -> mono {X:1}   via X (2.29e-02, rho=7.33e-02 k*=10)
    - 2.16e-02 -> mono {Greedy:1}   via Greedy (2.16e-02, rho=6.58e-02 k*=10)
    - 5.84e-04 -> mono {or(X,X):1}   via or(X,X) (5.84e-04, rho=7.74e-02 k*=10)
    - 5.23e-04 -> mono {and(X,X):1}   via and(X,X) (5.23e-04, rho=6.93e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
