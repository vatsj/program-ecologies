### arm=weak, n=6, game=stag, N=100, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 46, states 82, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 1.10e-10
mean payoff 3.9979, efficient 4.0000, deadweight loss 0.0021, mean bits in support 2.65

| pi | state |
|---|---|
| 0.9916 | mono {Stag:1} |
| 0.0030 | mono {not(THEM(^Stag)):1} |
| 0.0028 | mono {THEM(^Stag):1} |
| 0.0021 | mono {Hare:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Stag:1}
    - 9.10e-06 -> mono {THEM(^Stag):1}   via THEM(^Stag) (9.10e-06, rho=1.00e-02 k*=100)
    - 8.80e-07 -> mono {or(X,THEM(THEM)):1}   via or(X,THEM(THEM)) (8.80e-07, rho=1.00e-02 k*=100)
    - 8.80e-07 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (8.80e-07, rho=1.00e-02 k*=100)
    - 2.66e-07 -> mono {or(X,THEM(^Stag)):1}   via or(X,THEM(^Stag)) (2.66e-07, rho=1.00e-02 k*=100)
    - 1.83e-07 -> mono {Hare:1}   via Hare (1.83e-07, rho=5.55e-07 k*=100)
    - 1.11e-07 -> mono {X:1}   via X (1.11e-07, rho=3.54e-07 k*=100)
- mono {not(THEM(^Stag)):1}
    - 1.83e-07 -> mono {Hare:1}   via Hare (1.83e-07, rho=5.55e-07 k*=100)
    - 4.42e-10 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (4.42e-10, rho=5.55e-07 k*=100)
    - 4.42e-10 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (4.42e-10, rho=5.55e-07 k*=100)
    - 1.27e-10 -> mono {and(THEM(ME),Hare):1}   via and(THEM(ME),Hare) (1.27e-10, rho=5.55e-07 k*=100)
    - 4.89e-11 -> mono {not(THEM(^Hare)):1}   via not(THEM(^Hare)) (4.89e-11, rho=5.55e-07 k*=100)
    - 3.12e-11 -> mono {not(THEM(^X)):1}   via not(THEM(^X)) (3.12e-11, rho=3.54e-07 k*=100)
- mono {THEM(^Stag):1}
    - 3.29e-03 -> mono {Stag:1}   via Stag (3.29e-03, rho=1.00e-02 k*=100)
    - 8.80e-07 -> mono {or(X,THEM(THEM)):1}   via or(X,THEM(THEM)) (8.80e-07, rho=1.00e-02 k*=100)
    - 8.80e-07 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (8.80e-07, rho=1.00e-02 k*=100)
    - 2.66e-07 -> mono {or(X,THEM(^Stag)):1}   via or(X,THEM(^Stag)) (2.66e-07, rho=1.00e-02 k*=100)
    - 1.24e-08 -> mono {or(X,THEM(^X)):1}   via or(X,THEM(^X)) (1.24e-08, rho=4.68e-04 k*=100)
    - 5.14e-10 -> mono {or(X,THEM(^Hare)):1}   via or(X,THEM(^Hare)) (5.14e-10, rho=1.94e-05 k*=100)
- mono {Hare:1}
    - 6.75e-05 -> mono {THEM(^Stag):1}   via THEM(^Stag) (6.75e-05, rho=7.42e-02 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 9.10e-06 -> mono {THEM(^Hare):1}   via THEM(^Hare) (9.10e-06, rho=1.00e-02 k*=100)
    - 2.29e-06 -> mono {and(THEM(ME),Hare):1}   via and(THEM(ME),Hare) (2.29e-06, rho=1.00e-02 k*=100)
    - 8.80e-07 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (8.80e-07, rho=1.00e-02 k*=100)
