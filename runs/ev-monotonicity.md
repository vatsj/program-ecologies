# EV-monotonicity and weight responsiveness in arm T (2026-11-08)

Predictions `predictions/2026-11-08-ev-monotonicity.md`. Object: arm T, `dollar3`, main dose, A_f charge P_fail = 0.1, natural start (symmetrized post-anneal law; 3 recomputed pools of 16,384 islands), mean-field ODE (time = migrant events per island) and finite worlds (I = 1,024, 20 worlds, 10^5 events per island; finite-I, finite-time). Payoff modifications in dollars before the A_f charge.

## Validation (c = 0, b = 0)

Pool-mean class-share trajectory vs the stored `ode.json` (max abs difference over the five class shares): 0: 0.00e+00, 1000: 6.66e-16, 10000: 3.33e-16, 100000: 1.11e-16, end: 1.24e-12.

Per-pool end shares vs stored: 1.85e-12, 7.21e-13, 2.60e-12.

V* trajectory (0, 10^3, 10^4, 10^5, end), mine: 0.522400, 0.873810, 0.998874, 0.999270, 1.000000; stored (0, 10, 10^2, 10^3, 10^4, 10^5 and end checkpoints): 0.522400, 0.536314, 0.621648, 0.873810, 0.998874, 0.999270.

Control worlds (I = 1,024, queue-69 seeds): final pair counts identical to the stored worlds: True (max abs diff 0).

## Mean field (pool mean of 3 natural-start trajectories)

| condition | t | V* | F0 (1/2,1/2,0) | F1 | F2 | status per pool |
|---|---|---|---|---|---|---|
| control c=0, b=0 | 1e3 | 0.873810 | 0.291270 | 0.291270 | 0.291270 |  |
| control c=0, b=0 | 1e4 | 0.998874 | 0.332958 | 0.332958 | 0.332958 |  |
| control c=0, b=0 | 1e5 | 0.999270 | 0.333090 | 0.333090 | 0.333090 |  |
| control c=0, b=0 | end (t = 7.5e+06, 5.6e+06, 7.5e+06) | 1.000000 | 0.333333 | 0.333333 | 0.333333 | converged, converged, converged |
| penalty c=0.05 | 1e3 | 0.907962 | 0.302654 | 0.302654 | 0.302654 |  |
| penalty c=0.05 | 1e4 | 0.999024 | 0.333008 | 0.333008 | 0.333008 |  |
| penalty c=0.05 | 1e5 | 0.999808 | 0.333269 | 0.333269 | 0.333269 |  |
| penalty c=0.05 | end (t = 1.8e+06, 1.3e+06, 1.8e+06) | 1.000000 | 0.333333 | 0.333333 | 0.333333 | converged, converged, converged |
| penalty c=0.1 | 1e3 | 0.935505 | 0.311835 | 0.311835 | 0.311835 |  |
| penalty c=0.1 | 1e4 | 0.999400 | 0.333133 | 0.333133 | 0.333133 |  |
| penalty c=0.1 | 1e5 | 0.999998 | 0.333333 | 0.333333 | 0.333333 |  |
| penalty c=0.1 | end (t = 4.2e+05, 4.2e+05, 4.2e+05) | 1.000000 | 0.333333 | 0.333333 | 0.333333 | converged, converged, converged |
| bonus b=0.08333 | 1e3 | 0.891435 | 0.732857 | 0.079301 | 0.079277 |  |
| bonus b=0.08333 | 1e4 | 0.004125 | 0.003593 | 0.000097 | 0.000435 |  |
| bonus b=0.08333 | 1e5 | 0.999249 | 0.999249 | 0.000000 | 0.000000 |  |
| bonus b=0.08333 | end (t = 7.5e+06, 7.5e+06, 1e+07) | 1.000000 | 1.000000 | 0.000000 | 0.000000 | converged, converged, converged |
| bonus b=0.1667 | 1e3 | 0.918993 | 0.858906 | 0.030051 | 0.030037 |  |
| bonus b=0.1667 | 1e4 | 0.998251 | 0.998249 | 0.000001 | 0.000001 |  |
| bonus b=0.1667 | 1e5 | 0.999214 | 0.999214 | 0.000000 | 0.000000 |  |
| bonus b=0.1667 | end (t = 1e+07, 7.5e+06, 1e+07) | 1.000000 | 1.000000 | 0.000000 | 0.000000 | converged, converged, converged |
| EXPLORATORY bonus b=0.04167 | 1e3 | 0.882660 | 0.557678 | 0.162507 | 0.162475 |  |
| EXPLORATORY bonus b=0.04167 | 1e4 | 0.000164 | 0.000004 | 0.000018 | 0.000142 |  |
| EXPLORATORY bonus b=0.04167 | 1e5 | 0.333086 | 0.333086 | 0.000000 | 0.000000 |  |
| EXPLORATORY bonus b=0.04167 | end (t = 1e+07, 5.1e+06, 1e+07) | 0.333333 | 0.333333 | 0.000000 | 0.000000 | converged, converged, converged |
| EXPLORATORY bonus b=0.125 | 1e3 | 0.904938 | 0.815789 | 0.044582 | 0.044567 |  |
| EXPLORATORY bonus b=0.125 | 1e4 | 0.998344 | 0.998342 | 0.000001 | 0.000001 |  |
| EXPLORATORY bonus b=0.125 | 1e5 | 0.999214 | 0.999214 | 0.000000 | 0.000000 |  |
| EXPLORATORY bonus b=0.125 | end (t = 1e+07, 7.5e+06, 1e+07) | 1.000000 | 1.000000 | 0.000000 | 0.000000 | converged, converged, converged |

