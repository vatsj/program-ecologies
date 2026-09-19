### arm=weak, n=6, game=stag, N=100, w=0.01, x_on=True, role=False, mode=square

programs 1852, classes 46, states 111, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 2.00e-03
mean payoff 3.0743, efficient 4.0000, deadweight loss 0.9257, mean bits in support 2.75

| pi | state |
|---|---|
| 0.5661 | mono {D:1} |
| 0.1250 | mono {C:1} |
| 0.0984 | poly {C:0.5, X:0.49, or(X,X):0.01} |
| 0.0978 | mono {X:1} |
| 0.0908 | poly {C:0.5, X:0.5} |
| 0.0071 | mono {and(X,X):1} |
| 0.0032 | mono {or(X,X):1} |
| 0.0028 | mono {THEM(ME):1} |
| 0.0027 | mono {THEM(THEM):1} |
| 0.0013 | mono {THEM(^C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.71e-03 -> mono {X:1}   via X (1.71e-03, rho=5.46e-03 k*=100)
    - 1.39e-03 -> mono {C:1}   via C (1.39e-03, rho=4.22e-03 k*=100)
    - 5.38e-05 -> mono {and(X,X):1}   via and(X,X) (5.38e-05, rho=7.14e-03 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 3.45e-05 -> mono {or(X,X):1}   via or(X,X) (3.45e-05, rho=4.58e-03 k*=100)
- mono {C:1}
    - 5.79e-03 -> poly {C:0.5, X:0.5}   via X (5.79e-03, rho=1.85e-02 k*=50)
    - 3.74e-03 -> mono {D:1}   via D (3.74e-03, rho=1.14e-02 k*=100)
    - 7.56e-05 -> mono {and(X,X):1}   via and(X,X) (7.56e-05, rho=1.00e-02 k*=100)
    - 6.99e-05 -> mono {or(X,X):1}   via or(X,X) (6.99e-05, rho=9.27e-03 k*=100)
    - 3.12e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.12e-05, rho=8.45e-03 k*=100)
    - 3.10e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.10e-05, rho=8.45e-03 k*=100)
- poly {C:0.5, X:0.49, or(X,X):0.01}
    - 4.52e-03 -> mono {D:1}   via D (4.52e-03, rho=1.37e-02 k*=100)
    - 2.11e-03 -> mono {C:1}   via THEM(ME) (4.65e-04, rho=1.26e-01 k*=8), THEM(THEM) (4.62e-04, rho=1.26e-01 k*=8), or(X,and(X,X)) (2.82e-04, rho=1.00e+00 k*=1), or(X,or(X,X)) (2.82e-04, rho=1.00e+00 k*=1)
    - 1.94e-04 -> mono {X:1}   via not(THEM(^X)) (8.79e-05, rho=1.00e+00 k*=1), not(and(X,THEM(ME))) (2.66e-05, rho=1.00e+00 k*=1), not(and(X,THEM(THEM))) (2.66e-05, rho=1.00e+00 k*=1), not(and(THEM(ME),X)) (2.66e-05, rho=1.00e+00 k*=1)
    - 8.81e-05 -> mono {and(X,X):1}   via and(X,X) (8.81e-05, rho=1.17e-02 k*=100)
    - 9.56e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (9.56e-06, rho=1.20e-02 k*=100)
    - 9.56e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (9.56e-06, rho=1.20e-02 k*=100)
- mono {X:1}
    - 6.05e-03 -> poly {C:0.5, X:0.5}   via C (6.05e-03, rho=1.84e-02 k*=50)
    - 4.74e-03 -> mono {D:1}   via D (4.74e-03, rho=1.44e-02 k*=100)
    - 8.83e-05 -> mono {and(X,X):1}   via and(X,X) (8.83e-05, rho=1.17e-02 k*=100)
    - 6.93e-05 -> mono {or(X,X):1}   via or(X,X) (6.93e-05, rho=9.19e-03 k*=100)
    - 3.99e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.99e-05, rho=1.08e-02 k*=100)
    - 3.96e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.96e-05, rho=1.08e-02 k*=100)
