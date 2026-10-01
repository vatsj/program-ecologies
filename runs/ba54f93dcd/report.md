### arm=weak, n=6, game=pd, N=1000, w=0.3, x_on=True, role=True, mode=square, fmap=exp

programs 3994, classes 112, states 479, terminal classes 1, indeterminate 0, divergence rate 0.0006, flow into polymorphic targets 7.94e-08
mean payoff -0.9864, efficient 0.0000, deadweight loss 0.9864, mean bits in support 3.14

| pi | state |
|---|---|
| 0.9845 | mono {D:1} |
| 0.0130 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 7.03e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.03e-06, rho=1.36e-02 k*=1000)
    - 4.76e-06 -> mono {THEM(^X):1}   via THEM(^X) (4.76e-06, rho=9.68e-03 k*=1000)
    - 4.53e-06 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (4.53e-06, rho=9.68e-03 k*=1000)
    - 2.17e-06 -> mono {THEM(ME):1}   via THEM(ME) (2.17e-06, rho=1.00e-03 k*=1000)
    - 2.16e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (2.16e-06, rho=1.00e-03 k*=1000)
    - 5.15e-07 -> mono {THEM(^D):1}   via THEM(^D) (5.15e-07, rho=1.00e-03 k*=1000)
- mono {THEM(^C):1}
    - 2.49e-04 -> mono {C:1}   via C (2.49e-04, rho=1.00e-03 k*=1000)
    - 1.34e-04 -> mono {THEM(^D):1}   via THEM(^D) (1.34e-04, rho=2.60e-01 k*=1000)
    - 6.86e-05 -> mono {THEM(^X):1}   via THEM(^X) (6.86e-05, rho=1.40e-01 k*=1000)
    - 6.53e-05 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (6.53e-05, rho=1.40e-01 k*=1000)
    - 4.99e-06 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (4.99e-06, rho=1.40e-01 k*=1000)
    - 3.38e-06 -> mono {or(ROLE,THEM(^D)):1}   via or(ROLE,THEM(^D)) (3.38e-06, rho=1.40e-01 k*=1000)
