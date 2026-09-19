### arm=source, n=6, game=pd, N=100, w=0.01, x_on=True, role=False, mode=square

programs 2110, classes 220, states 2586, terminal classes 1, indeterminate 0, divergence rate 0.0014, flow into polymorphic targets 2.03e-06
mean payoff -0.6536, efficient 0.0000, deadweight loss 0.6536, mean bits in support 4.20

| pi | state |
|---|---|
| 0.3373 | mono {D:1} |
| 0.2041 | mono {X:1} |
| 0.1238 | mono {C:1} |
| 0.0842 | mono {not(C):1} |
| 0.0509 | mono {not(X):1} |
| 0.0368 | mono {not(not(not(C))):1} |
| 0.0309 | mono {not(D):1} |
| 0.0136 | mono {not(not(not(X))):1} |
| 0.0135 | mono {not(not(not(D))):1} |
| 0.0074 | mono {eq(THEM,ME):1} |
| 0.0074 | mono {eq(ME,THEM):1} |
| 0.0045 | mono {and(X,D):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.71e-03 -> mono {X:1}   via X (1.71e-03, rho=7.67e-03 k*=100)
    - 1.29e-03 -> mono {C:1}   via C (1.29e-03, rho=5.75e-03 k*=100)
    - 5.59e-04 -> mono {not(C):1}   via not(C) (5.59e-04, rho=1.00e-02 k*=100)
    - 4.28e-04 -> mono {not(X):1}   via not(X) (4.28e-04, rho=7.67e-03 k*=100)
    - 3.22e-04 -> mono {not(D):1}   via not(D) (3.22e-04, rho=5.75e-03 k*=100)
    - 2.44e-04 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-04, rho=1.00e-02 k*=100)
- mono {X:1}
    - 2.85e-03 -> mono {D:1}   via D (2.85e-03, rho=1.28e-02 k*=100)
    - 1.72e-03 -> mono {C:1}   via C (1.72e-03, rho=7.68e-03 k*=100)
    - 7.12e-04 -> mono {not(C):1}   via not(C) (7.12e-04, rho=1.28e-02 k*=100)
    - 5.59e-04 -> mono {not(X):1}   via not(X) (5.59e-04, rho=1.00e-02 k*=100)
    - 4.29e-04 -> mono {not(D):1}   via not(D) (4.29e-04, rho=7.68e-03 k*=100)
    - 3.11e-04 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.11e-04, rho=1.28e-02 k*=100)
- mono {C:1}
    - 3.55e-03 -> mono {D:1}   via D (3.55e-03, rho=1.59e-02 k*=100)
    - 2.85e-03 -> mono {X:1}   via X (2.85e-03, rho=1.27e-02 k*=100)
    - 8.87e-04 -> mono {not(C):1}   via not(C) (8.87e-04, rho=1.59e-02 k*=100)
    - 7.12e-04 -> mono {not(X):1}   via not(X) (7.12e-04, rho=1.27e-02 k*=100)
    - 5.59e-04 -> mono {not(D):1}   via not(D) (5.59e-04, rho=1.00e-02 k*=100)
    - 3.88e-04 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.88e-04, rho=1.59e-02 k*=100)
- mono {not(C):1}
    - 2.24e-03 -> mono {D:1}   via D (2.24e-03, rho=1.00e-02 k*=100)
    - 1.71e-03 -> mono {X:1}   via X (1.71e-03, rho=7.67e-03 k*=100)
    - 1.29e-03 -> mono {C:1}   via C (1.29e-03, rho=5.75e-03 k*=100)
    - 4.28e-04 -> mono {not(X):1}   via not(X) (4.28e-04, rho=7.67e-03 k*=100)
    - 3.22e-04 -> mono {not(D):1}   via not(D) (3.22e-04, rho=5.75e-03 k*=100)
    - 2.44e-04 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-04, rho=1.00e-02 k*=100)
- mono {not(X):1}
    - 2.85e-03 -> mono {D:1}   via D (2.85e-03, rho=1.28e-02 k*=100)
    - 2.24e-03 -> mono {X:1}   via X (2.24e-03, rho=1.00e-02 k*=100)
    - 1.72e-03 -> mono {C:1}   via C (1.72e-03, rho=7.68e-03 k*=100)
    - 7.12e-04 -> mono {not(C):1}   via not(C) (7.12e-04, rho=1.28e-02 k*=100)
    - 4.29e-04 -> mono {not(D):1}   via not(D) (4.29e-04, rho=7.68e-03 k*=100)
    - 3.11e-04 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.11e-04, rho=1.28e-02 k*=100)
