### arm=weak, n=5, game=chicken, N=10, w=1.0, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 53, states 480, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 5.22e-05
mean payoff 0.4985, efficient 0.5000, deadweight loss 0.0015, mean bits in support 3.42

| pi | state |
|---|---|
| 0.7988 | mono {ROLE:1} |
| 0.1986 | mono {not(ROLE):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 2.23e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.23e-05, rho=3.57e-03 k*=10)
    - 1.61e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.61e-05, rho=4.00e-02 k*=10)
    - 1.61e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.61e-05, rho=4.00e-02 k*=10)
    - 1.22e-05 -> mono {Swerve:1}   via Swerve (1.22e-05, rho=4.88e-05 k*=10)
    - 3.64e-06 -> mono {not(THEM(^ROLE)):1}   via not(THEM(^ROLE)) (3.64e-06, rho=1.00e-01 k*=10)
    - 1.69e-06 -> mono {or(ROLE,and(X,X)):1}   via or(ROLE,and(X,X)) (1.69e-06, rho=2.32e-02 k*=10)
- mono {not(ROLE):1}
    - 1.61e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.61e-05, rho=4.00e-02 k*=10)
    - 1.61e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.61e-05, rho=4.00e-02 k*=10)
    - 1.22e-05 -> mono {Swerve:1}   via Swerve (1.22e-05, rho=4.88e-05 k*=10)
    - 6.27e-06 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (6.27e-06, rho=3.57e-03 k*=10)
    - 3.64e-06 -> mono {not(THEM(^ROLE)):1}   via not(THEM(^ROLE)) (3.64e-06, rho=1.00e-01 k*=10)
    - 1.46e-06 -> mono {not(THEM(^Swerve)):1}   via not(THEM(^Swerve)) (1.46e-06, rho=4.00e-02 k*=10)
