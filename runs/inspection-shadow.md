# The inspection game's enforcer and its shadow (run report, 2026-10-24)

Spec `specs/2026-10-24-inspection-shadow.md`; predictions `predictions/2026-10-24-inspection-shadow.md`; notes `notes/inspection-shadow.md`; code `src/inspection_shadow*.py`; rows `runs/inspection_shadow/`. **Chain** = the ε → 0 object (π over pairs of monomorphic role classes, the whole state space of 157² or 167² pairs, no exploration cap); **lottery** = the ε = 0 seed lottery at the stated (N, I), mN, horizon 20N, with the declared rain in the rain cells; never π. Payoffs are game payoffs (gross of the price). Intervals are run-clustered 95% bootstrap (4,000 resamples).

## Completeness

85 of 85 jobs of the job file have an output.

## Statics: twin relation, sets, prudent class, priors

- c = 0: K = [157, 157]; |E| = 1246, |R| = 849, |R*| = 530 pair states. Twins of the net payoff of `N` against `C`: 38 classes, mass 0.31052 (`N` 0.30696, deterring 0.00332, other 0.00024). Net payoffs (inspector, inspectee): (CRI, C) = (0.00, 0.00) with 1 level charged; (N, C) = (0.00, 0.00) with 0.
- c = 0.01: K = [167, 167]; |E| = 1586, |R| = 1001, |R*| = 624 pair states. Twins of the net payoff of `N` against `C`: 1 classes, mass 0.30687 (`N` 0.30687, deterring 0.00000, other 0.00000). Net payoffs (inspector, inspectee): (CRI, C) = (-0.01, 0.00) with 1 level charged; (N, C) = (0.00, 0.00) with 0.
- Prudent class (eight classes, 38 spellings, mass 0.000738): `cr(THEM(^K))` (cost 2 vs CRI, 1 vs N); `cr(THEM(^X))` (cost 2 vs CRI, 1 vs N); `if(THEM(^K)=I,C,K)` (cost 2 vs CRI, 1 vs N); `cr(coin(N,THEM(^K)))` (cost 2 vs CRI, 1 vs N); `if(THEM(^X)=I,C,K)` (cost 2 vs CRI, 1 vs N); `cr(THEM(^coin(C,X)))` (cost 2 vs CRI, 1 vs N); `cr(coin(N,THEM(^X)))` (cost 2 vs CRI, 1 vs N); `cr(THEM(^coin(K,X)))` (cost 2 vs CRI, 1 vs N).
- Boost x10: m(S) 0.000738 → 0.007380, added mass 0.006642 taken from all other inspectee classes; control: the same 0.006642 added to `C` (0.37887 → 0.38551), taken from all classes outside `C`.

- `lottery3` equals `mixed2.lottery2` when no rain or arrival is used: **True**; weighted founders at factor 1 equal the unweighted draw: **True**.

## Chain, exact arm, c = 0 (whole state space, ε → 0)

| N | π(E) | odds E | π(R) | π(R*) | π(E*) | mean inspector payoff | mean inspectee payoff | inspection prob | cheat prob | forfeit mass in E | peak RSS GB | check vs two-role run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.2784 | 0.3858 | 0.1058 | 0.0981 | 0.2784 | -0.7769 | -0.1782 | 0.440 | 0.172 | 1.17e-05 | 1.7 | -0.777 vs -0.777 |
| 1000 | 0.3432 | 0.5225 | 0.2789 | 0.2519 | 0.3432 | -0.4959 | -0.0535 | 0.319 | 0.077 | 1.64e-04 | 1.8 | -0.496 vs -0.496 |
| 10000 | 0.1570 | 0.1862 | 0.1457 | 0.1163 | 0.1570 | -0.4707 | 0.0291 | 0.281 | 0.054 | 3.76e-04 | 2.6 | -0.471 vs -0.471 |
| 100000 | 0.0466 | 0.04891 | 0.0441 | 0.0315 | 0.0466 | -0.5327 | 0.0485 | 0.313 | 0.057 | 1.75e-04 | 2.4 | - |

Odds of E: least-squares slope of log odds on log N over N ≥ 10³: -0.514.

**Conditional exit hazard from R** (per mutation event; flux / π(R)), by category:

| category | N = 100 | N = 1000 | N = 10000 | N = 100000 | slope (N ≥ 10³) |
|---|---|---|---|---|---|
| A neutral shadow | 1.495e-03 | 1.365e-04 | 1.137e-05 | 1.002e-06 | -1.07 |
| B neutral other | 4.752e-05 | 3.762e-06 | 3.379e-07 | 3.234e-08 | -1.03 |
| C strict K | 0 | 0 | 0 | 0 | n/a |
| D strict non-reading inspectee | 1.271e-04 | 8.178e-05 | 7.382e-05 | 7.913e-05 | -0.01 |
| E strict reading inspectee (clean) | 8.503e-05 | 5.590e-05 | 3.526e-05 | 3.026e-05 | -0.13 |
| E strict reading inspectee (forfeit-driven) | 0 | 0 | 0 | 0 | n/a |
| F strict inspector | 7.317e-07 | 1.183e-07 | 2.824e-08 | 1.595e-08 | -0.44 |
| G deleterious | 2.384e-06 | 3.765e-09 | 1.589e-10 | 7.024e-12 | -1.36 |
| **total** | 1.758e-03 | 2.781e-04 | 1.208e-04 | 1.104e-04 | -0.20 |
| largest | A | A | D | D | |

**Conditional exit hazard from E** (per mutation event; flux / π(E)), by category:

| category | N = 100 | N = 1000 | N = 10000 | N = 100000 | slope (N ≥ 10³) |
|---|---|---|---|---|---|
| A neutral shadow | 0 | 0 | 0 | 0 | n/a |
| B neutral other | 1.882e-05 | 3.151e-06 | 3.208e-07 | 3.144e-08 | -1.00 |
| C strict K | 2.385e-02 | 7.199e-03 | 2.766e-03 | 2.107e-03 | -0.27 |
| D strict non-reading inspectee | 1.360e-02 | 4.157e-03 | 1.639e-03 | 1.269e-03 | -0.26 |
| E strict reading inspectee (clean) | 3.781e-04 | 1.498e-04 | 7.282e-05 | 5.912e-05 | -0.20 |
| E strict reading inspectee (forfeit-driven) | 0 | 0 | 0 | 0 | n/a |
| F strict inspector | 0 | 0 | 0 | 0 | n/a |
| G deleterious | 1.860e-06 | 3.108e-09 | 1.498e-10 | 6.768e-12 | -1.33 |
| **total** | 3.784e-02 | 1.151e-02 | 4.478e-03 | 3.435e-03 | -0.26 |
| largest | C | C | C | C | |

Strict inspectee flux out of E by the resident inspector (deterring / not deterring K): N = 100: 2.25e-05 / 1.05e-02; N = 1000: 3.84e-05 / 3.91e-03; N = 10000: 1.59e-05 / 6.87e-04; N = 100000: 4.82e-06 / 1.55e-04.

**Renewal identities** (exact; mutation events): mean sojourn in R, mean time outside R, mean sojourn in E, mean time outside E:

| N | sojourn R | outside R | sojourn E | outside E |
|---|---|---|---|---|
| 100 | 568.9 | 4806 | 26.43 | 68.49 |
| 1000 | 3596 | 9298 | 86.89 | 166.3 |
| 10000 | 8277 | 4.855e+04 | 223.3 | 1199 |
| 100000 | 9054 | 1.964e+05 | 291.1 | 5953 |

**Where π sits outside E** (occupancy of the detour categories; exclusive, in this order): 

| N | E | forfeit | shadow_excursion | cheater_major_other | light_cheater | committed_compliant | mixing | other |
|---|---|---|---|---|---|---|---|---|
| 100 | 0.2784 | 0.0000 | 0.0507 | 0.0600 | 0.0094 | 0.4321 | 0.1693 | 0.0000 |
| 1000 | 0.3432 | 0.0000 | 0.0188 | 0.0223 | 0.0865 | 0.4519 | 0.0773 | 0.0000 |
| 10000 | 0.1570 | 0.0000 | 0.0033 | 0.0040 | 0.2712 | 0.5269 | 0.0377 | 0.0000 |
| 100000 | 0.0466 | 0.0000 | 0.0007 | 0.0009 | 0.2976 | 0.5973 | 0.0569 | 0.0000 |

**First passage into E and into R** from the named states (exact, same elimination pass; mutation events; P(R) = probability that the first E state entered is in R):

N = 100:
| start | P(first entry in R) | mean time to E | mean time to R | time to E in: shadow excursion / cheater-major / light cheater / committed / mixing / forfeit | visits |
|---|---|---|---|---|---|
| (N,K) | 0.0173 | 60.45 | 4770 | 6.14 / 7.33 / 0.173 / 37 / 9.76 / 9.59e-07 | 3.95 |
| (I,K) | 0.0112 | 50.84 | 4789 | 0.0977 / 6.06 / 0.132 / 35.4 / 9.17 / 2.93e-08 | 2.82 |
| (I,C) | 0.0108 | 34.62 | 4775 | 0.0712 / 0.0658 / 0.00508 / 30.8 / 3.66 / 8.42e-09 | 1.43 |
| (CRI,light1/8) | 0.1155 | 654.3 | 4893 | 4.39 / 5.24 / 589 / 40.5 / 14.9 / 1.41e-06 | 5.44 |
| (N,light1/8) | 0.0173 | 86.59 | 4796 | 4.94 / 5.85 / 19.9 / 40.6 / 15.3 / 1.56e-06 | 4.94 |
| (P38,C) | 0.0108 | 61.67 | 4802 | 0.0455 / 0.0431 / 0.00978 / 59.5 / 2.09 / 5.7e-09 | 1.08 |

