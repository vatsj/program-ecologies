### arm=strong, n=6, game=pd, N=100, w=0.1, x_on=True, role=False, mode=square

programs 1726, classes 21, states 25, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 1.15e-10
mean payoff -0.9965, efficient 0.0000, deadweight loss 0.9965, mean bits in support 2.61

| pi | state |
|---|---|
| 0.9910 | mono {D:1} |
| 0.0051 | mono {X:1} |
| 0.0016 | mono {and(X,X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 6.93e-05 -> mono {X:1}   via X (6.93e-05, rho=2.20e-04 k*=100)
    - 3.84e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-05, rho=1.00e-02 k*=100)
    - 1.45e-05 -> mono {and(X,X):1}   via and(X,X) (1.45e-05, rho=1.82e-03 k*=100)
    - 1.38e-06 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.38e-06, rho=4.58e-03 k*=100)
    - 1.22e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.22e-06, rho=1.00e-02 k*=100)
    - 9.32e-07 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (9.32e-07, rho=1.00e-02 k*=100)
- mono {X:1}
    - 1.73e-02 -> mono {D:1}   via D (1.73e-02, rho=5.22e-02 k*=100)
    - 2.27e-04 -> mono {and(X,X):1}   via and(X,X) (2.27e-04, rho=2.84e-02 k*=100)
    - 9.23e-05 -> mono {C:1}   via C (9.23e-05, rho=2.78e-04 k*=100)
    - 1.61e-05 -> mono {or(X,X):1}   via or(X,X) (1.61e-05, rho=2.02e-03 k*=100)
    - 1.21e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.21e-05, rho=4.01e-02 k*=100)
    - 1.14e-05 -> mono {THEM(ME):1}   via THEM(ME) (1.14e-05, rho=2.96e-03 k*=100)
- mono {and(X,X):1}
    - 9.63e-03 -> mono {D:1}   via D (9.63e-03, rho=2.90e-02 k*=100)
    - 6.04e-04 -> mono {X:1}   via X (6.04e-04, rho=1.92e-03 k*=100)
    - 2.26e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.26e-05, rho=5.88e-03 k*=100)
    - 9.00e-06 -> mono {C:1}   via C (9.00e-06, rho=2.71e-05 k*=100)
    - 5.51e-06 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (5.51e-06, rho=1.83e-02 k*=100)
    - 3.54e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (3.54e-06, rho=2.90e-02 k*=100)
