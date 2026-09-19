### arm=weak, n=5, game=chicken, N=100, w=0.1, x_on=True, role=True, mode=square

programs 902, classes 53, states 553, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 6.61e-06
mean payoff 0.4988, efficient 0.5000, deadweight loss 0.0012, mean bits in support 3.41

| pi | state |
|---|---|
| 0.7990 | mono {ROLE:1} |
| 0.1987 | mono {not(ROLE):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 2.45e-06 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.45e-06, rho=3.91e-04 k*=100)
    - 1.38e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.38e-06, rho=3.44e-03 k*=100)
    - 1.38e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.38e-06, rho=3.44e-03 k*=100)
    - 1.38e-06 -> mono {C:1}   via C (1.38e-06, rho=5.53e-06 k*=100)
    - 3.64e-07 -> mono {not(THEM(^ROLE)):1}   via not(THEM(^ROLE)) (3.64e-07, rho=1.00e-02 k*=100)
    - 1.75e-07 -> mono {or(ROLE,and(X,X)):1}   via or(ROLE,and(X,X)) (1.75e-07, rho=2.41e-03 k*=100)
- mono {not(ROLE):1}
    - 1.38e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.38e-06, rho=3.44e-03 k*=100)
    - 1.38e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.38e-06, rho=3.44e-03 k*=100)
    - 1.38e-06 -> mono {C:1}   via C (1.38e-06, rho=5.53e-06 k*=100)
    - 6.87e-07 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (6.87e-07, rho=3.91e-04 k*=100)
    - 3.64e-07 -> mono {not(THEM(^ROLE)):1}   via not(THEM(^ROLE)) (3.64e-07, rho=1.00e-02 k*=100)
    - 1.25e-07 -> mono {not(THEM(^C)):1}   via not(THEM(^C)) (1.25e-07, rho=3.44e-03 k*=100)
