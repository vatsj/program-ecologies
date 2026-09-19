### arm=weak, n=6, game=stag, N=100, x_on=True, role=False, mode=square

programs 1852, classes 46, states 11698, terminal classes 2, indeterminate 0, divergence rate 0.0019
mean payoff 4.0000, efficient 4.0000, deadweight loss -0.0000, mean bits in support 2.62
absorption: class 0: 1.000, class 1: 0.000

| pi | state |
|---|---|
| 0.8317 | mono {C:1} |
| 0.0758 | neutral {C:0.99, THEM(^C):0.01} |
| 0.0290 | neutral {C:0.98, THEM(^C):0.02} |
| 0.0139 | neutral {C:0.97, THEM(^C):0.03} |
| 0.0073 | neutral {C:0.99, or(X,THEM(ME)):0.01} |
| 0.0073 | neutral {C:0.99, or(X,THEM(THEM)):0.01} |
| 0.0073 | neutral {C:0.96, THEM(^C):0.04} |
| 0.0040 | neutral {C:0.95, THEM(^C):0.05} |
| 0.0025 | neutral {C:0.98, or(X,THEM(ME)):0.02} |
| 0.0025 | neutral {C:0.98, or(X,THEM(THEM)):0.02} |
| 0.0023 | neutral {C:0.94, THEM(^C):0.06} |
| 0.0022 | neutral {C:0.99, or(X,THEM(^C)):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 9.10e-04 -> neutral {C:0.99, THEM(^C):0.01}   via THEM(^C) (9.10e-04)
    - 8.80e-05 -> neutral {C:0.99, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (8.80e-05)
    - 8.80e-05 -> neutral {C:0.99, or(X,THEM(ME)):0.01}   via or(X,THEM(ME)) (8.80e-05)
    - 2.66e-05 -> neutral {C:0.99, or(X,THEM(^C)):0.01}   via or(X,THEM(^C)) (2.66e-05)
- neutral {C:0.99, THEM(^C):0.01}
    - 9.99e-03 -> mono {C:1}   via C (3.29e-03), D (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 7.60e-03 -> neutral {C:0.98, THEM(^C):0.02}   via D (3.29e-03), X (3.12e-03), THEM(^C) (9.01e-04), and(X,X) (7.54e-05)
    - 8.71e-05 -> neutral {C:0.98, THEM(^C):0.01, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (8.71e-05)
    - 8.71e-05 -> neutral {C:0.98, THEM(^C):0.01, or(X,THEM(ME)):0.01}   via or(X,THEM(ME)) (8.71e-05)
    - 2.63e-05 -> neutral {C:0.98, THEM(^C):0.01, or(X,THEM(^C)):0.01}   via or(X,THEM(^C)) (2.63e-05)
    - 8.80e-07 -> neutral {C:0.99, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (8.80e-07)
- neutral {C:0.98, THEM(^C):0.02}
    - 1.98e-02 -> neutral {C:0.99, THEM(^C):0.01}   via C (6.58e-03), D (6.51e-03), X (6.19e-03), and(X,X) (1.49e-04)
    - 1.42e-02 -> neutral {C:0.97, THEM(^C):0.03}   via D (6.51e-03), X (6.19e-03), THEM(^C) (8.92e-04), and(X,X) (1.49e-04)
    - 8.62e-05 -> neutral {C:0.97, THEM(^C):0.02, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (8.62e-05)
    - 8.62e-05 -> neutral {C:0.97, THEM(^C):0.02, or(X,THEM(ME)):0.01}   via or(X,THEM(ME)) (8.62e-05)
    - 2.60e-05 -> neutral {C:0.97, THEM(^C):0.02, or(X,THEM(^C)):0.01}   via or(X,THEM(^C)) (2.60e-05)
    - 1.76e-06 -> neutral {C:0.98, THEM(^C):0.01, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (1.76e-06)
- neutral {C:0.97, THEM(^C):0.03}
    - 2.96e-02 -> neutral {C:0.98, THEM(^C):0.02}   via C (9.87e-03), D (9.67e-03), X (9.18e-03), and(X,X) (2.22e-04)
    - 2.06e-02 -> neutral {C:0.96, THEM(^C):0.04}   via D (9.67e-03), X (9.18e-03), THEM(^C) (8.83e-04), and(X,X) (2.22e-04)
    - 8.54e-05 -> neutral {C:0.96, THEM(^C):0.03, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (8.54e-05)
    - 8.54e-05 -> neutral {C:0.96, THEM(^C):0.03, or(X,THEM(ME)):0.01}   via or(X,THEM(ME)) (8.54e-05)
    - 2.58e-05 -> neutral {C:0.96, THEM(^C):0.03, or(X,THEM(^C)):0.01}   via or(X,THEM(^C)) (2.58e-05)
    - 2.64e-06 -> neutral {C:0.97, THEM(^C):0.02, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (2.64e-06)
- neutral {C:0.99, or(X,THEM(ME)):0.01}
    - 9.99e-03 -> mono {C:1}   via C (3.29e-03), D (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 6.79e-03 -> neutral {C:0.98, or(X,THEM(ME)):0.02}   via D (3.29e-03), X (3.12e-03), or(X,THEM(ME)) (8.71e-05), and(X,X) (7.54e-05)
    - 9.01e-04 -> neutral {C:0.98, THEM(^C):0.01, or(X,THEM(ME)):0.01}   via THEM(^C) (9.01e-04)
    - 8.71e-05 -> neutral {C:0.98, or(X,THEM(ME)):0.01, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (8.71e-05)
    - 2.63e-05 -> neutral {C:0.98, or(X,THEM(ME)):0.01, or(X,THEM(^C)):0.01}   via or(X,THEM(^C)) (2.63e-05)
    - 9.10e-06 -> neutral {C:0.99, THEM(^C):0.01}   via THEM(^C) (9.10e-06)
- neutral {C:0.99, or(X,THEM(THEM)):0.01}
    - 9.99e-03 -> mono {C:1}   via C (3.29e-03), D (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 6.79e-03 -> neutral {C:0.98, or(X,THEM(THEM)):0.02}   via D (3.29e-03), X (3.12e-03), or(X,THEM(THEM)) (8.71e-05), and(X,X) (7.54e-05)
    - 9.01e-04 -> neutral {C:0.98, THEM(^C):0.01, or(X,THEM(THEM)):0.01}   via THEM(^C) (9.01e-04)
    - 8.71e-05 -> neutral {C:0.98, or(X,THEM(ME)):0.01, or(X,THEM(THEM)):0.01}   via or(X,THEM(ME)) (8.71e-05)
    - 2.63e-05 -> neutral {C:0.98, or(X,THEM(THEM)):0.01, or(X,THEM(^C)):0.01}   via or(X,THEM(^C)) (2.63e-05)
    - 9.10e-06 -> neutral {C:0.99, THEM(^C):0.01}   via THEM(^C) (9.10e-06)
- neutral {C:0.96, THEM(^C):0.04}
    - 3.91e-02 -> neutral {C:0.97, THEM(^C):0.03}   via C (1.32e-02), D (1.28e-02), X (1.21e-02), and(X,X) (2.93e-04)
    - 2.69e-02 -> neutral {C:0.95, THEM(^C):0.05}   via D (1.28e-02), X (1.21e-02), THEM(^C) (8.74e-04), and(X,X) (2.93e-04)
    - 8.45e-05 -> neutral {C:0.95, THEM(^C):0.04, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (8.45e-05)
    - 8.45e-05 -> neutral {C:0.95, THEM(^C):0.04, or(X,THEM(ME)):0.01}   via or(X,THEM(ME)) (8.45e-05)
    - 2.55e-05 -> neutral {C:0.95, THEM(^C):0.04, or(X,THEM(^C)):0.01}   via or(X,THEM(^C)) (2.55e-05)
    - 3.52e-06 -> neutral {C:0.96, THEM(^C):0.03, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (3.52e-06)
- neutral {C:0.95, THEM(^C):0.05}
    - 4.86e-02 -> neutral {C:0.96, THEM(^C):0.04}   via C (1.64e-02), D (1.58e-02), X (1.50e-02), and(X,X) (3.62e-04)
    - 3.30e-02 -> neutral {C:0.94, THEM(^C):0.06}   via D (1.58e-02), X (1.50e-02), THEM(^C) (8.65e-04), and(X,X) (3.62e-04)
    - 8.36e-05 -> neutral {C:0.94, THEM(^C):0.05, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (8.36e-05)
    - 8.36e-05 -> neutral {C:0.94, THEM(^C):0.05, or(X,THEM(ME)):0.01}   via or(X,THEM(ME)) (8.36e-05)
    - 2.52e-05 -> neutral {C:0.94, THEM(^C):0.05, or(X,THEM(^C)):0.01}   via or(X,THEM(^C)) (2.52e-05)
    - 4.40e-06 -> neutral {C:0.95, THEM(^C):0.04, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (4.40e-06)
- neutral {C:0.98, or(X,THEM(ME)):0.02}
    - 1.98e-02 -> neutral {C:0.99, or(X,THEM(ME)):0.01}   via C (6.58e-03), D (6.51e-03), X (6.19e-03), and(X,X) (1.49e-04)
    - 1.33e-02 -> neutral {C:0.97, or(X,THEM(ME)):0.03}   via D (6.51e-03), X (6.19e-03), and(X,X) (1.49e-04), or(X,X) (1.49e-04)
    - 8.92e-04 -> neutral {C:0.97, THEM(^C):0.01, or(X,THEM(ME)):0.02}   via THEM(^C) (8.92e-04)
    - 8.62e-05 -> neutral {C:0.97, or(X,THEM(ME)):0.02, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (8.62e-05)
    - 2.60e-05 -> neutral {C:0.97, or(X,THEM(ME)):0.02, or(X,THEM(^C)):0.01}   via or(X,THEM(^C)) (2.60e-05)
    - 1.82e-05 -> neutral {C:0.98, THEM(^C):0.01, or(X,THEM(ME)):0.01}   via THEM(^C) (1.82e-05)
- neutral {C:0.98, or(X,THEM(THEM)):0.02}
    - 1.98e-02 -> neutral {C:0.99, or(X,THEM(THEM)):0.01}   via C (6.58e-03), D (6.51e-03), X (6.19e-03), and(X,X) (1.49e-04)
    - 1.33e-02 -> neutral {C:0.97, or(X,THEM(THEM)):0.03}   via D (6.51e-03), X (6.19e-03), and(X,X) (1.49e-04), or(X,X) (1.49e-04)
    - 8.92e-04 -> neutral {C:0.97, THEM(^C):0.01, or(X,THEM(THEM)):0.02}   via THEM(^C) (8.92e-04)
    - 8.62e-05 -> neutral {C:0.97, or(X,THEM(ME)):0.01, or(X,THEM(THEM)):0.02}   via or(X,THEM(ME)) (8.62e-05)
    - 2.60e-05 -> neutral {C:0.97, or(X,THEM(THEM)):0.02, or(X,THEM(^C)):0.01}   via or(X,THEM(^C)) (2.60e-05)
    - 1.82e-05 -> neutral {C:0.98, THEM(^C):0.01, or(X,THEM(THEM)):0.01}   via THEM(^C) (1.82e-05)
- neutral {C:0.94, THEM(^C):0.06}
    - 5.79e-02 -> neutral {C:0.95, THEM(^C):0.05}   via C (1.97e-02), D (1.87e-02), X (1.78e-02), and(X,X) (4.30e-04)
    - 3.90e-02 -> neutral {C:0.93, THEM(^C):0.07}   via D (1.87e-02), X (1.78e-02), THEM(^C) (8.55e-04), and(X,X) (4.30e-04)
    - 8.27e-05 -> neutral {C:0.93, THEM(^C):0.06, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (8.27e-05)
    - 8.27e-05 -> neutral {C:0.93, THEM(^C):0.06, or(X,THEM(ME)):0.01}   via or(X,THEM(ME)) (8.27e-05)
    - 2.50e-05 -> neutral {C:0.93, THEM(^C):0.06, or(X,THEM(^C)):0.01}   via or(X,THEM(^C)) (2.50e-05)
    - 5.28e-06 -> neutral {C:0.94, THEM(^C):0.05, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (5.28e-06)
- neutral {C:0.99, or(X,THEM(^C)):0.01}
    - 9.99e-03 -> mono {C:1}   via C (3.29e-03), D (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 6.73e-03 -> neutral {C:0.98, or(X,THEM(^C)):0.02}   via D (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05), or(X,X) (7.54e-05)
    - 9.01e-04 -> neutral {C:0.98, THEM(^C):0.01, or(X,THEM(^C)):0.01}   via THEM(^C) (9.01e-04)
    - 8.71e-05 -> neutral {C:0.98, or(X,THEM(THEM)):0.01, or(X,THEM(^C)):0.01}   via or(X,THEM(THEM)) (8.71e-05)
    - 8.71e-05 -> neutral {C:0.98, or(X,THEM(ME)):0.01, or(X,THEM(^C)):0.01}   via or(X,THEM(ME)) (8.71e-05)
    - 9.10e-06 -> neutral {C:0.99, THEM(^C):0.01}   via THEM(^C) (9.10e-06)
