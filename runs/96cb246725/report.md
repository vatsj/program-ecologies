### arm=weak, n=5, game=chicken, N=100, w=0.1, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 53, states 534, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 5.71e-06
mean payoff 0.4989, efficient 0.5000, deadweight loss 0.0011, mean bits in support 3.41

| pi | state |
|---|---|
| 0.7991 | mono {ROLE:1} |
| 0.1988 | mono {not(ROLE):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 2.13e-06 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.13e-06, rho=3.41e-04 k*=100)
    - 1.32e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.32e-06, rho=3.27e-03 k*=100)
    - 1.32e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.32e-06, rho=3.27e-03 k*=100)
    - 1.14e-06 -> mono {Swerve:1}   via Swerve (1.14e-06, rho=4.56e-06 k*=100)
    - 3.64e-07 -> mono {not(THEM(^ROLE)):1}   via not(THEM(^ROLE)) (3.64e-07, rho=1.00e-02 k*=100)
    - 1.64e-07 -> mono {or(ROLE,and(X,X)):1}   via or(ROLE,and(X,X)) (1.64e-07, rho=2.24e-03 k*=100)
- mono {not(ROLE):1}
    - 1.32e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.32e-06, rho=3.27e-03 k*=100)
    - 1.32e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.32e-06, rho=3.27e-03 k*=100)
    - 1.14e-06 -> mono {Swerve:1}   via Swerve (1.14e-06, rho=4.56e-06 k*=100)
    - 5.99e-07 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (5.99e-07, rho=3.41e-04 k*=100)
    - 3.64e-07 -> mono {not(THEM(^ROLE)):1}   via not(THEM(^ROLE)) (3.64e-07, rho=1.00e-02 k*=100)
    - 1.19e-07 -> mono {not(THEM(^Swerve)):1}   via not(THEM(^Swerve)) (1.19e-07, rho=3.27e-03 k*=100)
