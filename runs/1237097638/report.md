### arm=weak, n=5, game=chicken_norole, N=10, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 450, classes 30, states 523, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 1.50e-02
mean payoff -0.1508, efficient 0.5000, deadweight loss 0.6508, mean bits in support 4.72

| pi | state |
|---|---|
| 0.4070 | poly {Swerve:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1} |
| 0.0719 | poly {Swerve:0.7, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1} |
| 0.0564 | poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1} |
| 0.0559 | poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1} |
| 0.0471 | poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Swerve):0.1} |
| 0.0396 | poly {Straight:0.1, Swerve:0.7, X:0.1, and(X,X):0.1} |
| 0.0284 | poly {Straight:0.1, Swerve:0.7, X:0.2} |
| 0.0269 | poly {Straight:0.2, not(THEM(THEM)):0.8} |
| 0.0262 | poly {Straight:0.2, not(THEM(ME)):0.8} |
| 0.0242 | poly {Straight:0.1, Swerve:0.6, X:0.2, or(X,X):0.1} |
| 0.0232 | poly {Straight:0.1, Swerve:0.7, X:0.1, or(X,X):0.1} |
| 0.0182 | poly {Straight:0.1, Swerve:0.8, X:0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {Swerve:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}
    - 8.13e-03 -> poly {Swerve:0.6, X:0.2, and(X,X):0.1, or(X,X):0.1}   via THEM(ME) (3.68e-03, rho=1.00e+00 k*=1), THEM(THEM) (3.68e-03, rho=1.00e+00 k*=1), THEM(^Swerve) (7.65e-04, rho=1.00e+00 k*=1)
    - 2.06e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (2.06e-04, rho=2.99e-01 k*=10)
    - 2.06e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (2.06e-04, rho=2.99e-01 k*=10)
    - 1.52e-04 -> poly {Swerve:0.7, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Swerve):0.1}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Swerve:0.7, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1}
    - 9.20e-03 -> poly {Swerve:0.6, X:0.2, or(X,X):0.1, and(X,or(X,X)):0.1}   via THEM(ME) (3.68e-03, rho=1.00e+00 k*=1), THEM(THEM) (3.68e-03, rho=1.00e+00 k*=1), THEM(^Swerve) (7.65e-04, rho=1.00e+00 k*=1), THEM(^X) (7.65e-04, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 9.17e-04 -> poly {Swerve:0.6, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.2}   via THEM(^Straight) (7.65e-04, rho=1.00e+00 k*=1), and(X,THEM(ME)) (7.61e-05, rho=1.00e+00 k*=1), and(X,THEM(THEM)) (7.61e-05, rho=1.00e+00 k*=1)
    - 2.06e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (2.06e-04, rho=2.99e-01 k*=10)
    - 2.06e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (2.06e-04, rho=2.99e-01 k*=10)
    - 1.52e-04 -> poly {Swerve:0.5, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.2, or(THEM(ME),Swerve):0.1}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1}
    - 2.91e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.91e-04, rho=7.91e-02 k*=10)
    - 2.91e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.91e-04, rho=7.91e-02 k*=10)
    - 1.83e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.83e-04, rho=2.65e-01 k*=10)
    - 1.83e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.83e-04, rho=2.65e-01 k*=10)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, or(X,X):0.1, or(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}
    - 2.89e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.89e-04, rho=7.85e-02 k*=10)
    - 2.89e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.89e-04, rho=7.85e-02 k*=10)
    - 1.96e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.96e-04, rho=2.84e-01 k*=10)
    - 1.96e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.96e-04, rho=2.84e-01 k*=10)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Swerve):0.1}
    - 2.83e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.83e-04, rho=7.68e-02 k*=10)
    - 2.83e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.83e-04, rho=7.68e-02 k*=10)
    - 1.66e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (1.66e-04, rho=2.68e-01 k*=9)
    - 1.66e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.66e-04, rho=2.68e-01 k*=9)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(THEM(ME),Swerve):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),Swerve):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Straight:0.1, Swerve:0.7, X:0.1, and(X,X):0.1}
    - 6.74e-03 -> poly {Swerve:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 2.20e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.20e-04, rho=5.96e-02 k*=10)
    - 2.20e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.20e-04, rho=5.96e-02 k*=10)
    - 2.17e-04 -> poly {Straight:0.2, not(THEM(THEM)):0.8}   via not(THEM(THEM)) (2.17e-04, rho=3.15e-01 k*=8)
    - 2.17e-04 -> poly {Straight:0.2, not(THEM(ME)):0.8}   via not(THEM(ME)) (2.17e-04, rho=3.15e-01 k*=8)
    - 1.52e-04 -> poly {Swerve:0.8, X:0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Straight:0.1, Swerve:0.7, X:0.2}
    - 6.74e-03 -> poly {Straight:0.1, Swerve:0.6, X:0.2, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {Straight:0.1, Swerve:0.7, X:0.1, and(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 2.37e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.37e-04, rho=6.44e-02 k*=10)
    - 2.37e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.37e-04, rho=6.44e-02 k*=10)
    - 2.14e-04 -> poly {Straight:0.2, not(THEM(THEM)):0.8}   via not(THEM(THEM)) (2.14e-04, rho=3.11e-01 k*=8)
    - 2.14e-04 -> poly {Straight:0.2, not(THEM(ME)):0.8}   via not(THEM(ME)) (2.14e-04, rho=3.11e-01 k*=8)
- poly {Straight:0.2, not(THEM(THEM)):0.8}
    - 2.91e-03 -> mono {X:1}   via X (2.91e-03, rho=9.24e-03 k*=10)
    - 2.16e-03 -> mono {Swerve:1}   via Swerve (2.16e-03, rho=6.54e-03 k*=10)
    - 6.89e-04 -> poly {Straight:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.7}   via not(THEM(ME)) (6.89e-04, rho=1.00e+00 k*=1)
    - 1.82e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (1.82e-04, rho=4.94e-02 k*=10)
    - 1.82e-04 -> mono {THEM(ME):1}   via THEM(ME) (1.82e-04, rho=4.94e-02 k*=10)
    - 1.52e-04 -> poly {Straight:0.2, not(THEM(THEM)):0.7, or(THEM(ME),Swerve):0.1}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Straight:0.2, not(THEM(ME)):0.8}
    - 2.91e-03 -> mono {X:1}   via X (2.91e-03, rho=9.24e-03 k*=10)
    - 2.16e-03 -> mono {Swerve:1}   via Swerve (2.16e-03, rho=6.54e-03 k*=10)
    - 6.89e-04 -> poly {Straight:0.2, not(THEM(ME)):0.7, not(THEM(THEM)):0.1}   via not(THEM(THEM)) (6.89e-04, rho=1.00e+00 k*=1)
    - 1.82e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (1.82e-04, rho=4.94e-02 k*=10)
    - 1.82e-04 -> mono {THEM(ME):1}   via THEM(ME) (1.82e-04, rho=4.94e-02 k*=10)
    - 1.66e-04 -> mono {THEM(^Swerve):1}   via THEM(^Swerve) (1.66e-04, rho=2.17e-01 k*=10)
