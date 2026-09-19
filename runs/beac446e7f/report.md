### arm=strong, n=6, game=stag, N=1000, x_on=True, role=False, mode=square

programs 1726, classes 21, states 43053, terminal classes 2, indeterminate 0, divergence rate 0.0004
mean payoff 3.3320, efficient 4.0000, deadweight loss 0.6680, mean bits in support 2.64
absorption: class 0: 0.332, class 2: 0.668

| pi | state |
|---|---|
| 0.2847 | mono {C:1} |
| 0.0324 | neutral {D:0.991, THEM(ME):0.009} |
| 0.0318 | neutral {D:0.99, THEM(ME):0.01} |
| 0.0318 | neutral {D:0.992, THEM(ME):0.008} |
| 0.0304 | neutral {D:0.989, THEM(ME):0.011} |
| 0.0299 | neutral {D:0.993, THEM(ME):0.007} |
| 0.0282 | neutral {D:0.988, THEM(ME):0.012} |
| 0.0267 | neutral {D:0.994, THEM(ME):0.006} |
| 0.0265 | neutral {C:0.999, or(X,THEM(ME)):0.001} |
| 0.0257 | neutral {D:0.987, THEM(ME):0.013} |
| 0.0229 | neutral {D:0.986, THEM(ME):0.014} |
| 0.0223 | neutral {D:0.995, THEM(ME):0.005} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 9.32e-05 -> neutral {C:0.999, or(X,THEM(ME)):0.001}   via or(X,THEM(ME)) (9.32e-05)
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
- neutral {C:0.999, or(X,THEM(ME)):0.001}
    - 1.00e-03 -> mono {C:1}   via C (3.32e-04), D (3.32e-04), X (3.14e-04), and(X,X) (7.98e-06)
    - 7.61e-04 -> neutral {C:0.998, or(X,THEM(ME)):0.002}   via D (3.32e-04), X (3.14e-04), or(X,THEM(ME)) (9.31e-05), and(X,X) (7.98e-06)
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
