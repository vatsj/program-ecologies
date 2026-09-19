### arm=weak, n=6, game=pd, N=1000, w=1.0, x_on=True, role=False, mode=square

programs 1852, classes 48, states 834, terminal classes 1, indeterminate 179, divergence rate 0.0019, flow into polymorphic targets 8.22e-05
mean payoff -0.7051, efficient 0.0000, deadweight loss 0.7051, mean bits in support 5.14

| pi | state |
|---|---|
| 0.6950 | mono {D:1} |
| 0.2879 | mono {THEM(^C):1} |
| 0.0024 | mono {THEM(^X):1} |
| 0.0021 | mono {C:1} |
| 0.0018 | mono {X:1} |
| 0.0017 | mono {and(X,THEM(^X)):1} |
| 0.0015 | mono {and(X,THEM(^C)):1} |
| 0.0013 | poly {C:0.091, THEM(ME):0.182, and(X,THEM(^X)):0.727} |
| 0.0010 | poly {THEM(ME):0.333, and(X,THEM(^C)):0.667} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 4.55e-04 -> mono {THEM(^C):1}   via THEM(^C) (4.55e-04, rho=5.00e-01 k*=1000)
    - 4.41e-04 -> mono {THEM(^X):1}   via THEM(^X) (4.41e-04, rho=5.00e-01 k*=1000)
    - 1.33e-05 -> mono {and(X,THEM(^C)):1}   via and(X,THEM(^C)) (1.33e-05, rho=4.99e-01 k*=1000)
    - 1.32e-05 -> mono {and(X,THEM(^X)):1}   via and(X,THEM(^X)) (1.32e-05, rho=4.98e-01 k*=1000)
    - 6.64e-06 -> mono {THEM(^or(X,X)):1}   via THEM(^or(X,X)) (6.64e-06, rho=5.00e-01 k*=1000)
    - 6.63e-06 -> mono {THEM(^and(X,X)):1}   via THEM(^and(X,X)) (6.63e-06, rho=4.99e-01 k*=1000)
- mono {THEM(^C):1}
    - 4.56e-04 -> mono {THEM(^D):1}   via THEM(^D) (4.56e-04, rho=5.02e-01 k*=1000)
    - 3.29e-04 -> mono {C:1}   via C (3.29e-04, rho=1.00e-03 k*=1000)
    - 2.95e-04 -> mono {THEM(^X):1}   via THEM(^X) (2.95e-04, rho=3.34e-01 k*=1000)
    - 8.89e-06 -> mono {or(X,THEM(^D)):1}   via or(X,THEM(^D)) (8.89e-06, rho=3.35e-01 k*=1000)
    - 5.71e-06 -> mono {THEM(^and(X,X)):1}   via THEM(^and(X,X)) (5.71e-06, rho=4.30e-01 k*=1000)
    - 5.34e-06 -> mono {or(X,THEM(^X)):1}   via or(X,THEM(^X)) (5.34e-06, rho=2.01e-01 k*=1000)
- mono {THEM(^X):1}
    - 1.64e-01 -> mono {C:1}   via C (1.64e-01, rho=4.99e-01 k*=1000)
    - 2.51e-03 -> mono {or(X,X):1}   via or(X,X) (2.51e-03, rho=3.32e-01 k*=1000)
    - 4.56e-04 -> mono {THEM(^D):1}   via THEM(^D) (4.56e-04, rho=5.01e-01 k*=1000)
    - 3.12e-04 -> mono {X:1}   via X (3.12e-04, rho=1.00e-03 k*=1000)
    - 1.21e-04 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (1.21e-04, rho=4.28e-01 k*=1000)
    - 5.71e-05 -> poly {THEM(^X):0.667, or(THEM(THEM),C):0.333}   via or(THEM(THEM),C) (5.71e-05, rho=4.98e-01 k*=333)
- mono {C:1}
    - 1.65e-01 -> mono {D:1}   via D (1.65e-01, rho=5.02e-01 k*=1000)
    - 1.04e-01 -> mono {X:1}   via X (1.04e-01, rho=3.34e-01 k*=1000)
    - 3.24e-03 -> mono {and(X,X):1}   via and(X,X) (3.24e-03, rho=4.30e-01 k*=1000)
    - 1.51e-03 -> mono {or(X,X):1}   via or(X,X) (1.51e-03, rho=2.01e-01 k*=1000)
    - 3.99e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (3.99e-04, rho=5.02e-01 k*=1000)
    - 3.99e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (3.99e-04, rho=5.02e-01 k*=1000)
