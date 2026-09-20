### arm=weak, n=5, game=chicken_norole, N=100, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 450, classes 30, states 841, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 1.57e-04
mean payoff -0.2412, efficient 0.5000, deadweight loss 0.7412, mean bits in support 9.22

| pi | state |
|---|---|
| 0.3489 | poly {Straight:0.18, not(THEM(ME)):0.01, not(THEM(THEM)):0.8, or(THEM(ME),Swerve):0.01} |
| 0.3487 | poly {Straight:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.64, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.01} |
| 0.1141 | poly {Straight:0.18, not(THEM(ME)):0.8, not(THEM(THEM)):0.01, or(THEM(ME),Swerve):0.01} |
| 0.0295 | poly {Straight:0.19, not(THEM(ME)):0.64, not(THEM(THEM)):0.01, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.01} |
| 0.0165 | poly {Straight:0.18, not(THEM(ME)):0.01, not(THEM(THEM)):0.81} |
| 0.0146 | poly {Straight:0.18, not(THEM(ME)):0.81, not(THEM(THEM)):0.01} |
| 0.0102 | poly {Straight:0.22, Swerve:0.26, not(THEM(^X)):0.48, or(THEM(ME),Swerve):0.04} |
| 0.0080 | poly {Straight:0.17, Swerve:0.8, X:0.01, and(X,X):0.01, or(X,X):0.01} |
| 0.0040 | poly {Straight:0.18, not(THEM(THEM)):0.82} |
| 0.0039 | poly {Straight:0.18, not(THEM(ME)):0.82} |
| 0.0039 | poly {Straight:0.18, not(THEM(THEM)):0.81, or(THEM(ME),Swerve):0.01} |
| 0.0038 | mono {and(THEM(THEM),Straight):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {Straight:0.18, not(THEM(ME)):0.01, not(THEM(THEM)):0.8, or(THEM(ME),Swerve):0.01}
    - 1.04e-05 -> poly {Straight:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.64, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.01}   via not(THEM(^Straight)) (1.04e-05, rho=1.37e-01 k*=15)
    - 1.91e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (1.91e-06, rho=5.19e-04 k*=100)
    - 1.91e-06 -> mono {THEM(ME):1}   via THEM(ME) (1.91e-06, rho=5.19e-04 k*=100)
    - 1.47e-07 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (1.47e-07, rho=1.93e-03 k*=100)
    - 1.47e-07 -> mono {or(THEM(ME),X):1}   via or(THEM(ME),X) (1.47e-07, rho=1.93e-03 k*=100)
    - 8.71e-08 -> mono {X:1}   via X (8.71e-08, rho=2.76e-07 k*=100)
- poly {Straight:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.64, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.01}
    - 7.87e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (7.87e-06, rho=2.14e-03 k*=100)
    - 2.60e-06 -> mono {THEM(ME):1}   via THEM(ME) (2.60e-06, rho=7.07e-04 k*=100)
    - 1.64e-07 -> mono {X:1}   via X (1.64e-07, rho=5.19e-07 k*=100)
    - 1.63e-07 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (1.63e-07, rho=2.14e-03 k*=100)
    - 1.63e-07 -> mono {and(THEM(THEM),Straight):1}   via and(THEM(THEM),Straight) (1.63e-07, rho=2.14e-03 k*=100)
    - 1.63e-07 -> mono {and(THEM(ME),Straight):1}   via and(THEM(ME),Straight) (1.63e-07, rho=2.14e-03 k*=100)
- poly {Straight:0.18, not(THEM(ME)):0.8, not(THEM(THEM)):0.01, or(THEM(ME),Swerve):0.01}
    - 2.66e-05 -> mono {THEM(^Swerve):1}   via THEM(^Swerve) (2.66e-05, rho=3.51e-02 k*=99)
    - 1.04e-05 -> poly {Straight:0.19, not(THEM(ME)):0.64, not(THEM(THEM)):0.01, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.01}   via not(THEM(^Straight)) (1.04e-05, rho=1.37e-01 k*=15)
    - 1.91e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (1.91e-06, rho=5.19e-04 k*=100)
    - 1.91e-06 -> mono {THEM(ME):1}   via THEM(ME) (1.91e-06, rho=5.19e-04 k*=100)
    - 2.85e-07 -> mono {or(THEM(ME),Swerve):1}   via THEM(^Swerve) (2.85e-07, rho=3.51e-02 k*=99)
    - 1.47e-07 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (1.47e-07, rho=1.93e-03 k*=100)
- poly {Straight:0.19, not(THEM(ME)):0.64, not(THEM(THEM)):0.01, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.01}
    - 2.84e-05 -> mono {THEM(^Swerve):1}   via THEM(^Swerve) (2.84e-05, rho=3.75e-02 k*=99)
    - 7.87e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (7.87e-06, rho=2.14e-03 k*=100)
    - 2.60e-06 -> mono {THEM(ME):1}   via THEM(ME) (2.60e-06, rho=7.07e-04 k*=100)
    - 2.82e-07 -> mono {or(THEM(ME),Swerve):1}   via THEM(^Swerve) (2.82e-07, rho=3.75e-02 k*=99)
    - 1.64e-07 -> mono {X:1}   via X (1.64e-07, rho=5.19e-07 k*=100)
    - 1.63e-07 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (1.63e-07, rho=2.14e-03 k*=100)
- poly {Straight:0.18, not(THEM(ME)):0.01, not(THEM(THEM)):0.81}
    - 1.52e-04 -> poly {Straight:0.18, not(THEM(ME)):0.01, not(THEM(THEM)):0.8, or(THEM(ME),Swerve):0.01}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.04e-05 -> poly {Straight:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.65, not(THEM(^Straight)):0.15}   via not(THEM(^Straight)) (1.04e-05, rho=1.37e-01 k*=15)
    - 1.91e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (1.91e-06, rho=5.19e-04 k*=100)
    - 1.91e-06 -> mono {THEM(ME):1}   via THEM(ME) (1.91e-06, rho=5.19e-04 k*=100)
    - 1.47e-07 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (1.47e-07, rho=1.93e-03 k*=100)
    - 1.47e-07 -> mono {or(THEM(ME),X):1}   via or(THEM(ME),X) (1.47e-07, rho=1.93e-03 k*=100)
- poly {Straight:0.18, not(THEM(ME)):0.81, not(THEM(THEM)):0.01}
    - 1.52e-04 -> poly {Straight:0.18, not(THEM(ME)):0.8, not(THEM(THEM)):0.01, or(THEM(ME),Swerve):0.01}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 2.77e-05 -> mono {THEM(^Swerve):1}   via THEM(^Swerve) (2.77e-05, rho=3.62e-02 k*=100)
    - 1.04e-05 -> poly {Straight:0.19, not(THEM(ME)):0.65, not(THEM(THEM)):0.01, not(THEM(^Straight)):0.15}   via not(THEM(^Straight)) (1.04e-05, rho=1.37e-01 k*=15)
    - 1.91e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (1.91e-06, rho=5.19e-04 k*=100)
    - 1.91e-06 -> mono {THEM(ME):1}   via THEM(ME) (1.91e-06, rho=5.19e-04 k*=100)
    - 1.47e-07 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (1.47e-07, rho=1.93e-03 k*=100)
- poly {Straight:0.22, Swerve:0.26, not(THEM(^X)):0.48, or(THEM(ME),Swerve):0.04}
    - 1.38e-03 -> poly {Straight:0.23, Swerve:0.25, not(THEM(^X)):0.48, or(THEM(ME),Swerve):0.04}   via not(THEM(ME)) (6.89e-04, rho=1.00e+00 k*=1), not(THEM(THEM)) (6.89e-04, rho=1.00e+00 k*=1)
    - 9.63e-06 -> mono {X:1}   via X (9.63e-06, rho=3.06e-05 k*=100)
    - 4.88e-06 -> poly {Straight:0.2, not(THEM(^Swerve)):0.51, not(THEM(^X)):0.29}   via not(THEM(^Swerve)) (4.88e-06, rho=6.42e-02 k*=51)
    - 3.04e-06 -> mono {and(THEM(THEM),Straight):1}   via and(THEM(THEM),Straight) (3.04e-06, rho=4.12e-02 k*=97)
    - 3.04e-06 -> mono {and(THEM(ME),Straight):1}   via and(THEM(ME),Straight) (3.04e-06, rho=4.12e-02 k*=97)
    - 2.39e-06 -> mono {or(X,X):1}   via or(X,X) (2.39e-06, rho=3.55e-04 k*=100)
- poly {Straight:0.17, Swerve:0.8, X:0.01, and(X,X):0.01, or(X,X):0.01}
    - 1.52e-04 -> poly {Straight:0.17, Swerve:0.79, X:0.01, and(X,X):0.01, or(X,X):0.01, or(THEM(ME),Swerve):0.01}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Straight:0.17, Swerve:0.79, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,or(X,X)):0.01}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Straight:0.16, Swerve:0.8, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,or(X,X)):0.01}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Straight:0.16, Swerve:0.8, X:0.01, and(X,X):0.01, or(X,X):0.01, or(X,and(X,X)):0.01}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Straight:0.16, Swerve:0.8, X:0.01, and(X,X):0.01, or(X,X):0.01, and(X,and(X,X)):0.01}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 9.60e-05 -> poly {Straight:0.18, not(THEM(THEM)):0.82}   via not(THEM(THEM)) (9.60e-05, rho=1.39e-01 k*=82)
