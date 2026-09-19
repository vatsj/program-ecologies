### arm=weak, n=5, game=zerosum, N=100, w=0.1, x_on=True, role=True, mode=square

programs 902, classes 53, states 53, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 0.00e+00
mean payoff 0.0000, efficient 0.0000, deadweight loss 0.0000, mean bits in support 3.37

| pi | state |
|---|---|
| 0.4040 | mono {D:1} |
| 0.2314 | mono {X:1} |
| 0.1425 | mono {C:1} |
| 0.1199 | mono {ROLE:1} |
| 0.0709 | mono {not(ROLE):1} |
| 0.0056 | mono {and(X,ROLE):1} |
| 0.0055 | mono {and(X,X):1} |
| 0.0034 | mono {or(X,ROLE):1} |
| 0.0029 | mono {not(or(X,ROLE)):1} |
| 0.0026 | mono {or(X,X):1} |
| 0.0022 | mono {THEM(THEM):1} |
| 0.0022 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 4.40e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.40e-03, rho=9.27e-02 k*=100)
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 8.58e-05 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (8.58e-05, rho=4.89e-02 k*=100)
    - 8.58e-05 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (8.58e-05, rho=4.89e-02 k*=100)
    - 3.86e-05 -> mono {or(X,X):1}   via or(X,X) (3.86e-05, rho=1.00e-02 k*=100)
- mono {X:1}
    - 2.49e-03 -> mono {D:1}   via D (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
    - 6.26e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-05, rho=1.00e-02 k*=100)
    - 6.26e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.26e-05, rho=1.00e-02 k*=100)
- mono {C:1}
    - 1.76e-02 -> mono {ROLE:1}   via ROLE (1.76e-02, rho=9.27e-02 k*=100)
    - 2.49e-03 -> mono {D:1}   via D (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 3.06e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (3.06e-04, rho=4.89e-02 k*=100)
    - 3.06e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (3.06e-04, rho=4.89e-02 k*=100)
    - 3.86e-05 -> mono {or(X,X):1}   via or(X,X) (3.86e-05, rho=1.00e-02 k*=100)
- mono {ROLE:1}
    - 2.31e-02 -> mono {D:1}   via D (2.31e-02, rho=9.27e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
    - 3.06e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (3.06e-04, rho=4.89e-02 k*=100)
    - 1.89e-04 -> mono {and(X,X):1}   via and(X,X) (1.89e-04, rho=4.89e-02 k*=100)
    - 8.58e-05 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (8.58e-05, rho=4.89e-02 k*=100)
- mono {not(ROLE):1}
    - 2.31e-02 -> mono {C:1}   via C (2.31e-02, rho=9.27e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 3.06e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (3.06e-04, rho=4.89e-02 k*=100)
    - 1.89e-04 -> mono {or(X,X):1}   via or(X,X) (1.89e-04, rho=4.89e-02 k*=100)
    - 8.58e-05 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (8.58e-05, rho=4.89e-02 k*=100)
- mono {and(X,ROLE):1}
    - 1.22e-02 -> mono {D:1}   via D (1.22e-02, rho=4.89e-02 k*=100)
    - 2.32e-03 -> mono {not(ROLE):1}   via not(ROLE) (2.32e-03, rho=4.89e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.07e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (1.07e-04, rho=4.89e-02 k*=100)
    - 1.07e-04 -> mono {THEM(ME):1}   via THEM(ME) (1.07e-04, rho=4.89e-02 k*=100)
    - 1.04e-04 -> mono {and(X,X):1}   via and(X,X) (1.04e-04, rho=2.70e-02 k*=100)
- mono {and(X,X):1}
    - 2.49e-03 -> mono {D:1}   via D (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 2.32e-03 -> mono {not(ROLE):1}   via not(ROLE) (2.32e-03, rho=4.89e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 6.26e-05 -> mono {ROLE:1}   via ROLE (6.26e-05, rho=3.28e-04 k*=100)
    - 4.74e-05 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (4.74e-05, rho=2.70e-02 k*=100)
- mono {or(X,ROLE):1}
    - 1.22e-02 -> mono {D:1}   via D (1.22e-02, rho=4.89e-02 k*=100)
    - 9.30e-03 -> mono {ROLE:1}   via ROLE (9.30e-03, rho=4.89e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 3.06e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (3.06e-04, rho=4.89e-02 k*=100)
    - 1.04e-04 -> mono {and(X,X):1}   via and(X,X) (1.04e-04, rho=2.70e-02 k*=100)
    - 8.18e-05 -> mono {C:1}   via C (8.18e-05, rho=3.28e-04 k*=100)
- mono {not(or(X,ROLE)):1}
    - 1.22e-02 -> mono {C:1}   via C (1.22e-02, rho=4.89e-02 k*=100)
    - 2.32e-03 -> mono {not(ROLE):1}   via not(ROLE) (2.32e-03, rho=4.89e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.04e-04 -> mono {or(X,X):1}   via or(X,X) (1.04e-04, rho=2.70e-02 k*=100)
    - 8.58e-05 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (8.58e-05, rho=4.89e-02 k*=100)
    - 8.18e-05 -> mono {D:1}   via D (8.18e-05, rho=3.28e-04 k*=100)
- mono {or(X,X):1}
    - 9.30e-03 -> mono {ROLE:1}   via ROLE (9.30e-03, rho=4.89e-02 k*=100)
    - 2.49e-03 -> mono {D:1}   via D (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.69e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.69e-04, rho=2.70e-02 k*=100)
    - 1.69e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.69e-04, rho=2.70e-02 k*=100)
- mono {THEM(THEM):1}
    - 2.49e-03 -> mono {D:1}   via D (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
    - 3.06e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (3.06e-04, rho=4.89e-02 k*=100)
- mono {THEM(ME):1}
    - 2.49e-03 -> mono {D:1}   via D (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
    - 3.06e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (3.06e-04, rho=4.89e-02 k*=100)
