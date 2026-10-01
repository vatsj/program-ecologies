### arm=weak, n=6, game=pd, N=3000, w=1.0, x_on=True, role=True, mode=square, fmap=exp

programs 3994, classes 112, states 507, terminal classes 1, indeterminate 0, divergence rate 0.0006, flow into polymorphic targets 9.25e-08
mean payoff -0.9910, efficient 0.0000, deadweight loss 0.9910, mean bits in support 3.09

| pi | state |
|---|---|
| 0.9898 | mono {D:1} |
| 0.0088 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 7.40e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.40e-06, rho=1.44e-02 k*=3000)
    - 5.01e-06 -> mono {THEM(^X):1}   via THEM(^X) (5.01e-06, rho=1.02e-02 k*=3000)
    - 4.77e-06 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (4.77e-06, rho=1.02e-02 k*=3000)
    - 7.23e-07 -> mono {THEM(ME):1}   via THEM(ME) (7.23e-07, rho=3.33e-04 k*=3000)
    - 7.21e-07 -> mono {THEM(THEM):1}   via THEM(THEM) (7.21e-07, rho=3.33e-04 k*=3000)
    - 3.65e-07 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (3.65e-07, rho=1.02e-02 k*=3000)
- mono {THEM(^C):1}
    - 3.26e-04 -> mono {THEM(^D):1}   via THEM(^D) (3.26e-04, rho=6.32e-01 k*=3000)
    - 1.93e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.93e-04, rho=3.94e-01 k*=3000)
    - 1.84e-04 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (1.84e-04, rho=3.94e-01 k*=3000)
    - 8.31e-05 -> mono {C:1}   via C (8.31e-05, rho=3.33e-04 k*=3000)
    - 1.41e-05 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (1.41e-05, rho=3.94e-01 k*=3000)
    - 9.49e-06 -> mono {or(ROLE,THEM(^D)):1}   via or(ROLE,THEM(^D)) (9.49e-06, rho=3.94e-01 k*=3000)
