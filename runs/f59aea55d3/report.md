### arm=weak, n=6, game=pd, N=1000, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 48, states 129, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 2.60e-07
mean payoff -0.9824, efficient 0.0000, deadweight loss 0.9824, mean bits in support 2.75

| pi | state |
|---|---|
| 0.9804 | mono {D:1} |
| 0.0173 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.24e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.24e-05, rho=2.46e-02 k*=1000)
    - 1.55e-05 -> mono {THEM(^X):1}   via THEM(^X) (1.55e-05, rho=1.75e-02 k*=1000)
    - 3.68e-06 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-06, rho=1.00e-03 k*=1000)
    - 3.67e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-06, rho=1.00e-03 k*=1000)
    - 9.10e-07 -> mono {THEM(^D):1}   via THEM(^D) (9.10e-07, rho=1.00e-03 k*=1000)
    - 3.31e-07 -> mono {and(X,THEM(^C)):1}   via and(X,THEM(^C)) (3.31e-07, rho=1.25e-02 k*=1000)
- mono {THEM(^C):1}
    - 5.76e-04 -> mono {THEM(^D):1}   via THEM(^D) (5.76e-04, rho=6.33e-01 k*=1000)
    - 3.48e-04 -> mono {THEM(^X):1}   via THEM(^X) (3.48e-04, rho=3.94e-01 k*=1000)
    - 3.29e-04 -> mono {C:1}   via C (3.29e-04, rho=1.00e-03 k*=1000)
    - 1.05e-05 -> mono {or(X,THEM(^D)):1}   via or(X,THEM(^D)) (1.05e-05, rho=3.94e-01 k*=1000)
    - 7.02e-06 -> mono {THEM(^and(X,X)):1}   via THEM(^and(X,X)) (7.02e-06, rho=5.28e-01 k*=1000)
    - 5.90e-06 -> mono {or(X,THEM(^X)):1}   via or(X,THEM(^X)) (5.90e-06, rho=2.22e-01 k*=1000)
