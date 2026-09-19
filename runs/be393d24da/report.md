### arm=source, n=6, game=pd, N=10, w=0.1, x_on=True, role=False, mode=square

programs 2110, classes 220, states 2636, terminal classes 1, indeterminate 0, divergence rate 0.0014, flow into polymorphic targets 2.02e-05
mean payoff -0.6753, efficient 0.0000, deadweight loss 0.6753, mean bits in support 4.20

| pi | state |
|---|---|
| 0.3553 | mono {D:1} |
| 0.1971 | mono {X:1} |
| 0.1127 | mono {C:1} |
| 0.0887 | mono {not(C):1} |
| 0.0492 | mono {not(X):1} |
| 0.0387 | mono {not(not(not(C))):1} |
| 0.0281 | mono {not(D):1} |
| 0.0132 | mono {not(not(not(X))):1} |
| 0.0123 | mono {not(not(not(D))):1} |
| 0.0071 | mono {eq(ME,THEM):1} |
| 0.0071 | mono {eq(THEM,ME):1} |
| 0.0047 | mono {and(X,D):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.62e-02 -> mono {X:1}   via X (1.62e-02, rho=7.26e-02 k*=10)
    - 1.15e-02 -> mono {C:1}   via C (1.15e-02, rho=5.13e-02 k*=10)
    - 5.59e-03 -> mono {not(C):1}   via not(C) (5.59e-03, rho=1.00e-01 k*=10)
    - 4.06e-03 -> mono {not(X):1}   via not(X) (4.06e-03, rho=7.26e-02 k*=10)
    - 2.87e-03 -> mono {not(D):1}   via not(D) (2.87e-03, rho=5.13e-02 k*=10)
    - 2.44e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-03, rho=1.00e-01 k*=10)
- mono {X:1}
    - 2.94e-02 -> mono {D:1}   via D (2.94e-02, rho=1.32e-01 k*=10)
    - 1.65e-02 -> mono {C:1}   via C (1.65e-02, rho=7.39e-02 k*=10)
    - 7.36e-03 -> mono {not(C):1}   via not(C) (7.36e-03, rho=1.32e-01 k*=10)
    - 5.59e-03 -> mono {not(X):1}   via not(X) (5.59e-03, rho=1.00e-01 k*=10)
    - 4.13e-03 -> mono {not(D):1}   via not(D) (4.13e-03, rho=7.39e-02 k*=10)
    - 3.22e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.22e-03, rho=1.32e-01 k*=10)
- mono {C:1}
    - 3.67e-02 -> mono {D:1}   via D (3.67e-02, rho=1.64e-01 k*=10)
    - 2.90e-02 -> mono {X:1}   via X (2.90e-02, rho=1.30e-01 k*=10)
    - 9.18e-03 -> mono {not(C):1}   via not(C) (9.18e-03, rho=1.64e-01 k*=10)
    - 7.26e-03 -> mono {not(X):1}   via not(X) (7.26e-03, rho=1.30e-01 k*=10)
    - 5.59e-03 -> mono {not(D):1}   via not(D) (5.59e-03, rho=1.00e-01 k*=10)
    - 4.01e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (4.01e-03, rho=1.64e-01 k*=10)
- mono {not(C):1}
    - 2.24e-02 -> mono {D:1}   via D (2.24e-02, rho=1.00e-01 k*=10)
    - 1.62e-02 -> mono {X:1}   via X (1.62e-02, rho=7.26e-02 k*=10)
    - 1.15e-02 -> mono {C:1}   via C (1.15e-02, rho=5.13e-02 k*=10)
    - 4.06e-03 -> mono {not(X):1}   via not(X) (4.06e-03, rho=7.26e-02 k*=10)
    - 2.87e-03 -> mono {not(D):1}   via not(D) (2.87e-03, rho=5.13e-02 k*=10)
    - 2.44e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-03, rho=1.00e-01 k*=10)
- mono {not(X):1}
    - 2.94e-02 -> mono {D:1}   via D (2.94e-02, rho=1.32e-01 k*=10)
    - 2.24e-02 -> mono {X:1}   via X (2.24e-02, rho=1.00e-01 k*=10)
    - 1.65e-02 -> mono {C:1}   via C (1.65e-02, rho=7.39e-02 k*=10)
    - 7.36e-03 -> mono {not(C):1}   via not(C) (7.36e-03, rho=1.32e-01 k*=10)
    - 4.13e-03 -> mono {not(D):1}   via not(D) (4.13e-03, rho=7.39e-02 k*=10)
    - 3.22e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.22e-03, rho=1.32e-01 k*=10)