- mono {X:1}
    - 1.65e-01 -> mono {D:1}   via D (1.65e-01, rho=5.01e-01 k*=1000)
    - 2.52e-03 -> mono {and(X,X):1}   via and(X,X) (2.52e-03, rho=3.34e-01 k*=1000)
    - 1.21e-04 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.21e-04, rho=4.30e-01 k*=1000)
    - 5.75e-05 -> mono {and(THEM(THEM),D):1}   via and(THEM(THEM),D) (5.75e-05, rho=5.01e-01 k*=1000)
    - 5.75e-05 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (5.75e-05, rho=5.01e-01 k*=1000)
    - 5.67e-05 -> mono {and(X,or(X,X)):1}   via and(X,or(X,X)) (5.67e-05, rho=2.01e-01 k*=1000)
- mono {and(X,THEM(^X)):1}
    - 2.45e-03 -> mono {THEM(THEM):1}   via THEM(THEM) (2.45e-03, rho=6.67e-01 k*=1000)
    - 1.83e-03 -> poly {THEM(ME):0.333, and(X,THEM(^X)):0.667}   via THEM(ME) (1.83e-03, rho=4.98e-01 k*=333)
    - 6.83e-04 -> mono {THEM(^D):1}   via THEM(^D) (6.83e-04, rho=7.51e-01 k*=1000)
    - 4.41e-04 -> mono {THEM(^X):1}   via THEM(^X) (4.41e-04, rho=4.99e-01 k*=1000)
    - 2.94e-05 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (2.94e-05, rho=3.34e-01 k*=1000)
    - 2.94e-05 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (2.94e-05, rho=3.34e-01 k*=1000)
- mono {and(X,THEM(^C)):1}
    - 2.45e-03 -> mono {THEM(THEM):1}   via THEM(THEM) (2.45e-03, rho=6.67e-01 k*=1000)
    - 1.83e-03 -> poly {THEM(ME):0.333, and(X,THEM(^C)):0.667}   via THEM(ME) (1.83e-03, rho=4.98e-01 k*=333)
    - 6.83e-04 -> mono {THEM(^D):1}   via THEM(^D) (6.83e-04, rho=7.51e-01 k*=1000)
    - 5.89e-04 -> mono {THEM(^X):1}   via THEM(^X) (5.89e-04, rho=6.67e-01 k*=1000)
    - 4.55e-04 -> mono {THEM(^C):1}   via THEM(^C) (4.55e-04, rho=4.99e-01 k*=1000)
    - 2.94e-05 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (2.94e-05, rho=3.34e-01 k*=1000)
- poly {C:0.091, THEM(ME):0.182, and(X,THEM(^X)):0.727}
    - 9.14e-04 -> poly {C:0.267, THEM(THEM):0.2, and(X,THEM(^X)):0.533}   via THEM(THEM) (9.14e-04, rho=2.49e-01 k*=200)
    - 9.10e-04 -> poly {C:0.091, THEM(ME):0.182, THEM(^C):0.001, and(X,THEM(^X)):0.726}   via THEM(^C) (9.10e-04, rho=1.00e+00 k*=1)
    - 3.65e-04 -> poly {C:0.4, THEM(^D):0.2, and(X,THEM(^X)):0.4}   via THEM(^D) (3.65e-04, rho=4.01e-01 k*=200)
    - 2.21e-04 -> poly {C:0.25, THEM(^X):0.25, and(X,THEM(^X)):0.5}   via THEM(^X) (2.21e-04, rho=2.50e-01 k*=250)
    - 8.80e-05 -> poly {C:0.091, THEM(ME):0.182, and(THEM(THEM),X):0.001, and(X,THEM(^X)):0.726}   via and(THEM(THEM),X) (8.80e-05, rho=1.00e+00 k*=1)
    - 8.80e-05 -> poly {C:0.091, THEM(ME):0.182, and(THEM(ME),X):0.001, and(X,THEM(^X)):0.726}   via and(THEM(ME),X) (8.80e-05, rho=1.00e+00 k*=1)
- poly {THEM(ME):0.333, and(X,THEM(^C)):0.667}
    - 1.23e-03 -> mono {THEM(THEM):1}   via THEM(THEM) (1.23e-03, rho=3.34e-01 k*=1000)
    - 4.54e-04 -> mono {THEM(^C):1}   via THEM(^C) (4.54e-04, rho=4.99e-01 k*=1000)
    - 4.42e-04 -> mono {THEM(^X):1}   via THEM(^X) (4.42e-04, rho=5.00e-01 k*=1000)
    - 3.42e-04 -> mono {THEM(^D):1}   via THEM(^D) (3.42e-04, rho=5.02e-01 k*=750)
    - 1.14e-04 -> mono {THEM(ME):1}   via THEM(^D) (1.14e-04, rho=5.02e-01 k*=750)
    - 2.91e-05 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (2.91e-05, rho=3.30e-01 k*=1000)

INDETERMINATE transitions (replicator did not converge): 179; first: from poly {C:0.294, THEM(THEM):0.118, THEM(^X):0.118, and(X,THEM(^X)):0.47} with mutant and(X,and(X,X))
