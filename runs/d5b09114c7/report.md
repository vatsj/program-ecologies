### arm=strong, n=6, game=stag, N=1000, w=0.1, x_on=True, role=False, mode=square

programs 1726, classes 21, states 44, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 5.04e-07
mean payoff 3.8984, efficient 4.0000, deadweight loss 0.1016, mean bits in support 2.59

| pi | state |
|---|---|
| 0.8981 | mono {C:1} |
| 0.1015 | mono {D:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 2.19e-07 -> poly {C:0.5, X:0.5}   via X (2.19e-07, rho=6.98e-07 k*=500)
    - 2.06e-07 -> mono {D:1}   via D (2.06e-07, rho=6.20e-07 k*=1000)
    - 9.32e-08 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (9.32e-08, rho=1.00e-03 k*=1000)
    - 3.97e-09 -> mono {and(X,X):1}   via and(X,X) (3.97e-09, rho=4.98e-07 k*=1000)
    - 2.96e-09 -> mono {or(X,X):1}   via or(X,X) (2.96e-09, rho=3.71e-07 k*=1000)
    - 1.81e-09 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (1.81e-09, rho=6.02e-06 k*=1000)
- mono {D:1}
    - 3.84e-06 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-06, rho=1.00e-03 k*=1000)
    - 1.22e-07 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.22e-07, rho=1.00e-03 k*=1000)
    - 9.32e-08 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (9.32e-08, rho=1.00e-03 k*=1000)
    - 9.32e-08 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (9.32e-08, rho=1.00e-03 k*=1000)
    - 1.72e-17 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.72e-17, rho=5.71e-14 k*=1000)
    - 1.13e-22 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (1.13e-22, rho=1.22e-18 k*=1000)
