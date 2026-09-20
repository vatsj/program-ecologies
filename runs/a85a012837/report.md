### arm=weak, n=6, game=pd, N=10, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 48, states 120, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 9.39e-07
mean payoff -0.9888, efficient 0.0000, deadweight loss 0.9888, mean bits in support 2.68

| pi | state |
|---|---|
| 0.9787 | mono {D:1} |
| 0.0076 | mono {X:1} |
| 0.0044 | mono {THEM(^C):1} |
| 0.0019 | mono {C:1} |
| 0.0016 | mono {and(X,X):1} |
| 0.0012 | mono {THEM(ME):1} |
| 0.0012 | mono {THEM(THEM):1} |
| 0.0010 | mono {THEM(^X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 5.85e-04 -> mono {X:1}   via X (5.85e-04, rho=1.87e-03 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
    - 1.89e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.89e-04, rho=2.08e-01 k*=10)
    - 1.43e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.43e-04, rho=1.62e-01 k*=10)
    - 1.33e-04 -> mono {and(X,X):1}   via and(X,X) (1.33e-04, rho=1.77e-02 k*=10)
- mono {X:1}
    - 1.51e-01 -> mono {D:1}   via D (1.51e-01, rho=4.58e-01 k*=10)
    - 2.08e-03 -> mono {and(X,X):1}   via and(X,X) (2.08e-03, rho=2.76e-01 k*=10)
    - 6.16e-04 -> mono {C:1}   via C (6.16e-04, rho=1.87e-03 k*=10)
    - 1.47e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.47e-04, rho=1.62e-01 k*=10)
    - 1.47e-04 -> mono {THEM(ME):1}   via THEM(ME) (1.47e-04, rho=4.00e-02 k*=10)
    - 1.47e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (1.47e-04, rho=4.00e-02 k*=10)
- mono {THEM(^C):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 6.85e-03 -> mono {X:1}   via X (6.85e-03, rho=2.19e-02 k*=10)
    - 1.25e-03 -> mono {D:1}   via D (1.25e-03, rho=3.81e-03 k*=10)
    - 6.42e-04 -> mono {THEM(^D):1}   via THEM(^D) (6.42e-04, rho=7.05e-01 k*=10)
    - 4.05e-04 -> mono {THEM(^X):1}   via THEM(^X) (4.05e-04, rho=4.58e-01 k*=10)
    - 3.68e-04 -> mono {or(X,X):1}   via or(X,X) (3.68e-04, rho=4.88e-02 k*=10)
- mono {C:1}
    - 2.32e-01 -> mono {D:1}   via D (2.32e-01, rho=7.05e-01 k*=10)
    - 1.43e-01 -> mono {X:1}   via X (1.43e-01, rho=4.58e-01 k*=10)
    - 4.53e-03 -> mono {and(X,X):1}   via and(X,X) (4.53e-03, rho=6.00e-01 k*=10)
    - 2.08e-03 -> mono {or(X,X):1}   via or(X,X) (2.08e-03, rho=2.76e-01 k*=10)
    - 5.61e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (5.61e-04, rho=7.05e-01 k*=10)
    - 5.61e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (5.61e-04, rho=7.05e-01 k*=10)
- mono {and(X,X):1}
    - 9.09e-02 -> mono {D:1}   via D (9.09e-02, rho=2.76e-01 k*=10)
    - 5.52e-03 -> mono {X:1}   via X (5.52e-03, rho=1.77e-02 k*=10)
    - 2.48e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.48e-04, rho=6.75e-02 k*=10)
    - 2.47e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.47e-04, rho=6.75e-02 k*=10)
    - 1.70e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.70e-04, rho=1.87e-01 k*=10)
    - 1.17e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.17e-04, rho=1.33e-01 k*=10)
- mono {THEM(ME):1}
    - 1.76e-01 -> mono {C:1}   via C (1.76e-01, rho=5.34e-01 k*=10)
    - 9.23e-02 -> mono {X:1}   via X (9.23e-02, rho=2.95e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 3.16e-03 -> mono {or(X,X):1}   via or(X,X) (3.16e-03, rho=4.19e-01 k*=10)
    - 1.38e-03 -> mono {and(X,X):1}   via and(X,X) (1.38e-03, rho=1.83e-01 k*=10)
    - 4.86e-04 -> mono {THEM(^C):1}   via THEM(^C) (4.86e-04, rho=5.34e-01 k*=10)
- mono {THEM(THEM):1}
    - 1.76e-01 -> mono {C:1}   via C (1.76e-01, rho=5.34e-01 k*=10)
    - 9.23e-02 -> mono {X:1}   via X (9.23e-02, rho=2.95e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 3.16e-03 -> mono {or(X,X):1}   via or(X,X) (3.16e-03, rho=4.19e-01 k*=10)
    - 1.38e-03 -> mono {and(X,X):1}   via and(X,X) (1.38e-03, rho=1.83e-01 k*=10)
    - 4.86e-04 -> mono {THEM(^C):1}   via THEM(^C) (4.86e-04, rho=5.34e-01 k*=10)
- mono {THEM(^X):1}
    - 9.72e-02 -> mono {C:1}   via C (9.72e-02, rho=2.95e-01 k*=10)
    - 3.12e-02 -> mono {X:1}   via X (3.12e-02, rho=1.00e-01 k*=10)
    - 7.21e-03 -> mono {D:1}   via D (7.21e-03, rho=2.19e-02 k*=10)
    - 1.38e-03 -> mono {or(X,X):1}   via or(X,X) (1.38e-03, rho=1.83e-01 k*=10)
    - 4.17e-04 -> mono {THEM(^D):1}   via THEM(^D) (4.17e-04, rho=4.58e-01 k*=10)
    - 3.68e-04 -> mono {and(X,X):1}   via and(X,X) (3.68e-04, rho=4.88e-02 k*=10)
