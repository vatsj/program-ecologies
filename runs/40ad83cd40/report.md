### arm=weak, n=6, game=dollar, N=100, w=1.0, x_on=True, role=False, mode=square

programs 1852, classes 46, states 153, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 1.74e-07
mean payoff 0.5000, efficient 0.5000, deadweight loss 0.0000, mean bits in support 2.81

| pi | state |
|---|---|
| 0.9682 | mono {C:1} |
| 0.0109 | mono {THEM(ME):1} |
| 0.0108 | mono {THEM(THEM):1} |
| 0.0027 | mono {THEM(^C):1} |
| 0.0023 | mono {not(THEM(THEM)):1} |
| 0.0023 | mono {not(THEM(ME)):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 9.10e-06 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-06, rho=1.00e-02 k*=100)
    - 2.29e-06 -> mono {or(THEM(ME),C):1}   via or(THEM(ME),C) (2.29e-06, rho=1.00e-02 k*=100)
    - 8.80e-07 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (8.80e-07, rho=1.00e-02 k*=100)
    - 8.80e-07 -> mono {or(THEM(ME),X):1}   via or(THEM(ME),X) (8.80e-07, rho=1.00e-02 k*=100)
- mono {THEM(ME):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 9.10e-06 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-06, rho=1.00e-02 k*=100)
    - 7.95e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (7.95e-06, rho=1.00e-02 k*=100)
    - 7.95e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.95e-06, rho=1.00e-02 k*=100)
    - 2.29e-06 -> mono {or(THEM(ME),C):1}   via or(THEM(ME),C) (2.29e-06, rho=1.00e-02 k*=100)
- mono {THEM(THEM):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 9.10e-06 -> mono {THEM(^C):1}   via THEM(^C) (9.10e-06, rho=1.00e-02 k*=100)
    - 7.95e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (7.95e-06, rho=1.00e-02 k*=100)
    - 7.95e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.95e-06, rho=1.00e-02 k*=100)
    - 2.29e-06 -> mono {or(THEM(ME),C):1}   via or(THEM(ME),C) (2.29e-06, rho=1.00e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 2.29e-06 -> mono {or(THEM(ME),C):1}   via or(THEM(ME),C) (2.29e-06, rho=1.00e-02 k*=100)
    - 8.80e-07 -> mono {or(THEM(THEM),X):1}   via or(THEM(THEM),X) (8.80e-07, rho=1.00e-02 k*=100)
    - 8.80e-07 -> mono {or(THEM(ME),X):1}   via or(THEM(ME),X) (8.80e-07, rho=1.00e-02 k*=100)
- mono {not(THEM(THEM)):1}
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 7.95e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.95e-06, rho=1.00e-02 k*=100)
    - 2.29e-06 -> mono {or(THEM(ME),C):1}   via or(THEM(ME),C) (2.29e-06, rho=1.00e-02 k*=100)
    - 1.15e-06 -> mono {and(THEM(THEM),D):1}   via and(THEM(THEM),D) (1.15e-06, rho=1.00e-02 k*=100)
    - 1.15e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.15e-06, rho=1.00e-02 k*=100)
- mono {not(THEM(ME)):1}
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 7.95e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (7.95e-06, rho=1.00e-02 k*=100)
    - 2.29e-06 -> mono {or(THEM(ME),C):1}   via or(THEM(ME),C) (2.29e-06, rho=1.00e-02 k*=100)
    - 1.15e-06 -> mono {and(THEM(THEM),D):1}   via and(THEM(THEM),D) (1.15e-06, rho=1.00e-02 k*=100)
    - 1.15e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.15e-06, rho=1.00e-02 k*=100)
