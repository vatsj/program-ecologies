### arm=strong, n=6, game=stag, N=100, w=0.1, x_on=True, role=False, mode=square

programs 1726, classes 21, states 30, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 2.48e-05
mean payoff 3.0046, efficient 4.0000, deadweight loss 0.9954, mean bits in support 2.61

| pi | state |
|---|---|
| 0.9905 | mono {D:1} |
| 0.0049 | mono {C:1} |
| 0.0016 | mono {THEM(ME):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.84e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-05, rho=1.00e-02 k*=100)
    - 5.44e-06 -> mono {X:1}   via X (5.44e-06, rho=1.73e-05 k*=100)
    - 2.57e-06 -> mono {and(X,X):1}   via and(X,X) (2.57e-06, rho=3.23e-04 k*=100)
    - 1.22e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.22e-06, rho=1.00e-02 k*=100)
    - 9.32e-07 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (9.32e-07, rho=1.00e-02 k*=100)
    - 9.32e-07 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (9.32e-07, rho=1.00e-02 k*=100)
- mono {C:1}
    - 3.42e-03 -> poly {C:0.5, X:0.5}   via X (3.42e-03, rho=1.09e-02 k*=50)
    - 3.32e-03 -> mono {D:1}   via D (3.32e-03, rho=1.00e-02 k*=100)
    - 6.12e-05 -> mono {and(X,X):1}   via and(X,X) (6.12e-05, rho=7.67e-03 k*=100)
    - 4.37e-05 -> mono {or(X,X):1}   via or(X,X) (4.37e-05, rho=5.48e-03 k*=100)
    - 8.53e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.53e-06, rho=1.00e-02 k*=100)
    - 6.15e-06 -> mono {THEM(ME):1}   via THEM(ME) (6.15e-06, rho=1.60e-03 k*=100)
- mono {THEM(ME):1}
    - 1.92e-02 -> mono {C:1}   via C (1.92e-02, rho=5.78e-02 k*=100)
    - 3.32e-03 -> mono {D:1}   via D (3.32e-03, rho=1.00e-02 k*=100)
    - 7.49e-04 -> mono {X:1}   via X (7.49e-04, rho=2.38e-03 k*=100)
    - 7.98e-05 -> mono {or(X,X):1}   via or(X,X) (7.98e-05, rho=1.00e-02 k*=100)
    - 1.90e-05 -> mono {and(X,X):1}   via and(X,X) (1.90e-05, rho=2.38e-03 k*=100)
    - 8.51e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (8.51e-06, rho=1.00e-02 k*=100)
