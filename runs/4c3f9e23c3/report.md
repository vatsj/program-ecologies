### arm=strong, n=6, game=pd, N=1000, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 1726, classes 21, states 25, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 2.91e-12
mean payoff -0.9999, efficient 0.0000, deadweight loss 0.9999, mean bits in support 2.60

| pi | state |
|---|---|
| 0.9988 | mono {D:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.84e-06 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-06, rho=1.00e-03 k*=1000)
    - 1.22e-07 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.22e-07, rho=1.00e-03 k*=1000)
    - 9.32e-08 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (9.32e-08, rho=1.00e-03 k*=1000)
    - 9.32e-08 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (9.32e-08, rho=1.00e-03 k*=1000)
    - 1.38e-11 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.38e-11, rho=4.58e-08 k*=1000)
    - 2.67e-15 -> mono {and(X,X):1}   via and(X,X) (2.67e-15, rho=3.35e-13 k*=1000)
