### arm=weak, n=5, game=zerosum, N=100, w=0.3, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 53, states 53, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 0.00e+00
mean payoff 0.0000, efficient 0.0000, deadweight loss 0.0000, mean bits in support 3.40

| pi | state |
|---|---|
| 0.4334 | mono {Heads:1} |
| 0.2314 | mono {X:1} |
| 0.1243 | mono {Tails:1} |
| 0.1003 | mono {ROLE:1} |
| 0.0793 | mono {not(ROLE):1} |
| 0.0061 | mono {or(X,X):1} |
| 0.0048 | mono {or(X,ROLE):1} |
| 0.0031 | mono {not(and(X,ROLE)):1} |
| 0.0031 | mono {and(X,ROLE):1} |
| 0.0022 | mono {THEM(ME):1} |
| 0.0021 | mono {THEM(THEM):1} |
| 0.0021 | mono {and(X,X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Heads:1}
    - 1.24e-02 -> mono {not(ROLE):1}   via not(ROLE) (1.24e-02, rho=2.61e-01 k*=100)
    - 2.49e-03 -> mono {Tails:1}   via Tails (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 2.47e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (2.47e-04, rho=1.41e-01 k*=100)
    - 2.47e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (2.47e-04, rho=1.41e-01 k*=100)
    - 3.86e-05 -> mono {or(X,X):1}   via or(X,X) (3.86e-05, rho=1.00e-02 k*=100)
- mono {X:1}
    - 2.49e-03 -> mono {Heads:1}   via Heads (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {Tails:1}   via Tails (2.49e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
    - 6.26e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-05, rho=1.00e-02 k*=100)
    - 6.26e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.26e-05, rho=1.00e-02 k*=100)
- mono {Tails:1}
    - 4.98e-02 -> mono {ROLE:1}   via ROLE (4.98e-02, rho=2.61e-01 k*=100)
    - 2.49e-03 -> mono {Heads:1}   via Heads (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 8.80e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (8.80e-04, rho=1.41e-01 k*=100)
    - 8.80e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (8.80e-04, rho=1.41e-01 k*=100)
    - 3.86e-05 -> mono {or(X,X):1}   via or(X,X) (3.86e-05, rho=1.00e-02 k*=100)
- mono {ROLE:1}
    - 6.51e-02 -> mono {Heads:1}   via Heads (6.51e-02, rho=2.61e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 8.80e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (8.80e-04, rho=1.41e-01 k*=100)
    - 5.43e-04 -> mono {or(X,X):1}   via or(X,X) (5.43e-04, rho=1.41e-01 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
    - 2.47e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (2.47e-04, rho=1.41e-01 k*=100)
- mono {not(ROLE):1}
    - 6.51e-02 -> mono {Tails:1}   via Tails (6.51e-02, rho=2.61e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 8.80e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (8.80e-04, rho=1.41e-01 k*=100)
    - 5.43e-04 -> mono {and(X,X):1}   via and(X,X) (5.43e-04, rho=1.41e-01 k*=100)
    - 2.47e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (2.47e-04, rho=1.41e-01 k*=100)
- mono {or(X,X):1}
    - 6.68e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.68e-03, rho=1.41e-01 k*=100)
    - 2.49e-03 -> mono {Heads:1}   via Heads (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {Tails:1}   via Tails (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.28e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (1.28e-04, rho=7.30e-02 k*=100)
    - 1.28e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (1.28e-04, rho=7.30e-02 k*=100)
- mono {or(X,ROLE):1}
    - 3.50e-02 -> mono {Heads:1}   via Heads (3.50e-02, rho=1.41e-01 k*=100)
    - 6.68e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.68e-03, rho=1.41e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 3.06e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.06e-04, rho=1.41e-01 k*=100)
    - 3.06e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.06e-04, rho=1.41e-01 k*=100)
    - 2.82e-04 -> mono {or(X,X):1}   via or(X,X) (2.82e-04, rho=7.30e-02 k*=100)
- mono {not(and(X,ROLE)):1}
    - 3.50e-02 -> mono {Tails:1}   via Tails (3.50e-02, rho=1.41e-01 k*=100)
    - 6.68e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.68e-03, rho=1.41e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 2.82e-04 -> mono {and(X,X):1}   via and(X,X) (2.82e-04, rho=7.30e-02 k*=100)
    - 2.47e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (2.47e-04, rho=1.41e-01 k*=100)
    - 6.26e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.26e-05, rho=1.00e-02 k*=100)
- mono {and(X,ROLE):1}
    - 3.50e-02 -> mono {Heads:1}   via Heads (3.50e-02, rho=1.41e-01 k*=100)
    - 2.68e-02 -> mono {ROLE:1}   via ROLE (2.68e-02, rho=1.41e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 8.80e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (8.80e-04, rho=1.41e-01 k*=100)
    - 2.82e-04 -> mono {or(X,X):1}   via or(X,X) (2.82e-04, rho=7.30e-02 k*=100)
    - 5.66e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (5.66e-05, rho=1.41e-01 k*=100)
- mono {THEM(ME):1}
    - 2.49e-03 -> mono {Heads:1}   via Heads (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {Tails:1}   via Tails (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 8.80e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (8.80e-04, rho=1.41e-01 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
- mono {THEM(THEM):1}
    - 2.49e-03 -> mono {Heads:1}   via Heads (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {Tails:1}   via Tails (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 8.80e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (8.80e-04, rho=1.41e-01 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
- mono {and(X,X):1}
    - 2.68e-02 -> mono {ROLE:1}   via ROLE (2.68e-02, rho=1.41e-01 k*=100)
    - 2.49e-03 -> mono {Heads:1}   via Heads (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {Tails:1}   via Tails (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 4.57e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (4.57e-04, rho=7.30e-02 k*=100)
    - 4.57e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (4.57e-04, rho=7.30e-02 k*=100)
