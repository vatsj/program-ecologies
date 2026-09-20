### arm=weak, n=7, game=pd, N=10, w=1.0, x_on=True, role=False, mode=sparse, fmap=exp

programs 9426, classes 106, states 711, terminal classes 1, indeterminate 0, divergence rate 0.0115, flow into polymorphic targets 1.41e-06
mean payoff -0.9884, efficient 0.0000, deadweight loss 0.9884, mean bits in support 2.69

| pi | state |
|---|---|
| 0.9775 | mono {D:1} |
| 0.0077 | mono {X:1} |
| 0.0046 | mono {THEM(^C):1} |
| 0.0024 | mono {THEM(ME):1} |
| 0.0020 | mono {C:1} |
| 0.0018 | mono {and(X,X):1} |
| 0.0011 | mono {THEM(^X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 7.46e-04 -> mono {THEM(ME):1}   via THEM(ME) (7.46e-04, rho=1.00e-01 k*=10)
    - 5.81e-04 -> mono {X:1}   via X (5.81e-04, rho=1.87e-03 k*=10)
    - 1.97e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.97e-04, rho=2.08e-01 k*=10)
    - 1.47e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.47e-04, rho=1.62e-01 k*=10)
    - 1.43e-04 -> mono {and(X,X):1}   via and(X,X) (1.43e-04, rho=1.77e-02 k*=10)
    - 9.48e-05 -> mono {THEM(^D):1}   via THEM(^D) (9.48e-05, rho=1.00e-01 k*=10)
- mono {X:1}
    - 1.51e-01 -> mono {D:1}   via D (1.51e-01, rho=4.58e-01 k*=10)
    - 2.23e-03 -> mono {and(X,X):1}   via and(X,X) (2.23e-03, rho=2.76e-01 k*=10)
    - 6.16e-04 -> mono {C:1}   via C (6.16e-04, rho=1.87e-03 k*=10)
    - 2.98e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.98e-04, rho=4.00e-02 k*=10)
    - 1.53e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.53e-04, rho=1.62e-01 k*=10)
    - 1.50e-04 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.50e-04, rho=3.71e-01 k*=10)
- mono {THEM(^C):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 6.80e-03 -> mono {X:1}   via X (6.80e-03, rho=2.19e-02 k*=10)
    - 1.25e-03 -> mono {D:1}   via D (1.25e-03, rho=3.81e-03 k*=10)
    - 6.69e-04 -> mono {THEM(^D):1}   via THEM(^D) (6.69e-04, rho=7.05e-01 k*=10)
    - 4.17e-04 -> mono {THEM(^X):1}   via THEM(^X) (4.17e-04, rho=4.58e-01 k*=10)
    - 3.94e-04 -> mono {or(X,X):1}   via or(X,X) (3.94e-04, rho=4.88e-02 k*=10)
- mono {THEM(ME):1}
    - 1.76e-01 -> mono {C:1}   via C (1.76e-01, rho=5.34e-01 k*=10)
    - 9.17e-02 -> mono {X:1}   via X (9.17e-02, rho=2.95e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 3.39e-03 -> mono {or(X,X):1}   via or(X,X) (3.39e-03, rho=4.19e-01 k*=10)
    - 1.48e-03 -> mono {and(X,X):1}   via and(X,X) (1.48e-03, rho=1.83e-01 k*=10)
    - 5.07e-04 -> mono {THEM(^C):1}   via THEM(^C) (5.07e-04, rho=5.34e-01 k*=10)
- mono {C:1}
    - 2.32e-01 -> mono {D:1}   via D (2.32e-01, rho=7.05e-01 k*=10)
    - 1.42e-01 -> mono {X:1}   via X (1.42e-01, rho=4.58e-01 k*=10)
    - 4.85e-03 -> mono {and(X,X):1}   via and(X,X) (4.85e-03, rho=6.00e-01 k*=10)
    - 2.23e-03 -> mono {or(X,X):1}   via or(X,X) (2.23e-03, rho=2.76e-01 k*=10)
    - 5.66e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (5.66e-04, rho=7.05e-01 k*=10)
    - 5.64e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (5.64e-04, rho=7.05e-01 k*=10)
- mono {and(X,X):1}
    - 9.08e-02 -> mono {D:1}   via D (9.08e-02, rho=2.76e-01 k*=10)
    - 5.48e-03 -> mono {X:1}   via X (5.48e-03, rho=1.77e-02 k*=10)
    - 5.04e-04 -> mono {THEM(ME):1}   via THEM(ME) (5.04e-04, rho=6.75e-02 k*=10)
    - 1.77e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.77e-04, rho=1.87e-01 k*=10)
    - 1.21e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.21e-04, rho=1.33e-01 k*=10)
    - 8.71e-05 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (8.71e-05, rho=2.76e-01 k*=10)
- mono {THEM(^X):1}
    - 9.71e-02 -> mono {C:1}   via C (9.71e-02, rho=2.95e-01 k*=10)
    - 3.10e-02 -> mono {X:1}   via X (3.10e-02, rho=1.00e-01 k*=10)
    - 7.20e-03 -> mono {D:1}   via D (7.20e-03, rho=2.19e-02 k*=10)
    - 1.48e-03 -> mono {or(X,X):1}   via or(X,X) (1.48e-03, rho=1.83e-01 k*=10)
    - 4.34e-04 -> mono {THEM(^D):1}   via THEM(^D) (4.34e-04, rho=4.58e-01 k*=10)
    - 3.94e-04 -> mono {and(X,X):1}   via and(X,X) (3.94e-04, rho=4.88e-02 k*=10)
