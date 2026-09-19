### arm=strong, n=6, game=stag, N=100, x_on=True, role=False, mode=square

programs 1726, classes 21, states 1771, terminal classes 4, indeterminate 0, divergence rate 0.0004
mean payoff 1.3534, efficient 4.0000, deadweight loss 2.6466, mean bits in support 0.88
absorption: class 0: 0.334, class 2: 0.004, class 15: 0.000, class 18: 0.000

| pi | state |
|---|---|
| 0.3291 | mono {C:1} |
| 0.0041 | poly {C:0.99, THEM(ME):9.94e-09, or(X,THEM(ME)):0.01} |
| 0.0031 | neutral {C:0.99, or(X,THEM(ME)):0.01} |
| 0.0010 | neutral {C:0.98, or(X,THEM(ME)):0.02} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 9.32e-05 -> neutral {C:0.99, or(X,THEM(ME)):0.01}   via or(X,THEM(ME)) (9.32e-05)
- poly {C:0.99, THEM(ME):9.94e-09, or(X,THEM(ME)):0.01}: absorbing (no exits)
- neutral {C:0.99, or(X,THEM(ME)):0.01}
    - 1.00e-02 -> mono {C:1}   via C (3.32e-03), D (3.32e-03), X (3.14e-03), and(X,X) (7.98e-05)
    - 6.78e-03 -> neutral {C:0.98, or(X,THEM(ME)):0.02}   via D (3.32e-03), X (3.14e-03), or(X,THEM(ME)) (9.23e-05), and(X,X) (7.98e-05)
- neutral {C:0.98, or(X,THEM(ME)):0.02}
    - 1.99e-02 -> neutral {C:0.99, or(X,THEM(ME)):0.01}   via C (6.63e-03), D (6.56e-03), X (6.22e-03), and(X,X) (1.58e-04)
    - 1.33e-02 -> neutral {C:0.97, or(X,THEM(ME)):0.03}   via D (6.56e-03), X (6.22e-03), and(X,X) (1.58e-04), or(X,X) (1.58e-04)
