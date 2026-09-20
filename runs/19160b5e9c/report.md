### arm=weak, n=7, game=pd, N=100, w=1.0, x_on=True, role=False, mode=sparse, fmap=exp

programs 9426, classes 106, states 641, terminal classes 1, indeterminate 0, divergence rate 0.0113, flow into polymorphic targets 5.13e-07
mean payoff -0.9825, efficient 0.0000, deadweight loss 0.9825, mean bits in support 2.76

| pi | state |
|---|---|
| 0.9790 | mono {D:1} |
| 0.0163 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 7.46e-05 -> mono {THEM(ME):1}   via THEM(ME) (7.46e-05, rho=1.00e-02 k*=100)
    - 7.03e-05 -> mono {THEM(^C):1}   via THEM(^C) (7.03e-05, rho=7.42e-02 k*=100)
    - 4.88e-05 -> mono {THEM(^X):1}   via THEM(^X) (4.88e-05, rho=5.36e-02 k*=100)
    - 9.48e-06 -> mono {THEM(^D):1}   via THEM(^D) (9.48e-06, rho=1.00e-02 k*=100)
    - 3.15e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (3.15e-06, rho=1.00e-02 k*=100)
    - 1.28e-06 -> mono {and(X,THEM(^C)):1}   via and(X,THEM(^C)) (1.28e-06, rho=3.85e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 6.06e-04 -> mono {THEM(^D):1}   via THEM(^D) (6.06e-04, rho=6.39e-01 k*=100)
    - 3.64e-04 -> mono {THEM(^X):1}   via THEM(^X) (3.64e-04, rho=4.00e-01 k*=100)
    - 1.34e-05 -> mono {or(X,THEM(^D)):1}   via or(X,THEM(^D)) (1.34e-05, rho=4.02e-01 k*=100)
    - 9.87e-06 -> mono {THEM(^and(X,X)):1}   via THEM(^and(X,X)) (9.87e-06, rho=5.35e-01 k*=100)
    - 7.61e-06 -> mono {or(X,THEM(^X)):1}   via or(X,THEM(^X)) (7.61e-06, rho=2.28e-01 k*=100)
