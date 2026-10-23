# Rock-paper-scissors and mixed actions (run report, 2026-10-23)

Spec `specs/2026-10-23-rps-mixed.md`; predictions `predictions/2026-10-23-rps.md`; notes `notes/rps.md`. Code `src/rps.py`, `src/rps_n7.py`, `src/rps_run.py`, `src/rps_report.py`, tests `tests/test_rps.py`. Every chain number below is an epsilon -> 0 object (pi, closure-complete over the monomorphic class states, see §2); every lottery number is an epsilon = 0 finite-(N, I, horizon) statistic at (N, I) = (100, 64) unless stated, mN = 1, w = 0.3, never pi. Time in generations of I*N events. Intervals are 95% bootstrap intervals over runs.

## 0. Completeness

98 of 98 cells complete.

Missing or partial: none

## 1. Static numbers and validation

| arm | programs (n=6) | classes | classes (5 dec.) | antisymmetry err | cyclic relabel err (U) | mean forfeit mass over pairs | classes with distribution-heterogeneous members |
|---|---|---|---|---|---|---|---|
| pure | 46 | 18 | 18 | 0.0e+00 | 0.0e+00 | 4.73e-02 | 0 |
| sample | 1258 | 87 | 87 | 1.4e-16 | 8.3e-17 | 2.28e-04 | 1 |
| matched | 3696 | 87 | 87 | 1.4e-16 | 8.3e-17 | 1.77e-04 | 1 |
| exact | 3696 | 125 | 125 | 1.4e-16 | 8.3e-17 | 1.77e-04 | 1 |
| exact_uniform | 3696 | 123 | 123 | 1.1e-16 | 1.4e-16 | 0.00e+00 | 1 |
| exact_br | 3696 | 123 | 123 | 1.4e-16 | 8.3e-17 | 3.12e-05 | 1 |
| constants | 3 | 3 | 3 | 0.0e+00 | n/a | 0.00e+00 | 0 |
| constx | 4 | 4 | 4 | 0.0e+00 | n/a | 0.00e+00 | 0 |

Hand-computed named-class payoffs (notes §1.3, eleven programs, 121 entries) agree with the evaluator to 1e-12 (`tests/test_rps.py::test_hand_table`); the recursive reference evaluator agrees with the batched one on random and reading-heavy pairs in all six semantic arms; the two-type contest through `LogChain` reproduces `chain.Chain` and the closed-form Moran ratio; the blocked evaluator used for n = 7 reproduces the full table at n = 6.

### Prediction 1 statics

| arm | programs not forfeiting vs X | max |payoff vs X| among them | programs forfeiting vs X | forfeit mass of the exact (or matched) counter in self-play | opponents deterministic against N | counterexamples (u(N, b) != +1) | u(N, R/P/S) |
|---|---|---|---|---|---|---|---|
| sample | 1258 | 0.0e+00 | 0 | n/a | 141 | 0 | [1.0, 1.0, 1.0] |
| matched | 3696 | 0.0e+00 | 0 | 1.0 | 648 | 0 | [1.0, 1.0, 1.0] |
| exact | 3696 | 0.0e+00 | 0 | 1.0 | 1248 | 0 | [1.0, 1.0, 1.0] |

### Depth sweep (D = 11, 12, 13, 20)

Program-level, all pairs of the full table (payoff difference from D = 12):

| arm | D | max |dU| over all pairs | fraction of pairs with |dU| > 1e-9 | fraction with sign change | max |dU| on 1,000 sampled pairs |
|---|---|---|---|---|---|
| pure | 11 | 0 | 0.00e+00 | 0.00e+00 | 0 |
| pure | 13 | 0 | 0.00e+00 | 0.00e+00 | 0 |
| pure | 20 | 0 | 0.00e+00 | 0.00e+00 | 0 |
| sample | 11 | 0.0155 | 2.12e-03 | 2.02e-04 | 0.00781 |
| sample | 13 | 0.0112 | 2.06e-03 | 2.02e-04 | 0.00781 |
| sample | 20 | 0.0145 | 2.18e-03 | 6.07e-05 | 0.00732 |
| matched | 11 | 0.0155 | 9.02e-04 | 1.15e-04 | 3.05e-05 |
| matched | 13 | 0.0112 | 8.88e-04 | 1.15e-04 | 1.53e-05 |
| matched | 20 | 0.0145 | 9.31e-04 | 2.11e-05 | 3.04e-05 |
| exact | 11 | 1 | 9.68e-04 | 1.05e-04 | 3.05e-05 |
| exact | 13 | 2 | 9.54e-04 | 1.11e-04 | 1.53e-05 |
| exact | 20 | 0.0146 | 9.72e-04 | 1.05e-05 | 3.04e-05 |
| exact_uniform | 11 | 1 | 3.75e-04 | 5.01e-05 | 3.05e-05 |
| exact_uniform | 13 | 2 | 3.59e-04 | 4.83e-05 | 1.53e-05 |
| exact_uniform | 20 | 0.0219 | 3.37e-04 | 1.58e-05 | 3.04e-05 |
| exact_br | 11 | 1 | 4.03e-04 | 6.53e-05 | 3.05e-05 |
| exact_br | 13 | 2 | 3.89e-04 | 6.35e-05 | 1.53e-05 |
| exact_br | 20 | 0.0145 | 3.64e-04 | 1.05e-05 | 3.04e-05 |

On the pairs that matter (named classes, classes holding 0.99 of pi at N = 10^2..10^5, classes holding 0.99 of the primary lottery mass):

| arm | classes | D | pairs with |dU| > 1e-9 | pairs | sign flips | max |dU| | max |d forfeit mass| |
|---|---|---|---|---|---|---|---|
| pure | 13 | 11 | 0 | 169 | 0 | 0 | 0 |
| pure | 13 | 13 | 0 | 169 | 0 | 0 | 0 |
| pure | 13 | 20 | 0 | 169 | 0 | 0 | 0 |
| sample | 43 | 11 | 94 | 1849 | 24 | 0.0155 | 0.00781 |
| sample | 43 | 13 | 100 | 1849 | 24 | 0.0101 | 0.00781 |
| sample | 43 | 20 | 100 | 1849 | 6 | 0.0145 | 0.0146 |
| matched | 32 | 11 | 94 | 1024 | 24 | 0.0155 | 0.00781 |
| matched | 32 | 13 | 100 | 1024 | 24 | 0.0101 | 0.00781 |
| matched | 32 | 20 | 100 | 1024 | 6 | 0.0145 | 0.0146 |
| exact | 50 | 11 | 400 | 2500 | 102 | 1 | 0.00781 |
| exact | 50 | 13 | 406 | 2500 | 102 | 2 | 0.00781 |
| exact | 50 | 20 | 400 | 2500 | 6 | 0.0145 | 0.0146 |

