### arm=weak, n=5, game=bos, N=100, w=0.1, x_on=True, role=True, mode=square

programs 902, classes 54, states 516, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 8.52e-04
mean payoff 1.4743, efficient 1.5000, deadweight loss 0.0257, mean bits in support 3.06

| pi | state |
|---|---|
| 0.7127 | mono {C:1} |
| 0.2536 | mono {D:1} |
| 0.0094 | mono {X:1} |
| 0.0075 | poly {X:0.65, ROLE:0.34, not(ROLE):0.01} |
| 0.0026 | mono {ROLE:1} |
| 0.0022 | poly {C:0.5, D:0.49, X:0.01} |
| 0.0016 | mono {or(X,ROLE):1} |
| 0.0016 | poly {X:0.67, ROLE:0.33} |
| 0.0013 | poly {C:0.5, D:0.5} |
| 0.0011 | mono {and(X,ROLE):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 3.35e-04 -> poly {C:0.5, D:0.5}   via D (3.35e-04, rho=1.34e-03 k*=50)
    - 1.70e-04 -> mono {X:1}   via X (1.70e-04, rho=7.35e-04 k*=100)
    - 9.64e-05 -> mono {ROLE:1}   via ROLE (9.64e-05, rho=5.06e-04 k*=100)
    - 1.75e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.75e-05, rho=2.79e-03 k*=100)
    - 7.80e-06 -> mono {or(X,X):1}   via or(X,X) (7.80e-06, rho=2.02e-03 k*=100)
    - 5.23e-06 -> mono {and(X,ROLE):1}   via and(X,ROLE) (5.23e-06, rho=8.35e-04 k*=100)
- mono {D:1}
    - 3.35e-04 -> poly {C:0.5, D:0.5}   via C (3.35e-04, rho=1.34e-03 k*=50)
    - 1.70e-04 -> mono {X:1}   via X (1.70e-04, rho=7.35e-04 k*=100)
    - 9.64e-05 -> mono {ROLE:1}   via ROLE (9.64e-05, rho=5.06e-04 k*=100)
    - 1.75e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.75e-05, rho=2.79e-03 k*=100)
    - 7.80e-06 -> mono {and(X,X):1}   via and(X,X) (7.80e-06, rho=2.02e-03 k*=100)
    - 5.23e-06 -> mono {or(X,ROLE):1}   via or(X,ROLE) (5.23e-06, rho=8.35e-04 k*=100)
- mono {X:1}
    - 7.41e-03 -> poly {X:0.67, ROLE:0.33}   via ROLE (7.41e-03, rho=3.89e-02 k*=33)
    - 5.18e-03 -> mono {D:1}   via D (5.18e-03, rho=2.08e-02 k*=100)
    - 5.18e-03 -> mono {C:1}   via C (5.18e-03, rho=2.08e-02 k*=100)
    - 1.06e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.06e-04, rho=1.69e-02 k*=100)
    - 1.06e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.06e-04, rho=1.69e-02 k*=100)
    - 4.97e-05 -> mono {or(X,X):1}   via or(X,X) (4.97e-05, rho=1.29e-02 k*=100)
- poly {X:0.65, ROLE:0.34, not(ROLE):0.01}
    - 4.89e-03 -> mono {D:1}   via D (4.89e-03, rho=1.96e-02 k*=100)
    - 4.89e-03 -> mono {C:1}   via C (4.89e-03, rho=1.96e-02 k*=100)
    - 8.02e-05 -> poly {ROLE:0.57, not(ROLE):0.14, THEM(THEM):0.29}   via THEM(THEM) (8.02e-05, rho=3.68e-02 k*=29)
    - 8.02e-05 -> poly {ROLE:0.57, not(ROLE):0.14, THEM(ME):0.29}   via THEM(ME) (8.02e-05, rho=3.68e-02 k*=29)
    - 7.91e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.91e-05, rho=1.26e-02 k*=100)
    - 7.91e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (7.91e-05, rho=1.26e-02 k*=100)
- mono {ROLE:1}
    - 1.15e-02 -> mono {D:1}   via D (1.15e-02, rho=4.63e-02 k*=100)
    - 1.15e-02 -> mono {C:1}   via C (1.15e-02, rho=4.63e-02 k*=100)
    - 8.66e-03 -> poly {X:0.67, ROLE:0.33}   via X (8.66e-03, rho=3.74e-02 k*=67)
    - 3.51e-03 -> poly {ROLE:0.67, not(ROLE):0.33}   via not(ROLE) (3.51e-03, rho=7.38e-02 k*=33)
    - 1.63e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.63e-04, rho=2.60e-02 k*=100)
    - 1.63e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.63e-04, rho=2.60e-02 k*=100)
