### arm=weak, n=5, game=bos, N=100, w=0.01, x_on=True, role=True, mode=square

programs 902, classes 54, states 707, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 6.56e-03
mean payoff 1.1113, efficient 1.5000, deadweight loss 0.3887, mean bits in support 3.27

| pi | state |
|---|---|
| 0.2922 | mono {D:1} |
| 0.2922 | mono {C:1} |
| 0.1257 | poly {X:0.65, ROLE:0.34, not(ROLE):0.01} |
| 0.0966 | mono {X:1} |
| 0.0726 | mono {ROLE:1} |
| 0.0281 | poly {X:0.01, ROLE:0.66, not(ROLE):0.33} |
| 0.0159 | poly {X:0.67, ROLE:0.33} |
| 0.0133 | mono {not(ROLE):1} |
| 0.0089 | poly {C:0.5, D:0.5} |
| 0.0079 | poly {C:0.49, D:0.5, X:0.01} |
| 0.0079 | poly {C:0.5, D:0.49, X:0.01} |
| 0.0053 | mono {and(X,ROLE):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.88e-03 -> poly {C:0.5, D:0.5}   via C (3.88e-03, rho=1.56e-02 k*=50)
    - 1.81e-03 -> mono {X:1}   via X (1.81e-03, rho=7.80e-03 k*=100)
    - 1.48e-03 -> mono {ROLE:1}   via ROLE (1.48e-03, rho=7.79e-03 k*=100)
    - 2.80e-04 -> mono {not(ROLE):1}   via not(ROLE) (2.80e-04, rho=5.89e-03 k*=100)
    - 5.54e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (5.54e-05, rho=8.85e-03 k*=100)
    - 4.90e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (4.90e-05, rho=7.82e-03 k*=100)
- mono {C:1}
    - 3.88e-03 -> poly {C:0.5, D:0.5}   via D (3.88e-03, rho=1.56e-02 k*=50)
    - 1.81e-03 -> mono {X:1}   via X (1.81e-03, rho=7.80e-03 k*=100)
    - 1.48e-03 -> mono {ROLE:1}   via ROLE (1.48e-03, rho=7.79e-03 k*=100)
    - 2.80e-04 -> mono {not(ROLE):1}   via not(ROLE) (2.80e-04, rho=5.89e-03 k*=100)
    - 5.54e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (5.54e-05, rho=8.85e-03 k*=100)
    - 4.90e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (4.90e-05, rho=7.82e-03 k*=100)
- poly {X:0.65, ROLE:0.34, not(ROLE):0.01}
    - 2.76e-03 -> mono {D:1}   via D (2.76e-03, rho=1.11e-02 k*=100)
    - 2.76e-03 -> mono {C:1}   via C (2.76e-03, rho=1.11e-02 k*=100)
    - 7.57e-05 -> poly {ROLE:0.57, not(ROLE):0.14, THEM(THEM):0.29}   via THEM(THEM) (7.57e-05, rho=3.47e-02 k*=29)
    - 7.57e-05 -> poly {ROLE:0.57, not(ROLE):0.14, THEM(ME):0.29}   via THEM(ME) (7.57e-05, rho=3.47e-02 k*=29)
    - 6.43e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.43e-05, rho=1.03e-02 k*=100)
    - 6.43e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.43e-05, rho=1.03e-02 k*=100)
- mono {X:1}
    - 5.93e-03 -> poly {X:0.67, ROLE:0.33}   via ROLE (5.93e-03, rho=3.11e-02 k*=33)
    - 2.79e-03 -> mono {D:1}   via D (2.79e-03, rho=1.12e-02 k*=100)
    - 2.79e-03 -> mono {C:1}   via C (2.79e-03, rho=1.12e-02 k*=100)
    - 3.65e-04 -> mono {not(ROLE):1}   via not(ROLE) (3.65e-04, rho=7.69e-03 k*=100)
    - 6.65e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.65e-05, rho=1.06e-02 k*=100)
    - 6.65e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.65e-05, rho=1.06e-02 k*=100)
