# Mixed actions in two-role games: the inspection game and Basic Endgame (run report, 2026-10-23)

Spec `specs/2026-10-23-two-role-mixed.md`; predictions `predictions/2026-10-23-two-role-mixed.md`; notes `notes/mixed2.md`; code `src/mixed2*.py`; rows `runs/mixed2/`. Chain = the ε → 0 diagnostic (pi over pairs of monomorphic role classes); lottery = the ε = 0 seed lottery at (N, I) = (100, 64), mN = 1, 40 runs, generation 2,000 (size cell (400, 16), 20 runs), run-clustered 95% bootstrap intervals (4,000 resamples). Payoffs in verdicts are game payoffs (gross of the price).

## Completeness

| cell | object | runs / Ns |
|---|---|---|
| insp blind c=0 | lottery 40 runs; size missing; chain | 100, 1000, 10000 |
| insp sample c=0 | lottery 40 runs; size missing; chain | 100, 1000, 10000 |
| insp sample c=0.01 | lottery 40 runs; size missing; chain | 100, 1000, 10000 |
| insp exact c=0 | lottery 40 runs; size 20 runs; chain | 100, 1000, 10000 |
| insp exact c=0.01 | lottery 40 runs; size 20 runs; chain | 1000, 10000 |
| insp matched c=0 | lottery 40 runs; size missing; chain | 100, 1000, 10000 |
| insp matched c=0.01 | lottery 40 runs; size missing; chain | 100, 1000, 10000 |
| insp sr4 c=0 | lottery 40 runs; size missing; chain | 100, 1000, 10000 |
| insp sr4 c=0.01 | lottery missing; size missing; chain | missing |
| insp sr16 c=0 | lottery 40 runs; size missing; chain | 100, 1000, 10000 |
| insp sr16 c=0.01 | lottery missing; size missing; chain | missing |
| end blind c=0 | lottery 40 runs; size missing; chain | 100, 1000, 10000 |
| end sample c=0 | lottery 40 runs; size missing; chain | missing |
| end sample c=0.01 | lottery 40 runs; size missing; chain | 100, 1000, 10000 |
| end exact c=0 | lottery 40 runs; size missing; chain | 100, 1000, 10000 |
| end exact c=0.01 | lottery 40 runs; size missing; chain | 100, 1000, 10000 |
| end matched c=0 | lottery 40 runs; size missing; chain | missing |
| end matched c=0.01 | lottery 40 runs; size missing; chain | 100, 1000, 10000 |

## Prediction 1 (statics)

- Inspection hand table (8 × 5, both payoffs): max |evaluator − hand| = 0.00e+00 over 80 entries.
- Endgame hand table (exact arm, 66 entries) max error 1.11e-16; the SRII column in the matched arm 1.67e-16. One erratum to the notes (EXP against the reader columns, notes §2): the evaluator was right, the hand entry (−3) was wrong; 473/2187 re-derived by hand.
- Minimax: EQ earns between -1.7e-16 and 0.0e+00 against every II program of the n = 7 table (713 programs); II's X earns at least 0.0e+00 against every I program (argmin BET); X gains 0.3333 against CHECK and 0.1667 against XI.
- Dyadic grid (blind inspection arm, n = 8): 17 distinct inspection probabilities; minimal sizes {'0.25': 3, '0.375': 5, '0.3125': 7, '0.5': 1}; the smallest above 1/4 is 5/16 (size 7).
- **Verdict: held.**

## Lottery tables

