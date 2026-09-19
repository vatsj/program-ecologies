### arm=weak, n=5, game=demand, N=100, w=0.1, x_on=True, role=True, mode=square

programs 902, classes 53, states 1235, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 5.62e-03
mean payoff 0.4296, efficient 0.5000, deadweight loss 0.0704, mean bits in support 3.44

| pi | state |
|---|---|
| 0.3482 | mono {ROLE:1} |
| 0.0885 | mono {not(ROLE):1} |
| 0.0636 | mono {X:1} |
| 0.0574 | poly {C:0.34, D:0.01, X:0.63, and(X,X):0.01, or(X,X):0.01} |
| 0.0562 | poly {C:0.65, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01} |
| 0.0485 | poly {C:0.66, D:0.33, X:0.01} |
| 0.0401 | poly {C:0.34, D:0.01, X:0.65} |
| 0.0388 | mono {C:1} |
| 0.0300 | poly {C:0.34, D:0.01, X:0.64, or(X,X):0.01} |
| 0.0268 | mono {D:1} |
| 0.0264 | poly {C:0.66, D:0.32, X:0.01, and(X,X):0.01} |
| 0.0257 | poly {C:0.65, D:0.33, X:0.01, or(X,X):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 1.49e-03 -> mono {C:1}   via C (1.49e-03, rho=6.00e-03 k*=100)
    - 1.41e-03 -> mono {X:1}   via X (1.41e-03, rho=6.11e-03 k*=100)
    - 8.32e-04 -> mono {D:1}   via D (8.32e-04, rho=3.34e-03 k*=100)
    - 5.78e-04 -> poly {ROLE:0.5, not(ROLE):0.5}   via not(ROLE) (5.78e-04, rho=1.22e-02 k*=50)
    - 4.90e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (4.90e-05, rho=7.82e-03 k*=100)
    - 3.77e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (3.77e-05, rho=6.03e-03 k*=100)
- mono {not(ROLE):1}
    - 2.32e-03 -> poly {ROLE:0.5, not(ROLE):0.5}   via ROLE (2.32e-03, rho=1.22e-02 k*=50)
    - 1.49e-03 -> mono {C:1}   via C (1.49e-03, rho=6.00e-03 k*=100)
    - 1.41e-03 -> mono {X:1}   via X (1.41e-03, rho=6.11e-03 k*=100)
    - 8.32e-04 -> mono {D:1}   via D (8.32e-04, rho=3.34e-03 k*=100)
    - 3.84e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (3.84e-05, rho=6.14e-03 k*=100)
    - 2.96e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.96e-05, rho=4.73e-03 k*=100)
- mono {X:1}
    - 7.93e-03 -> poly {C:0.33, X:0.67}   via C (7.93e-03, rho=3.19e-02 k*=33)
    - 2.36e-03 -> mono {ROLE:1}   via ROLE (2.36e-03, rho=1.24e-02 k*=100)
    - 1.45e-03 -> mono {D:1}   via D (1.45e-03, rho=5.84e-03 k*=100)
    - 5.88e-04 -> mono {not(ROLE):1}   via not(ROLE) (5.88e-04, rho=1.24e-02 k*=100)
    - 7.01e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.01e-05, rho=1.12e-02 k*=100)
    - 6.06e-05 -> poly {X:0.33, or(X,X):0.67}   via or(X,X) (6.06e-05, rho=1.57e-02 k*=67)