- mono {ROLE:1}
    - 3.84e-03 -> poly {X:0.67, ROLE:0.33}   via X (3.84e-03, rho=1.66e-02 k*=67)
    - 3.14e-03 -> mono {D:1}   via D (3.14e-03, rho=1.26e-02 k*=100)
    - 3.14e-03 -> mono {C:1}   via C (3.14e-03, rho=1.26e-02 k*=100)
    - 1.60e-03 -> poly {ROLE:0.67, not(ROLE):0.33}   via not(ROLE) (1.60e-03, rho=3.37e-02 k*=33)
    - 7.34e-05 -> poly {ROLE:0.67, THEM(THEM):0.33}   via THEM(THEM) (7.34e-05, rho=3.37e-02 k*=33)
    - 7.34e-05 -> poly {ROLE:0.67, THEM(ME):0.33}   via THEM(ME) (7.34e-05, rho=3.37e-02 k*=33)
- poly {X:0.01, ROLE:0.66, not(ROLE):0.33}
    - 2.76e-03 -> mono {D:1}   via D (2.76e-03, rho=1.11e-02 k*=100)
    - 2.76e-03 -> mono {C:1}   via C (2.76e-03, rho=1.11e-02 k*=100)
    - 7.99e-05 -> poly {ROLE:0.57, not(ROLE):0.14, THEM(THEM):0.29}   via THEM(THEM) (7.99e-05, rho=3.66e-02 k*=29)
    - 7.99e-05 -> poly {ROLE:0.57, not(ROLE):0.14, THEM(ME):0.29}   via THEM(ME) (7.99e-05, rho=3.66e-02 k*=29)
    - 6.43e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.43e-05, rho=1.03e-02 k*=100)
    - 6.43e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.43e-05, rho=1.03e-02 k*=100)
- poly {X:0.67, ROLE:0.33}
    - 4.75e-02 -> poly {X:0.65, ROLE:0.34, not(ROLE):0.01}   via not(ROLE) (4.75e-02, rho=1.00e+00 k*=1)
    - 2.76e-03 -> mono {D:1}   via D (2.76e-03, rho=1.11e-02 k*=100)
    - 2.76e-03 -> mono {C:1}   via C (2.76e-03, rho=1.11e-02 k*=100)
    - 6.63e-05 -> poly {ROLE:0.67, THEM(THEM):0.33}   via THEM(THEM) (6.63e-05, rho=3.04e-02 k*=33)
    - 6.63e-05 -> poly {ROLE:0.67, THEM(ME):0.33}   via THEM(ME) (6.63e-05, rho=3.04e-02 k*=33)
    - 6.43e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.43e-05, rho=1.03e-02 k*=100)
- mono {not(ROLE):1}
    - 4.31e-03 -> poly {ROLE:0.67, not(ROLE):0.33}   via ROLE (4.31e-03, rho=2.26e-02 k*=67)
    - 3.90e-03 -> mono {D:1}   via D (3.90e-03, rho=1.57e-02 k*=100)
    - 3.90e-03 -> mono {C:1}   via C (3.90e-03, rho=1.57e-02 k*=100)
    - 3.29e-03 -> mono {X:1}   via X (3.29e-03, rho=1.42e-02 k*=100)
    - 9.96e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (9.96e-05, rho=1.59e-02 k*=100)
    - 9.96e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (9.96e-05, rho=1.59e-02 k*=100)
- poly {C:0.5, D:0.5}
    - 1.16e-01 -> poly {C:0.5, D:0.49, X:0.01}   via X (1.16e-01, rho=1.00e+00 k*=1)
    - 1.16e-01 -> poly {C:0.49, D:0.5, X:0.01}   via X (1.16e-01, rho=1.00e+00 k*=1)
    - 8.12e-03 -> mono {D:1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1), and(X,ROLE) (2.09e-03, rho=3.34e-01 k*=3), not(or(X,ROLE)) (1.76e-03, rho=1.00e+00 k*=1), and(X,and(X,ROLE)) (1.09e-04, rho=5.00e-01 k*=2)
    - 8.12e-03 -> mono {C:1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1), or(X,ROLE) (2.09e-03, rho=3.34e-01 k*=3), not(and(X,ROLE)) (1.76e-03, rho=1.00e+00 k*=1), or(X,or(X,ROLE)) (1.09e-04, rho=5.00e-01 k*=2)
    - 1.98e-03 -> poly {C:0.34, D:0.33, ROLE:0.33}   via ROLE (1.98e-03, rho=3.11e-02 k*=33)
    - 1.98e-03 -> poly {C:0.33, D:0.34, ROLE:0.33}   via ROLE (1.98e-03, rho=3.11e-02 k*=33)
