### arm=source, n=6, game=pd, N=10, w=1.0, x_on=True, role=False, mode=square, fmap=exp

programs 2110, classes 220, states 1950, terminal classes 1, indeterminate 0, divergence rate 0.0014, flow into polymorphic targets 1.35e-06
mean payoff -0.4746, efficient 0.0000, deadweight loss 0.4746, mean bits in support 6.92

| pi | state |
|---|---|
| 0.3213 | mono {D:1} |
| 0.2295 | mono {eq(ME,THEM):1} |
| 0.2295 | mono {eq(THEM,ME):1} |
| 0.0801 | mono {not(C):1} |
| 0.0350 | mono {not(not(not(C))):1} |
| 0.0052 | mono {not(not(eq(ME,THEM))):1} |
| 0.0052 | mono {not(not(eq(THEM,ME))):1} |
| 0.0052 | mono {and(eq(THEM,ME),C):1} |
| 0.0052 | mono {and(C,eq(THEM,ME)):1} |
| 0.0052 | mono {and(eq(ME,THEM),C):1} |
| 0.0052 | mono {or(eq(THEM,ME),D):1} |
| 0.0052 | mono {or(D,eq(THEM,ME)):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {D:1}
    - 5.59e-03 -> mono {not(C):1}   via not(C) (5.59e-03, rho=1.00e-01 k*=10)
    - 2.44e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-03, rho=1.00e-01 k*=10)
    - 6.20e-04 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (6.20e-04, rho=2.08e-01 k*=10)
    - 6.20e-04 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (6.20e-04, rho=2.08e-01 k*=10)
    - 4.19e-04 -> mono {X:1}   via X (4.19e-04, rho=1.87e-03 k*=10)
    - 2.98e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.98e-04, rho=1.00e-01 k*=10)
- mono {eq(ME,THEM):1}
    - 8.52e-04 -> mono {D:1}   via D (8.52e-04, rho=3.81e-03 k*=10)
    - 2.13e-04 -> mono {not(C):1}   via not(C) (2.13e-04, rho=3.81e-03 k*=10)
    - 9.31e-05 -> mono {not(not(not(C))):1}   via not(not(not(C))) (9.31e-05, rho=3.81e-03 k*=10)
    - 6.01e-05 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (6.01e-05, rho=2.02e-02 k*=10)
    - 1.32e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.32e-05, rho=2.02e-02 k*=10)
    - 1.14e-05 -> mono {THEM(ME):1}   via THEM(ME) (1.14e-05, rho=3.81e-03 k*=10)
- mono {eq(THEM,ME):1}
    - 8.52e-04 -> mono {D:1}   via D (8.52e-04, rho=3.81e-03 k*=10)
    - 2.13e-04 -> mono {not(C):1}   via not(C) (2.13e-04, rho=3.81e-03 k*=10)
    - 9.31e-05 -> mono {not(not(not(C))):1}   via not(not(not(C))) (9.31e-05, rho=3.81e-03 k*=10)
    - 6.01e-05 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (6.01e-05, rho=2.02e-02 k*=10)
    - 1.32e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.32e-05, rho=2.02e-02 k*=10)
    - 1.14e-05 -> mono {THEM(ME):1}   via THEM(ME) (1.14e-05, rho=3.81e-03 k*=10)
- mono {not(C):1}
    - 2.24e-02 -> mono {D:1}   via D (2.24e-02, rho=1.00e-01 k*=10)
    - 2.44e-03 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-03, rho=1.00e-01 k*=10)
    - 6.20e-04 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (6.20e-04, rho=2.08e-01 k*=10)
    - 6.20e-04 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (6.20e-04, rho=2.08e-01 k*=10)
    - 4.19e-04 -> mono {X:1}   via X (4.19e-04, rho=1.87e-03 k*=10)
    - 2.98e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.98e-04, rho=1.00e-01 k*=10)
- mono {not(not(not(C))):1}
    - 2.24e-02 -> mono {D:1}   via D (2.24e-02, rho=1.00e-01 k*=10)
    - 5.59e-03 -> mono {not(C):1}   via not(C) (5.59e-03, rho=1.00e-01 k*=10)
    - 6.20e-04 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (6.20e-04, rho=2.08e-01 k*=10)
    - 6.20e-04 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (6.20e-04, rho=2.08e-01 k*=10)
    - 4.19e-04 -> mono {X:1}   via X (4.19e-04, rho=1.87e-03 k*=10)
    - 2.98e-04 -> mono {THEM(THEM):1}   via THEM(THEM) (2.98e-04, rho=1.00e-01 k*=10)
