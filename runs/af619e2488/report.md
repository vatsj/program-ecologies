### arm=strong, n=6, game=pd, N=10, w=0.01, x_on=True, role=False, mode=square

programs 1726, classes 21, states 25, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 2.67e-07
mean payoff -0.5209, efficient 0.0000, deadweight loss 0.5209, mean bits in support 2.73

| pi | state |
|---|---|
| 0.3500 | mono {D:1} |
| 0.3140 | mono {X:1} |
| 0.3135 | mono {C:1} |
| 0.0082 | mono {and(X,X):1} |
| 0.0078 | mono {or(X,X):1} |
| 0.0038 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.13e-02 -> mono {C:1}   via C (3.13e-02, rho=9.45e-02 k*=10)
    - 3.06e-02 -> mono {X:1}   via X (3.06e-02, rho=9.72e-02 k*=10)
    - 7.87e-04 -> mono {and(X,X):1}   via and(X,X) (7.87e-04, rho=9.86e-02 k*=10)
    - 7.65e-04 -> mono {or(X,X):1}   via or(X,X) (7.65e-04, rho=9.59e-02 k*=10)
    - 3.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-04, rho=1.00e-01 k*=10)
    - 7.94e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.94e-05, rho=9.32e-02 k*=10)
- mono {X:1}
    - 3.41e-02 -> mono {D:1}   via D (3.41e-02, rho=1.03e-01 k*=10)
    - 3.22e-02 -> mono {C:1}   via C (3.22e-02, rho=9.73e-02 k*=10)
    - 8.09e-04 -> mono {and(X,X):1}   via and(X,X) (8.09e-04, rho=1.01e-01 k*=10)
    - 7.87e-04 -> mono {or(X,X):1}   via or(X,X) (7.87e-04, rho=9.86e-02 k*=10)
    - 3.81e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.81e-04, rho=9.93e-02 k*=10)
    - 8.46e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.46e-05, rho=9.93e-02 k*=10)
- mono {C:1}
    - 3.50e-02 -> mono {D:1}   via D (3.50e-02, rho=1.06e-01 k*=10)
    - 3.23e-02 -> mono {X:1}   via X (3.23e-02, rho=1.03e-01 k*=10)
    - 8.31e-04 -> mono {and(X,X):1}   via and(X,X) (8.31e-04, rho=1.04e-01 k*=10)
    - 8.09e-04 -> mono {or(X,X):1}   via or(X,X) (8.09e-04, rho=1.01e-01 k*=10)
    - 3.79e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.79e-04, rho=9.87e-02 k*=10)
    - 8.99e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.99e-05, rho=1.06e-01 k*=10)
- mono {and(X,X):1}
    - 3.36e-02 -> mono {D:1}   via D (3.36e-02, rho=1.01e-01 k*=10)
    - 3.18e-02 -> mono {C:1}   via C (3.18e-02, rho=9.59e-02 k*=10)
    - 3.10e-02 -> mono {X:1}   via X (3.10e-02, rho=9.86e-02 k*=10)
    - 7.76e-04 -> mono {or(X,X):1}   via or(X,X) (7.76e-04, rho=9.73e-02 k*=10)
    - 3.83e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.83e-04, rho=9.97e-02 k*=10)
    - 8.20e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.20e-05, rho=9.63e-02 k*=10)
- mono {or(X,X):1}
    - 3.45e-02 -> mono {D:1}   via D (3.45e-02, rho=1.04e-01 k*=10)
    - 3.27e-02 -> mono {C:1}   via C (3.27e-02, rho=9.86e-02 k*=10)
    - 3.19e-02 -> mono {X:1}   via X (3.19e-02, rho=1.01e-01 k*=10)
    - 8.20e-04 -> mono {and(X,X):1}   via and(X,X) (8.20e-04, rho=1.03e-01 k*=10)
    - 3.80e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.80e-04, rho=9.90e-02 k*=10)
    - 8.72e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.72e-05, rho=1.02e-01 k*=10)
- mono {THEM(ME):1}
    - 3.41e-02 -> mono {C:1}   via C (3.41e-02, rho=1.03e-01 k*=10)
    - 3.32e-02 -> mono {D:1}   via D (3.32e-02, rho=1.00e-01 k*=10)
    - 3.19e-02 -> mono {X:1}   via X (3.19e-02, rho=1.01e-01 k*=10)
    - 8.14e-04 -> mono {or(X,X):1}   via or(X,X) (8.14e-04, rho=1.02e-01 k*=10)
    - 8.03e-04 -> mono {and(X,X):1}   via and(X,X) (8.03e-04, rho=1.01e-01 k*=10)
    - 8.51e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.51e-05, rho=1.00e-01 k*=10)
