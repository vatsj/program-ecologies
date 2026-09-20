### arm=strong, n=6, game=stag, N=10, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 1726, classes 21, states 23, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 3.95e-08
mean payoff 3.0832, efficient 4.0000, deadweight loss 0.9168, mean bits in support 2.71

| pi | state |
|---|---|
| 0.5765 | mono {Hare:1} |
| 0.2120 | mono {X:1} |
| 0.1933 | mono {Stag:1} |
| 0.0078 | mono {and(X,X):1} |
| 0.0045 | mono {or(X,X):1} |
| 0.0036 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Hare:1}
    - 1.75e-02 -> mono {X:1}   via X (1.75e-02, rho=5.56e-02 k*=10)
    - 1.37e-02 -> mono {Stag:1}   via Stag (1.37e-02, rho=4.14e-02 k*=10)
    - 5.79e-04 -> mono {and(X,X):1}   via and(X,X) (5.79e-04, rho=7.26e-02 k*=10)
    - 3.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {or(X,X):1}   via or(X,X) (3.67e-04, rho=4.61e-02 k*=10)
    - 2.96e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (2.96e-05, rho=3.47e-02 k*=10)
- mono {X:1}
    - 4.77e-02 -> mono {Hare:1}   via Hare (4.77e-02, rho=1.44e-01 k*=10)
    - 2.87e-02 -> mono {Stag:1}   via Stag (2.87e-02, rho=8.66e-02 k*=10)
    - 9.40e-04 -> mono {and(X,X):1}   via and(X,X) (9.40e-04, rho=1.18e-01 k*=10)
    - 7.18e-04 -> mono {or(X,X):1}   via or(X,X) (7.18e-04, rho=9.00e-02 k*=10)
    - 4.09e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.09e-04, rho=1.07e-01 k*=10)
    - 9.08e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (9.08e-05, rho=1.07e-01 k*=10)
- mono {Stag:1}
    - 4.12e-02 -> mono {Hare:1}   via Hare (4.12e-02, rho=1.24e-01 k*=10)
    - 3.16e-02 -> mono {X:1}   via X (3.16e-02, rho=1.01e-01 k*=10)
    - 8.78e-04 -> mono {and(X,X):1}   via and(X,X) (8.78e-04, rho=1.10e-01 k*=10)
    - 7.75e-04 -> mono {or(X,X):1}   via or(X,X) (7.75e-04, rho=9.71e-02 k*=10)
    - 3.33e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.33e-04, rho=8.67e-02 k*=10)
    - 1.06e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.06e-04, rho=1.24e-01 k*=10)
- mono {and(X,X):1}
    - 4.28e-02 -> mono {Hare:1}   via Hare (4.28e-02, rho=1.29e-01 k*=10)
    - 2.54e-02 -> mono {X:1}   via X (2.54e-02, rho=8.10e-02 k*=10)
    - 2.16e-02 -> mono {Stag:1}   via Stag (2.16e-02, rho=6.51e-02 k*=10)
    - 5.58e-04 -> mono {or(X,X):1}   via or(X,X) (5.58e-04, rho=7.00e-02 k*=10)
    - 4.09e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.09e-04, rho=1.07e-01 k*=10)
    - 5.96e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (5.96e-05, rho=7.00e-02 k*=10)
- mono {or(X,X):1}
    - 4.70e-02 -> mono {Hare:1}   via Hare (4.70e-02, rho=1.42e-01 k*=10)
    - 3.37e-02 -> mono {X:1}   via X (3.37e-02, rho=1.07e-01 k*=10)
    - 3.30e-02 -> mono {Stag:1}   via Stag (3.30e-02, rho=9.96e-02 k*=10)
    - 9.67e-04 -> mono {and(X,X):1}   via and(X,X) (9.67e-04, rho=1.21e-01 k*=10)
    - 3.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-04, rho=1.00e-01 k*=10)
    - 1.09e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.09e-04, rho=1.28e-01 k*=10)
- mono {THEM(ME):1}
    - 4.29e-02 -> mono {Stag:1}   via Stag (4.29e-02, rho=1.29e-01 k*=10)
    - 3.32e-02 -> mono {Hare:1}   via Hare (3.32e-02, rho=1.00e-01 k*=10)
    - 2.74e-02 -> mono {X:1}   via X (2.74e-02, rho=8.73e-02 k*=10)
    - 7.98e-04 -> mono {or(X,X):1}   via or(X,X) (7.98e-04, rho=1.00e-01 k*=10)
    - 6.97e-04 -> mono {and(X,X):1}   via and(X,X) (6.97e-04, rho=8.73e-02 k*=10)
    - 8.51e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.51e-05, rho=1.00e-01 k*=10)
