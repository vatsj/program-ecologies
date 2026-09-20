### arm=strong, n=6, game=pd, N=10, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 1726, classes 21, states 25, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 1.89e-07
mean payoff -0.6763, efficient 0.0000, deadweight loss 0.6763, mean bits in support 2.72

| pi | state |
|---|---|
| 0.5202 | mono {D:1} |
| 0.2852 | mono {X:1} |
| 0.1740 | mono {C:1} |
| 0.0095 | mono {and(X,X):1} |
| 0.0055 | mono {or(X,X):1} |
| 0.0032 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.35e-02 -> mono {X:1}   via X (2.35e-02, rho=7.48e-02 k*=10)
    - 1.80e-02 -> mono {C:1}   via C (1.80e-02, rho=5.43e-02 k*=10)
    - 6.93e-04 -> mono {and(X,X):1}   via and(X,X) (6.93e-04, rho=8.68e-02 k*=10)
    - 5.10e-04 -> mono {or(X,X):1}   via or(X,X) (5.10e-04, rho=6.40e-02 k*=10)
    - 3.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-04, rho=1.00e-01 k*=10)
    - 3.83e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (3.83e-05, rho=4.49e-02 k*=10)
- mono {X:1}
    - 4.30e-02 -> mono {D:1}   via D (4.30e-02, rho=1.30e-01 k*=10)
    - 2.48e-02 -> mono {C:1}   via C (2.48e-02, rho=7.48e-02 k*=10)
    - 9.12e-04 -> mono {and(X,X):1}   via and(X,X) (9.12e-04, rho=1.14e-01 k*=10)
    - 6.93e-04 -> mono {or(X,X):1}   via or(X,X) (6.93e-04, rho=8.68e-02 k*=10)
    - 3.58e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.58e-04, rho=9.33e-02 k*=10)
    - 7.95e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.95e-05, rho=9.33e-02 k*=10)
- mono {C:1}
    - 5.41e-02 -> mono {D:1}   via D (5.41e-02, rho=1.63e-01 k*=10)
    - 4.07e-02 -> mono {X:1}   via X (4.07e-02, rho=1.30e-01 k*=10)
    - 1.16e-03 -> mono {and(X,X):1}   via and(X,X) (1.16e-03, rho=1.46e-01 k*=10)
    - 9.12e-04 -> mono {or(X,X):1}   via or(X,X) (9.12e-04, rho=1.14e-01 k*=10)
    - 3.33e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.33e-04, rho=8.67e-02 k*=10)
    - 1.39e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.39e-04, rho=1.63e-01 k*=10)
- mono {and(X,X):1}
    - 3.79e-02 -> mono {D:1}   via D (3.79e-02, rho=1.14e-01 k*=10)
    - 2.73e-02 -> mono {X:1}   via X (2.73e-02, rho=8.68e-02 k*=10)
    - 2.12e-02 -> mono {C:1}   via C (2.12e-02, rho=6.40e-02 k*=10)
    - 5.97e-04 -> mono {or(X,X):1}   via or(X,X) (5.97e-04, rho=7.48e-02 k*=10)
    - 3.71e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.71e-04, rho=9.67e-02 k*=10)
    - 5.63e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (5.63e-05, rho=6.62e-02 k*=10)
- mono {or(X,X):1}
    - 4.84e-02 -> mono {D:1}   via D (4.84e-02, rho=1.46e-01 k*=10)
    - 3.59e-02 -> mono {X:1}   via X (3.59e-02, rho=1.14e-01 k*=10)
    - 2.88e-02 -> mono {C:1}   via C (2.88e-02, rho=8.68e-02 k*=10)
    - 1.03e-03 -> mono {and(X,X):1}   via and(X,X) (1.03e-03, rho=1.30e-01 k*=10)
    - 3.46e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.46e-04, rho=9.00e-02 k*=10)
    - 1.07e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.07e-04, rho=1.26e-01 k*=10)
- mono {THEM(ME):1}
    - 4.29e-02 -> mono {C:1}   via C (4.29e-02, rho=1.29e-01 k*=10)
    - 3.58e-02 -> mono {X:1}   via X (3.58e-02, rho=1.14e-01 k*=10)
    - 3.32e-02 -> mono {D:1}   via D (3.32e-02, rho=1.00e-01 k*=10)
    - 9.69e-04 -> mono {or(X,X):1}   via or(X,X) (9.69e-04, rho=1.22e-01 k*=10)
    - 8.52e-04 -> mono {and(X,X):1}   via and(X,X) (8.52e-04, rho=1.07e-01 k*=10)
    - 8.51e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.51e-05, rho=1.00e-01 k*=10)
