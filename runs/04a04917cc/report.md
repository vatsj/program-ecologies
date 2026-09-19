### arm=weak, n=6, game=pd, N=100, w=0.1, x_on=True, role=False, mode=square, prior=uniform

programs 1852, classes 48, states 134, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 1.59e-05
mean payoff -0.9364, efficient 0.0000, deadweight loss 0.9364, mean bits in support 3.55

| pi | state |
|---|---|
| 0.8790 | mono {D:1} |
| 0.0374 | mono {THEM(^C):1} |
| 0.0143 | mono {and(X,X):1} |
| 0.0102 | mono {X:1} |
| 0.0078 | mono {C:1} |
| 0.0077 | mono {THEM(^X):1} |
| 0.0058 | mono {and(THEM(ME),D):1} |
| 0.0058 | mono {and(THEM(THEM),D):1} |
| 0.0056 | mono {and(X,and(X,X)):1} |
| 0.0039 | mono {and(X,THEM(^C)):1} |
| 0.0031 | mono {and(X,THEM(^X)):1} |
| 0.0023 | mono {THEM(^D):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.95e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.95e-04, rho=2.58e-02 k*=100)
    - 1.22e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.22e-04, rho=1.88e-02 k*=100)
    - 9.06e-05 -> mono {and(X,X):1}   via and(X,X) (9.06e-05, rho=1.82e-03 k*=100)
    - 7.56e-05 -> mono {THEM(^D):1}   via THEM(^D) (7.56e-05, rho=1.00e-02 k*=100)
    - 5.94e-05 -> mono {THEM(ME):1}   via THEM(ME) (5.94e-05, rho=1.00e-02 k*=100)
    - 5.40e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (5.40e-05, rho=1.00e-02 k*=100)
- mono {THEM(^C):1}
    - 3.09e-03 -> mono {C:1}   via C (3.09e-03, rho=1.00e-02 k*=100)
    - 7.14e-04 -> mono {THEM(^D):1}   via THEM(^D) (7.14e-04, rho=9.44e-02 k*=100)
    - 3.22e-04 -> mono {THEM(^X):1}   via THEM(^X) (3.22e-04, rho=4.97e-02 k*=100)
    - 2.57e-04 -> mono {X:1}   via X (2.57e-04, rho=1.46e-03 k*=100)
    - 2.03e-04 -> mono {or(X,X):1}   via or(X,X) (2.03e-04, rho=4.09e-03 k*=100)
    - 5.75e-05 -> mono {or(X,THEM(^D)):1}   via or(X,THEM(^D)) (5.75e-05, rho=5.33e-02 k*=100)
- mono {and(X,X):1}
    - 8.97e-03 -> mono {D:1}   via D (8.97e-03, rho=2.90e-02 k*=100)
    - 3.38e-04 -> mono {X:1}   via X (3.38e-04, rho=1.92e-03 k*=100)
    - 1.68e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.68e-04, rho=2.23e-02 k*=100)
    - 1.19e-04 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.19e-04, rho=1.83e-02 k*=100)
    - 9.36e-05 -> mono {THEM(^X):1}   via THEM(^X) (9.36e-05, rho=1.44e-02 k*=100)
    - 6.27e-05 -> mono {and(THEM(THEM),D):1}   via and(THEM(THEM),D) (6.27e-05, rho=2.90e-02 k*=100)
- mono {X:1}
    - 1.61e-02 -> mono {D:1}   via D (1.61e-02, rho=5.22e-02 k*=100)
    - 1.41e-03 -> mono {and(X,X):1}   via and(X,X) (1.41e-03, rho=2.84e-02 k*=100)
    - 2.60e-04 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (2.60e-04, rho=4.01e-02 k*=100)
    - 1.39e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.39e-04, rho=1.84e-02 k*=100)
    - 1.17e-04 -> mono {and(X,or(X,X)):1}   via and(X,or(X,X)) (1.17e-04, rho=1.81e-02 k*=100)
    - 1.13e-04 -> mono {and(THEM(THEM),D):1}   via and(THEM(THEM),D) (1.13e-04, rho=5.22e-02 k*=100)
- mono {C:1}
    - 2.92e-02 -> mono {D:1}   via D (2.92e-02, rho=9.44e-02 k*=100)
    - 8.75e-03 -> mono {X:1}   via X (8.75e-03, rho=4.97e-02 k*=100)
    - 3.60e-03 -> mono {and(X,X):1}   via and(X,X) (3.60e-03, rho=7.25e-02 k*=100)
    - 1.36e-03 -> mono {or(X,X):1}   via or(X,X) (1.36e-03, rho=2.73e-02 k*=100)
    - 5.42e-04 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (5.42e-04, rho=8.36e-02 k*=100)
    - 5.10e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (5.10e-04, rho=9.44e-02 k*=100)
