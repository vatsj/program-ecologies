### arm=source, n=6, game=pd, N=10, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 2110, classes 220, states 1950, terminal classes 1, indeterminate 0, divergence rate 0.0014, flow into polymorphic targets 4.08e-06
mean payoff -0.6664, efficient 0.0000, deadweight loss 0.6664, mean bits in support 4.20

| pi | state |
|---|---|
| 0.3470 | mono {D:1} |
| 0.2015 | mono {X:1} |
| 0.1171 | mono {C:1} |
| 0.0866 | mono {not(C):1} |
| 0.0503 | mono {not(X):1} |
| 0.0378 | mono {not(not(not(C))):1} |
| 0.0292 | mono {not(D):1} |
| 0.0135 | mono {not(not(not(X))):1} |
| 0.0128 | mono {not(not(not(D))):1} |
| 0.0069 | mono {eq(ME,THEM):1} |
| 0.0069 | mono {eq(THEM,ME):1} |
| 0.0046 | mono {and(D,D):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.67e-02 -> mono {X:1}   via X (1.67e-02, rho=7.48e-02 k*=10)
    - 1.21e-02 -> mono {C:1}   via C (1.21e-02, rho=5.43e-02 k*=10)
    - 5.59e-03 -> mono {not(C):1}   via not(C) (5.59e-03, rho=1.00e-01 k*=10)
    - 4.18e-03 -> mono {not(X):1}   via not(X) (4.18e-03, rho=7.48e-02 k*=10)
    - 3.03e-03 -> mono {not(D):1}   via not(D) (3.03e-03, rho=5.43e-02 k*=10)
    - 2.44e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-03, rho=1.00e-01 k*=10)
- mono {X:1}
    - 2.90e-02 -> mono {D:1}   via D (2.90e-02, rho=1.30e-01 k*=10)
    - 1.67e-02 -> mono {C:1}   via C (1.67e-02, rho=7.48e-02 k*=10)
    - 7.24e-03 -> mono {not(C):1}   via not(C) (7.24e-03, rho=1.30e-01 k*=10)
    - 5.59e-03 -> mono {not(X):1}   via not(X) (5.59e-03, rho=1.00e-01 k*=10)
    - 4.18e-03 -> mono {not(D):1}   via not(D) (4.18e-03, rho=7.48e-02 k*=10)
    - 3.17e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.17e-03, rho=1.30e-01 k*=10)
- mono {C:1}
    - 3.65e-02 -> mono {D:1}   via D (3.65e-02, rho=1.63e-01 k*=10)
    - 2.90e-02 -> mono {X:1}   via X (2.90e-02, rho=1.30e-01 k*=10)
    - 9.11e-03 -> mono {not(C):1}   via not(C) (9.11e-03, rho=1.63e-01 k*=10)
    - 7.24e-03 -> mono {not(X):1}   via not(X) (7.24e-03, rho=1.30e-01 k*=10)
    - 5.59e-03 -> mono {not(D):1}   via not(D) (5.59e-03, rho=1.00e-01 k*=10)
    - 3.98e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.98e-03, rho=1.63e-01 k*=10)
- mono {not(C):1}
    - 2.24e-02 -> mono {D:1}   via D (2.24e-02, rho=1.00e-01 k*=10)
    - 1.67e-02 -> mono {X:1}   via X (1.67e-02, rho=7.48e-02 k*=10)
    - 1.21e-02 -> mono {C:1}   via C (1.21e-02, rho=5.43e-02 k*=10)
    - 4.18e-03 -> mono {not(X):1}   via not(X) (4.18e-03, rho=7.48e-02 k*=10)
    - 3.03e-03 -> mono {not(D):1}   via not(D) (3.03e-03, rho=5.43e-02 k*=10)
    - 2.44e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-03, rho=1.00e-01 k*=10)
- mono {not(X):1}
    - 2.90e-02 -> mono {D:1}   via D (2.90e-02, rho=1.30e-01 k*=10)
    - 2.24e-02 -> mono {X:1}   via X (2.24e-02, rho=1.00e-01 k*=10)
    - 1.67e-02 -> mono {C:1}   via C (1.67e-02, rho=7.48e-02 k*=10)
    - 7.24e-03 -> mono {not(C):1}   via not(C) (7.24e-03, rho=1.30e-01 k*=10)
    - 4.18e-03 -> mono {not(D):1}   via not(D) (4.18e-03, rho=7.48e-02 k*=10)
    - 3.17e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.17e-03, rho=1.30e-01 k*=10)
- mono {not(not(not(C))):1}
    - 2.24e-02 -> mono {D:1}   via D (2.24e-02, rho=1.00e-01 k*=10)
    - 1.67e-02 -> mono {X:1}   via X (1.67e-02, rho=7.48e-02 k*=10)
    - 1.21e-02 -> mono {C:1}   via C (1.21e-02, rho=5.43e-02 k*=10)
    - 5.59e-03 -> mono {not(C):1}   via not(C) (5.59e-03, rho=1.00e-01 k*=10)
    - 4.18e-03 -> mono {not(X):1}   via not(X) (4.18e-03, rho=7.48e-02 k*=10)
    - 3.03e-03 -> mono {not(D):1}   via not(D) (3.03e-03, rho=5.43e-02 k*=10)
