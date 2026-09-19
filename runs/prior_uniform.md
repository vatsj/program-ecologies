# Prior diagnostic: weak arm, PD, n=6, N=100, w=0.1 — bits prior vs uniform mu over L_6

Uniform: mu(p) = 1/|L_6| for every program (class weight = number of members / 1852). Bits: mu = 2^-bits as in the sweep.

| state | pi (bits) | pi (uniform) | mu_class (bits) | mu_class (uniform) |
|---|---|---|---|---|
| mono {D:1} | 0.9787 | 0.8790 | 3.289e-01 | 3.089e-01 |
| mono {THEM(^C):1} | 0.0059 | 0.0374 | 9.101e-04 | 7.559e-03 |
| mono {and(X,X):1} | 0.0016 | 0.0143 | 7.542e-03 | 4.968e-02 |
| mono {X:1} | 0.0073 | 0.0102 | 3.124e-01 | 1.760e-01 |
| mono {C:1} | 0.0018 | 0.0078 | 3.289e-01 | 3.089e-01 |
| mono {THEM(^X):1} | 0.0010 | 0.0077 | 8.835e-04 | 6.479e-03 |
| mono {and(THEM(ME),D):1} | 0.0003 | 0.0058 | 1.146e-04 | 2.160e-03 |
| mono {and(THEM(THEM),D):1} | 0.0003 | 0.0058 | 1.146e-04 | 2.160e-03 |
| mono {and(X,and(X,X)):1} | 0.0002 | 0.0056 | 2.823e-04 | 6.479e-03 |
| mono {and(X,THEM(^C)):1} | 0.0002 | 0.0039 | 2.657e-05 | 1.080e-03 |
| mono {and(X,THEM(^X)):1} | 0.0001 | 0.0031 | 2.657e-05 | 1.080e-03 |
| mono {THEM(^D):1} | 0.0002 | 0.0023 | 9.101e-04 | 7.559e-03 |

bits: mean payoff -0.9876, states 118, cooperative all-THEM(^C) share 0.0059, all-D 0.9787, mean bits in support 2.69
uniform: mean payoff -0.9364, states 134, cooperative all-THEM(^C) share 0.0374, all-D 0.8790, mean bits in support 3.55

bits prior: all-D -> all-THEM(^C): P = 2.351e-05 (mu = 9.101e-04, rho = 2.584e-02); exits from all-THEM(^C):
  -> mono {C:1}  P = 3.289e-03  via `C` (mu = 3.289e-01, rho = 1.000e-02)
  -> mono {X:1}  P = 4.553e-04  via `X` (mu = 3.124e-01, rho = 1.457e-03)
  -> mono {THEM(^D):1}  P = 8.592e-05  via `THEM(^D)` (mu = 9.101e-04, rho = 9.441e-02)
  -> mono {D:1}  P = 4.441e-05  via `D` (mu = 3.289e-01, rho = 1.350e-04)
  -> mono {THEM(^X):1}  P = 4.394e-05  via `THEM(^X)` (mu = 8.835e-04, rho = 4.973e-02)

uniform prior: all-D -> all-THEM(^C): P = 1.953e-04 (mu = 7.559e-03, rho = 2.584e-02); exits from all-THEM(^C):
  -> mono {C:1}  P = 3.089e-03  via `C` (mu = 3.089e-01, rho = 1.000e-02)
  -> mono {THEM(^D):1}  P = 7.137e-04  via `THEM(^D)` (mu = 7.559e-03, rho = 9.441e-02)
  -> mono {THEM(^X):1}  P = 3.222e-04  via `THEM(^X)` (mu = 6.479e-03, rho = 4.973e-02)
  -> mono {X:1}  P = 2.565e-04  via `X` (mu = 1.760e-01, rho = 1.457e-03)
  -> mono {or(X,X):1}  P = 2.032e-04  via `or(X,X)` (mu = 4.968e-02, rho = 4.090e-03)

