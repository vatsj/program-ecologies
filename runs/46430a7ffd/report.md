### arm=weak, n=5, game=demand_norole, N=10, w=0.01, x_on=True, role=False, mode=square

programs 450, classes 30, states 771, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 6.75e-03
mean payoff 0.3932, efficient 0.5000, deadweight loss 0.1068, mean bits in support 4.33

| pi | state |
|---|---|
| 0.2060 | poly {C:0.4, D:0.1, X:0.3, and(X,X):0.1, or(X,X):0.1} |
| 0.1863 | poly {C:0.5, D:0.2, X:0.1, and(X,X):0.1, or(X,X):0.1} |
| 0.0366 | poly {C:0.4, D:0.1, X:0.5} |
| 0.0355 | poly {C:0.6, D:0.3, X:0.1} |
| 0.0307 | poly {C:0.4, D:0.1, X:0.4, and(X,X):0.1} |
| 0.0285 | poly {C:0.5, D:0.3, X:0.1, or(X,X):0.1} |
| 0.0285 | poly {C:0.6, D:0.2, X:0.1, and(X,X):0.1} |
| 0.0268 | poly {C:0.4, D:0.1, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1} |
| 0.0249 | poly {C:0.5, D:0.1, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1} |
| 0.0229 | poly {C:0.3, D:0.1, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1} |
| 0.0229 | poly {C:0.3, D:0.1, X:0.3, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),C):0.1} |
| 0.0228 | poly {C:0.4, D:0.1, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {C:0.4, D:0.1, X:0.3, and(X,X):0.1, or(X,X):0.1}
    - 3.68e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.68e-04, rho=9.99e-02 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=9.99e-02 k*=10)
    - 1.52e-04 -> poly {C:0.3, D:0.1, X:0.3, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.3, D:0.1, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.4, D:0.1, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.4, D:0.1, X:0.2, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.5, D:0.2, X:0.1, and(X,X):0.1, or(X,X):0.1}
    - 3.68e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.68e-04, rho=9.99e-02 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=9.99e-02 k*=10)
    - 1.52e-04 -> poly {C:0.4, D:0.2, X:0.1, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.4, D:0.2, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, D:0.1, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, D:0.1, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.4, D:0.1, X:0.5}
    - 6.74e-03 -> poly {C:0.4, D:0.1, X:0.4, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {C:0.4, D:0.1, X:0.4, and(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.68e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.68e-04, rho=9.99e-02 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=9.99e-02 k*=10)
    - 1.52e-04 -> poly {C:0.4, X:0.6}   via and(THEM(ME),X) (7.61e-05, rho=1.00e+00 k*=1), and(THEM(THEM),X) (7.61e-05, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.3, D:0.1, X:0.5, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.6, D:0.3, X:0.1}
    - 6.74e-03 -> poly {C:0.5, D:0.3, X:0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {C:0.6, D:0.2, X:0.1, and(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.68e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.68e-04, rho=9.98e-02 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=9.98e-02 k*=10)
    - 1.52e-04 -> poly {C:0.5, D:0.3, X:0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, D:0.3, X:0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.4, D:0.1, X:0.4, and(X,X):0.1}
    - 6.74e-03 -> poly {C:0.4, D:0.1, X:0.3, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.68e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.68e-04, rho=9.99e-02 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=9.99e-02 k*=10)
    - 1.52e-04 -> poly {C:0.5, X:0.3, and(X,X):0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.4, D:0.1, X:0.3, and(X,X):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.4, D:0.1, X:0.3, and(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.5, D:0.3, X:0.1, or(X,X):0.1}
    - 6.74e-03 -> poly {C:0.5, D:0.2, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.68e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.68e-04, rho=9.99e-02 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=9.99e-02 k*=10)
    - 1.52e-04 -> poly {C:0.4, D:0.3, X:0.1, or(X,X):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, D:0.2, X:0.1, or(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, D:0.2, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.6, D:0.2, X:0.1, and(X,X):0.1}
    - 6.74e-03 -> poly {C:0.5, D:0.2, X:0.1, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.68e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.68e-04, rho=9.99e-02 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=9.99e-02 k*=10)
    - 1.52e-04 -> poly {C:0.5, D:0.2, X:0.1, and(X,X):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, D:0.2, X:0.1, and(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, D:0.1, X:0.1, and(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.4, D:0.1, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}
    - 3.68e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.68e-04, rho=9.99e-02 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=9.99e-02 k*=10)
    - 1.52e-04 -> poly {C:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.3, D:0.1, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.3, D:0.1, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.4, D:0.1, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.5, D:0.1, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}
    - 3.68e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.68e-04, rho=9.99e-02 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=9.99e-02 k*=10)
    - 1.52e-04 -> poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.4, D:0.1, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.4, D:0.1, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.4, D:0.1, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.3, D:0.1, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}
    - 3.68e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.68e-04, rho=9.99e-02 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=9.99e-02 k*=10)
    - 1.52e-04 -> poly {C:0.2, D:0.1, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.3, D:0.1, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.3, D:0.1, X:0.2, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.3, D:0.1, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.3, D:0.1, X:0.3, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),C):0.1}
    - 3.68e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.68e-04, rho=9.99e-02 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=9.99e-02 k*=10)
    - 1.52e-04 -> poly {C:0.2, D:0.1, X:0.3, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.3, D:0.1, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.3, D:0.1, X:0.2, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(THEM(ME),C):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.3, D:0.1, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(THEM(ME),C):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.4, D:0.1, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1}
    - 3.68e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.68e-04, rho=9.99e-02 k*=10)
    - 3.68e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.68e-04, rho=9.99e-02 k*=10)
    - 1.52e-04 -> poly {C:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.4, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,and(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.3, D:0.1, X:0.2, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.4, D:0.1, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
