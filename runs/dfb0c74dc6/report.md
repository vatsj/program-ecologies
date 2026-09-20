### arm=weak, n=5, game=ult, N=100, w=0.1, x_on=True, role=True, mode=square, fmap=exp

programs 1586, classes 81, states 576, terminal classes 1, indeterminate 0, divergence rate 0.0005, flow into polymorphic targets 5.13e-04
mean payoff 0.4568, efficient 0.5000, deadweight loss 0.0432, mean bits in support 3.56

| pi | state |
|---|---|
| 0.3722 | mono {M:1} |
| 0.3490 | mono {L:1} |
| 0.0925 | mono {H:1} |
| 0.0650 | mono {X:1} |
| 0.0437 | mono {ROLE:1} |
| 0.0286 | poly {X:0.9, flip(ROLE):0.1} |
| 0.0058 | mono {min(M,X):1} |
| 0.0058 | mono {flip(ROLE):1} |
| 0.0056 | poly {ROLE:0.6, flip(ROLE):0.4} |
| 0.0026 | poly {X:0.9, min(M,ROLE):0.1} |
| 0.0025 | mono {max(M,X):1} |
| 0.0022 | poly {ROLE:0.59, flip(ROLE):0.4, min(M,ROLE):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {M:1}
    - 1.30e-03 -> mono {L:1}   via L (1.30e-03, rho=6.54e-03 k*=100)
    - 7.68e-04 -> mono {X:1}   via X (7.68e-04, rho=4.21e-03 k*=100)
    - 5.69e-04 -> mono {H:1}   via H (5.69e-04, rho=2.85e-03 k*=100)
    - 2.33e-04 -> mono {ROLE:1}   via ROLE (2.33e-04, rho=1.56e-03 k*=100)
    - 1.60e-04 -> mono {flip(ROLE):1}   via flip(ROLE) (1.60e-04, rho=4.30e-03 k*=100)
    - 3.69e-05 -> mono {min(M,X):1}   via min(M,X) (3.69e-05, rho=7.19e-03 k*=100)
- mono {L:1}
    - 1.23e-03 -> mono {M:1}   via M (1.23e-03, rho=6.54e-03 k*=100)
    - 8.95e-04 -> mono {ROLE:1}   via ROLE (8.95e-04, rho=5.99e-03 k*=100)
    - 7.68e-04 -> mono {X:1}   via X (7.68e-04, rho=4.21e-03 k*=100)
    - 5.69e-04 -> mono {H:1}   via H (5.69e-04, rho=2.85e-03 k*=100)
    - 5.82e-05 -> mono {flip(ROLE):1}   via flip(ROLE) (5.82e-05, rho=1.56e-03 k*=100)
    - 3.21e-05 -> mono {min(M,X):1}   via min(M,X) (3.21e-05, rho=6.26e-03 k*=100)
- mono {H:1}
    - 2.55e-03 -> mono {L:1}   via L (2.55e-03, rho=1.28e-02 k*=100)
    - 2.40e-03 -> mono {M:1}   via M (2.40e-03, rho=1.28e-02 k*=100)
    - 1.74e-03 -> mono {X:1}   via X (1.74e-03, rho=9.53e-03 k*=100)
    - 8.95e-04 -> mono {ROLE:1}   via ROLE (8.95e-04, rho=5.99e-03 k*=100)
    - 3.73e-04 -> mono {flip(ROLE):1}   via flip(ROLE) (3.73e-04, rho=1.00e-02 k*=100)
    - 5.76e-05 -> mono {min(M,X):1}   via min(M,X) (5.76e-05, rho=1.12e-02 k*=100)
- mono {X:1}
    - 3.74e-03 -> poly {X:0.9, flip(ROLE):0.1}   via flip(ROLE) (3.74e-03, rho=1.00e-01 k*=10)
    - 3.13e-03 -> mono {L:1}   via L (3.13e-03, rho=1.57e-02 k*=100)
    - 2.95e-03 -> mono {M:1}   via M (2.95e-03, rho=1.57e-02 k*=100)
    - 1.58e-03 -> mono {H:1}   via H (1.58e-03, rho=7.94e-03 k*=100)
    - 1.07e-03 -> mono {ROLE:1}   via ROLE (1.07e-03, rho=7.16e-03 k*=100)
    - 4.18e-04 -> poly {X:0.9, min(M,ROLE):0.1}   via min(M,ROLE) (4.18e-04, rho=1.01e-01 k*=10)
- mono {ROLE:1}
    - 3.40e-03 -> mono {M:1}   via M (3.40e-03, rho=1.81e-02 k*=100)
    - 3.09e-03 -> mono {H:1}   via H (3.09e-03, rho=1.55e-02 k*=100)
    - 3.09e-03 -> mono {L:1}   via L (3.09e-03, rho=1.55e-02 k*=100)
    - 2.46e-03 -> mono {X:1}   via X (2.46e-03, rho=1.35e-02 k*=100)
    - 1.19e-03 -> poly {ROLE:0.6, flip(ROLE):0.4}   via flip(ROLE) (1.19e-03, rho=3.19e-02 k*=40)
    - 7.98e-05 -> mono {max(M,X):1}   via max(M,X) (7.98e-05, rho=1.55e-02 k*=100)
- poly {X:0.9, flip(ROLE):0.1}
    - 3.26e-03 -> mono {L:1}   via L (3.26e-03, rho=1.63e-02 k*=100)
    - 2.89e-03 -> mono {M:1}   via M (2.89e-03, rho=1.54e-02 k*=100)
    - 1.54e-03 -> mono {H:1}   via H (1.54e-03, rho=7.72e-03 k*=100)
    - 1.13e-03 -> mono {ROLE:1}   via ROLE (1.13e-03, rho=7.55e-03 k*=100)
    - 2.02e-04 -> poly {X:0.64, flip(ROLE):0.14, min(M,ROLE):0.22}   via min(M,ROLE) (2.02e-04, rho=4.86e-02 k*=21)
    - 8.80e-05 -> poly {X:0.9, flip(ROLE):0.07, THEM(^ROLE):0.03}   via THEM(^ROLE) (8.80e-05, rho=3.34e-01 k*=3)
- mono {min(M,X):1}
    - 2.33e-03 -> mono {M:1}   via M (2.33e-03, rho=1.24e-02 k*=100)
    - 2.15e-03 -> mono {L:1}   via L (2.15e-03, rho=1.08e-02 k*=100)
    - 1.16e-03 -> mono {X:1}   via X (1.16e-03, rho=6.34e-03 k*=100)
    - 8.62e-04 -> mono {H:1}   via H (8.62e-04, rho=4.32e-03 k*=100)
    - 5.70e-04 -> mono {ROLE:1}   via ROLE (5.70e-04, rho=3.81e-03 k*=100)
    - 1.80e-04 -> mono {flip(ROLE):1}   via flip(ROLE) (1.80e-04, rho=4.82e-03 k*=100)
- mono {flip(ROLE):1}
    - 6.26e-03 -> mono {L:1}   via L (6.26e-03, rho=3.14e-02 k*=100)
    - 4.39e-03 -> poly {ROLE:0.6, flip(ROLE):0.4}   via ROLE (4.39e-03, rho=2.93e-02 k*=60)
    - 3.62e-03 -> mono {M:1}   via M (3.62e-03, rho=1.93e-02 k*=100)
    - 3.12e-03 -> poly {X:0.9, flip(ROLE):0.1}   via X (3.12e-03, rho=1.71e-02 k*=90)
    - 1.99e-03 -> mono {H:1}   via H (1.99e-03, rho=1.00e-02 k*=100)
    - 1.61e-04 -> poly {flip(ROLE):0.7, max(M,ROLE):0.3}   via max(M,ROLE) (1.61e-04, rho=3.87e-02 k*=30)
- poly {ROLE:0.6, flip(ROLE):0.4}
    - 4.16e-03 -> poly {ROLE:0.59, flip(ROLE):0.4, min(M,ROLE):0.01}   via min(M,ROLE) (4.16e-03, rho=1.00e+00 k*=1)
    - 3.08e-03 -> mono {L:1}   via L (3.08e-03, rho=1.55e-02 k*=100)
    - 2.55e-03 -> mono {M:1}   via M (2.55e-03, rho=1.36e-02 k*=100)
    - 1.99e-03 -> poly {X:0.9, flip(ROLE):0.1}   via X (1.99e-03, rho=1.09e-02 k*=90)
    - 1.79e-03 -> mono {H:1}   via H (1.79e-03, rho=8.98e-03 k*=100)
    - 8.06e-05 -> poly {ROLE:0.59, flip(ROLE):0.4, min(ROLE,max(M,X)):0.01}   via min(ROLE,max(M,X)) (8.06e-05, rho=1.00e+00 k*=1)
- poly {X:0.9, min(M,ROLE):0.1}
    - 3.00e-03 -> mono {M:1}   via M (3.00e-03, rho=1.60e-02 k*=100)
    - 3.00e-03 -> mono {L:1}   via L (3.00e-03, rho=1.50e-02 k*=100)
    - 2.68e-03 -> poly {X:0.64, flip(ROLE):0.14, min(M,ROLE):0.22}   via flip(ROLE) (2.68e-03, rho=7.18e-02 k*=14)
    - 1.62e-03 -> mono {H:1}   via H (1.62e-03, rho=8.11e-03 k*=100)
    - 1.05e-03 -> mono {ROLE:1}   via ROLE (1.05e-03, rho=7.04e-03 k*=100)
    - 7.02e-05 -> mono {min(M,X):1}   via min(M,X) (7.02e-05, rho=1.37e-02 k*=100)
- mono {max(M,X):1}
    - 3.74e-03 -> poly {flip(ROLE):0.1, max(M,X):0.9}   via flip(ROLE) (3.74e-03, rho=1.00e-01 k*=10)
    - 2.89e-03 -> mono {M:1}   via M (2.89e-03, rho=1.54e-02 k*=100)
    - 2.33e-03 -> mono {L:1}   via L (2.33e-03, rho=1.17e-02 k*=100)
    - 1.52e-03 -> mono {X:1}   via X (1.52e-03, rho=8.31e-03 k*=100)
    - 1.31e-03 -> mono {H:1}   via H (1.31e-03, rho=6.56e-03 k*=100)
    - 5.70e-04 -> mono {ROLE:1}   via ROLE (5.70e-04, rho=3.81e-03 k*=100)
- poly {ROLE:0.59, flip(ROLE):0.4, min(M,ROLE):0.01}
    - 3.08e-03 -> mono {L:1}   via L (3.08e-03, rho=1.55e-02 k*=100)
    - 2.78e-03 -> poly {X:0.64, flip(ROLE):0.14, min(M,ROLE):0.22}   via X (2.78e-03, rho=1.52e-02 k*=64)
    - 2.56e-03 -> mono {M:1}   via M (2.56e-03, rho=1.36e-02 k*=100)
    - 1.79e-03 -> mono {H:1}   via H (1.79e-03, rho=8.98e-03 k*=100)
    - 8.06e-05 -> poly {ROLE:0.58, flip(ROLE):0.4, min(M,ROLE):0.01, min(ROLE,max(M,X)):0.01}   via min(ROLE,max(M,X)) (8.06e-05, rho=1.00e+00 k*=1)
    - 6.40e-05 -> mono {min(M,X):1}   via min(M,X) (6.40e-05, rho=1.25e-02 k*=100)
