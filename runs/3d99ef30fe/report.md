### arm=weak, n=6, game=exchange, N=100, x_on=True, role=False, mode=square

programs 1852, classes 48, states 31925, terminal classes 1, indeterminate 619, divergence rate 0.0019
mean payoff 0.6039, efficient 2.0000, deadweight loss 1.3961, mean bits in support 4.25

| pi | state |
|---|---|
| 0.2181 | mono {D:1} |
| 0.0561 | neutral {D:0.99, THEM(ME):0.01} |
| 0.0557 | neutral {D:0.99, THEM(THEM):0.01} |
| 0.0294 | neutral {C:0.63, THEM(^C):0.37} |
| 0.0266 | neutral {C:0.64, THEM(^C):0.36} |
| 0.0239 | neutral {D:0.98, THEM(ME):0.02} |
| 0.0237 | neutral {D:0.98, THEM(THEM):0.02} |
| 0.0224 | neutral {C:0.62, THEM(^C):0.38} |
| 0.0213 | neutral {C:0.65, THEM(^C):0.35} |
| 0.0171 | neutral {D:0.99, THEM(^D):0.01} |
| 0.0169 | neutral {D:0.98, THEM(ME):0.01, THEM(THEM):0.01} |
| 0.0133 | neutral {C:0.61, THEM(^C):0.39} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.69e-03 -> neutral {D:0.99, THEM(ME):0.01}   via THEM(ME) (3.69e-03)
    - 3.67e-03 -> neutral {D:0.99, THEM(THEM):0.01}   via THEM(THEM) (3.67e-03)
    - 9.10e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-04)
    - 9.10e-04 -> neutral {D:0.99, THEM(^D):0.01}   via THEM(^D) (9.10e-04)
    - 8.83e-04 -> mono {THEM(^X):1}   via THEM(^X) (8.83e-04)
    - 2.29e-04 -> neutral {D:0.99, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (2.29e-04)
- neutral {D:0.99, THEM(ME):0.01}
    - 1.03e-02 -> neutral {D:0.98, THEM(ME):0.02}   via THEM(ME) (3.66e-03), C (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 9.89e-03 -> mono {D:1}   via D (3.29e-03), C (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 3.63e-03 -> neutral {D:0.98, THEM(ME):0.01, THEM(THEM):0.01}   via THEM(THEM) (3.63e-03)
    - 9.10e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-04)
    - 9.01e-04 -> neutral {D:0.98, THEM(ME):0.01, THEM(^D):0.01}   via THEM(^D) (9.01e-04)
    - 8.83e-04 -> mono {THEM(^X):1}   via THEM(^X) (8.83e-04)
- neutral {D:0.99, THEM(THEM):0.01}
    - 1.02e-02 -> neutral {D:0.98, THEM(THEM):0.02}   via THEM(THEM) (3.63e-03), C (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 9.89e-03 -> mono {D:1}   via D (3.29e-03), C (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 3.66e-03 -> neutral {D:0.98, THEM(ME):0.01, THEM(THEM):0.01}   via THEM(ME) (3.66e-03)
    - 9.10e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-04)
    - 9.01e-04 -> neutral {D:0.98, THEM(THEM):0.01, THEM(^D):0.01}   via THEM(^D) (9.01e-04)
    - 8.83e-04 -> mono {THEM(^X):1}   via THEM(^X) (8.83e-04)
- neutral {C:0.63, THEM(^C):0.37}
    - 2.79e-01 -> neutral {C:0.64, THEM(^C):0.36}   via C (1.22e-01), D (7.75e-02), X (7.36e-02), and(X,X) (1.78e-03)
    - 1.58e-01 -> neutral {C:0.62, THEM(^C):0.38}   via D (7.75e-02), X (7.36e-02), and(X,X) (1.78e-03), or(X,X) (1.78e-03)
    - 1.87e-03 -> mono {C:1}   via THEM(^D) (9.10e-04), THEM(^X) (8.83e-04), or(X,THEM(^D)) (2.66e-05), or(X,THEM(^X)) (2.66e-05)
    - 8.80e-05 -> poly {C:0.5, and(THEM(ME),X):0.5}   via and(THEM(ME),X) (8.80e-05)
    - 8.80e-05 -> poly {C:0.5, and(X,THEM(ME)):0.5}   via and(X,THEM(ME)) (8.80e-05)
    - 5.54e-05 -> neutral {C:0.62, THEM(^C):0.37, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (5.54e-05)
- neutral {C:0.64, THEM(^C):0.36}
    - 2.74e-01 -> neutral {C:0.65, THEM(^C):0.35}   via C (1.18e-01), D (7.66e-02), X (7.27e-02), and(X,X) (1.76e-03)
    - 1.56e-01 -> neutral {C:0.63, THEM(^C):0.37}   via D (7.66e-02), X (7.27e-02), and(X,X) (1.76e-03), or(X,X) (1.76e-03)
    - 1.87e-03 -> mono {C:1}   via THEM(^D) (9.10e-04), THEM(^X) (8.83e-04), or(X,THEM(^D)) (2.66e-05), or(X,THEM(^X)) (2.66e-05)
    - 8.80e-05 -> poly {C:0.5, and(THEM(ME),X):0.5}   via and(THEM(ME),X) (8.80e-05)
    - 8.80e-05 -> poly {C:0.5, and(X,THEM(ME)):0.5}   via and(X,THEM(ME)) (8.80e-05)
    - 5.63e-05 -> neutral {C:0.63, THEM(^C):0.36, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (5.63e-05)
- neutral {D:0.98, THEM(ME):0.02}
    - 1.97e-02 -> neutral {D:0.99, THEM(ME):0.01}   via D (6.58e-03), C (6.51e-03), X (6.19e-03), and(X,X) (1.49e-04)
    - 1.67e-02 -> neutral {D:0.97, THEM(ME):0.03}   via C (6.51e-03), X (6.19e-03), THEM(ME) (3.62e-03), and(X,X) (1.49e-04)
    - 3.59e-03 -> neutral {D:0.97, THEM(ME):0.02, THEM(THEM):0.01}   via THEM(THEM) (3.59e-03)
    - 9.10e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-04)
    - 8.92e-04 -> neutral {D:0.97, THEM(ME):0.02, THEM(^D):0.01}   via THEM(^D) (8.92e-04)
    - 8.83e-04 -> mono {THEM(^X):1}   via THEM(^X) (8.83e-04)
- neutral {D:0.98, THEM(THEM):0.02}
    - 1.97e-02 -> neutral {D:0.99, THEM(THEM):0.01}   via D (6.58e-03), C (6.51e-03), X (6.19e-03), and(X,X) (1.49e-04)
    - 1.67e-02 -> neutral {D:0.97, THEM(THEM):0.03}   via C (6.51e-03), X (6.19e-03), THEM(THEM) (3.59e-03), and(X,X) (1.49e-04)
    - 3.62e-03 -> neutral {D:0.97, THEM(ME):0.01, THEM(THEM):0.02}   via THEM(ME) (3.62e-03)
    - 9.10e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-04)
    - 8.92e-04 -> neutral {D:0.97, THEM(THEM):0.02, THEM(^D):0.01}   via THEM(^D) (8.92e-04)
    - 8.83e-04 -> mono {THEM(^X):1}   via THEM(^X) (8.83e-04)
- neutral {C:0.62, THEM(^C):0.38}
    - 2.84e-01 -> neutral {C:0.63, THEM(^C):0.37}   via C (1.25e-01), D (7.83e-02), X (7.44e-02), and(X,X) (1.79e-03)
    - 1.59e-01 -> neutral {C:0.61, THEM(^C):0.39}   via D (7.83e-02), X (7.44e-02), and(X,X) (1.79e-03), or(X,X) (1.79e-03)
    - 1.87e-03 -> mono {C:1}   via THEM(^D) (9.10e-04), THEM(^X) (8.83e-04), or(X,THEM(^D)) (2.66e-05), or(X,THEM(^X)) (2.66e-05)
    - 8.80e-05 -> poly {C:0.5, and(THEM(ME),X):0.5}   via and(THEM(ME),X) (8.80e-05)
    - 8.80e-05 -> poly {C:0.5, and(X,THEM(ME)):0.5}   via and(X,THEM(ME)) (8.80e-05)
    - 5.46e-05 -> neutral {C:0.61, THEM(^C):0.38, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (5.46e-05)
- neutral {C:0.65, THEM(^C):0.35}
    - 2.69e-01 -> neutral {C:0.66, THEM(^C):0.34}   via C (1.15e-01), D (7.56e-02), X (7.18e-02), and(X,X) (1.73e-03)
    - 1.54e-01 -> neutral {C:0.64, THEM(^C):0.36}   via D (7.56e-02), X (7.18e-02), and(X,X) (1.73e-03), or(X,X) (1.73e-03)
    - 1.87e-03 -> mono {C:1}   via THEM(^D) (9.10e-04), THEM(^X) (8.83e-04), or(X,THEM(^D)) (2.66e-05), or(X,THEM(^X)) (2.66e-05)
    - 8.80e-05 -> poly {C:0.5, and(THEM(ME),X):0.5}   via and(THEM(ME),X) (8.80e-05)
    - 8.80e-05 -> poly {C:0.5, and(X,THEM(ME)):0.5}   via and(X,THEM(ME)) (8.80e-05)
    - 5.72e-05 -> neutral {C:0.64, THEM(^C):0.35, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (5.72e-05)
- neutral {D:0.99, THEM(^D):0.01}
    - 9.89e-03 -> mono {D:1}   via D (3.29e-03), C (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 7.50e-03 -> neutral {D:0.98, THEM(^D):0.02}   via C (3.29e-03), X (3.12e-03), THEM(^D) (9.01e-04), and(X,X) (7.54e-05)
    - 3.66e-03 -> neutral {D:0.98, THEM(ME):0.01, THEM(^D):0.01}   via THEM(ME) (3.66e-03)
    - 3.63e-03 -> neutral {D:0.98, THEM(THEM):0.01, THEM(^D):0.01}   via THEM(THEM) (3.63e-03)
    - 1.67e-03 -> neutral {D:0.93, THEM(^D):0.07}   via THEM(^C) (8.33e-04), THEM(^X) (8.09e-04), THEM(^or(X,X)) (1.22e-05), THEM(^and(X,X)) (1.22e-05)
    - 2.27e-04 -> neutral {D:0.98, THEM(^D):0.01, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (2.27e-04)
- neutral {D:0.98, THEM(ME):0.01, THEM(THEM):0.01}
    - 1.02e-02 -> neutral {D:0.97, THEM(ME):0.02, THEM(THEM):0.01}   via THEM(ME) (3.62e-03), C (3.26e-03), X (3.09e-03), and(X,X) (7.47e-05)
    - 1.01e-02 -> neutral {D:0.97, THEM(ME):0.01, THEM(THEM):0.02}   via THEM(THEM) (3.59e-03), C (3.26e-03), X (3.09e-03), and(X,X) (7.47e-05)
    - 9.83e-03 -> neutral {D:0.99, THEM(THEM):0.01}   via D (3.29e-03), C (3.26e-03), X (3.09e-03), and(X,X) (7.47e-05)
    - 9.83e-03 -> neutral {D:0.99, THEM(ME):0.01}   via D (3.29e-03), C (3.26e-03), X (3.09e-03), and(X,X) (7.47e-05)
    - 9.10e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-04)
    - 8.92e-04 -> neutral {D:0.97, THEM(ME):0.01, THEM(THEM):0.01, THEM(^D):0.01}   via THEM(^D) (8.92e-04)
- neutral {C:0.61, THEM(^C):0.39}
    - 2.89e-01 -> neutral {C:0.62, THEM(^C):0.38}   via C (1.28e-01), D (7.90e-02), X (7.51e-02), and(X,X) (1.81e-03)
    - 1.61e-01 -> neutral {C:0.6, THEM(^C):0.4}   via D (7.90e-02), X (7.51e-02), and(X,X) (1.81e-03), or(X,X) (1.81e-03)
    - 1.87e-03 -> mono {C:1}   via THEM(^D) (9.10e-04), THEM(^X) (8.83e-04), or(X,THEM(^D)) (2.66e-05), or(X,THEM(^X)) (2.66e-05)
    - 8.80e-05 -> poly {C:0.5, and(THEM(ME),X):0.5}   via and(THEM(ME),X) (8.80e-05)
    - 8.80e-05 -> poly {C:0.5, and(X,THEM(ME)):0.5}   via and(X,THEM(ME)) (8.80e-05)
    - 5.37e-05 -> neutral {C:0.6, THEM(^C):0.39, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (5.37e-05)

INDETERMINATE transitions (replicator did not converge): 619; first: from poly {X:0.488, THEM(THEM):0.14, and(X,THEM(^X)):0.372} with mutant or(X,THEM(^X))
