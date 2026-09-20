### arm=weak, n=6, game=dollar, N=10, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 46, states 108, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 1.00e-05
mean payoff 0.2304, efficient 0.5000, deadweight loss 0.2696, mean bits in support 2.80

| pi | state |
|---|---|
| 0.3678 | mono {Half:1} |
| 0.3011 | mono {Greedy:1} |
| 0.3006 | mono {X:1} |
| 0.0077 | mono {or(X,X):1} |
| 0.0070 | mono {and(X,X):1} |
| 0.0041 | mono {THEM(ME):1} |
| 0.0041 | mono {THEM(THEM):1} |
| 0.0010 | mono {THEM(^Half):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Half:1}
    - 2.87e-02 -> mono {Greedy:1}   via Greedy (2.87e-02, rho=8.73e-02 k*=10)
    - 2.87e-02 -> mono {X:1}   via X (2.87e-02, rho=9.19e-02 k*=10)
    - 7.20e-04 -> mono {or(X,X):1}   via or(X,X) (7.20e-04, rho=9.55e-02 k*=10)
    - 6.73e-04 -> mono {and(X,X):1}   via and(X,X) (6.73e-04, rho=8.92e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {Greedy:1}
    - 3.51e-02 -> mono {Half:1}   via Half (3.51e-02, rho=1.07e-01 k*=10)
    - 3.18e-02 -> mono {X:1}   via X (3.18e-02, rho=1.02e-01 k*=10)
    - 7.82e-04 -> mono {or(X,X):1}   via or(X,X) (7.82e-04, rho=1.04e-01 k*=10)
    - 7.57e-04 -> mono {and(X,X):1}   via and(X,X) (7.57e-04, rho=1.00e-01 k*=10)
    - 3.94e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.94e-04, rho=1.07e-01 k*=10)
    - 3.91e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.91e-04, rho=1.07e-01 k*=10)
- mono {X:1}
    - 3.51e-02 -> mono {Half:1}   via Half (3.51e-02, rho=1.07e-01 k*=10)
    - 3.18e-02 -> mono {Greedy:1}   via Greedy (3.18e-02, rho=9.67e-02 k*=10)
    - 7.76e-04 -> mono {or(X,X):1}   via or(X,X) (7.76e-04, rho=1.03e-01 k*=10)
    - 7.39e-04 -> mono {and(X,X):1}   via and(X,X) (7.39e-04, rho=9.79e-02 k*=10)
    - 3.88e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.88e-04, rho=1.05e-01 k*=10)
    - 3.85e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.85e-04, rho=1.05e-01 k*=10)
- mono {or(X,X):1}
    - 3.43e-02 -> mono {Half:1}   via Half (3.43e-02, rho=1.04e-01 k*=10)
    - 3.05e-02 -> mono {Greedy:1}   via Greedy (3.05e-02, rho=9.27e-02 k*=10)
    - 3.02e-02 -> mono {X:1}   via X (3.02e-02, rho=9.67e-02 k*=10)
    - 7.11e-04 -> mono {and(X,X):1}   via and(X,X) (7.11e-04, rho=9.43e-02 k*=10)
    - 3.80e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.80e-04, rho=1.03e-01 k*=10)
    - 3.77e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.77e-04, rho=1.03e-01 k*=10)
- mono {and(X,X):1}
    - 3.54e-02 -> mono {Half:1}   via Half (3.54e-02, rho=1.08e-01 k*=10)
    - 3.26e-02 -> mono {Greedy:1}   via Greedy (3.26e-02, rho=9.92e-02 k*=10)
    - 3.18e-02 -> mono {X:1}   via X (3.18e-02, rho=1.02e-01 k*=10)
    - 7.86e-04 -> mono {or(X,X):1}   via or(X,X) (7.86e-04, rho=1.04e-01 k*=10)
    - 3.92e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.92e-04, rho=1.06e-01 k*=10)
    - 3.89e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.89e-04, rho=1.06e-01 k*=10)
- mono {THEM(ME):1}
    - 3.29e-02 -> mono {Half:1}   via Half (3.29e-02, rho=1.00e-01 k*=10)
    - 2.87e-02 -> mono {Greedy:1}   via Greedy (2.87e-02, rho=8.73e-02 k*=10)
    - 2.82e-02 -> mono {X:1}   via X (2.82e-02, rho=9.04e-02 k*=10)
    - 7.11e-04 -> mono {or(X,X):1}   via or(X,X) (7.11e-04, rho=9.43e-02 k*=10)
    - 6.64e-04 -> mono {and(X,X):1}   via and(X,X) (6.64e-04, rho=8.81e-02 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 3.29e-02 -> mono {Half:1}   via Half (3.29e-02, rho=1.00e-01 k*=10)
    - 2.87e-02 -> mono {Greedy:1}   via Greedy (2.87e-02, rho=8.73e-02 k*=10)
    - 2.82e-02 -> mono {X:1}   via X (2.82e-02, rho=9.04e-02 k*=10)
    - 7.11e-04 -> mono {or(X,X):1}   via or(X,X) (7.11e-04, rho=9.43e-02 k*=10)
    - 6.64e-04 -> mono {and(X,X):1}   via and(X,X) (6.64e-04, rho=8.81e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
- mono {THEM(^Half):1}
    - 3.29e-02 -> mono {Half:1}   via Half (3.29e-02, rho=1.00e-01 k*=10)
    - 2.87e-02 -> mono {Greedy:1}   via Greedy (2.87e-02, rho=8.73e-02 k*=10)
    - 2.82e-02 -> mono {X:1}   via X (2.82e-02, rho=9.04e-02 k*=10)
    - 7.11e-04 -> mono {or(X,X):1}   via or(X,X) (7.11e-04, rho=9.43e-02 k*=10)
    - 6.64e-04 -> mono {and(X,X):1}   via and(X,X) (6.64e-04, rho=8.81e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
