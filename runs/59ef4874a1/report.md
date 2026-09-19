### arm=weak, n=5, game=bos, N=10, w=1.0, x_on=True, role=True, mode=square

programs 902, classes 54, states 721, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 2.58e-02
mean payoff 1.3224, efficient 1.5000, deadweight loss 0.1776, mean bits in support 3.14

| pi | state |
|---|---|
| 0.4791 | mono {C:1} |
| 0.3111 | mono {D:1} |
| 0.0421 | mono {X:1} |
| 0.0353 | poly {X:0.7, ROLE:0.3} |
| 0.0273 | poly {C:0.5, D:0.5} |
| 0.0236 | poly {C:0.5, D:0.4, X:0.1} |
| 0.0230 | mono {ROLE:1} |
| 0.0135 | poly {X:0.6, ROLE:0.4} |
| 0.0086 | poly {X:0.5, ROLE:0.4, not(ROLE):0.1} |
| 0.0064 | poly {C:0.3, D:0.4, ROLE:0.3} |
| 0.0057 | poly {X:0.1, ROLE:0.6, not(ROLE):0.3} |
| 0.0041 | mono {or(X,ROLE):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {C:1}
    - 1.13e-02 -> poly {C:0.5, D:0.5}   via D (1.13e-02, rho=4.52e-02 k*=5)
    - 7.58e-03 -> mono {X:1}   via X (7.58e-03, rho=3.28e-02 k*=10)
    - 5.97e-03 -> mono {ROLE:1}   via ROLE (5.97e-03, rho=3.14e-02 k*=10)
    - 4.05e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (4.05e-04, rho=6.48e-02 k*=10)
    - 2.11e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (2.11e-04, rho=3.37e-02 k*=10)
    - 2.08e-04 -> mono {or(X,X):1}   via or(X,X) (2.08e-04, rho=5.39e-02 k*=10)
- mono {D:1}
    - 1.13e-02 -> poly {C:0.5, D:0.5}   via C (1.13e-02, rho=4.52e-02 k*=5)
    - 7.58e-03 -> mono {X:1}   via X (7.58e-03, rho=3.28e-02 k*=10)
    - 5.97e-03 -> mono {ROLE:1}   via ROLE (5.97e-03, rho=3.14e-02 k*=10)
    - 4.05e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (4.05e-04, rho=6.48e-02 k*=10)
    - 2.11e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (2.11e-04, rho=3.37e-02 k*=10)
    - 2.08e-04 -> mono {and(X,X):1}   via and(X,X) (2.08e-04, rho=5.39e-02 k*=10)
- mono {X:1}
    - 7.23e-02 -> poly {X:0.7, ROLE:0.3}   via ROLE (7.23e-02, rho=3.80e-01 k*=3)
    - 3.73e-02 -> mono {D:1}   via D (3.73e-02, rho=1.50e-01 k*=10)
    - 3.73e-02 -> mono {C:1}   via C (3.73e-02, rho=1.50e-01 k*=10)
    - 8.69e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (8.69e-04, rho=1.39e-01 k*=10)
    - 8.69e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (8.69e-04, rho=1.39e-01 k*=10)
    - 5.69e-04 -> mono {not(ROLE):1}   via not(ROLE) (5.69e-04, rho=1.20e-02 k*=10)
- poly {X:0.7, ROLE:0.3}
    - 4.75e-02 -> poly {X:0.6, ROLE:0.4}   via not(ROLE) (4.75e-02, rho=1.00e+00 k*=1)
    - 3.48e-02 -> mono {D:1}   via D (3.48e-02, rho=1.40e-01 k*=10)
    - 3.48e-02 -> mono {C:1}   via C (3.48e-02, rho=1.40e-01 k*=10)
    - 7.46e-04 -> poly {ROLE:0.7, THEM(THEM):0.3}   via THEM(THEM) (7.46e-04, rho=3.42e-01 k*=3)
    - 7.46e-04 -> poly {ROLE:0.7, THEM(ME):0.3}   via THEM(ME) (7.46e-04, rho=3.42e-01 k*=3)
    - 7.32e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.32e-04, rho=1.17e-01 k*=10)
