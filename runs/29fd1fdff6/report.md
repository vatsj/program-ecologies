### arm=weak, n=5, game=bos, N=10, w=0.01, x_on=True, role=True, mode=square

programs 902, classes 54, states 941, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 6.04e-02
mean payoff 0.9682, efficient 1.5000, deadweight loss 0.5318, mean bits in support 3.30

| pi | state |
|---|---|
| 0.2081 | mono {D:1} |
| 0.2081 | mono {C:1} |
| 0.0894 | mono {X:1} |
| 0.0804 | poly {X:0.7, ROLE:0.3} |
| 0.0765 | mono {ROLE:1} |
| 0.0634 | poly {C:0.5, D:0.5} |
| 0.0368 | poly {X:0.6, ROLE:0.4} |
| 0.0316 | poly {X:0.5, ROLE:0.4, not(ROLE):0.1} |
| 0.0283 | poly {X:0.1, ROLE:0.6, not(ROLE):0.3} |
| 0.0275 | poly {C:0.4, D:0.5, X:0.1} |
| 0.0275 | poly {C:0.5, D:0.4, X:0.1} |
| 0.0253 | mono {not(ROLE):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 4.88e-02 -> poly {C:0.5, D:0.5}   via C (4.88e-02, rho=1.96e-01 k*=5)
    - 2.27e-02 -> mono {X:1}   via X (2.27e-02, rho=9.80e-02 k*=10)
    - 1.87e-02 -> mono {ROLE:1}   via ROLE (1.87e-02, rho=9.83e-02 k*=10)
    - 4.55e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.55e-03, rho=9.58e-02 k*=10)
    - 6.20e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.20e-04, rho=9.91e-02 k*=10)
    - 6.14e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.14e-04, rho=9.82e-02 k*=10)
- mono {C:1}
    - 4.88e-02 -> poly {C:0.5, D:0.5}   via D (4.88e-02, rho=1.96e-01 k*=5)
    - 2.27e-02 -> mono {X:1}   via X (2.27e-02, rho=9.80e-02 k*=10)
    - 1.87e-02 -> mono {ROLE:1}   via ROLE (1.87e-02, rho=9.83e-02 k*=10)
    - 4.55e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.55e-03, rho=9.58e-02 k*=10)
    - 6.20e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.20e-04, rho=9.91e-02 k*=10)
    - 6.14e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.14e-04, rho=9.82e-02 k*=10)
- mono {X:1}
    - 6.36e-02 -> poly {X:0.7, ROLE:0.3}   via ROLE (6.36e-02, rho=3.34e-01 k*=3)
    - 2.51e-02 -> mono {D:1}   via D (2.51e-02, rho=1.01e-01 k*=10)
    - 2.51e-02 -> mono {C:1}   via C (2.51e-02, rho=1.01e-01 k*=10)
    - 4.64e-03 -> mono {not(ROLE):1}   via not(ROLE) (4.64e-03, rho=9.78e-02 k*=10)
    - 6.30e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.30e-04, rho=1.01e-01 k*=10)
    - 6.30e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.30e-04, rho=1.01e-01 k*=10)
- poly {X:0.7, ROLE:0.3}
    - 4.75e-02 -> poly {X:0.6, ROLE:0.4}   via not(ROLE) (4.75e-02, rho=1.00e+00 k*=1)
    - 2.51e-02 -> mono {D:1}   via D (2.51e-02, rho=1.01e-01 k*=10)
    - 2.51e-02 -> mono {C:1}   via C (2.51e-02, rho=1.01e-01 k*=10)
    - 7.27e-04 -> poly {ROLE:0.7, THEM(THEM):0.3}   via THEM(THEM) (7.27e-04, rho=3.33e-01 k*=3)
    - 7.27e-04 -> poly {ROLE:0.7, THEM(ME):0.3}   via THEM(ME) (7.27e-04, rho=3.33e-01 k*=3)
    - 6.28e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.28e-04, rho=1.00e-01 k*=10)