N = 1000:
| start | P(first entry in R) | mean time to E | mean time to R | time to E in: shadow excursion / cheater-major / light cheater / committed / mixing / forfeit | visits |
|---|---|---|---|---|---|
| (N,K) | 0.0184 | 92.35 | 7254 | 6.1 / 7.29 / 0.514 / 67.1 / 11.3 / 9.51e-08 | 3.91 |
| (I,K) | 0.0123 | 83.1 | 7289 | 0.0515 / 6.02 / 0.234 / 66.1 / 10.7 / 1.22e-09 | 2.78 |
| (I,C) | 0.0108 | 35.06 | 7252 | 0.0324 / 0.0325 / 0.00373 / 30.8 / 4.22 / 4.11e-10 | 1.4 |
| (CRI,light1/8) | 0.0191 | 6414 | 1.357e+04 | 4.44 / 5.76 / 5.89e+03 / 497 / 20 / 1.57e-07 | 5.87 |
| (N,light1/8) | 0.0194 | 145.1 | 7299 | 4.92 / 5.83 / 20.3 / 96.7 / 17.4 / 1.57e-07 | 4.91 |
| (P38,C) | 0.0107 | 61.92 | 7279 | 0.0237 / 0.0239 / 0.0026 / 59.6 / 2.23 / 2.99e-10 | 1.05 |

N = 10000:
| start | P(first entry in R) | mean time to E | mean time to R | time to E in: shadow excursion / cheater-major / light cheater / committed / mixing / forfeit | visits |
|---|---|---|---|---|---|
| (N,K) | 0.0207 | 259.8 | 1.873e+04 | 6.09 / 7.29 / 2.27 / 226 / 18.4 / 9.51e-09 | 3.91 |
| (I,K) | 0.0145 | 251.4 | 1.884e+04 | 0.0459 / 6.02 / 0.877 / 227 / 17.5 / 1.08e-10 | 2.78 |
| (I,C) | 0.0108 | 36.46 | 1.869e+04 | 0.0275 / 0.0283 / 0.012 / 32.1 / 4.33 / 3.57e-11 | 1.39 |
| (CRI,light1/8) | 0.0270 | 5.262e+04 | 7.097e+04 | 2.43 / 5.52 / 3.18e+04 / 2.04e+04 / 485 / 9.01e-09 | 5.94 |
| (N,light1/8) | 0.0236 | 450.5 | 1.886e+04 | 4.92 / 5.83 / 22 / 389 / 28.4 / 1.57e-08 | 4.91 |
| (P38,C) | 0.0107 | 62.94 | 1.872e+04 | 0.0212 / 0.0217 / 0.00921 / 60.6 / 2.3 / 2.72e-11 | 1.04 |

N = 100000:
| start | P(first entry in R) | mean time to E | mean time to R | time to E in: shadow excursion / cheater-major / light cheater / committed / mixing / forfeit | visits |
|---|---|---|---|---|---|
| (N,K) | 0.0223 | 652.4 | 4.245e+04 | 6.09 / 7.29 / 5.2 / 594 / 39.9 / 9.52e-10 | 3.91 |
| (I,K) | 0.0162 | 644.2 | 4.271e+04 | 0.0456 / 6.02 / 1.88 / 598 / 37.8 / 1.07e-11 | 2.78 |
| (I,C) | 0.0108 | 39.76 | 4.234e+04 | 0.027 / 0.0279 / 0.0263 / 35.2 / 4.49 / 3.52e-12 | 1.39 |
| (CRI,light1/8) | 0.0531 | 2.647e+05 | 3.052e+05 | 0.782 / 5.6 / 5.62e+04 / 2.01e+05 / 7.16e+03 / 2.85e-10 | 6.7 |
| (N,light1/8) | 0.0267 | 1140 | 4.276e+04 | 4.91 / 5.83 / 24.9 / 1.05e+03 / 58.5 / 1.57e-09 | 4.91 |
| (P38,C) | 0.0108 | 65.46 | 4.236e+04 | 0.0209 / 0.0215 / 0.0205 / 63 / 2.42 / 2.69e-12 | 1.04 |

Top contributors to the flux out of R at N = 10000: inspectee `coin(C,coin(C,X))` (strict) 36.0%; inspectee `coin(C,X)` (strict) 14.6%; inspectee `cr(THEM(ME))` (strict) 10.2%; inspector `N` (neutral) 9.4%; inspectee `cr(coin(N,THEM(ME)))` (strict) 8.4%; inspectee `coin(C,coin(C,coin(K,X)))` (strict) 5.6%; inspectee `coin(C,coin(K,X))` (strict) 3.0%; inspectee `cr(THEM(^C))` (strict) 2.8%.
Top contributors to the flux out of E at N = 10000: inspectee `K` (strict) 61.8%; inspectee `X` (strict) 28.9%; inspectee `coin(K,X)` (strict) 3.2%; inspectee `coin(C,X)` (strict) 1.8%; inspectee `coin(C,coin(C,X))` (strict) 1.0%; inspectee `cr(THEM(ME))` (strict) 0.5%; inspectee `coin(K,coin(C,X))` (strict) 0.5%; inspectee `coin(C,coin(K,X))` (strict) 0.4%.
Top states at N = 10000: (cr(THEM(ME)), coin(C,coin(C,X))) 0.102; (coin(N,coin(I,X)), cr(THEM(ME))) 0.098; (coin(I,coin(N,X)), cr(coin(N,THEM(ME)))) 0.086; (coin(N,cr(THEM(ME))), coin(C,coin(C,X))) 0.063; (cr(THEM(ME)), C) 0.060 [R]; (X, cr(THEM(ME))) 0.054; (coin(N,coin(I,X)), cr(THEM(^C))) 0.049; (cr(THEM(ME)), coin(C,coin(C,coin(K,X)))) 0.027.
Support: 231 pair states carry 0.99 of π (of 24649); balance residual 1.2e-06, circulation index 1.000.

Reference one-state hazards at (CRI, C) (notes §1.2): N = 100: neutral 1.55e-03, strict inspectee 7.54e-05; N = 1000: neutral 1.55e-04, strict inspectee 7.40e-05; N = 10000: neutral 1.55e-05, strict inspectee 7.40e-05; N = 100000: neutral 1.55e-06, strict inspectee 7.40e-05.

## Chain, exact arm, c = 0.01 (whole state space, ε → 0)

| N | π(E) | odds E | π(R) | π(R*) | π(E*) | mean inspector payoff | mean inspectee payoff | inspection prob | cheat prob | forfeit mass in E | peak RSS GB | check vs two-role run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.2714 | 0.3725 | 0.0936 | 0.0865 | 0.2714 | -0.7920 | -0.1838 | 0.446 | 0.177 | 2.51e-06 | 2.9 | - |
| 1000 | 0.3292 | 0.4907 | 0.2080 | 0.1871 | 0.3292 | -0.6323 | -0.1205 | 0.383 | 0.123 | 5.28e-06 | 4.1 | -0.632 vs -0.632 |
| 10000 | 0.3307 | 0.4942 | 0.2136 | 0.1890 | 0.3307 | -0.6228 | -0.1157 | 0.378 | 0.120 | 5.35e-06 | 3.7 | -0.623 vs -0.623 |
| 100000 | 0.3237 | 0.4786 | 0.2091 | 0.1849 | 0.3237 | -0.6308 | -0.1132 | 0.376 | 0.123 | 5.24e-06 | 3.5 | - |

Odds of E: least-squares slope of log odds on log N over N ≥ 10³: -0.005.

**Conditional exit hazard from R** (per mutation event; flux / π(R)), by category:

| category | N = 100 | N = 1000 | N = 10000 | N = 100000 | slope (N ≥ 10³) |
|---|---|---|---|---|---|
| A neutral shadow | 1.454e-06 | 1.399e-07 | 1.379e-08 | 1.379e-09 | -1.00 |
| B neutral other | 4.674e-05 | 4.723e-06 | 5.071e-07 | 5.105e-08 | -0.98 |
| C strict K | 0 | 0 | 0 | 0 | n/a |
| D strict non-reading inspectee | 1.312e-04 | 9.993e-05 | 9.919e-05 | 9.928e-05 | -0.00 |
| E strict reading inspectee (clean) | 8.282e-05 | 6.951e-05 | 6.813e-05 | 6.810e-05 | -0.00 |
| E strict reading inspectee (forfeit-driven) | 0 | 0 | 0 | 0 | n/a |
| F strict inspector | 1.737e-03 | 4.564e-04 | 4.267e-04 | 4.267e-04 | -0.01 |
| G deleterious | 4.349e-06 | 8.838e-09 | 9.536e-13 | 2.218e-16 | -3.80 |
| **total** | 2.004e-03 | 6.307e-04 | 5.945e-04 | 5.941e-04 | -0.01 |
| largest | F | F | F | F | |

**Conditional exit hazard from E** (per mutation event; flux / π(E)), by category:

| category | N = 100 | N = 1000 | N = 10000 | N = 100000 | slope (N ≥ 10³) |
|---|---|---|---|---|---|
| A neutral shadow | 0 | 0 | 0 | 0 | n/a |
| B neutral other | 1.687e-05 | 3.145e-06 | 3.508e-07 | 3.540e-08 | -0.97 |
| C strict K | 2.520e-02 | 1.414e-02 | 1.360e-02 | 1.359e-02 | -0.01 |
| D strict non-reading inspectee | 1.437e-02 | 8.100e-03 | 7.791e-03 | 7.787e-03 | -0.01 |
| E strict reading inspectee (clean) | 4.016e-04 | 2.533e-04 | 2.453e-04 | 2.452e-04 | -0.01 |
| E strict reading inspectee (forfeit-driven) | 0 | 0 | 0 | 0 | n/a |
| F strict inspector | 1.079e-09 | 4.282e-10 | 4.112e-10 | 4.109e-10 | -0.01 |
| G deleterious | 2.485e-06 | 2.385e-09 | 6.038e-13 | 1.693e-16 | -3.57 |
| **total** | 3.998e-02 | 2.250e-02 | 2.163e-02 | 2.162e-02 | -0.01 |
| largest | C | C | C | C | |

Strict inspectee flux out of E by the resident inspector (deterring / not deterring K): N = 100: 2.00e-05 / 1.08e-02; N = 1000: 3.52e-05 / 7.37e-03; N = 10000: 3.57e-05 / 7.12e-03; N = 100000: 3.50e-05 / 6.96e-03.

**Renewal identities** (exact; mutation events): mean sojourn in R, mean time outside R, mean sojourn in E, mean time outside E:

| N | sojourn R | outside R | sojourn E | outside E |
|---|---|---|---|---|
| 100 | 499 | 4833 | 25.01 | 67.15 |
| 1000 | 1586 | 6038 | 44.45 | 90.58 |
| 10000 | 1682 | 6193 | 46.23 | 93.54 |
| 100000 | 1683 | 6367 | 46.25 | 96.63 |

**Where π sits outside E** (occupancy of the detour categories; exclusive, in this order): 

