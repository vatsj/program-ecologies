### arm=strong, n=7, game=pd, N=10, w=0.1, x_on=True, role=False, mode=sparse, fmap=exp

programs 8770, classes 45, states 348, terminal classes 1, indeterminate 0, divergence rate 0.0058, flow into polymorphic targets 1.19e-06
mean payoff -0.6765, efficient 0.0000, deadweight loss 0.6765, mean bits in support 2.74

| pi | state |
|---|---|
| 0.5200 | mono {D:1} |
| 0.2834 | mono {X:1} |
| 0.1740 | mono {C:1} |
| 0.0102 | mono {and(X,X):1} |
| 0.0059 | mono {or(X,X):1} |
| 0.0033 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.34e-02 -> mono {X:1}   via X (2.34e-02, rho=7.48e-02 k*=10)
    - 1.80e-02 -> mono {C:1}   via C (1.80e-02, rho=5.43e-02 k*=10)
    - 7.44e-04 -> mono {and(X,X):1}   via and(X,X) (7.44e-04, rho=8.68e-02 k*=10)
    - 5.48e-04 -> mono {or(X,X):1}   via or(X,X) (5.48e-04, rho=6.40e-02 k*=10)
    - 3.90e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.90e-04, rho=1.00e-01 k*=10)
    - 4.02e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (4.02e-05, rho=9.33e-02 k*=10)
- mono {X:1}
    - 4.30e-02 -> mono {D:1}   via D (4.30e-02, rho=1.30e-01 k*=10)
    - 2.48e-02 -> mono {C:1}   via C (2.48e-02, rho=7.48e-02 k*=10)
    - 9.79e-04 -> mono {and(X,X):1}   via and(X,X) (9.79e-04, rho=1.14e-01 k*=10)
    - 7.44e-04 -> mono {or(X,X):1}   via or(X,X) (7.44e-04, rho=8.68e-02 k*=10)
    - 3.64e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.64e-04, rho=9.33e-02 k*=10)
    - 7.98e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.98e-05, rho=9.33e-02 k*=10)
- mono {C:1}
    - 5.41e-02 -> mono {D:1}   via D (5.41e-02, rho=1.63e-01 k*=10)
    - 4.05e-02 -> mono {X:1}   via X (4.05e-02, rho=1.30e-01 k*=10)
    - 1.25e-03 -> mono {and(X,X):1}   via and(X,X) (1.25e-03, rho=1.46e-01 k*=10)
    - 9.79e-04 -> mono {or(X,X):1}   via or(X,X) (9.79e-04, rho=1.14e-01 k*=10)
    - 3.38e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.38e-04, rho=8.67e-02 k*=10)
    - 1.39e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.39e-04, rho=1.63e-01 k*=10)
- mono {and(X,X):1}
    - 3.79e-02 -> mono {D:1}   via D (3.79e-02, rho=1.14e-01 k*=10)
    - 2.71e-02 -> mono {X:1}   via X (2.71e-02, rho=8.68e-02 k*=10)
    - 2.12e-02 -> mono {C:1}   via C (2.12e-02, rho=6.40e-02 k*=10)
    - 6.41e-04 -> mono {or(X,X):1}   via or(X,X) (6.41e-04, rho=7.48e-02 k*=10)
    - 3.77e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.77e-04, rho=9.67e-02 k*=10)
    - 5.66e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (5.66e-05, rho=6.62e-02 k*=10)
- mono {or(X,X):1}
    - 4.84e-02 -> mono {D:1}   via D (4.84e-02, rho=1.46e-01 k*=10)
    - 3.57e-02 -> mono {X:1}   via X (3.57e-02, rho=1.14e-01 k*=10)
    - 2.88e-02 -> mono {C:1}   via C (2.88e-02, rho=8.68e-02 k*=10)
    - 1.11e-03 -> mono {and(X,X):1}   via and(X,X) (1.11e-03, rho=1.30e-01 k*=10)
    - 3.51e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.51e-04, rho=9.00e-02 k*=10)
    - 1.08e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.08e-04, rho=1.26e-01 k*=10)
- mono {THEM(ME):1}
    - 4.29e-02 -> mono {C:1}   via C (4.29e-02, rho=1.29e-01 k*=10)
    - 3.56e-02 -> mono {X:1}   via X (3.56e-02, rho=1.14e-01 k*=10)
    - 3.31e-02 -> mono {D:1}   via D (3.31e-02, rho=1.00e-01 k*=10)
    - 1.04e-03 -> mono {or(X,X):1}   via or(X,X) (1.04e-03, rho=1.22e-01 k*=10)
    - 9.15e-04 -> mono {and(X,X):1}   via and(X,X) (9.15e-04, rho=1.07e-01 k*=10)
    - 8.55e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.55e-05, rho=1.00e-01 k*=10)
