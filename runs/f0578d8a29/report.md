### arm=weak, n=6, game=pd, N=1000, w=0.1, x_on=True, role=True, mode=square, fmap=exp

programs 3994, classes 112, states 479, terminal classes 1, indeterminate 0, divergence rate 0.0006, flow into polymorphic targets 4.17e-08
mean payoff -0.9875, efficient 0.0000, deadweight loss 0.9875, mean bits in support 3.14

| pi | state |
|---|---|
| 0.9847 | mono {D:1} |
| 0.0115 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 4.08e-06 -> mono {THEM(^C):1}   via THEM(^C) (4.08e-06, rho=7.92e-03 k*=1000)
    - 2.76e-06 -> mono {THEM(^X):1}   via THEM(^X) (2.76e-06, rho=5.61e-03 k*=1000)
    - 2.62e-06 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (2.62e-06, rho=5.61e-03 k*=1000)
    - 2.17e-06 -> mono {THEM(ME):1}   via THEM(ME) (2.17e-06, rho=1.00e-03 k*=1000)
    - 2.16e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (2.16e-06, rho=1.00e-03 k*=1000)
    - 5.15e-07 -> mono {THEM(^D):1}   via THEM(^D) (5.15e-07, rho=1.00e-03 k*=1000)
- mono {THEM(^C):1}
    - 2.49e-04 -> mono {C:1}   via C (2.49e-04, rho=1.00e-03 k*=1000)
    - 4.91e-05 -> mono {THEM(^D):1}   via THEM(^D) (4.91e-05, rho=9.53e-02 k*=1000)
    - 2.40e-05 -> mono {THEM(^X):1}   via THEM(^X) (2.40e-05, rho=4.89e-02 k*=1000)
    - 2.29e-05 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (2.29e-05, rho=4.89e-02 k*=1000)
    - 1.75e-06 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (1.75e-06, rho=4.89e-02 k*=1000)
    - 1.20e-06 -> mono {or(ROLE,THEM(^D)):1}   via or(ROLE,THEM(^D)) (1.20e-06, rho=4.98e-02 k*=1000)