| N | E | forfeit | shadow_excursion | cheater_major_other | light_cheater | committed_compliant | mixing | other |
|---|---|---|---|---|---|---|---|---|
| 100 | 0.2714 | 0.0000 | 0.0522 | 0.0618 | 0.0087 | 0.4319 | 0.1739 | 0.0000 |
| 1000 | 0.3292 | 0.0000 | 0.0353 | 0.0419 | 0.0282 | 0.4389 | 0.1264 | 0.0000 |
| 10000 | 0.3307 | 0.0000 | 0.0341 | 0.0405 | 0.0309 | 0.4385 | 0.1253 | 0.0000 |
| 100000 | 0.3237 | 0.0000 | 0.0333 | 0.0396 | 0.0303 | 0.4290 | 0.1441 | 0.0000 |

**First passage into E and into R** from the named states (exact, same elimination pass; mutation events; P(R) = probability that the first E state entered is in R):

N = 100:
| start | P(first entry in R) | mean time to E | mean time to R | time to E in: shadow excursion / cheater-major / light cheater / committed / mixing / forfeit | visits |
|---|---|---|---|---|---|
| (N,K) | 0.0170 | 59.81 | 4802 | 6.14 / 7.33 / 0.166 / 36.4 / 9.75 / 9.39e-08 | 3.95 |
| (I,K) | 0.0110 | 50.2 | 4821 | 0.0976 / 6.06 / 0.13 / 34.8 / 9.15 / 2.7e-09 | 2.82 |
| (I,C) | 0.0107 | 34.55 | 4807 | 0.0711 / 0.0658 / 0.00495 / 30.7 / 3.66 / 8.26e-10 | 1.43 |
| (CRI,light1/8) | 0.1031 | 583.7 | 4910 | 4.46 / 5.31 / 520 / 38.6 / 15.1 / 1.41e-07 | 5.5 |
| (N,light1/8) | 0.0169 | 85.41 | 4828 | 4.94 / 5.85 / 19.9 / 39.5 / 15.3 / 1.52e-07 | 4.94 |
| (P38,C) | 0.0105 | 61.58 | 4835 | 0.0455 / 0.0431 / 0.00955 / 59.4 / 2.09 / 5.59e-10 | 1.08 |

N = 1000:
| start | P(first entry in R) | mean time to E | mean time to R | time to E in: shadow excursion / cheater-major / light cheater / committed / mixing / forfeit | visits |
|---|---|---|---|---|---|
| (N,K) | 0.0174 | 69.68 | 5653 | 6.1 / 7.29 / 0.24 / 45.6 / 10.5 / 3.56e-13 | 3.91 |
| (I,K) | 0.0113 | 60.23 | 5678 | 0.0513 / 6.02 / 0.133 / 44.2 / 9.84 / 2.66e-14 | 2.78 |
| (I,C) | 0.0106 | 34.63 | 5656 | 0.0323 / 0.0324 / 0.00185 / 30.4 / 4.2 / 7.19e-15 | 1.4 |
| (CRI,light1/8) | 0.0176 | 2147 | 7729 | 4.78 / 5.81 / 2.03e+03 / 94.9 / 16.1 / 2.68e-12 | 5.89 |
| (N,light1/8) | 0.0177 | 103.2 | 5684 | 4.92 / 5.83 / 19.9 / 56.5 / 16.1 / 1.44e-12 | 4.91 |
| (P38,C) | 0.0105 | 61.43 | 5684 | 0.0236 / 0.0239 / 0.00127 / 59.2 / 2.21 / 5.49e-15 | 1.05 |

N = 10000:
| start | P(first entry in R) | mean time to E | mean time to R | time to E in: shadow excursion / cheater-major / light cheater / committed / mixing / forfeit | visits |
|---|---|---|---|---|---|
| (N,K) | 0.0174 | 70.84 | 5745 | 6.09 / 7.29 / 0.246 / 46.6 / 10.6 / 6.82e-15 | 3.91 |
| (I,K) | 0.0113 | 61.38 | 5771 | 0.0456 / 6.02 / 0.134 / 45.2 / 9.98 / 4.98e-16 | 2.78 |
| (I,C) | 0.0106 | 34.64 | 5748 | 0.0275 / 0.0283 / 0.0013 / 30.3 / 4.27 / 1.31e-16 | 1.39 |
| (CRI,light1/8) | 0.0176 | 2257 | 7930 | 4.77 / 5.8 / 2.13e+03 / 101 / 16.3 / 2.94e-14 | 5.89 |
| (N,light1/8) | 0.0178 | 105.1 | 5777 | 4.91 / 5.83 / 19.9 / 58.1 / 16.3 / 2.77e-14 | 4.91 |
| (P38,C) | 0.0105 | 61.41 | 5776 | 0.0212 / 0.0217 / 0.000993 / 59.1 / 2.25 / 1.02e-16 | 1.04 |

N = 100000:
| start | P(first entry in R) | mean time to E | mean time to R | time to E in: shadow excursion / cheater-major / light cheater / committed / mixing / forfeit | visits |
|---|---|---|---|---|---|
| (N,K) | 0.0174 | 71.63 | 5802 | 6.09 / 7.29 / 0.245 / 46.6 / 11.4 / 2.29e-26 | 3.91 |
| (I,K) | 0.0113 | 61.97 | 5828 | 0.045 / 6.02 / 0.133 / 45.2 / 10.6 / 1.67e-27 | 2.77 |
| (I,C) | 0.0106 | 34.64 | 5805 | 0.027 / 0.0279 / 0.00123 / 30.3 / 4.28 / 4.4e-28 | 1.39 |
| (CRI,light1/8) | 0.0176 | 2258 | 7988 | 4.77 / 5.8 / 2.13e+03 / 101 / 17.2 / 9.1e-26 | 5.89 |
| (N,light1/8) | 0.0178 | 106 | 5835 | 4.91 / 5.83 / 19.9 / 58.1 / 17.2 / 9.29e-26 | 4.91 |
| (P38,C) | 0.0105 | 61.42 | 5832 | 0.0209 / 0.0215 / 0.00096 / 59.1 / 2.25 / 3.42e-28 | 1.04 |

Top contributors to the flux out of R at N = 10000: inspector `N` (strict) 71.8%; inspectee `coin(C,coin(C,X))` (strict) 7.4%; inspectee `coin(C,X)` (strict) 6.2%; inspectee `cr(THEM(ME))` (strict) 5.6%; inspectee `cr(coin(N,THEM(ME)))` (strict) 1.6%; inspectee `cr(THEM(^C))` (strict) 1.6%; inspectee `coin(C,coin(K,X))` (strict) 1.2%; inspectee `coin(C,coin(C,coin(K,X)))` (strict) 1.2%.
Top contributors to the flux out of E at N = 10000: inspectee `K` (strict) 62.9%; inspectee `X` (strict) 29.5%; inspectee `coin(K,X)` (strict) 3.3%; inspectee `coin(C,X)` (strict) 1.6%; inspectee `coin(K,coin(C,X))` (strict) 0.5%; inspectee `cr(THEM(ME))` (strict) 0.4%; inspectee `coin(C,coin(K,X))` (strict) 0.4%; inspectee `coin(K,coin(K,X))` (strict) 0.3%.
Top states at N = 10000: (X, C) 0.122; (N, C) 0.117 [E]; (cr(THEM(ME)), C) 0.104 [R]; (I, C) 0.093; (X, cr(THEM(ME))) 0.080; (I, X) 0.037; (N, K) 0.030; (coin(N,X), C) 0.027.
Support: 249 pair states carry 0.99 of π (of 27889); balance residual 1.4e-06, circulation index 1.000.

Reference one-state hazards at (CRI, C) (notes §1.2): N = 100: neutral 1.04e-05, strict inspectee 7.33e-05; N = 1000: neutral 1.04e-06, strict inspectee 7.19e-05; N = 10000: neutral 1.04e-07, strict inspectee 7.19e-05; N = 100000: neutral 1.04e-08, strict inspectee 7.19e-05.

## Lottery size path (exact arm; ε = 0 seed lottery; mN = 1; horizon 20N)

**exact_c0_n100i64** (40 runs; N = 100, I = 64, horizon 2000, mN = 1): horizon value [95% CI]; value at generation 2,000; mean over the last N generations

| statistic | horizon | gen 2,000 | last-N window |
|---|---|---|---|
| efficient islands E | 0.648 [0.500, 0.792] | 0.648 [0.500, 0.792] | 0.651 |
| E* islands | 0.648 [0.500, 0.792] | 0.648 [0.500, 0.792] | 0.651 |
| efficient, responsive inspectors | 0.637 [0.492, 0.779] | 0.637 [0.492, 0.779] | 0.639 |
| efficient, shadow | 0.010 [0.000, 0.023] | 0.010 [0.000, 0.023] | 0.012 |
| committed and compliant | 0.109 [0.027, 0.205] | 0.109 [0.027, 0.205] | 0.107 |
| light-cheater islands | 0.185 [0.075, 0.310] | 0.185 [0.075, 0.310] | 0.186 |
| cheater-majority | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| inspector payoff | -0.223 [-0.334, -0.122] | -0.223 [-0.334, -0.122] | -0.222 |
| inspectee payoff | 0.037 [0.014, 0.062] | 0.037 [0.014, 0.062] | 0.037 |
| inspection prob | 0.067 [0.023, 0.119] | 0.067 [0.023, 0.119] | 0.066 |
| cheat prob | 0.040 [0.016, 0.067] | 0.040 [0.016, 0.067] | 0.040 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| share cr(THEM(ME)) class | 0.474 [0.326, 0.618] | 0.474 [0.326, 0.618] | 0.474 |
| share N | 0.027 [0.005, 0.055] | 0.027 [0.005, 0.055] | 0.029 |
| share K | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| share C | 0.606 [0.486, 0.731] | 0.606 [0.486, 0.731] | 0.609 |
| reading inspectees | 0.193 [0.110, 0.282] | 0.193 [0.110, 0.282] | 0.191 |
| prudent-class mass | 0.103 [0.041, 0.180] | 0.103 [0.041, 0.180] | 0.102 |
| responsive inspector mass | 0.850 [0.748, 0.939] | 0.850 [0.748, 0.939] | 0.849 |

Ladder labels at the horizon (R reader+committed, C constants+committed, N lax+compliant, K lax+cheating, IK committed+cheating): C 0.035, N 0.657, R 0.072, other 0.236; island label switches per island over the last N generations: 0.025.

