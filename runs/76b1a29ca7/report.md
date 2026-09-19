### arm=weak, n=6, game=pd, N=100, x_on=True, role=False, mode=square

programs 1852, classes 48, states 46503, terminal classes 1, indeterminate 125, divergence rate 0.0019
mean payoff -0.7237, efficient 0.0000, deadweight loss 0.7237, mean bits in support 4.42

| pi | state |
|---|---|
| 0.2182 | mono {D:1} |
| 0.0592 | neutral {D:0.99, THEM(ME):0.01} |
| 0.0592 | neutral {D:0.99, THEM(THEM):0.01} |
| 0.0258 | neutral {C:0.45, THEM(^C):0.55} |
| 0.0254 | neutral {C:0.46, THEM(^C):0.54} |
| 0.0254 | neutral {D:0.98, THEM(THEM):0.02} |
| 0.0252 | neutral {D:0.98, THEM(ME):0.02} |
| 0.0244 | neutral {C:0.47, THEM(^C):0.53} |
| 0.0224 | neutral {C:0.48, THEM(^C):0.52} |
| 0.0202 | neutral {C:0.44, THEM(^C):0.56} |
| 0.0185 | neutral {D:0.99, THEM(^D):0.01} |
| 0.0180 | neutral {D:0.98, THEM(ME):0.01, THEM(THEM):0.01} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.68e-03 -> neutral {D:0.99, THEM(ME):0.01}   via THEM(ME) (3.68e-03)
    - 3.67e-03 -> neutral {D:0.99, THEM(THEM):0.01}   via THEM(THEM) (3.67e-03)
    - 9.10e-04 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-04)
    - 9.10e-04 -> neutral {D:0.99, THEM(^D):0.01}   via THEM(^D) (9.10e-04)
    - 8.83e-04 -> mono {THEM(^X):1}   via THEM(^X) (8.83e-04)
    - 1.15e-04 -> neutral {D:0.99, and(THEM(THEM),D):0.01}   via and(THEM(THEM),D) (1.15e-04)
