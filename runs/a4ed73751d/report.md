### arm=strong, n=6, game=stag, N=10, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 1726, classes 21, states 23, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 7.01e-09
mean payoff 3.0086, efficient 4.0000, deadweight loss 0.9914, mean bits in support 2.65

| pi | state |
|---|---|
| 0.9039 | mono {Hare:1} |
| 0.0508 | mono {X:1} |
| 0.0361 | mono {Stag:1} |
| 0.0039 | mono {and(X,X):1} |
| 0.0031 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Hare:1}
    - 4.34e-03 -> mono {X:1}   via X (4.34e-03, rho=1.38e-02 k*=10)
    - 1.83e-03 -> mono {Stag:1}   via Stag (1.83e-03, rho=5.52e-03 k*=10)
    - 3.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-04, rho=1.00e-01 k*=10)
    - 2.77e-04 -> mono {and(X,X):1}   via and(X,X) (2.77e-04, rho=3.48e-02 k*=10)
    - 5.94e-05 -> mono {or(X,X):1}   via or(X,X) (5.94e-05, rho=7.45e-03 k*=10)
    - 1.78e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.78e-05, rho=5.91e-02 k*=10)
- mono {X:1}
    - 7.91e-02 -> mono {Hare:1}   via Hare (7.91e-02, rho=2.39e-01 k*=10)
    - 2.13e-02 -> mono {Stag:1}   via Stag (2.13e-02, rho=6.43e-02 k*=10)
    - 1.25e-03 -> mono {and(X,X):1}   via and(X,X) (1.25e-03, rho=1.57e-01 k*=10)
    - 5.75e-04 -> mono {or(X,X):1}   via or(X,X) (5.75e-04, rho=7.21e-02 k*=10)
    - 4.60e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.60e-04, rho=1.20e-01 k*=10)
    - 1.02e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.02e-04, rho=1.20e-01 k*=10)
- mono {Stag:1}
    - 4.96e-02 -> mono {Hare:1}   via Hare (4.96e-02, rho=1.50e-01 k*=10)
    - 3.17e-02 -> mono {X:1}   via X (3.17e-02, rho=1.01e-01 k*=10)
    - 9.80e-04 -> mono {and(X,X):1}   via and(X,X) (9.80e-04, rho=1.23e-01 k*=10)
    - 7.30e-04 -> mono {or(X,X):1}   via or(X,X) (7.30e-04, rho=9.16e-02 k*=10)
    - 2.36e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.36e-04, rho=6.14e-02 k*=10)
    - 1.27e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.27e-04, rho=1.50e-01 k*=10)
- mono {and(X,X):1}
    - 6.47e-02 -> mono {Hare:1}   via Hare (6.47e-02, rho=1.95e-01 k*=10)
    - 1.60e-02 -> mono {X:1}   via X (1.60e-02, rho=5.09e-02 k*=10)
    - 8.43e-03 -> mono {Stag:1}   via Stag (8.43e-03, rho=2.54e-02 k*=10)
    - 4.60e-04 -> mono {THEM(ME):1}   via THEM(ME) (4.60e-04, rho=1.20e-01 k*=10)
    - 2.52e-04 -> mono {or(X,X):1}   via or(X,X) (2.52e-04, rho=3.15e-02 k*=10)
    - 4.27e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (4.27e-05, rho=1.42e-01 k*=10)
- mono {THEM(ME):1}
    - 6.76e-02 -> mono {Stag:1}   via Stag (6.76e-02, rho=2.04e-01 k*=10)
    - 3.32e-02 -> mono {Hare:1}   via Hare (3.32e-02, rho=1.00e-01 k*=10)
    - 2.07e-02 -> mono {X:1}   via X (2.07e-02, rho=6.58e-02 k*=10)
    - 7.98e-04 -> mono {or(X,X):1}   via or(X,X) (7.98e-04, rho=1.00e-01 k*=10)
    - 5.25e-04 -> mono {and(X,X):1}   via and(X,X) (5.25e-04, rho=6.58e-02 k*=10)
    - 8.51e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.51e-05, rho=1.00e-01 k*=10)