- poly {C:0.5, D:0.49, X:0.01}
    - 1.32e-01 -> mono {C:1}   via ROLE (6.49e-02, rho=3.41e-01 k*=3), not(ROLE) (4.75e-02, rho=1.00e+00 k*=1), and(X,X) (3.86e-03, rho=1.00e+00 k*=1), or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.32e-05 -> mono {THEM(^D):1}   via THEM(^D) (1.32e-05, rho=5.95e-02 k*=50)
    - 1.32e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.32e-05, rho=5.95e-02 k*=50)
    - 1.01e-05 -> mono {D:1}   via and(THEM(ME),ROLE) (3.15e-06, rho=8.64e-02 k*=15), and(THEM(THEM),ROLE) (3.15e-06, rho=8.64e-02 k*=15), and(ROLE,THEM(ME)) (1.56e-06, rho=6.02e-02 k*=29), and(ROLE,THEM(THEM)) (1.56e-06, rho=6.02e-02 k*=29)
    - 9.50e-07 -> mono {and(X,THEM(THEM)):1}   via and(X,THEM(THEM)) (9.50e-07, rho=3.60e-02 k*=72)
    - 9.50e-07 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (9.50e-07, rho=3.60e-02 k*=72)
- mono {or(X,ROLE):1}
    - 6.14e-03 -> mono {C:1}   via C (6.14e-03, rho=2.47e-02 k*=100)
    - 1.88e-03 -> mono {D:1}   via D (1.88e-03, rho=7.57e-03 k*=100)
    - 1.22e-03 -> mono {X:1}   via X (1.22e-03, rho=5.28e-03 k*=100)
    - 4.78e-04 -> mono {ROLE:1}   via ROLE (4.78e-04, rho=2.51e-03 k*=100)
    - 2.80e-04 -> poly {or(X,ROLE):0.92, THEM(THEM):0.08}   via THEM(THEM) (2.80e-04, rho=1.29e-01 k*=8)
    - 2.80e-04 -> poly {or(X,ROLE):0.92, THEM(ME):0.08}   via THEM(ME) (2.80e-04, rho=1.29e-01 k*=8)
- poly {X:0.67, ROLE:0.33}
    - 4.75e-02 -> poly {X:0.65, ROLE:0.34, not(ROLE):0.01}   via not(ROLE) (4.75e-02, rho=1.00e+00 k*=1)
    - 4.89e-03 -> mono {D:1}   via D (4.89e-03, rho=1.96e-02 k*=100)
    - 4.89e-03 -> mono {C:1}   via C (4.89e-03, rho=1.96e-02 k*=100)
    - 7.91e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.91e-05, rho=1.26e-02 k*=100)
    - 7.91e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (7.91e-05, rho=1.26e-02 k*=100)
    - 6.80e-05 -> poly {ROLE:0.67, THEM(THEM):0.33}   via THEM(THEM) (6.80e-05, rho=3.12e-02 k*=33)
- poly {C:0.5, D:0.5}
    - 2.31e-01 -> poly {C:0.5, D:0.49, X:0.01}   via X (2.31e-01, rho=1.00e+00 k*=1)
    - 8.15e-03 -> mono {D:1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1), and(X,ROLE) (2.11e-03, rho=3.37e-01 k*=3), not(or(X,ROLE)) (1.76e-03, rho=1.00e+00 k*=1), and(X,and(X,ROLE)) (1.10e-04, rho=5.01e-01 k*=2)
    - 8.15e-03 -> mono {C:1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1), or(X,ROLE) (2.11e-03, rho=3.37e-01 k*=3), not(and(X,ROLE)) (1.76e-03, rho=1.00e+00 k*=1), or(X,or(X,ROLE)) (1.10e-04, rho=5.01e-01 k*=2)
    - 7.41e-03 -> poly {C:0.33, D:0.33, ROLE:0.34}   via ROLE (7.41e-03, rho=3.89e-02 k*=33)
    - 1.29e-04 -> poly {C:0.34, D:0.33, THEM(THEM):0.33}   via THEM(THEM) (1.29e-04, rho=5.91e-02 k*=33)
    - 1.29e-04 -> poly {C:0.34, D:0.33, THEM(ME):0.33}   via THEM(ME) (1.29e-04, rho=5.91e-02 k*=33)
- mono {and(X,ROLE):1}
    - 6.14e-03 -> mono {D:1}   via D (6.14e-03, rho=2.47e-02 k*=100)
    - 1.88e-03 -> mono {C:1}   via C (1.88e-03, rho=7.57e-03 k*=100)
    - 1.22e-03 -> mono {X:1}   via X (1.22e-03, rho=5.28e-03 k*=100)
    - 4.78e-04 -> mono {ROLE:1}   via ROLE (4.78e-04, rho=2.51e-03 k*=100)
    - 2.80e-04 -> poly {and(X,ROLE):0.92, THEM(THEM):0.08}   via THEM(THEM) (2.80e-04, rho=1.29e-01 k*=8)
    - 2.80e-04 -> poly {and(X,ROLE):0.92, THEM(ME):0.08}   via THEM(ME) (2.80e-04, rho=1.29e-01 k*=8)
