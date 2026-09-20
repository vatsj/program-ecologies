### arm=strong, n=6, game=stag, N=1000, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 1726, classes 21, states 23, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 0.00e+00
mean payoff 4.0000, efficient 4.0000, deadweight loss -0.0000, mean bits in support 2.59

| pi | state |
|---|---|
| 0.9997 | mono {Stag:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Stag:1}
    - 9.32e-08 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (9.32e-08, rho=1.00e-03 k*=1000)
    - 1.53e-42 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (1.53e-42, rho=1.64e-38 k*=1000)
    - 1.53e-42 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (1.53e-42, rho=1.64e-38 k*=1000)
    - 4.70e-43 -> mono {not(and(THEM(ME),X)):1}   via not(and(THEM(ME),X)) (4.70e-43, rho=1.64e-38 k*=1000)
    - 6.22e-46 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (6.22e-46, rho=2.07e-42 k*=1000)
    - 2.51e-49 -> mono {not(and(X,THEM(ME))):1}   via not(and(X,THEM(ME))) (2.51e-49, rho=8.76e-45 k*=1000)
