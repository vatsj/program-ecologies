### arm=weak, n=6, game=pd, N=100, w=1.0, x_on=True, role=True, mode=square, fmap=exp

programs 3994, classes 112, states 493, terminal classes 1, indeterminate 0, divergence rate 0.0006, flow into polymorphic targets 4.33e-07
mean payoff -0.9872, efficient 0.0000, deadweight loss 0.9872, mean bits in support 3.14

| pi | state |
|---|---|
| 0.9841 | mono {D:1} |
| 0.0116 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.82e-05 -> mono {THEM(^C):1}   via THEM(^C) (3.82e-05, rho=7.42e-02 k*=100)
    - 2.64e-05 -> mono {THEM(^X):1}   via THEM(^X) (2.64e-05, rho=5.36e-02 k*=100)
    - 2.51e-05 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (2.51e-05, rho=5.36e-02 k*=100)
    - 2.17e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.17e-05, rho=1.00e-02 k*=100)
    - 2.16e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.16e-05, rho=1.00e-02 k*=100)
    - 5.15e-06 -> mono {THEM(^D):1}   via THEM(^D) (5.15e-06, rho=1.00e-02 k*=100)
- mono {THEM(^C):1}
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 3.30e-04 -> mono {THEM(^D):1}   via THEM(^D) (3.30e-04, rho=6.39e-01 k*=100)
    - 1.96e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.96e-04, rho=4.00e-01 k*=100)
    - 1.87e-04 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (1.87e-04, rho=4.00e-01 k*=100)
    - 1.43e-05 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (1.43e-05, rho=4.00e-01 k*=100)
    - 9.73e-06 -> mono {or(ROLE,THEM(^D)):1}   via or(ROLE,THEM(^D)) (9.73e-06, rho=4.04e-01 k*=100)
