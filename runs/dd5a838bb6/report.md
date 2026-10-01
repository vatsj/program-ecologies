### arm=weak, n=6, game=pd, N=300, w=0.1, x_on=True, role=True, mode=square, fmap=exp

programs 3994, classes 112, states 493, terminal classes 1, indeterminate 0, divergence rate 0.0006, flow into polymorphic targets 5.84e-08
mean payoff -0.9902, efficient 0.0000, deadweight loss 0.9902, mean bits in support 3.11

| pi | state |
|---|---|
| 0.9866 | mono {D:1} |
| 0.0078 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 7.41e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.41e-06, rho=1.44e-02 k*=300)
    - 7.23e-06 -> mono {THEM(ME):1}   via THEM(ME) (7.23e-06, rho=3.33e-03 k*=300)
    - 7.21e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (7.21e-06, rho=3.33e-03 k*=300)
    - 5.02e-06 -> mono {THEM(^X):1}   via THEM(^X) (5.02e-06, rho=1.02e-02 k*=300)
    - 4.78e-06 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (4.78e-06, rho=1.02e-02 k*=300)
    - 1.72e-06 -> mono {THEM(^D):1}   via THEM(^D) (1.72e-06, rho=3.33e-03 k*=300)
- mono {THEM(^C):1}
    - 8.31e-04 -> mono {C:1}   via C (8.31e-04, rho=3.33e-03 k*=300)
    - 4.94e-05 -> mono {THEM(^D):1}   via THEM(^D) (4.94e-05, rho=9.58e-02 k*=300)
    - 2.41e-05 -> mono {THEM(^X):1}   via THEM(^X) (2.41e-05, rho=4.91e-02 k*=300)
    - 2.30e-05 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (2.30e-05, rho=4.91e-02 k*=300)
    - 1.76e-06 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (1.76e-06, rho=4.91e-02 k*=300)
    - 1.36e-06 -> mono {X:1}   via X (1.36e-06, rho=5.94e-06 k*=300)