- neutral {D:0.99, THEM(ME):0.01}
    - 1.02e-02 -> neutral {D:0.98, THEM(ME):0.02}   via THEM(ME) (3.64e-03), C (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 9.89e-03 -> mono {D:1}   via D (3.29e-03), C (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 3.63e-03 -> neutral {D:0.98, THEM(ME):0.01, THEM(THEM):0.01}   via THEM(THEM) (3.63e-03)
    - 9.01e-04 -> poly {THEM(ME):2.17e-19, THEM(^C):1}   via THEM(^C) (9.01e-04)
    - 9.01e-04 -> neutral {D:0.98, THEM(ME):0.01, THEM(^D):0.01}   via THEM(^D) (9.01e-04)
    - 8.75e-04 -> poly {THEM(ME):1.99e-08, THEM(^X):1}   via THEM(^X) (8.75e-04)
- neutral {D:0.99, THEM(THEM):0.01}
    - 1.02e-02 -> neutral {D:0.98, THEM(THEM):0.02}   via THEM(THEM) (3.63e-03), C (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 9.89e-03 -> mono {D:1}   via D (3.29e-03), C (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 3.64e-03 -> neutral {D:0.98, THEM(ME):0.01, THEM(THEM):0.01}   via THEM(ME) (3.64e-03)
    - 9.01e-04 -> poly {THEM(THEM):2.17e-19, THEM(^C):1}   via THEM(^C) (9.01e-04)
    - 9.01e-04 -> neutral {D:0.98, THEM(THEM):0.01, THEM(^D):0.01}   via THEM(^D) (9.01e-04)
    - 8.75e-04 -> poly {THEM(THEM):1.99e-08, THEM(^X):1}   via THEM(^X) (8.75e-04)
- neutral {C:0.45, THEM(^C):0.55}
    - 3.48e-01 -> neutral {C:0.46, THEM(^C):0.54}   via C (1.81e-01), D (8.22e-02), X (7.81e-02), and(X,X) (1.89e-03)
    - 1.67e-01 -> neutral {C:0.44, THEM(^C):0.56}   via D (8.22e-02), X (7.81e-02), and(X,X) (1.89e-03), or(X,X) (1.89e-03)
    - 9.10e-04 -> poly {C:1, THEM(^C):4.1e-20, THEM(^D):2.17e-19}   via THEM(^D) (9.10e-04)
    - 8.83e-04 -> poly {C:1, THEM(^X):1.99e-08}   via THEM(^X) (8.83e-04)
    - 4.84e-05 -> poly {C:0.00363, THEM(^C):0.00727, and(THEM(ME),X):0.989}   via and(THEM(ME),X) (4.84e-05)
    - 4.84e-05 -> neutral {C:0.45, THEM(^C):0.54, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (4.84e-05)
- neutral {C:0.46, THEM(^C):0.54}
    - 3.45e-01 -> neutral {C:0.47, THEM(^C):0.53}   via C (1.78e-01), D (8.25e-02), X (7.84e-02), and(X,X) (1.89e-03)
    - 1.68e-01 -> neutral {C:0.45, THEM(^C):0.55}   via D (8.25e-02), X (7.84e-02), and(X,X) (1.89e-03), or(X,X) (1.89e-03)
    - 9.10e-04 -> poly {C:1, THEM(^C):4.1e-20, THEM(^D):2.17e-19}   via THEM(^D) (9.10e-04)
    - 8.83e-04 -> poly {C:1, THEM(^X):1.99e-08}   via THEM(^X) (8.83e-04)
    - 4.75e-05 -> poly {C:0.0034, THEM(^C):0.0068, and(THEM(ME),X):0.99}   via and(THEM(ME),X) (4.75e-05)
    - 4.75e-05 -> neutral {C:0.46, THEM(^C):0.53, or(X,THEM(THEM)):0.01}   via or(X,THEM(THEM)) (4.75e-05)
- neutral {D:0.98, THEM(THEM):0.02}
    - 1.97e-02 -> neutral {D:0.99, THEM(THEM):0.01}   via D (6.58e-03), C (6.51e-03), X (6.19e-03), and(X,X) (1.49e-04)
    - 1.67e-02 -> neutral {D:0.97, THEM(THEM):0.03}   via C (6.51e-03), X (6.19e-03), THEM(THEM) (3.59e-03), and(X,X) (1.49e-04)
    - 3.61e-03 -> neutral {D:0.97, THEM(ME):0.01, THEM(THEM):0.02}   via THEM(ME) (3.61e-03)
    - 9.10e-04 -> poly {THEM(THEM):2.17e-19, THEM(^C):1}   via THEM(^C) (9.10e-04)
    - 8.92e-04 -> neutral {D:0.97, THEM(THEM):0.02, THEM(^D):0.01}   via THEM(^D) (8.92e-04)
    - 8.66e-04 -> poly {THEM(THEM):9.24e-17, THEM(^X):1}   via THEM(^X) (8.66e-04)
- neutral {D:0.98, THEM(ME):0.02}
    - 1.97e-02 -> neutral {D:0.99, THEM(ME):0.01}   via D (6.58e-03), C (6.51e-03), X (6.19e-03), and(X,X) (1.49e-04)
    - 1.67e-02 -> neutral {D:0.97, THEM(ME):0.03}   via C (6.51e-03), X (6.19e-03), THEM(ME) (3.61e-03), and(X,X) (1.49e-04)
    - 3.59e-03 -> neutral {D:0.97, THEM(ME):0.02, THEM(THEM):0.01}   via THEM(THEM) (3.59e-03)
    - 9.10e-04 -> poly {THEM(ME):2.17e-19, THEM(^C):1}   via THEM(^C) (9.10e-04)
    - 8.92e-04 -> neutral {D:0.97, THEM(ME):0.02, THEM(^D):0.01}   via THEM(^D) (8.92e-04)
    - 8.66e-04 -> poly {THEM(ME):9.24e-17, THEM(^X):1}   via THEM(^X) (8.66e-04)
- neutral {C:0.47, THEM(^C):0.53}
    - 3.42e-01 -> neutral {C:0.48, THEM(^C):0.52}   via C (1.74e-01), D (8.28e-02), X (7.86e-02), and(X,X) (1.90e-03)
    - 1.68e-01 -> neutral {C:0.46, THEM(^C):0.54}   via D (8.28e-02), X (7.86e-02), and(X,X) (1.90e-03), or(X,X) (1.90e-03)
    - 8.83e-04 -> poly {C:1, THEM(^X):1.99e-08}   via THEM(^X) (8.83e-04)
    - 4.82e-04 -> poly {C:1, THEM(^D):9.98e-09}   via THEM(^D) (4.82e-04)
    - 4.28e-04 -> poly {C:1, THEM(^C):4.1e-20, THEM(^D):2.17e-19}   via THEM(^D) (4.28e-04)
    - 4.66e-05 -> poly {C:0.00313, THEM(^C):0.00627, and(THEM(ME),X):0.991}   via and(THEM(ME),X) (4.66e-05)
- neutral {C:0.48, THEM(^C):0.52}
    - 3.39e-01 -> neutral {C:0.49, THEM(^C):0.51}   via C (1.71e-01), D (8.29e-02), X (7.88e-02), and(X,X) (1.90e-03)
    - 1.69e-01 -> neutral {C:0.47, THEM(^C):0.53}   via D (8.29e-02), X (7.88e-02), and(X,X) (1.90e-03), or(X,X) (1.90e-03)
    - 8.83e-04 -> poly {C:1, THEM(^X):1.99e-08}   via THEM(^X) (8.83e-04)
    - 4.73e-04 -> poly {C:1, THEM(^C):4.1e-20, THEM(^D):2.17e-19}   via THEM(^D) (4.73e-04)
    - 4.37e-04 -> poly {C:1, THEM(^D):9.98e-09}   via THEM(^D) (4.37e-04)
    - 4.58e-05 -> poly {C:0.00297, THEM(^C):0.00593, and(THEM(ME),X):0.991}   via and(THEM(ME),X) (4.58e-05)
- neutral {C:0.44, THEM(^C):0.56}
    - 3.50e-01 -> neutral {C:0.45, THEM(^C):0.55}   via C (1.84e-01), D (8.19e-02), X (7.78e-02), and(X,X) (1.88e-03)
    - 1.67e-01 -> neutral {C:0.43, THEM(^C):0.57}   via D (8.19e-02), X (7.78e-02), and(X,X) (1.88e-03), or(X,X) (1.88e-03)
    - 8.83e-04 -> poly {C:1, THEM(^X):1.99e-08}   via THEM(^X) (8.83e-04)
    - 5.10e-04 -> poly {C:1, THEM(^C):4.1e-20, THEM(^D):2.17e-19}   via THEM(^D) (5.10e-04)
    - 4.00e-04 -> poly {C:1, THEM(^D):9.98e-09}   via THEM(^D) (4.00e-04)
    - 4.93e-05 -> poly {C:0.00396, THEM(^C):0.00792, and(THEM(ME),X):0.988}   via and(THEM(ME),X) (4.93e-05)
- neutral {D:0.99, THEM(^D):0.01}
    - 9.89e-03 -> mono {D:1}   via D (3.29e-03), C (3.29e-03), X (3.12e-03), and(X,X) (7.54e-05)
    - 7.52e-03 -> neutral {D:0.98, THEM(^D):0.02}   via C (3.29e-03), X (3.12e-03), THEM(^D) (9.01e-04), and(X,X) (7.54e-05)
    - 3.64e-03 -> neutral {D:0.98, THEM(ME):0.01, THEM(^D):0.01}   via THEM(ME) (3.64e-03)
    - 3.63e-03 -> neutral {D:0.98, THEM(THEM):0.01, THEM(^D):0.01}   via THEM(THEM) (3.63e-03)
    - 1.13e-04 -> neutral {D:0.98, THEM(^D):0.01, and(THEM(THEM),D):0.01}   via and(THEM(THEM),D) (1.13e-04)
    - 1.13e-04 -> neutral {D:0.98, THEM(^D):0.01, and(THEM(ME),D):0.01}   via and(THEM(ME),D) (1.13e-04)
- neutral {D:0.98, THEM(ME):0.01, THEM(THEM):0.01}
    - 1.01e-02 -> neutral {D:0.97, THEM(ME):0.02, THEM(THEM):0.01}   via THEM(ME) (3.61e-03), C (3.26e-03), X (3.09e-03), and(X,X) (7.47e-05)
    - 1.01e-02 -> neutral {D:0.97, THEM(ME):0.01, THEM(THEM):0.02}   via THEM(THEM) (3.59e-03), C (3.26e-03), X (3.09e-03), and(X,X) (7.47e-05)
    - 9.83e-03 -> neutral {D:0.99, THEM(THEM):0.01}   via D (3.29e-03), C (3.26e-03), X (3.09e-03), and(X,X) (7.47e-05)
    - 9.83e-03 -> neutral {D:0.99, THEM(ME):0.01}   via D (3.29e-03), C (3.26e-03), X (3.09e-03), and(X,X) (7.47e-05)
    - 8.92e-04 -> poly {THEM(ME):3.25e-19, THEM(THEM):3.79e-19, THEM(^C):1}   via THEM(^C) (8.92e-04)
    - 8.92e-04 -> neutral {D:0.97, THEM(ME):0.01, THEM(THEM):0.01, THEM(^D):0.01}   via THEM(^D) (8.92e-04)

INDETERMINATE transitions (replicator did not converge): 125; first: from poly {X:0.364, THEM(THEM):0.273, and(X,THEM(^X)):0.364} with mutant THEM(^and(X,X))
