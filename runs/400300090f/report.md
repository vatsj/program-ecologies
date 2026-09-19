### arm=weak, n=6, game=exchange, N=100, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 48, states 805, terminal classes 1, indeterminate 68, divergence rate 0.0019, flow into polymorphic targets 1.68e-05
mean payoff 0.0372, efficient 2.0000, deadweight loss 1.9628, mean bits in support 2.75

| pi | state |
|---|---|
| 0.9773 | mono {D:1} |
| 0.0143 | mono {THEM(^C):1} |
| 0.0016 | mono {X:1} |
| 0.0010 | mono {C:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 5.32e-05 -> mono {THEM(^C):1}   via THEM(^C) (5.32e-05, rho=5.84e-02 k*=100)
    - 3.72e-05 -> mono {THEM(^X):1}   via THEM(^X) (3.72e-05, rho=4.21e-02 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 9.10e-06 -> mono {THEM(^D):1}   via THEM(^D) (9.10e-06, rho=1.00e-02 k*=100)
    - 2.29e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (2.29e-06, rho=1.00e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 2.42e-04 -> mono {THEM(^D):1}   via THEM(^D) (2.42e-04, rho=2.66e-01 k*=100)
    - 1.27e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.27e-04, rho=1.43e-01 k*=100)
    - 3.99e-06 -> mono {or(X,THEM(^D)):1}   via or(X,THEM(^D)) (3.99e-06, rho=1.50e-01 k*=100)
    - 2.75e-06 -> mono {THEM(^and(X,X)):1}   via THEM(^and(X,X)) (2.75e-06, rho=2.07e-01 k*=100)
    - 2.17e-06 -> mono {or(X,THEM(^X)):1}   via or(X,THEM(^X)) (2.17e-06, rho=8.16e-02 k*=100)
- mono {X:1}
    - 4.71e-02 -> mono {D:1}   via D (4.71e-02, rho=1.43e-01 k*=100)
    - 5.61e-04 -> mono {and(X,X):1}   via and(X,X) (5.61e-04, rho=7.44e-02 k*=100)
    - 3.83e-05 -> mono {THEM(^C):1}   via THEM(^C) (3.83e-05, rho=4.21e-02 k*=100)
    - 3.28e-05 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (3.28e-05, rho=1.43e-01 k*=100)
    - 3.09e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (3.09e-05, rho=1.09e-01 k*=100)
    - 1.09e-05 -> mono {and(X,or(X,X)):1}   via and(X,or(X,X)) (1.09e-05, rho=3.87e-02 k*=100)
- mono {C:1}
    - 8.75e-02 -> mono {D:1}   via D (8.75e-02, rho=2.66e-01 k*=100)
    - 4.47e-02 -> mono {X:1}   via X (4.47e-02, rho=1.43e-01 k*=100)
    - 1.56e-03 -> mono {and(X,X):1}   via and(X,X) (1.56e-03, rho=2.07e-01 k*=100)
    - 5.61e-04 -> mono {or(X,X):1}   via or(X,X) (5.61e-04, rho=7.44e-02 k*=100)
    - 2.12e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (2.12e-04, rho=2.66e-01 k*=100)
    - 2.12e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (2.12e-04, rho=2.66e-01 k*=100)

INDETERMINATE transitions (replicator did not converge): 68; first: from poly {C:0.33, X:0.17, THEM(THEM):0.17, and(X,THEM(^C)):0.33} with mutant or(X,THEM(^D))
