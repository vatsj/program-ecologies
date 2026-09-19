### arm=weak, n=5, game=zerosum, N=10, x_on=True, role=True, mode=square

programs 902, classes 53, states 103332, terminal classes 1, indeterminate 0, divergence rate 0.0010
mean payoff 0.0000, efficient 0.0000, deadweight loss 0.0000, mean bits in support 3.21

| pi | state |
|---|---|
| 0.0424 | neutral {C:0.2, D:0.5, X:0.3} |
| 0.0409 | neutral {C:0.1, D:0.6, X:0.3} |
| 0.0400 | neutral {C:0.1, D:0.5, X:0.4} |
| 0.0370 | neutral {C:0.2, D:0.6, X:0.2} |
| 0.0344 | neutral {C:0.2, D:0.4, X:0.4} |
| 0.0299 | neutral {C:0.1, D:0.4, X:0.5} |
| 0.0293 | neutral {C:0.3, D:0.5, X:0.2} |
| 0.0284 | neutral {C:0.1, D:0.7, X:0.2} |
| 0.0269 | neutral {C:0.3, D:0.4, X:0.3} |
| 0.0223 | neutral {D:0.6, X:0.4} |
| 0.0222 | neutral {C:0.2, D:0.7, X:0.1} |
| 0.0206 | neutral {D:0.7, X:0.3} |

Transitions out of the support (share of mutation events, mutants responsible):

- neutral {C:0.2, D:0.5, X:0.3}
    - 1.50e-01 -> neutral {C:0.2, D:0.4, X:0.4}   via X (1.16e-01), ROLE (3.17e-02), and(X,ROLE) (1.04e-03), or(X,ROLE) (1.04e-03)
    - 1.47e-01 -> neutral {C:0.3, D:0.4, X:0.3}   via C (1.24e-01), ROLE (2.12e-02), and(X,ROLE) (6.95e-04), or(X,ROLE) (6.95e-04)
    - 1.09e-01 -> neutral {C:0.2, D:0.6, X:0.2}   via D (7.47e-02), ROLE (3.17e-02), and(X,ROLE) (1.04e-03), or(X,ROLE) (1.04e-03)
    - 8.83e-02 -> neutral {C:0.3, D:0.5, X:0.2}   via C (7.47e-02), ROLE (1.27e-02), and(X,ROLE) (4.17e-04), or(X,ROLE) (4.17e-04)
    - 7.25e-02 -> neutral {C:0.1, D:0.6, X:0.3}   via D (4.98e-02), ROLE (2.12e-02), and(X,ROLE) (6.95e-04), or(X,ROLE) (6.95e-04)
    - 5.99e-02 -> neutral {C:0.1, D:0.5, X:0.4}   via X (4.63e-02), ROLE (1.27e-02), and(X,ROLE) (4.17e-04), or(X,ROLE) (4.17e-04)
- neutral {C:0.1, D:0.6, X:0.3}
    - 1.80e-01 -> neutral {C:0.1, D:0.5, X:0.4}   via X (1.39e-01), ROLE (3.81e-02), and(X,ROLE) (1.25e-03), or(X,ROLE) (1.25e-03)
    - 1.63e-01 -> neutral {C:0.2, D:0.5, X:0.3}   via C (1.49e-01), ROLE (1.27e-02), and(X,ROLE) (4.17e-04), or(X,ROLE) (4.17e-04)
    - 1.15e-01 -> neutral {C:0.1, D:0.7, X:0.2}   via D (7.47e-02), ROLE (3.81e-02), and(X,ROLE) (1.25e-03), or(X,ROLE) (1.25e-03)
    - 8.15e-02 -> neutral {C:0.2, D:0.6, X:0.2}   via C (7.47e-02), ROLE (6.35e-03), and(X,ROLE) (2.09e-04), or(X,ROLE) (2.09e-04)
    - 3.85e-02 -> neutral {D:0.7, X:0.3}   via D (2.49e-02), ROLE (1.27e-02), and(X,ROLE) (4.17e-04), or(X,ROLE) (4.17e-04)
    - 2.99e-02 -> neutral {D:0.6, X:0.4}   via X (2.31e-02), ROLE (6.35e-03), and(X,ROLE) (2.09e-04), or(X,ROLE) (2.09e-04)
