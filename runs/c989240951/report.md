### arm=strong, n=7, game=pd, N=10, w=0.3, x_on=True, role=False, mode=sparse, fmap=exp

programs 8770, classes 45, states 339, terminal classes 1, indeterminate 0, divergence rate 0.0057, flow into polymorphic targets 4.55e-07
mean payoff -0.8914, efficient 0.0000, deadweight loss 0.8914, mean bits in support 2.69

| pi | state |
|---|---|
| 0.8060 | mono {D:1} |
| 0.1476 | mono {X:1} |
| 0.0308 | mono {C:1} |
| 0.0092 | mono {and(X,X):1} |
| 0.0025 | mono {THEM(ME):1} |
| 0.0018 | mono {or(X,X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.20e-02 -> mono {X:1}   via X (1.20e-02, rho=3.83e-02 k*=10)
    - 3.85e-03 -> mono {C:1}   via C (3.85e-03, rho=1.16e-02 k*=10)
    - 5.48e-04 -> mono {and(X,X):1}   via and(X,X) (5.48e-04, rho=6.40e-02 k*=10)
    - 3.90e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.90e-04, rho=1.00e-01 k*=10)
    - 1.85e-04 -> mono {or(X,X):1}   via or(X,X) (1.85e-04, rho=2.16e-02 k*=10)
    - 3.48e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (3.48e-05, rho=8.07e-02 k*=10)
- mono {X:1}
    - 6.61e-02 -> mono {D:1}   via D (6.61e-02, rho=1.99e-01 k*=10)
    - 1.27e-02 -> mono {C:1}   via C (1.27e-02, rho=3.83e-02 k*=10)
    - 1.25e-03 -> mono {and(X,X):1}   via and(X,X) (1.25e-03, rho=1.46e-01 k*=10)
    - 5.48e-04 -> mono {or(X,X):1}   via or(X,X) (5.48e-04, rho=6.40e-02 k*=10)
    - 3.12e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.12e-04, rho=8.02e-02 k*=10)
    - 7.41e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (7.41e-05, rho=1.72e-01 k*=10)
- mono {C:1}
    - 1.04e-01 -> mono {D:1}   via D (1.04e-01, rho=3.15e-01 k*=10)
    - 6.23e-02 -> mono {X:1}   via X (6.23e-02, rho=1.99e-01 k*=10)
    - 2.20e-03 -> mono {and(X,X):1}   via and(X,X) (2.20e-03, rho=2.57e-01 k*=10)
    - 1.25e-03 -> mono {or(X,X):1}   via or(X,X) (1.25e-03, rho=1.46e-01 k*=10)
    - 2.69e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (2.69e-04, rho=3.15e-01 k*=10)
    - 2.39e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.39e-04, rho=6.14e-02 k*=10)
- mono {and(X,X):1}
    - 4.84e-02 -> mono {D:1}   via D (4.84e-02, rho=1.46e-01 k*=10)
    - 2.00e-02 -> mono {X:1}   via X (2.00e-02, rho=6.40e-02 k*=10)
    - 7.17e-03 -> mono {C:1}   via C (7.17e-03, rho=2.16e-02 k*=10)
    - 3.51e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.51e-04, rho=9.00e-02 k*=10)
    - 3.28e-04 -> mono {or(X,X):1}   via or(X,X) (3.28e-04, rho=3.83e-02 k*=10)
    - 5.25e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (5.25e-05, rho=1.22e-01 k*=10)
- mono {THEM(ME):1}
    - 6.76e-02 -> mono {C:1}   via C (6.76e-02, rho=2.04e-01 k*=10)
    - 4.56e-02 -> mono {X:1}   via X (4.56e-02, rho=1.46e-01 k*=10)
    - 3.31e-02 -> mono {D:1}   via D (3.31e-02, rho=1.00e-01 k*=10)
    - 1.49e-03 -> mono {or(X,X):1}   via or(X,X) (1.49e-03, rho=1.74e-01 k*=10)
    - 1.04e-03 -> mono {and(X,X):1}   via and(X,X) (1.04e-03, rho=1.22e-01 k*=10)
    - 8.55e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.55e-05, rho=1.00e-01 k*=10)
- mono {or(X,X):1}
    - 8.51e-02 -> mono {D:1}   via D (8.51e-02, rho=2.57e-01 k*=10)
    - 4.56e-02 -> mono {X:1}   via X (4.56e-02, rho=1.46e-01 k*=10)
    - 2.12e-02 -> mono {C:1}   via C (2.12e-02, rho=6.40e-02 k*=10)
    - 1.71e-03 -> mono {and(X,X):1}   via and(X,X) (1.71e-03, rho=1.99e-01 k*=10)
    - 2.75e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.75e-04, rho=7.06e-02 k*=10)
    - 1.61e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.61e-04, rho=1.88e-01 k*=10)
