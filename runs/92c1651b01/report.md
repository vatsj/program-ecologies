### arm=weak, n=5, game=chicken, N=100, w=1.0, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 53, states 527, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 7.85e-09
mean payoff 0.5000, efficient 0.5000, deadweight loss 0.0000, mean bits in support 15.16

| pi | state |
|---|---|
| 0.9971 | mono {THEM(^not(ROLE)):1} |
| 0.0023 | mono {ROLE:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {THEM(^not(ROLE)):1}
    - 3.06e-13 -> mono {Swerve:1}   via Swerve (3.06e-13, rho=1.23e-12 k*=100)
    - 3.55e-15 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (3.55e-15, rho=8.82e-12 k*=100)
    - 3.62e-16 -> mono {or(X,or(X,ROLE)):1}   via or(X,or(X,ROLE)) (3.62e-16, rho=1.66e-12 k*=100)
    - 8.95e-17 -> mono {or(THEM(ME),Swerve):1}   via or(THEM(ME),Swerve) (8.95e-17, rho=1.23e-12 k*=100)
    - 9.39e-18 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (9.39e-18, rho=1.29e-13 k*=100)
    - 5.56e-23 -> mono {or(X,ROLE):1}   via or(X,ROLE) (5.56e-23, rho=8.89e-21 k*=100)
- mono {ROLE:1}
    - 3.64e-07 -> mono {not(THEM(^ROLE)):1}   via not(THEM(^ROLE)) (3.64e-07, rho=1.00e-02 k*=100)
    - 3.55e-15 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (3.55e-15, rho=8.82e-12 k*=100)
    - 3.55e-15 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (3.55e-15, rho=8.82e-12 k*=100)
    - 3.21e-16 -> mono {not(THEM(^Swerve)):1}   via not(THEM(^Swerve)) (3.21e-16, rho=8.82e-12 k*=100)
    - 2.55e-16 -> mono {or(ROLE,and(X,X)):1}   via or(ROLE,and(X,X)) (2.55e-16, rho=3.50e-12 k*=100)
    - 6.12e-25 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.12e-25, rho=9.78e-23 k*=100)
