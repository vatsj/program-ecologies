### arm=weak, n=5, game=bos, N=10, w=0.1, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 54, states 742, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 1.23e-02
mean payoff 1.1275, efficient 1.5000, deadweight loss 0.3725, mean bits in support 3.33

| pi | state |
|---|---|
| 0.3056 | mono {B:1} |
| 0.3056 | mono {A:1} |
| 0.1686 | mono {X:1} |
| 0.0858 | mono {ROLE:1} |
| 0.0315 | poly {X:0.5, ROLE:0.1, not(ROLE):0.4} |
| 0.0243 | poly {X:0.1, ROLE:0.3, not(ROLE):0.6} |
| 0.0145 | mono {not(ROLE):1} |
| 0.0130 | poly {X:0.7, not(ROLE):0.3} |
| 0.0099 | poly {X:0.6, not(ROLE):0.4} |
| 0.0063 | poly {ROLE:0.3, not(ROLE):0.7} |
| 0.0042 | mono {or(X,ROLE):1} |
| 0.0042 | mono {and(X,ROLE):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {B:1}
    - 2.02e-02 -> mono {A:1}   via A (2.02e-02, rho=8.13e-02 k*=10)
    - 1.89e-02 -> mono {X:1}   via X (1.89e-02, rho=8.15e-02 k*=10)
    - 1.20e-02 -> mono {ROLE:1}   via ROLE (1.20e-02, rho=6.30e-02 k*=10)
    - 3.96e-03 -> mono {not(ROLE):1}   via not(ROLE) (3.96e-03, rho=8.34e-02 k*=10)
    - 5.01e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (5.01e-04, rho=8.01e-02 k*=10)
    - 4.53e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (4.53e-04, rho=7.24e-02 k*=10)
- mono {A:1}
    - 2.02e-02 -> mono {B:1}   via B (2.02e-02, rho=8.13e-02 k*=10)
    - 1.89e-02 -> mono {X:1}   via X (1.89e-02, rho=8.15e-02 k*=10)
    - 1.20e-02 -> mono {ROLE:1}   via ROLE (1.20e-02, rho=6.30e-02 k*=10)
    - 3.96e-03 -> mono {not(ROLE):1}   via not(ROLE) (3.96e-03, rho=8.34e-02 k*=10)
    - 5.01e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (5.01e-04, rho=8.01e-02 k*=10)
    - 4.53e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (4.53e-04, rho=7.24e-02 k*=10)
- mono {X:1}
    - 2.74e-02 -> mono {A:1}   via A (2.74e-02, rho=1.10e-01 k*=10)
    - 2.74e-02 -> mono {B:1}   via B (2.74e-02, rho=1.10e-01 k*=10)
    - 1.62e-02 -> poly {X:0.7, not(ROLE):0.3}   via not(ROLE) (1.62e-02, rho=3.42e-01 k*=3)
    - 1.50e-02 -> mono {ROLE:1}   via ROLE (1.50e-02, rho=7.86e-02 k*=10)
    - 5.87e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (5.87e-04, rho=9.39e-02 k*=10)
    - 5.87e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (5.87e-04, rho=9.39e-02 k*=10)
- mono {ROLE:1}
    - 3.67e-02 -> mono {A:1}   via A (3.67e-02, rho=1.47e-01 k*=10)
    - 3.67e-02 -> mono {B:1}   via B (3.67e-02, rho=1.47e-01 k*=10)
    - 3.15e-02 -> mono {X:1}   via X (3.15e-02, rho=1.36e-01 k*=10)
    - 9.87e-03 -> poly {ROLE:0.3, not(ROLE):0.7}   via not(ROLE) (9.87e-03, rho=2.08e-01 k*=7)
    - 7.67e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.67e-04, rho=1.23e-01 k*=10)
    - 7.67e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (7.67e-04, rho=1.23e-01 k*=10)
- poly {X:0.5, ROLE:0.1, not(ROLE):0.4}
    - 2.69e-02 -> mono {A:1}   via A (2.69e-02, rho=1.08e-01 k*=10)
    - 2.69e-02 -> mono {B:1}   via B (2.69e-02, rho=1.08e-01 k*=10)
    - 1.23e-03 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via or(X,ROLE) (1.23e-03, rho=1.96e-01 k*=5)
    - 1.23e-03 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.23e-03, rho=1.96e-01 k*=5)
    - 7.39e-04 -> poly {ROLE:0.1, not(ROLE):0.6, THEM(THEM):0.3}   via THEM(THEM) (7.39e-04, rho=3.39e-01 k*=3)
    - 7.39e-04 -> poly {ROLE:0.1, not(ROLE):0.6, THEM(ME):0.3}   via THEM(ME) (7.39e-04, rho=3.39e-01 k*=3)
- poly {X:0.1, ROLE:0.3, not(ROLE):0.6}
    - 2.69e-02 -> mono {A:1}   via A (2.69e-02, rho=1.08e-01 k*=10)
    - 2.69e-02 -> mono {B:1}   via B (2.69e-02, rho=1.08e-01 k*=10)
    - 1.23e-03 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via or(X,ROLE) (1.23e-03, rho=1.96e-01 k*=5)
    - 1.23e-03 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.23e-03, rho=1.96e-01 k*=5)
    - 7.57e-04 -> poly {ROLE:0.1, not(ROLE):0.6, THEM(THEM):0.3}   via THEM(THEM) (7.57e-04, rho=3.47e-01 k*=3)
    - 7.57e-04 -> poly {ROLE:0.1, not(ROLE):0.6, THEM(ME):0.3}   via THEM(ME) (7.57e-04, rho=3.47e-01 k*=3)
