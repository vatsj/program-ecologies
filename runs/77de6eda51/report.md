### arm=source, n=6, game=pd, N=100, w=1.0, x_on=True, role=False, mode=square

programs 2110, classes 220, states 3149, terminal classes 1, indeterminate 0, divergence rate 0.0014, flow into polymorphic targets 1.42e-17
mean payoff -0.1429, efficient 0.0000, deadweight loss 0.1429, mean bits in support 14.98

| pi | state |
|---|---|
| 0.0357 | mono {eq(ME,THEM):1} |
| 0.0357 | mono {eq(THEM,ME):1} |
| 0.0357 | mono {or(eq(THEM,ME),not(C)):1} |
| 0.0357 | mono {and(eq(THEM,ME),not(D)):1} |
| 0.0357 | mono {or(not(C),eq(ME,THEM)):1} |
| 0.0357 | mono {and(eq(ME,THEM),not(D)):1} |
| 0.0357 | mono {and(eq(ME,THEM),C):1} |
| 0.0357 | mono {and(X,eq(ME,THEM)):1} |
| 0.0357 | mono {and(X,eq(THEM,ME)):1} |
| 0.0357 | mono {or(D,eq(ME,THEM)):1} |
| 0.0357 | mono {and(C,eq(ME,THEM)):1} |
| 0.0357 | mono {not(not(eq(THEM,ME))):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {eq(ME,THEM):1}
    - 3.80e-38 -> poly {eq(ME,THEM):0.5, eq(THEM,ME):0.5}   via eq(THEM,ME) (3.80e-38, rho=1.28e-35 k*=50)
    - 8.37e-39 -> poly {eq(ME,THEM):0.5, THEM(^C):0.5}   via THEM(^C) (8.37e-39, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {eq(ME,THEM):0.5, THEM(^not(D)):0.5}   via THEM(^not(D)) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {eq(ME,THEM):0.5, or(eq(THEM,ME),D):0.5}   via or(eq(THEM,ME),D) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {eq(ME,THEM):0.5, and(eq(THEM,ME),C):0.5}   via and(eq(THEM,ME),C) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {eq(ME,THEM):0.5, or(eq(ME,THEM),D):0.5}   via or(eq(ME,THEM),D) (8.61e-40, rho=1.28e-35 k*=50)
- mono {eq(THEM,ME):1}
    - 3.80e-38 -> poly {eq(ME,THEM):0.5, eq(THEM,ME):0.5}   via eq(ME,THEM) (3.80e-38, rho=1.28e-35 k*=50)
    - 8.37e-39 -> poly {eq(THEM,ME):0.5, THEM(^C):0.5}   via THEM(^C) (8.37e-39, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {eq(THEM,ME):0.5, THEM(^not(D)):0.5}   via THEM(^not(D)) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {eq(THEM,ME):0.5, or(eq(THEM,ME),D):0.5}   via or(eq(THEM,ME),D) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {eq(THEM,ME):0.5, and(eq(THEM,ME),C):0.5}   via and(eq(THEM,ME),C) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {eq(THEM,ME):0.5, or(eq(ME,THEM),D):0.5}   via or(eq(ME,THEM),D) (8.61e-40, rho=1.28e-35 k*=50)
- mono {or(eq(THEM,ME),not(C)):1}
    - 3.80e-38 -> poly {eq(THEM,ME):0.5, or(eq(THEM,ME),not(C)):0.5}   via eq(THEM,ME) (3.80e-38, rho=1.28e-35 k*=50)
    - 3.80e-38 -> poly {eq(ME,THEM):0.5, or(eq(THEM,ME),not(C)):0.5}   via eq(ME,THEM) (3.80e-38, rho=1.28e-35 k*=50)
    - 8.37e-39 -> poly {THEM(^C):0.5, or(eq(THEM,ME),not(C)):0.5}   via THEM(^C) (8.37e-39, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {THEM(^not(D)):0.5, or(eq(THEM,ME),not(C)):0.5}   via THEM(^not(D)) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {or(eq(THEM,ME),D):0.5, or(eq(THEM,ME),not(C)):0.5}   via or(eq(THEM,ME),D) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {and(eq(THEM,ME),C):0.5, or(eq(THEM,ME),not(C)):0.5}   via and(eq(THEM,ME),C) (8.61e-40, rho=1.28e-35 k*=50)
- mono {and(eq(THEM,ME),not(D)):1}
    - 3.80e-38 -> poly {eq(THEM,ME):0.5, and(eq(THEM,ME),not(D)):0.5}   via eq(THEM,ME) (3.80e-38, rho=1.28e-35 k*=50)
    - 3.80e-38 -> poly {eq(ME,THEM):0.5, and(eq(THEM,ME),not(D)):0.5}   via eq(ME,THEM) (3.80e-38, rho=1.28e-35 k*=50)
    - 8.37e-39 -> poly {THEM(^C):0.5, and(eq(THEM,ME),not(D)):0.5}   via THEM(^C) (8.37e-39, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {THEM(^not(D)):0.5, and(eq(THEM,ME),not(D)):0.5}   via THEM(^not(D)) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {or(eq(THEM,ME),D):0.5, and(eq(THEM,ME),not(D)):0.5}   via or(eq(THEM,ME),D) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {and(eq(THEM,ME),C):0.5, and(eq(THEM,ME),not(D)):0.5}   via and(eq(THEM,ME),C) (8.61e-40, rho=1.28e-35 k*=50)
- mono {or(not(C),eq(ME,THEM)):1}
    - 3.80e-38 -> poly {eq(THEM,ME):0.5, or(not(C),eq(ME,THEM)):0.5}   via eq(THEM,ME) (3.80e-38, rho=1.28e-35 k*=50)
    - 3.80e-38 -> poly {eq(ME,THEM):0.5, or(not(C),eq(ME,THEM)):0.5}   via eq(ME,THEM) (3.80e-38, rho=1.28e-35 k*=50)
    - 8.37e-39 -> poly {THEM(^C):0.5, or(not(C),eq(ME,THEM)):0.5}   via THEM(^C) (8.37e-39, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {THEM(^not(D)):0.5, or(not(C),eq(ME,THEM)):0.5}   via THEM(^not(D)) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {or(eq(THEM,ME),D):0.5, or(not(C),eq(ME,THEM)):0.5}   via or(eq(THEM,ME),D) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {and(eq(THEM,ME),C):0.5, or(not(C),eq(ME,THEM)):0.5}   via and(eq(THEM,ME),C) (8.61e-40, rho=1.28e-35 k*=50)
- mono {and(eq(ME,THEM),not(D)):1}
    - 3.80e-38 -> poly {eq(THEM,ME):0.5, and(eq(ME,THEM),not(D)):0.5}   via eq(THEM,ME) (3.80e-38, rho=1.28e-35 k*=50)
    - 3.80e-38 -> poly {eq(ME,THEM):0.5, and(eq(ME,THEM),not(D)):0.5}   via eq(ME,THEM) (3.80e-38, rho=1.28e-35 k*=50)
    - 8.37e-39 -> poly {THEM(^C):0.5, and(eq(ME,THEM),not(D)):0.5}   via THEM(^C) (8.37e-39, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {THEM(^not(D)):0.5, and(eq(ME,THEM),not(D)):0.5}   via THEM(^not(D)) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {or(eq(THEM,ME),D):0.5, and(eq(ME,THEM),not(D)):0.5}   via or(eq(THEM,ME),D) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {and(eq(THEM,ME),C):0.5, and(eq(ME,THEM),not(D)):0.5}   via and(eq(THEM,ME),C) (8.61e-40, rho=1.28e-35 k*=50)
- mono {and(eq(ME,THEM),C):1}
    - 3.80e-38 -> poly {eq(THEM,ME):0.5, and(eq(ME,THEM),C):0.5}   via eq(THEM,ME) (3.80e-38, rho=1.28e-35 k*=50)
    - 3.80e-38 -> poly {eq(ME,THEM):0.5, and(eq(ME,THEM),C):0.5}   via eq(ME,THEM) (3.80e-38, rho=1.28e-35 k*=50)
    - 8.37e-39 -> poly {THEM(^C):0.5, and(eq(ME,THEM),C):0.5}   via THEM(^C) (8.37e-39, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {and(eq(ME,THEM),C):0.5, THEM(^not(D)):0.5}   via THEM(^not(D)) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {and(eq(ME,THEM),C):0.5, or(eq(THEM,ME),D):0.5}   via or(eq(THEM,ME),D) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {and(eq(ME,THEM),C):0.5, and(eq(THEM,ME),C):0.5}   via and(eq(THEM,ME),C) (8.61e-40, rho=1.28e-35 k*=50)
- mono {and(X,eq(ME,THEM)):1}
    - 5.00e-26 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (5.00e-26, rho=1.68e-23 k*=100)
    - 5.00e-26 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (5.00e-26, rho=1.68e-23 k*=100)
    - 1.10e-26 -> mono {THEM(^C):1}   via THEM(^C) (1.10e-26, rho=1.68e-23 k*=100)
    - 1.13e-27 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (1.13e-27, rho=1.68e-23 k*=100)
    - 1.13e-27 -> mono {or(eq(THEM,ME),D):1}   via or(eq(THEM,ME),D) (1.13e-27, rho=1.68e-23 k*=100)
    - 1.13e-27 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (1.13e-27, rho=1.68e-23 k*=100)
- mono {and(X,eq(THEM,ME)):1}
    - 5.00e-26 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (5.00e-26, rho=1.68e-23 k*=100)
    - 5.00e-26 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (5.00e-26, rho=1.68e-23 k*=100)
    - 1.10e-26 -> mono {THEM(^C):1}   via THEM(^C) (1.10e-26, rho=1.68e-23 k*=100)
    - 1.13e-27 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (1.13e-27, rho=1.68e-23 k*=100)
    - 1.13e-27 -> mono {or(eq(THEM,ME),D):1}   via or(eq(THEM,ME),D) (1.13e-27, rho=1.68e-23 k*=100)
    - 1.13e-27 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (1.13e-27, rho=1.68e-23 k*=100)
- mono {or(D,eq(ME,THEM)):1}
    - 3.80e-38 -> poly {eq(THEM,ME):0.5, or(D,eq(ME,THEM)):0.5}   via eq(THEM,ME) (3.80e-38, rho=1.28e-35 k*=50)
    - 3.80e-38 -> poly {eq(ME,THEM):0.5, or(D,eq(ME,THEM)):0.5}   via eq(ME,THEM) (3.80e-38, rho=1.28e-35 k*=50)
    - 8.37e-39 -> poly {THEM(^C):0.5, or(D,eq(ME,THEM)):0.5}   via THEM(^C) (8.37e-39, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {or(D,eq(ME,THEM)):0.5, THEM(^not(D)):0.5}   via THEM(^not(D)) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {or(D,eq(ME,THEM)):0.5, or(eq(THEM,ME),D):0.5}   via or(eq(THEM,ME),D) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {or(D,eq(ME,THEM)):0.5, and(eq(THEM,ME),C):0.5}   via and(eq(THEM,ME),C) (8.61e-40, rho=1.28e-35 k*=50)
- mono {and(C,eq(ME,THEM)):1}
    - 3.80e-38 -> poly {eq(THEM,ME):0.5, and(C,eq(ME,THEM)):0.5}   via eq(THEM,ME) (3.80e-38, rho=1.28e-35 k*=50)
    - 3.80e-38 -> poly {eq(ME,THEM):0.5, and(C,eq(ME,THEM)):0.5}   via eq(ME,THEM) (3.80e-38, rho=1.28e-35 k*=50)
    - 8.37e-39 -> poly {THEM(^C):0.5, and(C,eq(ME,THEM)):0.5}   via THEM(^C) (8.37e-39, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {and(C,eq(ME,THEM)):0.5, THEM(^not(D)):0.5}   via THEM(^not(D)) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {and(C,eq(ME,THEM)):0.5, or(eq(THEM,ME),D):0.5}   via or(eq(THEM,ME),D) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {and(C,eq(ME,THEM)):0.5, and(eq(THEM,ME),C):0.5}   via and(eq(THEM,ME),C) (8.61e-40, rho=1.28e-35 k*=50)
- mono {not(not(eq(THEM,ME))):1}
    - 3.80e-38 -> poly {eq(THEM,ME):0.5, not(not(eq(THEM,ME))):0.5}   via eq(THEM,ME) (3.80e-38, rho=1.28e-35 k*=50)
    - 3.80e-38 -> poly {eq(ME,THEM):0.5, not(not(eq(THEM,ME))):0.5}   via eq(ME,THEM) (3.80e-38, rho=1.28e-35 k*=50)
    - 8.37e-39 -> poly {THEM(^C):0.5, not(not(eq(THEM,ME))):0.5}   via THEM(^C) (8.37e-39, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {not(not(eq(THEM,ME))):0.5, THEM(^not(D)):0.5}   via THEM(^not(D)) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {not(not(eq(THEM,ME))):0.5, or(eq(THEM,ME),D):0.5}   via or(eq(THEM,ME),D) (8.61e-40, rho=1.28e-35 k*=50)
    - 8.61e-40 -> poly {not(not(eq(THEM,ME))):0.5, and(eq(THEM,ME),C):0.5}   via and(eq(THEM,ME),C) (8.61e-40, rho=1.28e-35 k*=50)
