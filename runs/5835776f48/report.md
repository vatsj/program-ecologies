### arm=weak, n=6, game=pd, N=10, w=1.0, x_on=True, role=False, mode=square

programs 1852, classes 48, states 142, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 1.42e-05
mean payoff -0.9801, efficient 0.0000, deadweight loss 0.9801, mean bits in support 2.81

| pi | state |
|---|---|
| 0.9692 | mono {D:1} |
| 0.0120 | mono {THEM(^C):1} |
| 0.0043 | mono {X:1} |
| 0.0031 | mono {C:1} |
| 0.0029 | mono {THEM(^X):1} |
| 0.0022 | mono {and(X,THEM(^X)):1} |
| 0.0020 | mono {and(X,THEM(^C)):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 4.55e-04 -> mono {THEM(^C):1}   via THEM(^C) (4.55e-04, rho=5.00e-01 k*=10)
    - 4.42e-04 -> mono {THEM(^X):1}   via THEM(^X) (4.42e-04, rho=5.00e-01 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
    - 9.10e-05 -> mono {THEM(^D):1}   via THEM(^D) (9.10e-05, rho=1.00e-01 k*=10)
    - 1.33e-05 -> mono {and(X,THEM(^C)):1}   via and(X,THEM(^C)) (1.33e-05, rho=5.00e-01 k*=10)
- mono {THEM(^C):1}
    - 3.29e-02 -> mono {C:1}   via C (3.29e-02, rho=1.00e-01 k*=10)
    - 2.70e-03 -> mono {X:1}   via X (2.70e-03, rho=8.63e-03 k*=10)
    - 5.91e-04 -> mono {THEM(^D):1}   via THEM(^D) (5.91e-04, rho=6.50e-01 k*=10)
    - 3.96e-04 -> mono {THEM(^X):1}   via THEM(^X) (3.96e-04, rho=4.48e-01 k*=10)
    - 3.15e-04 -> mono {or(X,X):1}   via or(X,X) (3.15e-04, rho=4.17e-02 k*=10)
    - 1.93e-05 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (1.93e-05, rho=6.84e-02 k*=10)
- mono {X:1}
    - 2.14e-01 -> mono {D:1}   via D (2.14e-01, rho=6.50e-01 k*=10)
    - 3.38e-03 -> mono {and(X,X):1}   via and(X,X) (3.38e-03, rho=4.48e-01 k*=10)
    - 1.79e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.79e-04, rho=1.96e-01 k*=10)
    - 1.60e-04 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.60e-04, rho=5.65e-01 k*=10)
    - 8.83e-05 -> mono {THEM(^X):1}   via THEM(^X) (8.83e-05, rho=1.00e-01 k*=10)
    - 7.91e-05 -> mono {and(X,or(X,X)):1}   via and(X,or(X,X)) (7.91e-05, rho=2.80e-01 k*=10)
- mono {C:1}
    - 2.14e-01 -> mono {D:1}   via D (2.14e-01, rho=6.50e-01 k*=10)
    - 1.40e-01 -> mono {X:1}   via X (1.40e-01, rho=4.48e-01 k*=10)
    - 4.26e-03 -> mono {and(X,X):1}   via and(X,X) (4.26e-03, rho=5.65e-01 k*=10)
    - 2.11e-03 -> mono {or(X,X):1}   via or(X,X) (2.11e-03, rho=2.80e-01 k*=10)
    - 5.17e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (5.17e-04, rho=6.50e-01 k*=10)
    - 5.17e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (5.17e-04, rho=6.50e-01 k*=10)
- mono {THEM(^X):1}
    - 1.18e-01 -> mono {C:1}   via C (1.18e-01, rho=3.58e-01 k*=10)
    - 3.12e-02 -> mono {X:1}   via X (3.12e-02, rho=1.00e-01 k*=10)
    - 1.81e-03 -> mono {or(X,X):1}   via or(X,X) (1.81e-03, rho=2.40e-01 k*=10)
    - 5.91e-04 -> mono {THEM(^D):1}   via THEM(^D) (5.91e-04, rho=6.50e-01 k*=10)
    - 8.80e-05 -> poly {THEM(^X):0.9, or(THEM(ME),X):0.1}   via or(THEM(ME),X) (8.80e-05, rho=1.00e+00 k*=1)
    - 8.56e-05 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (8.56e-05, rho=3.03e-01 k*=10)
- mono {and(X,THEM(^X)):1}
    - 2.59e-03 -> mono {THEM(THEM):1}   via THEM(THEM) (2.59e-03, rho=7.06e-01 k*=10)
    - 1.90e-03 -> poly {THEM(ME):0.3, and(X,THEM(^X)):0.7}   via THEM(ME) (1.90e-03, rho=5.16e-01 k*=3)
    - 7.70e-04 -> mono {THEM(^D):1}   via THEM(^D) (7.70e-04, rho=8.46e-01 k*=10)
    - 3.98e-04 -> mono {THEM(^X):1}   via THEM(^X) (3.98e-04, rho=4.51e-01 k*=10)
    - 8.80e-05 -> poly {or(THEM(THEM),X):0.1, and(X,THEM(^X)):0.9}   via or(THEM(THEM),X) (8.80e-05, rho=1.00e+00 k*=1)
    - 3.74e-05 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (3.74e-05, rho=4.25e-01 k*=10)
- mono {and(X,THEM(^C)):1}
    - 2.59e-03 -> mono {THEM(THEM):1}   via THEM(THEM) (2.59e-03, rho=7.06e-01 k*=10)
    - 1.90e-03 -> poly {THEM(ME):0.3, and(X,THEM(^C)):0.7}   via THEM(ME) (1.90e-03, rho=5.16e-01 k*=3)
    - 7.70e-04 -> mono {THEM(^D):1}   via THEM(^D) (7.70e-04, rho=8.46e-01 k*=10)
    - 6.31e-04 -> mono {THEM(^X):1}   via THEM(^X) (6.31e-04, rho=7.14e-01 k*=10)
    - 4.10e-04 -> mono {THEM(^C):1}   via THEM(^C) (4.10e-04, rho=4.51e-01 k*=10)
    - 8.80e-05 -> poly {or(THEM(THEM),X):0.1, and(X,THEM(^C)):0.9}   via or(THEM(THEM),X) (8.80e-05, rho=1.00e+00 k*=1)
