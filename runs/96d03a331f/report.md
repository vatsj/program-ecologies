### arm=weak, n=5, game=bos, N=10, w=0.1, x_on=True, role=True, mode=square

programs 902, classes 54, states 941, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 5.72e-02
mean payoff 1.0300, efficient 1.5000, deadweight loss 0.4700, mean bits in support 3.26

| pi | state |
|---|---|
| 0.2378 | mono {D:1} |
| 0.2378 | mono {C:1} |
| 0.0818 | mono {X:1} |
| 0.0731 | poly {X:0.7, ROLE:0.3} |
| 0.0679 | mono {ROLE:1} |
| 0.0608 | poly {C:0.5, D:0.5} |
| 0.0324 | poly {X:0.6, ROLE:0.4} |
| 0.0263 | poly {C:0.4, D:0.5, X:0.1} |
| 0.0263 | poly {C:0.5, D:0.4, X:0.1} |
| 0.0262 | poly {X:0.5, ROLE:0.4, not(ROLE):0.1} |
| 0.0236 | poly {C:0.2, D:0.2, X:0.1, ROLE:0.4, not(ROLE):0.1} |
| 0.0231 | poly {X:0.1, ROLE:0.6, not(ROLE):0.3} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 4.10e-02 -> poly {C:0.5, D:0.5}   via C (4.10e-02, rho=1.65e-01 k*=5)
    - 1.92e-02 -> mono {X:1}   via X (1.92e-02, rho=8.30e-02 k*=10)
    - 1.61e-02 -> mono {ROLE:1}   via ROLE (1.61e-02, rho=8.47e-02 k*=10)
    - 3.11e-03 -> mono {not(ROLE):1}   via not(ROLE) (3.11e-03, rho=6.54e-02 k*=10)
    - 5.78e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (5.78e-04, rho=9.24e-02 k*=10)
    - 5.25e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (5.25e-04, rho=8.39e-02 k*=10)
- mono {C:1}
    - 4.10e-02 -> poly {C:0.5, D:0.5}   via D (4.10e-02, rho=1.65e-01 k*=5)
    - 1.92e-02 -> mono {X:1}   via X (1.92e-02, rho=8.30e-02 k*=10)
    - 1.61e-02 -> mono {ROLE:1}   via ROLE (1.61e-02, rho=8.47e-02 k*=10)
    - 3.11e-03 -> mono {not(ROLE):1}   via not(ROLE) (3.11e-03, rho=6.54e-02 k*=10)
    - 5.78e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (5.78e-04, rho=9.24e-02 k*=10)
    - 5.25e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (5.25e-04, rho=8.39e-02 k*=10)
- mono {X:1}
    - 6.50e-02 -> poly {X:0.7, ROLE:0.3}   via ROLE (6.50e-02, rho=3.41e-01 k*=3)
    - 2.72e-02 -> mono {D:1}   via D (2.72e-02, rho=1.09e-01 k*=10)
    - 2.72e-02 -> mono {C:1}   via C (2.72e-02, rho=1.09e-01 k*=10)
    - 3.79e-03 -> mono {not(ROLE):1}   via not(ROLE) (3.79e-03, rho=7.97e-02 k*=10)
    - 6.63e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.63e-04, rho=1.06e-01 k*=10)
    - 6.63e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.63e-04, rho=1.06e-01 k*=10)
- poly {X:0.7, ROLE:0.3}
    - 4.75e-02 -> poly {X:0.6, ROLE:0.4}   via not(ROLE) (4.75e-02, rho=1.00e+00 k*=1)
    - 2.67e-02 -> mono {D:1}   via D (2.67e-02, rho=1.07e-01 k*=10)
    - 2.67e-02 -> mono {C:1}   via C (2.67e-02, rho=1.07e-01 k*=10)
    - 7.30e-04 -> poly {ROLE:0.7, THEM(THEM):0.3}   via THEM(THEM) (7.30e-04, rho=3.35e-01 k*=3)
    - 7.30e-04 -> poly {ROLE:0.7, THEM(ME):0.3}   via THEM(ME) (7.30e-04, rho=3.35e-01 k*=3)
    - 6.42e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.42e-04, rho=1.03e-01 k*=10)
