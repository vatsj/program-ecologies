### arm=weak, n=6, game=exchange, N=10, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 46, states 359, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 1.06e-04
mean payoff 0.6232, efficient 2.0000, deadweight loss 1.3768, mean bits in support 2.77

| pi | state |
|---|---|
| 0.5316 | mono {Keep:1} |
| 0.2790 | mono {X:1} |
| 0.1630 | mono {Give:1} |
| 0.0091 | mono {and(X,X):1} |
| 0.0050 | mono {or(X,X):1} |
| 0.0026 | mono {THEM(ME):1} |
| 0.0026 | mono {THEM(THEM):1} |
| 0.0014 | mono {THEM(^Give):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Keep:1}
    - 2.27e-02 -> mono {X:1}   via X (2.27e-02, rho=7.27e-02 k*=10)
    - 1.68e-02 -> mono {Give:1}   via Give (1.68e-02, rho=5.11e-02 k*=10)
    - 6.46e-04 -> mono {and(X,X):1}   via and(X,X) (6.46e-04, rho=8.57e-02 k*=10)
    - 4.62e-04 -> mono {or(X,X):1}   via or(X,X) (4.62e-04, rho=6.12e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {X:1}
    - 4.36e-02 -> mono {Keep:1}   via Keep (4.36e-02, rho=1.33e-01 k*=10)
    - 2.39e-02 -> mono {Give:1}   via Give (2.39e-02, rho=7.27e-02 k*=10)
    - 8.72e-04 -> mono {and(X,X):1}   via and(X,X) (8.72e-04, rho=1.16e-01 k*=10)
    - 6.46e-04 -> mono {or(X,X):1}   via or(X,X) (6.46e-04, rho=8.57e-02 k*=10)
    - 3.20e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.20e-04, rho=8.67e-02 k*=10)
    - 3.18e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.18e-04, rho=8.67e-02 k*=10)
- mono {Give:1}
    - 5.58e-02 -> mono {Keep:1}   via Keep (5.58e-02, rho=1.70e-01 k*=10)
    - 4.14e-02 -> mono {X:1}   via X (4.14e-02, rho=1.33e-01 k*=10)
    - 1.14e-03 -> mono {and(X,X):1}   via and(X,X) (1.14e-03, rho=1.51e-01 k*=10)
    - 8.72e-04 -> mono {or(X,X):1}   via or(X,X) (8.72e-04, rho=1.16e-01 k*=10)
    - 2.72e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.72e-04, rho=7.37e-02 k*=10)
    - 2.70e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.70e-04, rho=7.37e-02 k*=10)
- mono {and(X,X):1}
    - 3.80e-02 -> mono {Keep:1}   via Keep (3.80e-02, rho=1.16e-01 k*=10)
    - 2.68e-02 -> mono {X:1}   via X (2.68e-02, rho=8.57e-02 k*=10)
    - 2.01e-02 -> mono {Give:1}   via Give (2.01e-02, rho=6.12e-02 k*=10)
    - 5.49e-04 -> mono {or(X,X):1}   via or(X,X) (5.49e-04, rho=7.27e-02 k*=10)
    - 3.45e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.45e-04, rho=9.33e-02 k*=10)
    - 3.42e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.42e-04, rho=9.33e-02 k*=10)
- mono {or(X,X):1}
    - 4.95e-02 -> mono {Keep:1}   via Keep (4.95e-02, rho=1.51e-01 k*=10)
    - 3.61e-02 -> mono {X:1}   via X (3.61e-02, rho=1.16e-01 k*=10)
    - 2.82e-02 -> mono {Give:1}   via Give (2.82e-02, rho=8.57e-02 k*=10)
    - 1.00e-03 -> mono {and(X,X):1}   via and(X,X) (1.00e-03, rho=1.33e-01 k*=10)
    - 2.96e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.96e-04, rho=8.02e-02 k*=10)
    - 2.94e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.94e-04, rho=8.02e-02 k*=10)
- mono {THEM(ME):1}
    - 5.40e-02 -> mono {Give:1}   via Give (5.40e-02, rho=1.64e-01 k*=10)
    - 4.04e-02 -> mono {X:1}   via X (4.04e-02, rho=1.29e-01 k*=10)
    - 3.29e-02 -> mono {Keep:1}   via Keep (3.29e-02, rho=1.00e-01 k*=10)
    - 1.10e-03 -> mono {or(X,X):1}   via or(X,X) (1.10e-03, rho=1.46e-01 k*=10)
    - 8.60e-04 -> mono {and(X,X):1}   via and(X,X) (8.60e-04, rho=1.14e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 5.40e-02 -> mono {Give:1}   via Give (5.40e-02, rho=1.64e-01 k*=10)
    - 4.04e-02 -> mono {X:1}   via X (4.04e-02, rho=1.29e-01 k*=10)
    - 3.29e-02 -> mono {Keep:1}   via Keep (3.29e-02, rho=1.00e-01 k*=10)
    - 1.10e-03 -> mono {or(X,X):1}   via or(X,X) (1.10e-03, rho=1.46e-01 k*=10)
    - 8.60e-04 -> mono {and(X,X):1}   via and(X,X) (8.60e-04, rho=1.14e-01 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
- mono {THEM(^Give):1}
    - 3.29e-02 -> mono {Give:1}   via Give (3.29e-02, rho=1.00e-01 k*=10)
    - 2.37e-02 -> mono {X:1}   via X (2.37e-02, rho=7.59e-02 k*=10)
    - 1.87e-02 -> mono {Keep:1}   via Keep (1.87e-02, rho=5.67e-02 k*=10)
    - 6.59e-04 -> mono {or(X,X):1}   via or(X,X) (6.59e-04, rho=8.73e-02 k*=10)
    - 4.96e-04 -> mono {and(X,X):1}   via and(X,X) (4.96e-04, rho=6.58e-02 k*=10)
    - 2.72e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.72e-04, rho=7.37e-02 k*=10)
