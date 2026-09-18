### arm=strong, n=7, game=pd, N=10, x_on=True, role=False, mode=sparse

programs 8770, classes 44, states 5667, terminal classes 1, indeterminate 0, divergence rate 0.0055
mean payoff -1.0000, efficient 0.0000, deadweight loss 1.0000, mean bits in support 2.66

| pi | state |
|---|---|
| 0.9323 | mono {D:1} |
| 0.0365 | neutral {D:0.9, THEM(ME):0.1} |
| 0.0138 | neutral {D:0.8, THEM(ME):0.2} |
| 0.0066 | neutral {D:0.7, THEM(ME):0.3} |
| 0.0028 | neutral {D:0.6, THEM(ME):0.4} |
| 0.0016 | neutral {D:0.9, and(THEM(ME),D):0.1} |
| 0.0011 | neutral {D:0.9, and(X,THEM(ME)):0.1} |
| 0.0011 | neutral {D:0.9, and(THEM(ME),X):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.90e-03 -> neutral {D:0.9, THEM(ME):0.1}   via THEM(ME) (3.90e-03)
    - 1.68e-04 -> neutral {D:0.9, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (1.68e-04)
    - 1.23e-04 -> neutral {D:0.9, and(THEM(ME),X):0.1}   via and(THEM(ME),X) (1.23e-04)
    - 1.23e-04 -> neutral {D:0.9, and(X,THEM(ME)):0.1}   via and(X,THEM(ME)) (1.23e-04)
    - 7.67e-06 -> neutral {D:0.9, and(X,and(X,THEM(ME))):0.1}   via and(X,and(X,THEM(ME))) (7.67e-06)
    - 3.83e-06 -> neutral {D:0.9, and(THEM(ME),and(X,X)):0.1}   via and(THEM(ME),and(X,X)) (3.83e-06)
- neutral {D:0.9, THEM(ME):0.1}
    - 9.96e-02 -> mono {D:1}   via D (3.31e-02), C (3.31e-02), X (3.12e-02), and(X,X) (8.56e-04)
    - 6.99e-02 -> neutral {D:0.8, THEM(ME):0.2}   via C (3.31e-02), X (3.12e-02), THEM(ME) (3.51e-03), and(X,X) (8.56e-04)
    - 1.51e-04 -> neutral {D:0.8, THEM(ME):0.1, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (1.51e-04)
    - 1.10e-04 -> neutral {D:0.8, THEM(ME):0.1, and(THEM(ME),X):0.1}   via and(THEM(ME),X) (1.10e-04)
    - 1.10e-04 -> neutral {D:0.8, THEM(ME):0.1, and(X,THEM(ME)):0.1}   via and(X,THEM(ME)) (1.10e-04)
    - 1.68e-05 -> neutral {D:0.9, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (1.68e-05)
- neutral {D:0.8, THEM(ME):0.2}
    - 1.84e-01 -> neutral {D:0.9, THEM(ME):0.1}   via D (6.63e-02), C (5.89e-02), X (5.55e-02), and(X,X) (1.52e-03)
    - 1.21e-01 -> neutral {D:0.7, THEM(ME):0.3}   via C (5.89e-02), X (5.55e-02), THEM(ME) (3.12e-03), and(X,X) (1.52e-03)
    - 1.35e-04 -> neutral {D:0.7, THEM(ME):0.2, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (1.35e-04)
    - 9.81e-05 -> neutral {D:0.7, THEM(ME):0.2, and(THEM(ME),X):0.1}   via and(THEM(ME),X) (9.81e-05)
    - 9.81e-05 -> neutral {D:0.7, THEM(ME):0.2, and(X,THEM(ME)):0.1}   via and(X,THEM(ME)) (9.81e-05)
    - 3.36e-05 -> neutral {D:0.8, THEM(ME):0.1, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (3.36e-05)
- neutral {D:0.7, THEM(ME):0.3}
    - 2.54e-01 -> neutral {D:0.8, THEM(ME):0.2}   via D (9.94e-02), C (7.73e-02), X (7.29e-02), and(X,X) (2.00e-03)
    - 1.58e-01 -> neutral {D:0.6, THEM(ME):0.4}   via C (7.73e-02), X (7.29e-02), THEM(ME) (2.73e-03), and(X,X) (2.00e-03)
    - 1.18e-04 -> neutral {D:0.6, THEM(ME):0.3, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (1.18e-04)
    - 8.58e-05 -> neutral {D:0.6, THEM(ME):0.3, and(THEM(ME),X):0.1}   via and(THEM(ME),X) (8.58e-05)
    - 8.58e-05 -> poly {D:0.6, THEM(ME):0.3, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (8.58e-05)
    - 8.58e-05 -> neutral {D:0.6, THEM(ME):0.3, and(X,THEM(ME)):0.1}   via and(X,THEM(ME)) (8.58e-05)
- neutral {D:0.6, THEM(ME):0.4}
    - 3.10e-01 -> neutral {D:0.7, THEM(ME):0.3}   via D (1.33e-01), C (8.84e-02), X (8.33e-02), and(X,X) (2.28e-03)
    - 1.79e-01 -> neutral {D:0.5, THEM(ME):0.5}   via C (8.84e-02), X (8.33e-02), THEM(ME) (2.34e-03), and(X,X) (2.28e-03)
    - 1.01e-04 -> neutral {D:0.5, THEM(ME):0.4, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (1.01e-04)
    - 7.36e-05 -> neutral {D:0.5, THEM(ME):0.4, and(THEM(ME),X):0.1}   via and(THEM(ME),X) (7.36e-05)
    - 7.36e-05 -> poly {D:0.00344, THEM(ME):0.00172, or(X,THEM(ME)):0.995}   via or(X,THEM(ME)) (7.36e-05)
    - 7.36e-05 -> neutral {D:0.5, THEM(ME):0.4, and(X,THEM(ME)):0.1}   via and(X,THEM(ME)) (7.36e-05)
- neutral {D:0.9, and(THEM(ME),D):0.1}
    - 9.96e-02 -> mono {D:1}   via D (3.31e-02), C (3.31e-02), X (3.12e-02), and(X,X) (8.56e-04)
    - 6.66e-02 -> neutral {D:0.8, and(THEM(ME),D):0.2}   via C (3.31e-02), X (3.12e-02), and(X,X) (8.56e-04), or(X,X) (8.56e-04)
    - 3.51e-03 -> neutral {D:0.8, THEM(ME):0.1, and(THEM(ME),D):0.1}   via THEM(ME) (3.51e-03)
    - 3.90e-04 -> neutral {D:0.9, THEM(ME):0.1}   via THEM(ME) (3.90e-04)
    - 1.10e-04 -> neutral {D:0.8, and(THEM(ME),D):0.1, and(THEM(ME),X):0.1}   via and(THEM(ME),X) (1.10e-04)
    - 1.10e-04 -> neutral {D:0.8, and(X,THEM(ME)):0.1, and(THEM(ME),D):0.1}   via and(X,THEM(ME)) (1.10e-04)
- neutral {D:0.9, and(X,THEM(ME)):0.1}
    - 9.96e-02 -> mono {D:1}   via D (3.31e-02), C (3.31e-02), X (3.12e-02), and(X,X) (8.56e-04)
    - 6.65e-02 -> neutral {D:0.8, and(X,THEM(ME)):0.2}   via C (3.31e-02), X (3.12e-02), and(X,X) (8.56e-04), or(X,X) (8.56e-04)
    - 3.51e-03 -> neutral {D:0.8, THEM(ME):0.1, and(X,THEM(ME)):0.1}   via THEM(ME) (3.51e-03)
    - 3.90e-04 -> neutral {D:0.9, THEM(ME):0.1}   via THEM(ME) (3.90e-04)
    - 1.51e-04 -> neutral {D:0.8, and(X,THEM(ME)):0.1, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (1.51e-04)
    - 1.10e-04 -> neutral {D:0.8, and(X,THEM(ME)):0.1, and(THEM(ME),X):0.1}   via and(THEM(ME),X) (1.10e-04)
- neutral {D:0.9, and(THEM(ME),X):0.1}
    - 9.96e-02 -> mono {D:1}   via D (3.31e-02), C (3.31e-02), X (3.12e-02), and(X,X) (8.56e-04)
    - 6.65e-02 -> neutral {D:0.8, and(THEM(ME),X):0.2}   via C (3.31e-02), X (3.12e-02), and(X,X) (8.56e-04), or(X,X) (8.56e-04)
    - 3.51e-03 -> neutral {D:0.8, THEM(ME):0.1, and(THEM(ME),X):0.1}   via THEM(ME) (3.51e-03)
    - 3.90e-04 -> neutral {D:0.9, THEM(ME):0.1}   via THEM(ME) (3.90e-04)
    - 1.51e-04 -> neutral {D:0.8, and(THEM(ME),D):0.1, and(THEM(ME),X):0.1}   via and(THEM(ME),D) (1.51e-04)
    - 1.10e-04 -> neutral {D:0.8, and(X,THEM(ME)):0.1, and(THEM(ME),X):0.1}   via and(X,THEM(ME)) (1.10e-04)
