### arm=strong, n=6, game=pd, N=1000, x_on=True, role=False, mode=square

programs 1726, classes 21, states 42690, terminal classes 1, indeterminate 0, divergence rate 0.0004
mean payoff -1.0000, efficient 0.0000, deadweight loss 1.0000, mean bits in support 2.66

| pi | state |
|---|---|
| 0.0470 | neutral {D:0.991, THEM(ME):0.009} |
| 0.0462 | neutral {D:0.99, THEM(ME):0.01} |
| 0.0461 | neutral {D:0.992, THEM(ME):0.008} |
| 0.0441 | neutral {D:0.989, THEM(ME):0.011} |
| 0.0434 | neutral {D:0.993, THEM(ME):0.007} |
| 0.0410 | neutral {D:0.988, THEM(ME):0.012} |
| 0.0387 | neutral {D:0.994, THEM(ME):0.006} |
| 0.0373 | neutral {D:0.987, THEM(ME):0.013} |
| 0.0332 | neutral {D:0.986, THEM(ME):0.014} |
| 0.0323 | neutral {D:0.995, THEM(ME):0.005} |
| 0.0291 | neutral {D:0.985, THEM(ME):0.015} |
| 0.0251 | neutral {D:0.984, THEM(ME):0.016} |

Transitions out of the support (share of mutation events, mutants responsible):

- neutral {D:0.991, THEM(ME):0.009}
    - 9.73e-03 -> neutral {D:0.99, THEM(ME):0.01}   via THEM(ME) (3.80e-03), C (2.96e-03), X (2.81e-03), and(X,X) (7.12e-05)
    - 8.91e-03 -> neutral {D:0.992, THEM(ME):0.008}   via D (2.98e-03), C (2.96e-03), X (2.81e-03), and(X,X) (7.12e-05)
    - 1.21e-04 -> neutral {D:0.99, THEM(ME):0.009, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.21e-04)
    - 9.24e-05 -> neutral {D:0.99, THEM(ME):0.009, and(THEM(ME),X):0.001}   via and(THEM(ME),X) (9.24e-05)
    - 9.24e-05 -> neutral {D:0.99, THEM(ME):0.009, and(X,THEM(ME)):0.001}   via and(X,THEM(ME)) (9.24e-05)
    - 1.10e-06 -> neutral {D:0.991, THEM(ME):0.008, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.10e-06)
- neutral {D:0.99, THEM(ME):0.01}
    - 1.04e-02 -> neutral {D:0.989, THEM(ME):0.011}   via THEM(ME) (3.80e-03), C (3.29e-03), X (3.11e-03), and(X,X) (7.91e-05)
    - 9.90e-03 -> neutral {D:0.991, THEM(ME):0.009}   via D (3.32e-03), C (3.29e-03), X (3.11e-03), and(X,X) (7.91e-05)
    - 1.21e-04 -> neutral {D:0.989, THEM(ME):0.01, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.21e-04)
    - 9.23e-05 -> neutral {D:0.989, THEM(ME):0.01, and(THEM(ME),X):0.001}   via and(THEM(ME),X) (9.23e-05)
    - 9.23e-05 -> neutral {D:0.989, THEM(ME):0.01, and(X,THEM(ME)):0.001}   via and(X,THEM(ME)) (9.23e-05)
    - 1.22e-06 -> neutral {D:0.99, THEM(ME):0.009, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.22e-06)
