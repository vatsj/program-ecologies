# Standing variance: agent-based Moran, pd, weak n=6 with ROLE, N=100, w=0.3, burn-in 10000 generations, 100000 sampled, 5 seeds

Cooperative share = (mean payoff - u(D,D)) / (efficient - u(D,D)); classes = 112 behavioural classes of L_6 (3994 programs); mutation per birth at eps = epsN/N, mutants from mu over classes.

| epsN | coop share (mean ± sd over seeds) | THEM(^C) share | ALLC share | P(cooperator & ALLC coexist) |
|---|---|---|---|---|
| 0.1 | 0.0107 ± 0.0086 | 0.0066 ± 0.0085 | 0.0015 ± 0.0004 | 0.0008 ± 0.0011 |
| 1 | 0.0484 ± 0.0038 | 0.0162 ± 0.0029 | 0.0117 ± 0.0003 | 0.0130 ± 0.0019 |
| 10 | 0.2399 ± 0.0006 | 0.0006 ± 0.0001 | 0.0887 ± 0.0004 | 0.0141 ± 0.0006 |
