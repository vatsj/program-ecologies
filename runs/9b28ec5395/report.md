### arm=strong, n=6, game=stag, N=10, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 1726, classes 21, states 23, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 2.33e-10
mean payoff 3.0036, efficient 4.0000, deadweight loss 0.9964, mean bits in support 2.61

| pi | state |
|---|---|
| 0.9923 | mono {Hare:1} |
| 0.0040 | mono {Stag:1} |
| 0.0017 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Hare:1}
    - 3.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-04, rho=1.00e-01 k*=10)
    - 1.22e-05 -> mono {and(THEM(ME),Hare):1}   via and(THEM(ME),Hare) (1.22e-05, rho=1.00e-01 k*=10)
    - 1.18e-05 -> mono {X:1}   via X (1.18e-05, rho=3.77e-05 k*=10)
    - 1.09e-05 -> mono {and(X,X):1}   via and(X,X) (1.09e-05, rho=1.37e-03 k*=10)
    - 9.32e-06 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (9.32e-06, rho=1.00e-01 k*=10)
    - 9.32e-06 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (9.32e-06, rho=1.00e-01 k*=10)
- mono {Stag:1}
    - 4.77e-02 -> mono {Hare:1}   via Hare (4.77e-02, rho=1.44e-01 k*=10)
    - 2.93e-02 -> mono {X:1}   via X (2.93e-02, rho=9.33e-02 k*=10)
    - 9.71e-04 -> mono {and(X,X):1}   via and(X,X) (9.71e-04, rho=1.22e-01 k*=10)
    - 5.91e-04 -> mono {or(X,X):1}   via or(X,X) (5.91e-04, rho=7.41e-02 k*=10)
    - 1.22e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.22e-04, rho=1.44e-01 k*=10)
    - 4.02e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (4.02e-05, rho=1.34e-01 k*=10)
- mono {THEM(ME):1}
    - 1.77e-01 -> mono {Stag:1}   via Stag (1.77e-01, rho=5.34e-01 k*=10)
    - 3.32e-02 -> mono {Hare:1}   via Hare (3.32e-02, rho=1.00e-01 k*=10)
    - 6.89e-03 -> mono {X:1}   via X (6.89e-03, rho=2.19e-02 k*=10)
    - 7.98e-04 -> mono {or(X,X):1}   via or(X,X) (7.98e-04, rho=1.00e-01 k*=10)
    - 1.75e-04 -> mono {and(X,X):1}   via and(X,X) (1.75e-04, rho=2.19e-02 k*=10)
    - 8.51e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.51e-05, rho=1.00e-01 k*=10)
