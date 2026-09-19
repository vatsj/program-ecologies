### arm=weak, n=5, game=chicken, N=100, w=0.01, x_on=True, role=True, mode=square

programs 902, classes 53, states 834, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 4.13e-03
mean payoff 0.0489, efficient 0.5000, deadweight loss 0.4511, mean bits in support 3.41

| pi | state |
|---|---|
| 0.4778 | mono {ROLE:1} |
| 0.0716 | mono {not(ROLE):1} |
| 0.0585 | mono {X:1} |
| 0.0453 | poly {C:0.8, D:0.17, X:0.01, and(X,X):0.01, or(X,X):0.01} |
| 0.0450 | poly {C:0.65, D:0.01, X:0.34} |
| 0.0433 | poly {C:0.81, D:0.18, X:0.01} |
| 0.0310 | mono {C:1} |
| 0.0236 | poly {C:0.65, D:0.01, X:0.32, and(X,X):0.01, or(X,X):0.01} |
| 0.0234 | poly {C:0.65, D:0.01, X:0.33, and(X,X):0.01} |
| 0.0232 | poly {C:0.64, D:0.01, X:0.34, or(X,X):0.01} |
| 0.0231 | poly {C:0.64, D:0.01, X:0.33, and(X,X):0.01, or(X,X):0.01} |
| 0.0227 | poly {C:0.81, D:0.17, X:0.01, or(X,X):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 1.45e-03 -> mono {C:1}   via C (1.45e-03, rho=5.84e-03 k*=100)
    - 8.63e-04 -> mono {X:1}   via X (8.63e-04, rho=3.73e-03 k*=100)
    - 3.49e-04 -> poly {ROLE:0.5, not(ROLE):0.5}   via not(ROLE) (3.49e-04, rho=7.36e-03 k*=50)
    - 1.15e-04 -> mono {D:1}   via D (1.15e-04, rho=4.63e-04 k*=100)
    - 4.83e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (4.83e-05, rho=7.72e-03 k*=100)
    - 2.08e-05 -> mono {or(X,X):1}   via or(X,X) (2.08e-05, rho=5.38e-03 k*=100)
- mono {not(ROLE):1}
    - 1.45e-03 -> mono {C:1}   via C (1.45e-03, rho=5.84e-03 k*=100)
    - 1.40e-03 -> poly {ROLE:0.5, not(ROLE):0.5}   via ROLE (1.40e-03, rho=7.36e-03 k*=50)
    - 8.63e-04 -> mono {X:1}   via X (8.63e-04, rho=3.73e-03 k*=100)
    - 1.15e-04 -> mono {D:1}   via D (1.15e-04, rho=4.63e-04 k*=100)
    - 3.00e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (3.00e-05, rho=4.79e-03 k*=100)
    - 2.08e-05 -> mono {or(X,X):1}   via or(X,X) (2.08e-05, rho=5.38e-03 k*=100)
- mono {X:1}
    - 5.52e-03 -> poly {C:0.64, X:0.36}   via C (5.52e-03, rho=2.22e-02 k*=64)
    - 2.78e-03 -> mono {ROLE:1}   via ROLE (2.78e-03, rho=1.46e-02 k*=100)
    - 6.94e-04 -> mono {not(ROLE):1}   via not(ROLE) (6.94e-04, rho=1.46e-02 k*=100)
    - 4.03e-04 -> mono {D:1}   via D (4.03e-04, rho=1.62e-03 k*=100)
    - 9.33e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (9.33e-05, rho=1.49e-02 k*=100)
    - 5.24e-05 -> mono {or(X,X):1}   via or(X,X) (5.24e-05, rho=1.36e-02 k*=100)
- poly {C:0.8, D:0.17, X:0.01, and(X,X):0.01, or(X,X):0.01}
    - 2.43e-03 -> mono {ROLE:1}   via ROLE (2.43e-03, rho=1.27e-02 k*=100)
    - 6.05e-04 -> mono {not(ROLE):1}   via not(ROLE) (6.05e-04, rho=1.27e-02 k*=100)
    - 2.25e-04 -> poly {C:0.73, and(X,ROLE):0.27}   via and(X,ROLE) (2.25e-04, rho=3.59e-02 k*=27)
    - 7.29e-05 -> poly {C:0.79, D:0.17, X:0.01, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {C:0.79, D:0.17, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {C:0.8, D:0.16, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
- poly {C:0.65, D:0.01, X:0.34}
    - 3.86e-03 -> poly {C:0.64, D:0.01, X:0.34, or(X,X):0.01}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.65, D:0.01, X:0.33, and(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.43e-03 -> mono {ROLE:1}   via ROLE (2.43e-03, rho=1.28e-02 k*=100)
    - 6.07e-04 -> mono {not(ROLE):1}   via not(ROLE) (6.07e-04, rho=1.28e-02 k*=100)
    - 2.25e-04 -> poly {C:0.73, and(X,ROLE):0.27}   via and(X,ROLE) (2.25e-04, rho=3.60e-02 k*=27)
    - 7.29e-05 -> poly {C:0.64, D:0.01, X:0.34, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
- poly {C:0.81, D:0.18, X:0.01}
    - 3.86e-03 -> poly {C:0.81, D:0.17, X:0.01, or(X,X):0.01}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.81, D:0.17, X:0.01, and(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.43e-03 -> mono {ROLE:1}   via ROLE (2.43e-03, rho=1.27e-02 k*=100)
    - 6.05e-04 -> mono {not(ROLE):1}   via not(ROLE) (6.05e-04, rho=1.27e-02 k*=100)
    - 2.25e-04 -> poly {C:0.73, and(X,ROLE):0.27}   via and(X,ROLE) (2.25e-04, rho=3.59e-02 k*=27)
    - 7.29e-05 -> poly {C:0.8, D:0.18, X:0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
- mono {C:1}
    - 1.56e-02 -> poly {C:0.82, D:0.18}   via D (1.56e-02, rho=6.25e-02 k*=18)
    - 7.24e-03 -> poly {C:0.64, X:0.36}   via X (7.24e-03, rho=3.13e-02 k*=36)
    - 3.00e-03 -> mono {ROLE:1}   via ROLE (3.00e-03, rho=1.58e-02 k*=100)
    - 7.48e-04 -> mono {not(ROLE):1}   via not(ROLE) (7.48e-04, rho=1.58e-02 k*=100)
    - 2.65e-04 -> poly {C:0.73, and(X,ROLE):0.27}   via and(X,ROLE) (2.65e-04, rho=4.23e-02 k*=27)
    - 1.81e-04 -> poly {C:0.76, and(X,X):0.24}   via and(X,X) (1.81e-04, rho=4.69e-02 k*=24)
- poly {C:0.65, D:0.01, X:0.32, and(X,X):0.01, or(X,X):0.01}
    - 2.43e-03 -> mono {ROLE:1}   via ROLE (2.43e-03, rho=1.28e-02 k*=100)
    - 6.07e-04 -> mono {not(ROLE):1}   via not(ROLE) (6.07e-04, rho=1.28e-02 k*=100)
    - 2.25e-04 -> poly {C:0.73, and(X,ROLE):0.27}   via and(X,ROLE) (2.25e-04, rho=3.60e-02 k*=27)
    - 7.29e-05 -> poly {C:0.64, D:0.01, X:0.32, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {C:0.64, D:0.01, X:0.32, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {C:0.65, D:0.01, X:0.31, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
- poly {C:0.65, D:0.01, X:0.33, and(X,X):0.01}
    - 3.86e-03 -> poly {C:0.65, D:0.01, X:0.32, and(X,X):0.01, or(X,X):0.01}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.43e-03 -> mono {ROLE:1}   via ROLE (2.43e-03, rho=1.28e-02 k*=100)
    - 6.06e-04 -> mono {not(ROLE):1}   via not(ROLE) (6.06e-04, rho=1.28e-02 k*=100)
    - 2.25e-04 -> poly {C:0.73, and(X,ROLE):0.27}   via and(X,ROLE) (2.25e-04, rho=3.59e-02 k*=27)
    - 7.29e-05 -> poly {C:0.64, D:0.01, X:0.33, and(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {C:0.64, D:0.01, X:0.33, and(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
- poly {C:0.64, D:0.01, X:0.34, or(X,X):0.01}
    - 3.86e-03 -> poly {C:0.64, D:0.01, X:0.33, and(X,X):0.01, or(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.43e-03 -> mono {ROLE:1}   via ROLE (2.43e-03, rho=1.28e-02 k*=100)
    - 6.06e-04 -> mono {not(ROLE):1}   via not(ROLE) (6.06e-04, rho=1.28e-02 k*=100)
    - 2.25e-04 -> poly {C:0.73, and(X,ROLE):0.27}   via and(X,ROLE) (2.25e-04, rho=3.59e-02 k*=27)
    - 2.19e-04 -> poly {C:0.65, D:0.01, X:0.33, or(X,X):0.01}   via and(X,and(X,ROLE)) (2.19e-04, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {C:0.63, D:0.01, X:0.34, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
- poly {C:0.64, D:0.01, X:0.33, and(X,X):0.01, or(X,X):0.01}
    - 2.43e-03 -> mono {ROLE:1}   via ROLE (2.43e-03, rho=1.27e-02 k*=100)
    - 6.05e-04 -> mono {not(ROLE):1}   via not(ROLE) (6.05e-04, rho=1.27e-02 k*=100)
    - 2.25e-04 -> poly {C:0.73, and(X,ROLE):0.27}   via and(X,ROLE) (2.25e-04, rho=3.59e-02 k*=27)
    - 7.29e-05 -> poly {C:0.64, D:0.01, X:0.32, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {C:0.64, D:0.01, X:0.32, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {C:0.65, D:0.01, X:0.31, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
- poly {C:0.81, D:0.17, X:0.01, or(X,X):0.01}
    - 3.86e-03 -> poly {C:0.8, D:0.17, X:0.01, and(X,X):0.01, or(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.44e-03 -> mono {ROLE:1}   via ROLE (2.44e-03, rho=1.28e-02 k*=100)
    - 6.08e-04 -> mono {not(ROLE):1}   via not(ROLE) (6.08e-04, rho=1.28e-02 k*=100)
    - 2.26e-04 -> poly {C:0.73, and(X,ROLE):0.27}   via and(X,ROLE) (2.26e-04, rho=3.61e-02 k*=27)
    - 7.29e-05 -> poly {C:0.8, D:0.17, X:0.01, or(X,X):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {C:0.8, D:0.17, X:0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