Inferred versus actual opponent action (a reader of `THEM(ME)` sees the opponent at one level less depth), over the same class sets:

| arm | reading pairs | pairs with inferred != actual | mean TV | max TV | worst pairs |
|---|---|---|---|---|---|
| pure | 39 | 0 | 0 | 0.0000 | THEM(ME) vs P; THEM(ME) vs R |
| sample | 344 | 70 | 0.000364 | 0.0078 | THEM(ME) vs next(coin(P,THEM(ME))); THEM(ME) vs next(coin(R,THEM(ME))) |
| matched | 256 | 70 | 0.000489 | 0.0078 | THEM(ME) vs next(coin(P,THEM(ME))); THEM(ME) vs next(coin(R,THEM(ME))) |
| exact | 800 | 300 | 0.0287 | 0.9999 | cr(coin(S,THEM(ME))) vs cr(coin(P,THEM(ME))); cr(coin(X,THEM(ME))) vs cr(coin(P,THEM(ME))) |

## 2. The epsilon -> 0 chain (class table at n = 6, D = 12, w = 0.3, prior = length prior)

The explored set is the full monomorphic closure in every cell (expanded states = classes; theta_log 1e-12 / 1e-14 / 1e-16 and the lumped versus twin-expanded runs were executed for pure, sample and exact at N = 10^4 and agree to four decimals in every statistic: files `chain_*_th12.json`, `_th16.json`, `_lumped.json`). In an antisymmetric symmetric game a single mutant meets a monomorphic resident in a two-type contest, which has no interior attractor, so every state is monomorphic: the "polymorphic" part of the spec's chain never arises, no three-type replicator cycle is met (indeterminate events: 0 in all cells), and the chain is a weighted tournament on the classes. The three-constant polymorphism is never visited.

| arm | N | e (own exploiters) | e (exact-grammar exploiters) | action expl. | mixing (vs pop.) | self-play forfeit | constants | X | GN | GC | states for 0.99 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pure | 100 | 0.382 | 0.387 | 1.000 | 0.000 | 0.813 | 0.133 | 0.000 | 0.0000 | 0.0000 | 12 |
| pure | 1000 | 0.089 | 0.096 | 1.000 | 0.000 | 0.971 | 0.019 | 0.000 | 0.0000 | 0.0000 | 8 |
| pure | 10000 | 0.012 | 0.019 | 1.000 | 0.000 | 0.997 | 0.002 | 0.000 | 0.0000 | 0.0000 | 3 |
| pure | 100000 | 0.001 | 0.009 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.0000 | 0.0000 | 2 |
| pure | 1000000 | 0.000 | 0.008 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.0000 | 0.0000 | 2 |
| sample | 100 | 0.666 | 0.675 | 0.717 | 0.235 | 0.105 | 0.548 | 0.221 | 0.0028 | 0.0000 | 41 |
| sample | 1000 | 0.489 | 0.525 | 0.704 | 0.273 | 0.431 | 0.233 | 0.221 | 0.0128 | 0.0000 | 29 |
| sample | 10000 | 0.291 | 0.354 | 0.682 | 0.313 | 0.631 | 0.042 | 0.221 | 0.0263 | 0.0000 | 18 |
| sample | 100000 | 0.092 | 0.190 | 0.574 | 0.426 | 0.565 | 0.007 | 0.221 | 0.0773 | 0.0000 | 8 |
| sample | 1000000 | 0.017 | 0.169 | 0.244 | 0.756 | 0.242 | 0.001 | 0.221 | 0.2483 | 0.0000 | 6 |
| sample | 10000000 | 0.002 | 0.184 | 0.036 | 0.964 | 0.036 | 0.000 | 0.221 | 0.3569 | 0.0000 | 5 |
| matched | 100 | 0.679 | 0.687 | 0.723 | 0.239 | 0.091 | 0.579 | 0.227 | 0.0019 | 0.0000 | 29 |
| matched | 1000 | 0.504 | 0.540 | 0.706 | 0.274 | 0.403 | 0.263 | 0.227 | 0.0088 | 0.0000 | 24 |
| matched | 10000 | 0.293 | 0.358 | 0.682 | 0.313 | 0.623 | 0.050 | 0.227 | 0.0187 | 0.0000 | 16 |
| matched | 100000 | 0.086 | 0.185 | 0.607 | 0.392 | 0.598 | 0.008 | 0.227 | 0.0526 | 0.0000 | 8 |
| matched | 1000000 | 0.016 | 0.155 | 0.341 | 0.659 | 0.339 | 0.001 | 0.227 | 0.2062 | 0.0000 | 6 |
| matched | 10000000 | 0.002 | 0.176 | 0.064 | 0.936 | 0.064 | 0.000 | 0.227 | 0.3692 | 0.0000 | 5 |
| exact | 100 | 0.703 | 0.703 | 0.727 | 0.240 | 0.092 | 0.585 | 0.227 | 0.0010 | 0.0005 | 43 |
| exact | 1000 | 0.590 | 0.590 | 0.704 | 0.277 | 0.396 | 0.266 | 0.227 | 0.0046 | 0.0023 | 40 |
| exact | 10000 | 0.432 | 0.432 | 0.679 | 0.307 | 0.598 | 0.059 | 0.227 | 0.0114 | 0.0053 | 32 |
| exact | 100000 | 0.198 | 0.198 | 0.662 | 0.329 | 0.637 | 0.014 | 0.227 | 0.0389 | 0.0091 | 18 |
| exact | 1000000 | 0.055 | 0.055 | 0.467 | 0.530 | 0.461 | 0.003 | 0.227 | 0.1699 | 0.0066 | 12 |
| exact | 10000000 | 0.010 | 0.010 | 0.112 | 0.887 | 0.111 | 0.001 | 0.227 | 0.3758 | 0.0016 | 5 |
| exact_uniform | 100 | 0.703 | n/a | 0.635 | 0.333 | 0.000 | 0.585 | 0.227 | 0.0009 | 0.0005 | 41 |
| exact_uniform | 1000 | 0.590 | n/a | 0.306 | 0.674 | 0.000 | 0.264 | 0.227 | 0.0045 | 0.0023 | 40 |
| exact_uniform | 10000 | 0.433 | n/a | 0.080 | 0.906 | 0.000 | 0.058 | 0.227 | 0.0100 | 0.0046 | 31 |
| exact_uniform | 100000 | 0.184 | n/a | 0.023 | 0.968 | 0.000 | 0.013 | 0.227 | 0.0223 | 0.0052 | 18 |
| exact_uniform | 1000000 | 0.029 | n/a | 0.003 | 0.995 | 0.000 | 0.002 | 0.227 | 0.0306 | 0.0012 | 9 |
| exact_uniform | 10000000 | 0.003 | n/a | 0.000 | 0.999 | 0.000 | 0.000 | 0.227 | 0.0320 | 0.0001 | 3 |
| exact_br | 100 | 0.703 | n/a | 0.683 | 0.284 | 0.048 | 0.585 | 0.227 | 0.0010 | 0.0005 | 41 |
| exact_br | 1000 | 0.592 | n/a | 0.512 | 0.469 | 0.205 | 0.265 | 0.227 | 0.0045 | 0.0023 | 39 |
| exact_br | 10000 | 0.438 | n/a | 0.432 | 0.554 | 0.351 | 0.058 | 0.227 | 0.0108 | 0.0047 | 31 |
| exact_br | 100000 | 0.199 | n/a | 0.560 | 0.431 | 0.535 | 0.013 | 0.227 | 0.0362 | 0.0055 | 18 |
| constants | 100 | 1.000 | n/a | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.0000 | 0.0000 | 3 |
| constants | 1000 | 1.000 | n/a | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.0000 | 0.0000 | 3 |
| constants | 10000 | 1.000 | n/a | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.0000 | 0.0000 | 3 |
| constants | 100000 | 1.000 | n/a | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.0000 | 0.0000 | 3 |
| constx | 100 | 0.750 | n/a | 0.750 | 0.250 | 0.000 | 0.750 | 0.250 | 0.0000 | 0.0000 | 4 |
| constx | 1000 | 0.750 | n/a | 0.750 | 0.250 | 0.000 | 0.750 | 0.250 | 0.0000 | 0.0000 | 4 |
| constx | 10000 | 0.750 | n/a | 0.750 | 0.250 | 0.000 | 0.750 | 0.250 | 0.0000 | 0.0000 | 4 |
| constx | 100000 | 0.750 | n/a | 0.750 | 0.250 | 0.000 | 0.750 | 0.250 | 0.0000 | 0.0000 | 4 |

