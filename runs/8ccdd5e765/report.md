### arm=weak, n=5, game=chicken_norole, N=10, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 450, classes 30, states 482, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 2.19e-03
mean payoff -0.2406, efficient 0.5000, deadweight loss 0.7406, mean bits in support 9.16

| pi | state |
|---|---|
| 0.2184 | poly {Straight:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.5, not(THEM(^Straight)):0.1, or(THEM(ME),Swerve):0.1} |
| 0.1660 | poly {Straight:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.6, or(THEM(ME),Swerve):0.1} |
| 0.1109 | poly {Straight:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.7} |
| 0.0719 | poly {Straight:0.2, not(THEM(ME)):0.7, not(THEM(THEM)):0.1} |
| 0.0647 | poly {Straight:0.2, not(THEM(ME)):0.5, not(THEM(THEM)):0.1, not(THEM(^Straight)):0.1, or(THEM(ME),Swerve):0.1} |
| 0.0483 | poly {Straight:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.6, not(THEM(^Straight)):0.1} |
| 0.0455 | poly {Straight:0.2, not(THEM(THEM)):0.8} |
| 0.0418 | poly {Swerve:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1} |
| 0.0373 | poly {Straight:0.2, not(THEM(ME)):0.6, not(THEM(THEM)):0.1, or(THEM(ME),Swerve):0.1} |
| 0.0355 | poly {Straight:0.2, not(THEM(ME)):0.8} |
| 0.0331 | poly {Straight:0.2, not(THEM(ME)):0.7, or(THEM(ME),Swerve):0.1} |
| 0.0248 | poly {Straight:0.2, not(THEM(ME)):0.6, not(THEM(THEM)):0.1, not(THEM(^Straight)):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {Straight:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.5, not(THEM(^Straight)):0.1, or(THEM(ME),Swerve):0.1}
    - 7.65e-04 -> poly {Straight:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.4, not(THEM(^Straight)):0.2, or(THEM(ME),Swerve):0.1}   via THEM(^Swerve) (7.65e-04, rho=1.00e+00 k*=1)
    - 5.17e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (5.17e-05, rho=1.40e-02 k*=10)
    - 2.40e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.40e-05, rho=6.53e-03 k*=10)
    - 1.25e-05 -> mono {X:1}   via X (1.25e-05, rho=3.97e-05 k*=10)
    - 1.18e-06 -> mono {or(THEM(ME),X):1}   via or(THEM(ME),X) (1.18e-06, rho=1.55e-02 k*=10)
    - 1.15e-06 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (1.15e-06, rho=1.51e-02 k*=10)
- poly {Straight:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.6, or(THEM(ME),Swerve):0.1}
    - 7.61e-05 -> poly {Straight:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.5, not(THEM(^Straight)):0.1, or(THEM(ME),Swerve):0.1}   via not(THEM(^Straight)) (7.61e-05, rho=1.00e+00 k*=1)
    - 2.20e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.20e-05, rho=5.99e-03 k*=10)
    - 2.20e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.20e-05, rho=5.99e-03 k*=10)
    - 1.12e-05 -> mono {X:1}   via X (1.12e-05, rho=3.54e-05 k*=10)
    - 1.57e-06 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (1.57e-06, rho=2.07e-02 k*=10)
    - 1.57e-06 -> mono {or(THEM(ME),X):1}   via or(THEM(ME),X) (1.57e-06, rho=2.07e-02 k*=10)
- poly {Straight:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.7}
    - 1.52e-04 -> poly {Straight:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.6, or(THEM(ME),Swerve):0.1}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 7.61e-05 -> poly {Straight:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.6, not(THEM(^Straight)):0.1}   via not(THEM(^Straight)) (7.61e-05, rho=1.00e+00 k*=1)
    - 2.20e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.20e-05, rho=5.99e-03 k*=10)
    - 2.20e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.20e-05, rho=5.99e-03 k*=10)
    - 4.53e-06 -> mono {X:1}   via X (4.53e-06, rho=1.44e-05 k*=10)
    - 1.57e-06 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (1.57e-06, rho=2.07e-02 k*=10)
