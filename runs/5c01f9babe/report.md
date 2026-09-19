### arm=strong, n=6, game=pd, N=10, w=0.1, x_on=True, role=False, mode=square

programs 1726, classes 21, states 25, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 1.82e-07
mean payoff -0.6860, efficient 0.0000, deadweight loss 0.6860, mean bits in support 2.72

| pi | state |
|---|---|
| 0.5330 | mono {D:1} |
| 0.2791 | mono {X:1} |
| 0.1676 | mono {C:1} |
| 0.0095 | mono {and(X,X):1} |
| 0.0053 | mono {or(X,X):1} |
| 0.0032 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.28e-02 -> mono {X:1}   via X (2.28e-02, rho=7.26e-02 k*=10)
    - 1.70e-02 -> mono {C:1}   via C (1.70e-02, rho=5.13e-02 k*=10)
    - 6.82e-04 -> mono {and(X,X):1}   via and(X,X) (6.82e-04, rho=8.55e-02 k*=10)
    - 4.88e-04 -> mono {or(X,X):1}   via or(X,X) (4.88e-04, rho=6.12e-02 k*=10)
    - 3.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-04, rho=1.00e-01 k*=10)
    - 3.51e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (3.51e-05, rho=4.12e-02 k*=10)
- mono {X:1}
    - 4.37e-02 -> mono {D:1}   via D (4.37e-02, rho=1.32e-01 k*=10)
    - 2.45e-02 -> mono {C:1}   via C (2.45e-02, rho=7.39e-02 k*=10)
    - 9.19e-04 -> mono {and(X,X):1}   via and(X,X) (9.19e-04, rho=1.15e-01 k*=10)
    - 6.88e-04 -> mono {or(X,X):1}   via or(X,X) (6.88e-04, rho=8.62e-02 k*=10)
    - 3.57e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.57e-04, rho=9.29e-02 k*=10)
    - 7.91e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.91e-05, rho=9.29e-02 k*=10)
- mono {C:1}
    - 5.45e-02 -> mono {D:1}   via D (5.45e-02, rho=1.64e-01 k*=10)
    - 4.08e-02 -> mono {X:1}   via X (4.08e-02, rho=1.30e-01 k*=10)
    - 1.17e-03 -> mono {and(X,X):1}   via and(X,X) (1.17e-03, rho=1.47e-01 k*=10)
    - 9.12e-04 -> mono {or(X,X):1}   via or(X,X) (9.12e-04, rho=1.14e-01 k*=10)
    - 3.31e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.31e-04, rho=8.64e-02 k*=10)
    - 1.40e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.40e-04, rho=1.64e-01 k*=10)
- mono {and(X,X):1}
    - 3.83e-02 -> mono {D:1}   via D (3.83e-02, rho=1.16e-01 k*=10)
    - 2.70e-02 -> mono {X:1}   via X (2.70e-02, rho=8.59e-02 k*=10)
    - 2.06e-02 -> mono {C:1}   via C (2.06e-02, rho=6.21e-02 k*=10)
    - 5.84e-04 -> mono {or(X,X):1}   via or(X,X) (5.84e-04, rho=7.32e-02 k*=10)
    - 3.70e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.70e-04, rho=9.64e-02 k*=10)
    - 5.44e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (5.44e-05, rho=6.39e-02 k*=10)
- mono {or(X,X):1}
    - 4.91e-02 -> mono {D:1}   via D (4.91e-02, rho=1.48e-01 k*=10)
    - 3.61e-02 -> mono {X:1}   via X (3.61e-02, rho=1.15e-01 k*=10)
    - 2.87e-02 -> mono {C:1}   via C (2.87e-02, rho=8.66e-02 k*=10)
    - 1.04e-03 -> mono {and(X,X):1}   via and(X,X) (1.04e-03, rho=1.31e-01 k*=10)
    - 3.44e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.44e-04, rho=8.96e-02 k*=10)
    - 1.08e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.08e-04, rho=1.27e-01 k*=10)
- mono {THEM(ME):1}
    - 4.33e-02 -> mono {C:1}   via C (4.33e-02, rho=1.31e-01 k*=10)
    - 3.62e-02 -> mono {X:1}   via X (3.62e-02, rho=1.15e-01 k*=10)
    - 3.32e-02 -> mono {D:1}   via D (3.32e-02, rho=1.00e-01 k*=10)
    - 9.79e-04 -> mono {or(X,X):1}   via or(X,X) (9.79e-04, rho=1.23e-01 k*=10)
    - 8.57e-04 -> mono {and(X,X):1}   via and(X,X) (8.57e-04, rho=1.07e-01 k*=10)
    - 8.51e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.51e-05, rho=1.00e-01 k*=10)
