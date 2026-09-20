### arm=strong, n=6, game=stag, N=1000, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 1726, classes 21, states 23, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 3.31e-21
mean payoff 4.0000, efficient 4.0000, deadweight loss 0.0000, mean bits in support 2.59

| pi | state |
|---|---|
| 0.9997 | mono {Stag:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Stag:1}
    - 9.32e-08 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (9.32e-08, rho=1.00e-03 k*=1000)
    - 1.27e-17 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (1.27e-17, rho=1.37e-13 k*=1000)
    - 1.27e-17 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (1.27e-17, rho=1.37e-13 k*=1000)
    - 4.21e-18 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (4.21e-18, rho=1.40e-14 k*=1000)
    - 3.91e-18 -> mono {not(and(THEM(ME),X)):1}   via not(and(THEM(ME),X)) (3.91e-18, rho=1.37e-13 k*=1000)
    - 2.86e-19 -> mono {Hare:1}   via Hare (2.86e-19, rho=8.63e-19 k*=1000)
