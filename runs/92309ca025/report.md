### arm=weak, n=5, game=demand, N=10, w=0.01, x_on=True, role=True, mode=square

programs 902, classes 53, states 1173, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 4.26e-02
mean payoff 0.3800, efficient 0.5000, deadweight loss 0.1200, mean bits in support 3.41

| pi | state |
|---|---|
| 0.2055 | mono {ROLE:1} |
| 0.1728 | poly {C:0.6, D:0.3, X:0.1} |
| 0.1451 | poly {C:0.4, D:0.1, X:0.5} |
| 0.0956 | mono {D:1} |
| 0.0630 | mono {X:1} |
| 0.0436 | mono {C:1} |
| 0.0319 | mono {not(ROLE):1} |
| 0.0264 | poly {C:0.7, D:0.3} |
| 0.0241 | poly {C:0.5, D:0.3, X:0.1, or(X,X):0.1} |
| 0.0241 | poly {C:0.6, D:0.2, X:0.1, and(X,X):0.1} |
| 0.0240 | poly {C:0.3, X:0.7} |
| 0.0227 | poly {C:0.4, D:0.1, X:0.4, and(X,X):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 2.48e-02 -> mono {C:1}   via C (2.48e-02, rho=9.96e-02 k*=10)
    - 2.47e-02 -> mono {D:1}   via D (2.47e-02, rho=9.93e-02 k*=10)
    - 2.30e-02 -> mono {X:1}   via X (2.30e-02, rho=9.96e-02 k*=10)
    - 9.46e-03 -> poly {ROLE:0.5, not(ROLE):0.5}   via not(ROLE) (9.46e-03, rho=1.99e-01 k*=5)
    - 6.24e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.24e-04, rho=9.98e-02 k*=10)
    - 6.24e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.24e-04, rho=9.96e-02 k*=10)
- poly {C:0.6, D:0.3, X:0.1}
    - 1.91e-02 -> mono {ROLE:1}   via ROLE (1.91e-02, rho=1.00e-01 k*=10)
    - 4.76e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.76e-03, rho=1.00e-01 k*=10)
    - 3.86e-03 -> poly {C:0.5, D:0.3, X:0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.6, D:0.2, X:0.1, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.26e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
- poly {C:0.4, D:0.1, X:0.5}
    - 1.91e-02 -> mono {ROLE:1}   via ROLE (1.91e-02, rho=1.00e-01 k*=10)
    - 4.76e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.76e-03, rho=1.00e-01 k*=10)
    - 3.86e-03 -> poly {C:0.4, D:0.1, X:0.4, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.4, D:0.1, X:0.4, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.26e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
- mono {D:1}
    - 3.58e-02 -> poly {C:0.7, D:0.3}   via C (3.58e-02, rho=1.44e-01 k*=7)
    - 2.33e-02 -> mono {X:1}   via X (2.33e-02, rho=1.01e-01 k*=10)
    - 1.92e-02 -> mono {ROLE:1}   via ROLE (1.92e-02, rho=1.01e-01 k*=10)
    - 4.79e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.79e-03, rho=1.01e-01 k*=10)
    - 6.30e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.30e-04, rho=1.01e-01 k*=10)
    - 6.28e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.28e-04, rho=1.00e-01 k*=10)
- mono {X:1}
    - 8.30e-02 -> poly {C:0.3, X:0.7}   via C (8.30e-02, rho=3.33e-01 k*=3)
    - 2.48e-02 -> mono {D:1}   via D (2.48e-02, rho=9.97e-02 k*=10)
    - 1.91e-02 -> mono {ROLE:1}   via ROLE (1.91e-02, rho=1.00e-01 k*=10)
    - 4.76e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.76e-03, rho=1.00e-01 k*=10)
    - 6.26e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
    - 6.25e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.25e-04, rho=9.99e-02 k*=10)