Efficient islands at common t: t=100: 0.193, t=500: 0.602, t=1000: 0.636, t=2000: 0.648; at t/N: 1: 0.193, 2: 0.423, 5: 0.602, 10: 0.636, 20: 0.648.

**exact_c0_n400i16** (20 runs; N = 400, I = 16, horizon 8000, mN = 1): horizon value [95% CI]; value at generation 2,000; mean over the last N generations

| statistic | horizon | gen 2,000 | last-N window |
|---|---|---|---|
| efficient islands E | 0.400 [0.200, 0.600] | 0.406 [0.206, 0.606] | 0.400 |
| E* islands | 0.400 [0.200, 0.600] | 0.406 [0.206, 0.606] | 0.400 |
| efficient, responsive inspectors | 0.353 [0.153, 0.553] | 0.394 [0.200, 0.594] | 0.353 |
| efficient, shadow | 0.047 [0.000, 0.141] | 0.013 [0.000, 0.037] | 0.047 |
| committed and compliant | 0.500 [0.300, 0.700] | 0.497 [0.297, 0.700] | 0.500 |
| light-cheater islands | 0.100 [0.000, 0.250] | 0.062 [0.000, 0.175] | 0.100 |
| cheater-majority | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| inspector payoff | -0.325 [-0.450, -0.201] | -0.310 [-0.424, -0.198] | -0.325 |
| inspectee payoff | 0.022 [-0.000, 0.056] | 0.013 [-0.000, 0.036] | 0.022 |
| inspection prob | 0.237 [0.138, 0.344] | 0.241 [0.141, 0.342] | 0.237 |
| cheat prob | 0.022 [0.000, 0.056] | 0.019 [0.000, 0.046] | 0.022 |
| forfeit (inspector) | 0.000 [0.000, 0.001] | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.001 [0.000, 0.002] | 0.000 [0.000, 0.001] | 0.001 |
| share cr(THEM(ME)) class | 0.355 [0.155, 0.555] | 0.394 [0.200, 0.600] | 0.355 |
| share N | 0.095 [0.000, 0.240] | 0.046 [0.000, 0.123] | 0.095 |
| share K | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| share C | 0.498 [0.306, 0.689] | 0.542 [0.397, 0.682] | 0.485 |
| reading inspectees | 0.402 [0.226, 0.593] | 0.371 [0.231, 0.516] | 0.415 |
| prudent-class mass | 0.044 [0.000, 0.113] | 0.061 [0.011, 0.123] | 0.053 |
| responsive inspector mass | 0.405 [0.200, 0.605] | 0.460 [0.256, 0.660] | 0.405 |

Ladder labels at the horizon (R reader+committed, C constants+committed, N lax+compliant, K lax+cheating, IK committed+cheating): C 0.166, N 0.400, R 0.334, other 0.100; island label switches per island over the last N generations: 0.020.

Efficient islands at common t: t=100: 0.163, t=500: 0.381, t=1000: 0.416, t=2000: 0.406, t=4000: 0.400, t=8000: 0.400; at t/N: 1: 0.375, 2: 0.412, 5: 0.406, 10: 0.400, 20: 0.400.

**exact_c0_n800i8** (20 runs; N = 800, I = 8, horizon 16000, mN = 1): horizon value [95% CI]; value at generation 2,000; mean over the last N generations

| statistic | horizon | gen 2,000 | last-N window |
|---|---|---|---|
| efficient islands E | 0.800 [0.600, 0.950] | 0.744 [0.544, 0.912] | 0.800 |
| E* islands | 0.800 [0.600, 0.950] | 0.744 [0.544, 0.912] | 0.800 |
| efficient, responsive inspectors | 0.750 [0.550, 0.950] | 0.725 [0.525, 0.894] | 0.750 |
| efficient, shadow | 0.050 [0.000, 0.150] | 0.019 [0.000, 0.056] | 0.050 |
| committed and compliant | 0.100 [0.000, 0.250] | 0.119 [0.000, 0.269] | 0.100 |
| light-cheater islands | 0.100 [0.000, 0.250] | 0.081 [0.000, 0.212] | 0.100 |
| cheater-majority | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| inspector payoff | -0.132 [-0.275, -0.020] | -0.157 [-0.294, -0.047] | -0.132 |
| inspectee payoff | 0.022 [-0.000, 0.056] | 0.018 [-0.001, 0.047] | 0.022 |
| inspection prob | 0.044 [0.000, 0.113] | 0.061 [0.008, 0.131] | 0.044 |
| cheat prob | 0.022 [0.000, 0.056] | 0.026 [0.002, 0.058] | 0.022 |
| forfeit (inspector) | 0.000 [0.000, 0.001] | 0.000 [0.000, 0.001] | 0.000 |
| forfeit (inspectee) | 0.001 [0.000, 0.002] | 0.001 [0.000, 0.001] | 0.001 |
| share cr(THEM(ME)) class | 0.400 [0.200, 0.600] | 0.404 [0.222, 0.587] | 0.400 |
| share N | 0.050 [0.000, 0.150] | 0.031 [0.000, 0.076] | 0.050 |
| share K | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| share C | 0.773 [0.573, 0.923] | 0.708 [0.541, 0.854] | 0.771 |
| reading inspectees | 0.127 [0.000, 0.277] | 0.177 [0.062, 0.311] | 0.129 |
| prudent-class mass | 0.027 [0.000, 0.081] | 0.080 [0.023, 0.147] | 0.029 |
| responsive inspector mass | 0.850 [0.700, 1.000] | 0.850 [0.693, 0.974] | 0.850 |

Ladder labels at the horizon (R reader+committed, C constants+committed, N lax+compliant, K lax+cheating, IK committed+cheating): C 0.050, N 0.800, R 0.050, other 0.100; island label switches per island over the last N generations: 0.000.

Efficient islands at common t: t=100: 0.231, t=500: 0.637, t=1000: 0.669, t=2000: 0.744, t=4000: 0.775, t=8000: 0.800, t=16000: 0.800; at t/N: 1: 0.675, 2: 0.719, 5: 0.775, 10: 0.800, 20: 0.800.

**exact_c0_n400i64** (20 runs; N = 400, I = 64, horizon 8000, mN = 1): horizon value [95% CI]; value at generation 2,000; mean over the last N generations

| statistic | horizon | gen 2,000 | last-N window |
|---|---|---|---|
| efficient islands E | 0.672 [0.472, 0.850] | 0.656 [0.456, 0.844] | 0.674 |
| E* islands | 0.672 [0.472, 0.850] | 0.656 [0.456, 0.844] | 0.674 |
| efficient, responsive inspectors | 0.672 [0.472, 0.850] | 0.656 [0.456, 0.844] | 0.674 |
| efficient, shadow | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| committed and compliant | 0.005 [0.000, 0.016] | 0.033 [0.004, 0.080] | 0.005 |
| light-cheater islands | 0.290 [0.100, 0.488] | 0.270 [0.091, 0.452] | 0.288 |
| cheater-majority | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| inspector payoff | -0.197 [-0.336, -0.075] | -0.201 [-0.340, -0.078] | -0.197 |
| inspectee payoff | 0.046 [0.015, 0.081] | 0.043 [0.014, 0.074] | 0.046 |
| inspection prob | 0.006 [0.000, 0.014] | 0.018 [0.004, 0.039] | 0.006 |
| cheat prob | 0.049 [0.019, 0.083] | 0.046 [0.016, 0.080] | 0.049 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.001] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.000] | 0.001 [0.000, 0.001] | 0.000 |
| share cr(THEM(ME)) class | 0.640 [0.456, 0.815] | 0.620 [0.461, 0.773] | 0.640 |
| share N | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| share K | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| share C | 0.550 [0.376, 0.715] | 0.492 [0.349, 0.628] | 0.550 |
| reading inspectees | 0.145 [0.071, 0.243] | 0.214 [0.154, 0.273] | 0.144 |
| prudent-class mass | 0.126 [0.047, 0.229] | 0.133 [0.074, 0.198] | 0.124 |
| responsive inspector mass | 0.994 [0.984, 1.000] | 0.968 [0.926, 0.996] | 0.994 |

Ladder labels at the horizon (R reader+committed, C constants+committed, N lax+compliant, K lax+cheating, IK committed+cheating): N 0.689, R 0.005, other 0.305; island label switches per island over the last N generations: 0.003.

Efficient islands at common t: t=100: 0.248, t=500: 0.630, t=1000: 0.643, t=2000: 0.656, t=4000: 0.680, t=8000: 0.672; at t/N: 1: 0.634, 2: 0.629, 5: 0.656, 10: 0.680, 20: 0.672.

**exact_c0.01_n100i64** (40 runs; N = 100, I = 64, horizon 2000, mN = 1): horizon value [95% CI]; value at generation 2,000; mean over the last N generations

| statistic | horizon | gen 2,000 | last-N window |
|---|---|---|---|
| efficient islands E | 0.701 [0.552, 0.827] | 0.701 [0.552, 0.827] | 0.701 |
| E* islands | 0.701 [0.552, 0.827] | 0.701 [0.552, 0.827] | 0.701 |
| efficient, responsive inspectors | 0.637 [0.493, 0.776] | 0.637 [0.493, 0.776] | 0.641 |
| efficient, shadow | 0.064 [0.014, 0.129] | 0.064 [0.014, 0.129] | 0.059 |
| committed and compliant | 0.025 [0.000, 0.075] | 0.025 [0.000, 0.075] | 0.025 |
| light-cheater islands | 0.186 [0.080, 0.311] | 0.186 [0.080, 0.311] | 0.185 |
| cheater-majority | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| inspector payoff | -0.207 [-0.320, -0.106] | -0.207 [-0.320, -0.106] | -0.207 |
| inspectee payoff | 0.037 [0.016, 0.062] | 0.037 [0.016, 0.062] | 0.037 |
| inspection prob | 0.029 [0.007, 0.057] | 0.029 [0.007, 0.057] | 0.029 |
| cheat prob | 0.047 [0.022, 0.076] | 0.047 [0.022, 0.076] | 0.047 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| share cr(THEM(ME)) class | 0.357 [0.234, 0.484] | 0.357 [0.234, 0.484] | 0.362 |
| share N | 0.132 [0.052, 0.222] | 0.132 [0.052, 0.222] | 0.126 |
| share K | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| share C | 0.765 [0.629, 0.885] | 0.765 [0.629, 0.885] | 0.765 |
| reading inspectees | 0.005 [0.000, 0.012] | 0.005 [0.000, 0.012] | 0.005 |
| prudent-class mass | 0.001 [0.000, 0.003] | 0.001 [0.000, 0.003] | 0.001 |
| responsive inspector mass | 0.793 [0.679, 0.900] | 0.793 [0.679, 0.900] | 0.799 |

