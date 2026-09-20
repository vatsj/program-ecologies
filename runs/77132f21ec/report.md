### arm=strong, n=6, game=stag, N=100, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 1726, classes 21, states 23, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 6.86e-11
mean payoff 3.0078, efficient 4.0000, deadweight loss 0.9922, mean bits in support 2.60

| pi | state |
|---|---|
| 0.9890 | mono {Hare:1} |
| 0.0081 | mono {Stag:1} |
| 0.0012 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Hare:1}
    - 3.84e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-05, rho=1.00e-02 k*=100)
    - 1.22e-06 -> mono {and(THEM(ME),Hare):1}   via and(THEM(ME),Hare) (1.22e-06, rho=1.00e-02 k*=100)
    - 9.32e-07 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (9.32e-07, rho=1.00e-02 k*=100)
    - 9.32e-07 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (9.32e-07, rho=1.00e-02 k*=100)
    - 9.30e-07 -> mono {X:1}   via X (9.30e-07, rho=2.96e-06 k*=100)
    - 8.59e-07 -> mono {and(X,X):1}   via and(X,X) (8.59e-07, rho=1.08e-04 k*=100)
- mono {Stag:1}
    - 2.72e-03 -> mono {Hare:1}   via Hare (2.72e-03, rho=8.20e-03 k*=100)
    - 1.40e-03 -> mono {X:1}   via X (1.40e-03, rho=4.46e-03 k*=100)
    - 4.98e-05 -> mono {and(X,X):1}   via and(X,X) (4.98e-05, rho=6.25e-03 k*=100)
    - 3.46e-05 -> mono {or(X,X):1}   via or(X,X) (3.46e-05, rho=4.34e-03 k*=100)
    - 6.99e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (6.99e-06, rho=8.20e-03 k*=100)
    - 2.35e-06 -> mono {THEM(ME):1}   via THEM(ME) (2.35e-06, rho=6.11e-04 k*=100)
- mono {THEM(ME):1}
    - 2.72e-02 -> mono {Stag:1}   via Stag (2.72e-02, rho=8.21e-02 k*=100)
    - 3.32e-03 -> mono {Hare:1}   via Hare (3.32e-03, rho=1.00e-02 k*=100)
    - 4.90e-04 -> mono {X:1}   via X (4.90e-04, rho=1.56e-03 k*=100)
    - 7.98e-05 -> mono {or(X,X):1}   via or(X,X) (7.98e-05, rho=1.00e-02 k*=100)
    - 1.24e-05 -> mono {and(X,X):1}   via and(X,X) (1.24e-05, rho=1.56e-03 k*=100)
    - 1.00e-05 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (1.00e-05, rho=3.32e-02 k*=100)
