### arm=weak, n=6, game=pd, N=100, w=0.1, x_on=True, role=True, mode=square, fmap=exp

programs 3994, classes 112, states 493, terminal classes 1, indeterminate 0, divergence rate 0.0006, flow into polymorphic targets 7.92e-08
mean payoff -0.9855, efficient 0.0000, deadweight loss 0.9855, mean bits in support 3.11

| pi | state |
|---|---|
| 0.9709 | mono {D:1} |
| 0.0077 | mono {X:1} |
| 0.0063 | mono {ROLE:1} |
| 0.0037 | mono {THEM(^C):1} |
| 0.0022 | mono {and(X,ROLE):1} |
| 0.0016 | mono {not(ROLE):1} |
| 0.0014 | mono {and(X,X):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 7.34e-05 -> mono {X:1}   via X (7.34e-05, rho=3.21e-04 k*=100)
    - 6.03e-05 -> mono {ROLE:1}   via ROLE (6.03e-05, rho=3.21e-04 k*=100)
    - 2.17e-05 -> mono {THEM(ME):1}   via THEM(ME) (2.17e-05, rho=1.00e-02 k*=100)
    - 2.16e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.16e-05, rho=1.00e-02 k*=100)
    - 1.53e-05 -> mono {not(ROLE):1}   via not(ROLE) (1.53e-05, rho=3.21e-04 k*=100)
    - 1.45e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.45e-05, rho=2.19e-03 k*=100)
- mono {X:1}
    - 1.25e-02 -> mono {D:1}   via D (1.25e-02, rho=5.00e-02 k*=100)
    - 1.88e-03 -> mono {ROLE:1}   via ROLE (1.88e-03, rho=1.00e-02 k*=100)
    - 4.78e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.78e-04, rho=1.00e-02 k*=100)
    - 1.81e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.81e-04, rho=2.73e-02 k*=100)
    - 1.15e-04 -> mono {and(X,X):1}   via and(X,X) (1.15e-04, rho=2.73e-02 k*=100)
    - 7.99e-05 -> mono {C:1}   via C (7.99e-05, rho=3.21e-04 k*=100)
- mono {ROLE:1}
    - 1.25e-02 -> mono {D:1}   via D (1.25e-02, rho=5.00e-02 k*=100)
    - 2.29e-03 -> mono {X:1}   via X (2.29e-03, rho=1.00e-02 k*=100)
    - 4.78e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.78e-04, rho=1.00e-02 k*=100)
    - 1.81e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.81e-04, rho=2.73e-02 k*=100)
    - 1.15e-04 -> mono {and(X,X):1}   via and(X,X) (1.15e-04, rho=2.73e-02 k*=100)
    - 7.99e-05 -> mono {C:1}   via C (7.99e-05, rho=3.21e-04 k*=100)
- mono {THEM(^C):1}
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 3.57e-04 -> mono {X:1}   via X (3.57e-04, rho=1.56e-03 k*=100)
    - 2.93e-04 -> mono {ROLE:1}   via ROLE (2.93e-04, rho=1.56e-03 k*=100)
    - 7.45e-05 -> mono {not(ROLE):1}   via not(ROLE) (7.45e-05, rho=1.56e-03 k*=100)
    - 5.00e-05 -> mono {THEM(^D):1}   via THEM(^D) (5.00e-05, rho=9.70e-02 k*=100)
    - 4.60e-05 -> mono {D:1}   via D (4.60e-05, rho=1.84e-04 k*=100)
- mono {and(X,ROLE):1}
    - 6.81e-03 -> mono {D:1}   via D (6.81e-03, rho=2.73e-02 k*=100)
    - 5.00e-04 -> mono {X:1}   via X (5.00e-04, rho=2.19e-03 k*=100)
    - 4.11e-04 -> mono {ROLE:1}   via ROLE (4.11e-04, rho=2.19e-03 k*=100)
    - 1.04e-04 -> mono {not(ROLE):1}   via not(ROLE) (1.04e-04, rho=2.19e-03 k*=100)
    - 4.21e-05 -> mono {and(X,X):1}   via and(X,X) (4.21e-05, rho=1.00e-02 k*=100)
    - 2.28e-05 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (2.28e-05, rho=1.00e-02 k*=100)
- mono {not(ROLE):1}
    - 1.25e-02 -> mono {D:1}   via D (1.25e-02, rho=5.00e-02 k*=100)
    - 2.29e-03 -> mono {X:1}   via X (2.29e-03, rho=1.00e-02 k*=100)
    - 1.88e-03 -> mono {ROLE:1}   via ROLE (1.88e-03, rho=1.00e-02 k*=100)
    - 1.81e-04 -> mono {and(X,ROLE):1}   via and(X,ROLE) (1.81e-04, rho=2.73e-02 k*=100)
    - 1.15e-04 -> mono {and(X,X):1}   via and(X,X) (1.15e-04, rho=2.73e-02 k*=100)
    - 7.99e-05 -> mono {C:1}   via C (7.99e-05, rho=3.21e-04 k*=100)
- mono {and(X,X):1}
    - 6.81e-03 -> mono {D:1}   via D (6.81e-03, rho=2.73e-02 k*=100)
    - 5.00e-04 -> mono {X:1}   via X (5.00e-04, rho=2.19e-03 k*=100)
    - 4.11e-04 -> mono {ROLE:1}   via ROLE (4.11e-04, rho=2.19e-03 k*=100)
    - 1.04e-04 -> mono {not(ROLE):1}   via not(ROLE) (1.04e-04, rho=2.19e-03 k*=100)
    - 6.62e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.62e-05, rho=1.00e-02 k*=100)
    - 2.28e-05 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (2.28e-05, rho=1.00e-02 k*=100)
