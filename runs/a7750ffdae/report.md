### arm=weak, n=5, game=zerosum, N=100, x_on=True, role=True, mode=square

programs 902, classes 53, states 964558, terminal classes 4, indeterminate 0, divergence rate 0.0010
mean payoff 0.0000, efficient 0.0000, deadweight loss 0.0000, mean bits in support 3.05
absorption: class 2: 0.000, class 4: 0.000, class 0: 0.000, class 8: 1.000

| pi | state |
|---|---|
| 0.0038 | neutral {C:0.22, D:0.47, X:0.31} |
| 0.0037 | neutral {C:0.21, D:0.47, X:0.32} |
| 0.0037 | neutral {C:0.21, D:0.48, X:0.31} |
| 0.0037 | neutral {C:0.22, D:0.46, X:0.32} |
| 0.0037 | neutral {C:0.22, D:0.48, X:0.3} |
| 0.0037 | neutral {C:0.21, D:0.46, X:0.33} |
| 0.0035 | neutral {C:0.2, D:0.48, X:0.32} |
| 0.0035 | neutral {C:0.2, D:0.47, X:0.33} |
| 0.0035 | neutral {C:0.21, D:0.49, X:0.3} |
| 0.0034 | neutral {C:0.2, D:0.49, X:0.31} |
| 0.0034 | neutral {C:0.21, D:0.45, X:0.34} |
| 0.0034 | neutral {C:0.23, D:0.47, X:0.3} |

Transitions out of the support (share of mutation events, mutants responsible):

- neutral {C:0.22, D:0.47, X:0.31}
    - 1.39e-01 -> neutral {C:0.22, D:0.46, X:0.32}   via X (1.09e-01), ROLE (2.80e-02), and(X,ROLE) (9.21e-04), or(X,ROLE) (9.21e-04)
    - 1.38e-01 -> neutral {C:0.23, D:0.46, X:0.31}   via C (1.17e-01), ROLE (1.99e-02), and(X,ROLE) (6.54e-04), or(X,ROLE) (6.54e-04)
    - 1.07e-01 -> neutral {C:0.22, D:0.48, X:0.3}   via D (7.72e-02), ROLE (2.80e-02), and(X,ROLE) (9.21e-04), or(X,ROLE) (9.21e-04)
    - 9.12e-02 -> neutral {C:0.23, D:0.47, X:0.3}   via C (7.72e-02), ROLE (1.31e-02), and(X,ROLE) (4.31e-04), or(X,ROLE) (4.31e-04)
    - 7.61e-02 -> neutral {C:0.21, D:0.48, X:0.31}   via D (5.48e-02), ROLE (1.99e-02), and(X,ROLE) (6.54e-04), or(X,ROLE) (6.54e-04)
    - 6.50e-02 -> neutral {C:0.21, D:0.47, X:0.32}   via X (5.09e-02), ROLE (1.31e-02), and(X,ROLE) (4.31e-04), or(X,ROLE) (4.31e-04)
- neutral {C:0.21, D:0.47, X:0.32}
    - 1.40e-01 -> neutral {C:0.21, D:0.46, X:0.33}   via X (1.09e-01), ROLE (2.89e-02), and(X,ROLE) (9.51e-04), or(X,ROLE) (9.51e-04)
    - 1.37e-01 -> neutral {C:0.22, D:0.46, X:0.32}   via C (1.17e-01), ROLE (1.90e-02), and(X,ROLE) (6.24e-04), or(X,ROLE) (6.24e-04)
    - 1.11e-01 -> neutral {C:0.21, D:0.48, X:0.31}   via D (7.97e-02), ROLE (2.89e-02), and(X,ROLE) (9.51e-04), or(X,ROLE) (9.51e-04)
    - 9.35e-02 -> neutral {C:0.22, D:0.47, X:0.31}   via C (7.97e-02), ROLE (1.29e-02), and(X,ROLE) (4.25e-04), or(X,ROLE) (4.25e-04)
    - 7.26e-02 -> neutral {C:0.2, D:0.48, X:0.32}   via D (5.23e-02), ROLE (1.90e-02), and(X,ROLE) (6.24e-04), or(X,ROLE) (6.24e-04)
    - 6.24e-02 -> neutral {C:0.2, D:0.47, X:0.33}   via X (4.86e-02), ROLE (1.29e-02), and(X,ROLE) (4.25e-04), or(X,ROLE) (4.25e-04)
