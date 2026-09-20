### arm=weak, n=5, game=chicken, N=10, w=0.3, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 53, states 516, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 9.71e-03
mean payoff 0.3918, efficient 0.5000, deadweight loss 0.1082, mean bits in support 3.49

| pi | state |
|---|---|
| 0.6991 | mono {ROLE:1} |
| 0.1735 | mono {not(ROLE):1} |
| 0.0264 | poly {Straight:0.1, Swerve:0.8, X:0.1} |
| 0.0243 | poly {Straight:0.1, Swerve:0.7, X:0.2} |
| 0.0124 | mono {X:1} |
| 0.0115 | mono {Swerve:1} |
| 0.0066 | poly {Straight:0.2, Swerve:0.8} |
| 0.0065 | poly {Swerve:0.6, X:0.4} |
| 0.0055 | mono {or(X,ROLE):1} |
| 0.0053 | poly {Straight:0.1, Swerve:0.7, X:0.1, and(X,X):0.1} |
| 0.0052 | poly {Swerve:0.7, X:0.3} |
| 0.0037 | poly {Swerve:0.7, and(X,ROLE):0.3} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 4.08e-03 -> mono {Swerve:1}   via Swerve (4.08e-03, rho=1.64e-02 k*=10)
    - 1.65e-03 -> mono {X:1}   via X (1.65e-03, rho=7.15e-03 k*=10)
    - 2.81e-04 -> mono {not(ROLE):1}   via not(ROLE) (2.81e-04, rho=5.91e-03 k*=10)
    - 2.77e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.77e-04, rho=4.43e-02 k*=10)
    - 6.60e-05 -> mono {or(X,X):1}   via or(X,X) (6.60e-05, rho=1.71e-02 k*=10)
    - 3.23e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (3.23e-05, rho=8.02e-02 k*=10)
- mono {not(ROLE):1}
    - 4.08e-03 -> mono {Swerve:1}   via Swerve (4.08e-03, rho=1.64e-02 k*=10)
    - 1.65e-03 -> mono {X:1}   via X (1.65e-03, rho=7.15e-03 k*=10)
    - 1.13e-03 -> mono {ROLE:1}   via ROLE (1.13e-03, rho=5.91e-03 k*=10)
    - 7.99e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.99e-05, rho=1.28e-02 k*=10)
    - 7.79e-05 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (7.79e-05, rho=4.43e-02 k*=10)
    - 6.60e-05 -> mono {or(X,X):1}   via or(X,X) (6.60e-05, rho=1.71e-02 k*=10)
