### arm=weak, n=5, game=zerosum, N=10, w=0.01, x_on=True, role=True, mode=square

programs 902, classes 53, states 53, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 0.00e+00
mean payoff 0.0000, efficient 0.0000, deadweight loss 0.0000, mean bits in support 3.33

| pi | state |
|---|---|
| 0.2527 | mono {D:1} |
| 0.2453 | mono {C:1} |
| 0.2314 | mono {X:1} |
| 0.1904 | mono {ROLE:1} |
| 0.0475 | mono {not(ROLE):1} |
| 0.0063 | mono {and(X,ROLE):1} |
| 0.0062 | mono {or(X,ROLE):1} |
| 0.0039 | mono {and(X,X):1} |
| 0.0038 | mono {or(X,X):1} |
| 0.0022 | mono {THEM(THEM):1} |
| 0.0022 | mono {THEM(ME):1} |
| 0.0018 | mono {not(or(X,ROLE)):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.81e-02 -> mono {ROLE:1}   via ROLE (1.81e-02, rho=9.51e-02 k*=10)
    - 4.99e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.99e-03, rho=1.05e-01 k*=10)
    - 6.10e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.10e-04, rho=9.75e-02 k*=10)
    - 6.10e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.10e-04, rho=9.75e-02 k*=10)
- mono {C:1}
    - 2.49e-02 -> mono {D:1}   via D (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 2.00e-02 -> mono {ROLE:1}   via ROLE (2.00e-02, rho=1.05e-01 k*=10)
    - 4.52e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.52e-03, rho=9.51e-02 k*=10)
    - 6.42e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.42e-04, rho=1.03e-01 k*=10)
    - 6.42e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.42e-04, rho=1.03e-01 k*=10)
- mono {X:1}
    - 2.49e-02 -> mono {D:1}   via D (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 6.26e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
    - 6.26e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
- mono {ROLE:1}
    - 2.62e-02 -> mono {D:1}   via D (2.62e-02, rho=1.05e-01 k*=10)
    - 2.37e-02 -> mono {C:1}   via C (2.37e-02, rho=9.51e-02 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 6.42e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.42e-04, rho=1.03e-01 k*=10)
    - 6.10e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.10e-04, rho=9.75e-02 k*=10)
- mono {not(ROLE):1}
    - 2.62e-02 -> mono {C:1}   via C (2.62e-02, rho=1.05e-01 k*=10)
    - 2.37e-02 -> mono {D:1}   via D (2.37e-02, rho=9.51e-02 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 6.42e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.42e-04, rho=1.03e-01 k*=10)
    - 6.10e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.10e-04, rho=9.75e-02 k*=10)
- mono {and(X,ROLE):1}
    - 2.55e-02 -> mono {D:1}   via D (2.55e-02, rho=1.03e-01 k*=10)
    - 2.43e-02 -> mono {C:1}   via C (2.43e-02, rho=9.75e-02 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.86e-02 -> mono {ROLE:1}   via ROLE (1.86e-02, rho=9.75e-02 k*=10)
    - 4.87e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.87e-03, rho=1.03e-01 k*=10)
    - 6.10e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.10e-04, rho=9.75e-02 k*=10)
- mono {or(X,ROLE):1}
    - 2.55e-02 -> mono {D:1}   via D (2.55e-02, rho=1.03e-01 k*=10)
    - 2.43e-02 -> mono {C:1}   via C (2.43e-02, rho=9.75e-02 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.95e-02 -> mono {ROLE:1}   via ROLE (1.95e-02, rho=1.03e-01 k*=10)
    - 4.63e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.63e-03, rho=9.75e-02 k*=10)
    - 6.42e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.42e-04, rho=1.03e-01 k*=10)
- mono {and(X,X):1}
    - 2.49e-02 -> mono {D:1}   via D (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.86e-02 -> mono {ROLE:1}   via ROLE (1.86e-02, rho=9.75e-02 k*=10)
    - 4.87e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.87e-03, rho=1.03e-01 k*=10)
    - 6.18e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.18e-04, rho=9.88e-02 k*=10)
- mono {or(X,X):1}
    - 2.49e-02 -> mono {D:1}   via D (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.95e-02 -> mono {ROLE:1}   via ROLE (1.95e-02, rho=1.03e-01 k*=10)
    - 4.63e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.63e-03, rho=9.75e-02 k*=10)
    - 6.34e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.34e-04, rho=1.01e-01 k*=10)
- mono {THEM(THEM):1}
    - 2.49e-02 -> mono {D:1}   via D (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 6.42e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.42e-04, rho=1.03e-01 k*=10)
- mono {THEM(ME):1}
    - 2.49e-02 -> mono {D:1}   via D (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 6.42e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.42e-04, rho=1.03e-01 k*=10)
- mono {not(or(X,ROLE)):1}
    - 2.55e-02 -> mono {C:1}   via C (2.55e-02, rho=1.03e-01 k*=10)
    - 2.43e-02 -> mono {D:1}   via D (2.43e-02, rho=9.75e-02 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.86e-02 -> mono {ROLE:1}   via ROLE (1.86e-02, rho=9.75e-02 k*=10)
    - 4.87e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.87e-03, rho=1.03e-01 k*=10)
    - 6.26e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
