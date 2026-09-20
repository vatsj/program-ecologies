### arm=weak, n=5, game=bos, N=100, w=0.3, x_on=True, role=True, mode=square, fmap=exp

programs 902, classes 54, states 382, terminal classes 1, indeterminate 0, divergence rate 0.0010, flow into polymorphic targets 5.42e-06
mean payoff 1.4996, efficient 1.5000, deadweight loss 0.0004, mean bits in support 3.03

| pi | state |
|---|---|
| 0.4980 | mono {B:1} |
| 0.4980 | mono {A:1} |
| 0.0011 | poly {not(ROLE):0.33, THEM(^A):0.67} |
| 0.0011 | poly {not(ROLE):0.33, THEM(^B):0.67} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {B:1}
    - 4.39e-06 -> mono {THEM(^A):1}   via THEM(^A) (4.39e-06, rho=1.00e-02 k*=100)
    - 4.39e-06 -> mono {THEM(^B):1}   via THEM(^B) (4.39e-06, rho=1.00e-02 k*=100)
    - 3.64e-07 -> mono {and(ROLE,THEM(THEM)):1}   via and(ROLE,THEM(THEM)) (3.64e-07, rho=1.00e-02 k*=100)
    - 3.64e-07 -> mono {and(ROLE,THEM(ME)):1}   via and(ROLE,THEM(ME)) (3.64e-07, rho=1.00e-02 k*=100)
    - 3.64e-07 -> mono {and(X,THEM(THEM)):1}   via and(X,THEM(THEM)) (3.64e-07, rho=1.00e-02 k*=100)
    - 3.64e-07 -> mono {and(X,THEM(ME)):1}   via and(X,THEM(ME)) (3.64e-07, rho=1.00e-02 k*=100)
- mono {A:1}
    - 4.39e-06 -> mono {THEM(^A):1}   via THEM(^A) (4.39e-06, rho=1.00e-02 k*=100)
    - 4.39e-06 -> mono {THEM(^B):1}   via THEM(^B) (4.39e-06, rho=1.00e-02 k*=100)
    - 3.64e-07 -> mono {or(ROLE,THEM(THEM)):1}   via or(ROLE,THEM(THEM)) (3.64e-07, rho=1.00e-02 k*=100)
    - 3.64e-07 -> mono {or(ROLE,THEM(ME)):1}   via or(ROLE,THEM(ME)) (3.64e-07, rho=1.00e-02 k*=100)
    - 3.64e-07 -> mono {or(X,THEM(THEM)):1}   via or(X,THEM(THEM)) (3.64e-07, rho=1.00e-02 k*=100)
    - 3.64e-07 -> mono {or(X,THEM(ME)):1}   via or(X,THEM(ME)) (3.64e-07, rho=1.00e-02 k*=100)
- poly {not(ROLE):0.33, THEM(^A):0.67}
    - 9.99e-04 -> mono {A:1}   via A (9.99e-04, rho=4.01e-03 k*=100)
    - 9.99e-04 -> mono {B:1}   via B (9.99e-04, rho=4.01e-03 k*=100)
    - 3.64e-05 -> poly {not(ROLE):0.33, THEM(^A):0.66, or(ROLE,THEM(THEM)):0.01}   via or(ROLE,THEM(THEM)) (3.64e-05, rho=1.00e+00 k*=1)
    - 3.64e-05 -> poly {not(ROLE):0.33, THEM(^A):0.66, or(ROLE,THEM(ME)):0.01}   via or(ROLE,THEM(ME)) (3.64e-05, rho=1.00e+00 k*=1)
    - 3.41e-07 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (3.41e-07, rho=1.94e-04 k*=100)
    - 3.41e-07 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (3.41e-07, rho=1.94e-04 k*=100)
- poly {not(ROLE):0.33, THEM(^B):0.67}
    - 9.99e-04 -> mono {A:1}   via A (9.99e-04, rho=4.01e-03 k*=100)
    - 9.99e-04 -> mono {B:1}   via B (9.99e-04, rho=4.01e-03 k*=100)
    - 3.64e-05 -> poly {not(ROLE):0.33, THEM(^B):0.66, and(ROLE,THEM(THEM)):0.01}   via and(ROLE,THEM(THEM)) (3.64e-05, rho=1.00e+00 k*=1)
    - 3.64e-05 -> poly {not(ROLE):0.33, THEM(^B):0.66, and(ROLE,THEM(ME)):0.01}   via and(ROLE,THEM(ME)) (3.64e-05, rho=1.00e+00 k*=1)
    - 3.41e-07 -> mono {not(or(X,ROLE)):1}   via not(or(X,ROLE)) (3.41e-07, rho=1.94e-04 k*=100)
    - 3.41e-07 -> mono {not(and(X,ROLE)):1}   via not(and(X,ROLE)) (3.41e-07, rho=1.94e-04 k*=100)
