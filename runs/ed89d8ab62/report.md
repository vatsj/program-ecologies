### arm=weak, n=5, game=bos, N=100, w=1.0, x_on=True, role=True, mode=square

programs 902, classes 54, states 494, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 7.43e-06
mean payoff 1.4990, efficient 1.5000, deadweight loss 0.0010, mean bits in support 3.05

| pi | state |
|---|---|
| 0.4966 | mono {D:1} |
| 0.4966 | mono {C:1} |
| 0.0029 | poly {ROLE:0.33, THEM(^C):0.67} |
| 0.0029 | poly {ROLE:0.33, THEM(^D):0.67} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 4.39e-06 -> mono {THEM(^D):1}   via THEM(^D) (4.39e-06, rho=1.00e-02 k*=100)
    - 4.39e-06 -> mono {THEM(^C):1}   via THEM(^C) (4.39e-06, rho=1.00e-02 k*=100)
    - 3.64e-07 -> mono {and(ROLE,THEM(THEM)):1}   via and(ROLE,THEM(THEM)) (3.64e-07, rho=1.00e-02 k*=100)
    - 3.64e-07 -> mono {and(ROLE,THEM(ME)):1}   via and(ROLE,THEM(ME)) (3.64e-07, rho=1.00e-02 k*=100)
    - 3.64e-07 -> mono {and(X,THEM(THEM)):1}   via and(X,THEM(THEM)) (3.64e-07, rho=1.00e-02 k*=100)
    - 3.64e-07 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (3.64e-07, rho=1.00e-02 k*=100)
- mono {C:1}
    - 4.39e-06 -> mono {THEM(^D):1}   via THEM(^D) (4.39e-06, rho=1.00e-02 k*=100)
    - 4.39e-06 -> mono {THEM(^C):1}   via THEM(^C) (4.39e-06, rho=1.00e-02 k*=100)
    - 3.64e-07 -> mono {or(ROLE,THEM(THEM)):1}   via or(ROLE,THEM(THEM)) (3.64e-07, rho=1.00e-02 k*=100)
    - 3.64e-07 -> mono {or(ROLE,THEM(ME)):1}   via or(ROLE,THEM(ME)) (3.64e-07, rho=1.00e-02 k*=100)
    - 3.64e-07 -> mono {or(X,THEM(THEM)):1}   via or(X,THEM(THEM)) (3.64e-07, rho=1.00e-02 k*=100)
    - 3.64e-07 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (3.64e-07, rho=1.00e-02 k*=100)
- poly {ROLE:0.33, THEM(^C):0.67}
    - 6.25e-04 -> mono {D:1}   via D (6.25e-04, rho=2.51e-03 k*=100)
    - 6.25e-04 -> mono {C:1}   via C (6.25e-04, rho=2.51e-03 k*=100)
    - 3.60e-06 -> poly {ROLE:0.29, THEM(^C):0.57, and(THEM(THEM),ROLE):0.14}   via and(THEM(THEM),ROLE) (3.60e-06, rho=9.87e-02 k*=14)
    - 3.60e-06 -> poly {ROLE:0.29, THEM(^C):0.57, and(THEM(ME),ROLE):0.14}   via and(THEM(ME),ROLE) (3.60e-06, rho=9.87e-02 k*=14)
    - 2.98e-06 -> mono {and(ROLE,THEM(THEM)):1}   via and(ROLE,THEM(THEM)) (2.98e-06, rho=8.17e-02 k*=100)
    - 2.98e-06 -> mono {and(ROLE,THEM(ME)):1}   via and(ROLE,THEM(ME)) (2.98e-06, rho=8.17e-02 k*=100)
- poly {ROLE:0.33, THEM(^D):0.67}
    - 6.25e-04 -> mono {D:1}   via D (6.25e-04, rho=2.51e-03 k*=100)
    - 6.25e-04 -> mono {C:1}   via C (6.25e-04, rho=2.51e-03 k*=100)
    - 3.60e-06 -> poly {ROLE:0.29, THEM(^D):0.57, or(THEM(THEM),ROLE):0.14}   via or(THEM(THEM),ROLE) (3.60e-06, rho=9.87e-02 k*=14)
    - 3.60e-06 -> poly {ROLE:0.29, THEM(^D):0.57, or(THEM(ME),ROLE):0.14}   via or(THEM(ME),ROLE) (3.60e-06, rho=9.87e-02 k*=14)
    - 2.98e-06 -> mono {or(ROLE,THEM(THEM)):1}   via or(ROLE,THEM(THEM)) (2.98e-06, rho=8.17e-02 k*=100)
    - 2.98e-06 -> mono {or(ROLE,THEM(ME)):1}   via or(ROLE,THEM(ME)) (2.98e-06, rho=8.17e-02 k*=100)
