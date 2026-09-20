### arm=strong, n=6, game=pd, N=10, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 1726, classes 21, states 25, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 1.31e-09
mean payoff -0.9964, efficient 0.0000, deadweight loss 0.9964, mean bits in support 2.61

| pi | state |
|---|---|
| 0.9904 | mono {D:1} |
| 0.0051 | mono {X:1} |
| 0.0016 | mono {and(X,X):1} |
| 0.0012 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 5.89e-04 -> mono {X:1}   via X (5.89e-04, rho=1.87e-03 k*=10)
    - 3.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-04, rho=1.00e-01 k*=10)
    - 1.41e-04 -> mono {and(X,X):1}   via and(X,X) (1.41e-04, rho=1.77e-02 k*=10)
    - 1.38e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.38e-05, rho=4.58e-02 k*=10)
    - 1.22e-05 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.22e-05, rho=1.00e-01 k*=10)
    - 9.32e-06 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (9.32e-06, rho=1.00e-01 k*=10)
- mono {X:1}
    - 1.52e-01 -> mono {D:1}   via D (1.52e-01, rho=4.58e-01 k*=10)
    - 2.20e-03 -> mono {and(X,X):1}   via and(X,X) (2.20e-03, rho=2.76e-01 k*=10)
    - 6.21e-04 -> mono {C:1}   via C (6.21e-04, rho=1.87e-03 k*=10)
    - 1.53e-04 -> mono {THEM(ME):1}   via THEM(ME) (1.53e-04, rho=4.00e-02 k*=10)
    - 1.41e-04 -> mono {or(X,X):1}   via or(X,X) (1.41e-04, rho=1.77e-02 k*=10)
    - 1.12e-04 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.12e-04, rho=3.71e-01 k*=10)
- mono {and(X,X):1}
    - 9.16e-02 -> mono {D:1}   via D (9.16e-02, rho=2.76e-01 k*=10)
    - 5.55e-03 -> mono {X:1}   via X (5.55e-03, rho=1.77e-02 k*=10)
    - 2.59e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.59e-04, rho=6.75e-02 k*=10)
    - 5.45e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (5.45e-05, rho=1.81e-01 k*=10)
    - 5.20e-05 -> mono {C:1}   via C (5.20e-05, rho=1.57e-04 k*=10)
    - 3.37e-05 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (3.37e-05, rho=2.76e-01 k*=10)
- mono {THEM(ME):1}
    - 1.77e-01 -> mono {C:1}   via C (1.77e-01, rho=5.34e-01 k*=10)
    - 9.28e-02 -> mono {X:1}   via X (9.28e-02, rho=2.95e-01 k*=10)
    - 3.32e-02 -> mono {D:1}   via D (3.32e-02, rho=1.00e-01 k*=10)
    - 3.34e-03 -> mono {or(X,X):1}   via or(X,X) (3.34e-03, rho=4.19e-01 k*=10)
    - 1.46e-03 -> mono {and(X,X):1}   via and(X,X) (1.46e-03, rho=1.83e-01 k*=10)
    - 1.44e-04 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (1.44e-04, rho=4.78e-01 k*=10)