## Finite worlds (I = 1,024, 20 worlds, to 10^5 events per island)

| condition | worlds >= 0.99 on fair pairs | single-pair worlds | consensus F0 / F1 / F2 | unequal consensus | all three pairs >= 0.05 | mean share F0 / F1 / F2 at 10^5 | mean V* at 10^5 | mean F0 share at 10^3 / 10^4 |
|---|---|---|---|---|---|---|---|---|
| control c=0, b=0 | 18/20 | 13 | 4 / 8 / 1 | 2 | 1 | 0.233 / 0.486 / 0.180 | 0.8993 | 0.299 / 0.324 |
| penalty c=0.05 | 20/20 | 15 | 5 / 5 / 5 | 0 | 2 | 0.333 / 0.348 / 0.319 | 0.9998 | 0.315 / 0.313 |
| penalty c=0.1 | 20/20 | 16 | 3 / 6 / 7 | 0 | 0 | 0.239 / 0.371 / 0.391 | 1.0000 | 0.329 / 0.277 |
| bonus b=0.08333 | 10/20 | 10 | 6 / 2 / 2 | 10 | 0 | 0.300 / 0.100 / 0.100 | 0.4994 | 0.733 / 0.300 |
| bonus b=0.1667 | 20/20 | 20 | 20 / 0 / 0 | 0 | 0 | 0.999 / 0.000 / 0.000 | 0.9993 | 0.856 / 0.996 |
| EXPLORATORY bonus b=0.04167 | 14/20 | 14 | 6 / 3 / 5 | 6 | 0 | 0.300 / 0.150 / 0.250 | 0.6993 | 0.563 / 0.172 |
| EXPLORATORY bonus b=0.125 | 19/20 | 19 | 19 / 0 / 0 | 1 | 0 | 0.949 / 0.000 / 0.000 | 0.9491 | 0.812 / 0.996 |

Mean-field minimum of V* after 100 events per island (pool: value at event time), the excursion of the bonus runs:

- control c=0, b=0: 0.6218 at 100; 0.6233 at 100; 0.6199 at 100
- penalty c=0.05: 0.6489 at 100; 0.6503 at 100; 0.6463 at 100
- penalty c=0.1: 0.6723 at 100; 0.6736 at 100; 0.6692 at 100
- bonus b=0.08333: 0.0042 at 1e+04; 0.0005 at 2e+04; 0.0027 at 2e+04
- bonus b=0.1667: 0.6513 at 100; 0.6528 at 100; 0.6489 at 100
- EXPLORATORY bonus b=0.04167: 0.0004 at 2e+04; 0.0000 at 5.12e+06; 0.0000 at 1e+07
- EXPLORATORY bonus b=0.125: 0.6445 at 100; 0.6459 at 100; 0.6421 at 100

Finite worlds, mean V* (share of islands on fair pairs) at 10^3 / 3e3 / 10^4 / 3e4 / 10^5 events per island:

- control c=0, b=0: 0.869 / 0.993 / 0.999 / 0.899 / 0.899
- penalty c=0.05: 0.906 / 0.995 / 0.999 / 0.999 / 1.000
- penalty c=0.1: 0.935 / 0.998 / 1.000 / 1.000 / 1.000
- bonus b=0.08333: 0.889 / 0.962 / 0.306 / 0.499 / 0.499
- bonus b=0.1667: 0.915 / 0.986 / 0.996 / 0.999 / 0.999
- EXPLORATORY bonus b=0.04167: 0.881 / 0.964 / 0.198 / 0.690 / 0.699
- EXPLORATORY bonus b=0.125: 0.903 / 0.985 / 0.996 / 0.949 / 0.949

Penalty single-pair worlds pooled over c: [8, 11, 12], chi-square p against uniform = 0.657470857760857.

