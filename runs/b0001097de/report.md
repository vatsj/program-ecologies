### arm=weak, n=5, game=demand, N=100, w=1.0, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 53, states 723, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 1.26e-05
mean payoff 0.4999, efficient 0.5000, deadweight loss 0.0001, mean bits in support 3.41

| pi | state |
|---|---|
| 0.7988 | mono {ROLE:1} |
| 0.1993 | mono {not(ROLE):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 4.48e-06 -> mono {X:1}   via X (4.48e-06, rho=1.94e-05 k*=100)
    - 2.18e-06 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.18e-06, rho=3.48e-04 k*=100)
    - 1.19e-06 -> mono {Low:1}   via Low (1.19e-06, rho=4.77e-06 k*=100)
    - 8.80e-07 -> mono {not(ROLE):1}   via not(ROLE) (8.80e-07, rho=1.85e-05 k*=100)
    - 3.64e-07 -> mono {not(THEM(^ROLE)):1}   via not(THEM(^ROLE)) (3.64e-07, rho=1.00e-02 k*=100)
    - 2.46e-07 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (2.46e-07, rho=6.11e-04 k*=100)
- mono {not(ROLE):1}
    - 4.48e-06 -> mono {X:1}   via X (4.48e-06, rho=1.94e-05 k*=100)
    - 3.53e-06 -> mono {ROLE:1}   via ROLE (3.53e-06, rho=1.85e-05 k*=100)
    - 1.19e-06 -> mono {Low:1}   via Low (1.19e-06, rho=4.77e-06 k*=100)
    - 6.11e-07 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (6.11e-07, rho=3.48e-04 k*=100)
    - 3.64e-07 -> mono {not(THEM(^ROLE)):1}   via not(THEM(^ROLE)) (3.64e-07, rho=1.00e-02 k*=100)
    - 2.46e-07 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (2.46e-07, rho=6.11e-04 k*=100)
