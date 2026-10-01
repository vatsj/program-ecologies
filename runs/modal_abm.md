# E3: finite-eps N agent-based runs, modal arm (n = 6) vs weak arm (L_6 with X, ROLE); PD, w = 0.3, 200000 generations, second half

R = the arm's reciprocator (modal: FairBot BOX(THEM(ME)); weak: THEM(^C)). Cooperative phases = samples with island-mean P(C,C) > 0.5.

| arm | configuration | P(C,C) per replicate | mean | R share | ALLC share of population | ALLC share of population during cooperative phases |
|---|---|---|---|---|---|---|
| modal n=6 | big island, eps 1e-3 | 0.99, 0.99, 0.99 | 0.989 | 0.090 | 0.258 | 0.261 |
| modal n=6 | big island, eps 1e-3, cooperative start | 0.99, 0.99, 0.99 | 0.989 | 0.130 | 0.261 | 0.269 |
| modal n=6 | big island, eps 1e-4 | 0.97, 1.00, 0.96 | 0.978 | 0.287 | 0.127 | 0.130 |
| modal n=6 | 64 islands, w_g 0 | 0.98, 0.98, 0.98 | 0.980 | 0.125 | 0.105 | 0.105 |
| modal n=6 | 64 islands, w_g 10 | 0.98, 0.98, 0.98 | 0.982 | 0.251 | 0.115 | 0.115 |
| weak L_6 | big island, eps 1e-3 | 0.06, 0.06, 0.08 | 0.064 | 0.025 | 0.023 | 0.232 |
| weak L_6 | big island, eps 1e-3, cooperative start | 0.06, 0.06, 0.08 | 0.064 | 0.025 | 0.023 | 0.232 |
| weak L_6 | big island, eps 1e-4 | 0.00, 0.05, 0.00 | 0.018 | 0.012 | 0.004 | 0.065 |
| weak L_6 | 64 islands, w_g 0 | 0.13, 0.17, 0.13 | 0.144 | 0.028 | 0.063 | 0.054 |
| weak L_6 | 64 islands, w_g 10 | 0.88, 0.94, 0.63 | 0.817 | 0.662 | 0.123 | 0.132 |
