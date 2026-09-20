### arm=weak, n=5, game=chicken_norole, N=10, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 450, classes 30, states 521, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 1.61e-02
mean payoff -0.1487, efficient 0.5000, deadweight loss 0.6487, mean bits in support 4.29

| pi | state |
|---|---|
| 0.4408 | poly {Swerve:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1} |
| 0.0950 | poly {Swerve:0.7, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1} |
| 0.0629 | poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1} |
| 0.0622 | poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1} |
| 0.0499 | poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Swerve):0.1} |
| 0.0370 | poly {Straight:0.1, Swerve:0.7, X:0.1, and(X,X):0.1} |
| 0.0260 | poly {Straight:0.1, Swerve:0.7, X:0.2} |
| 0.0232 | poly {Straight:0.1, Swerve:0.7, X:0.1, or(X,X):0.1} |
| 0.0220 | poly {Straight:0.1, Swerve:0.6, X:0.2, or(X,X):0.1} |
| 0.0175 | poly {Straight:0.1, Swerve:0.8, X:0.1} |
| 0.0148 | poly {Swerve:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),Swerve):0.1} |
| 0.0148 | poly {Swerve:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(THEM(ME),Swerve):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {Swerve:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}
    - 8.13e-03 -> poly {Swerve:0.6, X:0.2, and(X,X):0.1, or(X,X):0.1}   via THEM(ME) (3.68e-03, rho=1.00e+00 k*=1), THEM(THEM) (3.68e-03, rho=1.00e+00 k*=1), THEM(^Swerve) (7.65e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.7, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Swerve):0.1}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Swerve:0.7, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1}
    - 9.20e-03 -> poly {Swerve:0.6, X:0.2, or(X,X):0.1, and(X,or(X,X)):0.1}   via THEM(ME) (3.68e-03, rho=1.00e+00 k*=1), THEM(THEM) (3.68e-03, rho=1.00e+00 k*=1), THEM(^Swerve) (7.65e-04, rho=1.00e+00 k*=1), THEM(^X) (7.65e-04, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 9.17e-04 -> poly {Swerve:0.6, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.2}   via THEM(^Straight) (7.65e-04, rho=1.00e+00 k*=1), and(X,THEM(ME)) (7.61e-05, rho=1.00e+00 k*=1), and(X,THEM(THEM)) (7.61e-05, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.5, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.2, or(THEM(ME),Swerve):0.1}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, or(X,X):0.1, or(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}
    - 3.41e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.41e-04, rho=9.26e-02 k*=10)
    - 3.41e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.41e-04, rho=9.26e-02 k*=10)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),Swerve):0.1}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1}
    - 3.42e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.42e-04, rho=9.29e-02 k*=10)
    - 3.42e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.42e-04, rho=9.29e-02 k*=10)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, or(X,X):0.1, or(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(THEM(ME),Swerve):0.1}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Swerve:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),Swerve):0.1}
    - 3.38e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.38e-04, rho=9.19e-02 k*=10)
    - 3.38e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.38e-04, rho=9.19e-02 k*=10)
    - 1.52e-04 -> poly {Swerve:0.6, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(THEM(ME),Swerve):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),Swerve):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(THEM(ME),Swerve):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(THEM(ME),Swerve):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Straight:0.1, Swerve:0.7, X:0.1, and(X,X):0.1}
    - 6.74e-03 -> poly {Swerve:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.15e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.15e-04, rho=8.55e-02 k*=10)
    - 3.15e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.15e-04, rho=8.55e-02 k*=10)
    - 1.52e-04 -> poly {Swerve:0.8, X:0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.7, X:0.1, and(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.7, X:0.1, and(X,X):0.1, or(X,and(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Straight:0.1, Swerve:0.7, X:0.2}
    - 6.74e-03 -> poly {Straight:0.1, Swerve:0.6, X:0.2, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {Straight:0.1, Swerve:0.7, X:0.1, and(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.22e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.22e-04, rho=8.73e-02 k*=10)
    - 3.22e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.22e-04, rho=8.73e-02 k*=10)
    - 1.52e-04 -> poly {Straight:0.1, Swerve:0.6, X:0.2, or(THEM(ME),Swerve):0.1}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Straight:0.1, Swerve:0.6, X:0.2, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Straight:0.1, Swerve:0.7, X:0.1, or(X,X):0.1}
    - 6.74e-03 -> poly {Swerve:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.23e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.23e-04, rho=8.77e-02 k*=10)
    - 3.23e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.23e-04, rho=8.77e-02 k*=10)
    - 1.52e-04 -> poly {Swerve:0.7, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.7, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Straight:0.1, Swerve:0.6, X:0.1, or(X,X):0.1, or(THEM(ME),Swerve):0.1}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Straight:0.1, Swerve:0.6, X:0.2, or(X,X):0.1}
    - 6.74e-03 -> poly {Swerve:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.27e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.27e-04, rho=8.89e-02 k*=10)
    - 3.27e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.27e-04, rho=8.89e-02 k*=10)
    - 1.52e-04 -> poly {Swerve:0.7, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.7, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Straight:0.1, Swerve:0.5, X:0.2, or(X,X):0.1, or(THEM(ME),Swerve):0.1}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Straight:0.1, Swerve:0.8, X:0.1}
    - 6.74e-03 -> poly {Straight:0.1, Swerve:0.7, X:0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {Straight:0.1, Swerve:0.7, X:0.1, and(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.19e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.19e-04, rho=8.68e-02 k*=10)
    - 3.19e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.19e-04, rho=8.68e-02 k*=10)
    - 1.52e-04 -> poly {Straight:0.1, Swerve:0.7, X:0.1, or(THEM(ME),Swerve):0.1}   via or(THEM(ME),Swerve) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Straight:0.1, Swerve:0.7, X:0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {Swerve:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),Swerve):0.1}
    - 3.41e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.41e-04, rho=9.26e-02 k*=10)
    - 3.41e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.41e-04, rho=9.26e-02 k*=10)
    - 1.52e-04 -> poly {Swerve:0.5, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1, or(THEM(ME),Swerve):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.5, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,or(X,X)):0.1, or(THEM(ME),Swerve):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(X,or(X,X)):0.1, or(THEM(ME),Swerve):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 9.39e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (9.39e-05, rho=1.55e-01 k*=9)
- poly {Swerve:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(THEM(ME),Swerve):0.1}
    - 3.42e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.42e-04, rho=9.29e-02 k*=10)
    - 3.42e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.42e-04, rho=9.29e-02 k*=10)
    - 1.52e-04 -> poly {Swerve:0.5, X:0.1, or(X,X):0.1, or(X,and(X,X)):0.1, and(X,or(X,X)):0.1, or(THEM(ME),Swerve):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.5, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,and(X,X)):0.1, or(THEM(ME),Swerve):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {Swerve:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(X,or(X,X)):0.1, or(THEM(ME),Swerve):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 9.02e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (9.02e-05, rho=1.50e-01 k*=9)
