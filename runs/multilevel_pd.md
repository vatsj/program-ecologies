# Island-level selection on emigration: pd, 64 islands of 100, complete graph, mN = 1, eps N = 0.1 per island, w = 0.3, start all-D, 500000 generations (finite eps N: approach rate, not the eps->0 object)

| w_g | P(C,C) 2nd half mean ± sd | P(C,C) 1st half mean | payoff | exits from THEM(^C) islands: faker / shadow / other (pooled) | dominant classes, 2nd half (rep 0) |
|---|---|---|---|---|---|
| 0 | 0.129 ± 0.023 | 0.140 | -0.786 | 6582 / 4286 / 341 | `D` 0.71, `THEM(^ROLE)` 0.13, `THEM(^X)` 0.04, `THEM(^C)` 0.03 |
| 1 | 0.148 ± 0.023 | 0.141 | -0.763 | 6188 / 3375 / 357 | `D` 0.63, `THEM(^ROLE)` 0.13, `THEM(^X)` 0.11, `C` 0.06 |
| 3 | 0.233 ± 0.016 | 0.226 | -0.669 | 2225 / 1159 / 370 | `D` 0.43, `THEM(^X)` 0.26, `C` 0.12, `and(X,THEM(ME))` 0.11 |
| 10 | 0.748 ± 0.065 | 0.730 | -0.217 | 61382 / 188546 / 6948 | `THEM(^C)` 0.61, `D` 0.16, `C` 0.12, `X` 0.02 |

Per replicate second-half P(C,C): w_g=0: 0.10, 0.17, 0.13, 0.14, 0.11; w_g=1: 0.15, 0.17, 0.16, 0.10, 0.15; w_g=3: 0.23, 0.23, 0.20, 0.25, 0.25; w_g=10: 0.76, 0.83, 0.74, 0.77, 0.63
