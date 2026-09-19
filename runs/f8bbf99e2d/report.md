### arm=strong, n=6, game=pd, N=1000, w=1.0, x_on=True, role=False, mode=square

programs 1726, classes 21, states 25, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 6.54e-12
mean payoff -1.0000, efficient 0.0000, deadweight loss 1.0000, mean bits in support 2.60

| pi | state |
|---|---|
| 0.9990 | mono {D:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.84e-06 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-06, rho=1.00e-03 k*=1000)
    - 1.22e-07 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.22e-07, rho=1.00e-03 k*=1000)
    - 9.32e-08 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (9.32e-08, rho=1.00e-03 k*=1000)
    - 9.32e-08 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (9.32e-08, rho=1.00e-03 k*=1000)
    - 0.00e+00 -> mono {not(or(THEM(ME),X)):1}   via not(or(THEM(ME),X)) (0.00e+00, rho=0.00e+00 k*=1000)
    - 0.00e+00 -> mono {not(and(THEM(ME),X)):1}   via not(and(THEM(ME),X)) (0.00e+00, rho=0.00e+00 k*=1000)
