### arm=weak, n=7, game=pd, N=100, w=1.0, x_on=True, role=False, mode=sparse

programs 9426, classes 105, states 2434, terminal classes 1, indeterminate 183, divergence rate 0.0103, flow into polymorphic targets 5.92e-04
mean payoff -0.8898, efficient 0.0000, deadweight loss 0.8898, mean bits in support 3.62

| pi | state |
|---|---|
| 0.8765 | mono {D:1} |
| 0.1016 | mono {THEM(^C):1} |
| 0.0030 | mono {C:1} |
| 0.0026 | mono {THEM(^X):1} |
| 0.0026 | mono {and(X,THEM(^X)):1} |
| 0.0023 | mono {X:1} |
| 0.0023 | mono {and(X,THEM(^C)):1} |
| 0.0018 | poly {C:0.09, THEM(ME):0.18, and(X,THEM(^X)):0.73} |
| 0.0015 | poly {THEM(ME):0.33, and(X,THEM(^C)):0.67} |
| 0.0010 | poly {C:0.24, D:0.01, X:0.01, and(X,X):0.01, or(X,X):0.01, THEM(^X):0.27, and(X,THEM(^X)):0.45} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 4.74e-04 -> mono {THEM(^C):1}   via THEM(^C) (4.74e-04, rho=5.00e-01 k*=100)
    - 4.55e-04 -> mono {THEM(^X):1}   via THEM(^X) (4.55e-04, rho=5.00e-01 k*=100)
    - 7.46e-05 -> mono {THEM(ME):1}   via THEM(ME) (7.46e-05, rho=1.00e-02 k*=100)
    - 1.67e-05 -> mono {and(X,THEM(^C)):1}   via and(X,THEM(^C)) (1.67e-05, rho=5.00e-01 k*=100)
    - 1.67e-05 -> mono {and(X,THEM(^X)):1}   via and(X,THEM(^X)) (1.67e-05, rho=5.00e-01 k*=100)
    - 9.48e-06 -> mono {THEM(^D):1}   via THEM(^D) (9.48e-06, rho=1.00e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 4.88e-04 -> mono {THEM(^D):1}   via THEM(^D) (4.88e-04, rho=5.15e-01 k*=100)
    - 3.14e-04 -> mono {THEM(^X):1}   via THEM(^X) (3.14e-04, rho=3.44e-01 k*=100)
    - 1.16e-05 -> mono {or(X,THEM(^D)):1}   via or(X,THEM(^D)) (1.16e-05, rho=3.46e-01 k*=100)
    - 8.16e-06 -> mono {THEM(^and(X,X)):1}   via THEM(^and(X,X)) (8.16e-06, rho=4.42e-01 k*=100)
    - 7.00e-06 -> mono {or(X,THEM(^X)):1}   via or(X,THEM(^X)) (7.00e-06, rho=2.10e-01 k*=100)
- mono {C:1}
    - 1.69e-01 -> mono {D:1}   via D (1.69e-01, rho=5.15e-01 k*=100)
    - 1.07e-01 -> mono {X:1}   via X (1.07e-01, rho=3.44e-01 k*=100)
    - 3.57e-03 -> mono {and(X,X):1}   via and(X,X) (3.57e-03, rho=4.42e-01 k*=100)
    - 1.68e-03 -> mono {or(X,X):1}   via or(X,X) (1.68e-03, rho=2.07e-01 k*=100)
    - 4.13e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (4.13e-04, rho=5.15e-01 k*=100)
    - 4.11e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (4.11e-04, rho=5.15e-01 k*=100)
- mono {THEM(^X):1}
    - 1.61e-01 -> mono {C:1}   via C (1.61e-01, rho=4.90e-01 k*=100)
    - 3.10e-03 -> mono {X:1}   via X (3.10e-03, rho=1.00e-02 k*=100)
    - 2.61e-03 -> mono {or(X,X):1}   via or(X,X) (2.61e-03, rho=3.23e-01 k*=100)
    - 4.88e-04 -> mono {THEM(^D):1}   via THEM(^D) (4.88e-04, rho=5.15e-01 k*=100)
    - 1.69e-04 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (1.69e-04, rho=4.18e-01 k*=100)
    - 1.52e-04 -> poly {THEM(^X):0.67, or(THEM(ME),C):0.33}   via or(THEM(ME),C) (1.52e-04, rho=4.83e-01 k*=33)
- mono {and(X,THEM(^X)):1}
    - 2.49e-03 -> mono {THEM(THEM):1}   via THEM(THEM) (2.49e-03, rho=6.70e-01 k*=100)
    - 1.81e-03 -> poly {THEM(ME):0.33, and(X,THEM(^X)):0.67}   via THEM(ME) (1.81e-03, rho=4.83e-01 k*=33)
    - 7.19e-04 -> mono {THEM(^D):1}   via THEM(^D) (7.19e-04, rho=7.59e-01 k*=100)
    - 4.51e-04 -> mono {THEM(^X):1}   via THEM(^X) (4.51e-04, rho=4.95e-01 k*=100)
    - 3.92e-05 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (3.92e-05, rho=3.40e-01 k*=100)
    - 3.92e-05 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (3.92e-05, rho=3.40e-01 k*=100)
- mono {X:1}
    - 1.69e-01 -> mono {D:1}   via D (1.69e-01, rho=5.15e-01 k*=100)
    - 2.79e-03 -> mono {and(X,X):1}   via and(X,X) (2.79e-03, rho=3.44e-01 k*=100)
    - 1.78e-04 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.78e-04, rho=4.42e-01 k*=100)
    - 1.62e-04 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.62e-04, rho=5.15e-01 k*=100)
    - 8.36e-05 -> mono {and(X,or(X,X)):1}   via and(X,or(X,X)) (8.36e-05, rho=2.07e-01 k*=100)
    - 6.86e-05 -> mono {THEM(^C):1}   via THEM(^C) (6.86e-05, rho=7.24e-02 k*=100)