- mono {ROLE:1}
    - 3.55e-02 -> poly {X:0.7, ROLE:0.3}   via X (3.55e-02, rho=1.53e-01 k*=7)
    - 2.92e-02 -> mono {D:1}   via D (2.92e-02, rho=1.17e-01 k*=10)
    - 2.92e-02 -> mono {C:1}   via C (2.92e-02, rho=1.17e-01 k*=10)
    - 1.68e-02 -> poly {ROLE:0.7, not(ROLE):0.3}   via not(ROLE) (1.68e-02, rho=3.55e-01 k*=3)
    - 7.73e-04 -> poly {ROLE:0.7, THEM(THEM):0.3}   via THEM(THEM) (7.73e-04, rho=3.55e-01 k*=3)
    - 7.73e-04 -> poly {ROLE:0.7, THEM(ME):0.3}   via THEM(ME) (7.73e-04, rho=3.55e-01 k*=3)
- poly {C:0.5, D:0.5}
    - 1.16e-01 -> poly {C:0.5, D:0.4, X:0.1}   via X (1.16e-01, rho=1.00e+00 k*=1)
    - 1.16e-01 -> poly {C:0.4, D:0.5, X:0.1}   via X (1.16e-01, rho=1.00e+00 k*=1)
    - 2.17e-02 -> poly {C:0.4, D:0.3, ROLE:0.3}   via ROLE (2.17e-02, rho=3.41e-01 k*=3)
    - 2.17e-02 -> poly {C:0.3, D:0.4, ROLE:0.3}   via ROLE (2.17e-02, rho=3.41e-01 k*=3)
    - 2.17e-02 -> poly {C:0.3, D:0.3, ROLE:0.4}   via ROLE (2.17e-02, rho=3.41e-01 k*=3)
    - 9.38e-03 -> mono {D:1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1), and(X,ROLE) (3.15e-03, rho=5.03e-01 k*=2), not(or(X,ROLE)) (1.76e-03, rho=1.00e+00 k*=1), and(X,or(X,ROLE)) (1.46e-04, rho=1.00e+00 k*=1)
- poly {X:0.6, ROLE:0.4}
    - 4.75e-02 -> poly {X:0.5, ROLE:0.4, not(ROLE):0.1}   via not(ROLE) (4.75e-02, rho=1.00e+00 k*=1)
    - 2.68e-02 -> mono {D:1}   via D (2.68e-02, rho=1.07e-01 k*=10)
    - 2.68e-02 -> mono {C:1}   via C (2.68e-02, rho=1.07e-01 k*=10)
    - 1.10e-03 -> poly {X:0.7, ROLE:0.3}   via not(THEM(ME)) (4.03e-04, rho=1.00e+00 k*=1), not(THEM(THEM)) (4.03e-04, rho=1.00e+00 k*=1), not(THEM(^C)) (3.64e-05, rho=1.00e+00 k*=1), not(THEM(^D)) (3.64e-05, rho=1.00e+00 k*=1)
    - 7.33e-04 -> poly {ROLE:0.7, THEM(THEM):0.3}   via THEM(THEM) (7.33e-04, rho=3.36e-01 k*=3)
    - 7.33e-04 -> poly {ROLE:0.7, THEM(ME):0.3}   via THEM(ME) (7.33e-04, rho=3.36e-01 k*=3)
- poly {C:0.4, D:0.5, X:0.1}
    - 2.67e-01 -> mono {D:1}   via ROLE (1.90e-01, rho=1.00e+00 k*=1), not(ROLE) (4.75e-02, rho=1.00e+00 k*=1), and(X,ROLE) (6.26e-03, rho=1.00e+00 k*=1), or(X,ROLE) (6.26e-03, rho=1.00e+00 k*=1)
    - 5.07e-05 -> mono {THEM(^D):1}   via THEM(^D) (5.07e-05, rho=2.19e-01 k*=5)
    - 5.07e-05 -> mono {THEM(^C):1}   via THEM(^C) (5.07e-05, rho=2.19e-01 k*=5)
    - 3.24e-05 -> mono {C:1}   via or(THEM(ME),ROLE) (1.26e-05, rho=3.44e-01 k*=3), or(THEM(THEM),ROLE) (1.26e-05, rho=3.44e-01 k*=3), or(ROLE,THEM(ME)) (2.56e-06, rho=1.84e-01 k*=6), or(ROLE,THEM(THEM)) (2.56e-06, rho=1.84e-01 k*=6)
    - 4.13e-06 -> mono {or(ROLE,THEM(THEM)):1}   via or(ROLE,THEM(THEM)) (4.13e-06, rho=1.84e-01 k*=6)
    - 4.13e-06 -> mono {or(ROLE,THEM(ME)):1}   via or(ROLE,THEM(ME)) (4.13e-06, rho=1.84e-01 k*=6)
