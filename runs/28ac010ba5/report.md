### arm=weak, n=5, game=bos, N=10, w=0.3, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 54, states 709, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 8.49e-03
mean payoff 1.3066, efficient 1.5000, deadweight loss 0.1934, mean bits in support 3.23

| pi | state |
|---|---|
| 0.3875 | mono {B:1} |
| 0.3875 | mono {A:1} |
| 0.1185 | mono {X:1} |
| 0.0199 | mono {ROLE:1} |
| 0.0197 | poly {X:0.5, ROLE:0.1, not(ROLE):0.4} |
| 0.0129 | poly {X:0.1, ROLE:0.3, not(ROLE):0.6} |
| 0.0101 | mono {not(ROLE):1} |
| 0.0095 | poly {X:0.7, not(ROLE):0.3} |
| 0.0070 | poly {X:0.6, not(ROLE):0.4} |
| 0.0038 | poly {ROLE:0.3, not(ROLE):0.7} |
| 0.0023 | mono {or(X,ROLE):1} |
| 0.0023 | mono {and(X,ROLE):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {B:1}
    - 1.29e-02 -> mono {A:1}   via A (1.29e-02, rho=5.16e-02 k*=10)
    - 1.22e-02 -> mono {X:1}   via X (1.22e-02, rho=5.26e-02 k*=10)
    - 3.90e-03 -> mono {ROLE:1}   via ROLE (3.90e-03, rho=2.05e-02 k*=10)
    - 2.66e-03 -> mono {not(ROLE):1}   via not(ROLE) (2.66e-03, rho=5.60e-02 k*=10)
    - 3.05e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (3.05e-04, rho=4.87e-02 k*=10)
    - 2.59e-04 -> mono {and(X,X):1}   via and(X,X) (2.59e-04, rho=6.72e-02 k*=10)
- mono {A:1}
    - 1.29e-02 -> mono {B:1}   via B (1.29e-02, rho=5.16e-02 k*=10)
    - 1.22e-02 -> mono {X:1}   via X (1.22e-02, rho=5.26e-02 k*=10)
    - 3.90e-03 -> mono {ROLE:1}   via ROLE (3.90e-03, rho=2.05e-02 k*=10)
    - 2.66e-03 -> mono {not(ROLE):1}   via not(ROLE) (2.66e-03, rho=5.60e-02 k*=10)
    - 3.05e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (3.05e-04, rho=4.87e-02 k*=10)
    - 2.59e-04 -> mono {or(X,X):1}   via or(X,X) (2.59e-04, rho=6.72e-02 k*=10)
- mono {X:1}
    - 3.22e-02 -> mono {A:1}   via A (3.22e-02, rho=1.29e-01 k*=10)
    - 3.22e-02 -> mono {B:1}   via B (3.22e-02, rho=1.29e-01 k*=10)
    - 1.70e-02 -> poly {X:0.7, not(ROLE):0.3}   via not(ROLE) (1.70e-02, rho=3.59e-01 k*=3)
    - 8.35e-03 -> mono {ROLE:1}   via ROLE (8.35e-03, rho=4.38e-02 k*=10)
    - 5.15e-04 -> mono {or(X,ROLE):1}   via or(X,ROLE) (5.15e-04, rho=8.23e-02 k*=10)
    - 5.15e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (5.15e-04, rho=8.23e-02 k*=10)
- mono {ROLE:1}
    - 6.53e-02 -> mono {A:1}   via A (6.53e-02, rho=2.62e-01 k*=10)
    - 6.53e-02 -> mono {B:1}   via B (6.53e-02, rho=2.62e-01 k*=10)
    - 5.28e-02 -> mono {X:1}   via X (5.28e-02, rho=2.28e-01 k*=10)
    - 1.78e-02 -> poly {ROLE:0.3, not(ROLE):0.7}   via not(ROLE) (1.78e-02, rho=3.75e-01 k*=7)
    - 1.09e-03 -> mono {or(X,ROLE):1}   via or(X,ROLE) (1.09e-03, rho=1.74e-01 k*=10)
    - 1.09e-03 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.09e-03, rho=1.74e-01 k*=10)
- poly {X:0.5, ROLE:0.1, not(ROLE):0.4}
    - 3.08e-02 -> mono {A:1}   via A (3.08e-02, rho=1.24e-01 k*=10)
    - 3.08e-02 -> mono {B:1}   via B (3.08e-02, rho=1.24e-01 k*=10)
    - 1.18e-03 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via or(X,ROLE) (1.18e-03, rho=1.89e-01 k*=5)
    - 1.18e-03 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.18e-03, rho=1.89e-01 k*=5)
    - 7.64e-04 -> poly {ROLE:0.1, not(ROLE):0.6, THEM(THEM):0.3}   via THEM(THEM) (7.64e-04, rho=3.50e-01 k*=3)
    - 7.64e-04 -> poly {ROLE:0.1, not(ROLE):0.6, THEM(ME):0.3}   via THEM(ME) (7.64e-04, rho=3.50e-01 k*=3)
- poly {X:0.1, ROLE:0.3, not(ROLE):0.6}
    - 3.08e-02 -> mono {A:1}   via A (3.08e-02, rho=1.24e-01 k*=10)
    - 3.08e-02 -> mono {B:1}   via B (3.08e-02, rho=1.24e-01 k*=10)
    - 1.18e-03 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via or(X,ROLE) (1.18e-03, rho=1.89e-01 k*=5)
    - 1.18e-03 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.18e-03, rho=1.89e-01 k*=5)
    - 8.19e-04 -> poly {ROLE:0.1, not(ROLE):0.6, THEM(THEM):0.3}   via THEM(THEM) (8.19e-04, rho=3.76e-01 k*=3)
    - 8.19e-04 -> poly {ROLE:0.1, not(ROLE):0.6, THEM(ME):0.3}   via THEM(ME) (8.19e-04, rho=3.76e-01 k*=3)
