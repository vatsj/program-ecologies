### arm=weak, n=5, game=zerosum, N=100, w=0.01, x_on=True, role=True, mode=square

programs 902, classes 53, states 53, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 0.00e+00
mean payoff 0.0000, efficient 0.0000, deadweight loss 0.0000, mean bits in support 3.33

| pi | state |
|---|---|
| 0.2866 | mono {D:1} |
| 0.2314 | mono {X:1} |
| 0.2162 | mono {C:1} |
| 0.1840 | mono {ROLE:1} |
| 0.0491 | mono {not(ROLE):1} |
| 0.0066 | mono {and(X,ROLE):1} |
| 0.0057 | mono {or(X,ROLE):1} |
| 0.0041 | mono {and(X,X):1} |
| 0.0036 | mono {or(X,X):1} |
| 0.0022 | mono {THEM(THEM):1} |
| 0.0022 | mono {THEM(ME):1} |
| 0.0019 | mono {not(or(X,ROLE)):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.11e-03 -> mono {ROLE:1}   via ROLE (1.11e-03, rho=5.81e-03 k*=100)
    - 7.50e-04 -> mono {not(ROLE):1}   via not(ROLE) (7.50e-04, rho=1.58e-02 k*=100)
    - 4.82e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (4.82e-05, rho=7.70e-03 k*=100)
    - 4.82e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (4.82e-05, rho=7.70e-03 k*=100)
- mono {X:1}
    - 2.49e-03 -> mono {D:1}   via D (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
    - 6.26e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-05, rho=1.00e-02 k*=100)
    - 6.26e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (6.26e-05, rho=1.00e-02 k*=100)
- mono {C:1}
    - 3.01e-03 -> mono {ROLE:1}   via ROLE (3.01e-03, rho=1.58e-02 k*=100)
    - 2.49e-03 -> mono {D:1}   via D (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 2.76e-04 -> mono {not(ROLE):1}   via not(ROLE) (2.76e-04, rho=5.81e-03 k*=100)
    - 7.95e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.95e-05, rho=1.27e-02 k*=100)
    - 7.95e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (7.95e-05, rho=1.27e-02 k*=100)
- mono {ROLE:1}
    - 3.93e-03 -> mono {D:1}   via D (3.93e-03, rho=1.58e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.45e-03 -> mono {C:1}   via C (1.45e-03, rho=5.81e-03 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
    - 7.95e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (7.95e-05, rho=1.27e-02 k*=100)
    - 4.91e-05 -> mono {and(X,X):1}   via and(X,X) (4.91e-05, rho=1.27e-02 k*=100)
- mono {not(ROLE):1}
    - 3.93e-03 -> mono {C:1}   via C (3.93e-03, rho=1.58e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 1.45e-03 -> mono {D:1}   via D (1.45e-03, rho=5.81e-03 k*=100)
    - 7.95e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.95e-05, rho=1.27e-02 k*=100)
    - 4.91e-05 -> mono {or(X,X):1}   via or(X,X) (4.91e-05, rho=1.27e-02 k*=100)
- mono {and(X,ROLE):1}
    - 3.16e-03 -> mono {D:1}   via D (3.16e-03, rho=1.27e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.92e-03 -> mono {C:1}   via C (1.92e-03, rho=7.70e-03 k*=100)
    - 1.47e-03 -> mono {ROLE:1}   via ROLE (1.47e-03, rho=7.70e-03 k*=100)
    - 6.03e-04 -> mono {not(ROLE):1}   via not(ROLE) (6.03e-04, rho=1.27e-02 k*=100)
    - 4.82e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (4.82e-05, rho=7.70e-03 k*=100)
- mono {or(X,ROLE):1}
    - 3.16e-03 -> mono {D:1}   via D (3.16e-03, rho=1.27e-02 k*=100)
    - 2.42e-03 -> mono {ROLE:1}   via ROLE (2.42e-03, rho=1.27e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.92e-03 -> mono {C:1}   via C (1.92e-03, rho=7.70e-03 k*=100)
    - 3.66e-04 -> mono {not(ROLE):1}   via not(ROLE) (3.66e-04, rho=7.70e-03 k*=100)
    - 7.95e-05 -> mono {and(X,ROLE):1}   via and(X,ROLE) (7.95e-05, rho=1.27e-02 k*=100)
- mono {and(X,X):1}
    - 2.49e-03 -> mono {D:1}   via D (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.47e-03 -> mono {ROLE:1}   via ROLE (1.47e-03, rho=7.70e-03 k*=100)
    - 6.03e-04 -> mono {not(ROLE):1}   via not(ROLE) (6.03e-04, rho=1.27e-02 k*=100)
    - 5.51e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (5.51e-05, rho=8.80e-03 k*=100)
- mono {or(X,X):1}
    - 2.49e-03 -> mono {D:1}   via D (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 2.42e-03 -> mono {ROLE:1}   via ROLE (2.42e-03, rho=1.27e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 3.66e-04 -> mono {not(ROLE):1}   via not(ROLE) (3.66e-04, rho=7.70e-03 k*=100)
    - 7.07e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.07e-05, rho=1.13e-02 k*=100)
- mono {THEM(THEM):1}
    - 2.49e-03 -> mono {D:1}   via D (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
    - 7.95e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.95e-05, rho=1.27e-02 k*=100)
- mono {THEM(ME):1}
    - 2.49e-03 -> mono {D:1}   via D (2.49e-03, rho=1.00e-02 k*=100)
    - 2.49e-03 -> mono {C:1}   via C (2.49e-03, rho=1.00e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.90e-03 -> mono {ROLE:1}   via ROLE (1.90e-03, rho=1.00e-02 k*=100)
    - 4.75e-04 -> mono {not(ROLE):1}   via not(ROLE) (4.75e-04, rho=1.00e-02 k*=100)
    - 7.95e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (7.95e-05, rho=1.27e-02 k*=100)
- mono {not(or(X,ROLE)):1}
    - 3.16e-03 -> mono {C:1}   via C (3.16e-03, rho=1.27e-02 k*=100)
    - 2.31e-03 -> mono {X:1}   via X (2.31e-03, rho=1.00e-02 k*=100)
    - 1.92e-03 -> mono {D:1}   via D (1.92e-03, rho=7.70e-03 k*=100)
    - 1.47e-03 -> mono {ROLE:1}   via ROLE (1.47e-03, rho=7.70e-03 k*=100)
    - 6.03e-04 -> mono {not(ROLE):1}   via not(ROLE) (6.03e-04, rho=1.27e-02 k*=100)
    - 6.26e-05 -> mono {or(X,ROLE):1}   via or(X,ROLE) (6.26e-05, rho=1.00e-02 k*=100)
