### arm=weak, n=5, game=chicken, N=10, w=0.1, x_on=True, role=True, mode=square

programs 902, classes 53, states 698, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 3.32e-02
mean payoff 0.0311, efficient 0.5000, deadweight loss 0.4689, mean bits in support 3.43

| pi | state |
|---|---|
| 0.4585 | mono {ROLE:1} |
| 0.0952 | poly {C:0.7, D:0.1, X:0.2} |
| 0.0907 | poly {C:0.8, D:0.1, X:0.1} |
| 0.0745 | mono {not(ROLE):1} |
| 0.0616 | mono {X:1} |
| 0.0346 | mono {C:1} |
| 0.0233 | poly {C:0.7, D:0.1, X:0.1, and(X,X):0.1} |
| 0.0195 | poly {C:0.6, X:0.4} |
| 0.0173 | poly {C:0.8, D:0.2} |
| 0.0165 | poly {C:0.7, X:0.3} |
| 0.0143 | poly {C:0.7, and(X,ROLE):0.3} |
| 0.0127 | poly {C:0.6, D:0.1, X:0.2, or(X,X):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 1.49e-02 -> mono {C:1}   via C (1.49e-02, rho=6.00e-02 k*=10)
    - 9.13e-03 -> mono {X:1}   via X (9.13e-03, rho=3.95e-02 k*=10)
    - 2.94e-03 -> poly {ROLE:0.5, not(ROLE):0.5}   via not(ROLE) (2.94e-03, rho=6.18e-02 k*=5)
    - 4.92e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (4.92e-04, rho=7.86e-02 k*=10)
    - 2.17e-04 -> mono {or(X,X):1}   via or(X,X) (2.17e-04, rho=5.63e-02 k*=10)
    - 1.71e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.71e-04, rho=2.73e-02 k*=10)
- poly {C:0.7, D:0.1, X:0.2}
    - 2.41e-02 -> mono {ROLE:1}   via ROLE (2.41e-02, rho=1.26e-01 k*=10)
    - 6.00e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.00e-03, rho=1.26e-01 k*=10)
    - 3.86e-03 -> poly {C:0.6, D:0.1, X:0.2, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.7, D:0.1, X:0.1, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.08e-03 -> poly {C:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.08e-03, rho=3.33e-01 k*=3)
    - 6.84e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.84e-04, rho=1.09e-01 k*=10)
- poly {C:0.8, D:0.1, X:0.1}
    - 2.48e-02 -> mono {ROLE:1}   via ROLE (2.48e-02, rho=1.30e-01 k*=10)
    - 6.18e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.18e-03, rho=1.30e-01 k*=10)
    - 3.86e-03 -> poly {C:0.7, D:0.1, X:0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.7, D:0.1, X:0.1, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.14e-03 -> poly {C:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.14e-03, rho=3.42e-01 k*=3)
    - 6.93e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.93e-04, rho=1.11e-01 k*=10)
- mono {not(ROLE):1}
    - 1.49e-02 -> mono {C:1}   via C (1.49e-02, rho=6.00e-02 k*=10)
    - 1.18e-02 -> poly {ROLE:0.5, not(ROLE):0.5}   via ROLE (1.18e-02, rho=6.18e-02 k*=5)
    - 9.13e-03 -> mono {X:1}   via X (9.13e-03, rho=3.95e-02 k*=10)
    - 2.99e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.99e-04, rho=4.78e-02 k*=10)
    - 2.17e-04 -> mono {or(X,X):1}   via or(X,X) (2.17e-04, rho=5.63e-02 k*=10)
    - 1.38e-04 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (1.38e-04, rho=7.86e-02 k*=10)
- mono {X:1}
    - 5.39e-02 -> poly {C:0.6, X:0.4}   via C (5.39e-02, rho=2.17e-01 k*=6)
    - 2.71e-02 -> mono {ROLE:1}   via ROLE (2.71e-02, rho=1.42e-01 k*=10)
    - 6.76e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.76e-03, rho=1.42e-01 k*=10)
    - 8.73e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (8.73e-04, rho=1.40e-01 k*=10)
    - 4.96e-04 -> mono {or(X,X):1}   via or(X,X) (4.96e-04, rho=1.28e-01 k*=10)
    - 3.75e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (3.75e-04, rho=5.99e-02 k*=10)
- mono {C:1}
    - 1.36e-01 -> poly {C:0.8, D:0.2}   via D (1.36e-01, rho=5.48e-01 k*=2)
    - 6.52e-02 -> poly {C:0.6, X:0.4}   via X (6.52e-02, rho=2.82e-01 k*=4)
    - 2.89e-02 -> mono {ROLE:1}   via ROLE (2.89e-02, rho=1.52e-01 k*=10)
    - 7.21e-03 -> mono {not(ROLE):1}   via not(ROLE) (7.21e-03, rho=1.52e-01 k*=10)
    - 2.36e-03 -> poly {C:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.36e-03, rho=3.78e-01 k*=3)
    - 2.07e-03 -> poly {C:0.8, and(X,X):0.2}   via and(X,X) (2.07e-03, rho=5.37e-01 k*=2)
