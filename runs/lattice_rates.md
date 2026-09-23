# Per-mutant rates on the torus (death-birth, von Neumann, weak n=6 with ROLE, 112 classes, w=0.3, mutation off inside trials)

## (a) rho_enter: one R in all-D, success = R share >= 1/2 (2000 trials, cap 20*side generations)

| R | side | rho_enter | undecided | mean generations to 1/2 |
|---|---|---|---|---|
| `THEM(^C)` | 32 | 0.1085 (217/2000) | 0 | 89 |
| `THEM(^C)` | 64 | 0.1130 (226/2000) | 0 | 157 |
| `or(X,THEM(ME))` | 32 | 0.0065 (13/2000) | 3 | 381 |
| `or(X,THEM(ME))` | 64 | 0.0035 (7/2000) | 0 | 829 |
| `THEM(^ROLE)` | 32 | 0.0545 (109/2000) | 0 | 151 |
| `THEM(^ROLE)` | 64 | 0.0700 (140/2000) | 0 | 261 |

## (b) M_exit: mutants from mu one at a time until the R share < 1/2 (50 trials; per-mutant cap 1000 generations)

| R | side | M_exit mean ± sd | median | generations mean | last mutant (top 3) |
|---|---|---|---|---|---|
| `THEM(^C)` | 32 | 1514.2 ± 1233.9 | 1080 | 7571 | `C` 37, `THEM(^D)` 6, `THEM(^X)` 4 |
| `THEM(^C)` | 64 | 2947.0 ± 2776.2 | 1980 | 18280 | `C` 20, `THEM(^D)` 14, `THEM(^ROLE)` 8 |
| `or(X,THEM(ME))` | 32 | 2583.6 ± 1927.0 | 1898 | 19224 | `C` 48, `ROLE` 1, `X` 1 |
| `or(X,THEM(ME))` | 64 | 7485.8 ± 7171.4 | 5649 | 62407 | `C` 45, `or(ROLE,THEM(^D))` 2, `not(THEM(^C))` 2 |
| `THEM(^ROLE)` | 32 | 37.8 ± 37.1 | 22 | 404 | `C` 47, `X` 2, `or(X,X)` 1 |
| `THEM(^ROLE)` | 64 | 47.7 ± 47.2 | 32 | 475 | `C` 50 |

## (c) Shadow pruning: all-R plus one ALLC and one D; lifetimes in generations (500 trials; censored at 5000)

| R | side | ALLC lifetime mean ± sd | ALLC median | ALLC censored | D lifetime mean ± sd | D median | D censored |
|---|---|---|---|---|---|---|---|
| `THEM(^C)` | 32 | 22.8 ± 262.5 | 1.1 | 1 | 1.91 ± 3.30 | 0.71 | 0 |
| `THEM(^C)` | 64 | 11.8 ± 105.5 | 1.0 | 0 | 2.58 ± 4.52 | 0.83 | 0 |
| `or(X,THEM(ME))` | 32 | 7.5 ± 26.3 | 0.9 | 0 | 5.13 ± 16.99 | 1.03 | 0 |
| `or(X,THEM(ME))` | 64 | 16.7 ± 162.1 | 1.2 | 0 | 5.22 ± 15.76 | 1.08 | 0 |
