### arm=weak, n=5, game=bos, N=100, w=0.1, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 54, states 406, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 6.42e-05
mean payoff 1.4884, efficient 1.5000, deadweight loss 0.0116, mean bits in support 3.04

| pi | state |
|---|---|
| 0.4913 | mono {A:1} |
| 0.4913 | mono {B:1} |
| 0.0099 | mono {X:1} |
| 0.0020 | poly {X:0.65, ROLE:0.01, not(ROLE):0.34} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {A:1}
    - 1.34e-04 -> mono {B:1}   via B (1.34e-04, rho=5.39e-04 k*=100)
    - 1.27e-04 -> mono {X:1}   via X (1.27e-04, rho=5.48e-04 k*=100)
    - 1.79e-05 -> mono {not(ROLE):1}   via not(ROLE) (1.79e-05, rho=3.77e-04 k*=100)
    - 6.25e-06 -> mono {or(X,X):1}   via or(X,X) (6.25e-06, rho=1.62e-03 k*=100)
    - 4.39e-06 -> mono {THEM(^A):1}   via THEM(^A) (4.39e-06, rho=1.00e-02 k*=100)
    - 4.39e-06 -> mono {THEM(^B):1}   via THEM(^B) (4.39e-06, rho=1.00e-02 k*=100)
- mono {B:1}
    - 1.34e-04 -> mono {A:1}   via A (1.34e-04, rho=5.39e-04 k*=100)
    - 1.27e-04 -> mono {X:1}   via X (1.27e-04, rho=5.48e-04 k*=100)
    - 1.79e-05 -> mono {not(ROLE):1}   via not(ROLE) (1.79e-05, rho=3.77e-04 k*=100)
    - 6.25e-06 -> mono {and(X,X):1}   via and(X,X) (6.25e-06, rho=1.62e-03 k*=100)
    - 4.39e-06 -> mono {THEM(^A):1}   via THEM(^A) (4.39e-06, rho=1.00e-02 k*=100)
    - 4.39e-06 -> mono {THEM(^B):1}   via THEM(^B) (4.39e-06, rho=1.00e-02 k*=100)
- mono {X:1}
    - 5.38e-03 -> mono {A:1}   via A (5.38e-03, rho=2.16e-02 k*=100)
    - 5.38e-03 -> mono {B:1}   via B (5.38e-03, rho=2.16e-02 k*=100)
    - 1.89e-03 -> poly {X:0.67, not(ROLE):0.33}   via not(ROLE) (1.89e-03, rho=3.97e-02 k*=33)
    - 5.06e-05 -> mono {or(X,X):1}   via or(X,X) (5.06e-05, rho=1.31e-02 k*=100)
    - 5.06e-05 -> mono {and(X,X):1}   via and(X,X) (5.06e-05, rho=1.31e-02 k*=100)
    - 3.43e-05 -> mono {ROLE:1}   via ROLE (3.43e-05, rho=1.80e-04 k*=100)
- poly {X:0.65, ROLE:0.01, not(ROLE):0.34}
    - 5.07e-03 -> mono {A:1}   via A (5.07e-03, rho=2.04e-02 k*=100)
    - 5.07e-03 -> mono {B:1}   via B (5.07e-03, rho=2.04e-02 k*=100)
    - 1.46e-04 -> poly {X:0.64, ROLE:0.01, not(ROLE):0.35}   via or(ROLE,and(X,X)) (7.29e-05, rho=1.00e+00 k*=1), and(ROLE,or(X,X)) (7.29e-05, rho=1.00e+00 k*=1)
    - 1.07e-04 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via or(X,ROLE) (1.07e-04, rho=1.71e-02 k*=50)
    - 1.07e-04 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.07e-04, rho=1.71e-02 k*=50)
    - 8.06e-05 -> poly {ROLE:0.14, not(ROLE):0.57, THEM(THEM):0.29}   via THEM(THEM) (8.06e-05, rho=3.70e-02 k*=29)
