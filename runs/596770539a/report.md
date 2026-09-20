### arm=weak, n=5, game=chicken_norole, N=100, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 450, classes 30, states 797, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 3.09e-06
mean payoff -0.3320, efficient 0.5000, deadweight loss 0.8320, mean bits in support 9.87

| pi | state |
|---|---|
| 0.9837 | poly {Straight:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.64, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.01} |
| 0.0065 | poly {Straight:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.58, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.07} |
| 0.0040 | poly {Straight:0.18, not(THEM(ME)):0.01, not(THEM(THEM)):0.8, or(THEM(ME),Swerve):0.01} |
| 0.0013 | poly {Straight:0.18, not(THEM(ME)):0.8, not(THEM(THEM)):0.01, or(THEM(ME),Swerve):0.01} |
| 0.0010 | poly {Straight:0.19, not(THEM(ME)):0.64, not(THEM(THEM)):0.01, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {Straight:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.64, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.01}
    - 1.12e-07 -> mono {THEM(THEM):1}   via THEM(THEM) (1.12e-07, rho=3.05e-05 k*=100)
    - 3.99e-09 -> mono {THEM(ME):1}   via THEM(ME) (3.99e-09, rho=1.08e-06 k*=100)
    - 2.32e-09 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (2.32e-09, rho=3.05e-05 k*=100)
    - 2.32e-09 -> mono {and(THEM(THEM),Straight):1}   via and(THEM(THEM),Straight) (2.32e-09, rho=3.05e-05 k*=100)
    - 2.32e-09 -> mono {and(THEM(ME),Straight):1}   via and(THEM(ME),Straight) (2.32e-09, rho=3.05e-05 k*=100)
    - 1.80e-09 -> mono {or(THEM(ME),X):1}   via or(THEM(ME),X) (1.80e-09, rho=2.36e-05 k*=100)
- poly {Straight:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.58, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.07}
    - 1.12e-07 -> mono {THEM(THEM):1}   via THEM(THEM) (1.12e-07, rho=3.05e-05 k*=100)
    - 3.99e-09 -> mono {THEM(ME):1}   via THEM(ME) (3.99e-09, rho=1.08e-06 k*=100)
    - 2.32e-09 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (2.32e-09, rho=3.05e-05 k*=100)
    - 2.32e-09 -> mono {and(THEM(THEM),Straight):1}   via and(THEM(THEM),Straight) (2.32e-09, rho=3.05e-05 k*=100)
    - 2.32e-09 -> mono {and(THEM(ME),Straight):1}   via and(THEM(ME),Straight) (2.32e-09, rho=3.05e-05 k*=100)
    - 1.80e-09 -> mono {or(THEM(ME),X):1}   via or(THEM(ME),X) (1.80e-09, rho=2.36e-05 k*=100)
- poly {Straight:0.18, not(THEM(ME)):0.01, not(THEM(THEM)):0.8, or(THEM(ME),Swerve):0.01}
    - 2.61e-05 -> poly {Straight:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.64, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.01}   via not(THEM(^Straight)) (2.61e-05, rho=3.42e-01 k*=15)
    - 3.29e-09 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (3.29e-09, rho=4.32e-05 k*=100)
    - 3.29e-09 -> mono {or(THEM(ME),X):1}   via or(THEM(ME),X) (3.29e-09, rho=4.32e-05 k*=100)
    - 1.60e-09 -> mono {THEM(THEM):1}   via THEM(THEM) (1.60e-09, rho=4.34e-07 k*=100)
    - 1.60e-09 -> mono {THEM(ME):1}   via THEM(ME) (1.60e-09, rho=4.34e-07 k*=100)
    - 3.31e-11 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (3.31e-11, rho=4.34e-07 k*=100)
- poly {Straight:0.18, not(THEM(ME)):0.8, not(THEM(THEM)):0.01, or(THEM(ME),Swerve):0.01}
    - 3.96e-05 -> mono {THEM(^Swerve):1}   via THEM(^Swerve) (3.96e-05, rho=5.24e-02 k*=99)
    - 2.61e-05 -> poly {Straight:0.19, not(THEM(ME)):0.64, not(THEM(THEM)):0.01, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.01}   via not(THEM(^Straight)) (2.61e-05, rho=3.42e-01 k*=15)
    - 4.26e-07 -> mono {or(THEM(ME),Swerve):1}   via THEM(^Swerve) (4.26e-07, rho=5.24e-02 k*=99)
    - 3.29e-09 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (3.29e-09, rho=4.32e-05 k*=100)
    - 3.29e-09 -> mono {or(THEM(ME),X):1}   via or(THEM(ME),X) (3.29e-09, rho=4.32e-05 k*=100)
    - 1.60e-09 -> mono {THEM(THEM):1}   via THEM(THEM) (1.60e-09, rho=4.34e-07 k*=100)
- poly {Straight:0.19, not(THEM(ME)):0.64, not(THEM(THEM)):0.01, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.01}
    - 4.45e-05 -> mono {THEM(^Swerve):1}   via THEM(^Swerve) (4.45e-05, rho=5.87e-02 k*=99)
    - 4.41e-07 -> mono {or(THEM(ME),Swerve):1}   via THEM(^Swerve) (4.41e-07, rho=5.87e-02 k*=99)
    - 1.12e-07 -> mono {THEM(THEM):1}   via THEM(THEM) (1.12e-07, rho=3.05e-05 k*=100)
    - 3.99e-09 -> mono {THEM(ME):1}   via THEM(ME) (3.99e-09, rho=1.08e-06 k*=100)
    - 2.32e-09 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (2.32e-09, rho=3.05e-05 k*=100)
    - 2.32e-09 -> mono {and(THEM(THEM),Straight):1}   via and(THEM(THEM),Straight) (2.32e-09, rho=3.05e-05 k*=100)