- mono {and(X,THEM(^C)):1}
    - 2.49e-03 -> mono {THEM(THEM):1}   via THEM(THEM) (2.49e-03, rho=6.70e-01 k*=100)
    - 1.81e-03 -> poly {THEM(ME):0.33, and(X,THEM(^C)):0.67}   via THEM(ME) (1.81e-03, rho=4.83e-01 k*=33)
    - 7.19e-04 -> mono {THEM(^D):1}   via THEM(^D) (7.19e-04, rho=7.59e-01 k*=100)
    - 6.11e-04 -> mono {THEM(^X):1}   via THEM(^X) (6.11e-04, rho=6.71e-01 k*=100)
    - 4.69e-04 -> mono {THEM(^C):1}   via THEM(^C) (4.69e-04, rho=4.95e-01 k*=100)
    - 3.92e-05 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (3.92e-05, rho=3.40e-01 k*=100)
- poly {C:0.09, THEM(ME):0.18, and(X,THEM(^X)):0.73}
    - 9.48e-04 -> poly {C:0.1, THEM(ME):0.18, THEM(^C):0.01, and(X,THEM(^X)):0.71}   via THEM(^C) (9.48e-04, rho=1.00e+00 k*=1)
    - 9.38e-04 -> poly {C:0.27, THEM(THEM):0.2, and(X,THEM(^X)):0.53}   via THEM(THEM) (9.38e-04, rho=2.52e-01 k*=20)
    - 3.93e-04 -> poly {C:0.4, THEM(^D):0.2, and(X,THEM(^X)):0.4}   via THEM(^D) (3.93e-04, rho=4.15e-01 k*=20)
    - 2.28e-04 -> poly {C:0.25, THEM(^X):0.25, and(X,THEM(^X)):0.5}   via THEM(^X) (2.28e-04, rho=2.50e-01 k*=25)
    - 1.15e-04 -> poly {C:0.09, THEM(ME):0.18, and(THEM(THEM),X):0.01, and(X,THEM(^X)):0.72}   via and(THEM(THEM),X) (1.15e-04, rho=1.00e+00 k*=1)
    - 1.15e-04 -> poly {C:0.09, THEM(ME):0.18, and(THEM(ME),X):0.01, and(X,THEM(^X)):0.72}   via and(THEM(ME),X) (1.15e-04, rho=1.00e+00 k*=1)
