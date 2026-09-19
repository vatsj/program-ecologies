### arm=weak, n=5, game=zerosum, N=10, w=1.0, x_on=True, role=True, mode=square

programs 902, classes 53, states 53, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 0.00e+00
mean payoff 0.0000, efficient 0.0000, deadweight loss 0.0000, mean bits in support 3.36

| pi | state |
|---|---|
| 0.3837 | mono {D:1} |
| 0.2314 | mono {X:1} |
| 0.1552 | mono {C:1} |
| 0.1325 | mono {ROLE:1} |
| 0.0656 | mono {not(ROLE):1} |
| 0.0060 | mono {and(X,ROLE):1} |
| 0.0054 | mono {and(X,X):1} |
| 0.0036 | mono {or(X,ROLE):1} |
| 0.0029 | mono {not(or(X,ROLE)):1} |
| 0.0027 | mono {or(X,X):1} |
| 0.0022 | mono {THEM(THEM):1} |
| 0.0022 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.75e-02 -> mono {not(ROLE):1}   via not(ROLE) (2.75e-02, rho=5.79e-01 k*=10)
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 6.91e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (6.91e-04, rho=3.93e-01 k*=10)
    - 6.91e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (6.91e-04, rho=3.93e-01 k*=10)
    - 3.86e-04 -> mono {or(X,X):1}   via or(X,X) (3.86e-04, rho=1.00e-01 k*=10)
- mono {X:1}
    - 2.49e-02 -> mono {D:1}   via D (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 6.26e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
    - 6.26e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
- mono {C:1}
    - 1.10e-01 -> mono {ROLE:1}   via ROLE (1.10e-01, rho=5.79e-01 k*=10)
    - 2.49e-02 -> mono {D:1}   via D (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 2.46e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.46e-03, rho=3.93e-01 k*=10)
    - 2.46e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.46e-03, rho=3.93e-01 k*=10)
    - 3.86e-04 -> mono {or(X,X):1}   via or(X,X) (3.86e-04, rho=1.00e-01 k*=10)
- mono {ROLE:1}
    - 1.44e-01 -> mono {D:1}   via D (1.44e-01, rho=5.79e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 2.46e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.46e-03, rho=3.93e-01 k*=10)
    - 1.52e-03 -> mono {and(X,X):1}   via and(X,X) (1.52e-03, rho=3.93e-01 k*=10)
    - 6.91e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (6.91e-04, rho=3.93e-01 k*=10)
- mono {not(ROLE):1}
    - 1.44e-01 -> mono {C:1}   via C (1.44e-01, rho=5.79e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 2.46e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.46e-03, rho=3.93e-01 k*=10)
    - 1.52e-03 -> mono {or(X,X):1}   via or(X,X) (1.52e-03, rho=3.93e-01 k*=10)
    - 6.91e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (6.91e-04, rho=3.93e-01 k*=10)
- mono {and(X,ROLE):1}
    - 9.80e-02 -> mono {D:1}   via D (9.80e-02, rho=3.93e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.87e-02 -> mono {not(ROLE):1}   via not(ROLE) (1.87e-02, rho=3.93e-01 k*=10)
    - 9.67e-04 -> mono {and(X,X):1}   via and(X,X) (9.67e-04, rho=2.50e-01 k*=10)
    - 8.58e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (8.58e-04, rho=3.93e-01 k*=10)
    - 8.58e-04 -> mono {THEM(ME):1}   via THEM(ME) (8.58e-04, rho=3.93e-01 k*=10)
- mono {and(X,X):1}
    - 2.49e-02 -> mono {D:1}   via D (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.87e-02 -> mono {not(ROLE):1}   via not(ROLE) (1.87e-02, rho=3.93e-01 k*=10)
    - 4.40e-04 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (4.40e-04, rho=2.50e-01 k*=10)
    - 4.40e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (4.40e-04, rho=2.50e-01 k*=10)
- mono {or(X,ROLE):1}
    - 9.80e-02 -> mono {D:1}   via D (9.80e-02, rho=3.93e-01 k*=10)
    - 7.49e-02 -> mono {ROLE:1}   via ROLE (7.49e-02, rho=3.93e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 2.46e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.46e-03, rho=3.93e-01 k*=10)
    - 9.67e-04 -> mono {and(X,X):1}   via and(X,X) (9.67e-04, rho=2.50e-01 k*=10)
    - 5.08e-04 -> mono {C:1}   via C (5.08e-04, rho=2.04e-03 k*=10)
- mono {not(or(X,ROLE)):1}
    - 9.80e-02 -> mono {C:1}   via C (9.80e-02, rho=3.93e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.87e-02 -> mono {not(ROLE):1}   via not(ROLE) (1.87e-02, rho=3.93e-01 k*=10)
    - 9.67e-04 -> mono {or(X,X):1}   via or(X,X) (9.67e-04, rho=2.50e-01 k*=10)
    - 6.91e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (6.91e-04, rho=3.93e-01 k*=10)
    - 6.26e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
- mono {or(X,X):1}
    - 7.49e-02 -> mono {ROLE:1}   via ROLE (7.49e-02, rho=3.93e-01 k*=10)
    - 2.49e-02 -> mono {D:1}   via D (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.57e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.57e-03, rho=2.50e-01 k*=10)
    - 1.57e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.57e-03, rho=2.50e-01 k*=10)
- mono {THEM(THEM):1}
    - 2.49e-02 -> mono {D:1}   via D (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 2.46e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.46e-03, rho=3.93e-01 k*=10)
- mono {THEM(ME):1}
    - 2.49e-02 -> mono {D:1}   via D (2.49e-02, rho=1.00e-01 k*=10)
    - 2.49e-02 -> mono {C:1}   via C (2.49e-02, rho=1.00e-01 k*=10)
    - 2.31e-02 -> mono {X:1}   via X (2.31e-02, rho=1.00e-01 k*=10)
    - 1.90e-02 -> mono {ROLE:1}   via ROLE (1.90e-02, rho=1.00e-01 k*=10)
    - 4.75e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-03, rho=1.00e-01 k*=10)
    - 2.46e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.46e-03, rho=3.93e-01 k*=10)