- neutral {C:0.1, D:0.5, X:0.4}
    - 1.61e-01 -> neutral {C:0.1, D:0.4, X:0.5}   via X (1.16e-01), ROLE (4.23e-02), and(X,ROLE) (1.39e-03), or(X,ROLE) (1.39e-03)
    - 1.45e-01 -> neutral {C:0.1, D:0.6, X:0.3}   via D (9.96e-02), ROLE (4.23e-02), and(X,ROLE) (1.39e-03), or(X,ROLE) (1.39e-03)
    - 1.36e-01 -> neutral {C:0.2, D:0.4, X:0.4}   via C (1.24e-01), ROLE (1.06e-02), and(X,ROLE) (3.48e-04), or(X,ROLE) (3.48e-04)
    - 1.09e-01 -> neutral {C:0.2, D:0.5, X:0.3}   via C (9.96e-02), ROLE (8.46e-03), and(X,ROLE) (2.78e-04), or(X,ROLE) (2.78e-04)
    - 3.62e-02 -> neutral {D:0.6, X:0.4}   via D (2.49e-02), ROLE (1.06e-02), and(X,ROLE) (3.48e-04), or(X,ROLE) (3.48e-04)
    - 3.22e-02 -> neutral {D:0.5, X:0.5}   via X (2.31e-02), ROLE (8.46e-03), and(X,ROLE) (2.78e-04), or(X,ROLE) (2.78e-04)
- neutral {C:0.2, D:0.6, X:0.2}
    - 1.77e-01 -> neutral {C:0.3, D:0.5, X:0.2}   via C (1.49e-01), ROLE (2.54e-02), and(X,ROLE) (8.35e-04), or(X,ROLE) (8.35e-04)
    - 1.66e-01 -> neutral {C:0.2, D:0.5, X:0.3}   via X (1.39e-01), ROLE (2.54e-02), and(X,ROLE) (8.35e-04), or(X,ROLE) (8.35e-04)
    - 7.70e-02 -> neutral {C:0.2, D:0.7, X:0.1}   via D (4.98e-02), ROLE (2.54e-02), and(X,ROLE) (8.35e-04), or(X,ROLE) (8.35e-04)
    - 7.70e-02 -> neutral {C:0.1, D:0.7, X:0.2}   via D (4.98e-02), ROLE (2.54e-02), and(X,ROLE) (8.35e-04), or(X,ROLE) (8.35e-04)
    - 5.89e-02 -> neutral {C:0.3, D:0.6, X:0.1}   via C (4.98e-02), ROLE (8.46e-03), and(X,ROLE) (2.78e-04), or(X,ROLE) (2.78e-04)
    - 5.53e-02 -> neutral {C:0.1, D:0.6, X:0.3}   via X (4.63e-02), ROLE (8.46e-03), and(X,ROLE) (2.78e-04), or(X,ROLE) (2.78e-04)
- neutral {C:0.2, D:0.4, X:0.4}
    - 1.36e-01 -> neutral {C:0.2, D:0.5, X:0.3}   via D (9.96e-02), ROLE (3.39e-02), and(X,ROLE) (1.11e-03), or(X,ROLE) (1.11e-03)
    - 1.29e-01 -> neutral {C:0.2, D:0.3, X:0.5}   via X (9.26e-02), ROLE (3.39e-02), and(X,ROLE) (1.11e-03), or(X,ROLE) (1.11e-03)
    - 1.18e-01 -> neutral {C:0.3, D:0.4, X:0.3}   via C (9.96e-02), ROLE (1.69e-02), and(X,ROLE) (5.56e-04), or(X,ROLE) (5.56e-04)
    - 1.18e-01 -> neutral {C:0.3, D:0.3, X:0.4}   via C (9.96e-02), ROLE (1.69e-02), and(X,ROLE) (5.56e-04), or(X,ROLE) (5.56e-04)
    - 6.79e-02 -> neutral {C:0.1, D:0.5, X:0.4}   via D (4.98e-02), ROLE (1.69e-02), and(X,ROLE) (5.56e-04), or(X,ROLE) (5.56e-04)
    - 6.44e-02 -> neutral {C:0.1, D:0.4, X:0.5}   via X (4.63e-02), ROLE (1.69e-02), and(X,ROLE) (5.56e-04), or(X,ROLE) (5.56e-04)