- poly {C:0.34, D:0.01, X:0.63, and(X,X):0.01, or(X,X):0.01}
    - 2.31e-03 -> mono {ROLE:1}   via ROLE (2.31e-03, rho=1.21e-02 k*=100)
    - 5.76e-04 -> mono {not(ROLE):1}   via not(ROLE) (5.76e-04, rho=1.21e-02 k*=100)
    - 2.19e-04 -> poly {C:0.35, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01}   via and(X,and(X,ROLE)) (2.19e-04, rho=1.00e+00 k*=1)
    - 1.22e-04 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.22e-04, rho=1.95e-02 k*=50)
    - 7.29e-05 -> poly {C:0.34, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {C:0.34, D:0.01, X:0.62, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
- poly {C:0.65, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01}
    - 2.31e-03 -> mono {ROLE:1}   via ROLE (2.31e-03, rho=1.21e-02 k*=100)
    - 5.76e-04 -> mono {not(ROLE):1}   via not(ROLE) (5.76e-04, rho=1.21e-02 k*=100)
    - 1.22e-04 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.22e-04, rho=1.95e-02 k*=50)
    - 7.29e-05 -> poly {C:0.64, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {C:0.64, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {C:0.65, D:0.31, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
- poly {C:0.66, D:0.33, X:0.01}
    - 3.86e-03 -> poly {C:0.65, D:0.33, X:0.01, or(X,X):0.01}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.66, D:0.32, X:0.01, and(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.31e-03 -> mono {ROLE:1}   via ROLE (2.31e-03, rho=1.21e-02 k*=100)
    - 5.76e-04 -> mono {not(ROLE):1}   via not(ROLE) (5.76e-04, rho=1.21e-02 k*=100)
    - 1.22e-04 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.22e-04, rho=1.95e-02 k*=50)
    - 7.29e-05 -> poly {C:0.65, D:0.33, X:0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
- poly {C:0.34, D:0.01, X:0.65}
    - 8.16e-03 -> poly {C:0.35, D:0.01, X:0.64}   via and(X,ROLE) (6.26e-03, rho=1.00e+00 k*=1), not(or(X,ROLE)) (1.76e-03, rho=1.00e+00 k*=1), and(X,or(X,ROLE)) (1.46e-04, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.34, D:0.01, X:0.64, or(X,X):0.01}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.34, D:0.01, X:0.64, and(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.31e-03 -> mono {ROLE:1}   via ROLE (2.31e-03, rho=1.21e-02 k*=100)
    - 5.76e-04 -> mono {not(ROLE):1}   via not(ROLE) (5.76e-04, rho=1.21e-02 k*=100)
    - 7.29e-05 -> poly {C:0.34, D:0.01, X:0.64, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
- mono {C:1}
    - 9.26e-03 -> poly {C:0.67, D:0.33}   via D (9.26e-03, rho=3.72e-02 k*=33)
    - 4.25e-03 -> poly {C:0.33, X:0.67}   via X (4.25e-03, rho=1.84e-02 k*=67)
    - 2.94e-03 -> mono {ROLE:1}   via ROLE (2.94e-03, rho=1.55e-02 k*=100)
    - 7.34e-04 -> mono {not(ROLE):1}   via not(ROLE) (7.34e-04, rho=1.55e-02 k*=100)
    - 1.58e-04 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.58e-04, rho=2.52e-02 k*=50)
    - 1.08e-04 -> poly {C:0.56, and(X,X):0.44}   via and(X,X) (1.08e-04, rho=2.79e-02 k*=44)
- poly {C:0.34, D:0.01, X:0.64, or(X,X):0.01}
    - 3.86e-03 -> poly {C:0.34, D:0.01, X:0.63, and(X,X):0.01, or(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.31e-03 -> mono {ROLE:1}   via ROLE (2.31e-03, rho=1.21e-02 k*=100)
    - 5.76e-04 -> mono {not(ROLE):1}   via not(ROLE) (5.76e-04, rho=1.21e-02 k*=100)
    - 2.19e-04 -> poly {C:0.34, D:0.02, X:0.63, or(X,X):0.01}   via and(X,and(X,ROLE)) (2.19e-04, rho=1.00e+00 k*=1)
    - 1.22e-04 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.22e-04, rho=1.95e-02 k*=50)
    - 7.29e-05 -> poly {C:0.33, D:0.01, X:0.64, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
- mono {D:1}
    - 8.00e-03 -> poly {C:0.67, D:0.33}   via C (8.00e-03, rho=3.21e-02 k*=67)
    - 4.45e-03 -> mono {X:1}   via X (4.45e-03, rho=1.92e-02 k*=100)
    - 4.27e-03 -> mono {ROLE:1}   via ROLE (4.27e-03, rho=2.24e-02 k*=100)
    - 1.06e-03 -> mono {not(ROLE):1}   via not(ROLE) (1.06e-03, rho=2.24e-02 k*=100)
    - 1.47e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.47e-04, rho=2.35e-02 k*=100)
    - 9.75e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (9.75e-05, rho=1.56e-02 k*=100)
- poly {C:0.66, D:0.32, X:0.01, and(X,X):0.01}
    - 3.86e-03 -> poly {C:0.65, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.31e-03 -> mono {ROLE:1}   via ROLE (2.31e-03, rho=1.21e-02 k*=100)
    - 5.76e-04 -> mono {not(ROLE):1}   via not(ROLE) (5.76e-04, rho=1.21e-02 k*=100)
    - 1.22e-04 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.22e-04, rho=1.95e-02 k*=50)
    - 7.29e-05 -> poly {C:0.65, D:0.32, X:0.01, and(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {C:0.65, D:0.32, X:0.01, and(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
- poly {C:0.65, D:0.33, X:0.01, or(X,X):0.01}
    - 3.86e-03 -> poly {C:0.65, D:0.32, X:0.01, and(X,X):0.01, or(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.31e-03 -> mono {ROLE:1}   via ROLE (2.31e-03, rho=1.21e-02 k*=100)
    - 5.76e-04 -> mono {not(ROLE):1}   via not(ROLE) (5.76e-04, rho=1.21e-02 k*=100)
    - 2.19e-04 -> poly {C:0.65, D:0.32, X:0.01, or(X,X):0.02}   via or(X,or(X,ROLE)) (2.19e-04, rho=1.00e+00 k*=1)
    - 1.22e-04 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.22e-04, rho=1.95e-02 k*=50)
    - 7.29e-05 -> poly {C:0.64, D:0.33, X:0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