- mono {not(not(not(C))):1}
    - 2.24e-03 -> mono {D:1}   via D (2.24e-03, rho=1.00e-02 k*=100)
    - 1.71e-03 -> mono {X:1}   via X (1.71e-03, rho=7.67e-03 k*=100)
    - 1.29e-03 -> mono {C:1}   via C (1.29e-03, rho=5.75e-03 k*=100)
    - 5.59e-04 -> mono {not(C):1}   via not(C) (5.59e-04, rho=1.00e-02 k*=100)
    - 4.28e-04 -> mono {not(X):1}   via not(X) (4.28e-04, rho=7.67e-03 k*=100)
    - 3.22e-04 -> mono {not(D):1}   via not(D) (3.22e-04, rho=5.75e-03 k*=100)
- mono {not(D):1}
    - 3.55e-03 -> mono {D:1}   via D (3.55e-03, rho=1.59e-02 k*=100)
    - 2.85e-03 -> mono {X:1}   via X (2.85e-03, rho=1.27e-02 k*=100)
    - 2.24e-03 -> mono {C:1}   via C (2.24e-03, rho=1.00e-02 k*=100)
    - 8.87e-04 -> mono {not(C):1}   via not(C) (8.87e-04, rho=1.59e-02 k*=100)
    - 7.12e-04 -> mono {not(X):1}   via not(X) (7.12e-04, rho=1.27e-02 k*=100)
    - 3.88e-04 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.88e-04, rho=1.59e-02 k*=100)
- mono {not(not(not(X))):1}
    - 2.85e-03 -> mono {D:1}   via D (2.85e-03, rho=1.28e-02 k*=100)
    - 2.24e-03 -> mono {X:1}   via X (2.24e-03, rho=1.00e-02 k*=100)
    - 1.72e-03 -> mono {C:1}   via C (1.72e-03, rho=7.68e-03 k*=100)
    - 7.12e-04 -> mono {not(C):1}   via not(C) (7.12e-04, rho=1.28e-02 k*=100)
    - 5.59e-04 -> mono {not(X):1}   via not(X) (5.59e-04, rho=1.00e-02 k*=100)
    - 4.29e-04 -> mono {not(D):1}   via not(D) (4.29e-04, rho=7.68e-03 k*=100)
- mono {not(not(not(D))):1}
    - 3.55e-03 -> mono {D:1}   via D (3.55e-03, rho=1.59e-02 k*=100)
    - 2.85e-03 -> mono {X:1}   via X (2.85e-03, rho=1.27e-02 k*=100)
    - 2.24e-03 -> mono {C:1}   via C (2.24e-03, rho=1.00e-02 k*=100)
    - 8.87e-04 -> mono {not(C):1}   via not(C) (8.87e-04, rho=1.59e-02 k*=100)
    - 7.12e-04 -> mono {not(X):1}   via not(X) (7.12e-04, rho=1.27e-02 k*=100)
    - 5.59e-04 -> mono {not(D):1}   via not(D) (5.59e-04, rho=1.00e-02 k*=100)
- mono {eq(THEM,ME):1}
    - 1.59e-03 -> mono {D:1}   via D (1.59e-03, rho=7.12e-03 k*=100)
    - 1.20e-03 -> mono {X:1}   via X (1.20e-03, rho=5.36e-03 k*=100)
    - 8.83e-04 -> mono {C:1}   via C (8.83e-04, rho=3.95e-03 k*=100)
    - 3.98e-04 -> mono {not(C):1}   via not(C) (3.98e-04, rho=7.12e-03 k*=100)
    - 2.99e-04 -> mono {not(X):1}   via not(X) (2.99e-04, rho=5.36e-03 k*=100)
    - 2.21e-04 -> mono {not(D):1}   via not(D) (2.21e-04, rho=3.95e-03 k*=100)
- mono {eq(ME,THEM):1}
    - 1.59e-03 -> mono {D:1}   via D (1.59e-03, rho=7.12e-03 k*=100)
    - 1.20e-03 -> mono {X:1}   via X (1.20e-03, rho=5.36e-03 k*=100)
    - 8.83e-04 -> mono {C:1}   via C (8.83e-04, rho=3.95e-03 k*=100)
    - 3.98e-04 -> mono {not(C):1}   via not(C) (3.98e-04, rho=7.12e-03 k*=100)
    - 2.99e-04 -> mono {not(X):1}   via not(X) (2.99e-04, rho=5.36e-03 k*=100)
    - 2.21e-04 -> mono {not(D):1}   via not(D) (2.21e-04, rho=3.95e-03 k*=100)
- mono {and(X,D):1}
    - 2.24e-03 -> mono {D:1}   via D (2.24e-03, rho=1.00e-02 k*=100)
    - 1.71e-03 -> mono {X:1}   via X (1.71e-03, rho=7.67e-03 k*=100)
    - 1.29e-03 -> mono {C:1}   via C (1.29e-03, rho=5.75e-03 k*=100)
    - 5.59e-04 -> mono {not(C):1}   via not(C) (5.59e-04, rho=1.00e-02 k*=100)
    - 4.28e-04 -> mono {not(X):1}   via not(X) (4.28e-04, rho=7.67e-03 k*=100)
    - 3.22e-04 -> mono {not(D):1}   via not(D) (3.22e-04, rho=5.75e-03 k*=100)
