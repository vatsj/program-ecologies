### game=ult, arm=mutual, n=5, N=100, w=0.1

proposer programs 902 (44 classes), responder programs 902 (44 classes), states expanded 152, cut flow 2.6e-05, divergence rate 0.0012
on-path rejection rate 0.1094, proposer share 0.5400, responder share 0.3506 (pi-weighted)
conditional programs in the support (pi > 1e-3): (THEM(THEM) | H) 0.004, (THEM(ME) | H) 0.004, (L | THEM(THEM)) 0.004, (L | THEM(ME)) 0.004, (THEM(THEM) | M) 0.001, (THEM(ME) | M) 0.001

| pi | proposer | responder | reject | share P | share R | offer dist | threshold dist |
|---|---|---|---|---|---|---|---|
| 0.3874 | `L` | `L` | 0.000 | 0.800 | 0.200 | [1.0, 0.0, 0.0] | [1.0, 0.0, 0.0] |
| 0.1911 | `M` | `M` | 0.000 | 0.500 | 0.500 | [0.0, 1.0, 0.0] | [0.0, 1.0, 0.0] |
| 0.0716 | `M` | `L` | 0.000 | 0.500 | 0.500 | [0.0, 1.0, 0.0] | [1.0, 0.0, 0.0] |
| 0.0468 | `L` | `X` | 0.667 | 0.267 | 0.067 | [1.0, 0.0, 0.0] | [0.33, 0.33, 0.33] |
| 0.0405 | `X` | `L` | 0.000 | 0.500 | 0.500 | [0.33, 0.33, 0.33] | [1.0, 0.0, 0.0] |
| 0.0376 | `M` | `X` | 0.333 | 0.333 | 0.333 | [0.0, 1.0, 0.0] | [0.33, 0.33, 0.33] |
| 0.0298 | `H` | `H` | 0.000 | 0.200 | 0.800 | [0.0, 0.0, 1.0] | [0.0, 0.0, 1.0] |
| 0.0245 | `X` | `M` | 0.333 | 0.233 | 0.433 | [0.33, 0.33, 0.33] | [0.0, 1.0, 0.0] |
| 0.0231 | `X` | `X` | 0.333 | 0.267 | 0.400 | [0.33, 0.33, 0.33] | [0.33, 0.33, 0.33] |
| 0.0209 | `L` | `H` | 1.000 | 0.000 | 0.000 | [1.0, 0.0, 0.0] | [0.0, 0.0, 1.0] |
| 0.0177 | `H` | `M` | 0.000 | 0.200 | 0.800 | [0.0, 0.0, 1.0] | [0.0, 1.0, 0.0] |
| 0.0159 | `H` | `X` | 0.000 | 0.200 | 0.800 | [0.0, 0.0, 1.0] | [0.33, 0.33, 0.33] |

Transitions out of the top states (P per mutation event; mutant, population, rho, mu):

- (L | L)
    - 5.56e-04 -> (L | X) via `X` in R (rho 4.80e-03, mu 2.31e-01)
    - 3.92e-04 -> (L | H) via `H` in R (rho 3.16e-03, mu 2.48e-01)
    - 3.79e-04 -> (L | M) via `M` in R (rho 3.16e-03, mu 2.40e-01)
    - 1.91e-04 -> (M | L) via `M` in P (rho 1.60e-03, mu 2.40e-01)
- (M | M)
    - 1.24e-03 -> (M | L) via `L` in R (rho 1.00e-02, mu 2.48e-01)
    - 4.53e-04 -> (M | X) via `X` in R (rho 3.91e-03, mu 2.31e-01)
    - 2.33e-04 -> (X | M) via `X` in P (rho 2.02e-03, mu 2.31e-01)
    - 1.98e-04 -> (H | M) via `H` in P (rho 1.60e-03, mu 2.48e-01)
- (M | L)
    - 3.86e-03 -> (L | L) via `L` in P (rho 3.11e-02, mu 2.48e-01)
    - 1.20e-03 -> (M | M) via `M` in R (rho 1.00e-02, mu 2.40e-01)
    - 1.16e-03 -> (X | L) via `X` in P (rho 1.00e-02, mu 2.31e-01)
    - 4.53e-04 -> (M | X) via `X` in R (rho 3.91e-03, mu 2.31e-01)
- (L | X)
    - 2.23e-03 -> (L | L) via `L` in R (rho 1.80e-02, mu 2.48e-01)
    - 1.64e-03 -> (M | X) via `M` in P (rho 1.37e-02, mu 2.40e-01)
    - 1.16e-03 -> (X | X) via `X` in P (rho 1.00e-02, mu 2.31e-01)
    - 8.76e-04 -> (H | X) via `H` in P (rho 7.06e-03, mu 2.48e-01)
- (X | L)
    - 3.86e-03 -> (L | L) via `L` in P (rho 3.11e-02, mu 2.48e-01)
    - 1.20e-03 -> (M | L) via `M` in P (rho 1.00e-02, mu 2.40e-01)
    - 8.46e-04 -> (X | M) via `M` in R (rho 7.06e-03, mu 2.40e-01)
    - 6.77e-04 -> (X | X) via `X` in R (rho 5.85e-03, mu 2.31e-01)
- (M | X)
    - 2.53e-03 -> (M | L) via `L` in R (rho 2.04e-02, mu 2.48e-01)
    - 2.44e-03 -> (M | M) via `M` in R (rho 2.04e-02, mu 2.40e-01)
    - 8.75e-04 -> (L | X) via `L` in P (rho 7.06e-03, mu 2.48e-01)
    - 8.17e-04 -> (X | X) via `X` in P (rho 7.06e-03, mu 2.31e-01)

