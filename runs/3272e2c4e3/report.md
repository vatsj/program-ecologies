### arm=strong, n=6, game=stag, N=1000, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 1726, classes 21, states 23, terminal classes 1, indeterminate 0, divergence rate 0.0004, flow into polymorphic targets 3.35e-13
mean payoff 3.9957, efficient 4.0000, deadweight loss 0.0043, mean bits in support 2.59

| pi | state |
|---|---|
| 0.9955 | mono {Stag:1} |
| 0.0042 | mono {Hare:1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {Stag:1}
    - 9.32e-08 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (9.32e-08, rho=1.00e-03 k*=1000)
    - 1.05e-08 -> mono {Hare:1}   via Hare (1.05e-08, rho=3.17e-08 k*=1000)
    - 5.10e-09 -> mono {X:1}   via X (5.10e-09, rho=1.62e-08 k*=1000)
    - 1.92e-10 -> mono {and(X,X):1}   via and(X,X) (1.92e-10, rho=2.40e-08 k*=1000)
    - 1.89e-10 -> mono {or(X,or(X,X)):1}   via or(X,or(X,X)) (1.89e-10, rho=6.27e-07 k*=1000)
    - 1.29e-10 -> mono {or(X,X):1}   via or(X,X) (1.29e-10, rho=1.62e-08 k*=1000)
- mono {Hare:1}
    - 3.84e-06 -> mono {THEM(ME):1}   via THEM(ME) (3.84e-06, rho=1.00e-03 k*=1000)
    - 1.22e-07 -> mono {and(THEM(ME),Hare):1}   via and(THEM(ME),Hare) (1.22e-07, rho=1.00e-03 k*=1000)
    - 9.32e-08 -> mono {and(THEM(ME),X):1}   via and(THEM(ME),X) (9.32e-08, rho=1.00e-03 k*=1000)
    - 9.32e-08 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (9.32e-08, rho=1.00e-03 k*=1000)
    - 1.13e-20 -> mono {and(X,and(X,X)):1}   via and(X,and(X,X)) (1.13e-20, rho=3.76e-17 k*=1000)
    - 1.63e-26 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (1.63e-26, rho=1.75e-22 k*=1000)