- mono {THEM(^X):1}
    - 1.20e-02 -> mono {C:1}   via C (1.20e-02, rho=3.87e-02 k*=100)
    - 1.76e-03 -> mono {X:1}   via X (1.76e-03, rho=1.00e-02 k*=100)
    - 1.07e-03 -> mono {or(X,X):1}   via or(X,X) (1.07e-03, rho=2.15e-02 k*=100)
    - 4.01e-04 -> mono {D:1}   via D (4.01e-04, rho=1.30e-03 k*=100)
    - 3.94e-04 -> mono {THEM(^D):1}   via THEM(^D) (3.94e-04, rho=5.22e-02 k*=100)
    - 1.93e-04 -> mono {and(X,X):1}   via and(X,X) (1.93e-04, rho=3.89e-03 k*=100)
- mono {and(THEM(ME),D):1}
    - 3.09e-03 -> mono {D:1}   via D (3.09e-03, rho=1.00e-02 k*=100)
    - 1.95e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.95e-04, rho=2.58e-02 k*=100)
    - 1.22e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.22e-04, rho=1.88e-02 k*=100)
    - 9.06e-05 -> mono {and(X,X):1}   via and(X,X) (9.06e-05, rho=1.82e-03 k*=100)
    - 7.56e-05 -> mono {THEM(^D):1}   via THEM(^D) (7.56e-05, rho=1.00e-02 k*=100)
    - 5.94e-05 -> mono {THEM(ME):1}   via THEM(ME) (5.94e-05, rho=1.00e-02 k*=100)
- mono {and(THEM(THEM),D):1}
    - 3.09e-03 -> mono {D:1}   via D (3.09e-03, rho=1.00e-02 k*=100)
    - 1.95e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.95e-04, rho=2.58e-02 k*=100)
    - 1.22e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.22e-04, rho=1.88e-02 k*=100)
    - 9.06e-05 -> mono {and(X,X):1}   via and(X,X) (9.06e-05, rho=1.82e-03 k*=100)
    - 7.56e-05 -> mono {THEM(^D):1}   via THEM(^D) (7.56e-05, rho=1.00e-02 k*=100)
    - 5.94e-05 -> mono {THEM(ME):1}   via THEM(ME) (5.94e-05, rho=1.00e-02 k*=100)
- mono {and(X,and(X,X)):1}
    - 5.70e-03 -> mono {D:1}   via D (5.70e-03, rho=1.84e-02 k*=100)
    - 2.30e-04 -> mono {and(X,X):1}   via and(X,X) (2.30e-04, rho=4.63e-03 k*=100)
    - 1.82e-04 -> mono {THEM(^C):1}   via THEM(^C) (1.82e-04, rho=2.41e-02 k*=100)
    - 1.21e-04 -> mono {X:1}   via X (1.21e-04, rho=6.85e-04 k*=100)
    - 1.08e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.08e-04, rho=1.67e-02 k*=100)
    - 5.91e-05 -> mono {THEM(^D):1}   via THEM(^D) (5.91e-05, rho=7.82e-03 k*=100)
- mono {and(X,THEM(^C)):1}
    - 1.17e-03 -> mono {D:1}   via D (1.17e-03, rho=3.78e-03 k*=100)
    - 5.55e-04 -> mono {THEM(^D):1}   via THEM(^D) (5.55e-04, rho=7.35e-02 k*=100)
    - 3.38e-04 -> mono {X:1}   via X (3.38e-04, rho=1.92e-03 k*=100)
    - 3.37e-04 -> mono {THEM(^X):1}   via THEM(^X) (3.37e-04, rho=5.20e-02 k*=100)
    - 2.75e-04 -> mono {C:1}   via C (2.75e-04, rho=8.92e-04 k*=100)
    - 2.48e-04 -> mono {THEM(^C):1}   via THEM(^C) (2.48e-04, rho=3.28e-02 k*=100)
- mono {and(X,THEM(^X)):1}
    - 1.93e-03 -> mono {D:1}   via D (1.93e-03, rho=6.24e-03 k*=100)
    - 5.86e-04 -> mono {X:1}   via X (5.86e-04, rho=3.33e-03 k*=100)
    - 4.90e-04 -> mono {C:1}   via C (4.90e-04, rho=1.59e-03 k*=100)
    - 2.89e-04 -> mono {THEM(^D):1}   via THEM(^D) (2.89e-04, rho=3.83e-02 k*=100)
    - 2.30e-04 -> mono {and(X,X):1}   via and(X,X) (2.30e-04, rho=4.63e-03 k*=100)
    - 2.08e-04 -> poly {THEM(ME):0.33, and(X,THEM(^X)):0.67}   via THEM(ME) (2.08e-04, rho=3.50e-02 k*=33)
- mono {THEM(^D):1}
    - 2.67e-02 -> mono {C:1}   via C (2.67e-02, rho=8.63e-02 k*=100)
    - 7.20e-03 -> mono {X:1}   via X (7.20e-03, rho=4.09e-02 k*=100)
    - 3.14e-03 -> mono {or(X,X):1}   via or(X,X) (3.14e-03, rho=6.31e-02 k*=100)
    - 3.09e-03 -> mono {D:1}   via D (3.09e-03, rho=1.00e-02 k*=100)
    - 1.11e-03 -> mono {and(X,X):1}   via and(X,X) (1.11e-03, rho=2.24e-02 k*=100)
    - 9.72e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (9.72e-04, rho=1.80e-01 k*=100)
