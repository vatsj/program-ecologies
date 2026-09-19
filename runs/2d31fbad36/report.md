### arm=weak, n=7, game=pd, N=10, x_on=True, role=False, mode=sparse

programs 9426, classes 105, states 20311, terminal classes 1, indeterminate 458, divergence rate 0.0124
mean payoff -0.6869, efficient 0.0000, deadweight loss 0.6869, mean bits in support 4.70

| pi | state |
|---|---|
| 0.5781 | mono {D:1} |
| 0.0770 | neutral {C:0.3, THEM(^C):0.7} |
| 0.0675 | neutral {C:0.2, THEM(^C):0.8} |
| 0.0654 | neutral {C:0.4, THEM(^C):0.6} |
| 0.0423 | neutral {D:0.9, THEM(ME):0.1} |
| 0.0359 | neutral {C:0.5, THEM(^C):0.5} |
| 0.0305 | neutral {C:0.1, THEM(^C):0.9} |
| 0.0165 | neutral {D:0.8, THEM(ME):0.2} |
| 0.0092 | mono {THEM(^C):1} |
| 0.0080 | neutral {D:0.7, THEM(ME):0.3} |
| 0.0075 | neutral {C:0.6, THEM(^C):0.4} |
| 0.0056 | neutral {D:0.9, THEM(^D):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 7.46e-03 -> neutral {D:0.9, THEM(ME):0.1}   via THEM(ME) (7.46e-03)
    - 9.48e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.48e-04)
    - 9.48e-04 -> neutral {D:0.9, THEM(^D):0.1}   via THEM(^D) (9.48e-04)
    - 9.11e-04 -> mono {THEM(^X):1}   via THEM(^X) (9.11e-04)
    - 3.15e-04 -> neutral {D:0.9, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (3.15e-04)
    - 1.15e-04 -> neutral {D:0.9, and(THEM(THEM),X):0.1}   via and(THEM(THEM),X) (1.15e-04)
- neutral {C:0.3, THEM(^C):0.7}
    - 3.86e-01 -> neutral {C:0.4, THEM(^C):0.6}   via C (2.30e-01), D (7.67e-02), X (7.24e-02), and(X,X) (1.89e-03)
    - 1.56e-01 -> neutral {C:0.2, THEM(^C):0.8}   via D (7.67e-02), X (7.24e-02), and(X,X) (1.89e-03), or(X,X) (1.89e-03)
    - 1.97e-03 -> mono {C:1}   via THEM(^D) (9.48e-04), THEM(^X) (9.11e-04), or(X,THEM(^D)) (3.33e-05), or(X,THEM(^X)) (3.33e-05)
    - 8.07e-05 -> poly {C:0.3, THEM(^C):0.6, and(THEM(ME),X):0.1}   via and(THEM(ME),X) (8.07e-05)
    - 8.07e-05 -> neutral {C:0.3, THEM(^C):0.6, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (8.07e-05)
    - 8.07e-05 -> neutral {C:0.3, THEM(^C):0.6, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (8.07e-05)
- neutral {C:0.2, THEM(^C):0.8}
    - 3.82e-01 -> neutral {C:0.3, THEM(^C):0.7}   via C (2.63e-01), D (5.84e-02), X (5.52e-02), and(X,X) (1.44e-03)
    - 1.19e-01 -> neutral {C:0.1, THEM(^C):0.9}   via D (5.84e-02), X (5.52e-02), and(X,X) (1.44e-03), or(X,X) (1.44e-03)
    - 1.97e-03 -> mono {C:1}   via THEM(^D) (9.48e-04), THEM(^X) (9.11e-04), or(X,THEM(^D)) (3.33e-05), or(X,THEM(^X)) (3.33e-05)
    - 9.23e-05 -> neutral {C:0.2, THEM(^C):0.7, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (9.23e-05)
    - 9.23e-05 -> neutral {C:0.2, THEM(^C):0.7, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (9.23e-05)
    - 3.33e-05 -> mono {and(X,THEM(^D)):1}   via and(X,THEM(^D)) (3.33e-05)
- neutral {C:0.4, THEM(^C):0.6}
    - 3.75e-01 -> neutral {C:0.5, THEM(^C):0.5}   via C (1.97e-01), D (8.76e-02), X (8.28e-02), and(X,X) (2.16e-03)
    - 1.78e-01 -> neutral {C:0.3, THEM(^C):0.7}   via D (8.76e-02), X (8.28e-02), and(X,X) (2.16e-03), or(X,X) (2.16e-03)
    - 1.97e-03 -> mono {C:1}   via THEM(^D) (9.48e-04), THEM(^X) (9.11e-04), or(X,THEM(^D)) (3.33e-05), or(X,THEM(^X)) (3.33e-05)
    - 6.92e-05 -> poly {C:0.00396, THEM(^C):0.00792, and(THEM(ME),X):0.988}   via and(THEM(ME),X) (6.92e-05)
    - 6.92e-05 -> neutral {C:0.4, THEM(^C):0.5, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (6.92e-05)
    - 6.92e-05 -> neutral {C:0.4, THEM(^C):0.5, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (6.92e-05)
- neutral {D:0.9, THEM(ME):0.1}
    - 9.89e-02 -> mono {D:1}   via D (3.29e-02), C (3.29e-02), X (3.10e-02), and(X,X) (8.09e-04)
    - 7.27e-02 -> neutral {D:0.8, THEM(ME):0.2}   via C (3.29e-02), X (3.10e-02), THEM(ME) (6.72e-03), and(X,X) (8.09e-04)
    - 9.48e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.48e-04)
    - 9.11e-04 -> mono {THEM(^X):1}   via THEM(^X) (9.11e-04)
    - 8.53e-04 -> neutral {D:0.8, THEM(ME):0.1, THEM(^D):0.1}   via THEM(^D) (8.53e-04)
    - 2.84e-04 -> neutral {D:0.8, THEM(ME):0.1, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (2.84e-04)
- neutral {C:0.5, THEM(^C):0.5}
    - 2.31e-01 -> neutral {C:0.2, THEM(^C):0.8}   via D (1.15e-01), X (1.09e-01), and(X,X) (2.83e-03), or(X,X) (2.83e-03)
    - 1.86e-01 -> neutral {C:0.4, THEM(^C):0.6}   via D (9.13e-02), X (8.62e-02), and(X,X) (2.25e-03), or(X,X) (2.25e-03)
    - 1.67e-01 -> neutral {C:0.6, THEM(^C):0.4}   via C (1.64e-01), THEM(ME) (2.07e-03), not(THEM(ME)) (2.22e-04), or(THEM(ME),C) (8.75e-05)
    - 9.87e-02 -> neutral {C:0.3, THEM(^C):0.7}   via D (4.92e-02), X (4.65e-02), or(X,X) (1.21e-03), and(X,X) (1.21e-03)
    - 1.97e-03 -> mono {C:1}   via THEM(^D) (9.48e-04), THEM(^X) (9.11e-04), or(X,THEM(^D)) (3.33e-05), or(X,THEM(^X)) (3.33e-05)
    - 5.79e-05 -> neutral {C:0.1, THEM(^C):0.9}   via not(THEM(^C)) (4.93e-05), and(X,and(X,THEM(ME))) (2.89e-06), or(X,and(X,THEM(ME))) (2.17e-06), and(X,or(X,THEM(ME))) (2.17e-06)
- neutral {C:0.1, THEM(^C):0.9}
    - 3.63e-01 -> neutral {C:0.2, THEM(^C):0.8}   via C (2.96e-01), D (3.29e-02), X (3.10e-02), and(X,X) (8.09e-04)
    - 6.69e-02 -> mono {THEM(^C):1}   via D (3.29e-02), X (3.10e-02), and(X,X) (8.09e-04), or(X,X) (8.09e-04)
    - 1.77e-03 -> mono {C:1}   via THEM(^D) (8.53e-04), THEM(^X) (8.20e-04), or(X,THEM(^D)) (3.00e-05), or(X,THEM(^X)) (3.00e-05)
    - 1.04e-04 -> neutral {C:0.1, THEM(^C):0.8, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (1.04e-04)
    - 1.04e-04 -> neutral {C:0.1, THEM(^C):0.8, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (1.04e-04)
    - 9.48e-05 -> mono {THEM(^D):1}   via THEM(^D) (9.48e-05)
- neutral {D:0.8, THEM(ME):0.2}
    - 1.83e-01 -> neutral {D:0.9, THEM(ME):0.1}   via D (6.57e-02), C (5.84e-02), X (5.52e-02), and(X,X) (1.44e-03)
    - 1.23e-01 -> neutral {D:0.7, THEM(ME):0.3}   via C (5.84e-02), X (5.52e-02), THEM(ME) (5.97e-03), and(X,X) (1.44e-03)
    - 9.48e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.48e-04)
    - 9.11e-04 -> mono {THEM(^X):1}   via THEM(^X) (9.11e-04)
    - 7.58e-04 -> neutral {D:0.7, THEM(ME):0.2, THEM(^D):0.1}   via THEM(^D) (7.58e-04)
    - 2.52e-04 -> neutral {D:0.7, THEM(ME):0.2, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (2.52e-04)
- mono {THEM(^C):1}
    - 3.29e-01 -> neutral {C:0.1, THEM(^C):0.9}   via C (3.29e-01)
    - 9.48e-04 -> mono {THEM(^D):1}   via THEM(^D) (9.48e-04)
    - 9.11e-04 -> mono {THEM(^X):1}   via THEM(^X) (9.11e-04)
    - 1.15e-04 -> neutral {THEM(^C):0.9, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (1.15e-04)
    - 1.15e-04 -> neutral {THEM(^C):0.9, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (1.15e-04)
    - 3.33e-05 -> mono {or(X,THEM(^X)):1}   via or(X,THEM(^X)) (3.33e-05)
- neutral {D:0.7, THEM(ME):0.3}
    - 2.53e-01 -> neutral {D:0.8, THEM(ME):0.2}   via D (9.86e-02), C (7.67e-02), X (7.24e-02), and(X,X) (1.89e-03)
    - 1.59e-01 -> neutral {D:0.6, THEM(ME):0.4}   via C (7.67e-02), X (7.24e-02), THEM(ME) (5.22e-03), and(X,X) (1.89e-03)
    - 9.48e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.48e-04)
    - 9.11e-04 -> mono {THEM(^X):1}   via THEM(^X) (9.11e-04)
    - 6.63e-04 -> neutral {D:0.6, THEM(ME):0.3, THEM(^D):0.1}   via THEM(^D) (6.63e-04)
    - 2.84e-04 -> neutral {D:0.7, THEM(ME):0.2, THEM(^D):0.1}   via THEM(^D) (2.84e-04)
- neutral {C:0.6, THEM(^C):0.4}
    - 3.29e-01 -> neutral {C:0.2, THEM(^C):0.8}   via D (1.64e-01), X (1.55e-01), and(X,X) (4.04e-03), or(X,X) (4.04e-03)
    - 2.11e-01 -> neutral {C:0.1, THEM(^C):0.9}   via D (1.05e-01), X (9.94e-02), or(X,X) (2.59e-03), and(X,X) (2.59e-03)
    - 1.34e-01 -> neutral {C:0.7, THEM(^C):0.3}   via C (1.31e-01), THEM(ME) (1.99e-03), or(THEM(ME),C) (8.40e-05), or(THEM(ME),X) (3.08e-05)
    - 1.19e-01 -> neutral {C:0.3, THEM(^C):0.7}   via D (5.91e-02), X (5.58e-02), or(X,X) (1.45e-03), and(X,X) (1.45e-03)
    - 3.19e-03 -> neutral {C:0.5, THEM(^C):0.5}   via THEM(ME) (1.99e-03), THEM(^C) (5.69e-04), not(THEM(ME)) (3.53e-04), or(THEM(ME),C) (8.40e-05)
    - 1.97e-03 -> mono {C:1}   via THEM(^D) (9.48e-04), THEM(^X) (9.11e-04), or(X,THEM(^D)) (3.33e-05), or(X,THEM(^X)) (3.33e-05)
- neutral {D:0.9, THEM(^D):0.1}
    - 9.89e-02 -> mono {D:1}   via D (3.29e-02), C (3.29e-02), X (3.10e-02), and(X,X) (8.09e-04)
    - 6.71e-02 -> neutral {D:0.8, THEM(^D):0.2}   via C (3.29e-02), X (3.10e-02), THEM(^D) (8.53e-04), and(X,X) (8.09e-04)
    - 6.72e-03 -> neutral {D:0.8, THEM(ME):0.1, THEM(^D):0.1}   via THEM(ME) (6.72e-03)
    - 7.46e-04 -> neutral {D:0.9, THEM(ME):0.1}   via THEM(ME) (7.46e-04)
    - 2.84e-04 -> neutral {D:0.8, THEM(^D):0.1, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (2.84e-04)
    - 1.04e-04 -> neutral {D:0.8, THEM(^D):0.1, and(THEM(THEM),X):0.1}   via and(THEM(THEM),X) (1.04e-04)

INDETERMINATE transitions (replicator did not converge): 458; first: from poly {C:0.206, X:0.0876, THEM(^X):0.294, and(X,THEM(^X)):0.412} with mutant or(X,or(X,THEM(THEM)))
