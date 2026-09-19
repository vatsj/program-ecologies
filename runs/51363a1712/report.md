### arm=weak, n=6, game=exchange, N=1000, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 48, states 1071, terminal classes 1, indeterminate 92, divergence rate 0.0019, flow into polymorphic targets 4.60e-06
mean payoff 0.0482, efficient 2.0000, deadweight loss 1.9518, mean bits in support 2.80

| pi | state |
|---|---|
| 0.9734 | mono {D:1} |
| 0.0215 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.02e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.02e-05, rho=1.12e-02 k*=1000)
    - 7.00e-06 -> mono {THEM(^X):1}   via THEM(^X) (7.00e-06, rho=7.92e-03 k*=1000)
    - 3.69e-06 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-06, rho=1.00e-03 k*=1000)
    - 3.67e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-06, rho=1.00e-03 k*=1000)
    - 9.10e-07 -> mono {THEM(^D):1}   via THEM(^D) (9.10e-07, rho=1.00e-03 k*=1000)
    - 2.29e-07 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (2.29e-07, rho=1.00e-03 k*=1000)
- mono {THEM(^C):1}
    - 3.29e-04 -> mono {C:1}   via C (3.29e-04, rho=1.00e-03 k*=1000)
    - 8.69e-05 -> mono {THEM(^D):1}   via THEM(^D) (8.69e-05, rho=9.54e-02 k*=1000)
    - 4.32e-05 -> mono {THEM(^X):1}   via THEM(^X) (4.32e-05, rho=4.89e-02 k*=1000)
    - 1.32e-06 -> mono {or(X,THEM(^D)):1}   via or(X,THEM(^D)) (1.32e-06, rho=4.98e-02 k*=1000)
    - 9.63e-07 -> mono {THEM(^and(X,X)):1}   via THEM(^and(X,X)) (9.63e-07, rho=7.25e-02 k*=1000)
    - 6.82e-07 -> mono {or(X,THEM(^X)):1}   via or(X,THEM(^X)) (6.82e-07, rho=2.57e-02 k*=1000)

INDETERMINATE transitions (replicator did not converge): 92; first: from poly {C:0.333, X:0.167, THEM(THEM):0.167, and(X,THEM(^C)):0.333} with mutant or(X,THEM(^D))