- poly {C:0.7, D:0.1, X:0.1, and(X,X):0.1}
    - 2.38e-02 -> mono {ROLE:1}   via ROLE (2.38e-02, rho=1.25e-01 k*=10)
    - 5.95e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.95e-03, rho=1.25e-01 k*=10)
    - 3.86e-03 -> poly {C:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.06e-03 -> poly {C:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.06e-03, rho=3.28e-01 k*=3)
    - 6.83e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.83e-04, rho=1.09e-01 k*=10)
    - 5.77e-04 -> poly {C:0.7, not(or(X,ROLE)):0.3}   via not(or(X,ROLE)) (5.77e-04, rho=3.28e-01 k*=3)
- poly {C:0.6, X:0.4}
    - 2.53e-01 -> poly {C:0.7, X:0.3}   via D (2.49e-01, rho=1.00e+00 k*=1), and(X,X) (3.86e-03, rho=1.00e+00 k*=1), and(X,and(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
    - 2.41e-02 -> mono {ROLE:1}   via ROLE (2.41e-02, rho=1.26e-01 k*=10)
    - 6.00e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.00e-03, rho=1.26e-01 k*=10)
    - 3.86e-03 -> poly {C:0.6, X:0.3, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.08e-03 -> poly {C:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.08e-03, rho=3.33e-01 k*=3)
    - 6.84e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.84e-04, rho=1.09e-01 k*=10)
- poly {C:0.8, D:0.2}
    - 2.31e-01 -> poly {C:0.8, D:0.1, X:0.1}   via X (2.31e-01, rho=1.00e+00 k*=1)
    - 2.41e-02 -> mono {ROLE:1}   via ROLE (2.41e-02, rho=1.26e-01 k*=10)
    - 6.00e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.00e-03, rho=1.26e-01 k*=10)
    - 3.86e-03 -> poly {C:0.7, D:0.2, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.8, D:0.1, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.08e-03 -> poly {C:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.08e-03, rho=3.33e-01 k*=3)
- poly {C:0.7, X:0.3}
    - 2.49e-01 -> poly {C:0.7, D:0.1, X:0.2}   via D (2.49e-01, rho=1.00e+00 k*=1)
    - 2.48e-02 -> mono {ROLE:1}   via ROLE (2.48e-02, rho=1.30e-01 k*=10)
    - 6.55e-03 -> poly {C:0.6, X:0.4}   via THEM(ME) (2.18e-03, rho=1.00e+00 k*=1), THEM(THEM) (2.18e-03, rho=1.00e+00 k*=1), THEM(^C) (4.39e-04, rho=1.00e+00 k*=1), THEM(^D) (4.39e-04, rho=1.00e+00 k*=1)
    - 6.18e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.18e-03, rho=1.30e-01 k*=10)
    - 3.86e-03 -> poly {C:0.6, X:0.3, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.7, X:0.2, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
- poly {C:0.7, and(X,ROLE):0.3}
    - 2.47e-02 -> mono {ROLE:1}   via ROLE (2.47e-02, rho=1.30e-01 k*=10)
    - 1.96e-02 -> mono {X:1}   via X (1.96e-02, rho=8.48e-02 k*=10)
    - 5.53e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.53e-03, rho=1.16e-01 k*=10)
    - 6.91e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.91e-04, rho=1.10e-01 k*=10)
    - 6.12e-04 -> mono {D:1}   via D (6.12e-04, rho=2.46e-03 k*=10)
    - 5.63e-04 -> poly {C:0.7, not(or(X,ROLE)):0.3}   via not(or(X,ROLE)) (5.63e-04, rho=3.21e-01 k*=3)
- poly {C:0.6, D:0.1, X:0.2, or(X,X):0.1}
    - 2.38e-02 -> mono {ROLE:1}   via ROLE (2.38e-02, rho=1.25e-01 k*=10)
    - 5.95e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.95e-03, rho=1.25e-01 k*=10)
    - 3.86e-03 -> poly {C:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.06e-03 -> poly {C:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.06e-03, rho=3.28e-01 k*=3)
    - 6.83e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.83e-04, rho=1.09e-01 k*=10)
    - 5.77e-04 -> poly {C:0.7, not(or(X,ROLE)):0.3}   via not(or(X,ROLE)) (5.77e-04, rho=3.28e-01 k*=3)