- poly {C:0.49, D:0.5, X:0.01}
    - 1.31e-01 -> mono {D:1}   via ROLE (6.36e-02, rho=3.34e-01 k*=3), not(ROLE) (4.75e-02, rho=1.00e+00 k*=1), and(X,X) (3.86e-03, rho=1.00e+00 k*=1), or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 7.23e-06 -> mono {C:1}   via or(THEM(ME),ROLE) (2.50e-06, rho=6.87e-02 k*=15), or(THEM(THEM),ROLE) (2.50e-06, rho=6.87e-02 k*=15), or(ROLE,THEM(ME)) (9.56e-07, rho=3.69e-02 k*=29), or(ROLE,THEM(THEM)) (9.56e-07, rho=3.69e-02 k*=29)
    - 5.11e-06 -> mono {THEM(^D):1}   via THEM(^D) (5.11e-06, rho=2.31e-02 k*=50)
    - 5.11e-06 -> mono {THEM(^C):1}   via THEM(^C) (5.11e-06, rho=2.31e-02 k*=50)
    - 4.15e-07 -> mono {or(X,THEM(THEM)):1}   via or(X,THEM(THEM)) (4.15e-07, rho=1.58e-02 k*=72)
    - 4.15e-07 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (4.15e-07, rho=1.58e-02 k*=72)
- poly {C:0.5, D:0.49, X:0.01}
    - 1.31e-01 -> mono {C:1}   via ROLE (6.36e-02, rho=3.34e-01 k*=3), not(ROLE) (4.75e-02, rho=1.00e+00 k*=1), and(X,X) (3.86e-03, rho=1.00e+00 k*=1), or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 7.23e-06 -> mono {D:1}   via and(THEM(ME),ROLE) (2.50e-06, rho=6.87e-02 k*=15), and(THEM(THEM),ROLE) (2.50e-06, rho=6.87e-02 k*=15), and(ROLE,THEM(ME)) (9.56e-07, rho=3.69e-02 k*=29), and(ROLE,THEM(THEM)) (9.56e-07, rho=3.69e-02 k*=29)
    - 5.11e-06 -> mono {THEM(^D):1}   via THEM(^D) (5.11e-06, rho=2.31e-02 k*=50)
    - 5.11e-06 -> mono {THEM(^C):1}   via THEM(^C) (5.11e-06, rho=2.31e-02 k*=50)
    - 4.15e-07 -> mono {and(X,THEM(THEM)):1}   via and(X,THEM(THEM)) (4.15e-07, rho=1.58e-02 k*=72)
    - 4.15e-07 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (4.15e-07, rho=1.58e-02 k*=72)
- mono {and(X,ROLE):1}
    - 2.80e-03 -> mono {D:1}   via D (2.80e-03, rho=1.12e-02 k*=100)
    - 2.48e-03 -> mono {C:1}   via C (2.48e-03, rho=9.95e-03 k*=100)
    - 2.17e-03 -> mono {X:1}   via X (2.17e-03, rho=9.39e-03 k*=100)
    - 1.68e-03 -> mono {ROLE:1}   via ROLE (1.68e-03, rho=8.84e-03 k*=100)
    - 3.62e-04 -> mono {not(ROLE):1}   via not(ROLE) (3.62e-04, rho=7.61e-03 k*=100)
    - 2.73e-04 -> poly {and(X,ROLE):0.92, THEM(THEM):0.08}   via THEM(THEM) (2.73e-04, rho=1.25e-01 k*=8)
