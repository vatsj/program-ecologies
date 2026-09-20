### arm=strong, n=6, game=pd, N=100, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 1726, classes 21, states 25, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 1.46e-10
mean payoff -0.9953, efficient 0.0000, deadweight loss 0.9953, mean bits in support 2.61

| pi | state |
|---|---|
| 0.9885 | mono {D:1} |
| 0.0071 | mono {X:1} |
| 0.0020 | mono {and(X,X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 1.01e-04 -> mono {X:1}   via X (1.01e-04, rho=3.21e-04 k*=100)
    - 3.84e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-05, rho=1.00e-02 k*=100)
    - 1.74e-05 -> mono {and(X,X):1}   via and(X,X) (1.74e-05, rho=2.19e-03 k*=100)
    - 1.50e-06 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.50e-06, rho=4.98e-03 k*=100)
    - 1.32e-06 -> mono {C:1}   via C (1.32e-06, rho=3.98e-06 k*=100)
    - 1.22e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (1.22e-06, rho=1.00e-02 k*=100)
- mono {X:1}
    - 1.66e-02 -> mono {D:1}   via D (1.66e-02, rho=5.00e-02 k*=100)
    - 2.18e-04 -> mono {and(X,X):1}   via and(X,X) (2.18e-04, rho=2.73e-02 k*=100)
    - 1.06e-04 -> mono {C:1}   via C (1.06e-04, rho=3.21e-04 k*=100)
    - 1.74e-05 -> mono {or(X,X):1}   via or(X,X) (1.74e-05, rho=2.19e-03 k*=100)
    - 1.26e-05 -> mono {THEM(ME):1}   via THEM(ME) (1.26e-05, rho=3.27e-03 k*=100)
    - 1.16e-05 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.16e-05, rho=3.84e-02 k*=100)
- mono {and(X,X):1}
    - 9.06e-03 -> mono {D:1}   via D (9.06e-03, rho=2.73e-02 k*=100)
    - 6.87e-04 -> mono {X:1}   via X (6.87e-04, rho=2.19e-03 k*=100)
    - 2.37e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.37e-05, rho=6.18e-03 k*=100)
    - 1.25e-05 -> mono {C:1}   via C (1.25e-05, rho=3.78e-05 k*=100)
    - 5.29e-06 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (5.29e-06, rho=1.76e-02 k*=100)
    - 3.33e-06 -> mono {and(THEM(ME),D):1}   via and(THEM(ME),D) (3.33e-06, rho=2.73e-02 k*=100)
