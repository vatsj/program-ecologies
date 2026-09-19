### arm=source, n=6, game=pd, N=10, w=0.01, x_on=True, role=False, mode=square

programs 2110, classes 220, states 2618, terminal classes 1, indeterminate 0, divergence rate 0.0014, flow into polymorphic targets 1.50e-05
mean payoff -0.5214, efficient 0.0000, deadweight loss 0.5214, mean bits in support 4.16

| pi | state |
|---|---|
| 0.2357 | mono {D:1} |
| 0.2232 | mono {X:1} |
| 0.2113 | mono {C:1} |
| 0.0589 | mono {not(C):1} |
| 0.0558 | mono {not(X):1} |
| 0.0528 | mono {not(D):1} |
| 0.0258 | mono {not(not(not(C))):1} |
| 0.0231 | mono {not(not(not(D))):1} |
| 0.0149 | mono {not(not(not(X))):1} |
| 0.0039 | mono {not(or(X,X)):1} |
| 0.0037 | mono {not(and(X,X)):1} |
| 0.0033 | mono {eq(THEM,ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.17e-02 -> mono {X:1}   via X (2.17e-02, rho=9.72e-02 k*=10)
    - 2.11e-02 -> mono {C:1}   via C (2.11e-02, rho=9.45e-02 k*=10)
    - 5.59e-03 -> mono {not(C):1}   via not(C) (5.59e-03, rho=1.00e-01 k*=10)
    - 5.43e-03 -> mono {not(X):1}   via not(X) (5.43e-03, rho=9.72e-02 k*=10)
    - 5.28e-03 -> mono {not(D):1}   via not(D) (5.28e-03, rho=9.45e-02 k*=10)
    - 2.44e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-03, rho=1.00e-01 k*=10)
- mono {X:1}
    - 2.30e-02 -> mono {D:1}   via D (2.30e-02, rho=1.03e-01 k*=10)
    - 2.17e-02 -> mono {C:1}   via C (2.17e-02, rho=9.73e-02 k*=10)
    - 5.74e-03 -> mono {not(C):1}   via not(C) (5.74e-03, rho=1.03e-01 k*=10)
    - 5.59e-03 -> mono {not(X):1}   via not(X) (5.59e-03, rho=1.00e-01 k*=10)
    - 5.43e-03 -> mono {not(D):1}   via not(D) (5.43e-03, rho=9.73e-02 k*=10)
    - 2.51e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.51e-03, rho=1.03e-01 k*=10)
- mono {C:1}
    - 2.36e-02 -> mono {D:1}   via D (2.36e-02, rho=1.06e-01 k*=10)
    - 2.30e-02 -> mono {X:1}   via X (2.30e-02, rho=1.03e-01 k*=10)
    - 5.90e-03 -> mono {not(C):1}   via not(C) (5.90e-03, rho=1.06e-01 k*=10)
    - 5.74e-03 -> mono {not(X):1}   via not(X) (5.74e-03, rho=1.03e-01 k*=10)
    - 5.59e-03 -> mono {not(D):1}   via not(D) (5.59e-03, rho=1.00e-01 k*=10)
    - 2.58e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.58e-03, rho=1.06e-01 k*=10)
- mono {not(C):1}
    - 2.24e-02 -> mono {D:1}   via D (2.24e-02, rho=1.00e-01 k*=10)
    - 2.17e-02 -> mono {X:1}   via X (2.17e-02, rho=9.72e-02 k*=10)
    - 2.11e-02 -> mono {C:1}   via C (2.11e-02, rho=9.45e-02 k*=10)
    - 5.43e-03 -> mono {not(X):1}   via not(X) (5.43e-03, rho=9.72e-02 k*=10)
    - 5.28e-03 -> mono {not(D):1}   via not(D) (5.28e-03, rho=9.45e-02 k*=10)
    - 2.44e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-03, rho=1.00e-01 k*=10)
- mono {not(X):1}
    - 2.30e-02 -> mono {D:1}   via D (2.30e-02, rho=1.03e-01 k*=10)
    - 2.24e-02 -> mono {X:1}   via X (2.24e-02, rho=1.00e-01 k*=10)
    - 2.17e-02 -> mono {C:1}   via C (2.17e-02, rho=9.73e-02 k*=10)
    - 5.74e-03 -> mono {not(C):1}   via not(C) (5.74e-03, rho=1.03e-01 k*=10)
    - 5.43e-03 -> mono {not(D):1}   via not(D) (5.43e-03, rho=9.73e-02 k*=10)
    - 2.51e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.51e-03, rho=1.03e-01 k*=10)
- mono {not(D):1}
    - 2.36e-02 -> mono {D:1}   via D (2.36e-02, rho=1.06e-01 k*=10)
    - 2.30e-02 -> mono {X:1}   via X (2.30e-02, rho=1.03e-01 k*=10)
    - 2.24e-02 -> mono {C:1}   via C (2.24e-02, rho=1.00e-01 k*=10)
    - 5.90e-03 -> mono {not(C):1}   via not(C) (5.90e-03, rho=1.06e-01 k*=10)
    - 5.74e-03 -> mono {not(X):1}   via not(X) (5.74e-03, rho=1.03e-01 k*=10)
    - 2.58e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.58e-03, rho=1.06e-01 k*=10)
