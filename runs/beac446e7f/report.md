### arm=strong, n=6, game=stag, N=1000, x_on=True, role=False, mode=square

programs 1726, classes 21, states 43063, terminal classes 7, indeterminate 0, divergence rate 0.0004
mean payoff 1.3132, efficient 4.0000, deadweight loss 2.6868, mean bits in support 0.85
absorption: class 0: 0.000, class 1: 0.318, class 3: 0.000, class 6: 0.010, class 10: 0.000, class 11: 0.000, class 12: 0.000

| pi | state |
|---|---|
| 0.2724 | mono {C:1} |
| 0.0254 | neutral {C:0.999, or(X,THEM(ME)):0.001} |
| 0.0100 | poly {C:0.999, THEM(ME):9.94e-09, or(X,THEM(ME)):0.001} |
| 0.0097 | neutral {C:0.998, or(X,THEM(ME)):0.002} |
| 0.0046 | neutral {C:0.997, or(X,THEM(ME)):0.003} |
| 0.0024 | neutral {C:0.996, or(X,THEM(ME)):0.004} |
| 0.0013 | neutral {C:0.995, or(X,THEM(ME)):0.005} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 9.32e-05 -> neutral {C:0.999, or(X,THEM(ME)):0.001}   via or(X,THEM(ME)) (9.32e-05)
- neutral {C:0.999, or(X,THEM(ME)):0.001}
    - 1.00e-03 -> mono {C:1}   via C (3.32e-04), D (3.32e-04), X (3.14e-04), and(X,X) (7.98e-06)
    - 7.61e-04 -> neutral {C:0.998, or(X,THEM(ME)):0.002}   via D (3.32e-04), X (3.14e-04), or(X,THEM(ME)) (9.31e-05), and(X,X) (7.98e-06)
- poly {C:0.999, THEM(ME):9.94e-09, or(X,THEM(ME)):0.001}: absorbing (no exits)
- neutral {C:0.998, or(X,THEM(ME)):0.002}
    - 2.00e-03 -> neutral {C:0.999, or(X,THEM(ME)):0.001}   via C (6.63e-04), D (6.62e-04), X (6.28e-04), and(X,X) (1.59e-05)
    - 1.43e-03 -> neutral {C:0.997, or(X,THEM(ME)):0.003}   via D (6.62e-04), X (6.28e-04), or(X,THEM(ME)) (9.30e-05), and(X,X) (1.59e-05)
- neutral {C:0.997, or(X,THEM(ME)):0.003}
    - 3.00e-03 -> neutral {C:0.998, or(X,THEM(ME)):0.002}   via C (9.95e-04), D (9.93e-04), X (9.41e-04), and(X,X) (2.39e-05)
    - 2.09e-03 -> neutral {C:0.996, or(X,THEM(ME)):0.004}   via D (9.93e-04), X (9.41e-04), or(X,THEM(ME)) (9.29e-05), and(X,X) (2.39e-05)
- neutral {C:0.996, or(X,THEM(ME)):0.004}
    - 3.99e-03 -> neutral {C:0.997, or(X,THEM(ME)):0.003}   via C (1.33e-03), D (1.32e-03), X (1.25e-03), and(X,X) (3.18e-05)
    - 2.76e-03 -> neutral {C:0.995, or(X,THEM(ME)):0.005}   via D (1.32e-03), X (1.25e-03), or(X,THEM(ME)) (9.28e-05), and(X,X) (3.18e-05)
- neutral {C:0.995, or(X,THEM(ME)):0.005}
    - 4.99e-03 -> neutral {C:0.996, or(X,THEM(ME)):0.004}   via C (1.66e-03), D (1.65e-03), X (1.57e-03), and(X,X) (3.97e-05)
    - 3.42e-03 -> neutral {C:0.994, or(X,THEM(ME)):0.006}   via D (1.65e-03), X (1.57e-03), or(X,THEM(ME)) (9.27e-05), and(X,X) (3.97e-05)