- poly {C:0.5, X:0.5}
    - 7.54e-03 -> poly {C:0.5, X:0.49, or(X,X):0.01}   via or(X,X) (7.54e-03, rho=1.00e+00 k*=1)
    - 4.53e-03 -> mono {D:1}   via D (4.53e-03, rho=1.38e-02 k*=100)
    - 1.81e-03 -> mono {C:1}   via THEM(ME) (4.65e-04, rho=1.26e-01 k*=8), THEM(THEM) (4.62e-04, rho=1.26e-01 k*=8), or(X,or(X,X)) (2.82e-04, rho=1.00e+00 k*=1), THEM(^X) (1.27e-04, rho=1.44e-01 k*=7)
    - 4.76e-04 -> mono {X:1}   via or(X,and(X,X)) (2.82e-04, rho=1.00e+00 k*=1), not(THEM(^X)) (8.79e-05, rho=1.00e+00 k*=1), not(and(X,THEM(ME))) (2.66e-05, rho=1.00e+00 k*=1), not(and(X,THEM(THEM))) (2.66e-05, rho=1.00e+00 k*=1)
    - 8.82e-05 -> mono {and(X,X):1}   via and(X,X) (8.82e-05, rho=1.17e-02 k*=100)
    - 9.55e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (9.55e-06, rho=1.20e-02 k*=100)
- mono {and(X,X):1}
    - 4.29e-03 -> mono {D:1}   via D (4.29e-03, rho=1.31e-02 k*=100)
    - 2.54e-03 -> mono {X:1}   via X (2.54e-03, rho=8.12e-03 k*=100)
    - 2.25e-03 -> mono {C:1}   via C (2.25e-03, rho=6.84e-03 k*=100)
    - 5.38e-05 -> mono {or(X,X):1}   via or(X,X) (5.38e-05, rho=7.14e-03 k*=100)
    - 3.99e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.99e-05, rho=1.08e-02 k*=100)
    - 3.96e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.96e-05, rho=1.08e-02 k*=100)
- mono {or(X,X):1}
    - 4.53e-03 -> mono {D:1}   via D (4.53e-03, rho=1.38e-02 k*=100)
    - 3.41e-03 -> mono {C:1}   via C (3.41e-03, rho=1.04e-02 k*=100)
    - 3.26e-03 -> mono {X:1}   via X (3.26e-03, rho=1.04e-02 k*=100)
    - 8.82e-05 -> mono {and(X,X):1}   via and(X,X) (8.82e-05, rho=1.17e-02 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
- mono {THEM(ME):1}
    - 4.46e-03 -> mono {C:1}   via C (4.46e-03, rho=1.36e-02 k*=100)
    - 3.29e-03 -> mono {D:1}   via D (3.29e-03, rho=1.00e-02 k*=100)
    - 2.66e-03 -> mono {X:1}   via X (2.66e-03, rho=8.51e-03 k*=100)
    - 7.54e-05 -> mono {or(X,X):1}   via or(X,X) (7.54e-05, rho=1.00e-02 k*=100)
    - 6.42e-05 -> mono {and(X,X):1}   via and(X,X) (6.42e-05, rho=8.51e-03 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
- mono {THEM(THEM):1}
    - 4.46e-03 -> mono {C:1}   via C (4.46e-03, rho=1.36e-02 k*=100)
    - 3.29e-03 -> mono {D:1}   via D (3.29e-03, rho=1.00e-02 k*=100)
    - 2.66e-03 -> mono {X:1}   via X (2.66e-03, rho=8.51e-03 k*=100)
    - 7.54e-05 -> mono {or(X,X):1}   via or(X,X) (7.54e-05, rho=1.00e-02 k*=100)
    - 6.42e-05 -> mono {and(X,X):1}   via and(X,X) (6.42e-05, rho=8.51e-03 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
- mono {THEM(^C):1}
    - 3.29e-03 -> mono {C:1}   via C (3.29e-03, rho=1.00e-02 k*=100)
    - 2.37e-03 -> mono {D:1}   via D (2.37e-03, rho=7.22e-03 k*=100)
    - 1.90e-03 -> mono {X:1}   via X (1.90e-03, rho=6.08e-03 k*=100)
    - 5.44e-05 -> mono {or(X,X):1}   via or(X,X) (5.44e-05, rho=7.22e-03 k*=100)
    - 4.59e-05 -> mono {and(X,X):1}   via and(X,X) (4.59e-05, rho=6.08e-03 k*=100)
    - 3.12e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.12e-05, rho=8.45e-03 k*=100)
