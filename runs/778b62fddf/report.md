### arm=strong, n=7, game=pd, N=100, w=0.1, x_on=True, role=False, mode=sparse, fmap=exp

programs 8770, classes 45, states 310, terminal classes 1, indeterminate 0, divergence rate 0.0053, flow into polymorphic targets 1.95e-09
mean payoff -0.9953, efficient 0.0000, deadweight loss 0.9953, mean bits in support 2.62

| pi | state |
|---|---|
| 0.9880 | mono {D:1} |
| 0.0071 | mono {X:1} |
| 0.0021 | mono {and(X,X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.00e-04 -> mono {X:1}   via X (1.00e-04, rho=3.21e-04 k*=100)
    - 3.90e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.90e-05, rho=1.00e-02 k*=100)
    - 1.87e-05 -> mono {and(X,X):1}   via and(X,X) (1.87e-05, rho=2.19e-03 k*=100)
    - 2.14e-06 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (2.14e-06, rho=4.98e-03 k*=100)
    - 1.68e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.68e-06, rho=1.00e-02 k*=100)
    - 1.32e-06 -> mono {C:1}   via C (1.32e-06, rho=3.98e-06 k*=100)
- mono {X:1}
    - 1.66e-02 -> mono {D:1}   via D (1.66e-02, rho=5.00e-02 k*=100)
    - 2.34e-04 -> mono {and(X,X):1}   via and(X,X) (2.34e-04, rho=2.73e-02 k*=100)
    - 1.06e-04 -> mono {C:1}   via C (1.06e-04, rho=3.21e-04 k*=100)
    - 1.87e-05 -> mono {or(X,X):1}   via or(X,X) (1.87e-05, rho=2.19e-03 k*=100)
    - 1.65e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.65e-05, rho=3.84e-02 k*=100)
    - 1.27e-05 -> mono {THEM(ME):1}   via THEM(ME) (1.27e-05, rho=3.27e-03 k*=100)
- mono {and(X,X):1}
    - 9.05e-03 -> mono {D:1}   via D (9.05e-03, rho=2.73e-02 k*=100)
    - 6.83e-04 -> mono {X:1}   via X (6.83e-04, rho=2.19e-03 k*=100)
    - 2.41e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.41e-05, rho=6.18e-03 k*=100)
    - 1.25e-05 -> mono {C:1}   via C (1.25e-05, rho=3.78e-05 k*=100)
    - 7.58e-06 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (7.58e-06, rho=1.76e-02 k*=100)
    - 4.59e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (4.59e-06, rho=2.73e-02 k*=100)