- poly {Straight:0.1, Swerve:0.8, X:0.1}
    - 3.58e-02 -> mono {ROLE:1}   via ROLE (3.58e-02, rho=1.88e-01 k*=10)
    - 8.92e-03 -> mono {not(ROLE):1}   via not(ROLE) (8.92e-03, rho=1.88e-01 k*=10)
    - 3.86e-03 -> poly {Straight:0.1, Swerve:0.7, X:0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {Straight:0.1, Swerve:0.7, X:0.1, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.26e-03 -> poly {Swerve:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.26e-03, rho=3.60e-01 k*=3)
    - 8.28e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (8.28e-04, rho=1.32e-01 k*=10)
- poly {Straight:0.1, Swerve:0.7, X:0.2}
    - 3.27e-02 -> mono {ROLE:1}   via ROLE (3.27e-02, rho=1.72e-01 k*=10)
    - 8.17e-03 -> mono {not(ROLE):1}   via not(ROLE) (8.17e-03, rho=1.72e-01 k*=10)
    - 3.86e-03 -> poly {Straight:0.1, Swerve:0.6, X:0.2, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {Straight:0.1, Swerve:0.7, X:0.1, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.08e-03 -> poly {Swerve:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.08e-03, rho=3.32e-01 k*=3)
    - 7.96e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.96e-04, rho=1.27e-01 k*=10)
- mono {X:1}
    - 7.90e-02 -> poly {Swerve:0.6, X:0.4}   via Swerve (7.90e-02, rho=3.17e-01 k*=6)
    - 3.69e-02 -> mono {ROLE:1}   via ROLE (3.69e-02, rho=1.94e-01 k*=10)
    - 9.20e-03 -> mono {not(ROLE):1}   via not(ROLE) (9.20e-03, rho=1.94e-01 k*=10)
    - 1.34e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.34e-03, rho=2.15e-01 k*=10)
    - 7.03e-04 -> mono {or(X,X):1}   via or(X,X) (7.03e-04, rho=1.82e-01 k*=10)
    - 3.92e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.92e-04, rho=1.80e-01 k*=10)
- mono {Swerve:1}
    - 1.63e-01 -> poly {Straight:0.2, Swerve:0.8}   via Straight (1.63e-01, rho=6.53e-01 k*=2)
    - 8.21e-02 -> poly {Swerve:0.6, X:0.4}   via X (8.21e-02, rho=3.55e-01 k*=4)
    - 5.40e-02 -> mono {ROLE:1}   via ROLE (5.40e-02, rho=2.83e-01 k*=10)
    - 1.35e-02 -> mono {not(ROLE):1}   via not(ROLE) (1.35e-02, rho=2.83e-01 k*=10)
    - 3.00e-03 -> poly {Swerve:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (3.00e-03, rho=4.79e-01 k*=3)
    - 2.38e-03 -> poly {Swerve:0.8, and(X,X):0.2}   via and(X,X) (2.38e-03, rho=6.17e-01 k*=2)
- poly {Straight:0.2, Swerve:0.8}
    - 2.31e-01 -> poly {Straight:0.1, Swerve:0.8, X:0.1}   via X (2.31e-01, rho=1.00e+00 k*=1)
    - 3.27e-02 -> mono {ROLE:1}   via ROLE (3.27e-02, rho=1.72e-01 k*=10)
    - 8.17e-03 -> mono {not(ROLE):1}   via not(ROLE) (8.17e-03, rho=1.72e-01 k*=10)
    - 3.86e-03 -> poly {Straight:0.2, Swerve:0.7, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {Straight:0.1, Swerve:0.8, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.08e-03 -> poly {Swerve:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.08e-03, rho=3.32e-01 k*=3)
- poly {Swerve:0.6, X:0.4}
    - 2.53e-01 -> poly {Swerve:0.7, X:0.3}   via Straight (2.49e-01, rho=1.00e+00 k*=1), and(X,X) (3.86e-03, rho=1.00e+00 k*=1), and(X,and(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
    - 3.27e-02 -> mono {ROLE:1}   via ROLE (3.27e-02, rho=1.72e-01 k*=10)
    - 8.17e-03 -> mono {not(ROLE):1}   via not(ROLE) (8.17e-03, rho=1.72e-01 k*=10)
    - 3.86e-03 -> poly {Swerve:0.6, X:0.3, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.08e-03 -> poly {Swerve:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.08e-03, rho=3.32e-01 k*=3)
    - 7.96e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.96e-04, rho=1.27e-01 k*=10)
- mono {or(X,ROLE):1}
    - 3.51e-02 -> mono {ROLE:1}   via ROLE (3.51e-02, rho=1.84e-01 k*=10)
    - 1.10e-02 -> mono {Swerve:1}   via Swerve (1.10e-02, rho=4.43e-02 k*=10)
    - 7.62e-03 -> mono {X:1}   via X (7.62e-03, rho=3.29e-02 k*=10)
    - 2.52e-03 -> mono {not(ROLE):1}   via not(ROLE) (2.52e-03, rho=5.31e-02 k*=10)
    - 2.15e-04 -> mono {or(X,X):1}   via or(X,X) (2.15e-04, rho=5.57e-02 k*=10)
    - 1.09e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (1.09e-04, rho=4.98e-02 k*=10)
- poly {Straight:0.1, Swerve:0.7, X:0.1, and(X,X):0.1}
    - 3.17e-02 -> mono {ROLE:1}   via ROLE (3.17e-02, rho=1.66e-01 k*=10)
    - 7.90e-03 -> mono {not(ROLE):1}   via not(ROLE) (7.90e-03, rho=1.66e-01 k*=10)
    - 3.86e-03 -> poly {Swerve:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.00e-03 -> poly {Swerve:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.00e-03, rho=3.20e-01 k*=3)
    - 7.92e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.92e-04, rho=1.26e-01 k*=10)
    - 5.62e-04 -> poly {Swerve:0.7, not(or(X,ROLE)):0.3}   via not(or(X,ROLE)) (5.62e-04, rho=3.20e-01 k*=3)
- poly {Swerve:0.7, X:0.3}
    - 2.49e-01 -> poly {Straight:0.1, Swerve:0.7, X:0.2}   via Straight (2.49e-01, rho=1.00e+00 k*=1)
    - 3.58e-02 -> mono {ROLE:1}   via ROLE (3.58e-02, rho=1.88e-01 k*=10)
    - 8.92e-03 -> mono {not(ROLE):1}   via not(ROLE) (8.92e-03, rho=1.88e-01 k*=10)
    - 6.55e-03 -> poly {Swerve:0.6, X:0.4}   via THEM(ME) (2.18e-03, rho=1.00e+00 k*=1), THEM(THEM) (2.18e-03, rho=1.00e+00 k*=1), THEM(^Straight) (4.39e-04, rho=1.00e+00 k*=1), THEM(^Swerve) (4.39e-04, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {Swerve:0.6, X:0.3, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {Swerve:0.7, X:0.2, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
- poly {Swerve:0.7, and(X,ROLE):0.3}
    - 3.60e-02 -> mono {ROLE:1}   via ROLE (3.60e-02, rho=1.89e-01 k*=10)
    - 1.42e-02 -> mono {X:1}   via X (1.42e-02, rho=6.13e-02 k*=10)
    - 6.39e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.39e-03, rho=1.34e-01 k*=10)
    - 8.24e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (8.24e-04, rho=1.32e-01 k*=10)
    - 5.24e-04 -> poly {Swerve:0.7, not(or(X,ROLE)):0.3}   via not(or(X,ROLE)) (5.24e-04, rho=2.98e-01 k*=3)
    - 3.65e-04 -> mono {or(X,X):1}   via or(X,X) (3.65e-04, rho=9.46e-02 k*=10)
