### arm=weak, n=6, game=pd, N=10, x_on=True, role=False, mode=square

programs 1852, classes 48, states 4200, terminal classes 1, indeterminate 74, divergence rate 0.0019
mean payoff -0.6843, efficient 0.0000, deadweight loss 0.6843, mean bits in support 4.67

| pi | state |
|---|---|
| 0.5757 | mono {D:1} |
| 0.0784 | neutral {C:0.3, THEM(^C):0.7} |
| 0.0688 | neutral {C:0.2, THEM(^C):0.8} |
| 0.0667 | neutral {C:0.4, THEM(^C):0.6} |
| 0.0366 | neutral {C:0.5, THEM(^C):0.5} |
| 0.0309 | neutral {C:0.1, THEM(^C):0.9} |
| 0.0210 | neutral {D:0.9, THEM(ME):0.1} |
| 0.0208 | neutral {D:0.9, THEM(THEM):0.1} |
| 0.0090 | mono {THEM(^C):1} |
| 0.0078 | neutral {D:0.8, THEM(ME):0.2} |
| 0.0078 | neutral {D:0.8, THEM(THEM):0.2} |
| 0.0077 | neutral {C:0.6, THEM(^C):0.4} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.68e-03 -> neutral {D:0.9, THEM(ME):0.1}   via THEM(ME) (3.68e-03)
    - 3.67e-03 -> neutral {D:0.9, THEM(THEM):0.1}   via THEM(THEM) (3.67e-03)
    - 9.10e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-04)
    - 9.10e-04 -> neutral {D:0.9, THEM(^D):0.1}   via THEM(^D) (9.10e-04)
    - 8.83e-04 -> mono {THEM(^X):1}   via THEM(^X) (8.83e-04)
    - 1.15e-04 -> neutral {D:0.9, and(THEM(THEM),D):0.1}   via and(THEM(THEM),D) (1.15e-04)
