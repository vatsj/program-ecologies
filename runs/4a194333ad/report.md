### arm=weak, n=5, game=zerosum, N=100, w=1.0, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 53, states 53, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 0.00e+00
mean payoff 0.0000, efficient 0.0000, deadweight loss 0.0000, mean bits in support 3.42

| pi | state |
|---|---|
| 0.4445 | mono {Heads:1} |
| 0.2314 | mono {X:1} |
| 0.1168 | mono {Tails:1} |
| 0.0921 | mono {ROLE:1} |
| 0.0828 | mono {not(ROLE):1} |
| 0.0067 | mono {or(X,X):1} |
| 0.0044 | mono {or(X,ROLE):1} |
| 0.0032 | mono {not(and(X,ROLE)):1} |
| 0.0030 | mono {and(X,ROLE):1} |
| 0.0021 | mono {THEM(ME):1} |
| 0.0021 | mono {THEM(THEM):1} |
| 0.0021 | mono {not(or(X,ROLE)):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Heads:1}
    - 3.02e-02 -> mono {not(ROLE):1}   via not(ROLE) (3.02e-02, rho=6.36e-01 k*=100)
    - 2.49e-03 -> mono {Tails:1}   via Tails (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 6.97e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (6.97e-04, rho=3.97e-01 k*=100)
    - 6.97e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (6.97e-04, rho=3.97e-01 k*=100)
    - 3.86e-05 -> mono {or(X,X):1}   via or(X,X) (3.86e-05, rho=1.00e-02 k*=100)
- mono {X:1}
    - 2.49e-03 -> mono {Heads:1}   via Heads (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {Tails:1}   via Tails (2.49e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
    - 6.26e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-05, rho=1.00e-02 k*=100)
    - 6.26e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.26e-05, rho=1.00e-02 k*=100)
- mono {Tails:1}
    - 1.21e-01 -> mono {ROLE:1}   via ROLE (1.21e-01, rho=6.36e-01 k*=100)
    - 2.49e-03 -> mono {Heads:1}   via Heads (2.49e-03, rho=1.00e-02 k*=100)
    - 2.48e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.48e-03, rho=3.97e-01 k*=100)
    - 2.48e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.48e-03, rho=3.97e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 4.88e-05 -> mono {or(X,or(X,ROLE)):1}   via or(X,or(X,ROLE)) (4.88e-05, rho=2.23e-01 k*=100)
- mono {ROLE:1}
    - 1.58e-01 -> mono {Heads:1}   via Heads (1.58e-01, rho=6.36e-01 k*=100)
    - 2.48e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.48e-03, rho=3.97e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.53e-03 -> mono {or(X,X):1}   via or(X,X) (1.53e-03, rho=3.97e-01 k*=100)
    - 6.97e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (6.97e-04, rho=3.97e-01 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
- mono {not(ROLE):1}
    - 1.58e-01 -> mono {Tails:1}   via Tails (1.58e-01, rho=6.36e-01 k*=100)
    - 2.48e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.48e-03, rho=3.97e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 1.53e-03 -> mono {and(X,X):1}   via and(X,X) (1.53e-03, rho=3.97e-01 k*=100)
    - 6.97e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (6.97e-04, rho=3.97e-01 k*=100)
- mono {or(X,X):1}
    - 1.88e-02 -> mono {not(ROLE):1}   via not(ROLE) (1.88e-02, rho=3.97e-01 k*=100)
    - 2.49e-03 -> mono {Heads:1}   via Heads (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {Tails:1}   via Tails (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 3.92e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (3.92e-04, rho=2.23e-01 k*=100)
    - 3.92e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (3.92e-04, rho=2.23e-01 k*=100)
- mono {or(X,ROLE):1}
    - 9.87e-02 -> mono {Heads:1}   via Heads (9.87e-02, rho=3.97e-01 k*=100)
    - 1.88e-02 -> mono {not(ROLE):1}   via not(ROLE) (1.88e-02, rho=3.97e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 8.64e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (8.64e-04, rho=3.97e-01 k*=100)
    - 8.64e-04 -> mono {THEM(ME):1}   via THEM(ME) (8.64e-04, rho=3.97e-01 k*=100)
    - 8.62e-04 -> mono {or(X,X):1}   via or(X,X) (8.62e-04, rho=2.23e-01 k*=100)
- mono {not(and(X,ROLE)):1}
    - 9.87e-02 -> mono {Tails:1}   via Tails (9.87e-02, rho=3.97e-01 k*=100)
    - 1.88e-02 -> mono {not(ROLE):1}   via not(ROLE) (1.88e-02, rho=3.97e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 8.62e-04 -> mono {and(X,X):1}   via and(X,X) (8.62e-04, rho=2.23e-01 k*=100)
    - 6.97e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (6.97e-04, rho=3.97e-01 k*=100)
    - 1.60e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.60e-04, rho=3.97e-01 k*=100)
- mono {and(X,ROLE):1}
    - 9.87e-02 -> mono {Heads:1}   via Heads (9.87e-02, rho=3.97e-01 k*=100)
    - 7.55e-02 -> mono {ROLE:1}   via ROLE (7.55e-02, rho=3.97e-01 k*=100)
    - 2.48e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.48e-03, rho=3.97e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 8.62e-04 -> mono {or(X,X):1}   via or(X,X) (8.62e-04, rho=2.23e-01 k*=100)
    - 1.60e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.60e-04, rho=3.97e-01 k*=100)
- mono {THEM(ME):1}
    - 2.49e-03 -> mono {Heads:1}   via Heads (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {Tails:1}   via Tails (2.49e-03, rho=1.00e-02 k*=100)
    - 2.48e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.48e-03, rho=3.97e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 6.97e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (6.97e-04, rho=3.97e-01 k*=100)
- mono {THEM(THEM):1}
    - 2.49e-03 -> mono {Heads:1}   via Heads (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {Tails:1}   via Tails (2.49e-03, rho=1.00e-02 k*=100)
    - 2.48e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.48e-03, rho=3.97e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 6.97e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (6.97e-04, rho=3.97e-01 k*=100)
- mono {not(or(X,ROLE)):1}
    - 9.87e-02 -> mono {Tails:1}   via Tails (9.87e-02, rho=3.97e-01 k*=100)
    - 7.55e-02 -> mono {ROLE:1}   via ROLE (7.55e-02, rho=3.97e-01 k*=100)
    - 2.48e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.48e-03, rho=3.97e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 8.64e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (8.64e-04, rho=3.97e-01 k*=100)
    - 8.64e-04 -> mono {THEM(ME):1}   via THEM(ME) (8.64e-04, rho=3.97e-01 k*=100)
