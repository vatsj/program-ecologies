### arm=strong, n=6, game=pd, N=100, w=0.01, x_on=True, role=False, mode=square

programs 1726, classes 21, states 25, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 1.88e-08
mean payoff -0.6639, efficient 0.0000, deadweight loss 0.6639, mean bits in support 2.72

| pi | state |
|---|---|
| 0.5061 | mono {D:1} |
| 0.2891 | mono {X:1} |
| 0.1843 | mono {C:1} |
| 0.0094 | mono {and(X,X):1} |
| 0.0057 | mono {or(X,X):1} |
| 0.0031 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.41e-03 -> mono {X:1}   via X (2.41e-03, rho=7.67e-03 k*=100)
    - 1.91e-03 -> mono {C:1}   via C (1.91e-03, rho=5.75e-03 k*=100)
    - 7.00e-05 -> mono {and(X,X):1}   via and(X,X) (7.00e-05, rho=8.78e-03 k*=100)
    - 5.31e-05 -> mono {or(X,X):1}   via or(X,X) (5.31e-05, rho=6.66e-03 k*=100)
    - 3.84e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-05, rho=1.00e-02 k*=100)
    - 3.93e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (3.93e-06, rho=4.61e-03 k*=100)
- mono {X:1}
    - 4.23e-03 -> mono {D:1}   via D (4.23e-03, rho=1.28e-02 k*=100)
    - 2.55e-03 -> mono {C:1}   via C (2.55e-03, rho=7.68e-03 k*=100)
    - 9.03e-05 -> mono {and(X,X):1}   via and(X,X) (9.03e-05, rho=1.13e-02 k*=100)
    - 7.01e-05 -> mono {or(X,X):1}   via or(X,X) (7.01e-05, rho=8.78e-03 k*=100)
    - 3.53e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.53e-05, rho=9.19e-03 k*=100)
    - 7.82e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.82e-06, rho=9.19e-03 k*=100)
- mono {C:1}
    - 5.27e-03 -> mono {D:1}   via D (5.27e-03, rho=1.59e-02 k*=100)
    - 4.00e-03 -> mono {X:1}   via X (4.00e-03, rho=1.27e-02 k*=100)
    - 1.14e-04 -> mono {and(X,X):1}   via and(X,X) (1.14e-04, rho=1.43e-02 k*=100)
    - 9.03e-05 -> mono {or(X,X):1}   via or(X,X) (9.03e-05, rho=1.13e-02 k*=100)
    - 3.22e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.22e-05, rho=8.39e-03 k*=100)
    - 1.35e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.35e-05, rho=1.59e-02 k*=100)
- mono {and(X,X):1}
    - 3.76e-03 -> mono {D:1}   via D (3.76e-03, rho=1.13e-02 k*=100)
    - 2.76e-03 -> mono {X:1}   via X (2.76e-03, rho=8.78e-03 k*=100)
    - 2.21e-03 -> mono {C:1}   via C (2.21e-03, rho=6.67e-03 k*=100)
    - 6.12e-05 -> mono {or(X,X):1}   via or(X,X) (6.12e-05, rho=7.67e-03 k*=100)
    - 3.68e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-05, rho=9.59e-03 k*=100)
    - 5.64e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (5.64e-06, rho=6.63e-03 k*=100)
- mono {or(X,X):1}
    - 4.73e-03 -> mono {D:1}   via D (4.73e-03, rho=1.43e-02 k*=100)
    - 3.56e-03 -> mono {X:1}   via X (3.56e-03, rho=1.13e-02 k*=100)
    - 2.91e-03 -> mono {C:1}   via C (2.91e-03, rho=8.79e-03 k*=100)
    - 1.02e-04 -> mono {and(X,X):1}   via and(X,X) (1.02e-04, rho=1.27e-02 k*=100)
    - 3.37e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.37e-05, rho=8.79e-03 k*=100)
    - 1.05e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (1.05e-05, rho=1.23e-02 k*=100)
- mono {THEM(ME):1}
    - 4.55e-03 -> mono {C:1}   via C (4.55e-03, rho=1.37e-02 k*=100)
    - 3.69e-03 -> mono {X:1}   via X (3.69e-03, rho=1.18e-02 k*=100)
    - 3.32e-03 -> mono {D:1}   via D (3.32e-03, rho=1.00e-02 k*=100)
    - 1.01e-04 -> mono {or(X,X):1}   via or(X,X) (1.01e-04, rho=1.27e-02 k*=100)
    - 8.66e-05 -> mono {and(X,X):1}   via and(X,X) (8.66e-05, rho=1.09e-02 k*=100)
    - 8.51e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.51e-06, rho=1.00e-02 k*=100)
