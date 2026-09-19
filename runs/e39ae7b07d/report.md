### arm=source, n=6, game=pd, N=100, w=0.1, x_on=True, role=False, mode=square

programs 2110, classes 220, states 2601, terminal classes 1, indeterminate 0, divergence rate 0.0014, flow into polymorphic targets 1.06e-05
mean payoff -0.2295, efficient 0.0000, deadweight loss 0.2295, mean bits in support 8.34

| pi | state |
|---|---|
| 0.3307 | mono {eq(ME,THEM):1} |
| 0.3307 | mono {eq(THEM,ME):1} |
| 0.1516 | mono {D:1} |
| 0.0378 | mono {not(C):1} |
| 0.0165 | mono {not(not(not(C))):1} |
| 0.0104 | poly {eq(ME,THEM):0.5, eq(THEM,ME):0.5} |
| 0.0088 | mono {not(not(eq(THEM,ME))):1} |
| 0.0088 | mono {not(not(eq(ME,THEM))):1} |
| 0.0088 | mono {or(D,eq(THEM,ME)):1} |
| 0.0088 | mono {and(eq(THEM,ME),C):1} |
| 0.0088 | mono {or(eq(ME,THEM),D):1} |
| 0.0088 | mono {and(C,eq(THEM,ME)):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {eq(ME,THEM):1}
    - 3.02e-05 -> mono {D:1}   via D (3.02e-05, rho=1.35e-04 k*=100)
    - 8.26e-06 -> poly {eq(ME,THEM):0.5, eq(THEM,ME):0.5}   via eq(THEM,ME) (8.26e-06, rho=2.77e-03 k*=50)
    - 7.54e-06 -> mono {not(C):1}   via not(C) (7.54e-06, rho=1.35e-04 k*=100)
    - 3.30e-06 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.30e-06, rho=1.35e-04 k*=100)
    - 1.82e-06 -> poly {eq(ME,THEM):0.5, THEM(^C):0.5}   via THEM(^C) (1.82e-06, rho=2.77e-03 k*=50)
    - 4.02e-07 -> mono {THEM(ME):1}   via THEM(ME) (4.02e-07, rho=1.35e-04 k*=100)
- mono {eq(THEM,ME):1}
    - 3.02e-05 -> mono {D:1}   via D (3.02e-05, rho=1.35e-04 k*=100)
    - 8.26e-06 -> poly {eq(ME,THEM):0.5, eq(THEM,ME):0.5}   via eq(ME,THEM) (8.26e-06, rho=2.77e-03 k*=50)
    - 7.54e-06 -> mono {not(C):1}   via not(C) (7.54e-06, rho=1.35e-04 k*=100)
    - 3.30e-06 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.30e-06, rho=1.35e-04 k*=100)
    - 1.82e-06 -> poly {eq(THEM,ME):0.5, THEM(^C):0.5}   via THEM(^C) (1.82e-06, rho=2.77e-03 k*=50)
    - 4.02e-07 -> mono {THEM(ME):1}   via THEM(ME) (4.02e-07, rho=1.35e-04 k*=100)
- mono {D:1}
    - 5.59e-04 -> mono {not(C):1}   via not(C) (5.59e-04, rho=1.00e-02 k*=100)
    - 2.44e-04 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-04, rho=1.00e-02 k*=100)
    - 7.70e-05 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (7.70e-05, rho=2.58e-02 k*=100)
    - 7.70e-05 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (7.70e-05, rho=2.58e-02 k*=100)
    - 4.93e-05 -> mono {X:1}   via X (4.93e-05, rho=2.20e-04 k*=100)
    - 2.98e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.98e-05, rho=1.00e-02 k*=100)
- mono {not(C):1}
    - 2.24e-03 -> mono {D:1}   via D (2.24e-03, rho=1.00e-02 k*=100)
    - 2.44e-04 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-04, rho=1.00e-02 k*=100)
    - 7.70e-05 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (7.70e-05, rho=2.58e-02 k*=100)
    - 7.70e-05 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (7.70e-05, rho=2.58e-02 k*=100)
    - 4.93e-05 -> mono {X:1}   via X (4.93e-05, rho=2.20e-04 k*=100)
    - 2.98e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.98e-05, rho=1.00e-02 k*=100)
