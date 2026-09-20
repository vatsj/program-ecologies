### game=ult_out, arm=mutual, n=5, N=100, w=0.1

proposer programs 902 (44 classes), responder programs 902 (45 classes), states expanded 160, cut flow 2.9e-05, divergence rate 0.0012
on-path rejection rate 0.2156, proposer share 0.3705, responder share 0.4785 (pi-weighted)
conditional programs in the support (pi > 1e-3): (THEM(THEM) | H) 0.004, (THEM(ME) | H) 0.004, (THEM(THEM) | M) 0.001, (THEM(ME) | M) 0.001

| pi | proposer | responder | reject | share P | share R | offer dist | threshold dist |
|---|---|---|---|---|---|---|---|
| 0.2338 | `M` | `M` | 0.000 | 0.500 | 0.500 | [0.0, 1.0, 0.0] | [0.0, 1.0, 0.0] |
| 0.1018 | `L` | `L` | 0.000 | 0.800 | 0.200 | [1.0, 0.0, 0.0] | [1.0, 0.0, 0.0] |
| 0.0827 | `M` | `X` | 0.333 | 0.333 | 0.433 | [0.0, 1.0, 0.0] | [0.33, 0.33, 0.33] |
| 0.0770 | `M` | `L` | 0.000 | 0.500 | 0.500 | [0.0, 1.0, 0.0] | [1.0, 0.0, 0.0] |
| 0.0729 | `H` | `H` | 0.000 | 0.200 | 0.800 | [0.0, 0.0, 1.0] | [0.0, 0.0, 1.0] |
| 0.0540 | `L` | `X` | 0.667 | 0.267 | 0.267 | [1.0, 0.0, 0.0] | [0.33, 0.33, 0.33] |
| 0.0461 | `L` | `H` | 1.000 | 0.000 | 0.300 | [1.0, 0.0, 0.0] | [0.0, 0.0, 1.0] |
| 0.0413 | `X` | `M` | 0.333 | 0.233 | 0.533 | [0.33, 0.33, 0.33] | [0.0, 1.0, 0.0] |
| 0.0396 | `X` | `X` | 0.333 | 0.267 | 0.500 | [0.33, 0.33, 0.33] | [0.33, 0.33, 0.33] |
| 0.0317 | `X` | `L` | 0.000 | 0.500 | 0.500 | [0.33, 0.33, 0.33] | [1.0, 0.0, 0.0] |
| 0.0316 | `H` | `M` | 0.000 | 0.200 | 0.800 | [0.0, 0.0, 1.0] | [0.0, 1.0, 0.0] |
| 0.0312 | `X` | `H` | 0.667 | 0.067 | 0.467 | [0.33, 0.33, 0.33] | [0.0, 0.0, 1.0] |

Transitions out of the top states (P per mutation event; mutant, population, rho, mu):

- (M | M)
    - 1.24e-03 -> (M | L) via `L` in R (rho 1.00e-02, mu 2.48e-01)
    - 8.17e-04 -> (M | X) via `X` in R (rho 7.06e-03, mu 2.31e-01)
    - 3.92e-04 -> (M | H) via `H` in R (rho 3.16e-03, mu 2.48e-01)
    - 2.33e-04 -> (X | M) via `X` in P (rho 2.02e-03, mu 2.31e-01)
- (L | L)
    - 1.95e-03 -> (L | H) via `H` in R (rho 1.57e-02, mu 2.48e-01)
    - 1.89e-03 -> (L | M) via `M` in R (rho 1.57e-02, mu 2.40e-01)
    - 1.58e-03 -> (L | X) via `X` in R (rho 1.37e-02, mu 2.31e-01)
    - 1.91e-04 -> (M | L) via `M` in P (rho 1.60e-03, mu 2.40e-01)
- (M | X)
    - 1.69e-03 -> (M | L) via `L` in R (rho 1.37e-02, mu 2.48e-01)
    - 1.64e-03 -> (M | M) via `M` in R (rho 1.37e-02, mu 2.40e-01)
    - 8.75e-04 -> (L | X) via `L` in P (rho 7.06e-03, mu 2.48e-01)
    - 8.17e-04 -> (X | X) via `X` in P (rho 7.06e-03, mu 2.31e-01)
- (M | L)
    - 3.86e-03 -> (L | L) via `L` in P (rho 3.11e-02, mu 2.48e-01)
    - 1.20e-03 -> (M | M) via `M` in R (rho 1.00e-02, mu 2.40e-01)
    - 1.16e-03 -> (X | L) via `X` in P (rho 1.00e-02, mu 2.31e-01)
    - 8.17e-04 -> (M | X) via `X` in R (rho 7.06e-03, mu 2.31e-01)
- (H | H)
    - 1.24e-03 -> (H | L) via `L` in R (rho 1.00e-02, mu 2.48e-01)
    - 1.20e-03 -> (H | M) via `M` in R (rho 1.00e-02, mu 2.40e-01)
    - 1.16e-03 -> (H | X) via `X` in R (rho 1.00e-02, mu 2.31e-01)
    - 5.56e-04 -> (X | H) via `X` in P (rho 4.80e-03, mu 2.31e-01)
- (L | X)
    - 1.64e-03 -> (M | X) via `M` in P (rho 1.37e-02, mu 2.40e-01)
    - 1.46e-03 -> (L | H) via `H` in R (rho 1.17e-02, mu 2.48e-01)
    - 1.41e-03 -> (L | M) via `M` in R (rho 1.17e-02, mu 2.40e-01)
    - 1.16e-03 -> (X | X) via `X` in P (rho 1.00e-02, mu 2.31e-01)

