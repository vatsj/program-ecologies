### arm=weak, n=6, game=pd, N=10, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 48, states 120, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 1.28e-06
mean payoff -0.6755, efficient 0.0000, deadweight loss 0.6755, mean bits in support 2.77

| pi | state |
|---|---|
| 0.5150 | mono {D:1} |
| 0.2841 | mono {X:1} |
| 0.1739 | mono {C:1} |
| 0.0090 | mono {and(X,X):1} |
| 0.0052 | mono {or(X,X):1} |
| 0.0031 | mono {THEM(ME):1} |
| 0.0031 | mono {THEM(THEM):1} |
| 0.0011 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.34e-02 -> mono {X:1}   via X (2.34e-02, rho=7.48e-02 k*=10)
    - 1.79e-02 -> mono {C:1}   via C (1.79e-02, rho=5.43e-02 k*=10)
    - 6.55e-04 -> mono {and(X,X):1}   via and(X,X) (6.55e-04, rho=8.68e-02 k*=10)
    - 4.82e-04 -> mono {or(X,X):1}   via or(X,X) (4.82e-04, rho=6.40e-02 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {X:1}
    - 4.26e-02 -> mono {D:1}   via D (4.26e-02, rho=1.30e-01 k*=10)
    - 2.46e-02 -> mono {C:1}   via C (2.46e-02, rho=7.48e-02 k*=10)
    - 8.62e-04 -> mono {and(X,X):1}   via and(X,X) (8.62e-04, rho=1.14e-01 k*=10)
    - 6.55e-04 -> mono {or(X,X):1}   via or(X,X) (6.55e-04, rho=8.68e-02 k*=10)
    - 3.43e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.43e-04, rho=9.33e-02 k*=10)
    - 3.42e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.42e-04, rho=9.33e-02 k*=10)
- mono {C:1}
    - 5.36e-02 -> mono {D:1}   via D (5.36e-02, rho=1.63e-01 k*=10)
    - 4.05e-02 -> mono {X:1}   via X (4.05e-02, rho=1.30e-01 k*=10)
    - 1.10e-03 -> mono {and(X,X):1}   via and(X,X) (1.10e-03, rho=1.46e-01 k*=10)
    - 8.62e-04 -> mono {or(X,X):1}   via or(X,X) (8.62e-04, rho=1.14e-01 k*=10)
    - 3.19e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.19e-04, rho=8.67e-02 k*=10)
    - 3.18e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.18e-04, rho=8.67e-02 k*=10)
- mono {and(X,X):1}
    - 3.76e-02 -> mono {D:1}   via D (3.76e-02, rho=1.14e-01 k*=10)
    - 2.71e-02 -> mono {X:1}   via X (2.71e-02, rho=8.68e-02 k*=10)
    - 2.10e-02 -> mono {C:1}   via C (2.10e-02, rho=6.40e-02 k*=10)
    - 5.64e-04 -> mono {or(X,X):1}   via or(X,X) (5.64e-04, rho=7.48e-02 k*=10)
    - 3.56e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.56e-04, rho=9.67e-02 k*=10)
    - 3.54e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.54e-04, rho=9.67e-02 k*=10)
- mono {or(X,X):1}
    - 4.80e-02 -> mono {D:1}   via D (4.80e-02, rho=1.46e-01 k*=10)
    - 3.57e-02 -> mono {X:1}   via X (3.57e-02, rho=1.14e-01 k*=10)
    - 2.86e-02 -> mono {C:1}   via C (2.86e-02, rho=8.68e-02 k*=10)
    - 9.78e-04 -> mono {and(X,X):1}   via and(X,X) (9.78e-04, rho=1.30e-01 k*=10)
    - 3.31e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.31e-04, rho=9.00e-02 k*=10)
    - 3.30e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.30e-04, rho=9.00e-02 k*=10)
- mono {THEM(ME):1}
    - 4.26e-02 -> mono {C:1}   via C (4.26e-02, rho=1.29e-01 k*=10)
    - 3.56e-02 -> mono {X:1}   via X (3.56e-02, rho=1.14e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 9.16e-04 -> mono {or(X,X):1}   via or(X,X) (9.16e-04, rho=1.22e-01 k*=10)
    - 8.06e-04 -> mono {and(X,X):1}   via and(X,X) (8.06e-04, rho=1.07e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 4.26e-02 -> mono {C:1}   via C (4.26e-02, rho=1.29e-01 k*=10)
    - 3.56e-02 -> mono {X:1}   via X (3.56e-02, rho=1.14e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 9.16e-04 -> mono {or(X,X):1}   via or(X,X) (9.16e-04, rho=1.22e-01 k*=10)
    - 8.06e-04 -> mono {and(X,X):1}   via and(X,X) (8.06e-04, rho=1.07e-01 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=1.00e-01 k*=10)
- mono {THEM(^C):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 2.73e-02 -> mono {X:1}   via X (2.73e-02, rho=8.73e-02 k*=10)
    - 2.50e-02 -> mono {D:1}   via D (2.50e-02, rho=7.59e-02 k*=10)
    - 7.05e-04 -> mono {or(X,X):1}   via or(X,X) (7.05e-04, rho=9.35e-02 k*=10)
    - 6.14e-04 -> mono {and(X,X):1}   via and(X,X) (6.14e-04, rho=8.15e-02 k*=10)
    - 3.19e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.19e-04, rho=8.67e-02 k*=10)