- poly {Straight:0.18, not(THEM(THEM)):0.82}
    - 6.89e-04 -> poly {Straight:0.18, not(THEM(ME)):0.01, not(THEM(THEM)):0.81}   via not(THEM(ME)) (6.89e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Straight:0.18, not(THEM(THEM)):0.81, or(THEM(ME),Swerve):0.01}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.04e-05 -> poly {Straight:0.19, not(THEM(THEM)):0.66, not(THEM(^Straight)):0.15}   via not(THEM(^Straight)) (1.04e-05, rho=1.37e-01 k*=15)
    - 1.91e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (1.91e-06, rho=5.19e-04 k*=100)
    - 1.91e-06 -> mono {THEM(ME):1}   via THEM(ME) (1.91e-06, rho=5.19e-04 k*=100)
    - 1.47e-07 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (1.47e-07, rho=1.93e-03 k*=100)
- poly {Straight:0.18, not(THEM(ME)):0.82}
    - 6.89e-04 -> poly {Straight:0.18, not(THEM(ME)):0.81, not(THEM(THEM)):0.01}   via not(THEM(THEM)) (6.89e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Straight:0.18, not(THEM(ME)):0.81, or(THEM(ME),Swerve):0.01}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 3.20e-05 -> mono {THEM(^Swerve):1}   via THEM(^Swerve) (3.20e-05, rho=4.18e-02 k*=100)
    - 1.04e-05 -> poly {Straight:0.19, not(THEM(ME)):0.66, not(THEM(^Straight)):0.15}   via not(THEM(^Straight)) (1.04e-05, rho=1.37e-01 k*=15)
    - 1.91e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (1.91e-06, rho=5.19e-04 k*=100)
    - 1.91e-06 -> mono {THEM(ME):1}   via THEM(ME) (1.91e-06, rho=5.19e-04 k*=100)
