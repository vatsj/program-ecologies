# lim_N: weak arm, n=6, N=1000 (with N=10, 100 from the sweep for comparison)

## pd, w=0.1, N=1000   (chain 2s, 118 states, cut flow 6.5e-08, poly_flow 6.5e-08)

pi(all-D) = 0.9796, pi(all-THEM(^C)) = 1.632e-02, pi(all-C) = 3.797e-04, mass on fully cooperative states = 1.670e-02, mean payoff -0.9827

Entries into all-THEM(^C) (per mutation event at the source; rate = mu * rho):

| from | mutant | mu | rho | mu*rho | pi(from) | flow pi*P |
|---|---|---|---|---|---|---|
| mono {D:1} | `THEM(^C)` | 6.79e-04 | 8.321e-03 | 5.647e-06 | 9.796e-01 | 7.418e-06 |
| mono {and(X,THEM(THEM)):1} | `THEM(^C)` | 6.79e-04 | 5.253e-02 | 3.565e-05 | 2.118e-04 | 1.013e-08 |
| mono {and(THEM(THEM),X):1} | `THEM(^C)` | 6.79e-04 | 5.253e-02 | 3.565e-05 | 2.101e-04 | 1.004e-08 |
| mono {and(X,THEM(^C)):1} | `THEM(^C)` | 6.79e-04 | 2.715e-02 | 1.843e-05 | 3.308e-04 | 8.175e-09 |
| mono {THEM(THEM):1} | `THEM(^C)` | 6.79e-04 | 9.898e-02 | 6.717e-05 | 7.413e-05 | 6.677e-09 |

Exits from all-THEM(^C):

| to | mutant | mu | rho | mu*rho | P(exit) |
|---|---|---|---|---|---|
| mono {C:1} | `C` | 2.45e-01 | 1.000e-03 | 2.453e-04 | 3.289e-04 |
| mono {THEM(^D):1} | `THEM(^D)` | 6.79e-04 | 9.126e-02 | 6.193e-05 | 8.305e-05 |
| mono {THEM(^X):1} | `THEM(^X)` | 6.59e-04 | 4.781e-02 | 3.149e-05 | 4.223e-05 |
| mono {or(X,THEM(^D)):1} | `or(X,THEM(^D))` | 1.98e-05 | 4.825e-02 | 9.559e-07 | 1.282e-06 |
| mono {THEM(^and(X,X)):1} | `THEM(^and(X,X))` | 9.91e-06 | 7.004e-02 | 6.938e-07 | 9.304e-07 |
| mono {or(X,THEM(^X)):1} | `or(X,THEM(^X))` | 1.98e-05 | 2.494e-02 | 4.942e-07 | 6.627e-07 |

Total exit probability per mutation event at all-THEM(^C): 4.578e-04 (mean residence 1/4.578e-04 = 2.18e+03 events); stationary in-flow 7.470e-06.

## pd, w=1, N=1000   (chain 37s, 834 states, cut flow 3.2e-06, poly_flow 8.2e-05)

pi(all-D) = 0.6950, pi(all-THEM(^C)) = 2.879e-01, pi(all-C) = 2.055e-03, mass on fully cooperative states = 2.900e-01, mean payoff -0.7051

Entries into all-THEM(^C) (per mutation event at the source; rate = mu * rho):

| from | mutant | mu | rho | mu*rho | pi(from) | flow pi*P |
|---|---|---|---|---|---|---|
| mono {D:1} | `THEM(^C)` | 6.79e-04 | 4.998e-01 | 3.391e-04 | 6.950e-01 | 3.161e-04 |
| mono {and(X,THEM(^C)):1} | `THEM(^C)` | 6.79e-04 | 4.995e-01 | 3.390e-04 | 1.489e-03 | 6.770e-07 |
| poly {THEM(ME):0.333, and(X,THEM(^C)):0.667} | `THEM(^C)` | 6.79e-04 | 4.991e-01 | 3.387e-04 | 1.025e-03 | 4.655e-07 |
| poly {C:0.267, THEM(THEM):0.199, THEM(^C):0.003, and(X,THEM(^X)):0.531} | `X` | 2.33e-01 | 6.364e-02 | 1.483e-02 | 1.360e-05 | 1.823e-07 |
| poly {C:0.267, THEM(THEM):0.199, THEM(^C):0.003, and(X,THEM(^X)):0.531} | `or(X,X)` | 5.62e-03 | 2.110e-02 | 1.187e-04 | 1.360e-05 | 1.823e-07 |
| mono {and(THEM(THEM),D):1} | `THEM(^C)` | 6.79e-04 | 4.998e-01 | 3.391e-04 | 2.388e-04 | 1.086e-07 |

