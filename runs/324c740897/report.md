### arm=strong, n=6, game=stag, N=100, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 1726, classes 21, states 23, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 5.07e-12
mean payoff 3.9919, efficient 4.0000, deadweight loss 0.0081, mean bits in support 2.59

| pi | state |
|---|---|
| 0.9917 | mono {Stag:1} |
| 0.0081 | mono {Hare:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Stag:1}
    - 9.32e-07 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (9.32e-07, rho=1.00e-02 k*=100)
    - 1.84e-07 -> mono {Hare:1}   via Hare (1.84e-07, rho=5.55e-07 k*=100)
    - 1.11e-07 -> mono {X:1}   via X (1.11e-07, rho=3.54e-07 k*=100)
    - 3.76e-09 -> mono {and(X,X):1}   via and(X,X) (3.76e-09, rho=4.71e-07 k*=100)
    - 2.88e-09 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (2.88e-09, rho=9.56e-06 k*=100)
    - 2.75e-09 -> mono {or(X,X):1}   via or(X,X) (2.75e-09, rho=3.45e-07 k*=100)
- mono {Hare:1}
    - 3.84e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-05, rho=1.00e-02 k*=100)
    - 1.22e-06 -> mono {and(THEM(ME),Hare):1}   via and(THEM(ME),Hare) (1.22e-06, rho=1.00e-02 k*=100)
    - 9.32e-07 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (9.32e-07, rho=1.00e-02 k*=100)
    - 9.32e-07 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (9.32e-07, rho=1.00e-02 k*=100)
    - 1.31e-19 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.31e-19, rho=4.35e-16 k*=100)
    - 1.25e-25 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (1.25e-25, rho=1.34e-21 k*=100)
