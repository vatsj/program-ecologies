### arm=strong, n=6, game=stag, N=1000, w=0.01, x_on=True, role=False, mode=square

programs 1726, classes 21, states 44, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 5.35e-06
mean payoff 3.0061, efficient 4.0000, deadweight loss 0.9939, mean bits in support 2.61

| pi | state |
|---|---|
| 0.9901 | mono {D:1} |
| 0.0064 | mono {C:1} |
| 0.0012 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.84e-06 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-06, rho=1.00e-03 k*=1000)
    - 1.22e-07 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.22e-07, rho=1.00e-03 k*=1000)
    - 1.13e-07 -> mono {X:1}   via X (1.13e-07, rho=3.59e-07 k*=1000)
    - 9.64e-08 -> mono {and(X,X):1}   via and(X,X) (9.64e-08, rho=1.21e-05 k*=1000)
    - 9.32e-08 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (9.32e-08, rho=1.00e-03 k*=1000)
    - 9.32e-08 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (9.32e-08, rho=1.00e-03 k*=1000)
- mono {C:1}
    - 2.66e-04 -> poly {C:0.5, X:0.5}   via X (2.66e-04, rho=8.48e-04 k*=500)
    - 2.63e-04 -> mono {D:1}   via D (2.63e-04, rho=7.94e-04 k*=1000)
    - 4.77e-06 -> mono {and(X,X):1}   via and(X,X) (4.77e-06, rho=5.98e-04 k*=1000)
    - 3.38e-06 -> mono {or(X,X):1}   via or(X,X) (3.38e-06, rho=4.24e-04 k*=1000)
    - 6.76e-07 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (6.76e-07, rho=7.94e-04 k*=1000)
    - 2.57e-07 -> mono {THEM(ME):1}   via THEM(ME) (2.57e-07, rho=6.70e-05 k*=1000)
- mono {THEM(ME):1}
    - 2.74e-03 -> mono {C:1}   via C (2.74e-03, rho=8.25e-03 k*=1000)
    - 3.32e-04 -> mono {D:1}   via D (3.32e-04, rho=1.00e-03 k*=1000)
    - 5.00e-05 -> mono {X:1}   via X (5.00e-05, rho=1.59e-04 k*=1000)
    - 7.98e-06 -> mono {or(X,X):1}   via or(X,X) (7.98e-06, rho=1.00e-03 k*=1000)
    - 1.27e-06 -> mono {and(X,X):1}   via and(X,X) (1.27e-06, rho=1.59e-04 k*=1000)
    - 9.91e-07 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (9.91e-07, rho=3.29e-03 k*=1000)
