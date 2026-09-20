### arm=weak, n=5, game=chicken, N=100, w=0.3, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 53, states 526, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 9.19e-07
mean payoff 0.4983, efficient 0.5000, deadweight loss 0.0017, mean bits in support 3.47

| pi | state |
|---|---|
| 0.7946 | mono {ROLE:1} |
| 0.1983 | mono {not(ROLE):1} |
| 0.0058 | poly {Straight:0.14, not(THEM(^ROLE)):0.86} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 3.64e-07 -> mono {not(THEM(^ROLE)):1}   via not(THEM(^ROLE)) (3.64e-07, rho=1.00e-02 k*=100)
    - 3.31e-08 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (3.31e-08, rho=8.21e-05 k*=100)
    - 3.31e-08 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (3.31e-08, rho=8.21e-05 k*=100)
    - 3.04e-09 -> mono {or(ROLE,and(X,X)):1}   via or(ROLE,and(X,X)) (3.04e-09, rho=4.17e-05 k*=100)
    - 2.99e-09 -> mono {not(THEM(^Swerve)):1}   via not(THEM(^Swerve)) (2.99e-09, rho=8.21e-05 k*=100)
    - 2.89e-10 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.89e-10, rho=4.61e-08 k*=100)
- mono {not(ROLE):1}
    - 3.64e-07 -> mono {not(THEM(^ROLE)):1}   via not(THEM(^ROLE)) (3.64e-07, rho=1.00e-02 k*=100)
    - 3.31e-08 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (3.31e-08, rho=8.21e-05 k*=100)
    - 3.31e-08 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (3.31e-08, rho=8.21e-05 k*=100)
    - 2.99e-09 -> mono {not(THEM(^Swerve)):1}   via not(THEM(^Swerve)) (2.99e-09, rho=8.21e-05 k*=100)
    - 8.11e-11 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (8.11e-11, rho=4.61e-08 k*=100)
    - 7.05e-15 -> mono {Swerve:1}   via Swerve (7.05e-15, rho=2.83e-14 k*=100)
- poly {Straight:0.14, not(THEM(^ROLE)):0.86}
    - 4.05e-05 -> mono {ROLE:1}   via ROLE (4.05e-05, rho=2.13e-04 k*=100)
    - 3.64e-05 -> poly {Straight:0.13, not(THEM(^ROLE)):0.86, and(ROLE,THEM(THEM)):0.01}   via and(ROLE,THEM(THEM)) (3.64e-05, rho=1.00e+00 k*=1)
    - 1.01e-05 -> mono {not(ROLE):1}   via not(ROLE) (1.01e-05, rho=2.13e-04 k*=100)
    - 2.58e-06 -> mono {and(THEM(THEM),ROLE):1}   via and(THEM(THEM),ROLE) (2.58e-06, rho=7.09e-02 k*=100)
    - 2.58e-06 -> mono {and(THEM(THEM),Straight):1}   via and(THEM(THEM),Straight) (2.58e-06, rho=7.09e-02 k*=100)
    - 2.58e-06 -> mono {and(THEM(ME),Straight):1}   via and(THEM(ME),Straight) (2.58e-06, rho=7.09e-02 k*=100)
