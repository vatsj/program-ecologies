### arm=weak, n=6, game=pd, N=100, w=0.1, x_on=True, role=False, mode=square

programs 1852, classes 48, states 118, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 9.88e-08
mean payoff -0.9876, efficient 0.0000, deadweight loss 0.9876, mean bits in support 2.69

| pi | state |
|---|---|
| 0.9787 | mono {D:1} |
| 0.0073 | mono {X:1} |
| 0.0059 | mono {THEM(^C):1} |
| 0.0018 | mono {C:1} |
| 0.0016 | mono {and(X,X):1} |
| 0.0010 | mono {THEM(^X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 6.89e-05 -> mono {X:1}   via X (6.89e-05, rho=2.20e-04 k*=100)
    - 3.68e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 2.35e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.35e-05, rho=2.58e-02 k*=100)
    - 1.66e-05 -> mono {THEM(^X):1}   via THEM(^X) (1.66e-05, rho=1.88e-02 k*=100)
    - 1.38e-05 -> mono {and(X,X):1}   via and(X,X) (1.38e-05, rho=1.82e-03 k*=100)
- mono {X:1}
    - 1.72e-02 -> mono {D:1}   via D (1.72e-02, rho=5.22e-02 k*=100)
    - 2.14e-04 -> mono {and(X,X):1}   via and(X,X) (2.14e-04, rho=2.84e-02 k*=100)
    - 9.16e-05 -> mono {C:1}   via C (9.16e-05, rho=2.78e-04 k*=100)
    - 1.67e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.67e-05, rho=1.84e-02 k*=100)
    - 1.52e-05 -> mono {or(X,X):1}   via or(X,X) (1.52e-05, rho=2.02e-03 k*=100)
    - 1.13e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.13e-05, rho=4.01e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 4.55e-04 -> mono {X:1}   via X (4.55e-04, rho=1.46e-03 k*=100)
    - 8.59e-05 -> mono {THEM(^D):1}   via THEM(^D) (8.59e-05, rho=9.44e-02 k*=100)
    - 4.44e-05 -> mono {D:1}   via D (4.44e-05, rho=1.35e-04 k*=100)
    - 4.39e-05 -> mono {THEM(^X):1}   via THEM(^X) (4.39e-05, rho=4.97e-02 k*=100)
    - 3.08e-05 -> mono {or(X,X):1}   via or(X,X) (3.08e-05, rho=4.09e-03 k*=100)
- mono {C:1}
    - 3.11e-02 -> mono {D:1}   via D (3.11e-02, rho=9.44e-02 k*=100)
    - 1.55e-02 -> mono {X:1}   via X (1.55e-02, rho=4.97e-02 k*=100)
    - 5.47e-04 -> mono {and(X,X):1}   via and(X,X) (5.47e-04, rho=7.25e-02 k*=100)
    - 2.06e-04 -> mono {or(X,X):1}   via or(X,X) (2.06e-04, rho=2.73e-02 k*=100)
    - 7.51e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (7.51e-05, rho=9.44e-02 k*=100)
    - 7.51e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.51e-05, rho=9.44e-02 k*=100)
- mono {and(X,X):1}
    - 9.55e-03 -> mono {D:1}   via D (9.55e-03, rho=2.90e-02 k*=100)
    - 6.01e-04 -> mono {X:1}   via X (6.01e-04, rho=1.92e-03 k*=100)
    - 2.16e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.16e-05, rho=5.88e-03 k*=100)
    - 2.15e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.15e-05, rho=5.88e-03 k*=100)
    - 2.03e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.03e-05, rho=2.23e-02 k*=100)
    - 1.28e-05 -> mono {THEM(^X):1}   via THEM(^X) (1.28e-05, rho=1.44e-02 k*=100)
- mono {THEM(^X):1}
    - 1.27e-02 -> mono {C:1}   via C (1.27e-02, rho=3.87e-02 k*=100)
    - 3.12e-03 -> mono {X:1}   via X (3.12e-03, rho=1.00e-02 k*=100)
    - 4.27e-04 -> mono {D:1}   via D (4.27e-04, rho=1.30e-03 k*=100)
    - 1.63e-04 -> mono {or(X,X):1}   via or(X,X) (1.63e-04, rho=2.15e-02 k*=100)
    - 4.75e-05 -> mono {THEM(^D):1}   via THEM(^D) (4.75e-05, rho=5.22e-02 k*=100)
    - 2.93e-05 -> mono {and(X,X):1}   via and(X,X) (2.93e-05, rho=3.89e-03 k*=100)