- poly {C:0.5, D:0.5}
    - 2.31e-01 -> poly {C:0.5, D:0.4, X:0.1}   via X (2.31e-01, rho=1.00e+00 k*=1)
    - 7.23e-02 -> poly {C:0.3, D:0.4, ROLE:0.3}   via ROLE (7.23e-02, rho=3.80e-01 k*=3)
    - 9.49e-03 -> mono {D:1}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1), and(X,ROLE) (3.25e-03, rho=5.19e-01 k*=2), not(or(X,ROLE)) (1.76e-03, rho=1.00e+00 k*=1), and(X,or(X,ROLE)) (1.46e-04, rho=1.00e+00 k*=1)
    - 9.49e-03 -> mono {C:1}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1), or(X,ROLE) (3.25e-03, rho=5.19e-01 k*=2), not(and(X,ROLE)) (1.76e-03, rho=1.00e+00 k*=1), or(X,and(X,ROLE)) (1.46e-04, rho=1.00e+00 k*=1)
    - 9.33e-04 -> poly {C:0.4, D:0.3, THEM(THEM):0.3}   via THEM(THEM) (9.33e-04, rho=4.28e-01 k*=3)
    - 9.33e-04 -> poly {C:0.4, D:0.3, THEM(ME):0.3}   via THEM(ME) (9.33e-04, rho=4.28e-01 k*=3)
- poly {C:0.5, D:0.4, X:0.1}
    - 2.67e-01 -> mono {C:1}   via ROLE (1.90e-01, rho=1.00e+00 k*=1), not(ROLE) (4.75e-02, rho=1.00e+00 k*=1), and(X,ROLE) (6.26e-03, rho=1.00e+00 k*=1), or(X,ROLE) (6.26e-03, rho=1.00e+00 k*=1)
    - 7.16e-05 -> mono {THEM(^D):1}   via THEM(^D) (7.16e-05, rho=3.10e-01 k*=5)
    - 7.16e-05 -> mono {THEM(^C):1}   via THEM(^C) (7.16e-05, rho=3.10e-01 k*=5)
    - 3.95e-05 -> mono {D:1}   via and(THEM(ME),ROLE) (1.45e-05, rho=3.97e-01 k*=3), and(THEM(THEM),ROLE) (1.45e-05, rho=3.97e-01 k*=3), and(ROLE,THEM(ME)) (3.72e-06, rho=2.67e-01 k*=6), and(ROLE,THEM(THEM)) (3.72e-06, rho=2.67e-01 k*=6)
    - 6.02e-06 -> mono {and(ROLE,THEM(THEM)):1}   via and(ROLE,THEM(THEM)) (6.02e-06, rho=2.67e-01 k*=6)
    - 6.02e-06 -> mono {and(ROLE,THEM(ME)):1}   via and(ROLE,THEM(ME)) (6.02e-06, rho=2.67e-01 k*=6)
- mono {ROLE:1}
    - 6.17e-02 -> mono {D:1}   via D (6.17e-02, rho=2.48e-01 k*=10)
    - 6.17e-02 -> mono {C:1}   via C (6.17e-02, rho=2.48e-01 k*=10)
    - 5.50e-02 -> poly {X:0.7, ROLE:0.3}   via X (5.50e-02, rho=2.38e-01 k*=7)
    - 2.29e-02 -> poly {ROLE:0.7, not(ROLE):0.3}   via not(ROLE) (2.29e-02, rho=4.81e-01 k*=3)
    - 1.14e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.14e-03, rho=1.81e-01 k*=10)
    - 1.14e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.14e-03, rho=1.81e-01 k*=10)
- poly {X:0.6, ROLE:0.4}
    - 4.75e-02 -> poly {X:0.5, ROLE:0.4, not(ROLE):0.1}   via not(ROLE) (4.75e-02, rho=1.00e+00 k*=1)
    - 3.53e-02 -> mono {D:1}   via D (3.53e-02, rho=1.42e-01 k*=10)
    - 3.53e-02 -> mono {C:1}   via C (3.53e-02, rho=1.42e-01 k*=10)
    - 1.10e-03 -> poly {X:0.7, ROLE:0.3}   via not(THEM(ME)) (4.03e-04, rho=1.00e+00 k*=1), not(THEM(THEM)) (4.03e-04, rho=1.00e+00 k*=1), not(THEM(^C)) (3.64e-05, rho=1.00e+00 k*=1), not(THEM(^D)) (3.64e-05, rho=1.00e+00 k*=1)
    - 7.67e-04 -> poly {ROLE:0.7, THEM(THEM):0.3}   via THEM(THEM) (7.67e-04, rho=3.52e-01 k*=3)
    - 7.67e-04 -> poly {ROLE:0.7, THEM(ME):0.3}   via THEM(ME) (7.67e-04, rho=3.52e-01 k*=3)