Exits from all-THEM(^C):

| to | mutant | mu | rho | mu*rho | P(exit) |
|---|---|---|---|---|---|
| mono {THEM(^D):1} | `THEM(^D)` | 6.79e-04 | 5.015e-01 | 3.403e-04 | 4.564e-04 |
| mono {C:1} | `C` | 2.45e-01 | 1.000e-03 | 2.453e-04 | 3.289e-04 |
| mono {THEM(^X):1} | `THEM(^X)` | 6.59e-04 | 3.344e-01 | 2.203e-04 | 2.955e-04 |
| mono {or(X,THEM(^D)):1} | `or(X,THEM(^D))` | 1.98e-05 | 3.347e-01 | 6.631e-06 | 8.892e-06 |
| mono {THEM(^and(X,X)):1} | `THEM(^and(X,X))` | 9.91e-06 | 4.299e-01 | 4.259e-06 | 5.711e-06 |
| mono {or(X,THEM(^X)):1} | `or(X,THEM(^X))` | 1.98e-05 | 2.010e-01 | 3.983e-06 | 5.342e-06 |

Total exit probability per mutation event at all-THEM(^C): 1.104e-03 (mean residence 1/1.104e-03 = 906 events); stationary in-flow 3.179e-04.

## stag, w=0.1, N=1000   (chain 2s, 108 states, cut flow 2.1e-07, poly_flow 2.1e-07)

pi(all-D) = 0.0146, pi(all-THEM(^C)) = 2.992e-03, pi(all-C) = 9.798e-01, mass on fully cooperative states = 9.853e-01, mean payoff 3.9853

Entries into all-THEM(^C) (per mutation event at the source; rate = mu * rho):

| from | mutant | mu | rho | mu*rho | pi(from) | flow pi*P |
|---|---|---|---|---|---|---|
| mono {C:1} | `THEM(^C)` | 6.79e-04 | 1.000e-03 | 6.786e-07 | 9.798e-01 | 8.916e-07 |
| mono {D:1} | `THEM(^C)` | 6.79e-04 | 6.937e-03 | 4.707e-06 | 1.464e-02 | 9.239e-08 |
| mono {or(X,THEM(ME)):1} | `THEM(^C)` | 6.79e-04 | 1.000e-03 | 6.786e-07 | 2.623e-04 | 2.387e-10 |
| mono {or(X,THEM(THEM)):1} | `THEM(^C)` | 6.79e-04 | 1.000e-03 | 6.786e-07 | 2.622e-04 | 2.386e-10 |
| mono {THEM(ME):1} | `THEM(^C)` | 6.79e-04 | 7.040e-02 | 4.777e-05 | 2.298e-06 | 1.472e-10 |

Exits from all-THEM(^C):

| to | mutant | mu | rho | mu*rho | P(exit) |
|---|---|---|---|---|---|
| mono {C:1} | `C` | 2.45e-01 | 1.000e-03 | 2.453e-04 | 3.289e-04 |
| mono {or(X,THEM(ME)):1} | `or(X,THEM(ME))` | 6.56e-05 | 1.000e-03 | 6.562e-08 | 8.799e-08 |
| mono {or(X,THEM(THEM)):1} | `or(X,THEM(THEM))` | 6.56e-05 | 1.000e-03 | 6.562e-08 | 8.799e-08 |
| mono {or(X,THEM(^C)):1} | `or(X,THEM(^C))` | 1.98e-05 | 1.000e-03 | 1.981e-08 | 2.657e-08 |
| mono {or(X,THEM(^X)):1} | `or(X,THEM(^X))` | 1.98e-05 | 1.078e-04 | 2.136e-09 | 2.864e-09 |
| poly {THEM(^C):0.5, THEM(^X):0.5} | `THEM(^X)` | 6.59e-04 | 6.978e-07 | 4.597e-10 | 6.165e-10 |

Total exit probability per mutation event at all-THEM(^C): 3.292e-04 (mean residence 1/3.292e-04 = 3.04e+03 events); stationary in-flow 9.850e-07.

