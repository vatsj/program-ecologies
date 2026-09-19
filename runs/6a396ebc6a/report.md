### arm=weak, n=6, game=pd, N=100, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 48, states 120, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 2.59e-07
mean payoff -0.9876, efficient 0.0000, deadweight loss 0.9876, mean bits in support 2.71

| pi | state |
|---|---|
| 0.9834 | mono {D:1} |
| 0.0103 | mono {THEM(^C):1} |
| 0.0014 | mono {X:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.83e-05 -> mono {THEM(^C):1}   via THEM(^C) (3.83e-05, rho=4.21e-02 k*=100)
    - 3.68e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 2.66e-05 -> mono {THEM(^X):1}   via THEM(^X) (2.66e-05, rho=3.01e-02 k*=100)
    - 9.10e-06 -> mono {THEM(^D):1}   via THEM(^D) (9.10e-06, rho=1.00e-02 k*=100)
    - 1.15e-06 -> mono {and(THEM(THEM),D):1}   via and(THEM(THEM),D) (1.15e-06, rho=1.00e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 2.40e-04 -> mono {THEM(^D):1}   via THEM(^D) (2.40e-04, rho=2.64e-01 k*=100)
    - 1.25e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.25e-04, rho=1.42e-01 k*=100)
    - 6.05e-06 -> mono {X:1}   via X (6.05e-06, rho=1.94e-05 k*=100)
    - 4.13e-06 -> mono {or(X,X):1}   via or(X,X) (4.13e-06, rho=5.48e-04 k*=100)
    - 3.87e-06 -> mono {or(X,THEM(^D)):1}   via or(X,THEM(^D)) (3.87e-06, rho=1.46e-01 k*=100)
- mono {X:1}
    - 4.67e-02 -> mono {D:1}   via D (4.67e-02, rho=1.42e-01 k*=100)
    - 5.56e-04 -> mono {and(X,X):1}   via and(X,X) (5.56e-04, rho=7.37e-02 k*=100)
    - 3.06e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (3.06e-05, rho=1.08e-01 k*=100)
    - 2.74e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.74e-05, rho=3.01e-02 k*=100)
    - 1.63e-05 -> mono {and(THEM(THEM),D):1}   via and(THEM(THEM),D) (1.63e-05, rho=1.42e-01 k*=100)
    - 1.63e-05 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.63e-05, rho=1.42e-01 k*=100)