- neutral {C:0.21, D:0.48, X:0.31}
    - 1.42e-01 -> neutral {C:0.21, D:0.47, X:0.32}   via X (1.11e-01), ROLE (2.86e-02), and(X,ROLE) (9.41e-04), or(X,ROLE) (9.41e-04)
    - 1.40e-01 -> neutral {C:0.22, D:0.47, X:0.31}   via C (1.20e-01), ROLE (1.94e-02), and(X,ROLE) (6.37e-04), or(X,ROLE) (6.37e-04)
    - 1.08e-01 -> neutral {C:0.21, D:0.49, X:0.3}   via D (7.72e-02), ROLE (2.86e-02), and(X,ROLE) (9.41e-04), or(X,ROLE) (9.41e-04)
    - 9.06e-02 -> neutral {C:0.22, D:0.48, X:0.3}   via C (7.72e-02), ROLE (1.25e-02), and(X,ROLE) (4.12e-04), or(X,ROLE) (4.12e-04)
    - 7.31e-02 -> neutral {C:0.2, D:0.49, X:0.31}   via D (5.23e-02), ROLE (1.94e-02), and(X,ROLE) (6.37e-04), or(X,ROLE) (6.37e-04)
    - 6.20e-02 -> neutral {C:0.2, D:0.48, X:0.32}   via X (4.86e-02), ROLE (1.25e-02), and(X,ROLE) (4.12e-04), or(X,ROLE) (4.12e-04)
- neutral {C:0.22, D:0.46, X:0.32}
    - 1.37e-01 -> neutral {C:0.22, D:0.45, X:0.33}   via X (1.06e-01), ROLE (2.83e-02), and(X,ROLE) (9.31e-04), or(X,ROLE) (9.31e-04)
    - 1.35e-01 -> neutral {C:0.23, D:0.45, X:0.32}   via C (1.15e-01), ROLE (1.95e-02), and(X,ROLE) (6.40e-04), or(X,ROLE) (6.40e-04)
    - 1.10e-01 -> neutral {C:0.22, D:0.47, X:0.31}   via D (7.97e-02), ROLE (2.83e-02), and(X,ROLE) (9.31e-04), or(X,ROLE) (9.31e-04)
    - 9.42e-02 -> neutral {C:0.23, D:0.46, X:0.31}   via C (7.97e-02), ROLE (1.35e-02), and(X,ROLE) (4.45e-04), or(X,ROLE) (4.45e-04)
    - 7.56e-02 -> neutral {C:0.21, D:0.47, X:0.32}   via D (5.48e-02), ROLE (1.95e-02), and(X,ROLE) (6.40e-04), or(X,ROLE) (6.40e-04)
    - 6.54e-02 -> neutral {C:0.21, D:0.46, X:0.33}   via X (5.09e-02), ROLE (1.35e-02), and(X,ROLE) (4.45e-04), or(X,ROLE) (4.45e-04)
- neutral {C:0.22, D:0.48, X:0.3}
    - 1.41e-01 -> neutral {C:0.23, D:0.47, X:0.3}   via C (1.20e-01), ROLE (2.03e-02), and(X,ROLE) (6.68e-04), or(X,ROLE) (6.68e-04)
    - 1.41e-01 -> neutral {C:0.22, D:0.47, X:0.31}   via X (1.11e-01), ROLE (2.77e-02), and(X,ROLE) (9.10e-04), or(X,ROLE) (9.10e-04)
    - 1.04e-01 -> neutral {C:0.22, D:0.49, X:0.29}   via D (7.47e-02), ROLE (2.77e-02), and(X,ROLE) (9.10e-04), or(X,ROLE) (9.10e-04)
    - 8.83e-02 -> neutral {C:0.23, D:0.48, X:0.29}   via C (7.47e-02), ROLE (1.27e-02), and(X,ROLE) (4.17e-04), or(X,ROLE) (4.17e-04)
    - 7.65e-02 -> neutral {C:0.21, D:0.49, X:0.3}   via D (5.48e-02), ROLE (2.03e-02), and(X,ROLE) (6.68e-04), or(X,ROLE) (6.68e-04)
    - 6.45e-02 -> neutral {C:0.21, D:0.48, X:0.31}   via X (5.09e-02), ROLE (1.27e-02), and(X,ROLE) (4.17e-04), or(X,ROLE) (4.17e-04)
