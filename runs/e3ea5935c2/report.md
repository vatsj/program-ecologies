### arm=strong, n=6, game=stag, N=100, x_on=True, role=False, mode=square

programs 1726, classes 21, states 3186, terminal classes 2, indeterminate 0, divergence rate 0.0004
mean payoff 3.3347, efficient 4.0000, deadweight loss 0.6653, mean bits in support 2.64
absorption: class 0: 0.335, class 2: 0.665

| pi | state |
|---|---|
| 0.3357 | mono {D:1} |
| 0.3296 | mono {C:1} |
| 0.1294 | neutral {D:0.99, THEM(ME):0.01} |
| 0.0683 | neutral {D:0.98, THEM(ME):0.02} |
| 0.0392 | neutral {D:0.97, THEM(ME):0.03} |
| 0.0233 | neutral {D:0.96, THEM(ME):0.04} |
| 0.0142 | neutral {D:0.95, THEM(ME):0.05} |
| 0.0087 | neutral {D:0.94, THEM(ME):0.06} |
| 0.0054 | neutral {D:0.93, THEM(ME):0.07} |
| 0.0041 | neutral {D:0.99, and(THEM(ME),D):0.01} |
| 0.0034 | neutral {D:0.92, THEM(ME):0.08} |
| 0.0031 | neutral {D:0.99, and(THEM(ME),X):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.84e-03 -> neutral {D:0.99, THEM(ME):0.01}   via THEM(ME) (3.84e-03)
    - 1.22e-04 -> neutral {D:0.99, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.22e-04)
    - 9.32e-05 -> neutral {D:0.99, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (9.32e-05)
    - 9.32e-05 -> neutral {D:0.99, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (9.32e-05)
- mono {C:1}
    - 9.32e-05 -> neutral {C:0.99, or(X,THEM(ME)):0.01}   via or(X,THEM(ME)) (9.32e-05)
- neutral {D:0.99, THEM(ME):0.01}
    - 1.04e-02 -> neutral {D:0.98, THEM(ME):0.02}   via THEM(ME) (3.80e-03), C (3.32e-03), X (3.14e-03), and(X,X) (7.98e-05)
    - 9.96e-03 -> mono {D:1}   via D (3.32e-03), C (3.32e-03), X (3.14e-03), and(X,X) (7.98e-05)
    - 1.21e-04 -> neutral {D:0.98, THEM(ME):0.01, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.21e-04)
    - 9.23e-05 -> neutral {D:0.98, THEM(ME):0.01, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (9.23e-05)
    - 9.23e-05 -> neutral {D:0.98, THEM(ME):0.01, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (9.23e-05)
    - 1.22e-06 -> neutral {D:0.99, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.22e-06)
- neutral {D:0.98, THEM(ME):0.02}
    - 1.98e-02 -> neutral {D:0.99, THEM(ME):0.01}   via D (6.63e-03), C (6.56e-03), X (6.22e-03), and(X,X) (1.58e-04)
    - 1.69e-02 -> neutral {D:0.97, THEM(ME):0.03}   via C (6.56e-03), X (6.22e-03), THEM(ME) (3.76e-03), and(X,X) (1.58e-04)
    - 1.19e-04 -> neutral {D:0.97, THEM(ME):0.02, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.19e-04)
    - 9.13e-05 -> neutral {D:0.97, THEM(ME):0.02, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (9.13e-05)
    - 9.13e-05 -> neutral {D:0.97, THEM(ME):0.02, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (9.13e-05)
    - 2.44e-06 -> neutral {D:0.98, THEM(ME):0.01, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (2.44e-06)
- neutral {D:0.97, THEM(ME):0.03}
    - 2.95e-02 -> neutral {D:0.98, THEM(ME):0.02}   via D (9.95e-03), C (9.75e-03), X (9.24e-03), and(X,X) (2.34e-04)
    - 2.32e-02 -> neutral {D:0.96, THEM(ME):0.04}   via C (9.75e-03), X (9.24e-03), THEM(ME) (3.72e-03), and(X,X) (2.34e-04)
    - 1.18e-04 -> neutral {D:0.96, THEM(ME):0.03, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.18e-04)
    - 9.04e-05 -> neutral {D:0.96, THEM(ME):0.03, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (9.04e-05)
    - 9.04e-05 -> neutral {D:0.96, THEM(ME):0.03, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (9.04e-05)
    - 3.66e-06 -> neutral {D:0.97, THEM(ME):0.02, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (3.66e-06)
- neutral {D:0.96, THEM(ME):0.04}
    - 3.90e-02 -> neutral {D:0.97, THEM(ME):0.03}   via D (1.33e-02), C (1.29e-02), X (1.22e-02), and(X,X) (3.09e-04)
    - 2.95e-02 -> neutral {D:0.95, THEM(ME):0.05}   via C (1.29e-02), X (1.22e-02), THEM(ME) (3.68e-03), and(X,X) (3.09e-04)
    - 1.17e-04 -> neutral {D:0.95, THEM(ME):0.04, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.17e-04)
    - 8.95e-05 -> neutral {D:0.95, THEM(ME):0.04, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (8.95e-05)
    - 8.95e-05 -> neutral {D:0.95, THEM(ME):0.04, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (8.95e-05)
    - 4.87e-06 -> neutral {D:0.96, THEM(ME):0.03, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (4.87e-06)
- neutral {D:0.95, THEM(ME):0.05}
    - 4.85e-02 -> neutral {D:0.96, THEM(ME):0.04}   via D (1.66e-02), C (1.59e-02), X (1.51e-02), and(X,X) (3.83e-04)
    - 3.55e-02 -> neutral {D:0.94, THEM(ME):0.06}   via C (1.59e-02), X (1.51e-02), THEM(ME) (3.65e-03), and(X,X) (3.83e-04)
    - 1.16e-04 -> neutral {D:0.94, THEM(ME):0.05, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.16e-04)
    - 8.86e-05 -> neutral {D:0.94, THEM(ME):0.05, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (8.86e-05)
    - 8.86e-05 -> neutral {D:0.94, THEM(ME):0.05, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (8.86e-05)
    - 6.09e-06 -> neutral {D:0.95, THEM(ME):0.04, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (6.09e-06)
- neutral {D:0.94, THEM(ME):0.06}
    - 5.77e-02 -> neutral {D:0.95, THEM(ME):0.05}   via D (1.99e-02), C (1.89e-02), X (1.79e-02), and(X,X) (4.54e-04)
    - 4.15e-02 -> neutral {D:0.93, THEM(ME):0.07}   via C (1.89e-02), X (1.79e-02), THEM(ME) (3.61e-03), and(X,X) (4.54e-04)
    - 1.15e-04 -> neutral {D:0.93, THEM(ME):0.06, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.15e-04)
    - 8.76e-05 -> neutral {D:0.93, THEM(ME):0.06, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (8.76e-05)
    - 8.76e-05 -> neutral {D:0.93, THEM(ME):0.06, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (8.76e-05)
    - 7.31e-06 -> neutral {D:0.94, THEM(ME):0.05, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (7.31e-06)
- neutral {D:0.93, THEM(ME):0.07}
    - 6.69e-02 -> neutral {D:0.94, THEM(ME):0.06}   via D (2.32e-02), C (2.18e-02), X (2.07e-02), and(X,X) (5.25e-04)
    - 4.73e-02 -> neutral {D:0.92, THEM(ME):0.08}   via C (2.18e-02), X (2.07e-02), THEM(ME) (3.57e-03), and(X,X) (5.25e-04)
    - 1.13e-04 -> neutral {D:0.92, THEM(ME):0.07, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.13e-04)
    - 8.67e-05 -> neutral {D:0.92, THEM(ME):0.07, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (8.67e-05)
    - 8.67e-05 -> neutral {D:0.92, THEM(ME):0.07, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (8.67e-05)
    - 8.53e-06 -> neutral {D:0.93, THEM(ME):0.06, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (8.53e-06)
- neutral {D:0.99, and(THEM(ME),D):0.01}
    - 9.96e-03 -> mono {D:1}   via D (3.32e-03), C (3.32e-03), X (3.14e-03), and(X,X) (7.98e-05)
    - 6.76e-03 -> neutral {D:0.98, and(THEM(ME),D):0.02}   via C (3.32e-03), X (3.14e-03), and(THEM(ME),D) (1.21e-04), and(X,X) (7.98e-05)
    - 3.80e-03 -> neutral {D:0.98, THEM(ME):0.01, and(THEM(ME),D):0.01}   via THEM(ME) (3.80e-03)
    - 9.23e-05 -> neutral {D:0.98, and(THEM(ME),D):0.01, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (9.23e-05)
    - 9.23e-05 -> neutral {D:0.98, and(X,THEM(ME)):0.01, and(THEM(ME),D):0.01}   via and(X,THEM(ME)) (9.23e-05)
    - 3.84e-05 -> neutral {D:0.99, THEM(ME):0.01}   via THEM(ME) (3.84e-05)
- neutral {D:0.92, THEM(ME):0.08}
    - 7.59e-02 -> neutral {D:0.93, THEM(ME):0.07}   via D (2.65e-02), C (2.46e-02), X (2.34e-02), and(X,X) (5.93e-04)
    - 5.29e-02 -> neutral {D:0.91, THEM(ME):0.09}   via C (2.46e-02), X (2.34e-02), THEM(ME) (3.53e-03), and(X,X) (5.93e-04)
    - 1.12e-04 -> neutral {D:0.91, THEM(ME):0.08, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.12e-04)
    - 8.58e-05 -> neutral {D:0.91, THEM(ME):0.08, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (8.58e-05)
    - 8.58e-05 -> neutral {D:0.91, THEM(ME):0.08, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (8.58e-05)
    - 9.75e-06 -> neutral {D:0.92, THEM(ME):0.07, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (9.75e-06)
- neutral {D:0.99, and(THEM(ME),X):0.01}
    - 9.96e-03 -> mono {D:1}   via D (3.32e-03), C (3.32e-03), X (3.14e-03), and(X,X) (7.98e-05)
    - 6.74e-03 -> neutral {D:0.98, and(THEM(ME),X):0.02}   via C (3.32e-03), X (3.14e-03), and(THEM(ME),X) (9.23e-05), and(X,X) (7.98e-05)
    - 3.80e-03 -> neutral {D:0.98, THEM(ME):0.01, and(THEM(ME),X):0.01}   via THEM(ME) (3.80e-03)
    - 1.21e-04 -> neutral {D:0.98, and(THEM(ME),D):0.01, and(THEM(ME),X):0.01}   via and(THEM(ME),D) (1.21e-04)
    - 9.23e-05 -> neutral {D:0.98, and(X,THEM(ME)):0.01, and(THEM(ME),X):0.01}   via and(X,THEM(ME)) (9.23e-05)
    - 3.84e-05 -> neutral {D:0.99, THEM(ME):0.01}   via THEM(ME) (3.84e-05)
