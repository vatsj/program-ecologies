### arm=weak, n=7, game=pd, N=100, w=0.1, x_on=True, role=False, mode=sparse

programs 9426, classes 105, states 626, terminal classes 1, indeterminate 0, divergence rate 0.0113, flow into polymorphic targets 9.40e-08
mean payoff -0.9873, efficient 0.0000, deadweight loss 0.9873, mean bits in support 2.69

| pi | state |
|---|---|
| 0.9781 | mono {D:1} |
| 0.0073 | mono {X:1} |
| 0.0061 | mono {THEM(^C):1} |
| 0.0018 | mono {C:1} |
| 0.0017 | mono {and(X,X):1} |
| 0.0016 | mono {THEM(ME):1} |
| 0.0010 | mono {THEM(^X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 7.46e-05 -> mono {THEM(ME):1}   via THEM(ME) (7.46e-05, rho=1.00e-02 k*=100)
    - 6.84e-05 -> mono {X:1}   via X (6.84e-05, rho=2.20e-04 k*=100)
    - 2.45e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.45e-05, rho=2.58e-02 k*=100)
    - 1.71e-05 -> mono {THEM(^X):1}   via THEM(^X) (1.71e-05, rho=1.88e-02 k*=100)
    - 1.47e-05 -> mono {and(X,X):1}   via and(X,X) (1.47e-05, rho=1.82e-03 k*=100)
    - 9.48e-06 -> mono {THEM(^D):1}   via THEM(^D) (9.48e-06, rho=1.00e-02 k*=100)
- mono {X:1}
    - 1.71e-02 -> mono {D:1}   via D (1.71e-02, rho=5.22e-02 k*=100)
    - 2.30e-04 -> mono {and(X,X):1}   via and(X,X) (2.30e-04, rho=2.84e-02 k*=100)
    - 9.15e-05 -> mono {C:1}   via C (9.15e-05, rho=2.78e-04 k*=100)
    - 2.21e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.21e-05, rho=2.96e-03 k*=100)
    - 1.74e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.74e-05, rho=1.84e-02 k*=100)
    - 1.64e-05 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.64e-05, rho=5.22e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 4.52e-04 -> mono {X:1}   via X (4.52e-04, rho=1.46e-03 k*=100)
    - 8.95e-05 -> mono {THEM(^D):1}   via THEM(^D) (8.95e-05, rho=9.44e-02 k*=100)
    - 4.53e-05 -> mono {THEM(^X):1}   via THEM(^X) (4.53e-05, rho=4.97e-02 k*=100)
    - 4.44e-05 -> mono {D:1}   via D (4.44e-05, rho=1.35e-04 k*=100)
    - 3.31e-05 -> mono {or(X,X):1}   via or(X,X) (3.31e-05, rho=4.09e-03 k*=100)
- mono {C:1}
    - 3.10e-02 -> mono {D:1}   via D (3.10e-02, rho=9.44e-02 k*=100)
    - 1.54e-02 -> mono {X:1}   via X (1.54e-02, rho=4.97e-02 k*=100)
    - 5.86e-04 -> mono {and(X,X):1}   via and(X,X) (5.86e-04, rho=7.25e-02 k*=100)
    - 2.21e-04 -> mono {or(X,X):1}   via or(X,X) (2.21e-04, rho=2.73e-02 k*=100)
    - 7.58e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (7.58e-05, rho=9.44e-02 k*=100)
    - 7.54e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.54e-05, rho=9.44e-02 k*=100)
- mono {and(X,X):1}
    - 9.55e-03 -> mono {D:1}   via D (9.55e-03, rho=2.90e-02 k*=100)
    - 5.97e-04 -> mono {X:1}   via X (5.97e-04, rho=1.92e-03 k*=100)
    - 4.39e-05 -> mono {THEM(ME):1}   via THEM(ME) (4.39e-05, rho=5.88e-03 k*=100)
    - 2.11e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.11e-05, rho=2.23e-02 k*=100)
    - 1.32e-05 -> mono {THEM(^X):1}   via THEM(^X) (1.32e-05, rho=1.44e-02 k*=100)
    - 9.15e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (9.15e-06, rho=2.90e-02 k*=100)
- mono {THEM(ME):1}
    - 2.84e-02 -> mono {C:1}   via C (2.84e-02, rho=8.63e-02 k*=100)
    - 1.27e-02 -> mono {X:1}   via X (1.27e-02, rho=4.09e-02 k*=100)
    - 3.29e-03 -> mono {D:1}   via D (3.29e-03, rho=1.00e-02 k*=100)
    - 5.11e-04 -> mono {or(X,X):1}   via or(X,X) (5.11e-04, rho=6.31e-02 k*=100)
    - 1.81e-04 -> mono {and(X,X):1}   via and(X,X) (1.81e-04, rho=2.24e-02 k*=100)
    - 8.18e-05 -> mono {THEM(^C):1}   via THEM(^C) (8.18e-05, rho=8.63e-02 k*=100)
- mono {THEM(^X):1}
    - 1.27e-02 -> mono {C:1}   via C (1.27e-02, rho=3.87e-02 k*=100)
    - 3.10e-03 -> mono {X:1}   via X (3.10e-03, rho=1.00e-02 k*=100)
    - 4.27e-04 -> mono {D:1}   via D (4.27e-04, rho=1.30e-03 k*=100)
    - 1.74e-04 -> mono {or(X,X):1}   via or(X,X) (1.74e-04, rho=2.15e-02 k*=100)
    - 4.94e-05 -> mono {THEM(^D):1}   via THEM(^D) (4.94e-05, rho=5.22e-02 k*=100)
    - 3.14e-05 -> mono {and(X,X):1}   via and(X,X) (3.14e-05, rho=3.89e-03 k*=100)