- mono {not(not(not(C))):1}
    - 2.24e-03 -> mono {D:1}   via D (2.24e-03, rho=1.00e-02 k*=100)
    - 5.59e-04 -> mono {not(C):1}   via not(C) (5.59e-04, rho=1.00e-02 k*=100)
    - 7.70e-05 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (7.70e-05, rho=2.58e-02 k*=100)
    - 7.70e-05 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (7.70e-05, rho=2.58e-02 k*=100)
    - 4.93e-05 -> mono {X:1}   via X (4.93e-05, rho=2.20e-04 k*=100)
    - 2.98e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.98e-05, rho=1.00e-02 k*=100)
- poly {eq(ME,THEM):0.5, eq(THEM,ME):0.5}
    - 2.90e-04 -> mono {D:1}   via D (2.90e-04, rho=1.30e-03 k*=100)
    - 7.25e-05 -> mono {not(C):1}   via not(C) (7.25e-05, rho=1.30e-03 k*=100)
    - 3.47e-05 -> mono {eq(THEM,ME):1}   via eq(THEM,^eq(THEM,ME)) (2.31e-05, rho=1.00e+00 k*=1), THEM(^eq(THEM,ME)) (1.16e-05, rho=1.00e+00 k*=1)
    - 3.47e-05 -> mono {eq(ME,THEM):1}   via eq(THEM,^eq(ME,THEM)) (2.31e-05, rho=1.00e+00 k*=1), THEM(^eq(ME,THEM)) (1.16e-05, rho=1.00e+00 k*=1)
    - 3.17e-05 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.17e-05, rho=1.30e-03 k*=100)
    - 5.04e-06 -> poly {eq(ME,THEM):0.25, eq(THEM,ME):0.25, THEM(^X):0.5}   via THEM(^X) (5.04e-06, rho=7.67e-03 k*=50)
- mono {not(not(eq(THEM,ME))):1}
    - 3.02e-05 -> mono {D:1}   via D (3.02e-05, rho=1.35e-04 k*=100)
    - 8.26e-06 -> poly {eq(THEM,ME):0.5, not(not(eq(THEM,ME))):0.5}   via eq(THEM,ME) (8.26e-06, rho=2.77e-03 k*=50)
    - 8.26e-06 -> poly {eq(ME,THEM):0.5, not(not(eq(THEM,ME))):0.5}   via eq(ME,THEM) (8.26e-06, rho=2.77e-03 k*=50)
    - 7.54e-06 -> mono {not(C):1}   via not(C) (7.54e-06, rho=1.35e-04 k*=100)
    - 3.30e-06 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.30e-06, rho=1.35e-04 k*=100)
    - 1.82e-06 -> poly {THEM(^C):0.5, not(not(eq(THEM,ME))):0.5}   via THEM(^C) (1.82e-06, rho=2.77e-03 k*=50)
- mono {not(not(eq(ME,THEM))):1}
    - 3.02e-05 -> mono {D:1}   via D (3.02e-05, rho=1.35e-04 k*=100)
    - 8.26e-06 -> poly {eq(THEM,ME):0.5, not(not(eq(ME,THEM))):0.5}   via eq(THEM,ME) (8.26e-06, rho=2.77e-03 k*=50)
    - 8.26e-06 -> poly {eq(ME,THEM):0.5, not(not(eq(ME,THEM))):0.5}   via eq(ME,THEM) (8.26e-06, rho=2.77e-03 k*=50)
    - 7.54e-06 -> mono {not(C):1}   via not(C) (7.54e-06, rho=1.35e-04 k*=100)
    - 3.30e-06 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.30e-06, rho=1.35e-04 k*=100)
    - 1.82e-06 -> poly {THEM(^C):0.5, not(not(eq(ME,THEM))):0.5}   via THEM(^C) (1.82e-06, rho=2.77e-03 k*=50)
