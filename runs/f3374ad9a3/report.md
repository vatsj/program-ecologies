### arm=weak, n=6, game=stag, N=100, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 46, states 82, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 3.56e-08
mean payoff 3.1646, efficient 4.0000, deadweight loss 0.8354, mean bits in support 2.70

| pi | state |
|---|---|
| 0.8320 | mono {Hare:1} |
| 0.1546 | mono {Stag:1} |
| 0.0102 | mono {THEM(^Stag):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Hare:1}
    - 3.83e-05 -> mono {THEM(^Stag):1}   via THEM(^Stag) (3.83e-05, rho=4.21e-02 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 9.10e-06 -> mono {THEM(^Hare):1}   via THEM(^Hare) (9.10e-06, rho=1.00e-02 k*=100)
    - 2.29e-06 -> mono {and(THEM(ME),Hare):1}   via and(THEM(ME),Hare) (2.29e-06, rho=1.00e-02 k*=100)
    - 8.80e-07 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (8.80e-07, rho=1.00e-02 k*=100)
- mono {Stag:1}
    - 4.11e-04 -> mono {Hare:1}   via Hare (4.11e-04, rho=1.25e-03 k*=100)
    - 2.10e-04 -> mono {X:1}   via X (2.10e-04, rho=6.73e-04 k*=100)
    - 9.10e-06 -> mono {THEM(^Stag):1}   via THEM(^Stag) (9.10e-06, rho=1.00e-02 k*=100)
    - 7.33e-06 -> mono {and(X,X):1}   via and(X,X) (7.33e-06, rho=9.71e-04 k*=100)
    - 4.85e-06 -> mono {or(X,X):1}   via or(X,X) (4.85e-06, rho=6.43e-04 k*=100)
    - 9.93e-07 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (9.93e-07, rho=1.25e-03 k*=100)
- mono {THEM(^Stag):1}
    - 3.29e-03 -> mono {Stag:1}   via Stag (3.29e-03, rho=1.00e-02 k*=100)
    - 1.14e-06 -> mono {THEM(^Hare):1}   via THEM(^Hare) (1.14e-06, rho=1.25e-03 k*=100)
    - 8.80e-07 -> mono {or(X,THEM(THEM)):1}   via or(X,THEM(THEM)) (8.80e-07, rho=1.00e-02 k*=100)
    - 8.80e-07 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (8.80e-07, rho=1.00e-02 k*=100)
    - 5.95e-07 -> mono {THEM(^X):1}   via THEM(^X) (5.95e-07, rho=6.73e-04 k*=100)
    - 2.66e-07 -> mono {or(X,THEM(^Stag)):1}   via or(X,THEM(^Stag)) (2.66e-07, rho=1.00e-02 k*=100)
