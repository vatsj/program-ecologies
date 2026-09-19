### arm=strong, n=6, game=pd, N=10, w=1.0, x_on=True, role=False, mode=square

programs 1726, classes 21, states 25, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 6.99e-10
mean payoff -0.9989, efficient 0.0000, deadweight loss 0.9989, mean bits in support 2.60

| pi | state |
|---|---|
| 0.9968 | mono {D:1} |
| 0.0011 | mono {X:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 3.84e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-04, rho=1.00e-01 k*=10)
    - 1.22e-05 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.22e-05, rho=1.00e-01 k*=10)
    - 9.32e-06 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (9.32e-06, rho=1.00e-01 k*=10)
    - 9.32e-06 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (9.32e-06, rho=1.00e-01 k*=10)
    - 4.92e-28 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (4.92e-28, rho=5.28e-24 k*=10)
    - 2.18e-31 -> mono {X:1}   via X (2.18e-31, rho=6.94e-31 k*=10)
- mono {X:1}
    - 2.15e-01 -> mono {D:1}   via D (2.15e-01, rho=6.50e-01 k*=10)
    - 3.58e-03 -> mono {and(X,X):1}   via and(X,X) (3.58e-03, rho=4.48e-01 k*=10)
    - 1.70e-04 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.70e-04, rho=5.65e-01 k*=10)
    - 8.44e-05 -> mono {and(X,or(X,X)):1}   via and(X,or(X,X)) (8.44e-05, rho=2.80e-01 k*=10)
    - 7.92e-05 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (7.92e-05, rho=6.50e-01 k*=10)
    - 3.97e-05 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (3.97e-05, rho=4.25e-01 k*=10)
