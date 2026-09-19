### arm=weak, n=5, game=chicken_norole, N=100, w=0.1, x_on=True, role=False, mode=square

programs 450, classes 30, states 935, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 1.39e-04
mean payoff -0.2531, efficient 0.5000, deadweight loss 0.7531, mean bits in support 9.36

| pi | state |
|---|---|
| 0.4164 | poly {D:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.64, not(THEM(^D)):0.15, or(THEM(ME),C):0.01} |
| 0.3360 | poly {D:0.18, not(THEM(ME)):0.01, not(THEM(THEM)):0.8, or(THEM(ME),C):0.01} |
| 0.0823 | poly {D:0.18, not(THEM(ME)):0.8, not(THEM(THEM)):0.01, or(THEM(ME),C):0.01} |
| 0.0271 | poly {D:0.19, not(THEM(ME)):0.64, not(THEM(THEM)):0.01, not(THEM(^D)):0.15, or(THEM(ME),C):0.01} |
| 0.0200 | poly {D:0.18, not(THEM(ME)):0.01, not(THEM(THEM)):0.81} |
| 0.0130 | poly {C:0.26, D:0.22, not(THEM(^X)):0.48, or(THEM(ME),C):0.04} |
| 0.0109 | poly {D:0.18, not(THEM(ME)):0.81, not(THEM(THEM)):0.01} |
| 0.0059 | poly {C:0.8, D:0.17, X:0.01, and(X,X):0.01, or(X,X):0.01} |
| 0.0049 | poly {D:0.18, not(THEM(THEM)):0.82} |
| 0.0033 | poly {D:0.18, not(THEM(THEM)):0.81, or(THEM(ME),C):0.01} |
| 0.0031 | poly {D:0.18, not(THEM(ME)):0.82} |
| 0.0030 | mono {and(THEM(THEM),D):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {D:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.64, not(THEM(^D)):0.15, or(THEM(ME),C):0.01}
    - 4.74e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (4.74e-06, rho=1.75e-03 k*=74)
    - 1.77e-06 -> mono {not(THEM(THEM)):1}   via THEM(THEM) (1.66e-06, rho=1.75e-03 k*=74), and(THEM(ME),D) (3.42e-08, rho=1.75e-03 k*=74), and(THEM(THEM),D) (3.42e-08, rho=1.75e-03 k*=74), and(THEM(THEM),X) (3.42e-08, rho=1.75e-03 k*=74)
    - 1.77e-06 -> mono {THEM(ME):1}   via THEM(ME) (1.77e-06, rho=4.81e-04 k*=100)
    - 1.36e-07 -> mono {C:1}   via C (1.36e-07, rho=4.14e-07 k*=100)
    - 1.05e-07 -> mono {or(THEM(ME),X):1}   via or(THEM(ME),X) (1.05e-07, rho=1.38e-03 k*=100)
    - 9.81e-08 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (9.81e-08, rho=1.75e-03 k*=74)
- poly {D:0.18, not(THEM(ME)):0.01, not(THEM(THEM)):0.8, or(THEM(ME),C):0.01}
    - 1.01e-05 -> poly {D:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.64, not(THEM(^D)):0.15, or(THEM(ME),C):0.01}   via not(THEM(^D)) (1.01e-05, rho=1.33e-01 k*=15)
    - 2.72e-06 -> mono {not(THEM(THEM)):1}   via THEM(ME) (1.14e-06, rho=6.37e-04 k*=50), THEM(THEM) (1.14e-06, rho=6.37e-04 k*=50), or(THEM(ME),X) (1.71e-07, rho=4.30e-03 k*=47), or(THEM(THEM),X) (1.71e-07, rho=4.30e-03 k*=47)
    - 1.17e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (1.17e-06, rho=6.37e-04 k*=50)
    - 1.17e-06 -> mono {THEM(ME):1}   via THEM(ME) (1.17e-06, rho=6.37e-04 k*=50)
    - 1.53e-07 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (1.53e-07, rho=4.30e-03 k*=47)
    - 1.53e-07 -> mono {or(THEM(ME),X):1}   via or(THEM(ME),X) (1.53e-07, rho=4.30e-03 k*=47)
- poly {D:0.18, not(THEM(ME)):0.8, not(THEM(THEM)):0.01, or(THEM(ME),C):0.01}
    - 2.71e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.71e-05, rho=3.59e-02 k*=99)
    - 1.01e-05 -> poly {D:0.19, not(THEM(ME)):0.64, not(THEM(THEM)):0.01, not(THEM(^D)):0.15, or(THEM(ME),C):0.01}   via not(THEM(^D)) (1.01e-05, rho=1.33e-01 k*=15)
    - 2.72e-06 -> mono {not(THEM(ME)):1}   via THEM(ME) (1.14e-06, rho=6.37e-04 k*=50), THEM(THEM) (1.14e-06, rho=6.37e-04 k*=50), or(THEM(ME),X) (1.71e-07, rho=4.30e-03 k*=47), or(THEM(THEM),X) (1.71e-07, rho=4.30e-03 k*=47)
    - 1.17e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (1.17e-06, rho=6.37e-04 k*=50)
    - 1.17e-06 -> mono {THEM(ME):1}   via THEM(ME) (1.17e-06, rho=6.37e-04 k*=50)
    - 3.26e-07 -> mono {or(THEM(ME),C):1}   via THEM(^C) (2.92e-07, rho=3.59e-02 k*=99), THEM(ME) (1.43e-08, rho=6.37e-04 k*=50), THEM(THEM) (1.43e-08, rho=6.37e-04 k*=50), or(THEM(ME),X) (2.13e-09, rho=4.30e-03 k*=47)
