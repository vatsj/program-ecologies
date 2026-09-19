### arm=weak, n=6, game=stag, N=1000, x_on=True, role=False, mode=square

programs 1852, classes 46, states 232239, terminal classes 2, indeterminate 0, divergence rate 0.0019
mean payoff 4.0001, efficient 4.0000, deadweight loss -0.0001, mean bits in support 2.61
absorption: class 0: 1.000, class 29: 0.000

| pi | state |
|---|---|
| 0.1652 | mono {C:1} |
| 0.1505 | neutral {C:0.999, THEM(^C):0.001} |
| 0.1190 | neutral {C:0.998, THEM(^C):0.002} |
| 0.0894 | neutral {C:0.997, THEM(^C):0.003} |
| 0.0653 | neutral {C:0.996, THEM(^C):0.004} |
| 0.0469 | neutral {C:0.995, THEM(^C):0.005} |
| 0.0333 | neutral {C:0.994, THEM(^C):0.006} |
| 0.0234 | neutral {C:0.993, THEM(^C):0.007} |
| 0.0164 | neutral {C:0.992, THEM(^C):0.008} |
| 0.0145 | neutral {C:0.999, or(X,THEM(THEM)):0.001} |
| 0.0145 | neutral {C:0.999, or(X,THEM(ME)):0.001} |
| 0.0133 | neutral {C:0.998, THEM(^C):0.001, or(X,THEM(THEM)):0.001} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 9.10e-04 -> neutral {C:0.999, THEM(^C):0.001}   via THEM(^C) (9.10e-04)
    - 8.80e-05 -> neutral {C:0.999, or(X,THEM(THEM)):0.001}   via or(X,THEM(THEM)) (8.80e-05)
    - 8.80e-05 -> neutral {C:0.999, or(X,THEM(ME)):0.001}   via or(X,THEM(ME)) (8.80e-05)
    - 2.66e-05 -> neutral {C:0.999, or(X,THEM(^C)):0.001}   via or(X,THEM(^C)) (2.66e-05)
- neutral {C:0.999, THEM(^C):0.001}
    - 1.58e-03 -> neutral {C:0.998, THEM(^C):0.002}   via THEM(^C) (9.09e-04), D (3.29e-04), X (3.12e-04), and(X,X) (7.54e-06)
    - 9.99e-04 -> mono {C:1}   via C (3.29e-04), D (3.29e-04), X (3.12e-04), and(X,X) (7.54e-06)
    - 8.79e-05 -> neutral {C:0.998, THEM(^C):0.001, or(X,THEM(THEM)):0.001}   via or(X,THEM(THEM)) (8.79e-05)
    - 8.79e-05 -> neutral {C:0.998, THEM(^C):0.001, or(X,THEM(ME)):0.001}   via or(X,THEM(ME)) (8.79e-05)
    - 2.65e-05 -> neutral {C:0.998, THEM(^C):0.001, or(X,THEM(^C)):0.001}   via or(X,THEM(^C)) (2.65e-05)
    - 8.80e-08 -> neutral {C:0.999, or(X,THEM(THEM)):0.001}   via or(X,THEM(THEM)) (8.80e-08)
- neutral {C:0.998, THEM(^C):0.002}
    - 2.25e-03 -> neutral {C:0.997, THEM(^C):0.003}   via THEM(^C) (9.08e-04), D (6.57e-04), X (6.24e-04), and(X,X) (1.51e-05)
    - 2.00e-03 -> neutral {C:0.999, THEM(^C):0.001}   via C (6.58e-04), D (6.57e-04), X (6.24e-04), and(X,X) (1.51e-05)
    - 8.78e-05 -> neutral {C:0.997, THEM(^C):0.002, or(X,THEM(THEM)):0.001}   via or(X,THEM(THEM)) (8.78e-05)
    - 8.78e-05 -> neutral {C:0.997, THEM(^C):0.002, or(X,THEM(ME)):0.001}   via or(X,THEM(ME)) (8.78e-05)
    - 2.65e-05 -> neutral {C:0.997, THEM(^C):0.002, or(X,THEM(^C)):0.001}   via or(X,THEM(^C)) (2.65e-05)
    - 1.76e-07 -> neutral {C:0.998, THEM(^C):0.001, or(X,THEM(THEM)):0.001}   via or(X,THEM(THEM)) (1.76e-07)
- neutral {C:0.997, THEM(^C):0.003}
    - 2.99e-03 -> neutral {C:0.998, THEM(^C):0.002}   via C (9.87e-04), D (9.85e-04), X (9.35e-04), and(X,X) (2.26e-05)
    - 2.91e-03 -> neutral {C:0.996, THEM(^C):0.004}   via D (9.85e-04), X (9.35e-04), THEM(^C) (9.07e-04), and(X,X) (2.26e-05)
    - 8.77e-05 -> neutral {C:0.996, THEM(^C):0.003, or(X,THEM(THEM)):0.001}   via or(X,THEM(THEM)) (8.77e-05)
    - 8.77e-05 -> neutral {C:0.996, THEM(^C):0.003, or(X,THEM(ME)):0.001}   via or(X,THEM(ME)) (8.77e-05)
    - 2.65e-05 -> neutral {C:0.996, THEM(^C):0.003, or(X,THEM(^C)):0.001}   via or(X,THEM(^C)) (2.65e-05)
    - 2.64e-07 -> neutral {C:0.997, THEM(^C):0.002, or(X,THEM(THEM)):0.001}   via or(X,THEM(THEM)) (2.64e-07)
