### arm=weak, n=6, game=pd, N=1000, w=0.1, x_on=True, role=False, mode=square

programs 1852, classes 48, states 118, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 6.53e-08
mean payoff -0.9827, efficient 0.0000, deadweight loss 0.9827, mean bits in support 2.76

| pi | state |
|---|---|
| 0.9796 | mono {D:1} |
| 0.0163 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 7.57e-06 -> mono {THEM(^C):1}   via THEM(^C) (7.57e-06, rho=8.32e-03 k*=1000)
    - 5.22e-06 -> mono {THEM(^X):1}   via THEM(^X) (5.22e-06, rho=5.90e-03 k*=1000)
    - 3.68e-06 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-06, rho=1.00e-03 k*=1000)
    - 3.67e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-06, rho=1.00e-03 k*=1000)
    - 9.10e-07 -> mono {THEM(^D):1}   via THEM(^D) (9.10e-07, rho=1.00e-03 k*=1000)
    - 1.15e-07 -> mono {and(THEM(THEM),D):1}   via and(THEM(THEM),D) (1.15e-07, rho=1.00e-03 k*=1000)
- mono {THEM(^C):1}
    - 3.29e-04 -> mono {C:1}   via C (3.29e-04, rho=1.00e-03 k*=1000)
    - 8.30e-05 -> mono {THEM(^D):1}   via THEM(^D) (8.30e-05, rho=9.13e-02 k*=1000)
    - 4.22e-05 -> mono {THEM(^X):1}   via THEM(^X) (4.22e-05, rho=4.78e-02 k*=1000)
    - 1.28e-06 -> mono {or(X,THEM(^D)):1}   via or(X,THEM(^D)) (1.28e-06, rho=4.82e-02 k*=1000)
    - 9.30e-07 -> mono {THEM(^and(X,X)):1}   via THEM(^and(X,X)) (9.30e-07, rho=7.00e-02 k*=1000)
    - 6.63e-07 -> mono {or(X,THEM(^X)):1}   via or(X,THEM(^X)) (6.63e-07, rho=2.49e-02 k*=1000)
