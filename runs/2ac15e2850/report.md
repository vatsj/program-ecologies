### arm=weak, n=7, game=pd, N=100, w=0.3, x_on=True, role=False, mode=sparse, fmap=exp

programs 9426, classes 106, states 620, terminal classes 1, indeterminate 0, divergence rate 0.0113, flow into polymorphic targets 9.77e-08
mean payoff -0.9873, efficient 0.0000, deadweight loss 0.9873, mean bits in support 2.71

| pi | state |
|---|---|
| 0.9834 | mono {D:1} |
| 0.0107 | mono {THEM(^C):1} |
| 0.0014 | mono {X:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 7.46e-05 -> mono {THEM(ME):1}   via THEM(ME) (7.46e-05, rho=1.00e-02 k*=100)
    - 3.99e-05 -> mono {THEM(^C):1}   via THEM(^C) (3.99e-05, rho=4.21e-02 k*=100)
    - 2.74e-05 -> mono {THEM(^X):1}   via THEM(^X) (2.74e-05, rho=3.01e-02 k*=100)
    - 9.48e-06 -> mono {THEM(^D):1}   via THEM(^D) (9.48e-06, rho=1.00e-02 k*=100)
    - 3.15e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (3.15e-06, rho=1.00e-02 k*=100)
    - 1.15e-06 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (1.15e-06, rho=1.00e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 2.50e-04 -> mono {THEM(^D):1}   via THEM(^D) (2.50e-04, rho=2.64e-01 k*=100)
    - 1.29e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.29e-04, rho=1.42e-01 k*=100)
    - 6.01e-06 -> mono {X:1}   via X (6.01e-06, rho=1.94e-05 k*=100)
    - 4.85e-06 -> mono {or(X,THEM(^D)):1}   via or(X,THEM(^D)) (4.85e-06, rho=1.46e-01 k*=100)
    - 4.43e-06 -> mono {or(X,X):1}   via or(X,X) (4.43e-06, rho=5.48e-04 k*=100)
- mono {X:1}
    - 4.66e-02 -> mono {D:1}   via D (4.66e-02, rho=1.42e-01 k*=100)
    - 5.96e-04 -> mono {and(X,X):1}   via and(X,X) (5.96e-04, rho=7.37e-02 k*=100)
    - 4.47e-05 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (4.47e-05, rho=1.42e-01 k*=100)
    - 4.37e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (4.37e-05, rho=1.08e-01 k*=100)
    - 2.85e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.85e-05, rho=3.01e-02 k*=100)
    - 1.55e-05 -> mono {and(X,or(X,X)):1}   via and(X,or(X,X)) (1.55e-05, rho=3.84e-02 k*=100)
