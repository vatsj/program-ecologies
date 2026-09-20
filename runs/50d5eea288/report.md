### arm=weak, n=5, game=chicken, N=10, w=0.1, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 53, states 608, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 3.02e-02
mean payoff -0.0521, efficient 0.5000, deadweight loss 0.5521, mean bits in support 3.49

| pi | state |
|---|---|
| 0.4130 | mono {ROLE:1} |
| 0.1039 | poly {Straight:0.1, Swerve:0.8, X:0.1} |
| 0.1029 | mono {not(ROLE):1} |
| 0.1013 | poly {Straight:0.1, Swerve:0.7, X:0.2} |
| 0.0703 | mono {X:1} |
| 0.0326 | mono {Swerve:1} |
| 0.0261 | poly {Straight:0.1, Swerve:0.7, X:0.1, and(X,X):0.1} |
| 0.0204 | poly {Swerve:0.6, X:0.4} |
| 0.0196 | poly {Straight:0.2, Swerve:0.8} |
| 0.0173 | poly {Swerve:0.7, X:0.3} |
| 0.0143 | poly {Swerve:0.7, and(X,ROLE):0.3} |
| 0.0135 | poly {Straight:0.1, Swerve:0.6, X:0.2, or(X,X):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 1.48e-02 -> mono {Swerve:1}   via Swerve (1.48e-02, rho=5.94e-02 k*=10)
    - 1.05e-02 -> mono {X:1}   via X (1.05e-02, rho=4.52e-02 k*=10)
    - 2.57e-03 -> mono {Straight:1}   via Straight (2.57e-03, rho=1.03e-02 k*=10)
    - 2.09e-03 -> mono {not(ROLE):1}   via not(ROLE) (2.09e-03, rho=4.39e-02 k*=10)
    - 4.88e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (4.88e-04, rho=7.80e-02 k*=10)
    - 2.28e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.28e-04, rho=3.64e-02 k*=10)
- poly {Straight:0.1, Swerve:0.8, X:0.1}
    - 2.47e-02 -> mono {ROLE:1}   via ROLE (2.47e-02, rho=1.30e-01 k*=10)
    - 6.15e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.15e-03, rho=1.30e-01 k*=10)
    - 3.86e-03 -> poly {Straight:0.1, Swerve:0.7, X:0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {Straight:0.1, Swerve:0.7, X:0.1, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.14e-03 -> poly {Swerve:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.14e-03, rho=3.42e-01 k*=3)
    - 6.93e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.93e-04, rho=1.11e-01 k*=10)
- mono {not(ROLE):1}
    - 1.48e-02 -> mono {Swerve:1}   via Swerve (1.48e-02, rho=5.94e-02 k*=10)
    - 1.05e-02 -> mono {X:1}   via X (1.05e-02, rho=4.52e-02 k*=10)
    - 8.37e-03 -> mono {ROLE:1}   via ROLE (8.37e-03, rho=4.39e-02 k*=10)
    - 2.57e-03 -> mono {Straight:1}   via Straight (2.57e-03, rho=1.03e-02 k*=10)
    - 3.31e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (3.31e-04, rho=5.29e-02 k*=10)
    - 2.25e-04 -> mono {or(X,X):1}   via or(X,X) (2.25e-04, rho=5.81e-02 k*=10)
- poly {Straight:0.1, Swerve:0.7, X:0.2}
    - 2.39e-02 -> mono {ROLE:1}   via ROLE (2.39e-02, rho=1.25e-01 k*=10)
    - 5.96e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.96e-03, rho=1.25e-01 k*=10)
    - 3.86e-03 -> poly {Straight:0.1, Swerve:0.6, X:0.2, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {Straight:0.1, Swerve:0.7, X:0.1, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.08e-03 -> poly {Swerve:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.08e-03, rho=3.33e-01 k*=3)
    - 6.83e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.83e-04, rho=1.09e-01 k*=10)
- mono {X:1}
    - 5.25e-02 -> poly {Swerve:0.6, X:0.4}   via Swerve (5.25e-02, rho=2.11e-01 k*=6)
    - 2.58e-02 -> mono {ROLE:1}   via ROLE (2.58e-02, rho=1.36e-01 k*=10)
    - 6.86e-03 -> mono {Straight:1}   via Straight (6.86e-03, rho=2.76e-02 k*=10)
    - 6.45e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.45e-03, rho=1.36e-01 k*=10)
    - 8.39e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (8.39e-04, rho=1.34e-01 k*=10)
    - 4.78e-04 -> mono {or(X,X):1}   via or(X,X) (4.78e-04, rho=1.24e-01 k*=10)
- mono {Swerve:1}
    - 1.38e-01 -> poly {Straight:0.2, Swerve:0.8}   via Straight (1.38e-01, rho=5.53e-01 k*=2)
    - 6.55e-02 -> poly {Swerve:0.6, X:0.4}   via X (6.55e-02, rho=2.83e-01 k*=4)
    - 2.93e-02 -> mono {ROLE:1}   via ROLE (2.93e-02, rho=1.54e-01 k*=10)
    - 7.30e-03 -> mono {not(ROLE):1}   via not(ROLE) (7.30e-03, rho=1.54e-01 k*=10)
    - 2.38e-03 -> poly {Swerve:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.38e-03, rho=3.81e-01 k*=3)
    - 2.08e-03 -> poly {Swerve:0.8, and(X,X):0.2}   via and(X,X) (2.08e-03, rho=5.40e-01 k*=2)
