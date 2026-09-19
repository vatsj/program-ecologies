### arm=weak, n=6, game=stag, N=1000, w=1.0, x_on=True, role=False, mode=square

programs 1852, classes 46, states 108, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 3.47e-15
mean payoff 4.0000, efficient 4.0000, deadweight loss 0.0000, mean bits in support 3.91

| pi | state |
|---|---|
| 0.8843 | mono {C:1} |
| 0.1127 | mono {not(THEM(^C)):1} |
| 0.0024 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 9.10e-07 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-07, rho=1.00e-03 k*=1000)
    - 8.80e-08 -> mono {or(X,THEM(THEM)):1}   via or(X,THEM(THEM)) (8.80e-08, rho=1.00e-03 k*=1000)
    - 8.80e-08 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (8.80e-08, rho=1.00e-03 k*=1000)
    - 2.66e-08 -> mono {or(X,THEM(^C)):1}   via or(X,THEM(^C)) (2.66e-08, rho=1.00e-03 k*=1000)
    - 1.12e-14 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (1.12e-14, rho=3.97e-11 k*=1000)
    - 1.01e-14 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (1.01e-14, rho=1.15e-10 k*=1000)
- mono {not(THEM(^C)):1}
    - 1.30e-15 -> mono {D:1}   via D (1.30e-15, rho=3.96e-15 k*=1000)
    - 3.15e-18 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (3.15e-18, rho=3.96e-15 k*=1000)
    - 3.15e-18 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (3.15e-18, rho=3.96e-15 k*=1000)
    - 1.07e-18 -> poly {not(THEM(^C)):0.5, not(THEM(^X)):0.5}   via not(THEM(^X)) (1.07e-18, rho=1.22e-14 k*=500)
    - 9.08e-19 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (9.08e-19, rho=3.96e-15 k*=1000)
    - 3.49e-19 -> mono {not(THEM(^D)):1}   via not(THEM(^D)) (3.49e-19, rho=3.96e-15 k*=1000)
- mono {THEM(^C):1}
    - 3.29e-04 -> mono {C:1}   via C (3.29e-04, rho=1.00e-03 k*=1000)
    - 8.80e-08 -> mono {or(X,THEM(THEM)):1}   via or(X,THEM(THEM)) (8.80e-08, rho=1.00e-03 k*=1000)
    - 8.80e-08 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (8.80e-08, rho=1.00e-03 k*=1000)
    - 2.66e-08 -> mono {or(X,THEM(^C)):1}   via or(X,THEM(^C)) (2.66e-08, rho=1.00e-03 k*=1000)
    - 1.05e-11 -> mono {or(X,THEM(^X)):1}   via or(X,THEM(^X)) (1.05e-11, rho=3.93e-07 k*=1000)
    - 3.06e-15 -> mono {or(X,THEM(^D)):1}   via or(X,THEM(^D)) (3.06e-15, rho=1.15e-10 k*=1000)