- poly {Straight:0.1, Swerve:0.6, X:0.2, or(X,X):0.1}
    - 6.74e-03 -> poly {Swerve:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 2.50e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.50e-04, rho=6.80e-02 k*=10)
    - 2.50e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.50e-04, rho=6.80e-02 k*=10)
    - 1.98e-04 -> poly {Straight:0.2, not(THEM(THEM)):0.8}   via not(THEM(THEM)) (1.98e-04, rho=2.87e-01 k*=8)
    - 1.98e-04 -> poly {Straight:0.2, not(THEM(ME)):0.8}   via not(THEM(ME)) (1.98e-04, rho=2.87e-01 k*=8)
    - 1.52e-04 -> poly {Swerve:0.7, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Straight:0.1, Swerve:0.7, X:0.1, or(X,X):0.1}
    - 6.74e-03 -> poly {Swerve:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 2.42e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.42e-04, rho=6.58e-02 k*=10)
    - 2.42e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.42e-04, rho=6.58e-02 k*=10)
    - 2.22e-04 -> poly {Straight:0.2, not(THEM(THEM)):0.8}   via not(THEM(THEM)) (2.22e-04, rho=3.23e-01 k*=8)
    - 2.22e-04 -> poly {Straight:0.2, not(THEM(ME)):0.8}   via not(THEM(ME)) (2.22e-04, rho=3.23e-01 k*=8)
    - 1.52e-04 -> poly {Swerve:0.7, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Straight:0.1, Swerve:0.8, X:0.1}
    - 6.74e-03 -> poly {Straight:0.1, Swerve:0.7, X:0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {Straight:0.1, Swerve:0.7, X:0.1, and(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 2.41e-04 -> poly {Straight:0.2, not(THEM(THEM)):0.8}   via not(THEM(THEM)) (2.41e-04, rho=3.50e-01 k*=8)
    - 2.41e-04 -> poly {Straight:0.2, not(THEM(ME)):0.8}   via not(THEM(ME)) (2.41e-04, rho=3.50e-01 k*=8)
    - 2.35e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.35e-04, rho=6.37e-02 k*=10)
    - 2.35e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.35e-04, rho=6.37e-02 k*=10)