- mono {or(D,eq(THEM,ME)):1}
    - 3.02e-05 -> mono {D:1}   via D (3.02e-05, rho=1.35e-04 k*=100)
    - 8.26e-06 -> poly {eq(THEM,ME):0.5, or(D,eq(THEM,ME)):0.5}   via eq(THEM,ME) (8.26e-06, rho=2.77e-03 k*=50)
    - 8.26e-06 -> poly {eq(ME,THEM):0.5, or(D,eq(THEM,ME)):0.5}   via eq(ME,THEM) (8.26e-06, rho=2.77e-03 k*=50)
    - 7.54e-06 -> mono {not(C):1}   via not(C) (7.54e-06, rho=1.35e-04 k*=100)
    - 3.30e-06 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.30e-06, rho=1.35e-04 k*=100)
    - 1.82e-06 -> poly {THEM(^C):0.5, or(D,eq(THEM,ME)):0.5}   via THEM(^C) (1.82e-06, rho=2.77e-03 k*=50)
- mono {and(eq(THEM,ME),C):1}
    - 3.02e-05 -> mono {D:1}   via D (3.02e-05, rho=1.35e-04 k*=100)
    - 8.26e-06 -> poly {eq(THEM,ME):0.5, and(eq(THEM,ME),C):0.5}   via eq(THEM,ME) (8.26e-06, rho=2.77e-03 k*=50)
    - 8.26e-06 -> poly {eq(ME,THEM):0.5, and(eq(THEM,ME),C):0.5}   via eq(ME,THEM) (8.26e-06, rho=2.77e-03 k*=50)
    - 7.54e-06 -> mono {not(C):1}   via not(C) (7.54e-06, rho=1.35e-04 k*=100)
    - 3.30e-06 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.30e-06, rho=1.35e-04 k*=100)
    - 1.82e-06 -> poly {THEM(^C):0.5, and(eq(THEM,ME),C):0.5}   via THEM(^C) (1.82e-06, rho=2.77e-03 k*=50)
- mono {or(eq(ME,THEM),D):1}
    - 3.02e-05 -> mono {D:1}   via D (3.02e-05, rho=1.35e-04 k*=100)
    - 8.26e-06 -> poly {eq(THEM,ME):0.5, or(eq(ME,THEM),D):0.5}   via eq(THEM,ME) (8.26e-06, rho=2.77e-03 k*=50)
    - 8.26e-06 -> poly {eq(ME,THEM):0.5, or(eq(ME,THEM),D):0.5}   via eq(ME,THEM) (8.26e-06, rho=2.77e-03 k*=50)
    - 7.54e-06 -> mono {not(C):1}   via not(C) (7.54e-06, rho=1.35e-04 k*=100)
    - 3.30e-06 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.30e-06, rho=1.35e-04 k*=100)
    - 1.82e-06 -> poly {THEM(^C):0.5, or(eq(ME,THEM),D):0.5}   via THEM(^C) (1.82e-06, rho=2.77e-03 k*=50)
- mono {and(C,eq(THEM,ME)):1}
    - 3.02e-05 -> mono {D:1}   via D (3.02e-05, rho=1.35e-04 k*=100)
    - 8.26e-06 -> poly {eq(THEM,ME):0.5, and(C,eq(THEM,ME)):0.5}   via eq(THEM,ME) (8.26e-06, rho=2.77e-03 k*=50)
    - 8.26e-06 -> poly {eq(ME,THEM):0.5, and(C,eq(THEM,ME)):0.5}   via eq(ME,THEM) (8.26e-06, rho=2.77e-03 k*=50)
    - 7.54e-06 -> mono {not(C):1}   via not(C) (7.54e-06, rho=1.35e-04 k*=100)
    - 3.30e-06 -> mono {not(not(not(C))):1}   via not(not(not(C))) (3.30e-06, rho=1.35e-04 k*=100)
    - 1.82e-06 -> poly {THEM(^C):0.5, and(C,eq(THEM,ME)):0.5}   via THEM(^C) (1.82e-06, rho=2.77e-03 k*=50)