- neutral {C:0.1, D:0.4, X:0.5}
    - 1.70e-01 -> neutral {C:0.1, D:0.5, X:0.4}   via D (1.24e-01), ROLE (4.23e-02), and(X,ROLE) (1.39e-03), or(X,ROLE) (1.39e-03)
    - 1.38e-01 -> neutral {C:0.1, D:0.3, X:0.6}   via X (9.26e-02), ROLE (4.23e-02), and(X,ROLE) (1.39e-03), or(X,ROLE) (1.39e-03)
    - 1.36e-01 -> neutral {C:0.2, D:0.4, X:0.4}   via C (1.24e-01), ROLE (1.06e-02), and(X,ROLE) (3.48e-04), or(X,ROLE) (3.48e-04)
    - 1.09e-01 -> neutral {C:0.2, D:0.3, X:0.5}   via C (9.96e-02), ROLE (8.46e-03), and(X,ROLE) (2.78e-04), or(X,ROLE) (2.78e-04)
    - 3.45e-02 -> neutral {D:0.4, X:0.6}   via X (2.31e-02), ROLE (1.06e-02), and(X,ROLE) (3.48e-04), or(X,ROLE) (3.48e-04)
    - 3.40e-02 -> neutral {D:0.5, X:0.5}   via D (2.49e-02), ROLE (8.46e-03), and(X,ROLE) (2.78e-04), or(X,ROLE) (2.78e-04)
- neutral {C:0.3, D:0.5, X:0.2}
    - 1.58e-01 -> neutral {C:0.4, D:0.4, X:0.2}   via C (1.24e-01), ROLE (3.17e-02), and(X,ROLE) (1.04e-03), or(X,ROLE) (1.04e-03)
    - 1.38e-01 -> neutral {C:0.3, D:0.4, X:0.3}   via X (1.16e-01), ROLE (2.12e-02), and(X,ROLE) (6.95e-04), or(X,ROLE) (6.95e-04)
    - 1.09e-01 -> neutral {C:0.2, D:0.6, X:0.2}   via D (7.47e-02), ROLE (3.17e-02), and(X,ROLE) (1.04e-03), or(X,ROLE) (1.04e-03)
    - 8.30e-02 -> neutral {C:0.2, D:0.5, X:0.3}   via X (6.94e-02), ROLE (1.27e-02), and(X,ROLE) (4.17e-04), or(X,ROLE) (4.17e-04)
    - 7.25e-02 -> neutral {C:0.3, D:0.6, X:0.1}   via D (4.98e-02), ROLE (2.12e-02), and(X,ROLE) (6.95e-04), or(X,ROLE) (6.95e-04)
    - 6.34e-02 -> neutral {C:0.4, D:0.5, X:0.1}   via C (4.98e-02), ROLE (1.27e-02), and(X,ROLE) (4.17e-04), or(X,ROLE) (4.17e-04)
- neutral {C:0.1, D:0.7, X:0.2}
    - 1.94e-01 -> neutral {C:0.1, D:0.6, X:0.3}   via X (1.62e-01), ROLE (2.96e-02), and(X,ROLE) (9.74e-04), or(X,ROLE) (9.74e-04)
    - 1.90e-01 -> neutral {C:0.2, D:0.6, X:0.2}   via C (1.74e-01), ROLE (1.48e-02), and(X,ROLE) (4.87e-04), or(X,ROLE) (4.87e-04)
    - 8.15e-02 -> neutral {C:0.1, D:0.8, X:0.1}   via D (4.98e-02), ROLE (2.96e-02), and(X,ROLE) (9.74e-04), or(X,ROLE) (9.74e-04)
    - 5.43e-02 -> neutral {C:0.2, D:0.7, X:0.1}   via C (4.98e-02), ROLE (4.23e-03), and(X,ROLE) (1.39e-04), or(X,ROLE) (1.39e-04)
    - 4.08e-02 -> neutral {D:0.8, X:0.2}   via D (2.49e-02), ROLE (1.48e-02), and(X,ROLE) (4.87e-04), or(X,ROLE) (4.87e-04)
    - 2.77e-02 -> neutral {D:0.7, X:0.3}   via X (2.31e-02), ROLE (4.23e-03), and(X,ROLE) (1.39e-04), or(X,ROLE) (1.39e-04)