- poly {C:0.5, D:0.4, X:0.1}
    - 2.67e-01 -> mono {C:1}   via ROLE (1.90e-01, rho=1.00e+00 k*=1), not(ROLE) (4.75e-02, rho=1.00e+00 k*=1), and(X,ROLE) (6.26e-03, rho=1.00e+00 k*=1), or(X,ROLE) (6.26e-03, rho=1.00e+00 k*=1)
    - 5.07e-05 -> mono {THEM(^D):1}   via THEM(^D) (5.07e-05, rho=2.19e-01 k*=5)
    - 5.07e-05 -> mono {THEM(^C):1}   via THEM(^C) (5.07e-05, rho=2.19e-01 k*=5)
    - 3.24e-05 -> mono {D:1}   via and(THEM(ME),ROLE) (1.26e-05, rho=3.44e-01 k*=3), and(THEM(THEM),ROLE) (1.26e-05, rho=3.44e-01 k*=3), and(ROLE,THEM(ME)) (2.56e-06, rho=1.84e-01 k*=6), and(ROLE,THEM(THEM)) (2.56e-06, rho=1.84e-01 k*=6)
    - 4.13e-06 -> mono {and(ROLE,THEM(THEM)):1}   via and(ROLE,THEM(THEM)) (4.13e-06, rho=1.84e-01 k*=6)
    - 4.13e-06 -> mono {and(ROLE,THEM(ME)):1}   via and(ROLE,THEM(ME)) (4.13e-06, rho=1.84e-01 k*=6)
- poly {X:0.5, ROLE:0.4, not(ROLE):0.1}
    - 2.67e-02 -> mono {D:1}   via D (2.67e-02, rho=1.07e-01 k*=10)
    - 2.67e-02 -> mono {C:1}   via C (2.67e-02, rho=1.07e-01 k*=10)
    - 7.38e-04 -> poly {ROLE:0.6, not(ROLE):0.1, THEM(THEM):0.3}   via THEM(THEM) (7.38e-04, rho=3.39e-01 k*=3)
    - 7.38e-04 -> poly {ROLE:0.6, not(ROLE):0.1, THEM(ME):0.3}   via THEM(ME) (7.38e-04, rho=3.39e-01 k*=3)
    - 6.42e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.42e-04, rho=1.03e-01 k*=10)
    - 6.42e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.42e-04, rho=1.03e-01 k*=10)
- poly {C:0.2, D:0.2, X:0.1, ROLE:0.4, not(ROLE):0.1}
    - 1.25e-02 -> mono {D:1}   via and(X,ROLE) (6.26e-03, rho=1.00e+00 k*=1), and(X,X) (3.86e-03, rho=1.00e+00 k*=1), not(or(X,ROLE)) (1.76e-03, rho=1.00e+00 k*=1), and(X,or(X,ROLE)) (1.46e-04, rho=1.00e+00 k*=1)
    - 1.25e-02 -> mono {C:1}   via or(X,ROLE) (6.26e-03, rho=1.00e+00 k*=1), or(X,X) (3.86e-03, rho=1.00e+00 k*=1), not(and(X,ROLE)) (1.76e-03, rho=1.00e+00 k*=1), or(X,and(X,ROLE)) (1.46e-04, rho=1.00e+00 k*=1)
    - 7.54e-04 -> poly {C:0.1, D:0.1, ROLE:0.5, THEM(THEM):0.3}   via THEM(THEM) (7.54e-04, rho=3.46e-01 k*=3)
    - 7.54e-04 -> poly {C:0.1, D:0.1, ROLE:0.5, THEM(ME):0.3}   via THEM(ME) (7.54e-04, rho=3.46e-01 k*=3)
    - 1.39e-04 -> poly {C:0.1, D:0.1, ROLE:0.5, THEM(^ROLE):0.3}   via THEM(^ROLE) (1.39e-04, rho=3.46e-01 k*=3)
    - 6.92e-05 -> poly {ROLE:0.3, THEM(^D):0.7}   via THEM(^D) (6.92e-05, rho=1.58e-01 k*=7)
- poly {X:0.1, ROLE:0.6, not(ROLE):0.3}
    - 2.67e-02 -> mono {D:1}   via D (2.67e-02, rho=1.07e-01 k*=10)
    - 2.67e-02 -> mono {C:1}   via C (2.67e-02, rho=1.07e-01 k*=10)
    - 7.54e-04 -> poly {ROLE:0.6, not(ROLE):0.1, THEM(THEM):0.3}   via THEM(THEM) (7.54e-04, rho=3.46e-01 k*=3)
    - 7.54e-04 -> poly {ROLE:0.6, not(ROLE):0.1, THEM(ME):0.3}   via THEM(ME) (7.54e-04, rho=3.46e-01 k*=3)
    - 6.42e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.42e-04, rho=1.03e-01 k*=10)
    - 6.42e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.42e-04, rho=1.03e-01 k*=10)
