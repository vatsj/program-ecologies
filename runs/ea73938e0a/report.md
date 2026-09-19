### arm=weak, n=6, game=pd, N=1000, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 48, states 118, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 1.27e-07
mean payoff -0.9819, efficient 0.0000, deadweight loss 0.9819, mean bits in support 2.76

| pi | state |
|---|---|
| 0.9795 | mono {D:1} |
| 0.0175 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.24e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.24e-05, rho=1.36e-02 k*=1000)
    - 8.55e-06 -> mono {THEM(^X):1}   via THEM(^X) (8.55e-06, rho=9.68e-03 k*=1000)
    - 3.68e-06 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-06, rho=1.00e-03 k*=1000)
    - 3.67e-06 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-06, rho=1.00e-03 k*=1000)
    - 9.10e-07 -> mono {THEM(^D):1}   via THEM(^D) (9.10e-07, rho=1.00e-03 k*=1000)
    - 1.82e-07 -> mono {and(X,THEM(^C)):1}   via and(X,THEM(^C)) (1.82e-07, rho=6.87e-03 k*=1000)
- mono {THEM(^C):1}
    - 3.29e-04 -> mono {C:1}   via C (3.29e-04, rho=1.00e-03 k*=1000)
    - 2.36e-04 -> mono {THEM(^D):1}   via THEM(^D) (2.36e-04, rho=2.60e-01 k*=1000)
    - 1.23e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.23e-04, rho=1.40e-01 k*=1000)
    - 3.72e-06 -> mono {or(X,THEM(^D)):1}   via or(X,THEM(^D)) (3.72e-06, rho=1.40e-01 k*=1000)
    - 2.68e-06 -> mono {THEM(^and(X,X)):1}   via THEM(^and(X,X)) (2.68e-06, rho=2.02e-01 k*=1000)
    - 1.94e-06 -> mono {or(X,THEM(^X)):1}   via or(X,THEM(^X)) (1.94e-06, rho=7.28e-02 k*=1000)