- mono {ROLE:1}
    - 3.33e-02 -> poly {X:0.7, ROLE:0.3}   via X (3.33e-02, rho=1.44e-01 k*=7)
    - 2.53e-02 -> mono {D:1}   via D (2.53e-02, rho=1.02e-01 k*=10)
    - 2.53e-02 -> mono {C:1}   via C (2.53e-02, rho=1.02e-01 k*=10)
    - 1.59e-02 -> poly {ROLE:0.7, not(ROLE):0.3}   via not(ROLE) (1.59e-02, rho=3.36e-01 k*=3)
    - 7.31e-04 -> poly {ROLE:0.7, THEM(THEM):0.3}   via THEM(THEM) (7.31e-04, rho=3.36e-01 k*=3)
    - 7.31e-04 -> poly {ROLE:0.7, THEM(ME):0.3}   via THEM(ME) (7.31e-04, rho=3.36e-01 k*=3)
- poly {C:0.5, D:0.5}
    - 1.16e-01 -> poly {C:0.5, D:0.4, X:0.1}   via X (1.16e-01, rho=1.00e+00 k*=1)
    - 1.16e-01 -> poly {C:0.4, D:0.5, X:0.1}   via X (1.16e-01, rho=1.00e+00 k*=1)
    - 2.12e-02 -> poly {C:0.4, D:0.3, ROLE:0.3}   via ROLE (2.12e-02, rho=3.34e-01 k*=3)
    - 2.12e-02 -> poly {C:0.3, D:0.4, ROLE:0.3}   via ROLE (2.12e-02, rho=3.34e-01 k*=3)
    - 2.12e-02 -> poly {C:0.3, D:0.3, ROLE:0.4}   via ROLE (2.12e-02, rho=3.34e-01 k*=3)
    - 9.36e-03 -> mono {D:1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1), and(X,ROLE) (3.13e-03, rho=5.00e-01 k*=2), not(or(X,ROLE)) (1.76e-03, rho=1.00e+00 k*=1), and(X,or(X,ROLE)) (1.46e-04, rho=1.00e+00 k*=1)
- poly {X:0.6, ROLE:0.4}
    - 4.75e-02 -> poly {X:0.5, ROLE:0.4, not(ROLE):0.1}   via not(ROLE) (4.75e-02, rho=1.00e+00 k*=1)
    - 2.51e-02 -> mono {D:1}   via D (2.51e-02, rho=1.01e-01 k*=10)
    - 2.51e-02 -> mono {C:1}   via C (2.51e-02, rho=1.01e-01 k*=10)
    - 1.10e-03 -> poly {X:0.7, ROLE:0.3}   via not(THEM(ME)) (4.03e-04, rho=1.00e+00 k*=1), not(THEM(THEM)) (4.03e-04, rho=1.00e+00 k*=1), not(THEM(^C)) (3.64e-05, rho=1.00e+00 k*=1), not(THEM(^D)) (3.64e-05, rho=1.00e+00 k*=1)
    - 7.27e-04 -> poly {ROLE:0.7, THEM(THEM):0.3}   via THEM(THEM) (7.27e-04, rho=3.34e-01 k*=3)
    - 7.27e-04 -> poly {ROLE:0.7, THEM(ME):0.3}   via THEM(ME) (7.27e-04, rho=3.34e-01 k*=3)
- poly {X:0.5, ROLE:0.4, not(ROLE):0.1}
    - 2.51e-02 -> mono {D:1}   via D (2.51e-02, rho=1.01e-01 k*=10)
    - 2.51e-02 -> mono {C:1}   via C (2.51e-02, rho=1.01e-01 k*=10)
    - 7.28e-04 -> poly {ROLE:0.6, not(ROLE):0.1, THEM(THEM):0.3}   via THEM(THEM) (7.28e-04, rho=3.34e-01 k*=3)
    - 7.28e-04 -> poly {ROLE:0.6, not(ROLE):0.1, THEM(ME):0.3}   via THEM(ME) (7.28e-04, rho=3.34e-01 k*=3)
    - 6.28e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.28e-04, rho=1.00e-01 k*=10)
    - 6.28e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.28e-04, rho=1.00e-01 k*=10)
