### arm=weak, n=5, game=demand, N=100, w=1.0, x_on=True, role=True, mode=square

programs 902, classes 53, states 786, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 1.42e-04
mean payoff 0.4990, efficient 0.5000, deadweight loss 0.0010, mean bits in support 3.42

| pi | state |
|---|---|
| 0.7890 | mono {ROLE:1} |
| 0.2007 | mono {not(ROLE):1} |
| 0.0019 | mono {X:1} |
| 0.0012 | poly {C:0.34, D:0.01, X:0.65} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {ROLE:1}
    - 3.12e-05 -> mono {X:1}   via X (3.12e-05, rho=1.35e-04 k*=100)
    - 1.80e-05 -> mono {C:1}   via C (1.80e-05, rho=7.21e-05 k*=100)
    - 1.02e-05 -> poly {ROLE:0.5, not(ROLE):0.5}   via not(ROLE) (1.02e-05, rho=2.15e-04 k*=50)
    - 7.53e-06 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.53e-06, rho=1.20e-03 k*=100)
    - 9.38e-07 -> mono {or(X,X):1}   via or(X,X) (9.38e-07, rho=2.43e-04 k*=100)
    - 7.61e-07 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (7.61e-07, rho=1.89e-03 k*=100)
- mono {not(ROLE):1}
    - 4.10e-05 -> poly {ROLE:0.5, not(ROLE):0.5}   via ROLE (4.10e-05, rho=2.15e-04 k*=50)
    - 3.12e-05 -> mono {X:1}   via X (3.12e-05, rho=1.35e-04 k*=100)
    - 1.80e-05 -> mono {C:1}   via C (1.80e-05, rho=7.21e-05 k*=100)
    - 2.11e-06 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (2.11e-06, rho=1.20e-03 k*=100)
    - 1.10e-06 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.10e-06, rho=1.76e-04 k*=100)
    - 9.38e-07 -> mono {or(X,X):1}   via or(X,X) (9.38e-07, rho=2.43e-04 k*=100)
- mono {X:1}
    - 1.09e-02 -> poly {C:0.33, X:0.67}   via C (1.09e-02, rho=4.36e-02 k*=33)
    - 4.92e-03 -> mono {ROLE:1}   via ROLE (4.92e-03, rho=2.58e-02 k*=100)
    - 1.23e-03 -> mono {not(ROLE):1}   via not(ROLE) (1.23e-03, rho=2.58e-02 k*=100)
    - 1.32e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.32e-04, rho=2.10e-02 k*=100)
    - 8.35e-05 -> poly {X:0.33, or(X,X):0.67}   via or(X,X) (8.35e-05, rho=2.16e-02 k*=67)
    - 3.69e-05 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (3.69e-05, rho=2.10e-02 k*=100)
- poly {C:0.34, D:0.01, X:0.65}
    - 8.16e-03 -> poly {C:0.35, D:0.01, X:0.64}   via and(X,ROLE) (6.26e-03, rho=1.00e+00 k*=1), not(or(X,ROLE)) (1.76e-03, rho=1.00e+00 k*=1), and(X,or(X,ROLE)) (1.46e-04, rho=1.00e+00 k*=1)
    - 4.61e-03 -> mono {ROLE:1}   via ROLE (4.61e-03, rho=2.42e-02 k*=100)
    - 3.86e-03 -> poly {C:0.34, D:0.01, X:0.64, or(X,X):0.01}   via or(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 3.86e-03 -> poly {C:0.34, D:0.01, X:0.64, and(X,X):0.01}   via and(X,X) (3.86e-03, rho=1.00e+00 k*=1)
    - 1.15e-03 -> mono {not(ROLE):1}   via not(ROLE) (1.15e-03, rho=2.42e-02 k*=100)
    - 8.66e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (8.66e-05, rho=1.38e-02 k*=100)
