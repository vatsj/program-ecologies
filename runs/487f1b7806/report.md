### arm=weak, n=5, game=demand, N=10, w=1.0, x_on=True, role=True, mode=square

programs 902, classes 53, states 1167, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 4.17e-02
mean payoff 0.4126, efficient 0.5000, deadweight loss 0.0874, mean bits in support 3.41

| pi | state |
|---|---|
| 0.3100 | mono {ROLE:1} |
| 0.1415 | poly {C:0.6, D:0.3, X:0.1} |
| 0.1357 | poly {C:0.4, D:0.1, X:0.5} |
| 0.0640 | mono {X:1} |
| 0.0464 | mono {not(ROLE):1} |
| 0.0450 | mono {D:1} |
| 0.0403 | mono {C:1} |
| 0.0247 | poly {C:0.3, X:0.7} |
| 0.0235 | poly {C:0.7, D:0.3} |
| 0.0210 | poly {C:0.4, X:0.6} |
| 0.0197 | poly {C:0.4, D:0.1, X:0.4, and(X,X):0.1} |
| 0.0181 | poly {C:0.5, D:0.3, X:0.1, or(X,X):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 1.79e-02 -> mono {C:1}   via C (1.79e-02, rho=7.19e-02 k*=10)
    - 1.72e-02 -> mono {X:1}   via X (1.72e-02, rho=7.44e-02 k*=10)
    - 1.29e-02 -> mono {D:1}   via D (1.29e-02, rho=5.19e-02 k*=10)
    - 6.92e-03 -> poly {ROLE:0.5, not(ROLE):0.5}   via not(ROLE) (6.92e-03, rho=1.46e-01 k*=5)
    - 5.35e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (5.35e-04, rho=8.54e-02 k*=10)
    - 4.71e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (4.71e-04, rho=7.53e-02 k*=10)
- poly {C:0.6, D:0.3, X:0.1}
    - 2.16e-02 -> mono {ROLE:1}   via ROLE (2.16e-02, rho=1.14e-01 k*=10)
    - 5.39e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.39e-03, rho=1.14e-01 k*=10)
    - 3.86e-03 -> poly {C:0.5, D:0.3, X:0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.6, D:0.2, X:0.1, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.42e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.42e-04, rho=1.03e-01 k*=10)
- poly {C:0.4, D:0.1, X:0.5}
    - 2.16e-02 -> mono {ROLE:1}   via ROLE (2.16e-02, rho=1.14e-01 k*=10)
    - 5.39e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.39e-03, rho=1.14e-01 k*=10)
    - 3.86e-03 -> poly {C:0.4, D:0.1, X:0.4, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.4, D:0.1, X:0.4, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.42e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.42e-04, rho=1.03e-01 k*=10)
- mono {X:1}
    - 8.47e-02 -> poly {C:0.3, X:0.7}   via C (8.47e-02, rho=3.40e-01 k*=3)
    - 2.18e-02 -> mono {ROLE:1}   via ROLE (2.18e-02, rho=1.14e-01 k*=10)
    - 1.81e-02 -> mono {D:1}   via D (1.81e-02, rho=7.27e-02 k*=10)
    - 5.43e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.43e-03, rho=1.14e-01 k*=10)
    - 6.60e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.60e-04, rho=1.05e-01 k*=10)
    - 5.91e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (5.91e-04, rho=9.44e-02 k*=10)
- mono {not(ROLE):1}
    - 2.78e-02 -> poly {ROLE:0.5, not(ROLE):0.5}   via ROLE (2.78e-02, rho=1.46e-01 k*=5)
    - 1.79e-02 -> mono {C:1}   via C (1.79e-02, rho=7.19e-02 k*=10)
    - 1.72e-02 -> mono {X:1}   via X (1.72e-02, rho=7.44e-02 k*=10)
    - 1.29e-02 -> mono {D:1}   via D (1.29e-02, rho=5.19e-02 k*=10)
    - 4.57e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (4.57e-04, rho=7.30e-02 k*=10)
    - 3.99e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (3.99e-04, rho=6.37e-02 k*=10)
