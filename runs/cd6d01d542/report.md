### arm=weak, n=5, game=chicken, N=100, w=1.0, x_on=True, role=True, mode=square

programs 902, classes 53, states 546, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 2.07e-07
mean payoff 0.4992, efficient 0.5000, deadweight loss 0.0008, mean bits in support 14.36

| pi | state |
|---|---|
| 0.9269 | mono {THEM(^not(ROLE)):1} |
| 0.0564 | mono {ROLE:1} |
| 0.0138 | mono {not(ROLE):1} |
| 0.0018 | poly {D:0.14, not(THEM(^ROLE)):0.86} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {THEM(^not(ROLE)):1}
    - 7.98e-12 -> mono {C:1}   via C (7.98e-12, rho=3.21e-11 k*=100)
    - 1.18e-12 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.18e-12, rho=2.94e-09 k*=100)
    - 2.34e-15 -> mono {or(THEM(ME),C):1}   via or(THEM(ME),C) (2.34e-15, rho=3.21e-11 k*=100)
    - 1.95e-15 -> mono {or(X,or(X,ROLE)):1}   via or(X,or(X,ROLE)) (1.95e-15, rho=8.90e-12 k*=100)
    - 1.69e-16 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (1.69e-16, rho=2.32e-12 k*=100)
    - 1.91e-28 -> mono {or(X,X):1}   via or(X,X) (1.91e-28, rho=4.94e-26 k*=100)
- mono {ROLE:1}
    - 3.64e-07 -> mono {not(THEM(^ROLE)):1}   via not(THEM(^ROLE)) (3.64e-07, rho=1.00e-02 k*=100)
    - 1.18e-12 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.18e-12, rho=2.94e-09 k*=100)
    - 1.18e-12 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.18e-12, rho=2.94e-09 k*=100)
    - 3.27e-13 -> mono {or(ROLE,and(X,X)):1}   via or(ROLE,and(X,X)) (3.27e-13, rho=4.49e-09 k*=100)
    - 1.07e-13 -> mono {not(THEM(^C)):1}   via not(THEM(^C)) (1.07e-13, rho=2.94e-09 k*=100)
    - 2.08e-19 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.08e-19, rho=3.32e-17 k*=100)
- mono {not(ROLE):1}
    - 3.64e-07 -> mono {not(THEM(^ROLE)):1}   via not(THEM(^ROLE)) (3.64e-07, rho=1.00e-02 k*=100)
    - 1.18e-12 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.18e-12, rho=2.94e-09 k*=100)
    - 1.18e-12 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.18e-12, rho=2.94e-09 k*=100)
    - 1.07e-13 -> mono {not(THEM(^C)):1}   via not(THEM(^C)) (1.07e-13, rho=2.94e-09 k*=100)
    - 5.83e-20 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (5.83e-20, rho=3.32e-17 k*=100)
    - 6.00e-39 -> mono {C:1}   via C (6.00e-39, rho=2.41e-38 k*=100)
- poly {D:0.14, not(THEM(^ROLE)):0.86}
    - 3.64e-05 -> poly {D:0.13, not(THEM(^ROLE)):0.86, and(ROLE,THEM(THEM)):0.01}   via and(ROLE,THEM(THEM)) (3.64e-05, rho=1.00e+00 k*=1)
    - 4.49e-06 -> mono {and(THEM(THEM),ROLE):1}   via and(THEM(THEM),ROLE) (4.49e-06, rho=1.23e-01 k*=100)
    - 4.49e-06 -> mono {and(THEM(THEM),D):1}   via and(THEM(THEM),D) (4.49e-06, rho=1.23e-01 k*=100)
    - 4.49e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (4.49e-06, rho=1.23e-01 k*=100)
    - 1.34e-09 -> mono {not(THEM(^ROLE)):1}   via ROLE (1.07e-09, rho=1.11e-08 k*=49), not(ROLE) (2.68e-10, rho=1.11e-08 k*=49), THEM(^ROLE) (1.18e-29, rho=5.90e-26 k*=50)
    - 1.04e-09 -> mono {ROLE:1}   via ROLE (1.04e-09, rho=1.11e-08 k*=49)
