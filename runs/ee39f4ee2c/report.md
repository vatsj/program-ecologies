### arm=weak, n=6, game=pd, N=1000, w=1.0, x_on=True, role=True, mode=square, fmap=exp

programs 3994, classes 112, states 510, terminal classes 1, indeterminate 0, divergence rate 0.0006, flow into polymorphic targets 1.57e-07
mean payoff -0.9871, efficient 0.0000, deadweight loss 0.9871, mean bits in support 3.13

| pi | state |
|---|---|
| 0.9856 | mono {D:1} |
| 0.0125 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.27e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.27e-05, rho=2.46e-02 k*=1000)
    - 8.62e-06 -> mono {THEM(^X):1}   via THEM(^X) (8.62e-06, rho=1.75e-02 k*=1000)
    - 8.20e-06 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (8.20e-06, rho=1.75e-02 k*=1000)
    - 2.17e-06 -> mono {THEM(ME):1}   via THEM(ME) (2.17e-06, rho=1.00e-03 k*=1000)
    - 2.16e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (2.16e-06, rho=1.00e-03 k*=1000)
    - 6.27e-07 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (6.27e-07, rho=1.75e-02 k*=1000)
- mono {THEM(^C):1}
    - 3.26e-04 -> mono {THEM(^D):1}   via THEM(^D) (3.26e-04, rho=6.33e-01 k*=1000)
    - 2.49e-04 -> mono {C:1}   via C (2.49e-04, rho=1.00e-03 k*=1000)
    - 1.94e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.94e-04, rho=3.94e-01 k*=1000)
    - 1.84e-04 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (1.84e-04, rho=3.94e-01 k*=1000)
    - 1.41e-05 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (1.41e-05, rho=3.94e-01 k*=1000)
    - 9.51e-06 -> mono {or(ROLE,THEM(^D)):1}   via or(ROLE,THEM(^D)) (9.51e-06, rho=3.95e-01 k*=1000)
