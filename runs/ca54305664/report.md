### arm=weak, n=6, game=stag, N=100, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 46, states 82, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 3.63e-08
mean payoff 3.0286, efficient 4.0000, deadweight loss 0.9714, mean bits in support 2.68

| pi | state |
|---|---|
| 0.9643 | mono {Hare:1} |
| 0.0229 | mono {Stag:1} |
| 0.0066 | mono {THEM(^Stag):1} |
| 0.0016 | mono {X:1} |
| 0.0012 | mono {THEM(ME):1} |
| 0.0011 | mono {THEM(THEM):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Hare:1}
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 2.25e-05 -> mono {THEM(^Stag):1}   via THEM(^Stag) (2.25e-05, rho=2.48e-02 k*=100)
    - 9.10e-06 -> mono {THEM(^Hare):1}   via THEM(^Hare) (9.10e-06, rho=1.00e-02 k*=100)
    - 2.89e-06 -> mono {THEM(^X):1}   via THEM(^X) (2.89e-06, rho=3.27e-03 k*=100)
    - 2.29e-06 -> mono {and(THEM(ME),Hare):1}   via and(THEM(ME),Hare) (2.29e-06, rho=1.00e-02 k*=100)
- mono {Stag:1}
    - 2.70e-03 -> mono {Hare:1}   via Hare (2.70e-03, rho=8.20e-03 k*=100)
    - 1.39e-03 -> mono {X:1}   via X (1.39e-03, rho=4.46e-03 k*=100)
    - 4.71e-05 -> mono {and(X,X):1}   via and(X,X) (4.71e-05, rho=6.25e-03 k*=100)
    - 3.27e-05 -> mono {or(X,X):1}   via or(X,X) (3.27e-05, rho=4.34e-03 k*=100)
    - 9.10e-06 -> mono {THEM(^Stag):1}   via THEM(^Stag) (9.10e-06, rho=1.00e-02 k*=100)
    - 6.53e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (6.53e-06, rho=8.20e-03 k*=100)
- mono {THEM(^Stag):1}
    - 3.29e-03 -> mono {Stag:1}   via Stag (3.29e-03, rho=1.00e-02 k*=100)
    - 6.07e-05 -> mono {Hare:1}   via Hare (6.07e-05, rho=1.84e-04 k*=100)
    - 7.47e-06 -> mono {THEM(^Hare):1}   via THEM(^Hare) (7.47e-06, rho=8.20e-03 k*=100)
    - 6.05e-06 -> mono {X:1}   via X (6.05e-06, rho=1.94e-05 k*=100)
    - 3.94e-06 -> mono {THEM(^X):1}   via THEM(^X) (3.94e-06, rho=4.46e-03 k*=100)
    - 2.26e-06 -> mono {THEM(ME):1}   via THEM(ME) (2.26e-06, rho=6.11e-04 k*=100)
- mono {X:1}
    - 2.04e-02 -> mono {Hare:1}   via Hare (2.04e-02, rho=6.20e-02 k*=100)
    - 1.26e-03 -> mono {Stag:1}   via Stag (1.26e-03, rho=3.84e-03 k*=100)
    - 2.42e-04 -> mono {and(X,X):1}   via and(X,X) (2.42e-04, rho=3.20e-02 k*=100)
    - 6.68e-05 -> mono {THEM(ME):1}   via THEM(ME) (6.68e-05, rho=1.81e-02 k*=100)
    - 6.63e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (6.63e-05, rho=1.81e-02 k*=100)
    - 2.99e-05 -> mono {or(X,X):1}   via or(X,X) (2.99e-05, rho=3.97e-03 k*=100)
- mono {THEM(ME):1}
    - 2.70e-02 -> mono {Stag:1}   via Stag (2.70e-02, rho=8.21e-02 k*=100)
    - 3.29e-03 -> mono {Hare:1}   via Hare (3.29e-03, rho=1.00e-02 k*=100)
    - 4.87e-04 -> mono {X:1}   via X (4.87e-04, rho=1.56e-03 k*=100)
    - 7.54e-05 -> mono {or(X,X):1}   via or(X,X) (7.54e-05, rho=1.00e-02 k*=100)
    - 7.47e-05 -> mono {THEM(^Stag):1}   via THEM(^Stag) (7.47e-05, rho=8.21e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
- mono {THEM(THEM):1}
    - 2.70e-02 -> mono {Stag:1}   via Stag (2.70e-02, rho=8.21e-02 k*=100)
    - 3.29e-03 -> mono {Hare:1}   via Hare (3.29e-03, rho=1.00e-02 k*=100)
    - 4.87e-04 -> mono {X:1}   via X (4.87e-04, rho=1.56e-03 k*=100)
    - 7.54e-05 -> mono {or(X,X):1}   via or(X,X) (7.54e-05, rho=1.00e-02 k*=100)
    - 7.47e-05 -> mono {THEM(^Stag):1}   via THEM(^Stag) (7.47e-05, rho=8.21e-02 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
