### arm=weak, n=6, game=pd, N=300, w=1.0, x_on=True, role=True, mode=square, fmap=exp

programs 3994, classes 112, states 493, terminal classes 1, indeterminate 0, divergence rate 0.0006, flow into polymorphic targets 2.71e-07
mean payoff -0.9852, efficient 0.0000, deadweight loss 0.9852, mean bits in support 3.15

| pi | state |
|---|---|
| 0.9831 | mono {D:1} |
| 0.0141 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.27e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.27e-05, rho=4.41e-02 k*=300)
    - 1.55e-05 -> mono {THEM(^X):1}   via THEM(^X) (1.55e-05, rho=3.16e-02 k*=300)
    - 1.48e-05 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (1.48e-05, rho=3.16e-02 k*=300)
    - 7.23e-06 -> mono {THEM(ME):1}   via THEM(ME) (7.23e-06, rho=3.33e-03 k*=300)
    - 7.21e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (7.21e-06, rho=3.33e-03 k*=300)
    - 1.72e-06 -> mono {THEM(^D):1}   via THEM(^D) (1.72e-06, rho=3.33e-03 k*=300)
- mono {THEM(^C):1}
    - 8.31e-04 -> mono {C:1}   via C (8.31e-04, rho=3.33e-03 k*=300)
    - 3.27e-04 -> mono {THEM(^D):1}   via THEM(^D) (3.27e-04, rho=6.35e-01 k*=300)
    - 1.94e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.94e-04, rho=3.95e-01 k*=300)
    - 1.85e-04 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (1.85e-04, rho=3.95e-01 k*=300)
    - 1.41e-05 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (1.41e-05, rho=3.95e-01 k*=300)
    - 9.57e-06 -> mono {or(ROLE,THEM(^D)):1}   via or(ROLE,THEM(^D)) (9.57e-06, rho=3.97e-01 k*=300)
