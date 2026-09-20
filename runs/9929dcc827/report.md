### arm=source, n=6, game=pd, N=100, w=0.1, x_on=True, role=False, mode=square, fmap=exp

programs 2110, classes 220, states 1921, terminal classes 1, indeterminate 0, divergence rate 0.0014, flow into polymorphic targets 7.93e-08
mean payoff -0.2720, efficient 0.0000, deadweight loss 0.2720, mean bits in support 8.01

| pi | state |
|---|---|
| 0.3201 | mono {eq(ME,THEM):1} |
| 0.3201 | mono {eq(THEM,ME):1} |
| 0.1838 | mono {D:1} |
| 0.0458 | mono {not(C):1} |
| 0.0200 | mono {not(not(not(C))):1} |
| 0.0073 | mono {and(eq(ME,THEM),C):1} |
| 0.0073 | mono {and(C,eq(ME,THEM)):1} |
| 0.0073 | mono {and(eq(THEM,ME),C):1} |
| 0.0073 | mono {or(eq(ME,THEM),D):1} |
| 0.0073 | mono {and(C,eq(THEM,ME)):1} |
| 0.0073 | mono {or(D,eq(THEM,ME)):1} |
| 0.0073 | mono {or(D,eq(ME,THEM)):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {eq(ME,THEM):1}
    - 4.12e-05 -> mono {D:1}   via D (4.12e-05, rho=1.84e-04 k*=100)
    - 1.03e-05 -> mono {not(C):1}   via not(C) (1.03e-05, rho=1.84e-04 k*=100)
    - 4.61e-06 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (4.61e-06, rho=1.55e-03 k*=100)
    - 4.50e-06 -> mono {not(not(not(C))):1}   via not(not(not(C))) (4.50e-06, rho=1.84e-04 k*=100)
    - 1.02e-06 -> mono {THEM(^C):1}   via THEM(^C) (1.02e-06, rho=1.55e-03 k*=100)
    - 6.62e-07 -> mono {X:1}   via X (6.62e-07, rho=2.96e-06 k*=100)
- mono {eq(THEM,ME):1}
    - 4.12e-05 -> mono {D:1}   via D (4.12e-05, rho=1.84e-04 k*=100)
    - 1.03e-05 -> mono {not(C):1}   via not(C) (1.03e-05, rho=1.84e-04 k*=100)
    - 4.61e-06 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (4.61e-06, rho=1.55e-03 k*=100)
    - 4.50e-06 -> mono {not(not(not(C))):1}   via not(not(not(C))) (4.50e-06, rho=1.84e-04 k*=100)
    - 1.02e-06 -> mono {THEM(^C):1}   via THEM(^C) (1.02e-06, rho=1.55e-03 k*=100)
    - 6.62e-07 -> mono {X:1}   via X (6.62e-07, rho=2.96e-06 k*=100)
- mono {D:1}
    - 5.59e-04 -> mono {not(C):1}   via not(C) (5.59e-04, rho=1.00e-02 k*=100)
    - 2.44e-04 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-04, rho=1.00e-02 k*=100)
    - 7.38e-05 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (7.38e-05, rho=2.48e-02 k*=100)
    - 7.38e-05 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (7.38e-05, rho=2.48e-02 k*=100)
    - 7.17e-05 -> mono {X:1}   via X (7.17e-05, rho=3.21e-04 k*=100)
    - 2.98e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.98e-05, rho=1.00e-02 k*=100)
- mono {not(C):1}
    - 2.24e-03 -> mono {D:1}   via D (2.24e-03, rho=1.00e-02 k*=100)
    - 2.44e-04 -> mono {not(not(not(C))):1}   via not(not(not(C))) (2.44e-04, rho=1.00e-02 k*=100)
    - 7.38e-05 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (7.38e-05, rho=2.48e-02 k*=100)
    - 7.38e-05 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (7.38e-05, rho=2.48e-02 k*=100)
    - 7.17e-05 -> mono {X:1}   via X (7.17e-05, rho=3.21e-04 k*=100)
    - 2.98e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.98e-05, rho=1.00e-02 k*=100)
- mono {not(not(not(C))):1}
    - 2.24e-03 -> mono {D:1}   via D (2.24e-03, rho=1.00e-02 k*=100)
    - 5.59e-04 -> mono {not(C):1}   via not(C) (5.59e-04, rho=1.00e-02 k*=100)
    - 7.38e-05 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (7.38e-05, rho=2.48e-02 k*=100)
    - 7.38e-05 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (7.38e-05, rho=2.48e-02 k*=100)
    - 7.17e-05 -> mono {X:1}   via X (7.17e-05, rho=3.21e-04 k*=100)
    - 2.98e-05 -> mono {THEM(THEM):1}   via THEM(THEM) (2.98e-05, rho=1.00e-02 k*=100)
