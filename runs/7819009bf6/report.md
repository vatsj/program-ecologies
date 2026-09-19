### arm=source, n=6, game=pd, N=10, x_on=True, role=False, mode=square

programs 2110, classes 220, states 33944, terminal classes 28, indeterminate 0, divergence rate 0.0014
mean payoff -0.0224, efficient 0.0000, deadweight loss 0.0224, mean bits in support 9.70
absorption: class 0: 0.423, class 1: 0.423, class 2: 0.010, class 3: 0.010, class 4: 0.010, class 5: 0.010, class 6: 0.010, class 7: 0.010, class 8: 0.010, class 9: 0.010, class 10: 0.010, class 11: 0.010, class 12: 0.010, class 13: 0.010, class 14: 0.010, class 15: 0.010, class 16: 0.002, class 17: 0.002, class 18: 0.002, class 19: 0.002, class 20: 0.002, class 21: 0.002, class 22: 0.002, class 23: 0.002, class 24: 0.002, class 25: 0.002, class 26: 0.002, class 27: 0.002

| pi | state |
|---|---|
| 0.4233 | mono {eq(THEM,ME):1} |
| 0.4233 | mono {eq(ME,THEM):1} |
| 0.0096 | mono {not(not(eq(THEM,ME))):1} |
| 0.0096 | mono {or(eq(THEM,ME),D):1} |
| 0.0096 | mono {and(eq(THEM,ME),C):1} |
| 0.0096 | mono {or(eq(ME,THEM),D):1} |
| 0.0096 | mono {and(eq(ME,THEM),C):1} |
| 0.0096 | mono {or(D,eq(THEM,ME)):1} |
| 0.0096 | mono {not(not(eq(ME,THEM))):1} |
| 0.0096 | mono {and(C,eq(THEM,ME)):1} |
| 0.0096 | mono {and(C,eq(ME,THEM)):1} |
| 0.0096 | mono {or(D,eq(ME,THEM)):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {eq(THEM,ME):1}: absorbing (no exits)
- mono {eq(ME,THEM):1}: absorbing (no exits)
- mono {not(not(eq(THEM,ME))):1}: absorbing (no exits)
- mono {or(eq(THEM,ME),D):1}: absorbing (no exits)
- mono {and(eq(THEM,ME),C):1}: absorbing (no exits)
- mono {or(eq(ME,THEM),D):1}: absorbing (no exits)
- mono {and(eq(ME,THEM),C):1}: absorbing (no exits)
- mono {or(D,eq(THEM,ME)):1}: absorbing (no exits)
- mono {not(not(eq(ME,THEM))):1}: absorbing (no exits)
- mono {and(C,eq(THEM,ME)):1}: absorbing (no exits)
- mono {and(C,eq(ME,THEM)):1}: absorbing (no exits)
- mono {or(D,eq(ME,THEM)):1}: absorbing (no exits)
