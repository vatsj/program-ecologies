### arm=weak, n=5, game=zerosum, N=100, w=1.0, x_on=True, role=True, mode=square

programs 902, classes 53, states 53, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 0.00e+00
mean payoff 0.0000, efficient 0.0000, deadweight loss 0.0000, mean bits in support 3.41

| pi | state |
|---|---|
| 0.4428 | mono {D:1} |
| 0.2314 | mono {X:1} |
| 0.1181 | mono {C:1} |
| 0.0936 | mono {ROLE:1} |
| 0.0821 | mono {not(ROLE):1} |
| 0.0066 | mono {and(X,X):1} |
| 0.0045 | mono {and(X,ROLE):1} |
| 0.0032 | mono {not(or(X,ROLE)):1} |
| 0.0030 | mono {or(X,ROLE):1} |
| 0.0021 | mono {THEM(THEM):1} |
| 0.0021 | mono {THEM(ME):1} |
| 0.0021 | mono {not(and(X,ROLE)):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.41e-02 -> mono {not(ROLE):1}   via not(ROLE) (2.41e-02, rho=5.08e-01 k*=100)
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 5.96e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (5.96e-04, rho=3.39e-01 k*=100)
    - 5.96e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (5.96e-04, rho=3.39e-01 k*=100)
    - 3.86e-05 -> mono {or(X,X):1}   via or(X,X) (3.86e-05, rho=1.00e-02 k*=100)
- mono {X:1}
    - 2.49e-03 -> mono {D:1}   via D (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
    - 6.26e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-05, rho=1.00e-02 k*=100)
    - 6.26e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.26e-05, rho=1.00e-02 k*=100)
- mono {C:1}
    - 9.67e-02 -> mono {ROLE:1}   via ROLE (9.67e-02, rho=5.08e-01 k*=100)
    - 2.49e-03 -> mono {D:1}   via D (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 2.12e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.12e-03, rho=3.39e-01 k*=100)
    - 2.12e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.12e-03, rho=3.39e-01 k*=100)
    - 4.45e-05 -> mono {or(X,or(X,ROLE)):1}   via or(X,or(X,ROLE)) (4.45e-05, rho=2.04e-01 k*=100)
- mono {ROLE:1}
    - 1.26e-01 -> mono {D:1}   via D (1.26e-01, rho=5.08e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 2.12e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.12e-03, rho=3.39e-01 k*=100)
    - 1.31e-03 -> mono {and(X,X):1}   via and(X,X) (1.31e-03, rho=3.39e-01 k*=100)
    - 5.96e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (5.96e-04, rho=3.39e-01 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
- mono {not(ROLE):1}
    - 1.26e-01 -> mono {C:1}   via C (1.26e-01, rho=5.08e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 2.12e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.12e-03, rho=3.39e-01 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 1.31e-03 -> mono {or(X,X):1}   via or(X,X) (1.31e-03, rho=3.39e-01 k*=100)
    - 5.96e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (5.96e-04, rho=3.39e-01 k*=100)
- mono {and(X,X):1}
    - 1.61e-02 -> mono {not(ROLE):1}   via not(ROLE) (1.61e-02, rho=3.39e-01 k*=100)
    - 2.49e-03 -> mono {D:1}   via D (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 3.58e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (3.58e-04, rho=2.04e-01 k*=100)
    - 3.58e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (3.58e-04, rho=2.04e-01 k*=100)
- mono {and(X,ROLE):1}
    - 8.44e-02 -> mono {D:1}   via D (8.44e-02, rho=3.39e-01 k*=100)
    - 1.61e-02 -> mono {not(ROLE):1}   via not(ROLE) (1.61e-02, rho=3.39e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 7.86e-04 -> mono {and(X,X):1}   via and(X,X) (7.86e-04, rho=2.04e-01 k*=100)
    - 7.39e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (7.39e-04, rho=3.39e-01 k*=100)
    - 7.39e-04 -> mono {THEM(ME):1}   via THEM(ME) (7.39e-04, rho=3.39e-01 k*=100)
- mono {not(or(X,ROLE)):1}
    - 8.44e-02 -> mono {C:1}   via C (8.44e-02, rho=3.39e-01 k*=100)
    - 1.61e-02 -> mono {not(ROLE):1}   via not(ROLE) (1.61e-02, rho=3.39e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 7.86e-04 -> mono {or(X,X):1}   via or(X,X) (7.86e-04, rho=2.04e-01 k*=100)
    - 5.96e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (5.96e-04, rho=3.39e-01 k*=100)
    - 1.37e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.37e-04, rho=3.39e-01 k*=100)
- mono {or(X,ROLE):1}
    - 8.44e-02 -> mono {D:1}   via D (8.44e-02, rho=3.39e-01 k*=100)
    - 6.45e-02 -> mono {ROLE:1}   via ROLE (6.45e-02, rho=3.39e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 2.12e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.12e-03, rho=3.39e-01 k*=100)
    - 7.86e-04 -> mono {and(X,X):1}   via and(X,X) (7.86e-04, rho=2.04e-01 k*=100)
    - 1.37e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.37e-04, rho=3.39e-01 k*=100)
- mono {THEM(THEM):1}
    - 2.49e-03 -> mono {D:1}   via D (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 2.12e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.12e-03, rho=3.39e-01 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 5.96e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (5.96e-04, rho=3.39e-01 k*=100)
- mono {THEM(ME):1}
    - 2.49e-03 -> mono {D:1}   via D (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 2.12e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.12e-03, rho=3.39e-01 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 5.96e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (5.96e-04, rho=3.39e-01 k*=100)
- mono {not(and(X,ROLE)):1}
    - 8.44e-02 -> mono {C:1}   via C (8.44e-02, rho=3.39e-01 k*=100)
    - 6.45e-02 -> mono {ROLE:1}   via ROLE (6.45e-02, rho=3.39e-01 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 2.12e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.12e-03, rho=3.39e-01 k*=100)
    - 7.86e-04 -> mono {or(X,X):1}   via or(X,X) (7.86e-04, rho=2.04e-01 k*=100)
    - 7.39e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (7.39e-04, rho=3.39e-01 k*=100)
