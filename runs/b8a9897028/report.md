### arm=source, n=6, game=pd, N=100, w=0.3, x_on=True, role=False, mode=square, fmap=exp

programs 2110, classes 220, states 1921, terminal classes 1, indeterminate 0, divergence rate 0.0014, flow into polymorphic targets 4.72e-11
mean payoff -0.0001, efficient 0.0000, deadweight loss 0.0001, mean bits in support 9.47

| pi | state |
|---|---|
| 0.4430 | mono {eq(THEM,ME):1} |
| 0.4430 | mono {eq(ME,THEM):1} |
| 0.0100 | mono {or(D,eq(THEM,ME)):1} |
| 0.0100 | mono {and(eq(ME,THEM),C):1} |
| 0.0100 | mono {or(eq(THEM,ME),D):1} |
| 0.0100 | mono {and(C,eq(THEM,ME)):1} |
| 0.0100 | mono {not(not(eq(THEM,ME))):1} |
| 0.0100 | mono {not(not(eq(ME,THEM))):1} |
| 0.0100 | mono {and(C,eq(ME,THEM)):1} |
| 0.0100 | mono {or(D,eq(ME,THEM)):1} |
| 0.0100 | mono {or(eq(ME,THEM),D):1} |
| 0.0100 | mono {and(eq(THEM,ME),C):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {eq(THEM,ME):1}
    - 5.52e-08 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (5.52e-08, rho=1.85e-05 k*=100)
    - 1.22e-08 -> mono {THEM(^C):1}   via THEM(^C) (1.22e-08, rho=1.85e-05 k*=100)
    - 3.88e-09 -> mono {D:1}   via D (3.88e-09, rho=1.74e-08 k*=100)
    - 1.25e-09 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (1.25e-09, rho=1.85e-05 k*=100)
    - 1.25e-09 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (1.25e-09, rho=1.85e-05 k*=100)
    - 1.25e-09 -> mono {or(eq(THEM,ME),D):1}   via or(eq(THEM,ME),D) (1.25e-09, rho=1.85e-05 k*=100)
- mono {eq(ME,THEM):1}
    - 5.52e-08 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (5.52e-08, rho=1.85e-05 k*=100)
    - 1.22e-08 -> mono {THEM(^C):1}   via THEM(^C) (1.22e-08, rho=1.85e-05 k*=100)
    - 3.88e-09 -> mono {D:1}   via D (3.88e-09, rho=1.74e-08 k*=100)
    - 1.25e-09 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (1.25e-09, rho=1.85e-05 k*=100)
    - 1.25e-09 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (1.25e-09, rho=1.85e-05 k*=100)
    - 1.25e-09 -> mono {or(eq(THEM,ME),D):1}   via or(eq(THEM,ME),D) (1.25e-09, rho=1.85e-05 k*=100)
- mono {or(D,eq(THEM,ME)):1}
    - 5.52e-08 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (5.52e-08, rho=1.85e-05 k*=100)
    - 5.52e-08 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (5.52e-08, rho=1.85e-05 k*=100)
    - 1.22e-08 -> mono {THEM(^C):1}   via THEM(^C) (1.22e-08, rho=1.85e-05 k*=100)
    - 3.88e-09 -> mono {D:1}   via D (3.88e-09, rho=1.74e-08 k*=100)
    - 1.25e-09 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (1.25e-09, rho=1.85e-05 k*=100)
    - 1.25e-09 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (1.25e-09, rho=1.85e-05 k*=100)
- mono {and(eq(ME,THEM),C):1}
    - 5.52e-08 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (5.52e-08, rho=1.85e-05 k*=100)
    - 5.52e-08 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (5.52e-08, rho=1.85e-05 k*=100)
    - 1.22e-08 -> mono {THEM(^C):1}   via THEM(^C) (1.22e-08, rho=1.85e-05 k*=100)
    - 3.88e-09 -> mono {D:1}   via D (3.88e-09, rho=1.74e-08 k*=100)
    - 1.25e-09 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (1.25e-09, rho=1.85e-05 k*=100)
    - 1.25e-09 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (1.25e-09, rho=1.85e-05 k*=100)
- mono {or(eq(THEM,ME),D):1}
    - 5.52e-08 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (5.52e-08, rho=1.85e-05 k*=100)
    - 5.52e-08 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (5.52e-08, rho=1.85e-05 k*=100)
    - 1.22e-08 -> mono {THEM(^C):1}   via THEM(^C) (1.22e-08, rho=1.85e-05 k*=100)
    - 3.88e-09 -> mono {D:1}   via D (3.88e-09, rho=1.74e-08 k*=100)
    - 1.25e-09 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (1.25e-09, rho=1.85e-05 k*=100)
    - 1.25e-09 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (1.25e-09, rho=1.85e-05 k*=100)
- mono {and(C,eq(THEM,ME)):1}
    - 5.52e-08 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (5.52e-08, rho=1.85e-05 k*=100)
    - 5.52e-08 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (5.52e-08, rho=1.85e-05 k*=100)
    - 1.22e-08 -> mono {THEM(^C):1}   via THEM(^C) (1.22e-08, rho=1.85e-05 k*=100)
    - 3.88e-09 -> mono {D:1}   via D (3.88e-09, rho=1.74e-08 k*=100)
    - 1.25e-09 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (1.25e-09, rho=1.85e-05 k*=100)
    - 1.25e-09 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (1.25e-09, rho=1.85e-05 k*=100)
- mono {not(not(eq(THEM,ME))):1}
    - 5.52e-08 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (5.52e-08, rho=1.85e-05 k*=100)
    - 5.52e-08 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (5.52e-08, rho=1.85e-05 k*=100)
    - 1.22e-08 -> mono {THEM(^C):1}   via THEM(^C) (1.22e-08, rho=1.85e-05 k*=100)
    - 3.88e-09 -> mono {D:1}   via D (3.88e-09, rho=1.74e-08 k*=100)
    - 1.25e-09 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (1.25e-09, rho=1.85e-05 k*=100)
    - 1.25e-09 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (1.25e-09, rho=1.85e-05 k*=100)
- mono {not(not(eq(ME,THEM))):1}
    - 5.52e-08 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (5.52e-08, rho=1.85e-05 k*=100)
    - 5.52e-08 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (5.52e-08, rho=1.85e-05 k*=100)
    - 1.22e-08 -> mono {THEM(^C):1}   via THEM(^C) (1.22e-08, rho=1.85e-05 k*=100)
    - 3.88e-09 -> mono {D:1}   via D (3.88e-09, rho=1.74e-08 k*=100)
    - 1.25e-09 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (1.25e-09, rho=1.85e-05 k*=100)
    - 1.25e-09 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (1.25e-09, rho=1.85e-05 k*=100)
- mono {and(C,eq(ME,THEM)):1}
    - 5.52e-08 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (5.52e-08, rho=1.85e-05 k*=100)
    - 5.52e-08 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (5.52e-08, rho=1.85e-05 k*=100)
    - 1.22e-08 -> mono {THEM(^C):1}   via THEM(^C) (1.22e-08, rho=1.85e-05 k*=100)
    - 3.88e-09 -> mono {D:1}   via D (3.88e-09, rho=1.74e-08 k*=100)
    - 1.25e-09 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (1.25e-09, rho=1.85e-05 k*=100)
    - 1.25e-09 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (1.25e-09, rho=1.85e-05 k*=100)
- mono {or(D,eq(ME,THEM)):1}
    - 5.52e-08 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (5.52e-08, rho=1.85e-05 k*=100)
    - 5.52e-08 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (5.52e-08, rho=1.85e-05 k*=100)
    - 1.22e-08 -> mono {THEM(^C):1}   via THEM(^C) (1.22e-08, rho=1.85e-05 k*=100)
    - 3.88e-09 -> mono {D:1}   via D (3.88e-09, rho=1.74e-08 k*=100)
    - 1.25e-09 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (1.25e-09, rho=1.85e-05 k*=100)
    - 1.25e-09 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (1.25e-09, rho=1.85e-05 k*=100)
- mono {or(eq(ME,THEM),D):1}
    - 5.52e-08 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (5.52e-08, rho=1.85e-05 k*=100)
    - 5.52e-08 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (5.52e-08, rho=1.85e-05 k*=100)
    - 1.22e-08 -> mono {THEM(^C):1}   via THEM(^C) (1.22e-08, rho=1.85e-05 k*=100)
    - 3.88e-09 -> mono {D:1}   via D (3.88e-09, rho=1.74e-08 k*=100)
    - 1.25e-09 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (1.25e-09, rho=1.85e-05 k*=100)
    - 1.25e-09 -> mono {and(eq(THEM,ME),C):1}   via and(eq(THEM,ME),C) (1.25e-09, rho=1.85e-05 k*=100)
- mono {and(eq(THEM,ME),C):1}
    - 5.52e-08 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (5.52e-08, rho=1.85e-05 k*=100)
    - 5.52e-08 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (5.52e-08, rho=1.85e-05 k*=100)
    - 1.22e-08 -> mono {THEM(^C):1}   via THEM(^C) (1.22e-08, rho=1.85e-05 k*=100)
    - 3.88e-09 -> mono {D:1}   via D (3.88e-09, rho=1.74e-08 k*=100)
    - 1.25e-09 -> mono {THEM(^not(D)):1}   via THEM(^not(D)) (1.25e-09, rho=1.85e-05 k*=100)
    - 1.25e-09 -> mono {or(eq(THEM,ME),D):1}   via or(eq(THEM,ME),D) (1.25e-09, rho=1.85e-05 k*=100)
