### arm=strong, n=6, game=stag, N=100, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 1726, classes 21, states 23, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 9.56e-11
mean payoff 3.0544, efficient 4.0000, deadweight loss 0.9456, mean bits in support 2.60

| pi | state |
|---|---|
| 0.9439 | mono {Hare:1} |
| 0.0545 | mono {Stag:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Hare:1}
    - 3.84e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-05, rho=1.00e-02 k*=100)
    - 1.22e-06 -> mono {and(THEM(ME),Hare):1}   via and(THEM(ME),Hare) (1.22e-06, rho=1.00e-02 k*=100)
    - 9.32e-07 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (9.32e-07, rho=1.00e-02 k*=100)
    - 9.32e-07 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (9.32e-07, rho=1.00e-02 k*=100)
    - 1.00e-09 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.00e-09, rho=3.33e-06 k*=100)
    - 9.58e-12 -> mono {and(X,X):1}   via and(X,X) (9.58e-12, rho=1.20e-09 k*=100)
- mono {Stag:1}
    - 4.14e-04 -> mono {Hare:1}   via Hare (4.14e-04, rho=1.25e-03 k*=100)
    - 2.12e-04 -> mono {X:1}   via X (2.12e-04, rho=6.73e-04 k*=100)
    - 7.75e-06 -> mono {and(X,X):1}   via and(X,X) (7.75e-06, rho=9.71e-04 k*=100)
    - 5.13e-06 -> mono {or(X,X):1}   via or(X,X) (5.13e-06, rho=6.43e-04 k*=100)
    - 1.06e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.06e-06, rho=1.25e-03 k*=100)
    - 9.32e-07 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (9.32e-07, rho=1.00e-02 k*=100)
