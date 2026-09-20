# Standing variance: agent-based Moran, pd, weak n=6 with ROLE, N=100, w=0.3, burn-in 10000 generations, 100000 sampled, 5 seeds

Cooperative share = (mean payoff - u(D,D)) / (efficient - u(D,D)); classes = 112 behavioural classes of L_6 (3994 programs); mutation per birth at eps = epsN/N, mutants from mu over classes.
P(C,C) = frequency of mutual-cooperation interactions and P(exploit) = frequency of (C,D)+(D,C) interactions over all agent pairs, role draw averaged.

| epsN | coop share (mean ± sd over seeds) | THEM(^C) share | ALLC share | P(cooperator & ALLC coexist) | P(C,C) | P(exploit) |
|---|---|---|---|---|---|---|
| 0.1 | 0.0107 ± 0.0086 | 0.0066 ± 0.0085 | 0.0015 ± 0.0004 | 0.0008 ± 0.0011 | 0.0075 ± 0.0087 | 0.0066 ± 0.0014 |
| 1 | 0.0484 ± 0.0038 | 0.0162 ± 0.0029 | 0.0117 ± 0.0003 | 0.0130 ± 0.0019 | 0.0202 ± 0.0032 | 0.0564 ± 0.0020 |
| 10 | 0.2399 ± 0.0006 | 0.0006 ± 0.0001 | 0.0887 ± 0.0004 | 0.0141 ± 0.0006 | 0.0610 ± 0.0003 | 0.3577 ± 0.0005 |