- poly {Straight:0.1, Swerve:0.7, X:0.1, and(X,X):0.1}
    - 2.36e-02 -> mono {ROLE:1}   via ROLE (2.36e-02, rho=1.24e-01 k*=10)
    - 5.89e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.89e-03, rho=1.24e-01 k*=10)
    - 3.86e-03 -> poly {Swerve:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.06e-03 -> poly {Swerve:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.06e-03, rho=3.29e-01 k*=3)
    - 6.82e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.82e-04, rho=1.09e-01 k*=10)
    - 5.78e-04 -> poly {Swerve:0.7, not(or(X,ROLE)):0.3}   via not(or(X,ROLE)) (5.78e-04, rho=3.29e-01 k*=3)
- poly {Swerve:0.6, X:0.4}
    - 2.53e-01 -> poly {Swerve:0.7, X:0.3}   via Straight (2.49e-01, rho=1.00e+00 k*=1), and(X,X) (3.86e-03, rho=1.00e+00 k*=1), and(X,and(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
    - 2.39e-02 -> mono {ROLE:1}   via ROLE (2.39e-02, rho=1.25e-01 k*=10)
    - 5.96e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.96e-03, rho=1.25e-01 k*=10)
    - 3.86e-03 -> poly {Swerve:0.6, X:0.3, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.08e-03 -> poly {Swerve:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.08e-03, rho=3.33e-01 k*=3)
    - 6.83e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.83e-04, rho=1.09e-01 k*=10)
- poly {Straight:0.2, Swerve:0.8}
    - 2.31e-01 -> poly {Straight:0.1, Swerve:0.8, X:0.1}   via X (2.31e-01, rho=1.00e+00 k*=1)
    - 2.39e-02 -> mono {ROLE:1}   via ROLE (2.39e-02, rho=1.25e-01 k*=10)
    - 5.96e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.96e-03, rho=1.25e-01 k*=10)
    - 3.86e-03 -> poly {Straight:0.2, Swerve:0.7, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {Straight:0.1, Swerve:0.8, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.08e-03 -> poly {Swerve:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.08e-03, rho=3.33e-01 k*=3)
- poly {Swerve:0.7, X:0.3}
    - 2.49e-01 -> poly {Straight:0.1, Swerve:0.7, X:0.2}   via Straight (2.49e-01, rho=1.00e+00 k*=1)
    - 2.47e-02 -> mono {ROLE:1}   via ROLE (2.47e-02, rho=1.30e-01 k*=10)
    - 6.55e-03 -> poly {Swerve:0.6, X:0.4}   via THEM(ME) (2.18e-03, rho=1.00e+00 k*=1), THEM(THEM) (2.18e-03, rho=1.00e+00 k*=1), THEM(^Straight) (4.39e-04, rho=1.00e+00 k*=1), THEM(^Swerve) (4.39e-04, rho=1.00e+00 k*=1)
    - 6.15e-03 -> mono {not(ROLE):1}   via not(ROLE) (6.15e-03, rho=1.30e-01 k*=10)
    - 3.86e-03 -> poly {Swerve:0.6, X:0.3, or(X,X):0.1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {Swerve:0.7, X:0.2, and(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
- poly {Swerve:0.7, and(X,ROLE):0.3}
    - 2.46e-02 -> mono {ROLE:1}   via ROLE (2.46e-02, rho=1.29e-01 k*=10)
    - 2.00e-02 -> mono {X:1}   via X (2.00e-02, rho=8.64e-02 k*=10)
    - 6.19e-03 -> mono {Straight:1}   via Straight (6.19e-03, rho=2.48e-02 k*=10)
    - 5.48e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.48e-03, rho=1.15e-01 k*=10)
    - 6.90e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.90e-04, rho=1.10e-01 k*=10)
    - 5.65e-04 -> poly {Swerve:0.7, not(or(X,ROLE)):0.3}   via not(or(X,ROLE)) (5.65e-04, rho=3.22e-01 k*=3)
- poly {Straight:0.1, Swerve:0.6, X:0.2, or(X,X):0.1}
    - 2.36e-02 -> mono {ROLE:1}   via ROLE (2.36e-02, rho=1.24e-01 k*=10)
    - 5.89e-03 -> mono {not(ROLE):1}   via not(ROLE) (5.89e-03, rho=1.24e-01 k*=10)
    - 3.86e-03 -> poly {Swerve:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 2.06e-03 -> poly {Swerve:0.7, and(X,ROLE):0.3}   via and(X,ROLE) (2.06e-03, rho=3.29e-01 k*=3)
    - 6.82e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.82e-04, rho=1.09e-01 k*=10)
    - 5.78e-04 -> poly {Swerve:0.7, not(or(X,ROLE)):0.3}   via not(or(X,ROLE)) (5.78e-04, rho=3.29e-01 k*=3)