**insp exact, c = 0, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| inspector payoff (game) | -0.223 [-0.333, -0.127] | -0.225 |
| inspector payoff (net) | -0.223 [-0.336, -0.124] | -0.225 |
| inspectee payoff (game) | 0.037 [0.015, 0.063] | 0.037 |
| P(inspect) | 0.067 [0.024, 0.117] | 0.068 |
| P(cheat) | 0.040 [0.016, 0.067] | 0.040 |
| inspector mass p>1/4 | 0.114 [0.035, 0.210] | 0.117 |
| mass p=1/4 | 0.025 [0.000, 0.076] | 0.025 |
| mass p<1/4 | 0.860 [0.750, 0.950] | 0.857 |
| mass at 5/16 | 0.000 [0.000, 0.001] | 0.000 |
| mass at 3/8 | 0.025 [0.000, 0.075] | 0.027 |
| mass at 1/2 | 0.063 [0.011, 0.132] | 0.060 |
| inspectee readers | 0.193 [0.111, 0.284] | 0.192 |
|  exact readers | 0.193 [0.113, 0.284] | 0.192 |
|  sampling readers | 0.000 [0.000, 0.000] | 0.000 |
|  behavioural readers | 0.005 [0.000, 0.015] | 0.006 |
| inspector readers | 0.850 [0.746, 0.937] | 0.844 |
| class C share | 0.606 [0.485, 0.728] | 0.607 |
| class K share | 0.000 [0.000, 0.000] | 0.000 |
| inspectee X share | 0.000 [0.000, 0.000] | 0.000 |
| class N share | 0.027 [0.005, 0.058] | 0.031 |
| class I share | 0.000 [0.000, 0.000] | 0.000 |
| inspectees q<=0.02 | 0.797 [0.671, 0.916] | 0.797 |
| inspectees q>=0.98 | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| best inspector program payoff vs the inspectees (net) | -0.158 [-0.268, -0.065] | -0.159 |
| best inspectee program payoff vs the inspectors (net) | 0.853 [0.753, 0.939] | 0.855 |
| individual mixing (inspector) | 0.158 [0.065, 0.271] | 0.163 |
| individual mixing (inspectee) | 0.203 [0.083, 0.328] | 0.203 |
| homozygosity 0 | 0.939 [0.908, 0.967] | 0.937 |
| homozygosity 1 | 0.910 [0.875, 0.943] | 0.908 |
| support 0 | 1.189 [1.102, 1.289] | 1.197 |
| support 1 | 1.268 [1.172, 1.377] | 1.279 |
| bounded-cr disagreement (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| islands committed | 0.114 [0.034, 0.209] | 0.117 |
| islands committed+compliant | 0.109 [0.029, 0.205] | 0.112 |
| islands at (0,0) | 0.648 [0.502, 0.790] | 0.644 |
| islands near Nash | 0.004 [0.000, 0.013] | 0.004 |
| islands cheat prob > 1/2 | 0.000 [0.000, 0.000] | 0.000 |
| island inspector payoff q10 | -0.239 [-0.352, -0.137] | -0.247 |
| island inspector payoff median | -0.222 [-0.334, -0.125] | -0.225 |
| island inspector payoff q90 | -0.202 [-0.306, -0.106] | -0.200 |

**insp exact, c = 0.01, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| inspector payoff (game) | -0.207 [-0.320, -0.107] | -0.200 |
| inspector payoff (net) | -0.215 [-0.326, -0.116] | -0.208 |
| inspectee payoff (game) | 0.037 [0.016, 0.061] | 0.035 |
| P(inspect) | 0.029 [0.007, 0.056] | 0.029 |
| P(cheat) | 0.047 [0.021, 0.075] | 0.045 |
| inspector mass p>1/4 | 0.039 [0.002, 0.099] | 0.040 |
| mass p=1/4 | 0.050 [0.000, 0.125] | 0.050 |
| mass p<1/4 | 0.910 [0.823, 0.985] | 0.910 |
| mass at 5/16 | 0.000 [0.000, 0.000] | 0.000 |
| mass at 3/8 | 0.025 [0.000, 0.075] | 0.025 |
| mass at 1/2 | 0.010 [0.000, 0.022] | 0.009 |
| inspectee readers | 0.005 [0.000, 0.011] | 0.009 |
|  exact readers | 0.005 [0.000, 0.012] | 0.009 |
|  sampling readers | 0.000 [0.000, 0.000] | 0.000 |
|  behavioural readers | 0.000 [0.000, 0.000] | 0.000 |
| inspector readers | 0.793 [0.676, 0.893] | 0.810 |
| class C share | 0.765 [0.634, 0.886] | 0.770 |
| class K share | 0.000 [0.000, 0.000] | 0.000 |
| inspectee X share | 0.000 [0.000, 0.000] | 0.000 |
| class N share | 0.132 [0.052, 0.220] | 0.115 |
| class I share | 0.000 [0.000, 0.000] | 0.000 |
| inspectees q<=0.02 | 0.769 [0.635, 0.890] | 0.777 |
| inspectees q>=0.98 | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspector) | 0.008 [0.007, 0.009] | 0.008 |
| price paid (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| best inspector program payoff vs the inspectees (net) | -0.187 [-0.303, -0.085] | -0.178 |
| best inspectee program payoff vs the inspectors (net) | 0.829 [0.743, 0.896] | 0.826 |
| individual mixing (inspector) | 0.091 [0.017, 0.178] | 0.095 |
| individual mixing (inspectee) | 0.231 [0.110, 0.369] | 0.223 |
| homozygosity 0 | 0.913 [0.877, 0.945] | 0.907 |
| homozygosity 1 | 0.987 [0.971, 0.998] | 0.981 |
| support 0 | 1.261 [1.162, 1.363] | 1.279 |
| support 1 | 1.038 [1.007, 1.082] | 1.057 |
| bounded-cr disagreement (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| islands committed | 0.037 [0.002, 0.095] | 0.036 |
| islands committed+compliant | 0.025 [0.000, 0.075] | 0.025 |
| islands at (0,0) | 0.701 [0.552, 0.826] | 0.702 |
| islands near Nash | 0.021 [0.003, 0.045] | 0.018 |
| islands cheat prob > 1/2 | 0.000 [0.000, 0.000] | 0.000 |
| island inspector payoff q10 | -0.220 [-0.339, -0.110] | -0.223 |
| island inspector payoff median | -0.209 [-0.321, -0.103] | -0.204 |
| island inspector payoff q90 | -0.193 [-0.302, -0.100] | -0.169 |

**insp blind, c = 0, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| inspector payoff (game) | -0.981 [-1.050, -0.913] | -0.972 |
| inspector payoff (net) | -0.981 [-1.049, -0.915] | -0.972 |
| inspectee payoff (game) | 0.006 [-0.013, 0.029] | -0.001 |
| P(inspect) | 0.253 [0.229, 0.277] | 0.257 |
| P(cheat) | 0.241 [0.216, 0.265] | 0.238 |
| inspector mass p>1/4 | 0.482 [0.427, 0.535] | 0.490 |
| mass p=1/4 | 0.060 [0.014, 0.125] | 0.060 |
| mass p<1/4 | 0.458 [0.399, 0.516] | 0.450 |
| mass at 5/16 | 0.000 [0.000, 0.000] | 0.000 |
| mass at 3/8 | 0.044 [0.008, 0.089] | 0.046 |
| mass at 1/2 | 0.421 [0.361, 0.484] | 0.429 |
| inspectee readers | 0.000 [0.000, 0.000] | 0.000 |
|  exact readers | 0.000 [0.000, 0.000] | 0.000 |
|  sampling readers | 0.000 [0.000, 0.000] | 0.000 |
|  behavioural readers | 0.000 [0.000, 0.000] | 0.000 |
| inspector readers | 0.000 [0.000, 0.000] | 0.000 |
| class C share | 0.484 [0.422, 0.545] | 0.493 |
| class K share | 0.021 [0.005, 0.043] | 0.020 |
| inspectee X share | 0.350 [0.285, 0.415] | 0.359 |
| class N share | 0.457 [0.398, 0.515] | 0.448 |
| class I share | 0.000 [0.000, 0.000] | 0.000 |
| inspectees q<=0.02 | 0.484 [0.423, 0.547] | 0.493 |
| inspectees q>=0.98 | 0.021 [0.005, 0.042] | 0.020 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| best inspector program payoff vs the inspectees (net) | -0.661 [-0.716, -0.601] | -0.651 |
| best inspectee program payoff vs the inspectors (net) | 0.312 [0.261, 0.368] | 0.302 |
| individual mixing (inspector) | 0.543 [0.484, 0.599] | 0.552 |
| individual mixing (inspectee) | 0.495 [0.432, 0.557] | 0.487 |
| homozygosity 0 | 0.765 [0.742, 0.792] | 0.757 |
| homozygosity 1 | 0.760 [0.739, 0.782] | 0.756 |
| support 0 | 1.727 [1.639, 1.802] | 1.749 |
| support 1 | 1.733 [1.657, 1.805] | 1.752 |
| bounded-cr disagreement (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| islands committed | 0.493 [0.434, 0.550] | 0.500 |
| islands committed+compliant | 0.163 [0.120, 0.221] | 0.165 |
| islands at (0,0) | 0.022 [0.014, 0.033] | 0.023 |
| islands near Nash | 0.089 [0.073, 0.105] | 0.080 |
| islands cheat prob > 1/2 | 0.029 [0.009, 0.051] | 0.027 |
| island inspector payoff q10 | -1.659 [-1.779, -1.539] | -1.631 |
| island inspector payoff median | -0.947 [-1.033, -0.862] | -0.949 |
| island inspector payoff q90 | -0.358 [-0.429, -0.295] | -0.339 |

**insp matched, c = 0, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| inspector payoff (game) | -0.566 [-0.694, -0.435] | -0.575 |
| inspector payoff (net) | -0.566 [-0.695, -0.430] | -0.575 |
| inspectee payoff (game) | 0.059 [0.035, 0.086] | 0.056 |
| P(inspect) | 0.111 [0.076, 0.148] | 0.116 |
| P(cheat) | 0.132 [0.097, 0.166] | 0.135 |
| inspector mass p>1/4 | 0.086 [0.025, 0.162] | 0.091 |
| mass p=1/4 | 0.209 [0.116, 0.316] | 0.212 |
| mass p<1/4 | 0.704 [0.593, 0.811] | 0.695 |
| mass at 5/16 | 0.000 [0.000, 0.000] | 0.001 |
| mass at 3/8 | 0.016 [0.000, 0.048] | 0.017 |
| mass at 1/2 | 0.046 [0.002, 0.110] | 0.048 |
| inspectee readers | 0.085 [0.026, 0.155] | 0.085 |
|  exact readers | 0.000 [0.000, 0.000] | 0.000 |
|  sampling readers | 0.085 [0.028, 0.162] | 0.085 |
|  behavioural readers | 0.005 [0.000, 0.015] | 0.006 |
| inspector readers | 0.653 [0.519, 0.782] | 0.664 |
| class C share | 0.373 [0.247, 0.508] | 0.370 |
| class K share | 0.000 [0.000, 0.000] | 0.000 |
| inspectee X share | 0.022 [0.000, 0.057] | 0.025 |
| class N share | 0.304 [0.192, 0.426] | 0.291 |
| class I share | 0.000 [0.000, 0.000] | 0.000 |
| inspectees q<=0.02 | 0.452 [0.311, 0.597] | 0.446 |
| inspectees q>=0.98 | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| best inspector program payoff vs the inspectees (net) | -0.523 [-0.657, -0.386] | -0.531 |
| best inspectee program payoff vs the inspectors (net) | 0.550 [0.436, 0.666] | 0.534 |
| individual mixing (inspector) | 0.407 [0.289, 0.525] | 0.421 |
| individual mixing (inspectee) | 0.548 [0.403, 0.692] | 0.554 |
| homozygosity 0 | 0.889 [0.854, 0.922] | 0.884 |
| homozygosity 1 | 0.944 [0.911, 0.973] | 0.939 |
| support 0 | 1.338 [1.236, 1.442] | 1.355 |
| support 1 | 1.168 [1.082, 1.260] | 1.183 |
| bounded-cr disagreement (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| islands committed | 0.084 [0.025, 0.157] | 0.092 |
| islands committed+compliant | 0.059 [0.014, 0.122] | 0.061 |
| islands at (0,0) | 0.321 [0.190, 0.460] | 0.319 |
| islands near Nash | 0.231 [0.133, 0.338] | 0.246 |
| islands cheat prob > 1/2 | 0.000 [0.000, 0.000] | 0.000 |
| island inspector payoff q10 | -0.668 [-0.814, -0.521] | -0.673 |
| island inspector payoff median | -0.549 [-0.681, -0.409] | -0.567 |
| island inspector payoff q90 | -0.484 [-0.628, -0.338] | -0.489 |

**insp sr16, c = 0, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| inspector payoff (game) | -0.279 [-0.354, -0.209] | -0.278 |
| inspector payoff (net) | -0.279 [-0.355, -0.207] | -0.278 |
| inspectee payoff (game) | 0.032 [0.017, 0.050] | 0.035 |
| P(inspect) | 0.120 [0.063, 0.183] | 0.117 |
| P(cheat) | 0.042 [0.027, 0.061] | 0.042 |
| inspector mass p>1/4 | 0.203 [0.090, 0.328] | 0.197 |
| mass p=1/4 | 0.025 [0.000, 0.075] | 0.025 |
| mass p<1/4 | 0.772 [0.644, 0.895] | 0.777 |
| mass at 5/16 | 0.000 [0.000, 0.000] | 0.000 |
| mass at 3/8 | 0.000 [0.000, 0.000] | 0.000 |
| mass at 1/2 | 0.178 [0.071, 0.298] | 0.178 |
| inspectee readers | 0.041 [0.005, 0.098] | 0.039 |
|  exact readers | 0.000 [0.000, 0.000] | 0.000 |
|  sampling readers | 0.612 [0.463, 0.745] | 0.598 |
|  behavioural readers | 0.003 [0.000, 0.009] | 0.003 |
| inspector readers | 0.726 [0.591, 0.853] | 0.719 |
| class C share | 0.238 [0.119, 0.365] | 0.250 |
| class K share | 0.000 [0.000, 0.000] | 0.000 |
| inspectee X share | 0.000 [0.000, 0.000] | 0.000 |
| class N share | 0.073 [0.013, 0.151] | 0.079 |
| class I share | 0.000 [0.000, 0.000] | 0.000 |
| inspectees q<=0.02 | 0.254 [0.133, 0.388] | 0.267 |
| inspectees q>=0.98 | 0.000 [0.000, 0.000] | 0.001 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| best inspector program payoff vs the inspectees (net) | -0.165 [-0.241, -0.102] | -0.164 |
| best inspectee program payoff vs the inspectors (net) | 0.287 [0.180, 0.410] | 0.295 |
| individual mixing (inspector) | 0.362 [0.224, 0.513] | 0.359 |
| individual mixing (inspectee) | 0.746 [0.613, 0.871] | 0.732 |
| homozygosity 0 | 0.956 [0.926, 0.982] | 0.954 |
| homozygosity 1 | 0.978 [0.957, 0.996] | 0.971 |
| support 0 | 1.131 [1.054, 1.225] | 1.142 |
| support 1 | 1.070 [1.013, 1.144] | 1.091 |
| bounded-cr disagreement (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| islands committed | 0.204 [0.085, 0.329] | 0.197 |
| islands committed+compliant | 0.196 [0.083, 0.324] | 0.193 |
| islands at (0,0) | 0.023 [0.000, 0.061] | 0.036 |
| islands near Nash | 0.000 [0.000, 0.000] | 0.001 |
| islands cheat prob > 1/2 | 0.000 [0.000, 0.000] | 0.001 |
| island inspector payoff q10 | -0.300 [-0.385, -0.224] | -0.310 |
| island inspector payoff median | -0.274 [-0.347, -0.204] | -0.271 |
| island inspector payoff q90 | -0.269 [-0.341, -0.200] | -0.259 |

**insp sr4, c = 0, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| inspector payoff (game) | -0.389 [-0.527, -0.265] | -0.379 |
| inspector payoff (net) | -0.389 [-0.524, -0.265] | -0.379 |
| inspectee payoff (game) | 0.067 [0.036, 0.102] | 0.066 |
| P(inspect) | 0.067 [0.039, 0.097] | 0.067 |
| P(cheat) | 0.085 [0.053, 0.121] | 0.082 |
| inspector mass p>1/4 | 0.025 [0.000, 0.059] | 0.030 |
| mass p=1/4 | 0.151 [0.051, 0.275] | 0.149 |
| mass p<1/4 | 0.824 [0.704, 0.929] | 0.821 |
| mass at 5/16 | 0.000 [0.000, 0.000] | 0.000 |
| mass at 3/8 | 0.000 [0.000, 0.000] | 0.000 |
| mass at 1/2 | 0.011 [0.000, 0.028] | 0.015 |
| inspectee readers | 0.164 [0.075, 0.262] | 0.164 |
|  exact readers | 0.000 [0.000, 0.000] | 0.000 |
|  sampling readers | 0.544 [0.408, 0.681] | 0.528 |
|  behavioural readers | 0.006 [0.000, 0.019] | 0.006 |
| inspector readers | 0.493 [0.343, 0.643] | 0.491 |
| class C share | 0.366 [0.240, 0.502] | 0.386 |
| class K share | 0.000 [0.000, 0.000] | 0.000 |
| inspectee X share | 0.015 [0.000, 0.044] | 0.010 |
| class N share | 0.336 [0.197, 0.475] | 0.336 |
| class I share | 0.000 [0.000, 0.000] | 0.000 |
| inspectees q<=0.02 | 0.500 [0.352, 0.644] | 0.515 |
| inspectees q>=0.98 | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| best inspector program payoff vs the inspectees (net) | -0.286 [-0.401, -0.183] | -0.277 |
| best inspectee program payoff vs the inspectors (net) | 0.471 [0.334, 0.607] | 0.466 |
| individual mixing (inspector) | 0.408 [0.268, 0.548] | 0.391 |
| individual mixing (inspectee) | 0.500 [0.351, 0.645] | 0.485 |
| homozygosity 0 | 0.962 [0.935, 0.986] | 0.959 |
| homozygosity 1 | 0.925 [0.894, 0.954] | 0.913 |
| support 0 | 1.118 [1.039, 1.202] | 1.128 |
| support 1 | 1.230 [1.138, 1.330] | 1.270 |
| bounded-cr disagreement (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| islands committed | 0.023 [0.000, 0.051] | 0.033 |
| islands committed+compliant | 0.008 [0.000, 0.021] | 0.018 |
| islands at (0,0) | 0.265 [0.148, 0.389] | 0.281 |
| islands near Nash | 0.007 [0.002, 0.014] | 0.009 |
| islands cheat prob > 1/2 | 0.000 [0.000, 0.001] | 0.000 |
| island inspector payoff q10 | -0.447 [-0.598, -0.311] | -0.445 |
| island inspector payoff median | -0.378 [-0.517, -0.255] | -0.365 |
| island inspector payoff q90 | -0.346 [-0.486, -0.227] | -0.330 |

**insp sample, c = 0, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| inspector payoff (game) | -0.641 [-0.783, -0.507] | -0.627 |
| inspector payoff (net) | -0.641 [-0.777, -0.499] | -0.627 |
| inspectee payoff (game) | 0.053 [0.028, 0.085] | 0.050 |
| P(inspect) | 0.164 [0.105, 0.231] | 0.159 |
| P(cheat) | 0.141 [0.106, 0.178] | 0.139 |
| inspector mass p>1/4 | 0.089 [0.024, 0.171] | 0.092 |
| mass p=1/4 | 0.197 [0.113, 0.291] | 0.203 |
| mass p<1/4 | 0.711 [0.593, 0.819] | 0.701 |
| mass at 5/16 | 0.000 [0.000, 0.000] | 0.000 |
| mass at 3/8 | 0.000 [0.000, 0.000] | 0.000 |
| mass at 1/2 | 0.019 [0.000, 0.046] | 0.034 |
| inspectee readers | 0.173 [0.079, 0.282] | 0.167 |
|  exact readers | 0.000 [0.000, 0.000] | 0.000 |
|  sampling readers | 0.173 [0.078, 0.280] | 0.167 |
|  behavioural readers | 0.062 [0.015, 0.120] | 0.058 |
| inspector readers | 0.772 [0.665, 0.869] | 0.778 |
| class C share | 0.321 [0.199, 0.449] | 0.336 |
| class K share | 0.000 [0.000, 0.000] | 0.000 |
| inspectee X share | 0.000 [0.000, 0.000] | 0.000 |
| class N share | 0.138 [0.065, 0.221] | 0.126 |
| class I share | 0.045 [0.000, 0.108] | 0.032 |
| inspectees q<=0.02 | 0.392 [0.258, 0.527] | 0.402 |
| inspectees q>=0.98 | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspector) | 0.000 [0.000, 0.001] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.001] | 0.000 |
| price paid (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| best inspector program payoff vs the inspectees (net) | -0.564 [-0.684, -0.446] | -0.550 |
| best inspectee program payoff vs the inspectors (net) | 0.271 [0.183, 0.371] | 0.258 |
| individual mixing (inspector) | 0.565 [0.434, 0.693] | 0.583 |
| individual mixing (inspectee) | 0.608 [0.473, 0.739] | 0.598 |
| homozygosity 0 | 0.892 [0.858, 0.925] | 0.896 |
| homozygosity 1 | 0.941 [0.911, 0.968] | 0.940 |
| support 0 | 1.329 [1.225, 1.434] | 1.316 |
| support 1 | 1.170 [1.093, 1.255] | 1.178 |
| bounded-cr disagreement (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| islands committed | 0.112 [0.032, 0.205] | 0.106 |
| islands committed+compliant | 0.078 [0.013, 0.159] | 0.073 |
| islands at (0,0) | 0.260 [0.135, 0.395] | 0.260 |
| islands near Nash | 0.242 [0.149, 0.344] | 0.246 |
| islands cheat prob > 1/2 | 0.000 [0.000, 0.000] | 0.001 |
| island inspector payoff q10 | -0.723 [-0.865, -0.584] | -0.720 |
| island inspector payoff median | -0.654 [-0.798, -0.509] | -0.630 |
| island inspector payoff q90 | -0.540 [-0.693, -0.393] | -0.531 |

**insp sample, c = 0.01, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| inspector payoff (game) | -0.679 [-0.825, -0.532] | -0.684 |
| inspector payoff (net) | -0.684 [-0.835, -0.542] | -0.688 |
| inspectee payoff (game) | 0.068 [0.016, 0.115] | 0.062 |
| P(inspect) | 0.128 [0.072, 0.196] | 0.135 |
| P(cheat) | 0.161 [0.121, 0.201] | 0.162 |
| inspector mass p>1/4 | 0.142 [0.058, 0.246] | 0.150 |
| mass p=1/4 | 0.105 [0.045, 0.177] | 0.122 |
| mass p<1/4 | 0.752 [0.646, 0.847] | 0.727 |
| mass at 5/16 | 0.000 [0.000, 0.000] | 0.000 |
| mass at 3/8 | 0.005 [0.000, 0.015] | 0.006 |
| mass at 1/2 | 0.105 [0.037, 0.190] | 0.115 |
| inspectee readers | 0.133 [0.046, 0.231] | 0.127 |
|  exact readers | 0.000 [0.000, 0.000] | 0.000 |
|  sampling readers | 0.133 [0.046, 0.232] | 0.127 |
|  behavioural readers | 0.033 [0.001, 0.074] | 0.032 |
| inspector readers | 0.369 [0.250, 0.495] | 0.396 |
| class C share | 0.340 [0.214, 0.478] | 0.344 |
| class K share | 0.000 [0.000, 0.000] | 0.000 |
| inspectee X share | 0.038 [0.000, 0.100] | 0.041 |
| class N share | 0.489 [0.367, 0.608] | 0.453 |
| class I share | 0.033 [0.000, 0.089] | 0.030 |
| inspectees q<=0.02 | 0.368 [0.231, 0.510] | 0.370 |
| inspectees q>=0.98 | 0.000 [0.000, 0.001] | 0.000 |
| forfeit (inspector) | 0.000 [0.000, 0.001] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.001] | 0.000 |
| price paid (inspector) | 0.005 [0.003, 0.007] | 0.005 |
| price paid (inspectee) | 0.002 [0.001, 0.003] | 0.002 |
| best inspector program payoff vs the inspectees (net) | -0.572 [-0.696, -0.440] | -0.575 |
| best inspectee program payoff vs the inspectors (net) | 0.537 [0.427, 0.650] | 0.503 |
| individual mixing (inspector) | 0.333 [0.222, 0.456] | 0.364 |
| individual mixing (inspectee) | 0.632 [0.493, 0.764] | 0.630 |
| homozygosity 0 | 0.883 [0.849, 0.918] | 0.873 |
| homozygosity 1 | 0.960 [0.934, 0.983] | 0.954 |
| support 0 | 1.368 [1.259, 1.481] | 1.393 |
| support 1 | 1.114 [1.046, 1.189] | 1.137 |
| bounded-cr disagreement (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| islands committed | 0.142 [0.052, 0.241] | 0.152 |
| islands committed+compliant | 0.055 [0.009, 0.120] | 0.054 |
| islands at (0,0) | 0.247 [0.127, 0.385] | 0.245 |
| islands near Nash | 0.111 [0.053, 0.185] | 0.123 |
| islands cheat prob > 1/2 | 0.000 [0.000, 0.000] | 0.001 |
| island inspector payoff q10 | -0.769 [-0.923, -0.618] | -0.776 |
| island inspector payoff median | -0.673 [-0.823, -0.527] | -0.679 |
| island inspector payoff q90 | -0.600 [-0.761, -0.446] | -0.593 |

**insp matched, c = 0.01, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| inspector payoff (game) | -0.688 [-0.918, -0.502] | -0.699 |
| inspector payoff (net) | -0.692 [-0.924, -0.510] | -0.704 |
| inspectee payoff (game) | 0.103 [0.057, 0.163] | 0.099 |
| P(inspect) | 0.089 [0.055, 0.128] | 0.093 |
| P(cheat) | 0.165 [0.117, 0.221] | 0.169 |
| inspector mass p>1/4 | 0.085 [0.023, 0.160] | 0.086 |
| mass p=1/4 | 0.131 [0.065, 0.206] | 0.142 |
| mass p<1/4 | 0.784 [0.685, 0.874] | 0.772 |
| mass at 5/16 | 0.000 [0.000, 0.000] | 0.000 |
| mass at 3/8 | 0.007 [0.000, 0.020] | 0.008 |
| mass at 1/2 | 0.078 [0.018, 0.151] | 0.078 |
| inspectee readers | 0.046 [0.004, 0.109] | 0.054 |
|  exact readers | 0.000 [0.000, 0.000] | 0.000 |
|  sampling readers | 0.046 [0.004, 0.107] | 0.054 |
|  behavioural readers | 0.011 [0.000, 0.030] | 0.014 |
| inspector readers | 0.478 [0.333, 0.617] | 0.494 |
| class C share | 0.402 [0.274, 0.540] | 0.392 |
| class K share | 0.003 [0.000, 0.009] | 0.007 |
| inspectee X share | 0.022 [0.000, 0.054] | 0.018 |
| class N share | 0.439 [0.311, 0.567] | 0.423 |
| class I share | 0.000 [0.000, 0.000] | 0.000 |
| inspectees q<=0.02 | 0.406 [0.269, 0.552] | 0.402 |
| inspectees q>=0.98 | 0.028 [0.000, 0.081] | 0.032 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspector) | 0.005 [0.003, 0.006] | 0.005 |
| price paid (inspectee) | 0.000 [0.000, 0.001] | 0.001 |
| best inspector program payoff vs the inspectees (net) | -0.545 [-0.679, -0.412] | -0.548 |
| best inspectee program payoff vs the inspectors (net) | 0.643 [0.528, 0.755] | 0.629 |
| individual mixing (inspector) | 0.326 [0.220, 0.440] | 0.343 |
| individual mixing (inspectee) | 0.566 [0.428, 0.703] | 0.565 |
| homozygosity 0 | 0.900 [0.860, 0.935] | 0.897 |
| homozygosity 1 | 0.951 [0.919, 0.978] | 0.945 |
| support 0 | 1.309 [1.195, 1.429] | 1.325 |
| support 1 | 1.150 [1.065, 1.246] | 1.168 |
| bounded-cr disagreement (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| islands committed | 0.091 [0.026, 0.171] | 0.091 |
| islands committed+compliant | 0.055 [0.010, 0.117] | 0.053 |
| islands at (0,0) | 0.291 [0.163, 0.425] | 0.283 |
| islands near Nash | 0.165 [0.088, 0.252] | 0.175 |
| islands cheat prob > 1/2 | 0.027 [0.000, 0.080] | 0.032 |
| island inspector payoff q10 | -0.803 [-1.039, -0.603] | -0.831 |
| island inspector payoff median | -0.666 [-0.890, -0.482] | -0.678 |
| island inspector payoff q90 | -0.607 [-0.845, -0.413] | -0.603 |

**insp exact, c = 0, size (20 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| inspector payoff (game) | -0.310 [-0.427, -0.194] | -0.306 |
| inspector payoff (net) | -0.310 [-0.427, -0.194] | -0.306 |
| inspectee payoff (game) | 0.013 [-0.000, 0.036] | 0.014 |
| P(inspect) | 0.241 [0.140, 0.342] | 0.240 |
| P(cheat) | 0.019 [0.000, 0.046] | 0.017 |
| inspector mass p>1/4 | 0.508 [0.284, 0.717] | 0.504 |
| mass p=1/4 | 0.000 [0.000, 0.000] | 0.000 |
| mass p<1/4 | 0.492 [0.289, 0.700] | 0.496 |
| mass at 5/16 | 0.000 [0.000, 0.000] | 0.000 |
| mass at 3/8 | 0.100 [0.000, 0.250] | 0.100 |
| mass at 1/2 | 0.403 [0.200, 0.607] | 0.399 |
| inspectee readers | 0.371 [0.233, 0.510] | 0.371 |
|  exact readers | 0.371 [0.237, 0.514] | 0.371 |
|  sampling readers | 0.000 [0.000, 0.000] | 0.000 |
|  behavioural readers | 0.000 [0.000, 0.000] | 0.000 |
| inspector readers | 0.460 [0.254, 0.674] | 0.453 |
| class C share | 0.542 [0.396, 0.684] | 0.548 |
| class K share | 0.000 [0.000, 0.000] | 0.000 |
| inspectee X share | 0.000 [0.000, 0.000] | 0.000 |
| class N share | 0.046 [0.000, 0.123] | 0.050 |
| class I share | 0.000 [0.000, 0.000] | 0.000 |
| inspectees q<=0.02 | 0.913 [0.777, 1.000] | 0.919 |
| inspectees q>=0.98 | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.001] | 0.000 |
| price paid (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| best inspector program payoff vs the inspectees (net) | -0.084 [-0.194, -0.002] | -0.079 |
| best inspectee program payoff vs the inspectors (net) | 0.506 [0.300, 0.750] | 0.503 |
| individual mixing (inspector) | 0.517 [0.317, 0.734] | 0.509 |
| individual mixing (inspectee) | 0.087 [0.000, 0.223] | 0.081 |
| homozygosity 0 | 0.970 [0.926, 1.000] | 0.973 |
| homozygosity 1 | 0.856 [0.808, 0.905] | 0.854 |
| support 0 | 1.087 [1.000, 1.209] | 1.084 |
| support 1 | 1.441 [1.284, 1.594] | 1.447 |
| bounded-cr disagreement (inspectee) | 0.016 [0.000, 0.049] | 0.019 |
| islands committed | 0.506 [0.300, 0.716] | 0.501 |
| islands committed+compliant | 0.497 [0.297, 0.700] | 0.499 |
| islands at (0,0) | 0.406 [0.200, 0.606] | 0.413 |
| islands near Nash | 0.009 [0.000, 0.028] | 0.004 |
| islands cheat prob > 1/2 | 0.000 [0.000, 0.000] | 0.000 |
| island inspector payoff q10 | -0.325 [-0.456, -0.195] | -0.325 |
| island inspector payoff median | -0.325 [-0.456, -0.200] | -0.319 |
| island inspector payoff q90 | -0.275 [-0.388, -0.168] | -0.276 |

**insp exact, c = 0.01, size (20 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| inspector payoff (game) | -0.376 [-0.792, -0.119] | -0.351 |
| inspector payoff (net) | -0.382 [-0.794, -0.121] | -0.357 |
| inspectee payoff (game) | 0.062 [0.000, 0.165] | 0.054 |
| P(inspect) | 0.127 [0.047, 0.217] | 0.127 |
| P(cheat) | 0.062 [0.000, 0.163] | 0.056 |
| inspector mass p>1/4 | 0.303 [0.107, 0.503] | 0.304 |
| mass p=1/4 | 0.000 [0.000, 0.000] | 0.000 |
| mass p<1/4 | 0.697 [0.493, 0.897] | 0.696 |
| mass at 5/16 | 0.100 [0.000, 0.250] | 0.100 |
| mass at 3/8 | 0.050 [0.000, 0.150] | 0.050 |
| mass at 1/2 | 0.153 [0.006, 0.310] | 0.154 |
| inspectee readers | 0.093 [0.016, 0.203] | 0.108 |
|  exact readers | 0.093 [0.016, 0.208] | 0.108 |
|  sampling readers | 0.000 [0.000, 0.000] | 0.000 |
|  behavioural readers | 0.007 [0.000, 0.017] | 0.018 |
| inspector readers | 0.606 [0.400, 0.809] | 0.617 |
| class C share | 0.810 [0.642, 0.950] | 0.795 |
| class K share | 0.000 [0.000, 0.000] | 0.000 |
| inspectee X share | 0.000 [0.000, 0.000] | 0.000 |
| class N share | 0.091 [0.000, 0.232] | 0.079 |
| class I share | 0.000 [0.000, 0.000] | 0.000 |
| inspectees q<=0.02 | 0.856 [0.706, 1.000] | 0.862 |
| inspectees q>=0.98 | 0.047 [0.000, 0.142] | 0.041 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspector) | 0.006 [0.004, 0.008] | 0.006 |
| price paid (inspectee) | 0.001 [0.000, 0.002] | 0.001 |
| best inspector program payoff vs the inspectees (net) | -0.066 [-0.159, -0.004] | -0.067 |
| best inspectee program payoff vs the inspectors (net) | 0.629 [0.442, 0.800] | 0.621 |
| individual mixing (inspector) | 0.303 [0.103, 0.503] | 0.305 |
| individual mixing (inspectee) | 0.097 [0.000, 0.241] | 0.097 |
| homozygosity 0 | 0.978 [0.957, 0.999] | 0.966 |
| homozygosity 1 | 0.965 [0.931, 0.994] | 0.952 |
| support 0 | 1.062 [1.003, 1.131] | 1.098 |
| support 1 | 1.109 [1.019, 1.219] | 1.139 |
| bounded-cr disagreement (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| islands committed | 0.303 [0.106, 0.503] | 0.304 |
| islands committed+compliant | 0.303 [0.103, 0.503] | 0.304 |
| islands at (0,0) | 0.550 [0.350, 0.750] | 0.556 |
| islands near Nash | 0.000 [0.000, 0.000] | 0.000 |
| islands cheat prob > 1/2 | 0.047 [0.000, 0.141] | 0.041 |
| island inspector payoff q10 | -0.388 [-0.803, -0.116] | -0.388 |
| island inspector payoff median | -0.388 [-0.825, -0.122] | -0.387 |
| island inspector payoff q90 | -0.387 [-0.802, -0.119] | -0.214 |

**insp exact_ee, c = 0, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| inspector payoff (game) | -0.502 [-0.574, -0.441] | -0.498 |
| inspector payoff (net) | -0.502 [-0.575, -0.442] | -0.498 |
| inspectee payoff (game) | -0.006 [-0.014, -0.000] | -0.000 |
| P(inspect) | 0.423 [0.398, 0.451] | 0.418 |
| P(cheat) | 0.029 [0.006, 0.056] | 0.027 |
| inspector mass p>1/4 | 0.955 [0.912, 0.990] | 0.942 |
| mass p=1/4 | 0.009 [0.000, 0.027] | 0.010 |
| mass p<1/4 | 0.036 [0.005, 0.075] | 0.048 |
| mass at 5/16 | 0.050 [0.000, 0.125] | 0.050 |
| mass at 3/8 | 0.440 [0.300, 0.590] | 0.435 |
| mass at 1/2 | 0.449 [0.304, 0.599] | 0.443 |
| inspectee readers | 0.506 [0.423, 0.588] | 0.517 |
|  exact readers | 0.495 [0.410, 0.577] | 0.506 |
|  sampling readers | 0.011 [0.000, 0.032] | 0.011 |
|  behavioural readers | 0.008 [0.000, 0.024] | 0.007 |
| inspector readers | 0.000 [0.000, 0.000] | 0.000 |
| class C share | 0.440 [0.377, 0.506] | 0.432 |
| class K share | 0.000 [0.000, 0.000] | 0.000 |
| inspectee X share | 0.054 [0.009, 0.110] | 0.051 |
| class N share | 0.036 [0.005, 0.076] | 0.048 |
| class I share | 0.016 [0.000, 0.048] | 0.015 |
| inspectees q<=0.02 | 0.941 [0.882, 0.986] | 0.944 |
| inspectees q>=0.98 | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| best inspector program payoff vs the inspectees (net) | -0.319 [-0.373, -0.271] | -0.319 |
| best inspectee program payoff vs the inspectors (net) | 0.036 [0.005, 0.075] | 0.048 |
| individual mixing (inspector) | 0.948 [0.896, 0.987] | 0.937 |
| individual mixing (inspectee) | 0.059 [0.014, 0.116] | 0.056 |
| homozygosity 0 | 0.971 [0.944, 0.994] | 0.971 |
| homozygosity 1 | 0.786 [0.763, 0.812] | 0.789 |
| support 0 | 1.086 [1.020, 1.171] | 1.088 |
| support 1 | 1.620 [1.541, 1.688] | 1.626 |
| bounded-cr disagreement (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| islands committed | 0.961 [0.921, 0.992] | 0.948 |
| islands committed+compliant | 0.907 [0.820, 0.977] | 0.909 |
| islands at (0,0) | 0.002 [0.000, 0.004] | 0.002 |
| islands near Nash | 0.009 [0.002, 0.019] | 0.009 |
| islands cheat prob > 1/2 | 0.000 [0.000, 0.000] | 0.000 |
| island inspector payoff q10 | -0.563 [-0.689, -0.461] | -0.572 |
| island inspector payoff median | -0.512 [-0.598, -0.442] | -0.502 |
| island inspector payoff q90 | -0.421 [-0.446, -0.396] | -0.414 |

**insp exact_ee, c = 0.01, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| inspector payoff (game) | -0.467 [-0.519, -0.427] | -0.476 |
| inspector payoff (net) | -0.467 [-0.520, -0.425] | -0.476 |
| inspectee payoff (game) | -0.000 [-0.003, 0.002] | 0.000 |
| P(inspect) | 0.419 [0.395, 0.443] | 0.418 |
| P(cheat) | 0.016 [0.001, 0.037] | 0.019 |
| inspector mass p>1/4 | 0.945 [0.884, 0.990] | 0.946 |
| mass p=1/4 | 0.025 [0.000, 0.070] | 0.020 |
| mass p<1/4 | 0.030 [0.000, 0.068] | 0.034 |
| mass at 5/16 | 0.050 [0.000, 0.125] | 0.050 |
| mass at 3/8 | 0.405 [0.255, 0.555] | 0.404 |
| mass at 1/2 | 0.490 [0.344, 0.640] | 0.492 |
| inspectee readers | 0.146 [0.095, 0.203] | 0.175 |
|  exact readers | 0.146 [0.094, 0.204] | 0.175 |
|  sampling readers | 0.000 [0.000, 0.000] | 0.000 |
|  behavioural readers | 0.002 [0.000, 0.006] | 0.003 |
| inspector readers | 0.000 [0.000, 0.000] | 0.000 |
| class C share | 0.824 [0.764, 0.881] | 0.792 |
| class K share | 0.002 [0.000, 0.007] | 0.007 |
| inspectee X share | 0.025 [0.000, 0.066] | 0.023 |
| class N share | 0.030 [0.000, 0.068] | 0.034 |
| class I share | 0.000 [0.000, 0.000] | 0.000 |
| inspectees q<=0.02 | 0.968 [0.927, 0.998] | 0.966 |
| inspectees q>=0.98 | 0.002 [0.000, 0.007] | 0.007 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspectee) | 0.001 [0.001, 0.002] | 0.002 |
| best inspector program payoff vs the inspectees (net) | -0.140 [-0.193, -0.096] | -0.162 |
| best inspectee program payoff vs the inspectors (net) | 0.029 [0.000, 0.067] | 0.034 |
| individual mixing (inspector) | 0.970 [0.932, 1.000] | 0.966 |
| individual mixing (inspectee) | 0.030 [0.002, 0.071] | 0.028 |
| homozygosity 0 | 0.977 [0.952, 0.998] | 0.976 |
| homozygosity 1 | 0.888 [0.857, 0.917] | 0.870 |
| support 0 | 1.073 [1.006, 1.158] | 1.078 |
| support 1 | 1.334 [1.247, 1.424] | 1.384 |
| bounded-cr disagreement (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| islands committed | 0.952 [0.898, 0.993] | 0.955 |
| islands committed+compliant | 0.929 [0.855, 0.987] | 0.931 |
| islands at (0,0) | 0.002 [0.000, 0.006] | 0.003 |
| islands near Nash | 0.004 [0.000, 0.009] | 0.006 |
| islands cheat prob > 1/2 | 0.002 [0.000, 0.007] | 0.007 |
| island inspector payoff q10 | -0.520 [-0.628, -0.438] | -0.545 |
| island inspector payoff median | -0.458 [-0.512, -0.419] | -0.467 |
| island inspector payoff q90 | -0.418 [-0.444, -0.391] | -0.416 |

**insp exact_er, c = 0, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| inspector payoff (game) | -0.290 [-0.410, -0.177] | -0.283 |
| inspector payoff (net) | -0.290 [-0.411, -0.178] | -0.283 |
| inspectee payoff (game) | 0.046 [0.024, 0.071] | 0.047 |
| P(inspect) | 0.023 [0.007, 0.044] | 0.024 |
| P(cheat) | 0.074 [0.045, 0.104] | 0.071 |
| inspector mass p>1/4 | 0.043 [0.010, 0.085] | 0.044 |
| mass p=1/4 | 0.000 [0.000, 0.000] | 0.000 |
| mass p<1/4 | 0.957 [0.914, 0.989] | 0.956 |
| mass at 5/16 | 0.000 [0.000, 0.001] | 0.000 |
| mass at 3/8 | 0.000 [0.000, 0.001] | 0.000 |
| mass at 1/2 | 0.032 [0.004, 0.072] | 0.034 |
| inspectee readers | 0.000 [0.000, 0.000] | 0.000 |
|  exact readers | 0.000 [0.000, 0.000] | 0.000 |
|  sampling readers | 0.000 [0.000, 0.000] | 0.000 |
|  behavioural readers | 0.000 [0.000, 0.000] | 0.000 |
| inspector readers | 0.717 [0.630, 0.794] | 0.715 |
| class C share | 0.626 [0.483, 0.765] | 0.632 |
| class K share | 0.009 [0.000, 0.025] | 0.009 |
| inspectee X share | 0.011 [0.000, 0.033] | 0.007 |
| class N share | 0.256 [0.193, 0.324] | 0.260 |
| class I share | 0.000 [0.000, 0.000] | 0.000 |
| inspectees q<=0.02 | 0.626 [0.482, 0.758] | 0.632 |
| inspectees q>=0.98 | 0.009 [0.000, 0.025] | 0.009 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| best inspector program payoff vs the inspectees (net) | -0.255 [-0.358, -0.159] | -0.249 |
| best inspectee program payoff vs the inspectors (net) | 0.270 [0.238, 0.310] | 0.270 |
| individual mixing (inspector) | 0.067 [0.024, 0.118] | 0.069 |
| individual mixing (inspectee) | 0.364 [0.229, 0.504] | 0.359 |
| homozygosity 0 | 0.825 [0.794, 0.856] | 0.824 |
| homozygosity 1 | 0.973 [0.952, 0.991] | 0.973 |
| support 0 | 1.534 [1.435, 1.630] | 1.531 |
| support 1 | 1.085 [1.027, 1.156] | 1.085 |
| bounded-cr disagreement (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| islands committed | 0.037 [0.005, 0.079] | 0.037 |
| islands committed+compliant | 0.008 [0.000, 0.021] | 0.010 |
| islands at (0,0) | 0.576 [0.428, 0.722] | 0.577 |
| islands near Nash | 0.021 [0.006, 0.043] | 0.021 |
| islands cheat prob > 1/2 | 0.010 [0.000, 0.024] | 0.009 |
| island inspector payoff q10 | -0.389 [-0.569, -0.233] | -0.389 |
| island inspector payoff median | -0.281 [-0.407, -0.163] | -0.267 |
| island inspector payoff q90 | -0.203 [-0.298, -0.113] | -0.197 |

**insp exact_er, c = 0.01, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| inspector payoff (game) | -0.506 [-0.639, -0.369] | -0.498 |
| inspector payoff (net) | -0.508 [-0.641, -0.377] | -0.501 |
| inspectee payoff (game) | 0.093 [0.065, 0.121] | 0.085 |
| P(inspect) | 0.033 [0.017, 0.052] | 0.040 |
| P(cheat) | 0.127 [0.093, 0.160] | 0.125 |
| inspector mass p>1/4 | 0.052 [0.027, 0.086] | 0.066 |
| mass p=1/4 | 0.011 [0.000, 0.029] | 0.008 |
| mass p<1/4 | 0.936 [0.900, 0.966] | 0.925 |
| mass at 5/16 | 0.000 [0.000, 0.000] | 0.000 |
| mass at 3/8 | 0.000 [0.000, 0.001] | 0.000 |
| mass at 1/2 | 0.040 [0.017, 0.073] | 0.044 |
| inspectee readers | 0.000 [0.000, 0.000] | 0.000 |
|  exact readers | 0.000 [0.000, 0.000] | 0.000 |
|  sampling readers | 0.000 [0.000, 0.000] | 0.000 |
|  behavioural readers | 0.000 [0.000, 0.000] | 0.000 |
| inspector readers | 0.247 [0.175, 0.329] | 0.297 |
| class C share | 0.404 [0.259, 0.555] | 0.409 |
| class K share | 0.006 [0.000, 0.019] | 0.006 |
| inspectee X share | 0.009 [0.000, 0.027] | 0.013 |
| class N share | 0.736 [0.656, 0.810] | 0.684 |
| class I share | 0.005 [0.000, 0.015] | 0.006 |
| inspectees q<=0.02 | 0.404 [0.258, 0.553] | 0.409 |
| inspectees q>=0.98 | 0.006 [0.000, 0.019] | 0.006 |
| forfeit (inspector) | 0.000 [0.000, 0.000] | 0.000 |
| forfeit (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| price paid (inspector) | 0.002 [0.002, 0.003] | 0.003 |
| price paid (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| best inspector program payoff vs the inspectees (net) | -0.478 [-0.604, -0.348] | -0.468 |
| best inspectee program payoff vs the inspectors (net) | 0.640 [0.563, 0.714] | 0.566 |
| individual mixing (inspector) | 0.075 [0.039, 0.119] | 0.092 |
| individual mixing (inspectee) | 0.590 [0.441, 0.735] | 0.585 |
| homozygosity 0 | 0.864 [0.840, 0.888] | 0.828 |
| homozygosity 1 | 0.972 [0.951, 0.990] | 0.963 |
| support 0 | 1.418 [1.339, 1.496] | 1.521 |
| support 1 | 1.087 [1.031, 1.156] | 1.115 |
| bounded-cr disagreement (inspectee) | 0.000 [0.000, 0.000] | 0.000 |
| islands committed | 0.043 [0.018, 0.076] | 0.055 |
| islands committed+compliant | 0.009 [0.000, 0.022] | 0.008 |
| islands at (0,0) | 0.359 [0.210, 0.507] | 0.360 |
| islands near Nash | 0.042 [0.023, 0.066] | 0.052 |
| islands cheat prob > 1/2 | 0.005 [0.000, 0.016] | 0.005 |
| island inspector payoff q10 | -0.586 [-0.764, -0.423] | -0.591 |
| island inspector payoff median | -0.499 [-0.630, -0.365] | -0.508 |
| island inspector payoff q90 | -0.443 [-0.569, -0.317] | -0.395 |

**end exact, c = 0.01, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| player I payoff (game) | -0.148 [-0.195, -0.100] | -0.148 |
| player II payoff (game) | 0.148 [0.103, 0.198] | 0.148 |
| bluff prob. (loser) | 0.148 [0.109, 0.190] | 0.152 |
| call prob. | 0.390 [0.295, 0.488] | 0.395 |
| winner betting | 0.968 [0.938, 0.993] | 0.967 |
| I mass |bluff-1/4|<=0.1 | 0.229 [0.105, 0.375] | 0.232 |
| II mass |call-1/2|<=0.1 | 0.472 [0.332, 0.620] | 0.463 |
| islands bluff within 0.1 | 0.304 [0.187, 0.427] | 0.323 |
| islands call within 0.1 | 0.461 [0.317, 0.607] | 0.455 |
| islands both | 0.151 [0.078, 0.244] | 0.165 |
| islands |value|<=0.1 | 0.480 [0.337, 0.630] | 0.475 |
| islands all three | 0.138 [0.062, 0.225] | 0.149 |
| class EQ (I) | 0.128 [0.030, 0.230] | 0.129 |
| class BET | 0.008 [0.000, 0.023] | 0.006 |
| class CHECK | 0.000 [0.000, 0.000] | 0.000 |
| class HON | 0.596 [0.474, 0.715] | 0.579 |
| class X (II) | 0.405 [0.260, 0.555] | 0.392 |
| class CALL | 0.011 [0.000, 0.033] | 0.008 |
| class FOLD | 0.043 [0.004, 0.101] | 0.046 |
| I readers | 0.089 [0.037, 0.147] | 0.106 |
| II readers | 0.540 [0.392, 0.693] | 0.554 |
| II exact readers | 0.540 [0.394, 0.693] | 0.554 |
| II sampling readers | 0.000 [0.000, 0.000] | 0.000 |
| II behavioural readers | 0.106 [0.042, 0.181] | 0.132 |
| exploitability of II: best I program payoff (net) | 0.506 [0.371, 0.636] | 0.518 |
| exploitability of I: best II program payoff (net) | 0.276 [0.235, 0.315] | 0.279 |
| forfeit I | 0.000 [0.000, 0.000] | 0.000 |
| forfeit II | 0.000 [0.000, 0.001] | 0.001 |
| price paid I | 0.001 [0.000, 0.002] | 0.002 |
| price paid II | 0.006 [0.004, 0.007] | 0.006 |
| island bluff q10 | 0.074 [0.038, 0.114] | 0.074 |
| island bluff median | 0.128 [0.087, 0.173] | 0.129 |
| island bluff q90 | 0.253 [0.195, 0.318] | 0.270 |
| island call q10 | 0.328 [0.232, 0.425] | 0.321 |
| island call median | 0.380 [0.283, 0.478] | 0.385 |
| island call q90 | 0.466 [0.368, 0.562] | 0.487 |
| mixing I | 0.396 [0.281, 0.523] | 0.411 |
| mixing II | 0.545 [0.411, 0.682] | 0.554 |
| support 0 | 1.288 [1.196, 1.383] | 1.313 |
| support 1 | 1.109 [1.043, 1.181] | 1.130 |
| bounded-cr disagreement (I) | 0.000 [0.000, 0.000] | 0.000 |
| bounded-cr disagreement (II) | 0.002 [0.000, 0.007] | 0.008 |

**end exact, c = 0, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| player I payoff (game) | -0.180 [-0.229, -0.130] | -0.178 |
| player II payoff (game) | 0.180 [0.129, 0.229] | 0.178 |
| bluff prob. (loser) | 0.236 [0.177, 0.296] | 0.240 |
| call prob. | 0.375 [0.287, 0.468] | 0.381 |
| winner betting | 0.981 [0.956, 0.999] | 0.980 |
| I mass |bluff-1/4|<=0.1 | 0.200 [0.075, 0.325] | 0.200 |
| II mass |call-1/2|<=0.1 | 0.396 [0.264, 0.538] | 0.401 |
| islands bluff within 0.1 | 0.255 [0.145, 0.379] | 0.260 |
| islands call within 0.1 | 0.394 [0.257, 0.536] | 0.397 |
| islands both | 0.114 [0.045, 0.206] | 0.119 |
| islands |value|<=0.1 | 0.418 [0.268, 0.575] | 0.419 |
| islands all three | 0.091 [0.020, 0.180] | 0.095 |
| class EQ (I) | 0.125 [0.025, 0.225] | 0.125 |
| class BET | 0.004 [0.000, 0.011] | 0.006 |
| class CHECK | 0.000 [0.000, 0.000] | 0.000 |
| class HON | 0.339 [0.228, 0.465] | 0.336 |
| class X (II) | 0.289 [0.153, 0.428] | 0.291 |
| class CALL | 0.000 [0.000, 0.000] | 0.000 |
| class FOLD | 0.034 [0.000, 0.078] | 0.029 |
| I readers | 0.367 [0.234, 0.506] | 0.366 |
| II readers | 0.671 [0.531, 0.807] | 0.672 |
| II exact readers | 0.660 [0.510, 0.800] | 0.660 |
| II sampling readers | 0.011 [0.000, 0.032] | 0.012 |
| II behavioural readers | 0.191 [0.092, 0.301] | 0.191 |
| exploitability of II: best I program payoff (net) | 0.686 [0.541, 0.813] | 0.680 |
| exploitability of I: best II program payoff (net) | 0.418 [0.316, 0.530] | 0.417 |
| forfeit I | 0.000 [0.000, 0.000] | 0.000 |
| forfeit II | 0.000 [0.000, 0.001] | 0.000 |
| price paid I | 0.000 [0.000, 0.000] | 0.000 |
| price paid II | 0.000 [0.000, 0.000] | 0.000 |
| island bluff q10 | 0.181 [0.120, 0.245] | 0.179 |
| island bluff median | 0.234 [0.171, 0.298] | 0.238 |
| island bluff q90 | 0.300 [0.237, 0.363] | 0.306 |
| island call q10 | 0.266 [0.176, 0.364] | 0.270 |
| island call median | 0.370 [0.274, 0.467] | 0.376 |
| island call q90 | 0.494 [0.382, 0.600] | 0.499 |
| mixing I | 0.566 [0.431, 0.701] | 0.568 |
| mixing II | 0.540 [0.405, 0.670] | 0.547 |
| support 0 | 1.259 [1.159, 1.364] | 1.281 |
| support 1 | 1.127 [1.046, 1.220] | 1.132 |
| bounded-cr disagreement (I) | 0.006 [0.000, 0.018] | 0.005 |
| bounded-cr disagreement (II) | 0.025 [0.000, 0.070] | 0.022 |

**end blind, c = 0, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| player I payoff (game) | -0.149 [-0.201, -0.097] | -0.146 |
| player II payoff (game) | 0.149 [0.097, 0.201] | 0.146 |
| bluff prob. (loser) | 0.115 [0.060, 0.176] | 0.117 |
| call prob. | 0.266 [0.190, 0.343] | 0.279 |
| winner betting | 0.952 [0.916, 0.981] | 0.954 |
| I mass |bluff-1/4|<=0.1 | 0.079 [0.004, 0.175] | 0.080 |
| II mass |call-1/2|<=0.1 | 0.366 [0.227, 0.513] | 0.366 |
| islands bluff within 0.1 | 0.108 [0.034, 0.202] | 0.105 |
| islands call within 0.1 | 0.370 [0.230, 0.517] | 0.371 |
| islands both | 0.036 [0.004, 0.091] | 0.036 |
| islands |value|<=0.1 | 0.451 [0.305, 0.598] | 0.449 |
| islands all three | 0.032 [0.002, 0.086] | 0.033 |
| class EQ (I) | 0.000 [0.000, 0.000] | 0.000 |
| class BET | 0.000 [0.000, 0.000] | 0.000 |
| class CHECK | 0.007 [0.000, 0.020] | 0.006 |
| class HON | 0.703 [0.566, 0.821] | 0.702 |
| class X (II) | 0.366 [0.227, 0.516] | 0.366 |
| class CALL | 0.030 [0.004, 0.063] | 0.043 |
| class FOLD | 0.479 [0.333, 0.625] | 0.466 |
| I readers | 0.000 [0.000, 0.000] | 0.000 |
| II readers | 0.000 [0.000, 0.000] | 0.000 |
| II exact readers | 0.000 [0.000, 0.000] | 0.000 |
| II sampling readers | 0.000 [0.000, 0.000] | 0.000 |
| II behavioural readers | 0.000 [0.000, 0.000] | 0.000 |
| exploitability of II: best I program payoff (net) | 0.516 [0.375, 0.654] | 0.506 |
| exploitability of I: best II program payoff (net) | 0.315 [0.293, 0.338] | 0.315 |
| forfeit I | 0.000 [0.000, 0.000] | 0.000 |
| forfeit II | 0.000 [0.000, 0.000] | 0.000 |
| price paid I | 0.000 [0.000, 0.000] | 0.000 |
| price paid II | 0.000 [0.000, 0.000] | 0.000 |
| island bluff q10 | 0.090 [0.038, 0.148] | 0.090 |
| island bluff median | 0.113 [0.058, 0.172] | 0.117 |
| island bluff q90 | 0.141 [0.079, 0.209] | 0.143 |
| island call q10 | 0.230 [0.151, 0.310] | 0.238 |
| island call median | 0.257 [0.184, 0.334] | 0.279 |
| island call q90 | 0.312 [0.222, 0.407] | 0.320 |
| mixing I | 0.269 [0.146, 0.402] | 0.274 |
| mixing II | 0.491 [0.338, 0.641] | 0.491 |
| support 0 | 1.146 [1.068, 1.236] | 1.141 |
| support 1 | 1.078 [1.017, 1.158] | 1.080 |
| bounded-cr disagreement (I) | 0.000 [0.000, 0.000] | 0.000 |
| bounded-cr disagreement (II) | 0.000 [0.000, 0.000] | 0.000 |

**end sample, c = 0.01, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| player I payoff (game) | -0.142 [-0.185, -0.101] | -0.142 |
| player II payoff (game) | 0.142 [0.101, 0.185] | 0.142 |
| bluff prob. (loser) | 0.104 [0.054, 0.159] | 0.092 |
| call prob. | 0.263 [0.193, 0.335] | 0.257 |
| winner betting | 0.972 [0.946, 0.994] | 0.973 |
| I mass |bluff-1/4|<=0.1 | 0.100 [0.025, 0.200] | 0.100 |
| II mass |call-1/2|<=0.1 | 0.265 [0.147, 0.396] | 0.262 |
| islands bluff within 0.1 | 0.134 [0.049, 0.232] | 0.129 |
| islands call within 0.1 | 0.269 [0.148, 0.408] | 0.266 |
| islands both | 0.036 [0.005, 0.086] | 0.034 |
| islands |value|<=0.1 | 0.400 [0.261, 0.546] | 0.395 |
| islands all three | 0.034 [0.004, 0.083] | 0.034 |
| class EQ (I) | 0.100 [0.025, 0.200] | 0.100 |
| class BET | 0.017 [0.000, 0.050] | 0.011 |
| class CHECK | 0.009 [0.000, 0.023] | 0.012 |
| class HON | 0.718 [0.592, 0.834] | 0.730 |
| class X (II) | 0.265 [0.143, 0.396] | 0.262 |
| class CALL | 0.031 [0.000, 0.069] | 0.029 |
| class FOLD | 0.402 [0.253, 0.547] | 0.411 |
| I readers | 0.016 [0.000, 0.047] | 0.007 |
| II readers | 0.125 [0.025, 0.225] | 0.125 |
| II exact readers | 0.000 [0.000, 0.000] | 0.000 |
| II sampling readers | 0.125 [0.025, 0.250] | 0.125 |
| II behavioural readers | 0.000 [0.000, 0.000] | 0.000 |
| exploitability of II: best I program payoff (net) | 0.506 [0.374, 0.641] | 0.514 |
| exploitability of I: best II program payoff (net) | 0.295 [0.257, 0.334] | 0.292 |
| forfeit I | 0.000 [0.000, 0.000] | 0.000 |
| forfeit II | 0.000 [0.000, 0.000] | 0.000 |
| price paid I | 0.000 [0.000, 0.000] | 0.000 |
| price paid II | 0.001 [0.000, 0.002] | 0.001 |
| island bluff q10 | 0.055 [0.021, 0.096] | 0.057 |
| island bluff median | 0.110 [0.057, 0.172] | 0.091 |
| island bluff q90 | 0.143 [0.073, 0.221] | 0.129 |
| island call q10 | 0.222 [0.158, 0.290] | 0.218 |
| island call median | 0.264 [0.193, 0.337] | 0.256 |
| island call q90 | 0.302 [0.213, 0.394] | 0.296 |
| mixing I | 0.242 [0.127, 0.366] | 0.232 |
| mixing II | 0.567 [0.416, 0.719] | 0.561 |
| support 0 | 1.166 [1.078, 1.260] | 1.162 |
| support 1 | 1.122 [1.038, 1.230] | 1.125 |
| bounded-cr disagreement (I) | 0.000 [0.000, 0.000] | 0.000 |
| bounded-cr disagreement (II) | 0.000 [0.000, 0.000] | 0.000 |

**end matched, c = 0.01, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| player I payoff (game) | -0.030 [-0.053, -0.012] | -0.035 |
| player II payoff (game) | 0.030 [0.012, 0.053] | 0.035 |
| bluff prob. (loser) | 0.168 [0.109, 0.232] | 0.159 |
| call prob. | 0.451 [0.410, 0.484] | 0.443 |
| winner betting | 0.964 [0.942, 0.984] | 0.967 |
| I mass |bluff-1/4|<=0.1 | 0.114 [0.025, 0.214] | 0.118 |
| II mass |call-1/2|<=0.1 | 0.769 [0.646, 0.882] | 0.733 |
| islands bluff within 0.1 | 0.167 [0.081, 0.266] | 0.189 |
| islands call within 0.1 | 0.781 [0.657, 0.892] | 0.740 |
| islands both | 0.132 [0.059, 0.221] | 0.144 |
| islands |value|<=0.1 | 0.854 [0.751, 0.944] | 0.832 |
| islands all three | 0.129 [0.054, 0.219] | 0.140 |
| class EQ (I) | 0.025 [0.000, 0.075] | 0.025 |
| class BET | 0.037 [0.001, 0.085] | 0.040 |
| class CHECK | 0.000 [0.000, 0.000] | 0.000 |
| class HON | 0.637 [0.507, 0.760] | 0.653 |
| class X (II) | 0.582 [0.438, 0.716] | 0.556 |
| class CALL | 0.019 [0.000, 0.044] | 0.023 |
| class FOLD | 0.084 [0.018, 0.170] | 0.092 |
| I readers | 0.077 [0.014, 0.156] | 0.066 |
| II readers | 0.125 [0.040, 0.224] | 0.132 |
| II exact readers | 0.000 [0.000, 0.000] | 0.000 |
| II sampling readers | 0.293 [0.172, 0.427] | 0.297 |
| II behavioural readers | 0.034 [0.000, 0.083] | 0.054 |
| exploitability of II: best I program payoff (net) | 0.134 [0.061, 0.221] | 0.150 |
| exploitability of I: best II program payoff (net) | 0.300 [0.262, 0.340] | 0.295 |
| forfeit I | 0.000 [0.000, 0.000] | 0.000 |
| forfeit II | 0.000 [0.000, 0.000] | 0.000 |
| price paid I | 0.001 [0.000, 0.002] | 0.001 |
| price paid II | 0.001 [0.000, 0.002] | 0.001 |
| island bluff q10 | 0.094 [0.048, 0.145] | 0.070 |
| island bluff median | 0.165 [0.102, 0.240] | 0.148 |
| island bluff q90 | 0.257 [0.171, 0.346] | 0.268 |
| island call q10 | 0.415 [0.365, 0.459] | 0.394 |
| island call median | 0.451 [0.410, 0.484] | 0.444 |
| island call q90 | 0.486 [0.437, 0.533] | 0.492 |
| mixing I | 0.326 [0.200, 0.457] | 0.307 |
| mixing II | 0.897 [0.803, 0.971] | 0.885 |
| support 0 | 1.201 [1.116, 1.291] | 1.242 |
| support 1 | 1.205 [1.106, 1.313] | 1.243 |
| bounded-cr disagreement (I) | 0.000 [0.000, 0.000] | 0.000 |
| bounded-cr disagreement (II) | 0.000 [0.000, 0.000] | 0.000 |

**end sample, c = 0, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| player I payoff (game) | -0.122 [-0.175, -0.069] | -0.122 |
| player II payoff (game) | 0.122 [0.070, 0.176] | 0.122 |
| bluff prob. (loser) | 0.112 [0.063, 0.164] | 0.121 |
| call prob. | 0.256 [0.188, 0.323] | 0.257 |
| winner betting | 0.969 [0.934, 0.994] | 0.969 |
| I mass |bluff-1/4|<=0.1 | 0.150 [0.050, 0.275] | 0.150 |
| II mass |call-1/2|<=0.1 | 0.327 [0.191, 0.469] | 0.326 |
| islands bluff within 0.1 | 0.178 [0.079, 0.296] | 0.183 |
| islands call within 0.1 | 0.330 [0.198, 0.477] | 0.328 |
| islands both | 0.063 [0.008, 0.139] | 0.066 |
| islands |value|<=0.1 | 0.507 [0.362, 0.650] | 0.506 |
| islands all three | 0.063 [0.009, 0.139] | 0.064 |
| class EQ (I) | 0.125 [0.025, 0.225] | 0.125 |
| class BET | 0.000 [0.000, 0.000] | 0.000 |
| class CHECK | 0.006 [0.000, 0.019] | 0.006 |
| class HON | 0.666 [0.524, 0.795] | 0.652 |
| class X (II) | 0.267 [0.148, 0.400] | 0.265 |
| class CALL | 0.021 [0.000, 0.055] | 0.023 |
| class FOLD | 0.421 [0.276, 0.568] | 0.425 |
| I readers | 0.003 [0.000, 0.010] | 0.006 |
| II readers | 0.150 [0.050, 0.260] | 0.150 |
| II exact readers | 0.000 [0.000, 0.000] | 0.000 |
| II sampling readers | 0.150 [0.050, 0.265] | 0.150 |
| II behavioural readers | 0.014 [0.000, 0.042] | 0.023 |
| exploitability of II: best I program payoff (net) | 0.487 [0.345, 0.618] | 0.490 |
| exploitability of I: best II program payoff (net) | 0.281 [0.242, 0.320] | 0.279 |
| forfeit I | 0.000 [0.000, 0.000] | 0.000 |
| forfeit II | 0.000 [0.000, 0.000] | 0.000 |
| price paid I | 0.000 [0.000, 0.000] | 0.000 |
| price paid II | 0.000 [0.000, 0.000] | 0.000 |
| island bluff q10 | 0.091 [0.044, 0.144] | 0.094 |
| island bluff median | 0.105 [0.057, 0.158] | 0.117 |
| island bluff q90 | 0.143 [0.087, 0.202] | 0.157 |
| island call q10 | 0.219 [0.156, 0.285] | 0.220 |
| island call median | 0.260 [0.190, 0.330] | 0.258 |
| island call q90 | 0.285 [0.201, 0.373] | 0.291 |
| mixing I | 0.317 [0.189, 0.454] | 0.336 |
| mixing II | 0.558 [0.413, 0.696] | 0.552 |
| support 0 | 1.109 [1.042, 1.187] | 1.121 |
| support 1 | 1.118 [1.037, 1.210] | 1.122 |
| bounded-cr disagreement (I) | 0.000 [0.000, 0.000] | 0.000 |
| bounded-cr disagreement (II) | 0.000 [0.000, 0.000] | 0.000 |

**end matched, c = 0, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| player I payoff (game) | -0.027 [-0.049, -0.007] | -0.029 |
| player II payoff (game) | 0.027 [0.007, 0.049] | 0.029 |
| bluff prob. (loser) | 0.221 [0.167, 0.279] | 0.223 |
| call prob. | 0.434 [0.388, 0.472] | 0.435 |
| winner betting | 0.954 [0.930, 0.975] | 0.951 |
| I mass |bluff-1/4|<=0.1 | 0.134 [0.043, 0.242] | 0.129 |
| II mass |call-1/2|<=0.1 | 0.659 [0.523, 0.794] | 0.642 |
| islands bluff within 0.1 | 0.197 [0.108, 0.300] | 0.201 |
| islands call within 0.1 | 0.678 [0.545, 0.805] | 0.663 |
| islands both | 0.104 [0.047, 0.178] | 0.101 |
| islands |value|<=0.1 | 0.772 [0.661, 0.877] | 0.774 |
| islands all three | 0.100 [0.045, 0.174] | 0.097 |
| class EQ (I) | 0.048 [0.000, 0.121] | 0.041 |
| class BET | 0.024 [0.005, 0.050] | 0.028 |
| class CHECK | 0.000 [0.000, 0.000] | 0.000 |
| class HON | 0.489 [0.356, 0.622] | 0.496 |
| class X (II) | 0.392 [0.249, 0.534] | 0.392 |
| class CALL | 0.054 [0.015, 0.103] | 0.055 |
| class FOLD | 0.145 [0.062, 0.238] | 0.139 |
| I readers | 0.131 [0.048, 0.230] | 0.146 |
| II readers | 0.225 [0.109, 0.355] | 0.229 |
| II exact readers | 0.000 [0.000, 0.000] | 0.000 |
| II sampling readers | 0.391 [0.254, 0.530] | 0.392 |
| II behavioural readers | 0.024 [0.000, 0.070] | 0.044 |
| exploitability of II: best I program payoff (net) | 0.209 [0.120, 0.309] | 0.206 |
| exploitability of I: best II program payoff (net) | 0.275 [0.240, 0.307] | 0.274 |
| forfeit I | 0.000 [0.000, 0.000] | 0.000 |
| forfeit II | 0.000 [0.000, 0.000] | 0.000 |
| price paid I | 0.000 [0.000, 0.000] | 0.000 |
| price paid II | 0.000 [0.000, 0.000] | 0.000 |
| island bluff q10 | 0.144 [0.089, 0.206] | 0.130 |
| island bluff median | 0.207 [0.145, 0.273] | 0.206 |
| island bluff q90 | 0.330 [0.259, 0.404] | 0.343 |
| island call q10 | 0.359 [0.298, 0.416] | 0.352 |
| island call median | 0.427 [0.379, 0.471] | 0.435 |
| island call q90 | 0.514 [0.451, 0.576] | 0.517 |
| mixing I | 0.486 [0.349, 0.624] | 0.475 |
| mixing II | 0.802 [0.680, 0.911] | 0.806 |
| support 0 | 1.229 [1.148, 1.315] | 1.285 |
| support 1 | 1.268 [1.162, 1.382] | 1.312 |
| bounded-cr disagreement (I) | 0.000 [0.000, 0.000] | 0.000 |
| bounded-cr disagreement (II) | 0.000 [0.000, 0.000] | 0.000 |

**end exact_ee, c = 0.01, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| player I payoff (game) | -0.208 [-0.258, -0.154] | -0.208 |
| player II payoff (game) | 0.208 [0.150, 0.258] | 0.208 |
| bluff prob. (loser) | 0.135 [0.085, 0.188] | 0.135 |
| call prob. | 0.283 [0.185, 0.394] | 0.282 |
| winner betting | 0.912 [0.851, 0.964] | 0.913 |
| I mass |bluff-1/4|<=0.1 | 0.234 [0.110, 0.369] | 0.228 |
| II mass |call-1/2|<=0.1 | 0.214 [0.104, 0.331] | 0.220 |
| islands bluff within 0.1 | 0.258 [0.137, 0.383] | 0.250 |
| islands call within 0.1 | 0.216 [0.104, 0.339] | 0.219 |
| islands both | 0.061 [0.009, 0.135] | 0.062 |
| islands |value|<=0.1 | 0.300 [0.175, 0.450] | 0.300 |
| islands all three | 0.049 [0.000, 0.121] | 0.050 |
| class EQ (I) | 0.100 [0.025, 0.200] | 0.100 |
| class BET | 0.000 [0.000, 0.000] | 0.000 |
| class CHECK | 0.000 [0.000, 0.000] | 0.000 |
| class HON | 0.568 [0.429, 0.702] | 0.567 |
| class X (II) | 0.167 [0.067, 0.292] | 0.167 |
| class CALL | 0.000 [0.000, 0.000] | 0.000 |
| class FOLD | 0.414 [0.269, 0.562] | 0.402 |
| I readers | 0.000 [0.000, 0.000] | 0.000 |
| II readers | 0.411 [0.269, 0.556] | 0.423 |
| II exact readers | 0.411 [0.270, 0.560] | 0.423 |
| II sampling readers | 0.000 [0.000, 0.000] | 0.000 |
| II behavioural readers | 0.125 [0.042, 0.226] | 0.131 |
| exploitability of II: best I program payoff (net) | 0.399 [0.260, 0.544] | 0.383 |
| exploitability of I: best II program payoff (net) | 0.303 [0.265, 0.340] | 0.303 |
| forfeit I | 0.000 [0.000, 0.000] | 0.000 |
| forfeit II | 0.000 [0.000, 0.000] | 0.000 |
| price paid I | 0.000 [0.000, 0.000] | 0.000 |
| price paid II | 0.004 [0.003, 0.006] | 0.004 |
| island bluff q10 | 0.109 [0.061, 0.162] | 0.107 |
| island bluff median | 0.136 [0.083, 0.190] | 0.136 |
| island bluff q90 | 0.161 [0.104, 0.221] | 0.162 |
| island call q10 | 0.212 [0.118, 0.312] | 0.208 |
| island call median | 0.286 [0.182, 0.400] | 0.284 |
| island call q90 | 0.350 [0.229, 0.475] | 0.354 |
| mixing I | 0.406 [0.268, 0.551] | 0.403 |
| mixing II | 0.315 [0.185, 0.445] | 0.323 |
| support 0 | 1.152 [1.075, 1.239] | 1.162 |
| support 1 | 1.092 [1.036, 1.157] | 1.103 |
| bounded-cr disagreement (I) | 0.000 [0.000, 0.000] | 0.000 |
| bounded-cr disagreement (II) | 0.000 [0.000, 0.000] | 0.000 |

**end exact_er, c = 0.01, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| player I payoff (game) | 0.001 [-0.002, 0.004] | -0.000 |
| player II payoff (game) | -0.001 [-0.004, 0.002] | 0.000 |
| bluff prob. (loser) | 0.252 [0.202, 0.305] | 0.256 |
| call prob. | 0.504 [0.497, 0.513] | 0.499 |
| winner betting | 1.000 [1.000, 1.000] | 1.000 |
| I mass |bluff-1/4|<=0.1 | 0.001 [0.000, 0.004] | 0.001 |
| II mass |call-1/2|<=0.1 | 0.884 [0.799, 0.957] | 0.876 |
| islands bluff within 0.1 | 0.172 [0.143, 0.202] | 0.183 |
| islands call within 0.1 | 0.877 [0.791, 0.949] | 0.872 |
| islands both | 0.142 [0.115, 0.171] | 0.151 |
| islands |value|<=0.1 | 0.925 [0.869, 0.971] | 0.924 |
| islands all three | 0.142 [0.115, 0.172] | 0.151 |
| class EQ (I) | 0.001 [0.000, 0.004] | 0.001 |
| class BET | 0.040 [0.009, 0.083] | 0.042 |
| class CHECK | 0.000 [0.000, 0.000] | 0.000 |
| class HON | 0.536 [0.450, 0.620] | 0.529 |
| class X (II) | 0.884 [0.799, 0.957] | 0.876 |
| class CALL | 0.056 [0.020, 0.099] | 0.053 |
| class FOLD | 0.051 [0.016, 0.095] | 0.060 |
| I readers | 0.233 [0.161, 0.312] | 0.262 |
| II readers | 0.000 [0.000, 0.000] | 0.000 |
| II exact readers | 0.000 [0.000, 0.000] | 0.000 |
| II sampling readers | 0.000 [0.000, 0.000] | 0.000 |
| II behavioural readers | 0.000 [0.000, 0.000] | 0.000 |
| exploitability of II: best I program payoff (net) | 0.070 [0.024, 0.127] | 0.078 |
| exploitability of I: best II program payoff (net) | 0.197 [0.166, 0.233] | 0.184 |
| forfeit I | 0.000 [0.000, 0.000] | 0.000 |
| forfeit II | 0.000 [0.000, 0.000] | 0.000 |
| price paid I | 0.002 [0.002, 0.003] | 0.002 |
| price paid II | 0.000 [0.000, 0.000] | 0.000 |
| island bluff q10 | 0.078 [0.037, 0.127] | 0.075 |
| island bluff median | 0.233 [0.171, 0.300] | 0.241 |
| island bluff q90 | 0.459 [0.401, 0.518] | 0.465 |
| island call q10 | 0.441 [0.395, 0.479] | 0.431 |
| island call median | 0.502 [0.492, 0.511] | 0.500 |
| island call q90 | 0.568 [0.526, 0.616] | 0.566 |
| mixing I | 0.424 [0.342, 0.511] | 0.429 |
| mixing II | 0.893 [0.808, 0.962] | 0.887 |
| support 0 | 1.616 [1.541, 1.690] | 1.661 |
| support 1 | 1.179 [1.071, 1.304] | 1.190 |
| bounded-cr disagreement (I) | 0.000 [0.000, 0.000] | 0.000 |
| bounded-cr disagreement (II) | 0.000 [0.000, 0.000] | 0.000 |

**end exact_ee, c = 0, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| player I payoff (game) | -0.250 [-0.292, -0.204] | -0.250 |
| player II payoff (game) | 0.250 [0.208, 0.287] | 0.250 |
| bluff prob. (loser) | 0.121 [0.071, 0.178] | 0.118 |
| call prob. | 0.250 [0.152, 0.353] | 0.241 |
| winner betting | 0.944 [0.904, 0.976] | 0.941 |
| I mass |bluff-1/4|<=0.1 | 0.165 [0.065, 0.284] | 0.165 |
| II mass |call-1/2|<=0.1 | 0.224 [0.109, 0.352] | 0.223 |
| islands bluff within 0.1 | 0.176 [0.074, 0.297] | 0.175 |
| islands call within 0.1 | 0.217 [0.106, 0.348] | 0.216 |
| islands both | 0.095 [0.028, 0.182] | 0.096 |
| islands |value|<=0.1 | 0.200 [0.075, 0.325] | 0.200 |
| islands all three | 0.087 [0.020, 0.177] | 0.089 |
| class EQ (I) | 0.109 [0.025, 0.209] | 0.110 |
| class BET | 0.000 [0.000, 0.000] | 0.000 |
| class CHECK | 0.008 [0.000, 0.016] | 0.009 |
| class HON | 0.610 [0.476, 0.736] | 0.610 |
| class X (II) | 0.150 [0.050, 0.275] | 0.150 |
| class CALL | 0.000 [0.000, 0.000] | 0.000 |
| class FOLD | 0.313 [0.193, 0.442] | 0.309 |
| I readers | 0.000 [0.000, 0.000] | 0.000 |
| II readers | 0.537 [0.402, 0.672] | 0.541 |
| II exact readers | 0.537 [0.401, 0.672] | 0.541 |
| II sampling readers | 0.000 [0.000, 0.000] | 0.000 |
| II behavioural readers | 0.083 [0.018, 0.167] | 0.079 |
| exploitability of II: best I program payoff (net) | 0.277 [0.158, 0.408] | 0.275 |
| exploitability of I: best II program payoff (net) | 0.297 [0.258, 0.333] | 0.297 |
| forfeit I | 0.000 [0.000, 0.000] | 0.000 |
| forfeit II | 0.000 [0.000, 0.000] | 0.000 |
| price paid I | 0.000 [0.000, 0.000] | 0.000 |
| price paid II | 0.000 [0.000, 0.000] | 0.000 |
| island bluff q10 | 0.107 [0.058, 0.162] | 0.104 |
| island bluff median | 0.120 [0.068, 0.177] | 0.116 |
| island bluff q90 | 0.138 [0.080, 0.197] | 0.136 |
| island call q10 | 0.207 [0.111, 0.313] | 0.203 |
| island call median | 0.248 [0.150, 0.357] | 0.237 |
| island call q90 | 0.296 [0.187, 0.414] | 0.288 |
| mixing I | 0.344 [0.207, 0.488] | 0.337 |
| mixing II | 0.306 [0.181, 0.436] | 0.303 |
| support 0 | 1.174 [1.086, 1.275] | 1.173 |
| support 1 | 1.143 [1.069, 1.223] | 1.139 |
| bounded-cr disagreement (I) | 0.000 [0.000, 0.000] | 0.000 |
| bounded-cr disagreement (II) | 0.000 [0.000, 0.000] | 0.000 |

**end exact_er, c = 0, primary (40 runs)**: generation 2,000 mean [95% run-clustered CI]; window 1,500–2,000 mean

| statistic | gen 2,000 | window |
|---|---|---|
| player I payoff (game) | 0.001 [-0.000, 0.003] | -0.001 |
| player II payoff (game) | -0.001 [-0.003, 0.000] | 0.001 |
| bluff prob. (loser) | 0.374 [0.334, 0.409] | 0.371 |
| call prob. | 0.499 [0.493, 0.505] | 0.498 |
| winner betting | 0.996 [0.989, 1.000] | 0.997 |
| I mass |bluff-1/4|<=0.1 | 0.001 [0.000, 0.002] | 0.001 |
| II mass |call-1/2|<=0.1 | 0.914 [0.827, 0.983] | 0.919 |
| islands bluff within 0.1 | 0.134 [0.103, 0.164] | 0.134 |
| islands call within 0.1 | 0.912 [0.829, 0.980] | 0.917 |
| islands both | 0.119 [0.090, 0.149] | 0.115 |
| islands |value|<=0.1 | 0.938 [0.880, 0.986] | 0.945 |
| islands all three | 0.119 [0.090, 0.149] | 0.115 |
| class EQ (I) | 0.001 [0.000, 0.002] | 0.001 |
| class BET | 0.016 [0.000, 0.039] | 0.015 |
| class CHECK | 0.000 [0.000, 0.000] | 0.000 |
| class HON | 0.276 [0.202, 0.359] | 0.277 |
| class X (II) | 0.914 [0.825, 0.978] | 0.919 |
| class CALL | 0.042 [0.009, 0.084] | 0.038 |
| class FOLD | 0.044 [0.010, 0.090] | 0.043 |
| I readers | 0.608 [0.497, 0.709] | 0.612 |
| II readers | 0.000 [0.000, 0.000] | 0.000 |
| II exact readers | 0.000 [0.000, 0.000] | 0.000 |
| II sampling readers | 0.000 [0.000, 0.000] | 0.000 |
| II behavioural readers | 0.000 [0.000, 0.000] | 0.000 |
| exploitability of II: best I program payoff (net) | 0.058 [0.013, 0.117] | 0.056 |
| exploitability of I: best II program payoff (net) | 0.090 [0.055, 0.131] | 0.085 |
| forfeit I | 0.000 [0.000, 0.000] | 0.000 |
| forfeit II | 0.000 [0.000, 0.000] | 0.000 |
| price paid I | 0.000 [0.000, 0.000] | 0.000 |
| price paid II | 0.000 [0.000, 0.000] | 0.000 |
| island bluff q10 | 0.201 [0.142, 0.260] | 0.214 |
| island bluff median | 0.392 [0.345, 0.436] | 0.387 |
| island bluff q90 | 0.508 [0.466, 0.549] | 0.501 |
| island call q10 | 0.457 [0.414, 0.490] | 0.454 |
| island call median | 0.496 [0.488, 0.504] | 0.498 |
| island call q90 | 0.548 [0.511, 0.593] | 0.541 |
| mixing I | 0.700 [0.606, 0.786] | 0.702 |
| mixing II | 0.914 [0.833, 0.981] | 0.919 |
| support 0 | 1.464 [1.380, 1.545] | 1.461 |
| support 1 | 1.110 [1.029, 1.215] | 1.100 |
| bounded-cr disagreement (I) | 0.000 [0.000, 0.000] | 0.000 |
| bounded-cr disagreement (II) | 0.000 [0.000, 0.000] | 0.000 |

## Continuation (runs 0–9, generation 10,000 against 2,000), joint actions and ladder transitions

- **insp_exact_c0**: u0g: -0.251 [-0.477, -0.050] → -0.250 [-0.475, -0.050] (diff 0.001 [-0.001, 0.004]); u1g: 0.055 [0.000, 0.116] → 0.056 [0.012, 0.119] (diff 0.001 [0.000, 0.003]); rd1: 0.113 [0.008, 0.269] → 0.094 [0.000, 0.282] (diff -0.019 [-0.082, 0.046]); p_insp: 0.027 [0.000, 0.079] → 0.025 [0.000, 0.075] (diff -0.002 [-0.007, 0.000]); q_cheat: 0.056 [0.001, 0.118] → 0.056 [0.000, 0.119] (diff 0.000 [-0.001, 0.001])
  joint: P_IC=0.066, P_IK=0.001, P_NC=0.894, P_NK=0.039, corr=0.039
  ladder labels (R reader+committed, C constants+committed, N lax+compliant, K lax+cheating, IK committed+cheating): occupancy C 0.052, IK 0.000, K 0.002, N 0.620, R 0.100, other 0.226; transitions per 25 generations (counts) R->C 2800, other->N 2730, N->other 2681, C->R 1966, C->other 1276, C->N 1259, other->R 1219, other->C 906
- **insp_exact_c0.01**: u0g: -0.297 [-0.543, -0.093] → -0.350 [-0.650, -0.100] (diff -0.053 [-0.145, 0.000]); u1g: 0.051 [0.000, 0.102] → 0.062 [0.000, 0.125] (diff 0.011 [0.000, 0.034]); rd1: 0.000 [0.000, 0.000] → 0.000 [0.000, 0.000] (diff 0.000 [0.000, 0.000]); p_insp: 0.035 [0.000, 0.089] → 0.025 [0.000, 0.075] (diff -0.010 [-0.029, 0.000]); q_cheat: 0.070 [0.019, 0.133] → 0.087 [0.025, 0.163] (diff 0.017 [0.000, 0.048])
  joint: P_IC=0.027, P_IK=0.002, P_NC=0.926, P_NK=0.045, corr=-0.031
  ladder labels (R reader+committed, C constants+committed, N lax+compliant, K lax+cheating, IK committed+cheating): occupancy C 0.039, IK 0.001, K 0.002, N 0.686, R 0.047, other 0.225; transitions per 25 generations (counts) other->N 2719, N->other 2629, R->C 1769, C->R 1153, C->N 911, C->other 879, other->R 737, other->C 592
- **insp_blind_c0**: u0g: -0.897 [-1.054, -0.719] → -0.838 [-1.062, -0.604] (diff 0.059 [-0.158, 0.322]); u1g: 0.032 [-0.021, 0.093] → 0.082 [0.009, 0.170] (diff 0.050 [-0.009, 0.109]); rd1: 0.000 [0.000, 0.000] → 0.000 [0.000, 0.000] (diff 0.000 [0.000, 0.000]); p_insp: 0.250 [0.175, 0.328] → 0.205 [0.120, 0.299] (diff -0.045 [-0.101, 0.011]); q_cheat: 0.205 [0.135, 0.265] → 0.184 [0.101, 0.262] (diff -0.021 [-0.110, 0.045])
  joint: P_IC=0.195, P_IK=0.059, P_NC=0.565, P_NK=0.182, corr=0.013
  ladder labels (R reader+committed, C constants+committed, N lax+compliant, K lax+cheating, IK committed+cheating): occupancy C 0.146, IK 0.027, K 0.026, N 0.128, other 0.673; transitions per 25 generations (counts) other->C 15814, N->other 15175, C->other 10745, other->N 9095, C->N 8137, other->IK 2855, IK->other 2811, other->K 2643
- **insp_matched_c0**: u0g: -0.605 [-0.855, -0.350] → -0.588 [-0.850, -0.300] (diff 0.017 [0.000, 0.051]); u1g: 0.098 [0.037, 0.165] → 0.104 [0.038, 0.171] (diff 0.006 [-0.017, 0.033]); rd1: 0.164 [0.000, 0.376] → 0.100 [0.000, 0.300] (diff -0.064 [-0.155, 0.000]); p_insp: 0.104 [0.023, 0.210] → 0.108 [0.018, 0.225] (diff 0.005 [-0.028, 0.037]); q_cheat: 0.134 [0.059, 0.200] → 0.125 [0.050, 0.200] (diff -0.009 [-0.028, 0.000])
  joint: P_IC=0.092, P_IK=0.018, P_NC=0.775, P_NK=0.114, corr=-0.035
  ladder labels (R reader+committed, C constants+committed, N lax+compliant, K lax+cheating, IK committed+cheating): occupancy C 0.034, IK 0.003, K 0.004, N 0.426, R 0.043, other 0.490; transitions per 25 generations (counts) N->other 7352, other->N 6326, other->C 2621, C->other 2116, C->N 1938, other->R 784, R->C 694, R->other 601
- **insp_sr16_c0**: u0g: -0.284 [-0.488, -0.138] → -0.283 [-0.478, -0.137] (diff 0.001 [-0.001, 0.003]); u1g: 0.052 [0.017, 0.102] → 0.052 [0.017, 0.105] (diff 0.000 [0.000, 0.000]); rd1: 0.003 [0.000, 0.009] → 0.000 [0.000, 0.000] (diff -0.003 [-0.009, 0.000]); p_insp: 0.075 [0.000, 0.175] → 0.074 [0.000, 0.173] (diff -0.001 [-0.003, 0.000]); q_cheat: 0.052 [0.017, 0.100] → 0.052 [0.017, 0.102] (diff 0.000 [0.000, 0.000])
  joint: P_IC=0.117, P_IK=0.003, P_NC=0.840, P_NK=0.040, corr=0.039
  ladder labels (R reader+committed, C constants+committed, N lax+compliant, K lax+cheating, IK committed+cheating): occupancy C 0.174, IK 0.001, K 0.003, N 0.574, R 0.059, other 0.190; transitions per 25 generations (counts) N->other 3147, other->N 2788, R->C 2617, C->R 1714, C->N 1479, other->C 1461, C->other 1304, other->R 925
- **insp_sr4_c0**: u0g: -0.310 [-0.440, -0.192] → -0.301 [-0.440, -0.172] (diff 0.009 [-0.036, 0.056]); u1g: 0.040 [0.007, 0.083] → 0.042 [0.008, 0.083] (diff 0.001 [0.000, 0.003]); rd1: 0.117 [0.004, 0.302] → 0.100 [0.000, 0.300] (diff -0.017 [-0.060, 0.020]); p_insp: 0.115 [0.054, 0.178] → 0.106 [0.042, 0.171] (diff -0.009 [-0.046, 0.016]); q_cheat: 0.052 [0.018, 0.094] → 0.051 [0.014, 0.095] (diff -0.000 [-0.008, 0.008])
  joint: P_IC=0.062, P_IK=0.005, P_NC=0.853, P_NK=0.081, corr=0.016
  ladder labels (R reader+committed, C constants+committed, N lax+compliant, K lax+cheating, IK committed+cheating): occupancy C 0.045, IK 0.001, K 0.002, N 0.561, R 0.014, other 0.377; transitions per 25 generations (counts) N->other 4770, other->N 4106, other->C 2919, C->other 2586, C->N 1428, other->R 625, R->C 499, R->other 374
- **end_exact_c0.01**: u0g: -0.142 [-0.229, -0.058] → -0.157 [-0.245, -0.067] (diff -0.016 [-0.050, 0.002]); u1g: 0.141 [0.058, 0.229] → 0.154 [0.067, 0.250] (diff 0.013 [-0.011, 0.050]); rd1: 0.652 [0.383, 0.883] → 0.613 [0.313, 0.900] (diff -0.039 [-0.270, 0.173]); bluff: 0.139 [0.080, 0.200] → 0.075 [0.000, 0.150] (diff -0.064 [-0.118, -0.022]); call: 0.400 [0.245, 0.575] → 0.357 [0.150, 0.607] (diff -0.043 [-0.171, 0.105])
  joint: P_W_bet_call=0.120, P_W_bet_fold=0.202, P_W_check=0.011, P_L_bet_call=0.063, P_L_bet_fold=0.035, P_L_check=0.568, P_call_given_bet=0.435, P_bluff_given_bet=0.234
- **end_exact_c0**: u0g: -0.150 [-0.250, -0.050] → -0.150 [-0.250, -0.050] (diff -0.000 [-0.000, 0.000]); u1g: 0.150 [0.050, 0.250] → 0.150 [0.067, 0.250] (diff 0.000 [0.000, 0.000]); rd1: 0.684 [0.426, 0.900] → 0.670 [0.370, 0.940] (diff -0.014 [-0.126, 0.084]); bluff: 0.227 [0.125, 0.328] → 0.250 [0.125, 0.375] (diff 0.023 [0.000, 0.058]); call: 0.385 [0.195, 0.597] → 0.403 [0.153, 0.650] (diff 0.017 [-0.046, 0.080])
  joint: P_W_bet_call=0.119, P_W_bet_fold=0.208, P_W_check=0.006, P_L_bet_call=0.100, P_L_bet_fold=0.058, P_L_check=0.509, P_call_given_bet=0.452, P_bluff_given_bet=0.325
- **end_blind_c0**: u0g: -0.187 [-0.279, -0.100] → -0.187 [-0.275, -0.096] (diff 0.000 [0.000, 0.000]); u1g: 0.187 [0.096, 0.275] → 0.187 [0.096, 0.275] (diff 0.000 [0.000, 0.000]); rd1: 0.000 [0.000, 0.000] → 0.000 [0.000, 0.000] (diff 0.000 [0.000, 0.000]); bluff: 0.125 [0.000, 0.250] → 0.125 [0.000, 0.250] (diff 0.000 [0.000, 0.000]); call: 0.225 [0.087, 0.375] → 0.225 [0.075, 0.375] (diff 0.000 [0.000, 0.000])
  joint: P_W_bet_call=0.083, P_W_bet_fold=0.234, P_W_check=0.016, P_L_bet_call=0.034, P_L_bet_fold=0.042, P_L_check=0.590, P_call_given_bet=0.298, P_bluff_given_bet=0.194
- **end_matched_c0.01**: u0g: -0.042 [-0.083, -0.011] → -0.065 [-0.139, -0.010] (diff -0.023 [-0.074, 0.007]); u1g: 0.042 [0.011, 0.082] → 0.065 [0.010, 0.143] (diff 0.023 [-0.007, 0.073]); rd1: 0.151 [0.000, 0.360] → 0.100 [0.000, 0.300] (diff -0.051 [-0.173, 0.019]); bluff: 0.159 [0.067, 0.255] → 0.127 [0.038, 0.230] (diff -0.032 [-0.109, 0.022]); call: 0.435 [0.328, 0.504] → 0.389 [0.250, 0.492] (diff -0.046 [-0.130, 0.000])
  joint: P_W_bet_call=0.145, P_W_bet_fold=0.176, P_W_check=0.012, P_L_bet_call=0.053, P_L_bet_fold=0.059, P_L_check=0.555, P_call_given_bet=0.456, P_bluff_given_bet=0.258

## Chain tables

**insp exact c=0 (exploration-capped, not converged where capped=True)** (chain, pi over pairs of monomorphic classes, K = [157, 157])

| N | states | capped | log10 unexplored flux | circulation | pi cycle | pi drift | pi rest | closed classes | u0 | u1 | p / bluff | q / call | readers (1) | mixing 0 | mixing 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 24649 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.7769 | -0.1782 | 0.440 | 0.172 | 0.097 | 0.365 | 0.153 |
| 1000 | 24649 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.4959 | -0.0535 | 0.319 | 0.077 | 0.366 | 0.420 | 0.145 |
| 10000 | 24649 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.4707 | 0.0291 | 0.281 | 0.054 | 0.569 | 0.534 | 0.293 |

Ladder rates (exact c=0 N=100, log10 rate per mutation event, N × rate): (P38,CRC)->(P38,C) -2.72, 0.189; (P38,C)->(N,C) -1.79, 1.63; (N,C)->(N,K) -1.41, 3.85; (N,K)->(I,K) -0.96, 10.9; (I,K)->(I,C) -0.95, 11.2; (I,C)->(N,C) -1.40, 3.98; (P38,C)->(P38,CRC) -5.17, 0.000676; (N,C)->(P38,C) -8.54, 2.88e-07; (P38,CRC)->(N,CRC) -47.75, 1.78e-46; (P38,CRC)->(P38,K) -8.13, 7.35e-07
Ladder rates (exact c=0 N=1000, log10 rate per mutation event, N × rate): (P38,CRC)->(P38,C) -3.72, 0.189; (P38,C)->(N,C) -1.79, 16.3; (N,C)->(N,K) -1.41, 38.5; (N,K)->(I,K) -0.96, 109; (I,K)->(I,C) -0.95, 112; (I,C)->(N,C) -1.40, 39.8; (P38,C)->(P38,CRC) -6.17, 0.000676; (N,C)->(P38,C) -52.51, 3.07e-50; (P38,CRC)->(N,CRC) -472.82, 0; (P38,CRC)->(P38,K) -66.76, 1.72e-64
Ladder rates (exact c=0 N=10000, log10 rate per mutation event, N × rate): (P38,CRC)->(P38,C) -4.72, 0.189; (P38,C)->(N,C) -1.79, 163; (N,C)->(N,K) -1.41, 385; (N,K)->(I,K) -0.96, 1.09e+03; (I,K)->(I,C) -0.95, 1.12e+03; (I,C)->(N,C) -1.40, 398; (P38,C)->(P38,CRC) -7.17, 0.000676; (N,C)->(P38,C) -492.24, 0; (P38,CRC)->(N,CRC) -4723.47, 0; (P38,CRC)->(P38,K) -653.06, 0

**insp exact c=0.01 (exploration-capped, not converged where capped=True)** (chain, pi over pairs of monomorphic classes, K = [167, 167])

| N | states | capped | log10 unexplored flux | circulation | pi cycle | pi drift | pi rest | closed classes | u0 | u1 | p / bluff | q / call | readers (1) | mixing 0 | mixing 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1000 | 27889 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.6323 | -0.1205 | 0.383 | 0.123 | 0.211 | 0.387 | 0.130 |
| 10000 | 27889 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.6228 | -0.1157 | 0.378 | 0.120 | 0.219 | 0.390 | 0.132 |

Ladder rates (exact c=0.01 N=1000, log10 rate per mutation event, N × rate): (P38,CRC)->(P38,C) -3.22, 0.597; (P38,C)->(N,C) -1.79, 16.3; (N,C)->(N,K) -1.41, 38.5; (N,K)->(I,K) -0.96, 109; (I,K)->(I,C) -0.95, 112; (I,C)->(N,C) -1.40, 39.8; (P38,C)->(P38,CRC) -6.97, 0.000106; (N,C)->(P38,C) -52.51, 3.07e-50; (P38,CRC)->(N,CRC) -472.82, 0; (P38,CRC)->(P38,K) -65.47, 3.39e-63
Ladder rates (exact c=0.01 N=10000, log10 rate per mutation event, N × rate): (P38,CRC)->(P38,C) -3.25, 5.67; (P38,C)->(N,C) -1.79, 163; (N,C)->(N,K) -1.41, 385; (N,K)->(I,K) -0.96, 1.09e+03; (I,K)->(I,C) -0.95, 1.12e+03; (I,C)->(N,C) -1.40, 398; (P38,C)->(P38,CRC) -18.72, 1.9e-15; (N,C)->(P38,C) -492.24, 0; (P38,CRC)->(N,CRC) -4723.47, 0; (P38,CRC)->(P38,K) -640.04, 0

**insp blind c=0 (exploration-capped, not converged where capped=True)** (chain, pi over pairs of monomorphic classes, K = [17, 17])

| N | states | capped | log10 unexplored flux | circulation | pi cycle | pi drift | pi rest | closed classes | u0 | u1 | p / bluff | q / call | readers (1) | mixing 0 | mixing 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 289 | False | n/a | 0.998 | 1.000 | 0.000 | 0.000 | 1 | -0.9335 | -0.2648 | 0.497 | 0.234 | 0.000 | 0.427 | 0.251 |
| 1000 | 289 | False | n/a | 1.000 | 1.000 | 0.000 | 0.000 | 1 | -0.9225 | -0.2606 | 0.494 | 0.230 | 0.000 | 0.432 | 0.247 |
| 10000 | 289 | False | n/a | 1.000 | 1.000 | 0.000 | 0.000 | 1 | -0.9211 | -0.2601 | 0.493 | 0.229 | 0.000 | 0.433 | 0.246 |

**insp matched c=0 (exploration-capped, not converged where capped=True)** (chain, pi over pairs of monomorphic classes, K = [97, 97])

| N | states | capped | log10 unexplored flux | circulation | pi cycle | pi drift | pi rest | closed classes | u0 | u1 | p / bluff | q / call | readers (1) | mixing 0 | mixing 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 9409 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.8614 | -0.2212 | 0.491 | 0.197 | 0.079 | 0.370 | 0.220 |
| 1000 | 9409 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.6559 | -0.1014 | 0.466 | 0.097 | 0.288 | 0.205 | 0.126 |
| 10000 | 9409 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.5689 | -0.0305 | 0.450 | 0.050 | 0.412 | 0.146 | 0.107 |

**insp matched c=0.01 (exploration-capped, not converged where capped=True)** (chain, pi over pairs of monomorphic classes, K = [106, 106])

| N | states | capped | log10 unexplored flux | circulation | pi cycle | pi drift | pi rest | closed classes | u0 | u1 | p / bluff | q / call | readers (1) | mixing 0 | mixing 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 11236 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.8698 | -0.2260 | 0.492 | 0.201 | 0.071 | 0.377 | 0.224 |
| 1000 | 11236 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.7624 | -0.1630 | 0.480 | 0.148 | 0.175 | 0.293 | 0.173 |
| 10000 | 11236 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.7549 | -0.1569 | 0.479 | 0.144 | 0.182 | 0.289 | 0.172 |

**insp sample c=0 (exploration-capped, not converged where capped=True)** (chain, pi over pairs of monomorphic classes, K = [83, 83])

| N | states | capped | log10 unexplored flux | circulation | pi cycle | pi drift | pi rest | closed classes | u0 | u1 | p / bluff | q / call | readers (1) | mixing 0 | mixing 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 6889 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.8341 | -0.2025 | 0.488 | 0.183 | 0.131 | 0.354 | 0.216 |
| 1000 | 6889 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.6467 | -0.0782 | 0.453 | 0.091 | 0.302 | 0.217 | 0.154 |
| 10000 | 6889 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.6424 | -0.0005 | 0.390 | 0.084 | 0.331 | 0.295 | 0.272 |

**insp sample c=0.01 (exploration-capped, not converged where capped=True)** (chain, pi over pairs of monomorphic classes, K = [86, 86])

| N | states | capped | log10 unexplored flux | circulation | pi cycle | pi drift | pi rest | closed classes | u0 | u1 | p / bluff | q / call | readers (1) | mixing 0 | mixing 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 7396 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.8436 | -0.2081 | 0.489 | 0.187 | 0.121 | 0.361 | 0.220 |
| 1000 | 7396 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.7259 | -0.1349 | 0.473 | 0.129 | 0.226 | 0.271 | 0.171 |
| 10000 | 7396 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.7193 | -0.1270 | 0.469 | 0.126 | 0.232 | 0.271 | 0.176 |

**insp sr16 c=0 (exploration-capped, not converged where capped=True)** (chain, pi over pairs of monomorphic classes, K = [436, 412])

| N | states | capped | log10 unexplored flux | circulation | pi cycle | pi drift | pi rest | closed classes | u0 | u1 | p / bluff | q / call | readers (1) | mixing 0 | mixing 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 1500 | True | -2.2 | 0.990 | 0.000 | 0.000 | 0.000 | 1 | -0.7964 | -0.1875 | 0.442 | 0.181 | 0.072 | 0.399 | 0.319 |
| 1000 | 1500 | True | -0.6 | 1.000 | 0.000 | 0.000 | 0.000 | 1 | -0.6091 | -0.1401 | 0.318 | 0.144 | 0.136 | 0.268 | 0.418 |
| 10000 | 1500 | True | -0.0 | 1.000 | 0.000 | 0.000 | 0.000 | 1 | -2.4555 | 0.5722 | 0.063 | 0.607 | 0.611 | 0.161 | 0.844 |

**insp sr4 c=0 (exploration-capped, not converged where capped=True)** (chain, pi over pairs of monomorphic classes, K = [533, 533])

| N | states | capped | log10 unexplored flux | circulation | pi cycle | pi drift | pi rest | closed classes | u0 | u1 | p / bluff | q / call | readers (1) | mixing 0 | mixing 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 1500 | True | -2.1 | 0.995 | 0.000 | 0.000 | 0.000 | 1 | -0.8347 | -0.2038 | 0.459 | 0.193 | 0.048 | 0.411 | 0.265 |
| 1000 | 1500 | True | -2.0 | 1.000 | 0.000 | 0.000 | 0.000 | 1 | -0.5547 | -0.1232 | 0.318 | 0.120 | 0.086 | 0.297 | 0.177 |
| 10000 | 1500 | True | -0.0 | 1.000 | 0.000 | 0.000 | 0.000 | 1 | -0.7637 | 0.1465 | 0.055 | 0.187 | 1.000 | 1.000 | 1.000 |

**end exact c=0.01 (exploration-capped, not converged where capped=True)** (chain, pi over pairs of monomorphic classes, K = [207, 78])

| N | states | capped | log10 unexplored flux | circulation | pi cycle | pi drift | pi rest | closed classes | u0 | u1 | p / bluff | q / call | readers (1) | mixing 0 | mixing 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 16146 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.1998 | 0.1998 | 0.267 | 0.757 | 0.034 | 0.314 | 0.276 |
| 1000 | 16146 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.1833 | 0.1833 | 0.254 | 0.707 | 0.099 | 0.352 | 0.319 |
| 10000 | 16146 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.1774 | 0.1774 | 0.250 | 0.690 | 0.108 | 0.371 | 0.336 |

**end exact c=0 (exploration-capped, not converged where capped=True)** (chain, pi over pairs of monomorphic classes, K = [201, 72])

| N | states | capped | log10 unexplored flux | circulation | pi cycle | pi drift | pi rest | closed classes | u0 | u1 | p / bluff | q / call | readers (1) | mixing 0 | mixing 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 14472 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.1991 | 0.1991 | 0.268 | 0.754 | 0.039 | 0.318 | 0.281 |
| 1000 | 14472 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.1591 | 0.1591 | 0.282 | 0.647 | 0.196 | 0.482 | 0.433 |
| 10000 | 14472 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.0719 | 0.0719 | 0.361 | 0.563 | 0.310 | 0.825 | 0.718 |

**end blind c=0 (exploration-capped, not converged where capped=True)** (chain, pi over pairs of monomorphic classes, K = [83, 17])

| N | states | capped | log10 unexplored flux | circulation | pi cycle | pi drift | pi rest | closed classes | u0 | u1 | p / bluff | q / call | readers (1) | mixing 0 | mixing 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 1411 | False | n/a | 0.971 | 1.000 | 0.000 | 0.000 | 1 | -0.3321 | 0.3321 | 0.185 | 0.892 | 0.000 | 0.210 | 0.159 |
| 1000 | 1411 | False | n/a | 0.997 | 1.000 | 0.000 | 0.000 | 1 | -0.3030 | 0.3030 | 0.100 | 0.941 | 0.000 | 0.162 | 0.093 |
| 10000 | 1409 | False | -9.8 | 1.000 | 1.000 | 0.000 | 0.000 | 1 | -0.2907 | 0.2907 | 0.091 | 0.946 | 0.000 | 0.174 | 0.087 |

**end sample c=0.01 (exploration-capped, not converged where capped=True)** (chain, pi over pairs of monomorphic classes, K = [113, 47])

| N | states | capped | log10 unexplored flux | circulation | pi cycle | pi drift | pi rest | closed classes | u0 | u1 | p / bluff | q / call | readers (1) | mixing 0 | mixing 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 5311 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.3319 | 0.3319 | 0.182 | 0.890 | 0.017 | 0.210 | 0.162 |
| 1000 | 5311 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.3032 | 0.3032 | 0.099 | 0.940 | 0.010 | 0.162 | 0.096 |
| 10000 | 5311 | False | n/a | n/a | 1.000 | 0.000 | 0.000 | 1 | -0.2907 | 0.2907 | 0.090 | 0.944 | 0.008 | 0.176 | 0.091 |

**end matched c=0.01 (exploration-capped, not converged where capped=True)** (chain, pi over pairs of monomorphic classes, K = [440, 197])

| N | states | capped | log10 unexplored flux | circulation | pi cycle | pi drift | pi rest | closed classes | u0 | u1 | p / bluff | q / call | readers (1) | mixing 0 | mixing 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 1500 | True | -2.2 | 0.976 | 0.000 | 0.000 | 0.000 | 1 | -0.2124 | 0.2124 | 0.283 | 0.752 | 0.005 | 0.310 | 0.380 |
| 1000 | 1500 | True | -2.2 | 0.999 | 0.000 | 0.000 | 0.000 | 1 | -0.2035 | 0.2035 | 0.250 | 0.771 | 0.004 | 0.285 | 0.345 |
| 10000 | 1500 | True | -2.2 | 1.000 | 0.000 | 0.000 | 0.000 | 1 | -0.2019 | 0.2019 | 0.246 | 0.772 | 0.004 | 0.285 | 0.344 |

## Verdicts

## Ablation (not in the spec): which role reads (inspection, lottery, generation 2,000)

| arm | c | inspector payoff | inspectee payoff | inspector readers | inspectee readers | inspector mass p>1/4 | islands at (0,0) | islands committed+compliant |
|---|---|---|---|---|---|---|---|---|
| blind | 0 | -0.981 [-1.049, -0.911] | 0.006 [-0.013, 0.029] | 0.00 | 0.00 | 0.48 | 0.02 | 0.16 |
| exact_ee | 0 | -0.502 [-0.575, -0.439] | -0.006 [-0.014, -0.000] | 0.00 | 0.51 | 0.95 | 0.00 | 0.91 |
| exact_ee | 0.01 | -0.467 [-0.516, -0.425] | -0.000 [-0.003, 0.002] | 0.00 | 0.15 | 0.95 | 0.00 | 0.93 |
| exact_er | 0 | -0.290 [-0.412, -0.182] | 0.046 [0.024, 0.071] | 0.72 | 0.00 | 0.04 | 0.58 | 0.01 |
| exact_er | 0.01 | -0.506 [-0.640, -0.374] | 0.093 [0.066, 0.121] | 0.25 | 0.00 | 0.05 | 0.36 | 0.01 |
| exact | 0 | -0.223 [-0.332, -0.124] | 0.037 [0.015, 0.062] | 0.85 | 0.19 | 0.11 | 0.65 | 0.11 |
| exact | 0.01 | -0.207 [-0.321, -0.106] | 0.037 [0.016, 0.062] | 0.79 | 0.00 | 0.04 | 0.70 | 0.03 |

## Ablation (not in the spec): which role reads (Endgame, lottery, generation 2,000)

| arm | c | value to I | bluff | call | islands both within 0.1 | EQ share | X share | I readers | II readers | exploitability of II | of I |
|---|---|---|---|---|---|---|---|---|---|---|---|
| blind | 0 | -0.149 [-0.201, -0.097] | 0.115 | 0.266 | 0.04 | 0.00 | 0.37 | 0.00 | 0.00 | 0.52 | 0.31 |
| exact_ee | 0 | -0.250 [-0.287, -0.204] | 0.121 | 0.250 | 0.10 | 0.11 | 0.15 | 0.00 | 0.54 | 0.28 | 0.30 |
| exact_ee | 0.01 | -0.208 [-0.262, -0.150] | 0.135 | 0.283 | 0.06 | 0.10 | 0.17 | 0.00 | 0.41 | 0.40 | 0.30 |
| exact_er | 0 | 0.001 [-0.000, 0.003] | 0.374 | 0.499 | 0.12 | 0.00 | 0.91 | 0.61 | 0.00 | 0.06 | 0.09 |
| exact_er | 0.01 | 0.001 [-0.002, 0.004] | 0.252 | 0.504 | 0.14 | 0.00 | 0.88 | 0.23 | 0.00 | 0.07 | 0.20 |
| exact | 0 | -0.180 [-0.229, -0.129] | 0.236 | 0.375 | 0.11 | 0.12 | 0.29 | 0.37 | 0.67 | 0.69 | 0.42 |
| exact | 0.01 | -0.148 [-0.195, -0.104] | 0.148 | 0.390 | 0.15 | 0.13 | 0.41 | 0.09 | 0.54 | 0.51 | 0.28 |

| prediction | verdict | key numbers |
|---|---|---|
| 1 statics | held | table errors 0.0e+00 / 1.1e-16; minimax -1.7e-16 |
| P2 | failed | {"part_a": "failed", "part_b": "failed", "reader_share_c0": [0.1934, 0.1157, 0.2839], "mass_38": 0.025, "mass_12": 0.0625859375, "mass_516": 0.000390625, "u0_c0": [-0.2231, -0.3284, -0.1264], "u0_c001": [-0.2071, -0.3151, -0.1059], "drop": [0.0161, -0.0904, 0.1205], "reader_share_c001": [0.0046, 0.0002, 0.0118], "gpt": {"verdict": "held", "sd_reader_share": 0.2772316661445024, "continuation_change_u0": 0.000953276062011954}, "gemini": {"verdict": "failed", "reader_share": 0.00457421875, "u0": -0.20706640625}} |
| P3 | held | {"u0_blind": [-0.9814, -1.049, -0.9131], "pi_cycle_N1e4": 1.0000000000000002, "circulation": {"100": 0.9977941136715651, "1000": 0.99983570529699, "10000": 0.9999839165072576}, "note": "the weakly improving graph over all pairs is one closed class in every arm: the registered cycle criterion cannot separate arms"} |
| P4 | held | {"means": {"exact": -0.22313213212966926, "sr16": -0.27930386545269326, "sr4": -0.38876614582909824, "matched": -0.5663682800292968}, "gap_exact_minus_matched": [0.3432, 0.1754, 0.5064], "ordering_holds": true, "gpt": {"verdict": "failed", "graded": true}, "gemini": {"verdict": "failed"}} |
| P5 | partial | {"islands_bluff10": 0.303515625, "islands_call10": 0.461328125, "islands_both10": 0.15078125, "value": [-0.1484, -0.1937, -0.1025], "bluff": [0.1476, 0.1094, 0.1891], "call": [0.3896, 0.2956, 0.4838], "winbet": [0.9675, 0.9401, 0.9925]} |
| P6 | failed | {"share_EQ": [0.1277, 0.0305, 0.2305], "share_X": [0.4055, 0.2555, 0.5554], "II_readers": [0.5404, 0.3916, 0.6904], "II_exact_readers": [0.5404, 0.3871, 0.6825]} |
