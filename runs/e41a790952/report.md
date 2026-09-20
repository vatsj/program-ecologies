### arm=weak, n=7, game=pd, N=100, w=0.1, x_on=True, role=False, mode=sparse, fmap=exp

programs 9426, classes 106, states 624, terminal classes 1, indeterminate 0, divergence rate 0.0113, flow into polymorphic targets 9.14e-08
mean payoff -0.9866, efficient 0.0000, deadweight loss 0.9866, mean bits in support 2.69

| pi | state |
|---|---|
| 0.9759 | mono {D:1} |
| 0.0093 | mono {X:1} |
| 0.0058 | mono {THEM(^C):1} |
| 0.0021 | mono {and(X,X):1} |
| 0.0018 | mono {C:1} |
| 0.0017 | mono {THEM(ME):1} |
| 0.0010 | mono {THEM(^X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 9.95e-05 -> mono {X:1}   via X (9.95e-05, rho=3.21e-04 k*=100)
    - 7.46e-05 -> mono {THEM(ME):1}   via THEM(ME) (7.46e-05, rho=1.00e-02 k*=100)
    - 2.35e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.35e-05, rho=2.48e-02 k*=100)
    - 1.77e-05 -> mono {and(X,X):1}   via and(X,X) (1.77e-05, rho=2.19e-03 k*=100)
    - 1.65e-05 -> mono {THEM(^X):1}   via THEM(^X) (1.65e-05, rho=1.81e-02 k*=100)
    - 9.48e-06 -> mono {THEM(^D):1}   via THEM(^D) (9.48e-06, rho=1.00e-02 k*=100)
- mono {X:1}
    - 1.64e-02 -> mono {D:1}   via D (1.64e-02, rho=5.00e-02 k*=100)
    - 2.21e-04 -> mono {and(X,X):1}   via and(X,X) (2.21e-04, rho=2.73e-02 k*=100)
    - 1.05e-04 -> mono {C:1}   via C (1.05e-04, rho=3.21e-04 k*=100)
    - 2.44e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.44e-05, rho=3.27e-03 k*=100)
    - 1.77e-05 -> mono {or(X,X):1}   via or(X,X) (1.77e-05, rho=2.19e-03 k*=100)
    - 1.71e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.71e-05, rho=1.81e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 4.84e-04 -> mono {X:1}   via X (4.84e-04, rho=1.56e-03 k*=100)
    - 9.19e-05 -> mono {THEM(^D):1}   via THEM(^D) (9.19e-05, rho=9.70e-02 k*=100)
    - 6.06e-05 -> mono {D:1}   via D (6.06e-05, rho=1.84e-04 k*=100)
    - 4.56e-05 -> mono {THEM(^X):1}   via THEM(^X) (4.56e-05, rho=5.00e-02 k*=100)
    - 3.36e-05 -> mono {or(X,X):1}   via or(X,X) (3.36e-05, rho=4.15e-03 k*=100)
- mono {and(X,X):1}
    - 8.98e-03 -> mono {D:1}   via D (8.98e-03, rho=2.73e-02 k*=100)
    - 6.79e-04 -> mono {X:1}   via X (6.79e-04, rho=2.19e-03 k*=100)
    - 4.61e-05 -> mono {THEM(ME):1}   via THEM(ME) (4.61e-05, rho=6.18e-03 k*=100)
    - 2.05e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.05e-05, rho=2.16e-02 k*=100)
    - 1.29e-05 -> mono {THEM(^X):1}   via THEM(^X) (1.29e-05, rho=1.41e-02 k*=100)
    - 1.24e-05 -> mono {C:1}   via C (1.24e-05, rho=3.78e-05 k*=100)
- mono {C:1}
    - 3.19e-02 -> mono {D:1}   via D (3.19e-02, rho=9.70e-02 k*=100)
    - 1.55e-02 -> mono {X:1}   via X (1.55e-02, rho=5.00e-02 k*=100)
    - 5.96e-04 -> mono {and(X,X):1}   via and(X,X) (5.96e-04, rho=7.37e-02 k*=100)
    - 2.21e-04 -> mono {or(X,X):1}   via or(X,X) (2.21e-04, rho=2.73e-02 k*=100)
    - 7.78e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (7.78e-05, rho=9.70e-02 k*=100)
    - 7.75e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.75e-05, rho=9.70e-02 k*=100)
- mono {THEM(ME):1}
    - 2.70e-02 -> mono {C:1}   via C (2.70e-02, rho=8.21e-02 k*=100)
    - 1.18e-02 -> mono {X:1}   via X (1.18e-02, rho=3.79e-02 k*=100)
    - 3.29e-03 -> mono {D:1}   via D (3.29e-03, rho=1.00e-02 k*=100)
    - 4.78e-04 -> mono {or(X,X):1}   via or(X,X) (4.78e-04, rho=5.91e-02 k*=100)
    - 1.70e-04 -> mono {and(X,X):1}   via and(X,X) (1.70e-04, rho=2.10e-02 k*=100)
    - 7.78e-05 -> mono {THEM(^C):1}   via THEM(^C) (7.78e-05, rho=8.21e-02 k*=100)
- mono {THEM(^X):1}
    - 1.25e-02 -> mono {C:1}   via C (1.25e-02, rho=3.79e-02 k*=100)
    - 3.10e-03 -> mono {X:1}   via X (3.10e-03, rho=1.00e-02 k*=100)
    - 5.13e-04 -> mono {D:1}   via D (5.13e-04, rho=1.56e-03 k*=100)
    - 1.70e-04 -> mono {or(X,X):1}   via or(X,X) (1.70e-04, rho=2.10e-02 k*=100)
    - 4.74e-05 -> mono {THEM(^D):1}   via THEM(^D) (4.74e-05, rho=5.00e-02 k*=100)
    - 3.36e-05 -> mono {and(X,X):1}   via and(X,X) (3.36e-05, rho=4.15e-03 k*=100)
