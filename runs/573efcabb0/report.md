### arm=weak, n=6, game=pd, N=100, w=1.0, x_on=True, role=False, mode=square

programs 1852, classes 48, states 668, terminal classes 1, indeterminate 25, divergence rate 0.0019, flow into polymorphic targets 5.23e-04
mean payoff -0.8932, efficient 0.0000, deadweight loss 0.8932, mean bits in support 3.57

| pi | state |
|---|---|
| 0.8820 | mono {D:1} |
| 0.0988 | mono {THEM(^C):1} |
| 0.0029 | mono {C:1} |
| 0.0025 | mono {THEM(^X):1} |
| 0.0023 | mono {X:1} |
| 0.0021 | mono {and(X,THEM(^X)):1} |
| 0.0019 | mono {and(X,THEM(^C)):1} |
| 0.0015 | poly {C:0.09, THEM(ME):0.18, and(X,THEM(^X)):0.73} |
| 0.0013 | poly {THEM(ME):0.33, and(X,THEM(^C)):0.67} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 4.55e-04 -> mono {THEM(^C):1}   via THEM(^C) (4.55e-04, rho=5.00e-01 k*=100)
    - 4.42e-04 -> mono {THEM(^X):1}   via THEM(^X) (4.42e-04, rho=5.00e-01 k*=100)
    - 3.68e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 1.33e-05 -> mono {and(X,THEM(^C)):1}   via and(X,THEM(^C)) (1.33e-05, rho=5.00e-01 k*=100)
    - 1.33e-05 -> mono {and(X,THEM(^X)):1}   via and(X,THEM(^X)) (1.33e-05, rho=5.00e-01 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 4.69e-04 -> mono {THEM(^D):1}   via THEM(^D) (4.69e-04, rho=5.15e-01 k*=100)
    - 3.04e-04 -> mono {THEM(^X):1}   via THEM(^X) (3.04e-04, rho=3.44e-01 k*=100)
    - 9.21e-06 -> mono {or(X,THEM(^D)):1}   via or(X,THEM(^D)) (9.21e-06, rho=3.46e-01 k*=100)
    - 5.87e-06 -> mono {THEM(^and(X,X)):1}   via THEM(^and(X,X)) (5.87e-06, rho=4.42e-01 k*=100)
    - 5.58e-06 -> mono {or(X,THEM(^X)):1}   via or(X,THEM(^X)) (5.58e-06, rho=2.10e-01 k*=100)
- mono {C:1}
    - 1.69e-01 -> mono {D:1}   via D (1.69e-01, rho=5.15e-01 k*=100)
    - 1.08e-01 -> mono {X:1}   via X (1.08e-01, rho=3.44e-01 k*=100)
    - 3.33e-03 -> mono {and(X,X):1}   via and(X,X) (3.33e-03, rho=4.42e-01 k*=100)
    - 1.56e-03 -> mono {or(X,X):1}   via or(X,X) (1.56e-03, rho=2.07e-01 k*=100)
    - 4.10e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (4.10e-04, rho=5.15e-01 k*=100)
    - 4.10e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (4.10e-04, rho=5.15e-01 k*=100)
- mono {THEM(^X):1}
    - 1.61e-01 -> mono {C:1}   via C (1.61e-01, rho=4.90e-01 k*=100)
    - 3.12e-03 -> mono {X:1}   via X (3.12e-03, rho=1.00e-02 k*=100)
    - 2.43e-03 -> mono {or(X,X):1}   via or(X,X) (2.43e-03, rho=3.23e-01 k*=100)
    - 4.69e-04 -> mono {THEM(^D):1}   via THEM(^D) (4.69e-04, rho=5.15e-01 k*=100)
    - 1.18e-04 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (1.18e-04, rho=4.18e-01 k*=100)
    - 5.53e-05 -> poly {THEM(^X):0.67, or(THEM(THEM),C):0.33}   via or(THEM(THEM),C) (5.53e-05, rho=4.83e-01 k*=33)
- mono {X:1}
    - 1.69e-01 -> mono {D:1}   via D (1.69e-01, rho=5.15e-01 k*=100)
    - 2.60e-03 -> mono {and(X,X):1}   via and(X,X) (2.60e-03, rho=3.44e-01 k*=100)
    - 1.25e-04 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.25e-04, rho=4.42e-01 k*=100)
    - 6.59e-05 -> mono {THEM(^C):1}   via THEM(^C) (6.59e-05, rho=7.24e-02 k*=100)
    - 5.90e-05 -> mono {and(THEM(THEM),D):1}   via and(THEM(THEM),D) (5.90e-05, rho=5.15e-01 k*=100)
    - 5.90e-05 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (5.90e-05, rho=5.15e-01 k*=100)
