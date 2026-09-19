### arm=weak, n=5, game=bos, N=100, x_on=True, role=True, mode=square

programs 902, classes 54, states 6152, terminal classes 1, indeterminate 0, divergence rate 0.0010
mean payoff 1.5000, efficient 1.5000, deadweight loss 0.0000, mean bits in support 3.03

| pi | state |
|---|---|
| 0.4177 | mono {C:1} |
| 0.4176 | mono {D:1} |
| 0.0184 | neutral {C:0.99, THEM(^C):0.01} |
| 0.0184 | neutral {D:0.99, THEM(^D):0.01} |
| 0.0181 | neutral {C:0.99, THEM(^D):0.01} |
| 0.0180 | neutral {D:0.99, THEM(^C):0.01} |
| 0.0074 | neutral {C:0.98, THEM(^C):0.02} |
| 0.0074 | neutral {D:0.98, THEM(^D):0.02} |
| 0.0071 | neutral {C:0.98, THEM(^D):0.02} |
| 0.0071 | neutral {D:0.98, THEM(^C):0.02} |
| 0.0038 | neutral {C:0.97, THEM(^C):0.03} |
| 0.0038 | neutral {D:0.97, THEM(^D):0.03} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 4.39e-04 -> neutral {C:0.99, THEM(^D):0.01}   via THEM(^D) (4.39e-04)
    - 4.39e-04 -> neutral {C:0.99, THEM(^C):0.01}   via THEM(^C) (4.39e-04)
    - 3.64e-05 -> neutral {C:0.99, or(ROLE,THEM(THEM)):0.01}   via or(ROLE,THEM(THEM)) (3.64e-05)
    - 3.64e-05 -> neutral {C:0.99, or(ROLE,THEM(ME)):0.01}   via or(ROLE,THEM(ME)) (3.64e-05)
    - 3.64e-05 -> neutral {C:0.99, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (3.64e-05)
    - 3.64e-05 -> neutral {C:0.99, or(X,THEM(ME)):0.01}   via or(X,THEM(ME)) (3.64e-05)
- mono {D:1}
    - 4.39e-04 -> neutral {D:0.99, THEM(^D):0.01}   via THEM(^D) (4.39e-04)
    - 4.39e-04 -> neutral {D:0.99, THEM(^C):0.01}   via THEM(^C) (4.39e-04)
    - 3.64e-05 -> neutral {D:0.99, and(ROLE,THEM(THEM)):0.01}   via and(ROLE,THEM(THEM)) (3.64e-05)
    - 3.64e-05 -> neutral {D:0.99, and(ROLE,THEM(ME)):0.01}   via and(ROLE,THEM(ME)) (3.64e-05)
    - 3.64e-05 -> neutral {D:0.99, and(X,THEM(THEM)):0.01}   via and(X,THEM(THEM)) (3.64e-05)
    - 3.64e-05 -> neutral {D:0.99, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (3.64e-05)
- neutral {C:0.99, THEM(^C):0.01}
    - 9.99e-03 -> mono {C:1}   via C (2.49e-03), D (2.49e-03), X (2.31e-03), ROLE (1.90e-03)
    - 7.94e-03 -> neutral {C:0.98, THEM(^C):0.02}   via D (2.49e-03), X (2.31e-03), ROLE (1.90e-03), not(ROLE) (4.75e-04)
    - 3.61e-05 -> neutral {C:0.98, THEM(^C):0.01, or(ROLE,THEM(THEM)):0.01}   via or(ROLE,THEM(THEM)) (3.61e-05)
    - 3.61e-05 -> neutral {C:0.98, THEM(^C):0.01, or(ROLE,THEM(ME)):0.01}   via or(ROLE,THEM(ME)) (3.61e-05)
    - 3.61e-05 -> neutral {C:0.98, THEM(^C):0.01, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (3.61e-05)
    - 3.61e-05 -> neutral {C:0.98, THEM(^C):0.01, or(X,THEM(ME)):0.01}   via or(X,THEM(ME)) (3.61e-05)
- neutral {D:0.99, THEM(^D):0.01}
    - 9.99e-03 -> mono {D:1}   via D (2.49e-03), C (2.49e-03), X (2.31e-03), ROLE (1.90e-03)
    - 7.94e-03 -> neutral {D:0.98, THEM(^D):0.02}   via C (2.49e-03), X (2.31e-03), ROLE (1.90e-03), not(ROLE) (4.75e-04)
    - 3.61e-05 -> neutral {D:0.98, THEM(^D):0.01, and(ROLE,THEM(THEM)):0.01}   via and(ROLE,THEM(THEM)) (3.61e-05)
    - 3.61e-05 -> neutral {D:0.98, THEM(^D):0.01, and(ROLE,THEM(ME)):0.01}   via and(ROLE,THEM(ME)) (3.61e-05)
    - 3.61e-05 -> neutral {D:0.98, THEM(^D):0.01, and(X,THEM(THEM)):0.01}   via and(X,THEM(THEM)) (3.61e-05)
    - 3.61e-05 -> neutral {D:0.98, THEM(^D):0.01, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (3.61e-05)
- neutral {C:0.99, THEM(^D):0.01}
    - 9.99e-03 -> mono {C:1}   via C (2.49e-03), D (2.49e-03), X (2.31e-03), ROLE (1.90e-03)
    - 7.94e-03 -> neutral {C:0.98, THEM(^D):0.02}   via D (2.49e-03), X (2.31e-03), ROLE (1.90e-03), not(ROLE) (4.75e-04)
    - 3.57e-05 -> neutral {C:0.99, or(ROLE,THEM(THEM)):0.01}   via or(ROLE,THEM(THEM)) (3.57e-05)
    - 3.57e-05 -> neutral {C:0.99, or(ROLE,THEM(ME)):0.01}   via or(ROLE,THEM(ME)) (3.57e-05)
    - 4.39e-06 -> neutral {C:0.99, THEM(^C):0.01}   via THEM(^C) (4.39e-06)
    - 7.21e-07 -> neutral {C:0.98, or(ROLE,THEM(THEM)):0.02}   via or(ROLE,THEM(THEM)) (7.21e-07)
- neutral {D:0.99, THEM(^C):0.01}
    - 9.99e-03 -> mono {D:1}   via D (2.49e-03), C (2.49e-03), X (2.31e-03), ROLE (1.90e-03)
    - 7.94e-03 -> neutral {D:0.98, THEM(^C):0.02}   via C (2.49e-03), X (2.31e-03), ROLE (1.90e-03), not(ROLE) (4.75e-04)
    - 3.57e-05 -> neutral {D:0.99, and(ROLE,THEM(THEM)):0.01}   via and(ROLE,THEM(THEM)) (3.57e-05)
    - 3.57e-05 -> neutral {D:0.99, and(ROLE,THEM(ME)):0.01}   via and(ROLE,THEM(ME)) (3.57e-05)
    - 4.39e-06 -> neutral {D:0.99, THEM(^D):0.01}   via THEM(^D) (4.39e-06)
    - 7.21e-07 -> neutral {D:0.98, and(ROLE,THEM(THEM)):0.02}   via and(ROLE,THEM(THEM)) (7.21e-07)
- neutral {C:0.98, THEM(^C):0.02}
    - 1.98e-02 -> neutral {C:0.99, THEM(^C):0.01}   via C (4.98e-03), D (4.93e-03), X (4.58e-03), ROLE (3.77e-03)
    - 1.53e-02 -> neutral {C:0.97, THEM(^C):0.03}   via D (4.93e-03), X (4.58e-03), ROLE (3.77e-03), not(ROLE) (9.40e-04)
    - 3.57e-05 -> neutral {C:0.97, THEM(^C):0.02, or(ROLE,THEM(THEM)):0.01}   via or(ROLE,THEM(THEM)) (3.57e-05)
    - 3.57e-05 -> neutral {C:0.97, THEM(^C):0.02, or(ROLE,THEM(ME)):0.01}   via or(ROLE,THEM(ME)) (3.57e-05)
    - 3.57e-05 -> neutral {C:0.97, THEM(^C):0.02, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (3.57e-05)
    - 3.57e-05 -> neutral {C:0.97, THEM(^C):0.02, or(X,THEM(ME)):0.01}   via or(X,THEM(ME)) (3.57e-05)
- neutral {D:0.98, THEM(^D):0.02}
    - 1.98e-02 -> neutral {D:0.99, THEM(^D):0.01}   via D (4.98e-03), C (4.93e-03), X (4.58e-03), ROLE (3.77e-03)
    - 1.53e-02 -> neutral {D:0.97, THEM(^D):0.03}   via C (4.93e-03), X (4.58e-03), ROLE (3.77e-03), not(ROLE) (9.40e-04)
    - 3.57e-05 -> neutral {D:0.97, THEM(^D):0.02, and(ROLE,THEM(THEM)):0.01}   via and(ROLE,THEM(THEM)) (3.57e-05)
    - 3.57e-05 -> neutral {D:0.97, THEM(^D):0.02, and(ROLE,THEM(ME)):0.01}   via and(ROLE,THEM(ME)) (3.57e-05)
    - 3.57e-05 -> neutral {D:0.97, THEM(^D):0.02, and(X,THEM(THEM)):0.01}   via and(X,THEM(THEM)) (3.57e-05)
    - 3.57e-05 -> neutral {D:0.97, THEM(^D):0.02, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (3.57e-05)
- neutral {C:0.98, THEM(^D):0.02}
    - 1.98e-02 -> neutral {C:0.99, THEM(^D):0.01}   via C (4.98e-03), D (4.93e-03), X (4.58e-03), ROLE (3.77e-03)
    - 1.53e-02 -> neutral {C:0.97, THEM(^D):0.03}   via D (4.93e-03), X (4.58e-03), ROLE (3.77e-03), not(ROLE) (9.40e-04)
    - 3.47e-05 -> neutral {C:0.98, or(ROLE,THEM(THEM)):0.02}   via or(ROLE,THEM(THEM)) (3.47e-05)
    - 3.47e-05 -> neutral {C:0.98, or(ROLE,THEM(ME)):0.02}   via or(ROLE,THEM(ME)) (3.47e-05)
    - 1.07e-06 -> neutral {C:0.97, or(ROLE,THEM(THEM)):0.03}   via or(ROLE,THEM(THEM)) (1.07e-06)
    - 1.07e-06 -> neutral {C:0.97, or(ROLE,THEM(ME)):0.03}   via or(ROLE,THEM(ME)) (1.07e-06)
- neutral {D:0.98, THEM(^C):0.02}
    - 1.98e-02 -> neutral {D:0.99, THEM(^C):0.01}   via D (4.98e-03), C (4.93e-03), X (4.58e-03), ROLE (3.77e-03)
    - 1.53e-02 -> neutral {D:0.97, THEM(^C):0.03}   via C (4.93e-03), X (4.58e-03), ROLE (3.77e-03), not(ROLE) (9.40e-04)
    - 3.47e-05 -> neutral {D:0.98, and(ROLE,THEM(THEM)):0.02}   via and(ROLE,THEM(THEM)) (3.47e-05)
    - 3.47e-05 -> neutral {D:0.98, and(ROLE,THEM(ME)):0.02}   via and(ROLE,THEM(ME)) (3.47e-05)
    - 1.07e-06 -> neutral {D:0.97, and(ROLE,THEM(THEM)):0.03}   via and(ROLE,THEM(THEM)) (1.07e-06)
    - 1.07e-06 -> neutral {D:0.97, and(ROLE,THEM(ME)):0.03}   via and(ROLE,THEM(ME)) (1.07e-06)
- neutral {C:0.97, THEM(^C):0.03}
    - 2.95e-02 -> neutral {C:0.98, THEM(^C):0.02}   via C (7.47e-03), D (7.32e-03), X (6.80e-03), ROLE (5.60e-03)
    - 2.25e-02 -> neutral {C:0.96, THEM(^C):0.04}   via D (7.32e-03), X (6.80e-03), ROLE (5.60e-03), not(ROLE) (1.40e-03)
    - 3.53e-05 -> neutral {C:0.96, THEM(^C):0.03, or(ROLE,THEM(THEM)):0.01}   via or(ROLE,THEM(THEM)) (3.53e-05)
    - 3.53e-05 -> neutral {C:0.96, THEM(^C):0.03, or(ROLE,THEM(ME)):0.01}   via or(ROLE,THEM(ME)) (3.53e-05)
    - 3.53e-05 -> neutral {C:0.96, THEM(^C):0.03, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (3.53e-05)
    - 3.53e-05 -> neutral {C:0.96, THEM(^C):0.03, or(X,THEM(ME)):0.01}   via or(X,THEM(ME)) (3.53e-05)
- neutral {D:0.97, THEM(^D):0.03}
    - 2.95e-02 -> neutral {D:0.98, THEM(^D):0.02}   via D (7.47e-03), C (7.32e-03), X (6.80e-03), ROLE (5.60e-03)
    - 2.25e-02 -> neutral {D:0.96, THEM(^D):0.04}   via C (7.32e-03), X (6.80e-03), ROLE (5.60e-03), not(ROLE) (1.40e-03)
    - 3.53e-05 -> neutral {D:0.96, THEM(^D):0.03, and(ROLE,THEM(THEM)):0.01}   via and(ROLE,THEM(THEM)) (3.53e-05)
    - 3.53e-05 -> neutral {D:0.96, THEM(^D):0.03, and(ROLE,THEM(ME)):0.01}   via and(ROLE,THEM(ME)) (3.53e-05)
    - 3.53e-05 -> neutral {D:0.96, THEM(^D):0.03, and(X,THEM(THEM)):0.01}   via and(X,THEM(THEM)) (3.53e-05)
    - 3.53e-05 -> neutral {D:0.96, THEM(^D):0.03, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (3.53e-05)