- neutral {C:0.996, THEM(^C):0.004}
    - 3.99e-03 -> neutral {C:0.997, THEM(^C):0.003}   via C (1.32e-03), D (1.31e-03), X (1.25e-03), and(X,X) (3.01e-05)
    - 3.58e-03 -> neutral {C:0.995, THEM(^C):0.005}   via D (1.31e-03), X (1.25e-03), THEM(^C) (9.06e-04), and(X,X) (3.01e-05)
    - 8.76e-05 -> neutral {C:0.995, THEM(^C):0.004, or(X,THEM(THEM)):0.001}   via or(X,THEM(THEM)) (8.76e-05)
    - 8.76e-05 -> neutral {C:0.995, THEM(^C):0.004, or(X,THEM(ME)):0.001}   via or(X,THEM(ME)) (8.76e-05)
    - 2.65e-05 -> neutral {C:0.995, THEM(^C):0.004, or(X,THEM(^C)):0.001}   via or(X,THEM(^C)) (2.65e-05)
    - 3.52e-07 -> neutral {C:0.996, THEM(^C):0.003, or(X,THEM(THEM)):0.001}   via or(X,THEM(THEM)) (3.52e-07)
- neutral {C:0.995, THEM(^C):0.005}
    - 4.98e-03 -> neutral {C:0.996, THEM(^C):0.004}   via C (1.64e-03), D (1.64e-03), X (1.56e-03), and(X,X) (3.76e-05)
    - 4.24e-03 -> neutral {C:0.994, THEM(^C):0.006}   via D (1.64e-03), X (1.56e-03), THEM(^C) (9.06e-04), and(X,X) (3.76e-05)
    - 8.76e-05 -> neutral {C:0.994, THEM(^C):0.005, or(X,THEM(THEM)):0.001}   via or(X,THEM(THEM)) (8.76e-05)
    - 8.76e-05 -> neutral {C:0.994, THEM(^C):0.005, or(X,THEM(ME)):0.001}   via or(X,THEM(ME)) (8.76e-05)
    - 2.64e-05 -> neutral {C:0.994, THEM(^C):0.005, or(X,THEM(^C)):0.001}   via or(X,THEM(^C)) (2.64e-05)
    - 4.40e-07 -> neutral {C:0.995, THEM(^C):0.004, or(X,THEM(THEM)):0.001}   via or(X,THEM(THEM)) (4.40e-07)
- neutral {C:0.994, THEM(^C):0.006}
    - 5.97e-03 -> neutral {C:0.995, THEM(^C):0.005}   via C (1.97e-03), D (1.96e-03), X (1.87e-03), and(X,X) (4.50e-05)
    - 4.90e-03 -> neutral {C:0.993, THEM(^C):0.007}   via D (1.96e-03), X (1.87e-03), THEM(^C) (9.05e-04), and(X,X) (4.50e-05)
    - 8.75e-05 -> neutral {C:0.993, THEM(^C):0.006, or(X,THEM(THEM)):0.001}   via or(X,THEM(THEM)) (8.75e-05)
    - 8.75e-05 -> neutral {C:0.993, THEM(^C):0.006, or(X,THEM(ME)):0.001}   via or(X,THEM(ME)) (8.75e-05)
    - 2.64e-05 -> neutral {C:0.993, THEM(^C):0.006, or(X,THEM(^C)):0.001}   via or(X,THEM(^C)) (2.64e-05)
    - 5.28e-07 -> neutral {C:0.994, THEM(^C):0.005, or(X,THEM(THEM)):0.001}   via or(X,THEM(THEM)) (5.28e-07)
- neutral {C:0.993, THEM(^C):0.007}
    - 6.96e-03 -> neutral {C:0.994, THEM(^C):0.006}   via C (2.30e-03), D (2.29e-03), X (2.17e-03), and(X,X) (5.25e-05)
    - 5.57e-03 -> neutral {C:0.992, THEM(^C):0.008}   via D (2.29e-03), X (2.17e-03), THEM(^C) (9.04e-04), and(X,X) (5.25e-05)
    - 8.74e-05 -> neutral {C:0.992, THEM(^C):0.007, or(X,THEM(THEM)):0.001}   via or(X,THEM(THEM)) (8.74e-05)
    - 8.74e-05 -> neutral {C:0.992, THEM(^C):0.007, or(X,THEM(ME)):0.001}   via or(X,THEM(ME)) (8.74e-05)
    - 2.64e-05 -> neutral {C:0.992, THEM(^C):0.007, or(X,THEM(^C)):0.001}   via or(X,THEM(^C)) (2.64e-05)
    - 6.16e-07 -> neutral {C:0.993, THEM(^C):0.006, or(X,THEM(THEM)):0.001}   via or(X,THEM(THEM)) (6.16e-07)
