### arm=source, n=6, game=pd, N=10, x_on=True, role=False, mode=square

programs 2110, classes 220, states 39891, terminal classes 28, indeterminate 18, divergence rate 0.0014
mean payoff -0.0222, efficient 0.0000, deadweight loss 0.0222, mean bits in support 9.69
absorption: class 0: 0.424, class 1: 0.009, class 2: 0.009, class 3: 0.009, class 4: 0.009, class 5: 0.009, class 6: 0.009, class 7: 0.009, class 8: 0.009, class 9: 0.009, class 10: 0.009, class 11: 0.009, class 12: 0.009, class 13: 0.009, class 14: 0.009, class 15: 0.424, class 16: 0.002, class 17: 0.002, class 18: 0.002, class 19: 0.002, class 20: 0.002, class 21: 0.002, class 22: 0.002, class 23: 0.002, class 24: 0.002, class 25: 0.002, class 26: 0.002, class 27: 0.002

| pi | state |
|---|---|
| 0.4239 | mono {eq(ME,THEM):1} |
| 0.4239 | mono {eq(THEM,ME):1} |
| 0.0095 | mono {and(eq(THEM,ME),C):1} |
| 0.0095 | mono {or(eq(THEM,ME),D):1} |
| 0.0095 | mono {and(eq(ME,THEM),C):1} |
| 0.0095 | mono {or(D,eq(THEM,ME)):1} |
| 0.0095 | mono {or(D,eq(ME,THEM)):1} |
| 0.0095 | mono {and(C,eq(THEM,ME)):1} |
| 0.0095 | mono {and(C,eq(ME,THEM)):1} |
| 0.0095 | mono {not(not(eq(THEM,ME))):1} |
| 0.0095 | mono {not(not(eq(ME,THEM))):1} |
| 0.0095 | mono {or(eq(ME,THEM),D):1} |

Transitions out of the support (share of mutation events, mutants responsible):

- mono {eq(ME,THEM):1}: absorbing (no exits)
- mono {eq(THEM,ME):1}: absorbing (no exits)
- mono {and(eq(THEM,ME),C):1}: absorbing (no exits)
- mono {or(eq(THEM,ME),D):1}: absorbing (no exits)
- mono {and(eq(ME,THEM),C):1}: absorbing (no exits)
- mono {or(D,eq(THEM,ME)):1}: absorbing (no exits)
- mono {or(D,eq(ME,THEM)):1}: absorbing (no exits)
- mono {and(C,eq(THEM,ME)):1}: absorbing (no exits)
- mono {and(C,eq(ME,THEM)):1}: absorbing (no exits)
- mono {not(not(eq(THEM,ME))):1}: absorbing (no exits)
- mono {not(not(eq(ME,THEM))):1}: absorbing (no exits)
- mono {or(eq(ME,THEM),D):1}: absorbing (no exits)

INDETERMINATE transitions (replicator did not converge): 18; first: from poly {X:0.444, THEM(THEM):0.333, and(X,THEM(^C)):0.222} with mutant not(THEM(^C))