- mono {not(D):1}
    - 3.65e-02 -> mono {D:1}   via D (3.65e-02, rho=1.63e-01 k*=10)
    - 2.90e-02 -> mono {X:1}   via X (2.90e-02, rho=1.30e-01 k*=10)
    - 2.24e-02 -> mono {C:1}   via C (2.24e-02, rho=1.00e-01 k*=10)
    - 9.11e-03 -> mono {not(C):1}   via not(C) (9.11e-03, rho=1.63e-01 k*=10)
    - 7.24e-03 -> mono {not(X):1}   via not(X) (7.24e-03, rho=1.30e-01 k*=10)
    - 3.98e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.98e-03, rho=1.63e-01 k*=10)
- mono {not(not(not(X))):1}
    - 2.90e-02 -> mono {D:1}   via D (2.90e-02, rho=1.30e-01 k*=10)
    - 2.24e-02 -> mono {X:1}   via X (2.24e-02, rho=1.00e-01 k*=10)
    - 1.67e-02 -> mono {C:1}   via C (1.67e-02, rho=7.48e-02 k*=10)
    - 7.24e-03 -> mono {not(C):1}   via not(C) (7.24e-03, rho=1.30e-01 k*=10)
    - 5.59e-03 -> mono {not(X):1}   via not(X) (5.59e-03, rho=1.00e-01 k*=10)
    - 4.18e-03 -> mono {not(D):1}   via not(D) (4.18e-03, rho=7.48e-02 k*=10)
- mono {not(not(not(D))):1}
    - 3.65e-02 -> mono {D:1}   via D (3.65e-02, rho=1.63e-01 k*=10)
    - 2.90e-02 -> mono {X:1}   via X (2.90e-02, rho=1.30e-01 k*=10)
    - 2.24e-02 -> mono {C:1}   via C (2.24e-02, rho=1.00e-01 k*=10)
    - 9.11e-03 -> mono {not(C):1}   via not(C) (9.11e-03, rho=1.63e-01 k*=10)
    - 7.24e-03 -> mono {not(X):1}   via not(X) (7.24e-03, rho=1.30e-01 k*=10)
    - 5.59e-03 -> mono {not(D):1}   via not(D) (5.59e-03, rho=1.00e-01 k*=10)
- mono {eq(ME,THEM):1}
    - 1.70e-02 -> mono {D:1}   via D (1.70e-02, rho=7.59e-02 k*=10)
    - 1.24e-02 -> mono {X:1}   via X (1.24e-02, rho=5.56e-02 k*=10)
    - 8.86e-03 -> mono {C:1}   via C (8.86e-03, rho=3.96e-02 k*=10)
    - 4.24e-03 -> mono {not(C):1}   via not(C) (4.24e-03, rho=7.59e-02 k*=10)
    - 3.11e-03 -> mono {not(X):1}   via not(X) (3.11e-03, rho=5.56e-02 k*=10)
    - 2.21e-03 -> mono {not(D):1}   via not(D) (2.21e-03, rho=3.96e-02 k*=10)
- mono {eq(THEM,ME):1}
    - 1.70e-02 -> mono {D:1}   via D (1.70e-02, rho=7.59e-02 k*=10)
    - 1.24e-02 -> mono {X:1}   via X (1.24e-02, rho=5.56e-02 k*=10)
    - 8.86e-03 -> mono {C:1}   via C (8.86e-03, rho=3.96e-02 k*=10)
    - 4.24e-03 -> mono {not(C):1}   via not(C) (4.24e-03, rho=7.59e-02 k*=10)
    - 3.11e-03 -> mono {not(X):1}   via not(X) (3.11e-03, rho=5.56e-02 k*=10)
    - 2.21e-03 -> mono {not(D):1}   via not(D) (2.21e-03, rho=3.96e-02 k*=10)
- mono {and(D,D):1}
    - 2.24e-02 -> mono {D:1}   via D (2.24e-02, rho=1.00e-01 k*=10)
    - 1.67e-02 -> mono {X:1}   via X (1.67e-02, rho=7.48e-02 k*=10)
    - 1.21e-02 -> mono {C:1}   via C (1.21e-02, rho=5.43e-02 k*=10)
    - 5.59e-03 -> mono {not(C):1}   via not(C) (5.59e-03, rho=1.00e-01 k*=10)
    - 4.18e-03 -> mono {not(X):1}   via not(X) (4.18e-03, rho=7.48e-02 k*=10)
    - 3.03e-03 -> mono {not(D):1}   via not(D) (3.03e-03, rho=5.43e-02 k*=10)
