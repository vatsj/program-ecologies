### arm=weak, n=6, game=dollar, N=100, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 1852, classes 46, states 80, terminal classes 1, indeterminate 0, divergence rate 0.0019, flow into polymorphic targets 2.32e-09
mean payoff 0.4981, efficient 0.5000, deadweight loss 0.0019, mean bits in support 2.83

| pi | state |
|---|---|
| 0.9622 | mono {Half:1} |
| 0.0108 | mono {THEM(ME):1} |
| 0.0107 | mono {THEM(THEM):1} |
| 0.0037 | mono {X:1} |
| 0.0027 | mono {THEM(^Half):1} |
| 0.0023 | mono {not(THEM(ME)):1} |
| 0.0023 | mono {not(THEM(THEM)):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Half:1}
    - 5.49e-05 -> mono {X:1}   via X (5.49e-05, rho=1.76e-04 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 9.42e-06 -> mono {or(X,X):1}   via or(X,X) (9.42e-06, rho=1.25e-03 k*=100)
    - 9.10e-06 -> mono {THEM(^Half):1}   via THEM(^Half) (9.10e-06, rho=1.00e-02 k*=100)
    - 6.37e-06 -> mono {Greedy:1}   via Greedy (6.37e-06, rho=1.94e-05 k*=100)
- mono {THEM(ME):1}
    - 3.29e-03 -> mono {Half:1}   via Half (3.29e-03, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 3.30e-05 -> mono {X:1}   via X (3.30e-05, rho=1.06e-04 k*=100)
    - 9.10e-06 -> mono {THEM(^Half):1}   via THEM(^Half) (9.10e-06, rho=1.00e-02 k*=100)
    - 7.95e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (7.95e-06, rho=1.00e-02 k*=100)
    - 7.95e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.95e-06, rho=1.00e-02 k*=100)
- mono {THEM(THEM):1}
    - 3.29e-03 -> mono {Half:1}   via Half (3.29e-03, rho=1.00e-02 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.30e-05 -> mono {X:1}   via X (3.30e-05, rho=1.06e-04 k*=100)
    - 9.10e-06 -> mono {THEM(^Half):1}   via THEM(^Half) (9.10e-06, rho=1.00e-02 k*=100)
    - 7.95e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (7.95e-06, rho=1.00e-02 k*=100)
    - 7.95e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.95e-06, rho=1.00e-02 k*=100)
- mono {X:1}
    - 1.43e-02 -> mono {Half:1}   via Half (1.43e-02, rho=4.36e-02 k*=100)
    - 8.46e-04 -> mono {Greedy:1}   via Greedy (8.46e-04, rho=2.57e-03 k*=100)
    - 1.79e-04 -> mono {or(X,X):1}   via or(X,X) (1.79e-04, rho=2.37e-02 k*=100)
    - 9.68e-05 -> mono {THEM(ME):1}   via THEM(ME) (9.68e-05, rho=2.62e-02 k*=100)
    - 9.61e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (9.61e-05, rho=2.62e-02 k*=100)
    - 3.25e-05 -> mono {and(X,X):1}   via and(X,X) (3.25e-05, rho=4.30e-03 k*=100)
- mono {THEM(^Half):1}
    - 3.29e-03 -> mono {Half:1}   via Half (3.29e-03, rho=1.00e-02 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 3.30e-05 -> mono {X:1}   via X (3.30e-05, rho=1.06e-04 k*=100)
    - 6.37e-06 -> mono {Greedy:1}   via Greedy (6.37e-06, rho=1.94e-05 k*=100)
    - 6.16e-06 -> mono {or(X,X):1}   via or(X,X) (6.16e-06, rho=8.16e-04 k*=100)
- mono {not(THEM(ME)):1}
    - 1.77e-04 -> mono {Half:1}   via Half (1.77e-04, rho=5.39e-04 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 3.30e-05 -> mono {X:1}   via X (3.30e-05, rho=1.06e-04 k*=100)
    - 7.95e-06 -> mono {not(THEM(THEM)):1}   via not(THEM(THEM)) (7.95e-06, rho=1.00e-02 k*=100)
    - 6.37e-06 -> mono {Greedy:1}   via Greedy (6.37e-06, rho=1.94e-05 k*=100)
- mono {not(THEM(THEM)):1}
    - 1.77e-04 -> mono {Half:1}   via Half (1.77e-04, rho=5.39e-04 k*=100)
    - 3.69e-05 -> mono {THEM(ME):1}   via THEM(ME) (3.69e-05, rho=1.00e-02 k*=100)
    - 3.67e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (3.67e-05, rho=1.00e-02 k*=100)
    - 3.30e-05 -> mono {X:1}   via X (3.30e-05, rho=1.06e-04 k*=100)
    - 7.95e-06 -> mono {not(THEM(ME)):1}   via not(THEM(ME)) (7.95e-06, rho=1.00e-02 k*=100)
    - 6.37e-06 -> mono {Greedy:1}   via Greedy (6.37e-06, rho=1.94e-05 k*=100)
