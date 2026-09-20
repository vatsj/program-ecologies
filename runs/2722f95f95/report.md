### arm=source, n=6, game=pd, N=10, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 2110, classes 220, states 1950, terminal classes 1, indeterminate 0, divergence rate 0.0014, flow into polymorphic targets 2.64e-06
mean payoff -0.8404, efficient 0.0000, deadweight loss 0.8404, mean bits in support 4.40

| pi | state |
|---|---|
| 0.5175 | mono {D:1} |
| 0.1289 | mono {not(C):1} |
| 0.1027 | mono {X:1} |
| 0.0563 | mono {not(not(not(C))):1} |
| 0.0255 | mono {not(X):1} |
| 0.0230 | mono {eq(ME,THEM):1} |
| 0.0230 | mono {eq(THEM,ME):1} |
| 0.0211 | mono {C:1} |
| 0.0069 | mono {not(not(D)):1} |
| 0.0069 | mono {and(D,X):1} |
| 0.0069 | mono {or(D,D):1} |
| 0.0069 | mono {and(D,C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 8.56e-03 -> mono {X:1}   via X (8.56e-03, rho=3.83e-02 k*=10)
    - 5.59e-03 -> mono {not(C):1}   via not(C) (5.59e-03, rho=1.00e-01 k*=10)
    - 2.60e-03 -> mono {C:1}   via C (2.60e-03, rho=1.16e-02 k*=10)
    - 2.44e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-03, rho=1.00e-01 k*=10)
    - 2.14e-03 -> mono {not(X):1}   via not(X) (2.14e-03, rho=3.83e-02 k*=10)
    - 6.49e-04 -> mono {not(D):1}   via not(D) (6.49e-04, rho=1.16e-02 k*=10)
- mono {not(C):1}
    - 2.24e-02 -> mono {D:1}   via D (2.24e-02, rho=1.00e-01 k*=10)
    - 8.56e-03 -> mono {X:1}   via X (8.56e-03, rho=3.83e-02 k*=10)
    - 2.60e-03 -> mono {C:1}   via C (2.60e-03, rho=1.16e-02 k*=10)
    - 2.44e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-03, rho=1.00e-01 k*=10)
    - 2.14e-03 -> mono {not(X):1}   via not(X) (2.14e-03, rho=3.83e-02 k*=10)
    - 6.49e-04 -> mono {not(D):1}   via not(D) (6.49e-04, rho=1.16e-02 k*=10)
- mono {X:1}
    - 4.46e-02 -> mono {D:1}   via D (4.46e-02, rho=1.99e-01 k*=10)
    - 1.11e-02 -> mono {not(C):1}   via not(C) (1.11e-02, rho=1.99e-01 k*=10)
    - 8.56e-03 -> mono {C:1}   via C (8.56e-03, rho=3.83e-02 k*=10)
    - 5.59e-03 -> mono {not(X):1}   via not(X) (5.59e-03, rho=1.00e-01 k*=10)
    - 4.87e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (4.87e-03, rho=1.99e-01 k*=10)
    - 2.14e-03 -> mono {not(D):1}   via not(D) (2.14e-03, rho=3.83e-02 k*=10)
- mono {not(not(not(C))):1}
    - 2.24e-02 -> mono {D:1}   via D (2.24e-02, rho=1.00e-01 k*=10)
    - 8.56e-03 -> mono {X:1}   via X (8.56e-03, rho=3.83e-02 k*=10)
    - 5.59e-03 -> mono {not(C):1}   via not(C) (5.59e-03, rho=1.00e-01 k*=10)
    - 2.60e-03 -> mono {C:1}   via C (2.60e-03, rho=1.16e-02 k*=10)
    - 2.14e-03 -> mono {not(X):1}   via not(X) (2.14e-03, rho=3.83e-02 k*=10)
    - 6.49e-04 -> mono {not(D):1}   via not(D) (6.49e-04, rho=1.16e-02 k*=10)
- mono {not(X):1}
    - 4.46e-02 -> mono {D:1}   via D (4.46e-02, rho=1.99e-01 k*=10)
    - 2.24e-02 -> mono {X:1}   via X (2.24e-02, rho=1.00e-01 k*=10)
    - 1.11e-02 -> mono {not(C):1}   via not(C) (1.11e-02, rho=1.99e-01 k*=10)
    - 8.56e-03 -> mono {C:1}   via C (8.56e-03, rho=3.83e-02 k*=10)
    - 4.87e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (4.87e-03, rho=1.99e-01 k*=10)
    - 2.14e-03 -> mono {not(D):1}   via not(D) (2.14e-03, rho=3.83e-02 k*=10)
