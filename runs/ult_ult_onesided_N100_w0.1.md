### game=ult, arm=onesided, n=5, N=100, w=0.1

proposer programs 902 (24 classes), responder programs 852 (18 classes), states expanded 144, cut flow 7.0e-06, divergence rate 0.0000
on-path rejection rate 0.1101, proposer share 0.5376, responder share 0.3523 (pi-weighted)
conditional programs in the support (pi > 1e-3): (THEM(ME) | H) 0.011, (THEM(ME) | M) 0.003, (THEM(ME) | L) 0.002

| pi | proposer | responder | reject | share P | share R | offer dist | threshold dist |
|---|---|---|---|---|---|---|---|
| 0.3908 | `L` | `L` | 0.000 | 0.800 | 0.200 | [1.0, 0.0, 0.0] | [1.0, 0.0, 0.0] |
| 0.1931 | `M` | `M` | 0.000 | 0.500 | 0.500 | [0.0, 1.0, 0.0] | [0.0, 1.0, 0.0] |
| 0.0727 | `M` | `L` | 0.000 | 0.500 | 0.500 | [0.0, 1.0, 0.0] | [1.0, 0.0, 0.0] |
| 0.0468 | `L` | `X` | 0.667 | 0.267 | 0.067 | [1.0, 0.0, 0.0] | [0.33, 0.33, 0.33] |
| 0.0411 | `X` | `L` | 0.000 | 0.500 | 0.500 | [0.33, 0.33, 0.33] | [1.0, 0.0, 0.0] |
| 0.0380 | `M` | `X` | 0.333 | 0.333 | 0.333 | [0.0, 1.0, 0.0] | [0.33, 0.33, 0.33] |
| 0.0300 | `H` | `H` | 0.000 | 0.200 | 0.800 | [0.0, 0.0, 1.0] | [0.0, 0.0, 1.0] |
| 0.0247 | `X` | `M` | 0.333 | 0.233 | 0.433 | [0.33, 0.33, 0.33] | [0.0, 1.0, 0.0] |
| 0.0233 | `X` | `X` | 0.333 | 0.267 | 0.400 | [0.33, 0.33, 0.33] | [0.33, 0.33, 0.33] |
| 0.0209 | `L` | `H` | 1.000 | 0.000 | 0.000 | [1.0, 0.0, 0.0] | [0.0, 0.0, 1.0] |
| 0.0178 | `H` | `M` | 0.000 | 0.200 | 0.800 | [0.0, 0.0, 1.0] | [0.0, 1.0, 0.0] |
| 0.0160 | `H` | `X` | 0.000 | 0.200 | 0.800 | [0.0, 0.0, 1.0] | [0.33, 0.33, 0.33] |

Transitions out of the top states (P per mutation event; mutant, population, rho, mu):

- (L | L)
    - 5.58e-04 -> (L | X) via `X` in R (rho 4.80e-03, mu 2.32e-01)
    - 3.95e-04 -> (L | H) via `H` in R (rho 3.16e-03, mu 2.50e-01)
    - 3.81e-04 -> (L | M) via `M` in R (rho 3.16e-03, mu 2.41e-01)
    - 1.91e-04 -> (M | L) via `M` in P (rho 1.60e-03, mu 2.40e-01)
- (M | M)
    - 1.25e-03 -> (M | L) via `L` in R (rho 1.00e-02, mu 2.50e-01)
    - 4.55e-04 -> (M | X) via `X` in R (rho 3.91e-03, mu 2.32e-01)
    - 2.33e-04 -> (X | M) via `X` in P (rho 2.02e-03, mu 2.31e-01)
    - 1.98e-04 -> (H | M) via `H` in P (rho 1.60e-03, mu 2.48e-01)
- (M | L)
    - 3.86e-03 -> (L | L) via `L` in P (rho 3.11e-02, mu 2.48e-01)
    - 1.21e-03 -> (M | M) via `M` in R (rho 1.00e-02, mu 2.41e-01)
    - 1.16e-03 -> (X | L) via `X` in P (rho 1.00e-02, mu 2.31e-01)
    - 4.55e-04 -> (M | X) via `X` in R (rho 3.91e-03, mu 2.32e-01)
- (L | X)
    - 2.25e-03 -> (L | L) via `L` in R (rho 1.80e-02, mu 2.50e-01)
    - 1.64e-03 -> (M | X) via `M` in P (rho 1.37e-02, mu 2.40e-01)
    - 1.16e-03 -> (X | X) via `X` in P (rho 1.00e-02, mu 2.31e-01)
    - 8.82e-04 -> (L | H) via `H` in R (rho 7.06e-03, mu 2.50e-01)
- (X | L)
    - 3.86e-03 -> (L | L) via `L` in P (rho 3.11e-02, mu 2.48e-01)
    - 1.20e-03 -> (M | L) via `M` in P (rho 1.00e-02, mu 2.40e-01)
    - 8.51e-04 -> (X | M) via `M` in R (rho 7.06e-03, mu 2.41e-01)
    - 6.80e-04 -> (X | X) via `X` in R (rho 5.85e-03, mu 2.32e-01)
- (M | X)
    - 2.55e-03 -> (M | L) via `L` in R (rho 2.04e-02, mu 2.50e-01)
    - 2.46e-03 -> (M | M) via `M` in R (rho 2.04e-02, mu 2.41e-01)
    - 8.76e-04 -> (L | X) via `L` in P (rho 7.06e-03, mu 2.48e-01)
    - 8.17e-04 -> (X | X) via `X` in P (rho 7.06e-03, mu 2.31e-01)

