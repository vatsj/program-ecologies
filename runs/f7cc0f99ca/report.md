### arm=weak, n=6, game=pd, N=100, w=0.3, x_on=True, role=True, mode=square, fmap=exp

programs 3994, classes 112, states 493, terminal classes 1, indeterminate 0, divergence rate 0.0006, flow into polymorphic targets 1.75e-07
mean payoff -0.9903, efficient 0.0000, deadweight loss 0.9903, mean bits in support 3.11

| pi | state |
|---|---|
| 0.9865 | mono {D:1} |
| 0.0077 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.17e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.17e-05, rho=1.00e-02 k*=100)
    - 2.17e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.17e-05, rho=4.21e-02 k*=100)
    - 2.16e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.16e-05, rho=1.00e-02 k*=100)
    - 1.48e-05 -> mono {THEM(^X):1}   via THEM(^X) (1.48e-05, rho=3.01e-02 k*=100)
    - 1.41e-05 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (1.41e-05, rho=3.01e-02 k*=100)
    - 5.15e-06 -> mono {THEM(^D):1}   via THEM(^D) (5.15e-06, rho=1.00e-02 k*=100)
- mono {THEM(^C):1}
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 1.36e-04 -> mono {THEM(^D):1}   via THEM(^D) (1.36e-04, rho=2.64e-01 k*=100)
    - 6.97e-05 -> mono {THEM(^X):1}   via THEM(^X) (6.97e-05, rho=1.42e-01 k*=100)
    - 6.64e-05 -> mono {THEM(^ROLE):1}   via THEM(^ROLE) (6.64e-05, rho=1.42e-01 k*=100)
    - 5.07e-06 -> mono {THEM(^not(ROLE)):1}   via THEM(^not(ROLE)) (5.07e-06, rho=1.42e-01 k*=100)
    - 4.43e-06 -> mono {X:1}   via X (4.43e-06, rho=1.94e-05 k*=100)