- mono {not(ROLE):1}
    - 6.78e-02 -> poly {ROLE:0.3, not(ROLE):0.7}   via ROLE (6.78e-02, rho=3.56e-01 k*=3)
    - 3.56e-02 -> poly {X:0.7, not(ROLE):0.3}   via X (3.56e-02, rho=1.54e-01 k*=7)
    - 2.95e-02 -> mono {A:1}   via A (2.95e-02, rho=1.18e-01 k*=10)
    - 2.95e-02 -> mono {B:1}   via B (2.95e-02, rho=1.18e-01 k*=10)
    - 1.36e-03 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via or(X,ROLE) (1.36e-03, rho=2.17e-01 k*=5)
    - 1.36e-03 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.36e-03, rho=2.17e-01 k*=5)
- poly {X:0.7, not(ROLE):0.3}
    - 1.90e-01 -> poly {X:0.6, not(ROLE):0.4}   via ROLE (1.90e-01, rho=1.00e+00 k*=1)
    - 2.69e-02 -> mono {A:1}   via A (2.69e-02, rho=1.08e-01 k*=10)
    - 2.69e-02 -> mono {B:1}   via B (2.69e-02, rho=1.08e-01 k*=10)
    - 1.23e-03 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via or(X,ROLE) (1.23e-03, rho=1.96e-01 k*=5)
    - 1.23e-03 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.23e-03, rho=1.96e-01 k*=5)
    - 7.30e-04 -> poly {not(ROLE):0.7, THEM(THEM):0.3}   via THEM(THEM) (7.30e-04, rho=3.35e-01 k*=3)
- poly {X:0.6, not(ROLE):0.4}
    - 1.90e-01 -> poly {X:0.5, ROLE:0.1, not(ROLE):0.4}   via ROLE (1.90e-01, rho=1.00e+00 k*=1)
    - 2.69e-02 -> mono {A:1}   via A (2.69e-02, rho=1.08e-01 k*=10)
    - 2.69e-02 -> mono {B:1}   via B (2.69e-02, rho=1.08e-01 k*=10)
    - 1.24e-03 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via or(X,ROLE) (1.24e-03, rho=1.98e-01 k*=5)
    - 1.24e-03 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.24e-03, rho=1.98e-01 k*=5)
    - 1.10e-03 -> poly {X:0.7, not(ROLE):0.3}   via not(THEM(ME)) (4.03e-04, rho=1.00e+00 k*=1), not(THEM(THEM)) (4.03e-04, rho=1.00e+00 k*=1), not(THEM(^B)) (3.64e-05, rho=1.00e+00 k*=1), not(THEM(^A)) (3.64e-05, rho=1.00e+00 k*=1)
- poly {ROLE:0.3, not(ROLE):0.7}
    - 2.31e-01 -> poly {X:0.1, ROLE:0.3, not(ROLE):0.6}   via X (2.31e-01, rho=1.00e+00 k*=1)
    - 2.69e-02 -> mono {A:1}   via A (2.69e-02, rho=1.08e-01 k*=10)
    - 2.69e-02 -> mono {B:1}   via B (2.69e-02, rho=1.08e-01 k*=10)
    - 1.24e-03 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via or(X,ROLE) (1.24e-03, rho=1.98e-01 k*=5)
    - 1.24e-03 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.24e-03, rho=1.98e-01 k*=5)
    - 7.61e-04 -> poly {ROLE:0.1, not(ROLE):0.6, THEM(THEM):0.3}   via THEM(THEM) (7.61e-04, rho=3.49e-01 k*=3)
- mono {or(X,ROLE):1}
    - 3.05e-02 -> mono {A:1}   via A (3.05e-02, rho=1.23e-01 k*=10)
    - 2.76e-02 -> mono {B:1}   via B (2.76e-02, rho=1.11e-01 k*=10)
    - 2.46e-02 -> mono {X:1}   via X (2.46e-02, rho=1.06e-01 k*=10)
    - 1.53e-02 -> mono {ROLE:1}   via ROLE (1.53e-02, rho=8.01e-02 k*=10)
    - 1.06e-02 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via not(ROLE) (1.06e-02, rho=2.24e-01 k*=5)
    - 5.95e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (5.95e-04, rho=9.51e-02 k*=10)
- mono {and(X,ROLE):1}
    - 3.05e-02 -> mono {B:1}   via B (3.05e-02, rho=1.23e-01 k*=10)
    - 2.76e-02 -> mono {A:1}   via A (2.76e-02, rho=1.11e-01 k*=10)
    - 2.46e-02 -> mono {X:1}   via X (2.46e-02, rho=1.06e-01 k*=10)
    - 1.53e-02 -> mono {ROLE:1}   via ROLE (1.53e-02, rho=8.01e-02 k*=10)
    - 1.06e-02 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via not(ROLE) (1.06e-02, rho=2.24e-01 k*=5)
    - 5.95e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (5.95e-04, rho=9.51e-02 k*=10)