- mono {not(not(eq(ME,THEM))):1}
    - 8.52e-04 -> mono {D:1}   via D (8.52e-04, rho=3.81e-03 k*=10)
    - 2.13e-04 -> mono {not(C):1}   via not(C) (2.13e-04, rho=3.81e-03 k*=10)
    - 9.31e-05 -> mono {not(not(not(C))):1}   via not(not(not(C))) (9.31e-05, rho=3.81e-03 k*=10)
    - 6.01e-05 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (6.01e-05, rho=2.02e-02 k*=10)
    - 6.01e-05 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (6.01e-05, rho=2.02e-02 k*=10)
    - 1.32e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.32e-05, rho=2.02e-02 k*=10)
- mono {not(not(eq(THEM,ME))):1}
    - 8.52e-04 -> mono {D:1}   via D (8.52e-04, rho=3.81e-03 k*=10)
    - 2.13e-04 -> mono {not(C):1}   via not(C) (2.13e-04, rho=3.81e-03 k*=10)
    - 9.31e-05 -> mono {not(not(not(C))):1}   via not(not(not(C))) (9.31e-05, rho=3.81e-03 k*=10)
    - 6.01e-05 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (6.01e-05, rho=2.02e-02 k*=10)
    - 6.01e-05 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (6.01e-05, rho=2.02e-02 k*=10)
    - 1.32e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.32e-05, rho=2.02e-02 k*=10)
- mono {and(eq(THEM,ME),C):1}
    - 8.52e-04 -> mono {D:1}   via D (8.52e-04, rho=3.81e-03 k*=10)
    - 2.13e-04 -> mono {not(C):1}   via not(C) (2.13e-04, rho=3.81e-03 k*=10)
    - 9.31e-05 -> mono {not(not(not(C))):1}   via not(not(not(C))) (9.31e-05, rho=3.81e-03 k*=10)
    - 6.01e-05 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (6.01e-05, rho=2.02e-02 k*=10)
    - 6.01e-05 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (6.01e-05, rho=2.02e-02 k*=10)
    - 1.32e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.32e-05, rho=2.02e-02 k*=10)
- mono {and(C,eq(THEM,ME)):1}
    - 8.52e-04 -> mono {D:1}   via D (8.52e-04, rho=3.81e-03 k*=10)
    - 2.13e-04 -> mono {not(C):1}   via not(C) (2.13e-04, rho=3.81e-03 k*=10)
    - 9.31e-05 -> mono {not(not(not(C))):1}   via not(not(not(C))) (9.31e-05, rho=3.81e-03 k*=10)
    - 6.01e-05 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (6.01e-05, rho=2.02e-02 k*=10)
    - 6.01e-05 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (6.01e-05, rho=2.02e-02 k*=10)
    - 1.32e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.32e-05, rho=2.02e-02 k*=10)
- mono {and(eq(ME,THEM),C):1}
    - 8.52e-04 -> mono {D:1}   via D (8.52e-04, rho=3.81e-03 k*=10)
    - 2.13e-04 -> mono {not(C):1}   via not(C) (2.13e-04, rho=3.81e-03 k*=10)
    - 9.31e-05 -> mono {not(not(not(C))):1}   via not(not(not(C))) (9.31e-05, rho=3.81e-03 k*=10)
    - 6.01e-05 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (6.01e-05, rho=2.02e-02 k*=10)
    - 6.01e-05 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (6.01e-05, rho=2.02e-02 k*=10)
    - 1.32e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.32e-05, rho=2.02e-02 k*=10)
- mono {or(eq(THEM,ME),D):1}
    - 8.52e-04 -> mono {D:1}   via D (8.52e-04, rho=3.81e-03 k*=10)
    - 2.13e-04 -> mono {not(C):1}   via not(C) (2.13e-04, rho=3.81e-03 k*=10)
    - 9.31e-05 -> mono {not(not(not(C))):1}   via not(not(not(C))) (9.31e-05, rho=3.81e-03 k*=10)
    - 6.01e-05 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (6.01e-05, rho=2.02e-02 k*=10)
    - 6.01e-05 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (6.01e-05, rho=2.02e-02 k*=10)
    - 1.32e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.32e-05, rho=2.02e-02 k*=10)
- mono {or(D,eq(THEM,ME)):1}
    - 8.52e-04 -> mono {D:1}   via D (8.52e-04, rho=3.81e-03 k*=10)
    - 2.13e-04 -> mono {not(C):1}   via not(C) (2.13e-04, rho=3.81e-03 k*=10)
    - 9.31e-05 -> mono {not(not(not(C))):1}   via not(not(not(C))) (9.31e-05, rho=3.81e-03 k*=10)
    - 6.01e-05 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (6.01e-05, rho=2.02e-02 k*=10)
    - 6.01e-05 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (6.01e-05, rho=2.02e-02 k*=10)
    - 1.32e-05 -> mono {THEM(^C):1}   via THEM(^C) (1.32e-05, rho=2.02e-02 k*=10)
