### arm=weak, n=6, game=exchange, N=10, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 46, states 328, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 6.98e-05
mean payoff 0.0265, efficient 2.0000, deadweight loss 1.9735, mean bits in support 2.69

| pi | state |
|---|---|
| 0.9787 | mono {Keep:1} |
| 0.0068 | mono {THEM(^Give):1} |
| 0.0063 | mono {X:1} |
| 0.0021 | mono {Give:1} |
| 0.0013 | mono {and(X,X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Keep:1}
    - 3.77e-04 -> mono {X:1}   via X (3.77e-04, rho=1.21e-03 k*=10)
    - 3.69e-04 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-04, rho=1.00e-01 k*=10)
    - 3.67e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-04, rho=1.00e-01 k*=10)
    - 2.44e-04 -> mono {THEM(^Give):1}   via THEM(^Give) (2.44e-04, rho=2.68e-01 k*=10)
    - 1.84e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.84e-04, rho=2.08e-01 k*=10)
    - 1.10e-04 -> mono {and(X,X):1}   via and(X,X) (1.10e-04, rho=1.46e-02 k*=10)
- mono {THEM(^Give):1}
    - 3.29e-02 -> mono {Give:1}   via Give (3.29e-02, rho=1.00e-01 k*=10)
    - 1.19e-03 -> mono {X:1}   via X (1.19e-03, rho=3.81e-03 k*=10)
    - 6.70e-04 -> mono {THEM(^Keep):1}   via THEM(^Keep) (6.70e-04, rho=7.36e-01 k*=10)
    - 4.30e-04 -> mono {THEM(^X):1}   via THEM(^X) (4.30e-04, rho=4.87e-01 k*=10)
    - 1.65e-04 -> mono {or(X,X):1}   via or(X,X) (1.65e-04, rho=2.19e-02 k*=10)
    - 2.96e-05 -> mono {Keep:1}   via Keep (2.96e-05, rho=8.99e-05 k*=10)
- mono {X:1}
    - 1.60e-01 -> mono {Keep:1}   via Keep (1.60e-01, rho=4.87e-01 k*=10)
    - 2.22e-03 -> mono {and(X,X):1}   via and(X,X) (2.22e-03, rho=2.94e-01 k*=10)
    - 3.97e-04 -> mono {Give:1}   via Give (3.97e-04, rho=1.21e-03 k*=10)
    - 1.89e-04 -> mono {THEM(^Give):1}   via THEM(^Give) (1.89e-04, rho=2.08e-01 k*=10)
    - 1.12e-04 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.12e-04, rho=3.96e-01 k*=10)
    - 1.12e-04 -> mono {and(THEM(ME),Keep):1}   via and(THEM(ME),Keep) (1.12e-04, rho=4.87e-01 k*=10)
- mono {Give:1}
    - 2.42e-01 -> mono {Keep:1}   via Keep (2.42e-01, rho=7.36e-01 k*=10)
    - 1.52e-01 -> mono {X:1}   via X (1.52e-01, rho=4.87e-01 k*=10)
    - 4.77e-03 -> mono {and(X,X):1}   via and(X,X) (4.77e-03, rho=6.32e-01 k*=10)
    - 2.22e-03 -> mono {or(X,X):1}   via or(X,X) (2.22e-03, rho=2.94e-01 k*=10)
    - 5.86e-04 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (5.86e-04, rho=7.36e-01 k*=10)
    - 5.86e-04 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (5.86e-04, rho=7.36e-01 k*=10)
- mono {and(X,X):1}
    - 9.67e-02 -> mono {Keep:1}   via Keep (9.67e-02, rho=2.94e-01 k*=10)
    - 4.57e-03 -> mono {X:1}   via X (4.57e-03, rho=1.46e-02 k*=10)
    - 2.20e-04 -> mono {THEM(^Give):1}   via THEM(^Give) (2.20e-04, rho=2.42e-01 k*=10)
    - 1.48e-04 -> mono {THEM(ME):1}   via THEM(ME) (1.48e-04, rho=4.00e-02 k*=10)
    - 1.47e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (1.47e-04, rho=4.00e-02 k*=10)
    - 1.43e-04 -> mono {THEM(^X):1}   via THEM(^X) (1.43e-04, rho=1.62e-01 k*=10)