- mono {D:1}
    - 5.79e-02 -> poly {C:0.7, D:0.3}   via C (5.79e-02, rho=2.33e-01 k*=7)
    - 3.60e-02 -> mono {X:1}   via X (3.60e-02, rho=1.55e-01 k*=10)
    - 3.31e-02 -> mono {ROLE:1}   via ROLE (3.31e-02, rho=1.74e-01 k*=10)
    - 8.25e-03 -> mono {not(ROLE):1}   via not(ROLE) (8.25e-03, rho=1.74e-01 k*=10)
    - 1.08e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.08e-03, rho=1.73e-01 k*=10)
    - 8.60e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (8.60e-04, rho=1.37e-01 k*=10)
- mono {C:1}
    - 9.31e-02 -> poly {C:0.7, D:0.3}   via D (9.31e-02, rho=3.74e-01 k*=3)
    - 3.83e-02 -> poly {C:0.3, X:0.7}   via X (3.83e-02, rho=1.65e-01 k*=7)
    - 2.55e-02 -> mono {ROLE:1}   via ROLE (2.55e-02, rho=1.34e-01 k*=10)
    - 6.35e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.35e-03, rho=1.34e-01 k*=10)
    - 1.46e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.46e-03, rho=2.33e-01 k*=5)
    - 1.09e-03 -> poly {C:0.6, and(X,X):0.4}   via and(X,X) (1.09e-03, rho=2.83e-01 k*=4)
- poly {C:0.3, X:0.7}
    - 2.49e-01 -> poly {C:0.4, X:0.6}   via D (2.49e-01, rho=1.00e+00 k*=1)
    - 2.16e-02 -> mono {ROLE:1}   via ROLE (2.16e-02, rho=1.14e-01 k*=10)
    - 5.39e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.39e-03, rho=1.14e-01 k*=10)
    - 3.86e-03 -> poly {C:0.3, X:0.6, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.4, X:0.5, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
- poly {C:0.7, D:0.3}
    - 2.31e-01 -> poly {C:0.6, D:0.3, X:0.1}   via X (2.31e-01, rho=1.00e+00 k*=1)
    - 2.18e-02 -> mono {ROLE:1}   via ROLE (2.18e-02, rho=1.14e-01 k*=10)
    - 5.44e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.44e-03, rho=1.14e-01 k*=10)
    - 3.86e-03 -> poly {C:0.6, D:0.3, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.6, D:0.3, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.27e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.27e-03, rho=2.02e-01 k*=5)
- poly {C:0.4, X:0.6}
    - 2.49e-01 -> poly {C:0.4, D:0.1, X:0.5}   via D (2.49e-01, rho=1.00e+00 k*=1)
    - 2.18e-02 -> mono {ROLE:1}   via ROLE (2.18e-02, rho=1.14e-01 k*=10)
    - 6.70e-03 -> poly {C:0.3, X:0.7}   via THEM(ME) (2.18e-03, rho=1.00e+00 k*=1), THEM(THEM) (2.18e-03, rho=1.00e+00 k*=1), THEM(^C) (4.39e-04, rho=1.00e+00 k*=1), THEM(^D) (4.39e-04, rho=1.00e+00 k*=1)
    - 5.44e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.44e-03, rho=1.14e-01 k*=10)
    - 3.86e-03 -> poly {C:0.3, X:0.6, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.4, X:0.5, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
- poly {C:0.4, D:0.1, X:0.4, and(X,X):0.1}
    - 2.16e-02 -> mono {ROLE:1}   via ROLE (2.16e-02, rho=1.13e-01 k*=10)
    - 5.38e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.38e-03, rho=1.13e-01 k*=10)
    - 3.86e-03 -> poly {C:0.4, D:0.1, X:0.3, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.24e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.24e-03, rho=1.98e-01 k*=5)
    - 6.42e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.42e-04, rho=1.03e-01 k*=10)
    - 3.49e-04 -> poly {C:0.5, not(or(X,ROLE)):0.5}   via not(or(X,ROLE)) (3.49e-04, rho=1.98e-01 k*=5)
- poly {C:0.5, D:0.3, X:0.1, or(X,X):0.1}
    - 2.16e-02 -> mono {ROLE:1}   via ROLE (2.16e-02, rho=1.13e-01 k*=10)
    - 5.38e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.38e-03, rho=1.13e-01 k*=10)
    - 3.86e-03 -> poly {C:0.5, D:0.2, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.24e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.24e-03, rho=1.98e-01 k*=5)
    - 6.42e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.42e-04, rho=1.03e-01 k*=10)
    - 3.49e-04 -> poly {C:0.5, not(or(X,ROLE)):0.5}   via not(or(X,ROLE)) (3.49e-04, rho=1.98e-01 k*=5)