- mono {not(ROLE):1}
    - 7.66e-02 -> poly {ROLE:0.3, not(ROLE):0.7}   via ROLE (7.66e-02, rho=4.02e-01 k*=3)
    - 4.11e-02 -> poly {X:0.7, not(ROLE):0.3}   via X (4.11e-02, rho=1.78e-01 k*=7)
    - 3.98e-02 -> mono {A:1}   via A (3.98e-02, rho=1.60e-01 k*=10)
    - 3.98e-02 -> mono {B:1}   via B (3.98e-02, rho=1.60e-01 k*=10)
    - 1.59e-03 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via or(X,ROLE) (1.59e-03, rho=2.54e-01 k*=5)
    - 1.59e-03 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.59e-03, rho=2.54e-01 k*=5)
- poly {X:0.7, not(ROLE):0.3}
    - 1.90e-01 -> poly {X:0.6, not(ROLE):0.4}   via ROLE (1.90e-01, rho=1.00e+00 k*=1)
    - 3.08e-02 -> mono {A:1}   via A (3.08e-02, rho=1.24e-01 k*=10)
    - 3.08e-02 -> mono {B:1}   via B (3.08e-02, rho=1.24e-01 k*=10)
    - 1.18e-03 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via or(X,ROLE) (1.18e-03, rho=1.89e-01 k*=5)
    - 1.18e-03 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.18e-03, rho=1.89e-01 k*=5)
    - 7.37e-04 -> poly {not(ROLE):0.7, THEM(THEM):0.3}   via THEM(THEM) (7.37e-04, rho=3.38e-01 k*=3)
- poly {X:0.6, not(ROLE):0.4}
    - 1.90e-01 -> poly {X:0.5, ROLE:0.1, not(ROLE):0.4}   via ROLE (1.90e-01, rho=1.00e+00 k*=1)
    - 3.09e-02 -> mono {A:1}   via A (3.09e-02, rho=1.24e-01 k*=10)
    - 3.09e-02 -> mono {B:1}   via B (3.09e-02, rho=1.24e-01 k*=10)
    - 1.21e-03 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via or(X,ROLE) (1.21e-03, rho=1.93e-01 k*=5)
    - 1.21e-03 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.21e-03, rho=1.93e-01 k*=5)
    - 1.10e-03 -> poly {X:0.7, not(ROLE):0.3}   via not(THEM(ME)) (4.03e-04, rho=1.00e+00 k*=1), not(THEM(THEM)) (4.03e-04, rho=1.00e+00 k*=1), not(THEM(^B)) (3.64e-05, rho=1.00e+00 k*=1), not(THEM(^A)) (3.64e-05, rho=1.00e+00 k*=1)
- poly {ROLE:0.3, not(ROLE):0.7}
    - 2.31e-01 -> poly {X:0.1, ROLE:0.3, not(ROLE):0.6}   via X (2.31e-01, rho=1.00e+00 k*=1)
    - 3.09e-02 -> mono {A:1}   via A (3.09e-02, rho=1.24e-01 k*=10)
    - 3.09e-02 -> mono {B:1}   via B (3.09e-02, rho=1.24e-01 k*=10)
    - 1.21e-03 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via or(X,ROLE) (1.21e-03, rho=1.93e-01 k*=5)
    - 1.21e-03 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.21e-03, rho=1.93e-01 k*=5)
    - 8.30e-04 -> poly {ROLE:0.1, not(ROLE):0.6, THEM(THEM):0.3}   via THEM(THEM) (8.30e-04, rho=3.81e-01 k*=3)
- mono {or(X,ROLE):1}
    - 4.34e-02 -> mono {A:1}   via A (4.34e-02, rho=1.74e-01 k*=10)
    - 3.20e-02 -> mono {B:1}   via B (3.20e-02, rho=1.29e-01 k*=10)
    - 2.77e-02 -> mono {X:1}   via X (2.77e-02, rho=1.20e-01 k*=10)
    - 1.32e-02 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via not(ROLE) (1.32e-02, rho=2.77e-01 k*=5)
    - 9.28e-03 -> mono {ROLE:1}   via ROLE (9.28e-03, rho=4.87e-02 k*=10)
    - 6.75e-04 -> poly {or(X,ROLE):0.6, THEM(THEM):0.4}   via THEM(THEM) (6.75e-04, rho=3.09e-01 k*=4)
- mono {and(X,ROLE):1}
    - 4.34e-02 -> mono {B:1}   via B (4.34e-02, rho=1.74e-01 k*=10)
    - 3.20e-02 -> mono {A:1}   via A (3.20e-02, rho=1.29e-01 k*=10)
    - 2.77e-02 -> mono {X:1}   via X (2.77e-02, rho=1.20e-01 k*=10)
    - 1.32e-02 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via not(ROLE) (1.32e-02, rho=2.77e-01 k*=5)
    - 9.28e-03 -> mono {ROLE:1}   via ROLE (9.28e-03, rho=4.87e-02 k*=10)
    - 6.75e-04 -> poly {and(X,ROLE):0.6, THEM(THEM):0.4}   via THEM(THEM) (6.75e-04, rho=3.09e-01 k*=4)
