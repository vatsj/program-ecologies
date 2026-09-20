### arm=strong, n=6, game=pd, N=100, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 1726, classes 21, states 25, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 3.85e-11
mean payoff -0.9998, efficient 0.0000, deadweight loss 0.9998, mean bits in support 2.60

| pi | state |
|---|---|
| 0.9987 | mono {D:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.84e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-05, rho=1.00e-02 k*=100)
    - 1.22e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.22e-06, rho=1.00e-02 k*=100)
    - 9.32e-07 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (9.32e-07, rho=1.00e-02 k*=100)
    - 9.32e-07 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (9.32e-07, rho=1.00e-02 k*=100)
    - 1.19e-10 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.19e-10, rho=3.94e-07 k*=100)
    - 1.94e-14 -> mono {and(X,X):1}   via and(X,X) (1.94e-14, rho=2.43e-12 k*=100)
