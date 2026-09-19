### arm=weak, n=6, game=pd, N=10, x_on=True, role=False, mode=square

programs 1852, classes 48, states 3358, terminal classes 1, indeterminate 136, divergence rate 0.0019
mean payoff -0.6844, efficient 0.0000, deadweight loss 0.6844, mean bits in support 4.66

| pi | state |
|---|---|
| 0.5823 | mono {D:1} |
| 0.0787 | neutral {C:0.3, THEM(^C):0.7} |
| 0.0690 | neutral {C:0.2, THEM(^C):0.8} |
| 0.0670 | neutral {C:0.4, THEM(^C):0.6} |
| 0.0368 | neutral {C:0.5, THEM(^C):0.5} |
| 0.0310 | neutral {C:0.1, THEM(^C):0.9} |
| 0.0210 | neutral {D:0.9, THEM(ME):0.1} |
| 0.0210 | neutral {D:0.9, THEM(THEM):0.1} |
| 0.0092 | mono {THEM(^C):1} |
| 0.0079 | neutral {D:0.8, THEM(THEM):0.2} |
| 0.0078 | neutral {D:0.8, THEM(ME):0.2} |
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
    - 1.87e-03 -> mono {C:1}   via THEM(^D) (9.10e-04), THEM(^X) (8.83e-04), or(X,THEM(^D)) (2.66e-05), or(X,THEM(^X)) (2.66e-05)
    - 6.16e-05 -> poly {C:0.3, THEM(^C):0.6, and(THEM(ME),X):0.1}   via and(THEM(ME),X) (6.16e-05)
    - 6.16e-05 -> neutral {C:0.3, THEM(^C):0.6, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (6.16e-05)
    - 6.16e-05 -> neutral {C:0.3, THEM(^C):0.6, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (6.16e-05)
- neutral {C:0.2, THEM(^C):0.8}
    - 3.82e-01 -> neutral {C:0.3, THEM(^C):0.7}   via C (2.63e-01), D (5.85e-02), X (5.55e-02), and(X,X) (1.34e-03)
    - 1.19e-01 -> neutral {C:0.1, THEM(^C):0.9}   via D (5.85e-02), X (5.55e-02), and(X,X) (1.34e-03), or(X,X) (1.34e-03)
    - 1.87e-03 -> mono {C:1}   via THEM(^D) (9.10e-04), THEM(^X) (8.83e-04), or(X,THEM(^D)) (2.66e-05), or(X,THEM(^X)) (2.66e-05)
    - 7.04e-05 -> neutral {C:0.2, THEM(^C):0.7, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (7.04e-05)
    - 7.04e-05 -> neutral {C:0.2, THEM(^C):0.7, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (7.04e-05)
    - 2.66e-05 -> mono {and(X,THEM(^D)):1}   via and(X,THEM(^D)) (2.66e-05)
- neutral {C:0.4, THEM(^C):0.6}
    - 3.75e-01 -> neutral {C:0.5, THEM(^C):0.5}   via C (1.97e-01), D (8.77e-02), X (8.33e-02), and(X,X) (2.01e-03)
    - 1.78e-01 -> neutral {C:0.3, THEM(^C):0.7}   via D (8.77e-02), X (8.33e-02), and(X,X) (2.01e-03), or(X,X) (2.01e-03)
    - 1.87e-03 -> mono {C:1}   via THEM(^D) (9.10e-04), THEM(^X) (8.83e-04), or(X,THEM(^D)) (2.66e-05), or(X,THEM(^X)) (2.66e-05)
    - 5.28e-05 -> poly {C:0.00396, THEM(^C):0.00792, and(THEM(ME),X):0.988}   via and(THEM(ME),X) (5.28e-05)
    - 5.28e-05 -> neutral {C:0.4, THEM(^C):0.5, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (5.28e-05)
    - 5.28e-05 -> neutral {C:0.4, THEM(^C):0.5, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (5.28e-05)
- neutral {C:0.5, THEM(^C):0.5}
    - 2.31e-01 -> neutral {C:0.2, THEM(^C):0.8}   via D (1.15e-01), X (1.09e-01), and(X,X) (2.64e-03), or(X,X) (2.64e-03)
    - 1.86e-01 -> neutral {C:0.4, THEM(^C):0.6}   via D (9.14e-02), X (8.68e-02), and(X,X) (2.09e-03), or(X,X) (2.09e-03)
    - 1.67e-01 -> neutral {C:0.6, THEM(^C):0.4}   via C (1.64e-01), THEM(ME) (1.02e-03), THEM(THEM) (1.02e-03), not(THEM(ME)) (2.21e-04)
    - 9.88e-02 -> neutral {C:0.3, THEM(^C):0.7}   via D (4.93e-02), X (4.68e-02), or(X,X) (1.13e-03), and(X,X) (1.13e-03)
    - 1.87e-03 -> mono {C:1}   via THEM(^D) (9.10e-04), THEM(^X) (8.83e-04), or(X,THEM(^D)) (2.66e-05), or(X,THEM(^X)) (2.66e-05)
    - 4.40e-05 -> poly {C:0.00396, THEM(^C):0.00792, and(THEM(ME),X):0.988}   via and(THEM(ME),X) (4.40e-05)
- neutral {C:0.1, THEM(^C):0.9}
    - 3.63e-01 -> neutral {C:0.2, THEM(^C):0.8}   via C (2.96e-01), D (3.29e-02), X (3.12e-02), and(X,X) (7.54e-04)
    - 6.69e-02 -> mono {THEM(^C):1}   via D (3.29e-02), X (3.12e-02), and(X,X) (7.54e-04), or(X,X) (7.54e-04)
    - 1.69e-03 -> mono {C:1}   via THEM(^D) (8.19e-04), THEM(^X) (7.95e-04), or(X,THEM(^D)) (2.39e-05), or(X,THEM(^X)) (2.39e-05)
    - 9.10e-05 -> mono {THEM(^D):1}   via THEM(^D) (9.10e-05)
    - 8.83e-05 -> mono {THEM(^X):1}   via THEM(^X) (8.83e-05)
    - 7.92e-05 -> neutral {C:0.1, THEM(^C):0.8, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (7.92e-05)
- neutral {D:0.9, THEM(ME):0.1}
    - 9.89e-02 -> mono {D:1}   via D (3.29e-02), C (3.29e-02), X (3.12e-02), and(X,X) (7.54e-04)
    - 6.93e-02 -> neutral {D:0.8, THEM(ME):0.2}   via C (3.29e-02), X (3.12e-02), THEM(ME) (3.31e-03), and(X,X) (7.54e-04)
    - 3.30e-03 -> neutral {D:0.8, THEM(ME):0.1, THEM(THEM):0.1}   via THEM(THEM) (3.30e-03)
    - 9.10e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-04)
    - 8.83e-04 -> mono {THEM(^X):1}   via THEM(^X) (8.83e-04)
    - 8.19e-04 -> neutral {D:0.8, THEM(ME):0.1, THEM(^D):0.1}   via THEM(^D) (8.19e-04)
- neutral {D:0.9, THEM(THEM):0.1}
    - 9.89e-02 -> mono {D:1}   via D (3.29e-02), C (3.29e-02), X (3.12e-02), and(X,X) (7.54e-04)
    - 6.93e-02 -> neutral {D:0.8, THEM(THEM):0.2}   via C (3.29e-02), X (3.12e-02), THEM(THEM) (3.30e-03), and(X,X) (7.54e-04)
    - 3.31e-03 -> neutral {D:0.8, THEM(ME):0.1, THEM(THEM):0.1}   via THEM(ME) (3.31e-03)
    - 9.10e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-04)
    - 8.83e-04 -> mono {THEM(^X):1}   via THEM(^X) (8.83e-04)
    - 8.19e-04 -> neutral {D:0.8, THEM(THEM):0.1, THEM(^D):0.1}   via THEM(^D) (8.19e-04)
- mono {THEM(^C):1}
    - 3.29e-01 -> neutral {C:0.1, THEM(^C):0.9}   via C (3.29e-01)
    - 9.10e-04 -> mono {THEM(^D):1}   via THEM(^D) (9.10e-04)
    - 8.83e-04 -> mono {THEM(^X):1}   via THEM(^X) (8.83e-04)
    - 8.80e-05 -> neutral {THEM(^C):0.9, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (8.80e-05)
    - 8.80e-05 -> neutral {THEM(^C):0.9, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (8.80e-05)
    - 2.66e-05 -> mono {or(X,THEM(^X)):1}   via or(X,THEM(^X)) (2.66e-05)
- neutral {D:0.8, THEM(THEM):0.2}
    - 1.83e-01 -> neutral {D:0.9, THEM(THEM):0.1}   via D (6.58e-02), C (5.85e-02), X (5.55e-02), and(X,X) (1.34e-03)
    - 1.20e-01 -> neutral {D:0.7, THEM(THEM):0.3}   via C (5.85e-02), X (5.55e-02), THEM(THEM) (2.93e-03), and(X,X) (1.34e-03)
    - 2.94e-03 -> neutral {D:0.7, THEM(ME):0.1, THEM(THEM):0.2}   via THEM(ME) (2.94e-03)
    - 9.10e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-04)
    - 8.83e-04 -> mono {THEM(^X):1}   via THEM(^X) (8.83e-04)
    - 7.36e-04 -> neutral {D:0.8, THEM(ME):0.1, THEM(THEM):0.1}   via THEM(ME) (7.36e-04)
- neutral {D:0.8, THEM(ME):0.2}
    - 1.83e-01 -> neutral {D:0.9, THEM(ME):0.1}   via D (6.58e-02), C (5.85e-02), X (5.55e-02), and(X,X) (1.34e-03)
    - 1.20e-01 -> neutral {D:0.7, THEM(ME):0.3}   via C (5.85e-02), X (5.55e-02), THEM(ME) (2.94e-03), and(X,X) (1.34e-03)
    - 2.93e-03 -> neutral {D:0.7, THEM(ME):0.2, THEM(THEM):0.1}   via THEM(THEM) (2.93e-03)
    - 9.10e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-04)
    - 8.83e-04 -> mono {THEM(^X):1}   via THEM(^X) (8.83e-04)
    - 7.33e-04 -> neutral {D:0.8, THEM(ME):0.1, THEM(THEM):0.1}   via THEM(THEM) (7.33e-04)
- neutral {C:0.6, THEM(^C):0.4}
    - 3.29e-01 -> neutral {C:0.2, THEM(^C):0.8}   via D (1.64e-01), X (1.56e-01), and(X,X) (3.77e-03), or(X,X) (3.77e-03)
    - 2.11e-01 -> neutral {C:0.1, THEM(^C):0.9}   via D (1.05e-01), X (1.00e-01), or(X,X) (2.42e-03), and(X,X) (2.42e-03)
    - 1.34e-01 -> neutral {C:0.7, THEM(^C):0.3}   via C (1.32e-01), THEM(ME) (9.81e-04), THEM(THEM) (9.78e-04), or(THEM(ME),C) (3.06e-05)
    - 1.19e-01 -> neutral {C:0.3, THEM(^C):0.7}   via D (5.91e-02), X (5.62e-02), or(X,X) (1.36e-03), and(X,X) (1.36e-03)
    - 3.06e-03 -> neutral {C:0.5, THEM(^C):0.5}   via THEM(ME) (9.81e-04), THEM(THEM) (9.78e-04), THEM(^C) (5.46e-04), not(THEM(ME)) (3.52e-04)
    - 1.87e-03 -> mono {C:1}   via THEM(^D) (9.10e-04), THEM(^X) (8.83e-04), or(X,THEM(^D)) (2.66e-05), or(X,THEM(^X)) (2.66e-05)

INDETERMINATE transitions (replicator did not converge): 136; first: from poly {C:0.213, D:0.07, X:0.0739, THEM(^X):0.357, and(X,THEM(^X)):0.286} with mutant THEM(THEM)