- poly {X:0.5, ROLE:0.4, not(ROLE):0.1}
    - 3.48e-02 -> mono {D:1}   via D (3.48e-02, rho=1.40e-01 k*=10)
    - 3.48e-02 -> mono {C:1}   via C (3.48e-02, rho=1.40e-01 k*=10)
    - 7.94e-04 -> poly {ROLE:0.6, not(ROLE):0.1, THEM(THEM):0.3}   via THEM(THEM) (7.94e-04, rho=3.64e-01 k*=3)
    - 7.94e-04 -> poly {ROLE:0.6, not(ROLE):0.1, THEM(ME):0.3}   via THEM(ME) (7.94e-04, rho=3.64e-01 k*=3)
    - 7.32e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.32e-04, rho=1.17e-01 k*=10)
    - 7.32e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (7.32e-04, rho=1.17e-01 k*=10)
- poly {C:0.3, D:0.4, ROLE:0.3}
    - 3.08e-01 -> mono {D:1}   via X (2.31e-01, rho=1.00e+00 k*=1), not(ROLE) (4.75e-02, rho=1.00e+00 k*=1), and(X,ROLE) (6.26e-03, rho=1.00e+00 k*=1), or(X,ROLE) (6.26e-03, rho=1.00e+00 k*=1)
    - 1.05e-04 -> poly {ROLE:0.3, THEM(^D):0.7}   via THEM(^D) (1.05e-04, rho=2.39e-01 k*=7)
    - 1.05e-04 -> poly {ROLE:0.3, THEM(^C):0.7}   via THEM(^C) (1.05e-04, rho=2.39e-01 k*=7)
    - 4.68e-05 -> mono {C:1}   via or(THEM(ME),ROLE) (1.96e-05, rho=5.38e-01 k*=2), or(THEM(THEM),ROLE) (1.96e-05, rho=5.38e-01 k*=2), or(ROLE,THEM(ME)) (2.76e-06, rho=2.23e-01 k*=7), or(ROLE,THEM(THEM)) (2.76e-06, rho=2.23e-01 k*=7)
    - 5.62e-06 -> mono {or(X,THEM(THEM)):1}   via or(X,THEM(THEM)) (5.62e-06, rho=1.82e-01 k*=8)
    - 5.62e-06 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (5.62e-06, rho=1.82e-01 k*=8)
- poly {X:0.1, ROLE:0.6, not(ROLE):0.3}
    - 3.48e-02 -> mono {D:1}   via D (3.48e-02, rho=1.40e-01 k*=10)
    - 3.48e-02 -> mono {C:1}   via C (3.48e-02, rho=1.40e-01 k*=10)
    - 8.81e-04 -> poly {ROLE:0.6, not(ROLE):0.1, THEM(THEM):0.3}   via THEM(THEM) (8.81e-04, rho=4.04e-01 k*=3)
    - 8.81e-04 -> poly {ROLE:0.6, not(ROLE):0.1, THEM(ME):0.3}   via THEM(ME) (8.81e-04, rho=4.04e-01 k*=3)
    - 7.32e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.32e-04, rho=1.17e-01 k*=10)
    - 7.32e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (7.32e-04, rho=1.17e-01 k*=10)
- mono {or(X,ROLE):1}
    - 3.69e-02 -> mono {C:1}   via C (3.69e-02, rho=1.48e-01 k*=10)
    - 1.96e-02 -> mono {D:1}   via D (1.96e-02, rho=7.88e-02 k*=10)
    - 1.57e-02 -> mono {X:1}   via X (1.57e-02, rho=6.79e-02 k*=10)
    - 9.52e-03 -> mono {ROLE:1}   via ROLE (9.52e-03, rho=5.00e-02 k*=10)
    - 2.18e-03 -> poly {or(X,ROLE):0.9, THEM(THEM):0.1}   via THEM(THEM) (2.18e-03, rho=1.00e+00 k*=1)
    - 2.18e-03 -> poly {or(X,ROLE):0.9, THEM(ME):0.1}   via THEM(ME) (2.18e-03, rho=1.00e+00 k*=1)
