### arm=strong, n=6, game=pd, N=10, x_on=True, role=False, mode=square

programs 1726, classes 21, states 269, terminal classes 1, indeterminate 0, divergence rate 0.0004
mean payoff -1.0000, efficient 0.0000, deadweight loss 1.0000, mean bits in support 2.65

| pi | state |
|---|---|
| 0.9351 | mono {D:1} |
| 0.0360 | neutral {D:0.9, THEM(ME):0.1} |
| 0.0137 | neutral {D:0.8, THEM(ME):0.2} |
| 0.0065 | neutral {D:0.7, THEM(ME):0.3} |
| 0.0028 | neutral {D:0.6, THEM(ME):0.4} |
| 0.0011 | neutral {D:0.9, and(THEM(ME),D):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.84e-03 -> neutral {D:0.9, THEM(ME):0.1}   via THEM(ME) (3.84e-03)
    - 1.22e-04 -> neutral {D:0.9, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (1.22e-04)
    - 9.32e-05 -> neutral {D:0.9, and(THEM(ME),X):0.1}   via and(THEM(ME),X) (9.32e-05)
    - 9.32e-05 -> neutral {D:0.9, and(X,THEM(ME)):0.1}   via and(X,THEM(ME)) (9.32e-05)
- neutral {D:0.9, THEM(ME):0.1}
    - 9.96e-02 -> mono {D:1}   via D (3.32e-02), C (3.32e-02), X (3.14e-02), and(X,X) (7.98e-04)
    - 6.99e-02 -> neutral {D:0.8, THEM(ME):0.2}   via C (3.32e-02), X (3.14e-02), THEM(ME) (3.45e-03), and(X,X) (7.98e-04)
    - 1.10e-04 -> neutral {D:0.8, THEM(ME):0.1, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (1.10e-04)
    - 8.39e-05 -> neutral {D:0.8, THEM(ME):0.1, and(THEM(ME),X):0.1}   via and(THEM(ME),X) (8.39e-05)
    - 8.39e-05 -> neutral {D:0.8, THEM(ME):0.1, and(X,THEM(ME)):0.1}   via and(X,THEM(ME)) (8.39e-05)
    - 1.22e-05 -> neutral {D:0.9, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (1.22e-05)
- neutral {D:0.8, THEM(ME):0.2}
    - 1.84e-01 -> neutral {D:0.9, THEM(ME):0.1}   via D (6.63e-02), C (5.89e-02), X (5.59e-02), and(X,X) (1.42e-03)
    - 1.21e-01 -> neutral {D:0.7, THEM(ME):0.3}   via C (5.89e-02), X (5.59e-02), THEM(ME) (3.07e-03), and(X,X) (1.42e-03)
    - 9.75e-05 -> neutral {D:0.7, THEM(ME):0.2, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (9.75e-05)
    - 7.46e-05 -> neutral {D:0.7, THEM(ME):0.2, and(THEM(ME),X):0.1}   via and(THEM(ME),X) (7.46e-05)
    - 7.46e-05 -> neutral {D:0.7, THEM(ME):0.2, and(X,THEM(ME)):0.1}   via and(X,THEM(ME)) (7.46e-05)
    - 2.44e-05 -> neutral {D:0.8, THEM(ME):0.1, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (2.44e-05)
- neutral {D:0.7, THEM(ME):0.3}
    - 2.54e-01 -> neutral {D:0.8, THEM(ME):0.2}   via D (9.95e-02), C (7.74e-02), X (7.33e-02), and(X,X) (1.86e-03)
    - 1.58e-01 -> neutral {D:0.6, THEM(ME):0.4}   via C (7.74e-02), X (7.33e-02), THEM(ME) (2.69e-03), and(X,X) (1.86e-03)
    - 8.53e-05 -> neutral {D:0.6, THEM(ME):0.3, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (8.53e-05)
    - 6.52e-05 -> neutral {D:0.6, THEM(ME):0.3, and(THEM(ME),X):0.1}   via and(THEM(ME),X) (6.52e-05)
    - 6.52e-05 -> poly {D:0.6, THEM(ME):0.3, or(X,THEM(ME)):0.1}   via or(X,THEM(ME)) (6.52e-05)
    - 6.52e-05 -> neutral {D:0.6, THEM(ME):0.3, and(X,THEM(ME)):0.1}   via and(X,THEM(ME)) (6.52e-05)
- neutral {D:0.6, THEM(ME):0.4}
    - 3.10e-01 -> neutral {D:0.7, THEM(ME):0.3}   via D (1.33e-01), C (8.84e-02), X (8.38e-02), and(X,X) (2.13e-03)
    - 1.79e-01 -> neutral {D:0.5, THEM(ME):0.5}   via C (8.84e-02), X (8.38e-02), THEM(ME) (2.30e-03), and(X,X) (2.13e-03)
    - 7.31e-05 -> neutral {D:0.5, THEM(ME):0.4, and(THEM(ME),D):0.1}   via and(THEM(ME),D) (7.31e-05)
    - 5.59e-05 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (5.59e-05)
    - 5.59e-05 -> neutral {D:0.5, THEM(ME):0.4, and(THEM(ME),X):0.1}   via and(THEM(ME),X) (5.59e-05)
    - 5.59e-05 -> neutral {D:0.5, THEM(ME):0.4, and(X,THEM(ME)):0.1}   via and(X,THEM(ME)) (5.59e-05)
- neutral {D:0.9, and(THEM(ME),D):0.1}
    - 9.96e-02 -> mono {D:1}   via D (3.32e-02), C (3.32e-02), X (3.14e-02), and(X,X) (7.98e-04)
    - 6.65e-02 -> neutral {D:0.8, and(THEM(ME),D):0.2}   via C (3.32e-02), X (3.14e-02), and(X,X) (7.98e-04), or(X,X) (7.98e-04)
    - 3.45e-03 -> neutral {D:0.8, THEM(ME):0.1, and(THEM(ME),D):0.1}   via THEM(ME) (3.45e-03)
    - 3.84e-04 -> neutral {D:0.9, THEM(ME):0.1}   via THEM(ME) (3.84e-04)
    - 8.39e-05 -> neutral {D:0.8, and(THEM(ME),D):0.1, and(THEM(ME),X):0.1}   via and(THEM(ME),X) (8.39e-05)
    - 8.39e-05 -> neutral {D:0.8, and(X,THEM(ME)):0.1, and(THEM(ME),D):0.1}   via and(X,THEM(ME)) (8.39e-05)
