### arm=weak, n=6, game=pd, N=10, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 48, states 120, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 8.76e-07
mean payoff -0.8867, efficient 0.0000, deadweight loss 0.8867, mean bits in support 2.73

| pi | state |
|---|---|
| 0.7974 | mono {D:1} |
| 0.1500 | mono {X:1} |
| 0.0323 | mono {C:1} |
| 0.0081 | mono {and(X,X):1} |
| 0.0024 | mono {THEM(ME):1} |
| 0.0023 | mono {THEM(THEM):1} |
| 0.0018 | mono {THEM(^C):1} |
| 0.0016 | mono {or(X,X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.20e-02 -> mono {X:1}   via X (1.20e-02, rho=3.83e-02 k*=10)
    - 3.82e-03 -> mono {C:1}   via C (3.82e-03, rho=1.16e-02 k*=10)
    - 4.82e-04 -> mono {and(X,X):1}   via and(X,X) (4.82e-04, rho=6.40e-02 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
    - 1.63e-04 -> mono {or(X,X):1}   via or(X,X) (1.63e-04, rho=2.16e-02 k*=10)
- mono {X:1}
    - 6.56e-02 -> mono {D:1}   via D (6.56e-02, rho=1.99e-01 k*=10)
    - 1.26e-02 -> mono {C:1}   via C (1.26e-02, rho=3.83e-02 k*=10)
    - 1.10e-03 -> mono {and(X,X):1}   via and(X,X) (1.10e-03, rho=1.46e-01 k*=10)
    - 4.82e-04 -> mono {or(X,X):1}   via or(X,X) (4.82e-04, rho=6.40e-02 k*=10)
    - 2.95e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.95e-04, rho=8.02e-02 k*=10)
    - 2.94e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.94e-04, rho=8.02e-02 k*=10)
- mono {C:1}
    - 1.04e-01 -> mono {D:1}   via D (1.04e-01, rho=3.15e-01 k*=10)
    - 6.23e-02 -> mono {X:1}   via X (6.23e-02, rho=1.99e-01 k*=10)
    - 1.94e-03 -> mono {and(X,X):1}   via and(X,X) (1.94e-03, rho=2.57e-01 k*=10)
    - 1.10e-03 -> mono {or(X,X):1}   via or(X,X) (1.10e-03, rho=1.46e-01 k*=10)
    - 2.51e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (2.51e-04, rho=3.15e-01 k*=10)
    - 2.51e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (2.51e-04, rho=3.15e-01 k*=10)
- mono {and(X,X):1}
    - 4.80e-02 -> mono {D:1}   via D (4.80e-02, rho=1.46e-01 k*=10)
    - 2.00e-02 -> mono {X:1}   via X (2.00e-02, rho=6.40e-02 k*=10)
    - 7.11e-03 -> mono {C:1}   via C (7.11e-03, rho=2.16e-02 k*=10)
    - 3.31e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.31e-04, rho=9.00e-02 k*=10)
    - 3.30e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.30e-04, rho=9.00e-02 k*=10)
    - 2.89e-04 -> mono {or(X,X):1}   via or(X,X) (2.89e-04, rho=3.83e-02 k*=10)
- mono {THEM(ME):1}
    - 6.71e-02 -> mono {C:1}   via C (6.71e-02, rho=2.04e-01 k*=10)
    - 4.56e-02 -> mono {X:1}   via X (4.56e-02, rho=1.46e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 1.31e-03 -> mono {or(X,X):1}   via or(X,X) (1.31e-03, rho=1.74e-01 k*=10)
    - 9.16e-04 -> mono {and(X,X):1}   via and(X,X) (9.16e-04, rho=1.22e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
- mono {THEM(THEM):1}
    - 6.71e-02 -> mono {C:1}   via C (6.71e-02, rho=2.04e-01 k*=10)
    - 4.56e-02 -> mono {X:1}   via X (4.56e-02, rho=1.46e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 1.31e-03 -> mono {or(X,X):1}   via or(X,X) (1.31e-03, rho=1.74e-01 k*=10)
    - 9.16e-04 -> mono {and(X,X):1}   via and(X,X) (9.16e-04, rho=1.22e-01 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=1.00e-01 k*=10)
- mono {THEM(^C):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 2.05e-02 -> mono {X:1}   via X (2.05e-02, rho=6.58e-02 k*=10)
    - 1.38e-02 -> mono {D:1}   via D (1.38e-02, rho=4.18e-02 k*=10)
    - 6.14e-04 -> mono {or(X,X):1}   via or(X,X) (6.14e-04, rho=8.15e-02 k*=10)
    - 3.97e-04 -> mono {and(X,X):1}   via and(X,X) (3.97e-04, rho=5.26e-02 k*=10)
    - 2.87e-04 -> mono {THEM(^D):1}   via THEM(^D) (2.87e-04, rho=3.15e-01 k*=10)
- mono {or(X,X):1}
    - 8.45e-02 -> mono {D:1}   via D (8.45e-02, rho=2.57e-01 k*=10)
    - 4.56e-02 -> mono {X:1}   via X (4.56e-02, rho=1.46e-01 k*=10)
    - 2.10e-02 -> mono {C:1}   via C (2.10e-02, rho=6.40e-02 k*=10)
    - 1.50e-03 -> mono {and(X,X):1}   via and(X,X) (1.50e-03, rho=1.99e-01 k*=10)
    - 2.60e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.60e-04, rho=7.06e-02 k*=10)
    - 2.59e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.59e-04, rho=7.06e-02 k*=10)