Ladder labels at the horizon (R reader+committed, C constants+committed, N lax+compliant, K lax+cheating, IK committed+cheating): C 0.022, N 0.703, R 0.003, other 0.272; island label switches per island over the last N generations: 0.002.

Efficient islands at common t: t=100: 0.237, t=500: 0.656, t=1000: 0.718, t=2000: 0.701; at t/N: 1: 0.237, 2: 0.516, 5: 0.656, 10: 0.718, 20: 0.701.

**exact_c0.01_n400i16** (20 runs; N = 400, I = 16, horizon 8000, mN = 1): horizon value [95% CI]; value at generation 2,000; mean over the last N generations

| statistic | horizon | gen 2,000 | last-N window |
|---|---|---|---|
| efficient islands E | 0.550 [0.350, 0.750] | 0.550 [0.350, 0.750] | 0.550 |
| E* islands | 0.550 [0.350, 0.750] | 0.550 [0.350, 0.750] | 0.550 |
| efficient, responsive inspectors | 0.500 [0.300, 0.700] | 0.506 [0.300, 0.713] | 0.500 |
| efficient, shadow | 0.050 [0.000, 0.150] | 0.044 [0.000, 0.131] | 0.050 |
| committed and compliant | 0.303 [0.103, 0.503] | 0.303 [0.103, 0.503] | 0.303 |
| light-cheater islands | 0.097 [0.000, 0.244] | 0.100 [0.000, 0.247] | 0.093 |
| cheater-majority | 0.050 [0.000, 0.150] | 0.047 [0.000, 0.141] | 0.050 |
| inspector payoff | -0.387 [-0.826, -0.118] | -0.376 [-0.794, -0.118] | -0.387 |
| inspectee payoff | 0.065 [0.000, 0.176] | 0.062 [0.000, 0.167] | 0.065 |
| inspection prob | 0.127 [0.044, 0.216] | 0.127 [0.044, 0.216] | 0.127 |
| cheat prob | 0.065 [0.000, 0.176] | 0.062 [0.000, 0.168] | 0.065 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| share cr(THEM(ME)) class | 0.397 [0.197, 0.600] | 0.411 [0.214, 0.618] | 0.397 |
| share N | 0.100 [0.000, 0.250] | 0.091 [0.000, 0.232] | 0.100 |
| share K | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| share C | 0.850 [0.700, 1.000] | 0.810 [0.644, 0.945] | 0.850 |
| reading inspectees | 0.053 [0.000, 0.156] | 0.093 [0.014, 0.204] | 0.053 |
| prudent-class mass | 0.000 [0.000, 0.000] | 0.002 [0.000, 0.006] | 0.000 |
| responsive inspector mass | 0.597 [0.397, 0.797] | 0.606 [0.401, 0.805] | 0.597 |

Ladder labels at the horizon (R reader+committed, C constants+committed, N lax+compliant, K lax+cheating, IK committed+cheating): C 0.300, K 0.050, N 0.550, R 0.003, other 0.097; island label switches per island over the last N generations: 0.000.

Efficient islands at common t: t=100: 0.197, t=500: 0.487, t=1000: 0.556, t=2000: 0.550, t=4000: 0.550, t=8000: 0.550; at t/N: 1: 0.497, 2: 0.519, 5: 0.550, 10: 0.550, 20: 0.550.

**exact_c0.01_n800i8** (20 runs; N = 800, I = 8, horizon 16000, mN = 1): horizon value [95% CI]; value at generation 2,000; mean over the last N generations

| statistic | horizon | gen 2,000 | last-N window |
|---|---|---|---|
| efficient islands E | 0.700 [0.500, 0.900] | 0.688 [0.475, 0.875] | 0.700 |
| E* islands | 0.700 [0.500, 0.900] | 0.688 [0.475, 0.875] | 0.700 |
| efficient, responsive inspectors | 0.600 [0.400, 0.800] | 0.625 [0.412, 0.812] | 0.600 |
| efficient, shadow | 0.100 [0.000, 0.250] | 0.062 [0.000, 0.169] | 0.100 |
| committed and compliant | 0.131 [0.000, 0.281] | 0.144 [0.025, 0.294] | 0.131 |
| light-cheater islands | 0.169 [0.037, 0.338] | 0.131 [0.013, 0.281] | 0.166 |
| cheater-majority | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| inspector payoff | -0.194 [-0.350, -0.069] | -0.199 [-0.355, -0.074] | -0.194 |
| inspectee payoff | 0.033 [0.004, 0.071] | 0.028 [0.004, 0.059] | 0.033 |
| inspection prob | 0.059 [0.000, 0.131] | 0.071 [0.016, 0.139] | 0.059 |
| cheat prob | 0.034 [0.005, 0.071] | 0.034 [0.005, 0.071] | 0.034 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| share cr(THEM(ME)) class | 0.169 [0.037, 0.350] | 0.210 [0.069, 0.390] | 0.169 |
| share N | 0.150 [0.000, 0.350] | 0.098 [0.000, 0.216] | 0.150 |
| share K | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| share C | 0.800 [0.600, 0.950] | 0.792 [0.600, 0.949] | 0.800 |
| reading inspectees | 0.031 [0.000, 0.092] | 0.039 [0.000, 0.108] | 0.031 |
| prudent-class mass | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| responsive inspector mass | 0.719 [0.519, 0.900] | 0.765 [0.595, 0.911] | 0.719 |

Ladder labels at the horizon (R reader+committed, C constants+committed, N lax+compliant, K lax+cheating, IK committed+cheating): C 0.100, N 0.700, R 0.031, other 0.169; island label switches per island over the last N generations: 0.000.

Efficient islands at common t: t=100: 0.200, t=500: 0.531, t=1000: 0.619, t=2000: 0.688, t=4000: 0.700, t=8000: 0.700, t=16000: 0.700; at t/N: 1: 0.588, 2: 0.662, 5: 0.700, 10: 0.700, 20: 0.700.

**exact_c0.01_n400i64** (20 runs; N = 400, I = 64, horizon 8000, mN = 1): horizon value [95% CI]; value at generation 2,000; mean over the last N generations

| statistic | horizon | gen 2,000 | last-N window |
|---|---|---|---|
| efficient islands E | 0.602 [0.400, 0.802] | 0.610 [0.400, 0.808] | 0.601 |
| E* islands | 0.602 [0.400, 0.802] | 0.610 [0.400, 0.808] | 0.601 |
| efficient, responsive inspectors | 0.602 [0.400, 0.802] | 0.609 [0.400, 0.808] | 0.601 |
| efficient, shadow | 0.000 [0.000, 0.000] | 0.002 [0.000, 0.005] | 0.000 |
| committed and compliant | 0.008 [0.000, 0.022] | 0.009 [0.000, 0.026] | 0.008 |
| light-cheater islands | 0.352 [0.160, 0.562] | 0.335 [0.151, 0.536] | 0.358 |
| cheater-majority | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| inspector payoff | -0.233 [-0.383, -0.101] | -0.220 [-0.353, -0.100] | -0.235 |
| inspectee payoff | 0.053 [0.023, 0.087] | 0.049 [0.022, 0.078] | 0.053 |
| inspection prob | 0.008 [0.000, 0.020] | 0.010 [0.001, 0.020] | 0.008 |
| cheat prob | 0.057 [0.025, 0.095] | 0.054 [0.024, 0.087] | 0.058 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| share cr(THEM(ME)) class | 0.529 [0.343, 0.708] | 0.587 [0.423, 0.743] | 0.532 |
| share N | 0.050 [0.000, 0.150] | 0.039 [0.000, 0.116] | 0.050 |
| share K | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 |
| share C | 0.605 [0.400, 0.805] | 0.618 [0.406, 0.813] | 0.603 |
| reading inspectees | 0.007 [0.000, 0.020] | 0.009 [0.000, 0.025] | 0.008 |
| prudent-class mass | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.001] | 0.000 |
| responsive inspector mass | 0.942 [0.836, 1.000] | 0.952 [0.868, 1.000] | 0.942 |

Ladder labels at the horizon (R reader+committed, C constants+committed, N lax+compliant, K lax+cheating, IK committed+cheating): C 0.001, N 0.655, R 0.007, other 0.338; island label switches per island over the last N generations: 0.001.

Efficient islands at common t: t=100: 0.253, t=500: 0.666, t=1000: 0.660, t=2000: 0.610, t=4000: 0.612, t=8000: 0.602; at t/N: 1: 0.678, 2: 0.674, 5: 0.610, 10: 0.612, 20: 0.602.

**Efficient islands along the path** (path effects: N, I and the horizon move together; (400, 64) crosses (400, 16) and (100, 64) at fixed I or N):

| c | cell | efficient at horizon | efficient at gen 2,000 | forfeit inspector / inspectee at horizon |
|---|---|---|---|---|
| 0 | n100i64 | 0.648 [0.500, 0.792] | 0.648 [0.500, 0.792] | 0.000 / 0.000 |
| 0 | n400i16 | 0.400 [0.200, 0.600] | 0.406 [0.206, 0.606] | 0.000 / 0.001 |
| 0 | n800i8 | 0.800 [0.600, 0.950] | 0.744 [0.544, 0.912] | 0.000 / 0.001 |
| 0 | n400i64 | 0.672 [0.472, 0.850] | 0.656 [0.456, 0.844] | 0.000 / 0.000 |
| 0.01 | n100i64 | 0.701 [0.552, 0.827] | 0.701 [0.552, 0.827] | 0.000 / 0.000 |
| 0.01 | n400i16 | 0.550 [0.350, 0.750] | 0.550 [0.350, 0.750] | 0.000 / 0.000 |
| 0.01 | n800i8 | 0.700 [0.500, 0.900] | 0.688 [0.475, 0.875] | 0.000 / 0.000 |
| 0.01 | n400i64 | 0.602 [0.400, 0.802] | 0.610 [0.400, 0.808] | 0.000 / 0.000 |

## Remedies (lottery cells; rain is ε N = 0.05 mutants per generation per island into the inspectee seat)