- mono {C:1}
    - 8.31e-02 -> poly {C:0.7, D:0.3}   via D (8.31e-02, rho=3.34e-01 k*=3)
    - 3.31e-02 -> poly {C:0.3, X:0.7}   via X (3.31e-02, rho=1.43e-01 k*=7)
    - 1.91e-02 -> mono {ROLE:1}   via ROLE (1.91e-02, rho=1.00e-01 k*=10)
    - 4.77e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.77e-03, rho=1.00e-01 k*=10)
    - 1.25e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 9.67e-04 -> poly {C:0.6, and(X,X):0.4}   via and(X,X) (9.67e-04, rho=2.50e-01 k*=4)
- mono {not(ROLE):1}
    - 3.79e-02 -> poly {ROLE:0.5, not(ROLE):0.5}   via ROLE (3.79e-02, rho=1.99e-01 k*=5)
    - 2.48e-02 -> mono {C:1}   via C (2.48e-02, rho=9.96e-02 k*=10)
    - 2.47e-02 -> mono {D:1}   via D (2.47e-02, rho=9.93e-02 k*=10)
    - 2.30e-02 -> mono {X:1}   via X (2.30e-02, rho=9.96e-02 k*=10)
    - 6.23e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.23e-04, rho=9.96e-02 k*=10)
    - 6.22e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.22e-04, rho=9.94e-02 k*=10)
- poly {C:0.7, D:0.3}
    - 2.31e-01 -> poly {C:0.6, D:0.3, X:0.1}   via X (2.31e-01, rho=1.00e+00 k*=1)
    - 1.91e-02 -> mono {ROLE:1}   via ROLE (1.91e-02, rho=1.00e-01 k*=10)
    - 4.76e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.76e-03, rho=1.00e-01 k*=10)
    - 3.86e-03 -> poly {C:0.6, D:0.3, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.6, D:0.3, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
- poly {C:0.5, D:0.3, X:0.1, or(X,X):0.1}
    - 1.91e-02 -> mono {ROLE:1}   via ROLE (1.91e-02, rho=1.00e-01 k*=10)
    - 4.76e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.76e-03, rho=1.00e-01 k*=10)
    - 3.86e-03 -> poly {C:0.5, D:0.2, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.26e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
    - 3.51e-04 -> poly {C:0.5, not(or(X,ROLE)):0.5}   via not(or(X,ROLE)) (3.51e-04, rho=2.00e-01 k*=5)
- poly {C:0.6, D:0.2, X:0.1, and(X,X):0.1}
    - 1.91e-02 -> mono {ROLE:1}   via ROLE (1.91e-02, rho=1.00e-01 k*=10)
    - 4.76e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.76e-03, rho=1.00e-01 k*=10)
    - 3.86e-03 -> poly {C:0.5, D:0.2, X:0.1, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.26e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
    - 3.51e-04 -> poly {C:0.5, not(or(X,ROLE)):0.5}   via not(or(X,ROLE)) (3.51e-04, rho=2.00e-01 k*=5)
- poly {C:0.3, X:0.7}
    - 2.49e-01 -> poly {C:0.4, X:0.6}   via D (2.49e-01, rho=1.00e+00 k*=1)
    - 1.91e-02 -> mono {ROLE:1}   via ROLE (1.91e-02, rho=1.00e-01 k*=10)
    - 4.76e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.76e-03, rho=1.00e-01 k*=10)
    - 3.86e-03 -> poly {C:0.3, X:0.6, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.4, X:0.5, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
- poly {C:0.4, D:0.1, X:0.4, and(X,X):0.1}
    - 1.91e-02 -> mono {ROLE:1}   via ROLE (1.91e-02, rho=1.00e-01 k*=10)
    - 4.76e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.76e-03, rho=1.00e-01 k*=10)
    - 3.86e-03 -> poly {C:0.4, D:0.1, X:0.3, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.25e-03 -> poly {C:0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.25e-03, rho=2.00e-01 k*=5)
    - 6.26e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-04, rho=1.00e-01 k*=10)
    - 3.51e-04 -> poly {C:0.5, not(or(X,ROLE)):0.5}   via not(or(X,ROLE)) (3.51e-04, rho=2.00e-01 k*=5)