- mono {not(not(not(C))):1}
    - 2.24e-02 -> mono {D:1}   via D (2.24e-02, rho=1.00e-01 k*=10)
    - 2.17e-02 -> mono {X:1}   via X (2.17e-02, rho=9.72e-02 k*=10)
    - 2.11e-02 -> mono {C:1}   via C (2.11e-02, rho=9.45e-02 k*=10)
    - 5.59e-03 -> mono {not(C):1}   via not(C) (5.59e-03, rho=1.00e-01 k*=10)
    - 5.43e-03 -> mono {not(X):1}   via not(X) (5.43e-03, rho=9.72e-02 k*=10)
    - 5.28e-03 -> mono {not(D):1}   via not(D) (5.28e-03, rho=9.45e-02 k*=10)
- mono {not(not(not(D))):1}
    - 2.36e-02 -> mono {D:1}   via D (2.36e-02, rho=1.06e-01 k*=10)
    - 2.30e-02 -> mono {X:1}   via X (2.30e-02, rho=1.03e-01 k*=10)
    - 2.24e-02 -> mono {C:1}   via C (2.24e-02, rho=1.00e-01 k*=10)
    - 5.90e-03 -> mono {not(C):1}   via not(C) (5.90e-03, rho=1.06e-01 k*=10)
    - 5.74e-03 -> mono {not(X):1}   via not(X) (5.74e-03, rho=1.03e-01 k*=10)
    - 5.59e-03 -> mono {not(D):1}   via not(D) (5.59e-03, rho=1.00e-01 k*=10)
- mono {not(not(not(X))):1}
    - 2.30e-02 -> mono {D:1}   via D (2.30e-02, rho=1.03e-01 k*=10)
    - 2.24e-02 -> mono {X:1}   via X (2.24e-02, rho=1.00e-01 k*=10)
    - 2.17e-02 -> mono {C:1}   via C (2.17e-02, rho=9.73e-02 k*=10)
    - 5.74e-03 -> mono {not(C):1}   via not(C) (5.74e-03, rho=1.03e-01 k*=10)
    - 5.59e-03 -> mono {not(X):1}   via not(X) (5.59e-03, rho=1.00e-01 k*=10)
    - 5.43e-03 -> mono {not(D):1}   via not(D) (5.43e-03, rho=9.73e-02 k*=10)
- mono {not(or(X,X)):1}
    - 2.27e-02 -> mono {D:1}   via D (2.27e-02, rho=1.01e-01 k*=10)
    - 2.20e-02 -> mono {X:1}   via X (2.20e-02, rho=9.86e-02 k*=10)
    - 2.14e-02 -> mono {C:1}   via C (2.14e-02, rho=9.59e-02 k*=10)
    - 5.67e-03 -> mono {not(C):1}   via not(C) (5.67e-03, rho=1.01e-01 k*=10)
    - 5.51e-03 -> mono {not(X):1}   via not(X) (5.51e-03, rho=9.86e-02 k*=10)
    - 5.36e-03 -> mono {not(D):1}   via not(D) (5.36e-03, rho=9.59e-02 k*=10)
- mono {not(and(X,X)):1}
    - 2.33e-02 -> mono {D:1}   via D (2.33e-02, rho=1.04e-01 k*=10)
    - 2.27e-02 -> mono {X:1}   via X (2.27e-02, rho=1.01e-01 k*=10)
    - 2.20e-02 -> mono {C:1}   via C (2.20e-02, rho=9.86e-02 k*=10)
    - 5.82e-03 -> mono {not(C):1}   via not(C) (5.82e-03, rho=1.04e-01 k*=10)
    - 5.67e-03 -> mono {not(X):1}   via not(X) (5.67e-03, rho=1.01e-01 k*=10)
    - 5.51e-03 -> mono {not(D):1}   via not(D) (5.51e-03, rho=9.86e-02 k*=10)
- mono {eq(THEM,ME):1}
    - 2.18e-02 -> mono {D:1}   via D (2.18e-02, rho=9.73e-02 k*=10)
    - 2.12e-02 -> mono {X:1}   via X (2.12e-02, rho=9.47e-02 k*=10)
    - 2.06e-02 -> mono {C:1}   via C (2.06e-02, rho=9.20e-02 k*=10)
    - 5.44e-03 -> mono {not(C):1}   via not(C) (5.44e-03, rho=9.73e-02 k*=10)
    - 5.29e-03 -> mono {not(X):1}   via not(X) (5.29e-03, rho=9.47e-02 k*=10)
    - 5.14e-03 -> mono {not(D):1}   via not(D) (5.14e-03, rho=9.20e-02 k*=10)
