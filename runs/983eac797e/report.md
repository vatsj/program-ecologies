### arm=weak, n=5, game=zerosum, N=10, w=0.3, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 53, states 53, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 0.00e+00
mean payoff 0.0000, efficient 0.0000, deadweight loss 0.0000, mean bits in support 3.35

| pi | state |
|---|---|
| 0.3411 | mono {Heads:1} |
| 0.2314 | mono {X:1} |
| 0.1805 | mono {Tails:1} |
| 0.1583 | mono {ROLE:1} |
| 0.0565 | mono {not(ROLE):1} |
| 0.0066 | mono {or(X,ROLE):1} |
| 0.0047 | mono {and(X,ROLE):1} |
| 0.0046 | mono {or(X,X):1} |
| 0.0032 | mono {and(X,X):1} |
| 0.0023 | mono {not(and(X,ROLE)):1} |
| 0.0022 | mono {THEM(ME):1} |
| 0.0022 | mono {THEM(THEM):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Heads:1}
    - 2.49e-02 -> mono {Tails:1}   via Tails (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.40e-02 -> mono {not(ROLE):1}   via not(ROLE) (1.40e-02, rho=2.94e-01 k*=10)
    - 2.79e-03 -> mono {ROLE:1}   via ROLE (2.79e-03, rho=1.46e-02 k*=10)
    - 3.86e-04 -> mono {or(X,X):1}   via or(X,X) (3.86e-04, rho=1.00e-01 k*=10)
    - 3.86e-04 -> mono {and(X,X):1}   via and(X,X) (3.86e-04, rho=1.00e-01 k*=10)
- mono {X:1}
    - 2.49e-02 -> mono {Heads:1}   via Heads (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {Tails:1}   via Tails (2.49e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 6.26e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
    - 6.26e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
- mono {Tails:1}
    - 5.60e-02 -> mono {ROLE:1}   via ROLE (5.60e-02, rho=2.94e-01 k*=10)
    - 2.49e-02 -> mono {Heads:1}   via Heads (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.18e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.18e-03, rho=1.89e-01 k*=10)
    - 1.18e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.18e-03, rho=1.89e-01 k*=10)
    - 6.95e-04 -> mono {not(ROLE):1}   via not(ROLE) (6.95e-04, rho=1.46e-02 k*=10)
- mono {ROLE:1}
    - 7.32e-02 -> mono {Heads:1}   via Heads (7.32e-02, rho=2.94e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 3.64e-03 -> mono {Tails:1}   via Tails (3.64e-03, rho=1.46e-02 k*=10)
    - 1.18e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.18e-03, rho=1.89e-01 k*=10)
    - 7.31e-04 -> mono {or(X,X):1}   via or(X,X) (7.31e-04, rho=1.89e-01 k*=10)
- mono {not(ROLE):1}
    - 7.32e-02 -> mono {Tails:1}   via Tails (7.32e-02, rho=2.94e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 3.64e-03 -> mono {Heads:1}   via Heads (3.64e-03, rho=1.46e-02 k*=10)
    - 1.18e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.18e-03, rho=1.89e-01 k*=10)
    - 7.31e-04 -> mono {and(X,X):1}   via and(X,X) (7.31e-04, rho=1.89e-01 k*=10)
- mono {or(X,ROLE):1}
    - 4.71e-02 -> mono {Heads:1}   via Heads (4.71e-02, rho=1.89e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.05e-02 -> mono {Tails:1}   via Tails (1.05e-02, rho=4.22e-02 k*=10)
    - 8.99e-03 -> mono {not(ROLE):1}   via not(ROLE) (8.99e-03, rho=1.89e-01 k*=10)
    - 8.04e-03 -> mono {ROLE:1}   via ROLE (8.04e-03, rho=4.22e-02 k*=10)
    - 5.46e-04 -> mono {or(X,X):1}   via or(X,X) (5.46e-04, rho=1.41e-01 k*=10)
- mono {and(X,ROLE):1}
    - 4.71e-02 -> mono {Heads:1}   via Heads (4.71e-02, rho=1.89e-01 k*=10)
    - 3.60e-02 -> mono {ROLE:1}   via ROLE (3.60e-02, rho=1.89e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.05e-02 -> mono {Tails:1}   via Tails (1.05e-02, rho=4.22e-02 k*=10)
    - 2.01e-03 -> mono {not(ROLE):1}   via not(ROLE) (2.01e-03, rho=4.22e-02 k*=10)
    - 1.18e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.18e-03, rho=1.89e-01 k*=10)
- mono {or(X,X):1}
    - 2.49e-02 -> mono {Heads:1}   via Heads (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {Tails:1}   via Tails (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 8.99e-03 -> mono {not(ROLE):1}   via not(ROLE) (8.99e-03, rho=1.89e-01 k*=10)
    - 8.04e-03 -> mono {ROLE:1}   via ROLE (8.04e-03, rho=4.22e-02 k*=10)
    - 4.18e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (4.18e-04, rho=6.68e-02 k*=10)
- mono {and(X,X):1}
    - 3.60e-02 -> mono {ROLE:1}   via ROLE (3.60e-02, rho=1.89e-01 k*=10)
    - 2.49e-02 -> mono {Heads:1}   via Heads (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {Tails:1}   via Tails (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 2.01e-03 -> mono {not(ROLE):1}   via not(ROLE) (2.01e-03, rho=4.22e-02 k*=10)
    - 8.85e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (8.85e-04, rho=1.41e-01 k*=10)
- mono {not(and(X,ROLE)):1}
    - 4.71e-02 -> mono {Tails:1}   via Tails (4.71e-02, rho=1.89e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.05e-02 -> mono {Heads:1}   via Heads (1.05e-02, rho=4.22e-02 k*=10)
    - 8.99e-03 -> mono {not(ROLE):1}   via not(ROLE) (8.99e-03, rho=1.89e-01 k*=10)
    - 8.04e-03 -> mono {ROLE:1}   via ROLE (8.04e-03, rho=4.22e-02 k*=10)
    - 6.26e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
- mono {THEM(ME):1}
    - 2.49e-02 -> mono {Heads:1}   via Heads (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {Tails:1}   via Tails (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 1.18e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.18e-03, rho=1.89e-01 k*=10)
- mono {THEM(THEM):1}
    - 2.49e-02 -> mono {Heads:1}   via Heads (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {Tails:1}   via Tails (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 1.18e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.18e-03, rho=1.89e-01 k*=10)