- poly {D:0.19, not(THEM(ME)):0.64, not(THEM(THEM)):0.01, not(THEM(^D)):0.15, or(THEM(ME),C):0.01}
    - 2.92e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.92e-05, rho=3.86e-02 k*=99)
    - 4.74e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (4.74e-06, rho=1.75e-03 k*=74)
    - 1.77e-06 -> mono {not(THEM(ME)):1}   via THEM(THEM) (1.66e-06, rho=1.75e-03 k*=74), and(THEM(ME),D) (3.42e-08, rho=1.75e-03 k*=74), and(THEM(THEM),D) (3.42e-08, rho=1.75e-03 k*=74), and(THEM(THEM),X) (3.42e-08, rho=1.75e-03 k*=74)
    - 1.77e-06 -> mono {THEM(ME):1}   via THEM(ME) (1.77e-06, rho=4.81e-04 k*=100)
    - 3.17e-07 -> mono {or(THEM(ME),C):1}   via THEM(^C) (2.90e-07, rho=3.86e-02 k*=99), THEM(THEM) (2.59e-08, rho=1.75e-03 k*=74), and(THEM(ME),D) (5.35e-10, rho=1.75e-03 k*=74), and(THEM(THEM),D) (5.35e-10, rho=1.75e-03 k*=74)
    - 1.36e-07 -> mono {C:1}   via C (1.36e-07, rho=4.14e-07 k*=100)
