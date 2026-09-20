### arm=weak, n=5, game=bos, N=10, w=1.0, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 54, states 533, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 1.40e-03
mean payoff 1.4758, efficient 1.5000, deadweight loss 0.0242, mean bits in support 3.06

| pi | state |
|---|---|
| 0.4835 | mono {A:1} |
| 0.4835 | mono {B:1} |
| 0.0186 | mono {X:1} |
| 0.0023 | poly {X:0.5, ROLE:0.1, not(ROLE):0.4} |
| 0.0016 | poly {X:0.7, not(ROLE):0.3} |
| 0.0013 | mono {not(ROLE):1} |
| 0.0011 | poly {X:0.1, ROLE:0.3, not(ROLE):0.6} |
| 0.0011 | poly {X:0.6, not(ROLE):0.4} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {A:1}
    - 2.15e-03 -> mono {X:1}   via X (2.15e-03, rho=9.31e-03 k*=10)
    - 1.97e-03 -> mono {B:1}   via B (1.97e-03, rho=7.91e-03 k*=10)
    - 4.72e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.72e-04, rho=9.93e-03 k*=10)
    - 8.76e-05 -> mono {or(X,X):1}   via or(X,X) (8.76e-05, rho=2.27e-02 k*=10)
    - 6.30e-05 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (6.30e-05, rho=3.58e-02 k*=10)
    - 4.39e-05 -> mono {THEM(^A):1}   via THEM(^A) (4.39e-05, rho=1.00e-01 k*=10)
- mono {B:1}
    - 2.15e-03 -> mono {X:1}   via X (2.15e-03, rho=9.31e-03 k*=10)
    - 1.97e-03 -> mono {A:1}   via A (1.97e-03, rho=7.91e-03 k*=10)
    - 4.72e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.72e-04, rho=9.93e-03 k*=10)
    - 8.76e-05 -> mono {and(X,X):1}   via and(X,X) (8.76e-05, rho=2.27e-02 k*=10)
    - 6.30e-05 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (6.30e-05, rho=3.58e-02 k*=10)
    - 4.39e-05 -> mono {THEM(^A):1}   via THEM(^A) (4.39e-05, rho=1.00e-01 k*=10)
- mono {X:1}
    - 4.66e-02 -> mono {A:1}   via A (4.66e-02, rho=1.87e-01 k*=10)
    - 4.66e-02 -> mono {B:1}   via B (4.66e-02, rho=1.87e-01 k*=10)
    - 1.99e-02 -> poly {X:0.7, not(ROLE):0.3}   via not(ROLE) (1.99e-02, rho=4.20e-01 k*=3)
    - 4.82e-04 -> mono {or(X,X):1}   via or(X,X) (4.82e-04, rho=1.25e-01 k*=10)
    - 4.82e-04 -> mono {and(X,X):1}   via and(X,X) (4.82e-04, rho=1.25e-01 k*=10)
    - 4.53e-04 -> mono {ROLE:1}   via ROLE (4.53e-04, rho=2.38e-03 k*=10)
- poly {X:0.5, ROLE:0.1, not(ROLE):0.4}
    - 4.22e-02 -> mono {A:1}   via A (4.22e-02, rho=1.69e-01 k*=10)
    - 4.22e-02 -> mono {B:1}   via B (4.22e-02, rho=1.69e-01 k*=10)
    - 1.02e-03 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via or(X,ROLE) (1.02e-03, rho=1.63e-01 k*=5)
    - 1.02e-03 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.02e-03, rho=1.63e-01 k*=5)
    - 8.54e-04 -> poly {ROLE:0.1, not(ROLE):0.6, THEM(THEM):0.3}   via THEM(THEM) (8.54e-04, rho=3.92e-01 k*=3)
    - 8.54e-04 -> poly {ROLE:0.1, not(ROLE):0.6, THEM(ME):0.3}   via THEM(ME) (8.54e-04, rho=3.92e-01 k*=3)
- poly {X:0.7, not(ROLE):0.3}
    - 1.90e-01 -> poly {X:0.6, not(ROLE):0.4}   via ROLE (1.90e-01, rho=1.00e+00 k*=1)
    - 4.22e-02 -> mono {A:1}   via A (4.22e-02, rho=1.69e-01 k*=10)
    - 4.22e-02 -> mono {B:1}   via B (4.22e-02, rho=1.69e-01 k*=10)
    - 1.02e-03 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via or(X,ROLE) (1.02e-03, rho=1.63e-01 k*=5)
    - 1.02e-03 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.02e-03, rho=1.63e-01 k*=5)
    - 7.61e-04 -> poly {not(ROLE):0.7, THEM(THEM):0.3}   via THEM(THEM) (7.61e-04, rho=3.49e-01 k*=3)
- mono {not(ROLE):1}
    - 1.09e-01 -> poly {ROLE:0.3, not(ROLE):0.7}   via ROLE (1.09e-01, rho=5.70e-01 k*=3)
    - 8.19e-02 -> mono {A:1}   via A (8.19e-02, rho=3.29e-01 k*=10)
    - 8.19e-02 -> mono {B:1}   via B (8.19e-02, rho=3.29e-01 k*=10)
    - 6.44e-02 -> poly {X:0.7, not(ROLE):0.3}   via X (6.44e-02, rho=2.78e-01 k*=7)
    - 2.53e-03 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via or(X,ROLE) (2.53e-03, rho=4.04e-01 k*=5)
    - 2.53e-03 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via and(X,ROLE) (2.53e-03, rho=4.04e-01 k*=5)
- poly {X:0.1, ROLE:0.3, not(ROLE):0.6}
    - 4.22e-02 -> mono {A:1}   via A (4.22e-02, rho=1.69e-01 k*=10)
    - 4.22e-02 -> mono {B:1}   via B (4.22e-02, rho=1.69e-01 k*=10)
    - 1.05e-03 -> poly {ROLE:0.1, not(ROLE):0.6, THEM(THEM):0.3}   via THEM(THEM) (1.05e-03, rho=4.80e-01 k*=3)
    - 1.05e-03 -> poly {ROLE:0.1, not(ROLE):0.6, THEM(ME):0.3}   via THEM(ME) (1.05e-03, rho=4.80e-01 k*=3)
    - 1.02e-03 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via or(X,ROLE) (1.02e-03, rho=1.63e-01 k*=5)
    - 1.02e-03 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.02e-03, rho=1.63e-01 k*=5)
- poly {X:0.6, not(ROLE):0.4}
    - 1.90e-01 -> poly {X:0.5, ROLE:0.1, not(ROLE):0.4}   via ROLE (1.90e-01, rho=1.00e+00 k*=1)
    - 4.32e-02 -> mono {A:1}   via A (4.32e-02, rho=1.73e-01 k*=10)
    - 4.32e-02 -> mono {B:1}   via B (4.32e-02, rho=1.73e-01 k*=10)
    - 1.11e-03 -> poly {not(ROLE):0.5, or(X,ROLE):0.5}   via or(X,ROLE) (1.11e-03, rho=1.77e-01 k*=5)
    - 1.11e-03 -> poly {not(ROLE):0.5, and(X,ROLE):0.5}   via and(X,ROLE) (1.11e-03, rho=1.77e-01 k*=5)
    - 1.10e-03 -> poly {X:0.7, not(ROLE):0.3}   via not(THEM(ME)) (4.03e-04, rho=1.00e+00 k*=1), not(THEM(THEM)) (4.03e-04, rho=1.00e+00 k*=1), not(THEM(^B)) (3.64e-05, rho=1.00e+00 k*=1), not(THEM(^A)) (3.64e-05, rho=1.00e+00 k*=1)