**c = 0, n400i16**: efficient islands E and related statistics at the horizon 8000

| cell | E | E* | efficient+responsive | efficient+shadow | committed+compliant | light-cheater | inspector payoff | cheat prob | prudent mass |
|---|---|---|---|---|---|---|---|---|---|
| base | 0.400 [0.200, 0.600] | 0.400 [0.200, 0.600] | 0.353 [0.153, 0.553] | 0.047 [0.000, 0.141] | 0.500 [0.300, 0.700] | 0.100 [0.000, 0.250] | -0.325 [-0.450, -0.201] | 0.022 [0.000, 0.056] | 0.044 [0.000, 0.113] |
| rainK | 0.500 [0.300, 0.700] | 0.500 [0.300, 0.700] | 0.500 [0.300, 0.700] | 0.000 [0.000, 0.000] | 0.394 [0.194, 0.600] | 0.100 [0.000, 0.250] | -0.279 [-0.423, -0.144] | 0.019 [0.000, 0.050] | 0.069 [0.000, 0.174] |
| rainC | 0.550 [0.350, 0.750] | 0.550 [0.350, 0.750] | 0.550 [0.350, 0.750] | 0.000 [0.000, 0.000] | 0.303 [0.106, 0.503] | 0.091 [0.000, 0.231] | -0.262 [-0.412, -0.131] | 0.030 [0.000, 0.067] | 0.023 [0.000, 0.070] |
| boost | 0.700 [0.500, 0.900] | 0.700 [0.500, 0.900] | 0.700 [0.500, 0.900] | 0.000 [0.000, 0.000] | 0.300 [0.100, 0.500] | 0.000 [0.000, 0.000] | -0.128 [-0.222, -0.044] | 0.000 [0.000, 0.000] | 0.239 [0.074, 0.425] |
| boostctl | 0.428 [0.228, 0.650] | 0.428 [0.228, 0.650] | 0.381 [0.181, 0.584] | 0.047 [0.000, 0.141] | 0.416 [0.212, 0.625] | 0.141 [0.000, 0.300] | -0.296 [-0.425, -0.177] | 0.019 [0.001, 0.039] | 0.210 [0.050, 0.400] |
- K rain minus matched C rain: efficient islands -0.050 [-0.200, 0.100] (gen 2,000: -0.025 [-0.178, 0.109]); efficient+responsive -0.050 [-0.200, 0.100].
- prudent x10 minus matched C control: efficient islands 0.272 [-0.028, 0.550] (gen 2,000: 0.297 [0.000, 0.550]); efficient+responsive 0.319 [0.019, 0.600].
- K rain minus base: efficient islands 0.100 [-0.250, 0.450] (gen 2,000: 0.078 [-0.266, 0.416]); efficient+responsive 0.147 [-0.203, 0.500].
- C rain minus base: efficient islands 0.150 [-0.200, 0.500] (gen 2,000: 0.103 [-0.231, 0.425]); efficient+responsive 0.197 [-0.153, 0.544].

**c = 0, n100i64**: efficient islands E and related statistics at the horizon 2000

| cell | E | E* | efficient+responsive | efficient+shadow | committed+compliant | light-cheater | inspector payoff | cheat prob | prudent mass |
|---|---|---|---|---|---|---|---|---|---|
| base | 0.648 [0.500, 0.792] | 0.648 [0.500, 0.792] | 0.637 [0.492, 0.779] | 0.010 [0.000, 0.023] | 0.109 [0.027, 0.205] | 0.185 [0.075, 0.310] | -0.223 [-0.334, -0.122] | 0.040 [0.016, 0.067] | 0.103 [0.041, 0.180] |
| rainK | 0.642 [0.491, 0.784] | 0.642 [0.491, 0.784] | 0.641 [0.491, 0.784] | 0.000 [0.000, 0.001] | 0.181 [0.079, 0.296] | 0.079 [0.009, 0.172] | -0.214 [-0.322, -0.118] | 0.034 [0.012, 0.061] | 0.077 [0.034, 0.125] |
| rainC | 0.629 [0.484, 0.764] | 0.629 [0.484, 0.764] | 0.621 [0.478, 0.755] | 0.008 [0.000, 0.021] | 0.135 [0.050, 0.238] | 0.105 [0.028, 0.202] | -0.251 [-0.366, -0.145] | 0.046 [0.020, 0.076] | 0.041 [0.009, 0.083] |
| boost | 0.751 [0.625, 0.876] | 0.751 [0.625, 0.876] | 0.751 [0.625, 0.876] | 0.000 [0.000, 0.000] | 0.070 [0.000, 0.153] | 0.175 [0.075, 0.300] | -0.155 [-0.253, -0.069] | 0.031 [0.009, 0.056] | 0.329 [0.249, 0.415] |
| boostctl | 0.566 [0.415, 0.715] | 0.567 [0.416, 0.715] | 0.556 [0.409, 0.703] | 0.011 [0.000, 0.029] | 0.136 [0.047, 0.239] | 0.256 [0.125, 0.394] | -0.254 [-0.350, -0.161] | 0.047 [0.024, 0.071] | 0.114 [0.051, 0.182] |
- K rain minus matched C rain: efficient islands 0.013 [-0.101, 0.128] (gen 2,000: 0.013 [-0.101, 0.128]); efficient+responsive 0.020 [-0.095, 0.136].
- prudent x10 minus matched C control: efficient islands 0.185 [0.022, 0.349] (gen 2,000: 0.185 [0.022, 0.349]); efficient+responsive 0.195 [0.033, 0.359].
- K rain minus base: efficient islands -0.006 [-0.182, 0.169] (gen 2,000: -0.006 [-0.182, 0.169]); efficient+responsive 0.004 [-0.168, 0.176].
- C rain minus base: efficient islands -0.018 [-0.200, 0.158] (gen 2,000: -0.018 [-0.200, 0.158]); efficient+responsive -0.016 [-0.200, 0.162].

**c = 0.01, n400i16**: efficient islands E and related statistics at the horizon 8000

| cell | E | E* | efficient+responsive | efficient+shadow | committed+compliant | light-cheater | inspector payoff | cheat prob | prudent mass |
|---|---|---|---|---|---|---|---|---|---|
| base | 0.550 [0.350, 0.750] | 0.550 [0.350, 0.750] | 0.500 [0.300, 0.700] | 0.050 [0.000, 0.150] | 0.303 [0.103, 0.503] | 0.097 [0.000, 0.244] | -0.387 [-0.826, -0.118] | 0.065 [0.000, 0.176] | 0.000 [0.000, 0.000] |
| rainK | 0.750 [0.550, 0.900] | 0.750 [0.550, 0.900] | 0.747 [0.547, 0.900] | 0.003 [0.000, 0.009] | 0.100 [0.000, 0.250] | 0.100 [0.000, 0.250] | -0.157 [-0.301, -0.050] | 0.028 [0.000, 0.069] | 0.000 [0.000, 0.000] |
| rainC | 0.650 [0.450, 0.850] | 0.650 [0.450, 0.850] | 0.600 [0.400, 0.800] | 0.050 [0.000, 0.150] | 0.103 [0.000, 0.253] | 0.206 [0.050, 0.400] | -0.248 [-0.419, -0.100] | 0.049 [0.012, 0.092] | 0.000 [0.000, 0.000] |
| boost | 0.650 [0.450, 0.850] | 0.650 [0.450, 0.850] | 0.650 [0.450, 0.850] | 0.000 [0.000, 0.000] | 0.250 [0.050, 0.450] | 0.050 [0.000, 0.150] | -0.147 [-0.241, -0.059] | 0.006 [0.000, 0.019] | 0.000 [0.000, 0.000] |
| boostctl | 0.600 [0.400, 0.800] | 0.600 [0.400, 0.800] | 0.550 [0.350, 0.750] | 0.050 [0.000, 0.150] | 0.256 [0.100, 0.450] | 0.138 [0.000, 0.300] | -0.214 [-0.352, -0.096] | 0.027 [0.000, 0.060] | 0.000 [0.000, 0.000] |
- K rain minus matched C rain: efficient islands 0.100 [0.000, 0.250] (gen 2,000: 0.084 [-0.013, 0.225]); efficient+responsive 0.147 [-0.003, 0.300].
- prudent x10 minus matched C control: efficient islands 0.050 [-0.250, 0.350] (gen 2,000: 0.075 [-0.225, 0.350]); efficient+responsive 0.100 [-0.200, 0.400].
- K rain minus base: efficient islands 0.200 [-0.100, 0.500] (gen 2,000: 0.194 [-0.106, 0.494]); efficient+responsive 0.247 [-0.053, 0.541].
- C rain minus base: efficient islands 0.100 [-0.200, 0.400] (gen 2,000: 0.109 [-0.191, 0.400]); efficient+responsive 0.100 [-0.250, 0.450].

**c = 0.01, n100i64**: efficient islands E and related statistics at the horizon 2000

| cell | E | E* | efficient+responsive | efficient+shadow | committed+compliant | light-cheater | inspector payoff | cheat prob | prudent mass |
|---|---|---|---|---|---|---|---|---|---|
| base | 0.701 [0.552, 0.827] | 0.701 [0.552, 0.827] | 0.637 [0.493, 0.776] | 0.064 [0.014, 0.129] | 0.025 [0.000, 0.075] | 0.186 [0.080, 0.311] | -0.207 [-0.320, -0.106] | 0.047 [0.022, 0.076] | 0.001 [0.000, 0.003] |
| rainK | 0.689 [0.541, 0.815] | 0.689 [0.541, 0.815] | 0.683 [0.536, 0.812] | 0.006 [0.000, 0.015] | 0.120 [0.033, 0.222] | 0.087 [0.021, 0.176] | -0.184 [-0.289, -0.097] | 0.033 [0.014, 0.058] | 0.003 [0.000, 0.006] |
| rainC | 0.608 [0.452, 0.756] | 0.608 [0.452, 0.756] | 0.552 [0.400, 0.696] | 0.056 [0.004, 0.128] | 0.107 [0.028, 0.208] | 0.186 [0.082, 0.307] | -0.386 [-0.634, -0.203] | 0.084 [0.038, 0.146] | 0.000 [0.000, 0.001] |
| boost | 0.823 [0.700, 0.926] | 0.823 [0.700, 0.926] | 0.823 [0.700, 0.926] | 0.000 [0.000, 0.000] | 0.057 [0.002, 0.132] | 0.101 [0.025, 0.201] | -0.106 [-0.184, -0.037] | 0.019 [0.003, 0.038] | 0.021 [0.003, 0.053] |
| boostctl | 0.732 [0.591, 0.866] | 0.732 [0.591, 0.866] | 0.666 [0.523, 0.797] | 0.066 [0.014, 0.131] | 0.057 [0.000, 0.132] | 0.171 [0.070, 0.295] | -0.207 [-0.350, -0.094] | 0.045 [0.016, 0.080] | 0.002 [0.000, 0.007] |
- K rain minus matched C rain: efficient islands 0.081 [-0.063, 0.233] (gen 2,000: 0.081 [-0.063, 0.233]); efficient+responsive 0.131 [-0.021, 0.287].
- prudent x10 minus matched C control: efficient islands 0.090 [-0.077, 0.259] (gen 2,000: 0.090 [-0.077, 0.259]); efficient+responsive 0.156 [-0.014, 0.328].
- K rain minus base: efficient islands -0.012 [-0.189, 0.163] (gen 2,000: -0.012 [-0.189, 0.163]); efficient+responsive 0.046 [-0.128, 0.212].
- C rain minus base: efficient islands -0.093 [-0.270, 0.075] (gen 2,000: -0.093 [-0.270, 0.075]); efficient+responsive -0.086 [-0.277, 0.103].

