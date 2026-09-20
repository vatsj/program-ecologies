### arm=weak, n=6, game=pd, N=100, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 48, states 119, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 6.31e-07
mean payoff -0.9831, efficient 0.0000, deadweight loss 0.9831, mean bits in support 2.76

| pi | state |
|---|---|
| 0.9797 | mono {D:1} |
| 0.0156 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 6.75e-05 -> mono {THEM(^C):1}   via THEM(^C) (6.75e-05, rho=7.42e-02 k*=100)
    - 4.74e-05 -> mono {THEM(^X):1}   via THEM(^X) (4.74e-05, rho=5.36e-02 k*=100)
    - 3.68e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 9.10e-06 -> mono {THEM(^D):1}   via THEM(^D) (9.10e-06, rho=1.00e-02 k*=100)
    - 1.15e-06 -> mono {and(THEM(THEM),D):1}   via and(THEM(THEM),D) (1.15e-06, rho=1.00e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 5.82e-04 -> mono {THEM(^D):1}   via THEM(^D) (5.82e-04, rho=6.39e-01 k*=100)
    - 3.53e-04 -> mono {THEM(^X):1}   via THEM(^X) (3.53e-04, rho=4.00e-01 k*=100)
    - 1.07e-05 -> mono {or(X,THEM(^D)):1}   via or(X,THEM(^D)) (1.07e-05, rho=4.02e-01 k*=100)
    - 7.10e-06 -> mono {THEM(^and(X,X)):1}   via THEM(^and(X,X)) (7.10e-06, rho=5.35e-01 k*=100)
    - 6.07e-06 -> mono {or(X,THEM(^X)):1}   via or(X,THEM(^X)) (6.07e-06, rho=2.28e-01 k*=100)
