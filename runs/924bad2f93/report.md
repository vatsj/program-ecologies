### arm=weak, n=7, game=pd, N=10, w=0.3, x_on=True, role=False, mode=sparse, fmap=exp

programs 9426, classes 106, states 808, terminal classes 1, indeterminate 0, divergence rate 0.0126, flow into polymorphic targets 2.00e-06
mean payoff -0.8866, efficient 0.0000, deadweight loss 0.8866, mean bits in support 2.74

| pi | state |
|---|---|
| 0.7965 | mono {D:1} |
| 0.1491 | mono {X:1} |
| 0.0324 | mono {C:1} |
| 0.0087 | mono {and(X,X):1} |
| 0.0048 | mono {THEM(ME):1} |
| 0.0018 | mono {THEM(^C):1} |
| 0.0017 | mono {or(X,X):1} |
| 0.0010 | mono {THEM(^X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.19e-02 -> mono {X:1}   via X (1.19e-02, rho=3.83e-02 k*=10)
    - 3.82e-03 -> mono {C:1}   via C (3.82e-03, rho=1.16e-02 k*=10)
    - 7.46e-04 -> mono {THEM(ME):1}   via THEM(ME) (7.46e-04, rho=1.00e-01 k*=10)
    - 5.17e-04 -> mono {and(X,X):1}   via and(X,X) (5.17e-04, rho=6.40e-02 k*=10)
    - 1.75e-04 -> mono {or(X,X):1}   via or(X,X) (1.75e-04, rho=2.16e-02 k*=10)
    - 1.32e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.32e-04, rho=1.39e-01 k*=10)
- mono {X:1}
    - 6.55e-02 -> mono {D:1}   via D (6.55e-02, rho=1.99e-01 k*=10)
    - 1.26e-02 -> mono {C:1}   via C (1.26e-02, rho=3.83e-02 k*=10)
    - 1.18e-03 -> mono {and(X,X):1}   via and(X,X) (1.18e-03, rho=1.46e-01 k*=10)
    - 5.98e-04 -> mono {THEM(ME):1}   via THEM(ME) (5.98e-04, rho=8.02e-02 k*=10)
    - 5.17e-04 -> mono {or(X,X):1}   via or(X,X) (5.17e-04, rho=6.40e-02 k*=10)
    - 1.14e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.14e-04, rho=1.20e-01 k*=10)
- mono {C:1}
    - 1.04e-01 -> mono {D:1}   via D (1.04e-01, rho=3.15e-01 k*=10)
    - 6.19e-02 -> mono {X:1}   via X (6.19e-02, rho=1.99e-01 k*=10)
    - 2.08e-03 -> mono {and(X,X):1}   via and(X,X) (2.08e-03, rho=2.57e-01 k*=10)
    - 1.18e-03 -> mono {or(X,X):1}   via or(X,X) (1.18e-03, rho=1.46e-01 k*=10)
    - 4.58e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.58e-04, rho=6.14e-02 k*=10)
    - 2.53e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (2.53e-04, rho=3.15e-01 k*=10)
- mono {and(X,X):1}
    - 4.80e-02 -> mono {D:1}   via D (4.80e-02, rho=1.46e-01 k*=10)
    - 1.99e-02 -> mono {X:1}   via X (1.99e-02, rho=6.40e-02 k*=10)
    - 7.10e-03 -> mono {C:1}   via C (7.10e-03, rho=2.16e-02 k*=10)
    - 6.72e-04 -> mono {THEM(ME):1}   via THEM(ME) (6.72e-04, rho=9.00e-02 k*=10)
    - 3.10e-04 -> mono {or(X,X):1}   via or(X,X) (3.10e-04, rho=3.83e-02 k*=10)
    - 1.23e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.23e-04, rho=1.29e-01 k*=10)
- mono {THEM(ME):1}
    - 6.70e-02 -> mono {C:1}   via C (6.70e-02, rho=2.04e-01 k*=10)
    - 4.53e-02 -> mono {X:1}   via X (4.53e-02, rho=1.46e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 1.40e-03 -> mono {or(X,X):1}   via or(X,X) (1.40e-03, rho=1.74e-01 k*=10)
    - 9.83e-04 -> mono {and(X,X):1}   via and(X,X) (9.83e-04, rho=1.22e-01 k*=10)
    - 1.93e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.93e-04, rho=2.04e-01 k*=10)
- mono {THEM(^C):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 2.04e-02 -> mono {X:1}   via X (2.04e-02, rho=6.58e-02 k*=10)
    - 1.37e-02 -> mono {D:1}   via D (1.37e-02, rho=4.18e-02 k*=10)
    - 6.59e-04 -> mono {or(X,X):1}   via or(X,X) (6.59e-04, rho=8.15e-02 k*=10)
    - 4.58e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.58e-04, rho=6.14e-02 k*=10)
    - 4.26e-04 -> mono {and(X,X):1}   via and(X,X) (4.26e-04, rho=5.26e-02 k*=10)
- mono {or(X,X):1}
    - 8.44e-02 -> mono {D:1}   via D (8.44e-02, rho=2.57e-01 k*=10)
    - 4.53e-02 -> mono {X:1}   via X (4.53e-02, rho=1.46e-01 k*=10)
    - 2.10e-02 -> mono {C:1}   via C (2.10e-02, rho=6.40e-02 k*=10)
    - 1.61e-03 -> mono {and(X,X):1}   via and(X,X) (1.61e-03, rho=1.99e-01 k*=10)
    - 5.27e-04 -> mono {THEM(ME):1}   via THEM(ME) (5.27e-04, rho=7.06e-02 k*=10)
    - 1.51e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.51e-04, rho=1.88e-01 k*=10)
- mono {THEM(^X):1}
    - 4.80e-02 -> mono {C:1}   via C (4.80e-02, rho=1.46e-01 k*=10)
    - 3.10e-02 -> mono {X:1}   via X (3.10e-02, rho=1.00e-01 k*=10)
    - 2.16e-02 -> mono {D:1}   via D (2.16e-02, rho=6.58e-02 k*=10)
    - 9.83e-04 -> mono {or(X,X):1}   via or(X,X) (9.83e-04, rho=1.22e-01 k*=10)
    - 6.59e-04 -> mono {and(X,X):1}   via and(X,X) (6.59e-04, rho=8.15e-02 k*=10)
    - 5.98e-04 -> mono {THEM(ME):1}   via THEM(ME) (5.98e-04, rho=8.02e-02 k*=10)