- poly {X:0.1, ROLE:0.6, not(ROLE):0.3}
    - 2.51e-02 -> mono {D:1}   via D (2.51e-02, rho=1.01e-01 k*=10)
    - 2.51e-02 -> mono {C:1}   via C (2.51e-02, rho=1.01e-01 k*=10)
    - 7.30e-04 -> poly {ROLE:0.6, not(ROLE):0.1, THEM(THEM):0.3}   via THEM(THEM) (7.30e-04, rho=3.35e-01 k*=3)
    - 7.30e-04 -> poly {ROLE:0.6, not(ROLE):0.1, THEM(ME):0.3}   via THEM(ME) (7.30e-04, rho=3.35e-01 k*=3)
    - 6.28e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.28e-04, rho=1.00e-01 k*=10)
    - 6.28e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.28e-04, rho=1.00e-01 k*=10)
- poly {C:0.4, D:0.5, X:0.1}
    - 2.67e-01 -> mono {D:1}   via ROLE (1.90e-01, rho=1.00e+00 k*=1), not(ROLE) (4.75e-02, rho=1.00e+00 k*=1), and(X,ROLE) (6.26e-03, rho=1.00e+00 k*=1), or(X,ROLE) (6.26e-03, rho=1.00e+00 k*=1)
    - 4.67e-05 -> mono {THEM(^D):1}   via THEM(^D) (4.67e-05, rho=2.02e-01 k*=5)
    - 4.67e-05 -> mono {THEM(^C):1}   via THEM(^C) (4.67e-05, rho=2.02e-01 k*=5)
    - 3.11e-05 -> mono {C:1}   via or(THEM(ME),ROLE) (1.22e-05, rho=3.35e-01 k*=3), or(THEM(THEM),ROLE) (1.22e-05, rho=3.35e-01 k*=3), or(ROLE,THEM(ME)) (2.35e-06, rho=1.68e-01 k*=6), or(ROLE,THEM(THEM)) (2.35e-06, rho=1.68e-01 k*=6)
    - 3.92e-06 -> mono {and(ROLE,THEM(THEM)):1}   via and(ROLE,THEM(THEM)) (3.92e-06, rho=3.35e-01 k*=3)
    - 3.92e-06 -> mono {and(ROLE,THEM(ME)):1}   via and(ROLE,THEM(ME)) (3.92e-06, rho=3.35e-01 k*=3)
- poly {C:0.5, D:0.4, X:0.1}
    - 2.67e-01 -> mono {C:1}   via ROLE (1.90e-01, rho=1.00e+00 k*=1), not(ROLE) (4.75e-02, rho=1.00e+00 k*=1), and(X,ROLE) (6.26e-03, rho=1.00e+00 k*=1), or(X,ROLE) (6.26e-03, rho=1.00e+00 k*=1)
    - 4.67e-05 -> mono {THEM(^D):1}   via THEM(^D) (4.67e-05, rho=2.02e-01 k*=5)
    - 4.67e-05 -> mono {THEM(^C):1}   via THEM(^C) (4.67e-05, rho=2.02e-01 k*=5)
    - 3.11e-05 -> mono {D:1}   via and(THEM(ME),ROLE) (1.22e-05, rho=3.35e-01 k*=3), and(THEM(THEM),ROLE) (1.22e-05, rho=3.35e-01 k*=3), and(ROLE,THEM(ME)) (2.35e-06, rho=1.68e-01 k*=6), and(ROLE,THEM(THEM)) (2.35e-06, rho=1.68e-01 k*=6)
    - 3.92e-06 -> mono {or(ROLE,THEM(THEM)):1}   via or(ROLE,THEM(THEM)) (3.92e-06, rho=3.35e-01 k*=3)
    - 3.92e-06 -> mono {or(ROLE,THEM(ME)):1}   via or(ROLE,THEM(ME)) (3.92e-06, rho=3.35e-01 k*=3)
- mono {not(ROLE):1}
    - 2.83e-02 -> poly {ROLE:0.7, not(ROLE):0.3}   via ROLE (2.83e-02, rho=1.49e-01 k*=7)
    - 2.60e-02 -> mono {D:1}   via D (2.60e-02, rho=1.04e-01 k*=10)
    - 2.60e-02 -> mono {C:1}   via C (2.60e-02, rho=1.04e-01 k*=10)
    - 2.39e-02 -> mono {X:1}   via X (2.39e-02, rho=1.03e-01 k*=10)
    - 6.53e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.53e-04, rho=1.04e-01 k*=10)
    - 6.53e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.53e-04, rho=1.04e-01 k*=10)
