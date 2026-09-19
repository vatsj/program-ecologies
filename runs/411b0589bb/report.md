### arm=weak, n=7, game=pd, N=100, x_on=True, role=False, mode=sparse

programs 9426, classes 105, states 187701, terminal classes 1, indeterminate 342, divergence rate 0.0132
mean payoff -0.7281, efficient 0.0000, deadweight loss 0.7281, mean bits in support 4.36

| pi | state |
|---|---|
| 0.2222 | mono {D:1} |
| 0.1127 | neutral {D:0.99, THEM(ME):0.01} |
| 0.0645 | neutral {D:0.98, THEM(ME):0.02} |
| 0.0387 | neutral {D:0.97, THEM(ME):0.03} |
| 0.0267 | neutral {C:0.45, THEM(^C):0.55} |
| 0.0263 | neutral {C:0.46, THEM(^C):0.54} |
| 0.0252 | neutral {C:0.47, THEM(^C):0.53} |
| 0.0238 | neutral {D:0.96, THEM(ME):0.04} |
| 0.0231 | neutral {C:0.48, THEM(^C):0.52} |
| 0.0210 | neutral {C:0.44, THEM(^C):0.56} |
| 0.0185 | neutral {C:0.49, THEM(^C):0.51} |
| 0.0184 | neutral {D:0.99, THEM(^D):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 7.46e-03 -> neutral {D:0.99, THEM(ME):0.01}   via THEM(ME) (7.46e-03)
    - 9.48e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.48e-04)
    - 9.48e-04 -> neutral {D:0.99, THEM(^D):0.01}   via THEM(^D) (9.48e-04)
    - 9.11e-04 -> mono {THEM(^X):1}   via THEM(^X) (9.11e-04)
    - 3.15e-04 -> neutral {D:0.99, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (3.15e-04)
    - 1.15e-04 -> neutral {D:0.99, and(THEM(THEM),X):0.01}   via and(THEM(THEM),X) (1.15e-04)
- neutral {D:0.99, THEM(ME):0.01}
    - 1.40e-02 -> neutral {D:0.98, THEM(ME):0.02}   via THEM(ME) (7.39e-03), C (3.29e-03), X (3.10e-03), and(X,X) (8.09e-05)
    - 9.89e-03 -> mono {D:1}   via D (3.29e-03), C (3.29e-03), X (3.10e-03), and(X,X) (8.09e-05)
    - 9.48e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.48e-04)
    - 9.38e-04 -> neutral {D:0.98, THEM(ME):0.01, THEM(^D):0.01}   via THEM(^D) (9.38e-04)
    - 9.11e-04 -> mono {THEM(^X):1}   via THEM(^X) (9.11e-04)
    - 3.12e-04 -> neutral {D:0.98, THEM(ME):0.01, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (3.12e-04)
- neutral {D:0.98, THEM(ME):0.02}
    - 2.04e-02 -> neutral {D:0.97, THEM(ME):0.03}   via THEM(ME) (7.31e-03), C (6.51e-03), X (6.14e-03), and(X,X) (1.60e-04)
    - 1.96e-02 -> neutral {D:0.99, THEM(ME):0.01}   via D (6.57e-03), C (6.51e-03), X (6.14e-03), and(X,X) (1.60e-04)
    - 9.48e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.48e-04)
    - 9.29e-04 -> neutral {D:0.97, THEM(ME):0.02, THEM(^D):0.01}   via THEM(^D) (9.29e-04)
    - 9.11e-04 -> mono {THEM(^X):1}   via THEM(^X) (9.11e-04)
    - 3.09e-04 -> neutral {D:0.97, THEM(ME):0.02, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (3.09e-04)
- neutral {D:0.97, THEM(ME):0.03}
    - 2.93e-02 -> neutral {D:0.98, THEM(ME):0.02}   via D (9.86e-03), C (9.66e-03), X (9.12e-03), and(X,X) (2.38e-04)
    - 2.66e-02 -> neutral {D:0.96, THEM(ME):0.04}   via C (9.66e-03), X (9.12e-03), THEM(ME) (7.24e-03), and(X,X) (2.38e-04)
    - 9.48e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.48e-04)
    - 9.19e-04 -> neutral {D:0.96, THEM(ME):0.03, THEM(^D):0.01}   via THEM(^D) (9.19e-04)
    - 9.11e-04 -> mono {THEM(^X):1}   via THEM(^X) (9.11e-04)
    - 3.06e-04 -> neutral {D:0.96, THEM(ME):0.03, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (3.06e-04)
- neutral {C:0.45, THEM(^C):0.55}
    - 3.48e-01 -> neutral {C:0.46, THEM(^C):0.54}   via C (1.81e-01), D (8.22e-02), X (7.76e-02), and(X,X) (2.02e-03)
    - 1.67e-01 -> neutral {C:0.44, THEM(^C):0.56}   via D (8.22e-02), X (7.76e-02), and(X,X) (2.02e-03), or(X,X) (2.02e-03)
    - 1.97e-03 -> mono {C:1}   via THEM(^D) (9.48e-04), THEM(^X) (9.11e-04), or(X,THEM(^D)) (3.33e-05), or(X,THEM(^X)) (3.33e-05)
    - 1.15e-04 -> poly {THEM(^C):0.01, and(THEM(ME),X):0.99}   via and(THEM(ME),X) (1.15e-04)
    - 1.15e-04 -> poly {THEM(^C):0.01, and(X,THEM(ME)):0.99}   via and(X,THEM(ME)) (1.15e-04)
    - 6.34e-05 -> neutral {C:0.45, THEM(^C):0.54, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (6.34e-05)
- neutral {C:0.46, THEM(^C):0.54}
    - 3.45e-01 -> neutral {C:0.47, THEM(^C):0.53}   via C (1.77e-01), D (8.25e-02), X (7.79e-02), and(X,X) (2.03e-03)
    - 1.68e-01 -> neutral {C:0.45, THEM(^C):0.55}   via D (8.25e-02), X (7.79e-02), and(X,X) (2.03e-03), or(X,X) (2.03e-03)
    - 1.97e-03 -> mono {C:1}   via THEM(^D) (9.48e-04), THEM(^X) (9.11e-04), or(X,THEM(^D)) (3.33e-05), or(X,THEM(^X)) (3.33e-05)
    - 1.15e-04 -> poly {THEM(^C):0.01, and(THEM(ME),X):0.99}   via and(THEM(ME),X) (1.15e-04)
    - 1.15e-04 -> poly {THEM(^C):0.01, and(X,THEM(ME)):0.99}   via and(X,THEM(ME)) (1.15e-04)
    - 6.23e-05 -> neutral {C:0.46, THEM(^C):0.53, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (6.23e-05)
- neutral {C:0.47, THEM(^C):0.53}
    - 3.42e-01 -> neutral {C:0.48, THEM(^C):0.52}   via C (1.74e-01), D (8.27e-02), X (7.81e-02), and(X,X) (2.03e-03)
    - 1.68e-01 -> neutral {C:0.46, THEM(^C):0.54}   via D (8.27e-02), X (7.81e-02), and(X,X) (2.03e-03), or(X,X) (2.03e-03)
    - 1.97e-03 -> mono {C:1}   via THEM(^D) (9.48e-04), THEM(^X) (9.11e-04), or(X,THEM(^D)) (3.33e-05), or(X,THEM(^X)) (3.33e-05)
    - 1.15e-04 -> poly {THEM(^C):0.01, and(THEM(ME),X):0.99}   via and(THEM(ME),X) (1.15e-04)
    - 1.15e-04 -> poly {THEM(^C):0.01, and(X,THEM(ME)):0.99}   via and(X,THEM(ME)) (1.15e-04)
    - 6.11e-05 -> neutral {C:0.47, THEM(^C):0.52, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (6.11e-05)
- neutral {D:0.96, THEM(ME):0.04}
    - 3.88e-02 -> neutral {D:0.97, THEM(ME):0.03}   via D (1.31e-02), C (1.27e-02), X (1.20e-02), and(X,X) (3.14e-04)
    - 3.28e-02 -> neutral {D:0.95, THEM(ME):0.05}   via C (1.27e-02), X (1.20e-02), THEM(ME) (7.16e-03), and(X,X) (3.14e-04)
    - 9.48e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.48e-04)
    - 9.11e-04 -> mono {THEM(^X):1}   via THEM(^X) (9.11e-04)
    - 9.10e-04 -> neutral {D:0.95, THEM(ME):0.04, THEM(^D):0.01}   via THEM(^D) (9.10e-04)
    - 3.03e-04 -> neutral {D:0.95, THEM(ME):0.04, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (3.03e-04)
- neutral {C:0.48, THEM(^C):0.52}
    - 3.39e-01 -> neutral {C:0.49, THEM(^C):0.51}   via C (1.71e-01), D (8.29e-02), X (7.83e-02), and(X,X) (2.04e-03)
    - 1.69e-01 -> neutral {C:0.47, THEM(^C):0.53}   via D (8.29e-02), X (7.83e-02), and(X,X) (2.04e-03), or(X,X) (2.04e-03)
    - 1.97e-03 -> mono {C:1}   via THEM(^D) (9.48e-04), THEM(^X) (9.11e-04), or(X,THEM(^D)) (3.33e-05), or(X,THEM(^X)) (3.33e-05)
    - 1.15e-04 -> poly {THEM(^C):0.01, and(THEM(ME),X):0.99}   via and(THEM(ME),X) (1.15e-04)
    - 1.15e-04 -> poly {THEM(^C):0.01, and(X,THEM(ME)):0.99}   via and(X,THEM(ME)) (1.15e-04)
    - 6.00e-05 -> neutral {C:0.48, THEM(^C):0.51, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (6.00e-05)
- neutral {C:0.44, THEM(^C):0.56}
    - 3.50e-01 -> neutral {C:0.45, THEM(^C):0.55}   via C (1.84e-01), D (8.18e-02), X (7.72e-02), and(X,X) (2.01e-03)
    - 1.67e-01 -> neutral {C:0.43, THEM(^C):0.57}   via D (8.18e-02), X (7.72e-02), and(X,X) (2.01e-03), or(X,X) (2.01e-03)
    - 1.97e-03 -> mono {C:1}   via THEM(^D) (9.48e-04), THEM(^X) (9.11e-04), or(X,THEM(^D)) (3.33e-05), or(X,THEM(^X)) (3.33e-05)
    - 1.15e-04 -> poly {THEM(^C):0.01, and(THEM(ME),X):0.99}   via and(THEM(ME),X) (1.15e-04)
    - 1.15e-04 -> poly {THEM(^C):0.01, and(X,THEM(ME)):0.99}   via and(X,THEM(ME)) (1.15e-04)
    - 6.46e-05 -> neutral {C:0.44, THEM(^C):0.55, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (6.46e-05)
- neutral {C:0.49, THEM(^C):0.51}
    - 3.36e-01 -> neutral {C:0.5, THEM(^C):0.5}   via C (1.68e-01), D (8.30e-02), X (7.83e-02), and(X,X) (2.04e-03)
    - 1.69e-01 -> neutral {C:0.48, THEM(^C):0.52}   via D (8.30e-02), X (7.83e-02), and(X,X) (2.04e-03), or(X,X) (2.04e-03)
    - 1.97e-03 -> mono {C:1}   via THEM(^D) (9.48e-04), THEM(^X) (9.11e-04), or(X,THEM(^D)) (3.33e-05), or(X,THEM(^X)) (3.33e-05)
    - 1.15e-04 -> poly {THEM(^C):0.01, and(THEM(ME),X):0.99}   via and(THEM(ME),X) (1.15e-04)
    - 1.15e-04 -> poly {THEM(^C):0.01, and(X,THEM(ME)):0.99}   via and(X,THEM(ME)) (1.15e-04)
    - 5.88e-05 -> neutral {C:0.49, THEM(^C):0.5, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (5.88e-05)
- neutral {D:0.99, THEM(^D):0.01}
    - 9.89e-03 -> mono {D:1}   via D (3.29e-03), C (3.29e-03), X (3.10e-03), and(X,X) (8.09e-05)
    - 7.56e-03 -> neutral {D:0.98, THEM(^D):0.02}   via C (3.29e-03), X (3.10e-03), THEM(^D) (9.38e-04), and(X,X) (8.09e-05)
    - 7.39e-03 -> neutral {D:0.98, THEM(ME):0.01, THEM(^D):0.01}   via THEM(ME) (7.39e-03)
    - 3.12e-04 -> neutral {D:0.98, THEM(^D):0.01, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (3.12e-04)
    - 1.14e-04 -> neutral {D:0.98, THEM(^D):0.01, and(THEM(THEM),X):0.01}   via and(THEM(THEM),X) (1.14e-04)
    - 1.14e-04 -> neutral {D:0.98, THEM(^D):0.01, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (1.14e-04)

INDETERMINATE transitions (replicator did not converge): 342; first: from poly {C:0.24, X:0.01, THEM(^X):0.26, and(X,THEM(^X)):0.49} with mutant or(THEM(THEM),X)
