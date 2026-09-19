### arm=weak, n=5, game=chicken_norole, N=100, w=1.0, x_on=True, role=False, mode=square

programs 450, classes 30, states 890, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 1.51e-47
mean payoff -0.3331, efficient 0.5000, deadweight loss 0.8331, mean bits in support 10.06

| pi | state |
|---|---|
| 1.0000 | poly {D:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.58, not(THEM(^D)):0.15, or(THEM(ME),C):0.07} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {D:0.19, not(THEM(ME)):0.01, not(THEM(THEM)):0.58, not(THEM(^D)):0.15, or(THEM(ME),C):0.07}
    - 3.71e-49 -> mono {THEM(^C):1}   via THEM(^C) (3.71e-49, rho=5.47e-46 k*=89)
    - 4.78e-50 -> mono {or(THEM(ME),C):1}   via THEM(^C) (4.78e-50, rho=5.47e-46 k*=89), THEM(THEM) (2.30e-209, rho=2.22e-205 k*=74), and(THEM(ME),D) (4.76e-211, rho=2.22e-205 k*=74), and(THEM(THEM),D) (4.76e-211, rho=2.22e-205 k*=74)
    - 2.72e-51 -> mono {not(THEM(^C)):1}   via not(THEM(^C)) (2.72e-51, rho=3.57e-47 k*=100)
    - 6.70e-58 -> mono {C:1}   via C (6.70e-58, rho=2.03e-57 k*=100)
    - 1.16e-123 -> mono {THEM(^X):1}   via THEM(^X) (1.16e-123, rho=1.52e-120 k*=100)
    - 2.66e-129 -> mono {and(X,X):1}   via and(X,X) (2.66e-129, rho=3.95e-127 k*=100)
