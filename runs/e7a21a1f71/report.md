### arm=weak, n=6, game=exchange, N=10, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 46, states 341, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 8.04e-05
mean payoff 0.1997, efficient 2.0000, deadweight loss 1.8003, mean bits in support 2.72

| pi | state |
|---|---|
| 0.8209 | mono {Keep:1} |
| 0.1339 | mono {X:1} |
| 0.0258 | mono {Give:1} |
| 0.0078 | mono {and(X,X):1} |
| 0.0029 | mono {THEM(^Give):1} |
| 0.0016 | mono {THEM(ME):1} |
| 0.0016 | mono {THEM(THEM):1} |
| 0.0014 | mono {or(X,X):1} |
| 0.0010 | mono {THEM(^X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Keep:1}
    - 1.08e-02 -> mono {X:1}   via X (1.08e-02, rho=3.47e-02 k*=10)
    - 3.02e-03 -> mono {Give:1}   via Give (3.02e-03, rho=9.18e-03 k*=10)
    - 4.62e-04 -> mono {and(X,X):1}   via and(X,X) (4.62e-04, rho=6.12e-02 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
    - 1.57e-04 -> mono {THEM(^Give):1}   via THEM(^Give) (1.57e-04, rho=1.72e-01 k*=10)
- mono {X:1}
    - 6.90e-02 -> mono {Keep:1}   via Keep (6.90e-02, rho=2.10e-01 k*=10)
    - 1.14e-02 -> mono {Give:1}   via Give (1.14e-02, rho=3.47e-02 k*=10)
    - 1.14e-03 -> mono {and(X,X):1}   via and(X,X) (1.14e-03, rho=1.51e-01 k*=10)
    - 4.62e-04 -> mono {or(X,X):1}   via or(X,X) (4.62e-04, rho=6.12e-02 k*=10)
    - 2.27e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.27e-04, rho=6.14e-02 k*=10)
    - 2.25e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.25e-04, rho=6.14e-02 k*=10)
- mono {Give:1}
    - 1.10e-01 -> mono {Keep:1}   via Keep (1.10e-01, rho=3.36e-01 k*=10)
    - 6.55e-02 -> mono {X:1}   via X (6.55e-02, rho=2.10e-01 k*=10)
    - 2.06e-03 -> mono {and(X,X):1}   via and(X,X) (2.06e-03, rho=2.73e-01 k*=10)
    - 1.14e-03 -> mono {or(X,X):1}   via or(X,X) (1.14e-03, rho=1.51e-01 k*=10)
    - 2.67e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (2.67e-04, rho=3.36e-01 k*=10)
    - 2.67e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (2.67e-04, rho=3.36e-01 k*=10)
- mono {and(X,X):1}
    - 4.95e-02 -> mono {Keep:1}   via Keep (4.95e-02, rho=1.51e-01 k*=10)
    - 1.91e-02 -> mono {X:1}   via X (1.91e-02, rho=6.12e-02 k*=10)
    - 6.03e-03 -> mono {Give:1}   via Give (6.03e-03, rho=1.83e-02 k*=10)
    - 2.96e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.96e-04, rho=8.02e-02 k*=10)
    - 2.94e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.94e-04, rho=8.02e-02 k*=10)
    - 2.61e-04 -> mono {or(X,X):1}   via or(X,X) (2.61e-04, rho=3.47e-02 k*=10)
- mono {THEM(^Give):1}
    - 3.29e-02 -> mono {Give:1}   via Give (3.29e-02, rho=1.00e-01 k*=10)
    - 1.31e-02 -> mono {X:1}   via X (1.31e-02, rho=4.18e-02 k*=10)
    - 5.15e-03 -> mono {Keep:1}   via Keep (5.15e-03, rho=1.56e-02 k*=10)
    - 4.96e-04 -> mono {or(X,X):1}   via or(X,X) (4.96e-04, rho=6.58e-02 k*=10)
    - 3.06e-04 -> mono {THEM(^Keep):1}   via THEM(^Keep) (3.06e-04, rho=3.36e-01 k*=10)
    - 1.95e-04 -> mono {and(X,X):1}   via and(X,X) (1.95e-04, rho=2.59e-02 k*=10)
- mono {THEM(ME):1}
    - 1.13e-01 -> mono {Give:1}   via Give (1.13e-01, rho=3.45e-01 k*=10)
    - 6.37e-02 -> mono {X:1}   via X (6.37e-02, rho=2.04e-01 k*=10)
    - 3.29e-02 -> mono {Keep:1}   via Keep (3.29e-02, rho=1.00e-01 k*=10)
    - 2.05e-03 -> mono {or(X,X):1}   via or(X,X) (2.05e-03, rho=2.71e-01 k*=10)
    - 1.10e-03 -> mono {and(X,X):1}   via and(X,X) (1.10e-03, rho=1.46e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 1.13e-01 -> mono {Give:1}   via Give (1.13e-01, rho=3.45e-01 k*=10)
    - 6.37e-02 -> mono {X:1}   via X (6.37e-02, rho=2.04e-01 k*=10)
    - 3.29e-02 -> mono {Keep:1}   via Keep (3.29e-02, rho=1.00e-01 k*=10)
    - 2.05e-03 -> mono {or(X,X):1}   via or(X,X) (2.05e-03, rho=2.71e-01 k*=10)
    - 1.10e-03 -> mono {and(X,X):1}   via and(X,X) (1.10e-03, rho=1.46e-01 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
- mono {or(X,X):1}
    - 8.97e-02 -> mono {Keep:1}   via Keep (8.97e-02, rho=2.73e-01 k*=10)
    - 4.70e-02 -> mono {X:1}   via X (4.70e-02, rho=1.51e-01 k*=10)
    - 2.01e-02 -> mono {Give:1}   via Give (2.01e-02, rho=6.12e-02 k*=10)
    - 1.58e-03 -> mono {and(X,X):1}   via and(X,X) (1.58e-03, rho=2.10e-01 k*=10)
    - 1.66e-04 -> mono {THEM(ME):1}   via THEM(ME) (1.66e-04, rho=4.49e-02 k*=10)
    - 1.64e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (1.64e-04, rho=4.49e-02 k*=10)
- mono {THEM(^X):1}
    - 6.71e-02 -> mono {Give:1}   via Give (6.71e-02, rho=2.04e-01 k*=10)
    - 3.12e-02 -> mono {X:1}   via X (3.12e-02, rho=1.00e-01 k*=10)
    - 1.38e-02 -> mono {Keep:1}   via Keep (1.38e-02, rho=4.18e-02 k*=10)
    - 1.10e-03 -> mono {or(X,X):1}   via or(X,X) (1.10e-03, rho=1.46e-01 k*=10)
    - 4.96e-04 -> mono {and(X,X):1}   via and(X,X) (4.96e-04, rho=6.58e-02 k*=10)
    - 2.27e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.27e-04, rho=6.14e-02 k*=10)