- mono {eq(ME,THEM):1}
    - 9.34e-03 -> mono {D:1}   via D (9.34e-03, rho=4.18e-02 k*=10)
    - 3.08e-03 -> mono {X:1}   via X (3.08e-03, rho=1.38e-02 k*=10)
    - 2.34e-03 -> mono {not(C):1}   via not(C) (2.34e-03, rho=4.18e-02 k*=10)
    - 1.02e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (1.02e-03, rho=4.18e-02 k*=10)
    - 8.56e-04 -> mono {C:1}   via C (8.56e-04, rho=3.83e-03 k*=10)
    - 7.71e-04 -> mono {not(X):1}   via not(X) (7.71e-04, rho=1.38e-02 k*=10)
- mono {eq(THEM,ME):1}
    - 9.34e-03 -> mono {D:1}   via D (9.34e-03, rho=4.18e-02 k*=10)
    - 3.08e-03 -> mono {X:1}   via X (3.08e-03, rho=1.38e-02 k*=10)
    - 2.34e-03 -> mono {not(C):1}   via not(C) (2.34e-03, rho=4.18e-02 k*=10)
    - 1.02e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (1.02e-03, rho=4.18e-02 k*=10)
    - 8.56e-04 -> mono {C:1}   via C (8.56e-04, rho=3.83e-03 k*=10)
    - 7.71e-04 -> mono {not(X):1}   via not(X) (7.71e-04, rho=1.38e-02 k*=10)
- mono {C:1}
    - 7.04e-02 -> mono {D:1}   via D (7.04e-02, rho=3.15e-01 k*=10)
    - 4.46e-02 -> mono {X:1}   via X (4.46e-02, rho=1.99e-01 k*=10)
    - 1.76e-02 -> mono {not(C):1}   via not(C) (1.76e-02, rho=3.15e-01 k*=10)
    - 1.11e-02 -> mono {not(X):1}   via not(X) (1.11e-02, rho=1.99e-01 k*=10)
    - 7.69e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (7.69e-03, rho=3.15e-01 k*=10)
    - 5.59e-03 -> mono {not(D):1}   via not(D) (5.59e-03, rho=1.00e-01 k*=10)
- mono {not(not(D)):1}
    - 2.24e-02 -> mono {D:1}   via D (2.24e-02, rho=1.00e-01 k*=10)
    - 8.56e-03 -> mono {X:1}   via X (8.56e-03, rho=3.83e-02 k*=10)
    - 5.59e-03 -> mono {not(C):1}   via not(C) (5.59e-03, rho=1.00e-01 k*=10)
    - 2.60e-03 -> mono {C:1}   via C (2.60e-03, rho=1.16e-02 k*=10)
    - 2.44e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-03, rho=1.00e-01 k*=10)
    - 2.14e-03 -> mono {not(X):1}   via not(X) (2.14e-03, rho=3.83e-02 k*=10)
- mono {and(D,X):1}
    - 2.24e-02 -> mono {D:1}   via D (2.24e-02, rho=1.00e-01 k*=10)
    - 8.56e-03 -> mono {X:1}   via X (8.56e-03, rho=3.83e-02 k*=10)
    - 5.59e-03 -> mono {not(C):1}   via not(C) (5.59e-03, rho=1.00e-01 k*=10)
    - 2.60e-03 -> mono {C:1}   via C (2.60e-03, rho=1.16e-02 k*=10)
    - 2.44e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-03, rho=1.00e-01 k*=10)
    - 2.14e-03 -> mono {not(X):1}   via not(X) (2.14e-03, rho=3.83e-02 k*=10)
- mono {or(D,D):1}
    - 2.24e-02 -> mono {D:1}   via D (2.24e-02, rho=1.00e-01 k*=10)
    - 8.56e-03 -> mono {X:1}   via X (8.56e-03, rho=3.83e-02 k*=10)
    - 5.59e-03 -> mono {not(C):1}   via not(C) (5.59e-03, rho=1.00e-01 k*=10)
    - 2.60e-03 -> mono {C:1}   via C (2.60e-03, rho=1.16e-02 k*=10)
    - 2.44e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-03, rho=1.00e-01 k*=10)
    - 2.14e-03 -> mono {not(X):1}   via not(X) (2.14e-03, rho=3.83e-02 k*=10)
- mono {and(D,C):1}
    - 2.24e-02 -> mono {D:1}   via D (2.24e-02, rho=1.00e-01 k*=10)
    - 8.56e-03 -> mono {X:1}   via X (8.56e-03, rho=3.83e-02 k*=10)
    - 5.59e-03 -> mono {not(C):1}   via not(C) (5.59e-03, rho=1.00e-01 k*=10)
    - 2.60e-03 -> mono {C:1}   via C (2.60e-03, rho=1.16e-02 k*=10)
    - 2.44e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-03, rho=1.00e-01 k*=10)
    - 2.14e-03 -> mono {not(X):1}   via not(X) (2.14e-03, rho=3.83e-02 k*=10)
