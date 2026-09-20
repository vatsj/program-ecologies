### arm=weak, n=7, game=pd, N=10, w=0.1, x_on=True, role=False, mode=sparse, fmap=exp

programs 9426, classes 106, states 846, terminal classes 1, indeterminate 0, divergence rate 0.0131, flow into polymorphic targets 3.56e-06
mean payoff -0.6756, efficient 0.0000, deadweight loss 0.6756, mean bits in support 2.79

| pi | state |
|---|---|
| 0.5147 | mono {D:1} |
| 0.2823 | mono {X:1} |
| 0.1738 | mono {C:1} |
| 0.0097 | mono {and(X,X):1} |
| 0.0062 | mono {THEM(ME):1} |
| 0.0056 | mono {or(X,X):1} |
| 0.0012 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.32e-02 -> mono {X:1}   via X (2.32e-02, rho=7.48e-02 k*=10)
    - 1.78e-02 -> mono {C:1}   via C (1.78e-02, rho=5.43e-02 k*=10)
    - 7.46e-04 -> mono {THEM(ME):1}   via THEM(ME) (7.46e-04, rho=1.00e-01 k*=10)
    - 7.02e-04 -> mono {and(X,X):1}   via and(X,X) (7.02e-04, rho=8.68e-02 k*=10)
    - 5.17e-04 -> mono {or(X,X):1}   via or(X,X) (5.17e-04, rho=6.40e-02 k*=10)
    - 1.07e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.07e-04, rho=1.13e-01 k*=10)
- mono {X:1}
    - 4.26e-02 -> mono {D:1}   via D (4.26e-02, rho=1.30e-01 k*=10)
    - 2.46e-02 -> mono {C:1}   via C (2.46e-02, rho=7.48e-02 k*=10)
    - 9.24e-04 -> mono {and(X,X):1}   via and(X,X) (9.24e-04, rho=1.14e-01 k*=10)
    - 7.02e-04 -> mono {or(X,X):1}   via or(X,X) (7.02e-04, rho=8.68e-02 k*=10)
    - 6.97e-04 -> mono {THEM(ME):1}   via THEM(ME) (6.97e-04, rho=9.33e-02 k*=10)
    - 1.01e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.01e-04, rho=1.07e-01 k*=10)
- mono {C:1}
    - 5.36e-02 -> mono {D:1}   via D (5.36e-02, rho=1.63e-01 k*=10)
    - 4.02e-02 -> mono {X:1}   via X (4.02e-02, rho=1.30e-01 k*=10)
    - 1.18e-03 -> mono {and(X,X):1}   via and(X,X) (1.18e-03, rho=1.46e-01 k*=10)
    - 9.24e-04 -> mono {or(X,X):1}   via or(X,X) (9.24e-04, rho=1.14e-01 k*=10)
    - 6.47e-04 -> mono {THEM(ME):1}   via THEM(ME) (6.47e-04, rho=8.67e-02 k*=10)
    - 1.31e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.31e-04, rho=1.63e-01 k*=10)
- mono {and(X,X):1}
    - 3.76e-02 -> mono {D:1}   via D (3.76e-02, rho=1.14e-01 k*=10)
    - 2.69e-02 -> mono {X:1}   via X (2.69e-02, rho=8.68e-02 k*=10)
    - 2.10e-02 -> mono {C:1}   via C (2.10e-02, rho=6.40e-02 k*=10)
    - 7.21e-04 -> mono {THEM(ME):1}   via THEM(ME) (7.21e-04, rho=9.67e-02 k*=10)
    - 6.05e-04 -> mono {or(X,X):1}   via or(X,X) (6.05e-04, rho=7.48e-02 k*=10)
    - 1.04e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.04e-04, rho=1.10e-01 k*=10)
- mono {THEM(ME):1}
    - 4.25e-02 -> mono {C:1}   via C (4.25e-02, rho=1.29e-01 k*=10)
    - 3.54e-02 -> mono {X:1}   via X (3.54e-02, rho=1.14e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 9.83e-04 -> mono {or(X,X):1}   via or(X,X) (9.83e-04, rho=1.22e-01 k*=10)
    - 8.64e-04 -> mono {and(X,X):1}   via and(X,X) (8.64e-04, rho=1.07e-01 k*=10)
    - 1.23e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.23e-04, rho=1.29e-01 k*=10)
- mono {or(X,X):1}
    - 4.80e-02 -> mono {D:1}   via D (4.80e-02, rho=1.46e-01 k*=10)
    - 3.55e-02 -> mono {X:1}   via X (3.55e-02, rho=1.14e-01 k*=10)
    - 2.85e-02 -> mono {C:1}   via C (2.85e-02, rho=8.68e-02 k*=10)
    - 1.05e-03 -> mono {and(X,X):1}   via and(X,X) (1.05e-03, rho=1.30e-01 k*=10)
    - 6.72e-04 -> mono {THEM(ME):1}   via THEM(ME) (6.72e-04, rho=9.00e-02 k*=10)
    - 1.01e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.01e-04, rho=1.26e-01 k*=10)
- mono {THEM(^C):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 2.71e-02 -> mono {X:1}   via X (2.71e-02, rho=8.73e-02 k*=10)
    - 2.50e-02 -> mono {D:1}   via D (2.50e-02, rho=7.59e-02 k*=10)
    - 7.56e-04 -> mono {or(X,X):1}   via or(X,X) (7.56e-04, rho=9.35e-02 k*=10)
    - 6.59e-04 -> mono {and(X,X):1}   via and(X,X) (6.59e-04, rho=8.15e-02 k*=10)
    - 6.47e-04 -> mono {THEM(ME):1}   via THEM(ME) (6.47e-04, rho=8.67e-02 k*=10)
