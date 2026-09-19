### arm=strong, n=7, game=pd, N=100, w=1.0, x_on=True, role=False, mode=sparse

programs 8770, classes 44, states 309, terminal classes 1, indeterminate 0, divergence rate 0.0053, flow into polymorphic targets 2.74e-10
mean payoff -0.9999, efficient 0.0000, deadweight loss 0.9999, mean bits in support 2.60

| pi | state |
|---|---|
| 0.9985 | mono {D:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.90e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.90e-05, rho=1.00e-02 k*=100)
    - 1.68e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.68e-06, rho=1.00e-02 k*=100)
    - 1.23e-06 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (1.23e-06, rho=1.00e-02 k*=100)
    - 1.23e-06 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (1.23e-06, rho=1.00e-02 k*=100)
    - 7.67e-08 -> mono {and(X,and(X,THEM(ME))):1}   via and(X,and(X,THEM(ME))) (7.67e-08, rho=1.00e-02 k*=100)
    - 3.83e-08 -> mono {and(THEM(ME),and(X,X)):1}   via and(THEM(ME),and(X,X)) (3.83e-08, rho=1.00e-02 k*=100)