- neutral {C:0.21, D:0.46, X:0.33}
    - 1.38e-01 -> neutral {C:0.21, D:0.45, X:0.34}   via X (1.06e-01), ROLE (2.92e-02), and(X,ROLE) (9.60e-04), or(X,ROLE) (9.60e-04)
    - 1.34e-01 -> neutral {C:0.22, D:0.45, X:0.33}   via C (1.15e-01), ROLE (1.86e-02), and(X,ROLE) (6.11e-04), or(X,ROLE) (6.11e-04)
    - 1.13e-01 -> neutral {C:0.21, D:0.47, X:0.32}   via D (8.22e-02), ROLE (2.92e-02), and(X,ROLE) (9.60e-04), or(X,ROLE) (9.60e-04)
    - 9.64e-02 -> neutral {C:0.22, D:0.46, X:0.32}   via C (8.22e-02), ROLE (1.33e-02), and(X,ROLE) (4.38e-04), or(X,ROLE) (4.38e-04)
    - 7.22e-02 -> neutral {C:0.2, D:0.47, X:0.33}   via D (5.23e-02), ROLE (1.86e-02), and(X,ROLE) (6.11e-04), or(X,ROLE) (6.11e-04)
    - 6.29e-02 -> neutral {C:0.2, D:0.46, X:0.34}   via X (4.86e-02), ROLE (1.33e-02), and(X,ROLE) (4.38e-04), or(X,ROLE) (4.38e-04)
- neutral {C:0.2, D:0.48, X:0.32}
    - 1.43e-01 -> neutral {C:0.2, D:0.47, X:0.33}   via X (1.11e-01), ROLE (2.95e-02), and(X,ROLE) (9.71e-04), or(X,ROLE) (9.71e-04)
    - 1.39e-01 -> neutral {C:0.21, D:0.47, X:0.32}   via C (1.20e-01), ROLE (1.85e-02), and(X,ROLE) (6.07e-04), or(X,ROLE) (6.07e-04)
    - 1.11e-01 -> neutral {C:0.2, D:0.49, X:0.31}   via D (7.97e-02), ROLE (2.95e-02), and(X,ROLE) (9.71e-04), or(X,ROLE) (9.71e-04)
    - 9.29e-02 -> neutral {C:0.21, D:0.48, X:0.31}   via C (7.97e-02), ROLE (1.23e-02), and(X,ROLE) (4.05e-04), or(X,ROLE) (4.05e-04)
    - 6.96e-02 -> neutral {C:0.19, D:0.49, X:0.32}   via D (4.98e-02), ROLE (1.85e-02), and(X,ROLE) (6.07e-04), or(X,ROLE) (6.07e-04)
    - 5.95e-02 -> neutral {C:0.19, D:0.48, X:0.33}   via X (4.63e-02), ROLE (1.23e-02), and(X,ROLE) (4.05e-04), or(X,ROLE) (4.05e-04)
- neutral {C:0.2, D:0.47, X:0.33}
    - 1.41e-01 -> neutral {C:0.2, D:0.46, X:0.34}   via X (1.09e-01), ROLE (2.98e-02), and(X,ROLE) (9.81e-04), or(X,ROLE) (9.81e-04)
    - 1.36e-01 -> neutral {C:0.21, D:0.46, X:0.33}   via C (1.17e-01), ROLE (1.81e-02), and(X,ROLE) (5.94e-04), or(X,ROLE) (5.94e-04)
    - 1.14e-01 -> neutral {C:0.2, D:0.48, X:0.32}   via D (8.22e-02), ROLE (2.98e-02), and(X,ROLE) (9.81e-04), or(X,ROLE) (9.81e-04)
    - 9.58e-02 -> neutral {C:0.21, D:0.47, X:0.32}   via C (8.22e-02), ROLE (1.27e-02), and(X,ROLE) (4.17e-04), or(X,ROLE) (4.17e-04)
    - 6.92e-02 -> neutral {C:0.19, D:0.48, X:0.33}   via D (4.98e-02), ROLE (1.81e-02), and(X,ROLE) (5.94e-04), or(X,ROLE) (5.94e-04)
    - 5.99e-02 -> neutral {C:0.19, D:0.47, X:0.34}   via X (4.63e-02), ROLE (1.27e-02), and(X,ROLE) (4.17e-04), or(X,ROLE) (4.17e-04)
- neutral {C:0.21, D:0.49, X:0.3}
    - 1.44e-01 -> neutral {C:0.21, D:0.48, X:0.31}   via X (1.13e-01), ROLE (2.83e-02), and(X,ROLE) (9.29e-04), or(X,ROLE) (9.29e-04)
    - 1.43e-01 -> neutral {C:0.22, D:0.48, X:0.3}   via C (1.22e-01), ROLE (1.98e-02), and(X,ROLE) (6.51e-04), or(X,ROLE) (6.51e-04)
    - 1.05e-01 -> neutral {C:0.21, D:0.5, X:0.29}   via D (7.47e-02), ROLE (2.83e-02), and(X,ROLE) (9.29e-04), or(X,ROLE) (9.29e-04)
    - 8.77e-02 -> neutral {C:0.22, D:0.49, X:0.29}   via C (7.47e-02), ROLE (1.21e-02), and(X,ROLE) (3.98e-04), or(X,ROLE) (3.98e-04)
    - 7.35e-02 -> neutral {C:0.2, D:0.5, X:0.3}   via D (5.23e-02), ROLE (1.98e-02), and(X,ROLE) (6.51e-04), or(X,ROLE) (6.51e-04)
    - 6.16e-02 -> neutral {C:0.2, D:0.49, X:0.31}   via X (4.86e-02), ROLE (1.21e-02), and(X,ROLE) (3.98e-04), or(X,ROLE) (3.98e-04)
