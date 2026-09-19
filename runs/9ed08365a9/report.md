### arm=weak, n=5, game=chicken_norole, N=10, w=0.1, x_on=True, role=False, mode=square

programs 450, classes 30, states 528, terminal classes 1, indeterminate 0, divergence rate 0.0027, flow into polymorphic targets 1.62e-02
mean payoff -0.1456, efficient 0.5000, deadweight loss 0.6456, mean bits in support 4.30

| pi | state |
|---|---|
| 0.4395 | poly {C:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1} |
| 0.0940 | poly {C:0.7, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1} |
| 0.0633 | poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1} |
| 0.0620 | poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1} |
| 0.0497 | poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),C):0.1} |
| 0.0352 | poly {C:0.7, D:0.1, X:0.1, and(X,X):0.1} |
| 0.0262 | poly {C:0.7, D:0.1, X:0.2} |
| 0.0237 | poly {C:0.7, D:0.1, X:0.1, or(X,X):0.1} |
| 0.0223 | poly {C:0.6, D:0.1, X:0.2, or(X,X):0.1} |
| 0.0181 | poly {C:0.8, D:0.1, X:0.1} |
| 0.0150 | poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),C):0.1} |
| 0.0149 | poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(THEM(ME),C):0.1} |

Transitions out of the support (share of mutation events, mutants responsible):

- poly {C:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}
    - 8.13e-03 -> poly {C:0.6, X:0.2, and(X,X):0.1, or(X,X):0.1}   via THEM(ME) (3.68e-03, rho=1.00e+00 k*=1), THEM(THEM) (3.68e-03, rho=1.00e+00 k*=1), THEM(^C) (7.65e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.7, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.7, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1}
    - 9.20e-03 -> poly {C:0.6, X:0.2, or(X,X):0.1, and(X,or(X,X)):0.1}   via THEM(ME) (3.68e-03, rho=1.00e+00 k*=1), THEM(THEM) (3.68e-03, rho=1.00e+00 k*=1), THEM(^C) (7.65e-04, rho=1.00e+00 k*=1), THEM(^X) (7.65e-04, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 9.17e-04 -> poly {C:0.6, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.2}   via THEM(^D) (7.65e-04, rho=1.00e+00 k*=1), and(X,THEM(ME)) (7.61e-05, rho=1.00e+00 k*=1), and(X,THEM(THEM)) (7.61e-05, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.2, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, X:0.1, or(X,X):0.1, or(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1}
    - 3.38e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.38e-04, rho=9.22e-02 k*=10)
    - 3.38e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.38e-04, rho=9.22e-02 k*=10)
    - 1.52e-04 -> poly {C:0.6, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1}
    - 3.40e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.40e-04, rho=9.24e-02 k*=10)
    - 3.40e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.40e-04, rho=9.24e-02 k*=10)
    - 1.52e-04 -> poly {C:0.6, X:0.1, or(X,X):0.1, or(X,and(X,X)):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(X,or(X,X)):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.6, X:0.1, and(X,X):0.1, or(X,X):0.1, or(THEM(ME),C):0.1}
    - 3.37e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.37e-04, rho=9.15e-02 k*=10)
    - 3.37e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.37e-04, rho=9.15e-02 k*=10)
    - 1.52e-04 -> poly {C:0.6, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(THEM(ME),C):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(THEM(ME),C):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.7, D:0.1, X:0.1, and(X,X):0.1}
    - 6.74e-03 -> poly {C:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.55e-04 -> mono {C:1}   via THEM(ME) (2.97e-04, rho=1.61e-01 k*=5), THEM(THEM) (2.97e-04, rho=1.61e-01 k*=5), THEM(^C) (6.16e-05, rho=1.61e-01 k*=5)
    - 2.97e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.97e-04, rho=1.61e-01 k*=5)
    - 2.97e-04 -> mono {THEM(ME):1}   via THEM(ME) (2.97e-04, rho=1.61e-01 k*=5)
    - 1.52e-04 -> poly {C:0.8, X:0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.7, X:0.1, and(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.7, D:0.1, X:0.2}
    - 6.74e-03 -> poly {C:0.6, D:0.1, X:0.2, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {C:0.7, D:0.1, X:0.1, and(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.85e-04 -> mono {C:1}   via THEM(ME) (3.10e-04, rho=1.68e-01 k*=5), THEM(THEM) (3.10e-04, rho=1.68e-01 k*=5), THEM(^C) (6.45e-05, rho=1.68e-01 k*=5)
    - 3.07e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.07e-04, rho=1.68e-01 k*=5)
    - 3.07e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.07e-04, rho=1.68e-01 k*=5)
    - 1.52e-04 -> poly {C:0.6, D:0.1, X:0.2, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.7, D:0.1, X:0.1, or(X,X):0.1}
    - 6.74e-03 -> poly {C:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.19e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.19e-04, rho=8.67e-02 k*=10)
    - 3.19e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.19e-04, rho=8.67e-02 k*=10)
    - 1.52e-04 -> poly {C:0.7, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.7, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.6, D:0.1, X:0.1, or(X,X):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.6, D:0.1, X:0.2, or(X,X):0.1}
    - 6.74e-03 -> poly {C:0.7, X:0.1, and(X,X):0.1, or(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 3.23e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.23e-04, rho=8.77e-02 k*=10)
    - 3.23e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.23e-04, rho=8.77e-02 k*=10)
    - 1.52e-04 -> poly {C:0.7, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.7, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, D:0.1, X:0.2, or(X,X):0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.8, D:0.1, X:0.1}
    - 6.74e-03 -> poly {C:0.7, D:0.1, X:0.1, or(X,X):0.1}   via or(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.74e-03 -> poly {C:0.7, D:0.1, X:0.1, and(X,X):0.1}   via and(X,X) (6.74e-03, rho=1.00e+00 k*=1)
    - 6.98e-04 -> mono {C:1}   via THEM(ME) (3.16e-04, rho=1.70e-01 k*=5), THEM(THEM) (3.16e-04, rho=1.70e-01 k*=5), THEM(^C) (6.57e-05, rho=1.70e-01 k*=5)
    - 3.09e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.09e-04, rho=1.70e-01 k*=5)
    - 3.09e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.09e-04, rho=1.70e-01 k*=5)
    - 1.52e-04 -> poly {C:0.7, D:0.1, X:0.1, or(THEM(ME),C):0.1}   via or(THEM(ME),C) (1.52e-04, rho=1.00e+00 k*=1)
- poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,or(X,X)):0.1, or(THEM(ME),C):0.1}
    - 3.38e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.38e-04, rho=9.22e-02 k*=10)
    - 3.38e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.38e-04, rho=9.22e-02 k*=10)
    - 1.52e-04 -> poly {C:0.5, X:0.1, or(X,X):0.1, and(X,or(X,X)):0.1, or(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via or(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 9.42e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (9.42e-05, rho=1.55e-01 k*=9)
- poly {C:0.5, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(THEM(ME),C):0.1}
    - 3.40e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.40e-04, rho=9.24e-02 k*=10)
    - 3.40e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.40e-04, rho=9.24e-02 k*=10)
    - 1.52e-04 -> poly {C:0.5, X:0.1, or(X,X):0.1, or(X,and(X,X)):0.1, and(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via and(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.5, X:0.1, or(X,X):0.1, and(X,and(X,X)):0.1, or(X,and(X,X)):0.1, or(THEM(ME),C):0.1}   via and(X,and(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 1.52e-04 -> poly {C:0.4, X:0.1, and(X,X):0.1, or(X,X):0.1, or(X,and(X,X)):0.1, or(X,or(X,X)):0.1, or(THEM(ME),C):0.1}   via or(X,or(X,X)) (1.52e-04, rho=1.00e+00 k*=1)
    - 9.07e-05 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (9.07e-05, rho=1.51e-01 k*=9)
