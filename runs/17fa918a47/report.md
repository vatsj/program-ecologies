### arm=weak, n=6, game=dollar, N=10, x_on=True, role=False, mode=square

programs 1852, classes 46, states 4160, terminal classes 2, indeterminate 0, divergence rate 0.0019
mean payoff 0.5000, efficient 0.5000, deadweight loss 0.0000, mean bits in support 2.76
absorption: class 0: 1.000, class 9: 0.000

| pi | state |
|---|---|
| 0.8607 | mono {C:1} |
| 0.0321 | neutral {C:0.9, THEM(ME):0.1} |
| 0.0318 | neutral {C:0.9, THEM(THEM):0.1} |
| 0.0122 | neutral {C:0.8, THEM(ME):0.2} |
| 0.0121 | neutral {C:0.8, THEM(THEM):0.2} |
| 0.0079 | neutral {C:0.9, THEM(^C):0.1} |
| 0.0058 | neutral {C:0.7, THEM(ME):0.3} |
| 0.0057 | neutral {C:0.7, THEM(THEM):0.3} |
| 0.0030 | neutral {C:0.6, THEM(ME):0.4} |
| 0.0029 | neutral {C:0.6, THEM(THEM):0.4} |
| 0.0029 | neutral {C:0.8, THEM(^C):0.2} |
| 0.0020 | neutral {C:0.9, or(THEM(ME),C):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 3.69e-03 -> neutral {C:0.9, THEM(ME):0.1}   via THEM(ME) (3.69e-03)
    - 3.67e-03 -> neutral {C:0.9, THEM(THEM):0.1}   via THEM(THEM) (3.67e-03)
    - 9.10e-04 -> neutral {C:0.9, THEM(^C):0.1}   via THEM(^C) (9.10e-04)
    - 2.29e-04 -> neutral {C:0.9, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (2.29e-04)
    - 8.80e-05 -> neutral {C:0.9, or(THEM(THEM),X):0.1}   via or(THEM(THEM),X) (8.80e-05)
    - 8.80e-05 -> neutral {C:0.9, or(THEM(ME),X):0.1}   via or(THEM(ME),X) (8.80e-05)
- neutral {C:0.9, THEM(ME):0.1}
    - 9.91e-02 -> mono {C:1}   via C (3.29e-02), D (3.29e-02), X (3.12e-02), and(X,X) (7.54e-04)
    - 6.95e-02 -> neutral {C:0.8, THEM(ME):0.2}   via D (3.29e-02), X (3.12e-02), THEM(ME) (3.32e-03), and(X,X) (7.54e-04)
    - 3.30e-03 -> neutral {C:0.8, THEM(ME):0.1, THEM(THEM):0.1}   via THEM(THEM) (3.30e-03)
    - 8.19e-04 -> neutral {C:0.8, THEM(ME):0.1, THEM(^C):0.1}   via THEM(^C) (8.19e-04)
    - 3.67e-04 -> neutral {C:0.9, THEM(THEM):0.1}   via THEM(THEM) (3.67e-04)
    - 2.06e-04 -> neutral {C:0.8, THEM(ME):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (2.06e-04)
- neutral {C:0.9, THEM(THEM):0.1}
    - 9.91e-02 -> mono {C:1}   via C (3.29e-02), D (3.29e-02), X (3.12e-02), and(X,X) (7.54e-04)
    - 6.95e-02 -> neutral {C:0.8, THEM(THEM):0.2}   via D (3.29e-02), X (3.12e-02), THEM(THEM) (3.30e-03), and(X,X) (7.54e-04)
    - 3.32e-03 -> neutral {C:0.8, THEM(ME):0.1, THEM(THEM):0.1}   via THEM(ME) (3.32e-03)
    - 8.19e-04 -> neutral {C:0.8, THEM(THEM):0.1, THEM(^C):0.1}   via THEM(^C) (8.19e-04)
    - 3.69e-04 -> neutral {C:0.9, THEM(ME):0.1}   via THEM(ME) (3.69e-04)
    - 2.06e-04 -> neutral {C:0.8, THEM(THEM):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (2.06e-04)
- neutral {C:0.8, THEM(ME):0.2}
    - 1.84e-01 -> neutral {C:0.9, THEM(ME):0.1}   via C (6.58e-02), D (5.85e-02), X (5.55e-02), and(X,X) (1.34e-03)
    - 1.21e-01 -> neutral {C:0.7, THEM(ME):0.3}   via D (5.85e-02), X (5.55e-02), THEM(ME) (2.95e-03), and(X,X) (1.34e-03)
    - 2.93e-03 -> neutral {C:0.7, THEM(ME):0.2, THEM(THEM):0.1}   via THEM(THEM) (2.93e-03)
    - 7.33e-04 -> neutral {C:0.8, THEM(ME):0.1, THEM(THEM):0.1}   via THEM(THEM) (7.33e-04)
    - 7.28e-04 -> neutral {C:0.7, THEM(ME):0.2, THEM(^C):0.1}   via THEM(^C) (7.28e-04)
    - 1.83e-04 -> neutral {C:0.7, THEM(ME):0.2, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.83e-04)
- neutral {C:0.8, THEM(THEM):0.2}
    - 1.84e-01 -> neutral {C:0.9, THEM(THEM):0.1}   via C (6.58e-02), D (5.85e-02), X (5.55e-02), and(X,X) (1.34e-03)
    - 1.21e-01 -> neutral {C:0.7, THEM(THEM):0.3}   via D (5.85e-02), X (5.55e-02), THEM(THEM) (2.93e-03), and(X,X) (1.34e-03)
    - 2.95e-03 -> neutral {C:0.7, THEM(ME):0.1, THEM(THEM):0.2}   via THEM(ME) (2.95e-03)
    - 7.38e-04 -> neutral {C:0.8, THEM(ME):0.1, THEM(THEM):0.1}   via THEM(ME) (7.38e-04)
    - 7.28e-04 -> neutral {C:0.7, THEM(THEM):0.2, THEM(^C):0.1}   via THEM(^C) (7.28e-04)
    - 1.83e-04 -> neutral {C:0.7, THEM(THEM):0.2, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.83e-04)
- neutral {C:0.9, THEM(^C):0.1}
    - 9.91e-02 -> mono {C:1}   via C (3.29e-02), D (3.29e-02), X (3.12e-02), and(X,X) (7.54e-04)
    - 6.70e-02 -> neutral {C:0.8, THEM(^C):0.2}   via D (3.29e-02), X (3.12e-02), THEM(^C) (8.19e-04), and(X,X) (7.54e-04)
    - 3.32e-03 -> neutral {C:0.8, THEM(ME):0.1, THEM(^C):0.1}   via THEM(ME) (3.32e-03)
    - 3.30e-03 -> neutral {C:0.8, THEM(THEM):0.1, THEM(^C):0.1}   via THEM(THEM) (3.30e-03)
    - 3.69e-04 -> neutral {C:0.9, THEM(ME):0.1}   via THEM(ME) (3.69e-04)
    - 3.67e-04 -> neutral {C:0.9, THEM(THEM):0.1}   via THEM(THEM) (3.67e-04)
- neutral {C:0.7, THEM(ME):0.3}
    - 2.53e-01 -> neutral {C:0.8, THEM(ME):0.2}   via C (9.87e-02), D (7.68e-02), X (7.29e-02), and(X,X) (1.76e-03)
    - 1.57e-01 -> neutral {C:0.6, THEM(ME):0.4}   via D (7.68e-02), X (7.29e-02), THEM(ME) (2.58e-03), and(X,X) (1.76e-03)
    - 2.57e-03 -> neutral {C:0.6, THEM(ME):0.3, THEM(THEM):0.1}   via THEM(THEM) (2.57e-03)
    - 1.10e-03 -> neutral {C:0.7, THEM(ME):0.2, THEM(THEM):0.1}   via THEM(THEM) (1.10e-03)
    - 6.37e-04 -> neutral {C:0.6, THEM(ME):0.3, THEM(^C):0.1}   via THEM(^C) (6.37e-04)
    - 2.73e-04 -> neutral {C:0.7, THEM(ME):0.2, THEM(^C):0.1}   via THEM(^C) (2.73e-04)
- neutral {C:0.7, THEM(THEM):0.3}
    - 2.53e-01 -> neutral {C:0.8, THEM(THEM):0.2}   via C (9.87e-02), D (7.68e-02), X (7.29e-02), and(X,X) (1.76e-03)
    - 1.57e-01 -> neutral {C:0.6, THEM(THEM):0.4}   via D (7.68e-02), X (7.29e-02), THEM(THEM) (2.57e-03), and(X,X) (1.76e-03)
    - 2.58e-03 -> neutral {C:0.6, THEM(ME):0.1, THEM(THEM):0.3}   via THEM(ME) (2.58e-03)
    - 1.11e-03 -> neutral {C:0.7, THEM(ME):0.1, THEM(THEM):0.2}   via THEM(ME) (1.11e-03)
    - 6.37e-04 -> neutral {C:0.6, THEM(THEM):0.3, THEM(^C):0.1}   via THEM(^C) (6.37e-04)
    - 2.73e-04 -> neutral {C:0.7, THEM(THEM):0.2, THEM(^C):0.1}   via THEM(^C) (2.73e-04)
- neutral {C:0.6, THEM(ME):0.4}
    - 3.08e-01 -> neutral {C:0.7, THEM(ME):0.3}   via C (1.32e-01), D (8.77e-02), X (8.33e-02), and(X,X) (2.01e-03)
    - 1.79e-01 -> neutral {C:0.5, THEM(ME):0.5}   via D (8.77e-02), X (8.33e-02), THEM(ME) (2.22e-03), and(X,X) (2.01e-03)
    - 2.20e-03 -> neutral {C:0.5, THEM(ME):0.4, THEM(THEM):0.1}   via THEM(THEM) (2.20e-03)
    - 1.47e-03 -> neutral {C:0.6, THEM(ME):0.3, THEM(THEM):0.1}   via THEM(THEM) (1.47e-03)
    - 5.46e-04 -> neutral {C:0.5, THEM(ME):0.4, THEM(^C):0.1}   via THEM(^C) (5.46e-04)
    - 3.64e-04 -> neutral {C:0.6, THEM(ME):0.3, THEM(^C):0.1}   via THEM(^C) (3.64e-04)
- neutral {C:0.6, THEM(THEM):0.4}
    - 3.08e-01 -> neutral {C:0.7, THEM(THEM):0.3}   via C (1.32e-01), D (8.77e-02), X (8.33e-02), and(X,X) (2.01e-03)
    - 1.79e-01 -> neutral {C:0.5, THEM(THEM):0.5}   via D (8.77e-02), X (8.33e-02), THEM(THEM) (2.20e-03), and(X,X) (2.01e-03)
    - 2.22e-03 -> neutral {C:0.5, THEM(ME):0.1, THEM(THEM):0.4}   via THEM(ME) (2.22e-03)
    - 1.48e-03 -> neutral {C:0.6, THEM(ME):0.1, THEM(THEM):0.3}   via THEM(ME) (1.48e-03)
    - 5.46e-04 -> neutral {C:0.5, THEM(THEM):0.4, THEM(^C):0.1}   via THEM(^C) (5.46e-04)
    - 3.64e-04 -> neutral {C:0.6, THEM(THEM):0.3, THEM(^C):0.1}   via THEM(^C) (3.64e-04)
- neutral {C:0.8, THEM(^C):0.2}
    - 1.84e-01 -> neutral {C:0.9, THEM(^C):0.1}   via C (6.58e-02), D (5.85e-02), X (5.55e-02), and(X,X) (1.34e-03)
    - 1.18e-01 -> neutral {C:0.7, THEM(^C):0.3}   via D (5.85e-02), X (5.55e-02), and(X,X) (1.34e-03), or(X,X) (1.34e-03)
    - 2.95e-03 -> neutral {C:0.7, THEM(ME):0.1, THEM(^C):0.2}   via THEM(ME) (2.95e-03)
    - 2.93e-03 -> neutral {C:0.7, THEM(THEM):0.1, THEM(^C):0.2}   via THEM(THEM) (2.93e-03)
    - 7.38e-04 -> neutral {C:0.8, THEM(ME):0.1, THEM(^C):0.1}   via THEM(ME) (7.38e-04)
    - 7.33e-04 -> neutral {C:0.8, THEM(THEM):0.1, THEM(^C):0.1}   via THEM(THEM) (7.33e-04)
- neutral {C:0.9, or(THEM(ME),C):0.1}
    - 9.91e-02 -> mono {C:1}   via C (3.29e-02), D (3.29e-02), X (3.12e-02), and(X,X) (7.54e-04)
    - 6.64e-02 -> neutral {C:0.8, or(THEM(ME),C):0.2}   via D (3.29e-02), X (3.12e-02), and(X,X) (7.54e-04), or(X,X) (7.54e-04)
    - 3.32e-03 -> neutral {C:0.8, THEM(ME):0.1, or(THEM(ME),C):0.1}   via THEM(ME) (3.32e-03)
    - 3.30e-03 -> neutral {C:0.8, THEM(THEM):0.1, or(THEM(ME),C):0.1}   via THEM(THEM) (3.30e-03)
    - 8.19e-04 -> neutral {C:0.8, THEM(^C):0.1, or(THEM(ME),C):0.1}   via THEM(^C) (8.19e-04)
    - 3.69e-04 -> neutral {C:0.9, THEM(ME):0.1}   via THEM(ME) (3.69e-04)