- neutral {C:0.3, D:0.4, X:0.3}
    - 1.16e-01 -> neutral {C:0.2, D:0.5, X:0.3}   via D (7.47e-02), ROLE (3.83e-02), and(X,ROLE) (1.26e-03), or(X,ROLE) (1.26e-03)
    - 1.02e-01 -> neutral {C:0.3, D:0.5, X:0.2}   via D (7.47e-02), ROLE (2.54e-02), and(X,ROLE) (8.35e-04), or(X,ROLE) (8.35e-04)
    - 9.96e-02 -> neutral {C:0.4, D:0.3, X:0.3}   via C (9.96e-02), or(ROLE,THEM(ME)) (4.86e-06), or(ROLE,THEM(THEM)) (4.86e-06), or(THEM(ME),ROLE) (4.86e-06)
    - 9.51e-02 -> neutral {C:0.4, D:0.4, X:0.2}   via C (7.47e-02), ROLE (1.90e-02), and(X,ROLE) (6.26e-04), or(X,ROLE) (6.26e-04)
    - 9.26e-02 -> neutral {C:0.3, D:0.3, X:0.4}   via X (9.26e-02), or(ROLE,THEM(ME)) (4.86e-06), or(ROLE,THEM(THEM)) (4.86e-06), or(THEM(ME),ROLE) (4.86e-06)
    - 8.98e-02 -> neutral {C:0.2, D:0.4, X:0.4}   via X (6.94e-02), ROLE (1.90e-02), and(X,ROLE) (6.26e-04), or(X,ROLE) (6.26e-04)
- neutral {D:0.6, X:0.4}
    - 1.93e-01 -> neutral {D:0.5, X:0.5}   via X (1.39e-01), ROLE (5.08e-02), and(X,ROLE) (1.67e-03), or(X,ROLE) (1.67e-03)
    - 1.54e-01 -> neutral {D:0.7, X:0.3}   via D (9.96e-02), ROLE (5.08e-02), and(X,ROLE) (1.67e-03), or(X,ROLE) (1.67e-03)
    - 1.49e-01 -> neutral {C:0.1, D:0.5, X:0.4}   via C (1.49e-01)
    - 9.96e-02 -> neutral {C:0.1, D:0.6, X:0.3}   via C (9.96e-02)
    - 2.28e-02 -> neutral {X:0.4, not(ROLE):0.6}   via not(ROLE) (2.28e-02)
    - 1.33e-02 -> neutral {X:0.3, not(ROLE):0.7}   via not(ROLE) (1.33e-02)
- neutral {C:0.2, D:0.7, X:0.1}
    - 2.06e-01 -> neutral {C:0.3, D:0.6, X:0.1}   via C (1.74e-01), ROLE (2.96e-02), and(X,ROLE) (9.74e-04), or(X,ROLE) (9.74e-04)
    - 1.78e-01 -> neutral {C:0.2, D:0.6, X:0.2}   via X (1.62e-01), ROLE (1.48e-02), and(X,ROLE) (4.87e-04), or(X,ROLE) (4.87e-04)
    - 8.15e-02 -> neutral {C:0.1, D:0.8, X:0.1}   via D (4.98e-02), ROLE (2.96e-02), and(X,ROLE) (9.74e-04), or(X,ROLE) (9.74e-04)
    - 5.08e-02 -> neutral {C:0.1, D:0.7, X:0.2}   via X (4.63e-02), ROLE (4.23e-03), and(X,ROLE) (1.39e-04), or(X,ROLE) (1.39e-04)
    - 4.08e-02 -> neutral {C:0.2, D:0.8}   via D (2.49e-02), ROLE (1.48e-02), and(X,ROLE) (4.87e-04), or(X,ROLE) (4.87e-04)
    - 2.94e-02 -> neutral {C:0.3, D:0.7}   via C (2.49e-02), ROLE (4.23e-03), and(X,ROLE) (1.39e-04), or(X,ROLE) (1.39e-04)
- neutral {D:0.7, X:0.3}
    - 2.10e-01 -> neutral {D:0.6, X:0.4}   via X (1.62e-01), ROLE (4.44e-02), and(X,ROLE) (1.46e-03), or(X,ROLE) (1.46e-03)
    - 1.74e-01 -> neutral {C:0.1, D:0.6, X:0.3}   via C (1.74e-01)
    - 1.22e-01 -> neutral {D:0.8, X:0.2}   via D (7.47e-02), ROLE (4.44e-02), and(X,ROLE) (1.46e-03), or(X,ROLE) (1.46e-03)
    - 7.47e-02 -> neutral {C:0.1, D:0.7, X:0.2}   via C (7.47e-02)
    - 2.61e-02 -> neutral {X:0.3, not(ROLE):0.7}   via not(ROLE) (2.61e-02)
    - 1.14e-02 -> neutral {X:0.2, not(ROLE):0.8}   via not(ROLE) (1.14e-02)
