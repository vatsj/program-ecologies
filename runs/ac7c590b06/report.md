### arm=strong, n=7, game=pd, N=10, w=1.0, x_on=True, role=False, mode=sparse

programs 8770, classes 44, states 309, terminal classes 1, indeterminate 0, divergence rate 0.0053, flow into polymorphic targets 4.61e-09
mean payoff -0.9989, efficient 0.0000, deadweight loss 0.9989, mean bits in support 2.60

| pi | state |
|---|---|
| 0.9964 | mono {D:1} |
| 0.0011 | mono {X:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.90e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.90e-04, rho=1.00e-01 k*=10)
    - 1.68e-05 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.68e-05, rho=1.00e-01 k*=10)
    - 1.23e-05 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (1.23e-05, rho=1.00e-01 k*=10)
    - 1.23e-05 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (1.23e-05, rho=1.00e-01 k*=10)
    - 7.67e-07 -> mono {and(X,and(X,THEM(ME))):1}   via and(X,and(X,THEM(ME))) (7.67e-07, rho=1.00e-01 k*=10)
    - 3.83e-07 -> mono {and(THEM(ME),and(X,X)):1}   via and(THEM(ME),and(X,X)) (3.83e-07, rho=1.00e-01 k*=10)
- mono {X:1}
    - 2.15e-01 -> mono {D:1}   via D (2.15e-01, rho=6.50e-01 k*=10)
    - 3.84e-03 -> mono {and(X,X):1}   via and(X,X) (3.84e-03, rho=4.48e-01 k*=10)
    - 2.44e-04 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (2.44e-04, rho=5.65e-01 k*=10)
    - 1.21e-04 -> mono {and(X,or(X,X)):1}   via and(X,or(X,X)) (1.21e-04, rho=2.80e-01 k*=10)
    - 1.09e-04 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.09e-04, rho=6.50e-01 k*=10)
    - 5.22e-05 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (5.22e-05, rho=4.25e-01 k*=10)