- mono {not(not(not(C))):1}
    - 2.24e-02 -> mono {D:1}   via D (2.24e-02, rho=1.00e-01 k*=10)
    - 1.62e-02 -> mono {X:1}   via X (1.62e-02, rho=7.26e-02 k*=10)
    - 1.15e-02 -> mono {C:1}   via C (1.15e-02, rho=5.13e-02 k*=10)
    - 5.59e-03 -> mono {not(C):1}   via not(C) (5.59e-03, rho=1.00e-01 k*=10)
    - 4.06e-03 -> mono {not(X):1}   via not(X) (4.06e-03, rho=7.26e-02 k*=10)
    - 2.87e-03 -> mono {not(D):1}   via not(D) (2.87e-03, rho=5.13e-02 k*=10)
- mono {not(D):1}
    - 3.67e-02 -> mono {D:1}   via D (3.67e-02, rho=1.64e-01 k*=10)
    - 2.90e-02 -> mono {X:1}   via X (2.90e-02, rho=1.30e-01 k*=10)
    - 2.24e-02 -> mono {C:1}   via C (2.24e-02, rho=1.00e-01 k*=10)
    - 9.18e-03 -> mono {not(C):1}   via not(C) (9.18e-03, rho=1.64e-01 k*=10)
    - 7.26e-03 -> mono {not(X):1}   via not(X) (7.26e-03, rho=1.30e-01 k*=10)
    - 4.01e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (4.01e-03, rho=1.64e-01 k*=10)
- mono {not(not(not(X))):1}
    - 2.94e-02 -> mono {D:1}   via D (2.94e-02, rho=1.32e-01 k*=10)
    - 2.24e-02 -> mono {X:1}   via X (2.24e-02, rho=1.00e-01 k*=10)
    - 1.65e-02 -> mono {C:1}   via C (1.65e-02, rho=7.39e-02 k*=10)
    - 7.36e-03 -> mono {not(C):1}   via not(C) (7.36e-03, rho=1.32e-01 k*=10)
    - 5.59e-03 -> mono {not(X):1}   via not(X) (5.59e-03, rho=1.00e-01 k*=10)
    - 4.13e-03 -> mono {not(D):1}   via not(D) (4.13e-03, rho=7.39e-02 k*=10)
- mono {not(not(not(D))):1}
    - 3.67e-02 -> mono {D:1}   via D (3.67e-02, rho=1.64e-01 k*=10)
    - 2.90e-02 -> mono {X:1}   via X (2.90e-02, rho=1.30e-01 k*=10)
    - 2.24e-02 -> mono {C:1}   via C (2.24e-02, rho=1.00e-01 k*=10)
    - 9.18e-03 -> mono {not(C):1}   via not(C) (9.18e-03, rho=1.64e-01 k*=10)
    - 7.26e-03 -> mono {not(X):1}   via not(X) (7.26e-03, rho=1.30e-01 k*=10)
    - 5.59e-03 -> mono {not(D):1}   via not(D) (5.59e-03, rho=1.00e-01 k*=10)
- mono {eq(ME,THEM):1}
    - 1.66e-02 -> mono {D:1}   via D (1.66e-02, rho=7.44e-02 k*=10)
    - 1.19e-02 -> mono {X:1}   via X (1.19e-02, rho=5.33e-02 k*=10)
    - 8.35e-03 -> mono {C:1}   via C (8.35e-03, rho=3.73e-02 k*=10)
    - 4.16e-03 -> mono {not(C):1}   via not(C) (4.16e-03, rho=7.44e-02 k*=10)
    - 2.98e-03 -> mono {not(X):1}   via not(X) (2.98e-03, rho=5.33e-02 k*=10)
    - 2.09e-03 -> mono {not(D):1}   via not(D) (2.09e-03, rho=3.73e-02 k*=10)
- mono {eq(THEM,ME):1}
    - 1.66e-02 -> mono {D:1}   via D (1.66e-02, rho=7.44e-02 k*=10)
    - 1.19e-02 -> mono {X:1}   via X (1.19e-02, rho=5.33e-02 k*=10)
    - 8.35e-03 -> mono {C:1}   via C (8.35e-03, rho=3.73e-02 k*=10)
    - 4.16e-03 -> mono {not(C):1}   via not(C) (4.16e-03, rho=7.44e-02 k*=10)
    - 2.98e-03 -> mono {not(X):1}   via not(X) (2.98e-03, rho=5.33e-02 k*=10)
    - 2.09e-03 -> mono {not(D):1}   via not(D) (2.09e-03, rho=3.73e-02 k*=10)
- mono {and(X,D):1}
    - 2.24e-02 -> mono {D:1}   via D (2.24e-02, rho=1.00e-01 k*=10)
    - 1.62e-02 -> mono {X:1}   via X (1.62e-02, rho=7.26e-02 k*=10)
    - 1.15e-02 -> mono {C:1}   via C (1.15e-02, rho=5.13e-02 k*=10)
    - 5.59e-03 -> mono {not(C):1}   via not(C) (5.59e-03, rho=1.00e-01 k*=10)
    - 4.06e-03 -> mono {not(X):1}   via not(X) (4.06e-03, rho=7.26e-02 k*=10)
    - 2.87e-03 -> mono {not(D):1}   via not(D) (2.87e-03, rho=5.13e-02 k*=10)
