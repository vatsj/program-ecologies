### arm=weak, n=6, game=exchange, N=100, w=1.0, x_on=True, role=False, mode=square

programs 1852, classes 48, states 783, terminal classes 1, indeterminate 69, divergence rate 0.0019, flow into polymorphic targets 2.16e-05
mean payoff 0.0580, efficient 2.0000, deadweight loss 1.9420, mean bits in support 2.83

| pi | state |
|---|---|
| 0.9668 | mono {D:1} |
| 0.0237 | mono {THEM(^C):1} |
| 0.0015 | mono {X:1} |
| 0.0014 | mono {C:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 8.95e-05 -> mono {THEM(^C):1}   via THEM(^C) (8.95e-05, rho=9.84e-02 k*=100)
    - 6.40e-05 -> mono {THEM(^X):1}   via THEM(^X) (6.40e-05, rho=7.24e-02 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 9.10e-06 -> mono {THEM(^D):1}   via THEM(^D) (9.10e-06, rho=1.00e-02 k*=100)
    - 2.29e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (2.29e-06, rho=1.00e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 2.39e-04 -> mono {THEM(^D):1}   via THEM(^D) (2.39e-04, rho=2.63e-01 k*=100)
    - 1.33e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.33e-04, rho=1.51e-01 k*=100)
    - 4.17e-06 -> mono {or(X,THEM(^D)):1}   via or(X,THEM(^D)) (4.17e-06, rho=1.57e-01 k*=100)
    - 2.80e-06 -> mono {THEM(^and(X,X)):1}   via THEM(^and(X,X)) (2.80e-06, rho=2.11e-01 k*=100)
    - 2.34e-06 -> mono {or(X,THEM(^X)):1}   via or(X,THEM(^X)) (2.34e-06, rho=8.80e-02 k*=100)
- mono {X:1}
    - 6.94e-02 -> mono {D:1}   via D (6.94e-02, rho=2.11e-01 k*=100)
    - 8.86e-04 -> mono {and(X,X):1}   via and(X,X) (8.86e-04, rho=1.17e-01 k*=100)
    - 4.83e-05 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (4.83e-05, rho=2.11e-01 k*=100)
    - 4.80e-05 -> mono {THEM(^C):1}   via THEM(^C) (4.80e-05, rho=5.27e-02 k*=100)
    - 4.70e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (4.70e-05, rho=1.67e-01 k*=100)
    - 1.76e-05 -> mono {and(X,or(X,X)):1}   via and(X,or(X,X)) (1.76e-05, rho=6.23e-02 k*=100)
- mono {C:1}
    - 8.66e-02 -> mono {D:1}   via D (8.66e-02, rho=2.63e-01 k*=100)
    - 4.71e-02 -> mono {X:1}   via X (4.71e-02, rho=1.51e-01 k*=100)
    - 1.59e-03 -> mono {and(X,X):1}   via and(X,X) (1.59e-03, rho=2.11e-01 k*=100)
    - 6.14e-04 -> mono {or(X,X):1}   via or(X,X) (6.14e-04, rho=8.14e-02 k*=100)
    - 2.09e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (2.09e-04, rho=2.63e-01 k*=100)
    - 2.09e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (2.09e-04, rho=2.63e-01 k*=100)

INDETERMINATE transitions (replicator did not converge): 69; first: from poly {X:0.5, THEM(THEM):0.25, and(X,THEM(^C)):0.25} with mutant or(X,THEM(^D))