- neutral {C:0.992, THEM(^C):0.008}
    - 7.95e-03 -> neutral {C:0.993, THEM(^C):0.007}   via C (2.63e-03), D (2.61e-03), X (2.48e-03), and(X,X) (5.99e-05)
    - 6.22e-03 -> neutral {C:0.991, THEM(^C):0.009}   via D (2.61e-03), X (2.48e-03), THEM(^C) (9.03e-04), and(X,X) (5.99e-05)
    - 8.73e-05 -> neutral {C:0.991, THEM(^C):0.008, or(X,THEM(THEM)):0.001}   via or(X,THEM(THEM)) (8.73e-05)
    - 8.73e-05 -> neutral {C:0.991, THEM(^C):0.008, or(X,THEM(ME)):0.001}   via or(X,THEM(ME)) (8.73e-05)
    - 2.64e-05 -> neutral {C:0.991, THEM(^C):0.008, or(X,THEM(^C)):0.001}   via or(X,THEM(^C)) (2.64e-05)
    - 7.04e-07 -> neutral {C:0.992, THEM(^C):0.007, or(X,THEM(THEM)):0.001}   via or(X,THEM(THEM)) (7.04e-07)
- neutral {C:0.999, or(X,THEM(THEM)):0.001}
    - 9.99e-04 -> mono {C:1}   via C (3.29e-04), D (3.29e-04), X (3.12e-04), and(X,X) (7.54e-06)
    - 9.09e-04 -> neutral {C:0.998, THEM(^C):0.001, or(X,THEM(THEM)):0.001}   via THEM(^C) (9.09e-04)
    - 7.58e-04 -> neutral {C:0.998, or(X,THEM(THEM)):0.002}   via D (3.29e-04), X (3.12e-04), or(X,THEM(THEM)) (8.79e-05), and(X,X) (7.54e-06)
    - 8.79e-05 -> neutral {C:0.998, or(X,THEM(ME)):0.001, or(X,THEM(THEM)):0.001}   via or(X,THEM(ME)) (8.79e-05)
    - 2.65e-05 -> neutral {C:0.998, or(X,THEM(THEM)):0.001, or(X,THEM(^C)):0.001}   via or(X,THEM(^C)) (2.65e-05)
    - 9.10e-07 -> neutral {C:0.999, THEM(^C):0.001}   via THEM(^C) (9.10e-07)
- neutral {C:0.999, or(X,THEM(ME)):0.001}
    - 9.99e-04 -> mono {C:1}   via C (3.29e-04), D (3.29e-04), X (3.12e-04), and(X,X) (7.54e-06)
    - 9.09e-04 -> neutral {C:0.998, THEM(^C):0.001, or(X,THEM(ME)):0.001}   via THEM(^C) (9.09e-04)
    - 7.58e-04 -> neutral {C:0.998, or(X,THEM(ME)):0.002}   via D (3.29e-04), X (3.12e-04), or(X,THEM(ME)) (8.79e-05), and(X,X) (7.54e-06)
    - 8.79e-05 -> neutral {C:0.998, or(X,THEM(ME)):0.001, or(X,THEM(THEM)):0.001}   via or(X,THEM(THEM)) (8.79e-05)
    - 2.65e-05 -> neutral {C:0.998, or(X,THEM(ME)):0.001, or(X,THEM(^C)):0.001}   via or(X,THEM(^C)) (2.65e-05)
    - 9.10e-07 -> neutral {C:0.999, THEM(^C):0.001}   via THEM(^C) (9.10e-07)
- neutral {C:0.998, THEM(^C):0.001, or(X,THEM(THEM)):0.001}
    - 1.58e-03 -> neutral {C:0.997, THEM(^C):0.002, or(X,THEM(THEM)):0.001}   via THEM(^C) (9.08e-04), D (3.29e-04), X (3.12e-04), and(X,X) (7.53e-06)
    - 9.98e-04 -> neutral {C:0.999, or(X,THEM(THEM)):0.001}   via C (3.29e-04), D (3.29e-04), X (3.12e-04), and(X,X) (7.53e-06)
    - 9.98e-04 -> neutral {C:0.999, THEM(^C):0.001}   via C (3.29e-04), D (3.29e-04), X (3.12e-04), and(X,X) (7.53e-06)
    - 7.57e-04 -> neutral {C:0.997, THEM(^C):0.001, or(X,THEM(THEM)):0.002}   via D (3.29e-04), X (3.12e-04), or(X,THEM(THEM)) (8.78e-05), and(X,X) (7.53e-06)
    - 8.78e-05 -> neutral {C:0.997, THEM(^C):0.001, or(X,THEM(ME)):0.001, or(X,THEM(THEM)):0.001}   via or(X,THEM(ME)) (8.78e-05)
    - 2.65e-05 -> neutral {C:0.997, THEM(^C):0.001, or(X,THEM(THEM)):0.001, or(X,THEM(^C)):0.001}   via or(X,THEM(^C)) (2.65e-05)