- neutral {D:0.992, THEM(ME):0.008}
    - 9.08e-03 -> neutral {D:0.991, THEM(ME):0.009}   via THEM(ME) (3.81e-03), C (2.63e-03), X (2.50e-03), and(X,X) (6.34e-05)
    - 7.93e-03 -> neutral {D:0.993, THEM(ME):0.007}   via D (2.65e-03), C (2.63e-03), X (2.50e-03), and(X,X) (6.34e-05)
    - 1.21e-04 -> neutral {D:0.991, THEM(ME):0.008, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.21e-04)
    - 9.25e-05 -> neutral {D:0.991, THEM(ME):0.008, and(THEM(ME),X):0.001}   via and(THEM(ME),X) (9.25e-05)
    - 9.25e-05 -> neutral {D:0.991, THEM(ME):0.008, and(X,THEM(ME)):0.001}   via and(X,THEM(ME)) (9.25e-05)
    - 9.75e-07 -> neutral {D:0.992, THEM(ME):0.007, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (9.75e-07)
- neutral {D:0.989, THEM(ME):0.011}
    - 1.10e-02 -> neutral {D:0.988, THEM(ME):0.012}   via THEM(ME) (3.80e-03), C (3.61e-03), X (3.42e-03), and(X,X) (8.69e-05)
    - 1.09e-02 -> neutral {D:0.99, THEM(ME):0.01}   via D (3.65e-03), C (3.61e-03), X (3.42e-03), and(X,X) (8.69e-05)
    - 1.21e-04 -> neutral {D:0.988, THEM(ME):0.011, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.21e-04)
    - 9.22e-05 -> neutral {D:0.988, THEM(ME):0.011, and(THEM(ME),X):0.001}   via and(THEM(ME),X) (9.22e-05)
    - 9.22e-05 -> neutral {D:0.988, THEM(ME):0.011, and(X,THEM(ME)):0.001}   via and(X,THEM(ME)) (9.22e-05)
    - 1.34e-06 -> neutral {D:0.989, THEM(ME):0.01, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.34e-06)
- neutral {D:0.993, THEM(ME):0.007}
    - 8.43e-03 -> neutral {D:0.992, THEM(ME):0.008}   via THEM(ME) (3.81e-03), C (2.31e-03), X (2.19e-03), and(X,X) (5.55e-05)
    - 6.94e-03 -> neutral {D:0.994, THEM(ME):0.006}   via D (2.32e-03), C (2.31e-03), X (2.19e-03), and(X,X) (5.55e-05)
    - 1.21e-04 -> neutral {D:0.992, THEM(ME):0.007, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.21e-04)
    - 9.26e-05 -> neutral {D:0.992, THEM(ME):0.007, and(THEM(ME),X):0.001}   via and(THEM(ME),X) (9.26e-05)
    - 9.26e-05 -> neutral {D:0.992, THEM(ME):0.007, and(X,THEM(ME)):0.001}   via and(X,THEM(ME)) (9.26e-05)
    - 8.53e-07 -> neutral {D:0.993, THEM(ME):0.006, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (8.53e-07)
- neutral {D:0.988, THEM(ME):0.012}
    - 1.19e-02 -> neutral {D:0.989, THEM(ME):0.011}   via D (3.98e-03), C (3.93e-03), X (3.73e-03), and(X,X) (9.47e-05)
    - 1.17e-02 -> neutral {D:0.987, THEM(ME):0.013}   via C (3.93e-03), THEM(ME) (3.79e-03), X (3.73e-03), and(X,X) (9.47e-05)
    - 1.20e-04 -> neutral {D:0.987, THEM(ME):0.012, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.20e-04)
    - 9.21e-05 -> neutral {D:0.987, THEM(ME):0.012, and(THEM(ME),X):0.001}   via and(THEM(ME),X) (9.21e-05)
    - 9.21e-05 -> neutral {D:0.987, THEM(ME):0.012, and(X,THEM(ME)):0.001}   via and(X,THEM(ME)) (9.21e-05)
    - 1.46e-06 -> neutral {D:0.988, THEM(ME):0.011, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.46e-06)
- neutral {D:0.994, THEM(ME):0.006}
    - 7.78e-03 -> neutral {D:0.993, THEM(ME):0.007}   via THEM(ME) (3.82e-03), C (1.98e-03), X (1.88e-03), and(X,X) (4.76e-05)
    - 5.96e-03 -> neutral {D:0.995, THEM(ME):0.005}   via D (1.99e-03), C (1.98e-03), X (1.88e-03), and(X,X) (4.76e-05)
    - 1.21e-04 -> neutral {D:0.993, THEM(ME):0.006, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.21e-04)
    - 9.27e-05 -> neutral {D:0.993, THEM(ME):0.006, and(THEM(ME),X):0.001}   via and(THEM(ME),X) (9.27e-05)
    - 9.27e-05 -> neutral {D:0.993, THEM(ME):0.006, and(X,THEM(ME)):0.001}   via and(X,THEM(ME)) (9.27e-05)
    - 7.31e-07 -> neutral {D:0.994, THEM(ME):0.005, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (7.31e-07)
- neutral {D:0.987, THEM(ME):0.013}
    - 1.28e-02 -> neutral {D:0.988, THEM(ME):0.012}   via D (4.31e-03), C (4.26e-03), X (4.04e-03), and(X,X) (1.02e-04)
    - 1.23e-02 -> neutral {D:0.986, THEM(ME):0.014}   via C (4.26e-03), X (4.04e-03), THEM(ME) (3.79e-03), and(X,X) (1.02e-04)
    - 1.20e-04 -> neutral {D:0.986, THEM(ME):0.013, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.20e-04)
    - 9.20e-05 -> neutral {D:0.986, THEM(ME):0.013, and(THEM(ME),X):0.001}   via and(THEM(ME),X) (9.20e-05)
    - 9.20e-05 -> neutral {D:0.986, THEM(ME):0.013, and(X,THEM(ME)):0.001}   via and(X,THEM(ME)) (9.20e-05)
    - 1.58e-06 -> neutral {D:0.987, THEM(ME):0.012, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.58e-06)
- neutral {D:0.986, THEM(ME):0.014}
    - 1.38e-02 -> neutral {D:0.987, THEM(ME):0.013}   via D (4.64e-03), C (4.58e-03), X (4.34e-03), and(X,X) (1.10e-04)
    - 1.30e-02 -> neutral {D:0.985, THEM(ME):0.015}   via C (4.58e-03), X (4.34e-03), THEM(ME) (3.78e-03), and(X,X) (1.10e-04)
    - 1.20e-04 -> neutral {D:0.985, THEM(ME):0.014, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.20e-04)
    - 9.19e-05 -> neutral {D:0.985, THEM(ME):0.014, and(THEM(ME),X):0.001}   via and(THEM(ME),X) (9.19e-05)
    - 9.19e-05 -> neutral {D:0.985, THEM(ME):0.014, and(X,THEM(ME)):0.001}   via and(X,THEM(ME)) (9.19e-05)
    - 1.71e-06 -> neutral {D:0.986, THEM(ME):0.013, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.71e-06)
- neutral {D:0.995, THEM(ME):0.005}
    - 7.13e-03 -> neutral {D:0.994, THEM(ME):0.006}   via THEM(ME) (3.82e-03), C (1.65e-03), X (1.57e-03), and(X,X) (3.97e-05)
    - 4.97e-03 -> neutral {D:0.996, THEM(ME):0.004}   via D (1.66e-03), C (1.65e-03), X (1.57e-03), and(X,X) (3.97e-05)
    - 1.21e-04 -> neutral {D:0.994, THEM(ME):0.005, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.21e-04)
    - 9.27e-05 -> neutral {D:0.994, THEM(ME):0.005, and(THEM(ME),X):0.001}   via and(THEM(ME),X) (9.27e-05)
    - 9.27e-05 -> neutral {D:0.994, THEM(ME):0.005, and(X,THEM(ME)):0.001}   via and(X,THEM(ME)) (9.27e-05)
    - 6.09e-07 -> neutral {D:0.995, THEM(ME):0.004, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (6.09e-07)
- neutral {D:0.985, THEM(ME):0.015}
    - 1.48e-02 -> neutral {D:0.986, THEM(ME):0.014}   via D (4.97e-03), C (4.90e-03), X (4.65e-03), and(X,X) (1.18e-04)
    - 1.36e-02 -> neutral {D:0.984, THEM(ME):0.016}   via C (4.90e-03), X (4.65e-03), THEM(ME) (3.78e-03), and(X,X) (1.18e-04)
    - 1.20e-04 -> neutral {D:0.984, THEM(ME):0.015, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.20e-04)
    - 9.18e-05 -> neutral {D:0.984, THEM(ME):0.015, and(THEM(ME),X):0.001}   via and(THEM(ME),X) (9.18e-05)
    - 9.18e-05 -> neutral {D:0.984, THEM(ME):0.015, and(X,THEM(ME)):0.001}   via and(X,THEM(ME)) (9.18e-05)
    - 1.83e-06 -> neutral {D:0.985, THEM(ME):0.014, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.83e-06)
- neutral {D:0.984, THEM(ME):0.016}
    - 1.58e-02 -> neutral {D:0.985, THEM(ME):0.015}   via D (5.31e-03), C (5.23e-03), X (4.95e-03), and(X,X) (1.26e-04)
    - 1.42e-02 -> neutral {D:0.983, THEM(ME):0.017}   via C (5.23e-03), X (4.95e-03), THEM(ME) (3.78e-03), and(X,X) (1.26e-04)
    - 1.20e-04 -> neutral {D:0.983, THEM(ME):0.016, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.20e-04)
    - 9.17e-05 -> neutral {D:0.983, THEM(ME):0.016, and(THEM(ME),X):0.001}   via and(THEM(ME),X) (9.17e-05)
    - 9.17e-05 -> neutral {D:0.983, THEM(ME):0.016, and(X,THEM(ME)):0.001}   via and(X,THEM(ME)) (9.17e-05)
    - 1.95e-06 -> neutral {D:0.984, THEM(ME):0.015, and(THEM(ME),D):0.001}   via and(THEM(ME),D) (1.95e-06)
