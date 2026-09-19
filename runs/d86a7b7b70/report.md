### arm=weak, n=5, game=chicken, N=10, w=1.0, x_on=True, role=True, mode=square

programs 902, classes 53, states 498, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 9.69e-05
mean payoff 0.4964, efficient 0.5000, deadweight loss 0.0036, mean bits in support 3.44

| pi | state |
|---|---|
| 0.7960 | mono {ROLE:1} |
| 0.1981 | mono {not(ROLE):1} |
| 0.0019 | poly {D:0.2, not(THEM(THEM)):0.8} |
| 0.0019 | poly {D:0.2, not(THEM(ME)):0.8} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 5.96e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (5.96e-05, rho=9.52e-03 k*=10)
    - 3.48e-05 -> mono {C:1}   via C (3.48e-05, rho=1.40e-04 k*=10)
    - 2.15e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (2.15e-05, rho=5.35e-02 k*=10)
    - 2.15e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (2.15e-05, rho=5.35e-02 k*=10)
    - 3.64e-06 -> mono {not(THEM(^ROLE)):1}   via not(THEM(^ROLE)) (3.64e-06, rho=1.00e-01 k*=10)
    - 2.75e-06 -> mono {or(ROLE,and(X,X)):1}   via or(ROLE,and(X,X)) (2.75e-06, rho=3.77e-02 k*=10)
- mono {not(ROLE):1}
    - 3.48e-05 -> mono {C:1}   via C (3.48e-05, rho=1.40e-04 k*=10)
    - 2.15e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (2.15e-05, rho=5.35e-02 k*=10)
    - 2.15e-05 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (2.15e-05, rho=5.35e-02 k*=10)
    - 1.67e-05 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (1.67e-05, rho=9.52e-03 k*=10)
    - 3.64e-06 -> mono {not(THEM(^ROLE)):1}   via not(THEM(^ROLE)) (3.64e-06, rho=1.00e-01 k*=10)
    - 1.95e-06 -> mono {not(THEM(^C)):1}   via not(THEM(^C)) (1.95e-06, rho=5.35e-02 k*=10)
- poly {D:0.2, not(THEM(THEM)):0.8}
    - 6.94e-03 -> mono {ROLE:1}   via ROLE (6.94e-03, rho=3.64e-02 k*=10)
    - 1.73e-03 -> mono {not(ROLE):1}   via not(ROLE) (1.73e-03, rho=3.64e-02 k*=10)
    - 4.03e-04 -> poly {D:0.2, not(THEM(ME)):0.1, not(THEM(THEM)):0.7}   via not(THEM(ME)) (4.03e-04, rho=1.00e+00 k*=1)
    - 7.29e-05 -> poly {D:0.2, not(THEM(THEM)):0.7, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
    - 4.39e-05 -> mono {THEM(^C):1}   via THEM(^C) (4.39e-05, rho=1.00e-01 k*=10)
    - 3.64e-05 -> poly {D:0.2, not(THEM(THEM)):0.7, not(THEM(^D)):0.1}   via not(THEM(^D)) (3.64e-05, rho=1.00e+00 k*=1)
- poly {D:0.2, not(THEM(ME)):0.8}
    - 6.94e-03 -> mono {ROLE:1}   via ROLE (6.94e-03, rho=3.64e-02 k*=10)
    - 1.73e-03 -> mono {not(ROLE):1}   via not(ROLE) (1.73e-03, rho=3.64e-02 k*=10)
    - 4.03e-04 -> poly {D:0.2, not(THEM(ME)):0.7, not(THEM(THEM)):0.1}   via not(THEM(THEM)) (4.03e-04, rho=1.00e+00 k*=1)
    - 2.17e-04 -> mono {THEM(^C):1}   via THEM(^C) (2.17e-04, rho=4.93e-01 k*=10)
    - 7.29e-05 -> poly {D:0.2, not(THEM(ME)):0.7, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (7.29e-05, rho=1.00e+00 k*=1)
    - 3.64e-05 -> poly {D:0.2, not(THEM(ME)):0.7, not(THEM(^D)):0.1}   via not(THEM(^D)) (3.64e-05, rho=1.00e+00 k*=1)