- neutral {C:0.3, THEM(^C):0.7}
    - 3.86e-01 -> neutral {C:0.4, THEM(^C):0.6}   via C (2.30e-01), D (7.68e-02), X (7.29e-02), and(X,X) (1.76e-03)
    - 1.56e-01 -> neutral {C:0.2, THEM(^C):0.8}   via D (7.68e-02), X (7.29e-02), and(X,X) (1.76e-03), or(X,X) (1.76e-03)
    - 9.10e-04 -> poly {C:1, THEM(^C):2.45e-19, THEM(^D):2.17e-19}   via THEM(^D) (9.10e-04)
    - 8.83e-04 -> poly {C:1, THEM(^X):1.99e-08}   via THEM(^X) (8.83e-04)
    - 6.16e-05 -> poly {C:0.3, THEM(^C):0.6, and(THEM(ME),X):0.1}   via and(THEM(ME),X) (6.16e-05)
    - 6.16e-05 -> neutral {C:0.3, THEM(^C):0.6, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (6.16e-05)
- neutral {C:0.2, THEM(^C):0.8}
    - 3.82e-01 -> neutral {C:0.3, THEM(^C):0.7}   via C (2.63e-01), D (5.85e-02), X (5.55e-02), and(X,X) (1.34e-03)
    - 1.19e-01 -> neutral {C:0.1, THEM(^C):0.9}   via D (5.85e-02), X (5.55e-02), and(X,X) (1.34e-03), or(X,X) (1.34e-03)
    - 9.10e-04 -> poly {C:1, THEM(^C):2.45e-19, THEM(^D):2.17e-19}   via THEM(^D) (9.10e-04)
    - 8.83e-04 -> poly {C:1, THEM(^X):1.99e-08}   via THEM(^X) (8.83e-04)
    - 7.04e-05 -> neutral {C:0.2, THEM(^C):0.7, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (7.04e-05)
    - 7.04e-05 -> neutral {C:0.2, THEM(^C):0.7, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (7.04e-05)
- neutral {C:0.4, THEM(^C):0.6}
    - 3.75e-01 -> neutral {C:0.5, THEM(^C):0.5}   via C (1.97e-01), D (8.77e-02), X (8.33e-02), and(X,X) (2.01e-03)
    - 1.78e-01 -> neutral {C:0.3, THEM(^C):0.7}   via D (8.77e-02), X (8.33e-02), and(X,X) (2.01e-03), or(X,X) (2.01e-03)
    - 9.10e-04 -> poly {C:1, THEM(^C):2.45e-19, THEM(^D):2.17e-19}   via THEM(^D) (9.10e-04)
    - 8.83e-04 -> poly {C:1, THEM(^X):1.99e-08}   via THEM(^X) (8.83e-04)
    - 5.28e-05 -> poly {C:0.00396, THEM(^C):0.00792, and(THEM(ME),X):0.988}   via and(THEM(ME),X) (5.28e-05)
    - 5.28e-05 -> neutral {C:0.4, THEM(^C):0.5, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (5.28e-05)
- neutral {C:0.5, THEM(^C):0.5}
    - 2.31e-01 -> neutral {C:0.2, THEM(^C):0.8}   via D (1.15e-01), X (1.09e-01), and(X,X) (2.64e-03), or(X,X) (2.64e-03)
    - 1.86e-01 -> neutral {C:0.4, THEM(^C):0.6}   via D (9.14e-02), X (8.68e-02), and(X,X) (2.09e-03), or(X,X) (2.09e-03)
    - 1.67e-01 -> neutral {C:0.6, THEM(^C):0.4}   via C (1.64e-01), THEM(ME) (1.02e-03), THEM(THEM) (1.02e-03), not(THEM(ME)) (2.21e-04)
    - 9.88e-02 -> neutral {C:0.3, THEM(^C):0.7}   via D (4.93e-02), X (4.68e-02), or(X,X) (1.13e-03), and(X,X) (1.13e-03)
    - 9.10e-04 -> poly {C:1, THEM(^C):2.45e-19, THEM(^D):2.17e-19}   via THEM(^D) (9.10e-04)
    - 8.83e-04 -> poly {C:1, THEM(^X):1.99e-08}   via THEM(^X) (8.83e-04)
- neutral {C:0.1, THEM(^C):0.9}
    - 3.63e-01 -> neutral {C:0.2, THEM(^C):0.8}   via C (2.96e-01), D (3.29e-02), X (3.12e-02), and(X,X) (7.54e-04)
    - 6.69e-02 -> mono {THEM(^C):1}   via D (3.29e-02), X (3.12e-02), and(X,X) (7.54e-04), or(X,X) (7.54e-04)
    - 8.19e-04 -> poly {C:1, THEM(^C):2.45e-19, THEM(^D):2.17e-19}   via THEM(^D) (8.19e-04)
    - 7.95e-04 -> poly {C:1, THEM(^X):1.99e-08}   via THEM(^X) (7.95e-04)
    - 9.10e-05 -> mono {THEM(^D):1}   via THEM(^D) (9.10e-05)
    - 8.83e-05 -> mono {THEM(^X):1}   via THEM(^X) (8.83e-05)
- neutral {D:0.9, THEM(ME):0.1}
    - 9.89e-02 -> mono {D:1}   via D (3.29e-02), C (3.29e-02), X (3.12e-02), and(X,X) (7.54e-04)
    - 6.93e-02 -> neutral {D:0.8, THEM(ME):0.2}   via C (3.29e-02), X (3.12e-02), THEM(ME) (3.31e-03), and(X,X) (7.54e-04)
    - 3.30e-03 -> neutral {D:0.8, THEM(ME):0.1, THEM(THEM):0.1}   via THEM(THEM) (3.30e-03)
    - 8.19e-04 -> poly {THEM(ME):3.25e-19, THEM(^C):1}   via THEM(^C) (8.19e-04)
    - 8.19e-04 -> neutral {D:0.8, THEM(ME):0.1, THEM(^D):0.1}   via THEM(^D) (8.19e-04)
    - 7.95e-04 -> poly {THEM(ME):8.46e-17, THEM(^X):1}   via THEM(^X) (7.95e-04)
- neutral {D:0.9, THEM(THEM):0.1}
    - 9.89e-02 -> mono {D:1}   via D (3.29e-02), C (3.29e-02), X (3.12e-02), and(X,X) (7.54e-04)
    - 6.93e-02 -> neutral {D:0.8, THEM(THEM):0.2}   via C (3.29e-02), X (3.12e-02), THEM(THEM) (3.30e-03), and(X,X) (7.54e-04)
    - 3.31e-03 -> neutral {D:0.8, THEM(ME):0.1, THEM(THEM):0.1}   via THEM(ME) (3.31e-03)
    - 8.19e-04 -> poly {THEM(THEM):3.25e-19, THEM(^C):1}   via THEM(^C) (8.19e-04)
    - 8.19e-04 -> neutral {D:0.8, THEM(THEM):0.1, THEM(^D):0.1}   via THEM(^D) (8.19e-04)
    - 7.95e-04 -> poly {THEM(THEM):8.46e-17, THEM(^X):1}   via THEM(^X) (7.95e-04)
- mono {THEM(^C):1}
    - 3.29e-01 -> neutral {C:0.1, THEM(^C):0.9}   via C (3.29e-01)
    - 9.10e-04 -> mono {THEM(^D):1}   via THEM(^D) (9.10e-04)
    - 8.83e-04 -> mono {THEM(^X):1}   via THEM(^X) (8.83e-04)
    - 8.80e-05 -> neutral {THEM(^C):0.9, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (8.80e-05)
    - 8.80e-05 -> neutral {THEM(^C):0.9, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (8.80e-05)
    - 2.66e-05 -> mono {or(X,THEM(^X)):1}   via or(X,THEM(^X)) (2.66e-05)
- neutral {D:0.8, THEM(ME):0.2}
    - 1.83e-01 -> neutral {D:0.9, THEM(ME):0.1}   via D (6.58e-02), C (5.85e-02), X (5.55e-02), and(X,X) (1.34e-03)
    - 1.20e-01 -> neutral {D:0.7, THEM(ME):0.3}   via C (5.85e-02), X (5.55e-02), THEM(ME) (2.94e-03), and(X,X) (1.34e-03)
    - 2.93e-03 -> neutral {D:0.7, THEM(ME):0.2, THEM(THEM):0.1}   via THEM(THEM) (2.93e-03)
    - 9.10e-04 -> poly {THEM(ME):3.25e-19, THEM(^C):1}   via THEM(^C) (9.10e-04)
    - 7.33e-04 -> neutral {D:0.8, THEM(ME):0.1, THEM(THEM):0.1}   via THEM(THEM) (7.33e-04)
    - 7.28e-04 -> neutral {D:0.7, THEM(ME):0.2, THEM(^D):0.1}   via THEM(^D) (7.28e-04)
- neutral {D:0.8, THEM(THEM):0.2}
    - 1.83e-01 -> neutral {D:0.9, THEM(THEM):0.1}   via D (6.58e-02), C (5.85e-02), X (5.55e-02), and(X,X) (1.34e-03)
    - 1.20e-01 -> neutral {D:0.7, THEM(THEM):0.3}   via C (5.85e-02), X (5.55e-02), THEM(THEM) (2.93e-03), and(X,X) (1.34e-03)
    - 2.94e-03 -> neutral {D:0.7, THEM(ME):0.1, THEM(THEM):0.2}   via THEM(ME) (2.94e-03)
    - 9.10e-04 -> poly {THEM(THEM):3.25e-19, THEM(^C):1}   via THEM(^C) (9.10e-04)
    - 7.36e-04 -> neutral {D:0.8, THEM(ME):0.1, THEM(THEM):0.1}   via THEM(ME) (7.36e-04)
    - 7.28e-04 -> neutral {D:0.7, THEM(THEM):0.2, THEM(^D):0.1}   via THEM(^D) (7.28e-04)
- neutral {C:0.6, THEM(^C):0.4}
    - 3.29e-01 -> neutral {C:0.2, THEM(^C):0.8}   via D (1.64e-01), X (1.56e-01), and(X,X) (3.77e-03), or(X,X) (3.77e-03)
    - 2.11e-01 -> neutral {C:0.1, THEM(^C):0.9}   via D (1.05e-01), X (1.00e-01), or(X,X) (2.42e-03), and(X,X) (2.42e-03)
    - 1.34e-01 -> neutral {C:0.7, THEM(^C):0.3}   via C (1.32e-01), THEM(ME) (9.81e-04), THEM(THEM) (9.78e-04), or(THEM(ME),C) (3.06e-05)
    - 1.19e-01 -> neutral {C:0.3, THEM(^C):0.7}   via D (5.91e-02), X (5.62e-02), or(X,X) (1.36e-03), and(X,X) (1.36e-03)
    - 3.06e-03 -> neutral {C:0.5, THEM(^C):0.5}   via THEM(ME) (9.81e-04), THEM(THEM) (9.78e-04), THEM(^C) (5.46e-04), not(THEM(ME)) (3.52e-04)
    - 9.10e-04 -> poly {C:1, THEM(^C):2.45e-19, THEM(^D):2.17e-19}   via THEM(^D) (9.10e-04)

INDETERMINATE transitions (replicator did not converge): 74; first: from poly {C:0.267, THEM(THEM):0.2, and(X,THEM(^X)):0.533} with mutant THEM(^and(X,X))
