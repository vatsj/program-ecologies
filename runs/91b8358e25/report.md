### arm=source, n=6, game=pd, N=10, w=1.0, x_on=True, role=False, mode=square

programs 2110, classes 220, states 3158, terminal classes 1, indeterminate 0, divergence rate 0.0014, flow into polymorphic targets 8.03e-11
mean payoff -0.0001, efficient 0.0000, deadweight loss 0.0001, mean bits in support 8.82

| pi | state |
|---|---|
| 0.4996 | mono {eq(THEM,ME):1} |
| 0.4996 | mono {eq(ME,THEM):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {eq(THEM,ME):1}
    - 5.24e-11 -> poly {eq(ME,THEM):0.5, eq(THEM,ME):0.5}   via eq(ME,THEM) (5.24e-11, rho=1.76e-08 k*=5)
    - 1.15e-11 -> poly {eq(THEM,ME):0.5, THEM(^C):0.5}   via THEM(^C) (1.15e-11, rho=1.76e-08 k*=5)
    - 1.19e-12 -> poly {eq(THEM,ME):0.5, THEM(^not(D)):0.5}   via THEM(^not(D)) (1.19e-12, rho=1.76e-08 k*=5)
    - 1.19e-12 -> poly {eq(THEM,ME):0.5, or(eq(THEM,ME),D):0.5}   via or(eq(THEM,ME),D) (1.19e-12, rho=1.76e-08 k*=5)
    - 1.19e-12 -> poly {eq(THEM,ME):0.5, and(eq(THEM,ME),C):0.5}   via and(eq(THEM,ME),C) (1.19e-12, rho=1.76e-08 k*=5)
    - 1.19e-12 -> poly {eq(THEM,ME):0.5, or(eq(ME,THEM),D):0.5}   via or(eq(ME,THEM),D) (1.19e-12, rho=1.76e-08 k*=5)
- mono {eq(ME,THEM):1}
    - 5.24e-11 -> poly {eq(ME,THEM):0.5, eq(THEM,ME):0.5}   via eq(THEM,ME) (5.24e-11, rho=1.76e-08 k*=5)
    - 1.15e-11 -> poly {eq(ME,THEM):0.5, THEM(^C):0.5}   via THEM(^C) (1.15e-11, rho=1.76e-08 k*=5)
    - 1.19e-12 -> poly {eq(ME,THEM):0.5, THEM(^not(D)):0.5}   via THEM(^not(D)) (1.19e-12, rho=1.76e-08 k*=5)
    - 1.19e-12 -> poly {eq(ME,THEM):0.5, or(eq(THEM,ME),D):0.5}   via or(eq(THEM,ME),D) (1.19e-12, rho=1.76e-08 k*=5)
    - 1.19e-12 -> poly {eq(ME,THEM):0.5, and(eq(THEM,ME),C):0.5}   via and(eq(THEM,ME),C) (1.19e-12, rho=1.76e-08 k*=5)
    - 1.19e-12 -> poly {eq(ME,THEM):0.5, or(eq(ME,THEM),D):0.5}   via or(eq(ME,THEM),D) (1.19e-12, rho=1.76e-08 k*=5)