- poly {Straight:0.2, not(THEM(ME)):0.7, not(THEM(THEM)):0.1}
    - 1.52e-04 -> poly {Straight:0.2, not(THEM(ME)):0.6, not(THEM(THEM)):0.1, or(THEM(ME),Swerve):0.1}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 7.61e-05 -> poly {Straight:0.2, not(THEM(ME)):0.6, not(THEM(THEM)):0.1, not(THEM(^Straight)):0.1}   via not(THEM(^Straight)) (7.61e-05, rho=1.00e+00 k*=1)
    - 5.72e-05 -> mono {THEM(^Swerve):1}   via THEM(^Swerve) (5.72e-05, rho=7.48e-02 k*=10)
    - 2.20e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.20e-05, rho=5.99e-03 k*=10)
    - 2.20e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.20e-05, rho=5.99e-03 k*=10)
    - 4.53e-06 -> mono {X:1}   via X (4.53e-06, rho=1.44e-05 k*=10)
- poly {Straight:0.2, not(THEM(ME)):0.5, not(THEM(THEM)):0.1, not(THEM(^Straight)):0.1, or(THEM(ME),Swerve):0.1}
    - 5.17e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (5.17e-05, rho=1.40e-02 k*=10)
    - 3.34e-05 -> mono {THEM(^Swerve):1}   via THEM(^Swerve) (3.34e-05, rho=4.87e-02 k*=9)
    - 2.40e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.40e-05, rho=6.53e-03 k*=10)
    - 1.25e-05 -> mono {X:1}   via X (1.25e-05, rho=3.97e-05 k*=10)
    - 3.88e-06 -> mono {or(THEM(ME),Swerve):1}   via THEM(^Swerve) (3.88e-06, rho=4.87e-02 k*=9)
    - 1.18e-06 -> mono {or(THEM(ME),X):1}   via or(THEM(ME),X) (1.18e-06, rho=1.55e-02 k*=10)
- poly {Straight:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.6, not(THEM(^Straight)):0.1}
    - 1.52e-04 -> poly {Straight:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.5, not(THEM(^Straight)):0.1, or(THEM(ME),Swerve):0.1}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 5.17e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (5.17e-05, rho=1.40e-02 k*=10)
    - 2.40e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.40e-05, rho=6.53e-03 k*=10)
    - 5.08e-06 -> mono {X:1}   via X (5.08e-06, rho=1.61e-05 k*=10)
    - 1.18e-06 -> mono {or(THEM(ME),X):1}   via or(THEM(ME),X) (1.18e-06, rho=1.55e-02 k*=10)
    - 1.15e-06 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (1.15e-06, rho=1.51e-02 k*=10)
- poly {Straight:0.2, not(THEM(THEM)):0.8}
    - 6.89e-04 -> poly {Straight:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.7}   via not(THEM(ME)) (6.89e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Straight:0.2, not(THEM(THEM)):0.7, or(THEM(ME),Swerve):0.1}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 7.61e-05 -> poly {Straight:0.2, not(THEM(THEM)):0.7, not(THEM(^Straight)):0.1}   via not(THEM(^Straight)) (7.61e-05, rho=1.00e+00 k*=1)
    - 2.20e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.20e-05, rho=5.99e-03 k*=10)
    - 2.20e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.20e-05, rho=5.99e-03 k*=10)
    - 4.53e-06 -> mono {X:1}   via X (4.53e-06, rho=1.44e-05 k*=10)
