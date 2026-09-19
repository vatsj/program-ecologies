### arm=weak, n=6, game=stag, N=10, x_on=True, role=False, mode=square

programs 1852, classes 46, states 1332, terminal classes 2, indeterminate 0, divergence rate 0.0019
mean payoff 4.0000, efficient 4.0000, deadweight loss -0.0000, mean bits in support 2.62
absorption: class 0: 1.000, class 12: 0.000

| pi | state |
|---|---|
| 0.9812 | mono {C:1} |
| 0.0089 | neutral {C:0.9, THEM(^C):0.1} |
| 0.0033 | neutral {C:0.8, THEM(^C):0.2} |
| 0.0015 | neutral {C:0.7, THEM(^C):0.3} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 9.10e-04 -> neutral {C:0.9, THEM(^C):0.1}   via THEM(^C) (9.10e-04)
    - 8.80e-05 -> neutral {C:0.9, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (8.80e-05)
    - 8.80e-05 -> neutral {C:0.9, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (8.80e-05)
    - 2.66e-05 -> neutral {C:0.9, or(X,THEM(^C)):0.1}   via or(X,THEM(^C)) (2.66e-05)
- neutral {C:0.9, THEM(^C):0.1}
    - 9.99e-02 -> mono {C:1}   via C (3.29e-02), D (3.29e-02), X (3.12e-02), and(X,X) (7.54e-04)
    - 6.78e-02 -> neutral {C:0.8, THEM(^C):0.2}   via D (3.29e-02), X (3.12e-02), THEM(^C) (8.19e-04), and(X,X) (7.54e-04)
    - 7.92e-05 -> neutral {C:0.8, THEM(^C):0.1, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (7.92e-05)
    - 7.92e-05 -> neutral {C:0.8, THEM(^C):0.1, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (7.92e-05)
    - 2.39e-05 -> neutral {C:0.8, THEM(^C):0.1, or(X,THEM(^C)):0.1}   via or(X,THEM(^C)) (2.39e-05)
    - 8.80e-06 -> neutral {C:0.9, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (8.80e-06)
- neutral {C:0.8, THEM(^C):0.2}
    - 1.85e-01 -> neutral {C:0.9, THEM(^C):0.1}   via C (6.58e-02), D (5.85e-02), X (5.55e-02), and(X,X) (1.34e-03)
    - 1.20e-01 -> neutral {C:0.7, THEM(^C):0.3}   via D (5.85e-02), X (5.55e-02), and(X,X) (1.34e-03), or(X,X) (1.34e-03)
    - 7.04e-05 -> neutral {C:0.7, THEM(^C):0.2, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (7.04e-05)
    - 7.04e-05 -> neutral {C:0.7, THEM(^C):0.2, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (7.04e-05)
    - 2.13e-05 -> neutral {C:0.7, THEM(^C):0.2, or(X,THEM(^C)):0.1}   via or(X,THEM(^C)) (2.13e-05)
    - 1.76e-05 -> neutral {C:0.8, THEM(^C):0.1, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (1.76e-05)
- neutral {C:0.7, THEM(^C):0.3}
    - 2.55e-01 -> neutral {C:0.8, THEM(^C):0.2}   via C (9.87e-02), D (7.68e-02), X (7.29e-02), and(X,X) (1.76e-03)
    - 1.57e-01 -> neutral {C:0.6, THEM(^C):0.4}   via D (7.68e-02), X (7.29e-02), and(X,X) (1.76e-03), or(X,X) (1.76e-03)
    - 6.16e-05 -> neutral {C:0.6, THEM(^C):0.3, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (6.16e-05)
    - 6.16e-05 -> neutral {C:0.6, THEM(^C):0.3, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (6.16e-05)
    - 2.64e-05 -> neutral {C:0.7, THEM(^C):0.2, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (2.64e-05)
    - 2.64e-05 -> neutral {C:0.7, THEM(^C):0.2, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (2.64e-05)
