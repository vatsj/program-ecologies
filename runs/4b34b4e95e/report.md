### arm=weak, n=6, game=exchange, N=100, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 48, states 663, terminal classes 1, indeterminate 63, divergence rate 0.0019, flow into polymorphic targets 1.97e-05
mean payoff 0.0481, efficient 2.0000, deadweight loss 1.9519, mean bits in support 2.80

| pi | state |
|---|---|
| 0.9732 | mono {D:1} |
| 0.0213 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 9.25e-05 -> mono {THEM(^C):1}   via THEM(^C) (9.25e-05, rho=1.02e-01 k*=100)
    - 6.55e-05 -> mono {THEM(^X):1}   via THEM(^X) (6.55e-05, rho=7.42e-02 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 9.10e-06 -> mono {THEM(^D):1}   via THEM(^D) (9.10e-06, rho=1.00e-02 k*=100)
    - 2.29e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (2.29e-06, rho=1.00e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 5.85e-04 -> mono {THEM(^D):1}   via THEM(^D) (5.85e-04, rho=6.43e-01 k*=100)
    - 3.56e-04 -> mono {THEM(^X):1}   via THEM(^X) (3.56e-04, rho=4.03e-01 k*=100)
    - 1.08e-05 -> mono {or(X,THEM(^D)):1}   via or(X,THEM(^D)) (1.08e-05, rho=4.07e-01 k*=100)
    - 7.15e-06 -> mono {THEM(^and(X,X)):1}   via THEM(^and(X,X)) (7.15e-06, rho=5.38e-01 k*=100)
    - 6.20e-06 -> mono {or(X,THEM(^X)):1}   via or(X,THEM(^X)) (6.20e-06, rho=2.33e-01 k*=100)

INDETERMINATE transitions (replicator did not converge): 63; first: from poly {X:0.5, THEM(THEM):0.25, and(X,THEM(^C)):0.25} with mutant or(X,THEM(^D))
