### arm=weak, n=5, game=zerosum, N=10, w=1.0, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 53, states 53, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 0.00e+00
mean payoff 0.0000, efficient 0.0000, deadweight loss 0.0000, mean bits in support 3.37

| pi | state |
|---|---|
| 0.3906 | mono {Heads:1} |
| 0.2314 | mono {X:1} |
| 0.1509 | mono {Tails:1} |
| 0.1283 | mono {ROLE:1} |
| 0.0673 | mono {not(ROLE):1} |
| 0.0059 | mono {or(X,ROLE):1} |
| 0.0055 | mono {or(X,X):1} |
| 0.0035 | mono {and(X,ROLE):1} |
| 0.0029 | mono {not(and(X,ROLE)):1} |
| 0.0026 | mono {and(X,X):1} |
| 0.0022 | mono {THEM(ME):1} |
| 0.0022 | mono {THEM(THEM):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Heads:1}
    - 3.19e-02 -> mono {not(ROLE):1}   via not(ROLE) (3.19e-02, rho=6.71e-01 k*=10)
    - 2.49e-02 -> mono {Tails:1}   via Tails (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 7.52e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (7.52e-04, rho=4.28e-01 k*=10)
    - 7.52e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (7.52e-04, rho=4.28e-01 k*=10)
    - 3.86e-04 -> mono {or(X,X):1}   via or(X,X) (3.86e-04, rho=1.00e-01 k*=10)
- mono {X:1}
    - 2.49e-02 -> mono {Heads:1}   via Heads (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {Tails:1}   via Tails (2.49e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 6.26e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
    - 6.26e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
- mono {Tails:1}
    - 1.28e-01 -> mono {ROLE:1}   via ROLE (1.28e-01, rho=6.71e-01 k*=10)
    - 2.49e-02 -> mono {Heads:1}   via Heads (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 2.68e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.68e-03, rho=4.28e-01 k*=10)
    - 2.68e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.68e-03, rho=4.28e-01 k*=10)
    - 3.86e-04 -> mono {or(X,X):1}   via or(X,X) (3.86e-04, rho=1.00e-01 k*=10)
- mono {ROLE:1}
    - 1.67e-01 -> mono {Heads:1}   via Heads (1.67e-01, rho=6.71e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 2.68e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.68e-03, rho=4.28e-01 k*=10)
    - 1.65e-03 -> mono {or(X,X):1}   via or(X,X) (1.65e-03, rho=4.28e-01 k*=10)
    - 7.52e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (7.52e-04, rho=4.28e-01 k*=10)
- mono {not(ROLE):1}
    - 1.67e-01 -> mono {Tails:1}   via Tails (1.67e-01, rho=6.71e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 2.68e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.68e-03, rho=4.28e-01 k*=10)
    - 1.65e-03 -> mono {and(X,X):1}   via and(X,X) (1.65e-03, rho=4.28e-01 k*=10)
    - 7.52e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (7.52e-04, rho=4.28e-01 k*=10)
- mono {or(X,ROLE):1}
    - 1.07e-01 -> mono {Heads:1}   via Heads (1.07e-01, rho=4.28e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 2.03e-02 -> mono {not(ROLE):1}   via not(ROLE) (2.03e-02, rho=4.28e-01 k*=10)
    - 9.99e-04 -> mono {or(X,X):1}   via or(X,X) (9.99e-04, rho=2.59e-01 k*=10)
    - 9.33e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (9.33e-04, rho=4.28e-01 k*=10)
    - 9.33e-04 -> mono {THEM(ME):1}   via THEM(ME) (9.33e-04, rho=4.28e-01 k*=10)
- mono {or(X,X):1}
    - 2.49e-02 -> mono {Heads:1}   via Heads (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {Tails:1}   via Tails (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 2.03e-02 -> mono {not(ROLE):1}   via not(ROLE) (2.03e-02, rho=4.28e-01 k*=10)
    - 5.49e-04 -> mono {ROLE:1}   via ROLE (5.49e-04, rho=2.88e-03 k*=10)
    - 4.54e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (4.54e-04, rho=2.59e-01 k*=10)
- mono {and(X,ROLE):1}
    - 1.07e-01 -> mono {Heads:1}   via Heads (1.07e-01, rho=4.28e-01 k*=10)
    - 8.15e-02 -> mono {ROLE:1}   via ROLE (8.15e-02, rho=4.28e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 2.68e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.68e-03, rho=4.28e-01 k*=10)
    - 9.99e-04 -> mono {or(X,X):1}   via or(X,X) (9.99e-04, rho=2.59e-01 k*=10)
    - 7.18e-04 -> mono {Tails:1}   via Tails (7.18e-04, rho=2.88e-03 k*=10)
- mono {not(and(X,ROLE)):1}
    - 1.07e-01 -> mono {Tails:1}   via Tails (1.07e-01, rho=4.28e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 2.03e-02 -> mono {not(ROLE):1}   via not(ROLE) (2.03e-02, rho=4.28e-01 k*=10)
    - 9.99e-04 -> mono {and(X,X):1}   via and(X,X) (9.99e-04, rho=2.59e-01 k*=10)
    - 7.52e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (7.52e-04, rho=4.28e-01 k*=10)
    - 7.18e-04 -> mono {Heads:1}   via Heads (7.18e-04, rho=2.88e-03 k*=10)
- mono {and(X,X):1}
    - 8.15e-02 -> mono {ROLE:1}   via ROLE (8.15e-02, rho=4.28e-01 k*=10)
    - 2.49e-02 -> mono {Heads:1}   via Heads (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {Tails:1}   via Tails (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.62e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.62e-03, rho=2.59e-01 k*=10)
    - 1.62e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.62e-03, rho=2.59e-01 k*=10)
- mono {THEM(ME):1}
    - 2.49e-02 -> mono {Heads:1}   via Heads (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {Tails:1}   via Tails (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 2.68e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.68e-03, rho=4.28e-01 k*=10)
- mono {THEM(THEM):1}
    - 2.49e-02 -> mono {Heads:1}   via Heads (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {Tails:1}   via Tails (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 2.68e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.68e-03, rho=4.28e-01 k*=10)
