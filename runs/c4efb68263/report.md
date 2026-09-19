### arm=strong, n=7, game=pd, N=100, x_on=True, role=False, mode=sparse

programs 8770, classes 44, states 47728, terminal classes 1, indeterminate 0, divergence rate 0.0058
mean payoff -1.0000, efficient 0.0000, deadweight loss 1.0000, mean bits in support 2.67

| pi | state |
|---|---|
| 0.4902 | mono {D:1} |
| 0.1918 | neutral {D:0.99, THEM(ME):0.01} |
| 0.1018 | neutral {D:0.98, THEM(ME):0.02} |
| 0.0586 | neutral {D:0.97, THEM(ME):0.03} |
| 0.0350 | neutral {D:0.96, THEM(ME):0.04} |
| 0.0213 | neutral {D:0.95, THEM(ME):0.05} |
| 0.0131 | neutral {D:0.94, THEM(ME):0.06} |
| 0.0083 | neutral {D:0.99, and(THEM(ME),D):0.01} |
| 0.0082 | neutral {D:0.93, THEM(ME):0.07} |
| 0.0060 | neutral {D:0.99, and(THEM(ME),X):0.01} |
| 0.0060 | neutral {D:0.99, and(X,THEM(ME)):0.01} |
| 0.0051 | neutral {D:0.92, THEM(ME):0.08} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.90e-03 -> neutral {D:0.99, THEM(ME):0.01}   via THEM(ME) (3.90e-03)
    - 1.68e-04 -> neutral {D:0.99, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.68e-04)
    - 1.23e-04 -> neutral {D:0.99, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (1.23e-04)
    - 1.23e-04 -> neutral {D:0.99, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (1.23e-04)
    - 7.67e-06 -> neutral {D:0.99, and(X,and(X,THEM(ME))):0.01}   via and(X,and(X,THEM(ME))) (7.67e-06)
    - 3.83e-06 -> neutral {D:0.99, and(THEM(ME),and(X,X)):0.01}   via and(THEM(ME),and(X,X)) (3.83e-06)
- neutral {D:0.99, THEM(ME):0.01}
    - 1.05e-02 -> neutral {D:0.98, THEM(ME):0.02}   via THEM(ME) (3.86e-03), C (3.31e-03), X (3.12e-03), and(X,X) (8.56e-05)
    - 9.96e-03 -> mono {D:1}   via D (3.31e-03), C (3.31e-03), X (3.12e-03), and(X,X) (8.56e-05)
    - 1.66e-04 -> neutral {D:0.98, THEM(ME):0.01, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.66e-04)
    - 1.21e-04 -> neutral {D:0.98, THEM(ME):0.01, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (1.21e-04)
    - 1.21e-04 -> neutral {D:0.98, THEM(ME):0.01, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (1.21e-04)
    - 7.59e-06 -> neutral {D:0.98, THEM(ME):0.01, and(X,and(X,THEM(ME))):0.01}   via and(X,and(X,THEM(ME))) (7.59e-06)
- neutral {D:0.98, THEM(ME):0.02}
    - 1.98e-02 -> neutral {D:0.99, THEM(ME):0.01}   via D (6.63e-03), C (6.56e-03), X (6.18e-03), and(X,X) (1.70e-04)
    - 1.70e-02 -> neutral {D:0.97, THEM(ME):0.03}   via C (6.56e-03), X (6.18e-03), THEM(ME) (3.82e-03), and(X,X) (1.70e-04)
    - 1.65e-04 -> neutral {D:0.97, THEM(ME):0.02, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.65e-04)
    - 1.20e-04 -> neutral {D:0.97, THEM(ME):0.02, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (1.20e-04)
    - 1.20e-04 -> neutral {D:0.97, THEM(ME):0.02, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (1.20e-04)
    - 7.51e-06 -> neutral {D:0.97, THEM(ME):0.02, and(X,and(X,THEM(ME))):0.01}   via and(X,and(X,THEM(ME))) (7.51e-06)
- neutral {D:0.97, THEM(ME):0.03}
    - 2.95e-02 -> neutral {D:0.98, THEM(ME):0.02}   via D (9.94e-03), C (9.74e-03), X (9.18e-03), and(X,X) (2.52e-04)
    - 2.33e-02 -> neutral {D:0.96, THEM(ME):0.04}   via C (9.74e-03), X (9.18e-03), THEM(ME) (3.78e-03), and(X,X) (2.52e-04)
    - 1.63e-04 -> neutral {D:0.96, THEM(ME):0.03, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.63e-04)
    - 1.19e-04 -> neutral {D:0.96, THEM(ME):0.03, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (1.19e-04)
    - 1.19e-04 -> neutral {D:0.96, THEM(ME):0.03, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (1.19e-04)
    - 7.44e-06 -> neutral {D:0.96, THEM(ME):0.03, and(X,and(X,THEM(ME))):0.01}   via and(X,and(X,THEM(ME))) (7.44e-06)
- neutral {D:0.96, THEM(ME):0.04}
    - 3.90e-02 -> neutral {D:0.97, THEM(ME):0.03}   via D (1.33e-02), C (1.29e-02), X (1.21e-02), and(X,X) (3.32e-04)
    - 2.95e-02 -> neutral {D:0.95, THEM(ME):0.05}   via C (1.29e-02), X (1.21e-02), THEM(ME) (3.74e-03), and(X,X) (3.32e-04)
    - 1.61e-04 -> neutral {D:0.95, THEM(ME):0.04, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.61e-04)
    - 1.18e-04 -> neutral {D:0.95, THEM(ME):0.04, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (1.18e-04)
    - 1.18e-04 -> neutral {D:0.95, THEM(ME):0.04, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (1.18e-04)
    - 7.36e-06 -> neutral {D:0.95, THEM(ME):0.04, and(X,and(X,THEM(ME))):0.01}   via and(X,and(X,THEM(ME))) (7.36e-06)
- neutral {D:0.95, THEM(ME):0.05}
    - 4.84e-02 -> neutral {D:0.96, THEM(ME):0.04}   via D (1.66e-02), C (1.59e-02), X (1.50e-02), and(X,X) (4.11e-04)
    - 3.56e-02 -> neutral {D:0.94, THEM(ME):0.06}   via C (1.59e-02), X (1.50e-02), THEM(ME) (3.70e-03), and(X,X) (4.11e-04)
    - 1.60e-04 -> neutral {D:0.94, THEM(ME):0.05, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.60e-04)
    - 1.16e-04 -> neutral {D:0.94, THEM(ME):0.05, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (1.16e-04)
    - 1.16e-04 -> neutral {D:0.94, THEM(ME):0.05, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (1.16e-04)
    - 8.41e-06 -> neutral {D:0.95, THEM(ME):0.04, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (8.41e-06)
- neutral {D:0.94, THEM(ME):0.06}
    - 5.77e-02 -> neutral {D:0.95, THEM(ME):0.05}   via D (1.99e-02), C (1.89e-02), X (1.78e-02), and(X,X) (4.88e-04)
    - 4.15e-02 -> neutral {D:0.93, THEM(ME):0.07}   via C (1.89e-02), X (1.78e-02), THEM(ME) (3.66e-03), and(X,X) (4.88e-04)
    - 1.58e-04 -> neutral {D:0.93, THEM(ME):0.06, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.58e-04)
    - 1.15e-04 -> neutral {D:0.93, THEM(ME):0.06, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (1.15e-04)
    - 1.15e-04 -> neutral {D:0.93, THEM(ME):0.06, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (1.15e-04)
    - 1.01e-05 -> neutral {D:0.94, THEM(ME):0.05, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.01e-05)
- neutral {D:0.99, and(THEM(ME),D):0.01}
    - 9.96e-03 -> mono {D:1}   via D (3.31e-03), C (3.31e-03), X (3.12e-03), and(X,X) (8.56e-05)
    - 6.81e-03 -> neutral {D:0.98, and(THEM(ME),D):0.02}   via C (3.31e-03), X (3.12e-03), and(THEM(ME),D) (1.66e-04), and(X,X) (8.56e-05)
    - 3.86e-03 -> neutral {D:0.98, THEM(ME):0.01, and(THEM(ME),D):0.01}   via THEM(ME) (3.86e-03)
    - 1.21e-04 -> neutral {D:0.98, and(THEM(ME),D):0.01, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (1.21e-04)
    - 1.21e-04 -> neutral {D:0.98, and(X,THEM(ME)):0.01, and(THEM(ME),D):0.01}   via and(X,THEM(ME)) (1.21e-04)
    - 3.90e-05 -> neutral {D:0.99, THEM(ME):0.01}   via THEM(ME) (3.90e-05)
- neutral {D:0.93, THEM(ME):0.07}
    - 6.69e-02 -> neutral {D:0.94, THEM(ME):0.06}   via D (2.32e-02), C (2.18e-02), X (2.05e-02), and(X,X) (5.63e-04)
    - 4.73e-02 -> neutral {D:0.92, THEM(ME):0.08}   via C (2.18e-02), X (2.05e-02), THEM(ME) (3.62e-03), and(X,X) (5.63e-04)
    - 1.56e-04 -> neutral {D:0.92, THEM(ME):0.07, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.56e-04)
    - 1.14e-04 -> neutral {D:0.92, THEM(ME):0.07, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (1.14e-04)
    - 1.14e-04 -> neutral {D:0.92, THEM(ME):0.07, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (1.14e-04)
    - 1.18e-05 -> neutral {D:0.93, THEM(ME):0.06, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.18e-05)
- neutral {D:0.99, and(THEM(ME),X):0.01}
    - 9.96e-03 -> mono {D:1}   via D (3.31e-03), C (3.31e-03), X (3.12e-03), and(X,X) (8.56e-05)
    - 6.76e-03 -> neutral {D:0.98, and(THEM(ME),X):0.02}   via C (3.31e-03), X (3.12e-03), and(THEM(ME),X) (1.21e-04), and(X,X) (8.56e-05)
    - 3.86e-03 -> neutral {D:0.98, THEM(ME):0.01, and(THEM(ME),X):0.01}   via THEM(ME) (3.86e-03)
    - 1.66e-04 -> neutral {D:0.98, and(THEM(ME),D):0.01, and(THEM(ME),X):0.01}   via and(THEM(ME),D) (1.66e-04)
    - 1.21e-04 -> neutral {D:0.98, and(X,THEM(ME)):0.01, and(THEM(ME),X):0.01}   via and(X,THEM(ME)) (1.21e-04)
    - 3.90e-05 -> neutral {D:0.99, THEM(ME):0.01}   via THEM(ME) (3.90e-05)
- neutral {D:0.99, and(X,THEM(ME)):0.01}
    - 9.96e-03 -> mono {D:1}   via D (3.31e-03), C (3.31e-03), X (3.12e-03), and(X,X) (8.56e-05)
    - 6.76e-03 -> neutral {D:0.98, and(X,THEM(ME)):0.02}   via C (3.31e-03), X (3.12e-03), and(X,THEM(ME)) (1.21e-04), and(X,X) (8.56e-05)
    - 3.86e-03 -> neutral {D:0.98, THEM(ME):0.01, and(X,THEM(ME)):0.01}   via THEM(ME) (3.86e-03)
    - 1.66e-04 -> neutral {D:0.98, and(X,THEM(ME)):0.01, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.66e-04)
    - 1.21e-04 -> neutral {D:0.98, and(X,THEM(ME)):0.01, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (1.21e-04)
    - 3.90e-05 -> neutral {D:0.99, THEM(ME):0.01}   via THEM(ME) (3.90e-05)
- neutral {D:0.92, THEM(ME):0.08}
    - 7.59e-02 -> neutral {D:0.93, THEM(ME):0.07}   via D (2.65e-02), C (2.46e-02), X (2.32e-02), and(X,X) (6.37e-04)
    - 5.30e-02 -> neutral {D:0.91, THEM(ME):0.09}   via C (2.46e-02), X (2.32e-02), THEM(ME) (3.58e-03), and(X,X) (6.37e-04)
    - 1.55e-04 -> neutral {D:0.91, THEM(ME):0.08, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.55e-04)
    - 1.13e-04 -> neutral {D:0.91, THEM(ME):0.08, and(THEM(ME),X):0.01}   via and(THEM(ME),X) (1.13e-04)
    - 1.13e-04 -> neutral {D:0.91, THEM(ME):0.08, and(X,THEM(ME)):0.01}   via and(X,THEM(ME)) (1.13e-04)
    - 1.35e-05 -> neutral {D:0.92, THEM(ME):0.07, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.35e-05)