**X is an always-neutral entrant: pi(class X) equals its prior mass exactly.** Every program that does not forfeit against X earns 0 against it and X earns 0 against everything, so X invades every monomorphic state at the neutral rate 1/N and leaves it at the neutral rate; detailed balance gives pi(X) = mu(X) at every N. Max |pi(X) - mu(X)| over the 24 cells where X is in the grammar: 1.5e-15.

Support and transition structure at N = 10^4 (top states; each is a monomorphic class):

* **pure** (K = 18; states for 0.99 of pi: 3): next(THEM(ME)) 0.970; THEM(ME) 0.018; next(THEM(THEM)) 0.004; THEM(THEM) 0.004; R 0.001; P 0.001
  Top state exits (log10 rate per mutation event): -5.35; to THEM(ME) (-5.74; by THEM(ME)); THEM(THEM) (-5.79; by THEM(THEM)); next(THEM(THEM)) (-6.28; by next(THEM(THEM)))
* **sample** (K = 87; states for 0.99 of pi: 18): next(THEM(ME)) 0.391; X 0.221; next(THEM(THEM)) 0.207; next(THEM(^X)) 0.062; THEM(THEM) 0.029; next(coin(X,THEM(ME))) 0.026
  Top state exits (log10 rate per mutation event): -4.62; to X (-4.66; by X); coin(X,THEM(ME)) (-6.23; by coin(X,THEM(ME))); THEM(ME) (-6.47; by THEM(ME))
* **matched** (K = 87; states for 0.99 of pi: 16): next(THEM(ME)) 0.391; X 0.227; next(THEM(THEM)) 0.203; next(THEM(^X)) 0.065; THEM(THEM) 0.026; next(coin(X,THEM(ME))) 0.019
  Top state exits (log10 rate per mutation event): -4.62; to X (-4.64; by X); coin(X,THEM(ME)) (-6.58; by coin(X,THEM(ME))); THEM(ME) (-6.65; by THEM(ME))
* **exact** (K = 125; states for 0.99 of pi: 32): next(THEM(ME)) 0.229; X 0.227; cr(THEM(ME)) 0.140; cr(THEM(THEM)) 0.103; next(THEM(THEM)) 0.093; THEM(THEM) 0.031
  Top state exits (log10 rate per mutation event): -4.62; to X (-4.64; by X); coin(X,THEM(ME)) (-6.58; by coin(X,THEM(ME))); THEM(ME) (-6.66; by THEM(ME))

Convergence in N (exact, e own / e exact-set / mixing): N=100: 0.703 / 0.703 / 0.240; N=1000: 0.590 / 0.590 / 0.277; N=10000: 0.432 / 0.432 / 0.307; N=100000: 0.198 / 0.198 / 0.329; N=1000000: 0.055 / 0.055 / 0.530; N=10000000: 0.010 / 0.010 / 0.887.

### The N -> infinity limit of the chain, and the approach to it