- poly {Straight:0.18, not(THEM(THEM)):0.81, or(THEM(ME),Swerve):0.01}
    - 6.89e-04 -> poly {Straight:0.18, not(THEM(ME)):0.01, not(THEM(THEM)):0.8, or(THEM(ME),Swerve):0.01}   via not(THEM(ME)) (6.89e-04, rho=1.00e+00 k*=1)
    - 1.04e-05 -> poly {Straight:0.19, not(THEM(THEM)):0.65, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.01}   via not(THEM(^Straight)) (1.04e-05, rho=1.37e-01 k*=15)
    - 1.91e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (1.91e-06, rho=5.19e-04 k*=100)
    - 1.91e-06 -> mono {THEM(ME):1}   via THEM(ME) (1.91e-06, rho=5.19e-04 k*=100)
    - 1.47e-07 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (1.47e-07, rho=1.93e-03 k*=100)
    - 1.47e-07 -> mono {or(THEM(ME),X):1}   via or(THEM(ME),X) (1.47e-07, rho=1.93e-03 k*=100)
- mono {and(THEM(THEM),Straight):1}
    - 3.68e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.68e-05, rho=1.00e-02 k*=100)
    - 3.68e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-05, rho=1.00e-02 k*=100)
    - 6.89e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (6.89e-06, rho=1.00e-02 k*=100)
    - 6.89e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (6.89e-06, rho=1.00e-02 k*=100)
    - 1.52e-06 -> mono {or(THEM(ME),Swerve):1}   via or(THEM(ME),Swerve) (1.52e-06, rho=1.00e-02 k*=100)
    - 7.61e-07 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (7.61e-07, rho=1.00e-02 k*=100)
