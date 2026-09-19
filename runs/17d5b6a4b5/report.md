### arm=weak, n=6, game=stag, N=1000, w=0.1, x_on=True, role=False, mode=square

programs 1852, classes 46, states 108, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 2.14e-07
mean payoff 3.9853, efficient 4.0000, deadweight loss 0.0147, mean bits in support 2.64

| pi | state |
|---|---|
| 0.9798 | mono {C:1} |
| 0.0146 | mono {D:1} |
| 0.0030 | mono {THEM(^C):1} |
| 0.0020 | mono {not(THEM(^C)):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 9.10e-07 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-07, rho=1.00e-03 k*=1000)
    - 2.18e-07 -> poly {C:0.5, X:0.5}   via X (2.18e-07, rho=6.98e-07 k*=500)
    - 2.04e-07 -> mono {D:1}   via D (2.04e-07, rho=6.20e-07 k*=1000)
    - 8.80e-08 -> mono {or(X,THEM(THEM)):1}   via or(X,THEM(THEM)) (8.80e-08, rho=1.00e-03 k*=1000)
    - 8.80e-08 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (8.80e-08, rho=1.00e-03 k*=1000)
    - 2.66e-08 -> mono {or(X,THEM(^C)):1}   via or(X,THEM(^C)) (2.66e-08, rho=1.00e-03 k*=1000)
- mono {D:1}
    - 6.31e-06 -> mono {THEM(^C):1}   via THEM(^C) (6.31e-06, rho=6.94e-03 k*=1000)
    - 3.69e-06 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-06, rho=1.00e-03 k*=1000)
    - 3.67e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-06, rho=1.00e-03 k*=1000)
    - 9.10e-07 -> mono {THEM(^D):1}   via THEM(^D) (9.10e-07, rho=1.00e-03 k*=1000)
    - 2.29e-07 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (2.29e-07, rho=1.00e-03 k*=1000)
    - 8.80e-08 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (8.80e-08, rho=1.00e-03 k*=1000)
- mono {THEM(^C):1}
    - 3.29e-04 -> mono {C:1}   via C (3.29e-04, rho=1.00e-03 k*=1000)
    - 8.80e-08 -> mono {or(X,THEM(THEM)):1}   via or(X,THEM(THEM)) (8.80e-08, rho=1.00e-03 k*=1000)
    - 8.80e-08 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (8.80e-08, rho=1.00e-03 k*=1000)
    - 2.66e-08 -> mono {or(X,THEM(^C)):1}   via or(X,THEM(^C)) (2.66e-08, rho=1.00e-03 k*=1000)
    - 2.86e-09 -> mono {or(X,THEM(^X)):1}   via or(X,THEM(^X)) (2.86e-09, rho=1.08e-04 k*=1000)
    - 6.16e-10 -> poly {THEM(^C):0.5, THEM(^X):0.5}   via THEM(^X) (6.16e-10, rho=6.98e-07 k*=500)
- mono {not(THEM(^C)):1}
    - 2.04e-07 -> mono {D:1}   via D (2.04e-07, rho=6.20e-07 k*=1000)
    - 4.93e-10 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (4.93e-10, rho=6.20e-07 k*=1000)
    - 4.93e-10 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (4.93e-10, rho=6.20e-07 k*=1000)
    - 1.42e-10 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.42e-10, rho=6.20e-07 k*=1000)
    - 6.14e-11 -> poly {not(THEM(^C)):0.5, not(THEM(^X)):0.5}   via not(THEM(^X)) (6.14e-11, rho=6.98e-07 k*=500)
    - 5.46e-11 -> mono {not(THEM(^D)):1}   via not(THEM(^D)) (5.46e-11, rho=6.20e-07 k*=1000)
