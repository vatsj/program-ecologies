### arm=weak, n=5, game=zerosum, N=100, w=0.1, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 53, states 53, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 0.00e+00
mean payoff 0.0000, efficient 0.0000, deadweight loss 0.0000, mean bits in support 3.37

| pi | state |
|---|---|
| 0.4054 | mono {Heads:1} |
| 0.2314 | mono {X:1} |
| 0.1417 | mono {Tails:1} |
| 0.1190 | mono {ROLE:1} |
| 0.0713 | mono {not(ROLE):1} |
| 0.0056 | mono {or(X,ROLE):1} |
| 0.0055 | mono {or(X,X):1} |
| 0.0034 | mono {and(X,ROLE):1} |
| 0.0029 | mono {not(and(X,ROLE)):1} |
| 0.0026 | mono {and(X,X):1} |
| 0.0022 | mono {THEM(ME):1} |
| 0.0022 | mono {THEM(THEM):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Heads:1}
    - 4.56e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.56e-03, rho=9.61e-02 k*=100)
    - 2.49e-03 -> mono {Tails:1}   via Tails (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 8.71e-05 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (8.71e-05, rho=4.96e-02 k*=100)
    - 8.71e-05 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (8.71e-05, rho=4.96e-02 k*=100)
    - 3.86e-05 -> mono {or(X,X):1}   via or(X,X) (3.86e-05, rho=1.00e-02 k*=100)
- mono {X:1}
    - 2.49e-03 -> mono {Heads:1}   via Heads (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {Tails:1}   via Tails (2.49e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
    - 6.26e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-05, rho=1.00e-02 k*=100)
    - 6.26e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.26e-05, rho=1.00e-02 k*=100)
- mono {Tails:1}
    - 1.83e-02 -> mono {ROLE:1}   via ROLE (1.83e-02, rho=9.61e-02 k*=100)
    - 2.49e-03 -> mono {Heads:1}   via Heads (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 3.10e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (3.10e-04, rho=4.96e-02 k*=100)
    - 3.10e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (3.10e-04, rho=4.96e-02 k*=100)
    - 3.86e-05 -> mono {or(X,X):1}   via or(X,X) (3.86e-05, rho=1.00e-02 k*=100)
- mono {ROLE:1}
    - 2.39e-02 -> mono {Heads:1}   via Heads (2.39e-02, rho=9.61e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
    - 3.10e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (3.10e-04, rho=4.96e-02 k*=100)
    - 1.91e-04 -> mono {or(X,X):1}   via or(X,X) (1.91e-04, rho=4.96e-02 k*=100)
    - 8.71e-05 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (8.71e-05, rho=4.96e-02 k*=100)
- mono {not(ROLE):1}
    - 2.39e-02 -> mono {Tails:1}   via Tails (2.39e-02, rho=9.61e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 3.10e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (3.10e-04, rho=4.96e-02 k*=100)
    - 1.91e-04 -> mono {and(X,X):1}   via and(X,X) (1.91e-04, rho=4.96e-02 k*=100)
    - 8.71e-05 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (8.71e-05, rho=4.96e-02 k*=100)
- mono {or(X,ROLE):1}
    - 1.23e-02 -> mono {Heads:1}   via Heads (1.23e-02, rho=4.96e-02 k*=100)
    - 2.35e-03 -> mono {not(ROLE):1}   via not(ROLE) (2.35e-03, rho=4.96e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.08e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (1.08e-04, rho=4.96e-02 k*=100)
    - 1.08e-04 -> mono {THEM(ME):1}   via THEM(ME) (1.08e-04, rho=4.96e-02 k*=100)
    - 1.05e-04 -> mono {or(X,X):1}   via or(X,X) (1.05e-04, rho=2.71e-02 k*=100)
- mono {or(X,X):1}
    - 2.49e-03 -> mono {Heads:1}   via Heads (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {Tails:1}   via Tails (2.49e-03, rho=1.00e-02 k*=100)
    - 2.35e-03 -> mono {not(ROLE):1}   via not(ROLE) (2.35e-03, rho=4.96e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 6.36e-05 -> mono {ROLE:1}   via ROLE (6.36e-05, rho=3.34e-04 k*=100)
    - 4.76e-05 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (4.76e-05, rho=2.71e-02 k*=100)
- mono {and(X,ROLE):1}
    - 1.23e-02 -> mono {Heads:1}   via Heads (1.23e-02, rho=4.96e-02 k*=100)
    - 9.44e-03 -> mono {ROLE:1}   via ROLE (9.44e-03, rho=4.96e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 3.10e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (3.10e-04, rho=4.96e-02 k*=100)
    - 1.05e-04 -> mono {or(X,X):1}   via or(X,X) (1.05e-04, rho=2.71e-02 k*=100)
    - 8.32e-05 -> mono {Tails:1}   via Tails (8.32e-05, rho=3.34e-04 k*=100)
- mono {not(and(X,ROLE)):1}
    - 1.23e-02 -> mono {Tails:1}   via Tails (1.23e-02, rho=4.96e-02 k*=100)
    - 2.35e-03 -> mono {not(ROLE):1}   via not(ROLE) (2.35e-03, rho=4.96e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.05e-04 -> mono {and(X,X):1}   via and(X,X) (1.05e-04, rho=2.71e-02 k*=100)
    - 8.71e-05 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (8.71e-05, rho=4.96e-02 k*=100)
    - 8.32e-05 -> mono {Heads:1}   via Heads (8.32e-05, rho=3.34e-04 k*=100)
- mono {and(X,X):1}
    - 9.44e-03 -> mono {ROLE:1}   via ROLE (9.44e-03, rho=4.96e-02 k*=100)
    - 2.49e-03 -> mono {Heads:1}   via Heads (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {Tails:1}   via Tails (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.70e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.70e-04, rho=2.71e-02 k*=100)
    - 1.70e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.70e-04, rho=2.71e-02 k*=100)
- mono {THEM(ME):1}
    - 2.49e-03 -> mono {Heads:1}   via Heads (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {Tails:1}   via Tails (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
    - 3.10e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (3.10e-04, rho=4.96e-02 k*=100)
- mono {THEM(THEM):1}
    - 2.49e-03 -> mono {Heads:1}   via Heads (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {Tails:1}   via Tails (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
    - 3.10e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (3.10e-04, rho=4.96e-02 k*=100)
