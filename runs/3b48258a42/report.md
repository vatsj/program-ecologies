### arm=weak, n=6, game=exchange, N=100, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 48, states 402, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 9.68e-06
mean payoff 0.0338, efficient 2.0000, deadweight loss 1.9662, mean bits in support 2.71

| pi | state |
|---|---|
| 0.9740 | mono {D:1} |
| 0.0092 | mono {X:1} |
| 0.0089 | mono {THEM(^C):1} |
| 0.0021 | mono {C:1} |
| 0.0020 | mono {and(X,X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 9.62e-05 -> mono {X:1}   via X (9.62e-05, rho=3.08e-04 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 3.15e-05 -> mono {THEM(^C):1}   via THEM(^C) (3.15e-05, rho=3.46e-02 k*=100)
    - 2.19e-05 -> mono {THEM(^X):1}   via THEM(^X) (2.19e-05, rho=2.48e-02 k*=100)
    - 1.62e-05 -> mono {and(X,X):1}   via and(X,X) (1.62e-05, rho=2.15e-03 k*=100)
- mono {X:1}
    - 1.66e-02 -> mono {D:1}   via D (1.66e-02, rho=5.05e-02 k*=100)
    - 2.08e-04 -> mono {and(X,X):1}   via and(X,X) (2.08e-04, rho=2.75e-02 k*=100)
    - 1.01e-04 -> mono {C:1}   via C (1.01e-04, rho=3.08e-04 k*=100)
    - 2.25e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.25e-05, rho=2.48e-02 k*=100)
    - 1.62e-05 -> mono {or(X,X):1}   via or(X,X) (1.62e-05, rho=2.15e-03 k*=100)
    - 1.16e-05 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.16e-05, rho=5.05e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 8.91e-05 -> mono {THEM(^D):1}   via THEM(^D) (8.91e-05, rho=9.79e-02 k*=100)
    - 5.76e-05 -> mono {X:1}   via X (5.76e-05, rho=1.84e-04 k*=100)
    - 4.46e-05 -> mono {THEM(^X):1}   via THEM(^X) (4.46e-05, rho=5.05e-02 k*=100)
    - 1.18e-05 -> mono {or(X,X):1}   via or(X,X) (1.18e-05, rho=1.56e-03 k*=100)
    - 1.52e-06 -> mono {or(X,THEM(^D)):1}   via or(X,THEM(^D)) (1.52e-06, rho=5.73e-02 k*=100)
- mono {C:1}
    - 3.22e-02 -> mono {D:1}   via D (3.22e-02, rho=9.79e-02 k*=100)
    - 1.58e-02 -> mono {X:1}   via X (1.58e-02, rho=5.05e-02 k*=100)
    - 5.61e-04 -> mono {and(X,X):1}   via and(X,X) (5.61e-04, rho=7.44e-02 k*=100)
    - 2.08e-04 -> mono {or(X,X):1}   via or(X,X) (2.08e-04, rho=2.75e-02 k*=100)
    - 7.79e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (7.79e-05, rho=9.79e-02 k*=100)
    - 7.79e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.79e-05, rho=9.79e-02 k*=100)
- mono {and(X,X):1}
    - 9.05e-03 -> mono {D:1}   via D (9.05e-03, rho=2.75e-02 k*=100)
    - 6.71e-04 -> mono {X:1}   via X (6.71e-04, rho=2.15e-03 k*=100)
    - 2.74e-05 -> mono {THEM(^C):1}   via THEM(^C) (2.74e-05, rho=3.01e-02 k*=100)
    - 1.60e-05 -> mono {THEM(^X):1}   via THEM(^X) (1.60e-05, rho=1.81e-02 k*=100)
    - 1.21e-05 -> mono {THEM(ME):1}   via THEM(ME) (1.21e-05, rho=3.27e-03 k*=100)
    - 1.20e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (1.20e-05, rho=3.27e-03 k*=100)