Let Z0 be the classes nobody can exploit (e(c) = max_k U[k, c] = 0 over the arm's own classes). Members of Z0 are payoff-neutral to one another, a mutant strictly beating a non-Z0 state exits it at an N-independent rate while neutral moves cost 1/N, so as N -> infinity pi concentrates on Z0 with weights proportional to the prior: pi_inf(c) = mu(c) / mu(Z0) on Z0 (and pi(X) = mu(X) at every finite N). This is exact for the class table; the finite-N chain approaches it at a speed set by the smallest exploitabilities in the table.

| arm | |Z0| | prior mass of Z0 | mixing under pi_inf | self-play forfeit under pi_inf | action expl. under pi_inf | pi(Z0) N=10^2 | 10^3 | 10^4 | 10^5 | 10^6 | 10^7 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pure | 2 | 0.0236 | 0.00 | 1.00 | 1.00 | 0.618 | 0.911 | 0.988 | 0.999 | 1.000 | - |
| sample | 4 | 0.2211 | 1.00 | 0.00 | 0.00 | 0.232 | 0.268 | 0.312 | 0.425 | 0.756 | 0.964 |
| matched | 4 | 0.2278 | 1.00 | 0.00 | 0.00 | 0.237 | 0.271 | 0.312 | 0.392 | 0.659 | 0.936 |
| exact | 2 | 0.2275 | 1.00 | 0.00 | 0.00 | 0.228 | 0.232 | 0.239 | 0.266 | 0.397 | 0.603 |
| exact_uniform | 5 | 0.2301 | 1.00 | 0.00 | 0.00 | 0.252 | 0.336 | 0.471 | 0.765 | 0.963 | 0.996 |
| exact_br | 3 | 0.2276 | 1.00 | 0.00 | 0.00 | 0.229 | 0.232 | 0.239 | 0.276 | - | - |

Members of Z0 (exact arm): X, next(coin(X,THEM(ME))). Pure arm: THEM(ME), next(THEM(ME)).

pi mass by exploitability bucket e(c) of the state's class (exact arm; the tiny-e classes are exploitable only through the cap residue):

| N | e = 0 | (0, 1e-3] | (1e-3, 1e-2] | (1e-2, 0.1] | (0.1, 0.5] | (0.5, 1] |
|---|---|---|---|---|---|---|
| 100 | 0.228 | 0.000 | 0.022 | 0.002 | 0.085 | 0.663 |
| 1000 | 0.232 | 0.000 | 0.101 | 0.002 | 0.141 | 0.524 |
| 10000 | 0.239 | 0.001 | 0.229 | 0.002 | 0.178 | 0.351 |
| 100000 | 0.266 | 0.014 | 0.463 | 0.002 | 0.102 | 0.153 |
| 1000000 | 0.397 | 0.115 | 0.416 | 0.001 | 0.032 | 0.039 |
| 10000000 | 0.603 | 0.281 | 0.103 | 0.000 | 0.006 | 0.007 |

### Sensitivity to the cap D (N = 10^4 and 10^3) and to the prior (2^-nodes)

| arm | N | D = 11: e / mixing | D = 12 | D = 13 | D = 20 |
|---|---|---|---|---|---|
| pure | 1000 | 0.089 / 0.000 | 0.089 / 0.000 | 0.089 / 0.000 | 0.089 / 0.000 |
| pure | 10000 | 0.012 / 0.000 | 0.012 / 0.000 | 0.012 / 0.000 | 0.012 / 0.000 |
| sample | 1000 | 0.487 / 0.276 | 0.489 / 0.273 | 0.487 / 0.276 | 0.487 / 0.272 |
| sample | 10000 | 0.286 / 0.310 | 0.291 / 0.313 | 0.286 / 0.310 | 0.286 / 0.307 |
| matched | 1000 | 0.503 / 0.276 | 0.504 / 0.274 | 0.503 / 0.276 | 0.503 / 0.274 |
| matched | 10000 | 0.288 / 0.312 | 0.293 / 0.313 | 0.288 / 0.312 | 0.289 / 0.310 |
| exact | 1000 | 0.535 / 0.279 | 0.590 / 0.277 | 0.537 / 0.279 | 0.590 / 0.276 |
| exact | 10000 | 0.312 / 0.302 | 0.432 / 0.307 | 0.313 / 0.302 | 0.430 / 0.305 |

Prior 2^-nodes (normalised at n = 6; labelled sensitivity, the primary prior is the length prior):

| arm | N | e | e (exact set) | mixing | self-play forfeit | constants | X | GN |
|---|---|---|---|---|---|---|---|---|
| pure | 100 | 0.335 | 0.341 | 0.000 | 0.842 | 0.090 | 0.000 | 0.000 |
| pure | 1000 | 0.070 | 0.077 | 0.000 | 0.976 | 0.012 | 0.000 | 0.000 |
| pure | 10000 | 0.008 | 0.016 | 0.000 | 0.997 | 0.001 | 0.000 | 0.000 |
| sample | 100 | 0.470 | 0.536 | 0.179 | 0.202 | 0.096 | 0.059 | 0.033 |
| sample | 1000 | 0.175 | 0.333 | 0.429 | 0.433 | 0.020 | 0.059 | 0.192 |
| sample | 10000 | 0.033 | 0.255 | 0.705 | 0.274 | 0.003 | 0.059 | 0.401 |
| matched | 100 | 0.482 | 0.558 | 0.198 | 0.179 | 0.120 | 0.072 | 0.030 |
| matched | 1000 | 0.174 | 0.374 | 0.452 | 0.394 | 0.027 | 0.072 | 0.163 |
| matched | 10000 | 0.030 | 0.297 | 0.678 | 0.300 | 0.004 | 0.072 | 0.325 |
| exact | 100 | 0.619 | 0.619 | 0.255 | 0.188 | 0.163 | 0.072 | 0.020 |
| exact | 1000 | 0.388 | 0.388 | 0.404 | 0.351 | 0.055 | 0.072 | 0.136 |
| exact | 10000 | 0.122 | 0.122 | 0.564 | 0.366 | 0.014 | 0.072 | 0.405 |

### n = 7 (blocked evaluation; classes by payoff rows over all 17,888 programs)

| arm | classes | N | e | e (exact set) | mixing | self-play forfeit | constants | X | states for 0.99 |
|---|---|---|---|---|---|---|---|---|---|
| pure | 24 | 100 | 0.337 | 0.408 | 0.000 | 0.822 | 0.123 | 0.000 | 13 |
| pure | 24 | 1000 | 0.069 | 0.156 | 0.000 | 0.974 | 0.016 | 0.000 | 10 |
| pure | 24 | 10000 | 0.008 | 0.098 | 0.000 | 0.997 | 0.002 | 0.000 | 5 |
| pure | 24 | 100000 | 0.001 | 0.091 | 0.000 | 1.000 | 0.000 | 0.000 | 3 |
| sample | 254 | 100 | 0.660 | 0.677 | 0.234 | 0.104 | 0.536 | 0.218 | 57 |
| sample | 254 | 1000 | 0.482 | 0.528 | 0.275 | 0.425 | 0.224 | 0.218 | 52 |
| sample | 254 | 10000 | 0.277 | 0.350 | 0.321 | 0.620 | 0.041 | 0.218 | 25 |
| sample | 254 | 100000 | 0.082 | 0.202 | 0.445 | 0.546 | 0.007 | 0.218 | 10 |
| matched | 254 | 100 | 0.673 | 0.687 | 0.238 | 0.091 | 0.566 | 0.225 | 44 |
| matched | 254 | 1000 | 0.495 | 0.540 | 0.277 | 0.400 | 0.252 | 0.225 | 41 |
| matched | 254 | 10000 | 0.272 | 0.347 | 0.323 | 0.611 | 0.049 | 0.225 | 23 |
| matched | 254 | 100000 | 0.073 | 0.187 | 0.414 | 0.576 | 0.007 | 0.225 | 10 |
| exact | 376 | 100 | 0.703 | 0.703 | 0.240 | 0.093 | 0.573 | 0.225 | 59 |
| exact | 376 | 1000 | 0.591 | 0.591 | 0.281 | 0.392 | 0.256 | 0.225 | 63 |
| exact | 376 | 10000 | 0.422 | 0.422 | 0.314 | 0.586 | 0.060 | 0.225 | 41 |
| exact | 376 | 100000 | 0.187 | 0.187 | 0.340 | 0.626 | 0.014 | 0.225 | 20 |

N -> infinity limit at n = 7 (unexploitable classes): pure: |Z0| = 5, prior mass 0.0261, mixing 0.00; sample: |Z0| = 4, prior mass 0.2180, mixing 1.00; matched: |Z0| = 4, prior mass 0.2250, mixing 1.00; exact: |Z0| = 3, prior mass 0.2249, mixing 1.00

## 3. The epsilon = 0 seed lottery, (N, I) = (100, 64), mN = 1, 40 runs, generation 2,000

Founders iid from the length prior (common random numbers across arms; exact and sample-matched paired spelling for spelling), complete island graph, w = 0.3. Run-clustered 95% intervals.

| arm | runs | in-pop. program exploitability | islands with e <= 0.05 | e (exact-grammar exploiters) | action exploitability | individual mixing | plays forfeited | resident regret | classes alive (1500-2000) | homozygosity (1500-2000) |
|---|---|---|---|---|---|---|---|---|---|---|
| pure | 40 | 0.37 [0.28, 0.47] | 0.52 [0.42, 0.61] | 0.47 [0.39, 0.56] | 1.00 [1.00, 1.00] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 0.37 [0.28, 0.47] | 1.86 [1.75, 1.96] | 0.79 [0.77, 0.82] |
| sample | 40 | 0.34 [0.22, 0.46] | 0.58 [0.44, 0.71] | 0.40 [0.28, 0.52] | 0.72 [0.63, 0.81] | 0.22 [0.14, 0.30] | 0.69 [0.58, 0.78] | 0.34 [0.22, 0.46] | 1.61 [1.48, 1.74] | 0.86 [0.83, 0.89] |
| matched | 40 | 0.49 [0.38, 0.61] | 0.36 [0.23, 0.49] | 0.54 [0.43, 0.65] | 0.67 [0.59, 0.75] | 0.25 [0.18, 0.32] | 0.59 [0.48, 0.69] | 0.49 [0.38, 0.61] | 1.70 [1.59, 1.81] | 0.83 [0.81, 0.86] |
| exact | 40 | 0.60 [0.48, 0.71] | 0.25 [0.13, 0.37] | 0.60 [0.48, 0.71] | 0.69 [0.60, 0.77] | 0.25 [0.18, 0.32] | 0.52 [0.40, 0.62] | 0.60 [0.48, 0.71] | 1.72 [1.57, 1.87] | 0.83 [0.80, 0.86] |
| exact_uniform | 40 | 0.60 [0.50, 0.70] | 0.17 [0.09, 0.27] | n/a | 0.11 [0.04, 0.21] | 0.87 [0.76, 0.96] | 0.00 [0.00, 0.00] | 0.60 [0.50, 0.70] | 1.75 [1.61, 1.90] | 0.82 [0.79, 0.86] |
| exact_br | 40 | 0.49 [0.39, 0.59] | 0.21 [0.14, 0.30] | n/a | 0.29 [0.19, 0.41] | 0.62 [0.49, 0.74] | 0.18 [0.10, 0.27] | 0.49 [0.39, 0.59] | 1.91 [1.78, 2.03] | 0.79 [0.76, 0.82] |
| constants | 40 | 0.82 [0.78, 0.87] | 0.00 [0.00, 0.00] | n/a | 0.82 [0.78, 0.87] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.82 [0.78, 0.87] | 1.91 [1.72, 2.08] | 0.81 [0.77, 0.85] |
| constx | 40 | 0.76 [0.72, 0.79] | 0.01 [0.00, 0.03] | n/a | 0.76 [0.72, 0.79] | 0.06 [0.03, 0.10] | 0.00 [0.00, 0.00] | 0.76 [0.72, 0.79] | 2.10 [1.94, 2.26] | 0.77 [0.73, 0.80] |

Named-class shares of the population at generation 2,000 (mean over islands, then runs):

| arm | constants | X | THEM(ME) | next(THEM(ME)) | cr(THEM(ME)) | guarded next | guarded cr | coin(R,P) |
|---|---|---|---|---|---|---|---|---|
| pure | 0.000 [0.000, 0.000] | n/a | 0.020 [0.001, 0.046] | 0.489 [0.403, 0.568] | n/a | n/a | n/a | n/a |
| sample | 0.025 [0.000, 0.075] | 0.130 [0.089, 0.175] | 0.004 [0.000, 0.011] | 0.417 [0.290, 0.546] | n/a | 0.031 [0.000, 0.086] | n/a | 0.022 [0.000, 0.066] |
| matched | 0.050 [0.000, 0.117] | 0.215 [0.156, 0.280] | 0.000 [0.000, 0.000] | 0.224 [0.124, 0.336] | n/a | 0.000 [0.000, 0.000] | n/a | 0.000 [0.000, 0.000] |
| exact | 0.132 [0.045, 0.234] | 0.191 [0.133, 0.255] | 0.000 [0.000, 0.000] | 0.157 [0.076, 0.250] | 0.091 [0.028, 0.169] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| exact_uniform | 0.060 [0.000, 0.134] | 0.180 [0.120, 0.242] | 0.000 [0.000, 0.000] | 0.124 [0.043, 0.222] | 0.143 [0.065, 0.231] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| exact_br | 0.073 [0.000, 0.150] | 0.302 [0.227, 0.383] | 0.003 [0.000, 0.008] | 0.096 [0.043, 0.156] | 0.109 [0.051, 0.180] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.010 [0.000, 0.030] |
| constants | 1.000 [1.000, 1.000] | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| constx | 0.939 [0.896, 0.972] | 0.061 [0.028, 0.104] | n/a | n/a | n/a | n/a | n/a | n/a |

Dominant class of the island at generation 2,000 (share of all islands over the 40 runs):

* **pure:** next(THEM(ME)) 0.50; next(THEM(THEM)) 0.41; THEM(THEM) 0.07; THEM(ME) 0.02
* **sample:** next(THEM(ME)) 0.43; next(THEM(THEM)) 0.27; X 0.12; next(THEM(^X)) 0.05; THEM(THEM) 0.04; next(coin(X,THEM(ME))) 0.03
* **matched:** next(THEM(THEM)) 0.42; next(THEM(ME)) 0.23; X 0.20; coin(P,X) 0.04; next(THEM(^X)) 0.03; R 0.03
* **exact:** cr(THEM(THEM)) 0.21; X 0.19; next(THEM(ME)) 0.16; next(THEM(THEM)) 0.09; cr(THEM(ME)) 0.09; P 0.06

Share of islands whose dominant class changed between generation 500 and 2,000 (transitions, rule 4): pure 0.49 [0.45, 0.53]; sample 0.39 [0.32, 0.46]; matched 0.45 [0.38, 0.51]; exact 0.45 [0.37, 0.52]

The three readings, by islands at generation 2,000 (fraction of islands, run-clustered):

| arm | (I) individuals mix and e <= 0.05 | individuals mix but exploitable | (M) no individual mixing, population marginal uniform | e <= 0.05 without mixing | monomorphic (homozygosity >= 0.99) | island forfeits >= 0.99 of plays |
|---|---|---|---|---|---|---|
| pure | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.52 [0.42, 0.61] | 0.26 [0.19, 0.34] | 1.00 [1.00, 1.00] |
| sample | 0.09 [0.03, 0.17] | 0.01 [0.00, 0.03] | 0.00 [0.00, 0.00] | 0.43 [0.30, 0.56] | 0.50 [0.40, 0.60] | 0.50 [0.38, 0.62] |
| matched | 0.08 [0.04, 0.15] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.23 [0.13, 0.34] | 0.39 [0.31, 0.48] | 0.36 [0.26, 0.47] |
| exact | 0.05 [0.03, 0.07] | 0.04 [0.00, 0.10] | 0.00 [0.00, 0.00] | 0.14 [0.07, 0.23] | 0.43 [0.32, 0.54] | 0.32 [0.21, 0.43] |
| exact_uniform | 0.17 [0.09, 0.27] | 0.68 [0.55, 0.80] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.42 [0.31, 0.53] | 0.00 [0.00, 0.00] |
| exact_br | 0.11 [0.07, 0.16] | 0.39 [0.27, 0.51] | 0.00 [0.00, 0.01] | 0.07 [0.02, 0.12] | 0.30 [0.21, 0.40] | 0.09 [0.03, 0.17] |

Pooled action frequencies over non-forfeit plays (R, P, S; mean over islands, then runs) and per-run asymmetry (max deviation of the run's island-pooled frequency from 1/3):

| arm | R | P | S | per-run asymmetry |
|---|---|---|---|---|
| pure | nan [nan, nan] | nan [nan, nan] | nan [nan, nan] | nan [nan, nan] |
| sample | 0.327 [0.300, 0.348] | 0.360 [0.333, 0.410] | 0.312 [0.281, 0.333] | 0.032 [0.000, 0.086] |
| matched | 0.331 [0.293, 0.377] | 0.328 [0.296, 0.358] | 0.340 [0.303, 0.387] | 0.065 [0.021, 0.119] |
| exact | 0.308 [0.254, 0.363] | 0.334 [0.274, 0.403] | 0.358 [0.293, 0.430] | 0.124 [0.049, 0.208] |
| exact_uniform | 0.341 [0.295, 0.399] | 0.306 [0.274, 0.333] | 0.352 [0.311, 0.400] | 0.073 [0.023, 0.138] |
| exact_br | 0.305 [0.274, 0.330] | 0.355 [0.308, 0.410] | 0.341 [0.301, 0.387] | 0.071 [0.022, 0.129] |

Paired differences exact minus sample-matched (founders paired spelling for spelling), run-clustered:

| statistic (exact - matched) | difference |
|---|---|
| e_prog | 0.106 [-0.057, 0.266] |
| share_e_le_0.05 | -0.110 [-0.286, 0.065] |
| mix_pop | -0.000 [-0.095, 0.092] |
| forfeit_plays | -0.072 [-0.198, 0.057] |

### Supplementary replicate: 200 further runs (independent founders), arms pure / sample / matched / exact

| arm | runs | e | islands with e <= 0.05 | e (exact set) | mixing | X share |
|---|---|---|---|---|---|---|
| pure | 200 | 0.367 [0.326, 0.407] | 0.519 [0.477, 0.561] | 0.481 [0.441, 0.521] | 0.000 [0.000, 0.000] | n/a |
| sample | 200 | 0.426 [0.372, 0.476] | 0.446 [0.390, 0.508] | 0.489 [0.438, 0.540] | 0.281 [0.244, 0.321] | 0.212 [0.185, 0.242] |
| matched | 200 | 0.437 [0.384, 0.492] | 0.449 [0.389, 0.509] | 0.520 [0.468, 0.573] | 0.251 [0.211, 0.293] | 0.171 [0.143, 0.200] |
| exact | 200 | 0.583 [0.537, 0.628] | 0.187 [0.144, 0.233] | 0.583 [0.537, 0.628] | 0.241 [0.206, 0.279] | 0.192 [0.165, 0.221] |

Paired exact - matched over 200 runs: e_prog 0.146 [0.073, 0.219]; share_e_le_0.05 -0.262 [-0.343, -0.181]; mix_pop -0.010 [-0.064, 0.046]

### Size cell (N, I) = (400, 16), 20 runs

| arm | runs | e | islands with e <= 0.05 | mixing | plays forfeited | classes alive | X share |
|---|---|---|---|---|---|---|---|
| pure | 20 | 0.31 [0.22, 0.42] | 0.56 [0.44, 0.68] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] | 1.87 [1.73, 2.01] | n/a |
| sample | 20 | 0.52 [0.34, 0.69] | 0.38 [0.20, 0.58] | 0.25 [0.13, 0.39] | 0.58 [0.42, 0.74] | 1.76 [1.52, 1.99] | 0.18 [0.09, 0.29] |
| matched | 20 | 0.39 [0.24, 0.55] | 0.50 [0.32, 0.67] | 0.22 [0.11, 0.35] | 0.70 [0.53, 0.84] | 1.90 [1.62, 2.20] | 0.16 [0.09, 0.25] |
| exact | 20 | 0.63 [0.49, 0.75] | 0.12 [0.03, 0.24] | 0.23 [0.14, 0.34] | 0.53 [0.36, 0.69] | 2.02 [1.80, 2.26] | 0.18 [0.11, 0.25] |
| exact_uniform | 20 | 0.50 [0.36, 0.65] | 0.23 [0.09, 0.39] | 0.92 [0.80, 1.00] | 0.00 [0.00, 0.00] | 2.00 [1.73, 2.30] | 0.23 [0.15, 0.32] |
| exact_br | 20 | 0.48 [0.36, 0.60] | 0.21 [0.10, 0.33] | 0.67 [0.50, 0.83] | 0.29 [0.14, 0.45] | 1.93 [1.68, 2.16] | 0.20 [0.11, 0.30] |
| constants | 20 | 0.65 [0.61, 0.71] | 0.00 [0.00, 0.01] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 2.60 [2.40, 2.73] | n/a |
| constx | 20 | 0.66 [0.61, 0.72] | 0.00 [0.00, 0.00] | 0.02 [0.01, 0.03] | 0.00 [0.00, 0.00] | 2.57 [2.32, 2.77] | 0.02 [0.01, 0.03] |

### Continuation of the first 10 primary runs to 10,000 generations

| arm | runs | g = 2,000: e / share e <= 0.05 / mixing | g = 5,000 | g = 10,000 |
|---|---|---|---|---|
| pure | 10 | 0.33 / 0.52 / 0.00 | 0.47 / 0.44 / 0.00 | 0.59 / 0.40 / 0.00 |
| sample | 10 | 0.46 / 0.42 / 0.14 | 0.39 / 0.51 / 0.26 | 0.43 / 0.45 / 0.23 |
| matched | 10 | 0.48 / 0.36 / 0.23 | 0.56 / 0.33 / 0.22 | 0.59 / 0.32 / 0.19 |
| exact | 10 | 0.51 / 0.28 / 0.27 | 0.54 / 0.30 / 0.19 | 0.51 / 0.36 / 0.16 |
| exact_uniform | 10 | 0.58 / 0.16 / 0.84 | 0.51 / 0.20 / 0.89 | 0.47 / 0.30 / 0.90 |
| exact_br | 10 | 0.43 / 0.22 / 0.58 | 0.43 / 0.27 / 0.61 | 0.46 / 0.33 / 0.62 |
| constants | 10 | 0.80 / 0.00 / 0.00 | 0.84 / 0.00 / 0.00 | 0.96 / 0.00 / 0.00 |
| constx | 10 | 0.68 / 0.00 / 0.04 | 0.79 / 0.01 / 0.05 | 0.93 / 0.00 / 0.00 |

Time course (exact arm, 40 runs; e / share of islands with e <= 0.05 / mixing / classes alive): g=100: 0.59 / 0.13 / 0.24 / 2.63; g=250: 0.56 / 0.21 / 0.24 / 2.11; g=500: 0.56 / 0.23 / 0.26 / 2.07; g=1000: 0.55 / 0.25 / 0.26 / 1.89; g=2000: 0.60 / 0.25 / 0.25 / 1.66

### n = 7 lottery (40 runs, generation 2,000)

| arm | runs | e | islands with e <= 0.05 | e (exact set) | mixing | plays forfeited |
|---|---|---|---|---|---|---|
| pure | 40 | 0.34 [0.26, 0.42] | 0.52 [0.42, 0.62] | 0.52 [0.44, 0.61] | 0.00 [0.00, 0.00] | 1.00 [1.00, 1.00] |
| sample | 40 | 0.40 [0.29, 0.53] | 0.49 [0.36, 0.63] | 0.44 [0.32, 0.56] | 0.24 [0.16, 0.31] | 0.63 [0.53, 0.74] |
| matched | 40 | 0.41 [0.30, 0.51] | 0.43 [0.30, 0.56] | 0.46 [0.36, 0.57] | 0.32 [0.24, 0.41] | 0.42 [0.31, 0.54] |
| exact | 40 | 0.52 [0.41, 0.62] | 0.23 [0.12, 0.35] | 0.52 [0.41, 0.62] | 0.27 [0.19, 0.35] | 0.49 [0.37, 0.60] |

## 4. The eleven-program toy chain (notes §1.4)

| D | N | u(TM, GN) | pi mass on {X, GN, GC} | top state | its pi |
|---|---|---|---|---|---|
| 11 | 100 | 0.0000 | 0.4470 | C:1.000 | 0.217 |
| 11 | 1000 | 0.0000 | 0.4610 | C:1.000 | 0.226 |
| 11 | 10000 | 0.0000 | 0.4624 | C:1.000 | 0.227 |
| 12 | 100 | -0.0078 | 0.4864 | C:1.000 | 0.201 |
| 12 | 1000 | -0.0078 | 0.8171 | GC:1.000 | 0.365 |
| 12 | 10000 | -0.0078 | 0.9882 | GC:1.000 | 0.450 |
| 13 | 100 | 0.0000 | 0.4470 | C:1.000 | 0.217 |
| 13 | 1000 | 0.0000 | 0.4610 | C:1.000 | 0.226 |
| 13 | 10000 | 0.0000 | 0.4624 | C:1.000 | 0.227 |
| 20 | 100 | -0.0005 | 0.4494 | C:1.000 | 0.216 |
| 20 | 1000 | -0.0005 | 0.4860 | C:1.000 | 0.215 |
| 20 | 10000 | -0.0005 | 0.7102 | GC:1.000 | 0.312 |

## 5. Verdicts (conventions of `predictions/2026-10-23-rps.md`)

| item | verdict | evidence |
|---|---|---|
| 1 statics | held | no program of the sample/matched/exact tables forfeits against X or earns != 0 against it (max 0.0e+00); cr(THEM(ME)) self-play forfeit mass 1.000000; next(THEM(ME)) earns +1 against all 141 / 648 / 1248 deterministic opponents (sample / matched / exact), 0 counterexamples, beats R, P, S |
| 2 symmetry | partial | payoff-tensor relabeling error max 1.4e-16; pi equivariance error max 1.9e-16 over 24 cells (both held to machine precision); pooled lottery action frequencies (40 runs) contain 1/3 in the arms ['matched', 'exact'], and exclude it narrowly for {'sample': ['freqS'], 'exact_uniform': ['freqP'], 'exact_br': ['freqR']} (15 intervals, one expected by chance); 200-run replicate (intervals contain 1/3): {'sample': (True, ['0.343 [0.321, 0.366]', '0.327 [0.309, 0.347]', '0.330 [0.312, 0.349]']), 'matched': (True, ['0.336 [0.313, 0.360]', '0.347 [0.323, 0.373]', '0.317 [0.296, 0.338]']), 'exact': (True, ['0.344 [0.315, 0.375]', '0.328 [0.302, 0.357]', '0.328 [0.299, 0.355]'])}; per-run asymmetry (max deviation of a run's pooled frequency from 1/3) exact 0.124 [0.049, 0.208], matched 0.065 [0.021, 0.119], sample 0.032 [0.000, 0.086] |
| 3 pure arm | held | N = 10^4: self-play forfeit share 0.997, constants 0.0020, mixing 0.000, e (own exploiters) 0.0117, e (exact-grammar exploiters) 0.0195. Counter (L) ladder: pi-weighted sign-flip fraction across D = 11, 12, 13, 20 is 0.0000 -> not shown; counter (N) neutral readers: 24 pairs of support readers have non-zero payoff (max |u| 1.00) -> not shown |
| 4 sample arm | failed | e (own exploiters) sample [0.666, 0.489, 0.291] vs exact [0.703, 0.59, 0.432] at N = 10^2, 10^3, 10^4: the sample arm is at most the exact arm at every N (the falsifier); e(10^4)/e(10^2) sample 0.44, exact 0.61. With the exploiter set fixed to the exact grammar: sample [0.675, 0.525, 0.354] (exact [0.703, 0.59, 0.432]). mixing at 10^4: sample 0.313, exact 0.307 Supplementary (not scored): N = 1e+06: sample e 0.0172 / mixing 0.756; exact e 0.0548 / mixing 0.530 | N = 1e+07: sample e 0.0021 / mixing 0.964; exact e 0.0100 / mixing 0.887 |
| 5 exact arm | failed | (5a) chain N = 10^4: e 0.432 (needs <= 0.05, falsifier > 0.15), mixing 0.307 (needs >= 0.8, falsifier < 0.5); (5b) lottery: islands with e <= 0.05 = 0.25 [0.13, 0.37] (needs >= 0.8, falsifier < 0.5), mean e 0.60 [0.48, 0.71]; (5c) exact - matched at 10^4: chain +0.139 (exact e 0.432, matched 0.293; exact-set control exact 0.432, matched 0.358), lottery paired 0.106 [-0.057, 0.266] (40 runs; 200-run replicate 0.146 [0.073, 0.219]) (needs < 0). Supplementary (not scored, the approach to the limit): N = 1e+06: exact e 0.0548 / mixing 0.530; matched e 0.0158 / mixing 0.659; sample e 0.0172 / mixing 0.756 | N = 1e+07: exact e 0.0100 / mixing 0.887; matched e 0.0022 / mixing 0.936; sample e 0.0021 / mixing 0.964 |
| 5 counter (gemini): X holds the mixing mass, matched control erases the difference | partial | X is 0.74 (exact) and 0.70 (sample) of the mixing mass at 10^4 (needs >= 0.5), pi(X) = prior mass 0.227 in every cell; |exact - matched| = 0.139 (needs <= 0.02): the matched control does not erase the difference, and its sign is that exact is MORE exploitable |
| 5 counter (gpt): mixing substantial in both, no robust sign for exact - matched | failed | mixing at 10^4: sample 0.313, exact 0.307 (needs >= 0.5 in both); exact - matched = {11: 0.023, 12: 0.139, 13: 0.025, 20: 0.141} across D in (11, 12, 13, 20) and {100: 0.024, 1000: 0.085, 10000: 0.139} across N in (10^2, 10^3, 10^4): sign never changes (always exact > matched) |
| 6 uniform default | held | exact-uniform: plays forfeited 0.0e+00; vs exact at 10^4: e 0.433 vs 0.432, mixing 0.906 vs 0.307 (d 0.599), top-3 pi mass 0.604 vs 0.596; self-play TV from uniform: exact-uniform 0.053, exact 0.652, pure 0.999; action exploitability 0.080 vs 0.679. The mixing change is by construction (readers that forfeit become uniform); exploitability is unchanged. Lottery: mixing 0.87 [0.76, 0.96] vs 0.25 [0.18, 0.32], e 0.60 [0.50, 0.70] vs 0.60 [0.48, 0.71] |
| RS statement (reading (I): individual mixers, unexploitable) | failed | chain N = 10^4: exploitability / mixing sample 0.291 / 0.313, matched 0.293 / 0.313, exact 0.432 / 0.307; lottery islands with e <= 0.05: sample 0.58 [0.44, 0.71], matched 0.36 [0.23, 0.49], exact 0.25 [0.13, 0.37]. Reading (W) is trivially true (pooled frequencies uniform); reading (M) island share 0.00 [0.00, 0.00] (population marginal uniform, individuals not mixing) Supplementary, the chain at larger N (not scored): N = 1e+06: sample e 0.0172 / mixing 0.756; matched e 0.0158 / mixing 0.659; exact e 0.0548 / mixing 0.530 | N = 1e+07: sample e 0.0021 / mixing 0.964; matched e 0.0022 / mixing 0.936; exact e 0.0100 / mixing 0.887 |

