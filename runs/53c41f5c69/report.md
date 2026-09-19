### arm=strong, n=7, game=pd, N=100, w=0.1, x_on=True, role=False, mode=sparse

programs 8770, classes 44, states 311, terminal classes 1, indeterminate 0, divergence rate 0.0053, flow into polymorphic targets 1.47e-09
mean payoff -0.9964, efficient 0.0000, deadweight loss 0.9964, mean bits in support 2.61

| pi | state |
|---|---|
| 0.9906 | mono {D:1} |
| 0.0051 | mono {X:1} |
| 0.0017 | mono {and(X,X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 6.89e-05 -> mono {X:1}   via X (6.89e-05, rho=2.20e-04 k*=100)
    - 3.90e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.90e-05, rho=1.00e-02 k*=100)
    - 1.56e-05 -> mono {and(X,X):1}   via and(X,X) (1.56e-05, rho=1.82e-03 k*=100)
    - 1.97e-06 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.97e-06, rho=4.58e-03 k*=100)
    - 1.68e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.68e-06, rho=1.00e-02 k*=100)
    - 1.23e-06 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (1.23e-06, rho=1.00e-02 k*=100)
- mono {X:1}
    - 1.73e-02 -> mono {D:1}   via D (1.73e-02, rho=5.22e-02 k*=100)
    - 2.44e-04 -> mono {and(X,X):1}   via and(X,X) (2.44e-04, rho=2.84e-02 k*=100)
    - 9.23e-05 -> mono {C:1}   via C (9.23e-05, rho=2.78e-04 k*=100)
    - 1.73e-05 -> mono {or(X,X):1}   via or(X,X) (1.73e-05, rho=2.02e-03 k*=100)
    - 1.73e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.73e-05, rho=4.01e-02 k*=100)
    - 1.15e-05 -> mono {THEM(ME):1}   via THEM(ME) (1.15e-05, rho=2.96e-03 k*=100)
- mono {and(X,X):1}
    - 9.63e-03 -> mono {D:1}   via D (9.63e-03, rho=2.90e-02 k*=100)
    - 6.00e-04 -> mono {X:1}   via X (6.00e-04, rho=1.92e-03 k*=100)
    - 2.29e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.29e-05, rho=5.88e-03 k*=100)
    - 9.00e-06 -> mono {C:1}   via C (9.00e-06, rho=2.71e-05 k*=100)
    - 7.90e-06 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (7.90e-06, rho=1.83e-02 k*=100)
    - 4.88e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (4.88e-06, rho=2.90e-02 k*=100)
