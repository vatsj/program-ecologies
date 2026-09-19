### arm=weak, n=5, game=demand, N=100, x_on=True, role=True, mode=square

programs 902, classes 53, states 23935, terminal classes 2, indeterminate 0, divergence rate 0.0010
mean payoff 0.5000, efficient 0.5000, deadweight loss 0.0000, mean bits in support 3.00
absorption: class 0: 0.000, class 1: 1.000

| pi | state |
|---|---|
| 0.9924 | mono {ROLE:1} |
| 0.0036 | neutral {ROLE:0.99, not(THEM(^ROLE)):0.01} |
| 0.0015 | neutral {ROLE:0.98, not(THEM(^ROLE)):0.02} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 3.64e-05 -> neutral {ROLE:0.99, not(THEM(^ROLE)):0.01}   via not(THEM(^ROLE)) (3.64e-05)
- neutral {ROLE:0.99, not(THEM(^ROLE)):0.01}
    - 1.00e-02 -> mono {ROLE:1}   via C (2.49e-03), D (2.49e-03), X (2.31e-03), ROLE (1.90e-03)
    - 8.13e-03 -> neutral {ROLE:0.98, not(THEM(^ROLE)):0.02}   via C (2.49e-03), D (2.49e-03), X (2.31e-03), not(ROLE) (4.75e-04)
- neutral {ROLE:0.98, not(THEM(^ROLE)):0.02}
    - 1.98e-02 -> neutral {ROLE:0.99, not(THEM(^ROLE)):0.01}   via C (4.93e-03), D (4.93e-03), X (4.58e-03), ROLE (3.81e-03)
    - 1.61e-02 -> neutral {ROLE:0.97, not(THEM(^ROLE)):0.03}   via C (4.93e-03), D (4.93e-03), X (4.58e-03), not(ROLE) (9.40e-04)
