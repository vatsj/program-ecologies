### arm=source, n=6, game=pd, N=100, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 2110, classes 220, states 1921, terminal classes 1, indeterminate 0, divergence rate 0.0014, flow into polymorphic targets 1.80e-18
mean payoff -0.0000, efficient 0.0000, deadweight loss 0.0000, mean bits in support 9.45

| pi | state |
|---|---|
| 0.4446 | mono {eq(ME,THEM):1} |
| 0.4445 | mono {eq(THEM,ME):1} |
| 0.0097 | mono {not(not(eq(ME,THEM))):1} |
| 0.0097 | mono {or(eq(THEM,ME),D):1} |
| 0.0097 | mono {not(not(eq(THEM,ME))):1} |
| 0.0097 | mono {and(eq(THEM,ME),C):1} |
| 0.0097 | mono {or(D,eq(ME,THEM)):1} |
| 0.0097 | mono {and(C,eq(ME,THEM)):1} |
| 0.0097 | mono {and(C,eq(THEM,ME)):1} |
| 0.0097 | mono {or(eq(ME,THEM),D):1} |
| 0.0097 | mono {and(eq(ME,THEM),C):1} |
| 0.0097 | mono {or(D,eq(THEM,ME)):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {eq(ME,THEM):1}
    - 3.01e-15 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (3.01e-15, rho=1.01e-12 k*=100)
    - 6.64e-16 -> mono {THEM(^C):1}   via THEM(^C) (6.64e-16, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {or(eq(THEM,ME),D):1}   via or(eq(THEM,ME),D) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {and(eq(ME,THEM),C):1}   via and(eq(ME,THEM),C) (6.83e-17, rho=1.01e-12 k*=100)
- mono {eq(THEM,ME):1}
    - 3.01e-15 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (3.01e-15, rho=1.01e-12 k*=100)
    - 6.64e-16 -> mono {THEM(^C):1}   via THEM(^C) (6.64e-16, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {or(eq(THEM,ME),D):1}   via or(eq(THEM,ME),D) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {and(eq(ME,THEM),C):1}   via and(eq(ME,THEM),C) (6.83e-17, rho=1.01e-12 k*=100)
- mono {not(not(eq(ME,THEM))):1}
    - 3.01e-15 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (3.01e-15, rho=1.01e-12 k*=100)
    - 3.01e-15 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (3.01e-15, rho=1.01e-12 k*=100)
    - 6.64e-16 -> mono {THEM(^C):1}   via THEM(^C) (6.64e-16, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {or(eq(THEM,ME),D):1}   via or(eq(THEM,ME),D) (6.83e-17, rho=1.01e-12 k*=100)
- mono {or(eq(THEM,ME),D):1}
    - 3.01e-15 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (3.01e-15, rho=1.01e-12 k*=100)
    - 3.01e-15 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (3.01e-15, rho=1.01e-12 k*=100)
    - 6.64e-16 -> mono {THEM(^C):1}   via THEM(^C) (6.64e-16, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {and(eq(ME,THEM),C):1}   via and(eq(ME,THEM),C) (6.83e-17, rho=1.01e-12 k*=100)
- mono {not(not(eq(THEM,ME))):1}
    - 3.01e-15 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (3.01e-15, rho=1.01e-12 k*=100)
    - 3.01e-15 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (3.01e-15, rho=1.01e-12 k*=100)
    - 6.64e-16 -> mono {THEM(^C):1}   via THEM(^C) (6.64e-16, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {or(eq(THEM,ME),D):1}   via or(eq(THEM,ME),D) (6.83e-17, rho=1.01e-12 k*=100)
- mono {and(eq(THEM,ME),C):1}
    - 3.01e-15 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (3.01e-15, rho=1.01e-12 k*=100)
    - 3.01e-15 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (3.01e-15, rho=1.01e-12 k*=100)
    - 6.64e-16 -> mono {THEM(^C):1}   via THEM(^C) (6.64e-16, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {or(eq(THEM,ME),D):1}   via or(eq(THEM,ME),D) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {and(eq(ME,THEM),C):1}   via and(eq(ME,THEM),C) (6.83e-17, rho=1.01e-12 k*=100)
- mono {or(D,eq(ME,THEM)):1}
    - 3.01e-15 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (3.01e-15, rho=1.01e-12 k*=100)
    - 3.01e-15 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (3.01e-15, rho=1.01e-12 k*=100)
    - 6.64e-16 -> mono {THEM(^C):1}   via THEM(^C) (6.64e-16, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {or(eq(THEM,ME),D):1}   via or(eq(THEM,ME),D) (6.83e-17, rho=1.01e-12 k*=100)
- mono {and(C,eq(ME,THEM)):1}
    - 3.01e-15 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (3.01e-15, rho=1.01e-12 k*=100)
    - 3.01e-15 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (3.01e-15, rho=1.01e-12 k*=100)
    - 6.64e-16 -> mono {THEM(^C):1}   via THEM(^C) (6.64e-16, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {or(eq(THEM,ME),D):1}   via or(eq(THEM,ME),D) (6.83e-17, rho=1.01e-12 k*=100)
- mono {and(C,eq(THEM,ME)):1}
    - 3.01e-15 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (3.01e-15, rho=1.01e-12 k*=100)
    - 3.01e-15 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (3.01e-15, rho=1.01e-12 k*=100)
    - 6.64e-16 -> mono {THEM(^C):1}   via THEM(^C) (6.64e-16, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {or(eq(THEM,ME),D):1}   via or(eq(THEM,ME),D) (6.83e-17, rho=1.01e-12 k*=100)
- mono {or(eq(ME,THEM),D):1}
    - 3.01e-15 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (3.01e-15, rho=1.01e-12 k*=100)
    - 3.01e-15 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (3.01e-15, rho=1.01e-12 k*=100)
    - 6.64e-16 -> mono {THEM(^C):1}   via THEM(^C) (6.64e-16, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {or(eq(THEM,ME),D):1}   via or(eq(THEM,ME),D) (6.83e-17, rho=1.01e-12 k*=100)
- mono {and(eq(ME,THEM),C):1}
    - 3.01e-15 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (3.01e-15, rho=1.01e-12 k*=100)
    - 3.01e-15 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (3.01e-15, rho=1.01e-12 k*=100)
    - 6.64e-16 -> mono {THEM(^C):1}   via THEM(^C) (6.64e-16, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {or(eq(THEM,ME),D):1}   via or(eq(THEM,ME),D) (6.83e-17, rho=1.01e-12 k*=100)
- mono {or(D,eq(THEM,ME)):1}
    - 3.01e-15 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (3.01e-15, rho=1.01e-12 k*=100)
    - 3.01e-15 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (3.01e-15, rho=1.01e-12 k*=100)
    - 6.64e-16 -> mono {THEM(^C):1}   via THEM(^C) (6.64e-16, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (6.83e-17, rho=1.01e-12 k*=100)
    - 6.83e-17 -> mono {or(eq(THEM,ME),D):1}   via or(eq(THEM,ME),D) (6.83e-17, rho=1.01e-12 k*=100)
