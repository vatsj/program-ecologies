### arm=weak, n=6, game=pd, N=10000, w=1.0, x_on=True, role=True, mode=square, fmap=exp

programs 3994, classes 112, states 508, terminal classes 1, indeterminate 0, divergence rate 0.0006, flow into polymorphic targets 5.03e-08
mean payoff -0.9947, efficient 0.0000, deadweight loss 0.9947, mean bits in support 3.06

| pi | state |
|---|---|
| 0.9937 | mono {D:1} |
| 0.0052 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 4.08e-06 -> mono {THEM(^C):1}   via THEM(^C) (4.08e-06, rho=7.92e-03 k*=10000)
    - 2.76e-06 -> mono {THEM(^X):1}   via THEM(^X) (2.76e-06, rho=5.61e-03 k*=10000)
    - 2.62e-06 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (2.62e-06, rho=5.61e-03 k*=10000)
    - 2.17e-07 -> mono {THEM(ME):1}   via THEM(ME) (2.17e-07, rho=1.00e-04 k*=10000)
    - 2.16e-07 -> mono {THEM(THEM):1}   via THEM(THEM) (2.16e-07, rho=1.00e-04 k*=10000)
    - 2.01e-07 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (2.01e-07, rho=5.61e-03 k*=10000)
- mono {THEM(^C):1}
    - 3.26e-04 -> mono {THEM(^D):1}   via THEM(^D) (3.26e-04, rho=6.32e-01 k*=10000)
    - 1.93e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.93e-04, rho=3.94e-01 k*=10000)
    - 1.84e-04 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (1.84e-04, rho=3.94e-01 k*=10000)
    - 2.49e-05 -> mono {C:1}   via C (2.49e-05, rho=1.00e-04 k*=10000)
    - 1.41e-05 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (1.41e-05, rho=3.94e-01 k*=10000)
    - 9.48e-06 -> mono {or(ROLE,THEM(^D)):1}   via or(ROLE,THEM(^D)) (9.48e-06, rho=3.94e-01 k*=10000)