### Chain remedy (prior change, N = 10^4; whole state space)

| c | prior | π(E) | π(R) | mean inspector payoff | π(E) minus control |
|---|---|---|---|---|---|
| 0 | base | 0.1570 | 0.1457 | -0.4707 | -0.0028 |
| 0 | boost | 0.1724 | 0.1671 | -0.4592 | 0.0127 |
| 0 | control | 0.1597 | 0.1481 | -0.4700 | 0.0000 |
| 0.01 | base | 0.3307 | 0.2136 | -0.6228 | -0.0037 |
| 0.01 | boost | 0.3112 | 0.2307 | -0.5530 | -0.0233 |
| 0.01 | control | 0.3344 | 0.2151 | -0.6216 | 0.0000 |

## Controls

### Blind arm (no program reads) and inspector-only reading (`exact_er`) in the lottery

| cell | efficient islands (horizon) | efficient (gen 2,000) | inspector payoff | cheat prob | committed+compliant |
|---|---|---|---|---|---|
| blind c=0 n100i64 | 0.022 [0.014, 0.033] | 0.022 [0.014, 0.033] | -0.981 [-1.048, -0.911] | 0.241 [0.215, 0.264] | 0.163 [0.119, 0.220] |
| blind c=0 n400i16 | 0.006 [0.000, 0.016] | 0.034 [0.006, 0.069] | -1.053 [-1.186, -0.938] | 0.269 [0.230, 0.314] | 0.141 [0.091, 0.197] |
| blind c=0 n800i8 | 0.119 [0.013, 0.269] | 0.000 [0.000, 0.000] | -1.041 [-1.263, -0.816] | 0.266 [0.206, 0.327] | 0.069 [0.025, 0.125] |
| blind c=0 n400i64 | 0.017 [0.010, 0.024] | 0.011 [0.005, 0.017] | -0.977 [-1.007, -0.949] | 0.242 [0.232, 0.253] | 0.129 [0.098, 0.158] |
| exact_er c=0 n100i64 | 0.576 [0.425, 0.727] | 0.576 [0.425, 0.727] | -0.290 [-0.410, -0.178] | 0.074 [0.045, 0.104] | 0.008 [0.000, 0.021] |
| exact_er c=0.01 n100i64 | 0.359 [0.216, 0.507] | 0.359 [0.216, 0.507] | -0.506 [-0.635, -0.372] | 0.127 [0.093, 0.159] | 0.009 [0.000, 0.022] |

### Chain, inspector-only reading (`exact_er`)

| N | π(E) | π(R) | π(R*) | mean inspector payoff | largest exit from R | hazard from R (A neutral shadow / total) |
|---|---|---|---|---|---|---|
| 1000 | 0.4422 | 0.3588 | 0.3387 | -0.5270 | A neutral shadow | 1.54e-04 / 2.61e-04 |
| 10000 | 0.1714 | 0.1568 | 0.1489 | -0.5458 | D strict non-reading inspectee | 1.54e-05 / 1.05e-04 |

### Migration, mN in {0, 1, 10} at (100, 64)

| c | mN | efficient islands | gen 2,000 inspector payoff | committed+compliant | efficient+responsive |
|---|---|---|---|---|---|
| 0 | 0 | 0.585 [0.567, 0.602] | -0.555 [-0.590, -0.520] | 0.160 [0.145, 0.175] | 0.027 [0.021, 0.033] |
| 0 | 1 | 0.648 [0.500, 0.792] | -0.223 [-0.334, -0.122] | 0.109 [0.027, 0.205] | 0.637 [0.492, 0.779] |
| 0 | 10 | 0.388 [0.238, 0.550] | -0.302 [-0.391, -0.216] | 0.448 [0.298, 0.598] | 0.317 [0.181, 0.467] |
| 0.01 | 0 | 0.587 [0.570, 0.603] | -0.549 [-0.584, -0.513] | 0.159 [0.145, 0.174] | 0.025 [0.020, 0.031] |
| 0.01 | 1 | 0.701 [0.552, 0.827] | -0.207 [-0.320, -0.106] | 0.025 [0.000, 0.075] | 0.637 [0.493, 0.776] |
| 0.01 | 10 | 0.500 [0.350, 0.650] | -0.272 [-0.372, -0.178] | 0.350 [0.200, 0.500] | 0.425 [0.275, 0.575] |

### Direct starts (monomorphic islands, no mutation, no migration; one K arrival into every island at generation 100 where K = 1)

Base `CRI` = `cr(THEM(ME))`, twin `N` (or the reverse); the injected twin is n copies; fractions are islands (64 per run, 20 runs). `twin fixed` = the injected twin has fixed; `K majority` = K above one half; `recovered` = responsive inspectors hold at least half the seat and K is below 1%. First row of each pair: generation 100 (before the arrival); second: the horizon 20N.

| N | base | injected | K arrival | at generation | twin fixed | K majority | efficient | efficient+shadow | recovered |
|---|---|---|---|---|---|---|---|---|---|
| 100 | CRI | 1 | 0 | 100 | 0.011 | 0.000 | 1.000 | 0.016 | 0.984 |
| 100 | CRI | 1 | 0 | 2000 | 0.016 | 0.000 | 1.000 | 0.016 | 0.984 |
| 100 | CRI | 1 | 1 | 100 | 0.011 | 0.000 | 1.000 | 0.016 | 0.984 |
| 100 | CRI | 1 | 1 | 2000 | 0.016 | 0.005 | 0.995 | 0.011 | 0.984 |
| 100 | CRI | 10 | 0 | 100 | 0.065 | 0.000 | 1.000 | 0.102 | 0.898 |
| 100 | CRI | 10 | 0 | 2000 | 0.101 | 0.000 | 1.000 | 0.101 | 0.899 |
| 100 | CRI | 10 | 1 | 100 | 0.065 | 0.000 | 1.000 | 0.102 | 0.898 |
| 100 | CRI | 10 | 1 | 2000 | 0.099 | 0.015 | 0.985 | 0.084 | 0.901 |
| 100 | CRI | 50 | 0 | 100 | 0.398 | 0.000 | 1.000 | 0.498 | 0.502 |
| 100 | CRI | 50 | 0 | 2000 | 0.498 | 0.000 | 1.000 | 0.498 | 0.502 |
| 100 | CRI | 50 | 1 | 100 | 0.398 | 0.000 | 1.000 | 0.498 | 0.502 |
| 100 | CRI | 50 | 1 | 2000 | 0.493 | 0.111 | 0.889 | 0.382 | 0.507 |
| 100 | N | 1 | 0 | 100 | 0.009 | 0.000 | 1.000 | 0.987 | 0.013 |
| 100 | N | 1 | 0 | 2000 | 0.013 | 0.000 | 1.000 | 0.988 | 0.013 |
| 100 | N | 1 | 1 | 100 | 0.009 | 0.000 | 1.000 | 0.987 | 0.013 |
| 100 | N | 1 | 1 | 2000 | 0.013 | 0.255 | 0.745 | 0.733 | 0.013 |
| 100 | N | 10 | 0 | 100 | 0.064 | 0.000 | 1.000 | 0.896 | 0.104 |
| 100 | N | 10 | 0 | 2000 | 0.100 | 0.000 | 1.000 | 0.900 | 0.100 |
| 100 | N | 10 | 1 | 100 | 0.064 | 0.000 | 1.000 | 0.896 | 0.104 |
| 100 | N | 10 | 1 | 2000 | 0.102 | 0.250 | 0.750 | 0.648 | 0.102 |
| 100 | N | 50 | 0 | 100 | 0.408 | 0.000 | 1.000 | 0.498 | 0.502 |
| 100 | N | 50 | 0 | 2000 | 0.502 | 0.000 | 1.000 | 0.498 | 0.502 |
| 100 | N | 50 | 1 | 100 | 0.408 | 0.000 | 1.000 | 0.498 | 0.502 |
| 100 | N | 50 | 1 | 2000 | 0.507 | 0.111 | 0.889 | 0.382 | 0.507 |
| 400 | CRI | 1 | 0 | 100 | 0.000 | 0.000 | 1.000 | 0.001 | 0.999 |
| 400 | CRI | 1 | 0 | 8000 | 0.002 | 0.000 | 1.000 | 0.002 | 0.998 |
| 400 | CRI | 1 | 1 | 100 | 0.000 | 0.000 | 1.000 | 0.001 | 0.999 |
| 400 | CRI | 1 | 1 | 8000 | 0.002 | 0.000 | 1.000 | 0.002 | 0.998 |
| 400 | CRI | 40 | 0 | 100 | 0.000 | 0.000 | 1.000 | 0.054 | 0.946 |
| 400 | CRI | 40 | 0 | 8000 | 0.095 | 0.000 | 1.000 | 0.095 | 0.905 |
| 400 | CRI | 40 | 1 | 100 | 0.000 | 0.000 | 1.000 | 0.054 | 0.946 |
| 400 | CRI | 40 | 1 | 8000 | 0.094 | 0.000 | 1.000 | 0.094 | 0.906 |
| 400 | CRI | 200 | 0 | 100 | 0.074 | 0.000 | 1.000 | 0.502 | 0.498 |
| 400 | CRI | 200 | 0 | 8000 | 0.497 | 0.000 | 1.000 | 0.497 | 0.503 |
| 400 | CRI | 200 | 1 | 100 | 0.074 | 0.000 | 1.000 | 0.502 | 0.498 |
| 400 | CRI | 200 | 1 | 8000 | 0.479 | 0.015 | 0.985 | 0.464 | 0.521 |
| 400 | N | 1 | 0 | 100 | 0.000 | 0.000 | 1.000 | 0.998 | 0.002 |
| 400 | N | 1 | 0 | 8000 | 0.002 | 0.000 | 1.000 | 0.998 | 0.002 |
| 400 | N | 1 | 1 | 100 | 0.000 | 0.000 | 1.000 | 0.998 | 0.002 |
| 400 | N | 1 | 1 | 8000 | 0.002 | 0.253 | 0.747 | 0.745 | 0.002 |
| 400 | N | 40 | 0 | 100 | 0.001 | 0.000 | 1.000 | 0.937 | 0.063 |
| 400 | N | 40 | 0 | 8000 | 0.098 | 0.000 | 1.000 | 0.902 | 0.098 |
| 400 | N | 40 | 1 | 100 | 0.001 | 0.000 | 1.000 | 0.937 | 0.063 |
| 400 | N | 40 | 1 | 8000 | 0.111 | 0.169 | 0.831 | 0.720 | 0.111 |
| 400 | N | 200 | 0 | 100 | 0.059 | 0.000 | 1.000 | 0.502 | 0.498 |
| 400 | N | 200 | 0 | 8000 | 0.503 | 0.000 | 1.000 | 0.497 | 0.503 |
| 400 | N | 200 | 1 | 100 | 0.059 | 0.000 | 1.000 | 0.502 | 0.498 |
| 400 | N | 200 | 1 | 8000 | 0.521 | 0.015 | 0.985 | 0.464 | 0.521 |

