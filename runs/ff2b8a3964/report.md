### arm=weak, n=5, game=zerosum, N=10, w=0.1, x_on=True, role=True, mode=square

programs 902, classes 53, states 53, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 0.00e+00
mean payoff 0.0000, efficient 0.0000, deadweight loss 0.0000, mean bits in support 3.33

| pi | state |
|---|---|
| 0.2863 | mono {D:1} |
| 0.2314 | mono {X:1} |
| 0.2165 | mono {C:1} |
| 0.1841 | mono {ROLE:1} |
| 0.0491 | mono {not(ROLE):1} |
| 0.0066 | mono {and(X,ROLE):1} |
| 0.0057 | mono {or(X,ROLE):1} |
| 0.0041 | mono {and(X,X):1} |
| 0.0036 | mono {or(X,X):1} |
| 0.0022 | mono {THEM(THEM):1} |
| 0.0022 | mono {THEM(ME):1} |
| 0.0019 | mono {not(or(X,ROLE)):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.09e-02 -> mono {ROLE:1}   via ROLE (1.09e-02, rho=5.72e-02 k*=10)
    - 7.40e-03 -> mono {not(ROLE):1}   via not(ROLE) (7.40e-03, rho=1.56e-01 k*=10)
    - 4.80e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (4.80e-04, rho=7.67e-02 k*=10)
    - 4.80e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (4.80e-04, rho=7.67e-02 k*=10)
- mono {X:1}
    - 2.49e-02 -> mono {D:1}   via D (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 6.26e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
    - 6.26e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
- mono {C:1}
    - 2.97e-02 -> mono {ROLE:1}   via ROLE (2.97e-02, rho=1.56e-01 k*=10)
    - 2.49e-02 -> mono {D:1}   via D (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 2.72e-03 -> mono {not(ROLE):1}   via not(ROLE) (2.72e-03, rho=5.72e-02 k*=10)
    - 7.92e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.92e-04, rho=1.27e-01 k*=10)
    - 7.92e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (7.92e-04, rho=1.27e-01 k*=10)
- mono {ROLE:1}
    - 3.88e-02 -> mono {D:1}   via D (3.88e-02, rho=1.56e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.42e-02 -> mono {C:1}   via C (1.42e-02, rho=5.72e-02 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 7.92e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (7.92e-04, rho=1.27e-01 k*=10)
    - 4.89e-04 -> mono {and(X,X):1}   via and(X,X) (4.89e-04, rho=1.27e-01 k*=10)
- mono {not(ROLE):1}
    - 3.88e-02 -> mono {C:1}   via C (3.88e-02, rho=1.56e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 1.42e-02 -> mono {D:1}   via D (1.42e-02, rho=5.72e-02 k*=10)
    - 7.92e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.92e-04, rho=1.27e-01 k*=10)
    - 4.89e-04 -> mono {or(X,X):1}   via or(X,X) (4.89e-04, rho=1.27e-01 k*=10)
- mono {and(X,ROLE):1}
    - 3.15e-02 -> mono {D:1}   via D (3.15e-02, rho=1.27e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.91e-02 -> mono {C:1}   via C (1.91e-02, rho=7.67e-02 k*=10)
    - 1.46e-02 -> mono {ROLE:1}   via ROLE (1.46e-02, rho=7.67e-02 k*=10)
    - 6.01e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.01e-03, rho=1.27e-01 k*=10)
    - 4.80e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (4.80e-04, rho=7.67e-02 k*=10)
- mono {or(X,ROLE):1}
    - 3.15e-02 -> mono {D:1}   via D (3.15e-02, rho=1.27e-01 k*=10)
    - 2.41e-02 -> mono {ROLE:1}   via ROLE (2.41e-02, rho=1.27e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.91e-02 -> mono {C:1}   via C (1.91e-02, rho=7.67e-02 k*=10)
    - 3.65e-03 -> mono {not(ROLE):1}   via not(ROLE) (3.65e-03, rho=7.67e-02 k*=10)
    - 7.92e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (7.92e-04, rho=1.27e-01 k*=10)
- mono {and(X,X):1}
    - 2.49e-02 -> mono {D:1}   via D (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.46e-02 -> mono {ROLE:1}   via ROLE (1.46e-02, rho=7.67e-02 k*=10)
    - 6.01e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.01e-03, rho=1.27e-01 k*=10)
    - 5.50e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (5.50e-04, rho=8.79e-02 k*=10)
- mono {or(X,X):1}
    - 2.49e-02 -> mono {D:1}   via D (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=1.00e-01 k*=10)
    - 2.41e-02 -> mono {ROLE:1}   via ROLE (2.41e-02, rho=1.27e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 3.65e-03 -> mono {not(ROLE):1}   via not(ROLE) (3.65e-03, rho=7.67e-02 k*=10)
    - 7.07e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.07e-04, rho=1.13e-01 k*=10)
- mono {THEM(THEM):1}
    - 2.49e-02 -> mono {D:1}   via D (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 7.92e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.92e-04, rho=1.27e-01 k*=10)
- mono {THEM(ME):1}
    - 2.49e-02 -> mono {D:1}   via D (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 7.92e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.92e-04, rho=1.27e-01 k*=10)
- mono {not(or(X,ROLE)):1}
    - 3.15e-02 -> mono {C:1}   via C (3.15e-02, rho=1.27e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.91e-02 -> mono {D:1}   via D (1.91e-02, rho=7.67e-02 k*=10)
    - 1.46e-02 -> mono {ROLE:1}   via ROLE (1.46e-02, rho=7.67e-02 k*=10)
    - 6.01e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.01e-03, rho=1.27e-01 k*=10)
    - 6.26e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
