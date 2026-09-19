### arm=weak, n=7, game=pd, N=10, w=1.0, x_on=True, role=False, mode=sparse

programs 9426, classes 105, states 765, terminal classes 1, indeterminate 0, divergence rate 0.0118, flow into polymorphic targets 1.81e-05
mean payoff -0.9791, efficient 0.0000, deadweight loss 0.9791, mean bits in support 2.84

| pi | state |
|---|---|
| 0.9667 | mono {D:1} |
| 0.0125 | mono {THEM(^C):1} |
| 0.0044 | mono {X:1} |
| 0.0032 | mono {C:1} |
| 0.0030 | mono {THEM(^X):1} |
| 0.0027 | mono {and(X,THEM(^X)):1} |
| 0.0024 | mono {and(X,THEM(^C)):1} |
| 0.0012 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 7.46e-04 -> mono {THEM(ME):1}   via THEM(ME) (7.46e-04, rho=1.00e-01 k*=10)
    - 4.74e-04 -> mono {THEM(^C):1}   via THEM(^C) (4.74e-04, rho=5.00e-01 k*=10)
    - 4.55e-04 -> mono {THEM(^X):1}   via THEM(^X) (4.55e-04, rho=5.00e-01 k*=10)
    - 9.48e-05 -> mono {THEM(^D):1}   via THEM(^D) (9.48e-05, rho=1.00e-01 k*=10)
    - 3.15e-05 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (3.15e-05, rho=1.00e-01 k*=10)
    - 1.67e-05 -> mono {and(X,THEM(^C)):1}   via and(X,THEM(^C)) (1.67e-05, rho=5.00e-01 k*=10)
- mono {THEM(^C):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 2.68e-03 -> mono {X:1}   via X (2.68e-03, rho=8.63e-03 k*=10)
    - 6.16e-04 -> mono {THEM(^D):1}   via THEM(^D) (6.16e-04, rho=6.50e-01 k*=10)
    - 4.08e-04 -> mono {THEM(^X):1}   via THEM(^X) (4.08e-04, rho=4.48e-01 k*=10)
    - 3.37e-04 -> mono {or(X,X):1}   via or(X,X) (3.37e-04, rho=4.17e-02 k*=10)
    - 2.76e-05 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (2.76e-05, rho=6.84e-02 k*=10)
- mono {X:1}
    - 2.14e-01 -> mono {D:1}   via D (2.14e-01, rho=6.50e-01 k*=10)
    - 3.63e-03 -> mono {and(X,X):1}   via and(X,X) (3.63e-03, rho=4.48e-01 k*=10)
    - 2.28e-04 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (2.28e-04, rho=5.65e-01 k*=10)
    - 2.05e-04 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (2.05e-04, rho=6.50e-01 k*=10)
    - 1.86e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.86e-04, rho=1.96e-01 k*=10)
    - 1.13e-04 -> mono {and(X,or(X,X)):1}   via and(X,or(X,X)) (1.13e-04, rho=2.80e-01 k*=10)
- mono {C:1}
    - 2.14e-01 -> mono {D:1}   via D (2.14e-01, rho=6.50e-01 k*=10)
    - 1.39e-01 -> mono {X:1}   via X (1.39e-01, rho=4.48e-01 k*=10)
    - 4.57e-03 -> mono {and(X,X):1}   via and(X,X) (4.57e-03, rho=5.65e-01 k*=10)
    - 2.27e-03 -> mono {or(X,X):1}   via or(X,X) (2.27e-03, rho=2.80e-01 k*=10)
    - 5.22e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (5.22e-04, rho=6.50e-01 k*=10)
    - 5.19e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (5.19e-04, rho=6.50e-01 k*=10)
- mono {THEM(^X):1}
    - 1.18e-01 -> mono {C:1}   via C (1.18e-01, rho=3.58e-01 k*=10)
    - 3.10e-02 -> mono {X:1}   via X (3.10e-02, rho=1.00e-01 k*=10)
    - 1.94e-03 -> mono {or(X,X):1}   via or(X,X) (1.94e-03, rho=2.40e-01 k*=10)
    - 6.16e-04 -> mono {THEM(^D):1}   via THEM(^D) (6.16e-04, rho=6.50e-01 k*=10)
    - 1.63e-04 -> poly {THEM(^X):0.7, or(THEM(ME),C):0.3}   via or(THEM(ME),C) (1.63e-04, rho=5.16e-01 k*=3)
    - 1.22e-04 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (1.22e-04, rho=3.03e-01 k*=10)
- mono {and(X,THEM(^X)):1}
    - 2.62e-03 -> mono {THEM(THEM):1}   via THEM(THEM) (2.62e-03, rho=7.06e-01 k*=10)
    - 1.93e-03 -> poly {THEM(ME):0.3, and(X,THEM(^X)):0.7}   via THEM(ME) (1.93e-03, rho=5.16e-01 k*=3)
    - 8.02e-04 -> mono {THEM(^D):1}   via THEM(^D) (8.02e-04, rho=8.46e-01 k*=10)
    - 4.11e-04 -> mono {THEM(^X):1}   via THEM(^X) (4.11e-04, rho=4.51e-01 k*=10)
    - 1.15e-04 -> poly {or(THEM(THEM),X):0.1, and(X,THEM(^X)):0.9}   via or(THEM(THEM),X) (1.15e-04, rho=1.00e+00 k*=1)
    - 4.91e-05 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (4.91e-05, rho=4.25e-01 k*=10)
- mono {and(X,THEM(^C)):1}
    - 2.62e-03 -> mono {THEM(THEM):1}   via THEM(THEM) (2.62e-03, rho=7.06e-01 k*=10)
    - 1.93e-03 -> poly {THEM(ME):0.3, and(X,THEM(^C)):0.7}   via THEM(ME) (1.93e-03, rho=5.16e-01 k*=3)
    - 8.02e-04 -> mono {THEM(^D):1}   via THEM(^D) (8.02e-04, rho=8.46e-01 k*=10)
    - 6.51e-04 -> mono {THEM(^X):1}   via THEM(^X) (6.51e-04, rho=7.14e-01 k*=10)
    - 4.27e-04 -> mono {THEM(^C):1}   via THEM(^C) (4.27e-04, rho=4.51e-01 k*=10)
    - 1.15e-04 -> poly {or(THEM(THEM),X):0.1, and(X,THEM(^C)):0.9}   via or(THEM(THEM),X) (1.15e-04, rho=1.00e+00 k*=1)
- mono {THEM(ME):1}
    - 2.85e-01 -> mono {C:1}   via C (2.85e-01, rho=8.67e-01 k*=10)
    - 2.69e-01 -> mono {X:1}   via X (2.69e-01, rho=8.67e-01 k*=10)
    - 3.29e-02 -> mono {D:1}   via D (3.29e-02, rho=1.00e-01 k*=10)
    - 7.01e-03 -> mono {or(X,X):1}   via or(X,X) (7.01e-03, rho=8.67e-01 k*=10)
    - 7.01e-03 -> mono {and(X,X):1}   via and(X,X) (7.01e-03, rho=8.67e-01 k*=10)
    - 8.21e-04 -> mono {THEM(^C):1}   via THEM(^C) (8.21e-04, rho=8.67e-01 k*=10)
