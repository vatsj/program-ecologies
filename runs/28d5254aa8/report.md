### arm=strong, n=6, game=pd, N=10, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 1726, classes 21, states 25, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 5.62e-08
mean payoff -0.8913, efficient 0.0000, deadweight loss 0.8913, mean bits in support 2.68

| pi | state |
|---|---|
| 0.8065 | mono {D:1} |
| 0.1485 | mono {X:1} |
| 0.0308 | mono {C:1} |
| 0.0086 | mono {and(X,X):1} |
| 0.0025 | mono {THEM(ME):1} |
| 0.0017 | mono {or(X,X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.20e-02 -> mono {X:1}   via X (1.20e-02, rho=3.83e-02 k*=10)
    - 3.85e-03 -> mono {C:1}   via C (3.85e-03, rho=1.16e-02 k*=10)
    - 5.10e-04 -> mono {and(X,X):1}   via and(X,X) (5.10e-04, rho=6.40e-02 k*=10)
    - 3.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-04, rho=1.00e-01 k*=10)
    - 1.72e-04 -> mono {or(X,X):1}   via or(X,X) (1.72e-04, rho=2.16e-02 k*=10)
    - 2.43e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (2.43e-05, rho=8.07e-02 k*=10)
- mono {X:1}
    - 6.61e-02 -> mono {D:1}   via D (6.61e-02, rho=1.99e-01 k*=10)
    - 1.27e-02 -> mono {C:1}   via C (1.27e-02, rho=3.83e-02 k*=10)
    - 1.16e-03 -> mono {and(X,X):1}   via and(X,X) (1.16e-03, rho=1.46e-01 k*=10)
    - 5.10e-04 -> mono {or(X,X):1}   via or(X,X) (5.10e-04, rho=6.40e-02 k*=10)
    - 3.08e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.08e-04, rho=8.02e-02 k*=10)
    - 6.83e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (6.83e-05, rho=8.02e-02 k*=10)
- mono {C:1}
    - 1.04e-01 -> mono {D:1}   via D (1.04e-01, rho=3.15e-01 k*=10)
    - 6.27e-02 -> mono {X:1}   via X (6.27e-02, rho=1.99e-01 k*=10)
    - 2.05e-03 -> mono {and(X,X):1}   via and(X,X) (2.05e-03, rho=2.57e-01 k*=10)
    - 1.16e-03 -> mono {or(X,X):1}   via or(X,X) (1.16e-03, rho=1.46e-01 k*=10)
    - 2.68e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (2.68e-04, rho=3.15e-01 k*=10)
    - 2.36e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.36e-04, rho=6.14e-02 k*=10)
- mono {and(X,X):1}
    - 4.84e-02 -> mono {D:1}   via D (4.84e-02, rho=1.46e-01 k*=10)
    - 2.01e-02 -> mono {X:1}   via X (2.01e-02, rho=6.40e-02 k*=10)
    - 7.17e-03 -> mono {C:1}   via C (7.17e-03, rho=2.16e-02 k*=10)
    - 3.46e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.46e-04, rho=9.00e-02 k*=10)
    - 3.05e-04 -> mono {or(X,X):1}   via or(X,X) (3.05e-04, rho=3.83e-02 k*=10)
    - 3.67e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (3.67e-05, rho=1.22e-01 k*=10)
- mono {THEM(ME):1}
    - 6.76e-02 -> mono {C:1}   via C (6.76e-02, rho=2.04e-01 k*=10)
    - 4.59e-02 -> mono {X:1}   via X (4.59e-02, rho=1.46e-01 k*=10)
    - 3.32e-02 -> mono {D:1}   via D (3.32e-02, rho=1.00e-01 k*=10)
    - 1.38e-03 -> mono {or(X,X):1}   via or(X,X) (1.38e-03, rho=1.74e-01 k*=10)
    - 9.69e-04 -> mono {and(X,X):1}   via and(X,X) (9.69e-04, rho=1.22e-01 k*=10)
    - 8.51e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.51e-05, rho=1.00e-01 k*=10)
- mono {or(X,X):1}
    - 8.52e-02 -> mono {D:1}   via D (8.52e-02, rho=2.57e-01 k*=10)
    - 4.59e-02 -> mono {X:1}   via X (4.59e-02, rho=1.46e-01 k*=10)
    - 2.12e-02 -> mono {C:1}   via C (2.12e-02, rho=6.40e-02 k*=10)
    - 1.59e-03 -> mono {and(X,X):1}   via and(X,X) (1.59e-03, rho=1.99e-01 k*=10)
    - 2.71e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.71e-04, rho=7.06e-02 k*=10)
    - 1.60e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.60e-04, rho=1.88e-01 k*=10)
