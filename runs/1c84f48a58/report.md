### arm=strong, n=7, game=pd, N=100, w=0.01, x_on=True, role=False, mode=sparse

programs 8770, classes 44, states 329, terminal classes 1, indeterminate 0, divergence rate 0.0053, flow into polymorphic targets 1.11e-07
mean payoff -0.6640, efficient 0.0000, deadweight loss 0.6640, mean bits in support 2.73

| pi | state |
|---|---|
| 0.5061 | mono {D:1} |
| 0.2874 | mono {X:1} |
| 0.1843 | mono {C:1} |
| 0.0101 | mono {and(X,X):1} |
| 0.0061 | mono {or(X,X):1} |
| 0.0031 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.39e-03 -> mono {X:1}   via X (2.39e-03, rho=7.67e-03 k*=100)
    - 1.91e-03 -> mono {C:1}   via C (1.91e-03, rho=5.75e-03 k*=100)
    - 7.52e-05 -> mono {and(X,X):1}   via and(X,X) (7.52e-05, rho=8.78e-03 k*=100)
    - 5.70e-05 -> mono {or(X,X):1}   via or(X,X) (5.70e-05, rho=6.66e-03 k*=100)
    - 3.90e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.90e-05, rho=1.00e-02 k*=100)
    - 4.04e-06 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (4.04e-06, rho=9.38e-03 k*=100)
- mono {X:1}
    - 4.23e-03 -> mono {D:1}   via D (4.23e-03, rho=1.28e-02 k*=100)
    - 2.54e-03 -> mono {C:1}   via C (2.54e-03, rho=7.68e-03 k*=100)
    - 9.70e-05 -> mono {and(X,X):1}   via and(X,X) (9.70e-05, rho=1.13e-02 k*=100)
    - 7.52e-05 -> mono {or(X,X):1}   via or(X,X) (7.52e-05, rho=8.78e-03 k*=100)
    - 3.58e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.58e-05, rho=9.19e-03 k*=100)
    - 7.86e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.86e-06, rho=9.19e-03 k*=100)
- mono {C:1}
    - 5.26e-03 -> mono {D:1}   via D (5.26e-03, rho=1.59e-02 k*=100)
    - 3.98e-03 -> mono {X:1}   via X (3.98e-03, rho=1.27e-02 k*=100)
    - 1.22e-04 -> mono {and(X,X):1}   via and(X,X) (1.22e-04, rho=1.43e-02 k*=100)
    - 9.69e-05 -> mono {or(X,X):1}   via or(X,X) (9.69e-05, rho=1.13e-02 k*=100)
    - 3.27e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.27e-05, rho=8.39e-03 k*=100)
    - 1.36e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.36e-05, rho=1.59e-02 k*=100)
- mono {and(X,X):1}
    - 3.75e-03 -> mono {D:1}   via D (3.75e-03, rho=1.13e-02 k*=100)
    - 2.74e-03 -> mono {X:1}   via X (2.74e-03, rho=8.78e-03 k*=100)
    - 2.21e-03 -> mono {C:1}   via C (2.21e-03, rho=6.67e-03 k*=100)
    - 6.57e-05 -> mono {or(X,X):1}   via or(X,X) (6.57e-05, rho=7.67e-03 k*=100)
    - 3.74e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.74e-05, rho=9.59e-03 k*=100)
    - 5.67e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (5.67e-06, rho=6.63e-03 k*=100)
- mono {or(X,X):1}
    - 4.73e-03 -> mono {D:1}   via D (4.73e-03, rho=1.43e-02 k*=100)
    - 3.54e-03 -> mono {X:1}   via X (3.54e-03, rho=1.13e-02 k*=100)
    - 2.91e-03 -> mono {C:1}   via C (2.91e-03, rho=8.79e-03 k*=100)
    - 1.09e-04 -> mono {and(X,X):1}   via and(X,X) (1.09e-04, rho=1.27e-02 k*=100)
    - 3.42e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.42e-05, rho=8.79e-03 k*=100)
    - 1.05e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.05e-05, rho=1.23e-02 k*=100)
- mono {THEM(ME):1}
    - 4.55e-03 -> mono {C:1}   via C (4.55e-03, rho=1.37e-02 k*=100)
    - 3.67e-03 -> mono {X:1}   via X (3.67e-03, rho=1.18e-02 k*=100)
    - 3.31e-03 -> mono {D:1}   via D (3.31e-03, rho=1.00e-02 k*=100)
    - 1.09e-04 -> mono {or(X,X):1}   via or(X,X) (1.09e-04, rho=1.27e-02 k*=100)
    - 9.29e-05 -> mono {and(X,X):1}   via and(X,X) (9.29e-05, rho=1.09e-02 k*=100)
    - 8.55e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.55e-06, rho=1.00e-02 k*=100)
