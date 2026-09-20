### arm=weak, n=5, game=zerosum, N=10, w=0.1, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 53, states 53, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 0.00e+00
mean payoff 0.0000, efficient 0.0000, deadweight loss 0.0000, mean bits in support 3.33

| pi | state |
|---|---|
| 0.2864 | mono {Heads:1} |
| 0.2314 | mono {X:1} |
| 0.2163 | mono {Tails:1} |
| 0.1840 | mono {ROLE:1} |
| 0.0491 | mono {not(ROLE):1} |
| 0.0066 | mono {or(X,ROLE):1} |
| 0.0057 | mono {and(X,ROLE):1} |
| 0.0041 | mono {or(X,X):1} |
| 0.0036 | mono {and(X,X):1} |
| 0.0022 | mono {THEM(ME):1} |
| 0.0022 | mono {THEM(THEM):1} |
| 0.0019 | mono {not(and(X,ROLE)):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Heads:1}
    - 2.49e-02 -> mono {Tails:1}   via Tails (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.10e-02 -> mono {ROLE:1}   via ROLE (1.10e-02, rho=5.77e-02 k*=10)
    - 7.45e-03 -> mono {not(ROLE):1}   via not(ROLE) (7.45e-03, rho=1.57e-01 k*=10)
    - 4.81e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (4.81e-04, rho=7.69e-02 k*=10)
    - 4.81e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (4.81e-04, rho=7.69e-02 k*=10)
- mono {X:1}
    - 2.49e-02 -> mono {Heads:1}   via Heads (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {Tails:1}   via Tails (2.49e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 6.26e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
    - 6.26e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
- mono {Tails:1}
    - 2.99e-02 -> mono {ROLE:1}   via ROLE (2.99e-02, rho=1.57e-01 k*=10)
    - 2.49e-02 -> mono {Heads:1}   via Heads (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 2.74e-03 -> mono {not(ROLE):1}   via not(ROLE) (2.74e-03, rho=5.77e-02 k*=10)
    - 7.94e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.94e-04, rho=1.27e-01 k*=10)
    - 7.94e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (7.94e-04, rho=1.27e-01 k*=10)
- mono {ROLE:1}
    - 3.90e-02 -> mono {Heads:1}   via Heads (3.90e-02, rho=1.57e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.44e-02 -> mono {Tails:1}   via Tails (1.44e-02, rho=5.77e-02 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 7.94e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.94e-04, rho=1.27e-01 k*=10)
    - 4.90e-04 -> mono {or(X,X):1}   via or(X,X) (4.90e-04, rho=1.27e-01 k*=10)
- mono {not(ROLE):1}
    - 3.90e-02 -> mono {Tails:1}   via Tails (3.90e-02, rho=1.57e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 1.44e-02 -> mono {Heads:1}   via Heads (1.44e-02, rho=5.77e-02 k*=10)
    - 7.94e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (7.94e-04, rho=1.27e-01 k*=10)
    - 4.90e-04 -> mono {and(X,X):1}   via and(X,X) (4.90e-04, rho=1.27e-01 k*=10)
- mono {or(X,ROLE):1}
    - 3.16e-02 -> mono {Heads:1}   via Heads (3.16e-02, rho=1.27e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.91e-02 -> mono {Tails:1}   via Tails (1.91e-02, rho=7.69e-02 k*=10)
    - 1.46e-02 -> mono {ROLE:1}   via ROLE (1.46e-02, rho=7.69e-02 k*=10)
    - 6.02e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.02e-03, rho=1.27e-01 k*=10)
    - 4.81e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (4.81e-04, rho=7.69e-02 k*=10)
- mono {and(X,ROLE):1}
    - 3.16e-02 -> mono {Heads:1}   via Heads (3.16e-02, rho=1.27e-01 k*=10)
    - 2.41e-02 -> mono {ROLE:1}   via ROLE (2.41e-02, rho=1.27e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.91e-02 -> mono {Tails:1}   via Tails (1.91e-02, rho=7.69e-02 k*=10)
    - 3.65e-03 -> mono {not(ROLE):1}   via not(ROLE) (3.65e-03, rho=7.69e-02 k*=10)
    - 7.94e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.94e-04, rho=1.27e-01 k*=10)
- mono {or(X,X):1}
    - 2.49e-02 -> mono {Heads:1}   via Heads (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {Tails:1}   via Tails (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.46e-02 -> mono {ROLE:1}   via ROLE (1.46e-02, rho=7.69e-02 k*=10)
    - 6.02e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.02e-03, rho=1.27e-01 k*=10)
    - 5.51e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (5.51e-04, rho=8.80e-02 k*=10)
- mono {and(X,X):1}
    - 2.49e-02 -> mono {Heads:1}   via Heads (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {Tails:1}   via Tails (2.49e-02, rho=1.00e-01 k*=10)
    - 2.41e-02 -> mono {ROLE:1}   via ROLE (2.41e-02, rho=1.27e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 3.65e-03 -> mono {not(ROLE):1}   via not(ROLE) (3.65e-03, rho=7.69e-02 k*=10)
    - 7.07e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.07e-04, rho=1.13e-01 k*=10)
- mono {THEM(ME):1}
    - 2.49e-02 -> mono {Heads:1}   via Heads (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {Tails:1}   via Tails (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 7.94e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (7.94e-04, rho=1.27e-01 k*=10)
- mono {THEM(THEM):1}
    - 2.49e-02 -> mono {Heads:1}   via Heads (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {Tails:1}   via Tails (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 7.94e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (7.94e-04, rho=1.27e-01 k*=10)
- mono {not(and(X,ROLE)):1}
    - 3.16e-02 -> mono {Tails:1}   via Tails (3.16e-02, rho=1.27e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.91e-02 -> mono {Heads:1}   via Heads (1.91e-02, rho=7.69e-02 k*=10)
    - 1.46e-02 -> mono {ROLE:1}   via ROLE (1.46e-02, rho=7.69e-02 k*=10)
    - 6.02e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.02e-03, rho=1.27e-01 k*=10)
    - 6.26e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