- poly {Swerve:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}
    - 8.13e-03 -> poly {Swerve:0.6, X:0.2, and(X,X):0.1, or(X,X):0.1}   via THEM(ME) (3.68e-03, rho=1.00e+00 k*=1), THEM(THEM) (3.68e-03, rho=1.00e+00 k*=1), THEM(^Swerve) (7.65e-04, rho=1.00e+00 k*=1)
    - 4.60e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (4.60e-04, rho=6.68e-01 k*=10)
    - 4.60e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (4.60e-04, rho=6.68e-01 k*=10)
    - 1.52e-04 -> poly {Swerve:0.7, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Swerve):0.1}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Straight:0.2, not(THEM(ME)):0.6, not(THEM(THEM)):0.1, or(THEM(ME),Swerve):0.1}
    - 7.65e-04 -> poly {Straight:0.2, not(THEM(ME)):0.7, or(THEM(ME),Swerve):0.1}   via THEM(^Swerve) (7.65e-04, rho=1.00e+00 k*=1)
    - 7.61e-05 -> poly {Straight:0.2, not(THEM(ME)):0.5, not(THEM(THEM)):0.1, not(THEM(^Straight)):0.1, or(THEM(ME),Swerve):0.1}   via not(THEM(^Straight)) (7.61e-05, rho=1.00e+00 k*=1)
    - 2.20e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.20e-05, rho=5.99e-03 k*=10)
    - 2.20e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.20e-05, rho=5.99e-03 k*=10)
    - 1.12e-05 -> mono {X:1}   via X (1.12e-05, rho=3.54e-05 k*=10)
    - 1.57e-06 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (1.57e-06, rho=2.07e-02 k*=10)
- poly {Straight:0.2, not(THEM(ME)):0.8}
    - 6.89e-04 -> poly {Straight:0.2, not(THEM(ME)):0.7, not(THEM(THEM)):0.1}   via not(THEM(THEM)) (6.89e-04, rho=1.00e+00 k*=1)
    - 2.72e-04 -> mono {THEM(^Swerve):1}   via THEM(^Swerve) (2.72e-04, rho=3.56e-01 k*=10)
    - 1.52e-04 -> poly {Straight:0.2, not(THEM(ME)):0.7, or(THEM(ME),Swerve):0.1}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 7.61e-05 -> poly {Straight:0.2, not(THEM(ME)):0.7, not(THEM(^Straight)):0.1}   via not(THEM(^Straight)) (7.61e-05, rho=1.00e+00 k*=1)
    - 2.20e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.20e-05, rho=5.99e-03 k*=10)
    - 2.20e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.20e-05, rho=5.99e-03 k*=10)
- poly {Straight:0.2, not(THEM(ME)):0.7, or(THEM(ME),Swerve):0.1}
    - 6.89e-04 -> poly {Straight:0.2, not(THEM(ME)):0.6, not(THEM(THEM)):0.1, or(THEM(ME),Swerve):0.1}   via not(THEM(THEM)) (6.89e-04, rho=1.00e+00 k*=1)
    - 1.94e-04 -> mono {THEM(^Swerve):1}   via THEM(^Swerve) (1.94e-04, rho=2.74e-01 k*=9)
    - 7.61e-05 -> poly {Straight:0.2, not(THEM(ME)):0.6, not(THEM(^Straight)):0.1, or(THEM(ME),Swerve):0.1}   via not(THEM(^Straight)) (7.61e-05, rho=1.00e+00 k*=1)
    - 2.20e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.20e-05, rho=5.99e-03 k*=10)
    - 2.20e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.20e-05, rho=5.99e-03 k*=10)
    - 1.57e-05 -> mono {or(THEM(ME),Swerve):1}   via THEM(^Swerve) (1.57e-05, rho=2.74e-01 k*=9)
- poly {Straight:0.2, not(THEM(ME)):0.6, not(THEM(THEM)):0.1, not(THEM(^Straight)):0.1}
    - 1.52e-04 -> poly {Straight:0.2, not(THEM(ME)):0.5, not(THEM(THEM)):0.1, not(THEM(^Straight)):0.1, or(THEM(ME),Swerve):0.1}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 6.03e-05 -> mono {THEM(^Swerve):1}   via THEM(^Swerve) (6.03e-05, rho=7.89e-02 k*=10)
    - 5.17e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (5.17e-05, rho=1.40e-02 k*=10)
    - 2.40e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.40e-05, rho=6.53e-03 k*=10)
    - 5.08e-06 -> mono {X:1}   via X (5.08e-06, rho=1.61e-05 k*=10)
    - 1.18e-06 -> mono {or(THEM(ME),X):1}   via or(THEM(ME),X) (1.18e-06, rho=1.55e-02 k*=10)