## Post-hoc ablations of the inspector and inspectee priors (chain, exact arm, c = 0; added after the counted cells were seen; no registered prediction)

`noshadow`: the six unconditional-shadow inspector classes (payoff twins of `cr(THEM(ME))` against `C` that do not deter K; prior mass 0.3072, `N` among them) get prior mass 0; `nolight`: the twelve inspectee classes that strictly invade (CRI, C) (mass 0.0031) get 0; `nolightnr` / `nolightrd`: only the non-reading / only the reading ones; `neither`: both removed. Everything renormalised. Whole state space, float32 storage.

| variant | N | π(E) | π(R) | odds E | mean inspector payoff | largest exit from R | hazard from R | committed+compliant | light cheater | shadow excursion |
|---|---|---|---|---|---|---|---|---|---|---|
| base | 1000 | 0.3432 | 0.2789 | 0.5225 | -0.4959 | A | 2.78e-04 | 0.452 | 0.086 | 0.0188 |
| base | 10000 | 0.1570 | 0.1457 | 0.1862 | -0.4707 | D | 1.21e-04 | 0.527 | 0.271 | 0.0033 |
| base | 100000 | 0.0466 | 0.0441 | 0.04891 | -0.5327 | D | 1.10e-04 | 0.597 | 0.298 | 0.0007 |
| noshadow | 1000 | 0.1790 | 0.1790 | 0.218 | -0.4613 | D | 1.07e-04 | 0.086 | 0.663 | 0.0001 |
| noshadow | 10000 | 0.0996 | 0.0996 | 0.1106 | -0.5292 | D | 1.04e-04 | 0.252 | 0.582 | 0.0000 |
| noshadow | 100000 | 0.0461 | 0.0461 | 0.04836 | -0.5569 | D | 1.07e-04 | 0.500 | 0.357 | 0.0000 |
| nolight | 1000 | 0.4520 | 0.3883 | 0.8247 | -0.4311 | A | 1.98e-04 | 0.415 | 0.014 | 0.0185 |
| nolight | 10000 | 0.6356 | 0.6261 | 1.744 | -0.1981 | A | 2.34e-05 | 0.287 | 0.038 | 0.0028 |
| nolight | 100000 | 0.8112 | 0.8099 | 4.296 | -0.1053 | A | 3.00e-06 | 0.102 | 0.062 | 0.0004 |
| nolightnr | 10000 | 0.3956 | 0.3850 | 0.6545 | -0.3419 | E | 4.30e-05 | 0.513 | 0.041 | 0.0031 |
| nolightnr | 100000 | 0.2392 | 0.2369 | 0.3145 | -0.4191 | E | 1.91e-05 | 0.590 | 0.076 | 0.0007 |
| nolightrd | 10000 | 0.1739 | 0.1633 | 0.2105 | -0.4541 | D | 1.01e-04 | 0.323 | 0.464 | 0.0031 |
| nolightrd | 100000 | 0.0355 | 0.0339 | 0.03676 | -0.6122 | D | 8.71e-05 | 0.125 | 0.819 | 0.0005 |
| neither | 1000 | 0.9758 | 0.9758 | 40.36 | -0.0110 | E | 3.24e-06 | 0.010 | 0.003 | 0.0000 |
| neither | 10000 | 0.9895 | 0.9895 | 94.39 | -0.0057 | E | 3.81e-07 | 0.004 | 0.004 | 0.0000 |
| neither | 100000 | 0.9962 | 0.9962 | 259 | -0.0026 | E | 4.18e-08 | 0.001 | 0.002 | 0.0000 |

Odds slopes over the available N: base -0.514; noshadow -0.327; nolight 0.358; nolightnr -0.318; nolightrd -0.758; neither 0.404.

## Verdicts (conventions of predictions/2026-10-24-inspection-shadow.md)

- **Prediction 1 (mechanism): FAILED.** Neutral-drift hazard from R has slope -1.067 over N = [1000, 10000, 100000] (range −1.2…−0.8: yes). Largest exit from R: N=1000 A; N=10000 D; N=100000 D; largest exit from E: N=1000 C; N=10000 C; N=100000 C (strict inspectee flux from non-deterring / deterring inspectors: N=1000 3.91e-03/3.84e-05; N=10000 6.87e-04/1.59e-05; N=100000 1.55e-04/4.82e-06). Falsifier fired at 2 of 3 values of N.
- **Prediction 2 (scaling): HELD.** Odds of E over N = [1000, 10000, 100000]: 0.5225, 0.1862, 0.04891; least-squares slope -0.514 (held iff < 0.5). P(E) = 0.3432, 0.1570, 0.0466; it rises at every consecutive pair: False (gpt-6.1-sol and gemini-4-argon counter-predictions: failed).
- **Prediction 3 (lottery path): FAILED.** Efficient islands at (800, 8), c = 0, generation 16,000: 0.800 [0.600, 0.950] (generation 2,000: 0.744 [0.544, 0.912]); at (100, 64): 0.648 [0.500, 0.792]. Gemini-4-argon counter-prediction (stay at or above 0.5): held.
- **Prediction 4 (cheater fringe): FAILED.** K rain minus matched C rain, efficient islands at (400, 16), c = 0, generation 8,000: -0.050 [-0.200, 0.100].
- **Prediction 5 (prudent inspectees): PARTIAL.** Chain, N = 10^4, c = 0: π(E) boosted minus matched control = 0.0127 (π(R): 0.0190).
- **Prediction 6 (price): HELD.** Effect at c = 0: 0.0127; at c = 0.01: -0.0233.
- **E1 (crossover between 10^3 and 10^4): HELD.** Largest exit from R by N: {1000: 'A_neutral_shadow', 10000: 'D_strict_other_nonreader', 100000: 'D_strict_other_nonreader'}.
- **E2 (odds slope negative): HELD.** Slope -0.514.
- **E3 (tolerated light cheaters hold more π than the shadow excursion at N ≥ 10^4): HELD.** Light-cheater / shadow-excursion occupancy: N=10000 0.2712 / 0.0033; N=100000 0.2976 / 0.0007.
- **E4 (c = 0.01: leaving R by the shadow is selection, slope above −0.3): HELD.** Slope of the (A + F) hazard over N = [1000, 10000, 100000]: -0.015.
- **E5 (prudent boost effect in [0, 0.1)): HELD.** Effect 0.0127.

## Deviations, caveats and readings

- **Float32 storage** of the whole-space jump-chain matrices (memory contention with the exploration audit; every file records its dtype). Controls: against the previous run's float64 solver the top-12 π agree to 7·10⁻⁷ relative at c = 0 (N = 10², 10³, 10⁴) and c = 0.01 (10³, 10⁴), the mean payoffs to five digits; the global-balance residual of every cell is below 2·10⁻⁶; a 6,400-state sub-arm agrees with float64 to 2·10⁻⁶ at N up to 10⁵.
- **No cut** from the spec's cut order: N = 10⁵, (800, 8), (400, 64), mN = 10 and the c = 0.01 remedy cells were all run.
- **Post-hoc additions (no registered prediction):** the ablations above (shadow and light cheaters removed from the priors), the direct-start design (notes §2.10), the descriptive island statistics (E*, efficient+responsive, efficient+shadow, light-cheater islands). Their definitions were fixed in the predictions file or the notes before the counted cells, except the ablations, which were added after the chain tables were seen.
- **Prediction 6** is scored held by the registered rule (the c = 0 effect is positive, the c = 0.01 effect is smaller), but both effects are within 0.03 of zero and the c = 0 effect is the "partial" of Prediction 5; it is not evidence of a price effect.
- **Lottery intervals** are wide (20 runs of 8–16 islands at the larger sizes); the size path is not monotone, and the crossed cell (400, 64) shows that I, not N, moves the (400, 16) value.
- **Hand estimates of notes §1.2 checked against the chain.** Held: the neutral hazard 0.1546/N (measured slope −1.07), the crossover near 2.1·10³ (measured between 10³ and 10⁴), the one-state strict hazard 7.4·10⁻⁵ (reproduced), and about 1% of loops of the four-cycle reaching R (first entry into R from (I, C): 0.0108 against 0.00332/0.31052 = 0.0107). **Refuted:** the estimate that the stationary mass of E \ R is about 2.5/N (measured 0.064 at N = 10³, 26 times larger): E \ R is re-entered from the cycle of constants about 100 times per drift entry from R, so the flux out of E is dominated by `K` striking states of E \ R that were entered from outside E (3.9·10⁻³ against 3.8·10⁻⁵ per event at N = 10³).

