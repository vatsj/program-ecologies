### arm=weak, n=6, game=exchange, N=100, w=0.1, x_on=True, role=False, mode=square

programs 1852, classes 48, states 382, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 9.62e-06
mean payoff 0.0363, efficient 2.0000, deadweight loss 1.9637, mean bits in support 2.71

| pi | state |
|---|---|
| 0.9717 | mono {D:1} |
| 0.0110 | mono {X:1} |
| 0.0087 | mono {THEM(^C):1} |
| 0.0025 | mono {C:1} |
| 0.0021 | mono {and(X,X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.12e-04 -> mono {X:1}   via X (1.12e-04, rho=3.57e-04 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 3.11e-05 -> mono {THEM(^C):1}   via THEM(^C) (3.11e-05, rho=3.42e-02 k*=100)
    - 2.17e-05 -> mono {THEM(^X):1}   via THEM(^X) (2.17e-05, rho=2.46e-02 k*=100)
    - 1.67e-05 -> mono {and(X,X):1}   via and(X,X) (1.67e-05, rho=2.21e-03 k*=100)
- mono {X:1}
    - 1.52e-02 -> mono {D:1}   via D (1.52e-02, rho=4.63e-02 k*=100)
    - 1.94e-04 -> mono {and(X,X):1}   via and(X,X) (1.94e-04, rho=2.57e-02 k*=100)
    - 1.66e-04 -> mono {C:1}   via C (1.66e-04, rho=5.04e-04 k*=100)
    - 2.14e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.14e-05, rho=2.35e-02 k*=100)
    - 1.95e-05 -> mono {or(X,X):1}   via or(X,X) (1.95e-05, rho=2.58e-03 k*=100)
    - 1.06e-05 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.06e-05, rho=4.63e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 9.70e-05 -> mono {X:1}   via X (9.70e-05, rho=3.11e-04 k*=100)
    - 7.41e-05 -> mono {THEM(^D):1}   via THEM(^D) (7.41e-05, rho=8.14e-02 k*=100)
    - 3.78e-05 -> mono {THEM(^X):1}   via THEM(^X) (3.78e-05, rho=4.28e-02 k*=100)
    - 1.57e-05 -> mono {or(X,X):1}   via or(X,X) (1.57e-05, rho=2.08e-03 k*=100)
    - 1.35e-06 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (1.35e-06, rho=4.80e-03 k*=100)
- mono {C:1}
    - 2.68e-02 -> mono {D:1}   via D (2.68e-02, rho=8.14e-02 k*=100)
    - 1.34e-02 -> mono {X:1}   via X (1.34e-02, rho=4.28e-02 k*=100)
    - 4.70e-04 -> mono {and(X,X):1}   via and(X,X) (4.70e-04, rho=6.23e-02 k*=100)
    - 1.82e-04 -> mono {or(X,X):1}   via or(X,X) (1.82e-04, rho=2.42e-02 k*=100)
    - 6.48e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (6.48e-05, rho=8.14e-02 k*=100)
    - 6.48e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (6.48e-05, rho=8.14e-02 k*=100)
- mono {and(X,X):1}
    - 8.77e-03 -> mono {D:1}   via D (8.77e-03, rho=2.67e-02 k*=100)
    - 7.49e-04 -> mono {X:1}   via X (7.49e-04, rho=2.40e-03 k*=100)
    - 2.65e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.65e-05, rho=2.91e-02 k*=100)
    - 2.23e-05 -> mono {C:1}   via C (2.23e-05, rho=6.77e-05 k*=100)
    - 1.56e-05 -> mono {THEM(^X):1}   via THEM(^X) (1.56e-05, rho=1.76e-02 k*=100)
    - 1.27e-05 -> mono {THEM(ME):1}   via THEM(ME) (1.27e-05, rho=3.44e-03 k*=100)
