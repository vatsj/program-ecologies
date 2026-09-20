### arm=weak, n=6, game=pd, N=100, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 48, states 119, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 9.22e-08
mean payoff -0.9868, efficient 0.0000, deadweight loss 0.9868, mean bits in support 2.69

| pi | state |
|---|---|
| 0.9766 | mono {D:1} |
| 0.0093 | mono {X:1} |
| 0.0056 | mono {THEM(^C):1} |
| 0.0020 | mono {and(X,X):1} |
| 0.0018 | mono {C:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.00e-04 -> mono {X:1}   via X (1.00e-04, rho=3.21e-04 k*=100)
    - 3.68e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 2.25e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.25e-05, rho=2.48e-02 k*=100)
    - 1.65e-05 -> mono {and(X,X):1}   via and(X,X) (1.65e-05, rho=2.19e-03 k*=100)
    - 1.60e-05 -> mono {THEM(^X):1}   via THEM(^X) (1.60e-05, rho=1.81e-02 k*=100)
- mono {X:1}
    - 1.65e-02 -> mono {D:1}   via D (1.65e-02, rho=5.00e-02 k*=100)
    - 2.06e-04 -> mono {and(X,X):1}   via and(X,X) (2.06e-04, rho=2.73e-02 k*=100)
    - 1.05e-04 -> mono {C:1}   via C (1.05e-04, rho=3.21e-04 k*=100)
    - 1.65e-05 -> mono {or(X,X):1}   via or(X,X) (1.65e-05, rho=2.19e-03 k*=100)
    - 1.65e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.65e-05, rho=1.81e-02 k*=100)
    - 1.20e-05 -> mono {THEM(ME):1}   via THEM(ME) (1.20e-05, rho=3.27e-03 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 4.87e-04 -> mono {X:1}   via X (4.87e-04, rho=1.56e-03 k*=100)
    - 8.83e-05 -> mono {THEM(^D):1}   via THEM(^D) (8.83e-05, rho=9.70e-02 k*=100)
    - 6.07e-05 -> mono {D:1}   via D (6.07e-05, rho=1.84e-04 k*=100)
    - 4.42e-05 -> mono {THEM(^X):1}   via THEM(^X) (4.42e-05, rho=5.00e-02 k*=100)
    - 3.13e-05 -> mono {or(X,X):1}   via or(X,X) (3.13e-05, rho=4.15e-03 k*=100)
- mono {and(X,X):1}
    - 8.98e-03 -> mono {D:1}   via D (8.98e-03, rho=2.73e-02 k*=100)
    - 6.83e-04 -> mono {X:1}   via X (6.83e-04, rho=2.19e-03 k*=100)
    - 2.27e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.27e-05, rho=6.18e-03 k*=100)
    - 2.27e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.27e-05, rho=6.18e-03 k*=100)
    - 1.97e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.97e-05, rho=2.16e-02 k*=100)
    - 1.25e-05 -> mono {THEM(^X):1}   via THEM(^X) (1.25e-05, rho=1.41e-02 k*=100)
- mono {C:1}
    - 3.19e-02 -> mono {D:1}   via D (3.19e-02, rho=9.70e-02 k*=100)
    - 1.56e-02 -> mono {X:1}   via X (1.56e-02, rho=5.00e-02 k*=100)
    - 5.56e-04 -> mono {and(X,X):1}   via and(X,X) (5.56e-04, rho=7.37e-02 k*=100)
    - 2.06e-04 -> mono {or(X,X):1}   via or(X,X) (2.06e-04, rho=2.73e-02 k*=100)
    - 7.72e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (7.72e-05, rho=9.70e-02 k*=100)
    - 7.72e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.72e-05, rho=9.70e-02 k*=100)
