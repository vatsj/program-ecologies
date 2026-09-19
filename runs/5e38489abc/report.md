### arm=strong, n=6, game=stag, N=1000, w=1.0, x_on=True, role=False, mode=square

programs 1726, classes 21, states 29, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 3.83e-15
mean payoff 4.0000, efficient 4.0000, deadweight loss 0.0000, mean bits in support 2.59

| pi | state |
|---|---|
| 0.9997 | mono {C:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 9.32e-08 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (9.32e-08, rho=1.00e-03 k*=1000)
    - 1.20e-14 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (1.20e-14, rho=3.97e-11 k*=1000)
    - 1.07e-14 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (1.07e-14, rho=1.15e-10 k*=1000)
    - 1.07e-14 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (1.07e-14, rho=1.15e-10 k*=1000)
    - 3.82e-15 -> poly {C:0.5, X:0.5}   via X (3.82e-15, rho=1.22e-14 k*=500)
    - 3.30e-15 -> mono {not(and(THEM(ME),X)):1}   via not(and(THEM(ME),X)) (3.30e-15, rho=1.15e-10 k*=1000)
