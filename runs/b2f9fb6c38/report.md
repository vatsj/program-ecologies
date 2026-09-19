### arm=weak, n=6, game=dollar, N=100, x_on=True, role=False, mode=square

programs 1852, classes 46, states 56728, terminal classes 2, indeterminate 0, divergence rate 0.0019
mean payoff 0.5000, efficient 0.5000, deadweight loss 0.0000, mean bits in support 2.75
absorption: class 0: 1.000, class 10: 0.000

| pi | state |
|---|---|
| 0.2342 | mono {C:1} |
| 0.0873 | neutral {C:0.99, THEM(ME):0.01} |
| 0.0866 | neutral {C:0.99, THEM(THEM):0.01} |
| 0.0455 | neutral {C:0.98, THEM(ME):0.02} |
| 0.0451 | neutral {C:0.98, THEM(THEM):0.02} |
| 0.0322 | neutral {C:0.98, THEM(ME):0.01, THEM(THEM):0.01} |
| 0.0260 | neutral {C:0.97, THEM(ME):0.03} |
| 0.0257 | neutral {C:0.97, THEM(THEM):0.03} |
| 0.0215 | neutral {C:0.99, THEM(^C):0.01} |
| 0.0167 | neutral {C:0.97, THEM(ME):0.02, THEM(THEM):0.01} |
| 0.0167 | neutral {C:0.97, THEM(ME):0.01, THEM(THEM):0.02} |
| 0.0154 | neutral {C:0.96, THEM(ME):0.04} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 3.69e-03 -> neutral {C:0.99, THEM(ME):0.01}   via THEM(ME) (3.69e-03)
    - 3.67e-03 -> neutral {C:0.99, THEM(THEM):0.01}   via THEM(THEM) (3.67e-03)
    - 9.10e-04 -> neutral {C:0.99, THEM(^C):0.01}   via THEM(^C) (9.10e-04)
    - 2.29e-04 -> neutral {C:0.99, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (2.29e-04)
    - 8.80e-05 -> neutral {C:0.99, or(THEM(THEM),X):0.01}   via or(THEM(THEM),X) (8.80e-05)
    - 8.80e-05 -> neutral {C:0.99, or(THEM(ME),X):0.01}   via or(THEM(ME),X) (8.80e-05)
- neutral {C:0.99, THEM(ME):0.01}
    - 1.03e-02 -> neutral {C:0.98, THEM(ME):0.02}   via THEM(ME) (3.66e-03), D (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 9.91e-03 -> mono {C:1}   via C (3.29e-03), D (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 3.63e-03 -> neutral {C:0.98, THEM(ME):0.01, THEM(THEM):0.01}   via THEM(THEM) (3.63e-03)
    - 9.01e-04 -> neutral {C:0.98, THEM(ME):0.01, THEM(^C):0.01}   via THEM(^C) (9.01e-04)
    - 2.27e-04 -> neutral {C:0.98, THEM(ME):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (2.27e-04)
    - 8.71e-05 -> neutral {C:0.98, THEM(ME):0.01, or(THEM(THEM),X):0.01}   via or(THEM(THEM),X) (8.71e-05)
- neutral {C:0.99, THEM(THEM):0.01}
    - 1.03e-02 -> neutral {C:0.98, THEM(THEM):0.02}   via THEM(THEM) (3.63e-03), D (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 9.91e-03 -> mono {C:1}   via C (3.29e-03), D (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 3.66e-03 -> neutral {C:0.98, THEM(ME):0.01, THEM(THEM):0.01}   via THEM(ME) (3.66e-03)
    - 9.01e-04 -> neutral {C:0.98, THEM(THEM):0.01, THEM(^C):0.01}   via THEM(^C) (9.01e-04)
    - 2.27e-04 -> neutral {C:0.98, THEM(THEM):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (2.27e-04)
    - 8.71e-05 -> neutral {C:0.98, THEM(THEM):0.01, or(THEM(THEM),X):0.01}   via or(THEM(THEM),X) (8.71e-05)
- neutral {C:0.98, THEM(ME):0.02}
    - 1.97e-02 -> neutral {C:0.99, THEM(ME):0.01}   via C (6.58e-03), D (6.51e-03), X (6.19e-03), and(X,X) (1.49e-04)
    - 1.67e-02 -> neutral {C:0.97, THEM(ME):0.03}   via D (6.51e-03), X (6.19e-03), THEM(ME) (3.62e-03), and(X,X) (1.49e-04)
    - 3.59e-03 -> neutral {C:0.97, THEM(ME):0.02, THEM(THEM):0.01}   via THEM(THEM) (3.59e-03)
    - 8.92e-04 -> neutral {C:0.97, THEM(ME):0.02, THEM(^C):0.01}   via THEM(^C) (8.92e-04)
    - 2.25e-04 -> neutral {C:0.97, THEM(ME):0.02, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (2.25e-04)
    - 8.62e-05 -> neutral {C:0.97, THEM(ME):0.02, or(THEM(THEM),X):0.01}   via or(THEM(THEM),X) (8.62e-05)
- neutral {C:0.98, THEM(THEM):0.02}
    - 1.97e-02 -> neutral {C:0.99, THEM(THEM):0.01}   via C (6.58e-03), D (6.51e-03), X (6.19e-03), and(X,X) (1.49e-04)
    - 1.67e-02 -> neutral {C:0.97, THEM(THEM):0.03}   via D (6.51e-03), X (6.19e-03), THEM(THEM) (3.59e-03), and(X,X) (1.49e-04)
    - 3.62e-03 -> neutral {C:0.97, THEM(ME):0.01, THEM(THEM):0.02}   via THEM(ME) (3.62e-03)
    - 8.92e-04 -> neutral {C:0.97, THEM(THEM):0.02, THEM(^C):0.01}   via THEM(^C) (8.92e-04)
    - 2.25e-04 -> neutral {C:0.97, THEM(THEM):0.02, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (2.25e-04)
    - 8.62e-05 -> neutral {C:0.97, THEM(THEM):0.02, or(THEM(THEM),X):0.01}   via or(THEM(THEM),X) (8.62e-05)
- neutral {C:0.98, THEM(ME):0.01, THEM(THEM):0.01}
    - 1.02e-02 -> neutral {C:0.97, THEM(ME):0.02, THEM(THEM):0.01}   via THEM(ME) (3.62e-03), D (3.26e-03), X (3.09e-03), and(X,X) (7.47e-05)
    - 1.01e-02 -> neutral {C:0.97, THEM(ME):0.01, THEM(THEM):0.02}   via THEM(THEM) (3.59e-03), D (3.26e-03), X (3.09e-03), and(X,X) (7.47e-05)
    - 9.84e-03 -> neutral {C:0.99, THEM(THEM):0.01}   via C (3.29e-03), D (3.26e-03), X (3.09e-03), and(X,X) (7.47e-05)
    - 9.84e-03 -> neutral {C:0.99, THEM(ME):0.01}   via C (3.29e-03), D (3.26e-03), X (3.09e-03), and(X,X) (7.47e-05)
    - 8.92e-04 -> neutral {C:0.97, THEM(ME):0.01, THEM(THEM):0.01, THEM(^C):0.01}   via THEM(^C) (8.92e-04)
    - 2.25e-04 -> neutral {C:0.97, THEM(ME):0.01, THEM(THEM):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (2.25e-04)
- neutral {C:0.97, THEM(ME):0.03}
    - 2.93e-02 -> neutral {C:0.98, THEM(ME):0.02}   via C (9.87e-03), D (9.67e-03), X (9.18e-03), and(X,X) (2.22e-04)
    - 2.30e-02 -> neutral {C:0.96, THEM(ME):0.04}   via D (9.67e-03), X (9.18e-03), THEM(ME) (3.58e-03), and(X,X) (2.22e-04)
    - 3.56e-03 -> neutral {C:0.96, THEM(ME):0.03, THEM(THEM):0.01}   via THEM(THEM) (3.56e-03)
    - 8.83e-04 -> neutral {C:0.96, THEM(ME):0.03, THEM(^C):0.01}   via THEM(^C) (8.83e-04)
    - 2.22e-04 -> neutral {C:0.96, THEM(ME):0.03, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (2.22e-04)
    - 1.10e-04 -> neutral {C:0.97, THEM(ME):0.02, THEM(THEM):0.01}   via THEM(THEM) (1.10e-04)
- neutral {C:0.97, THEM(THEM):0.03}
    - 2.93e-02 -> neutral {C:0.98, THEM(THEM):0.02}   via C (9.87e-03), D (9.67e-03), X (9.18e-03), and(X,X) (2.22e-04)
    - 2.30e-02 -> neutral {C:0.96, THEM(THEM):0.04}   via D (9.67e-03), X (9.18e-03), THEM(THEM) (3.56e-03), and(X,X) (2.22e-04)
    - 3.58e-03 -> neutral {C:0.96, THEM(ME):0.01, THEM(THEM):0.03}   via THEM(ME) (3.58e-03)
    - 8.83e-04 -> neutral {C:0.96, THEM(THEM):0.03, THEM(^C):0.01}   via THEM(^C) (8.83e-04)
    - 2.22e-04 -> neutral {C:0.96, THEM(THEM):0.03, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (2.22e-04)
    - 1.11e-04 -> neutral {C:0.97, THEM(ME):0.01, THEM(THEM):0.02}   via THEM(ME) (1.11e-04)
- neutral {C:0.99, THEM(^C):0.01}
    - 9.91e-03 -> mono {C:1}   via C (3.29e-03), D (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 7.52e-03 -> neutral {C:0.98, THEM(^C):0.02}   via D (3.29e-03), X (3.12e-03), THEM(^C) (9.01e-04), and(X,X) (7.54e-05)
    - 3.66e-03 -> neutral {C:0.98, THEM(ME):0.01, THEM(^C):0.01}   via THEM(ME) (3.66e-03)
    - 3.63e-03 -> neutral {C:0.98, THEM(THEM):0.01, THEM(^C):0.01}   via THEM(THEM) (3.63e-03)
    - 2.27e-04 -> neutral {C:0.98, THEM(^C):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (2.27e-04)
    - 8.71e-05 -> neutral {C:0.98, THEM(^C):0.01, or(THEM(THEM),X):0.01}   via or(THEM(THEM),X) (8.71e-05)
- neutral {C:0.97, THEM(ME):0.02, THEM(THEM):0.01}
    - 1.96e-02 -> neutral {C:0.98, THEM(ME):0.01, THEM(THEM):0.01}   via C (6.58e-03), D (6.45e-03), X (6.12e-03), and(X,X) (1.48e-04)
    - 1.66e-02 -> neutral {C:0.96, THEM(ME):0.03, THEM(THEM):0.01}   via D (6.45e-03), X (6.12e-03), THEM(ME) (3.58e-03), and(X,X) (1.48e-04)
    - 1.00e-02 -> neutral {C:0.96, THEM(ME):0.02, THEM(THEM):0.02}   via THEM(THEM) (3.56e-03), D (3.22e-03), X (3.06e-03), and(X,X) (7.39e-05)
    - 9.78e-03 -> neutral {C:0.98, THEM(ME):0.02}   via C (3.29e-03), D (3.22e-03), X (3.06e-03), and(X,X) (7.39e-05)
    - 8.83e-04 -> neutral {C:0.96, THEM(ME):0.02, THEM(THEM):0.01, THEM(^C):0.01}   via THEM(^C) (8.83e-04)
    - 2.22e-04 -> neutral {C:0.96, THEM(ME):0.02, THEM(THEM):0.01, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (2.22e-04)
- neutral {C:0.97, THEM(ME):0.01, THEM(THEM):0.02}
    - 1.96e-02 -> neutral {C:0.98, THEM(ME):0.01, THEM(THEM):0.01}   via C (6.58e-03), D (6.45e-03), X (6.12e-03), and(X,X) (1.48e-04)
    - 1.65e-02 -> neutral {C:0.96, THEM(ME):0.01, THEM(THEM):0.03}   via D (6.45e-03), X (6.12e-03), THEM(THEM) (3.56e-03), and(X,X) (1.48e-04)
    - 1.01e-02 -> neutral {C:0.96, THEM(ME):0.02, THEM(THEM):0.02}   via THEM(ME) (3.58e-03), D (3.22e-03), X (3.06e-03), and(X,X) (7.39e-05)
    - 9.78e-03 -> neutral {C:0.98, THEM(THEM):0.02}   via C (3.29e-03), D (3.22e-03), X (3.06e-03), and(X,X) (7.39e-05)
    - 8.83e-04 -> neutral {C:0.96, THEM(ME):0.01, THEM(THEM):0.02, THEM(^C):0.01}   via THEM(^C) (8.83e-04)
    - 2.22e-04 -> neutral {C:0.96, THEM(ME):0.01, THEM(THEM):0.02, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (2.22e-04)
- neutral {C:0.96, THEM(ME):0.04}
    - 3.88e-02 -> neutral {C:0.97, THEM(ME):0.03}   via C (1.32e-02), D (1.28e-02), X (1.21e-02), and(X,X) (2.93e-04)
    - 2.92e-02 -> neutral {C:0.95, THEM(ME):0.05}   via D (1.28e-02), X (1.21e-02), THEM(ME) (3.54e-03), and(X,X) (2.93e-04)
    - 3.52e-03 -> neutral {C:0.95, THEM(ME):0.04, THEM(THEM):0.01}   via THEM(THEM) (3.52e-03)
    - 8.74e-04 -> neutral {C:0.95, THEM(ME):0.04, THEM(^C):0.01}   via THEM(^C) (8.74e-04)
    - 2.20e-04 -> neutral {C:0.95, THEM(ME):0.04, or(THEM(ME),C):0.01}   via or(THEM(ME),C) (2.20e-04)
    - 1.47e-04 -> neutral {C:0.96, THEM(ME):0.03, THEM(THEM):0.01}   via THEM(THEM) (1.47e-04)