- poly {D:0.18, not(THEM(ME)):0.01, not(THEM(THEM)):0.81}
    - 1.52e-04 -> poly {D:0.18, not(THEM(ME)):0.01, not(THEM(THEM)):0.8, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.01e-05 -> poly {D:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.65, not(THEM(^D)):0.15}   via not(THEM(^D)) (1.01e-05, rho=1.33e-01 k*=15)
    - 2.76e-06 -> mono {not(THEM(THEM)):1}   via THEM(ME) (1.16e-06, rho=6.37e-04 k*=50), THEM(THEM) (1.16e-06, rho=6.37e-04 k*=50), or(THEM(ME),X) (1.73e-07, rho=4.30e-03 k*=47), or(THEM(THEM),X) (1.73e-07, rho=4.30e-03 k*=47)
    - 1.17e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (1.17e-06, rho=6.37e-04 k*=50)
    - 1.17e-06 -> mono {THEM(ME):1}   via THEM(ME) (1.17e-06, rho=6.37e-04 k*=50)
    - 1.53e-07 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (1.53e-07, rho=4.30e-03 k*=47)
- poly {C:0.26, D:0.22, not(THEM(^X)):0.48, or(THEM(ME),C):0.04}
    - 1.38e-03 -> poly {C:0.25, D:0.23, not(THEM(^X)):0.48, or(THEM(ME),C):0.04}   via not(THEM(ME)) (6.89e-04, rho=1.00e+00 k*=1), not(THEM(THEM)) (6.89e-04, rho=1.00e+00 k*=1)
    - 4.98e-06 -> poly {D:0.2, not(THEM(^C)):0.51, not(THEM(^X)):0.29}   via not(THEM(^C)) (4.98e-06, rho=6.55e-02 k*=51)
    - 3.17e-06 -> mono {and(THEM(THEM),D):1}   via and(THEM(THEM),D) (3.17e-06, rho=4.30e-02 k*=97)
    - 3.17e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (3.17e-06, rho=4.30e-02 k*=97)
    - 2.72e-06 -> mono {X:1}   via X (2.72e-06, rho=8.62e-06 k*=100)
    - 1.57e-06 -> mono {or(X,X):1}   via or(X,X) (1.57e-06, rho=2.33e-04 k*=100)
- poly {D:0.18, not(THEM(ME)):0.81, not(THEM(THEM)):0.01}
    - 1.52e-04 -> poly {D:0.18, not(THEM(ME)):0.8, not(THEM(THEM)):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 2.83e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.83e-05, rho=3.70e-02 k*=100)
    - 1.01e-05 -> poly {D:0.19, not(THEM(ME)):0.65, not(THEM(THEM)):0.01, not(THEM(^D)):0.15}   via not(THEM(^D)) (1.01e-05, rho=1.33e-01 k*=15)
    - 2.76e-06 -> mono {not(THEM(ME)):1}   via THEM(ME) (1.16e-06, rho=6.37e-04 k*=50), THEM(THEM) (1.16e-06, rho=6.37e-04 k*=50), or(THEM(ME),X) (1.73e-07, rho=4.30e-03 k*=47), or(THEM(THEM),X) (1.73e-07, rho=4.30e-03 k*=47)
    - 1.17e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (1.17e-06, rho=6.37e-04 k*=50)
    - 1.17e-06 -> mono {THEM(ME):1}   via THEM(ME) (1.17e-06, rho=6.37e-04 k*=50)
- poly {C:0.8, D:0.17, X:0.01, and(X,X):0.01, or(X,X):0.01}
    - 1.52e-04 -> poly {C:0.79, D:0.17, X:0.01, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.79, D:0.17, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.8, D:0.16, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.8, D:0.16, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.8, D:0.16, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 9.14e-05 -> poly {D:0.18, not(THEM(THEM)):0.82}   via not(THEM(THEM)) (9.14e-05, rho=1.33e-01 k*=82)
- poly {D:0.18, not(THEM(THEM)):0.82}
    - 6.89e-04 -> poly {D:0.18, not(THEM(ME)):0.01, not(THEM(THEM)):0.81}   via not(THEM(ME)) (6.89e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {D:0.18, not(THEM(THEM)):0.81, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.01e-05 -> poly {D:0.19, not(THEM(THEM)):0.66, not(THEM(^D)):0.15}   via not(THEM(^D)) (1.01e-05, rho=1.33e-01 k*=15)
    - 2.79e-06 -> mono {not(THEM(THEM)):1}   via THEM(ME) (1.17e-06, rho=6.37e-04 k*=50), THEM(THEM) (1.17e-06, rho=6.37e-04 k*=50), or(THEM(ME),X) (1.75e-07, rho=4.30e-03 k*=47), or(THEM(THEM),X) (1.75e-07, rho=4.30e-03 k*=47)
    - 1.17e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (1.17e-06, rho=6.37e-04 k*=50)
    - 1.17e-06 -> mono {THEM(ME):1}   via THEM(ME) (1.17e-06, rho=6.37e-04 k*=50)
- poly {D:0.18, not(THEM(THEM)):0.81, or(THEM(ME),C):0.01}
    - 6.89e-04 -> poly {D:0.18, not(THEM(ME)):0.01, not(THEM(THEM)):0.8, or(THEM(ME),C):0.01}   via not(THEM(ME)) (6.89e-04, rho=1.00e+00 k*=1)
    - 1.01e-05 -> poly {D:0.19, not(THEM(THEM)):0.65, not(THEM(^D)):0.15, or(THEM(ME),C):0.01}   via not(THEM(^D)) (1.01e-05, rho=1.33e-01 k*=15)
    - 2.76e-06 -> mono {not(THEM(THEM)):1}   via THEM(ME) (1.16e-06, rho=6.37e-04 k*=50), THEM(THEM) (1.16e-06, rho=6.37e-04 k*=50), or(THEM(ME),X) (1.73e-07, rho=4.30e-03 k*=47), or(THEM(THEM),X) (1.73e-07, rho=4.30e-03 k*=47)
    - 1.17e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (1.17e-06, rho=6.37e-04 k*=50)
    - 1.17e-06 -> mono {THEM(ME):1}   via THEM(ME) (1.17e-06, rho=6.37e-04 k*=50)
    - 1.53e-07 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (1.53e-07, rho=4.30e-03 k*=47)
- poly {D:0.18, not(THEM(ME)):0.82}
    - 6.89e-04 -> poly {D:0.18, not(THEM(ME)):0.81, not(THEM(THEM)):0.01}   via not(THEM(THEM)) (6.89e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {D:0.18, not(THEM(ME)):0.81, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.27e-05 -> mono {THEM(^C):1}   via THEM(^C) (3.27e-05, rho=4.27e-02 k*=100)
    - 1.01e-05 -> poly {D:0.19, not(THEM(ME)):0.66, not(THEM(^D)):0.15}   via not(THEM(^D)) (1.01e-05, rho=1.33e-01 k*=15)
    - 2.79e-06 -> mono {not(THEM(ME)):1}   via THEM(ME) (1.17e-06, rho=6.37e-04 k*=50), THEM(THEM) (1.17e-06, rho=6.37e-04 k*=50), or(THEM(ME),X) (1.75e-07, rho=4.30e-03 k*=47), or(THEM(THEM),X) (1.75e-07, rho=4.30e-03 k*=47)
    - 1.17e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (1.17e-06, rho=6.37e-04 k*=50)
- mono {and(THEM(THEM),D):1}
    - 3.68e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.68e-05, rho=1.00e-02 k*=100)
    - 3.68e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-05, rho=1.00e-02 k*=100)
    - 6.89e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (6.89e-06, rho=1.00e-02 k*=100)
    - 6.89e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (6.89e-06, rho=1.00e-02 k*=100)
    - 1.52e-06 -> mono {or(THEM(ME),C):1}   via or(THEM(ME),C) (1.52e-06, rho=1.00e-02 k*=100)
    - 7.61e-07 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (7.61e-07, rho=1.00e-02 k*=100)
