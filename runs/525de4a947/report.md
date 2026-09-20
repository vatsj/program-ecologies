### arm=strong, n=6, game=stag, N=10, w=0.01, x_on=True, role=False, mode=square, fmap=exp

programs 1726, classes 21, states 23, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 6.58e-08
mean payoff 3.1607, efficient 4.0000, deadweight loss 0.8393, mean bits in support 2.73

| pi | state |
|---|---|
| 0.3545 | mono {Hare:1} |
| 0.3177 | mono {Stag:1} |
| 0.3056 | mono {X:1} |
| 0.0081 | mono {and(X,X):1} |
| 0.0076 | mono {or(X,X):1} |
| 0.0038 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Hare:1}
    - 3.05e-02 -> mono {Stag:1}   via Stag (3.05e-02, rho=9.21e-02 k*=10)
    - 2.98e-02 -> mono {X:1}   via X (2.98e-02, rho=9.47e-02 k*=10)
    - 7.74e-04 -> mono {and(X,X):1}   via and(X,X) (7.74e-04, rho=9.70e-02 k*=10)
    - 7.42e-04 -> mono {or(X,X):1}   via or(X,X) (7.42e-04, rho=9.31e-02 k*=10)
    - 3.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-04, rho=1.00e-01 k*=10)
    - 7.73e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.73e-05, rho=9.08e-02 k*=10)
- mono {Stag:1}
    - 3.41e-02 -> mono {Hare:1}   via Hare (3.41e-02, rho=1.03e-01 k*=10)
    - 3.15e-02 -> mono {X:1}   via X (3.15e-02, rho=1.00e-01 k*=10)
    - 8.07e-04 -> mono {and(X,X):1}   via and(X,X) (8.07e-04, rho=1.01e-01 k*=10)
    - 7.95e-04 -> mono {or(X,X):1}   via or(X,X) (7.95e-04, rho=9.97e-02 k*=10)
    - 3.79e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.79e-04, rho=9.87e-02 k*=10)
    - 8.75e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.75e-05, rho=1.03e-01 k*=10)
- mono {X:1}
    - 3.45e-02 -> mono {Hare:1}   via Hare (3.45e-02, rho=1.04e-01 k*=10)
    - 3.27e-02 -> mono {Stag:1}   via Stag (3.27e-02, rho=9.86e-02 k*=10)
    - 8.11e-04 -> mono {and(X,X):1}   via and(X,X) (8.11e-04, rho=1.02e-01 k*=10)
    - 7.89e-04 -> mono {or(X,X):1}   via or(X,X) (7.89e-04, rho=9.90e-02 k*=10)
    - 3.86e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.86e-04, rho=1.01e-01 k*=10)
    - 8.57e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.57e-05, rho=1.01e-01 k*=10)
- mono {and(X,X):1}
    - 3.41e-02 -> mono {Hare:1}   via Hare (3.41e-02, rho=1.03e-01 k*=10)
    - 3.18e-02 -> mono {Stag:1}   via Stag (3.18e-02, rho=9.59e-02 k*=10)
    - 3.08e-02 -> mono {X:1}   via X (3.08e-02, rho=9.80e-02 k*=10)
    - 7.71e-04 -> mono {or(X,X):1}   via or(X,X) (7.71e-04, rho=9.66e-02 k*=10)
    - 3.86e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.86e-04, rho=1.01e-01 k*=10)
    - 8.23e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.23e-05, rho=9.66e-02 k*=10)
- mono {or(X,X):1}
    - 3.45e-02 -> mono {Hare:1}   via Hare (3.45e-02, rho=1.04e-01 k*=10)
    - 3.31e-02 -> mono {Stag:1}   via Stag (3.31e-02, rho=1.00e-01 k*=10)
    - 3.17e-02 -> mono {X:1}   via X (3.17e-02, rho=1.01e-01 k*=10)
    - 8.14e-04 -> mono {and(X,X):1}   via and(X,X) (8.14e-04, rho=1.02e-01 k*=10)
    - 3.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-04, rho=1.00e-01 k*=10)
    - 8.75e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.75e-05, rho=1.03e-01 k*=10)
- mono {THEM(ME):1}
    - 3.40e-02 -> mono {Stag:1}   via Stag (3.40e-02, rho=1.03e-01 k*=10)
    - 3.32e-02 -> mono {Hare:1}   via Hare (3.32e-02, rho=1.00e-01 k*=10)
    - 3.10e-02 -> mono {X:1}   via X (3.10e-02, rho=9.87e-02 k*=10)
    - 7.98e-04 -> mono {or(X,X):1}   via or(X,X) (7.98e-04, rho=1.00e-01 k*=10)
    - 7.87e-04 -> mono {and(X,X):1}   via and(X,X) (7.87e-04, rho=9.87e-02 k*=10)
    - 8.51e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.51e-05, rho=1.00e-01 k*=10)
