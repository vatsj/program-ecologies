### arm=strong, n=7, game=pd, N=10, w=0.01, x_on=True, role=False, mode=sparse

programs 8770, classes 44, states 353, terminal classes 1, indeterminate 0, divergence rate 0.0058, flow into polymorphic targets 1.61e-06
mean payoff -0.5210, efficient 0.0000, deadweight loss 0.5210, mean bits in support 2.75

| pi | state |
|---|---|
| 0.3500 | mono {D:1} |
| 0.3135 | mono {C:1} |
| 0.3121 | mono {X:1} |
| 0.0088 | mono {and(X,X):1} |
| 0.0083 | mono {or(X,X):1} |
| 0.0038 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.13e-02 -> mono {C:1}   via C (3.13e-02, rho=9.45e-02 k*=10)
    - 3.04e-02 -> mono {X:1}   via X (3.04e-02, rho=9.72e-02 k*=10)
    - 8.45e-04 -> mono {and(X,X):1}   via and(X,X) (8.45e-04, rho=9.86e-02 k*=10)
    - 8.21e-04 -> mono {or(X,X):1}   via or(X,X) (8.21e-04, rho=9.59e-02 k*=10)
    - 3.90e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.90e-04, rho=1.00e-01 k*=10)
    - 7.97e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.97e-05, rho=9.32e-02 k*=10)
- mono {C:1}
    - 3.50e-02 -> mono {D:1}   via D (3.50e-02, rho=1.06e-01 k*=10)
    - 3.21e-02 -> mono {X:1}   via X (3.21e-02, rho=1.03e-01 k*=10)
    - 8.92e-04 -> mono {and(X,X):1}   via and(X,X) (8.92e-04, rho=1.04e-01 k*=10)
    - 8.68e-04 -> mono {or(X,X):1}   via or(X,X) (8.68e-04, rho=1.01e-01 k*=10)
    - 3.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-04, rho=9.87e-02 k*=10)
    - 9.03e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (9.03e-05, rho=1.06e-01 k*=10)
- mono {X:1}
    - 3.41e-02 -> mono {D:1}   via D (3.41e-02, rho=1.03e-01 k*=10)
    - 3.22e-02 -> mono {C:1}   via C (3.22e-02, rho=9.73e-02 k*=10)
    - 8.68e-04 -> mono {and(X,X):1}   via and(X,X) (8.68e-04, rho=1.01e-01 k*=10)
    - 8.45e-04 -> mono {or(X,X):1}   via or(X,X) (8.45e-04, rho=9.86e-02 k*=10)
    - 3.87e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.87e-04, rho=9.93e-02 k*=10)
    - 8.50e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.50e-05, rho=9.93e-02 k*=10)
- mono {and(X,X):1}
    - 3.36e-02 -> mono {D:1}   via D (3.36e-02, rho=1.01e-01 k*=10)
    - 3.18e-02 -> mono {C:1}   via C (3.18e-02, rho=9.59e-02 k*=10)
    - 3.08e-02 -> mono {X:1}   via X (3.08e-02, rho=9.86e-02 k*=10)
    - 8.33e-04 -> mono {or(X,X):1}   via or(X,X) (8.33e-04, rho=9.73e-02 k*=10)
    - 3.88e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.88e-04, rho=9.97e-02 k*=10)
    - 8.23e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.23e-05, rho=9.63e-02 k*=10)
- mono {or(X,X):1}
    - 3.45e-02 -> mono {D:1}   via D (3.45e-02, rho=1.04e-01 k*=10)
    - 3.27e-02 -> mono {C:1}   via C (3.27e-02, rho=9.86e-02 k*=10)
    - 3.17e-02 -> mono {X:1}   via X (3.17e-02, rho=1.01e-01 k*=10)
    - 8.80e-04 -> mono {and(X,X):1}   via and(X,X) (8.80e-04, rho=1.03e-01 k*=10)
    - 3.86e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.86e-04, rho=9.90e-02 k*=10)
    - 8.76e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.76e-05, rho=1.02e-01 k*=10)
- mono {THEM(ME):1}
    - 3.40e-02 -> mono {C:1}   via C (3.40e-02, rho=1.03e-01 k*=10)
    - 3.31e-02 -> mono {D:1}   via D (3.31e-02, rho=1.00e-01 k*=10)
    - 3.17e-02 -> mono {X:1}   via X (3.17e-02, rho=1.01e-01 k*=10)
    - 8.74e-04 -> mono {or(X,X):1}   via or(X,X) (8.74e-04, rho=1.02e-01 k*=10)
    - 8.62e-04 -> mono {and(X,X):1}   via and(X,X) (8.62e-04, rho=1.01e-01 k*=10)
    - 8.55e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.55e-05, rho=1.00e-01 k*=10)
