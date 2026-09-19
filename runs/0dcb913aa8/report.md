### arm=strong, n=6, game=stag, N=100, w=1.0, x_on=True, role=False, mode=square

programs 1726, classes 21, states 30, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 2.30e-05
mean payoff 3.0207, efficient 4.0000, deadweight loss 0.9793, mean bits in support 2.60

| pi | state |
|---|---|
| 0.9770 | mono {D:1} |
| 0.0207 | mono {C:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.84e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-05, rho=1.00e-02 k*=100)
    - 1.22e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.22e-06, rho=1.00e-02 k*=100)
    - 9.32e-07 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (9.32e-07, rho=1.00e-02 k*=100)
    - 9.32e-07 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (9.32e-07, rho=1.00e-02 k*=100)
    - 3.27e-09 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (3.27e-09, rho=1.09e-05 k*=100)
    - 4.83e-11 -> mono {and(X,X):1}   via and(X,X) (4.83e-11, rho=6.06e-09 k*=100)
- mono {C:1}
    - 8.78e-04 -> poly {C:0.5, X:0.5}   via X (8.78e-04, rho=2.79e-03 k*=50)
    - 8.55e-04 -> mono {D:1}   via D (8.55e-04, rho=2.58e-03 k*=100)
    - 1.68e-05 -> mono {and(X,X):1}   via and(X,X) (1.68e-05, rho=2.11e-03 k*=100)
    - 1.18e-05 -> mono {or(X,X):1}   via or(X,X) (1.18e-05, rho=1.47e-03 k*=100)
    - 2.20e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (2.20e-06, rho=2.58e-03 k*=100)
    - 9.39e-07 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (9.39e-07, rho=3.12e-03 k*=100)
