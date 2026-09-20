### arm=weak, n=5, game=chicken_norole, N=100, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 450, classes 30, states 738, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 2.28e-13
mean payoff -0.3331, efficient 0.5000, deadweight loss 0.8331, mean bits in support 9.87

| pi | state |
|---|---|
| 0.9959 | poly {Straight:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.64, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.01} |
| 0.0041 | poly {Straight:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.58, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.07} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {Straight:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.64, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.01}
    - 1.09e-14 -> mono {THEM(THEM):1}   via THEM(THEM) (1.09e-14, rho=2.95e-12 k*=100)
    - 2.25e-16 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (2.25e-16, rho=2.95e-12 k*=100)
    - 2.25e-16 -> mono {and(THEM(THEM),Straight):1}   via and(THEM(THEM),Straight) (2.25e-16, rho=2.95e-12 k*=100)
    - 2.25e-16 -> mono {and(THEM(ME),Straight):1}   via and(THEM(ME),Straight) (2.25e-16, rho=2.95e-12 k*=100)
    - 1.99e-16 -> mono {or(THEM(ME),X):1}   via or(THEM(ME),X) (1.99e-16, rho=2.61e-12 k*=100)
    - 3.61e-17 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (3.61e-17, rho=4.74e-13 k*=100)
- poly {Straight:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.58, not(THEM(^Straight)):0.15, or(THEM(ME),Swerve):0.07}
    - 1.09e-14 -> mono {THEM(THEM):1}   via THEM(THEM) (1.09e-14, rho=2.95e-12 k*=100)
    - 2.25e-16 -> mono {and(THEM(THEM),X):1}   via and(THEM(THEM),X) (2.25e-16, rho=2.95e-12 k*=100)
    - 2.25e-16 -> mono {and(THEM(THEM),Straight):1}   via and(THEM(THEM),Straight) (2.25e-16, rho=2.95e-12 k*=100)
    - 2.25e-16 -> mono {and(THEM(ME),Straight):1}   via and(THEM(ME),Straight) (2.25e-16, rho=2.95e-12 k*=100)
    - 1.99e-16 -> mono {or(THEM(ME),X):1}   via or(THEM(ME),X) (1.99e-16, rho=2.61e-12 k*=100)
    - 3.61e-17 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (3.61e-17, rho=4.74e-13 k*=100)