- mono {and(eq(ME,THEM),C):1}
    - 4.12e-05 -> mono {D:1}   via D (4.12e-05, rho=1.84e-04 k*=100)
    - 1.03e-05 -> mono {not(C):1}   via not(C) (1.03e-05, rho=1.84e-04 k*=100)
    - 4.61e-06 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (4.61e-06, rho=1.55e-03 k*=100)
    - 4.61e-06 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (4.61e-06, rho=1.55e-03 k*=100)
    - 4.50e-06 -> mono {not(not(not(C))):1}   via not(not(not(C))) (4.50e-06, rho=1.84e-04 k*=100)
    - 1.02e-06 -> mono {THEM(^C):1}   via THEM(^C) (1.02e-06, rho=1.55e-03 k*=100)
- mono {and(C,eq(ME,THEM)):1}
    - 4.12e-05 -> mono {D:1}   via D (4.12e-05, rho=1.84e-04 k*=100)
    - 1.03e-05 -> mono {not(C):1}   via not(C) (1.03e-05, rho=1.84e-04 k*=100)
    - 4.61e-06 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (4.61e-06, rho=1.55e-03 k*=100)
    - 4.61e-06 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (4.61e-06, rho=1.55e-03 k*=100)
    - 4.50e-06 -> mono {not(not(not(C))):1}   via not(not(not(C))) (4.50e-06, rho=1.84e-04 k*=100)
    - 1.02e-06 -> mono {THEM(^C):1}   via THEM(^C) (1.02e-06, rho=1.55e-03 k*=100)
- mono {and(eq(THEM,ME),C):1}
    - 4.12e-05 -> mono {D:1}   via D (4.12e-05, rho=1.84e-04 k*=100)
    - 1.03e-05 -> mono {not(C):1}   via not(C) (1.03e-05, rho=1.84e-04 k*=100)
    - 4.61e-06 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (4.61e-06, rho=1.55e-03 k*=100)
    - 4.61e-06 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (4.61e-06, rho=1.55e-03 k*=100)
    - 4.50e-06 -> mono {not(not(not(C))):1}   via not(not(not(C))) (4.50e-06, rho=1.84e-04 k*=100)
    - 1.02e-06 -> mono {THEM(^C):1}   via THEM(^C) (1.02e-06, rho=1.55e-03 k*=100)
- mono {or(eq(ME,THEM),D):1}
    - 4.12e-05 -> mono {D:1}   via D (4.12e-05, rho=1.84e-04 k*=100)
    - 1.03e-05 -> mono {not(C):1}   via not(C) (1.03e-05, rho=1.84e-04 k*=100)
    - 4.61e-06 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (4.61e-06, rho=1.55e-03 k*=100)
    - 4.61e-06 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (4.61e-06, rho=1.55e-03 k*=100)
    - 4.50e-06 -> mono {not(not(not(C))):1}   via not(not(not(C))) (4.50e-06, rho=1.84e-04 k*=100)
    - 1.02e-06 -> mono {THEM(^C):1}   via THEM(^C) (1.02e-06, rho=1.55e-03 k*=100)
- mono {and(C,eq(THEM,ME)):1}
    - 4.12e-05 -> mono {D:1}   via D (4.12e-05, rho=1.84e-04 k*=100)
    - 1.03e-05 -> mono {not(C):1}   via not(C) (1.03e-05, rho=1.84e-04 k*=100)
    - 4.61e-06 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (4.61e-06, rho=1.55e-03 k*=100)
    - 4.61e-06 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (4.61e-06, rho=1.55e-03 k*=100)
    - 4.50e-06 -> mono {not(not(not(C))):1}   via not(not(not(C))) (4.50e-06, rho=1.84e-04 k*=100)
    - 1.02e-06 -> mono {THEM(^C):1}   via THEM(^C) (1.02e-06, rho=1.55e-03 k*=100)
- mono {or(D,eq(THEM,ME)):1}
    - 4.12e-05 -> mono {D:1}   via D (4.12e-05, rho=1.84e-04 k*=100)
    - 1.03e-05 -> mono {not(C):1}   via not(C) (1.03e-05, rho=1.84e-04 k*=100)
    - 4.61e-06 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (4.61e-06, rho=1.55e-03 k*=100)
    - 4.61e-06 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (4.61e-06, rho=1.55e-03 k*=100)
    - 4.50e-06 -> mono {not(not(not(C))):1}   via not(not(not(C))) (4.50e-06, rho=1.84e-04 k*=100)
    - 1.02e-06 -> mono {THEM(^C):1}   via THEM(^C) (1.02e-06, rho=1.55e-03 k*=100)
- mono {or(D,eq(ME,THEM)):1}
    - 4.12e-05 -> mono {D:1}   via D (4.12e-05, rho=1.84e-04 k*=100)
    - 1.03e-05 -> mono {not(C):1}   via not(C) (1.03e-05, rho=1.84e-04 k*=100)
    - 4.61e-06 -> mono {eq(THEM,ME):1}   via eq(THEM,ME) (4.61e-06, rho=1.55e-03 k*=100)
    - 4.61e-06 -> mono {eq(ME,THEM):1}   via eq(ME,THEM) (4.61e-06, rho=1.55e-03 k*=100)
    - 4.50e-06 -> mono {not(not(not(C))):1}   via not(not(not(C))) (4.50e-06, rho=1.84e-04 k*=100)
    - 1.02e-06 -> mono {THEM(^C):1}   via THEM(^C) (1.02e-06, rho=1.55e-03 k*=100)
