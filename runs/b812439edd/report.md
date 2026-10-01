### arm=weak, n=6, game=pd, N=300, w=0.3, x_on=True, role=True, mode=square, fmap=exp

programs 3994, classes 112, states 493, terminal classes 1, indeterminate 0, divergence rate 0.0006, flow into polymorphic targets 1.32e-07
mean payoff -0.9876, efficient 0.0000, deadweight loss 0.9876, mean bits in support 3.14

| pi | state |
|---|---|
| 0.9847 | mono {D:1} |
| 0.0112 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.27e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.27e-05, rho=2.46e-02 k*=300)
    - 8.63e-06 -> mono {THEM(^X):1}   via THEM(^X) (8.63e-06, rho=1.76e-02 k*=300)
    - 8.21e-06 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (8.21e-06, rho=1.76e-02 k*=300)
    - 7.23e-06 -> mono {THEM(ME):1}   via THEM(ME) (7.23e-06, rho=3.33e-03 k*=300)
    - 7.21e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (7.21e-06, rho=3.33e-03 k*=300)
    - 1.72e-06 -> mono {THEM(^D):1}   via THEM(^D) (1.72e-06, rho=3.33e-03 k*=300)
- mono {THEM(^C):1}
    - 8.31e-04 -> mono {C:1}   via C (8.31e-04, rho=3.33e-03 k*=300)
    - 1.34e-04 -> mono {THEM(^D):1}   via THEM(^D) (1.34e-04, rho=2.61e-01 k*=300)
    - 6.89e-05 -> mono {THEM(^X):1}   via THEM(^X) (6.89e-05, rho=1.40e-01 k*=300)
    - 6.55e-05 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (6.55e-05, rho=1.40e-01 k*=300)
    - 5.01e-06 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (5.01e-06, rho=1.40e-01 k*=300)
    - 3.44e-06 -> mono {or(ROLE,THEM(^D)):1}   via or(ROLE,THEM(^D)) (3.44e-06, rho=1.43e-01 k*=300)