- mono {and(X,THEM(^X)):1}
    - 2.46e-03 -> mono {THEM(THEM):1}   via THEM(THEM) (2.46e-03, rho=6.70e-01 k*=100)
    - 1.78e-03 -> poly {THEM(ME):0.33, and(X,THEM(^X)):0.67}   via THEM(ME) (1.78e-03, rho=4.83e-01 k*=33)
    - 6.91e-04 -> mono {THEM(^D):1}   via THEM(^D) (6.91e-04, rho=7.59e-01 k*=100)
    - 4.37e-04 -> mono {THEM(^X):1}   via THEM(^X) (4.37e-04, rho=4.95e-01 k*=100)
    - 2.99e-05 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (2.99e-05, rho=3.40e-01 k*=100)
    - 2.99e-05 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (2.99e-05, rho=3.40e-01 k*=100)
- mono {and(X,THEM(^C)):1}
    - 2.46e-03 -> mono {THEM(THEM):1}   via THEM(THEM) (2.46e-03, rho=6.70e-01 k*=100)
    - 1.78e-03 -> poly {THEM(ME):0.33, and(X,THEM(^C)):0.67}   via THEM(ME) (1.78e-03, rho=4.83e-01 k*=33)
    - 6.91e-04 -> mono {THEM(^D):1}   via THEM(^D) (6.91e-04, rho=7.59e-01 k*=100)
    - 5.93e-04 -> mono {THEM(^X):1}   via THEM(^X) (5.93e-04, rho=6.71e-01 k*=100)
    - 4.50e-04 -> mono {THEM(^C):1}   via THEM(^C) (4.50e-04, rho=4.95e-01 k*=100)
    - 2.99e-05 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (2.99e-05, rho=3.40e-01 k*=100)
- poly {C:0.09, THEM(ME):0.18, and(X,THEM(^X)):0.73}
    - 9.25e-04 -> poly {C:0.27, THEM(THEM):0.2, and(X,THEM(^X)):0.53}   via THEM(THEM) (9.25e-04, rho=2.52e-01 k*=20)
    - 9.10e-04 -> poly {C:0.1, THEM(ME):0.18, THEM(^C):0.01, and(X,THEM(^X)):0.71}   via THEM(^C) (9.10e-04, rho=1.00e+00 k*=1)
    - 3.77e-04 -> poly {C:0.4, THEM(^D):0.2, and(X,THEM(^X)):0.4}   via THEM(^D) (3.77e-04, rho=4.15e-01 k*=20)
    - 2.21e-04 -> poly {C:0.25, THEM(^X):0.25, and(X,THEM(^X)):0.5}   via THEM(^X) (2.21e-04, rho=2.50e-01 k*=25)
    - 8.80e-05 -> poly {C:0.09, THEM(ME):0.18, and(THEM(THEM),X):0.01, and(X,THEM(^X)):0.72}   via and(THEM(THEM),X) (8.80e-05, rho=1.00e+00 k*=1)
    - 8.80e-05 -> poly {C:0.09, THEM(ME):0.18, and(THEM(ME),X):0.01, and(X,THEM(^X)):0.72}   via and(THEM(ME),X) (8.80e-05, rho=1.00e+00 k*=1)
- poly {THEM(ME):0.33, and(X,THEM(^C)):0.67}
    - 1.26e-03 -> mono {THEM(THEM):1}   via THEM(THEM) (1.26e-03, rho=3.44e-01 k*=100)
    - 4.47e-04 -> mono {THEM(^C):1}   via THEM(^C) (4.47e-04, rho=4.91e-01 k*=100)
    - 4.46e-04 -> mono {THEM(^X):1}   via THEM(^X) (4.46e-04, rho=5.04e-01 k*=100)
    - 3.53e-04 -> mono {THEM(^D):1}   via THEM(^D) (3.53e-04, rho=5.17e-01 k*=75)
    - 1.18e-04 -> mono {THEM(ME):1}   via THEM(^D) (1.18e-04, rho=5.17e-01 k*=75)
    - 2.66e-05 -> poly {THEM(ME):0.33, and(X,THEM(^C)):0.66, and(X,THEM(^X)):0.01}   via and(X,THEM(^X)) (2.66e-05, rho=1.00e+00 k*=1)

INDETERMINATE transitions (replicator did not converge): 25; first: from poly {C:0.33, THEM(^C):0.65, and(X,THEM(^X)):0.02} with mutant THEM(^or(X,X))