- poly {THEM(ME):0.33, and(X,THEM(^C)):0.67}
    - 1.28e-03 -> mono {THEM(THEM):1}   via THEM(THEM) (1.28e-03, rho=3.44e-01 k*=100)
    - 4.65e-04 -> mono {THEM(^C):1}   via THEM(^C) (4.65e-04, rho=4.91e-01 k*=100)
    - 4.59e-04 -> mono {THEM(^X):1}   via THEM(^X) (4.59e-04, rho=5.04e-01 k*=100)
    - 3.68e-04 -> mono {THEM(^D):1}   via THEM(^D) (3.68e-04, rho=5.17e-01 k*=75)
    - 1.23e-04 -> mono {THEM(ME):1}   via THEM(^D) (1.22e-04, rho=5.17e-01 k*=75), THEM(^not(THEM(ME))) (4.60e-07, rho=5.17e-01 k*=75), and(THEM(ME),THEM(THEM)) (2.64e-07, rho=4.44e-01 k*=83), and(THEM(THEM),THEM(THEM)) (1.84e-07, rho=4.83e-01 k*=79)
    - 3.47e-05 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (3.47e-05, rho=3.01e-01 k*=100)
- poly {C:0.24, D:0.01, X:0.01, and(X,X):0.01, or(X,X):0.01, THEM(^X):0.27, and(X,THEM(^X)):0.45}
    - 9.18e-04 -> poly {C:0.23, D:0.01, X:0.01, and(X,X):0.01, or(X,X):0.01, THEM(^X):0.28, and(X,THEM(^X)):0.45}   via not(THEM(ME)) (7.99e-04, rho=1.00e+00 k*=1), not(THEM(^D)) (1.15e-04, rho=1.00e+00 k*=1), not(THEM(^THEM(ME))) (3.57e-06, rho=1.00e+00 k*=1)
    - 5.74e-04 -> poly {C:0.2, D:0.16, X:0.04, and(X,X):0.08, or(X,X):0.02, THEM(^X):0.5}   via THEM(THEM) (5.74e-04, rho=1.54e-01 k*=9), and(or(X,X),THEM(THEM)) (2.28e-07, rho=1.28e-01 k*=11), and(THEM(THEM),or(X,X)) (2.28e-07, rho=1.28e-01 k*=11)
    - 4.03e-04 -> poly {C:0.23, D:0.01, X:0.01, and(X,X):0.01, or(X,X):0.01, THEM(^X):0.27, or(X,or(X,X)):0.01, and(X,THEM(^X)):0.45}   via or(X,or(X,X)) (4.03e-04, rho=1.00e+00 k*=1)
    - 4.03e-04 -> poly {C:0.23, D:0.01, X:0.01, and(X,X):0.01, or(X,X):0.01, THEM(^X):0.28, and(X,or(X,X)):0.01, and(X,THEM(^X)):0.44}   via and(X,or(X,X)) (4.03e-04, rho=1.00e+00 k*=1)
    - 4.03e-04 -> poly {C:0.23, D:0.01, X:0.01, and(X,X):0.01, or(X,X):0.01, THEM(^X):0.28, or(X,and(X,X)):0.01, and(X,THEM(^X)):0.44}   via or(X,and(X,X)) (4.03e-04, rho=1.00e+00 k*=1)
    - 4.03e-04 -> poly {C:0.23, D:0.01, X:0.01, and(X,X):0.01, or(X,X):0.01, THEM(^X):0.28, and(X,and(X,X)):0.01, and(X,THEM(^X)):0.44}   via and(X,and(X,X)) (4.03e-04, rho=1.00e+00 k*=1)

INDETERMINATE transitions (replicator did not converge): 183; first: from poly {C:0.33, THEM(^C):0.65, and(X,THEM(^X)):0.02} with mutant THEM(^or(X,X))