- neutral {C:0.2, D:0.49, X:0.31}
    - 1.45e-01 -> neutral {C:0.2, D:0.48, X:0.32}   via X (1.13e-01), ROLE (2.92e-02), and(X,ROLE) (9.60e-04), or(X,ROLE) (9.60e-04)
    - 1.42e-01 -> neutral {C:0.21, D:0.48, X:0.31}   via C (1.22e-01), ROLE (1.89e-02), and(X,ROLE) (6.20e-04), or(X,ROLE) (6.20e-04)
    - 1.08e-01 -> neutral {C:0.2, D:0.5, X:0.3}   via D (7.72e-02), ROLE (2.92e-02), and(X,ROLE) (9.60e-04), or(X,ROLE) (9.60e-04)
    - 9.00e-02 -> neutral {C:0.21, D:0.49, X:0.3}   via C (7.72e-02), ROLE (1.19e-02), and(X,ROLE) (3.92e-04), or(X,ROLE) (3.92e-04)
    - 7.00e-02 -> neutral {C:0.19, D:0.5, X:0.31}   via D (4.98e-02), ROLE (1.89e-02), and(X,ROLE) (6.20e-04), or(X,ROLE) (6.20e-04)
    - 5.91e-02 -> neutral {C:0.19, D:0.49, X:0.32}   via X (4.63e-02), ROLE (1.19e-02), and(X,ROLE) (3.92e-04), or(X,ROLE) (3.92e-04)
- neutral {C:0.21, D:0.45, X:0.34}
    - 1.36e-01 -> neutral {C:0.21, D:0.44, X:0.35}   via X (1.04e-01), ROLE (2.94e-02), and(X,ROLE) (9.67e-04), or(X,ROLE) (9.67e-04)
    - 1.32e-01 -> neutral {C:0.22, D:0.44, X:0.34}   via C (1.12e-01), ROLE (1.82e-02), and(X,ROLE) (5.97e-04), or(X,ROLE) (5.97e-04)
    - 1.16e-01 -> neutral {C:0.21, D:0.46, X:0.33}   via D (8.46e-02), ROLE (2.94e-02), and(X,ROLE) (9.67e-04), or(X,ROLE) (9.67e-04)
    - 9.94e-02 -> neutral {C:0.22, D:0.45, X:0.33}   via C (8.46e-02), ROLE (1.37e-02), and(X,ROLE) (4.51e-04), or(X,ROLE) (4.51e-04)
    - 7.18e-02 -> neutral {C:0.2, D:0.46, X:0.34}   via D (5.23e-02), ROLE (1.82e-02), and(X,ROLE) (5.97e-04), or(X,ROLE) (5.97e-04)
    - 6.33e-02 -> neutral {C:0.2, D:0.45, X:0.35}   via X (4.86e-02), ROLE (1.37e-02), and(X,ROLE) (4.51e-04), or(X,ROLE) (4.51e-04)
- neutral {C:0.23, D:0.47, X:0.3}
    - 1.39e-01 -> neutral {C:0.24, D:0.46, X:0.3}   via C (1.17e-01), ROLE (2.08e-02), and(X,ROLE) (6.83e-04), or(X,ROLE) (6.83e-04)
    - 1.38e-01 -> neutral {C:0.23, D:0.46, X:0.31}   via X (1.09e-01), ROLE (2.71e-02), and(X,ROLE) (8.91e-04), or(X,ROLE) (8.91e-04)
    - 1.04e-01 -> neutral {C:0.23, D:0.48, X:0.29}   via D (7.47e-02), ROLE (2.71e-02), and(X,ROLE) (8.91e-04), or(X,ROLE) (8.91e-04)
    - 8.89e-02 -> neutral {C:0.24, D:0.47, X:0.29}   via C (7.47e-02), ROLE (1.33e-02), and(X,ROLE) (4.36e-04), or(X,ROLE) (4.36e-04)
    - 7.95e-02 -> neutral {C:0.22, D:0.48, X:0.3}   via D (5.73e-02), ROLE (2.08e-02), and(X,ROLE) (6.83e-04), or(X,ROLE) (6.83e-04)
    - 6.74e-02 -> neutral {C:0.22, D:0.47, X:0.31}   via X (5.32e-02), ROLE (1.33e-02), and(X,ROLE) (4.36e-04), or(X,ROLE) (4.36e-04)
