### arm=weak, n=5, game=bos, N=10, x_on=True, role=True, mode=square

programs 902, classes 54, states 1121, terminal classes 1, indeterminate 0, divergence rate 0.0010
mean payoff 1.4554, efficient 1.5000, deadweight loss 0.0446, mean bits in support 4.73

| pi | state |
|---|---|
| 0.3576 | mono {C:1} |
| 0.3576 | mono {D:1} |
| 0.0676 | poly {ROLE:0.3, THEM(^D):0.7} |
| 0.0676 | poly {ROLE:0.3, THEM(^C):0.7} |
| 0.0338 | poly {ROLE:0.3, THEM(^D):0.6, or(THEM(THEM),ROLE):0.1} |
| 0.0338 | poly {ROLE:0.3, THEM(^D):0.6, or(THEM(ME),ROLE):0.1} |
| 0.0338 | poly {ROLE:0.3, THEM(^C):0.6, and(THEM(THEM),ROLE):0.1} |
| 0.0338 | poly {ROLE:0.3, THEM(^C):0.6, and(THEM(ME),ROLE):0.1} |
| 0.0015 | neutral {C:0.9, THEM(^C):0.1} |
| 0.0015 | neutral {D:0.9, THEM(^D):0.1} |
| 0.0015 | neutral {C:0.9, THEM(^D):0.1} |
| 0.0015 | neutral {D:0.9, THEM(^C):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 4.39e-04 -> neutral {C:0.9, THEM(^D):0.1}   via THEM(^D) (4.39e-04)
    - 4.39e-04 -> neutral {C:0.9, THEM(^C):0.1}   via THEM(^C) (4.39e-04)
    - 3.64e-05 -> neutral {C:0.9, or(ROLE,THEM(THEM)):0.1}   via or(ROLE,THEM(THEM)) (3.64e-05)
    - 3.64e-05 -> neutral {C:0.9, or(ROLE,THEM(ME)):0.1}   via or(ROLE,THEM(ME)) (3.64e-05)
    - 3.64e-05 -> neutral {C:0.9, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (3.64e-05)
    - 3.64e-05 -> neutral {C:0.9, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (3.64e-05)
- mono {D:1}
    - 4.39e-04 -> neutral {D:0.9, THEM(^D):0.1}   via THEM(^D) (4.39e-04)
    - 4.39e-04 -> neutral {D:0.9, THEM(^C):0.1}   via THEM(^C) (4.39e-04)
    - 3.64e-05 -> neutral {D:0.9, and(ROLE,THEM(THEM)):0.1}   via and(ROLE,THEM(THEM)) (3.64e-05)
    - 3.64e-05 -> neutral {D:0.9, and(ROLE,THEM(ME)):0.1}   via and(ROLE,THEM(ME)) (3.64e-05)
    - 3.64e-05 -> neutral {D:0.9, and(X,THEM(THEM)):0.1}   via and(X,THEM(THEM)) (3.64e-05)
    - 3.64e-05 -> neutral {D:0.9, and(X,THEM(ME)):0.1}   via and(X,THEM(ME)) (3.64e-05)
- poly {ROLE:0.3, THEM(^D):0.7}
    - 3.64e-05 -> mono {or(ROLE,THEM(THEM)):1}   via or(ROLE,THEM(THEM)) (3.64e-05)
    - 3.64e-05 -> mono {or(ROLE,THEM(ME)):1}   via or(ROLE,THEM(ME)) (3.64e-05)
    - 3.64e-05 -> poly {ROLE:0.3, THEM(^D):0.6, or(THEM(THEM),ROLE):0.1}   via or(THEM(THEM),ROLE) (3.64e-05)
    - 3.64e-05 -> poly {ROLE:0.3, THEM(^D):0.6, or(THEM(ME),ROLE):0.1}   via or(THEM(ME),ROLE) (3.64e-05)
- poly {ROLE:0.3, THEM(^C):0.7}
    - 3.64e-05 -> mono {and(ROLE,THEM(THEM)):1}   via and(ROLE,THEM(THEM)) (3.64e-05)
    - 3.64e-05 -> mono {and(ROLE,THEM(ME)):1}   via and(ROLE,THEM(ME)) (3.64e-05)
    - 3.64e-05 -> poly {ROLE:0.3, THEM(^C):0.6, and(THEM(THEM),ROLE):0.1}   via and(THEM(THEM),ROLE) (3.64e-05)
    - 3.64e-05 -> poly {ROLE:0.3, THEM(^C):0.6, and(THEM(ME),ROLE):0.1}   via and(THEM(ME),ROLE) (3.64e-05)
- poly {ROLE:0.3, THEM(^D):0.6, or(THEM(THEM),ROLE):0.1}
    - 3.64e-05 -> mono {or(ROLE,THEM(THEM)):1}   via or(ROLE,THEM(THEM)) (3.64e-05)
    - 3.64e-05 -> mono {or(ROLE,THEM(ME)):1}   via or(ROLE,THEM(ME)) (3.64e-05)
    - 3.64e-06 -> poly {ROLE:0.3, THEM(^D):0.6, or(THEM(ME),ROLE):0.1}   via or(THEM(ME),ROLE) (3.64e-06)
- poly {ROLE:0.3, THEM(^D):0.6, or(THEM(ME),ROLE):0.1}
    - 3.64e-05 -> mono {or(ROLE,THEM(THEM)):1}   via or(ROLE,THEM(THEM)) (3.64e-05)
    - 3.64e-05 -> mono {or(ROLE,THEM(ME)):1}   via or(ROLE,THEM(ME)) (3.64e-05)
    - 3.64e-06 -> poly {ROLE:0.3, THEM(^D):0.6, or(THEM(THEM),ROLE):0.1}   via or(THEM(THEM),ROLE) (3.64e-06)
- poly {ROLE:0.3, THEM(^C):0.6, and(THEM(THEM),ROLE):0.1}
    - 3.64e-05 -> mono {and(ROLE,THEM(THEM)):1}   via and(ROLE,THEM(THEM)) (3.64e-05)
    - 3.64e-05 -> mono {and(ROLE,THEM(ME)):1}   via and(ROLE,THEM(ME)) (3.64e-05)
    - 3.64e-06 -> poly {ROLE:0.3, THEM(^C):0.6, and(THEM(ME),ROLE):0.1}   via and(THEM(ME),ROLE) (3.64e-06)
- poly {ROLE:0.3, THEM(^C):0.6, and(THEM(ME),ROLE):0.1}
    - 3.64e-05 -> mono {and(ROLE,THEM(THEM)):1}   via and(ROLE,THEM(THEM)) (3.64e-05)
    - 3.64e-05 -> mono {and(ROLE,THEM(ME)):1}   via and(ROLE,THEM(ME)) (3.64e-05)
    - 3.64e-06 -> poly {ROLE:0.3, THEM(^C):0.6, and(THEM(THEM),ROLE):0.1}   via and(THEM(THEM),ROLE) (3.64e-06)
- neutral {C:0.9, THEM(^C):0.1}
    - 9.99e-02 -> mono {C:1}   via C (2.49e-02), D (2.49e-02), X (2.31e-02), ROLE (1.90e-02)
    - 7.54e-02 -> neutral {C:0.8, THEM(^C):0.2}   via D (2.49e-02), X (2.31e-02), ROLE (1.90e-02), not(ROLE) (4.75e-03)
    - 4.39e-05 -> neutral {C:0.9, THEM(^D):0.1}   via THEM(^D) (4.39e-05)
    - 3.28e-05 -> neutral {C:0.8, THEM(^C):0.1, or(ROLE,THEM(THEM)):0.1}   via or(ROLE,THEM(THEM)) (3.28e-05)
    - 3.28e-05 -> neutral {C:0.8, THEM(^C):0.1, or(ROLE,THEM(ME)):0.1}   via or(ROLE,THEM(ME)) (3.28e-05)
    - 3.28e-05 -> neutral {C:0.8, THEM(^C):0.1, or(X,THEM(THEM)):0.1}   via or(X,THEM(THEM)) (3.28e-05)
- neutral {D:0.9, THEM(^D):0.1}
    - 9.99e-02 -> mono {D:1}   via D (2.49e-02), C (2.49e-02), X (2.31e-02), ROLE (1.90e-02)
    - 7.54e-02 -> neutral {D:0.8, THEM(^D):0.2}   via C (2.49e-02), X (2.31e-02), ROLE (1.90e-02), not(ROLE) (4.75e-03)
    - 4.39e-05 -> neutral {D:0.9, THEM(^C):0.1}   via THEM(^C) (4.39e-05)
    - 3.28e-05 -> neutral {D:0.8, THEM(^D):0.1, and(ROLE,THEM(THEM)):0.1}   via and(ROLE,THEM(THEM)) (3.28e-05)
    - 3.28e-05 -> neutral {D:0.8, THEM(^D):0.1, and(ROLE,THEM(ME)):0.1}   via and(ROLE,THEM(ME)) (3.28e-05)
    - 3.28e-05 -> neutral {D:0.8, THEM(^D):0.1, and(X,THEM(THEM)):0.1}   via and(X,THEM(THEM)) (3.28e-05)
- neutral {C:0.9, THEM(^D):0.1}
    - 9.99e-02 -> mono {C:1}   via C (2.49e-02), D (2.49e-02), X (2.31e-02), ROLE (1.90e-02)
    - 7.54e-02 -> neutral {C:0.8, THEM(^D):0.2}   via D (2.49e-02), X (2.31e-02), ROLE (1.90e-02), not(ROLE) (4.75e-03)
    - 4.39e-05 -> neutral {C:0.9, THEM(^C):0.1}   via THEM(^C) (4.39e-05)
    - 2.99e-05 -> neutral {C:0.9, or(ROLE,THEM(THEM)):0.1}   via or(ROLE,THEM(THEM)) (2.99e-05)
    - 2.99e-05 -> neutral {C:0.9, or(ROLE,THEM(ME)):0.1}   via or(ROLE,THEM(ME)) (2.99e-05)
    - 6.56e-06 -> neutral {C:0.8, or(ROLE,THEM(THEM)):0.2}   via or(ROLE,THEM(THEM)) (6.56e-06)
- neutral {D:0.9, THEM(^C):0.1}
    - 9.99e-02 -> mono {D:1}   via D (2.49e-02), C (2.49e-02), X (2.31e-02), ROLE (1.90e-02)
    - 7.54e-02 -> neutral {D:0.8, THEM(^C):0.2}   via C (2.49e-02), X (2.31e-02), ROLE (1.90e-02), not(ROLE) (4.75e-03)
    - 4.39e-05 -> neutral {D:0.9, THEM(^D):0.1}   via THEM(^D) (4.39e-05)
    - 2.99e-05 -> neutral {D:0.9, and(ROLE,THEM(THEM)):0.1}   via and(ROLE,THEM(THEM)) (2.99e-05)
    - 2.99e-05 -> neutral {D:0.9, and(ROLE,THEM(ME)):0.1}   via and(ROLE,THEM(ME)) (2.99e-05)
    - 6.56e-06 -> neutral {D:0.8, and(ROLE,THEM(THEM)):0.2}   via and(ROLE,THEM(THEM)) (6.56e-06)
