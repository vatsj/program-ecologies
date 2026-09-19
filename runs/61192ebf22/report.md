### arm=weak, n=6, game=stag, N=100, w=1.0, x_on=True, role=False, mode=square

programs 1852, classes 46, states 111, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 6.80e-05
mean payoff 3.0725, efficient 4.0000, deadweight loss 0.9275, mean bits in support 2.70

| pi | state |
|---|---|
| 0.9221 | mono {D:1} |
| 0.0625 | mono {C:1} |
| 0.0099 | mono {THEM(^C):1} |
| 0.0018 | poly {C:0.5, X:0.5} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 3.46e-05 -> mono {THEM(^C):1}   via THEM(^C) (3.46e-05, rho=3.81e-02 k*=100)
    - 9.10e-06 -> mono {THEM(^D):1}   via THEM(^D) (9.10e-06, rho=1.00e-02 k*=100)
    - 2.29e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (2.29e-06, rho=1.00e-02 k*=100)
    - 8.80e-07 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (8.80e-07, rho=1.00e-02 k*=100)
- mono {C:1}
    - 8.73e-04 -> poly {C:0.5, X:0.5}   via X (8.73e-04, rho=2.79e-03 k*=50)
    - 8.48e-04 -> mono {D:1}   via D (8.48e-04, rho=2.58e-03 k*=100)
    - 1.59e-05 -> mono {and(X,X):1}   via and(X,X) (1.59e-05, rho=2.11e-03 k*=100)
    - 1.11e-05 -> mono {or(X,X):1}   via or(X,X) (1.11e-05, rho=1.47e-03 k*=100)
    - 9.10e-06 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-06, rho=1.00e-02 k*=100)
    - 2.05e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (2.05e-06, rho=2.58e-03 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 2.47e-06 -> poly {THEM(^C):0.5, THEM(^X):0.5}   via THEM(^X) (2.47e-06, rho=2.79e-03 k*=50)
    - 2.35e-06 -> mono {THEM(^D):1}   via THEM(^D) (2.35e-06, rho=2.58e-03 k*=100)
    - 8.80e-07 -> mono {or(X,THEM(THEM)):1}   via or(X,THEM(THEM)) (8.80e-07, rho=1.00e-02 k*=100)
    - 8.80e-07 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (8.80e-07, rho=1.00e-02 k*=100)
    - 2.66e-07 -> mono {or(X,THEM(^C)):1}   via or(X,THEM(^C)) (2.66e-07, rho=1.00e-02 k*=100)
- poly {C:0.5, X:0.5}
    - 2.02e-02 -> mono {D:1}   via D (2.02e-02, rho=6.13e-02 k*=100)
    - 7.54e-03 -> poly {C:0.5, X:0.49, or(X,X):0.01}   via or(X,X) (7.54e-03, rho=1.00e+00 k*=1)
    - 2.07e-03 -> mono {C:1}   via THEM(ME) (5.60e-04, rho=1.52e-01 k*=8), THEM(THEM) (5.56e-04, rho=1.52e-01 k*=8), or(X,or(X,X)) (2.82e-04, rho=1.00e+00 k*=1), THEM(^X) (1.48e-04, rho=1.68e-01 k*=7)
    - 4.76e-04 -> mono {X:1}   via or(X,and(X,X)) (2.82e-04, rho=1.00e+00 k*=1), not(THEM(^X)) (8.79e-05, rho=1.00e+00 k*=1), not(and(X,THEM(ME))) (2.66e-05, rho=1.00e+00 k*=1), not(and(X,THEM(THEM))) (2.66e-05, rho=1.00e+00 k*=1)
    - 3.16e-04 -> mono {and(X,X):1}   via and(X,X) (3.16e-04, rho=4.20e-02 k*=100)
    - 1.95e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.95e-05, rho=2.46e-02 k*=100)