## stag, w=1, N=1000   (chain 2s, 108 states, cut flow 3.5e-15, poly_flow 3.5e-15)

pi(all-D) = 0.0000, pi(all-THEM(^C)) = 2.446e-03, pi(all-C) = 8.843e-01, mass on fully cooperative states = 1.000e+00, mean payoff 4.0000

Entries into all-THEM(^C) (per mutation event at the source; rate = mu * rho):

| from | mutant | mu | rho | mu*rho | pi(from) | flow pi*P |
|---|---|---|---|---|---|---|
| mono {C:1} | `THEM(^C)` | 6.79e-04 | 1.000e-03 | 6.786e-07 | 8.843e-01 | 8.047e-07 |
| mono {or(X,THEM(ME)):1} | `THEM(^C)` | 6.79e-04 | 1.000e-03 | 6.786e-07 | 2.366e-04 | 2.153e-10 |
| mono {or(X,THEM(THEM)):1} | `THEM(^C)` | 6.79e-04 | 1.000e-03 | 6.786e-07 | 2.366e-04 | 2.153e-10 |
| mono {or(X,THEM(^C)):1} | `THEM(^C)` | 6.79e-04 | 1.000e-03 | 6.786e-07 | 7.143e-05 | 6.500e-11 |
| mono {D:1} | `THEM(^C)` | 6.79e-04 | 1.241e-02 | 8.424e-06 | 2.280e-09 | 2.575e-14 |

Exits from all-THEM(^C):

| to | mutant | mu | rho | mu*rho | P(exit) |
|---|---|---|---|---|---|
| mono {C:1} | `C` | 2.45e-01 | 1.000e-03 | 2.453e-04 | 3.289e-04 |
| mono {or(X,THEM(ME)):1} | `or(X,THEM(ME))` | 6.56e-05 | 1.000e-03 | 6.562e-08 | 8.799e-08 |
| mono {or(X,THEM(THEM)):1} | `or(X,THEM(THEM))` | 6.56e-05 | 1.000e-03 | 6.562e-08 | 8.799e-08 |
| mono {or(X,THEM(^C)):1} | `or(X,THEM(^C))` | 1.98e-05 | 1.000e-03 | 1.981e-08 | 2.657e-08 |
| mono {or(X,THEM(^X)):1} | `or(X,THEM(^X))` | 1.98e-05 | 3.934e-07 | 7.794e-12 | 1.045e-11 |
| mono {or(X,THEM(^D)):1} | `or(X,THEM(^D))` | 1.98e-05 | 1.153e-10 | 2.284e-15 | 3.063e-15 |

Total exit probability per mutation event at all-THEM(^C): 3.291e-04 (mean residence 1/3.291e-04 = 3.04e+03 events); stationary in-flow 8.052e-07.

## N series (weak arm, n=6)

| game | w | N | all-D | all-THEM(^C) | all-C | mean payoff |
|---|---|---|---|---|---|---|
| pd | 0.1 | 10 | 0.5277 | 1.15e-03 | 1.68e-01 | -0.6849 |
| pd | 0.1 | 100 | 0.9787 | 5.89e-03 | 1.81e-03 | -0.9876 |
| pd | 0.1 | 1000 | 0.9796 | 1.63e-02 | 0.00e+00 | -0.9827 |
| pd | 1 | 10 | 0.9692 | 1.20e-02 | 3.14e-03 | -0.9801 |
| pd | 1 | 100 | 0.8820 | 9.88e-02 | 2.86e-03 | -0.8932 |
| pd | 1 | 1000 | 0.6950 | 2.88e-01 | 2.06e-03 | -0.7051 |
| stag | 0.1 | 10 | 0.5331 | 1.16e-03 | 1.02e-01 | 3.0497 |
| stag | 0.1 | 100 | 0.9707 | 5.54e-03 | 1.40e-02 | 3.0191 |
| stag | 0.1 | 1000 | 0.0146 | 2.99e-03 | 9.80e-01 | 3.9853 |
| stag | 1 | 10 | 0.9070 | 1.93e-03 | 1.29e-02 | 2.9959 |
| stag | 1 | 100 | 0.9221 | 9.94e-03 | 6.25e-02 | 3.0725 |
| stag | 1 | 1000 | 0.0000 | 2.45e-03 | 8.84e-01 | 4.0000 |
