### arm=weak, n=5, game=chicken_norole, N=10, w=1.0, x_on=True, role=False, mode=square

programs 450, classes 30, states 448, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 6.89e-04
mean payoff -0.2697, efficient 0.5000, deadweight loss 0.7697, mean bits in support 9.90

| pi | state |
|---|---|
| 0.5608 | poly {D:0.2, not(THEM(ME)):0.5, not(THEM(THEM)):0.1, not(THEM(^D)):0.1, or(THEM(ME),C):0.1} |
| 0.4244 | poly {D:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.5, not(THEM(^D)):0.1, or(THEM(ME),C):0.1} |
| 0.0020 | poly {D:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.7} |
| 0.0018 | poly {D:0.2, not(THEM(ME)):0.7, not(THEM(THEM)):0.1} |
| 0.0018 | poly {D:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.6, or(THEM(ME),C):0.1} |
| 0.0011 | poly {D:0.2, not(THEM(ME)):0.6, not(THEM(THEM)):0.1, or(THEM(ME),C):0.1} |
| 0.0011 | poly {D:0.2, not(THEM(ME)):0.6, not(THEM(THEM)):0.1, not(THEM(^D)):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {D:0.2, not(THEM(ME)):0.5, not(THEM(THEM)):0.1, not(THEM(^D)):0.1, or(THEM(ME),C):0.1}
    - 4.57e-07 -> mono {C:1}   via C (4.57e-07, rho=1.39e-06 k*=10)
    - 2.49e-09 -> mono {not(THEM(^C)):1}   via not(THEM(^C)) (2.49e-09, rho=3.27e-05 k*=10)
    - 3.81e-10 -> mono {THEM(^C):1}   via THEM(^C) (3.81e-10, rho=5.56e-07 k*=9)
    - 4.42e-11 -> mono {or(THEM(ME),C):1}   via THEM(^C) (4.42e-11, rho=5.56e-07 k*=9), THEM(THEM) (2.33e-21, rho=1.63e-17 k*=7), and(THEM(ME),D) (4.82e-23, rho=1.63e-17 k*=7), and(THEM(THEM),D) (4.82e-23, rho=1.63e-17 k*=7)
    - 1.97e-14 -> mono {and(X,X):1}   via and(X,X) (1.97e-14, rho=2.93e-12 k*=10)
    - 7.26e-15 -> mono {THEM(^X):1}   via THEM(^X) (7.26e-15, rho=9.49e-12 k*=10)
- poly {D:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.5, not(THEM(^D)):0.1, or(THEM(ME),C):0.1}
    - 7.65e-04 -> poly {D:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.4, not(THEM(^D)):0.2, or(THEM(ME),C):0.1}   via THEM(^C) (7.65e-04, rho=1.00e+00 k*=1)
    - 4.57e-07 -> mono {C:1}   via C (4.57e-07, rho=1.39e-06 k*=10)
    - 2.49e-09 -> mono {not(THEM(^C)):1}   via not(THEM(^C)) (2.49e-09, rho=3.27e-05 k*=10)
    - 1.97e-14 -> mono {and(X,X):1}   via and(X,X) (1.97e-14, rho=2.93e-12 k*=10)
    - 7.26e-15 -> mono {THEM(^X):1}   via THEM(^X) (7.26e-15, rho=9.49e-12 k*=10)
    - 4.19e-16 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (4.19e-16, rho=2.75e-12 k*=10)
- poly {D:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.7}
    - 1.52e-04 -> poly {D:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.6, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 8.50e-05 -> mono {THEM(^C):1}   via THEM(^C) (8.50e-05, rho=1.11e-01 k*=10)
    - 7.61e-05 -> poly {D:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.6, not(THEM(^D)):0.1}   via not(THEM(^D)) (7.61e-05, rho=1.00e+00 k*=1)
    - 2.33e-10 -> mono {THEM(^X):1}   via THEM(^X) (2.33e-10, rho=3.05e-07 k*=10)
    - 2.57e-11 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (2.57e-11, rho=3.37e-07 k*=10)
    - 6.99e-13 -> mono {C:1}   via C (6.99e-13, rho=2.12e-12 k*=10)
- poly {D:0.2, not(THEM(ME)):0.7, not(THEM(THEM)):0.1}
    - 1.52e-04 -> poly {D:0.2, not(THEM(ME)):0.6, not(THEM(THEM)):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 7.61e-05 -> poly {D:0.2, not(THEM(ME)):0.6, not(THEM(THEM)):0.1, not(THEM(^D)):0.1}   via not(THEM(^D)) (7.61e-05, rho=1.00e+00 k*=1)
    - 5.09e-10 -> mono {THEM(^C):1}   via THEM(^C) (5.09e-10, rho=6.66e-07 k*=10)
    - 2.33e-10 -> mono {THEM(^X):1}   via THEM(^X) (2.33e-10, rho=3.05e-07 k*=10)
    - 2.29e-11 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (2.29e-11, rho=3.01e-07 k*=10)
    - 6.99e-13 -> mono {C:1}   via C (6.99e-13, rho=2.12e-12 k*=10)
- poly {D:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.6, or(THEM(ME),C):0.1}
    - 7.70e-05 -> mono {THEM(^C):1}   via THEM(^C) (7.70e-05, rho=1.25e-01 k*=8)
    - 7.61e-05 -> poly {D:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.5, not(THEM(^D)):0.1, or(THEM(ME),C):0.1}   via not(THEM(^D)) (7.61e-05, rho=1.00e+00 k*=1)
    - 1.86e-05 -> mono {or(THEM(ME),C):1}   via THEM(^C) (1.86e-05, rho=1.25e-01 k*=8), or(THEM(ME),X) (2.02e-14, rho=3.97e-09 k*=5), or(THEM(THEM),X) (2.02e-14, rho=3.97e-09 k*=5), THEM(ME) (3.18e-21, rho=1.39e-17 k*=5)
    - 4.19e-07 -> mono {C:1}   via C (4.19e-07, rho=1.27e-06 k*=10)
    - 2.28e-09 -> mono {not(THEM(^C)):1}   via not(THEM(^C)) (2.28e-09, rho=3.00e-05 k*=10)
    - 2.43e-13 -> mono {not(THEM(THEM)):1}   via or(THEM(ME),X) (1.21e-13, rho=3.97e-09 k*=5), or(THEM(THEM),X) (1.21e-13, rho=3.97e-09 k*=5), THEM(ME) (1.91e-20, rho=1.39e-17 k*=5), THEM(THEM) (1.91e-20, rho=1.39e-17 k*=5)
- poly {D:0.2, not(THEM(ME)):0.6, not(THEM(THEM)):0.1, or(THEM(ME),C):0.1}
    - 7.65e-04 -> poly {D:0.2, not(THEM(ME)):0.7, or(THEM(ME),C):0.1}   via THEM(^C) (7.65e-04, rho=1.00e+00 k*=1)
    - 7.61e-05 -> poly {D:0.2, not(THEM(ME)):0.5, not(THEM(THEM)):0.1, not(THEM(^D)):0.1, or(THEM(ME),C):0.1}   via not(THEM(^D)) (7.61e-05, rho=1.00e+00 k*=1)
    - 4.19e-07 -> mono {C:1}   via C (4.19e-07, rho=1.27e-06 k*=10)
    - 2.28e-09 -> mono {not(THEM(^C)):1}   via not(THEM(^C)) (2.28e-09, rho=3.00e-05 k*=10)
    - 2.43e-13 -> mono {not(THEM(ME)):1}   via or(THEM(ME),X) (1.21e-13, rho=3.97e-09 k*=5), or(THEM(THEM),X) (1.21e-13, rho=3.97e-09 k*=5), THEM(ME) (1.91e-20, rho=1.39e-17 k*=5), THEM(THEM) (1.91e-20, rho=1.39e-17 k*=5)
    - 1.41e-13 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (1.41e-13, rho=3.97e-09 k*=5)
- poly {D:0.2, not(THEM(ME)):0.6, not(THEM(THEM)):0.1, not(THEM(^D)):0.1}
    - 1.52e-04 -> poly {D:0.2, not(THEM(ME)):0.5, not(THEM(THEM)):0.1, not(THEM(^D)):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 5.48e-10 -> mono {THEM(^C):1}   via THEM(^C) (5.48e-10, rho=7.17e-07 k*=10)
    - 2.38e-10 -> mono {THEM(^X):1}   via THEM(^X) (2.38e-10, rho=3.11e-07 k*=10)
    - 2.33e-11 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (2.33e-11, rho=3.05e-07 k*=10)
    - 7.60e-13 -> mono {C:1}   via C (7.60e-13, rho=2.31e-12 k*=10)
    - 3.94e-13 -> mono {X:1}   via X (3.94e-13, rho=1.25e-12 k*=10)
