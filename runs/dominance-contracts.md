# Dominance contracts and refusal on islands: run report (2026-10-14)

Spec `specs/2026-10-14-dominance-contracts.md`; notes `notes/dominance-contracts.md`; predictions `predictions/2026-10-14-dominance-contracts.md`; code `src/dominance_contracts.py`, `src/dominance_contracts_run.py`, `src/dominance_contracts_report.py`. ε = 0 island lottery, I = 64, w = 0.3, weak arm n = 6, length-prior seeds shared with the stable-sets L cells (paired founders). Occupancy = fraction of islands classified (≥ 0.95) on a V\* member; [95% bootstrap over runs]. Support ⊆ V\* (strict) = every island on a member or member-mixed; "ss" = the stable-sets definition (classified islands only).

## Baseline identity (ν = 0 rerun vs the stored stable-sets runs)

- B0: 40/40 runs identical (stop generation, status, migrant births, every horizon's class labels)
- B1: 40/40 runs identical (stop generation, status, migrant births, every horizon's class labels)
- B0-N50: 20/20 runs identical (stop generation, status, migrant births, every horizon's class labels)
- B1-N50: 20/20 runs identical (stop generation, status, migrant births, every horizon's class labels)
- B0-N200: 20/20 runs identical (stop generation, status, migrant births, every horizon's class labels)
- B1-N200: 20/20 runs identical (stop generation, status, migrant births, every horizon's class labels)

## Occupancy and classes

| cell | H | runs | occupancy | modal-play occupancy | paired Δ vs baseline | unequal | wasteful | disagr. | grand | MM | MO | support strict | support ss | coverage | consensus | efficiency | Δ eff |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B0 | 2000 | 40 | 0.281 [0.263, 0.298] | 0.281 [0.263, 0.298] | – | 0.417 | 0.229 | 0.070 | 0.003 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.886 | – |
| B0 | 10000 | 40 | 0.281 [0.263, 0.298] | 0.281 [0.263, 0.298] | – | 0.417 | 0.229 | 0.070 | 0.003 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.886 | – |
| B1 | 2000 | 40 | 0.739 [0.625, 0.850] | 0.843 [0.725, 0.943] | – | 0.138 | 0.000 | 0.000 | 0.000 | 0.097 | 0.026 | 0.82 | 0.82 | 0.00 | 0.65 | 1.000 | – |
| B1 | 10000 | 40 | 0.805 [0.680, 0.910] | 0.825 [0.700, 0.925] | – | 0.175 | 0.000 | 0.000 | 0.000 | 0.020 | 0.000 | 0.82 | 0.82 | 0.00 | 0.95 | 1.000 | – |
| D1-0 | 2000 | 40 | 0.338 [0.318, 0.359] | 0.338 [0.318, 0.359] | 0.057 [0.036, 0.077] | 0.505 | 0.157 | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.974 | +0.087 |
| D1-0 | 10000 | 40 | 0.315 [0.299, 0.330] | 0.315 [0.299, 0.330] | 0.034 [0.009, 0.057] | 0.517 | 0.168 | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.972 | +0.085 |
| D1-1 | 2000 | 40 | 0.091 [0.077, 0.105] | 0.338 [0.315, 0.360] | -0.648 [-0.766, -0.529] | 0.103 | 0.074 | 0.000 | 0.000 | 0.012 | 0.720 | 0.00 | 0.00 | 0.60 | 0.00 | 0.880 | -0.120 |
| D1-1 | 10000 | 40 | 0.084 [0.074, 0.093] | 0.324 [0.303, 0.345] | -0.721 [-0.828, -0.600] | 0.095 | 0.076 | 0.000 | 0.000 | 0.011 | 0.734 | 0.00 | 0.00 | 0.50 | 0.00 | 0.878 | -0.122 |
| R1pub-0 | 2000 | 40 | 0.845 [0.832, 0.856] | 0.845 [0.832, 0.856] | 0.563 [0.542, 0.586] | 0.122 | 0.033 | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.994 | +0.108 |
| R1pub-0 | 10000 | 40 | 0.915 [0.907, 0.923] | 0.915 [0.907, 0.923] | 0.634 [0.616, 0.654] | 0.064 | 0.021 | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.997 | +0.110 |
| R1pub-1 | 2000 | 40 | 0.257 [0.230, 0.282] | 0.862 [0.823, 0.894] | -0.482 [-0.602, -0.359] | 0.014 | 0.016 | 0.000 | 0.000 | 0.211 | 0.502 | 0.00 | 0.38 | 0.97 | 0.00 | 0.934 | -0.066 |
| R1pub-1 | 10000 | 40 | 0.312 [0.293, 0.329] | 0.990 [0.980, 0.996] | -0.493 [-0.602, -0.372] | 0.001 | 0.000 | 0.000 | 0.000 | 0.326 | 0.361 | 0.00 | 0.95 | 1.00 | 0.00 | 0.951 | -0.049 |
| R2-0 | 2000 | 40 | 1.000 [0.999, 1.000] | 1.000 [0.999, 1.000] | 0.718 [0.702, 0.737] | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.97 | 0.97 | 1.00 | 0.00 | 1.000 | +0.113 |
| R2-0 | 10000 | 40 | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.719 [0.702, 0.737] | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.00 | 1.00 | 1.00 | 0.00 | 1.000 | +0.114 |
| R2-1 | 2000 | 40 | 0.331 [0.313, 0.350] | 0.996 [0.994, 0.998] | -0.408 [-0.523, -0.291] | 0.000 | 0.000 | 0.000 | 0.000 | 0.337 | 0.331 | 0.00 | 0.95 | 0.97 | 0.00 | 0.953 | -0.046 |
| R2-1 | 10000 | 40 | 0.316 [0.295, 0.336] | 0.998 [0.996, 0.999] | -0.489 [-0.601, -0.365] | 0.000 | 0.000 | 0.000 | 0.000 | 0.346 | 0.339 | 0.00 | 1.00 | 1.00 | 0.00 | 0.953 | -0.047 |
| R1priv-0 | 2000 | 40 | 0.675 [0.657, 0.691] | 0.675 [0.657, 0.691] | 0.394 [0.371, 0.417] | 0.231 | 0.091 | 0.003 | 0.000 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.981 | +0.095 |
| R1priv-1 | 2000 | 40 | 0.284 [0.266, 0.303] | 0.961 [0.939, 0.978] | -0.455 [-0.571, -0.335] | 0.004 | 0.003 | 0.000 | 0.000 | 0.305 | 0.403 | 0.00 | 0.70 | 1.00 | 0.00 | 0.944 | -0.056 |
| R1blind-0 | 2000 | 40 | 0.332 [0.313, 0.352] | 0.332 [0.313, 0.352] | 0.050 [0.026, 0.077] | 0.509 | 0.160 | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.973 | +0.087 |
| R1blind-1 | 2000 | 40 | 0.091 [0.079, 0.104] | 0.329 [0.309, 0.349] | -0.648 [-0.754, -0.538] | 0.098 | 0.066 | 0.000 | 0.000 | 0.009 | 0.736 | 0.00 | 0.00 | 0.62 | 0.00 | 0.876 | -0.124 |
| D3-0 | 2000 | 40 | 0.398 [0.377, 0.419] | 0.515 [0.497, 0.533] | 0.117 [0.089, 0.144] | 0.250 | 0.043 | 0.000 | 0.000 | 0.001 | 0.308 | 0.00 | 0.00 | 1.00 | 0.00 | 0.947 | +0.060 |
| D3-1 | 2000 | 40 | 0.134 [0.110, 0.158] | 0.764 [0.741, 0.788] | -0.605 [-0.720, -0.492] | 0.002 | 0.000 | 0.000 | 0.000 | 0.049 | 0.815 | 0.00 | 0.85 | 0.17 | 0.00 | 0.864 | -0.136 |
| D4-0 | 2000 | 40 | 0.220 [0.207, 0.234] | 0.220 [0.207, 0.234] | -0.061 [-0.082, -0.041] | 0.375 | 0.388 | 0.016 | 0.002 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.902 | +0.015 |
| D4-1 | 2000 | 40 | 0.399 [0.258, 0.546] | 0.470 [0.320, 0.625] | -0.340 [-0.508, -0.164] | 0.440 | 0.007 | 0.000 | 0.000 | 0.066 | 0.089 | 0.42 | 0.42 | 0.00 | 0.65 | 0.994 | -0.005 |
| B0-N50 | 2000 | 20 | 0.171 [0.155, 0.189] | 0.171 [0.155, 0.189] | – | 0.312 | 0.261 | 0.253 | 0.003 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.696 | – |
| B0-N50 | 10000 | 20 | 0.171 [0.155, 0.189] | 0.171 [0.155, 0.189] | – | 0.312 | 0.261 | 0.253 | 0.003 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.696 | – |
| B1-N50 | 2000 | 20 | 0.837 [0.683, 0.984] | 0.850 [0.700, 1.000] | – | 0.150 | 0.000 | 0.000 | 0.000 | 0.013 | 0.000 | 0.85 | 0.85 | 0.00 | 0.90 | 1.000 | – |
| B1-N50 | 10000 | 20 | 0.826 [0.653, 0.976] | 0.850 [0.700, 1.000] | – | 0.150 | 0.000 | 0.000 | 0.000 | 0.024 | 0.000 | 0.85 | 0.85 | 0.00 | 0.95 | 1.000 | – |
| B0-N200 | 2000 | 20 | 0.407 [0.374, 0.441] | 0.407 [0.374, 0.441] | – | 0.472 | 0.117 | 0.003 | 0.001 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.976 | – |
| B0-N200 | 10000 | 20 | 0.407 [0.374, 0.441] | 0.407 [0.374, 0.441] | – | 0.472 | 0.117 | 0.003 | 0.001 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.976 | – |
| B1-N200 | 2000 | 20 | 0.500 [0.360, 0.644] | 0.715 [0.547, 0.860] | – | 0.216 | 0.000 | 0.000 | 0.000 | 0.144 | 0.141 | 0.00 | 0.40 | 0.10 | 0.00 | 0.988 | – |
| B1-N200 | 10000 | 20 | 0.155 [0.037, 0.306] | 0.249 [0.098, 0.449] | – | 0.750 | 0.000 | 0.000 | 0.000 | 0.093 | 0.002 | 0.20 | 0.25 | 0.00 | 0.85 | 1.000 | – |
| D1-0-N50 | 2000 | 20 | 0.352 [0.325, 0.378] | 0.352 [0.325, 0.378] | 0.180 [0.148, 0.212] | 0.485 | 0.163 | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.973 | +0.277 |
| D1-0-N50 | 10000 | 20 | 0.317 [0.290, 0.341] | 0.317 [0.290, 0.341] | 0.146 [0.113, 0.177] | 0.531 | 0.152 | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.975 | +0.279 |
| D1-1-N50 | 2000 | 20 | 0.042 [0.034, 0.051] | 0.309 [0.279, 0.339] | -0.795 [-0.942, -0.637] | 0.048 | 0.030 | 0.000 | 0.000 | 0.006 | 0.873 | 0.00 | 0.00 | 0.15 | 0.00 | 0.823 | -0.177 |
| D1-1-N50 | 10000 | 20 | 0.042 [0.031, 0.054] | 0.327 [0.300, 0.354] | -0.784 [-0.927, -0.614] | 0.041 | 0.041 | 0.001 | 0.000 | 0.012 | 0.863 | 0.00 | 0.00 | 0.25 | 0.00 | 0.831 | -0.169 |
| D1-0-N200 | 2000 | 20 | 0.355 [0.326, 0.380] | 0.355 [0.326, 0.380] | -0.052 [-0.097, -0.009] | 0.477 | 0.169 | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.972 | -0.005 |
| D1-0-N200 | 10000 | 20 | 0.310 [0.285, 0.334] | 0.310 [0.285, 0.334] | -0.097 [-0.134, -0.059] | 0.522 | 0.168 | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.972 | -0.004 |
| D1-1-N200 | 2000 | 20 | 0.145 [0.125, 0.164] | 0.327 [0.306, 0.348] | -0.355 [-0.497, -0.216] | 0.164 | 0.105 | 0.000 | 0.000 | 0.018 | 0.569 | 0.00 | 0.00 | 0.85 | 0.00 | 0.912 | -0.076 |
| D1-1-N200 | 10000 | 20 | 0.150 [0.131, 0.168] | 0.324 [0.292, 0.353] | -0.005 [-0.152, 0.110] | 0.184 | 0.103 | 0.000 | 0.000 | 0.015 | 0.548 | 0.00 | 0.00 | 0.90 | 0.00 | 0.917 | -0.083 |
| R1pub-0-N50 | 2000 | 20 | 0.851 [0.829, 0.872] | 0.851 [0.829, 0.872] | 0.680 [0.648, 0.709] | 0.111 | 0.038 | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.994 | +0.298 |
| R1pub-0-N50 | 10000 | 20 | 0.912 [0.898, 0.925] | 0.912 [0.898, 0.925] | 0.741 [0.719, 0.761] | 0.066 | 0.023 | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.996 | +0.300 |
| R1pub-1-N50 | 2000 | 20 | 0.152 [0.116, 0.188] | 0.778 [0.709, 0.846] | -0.684 [-0.832, -0.516] | 0.016 | 0.014 | 0.001 | 0.000 | 0.127 | 0.690 | 0.00 | 0.30 | 0.50 | 0.00 | 0.883 | -0.117 |
| R1pub-1-N50 | 10000 | 20 | 0.253 [0.216, 0.293] | 0.942 [0.926, 0.957] | -0.573 [-0.721, -0.398] | 0.001 | 0.002 | 0.000 | 0.000 | 0.242 | 0.502 | 0.00 | 0.90 | 0.70 | 0.00 | 0.924 | -0.076 |
| R1pub-0-N200 | 2000 | 20 | 0.838 [0.816, 0.859] | 0.838 [0.816, 0.859] | 0.431 [0.386, 0.477] | 0.125 | 0.037 | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.994 | +0.017 |
| R1pub-0-N200 | 10000 | 20 | 0.911 [0.896, 0.926] | 0.911 [0.896, 0.926] | 0.504 [0.470, 0.538] | 0.068 | 0.021 | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.996 | +0.020 |
| R1pub-1-N200 | 2000 | 20 | 0.373 [0.341, 0.402] | 0.801 [0.761, 0.835] | -0.127 [-0.257, 0.003] | 0.047 | 0.034 | 0.000 | 0.000 | 0.186 | 0.359 | 0.00 | 0.00 | 1.00 | 0.00 | 0.954 | -0.034 |
| R1pub-1-N200 | 10000 | 20 | 0.459 [0.428, 0.489] | 0.963 [0.931, 0.988] | 0.304 [0.155, 0.424] | 0.005 | 0.006 | 0.000 | 0.000 | 0.348 | 0.182 | 0.00 | 0.70 | 1.00 | 0.00 | 0.971 | -0.028 |
| R1priv-0-N50 | 2000 | 20 | 0.687 [0.661, 0.714] | 0.687 [0.661, 0.714] | 0.516 [0.487, 0.545] | 0.209 | 0.100 | 0.004 | 0.000 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.979 | +0.283 |
| R1priv-1-N50 | 2000 | 20 | 0.220 [0.178, 0.259] | 0.895 [0.812, 0.949] | -0.617 [-0.763, -0.448] | 0.005 | 0.005 | 0.000 | 0.000 | 0.207 | 0.562 | 0.00 | 0.65 | 0.70 | 0.00 | 0.909 | -0.091 |
| R1priv-0-N200 | 2000 | 20 | 0.684 [0.652, 0.716] | 0.684 [0.652, 0.716] | 0.277 [0.237, 0.315] | 0.230 | 0.081 | 0.004 | 0.000 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.982 | +0.006 |
| R1priv-1-N200 | 2000 | 20 | 0.415 [0.367, 0.459] | 0.916 [0.875, 0.953] | -0.085 [-0.221, 0.046] | 0.020 | 0.016 | 0.000 | 0.000 | 0.280 | 0.270 | 0.00 | 0.35 | 1.00 | 0.00 | 0.962 | -0.026 |
| D3p-0 | 2000 | 40 | 0.277 [0.264, 0.292] | 0.409 [0.393, 0.427] | -0.004 [-0.025, 0.017] | 0.243 | 0.050 | 0.000 | 0.000 | 0.005 | 0.424 | 0.00 | 0.00 | 1.00 | 0.00 | 0.917 | +0.031 |
| D3p-1 | 2000 | 40 | 0.025 [0.019, 0.031] | 0.402 [0.379, 0.425] | -0.714 [-0.824, -0.602] | 0.010 | 0.003 | 0.000 | 0.000 | 0.008 | 0.954 | 0.00 | 0.45 | 0.05 | 0.00 | 0.802 | -0.198 |
| D2-0 | 2000 | 40 | 0.345 [0.325, 0.366] | 0.345 [0.325, 0.366] | 0.063 [0.038, 0.088] | 0.496 | 0.159 | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 | 0.00 | 1.00 | 0.00 | 0.973 | +0.087 |
| D2-1 | 2000 | 40 | 0.261 [0.221, 0.305] | 0.679 [0.625, 0.732] | -0.478 [-0.591, -0.356] | 0.048 | 0.007 | 0.000 | 0.000 | 0.089 | 0.595 | 0.00 | 0.23 | 0.12 | 0.00 | 0.929 | -0.071 |

Occupancy at 500 / 1,000 (main cells):

- B0: 500: 0.281, 1000: 0.281
- B1: 500: 0.286, 1000: 0.674
- D1-0: 500: 0.346, 1000: 0.337
- D1-1: 500: 0.077, 1000: 0.095
- R1pub-0: 500: 0.702, 1000: 0.788
- R1pub-1: 500: 0.207, 1000: 0.229
- R2-0: 500: 0.873, 1000: 0.979
- R2-1: 500: 0.327, 1000: 0.336
- R1priv-0: 500: 0.583, 1000: 0.619
- R1priv-1: 500: 0.152, 1000: 0.224
- R1blind-0: 500: 0.324, 1000: 0.332
- R1blind-1: 500: 0.087, 1000: 0.082
- D3-0: 500: 0.365, 1000: 0.401
- D3-1: 500: 0.079, 1000: 0.107
- D4-0: 500: 0.220, 1000: 0.220
- D4-1: 500: 0.202, 1000: 0.332
- D3p-0: 500: 0.285, 1000: 0.269
- D3p-1: 500: 0.028, 1000: 0.030
- D2-0: 500: 0.297, 1000: 0.323
- D2-1: 500: 0.131, 1000: 0.294

## Transition structure

### B0

- contract counters (all runs): {'draws': 0, 'null': 0, 'empty_menu': 0, 'guarded': 0, 'refused': 0, 'installed': 0, 'infeasible': 0, 'overflow': 0}
- guard: {}
- settled transitions by trigger: {'strict P': 38}
- entries into V\* by trigger: {'strict P': 5}; exits from V\*: {}; member-island generations 7151223
- after a member exit, next member same / other: 0 / 0
- contract jump rows (class at the event → class one generation later), with the generator's rows:
- non-contract settled transitions: {'disagreement>wasteful': 15, 'disagreement>unequal': 14, 'disagreement>member': 3, 'wasteful>unequal': 3, 'disagreement>grand': 1, 'wasteful>member': 1, 'unequal>member': 1}
- net circulation n(A→B) − n(B→A): {'disagreement<>wasteful': 15, 'disagreement<>unequal': 14, 'disagreement<>member': 3, 'disagreement<>grand': 1}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {}

### B1

- contract counters (all runs): {'draws': 0, 'null': 0, 'empty_menu': 0, 'guarded': 0, 'refused': 0, 'installed': 0, 'infeasible': 0, 'overflow': 0}
- guard: {}
- settled transitions by trigger: {'migration': 7046, 'strict P': 1, 'drift': 2}
- entries into V\* by trigger: {'migration': 1212}; exits from V\*: {'migration': 562}; member-island generations 19943249
- after a member exit, next member same / other: 60 / 101
- contract jump rows (class at the event → class one generation later), with the generator's rows:
- non-contract settled transitions: {'member>member': 4526, 'unequal>member': 981, 'unequal>unequal': 655, 'member>unequal': 538, 'wasteful>member': 155, 'disagreement>member': 76, 'disagreement>unequal': 37, 'wasteful>unequal': 27, 'unequal>wasteful': 24, 'member>wasteful': 23, 'disagreement>wasteful': 6, 'member>disagreement': 1}
- net circulation n(A→B) − n(B→A): {'disagreement<>member': 75, 'member<>unequal': -443, 'member<>wasteful': -132, 'disagreement<>wasteful': 6, 'unequal<>wasteful': -3, 'disagreement<>unequal': 37}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'M>M>M': 3291, 'U>U>U': 411, 'U>M>U': 60, 'M>U>M': 49, 'U>M>U>U': 11, 'M>W>M': 10, 'M>U>M>M': 5, 'M>M>M>M': 5, 'U>M>M>U': 4, 'M>W>M>M': 3}

### D1-0

- contract counters (all runs): {'draws': 2561332, 'null': 2290833, 'empty_menu': 0, 'guarded': 62839, 'refused': 0, 'installed': 270499, 'infeasible': 853385, 'overflow': 0}
- guard: {'guarded': 62839, 'went_through': 62839}
- settled transitions by trigger: {'contract': 255899, 'strict P': 1}
- entries into V\* by trigger: {'contract': 60292, 'strict P': 1}; exits from V\*: {'contract': 59952}; member-island generations 8515788
- after a member exit, next member same / other: 18952 / 39253
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 59): member 0.153, unequal 0.322, wasteful 0.525 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 62791): member 0.000, unequal 1.000, wasteful 0.000 | generator unequal 1.000
  - member-mixed (n = 2): unequal 1.000 | generator 
  - other-mixed (n = 2341): member 0.170, unequal 0.326, wasteful 0.504 | generator 
  - unequal (n = 141434): member 0.333, unequal 0.334, wasteful 0.333 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 63872): member 0.252, unequal 0.499, wasteful 0.249 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'disagreement>member': 1}
- net circulation n(A→B) − n(B→A): {'member<>unequal': 14178, 'unequal<>wasteful': 13759, 'member<>wasteful': -14510, 'disagreement<>wasteful': 21, 'disagreement<>member': 9, 'disagreement<>unequal': 16}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'long': 11906, 'U>U>M>U': 6709, 'U>M>U>U': 6613, 'M>U>U>M': 6076, 'U>W>M>U': 4915, 'M>U>W>M': 4472, 'U>U>U>U': 4355, 'U>U>W>U': 3249, 'U>W>U>U': 3192, 'U>M>U>M>U': 3049}

### D1-1

- contract counters (all runs): {'draws': 2557167, 'null': 1746226, 'empty_menu': 0, 'guarded': 133511, 'refused': 0, 'installed': 810941, 'infeasible': 852693, 'overflow': 0}
- guard: {'guarded': 133511, 'went_through': 133511}
- settled transitions by trigger: {'contract': 352466, 'contract residue': 503, 'migration': 1095}
- entries into V\* by trigger: {'contract': 72296, 'contract residue': 342, 'migration': 657}; exits from V\*: {'contract': 73044, 'migration': 63, 'contract residue': 17}; member-island generations 2964353
- after a member exit, next member same / other: 23254 / 48155
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 23): member 0.348, unequal 0.217, wasteful 0.435 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 50578): member 0.386, member-mixed 0.003, other-mixed 0.032, unequal 0.318, wasteful 0.262 | generator unequal 1.000
  - member-mixed (n = 6172): member 0.393, member-mixed 0.003, other-mixed 0.029, unequal 0.288, wasteful 0.286 | generator 
  - other-mixed (n = 619186): member 0.243, member-mixed 0.001, other-mixed 0.034, unequal 0.362, wasteful 0.360 | generator 
  - unequal (n = 66807): member 0.136, other-mixed 0.037, unequal 0.473, wasteful 0.354 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 68175): member 0.246, member-mixed 0.001, other-mixed 0.035, unequal 0.330, wasteful 0.389 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'wasteful>member': 816, 'wasteful>unequal': 321, 'unequal>member': 183, 'member>member': 88, 'unequal>unequal': 70, 'member>unequal': 59, 'member>wasteful': 21, 'unequal>wasteful': 20, 'wasteful>wasteful': 19, 'unequal>disagreement': 1}
- net circulation n(A→B) − n(B→A): {'unequal<>wasteful': 3907, 'member<>wasteful': -4144, 'member<>unequal': 3976, 'disagreement<>wasteful': 8, 'disagreement<>member': 3, 'disagreement<>unequal': 2}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'long': 14989, 'M>M>M': 4643, 'U>U>U': 3962, 'M>W>M': 3472, 'M>U>M': 3064, 'U>W>U': 2777, 'U>M>U': 2073, 'W>U>W': 1607, 'W>M>W': 1344, 'M>U>W>M': 1298}

### R1pub-0

- contract counters (all runs): {'draws': 2558082, 'null': 2349910, 'empty_menu': 0, 'guarded': 163321, 'refused': 152015, 'installed': 56157, 'infeasible': 852068, 'overflow': 0}
- guard: {'guarded': 163321, 'refused': 152015, 'drawn_carrier': 152015, 'carriers_present': 152127, 'went_through': 11306}
- settled transitions by trigger: {'contract': 51370}
- entries into V\* by trigger: {'contract': 12651}; exits from V\*: {'contract': 10817}; member-island generations 22054003
- after a member exit, next member same / other: 3444 / 7159
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 55): member 0.218, unequal 0.255, wasteful 0.527 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 11297): member 0.000, unequal 1.000, wasteful 0.000 | generator unequal 1.000
  - member-mixed (n = 1): member 1.000 | generator 
  - other-mixed (n = 2337): member 0.171, unequal 0.323, wasteful 0.506 | generator 
  - unequal (n = 28363): member 0.337, unequal 0.330, wasteful 0.333 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 14104): member 0.255, unequal 0.498, wasteful 0.247 | generator member 0.250, unequal 0.500, wasteful 0.250
- net circulation n(A→B) − n(B→A): {'unequal<>wasteful': 2189, 'member<>unequal': 1486, 'member<>wasteful': -3313, 'disagreement<>wasteful': 17, 'disagreement<>member': 7, 'disagreement<>unequal': 11}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'long': 2022, 'U>U>M>U': 1295, 'M>U>U>M': 1114, 'U>M>U>U': 1085, 'U>W>M>U': 933, 'U>M>U>M>U': 885, 'U>U>U>U': 878, 'M>U>W>M': 805, 'M>U>M>U>M': 708, 'U>U>W>U': 683}
- refusal: {"change": [-0.006947910040616989, -0.017026914469897746, 0.002946716025471687], "below_half_2000": 0.6, "rising": 0.425, "traj": {"0": 0.4987, "250": 0.4913, "500": 0.4918, "1000": 0.4918, "2000": 0.4918, "5000": 0.4918, "10000": 0.4918}, "islands_2000": {"spearman": 0.6309898336853289, "n": 2560, "share_by_fixed_bits": {"0": [0.336, 321], "1": [0.809, 993], "2": [1.0, 954], "3": [1.0, 292]}, "share_by_protection": {"prot_pub=True": [0.989, 1873], "prot_priv=False": [0.933, 1539], "prot_priv=True": [1.0, 623], "prot_pub=False": [0.712, 289]}}, "islands_10000": {"spearman": 0.5797811877617771, "n": 2560, "share_by_fixed_bits": {"0": [0.36, 321], "1": [0.992, 993], "2": [1.0, 954], "3": [1.0, 292]}, "share_by_protection": {"prot_pub=True": [1.0, 2228], "prot_priv=False": [0.972, 1720], "prot_priv=True": [1.0, 623], "prot_pub=False": [0.594, 115]}}}

### R1pub-1

- contract counters (all runs): {'draws': 2558591, 'null': 1852169, 'empty_menu': 0, 'guarded': 395716, 'refused': 380038, 'installed': 326384, 'infeasible': 852602, 'overflow': 0}
- guard: {'guarded': 395716, 'refused': 380038, 'drawn_carrier': 380038, 'carriers_present': 395276, 'went_through': 15678}
- settled transitions by trigger: {'contract': 169442, 'migration': 11468, 'contract residue': 2805}
- entries into V\* by trigger: {'contract': 12380, 'contract residue': 386, 'migration': 486}; exits from V\*: {'contract': 11562, 'migration': 17, 'contract residue': 6}; member-island generations 15002544
- after a member exit, next member same / other: 3800 / 7752
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 10): other-mixed 0.100, unequal 0.300, wasteful 0.600 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 65913): member 0.929, member-mixed 0.010, other-mixed 0.006, unequal 0.030, wasteful 0.025 | generator unequal 1.000
  - member-mixed (n = 75315): member 0.953, member-mixed 0.010, other-mixed 0.004, unequal 0.016, wasteful 0.016 | generator 
  - other-mixed (n = 170285): member 0.657, member-mixed 0.006, other-mixed 0.018, unequal 0.156, wasteful 0.163 | generator 
  - unequal (n = 6763): member 0.134, other-mixed 0.039, unequal 0.466, wasteful 0.361 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 8098): member 0.253, member-mixed 0.002, other-mixed 0.035, unequal 0.333, wasteful 0.377 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'member>member': 13364, 'wasteful>member': 706, 'unequal>member': 165, 'member>wasteful': 12, 'member>unequal': 11, 'wasteful>unequal': 7, 'wasteful>wasteful': 7, 'disagreement>member': 1}
- net circulation n(A→B) − n(B→A): {'unequal<>wasteful': 898, 'member<>unequal': 69, 'member<>wasteful': -1732, 'disagreement<>member': 4, 'disagreement<>unequal': 3, 'disagreement<>wasteful': 7}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'M>M>M': 68437, 'M>M>M>M': 29259, 'M>W>M': 1012, 'long': 937, 'M>W>M>M': 875, 'M>M>W>M': 846, 'M>U>M': 730, 'M>U>M>M': 623, 'M>M>U>M': 571, 'M>W>M>M>M': 271}
- refusal: {"change": [0.29917710050940516, 0.2597799015417695, 0.3417551887594163], "below_half_2000": 0.1, "rising": 1.0, "traj": {"0": 0.4994, "250": 0.5075, "500": 0.5304, "1000": 0.5845, "2000": 0.6682, "5000": 0.7592, "10000": 0.7986}, "islands_2000": {"spearman": 0.19669388661780063, "n": 2560, "share_by_fixed_bits": {"1": [0.206, 10], "2": [0.281, 35], "3": [0.338, 30]}, "share_by_protection": {"prot_pub=True": [0.356, 32], "prot_priv=False": [0.346, 12], "prot_priv=True": [0.362, 20]}}, "islands_10000": {"spearman": 0.033502982854760686, "n": 2560, "share_by_fixed_bits": {"1": [0.178, 2], "2": [0.324, 957], "3": [0.327, 635]}, "share_by_protection": {"prot_pub=True": [0.355, 531], "prot_priv=True": [0.354, 299], "prot_priv=False": [0.357, 232]}}}

### R2-0

- contract counters (all runs): {'draws': 2559646, 'null': 2364719, 'empty_menu': 0, 'guarded': 185617, 'refused': 185617, 'installed': 9310, 'infeasible': 853213, 'overflow': 0}
- guard: {'guarded': 185617, 'refused': 185617, 'drawn_carrier': 185617, 'carriers_present': 185617}
- settled transitions by trigger: {'contract': 6576, 'strict P': 1}
- entries into V\* by trigger: {'contract': 2007}; exits from V\*: {}; member-island generations 25026727
- after a member exit, next member same / other: 0 / 0
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 57): member 0.140, unequal 0.333, wasteful 0.526 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 4): member 1.000 | generator unequal 1.000
  - member-mixed (n = 1): member 1.000 | generator 
  - other-mixed (n = 2316): member 0.178, unequal 0.322, wasteful 0.500 | generator 
  - unequal (n = 3622): member 0.327, unequal 0.333, wasteful 0.340 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 3310): member 0.261, unequal 0.478, wasteful 0.261 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'disagreement>unequal': 1}
- net circulation n(A→B) − n(B→A): {'unequal<>wasteful': -320, 'disagreement<>unequal': 17, 'disagreement<>wasteful': 20, 'disagreement<>member': 7}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'U>U>U>U': 110, 'U>W>U>U': 97, 'U>U>W>U': 88, 'W>U>U>W': 69, 'U>W>W>U': 64, 'W>U>W>W': 47, 'W>W>U>W': 46, 'W>W>W>W': 41, 'U>U>U': 21, 'U>W>U>W>U': 20}
- refusal: {"change": [0.0, 0.0, 0.0], "below_half_2000": 0.0, "rising": 0.0, "traj": {"0": 1.0, "250": 1.0, "500": 1.0, "1000": 1.0, "2000": 1.0, "5000": 1.0, "10000": 1.0}, "islands_2000": {"spearman": NaN, "n": 2560, "share_by_fixed_bits": {"3": [0.999, 2560]}, "share_by_protection": {"prot_pub=True": [1.0, 2559], "prot_priv=True": [1.0, 2559]}}, "islands_10000": {"spearman": NaN, "n": 2560, "share_by_fixed_bits": {"3": [1.0, 2560]}, "share_by_protection": {"prot_pub=True": [1.0, 2560], "prot_priv=True": [1.0, 2560]}}}

### R2-1

- contract counters (all runs): {'draws': 2560268, 'null': 1865707, 'empty_menu': 0, 'guarded': 428818, 'refused': 428818, 'installed': 265743, 'infeasible': 852951, 'overflow': 0}
- guard: {'guarded': 428818, 'refused': 428818, 'drawn_carrier': 428818, 'carriers_present': 428818}
- settled transitions by trigger: {'contract': 146073, 'migration': 14135, 'contract residue': 2941}
- entries into V\* by trigger: {'contract': 2056, 'contract residue': 61, 'migration': 82}; exits from V\*: {'contract': 622, 'migration': 4, 'contract residue': 1}; member-island generations 16620035
- after a member exit, next member same / other: 222 / 401
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 20): member 0.300, unequal 0.350, wasteful 0.350 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 68154): member 0.988, member-mixed 0.010, other-mixed 0.002 | generator unequal 1.000
  - member-mixed (n = 90740): member 0.987, member-mixed 0.011, other-mixed 0.002 | generator 
  - other-mixed (n = 104373): member 0.895, member-mixed 0.009, other-mixed 0.007, unequal 0.042, wasteful 0.047 | generator 
  - unequal (n = 1073): member 0.121, other-mixed 0.039, unequal 0.460, wasteful 0.379 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 1383): member 0.234, member-mixed 0.001, other-mixed 0.032, unequal 0.341, wasteful 0.393 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'member>member': 16925, 'wasteful>member': 107, 'unequal>member': 36, 'member>wasteful': 3, 'member>unequal': 2, 'wasteful>unequal': 1, 'unequal>wasteful': 1, 'unequal>unequal': 1}
- net circulation n(A→B) − n(B→A): {'unequal<>wasteful': 67, 'member<>wasteful': -856, 'member<>unequal': -711, 'disagreement<>unequal': 4, 'disagreement<>member': 5, 'disagreement<>wasteful': 5}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'M>M>M': 79960, 'M>M>M>M': 35754, 'M>W>M>M': 82, 'M>W>M': 78, 'M>M>W>M': 72, 'M>U>M': 47, 'M>U>M>M': 36, 'M>W>M>M>M': 30, 'M>M>U>M': 30, 'U>U>U': 24}
- refusal: {"change": [0.0, 0.0, 0.0], "below_half_2000": 0.0, "rising": 0.0, "traj": {"0": 1.0, "250": 1.0, "500": 1.0, "1000": 1.0, "2000": 1.0, "5000": 1.0, "10000": 1.0}, "islands_2000": {"spearman": NaN, "n": 2560, "share_by_fixed_bits": {"3": [0.329, 2560]}, "share_by_protection": {"prot_pub=True": [0.357, 848], "prot_priv=True": [0.357, 848]}}, "islands_10000": {"spearman": NaN, "n": 2560, "share_by_fixed_bits": {"3": [0.326, 2560]}, "share_by_protection": {"prot_pub=True": [0.354, 808], "prot_priv=True": [0.354, 808]}}}

### R1priv-0

- contract counters (all runs): {'draws': 512014, 'null': 460000, 'empty_menu': 0, 'guarded': 22084, 'refused': 0, 'installed': 52014, 'infeasible': 170912, 'overflow': 0}
- guard: {'guarded': 22084, 'went_through': 22084, 'carriers_present': 17731}
- settled transitions by trigger: {'contract': 32206}
- entries into V\* by trigger: {'contract': 7770}; exits from V\*: {'contract': 6551}; member-island generations 3013202
- after a member exit, next member same / other: 1826 / 3888
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 2323): member 0.163, unequal 0.341, wasteful 0.496 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 22002): disagreement 0.103, member 0.683, other-mixed 0.012, unequal 0.201 | generator unequal 1.000
  - member-mixed (n = 1): member 1.000 | generator 
  - other-mixed (n = 2550): disagreement 0.001, member 0.175, other-mixed 0.029, unequal 0.318, wasteful 0.477 | generator 
  - unequal (n = 15411): member 0.333, unequal 0.336, wasteful 0.331 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 9727): member 0.267, unequal 0.479, wasteful 0.254 | generator member 0.250, unequal 0.500, wasteful 0.250
- net circulation n(A→B) − n(B→A): {'disagreement<>wasteful': 815, 'unequal<>wasteful': 402, 'member<>unequal': -461, 'disagreement<>unequal': 580, 'member<>wasteful': -2127, 'disagreement<>member': -1369}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'long': 1056, 'U>U>M>U': 493, 'U>U>U>U': 452, 'M>U>U>M': 405, 'U>W>M>U': 397, 'U>M>U>M>U': 357, 'U>M>U>U': 325, 'M>U>W>M': 295, 'U>U>W>U': 294, 'M>U>M>U>M': 284}
- refusal: {"change": [-0.01111457273364067, -0.022398426458239553, 0.00018155671656130731], "below_half_2000": 0.6, "rising": 0.375, "traj": {"0": 0.4987, "250": 0.4881, "500": 0.4876, "1000": 0.4876, "2000": 0.4876}, "islands_2000": {"spearman": 0.6703029327843574, "n": 2560, "share_by_fixed_bits": {"0": [0.332, 351], "1": [0.486, 976], "2": [0.881, 930], "3": [1.0, 303]}, "share_by_protection": {"prot_pub=True": [0.945, 1200], "prot_priv=False": [0.684, 704], "prot_priv=True": [0.99, 1024], "prot_pub=False": [0.683, 528]}}}

### R1priv-1

- contract counters (all runs): {'draws': 511985, 'null': 360361, 'empty_menu': 0, 'guarded': 65476, 'refused': 0, 'installed': 151624, 'infeasible': 170138, 'overflow': 0}
- guard: {'guarded': 65476, 'went_through': 65476, 'carriers_present': 65435}
- settled transitions by trigger: {'contract': 41300, 'contract residue': 123, 'migration': 324}
- entries into V\* by trigger: {'contract': 6198, 'migration': 112, 'contract residue': 70}; exits from V\*: {'contract': 4729, 'migration': 6, 'contract residue': 3}; member-island generations 2207474
- after a member exit, next member same / other: 1552 / 3107
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 127): member 0.157, other-mixed 0.024, unequal 0.299, wasteful 0.520 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 23810): disagreement 0.005, member 0.708, member-mixed 0.056, other-mixed 0.227, unequal 0.002, wasteful 0.002 | generator unequal 1.000
  - member-mixed (n = 18954): disagreement 0.001, member 0.425, member-mixed 0.360, other-mixed 0.212, unequal 0.001, wasteful 0.001 | generator 
  - other-mixed (n = 100766): disagreement 0.002, member 0.311, member-mixed 0.019, other-mixed 0.375, unequal 0.142, wasteful 0.152 | generator 
  - unequal (n = 3552): member 0.144, other-mixed 0.037, unequal 0.463, wasteful 0.356 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 4415): member 0.255, member-mixed 0.001, other-mixed 0.035, unequal 0.325, wasteful 0.383 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'member>member': 238, 'wasteful>member': 133, 'unequal>member': 45, 'wasteful>unequal': 11, 'member>wasteful': 6, 'disagreement>member': 4, 'wasteful>wasteful': 3, 'member>unequal': 3, 'unequal>wasteful': 2, 'unequal>unequal': 2}
- net circulation n(A→B) − n(B→A): {'unequal<>wasteful': 329, 'member<>wasteful': -1170, 'disagreement<>member': -42, 'member<>unequal': -514, 'disagreement<>unequal': 34, 'disagreement<>wasteful': 22}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'M>M>M': 8744, 'M>M>M>M': 3123, 'long': 468, 'M>W>M': 393, 'M>U>M': 279, 'M>W>M>M': 275, 'M>M>W>M': 213, 'M>U>M>M': 202, 'M>M>U>M': 152, 'U>U>U': 120}
- refusal: {"change": [0.4601250097155571, 0.4397571414895356, 0.47614502822980287], "below_half_2000": 0.0, "rising": 1.0, "traj": {"0": 0.4994, "250": 0.5334, "500": 0.5837, "1000": 0.7256, "2000": 0.9596}, "islands_2000": {"spearman": 0.14788858794708962, "n": 2560, "share_by_fixed_bits": {"2": [0.25, 5], "3": [0.313, 1739]}, "share_by_protection": {"prot_pub=True": [0.341, 529], "prot_priv=True": [0.341, 527], "prot_priv=False": [0.2, 2]}}}

### R1blind-0

- contract counters (all runs): {'draws': 512262, 'null': 456274, 'empty_menu': 0, 'guarded': 12323, 'refused': 0, 'installed': 55988, 'infeasible': 171136, 'overflow': 0}
- guard: {'guarded': 12323, 'went_through': 12323, 'carriers_present': 9233}
- settled transitions by trigger: {'contract': 50970}
- entries into V\* by trigger: {'contract': 12052}; exits from V\*: {'contract': 11676}; member-island generations 1657953
- after a member exit, next member same / other: 3238 / 6736
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 55): member 0.255, unequal 0.236, wasteful 0.509 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 12290): member 0.000, unequal 1.000, wasteful 0.000 | generator unequal 1.000
  - other-mixed (n = 2356): member 0.168, unequal 0.332, wasteful 0.500 | generator 
  - unequal (n = 27911): member 0.334, unequal 0.334, wasteful 0.332 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 13376): member 0.250, unequal 0.504, wasteful 0.245 | generator member 0.250, unequal 0.500, wasteful 0.250
- net circulation n(A→B) − n(B→A): {'member<>unequal': 2622, 'unequal<>wasteful': 2228, 'member<>wasteful': -2991, 'disagreement<>member': 7, 'disagreement<>wasteful': 20, 'disagreement<>unequal': 8}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'long': 1485, 'U>U>M>U': 1177, 'U>M>U>U': 1166, 'M>U>U>M': 1066, 'U>W>M>U': 866, 'M>U>W>M': 810, 'U>U>U>U': 765, 'U>W>U>U': 606, 'U>U>W>U': 605, 'U>M>U>M>U': 516}
- refusal: {"change": [-0.006296867132186889, -0.017249205838888882, 0.005221526175737373], "below_half_2000": 0.65, "rising": 0.35, "traj": {"0": 0.4987, "250": 0.4925, "500": 0.4925, "1000": 0.4925, "2000": 0.4925}, "islands_2000": {"spearman": 0.024571802697539318, "n": 2560, "share_by_fixed_bits": {"0": [0.34, 330], "1": [0.311, 997], "2": [0.342, 914], "3": [0.346, 319]}, "share_by_protection": {"prot_pub=True": [0.548, 536], "prot_priv=False": [0.55, 631], "prot_pub=False": [0.546, 313], "prot_priv=True": [0.541, 218]}}}

### R1blind-1

- contract counters (all runs): {'draws': 512098, 'null': 349009, 'empty_menu': 0, 'guarded': 26399, 'refused': 0, 'installed': 163089, 'infeasible': 170222, 'overflow': 0}
- guard: {'guarded': 26399, 'went_through': 26399, 'carriers_present': 26081}
- settled transitions by trigger: {'contract': 68387, 'contract residue': 101, 'migration': 210}
- entries into V\* by trigger: {'contract': 14139, 'contract residue': 75, 'migration': 144}; exits from V\*: {'contract': 14159, 'migration': 13, 'contract residue': 3}; member-island generations 590349
- after a member exit, next member same / other: 4098 / 8376
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 9): other-mixed 0.111, unequal 0.667, wasteful 0.222 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 10256): member 0.392, member-mixed 0.003, other-mixed 0.030, unequal 0.320, wasteful 0.255 | generator unequal 1.000
  - member-mixed (n = 1226): member 0.386, member-mixed 0.004, other-mixed 0.036, unequal 0.272, wasteful 0.302 | generator 
  - other-mixed (n = 124541): member 0.243, member-mixed 0.001, other-mixed 0.034, unequal 0.360, wasteful 0.362 | generator 
  - unequal (n = 13206): member 0.140, other-mixed 0.037, unequal 0.467, wasteful 0.357 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 13851): member 0.249, member-mixed 0.002, other-mixed 0.033, unequal 0.328, wasteful 0.389 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'wasteful>member': 182, 'wasteful>unequal': 41, 'unequal>member': 37, 'unequal>unequal': 14, 'member>member': 13, 'member>unequal': 13, 'wasteful>wasteful': 4, 'unequal>wasteful': 4, 'member>wasteful': 3}
- net circulation n(A→B) − n(B→A): {'unequal<>wasteful': 768, 'member<>unequal': 823, 'member<>wasteful': -1001, 'disagreement<>member': 5, 'disagreement<>wasteful': 5, 'disagreement<>unequal': 5}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'long': 2195, 'M>M>M': 935, 'U>U>U': 775, 'M>W>M': 720, 'M>U>M': 598, 'U>W>U': 539, 'U>M>U': 384, 'W>U>W': 309, 'W>M>W': 262, 'M>U>W>M': 228}
- refusal: {"change": [-0.008408847451210021, -0.05259536331519485, 0.03551504410803318], "below_half_2000": 0.55, "rising": 0.45, "traj": {"0": 0.4994, "250": 0.5032, "500": 0.5061, "1000": 0.5109, "2000": 0.491}, "islands_2000": {"spearman": 0.003952008835594362, "n": 2560, "share_by_fixed_bits": {"0": [0.07, 14], "1": [0.066, 22], "2": [0.093, 55], "3": [0.141, 7]}, "share_by_protection": {"prot_pub=False": [0.111, 4], "prot_priv=False": [0.112, 10], "prot_pub=True": [0.124, 11], "prot_priv=True": [0.139, 5]}}}

### D3-0

- contract counters (all runs): {'draws': 512906, 'null': 415395, 'empty_menu': 0, 'guarded': 26330, 'refused': 0, 'installed': 97511, 'infeasible': 170413, 'overflow': 0}
- guard: {'guarded': 26330, 'went_through': 26330}
- settled transitions by trigger: {'contract': 10119, 'contract residue': 34}
- entries into V\* by trigger: {'contract': 3130, 'contract residue': 6}; exits from V\*: {'contract': 2709, 'contract residue': 12}; member-island generations 2119617
- after a member exit, next member same / other: 445 / 1161
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 116): disagreement 0.078, other-mixed 0.922 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 15095): member 0.011, member-mixed 0.002, other-mixed 0.986 | generator unequal 1.000
  - member-mixed (n = 529): member 0.015, member-mixed 0.070, other-mixed 0.915 | generator 
  - other-mixed (n = 62663): member 0.002, member-mixed 0.000, other-mixed 0.995, unequal 0.002, wasteful 0.000 | generator 
  - unequal (n = 15006): other-mixed 0.989, unequal 0.011 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 4102): other-mixed 0.987, wasteful 0.013 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'member>unequal': 12, 'unequal>member': 5, 'unequal>wasteful': 5, 'unequal>unequal': 5, 'wasteful>wasteful': 2, 'wasteful>unequal': 2, 'member>member': 2, 'wasteful>member': 1}
- net circulation n(A→B) − n(B→A): {'unequal<>wasteful': 251, 'member<>unequal': 90, 'member<>wasteful': -483, 'disagreement<>member': 22, 'disagreement<>unequal': 34, 'disagreement<>wasteful': 7}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'M>U>U>M': 158, 'M>U>M': 122, 'U>U>M>U': 108, 'U>M>U>U': 107, 'U>U>U': 78, 'U>M>U': 74, 'U>U>U>U': 69, 'M>U>W>M': 47, 'M>U>M>U>M': 37, 'U>U>W>U': 33}
- β < 1 fates by edge class: {'other-mixed>wasteful': {'lost': 3164, 'superseded': 19119, 'joint': 465, 'one-sided': 2163, 'open': 229}, 'other-mixed>unequal': {'superseded': 16348, 'joint': 1824, 'lost': 3048, 'one-sided': 1072, 'open': 221}, 'other-mixed>member': {'superseded': 10651, 'lost': 1864, 'joint': 1523, 'one-sided': 811, 'open': 161}, 'member>member': {'superseded': 293, 'joint': 170, 'lost': 119, 'one-sided': 59, 'open': 9}, 'unequal>member': {'superseded': 3238, 'lost': 779, 'one-sided': 407, 'joint': 222, 'open': 68}, 'member-mixed>unequal': {'superseded': 146, 'lost': 55, 'open': 2, 'one-sided': 10, 'joint': 3}, 'unequal>wasteful': {'superseded': 3454, 'lost': 934, 'one-sided': 491, 'joint': 116, 'open': 76}, 'wasteful>member': {'superseded': 774, 'joint': 54, 'one-sided': 70, 'lost': 118, 'open': 13}, 'unequal>unequal': {'lost': 1033, 'superseded': 3358, 'one-sided': 282, 'joint': 473, 'open': 75}, 'wasteful>wasteful': {'lost': 136, 'superseded': 850, 'one-sided': 62, 'joint': 55, 'open': 8}, 'member>unequal': {'superseded': 8001, 'lost': 3633, 'joint': 508, 'one-sided': 1615, 'open': 249}, 'wasteful>unequal': {'superseded': 1428, 'lost': 316, 'one-sided': 103, 'joint': 94, 'open': 21}, 'member>wasteful': {'superseded': 279, 'lost': 89, 'one-sided': 62, 'open': 8, 'joint': 1}, 'member-mixed>wasteful': {'lost': 43, 'superseded': 132, 'joint': 1, 'open': 3, 'one-sided': 6}, 'member-mixed>member': {'superseded': 81, 'one-sided': 7, 'lost': 21, 'joint': 17, 'open': 2}, 'disagreement>wasteful': {'superseded': 43, 'joint': 2, 'one-sided': 3}, 'disagreement>unequal': {'superseded': 38, 'joint': 5, 'lost': 1}, 'disagreement>member': {'superseded': 23, 'joint': 1}}

### D3-1

- contract counters (all runs): {'draws': 511780, 'null': 325548, 'empty_menu': 0, 'guarded': 76096, 'refused': 0, 'installed': 186232, 'infeasible': 170422, 'overflow': 0}
- guard: {'guarded': 76096, 'went_through': 76096}
- settled transitions by trigger: {'contract': 5430, 'migration': 49, 'contract residue': 14}
- entries into V\* by trigger: {'contract': 888, 'migration': 6, 'contract residue': 4}; exits from V\*: {'contract': 600, 'migration': 6, 'contract residue': 1}; member-island generations 1997210
- after a member exit, next member same / other: 190 / 258
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 29): disagreement 0.034, other-mixed 0.966 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 11049): member 0.105, member-mixed 0.034, other-mixed 0.861 | generator unequal 1.000
  - member-mixed (n = 6481): member 0.029, member-mixed 0.143, other-mixed 0.828 | generator 
  - other-mixed (n = 168012): member 0.003, member-mixed 0.004, other-mixed 0.992, unequal 0.000, wasteful 0.000 | generator 
  - unequal (n = 508): other-mixed 0.933, unequal 0.067 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 153): other-mixed 0.974, wasteful 0.026 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'member>member': 46, 'unequal>member': 6, 'member>unequal': 5, 'wasteful>member': 4, 'member>wasteful': 2}
- net circulation n(A→B) − n(B→A): {'member<>wasteful': -68, 'member<>unequal': -210, 'disagreement<>member': 13, 'disagreement<>unequal': 4, 'unequal<>wasteful': 8, 'disagreement<>wasteful': 1}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'M>M>M': 1122, 'M>U>M': 135, 'M>M>M>M': 121, 'M>W>M': 49, 'M>U>M>M': 46, 'M>M>U>M': 33, 'M>M>W>M': 20, 'U>M>U': 14, 'M>W>M>M': 11, 'M>M>M>U>M': 8}
- β < 1 fates by edge class: {'other-mixed>wasteful': {'superseded': 59074, 'lost': 5592, 'one-sided': 1753, 'joint': 37, 'open': 641}, 'other-mixed>member': {'superseded': 39613, 'one-sided': 546, 'lost': 2027, 'joint': 2596, 'open': 556}, 'other-mixed>unequal': {'superseded': 46861, 'joint': 184, 'lost': 7570, 'one-sided': 370, 'open': 592}, 'member>member': {'lost': 292, 'joint': 862, 'superseded': 2951, 'one-sided': 87, 'open': 61}, 'wasteful>unequal': {'superseded': 36, 'lost': 8, 'one-sided': 1}, 'member>wasteful': {'lost': 484, 'superseded': 2344, 'one-sided': 57, 'open': 68, 'joint': 1}, 'member>unequal': {'superseded': 2909, 'lost': 799, 'one-sided': 65, 'open': 65, 'joint': 4}, 'member-mixed>wasteful': {'superseded': 1700, 'lost': 311, 'open': 42, 'one-sided': 40}, 'unequal>unequal': {'superseded': 194, 'lost': 24, 'joint': 13, 'one-sided': 2, 'open': 3}, 'member-mixed>unequal': {'superseded': 1455, 'lost': 472, 'one-sided': 16, 'open': 21}, 'unequal>wasteful': {'superseded': 172, 'lost': 16, 'one-sided': 5, 'open': 3}, 'member-mixed>member': {'superseded': 1937, 'joint': 252, 'lost': 156, 'open': 28, 'one-sided': 51}, 'unequal>member': {'superseded': 68, 'lost': 8}, 'wasteful>wasteful': {'superseded': 50, 'lost': 9, 'joint': 2}, 'disagreement>member': {'superseded': 10}, 'disagreement>wasteful': {'superseded': 11, 'one-sided': 1}, 'wasteful>member': {'superseded': 43, 'lost': 4}, 'disagreement>unequal': {'superseded': 7}}

### D4-0

- contract counters (all runs): {'draws': 511657, 'null': 141280, 'empty_menu': 368137, 'guarded': 50, 'refused': 0, 'installed': 2240, 'infeasible': 43170, 'overflow': 0}
- guard: {'guarded': 50, 'went_through': 50}
- settled transitions by trigger: {'contract': 252, 'strict P': 8}
- entries into V\* by trigger: {'contract': 68, 'strict P': 1}; exits from V\*: {'contract': 29}; member-island generations 1108118
- after a member exit, next member same / other: 0 / 2
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 27): member 0.259, unequal 0.185, wasteful 0.556 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 34): unequal 1.000 | generator unequal 1.000
  - other-mixed (n = 1906): member 0.164, unequal 0.335, wasteful 0.501 | generator 
  - unequal (n = 88): member 0.250, unequal 0.443, wasteful 0.307 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 185): member 0.351, unequal 0.378, wasteful 0.270 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'disagreement>unequal': 3, 'disagreement>grand': 3, 'disagreement>member': 1, 'wasteful>unequal': 1}
- net circulation n(A→B) − n(B→A): {'member<>unequal': 10, 'disagreement<>unequal': 8, 'unequal<>wasteful': -38, 'disagreement<>wasteful': 7, 'disagreement<>member': 3, 'disagreement<>grand': 3}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'W>U>W': 1}
- menu G: {'size': {'0': 18.163, '100': 0.402, '250': 0.292, '500': 0.287, '1000': 0.287, '2000': 0.287}, 'coverage': {'0': nan, '100': 0.0, '250': 0.0, '500': 0.0, '1000': 0.0, '2000': 0.0}}

### D4-1

- contract counters (all runs): {'draws': 512388, 'null': 290083, 'empty_menu': 176661, 'guarded': 3384, 'refused': 0, 'installed': 45644, 'infeasible': 105256, 'overflow': 0}
- guard: {'guarded': 3384, 'went_through': 3384}
- settled transitions by trigger: {'migration': 2588, 'contract': 12429, 'contract residue': 460}
- entries into V\* by trigger: {'contract': 2391, 'contract residue': 202, 'migration': 629}; exits from V\*: {'contract residue': 66, 'contract': 2161, 'migration': 376}; member-island generations 1843075
- after a member exit, next member same / other: 1156 / 526
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 14): member 0.071, unequal 0.429, wasteful 0.500 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 4870): member 0.798, member-mixed 0.002, other-mixed 0.011, unequal 0.081, wasteful 0.109 | generator unequal 1.000
  - member-mixed (n = 578): member 0.808, member-mixed 0.002, other-mixed 0.012, unequal 0.043, wasteful 0.135 | generator 
  - other-mixed (n = 28891): member 0.216, member-mixed 0.001, other-mixed 0.027, unequal 0.447, wasteful 0.309 | generator 
  - unequal (n = 7738): member 0.032, other-mixed 0.019, unequal 0.845, wasteful 0.104 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 3553): member 0.098, other-mixed 0.030, unequal 0.188, wasteful 0.683 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'unequal>unequal': 769, 'member>member': 633, 'wasteful>member': 540, 'member>unequal': 415, 'unequal>member': 290, 'wasteful>unequal': 264, 'unequal>wasteful': 91, 'member>wasteful': 27, 'wasteful>wasteful': 16, 'unequal>disagreement': 1, 'disagreement>unequal': 1, 'disagreement>member': 1}
- net circulation n(A→B) − n(B→A): {'unequal<>wasteful': -151, 'member<>unequal': 79, 'member<>wasteful': -694, 'disagreement<>member': 4, 'disagreement<>wasteful': 8, 'disagreement<>unequal': 5}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'U>U>U': 1450, 'M>M>M': 678, 'U>W>U': 454, 'M>W>M': 411, 'W>U>W': 293, 'W>M>W': 241, 'M>U>M': 228, 'U>M>U': 205, 'M>U>U>M': 146, 'W>W>W': 144}
- menu G: {'size': {'0': 18.147, '100': 1.386, '250': 1.325, '500': 1.245, '1000': 0.923, '2000': 0.812}, 'coverage': {'0': nan, '100': 0.025, '250': 0.022, '500': 0.006, '1000': 0.008, '2000': 0.004}}

### B0-N50

- contract counters (all runs): {'draws': 0, 'null': 0, 'empty_menu': 0, 'guarded': 0, 'refused': 0, 'installed': 0, 'infeasible': 0, 'overflow': 0}
- guard: {}
- settled transitions by trigger: {'strict P': 6}
- entries into V\* by trigger: {}; exits from V\*: {}; member-island generations 2180609
- after a member exit, next member same / other: 0 / 0
- contract jump rows (class at the event → class one generation later), with the generator's rows:
- non-contract settled transitions: {'disagreement>unequal': 5, 'disagreement>wasteful': 1}
- net circulation n(A→B) − n(B→A): {'disagreement<>unequal': 5, 'disagreement<>wasteful': 1}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {}

### B1-N50

- contract counters (all runs): {'draws': 0, 'null': 0, 'empty_menu': 0, 'guarded': 0, 'refused': 0, 'installed': 0, 'infeasible': 0, 'overflow': 0}
- guard: {}
- settled transitions by trigger: {'migration': 2422}
- entries into V\* by trigger: {'migration': 437}; exits from V\*: {'migration': 83}; member-island generations 10367122
- after a member exit, next member same / other: 30 / 6
- contract jump rows (class at the event → class one generation later), with the generator's rows:
- non-contract settled transitions: {'member>member': 1790, 'unequal>member': 244, 'disagreement>member': 131, 'member>unequal': 75, 'wasteful>member': 62, 'disagreement>unequal': 46, 'unequal>unequal': 37, 'wasteful>unequal': 15, 'disagreement>wasteful': 10, 'member>wasteful': 8, 'unequal>wasteful': 3, 'wasteful>wasteful': 1}
- net circulation n(A→B) − n(B→A): {'disagreement<>unequal': 46, 'disagreement<>member': 131, 'member<>unequal': -169, 'disagreement<>wasteful': 10, 'member<>wasteful': -54, 'unequal<>wasteful': -12}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'M>M>M': 1541, 'M>U>M': 24, 'U>M>U': 7, 'M>W>M': 6, 'U>W>U': 2, 'U>M>M>U': 1, 'M>M>M>M': 1}

### B0-N200

- contract counters (all runs): {'draws': 0, 'null': 0, 'empty_menu': 0, 'guarded': 0, 'refused': 0, 'installed': 0, 'infeasible': 0, 'overflow': 0}
- guard: {}
- settled transitions by trigger: {'strict P': 5, 'other': 1, 'drift': 1}
- entries into V\* by trigger: {'strict P': 1}; exits from V\*: {}; member-island generations 5157914
- after a member exit, next member same / other: 0 / 0
- contract jump rows (class at the event → class one generation later), with the generator's rows:
- non-contract settled transitions: {'disagreement>unequal': 4, 'disagreement>wasteful': 1, 'disagreement>member': 1, 'member>member': 1}
- net circulation n(A→B) − n(B→A): {'disagreement<>unequal': 4, 'disagreement<>wasteful': 1, 'disagreement<>member': 1}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {}

### B1-N200

- contract counters (all runs): {'draws': 0, 'null': 0, 'empty_menu': 0, 'guarded': 0, 'refused': 0, 'installed': 0, 'infeasible': 0, 'overflow': 0}
- guard: {}
- settled transitions by trigger: {'migration': 4100}
- entries into V\* by trigger: {'migration': 658}; exits from V\*: {'migration': 1017}; member-island generations 4911042
- after a member exit, next member same / other: 20 / 95
- contract jump rows (class at the event → class one generation later), with the generator's rows:
- non-contract settled transitions: {'member>member': 2246, 'member>unequal': 1016, 'unequal>member': 639, 'unequal>unequal': 158, 'wasteful>member': 19, 'wasteful>unequal': 11, 'unequal>wasteful': 9, 'member>wasteful': 1, 'disagreement>unequal': 1}
- net circulation n(A→B) − n(B→A): {'unequal<>wasteful': -2, 'member<>unequal': 377, 'member<>wasteful': -18, 'disagreement<>unequal': 1}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'M>M>M': 1469, 'U>M>M>U': 35, 'U>M>U': 24, 'M>U>M>M': 21, 'M>U>M': 18, 'U>U>M>U': 11, 'M>M>U>M': 4, 'U>U>M>M>U': 2, 'U>W>M>M>U': 2, 'M>W>M': 1}

### D1-0-N50

- contract counters (all runs): {'draws': 1279820, 'null': 1143918, 'empty_menu': 0, 'guarded': 31528, 'refused': 0, 'installed': 135902, 'infeasible': 426324, 'overflow': 0}
- guard: {'guarded': 31528, 'went_through': 31528}
- settled transitions by trigger: {'contract': 128694}
- entries into V\* by trigger: {'contract': 30265}; exits from V\*: {'contract': 30116}; member-island generations 4219390
- after a member exit, next member same / other: 9687 / 19553
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 129): member 0.209, unequal 0.264, wasteful 0.527 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 31510): unequal 1.000 | generator unequal 1.000
  - other-mixed (n = 1051): member 0.205, unequal 0.324, wasteful 0.471 | generator 
  - unequal (n = 70973): member 0.333, unequal 0.332, wasteful 0.335 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 32239): member 0.249, unequal 0.501, wasteful 0.250 | generator member 0.250, unequal 0.500, wasteful 0.250
- net circulation n(A→B) − n(B→A): {'unequal<>wasteful': 6853, 'member<>unequal': 7100, 'member<>wasteful': -7230, 'disagreement<>member': 19, 'disagreement<>wasteful': 44, 'disagreement<>unequal': 24}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'long': 5895, 'U>U>M>U': 3466, 'U>M>U>U': 3362, 'M>U>U>M': 3147, 'U>W>M>U': 2435, 'M>U>W>M': 2245, 'U>U>U>U': 2146, 'U>W>U>U': 1692, 'U>U>W>U': 1683, 'U>M>U>M>U': 1549}

### D1-1-N50

- contract counters (all runs): {'draws': 1279420, 'null': 826052, 'empty_menu': 0, 'guarded': 74949, 'refused': 0, 'installed': 453368, 'infeasible': 427372, 'overflow': 0}
- guard: {'guarded': 74949, 'went_through': 74949}
- settled transitions by trigger: {'contract': 68177, 'migration': 186, 'contract residue': 98}
- entries into V\* by trigger: {'contract': 16309, 'migration': 86, 'contract residue': 52}; exits from V\*: {'contract': 16349, 'migration': 22, 'contract residue': 10}; member-island generations 760080
- after a member exit, next member same / other: 5151 / 10432
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 115): member 0.200, member-mixed 0.009, other-mixed 0.252, unequal 0.209, wasteful 0.330 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 11068): member 0.293, member-mixed 0.012, other-mixed 0.210, unequal 0.287, wasteful 0.198 | generator unequal 1.000
  - member-mixed (n = 2102): member 0.313, member-mixed 0.026, other-mixed 0.213, unequal 0.218, wasteful 0.231 | generator 
  - other-mixed (n = 407772): member 0.194, member-mixed 0.005, other-mixed 0.223, unequal 0.271, wasteful 0.306 | generator 
  - unequal (n = 13505): member 0.131, other-mixed 0.229, unequal 0.361, wasteful 0.279 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 18806): member 0.204, member-mixed 0.006, other-mixed 0.228, unequal 0.269, wasteful 0.292 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'wasteful>member': 104, 'member>member': 34, 'unequal>member': 33, 'wasteful>unequal': 32, 'member>wasteful': 19, 'unequal>wasteful': 16, 'member>unequal': 12, 'unequal>unequal': 12, 'wasteful>wasteful': 11, 'unequal>disagreement': 8, 'member>disagreement': 1, 'disagreement>member': 1}
- net circulation n(A→B) − n(B→A): {'member<>wasteful': -257, 'member<>unequal': 210, 'unequal<>wasteful': 202, 'disagreement<>wasteful': 9, 'disagreement<>member': 19, 'disagreement<>unequal': 7}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'long': 2447, 'M>W>M': 990, 'M>U>M': 906, 'M>M>M': 892, 'U>M>U': 454, 'U>W>U': 377, 'U>U>U': 337, 'W>U>W': 335, 'M>U>W>M': 328, 'W>M>W': 320}

### D1-0-N200

- contract counters (all runs): {'draws': 1281545, 'null': 1145607, 'empty_menu': 0, 'guarded': 31570, 'refused': 0, 'installed': 135938, 'infeasible': 426608, 'overflow': 0}
- guard: {'guarded': 31570, 'went_through': 31570}
- settled transitions by trigger: {'contract': 128615}
- entries into V\* by trigger: {'contract': 30264}; exits from V\*: {'contract': 30116}; member-island generations 4236278
- after a member exit, next member same / other: 9632 / 19606
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 1): wasteful 1.000 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 31540): member 0.000, unequal 1.000, wasteful 0.000 | generator unequal 1.000
  - member-mixed (n = 2): member 0.500, wasteful 0.500 | generator 
  - other-mixed (n = 1241): member 0.180, unequal 0.329, wasteful 0.491 | generator 
  - unequal (n = 70840): member 0.334, unequal 0.331, wasteful 0.335 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 32314): member 0.249, unequal 0.498, wasteful 0.254 | generator member 0.250, unequal 0.500, wasteful 0.250
- net circulation n(A→B) − n(B→A): {'member<>unequal': 7127, 'unequal<>wasteful': 6892, 'member<>wasteful': -7275, 'disagreement<>wasteful': 1}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'long': 5924, 'U>U>M>U': 3385, 'U>M>U>U': 3383, 'M>U>U>M': 3195, 'U>W>M>U': 2445, 'M>U>W>M': 2195, 'U>U>U>U': 2126, 'U>M>U>M>U': 1604, 'U>U>W>U': 1601, 'U>W>U>U': 1599}

### D1-1-N200

- contract counters (all runs): {'draws': 1279561, 'null': 891580, 'empty_menu': 0, 'guarded': 60275, 'refused': 0, 'installed': 387981, 'infeasible': 426884, 'overflow': 0}
- guard: {'guarded': 60275, 'went_through': 60275}
- settled transitions by trigger: {'contract': 261014, 'contract residue': 299, 'migration': 851}
- entries into V\* by trigger: {'contract': 46756, 'contract residue': 204, 'migration': 485}; exits from V\*: {'contract': 47255, 'migration': 29, 'contract residue': 7}; member-island generations 2505217
- after a member exit, next member same / other: 14616 / 31809
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - member (n = 44723): member 0.410, member-mixed 0.000, other-mixed 0.001, unequal 0.314, wasteful 0.275 | generator unequal 1.000
  - member-mixed (n = 4938): member 0.428, member-mixed 0.000, other-mixed 0.001, unequal 0.285, wasteful 0.287 | generator 
  - other-mixed (n = 220547): member 0.248, member-mixed 0.000, other-mixed 0.001, unequal 0.387, wasteful 0.363 | generator 
  - unequal (n = 64110): member 0.135, other-mixed 0.001, unequal 0.493, wasteful 0.370 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 53663): member 0.249, other-mixed 0.001, unequal 0.342, wasteful 0.408 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'wasteful>member': 618, 'wasteful>unequal': 357, 'unequal>member': 71, 'unequal>unequal': 43, 'member>unequal': 36, 'member>member': 13, 'wasteful>wasteful': 12}
- net circulation n(A→B) − n(B→A): {'member<>unequal': 5019, 'unequal<>wasteful': 4971, 'member<>wasteful': -5173}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'long': 12478, 'U>U>U': 3903, 'M>M>M': 3587, 'M>W>M': 2050, 'U>W>U': 1951, 'U>U>U>U': 1184, 'U>U>W>U': 1082, 'W>U>W': 1043, 'U>W>U>U': 1039, 'W>W>W': 999}

### R1pub-0-N50

- contract counters (all runs): {'draws': 1278942, 'null': 1174360, 'empty_menu': 0, 'guarded': 82213, 'refused': 76612, 'installed': 27970, 'infeasible': 425997, 'overflow': 0}
- guard: {'guarded': 82213, 'refused': 76612, 'drawn_carrier': 76612, 'carriers_present': 76646, 'went_through': 5601}
- settled transitions by trigger: {'contract': 25653}
- entries into V\* by trigger: {'contract': 6281}; exits from V\*: {'contract': 5353}; member-island generations 11043945
- after a member exit, next member same / other: 1696 / 3546
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 127): member 0.134, unequal 0.331, wasteful 0.535 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 5597): unequal 1.000 | generator unequal 1.000
  - other-mixed (n = 1023): member 0.175, unequal 0.330, wasteful 0.495 | generator 
  - unequal (n = 14246): member 0.333, unequal 0.338, wasteful 0.329 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 6977): member 0.256, unequal 0.501, wasteful 0.244 | generator member 0.250, unequal 0.500, wasteful 0.250
- net circulation n(A→B) − n(B→A): {'unequal<>wasteful': 1074, 'disagreement<>unequal': 30, 'disagreement<>wasteful': 46, 'member<>unequal': 716, 'member<>wasteful': -1631, 'disagreement<>member': 13}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'long': 978, 'U>U>M>U': 686, 'M>U>U>M': 538, 'U>M>U>U': 538, 'U>W>M>U': 433, 'U>U>U>U': 421, 'U>M>U>M>U': 400, 'M>U>W>M': 390, 'U>W>U>U': 345, 'M>U>M>U>M': 321}
- refusal: {"change": [-0.009427084028720856, -0.022919656150043013, 0.005390892773866624], "below_half_2000": 0.6, "rising": 0.35, "traj": {"0": 0.5008, "250": 0.4914, "500": 0.4914, "1000": 0.4914, "2000": 0.4914, "5000": 0.4914, "10000": 0.4914}, "islands_2000": {"spearman": 0.6388066160800192, "n": 1280, "share_by_fixed_bits": {"0": [0.327, 166], "1": [0.822, 501], "2": [0.998, 453], "3": [1.0, 160]}, "share_by_protection": {"prot_pub=True": [0.986, 953], "prot_priv=True": [1.0, 305], "prot_priv=False": [0.923, 784], "prot_pub=False": [0.654, 136]}}, "islands_10000": {"spearman": 0.5903919387272961, "n": 1280, "share_by_fixed_bits": {"0": [0.333, 166], "1": [0.994, 501], "2": [1.0, 453], "3": [1.0, 160]}, "share_by_protection": {"prot_pub=True": [1.0, 1108], "prot_priv=True": [1.0, 305], "prot_priv=False": [0.973, 862], "prot_pub=False": [0.611, 59]}}}

### R1pub-1-N50

- contract counters (all runs): {'draws': 1279246, 'null': 903426, 'empty_menu': 0, 'guarded': 206741, 'refused': 199065, 'installed': 176755, 'infeasible': 426492, 'overflow': 0}
- guard: {'guarded': 206741, 'refused': 199065, 'drawn_carrier': 199065, 'carriers_present': 206110, 'went_through': 7676}
- settled transitions by trigger: {'contract': 51920, 'migration': 7565, 'contract residue': 2013}
- entries into V\* by trigger: {'contract': 4540, 'migration': 230, 'contract residue': 175}; exits from V\*: {'contract': 4311, 'migration': 27, 'contract residue': 7}; member-island generations 6269243
- after a member exit, next member same / other: 1591 / 2725
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 45): member 0.111, other-mixed 0.200, unequal 0.222, wasteful 0.467 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 16140): member 0.822, member-mixed 0.076, other-mixed 0.065, unequal 0.023, wasteful 0.014 | generator unequal 1.000
  - member-mixed (n = 25526): member 0.849, member-mixed 0.081, other-mixed 0.051, unequal 0.009, wasteful 0.011 | generator 
  - other-mixed (n = 130079): member 0.523, member-mixed 0.043, other-mixed 0.138, unequal 0.134, wasteful 0.161 | generator 
  - unequal (n = 1932): member 0.143, other-mixed 0.254, unequal 0.350, wasteful 0.253 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 3033): member 0.215, member-mixed 0.010, other-mixed 0.224, unequal 0.270, wasteful 0.282 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'member>member': 9129, 'wasteful>member': 311, 'unequal>member': 94, 'member>wasteful': 33, 'unequal>wasteful': 4, 'wasteful>wasteful': 4, 'member>disagreement': 1, 'wasteful>unequal': 1, 'unequal>unequal': 1}
- net circulation n(A→B) − n(B→A): {'member<>wasteful': -395, 'member<>unequal': -182, 'unequal<>wasteful': 95, 'disagreement<>member': 23, 'disagreement<>wasteful': 7, 'disagreement<>unequal': 12}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'M>M>M': 25505, 'M>M>M>M': 8615, 'M>W>M': 767, 'M>W>M>M': 567, 'M>M>W>M': 561, 'M>U>M': 445, 'M>U>M>M': 297, 'M>M>U>M': 272, 'M>W>M>M>M': 233, 'M>M>W>M>M': 205}
- refusal: {"change": [0.29035939276218414, 0.22392879236489535, 0.363116927370429], "below_half_2000": 0.25, "rising": 1.0, "traj": {"0": 0.4992, "250": 0.5176, "500": 0.5026, "1000": 0.566, "2000": 0.6368, "5000": 0.7831, "10000": 0.7896}, "islands_2000": {"spearman": 0.2932604558806178, "n": 1280, "share_by_fixed_bits": {"0": [0.061, 3], "1": [0.113, 34], "2": [0.187, 145], "3": [0.186, 44]}, "share_by_protection": {"prot_pub=True": [0.218, 40], "prot_priv=True": [0.201, 20], "prot_priv=False": [0.221, 22], "prot_pub=False": [0.068, 2]}}, "islands_10000": {"spearman": -0.05965982767992192, "n": 1280, "share_by_fixed_bits": {"2": [0.253, 779], "3": [0.233, 453]}, "share_by_protection": {"prot_pub=True": [0.288, 299], "prot_priv=True": [0.302, 178], "prot_priv=False": [0.266, 121]}}}

### R1pub-0-N200

- contract counters (all runs): {'draws': 1281566, 'null': 1176839, 'empty_menu': 0, 'guarded': 81741, 'refused': 76058, 'installed': 28669, 'infeasible': 427527, 'overflow': 0}
- guard: {'guarded': 81741, 'refused': 76058, 'drawn_carrier': 76058, 'carriers_present': 76231, 'went_through': 5683}
- settled transitions by trigger: {'contract': 26237}
- entries into V\* by trigger: {'contract': 6369}; exits from V\*: {'contract': 5481}; member-island generations 10999439
- after a member exit, next member same / other: 1746 / 3622
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 1): unequal 1.000 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 5675): member 0.000, unequal 1.000 | generator unequal 1.000
  - other-mixed (n = 1234): member 0.193, unequal 0.327, wasteful 0.480 | generator 
  - unequal (n = 14508): member 0.329, unequal 0.337, wasteful 0.334 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 7251): member 0.250, unequal 0.496, wasteful 0.254 | generator member 0.250, unequal 0.500, wasteful 0.250
- net circulation n(A→B) − n(B→A): {'unequal<>wasteful': 1128, 'member<>unequal': 785, 'member<>wasteful': -1673}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'long': 959, 'U>U>M>U': 692, 'M>U>U>M': 590, 'U>M>U>U': 540, 'U>W>M>U': 484, 'U>U>U>U': 475, 'U>M>U>M>U': 432, 'M>U>W>M': 403, 'M>U>M>U>M': 364, 'U>W>U>U': 361}
- refusal: {"change": [-0.00432942807674408, -0.019370249323546886, 0.011442872770130627], "below_half_2000": 0.5, "rising": 0.45, "traj": {"0": 0.5002, "250": 0.4951, "500": 0.4966, "1000": 0.4958, "2000": 0.4958, "5000": 0.4958, "10000": 0.4958}, "islands_2000": {"spearman": 0.6396421434334966, "n": 1280, "share_by_fixed_bits": {"0": [0.334, 163], "1": [0.783, 482], "2": [1.0, 483], "3": [1.0, 152]}, "share_by_protection": {"prot_pub=True": [0.992, 927], "prot_priv=False": [0.93, 772], "prot_priv=True": [1.0, 301], "prot_pub=False": [0.679, 146]}}, "islands_10000": {"spearman": 0.6022621278893269, "n": 1280, "share_by_fixed_bits": {"0": [0.327, 163], "1": [0.997, 482], "2": [1.0, 483], "3": [1.0, 152]}, "share_by_protection": {"prot_pub=True": [1.0, 1113], "prot_priv=False": [0.97, 865], "prot_priv=True": [1.0, 301], "prot_pub=False": [0.512, 53]}}}

### R1pub-1-N200

- contract counters (all runs): {'draws': 1282050, 'null': 941509, 'empty_menu': 0, 'guarded': 173241, 'refused': 161766, 'installed': 178775, 'infeasible': 428063, 'overflow': 0}
- guard: {'guarded': 173241, 'refused': 161766, 'drawn_carrier': 161766, 'carriers_present': 173065, 'went_through': 11475}
- settled transitions by trigger: {'contract': 114830, 'contract residue': 557, 'migration': 1889}
- entries into V\* by trigger: {'contract': 10294, 'migration': 379, 'contract residue': 239}; exits from V\*: {'contract': 9981, 'migration': 3, 'contract residue': 1}; member-island generations 8545030
- after a member exit, next member same / other: 3043 / 6898
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 1): member 1.000 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 54021): member 0.905, member-mixed 0.000, other-mixed 0.000, unequal 0.050, wasteful 0.045 | generator unequal 1.000
  - member-mixed (n = 39790): member 0.941, member-mixed 0.000, other-mixed 0.000, unequal 0.028, wasteful 0.030 | generator 
  - other-mixed (n = 65093): member 0.531, member-mixed 0.000, other-mixed 0.001, unequal 0.241, wasteful 0.227 | generator 
  - unequal (n = 10311): member 0.130, other-mixed 0.001, unequal 0.502, wasteful 0.366 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 9559): member 0.251, other-mixed 0.001, unequal 0.345, wasteful 0.403 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'member>member': 1804, 'wasteful>member': 529, 'unequal>member': 89, 'wasteful>unequal': 14, 'member>unequal': 3, 'unequal>wasteful': 2, 'wasteful>wasteful': 2, 'unequal>unequal': 2, 'member>wasteful': 1}
- net circulation n(A→B) − n(B→A): {'member<>wasteful': -1893, 'unequal<>wasteful': 1423, 'member<>unequal': 966}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'M>M>M': 32432, 'M>M>M>M': 14407, 'long': 1791, 'U>U>U': 652, 'M>W>M': 582, 'M>W>M>M': 505, 'M>M>W>M': 475, 'M>M>U>M': 313, 'M>U>M>M': 304, 'U>W>U': 260}
- refusal: {"change": [0.28574870675802233, 0.2312929118424654, 0.34355370845645666], "below_half_2000": 0.2, "rising": 1.0, "traj": {"0": 0.499, "250": 0.5081, "500": 0.5172, "1000": 0.5399, "2000": 0.5815, "5000": 0.7275, "10000": 0.7847}, "islands_2000": {"spearman": 0.1869472766164471, "n": 1280, "share_by_fixed_bits": {"1": [0.324, 1], "2": [0.426, 2], "3": [0.403, 5]}, "share_by_protection": {"prot_pub=True": [0.412, 6], "prot_priv=False": [0.26, 2], "prot_priv=True": [0.455, 5], "prot_pub=False": [0.324, 1]}}, "islands_10000": {"spearman": 0.08761712366441342, "n": 1280, "share_by_fixed_bits": {"2": [0.467, 293], "3": [0.48, 225]}, "share_by_protection": {"prot_pub=True": [0.505, 243], "prot_priv=False": [0.493, 84], "prot_priv=True": [0.511, 159]}}}

### R1priv-0-N50

- contract counters (all runs): {'draws': 256212, 'null': 230133, 'empty_menu': 0, 'guarded': 11118, 'refused': 0, 'installed': 26079, 'infeasible': 85850, 'overflow': 0}
- guard: {'guarded': 11118, 'went_through': 11118, 'carriers_present': 9057}
- settled transitions by trigger: {'contract': 16106, 'strict P': 1}
- entries into V\* by trigger: {'contract': 3788}; exits from V\*: {'contract': 3157}; member-island generations 1510653
- after a member exit, next member same / other: 900 / 1857
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 1309): member 0.170, unequal 0.328, wasteful 0.502 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 11086): disagreement 0.108, member 0.699, other-mixed 0.005, unequal 0.189 | generator unequal 1.000
  - other-mixed (n = 1082): disagreement 0.001, member 0.184, other-mixed 0.026, unequal 0.312, wasteful 0.477 | generator 
  - unequal (n = 7647): member 0.326, unequal 0.340, wasteful 0.334 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 4955): member 0.252, unequal 0.483, wasteful 0.265 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'disagreement>unequal': 1}
- net circulation n(A→B) − n(B→A): {'unequal<>wasteful': 135, 'member<>unequal': -306, 'disagreement<>unequal': 318, 'disagreement<>wasteful': 469, 'disagreement<>member': -703, 'member<>wasteful': -1028}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'long': 436, 'U>U>U>U': 252, 'U>U>M>U': 208, 'U>W>U>U': 179, 'M>U>U>M': 173, 'U>W>M>U': 169, 'U>U>W>U': 166, 'U>M>U>M>U': 154, 'U>M>U>U': 140, 'M>U>W>M': 135}
- refusal: {"change": [0.0015104159712791443, -0.012426827177405356, 0.01588191654533147], "below_half_2000": 0.5, "rising": 0.5, "traj": {"0": 0.5008, "250": 0.5023, "500": 0.5023, "1000": 0.5023, "2000": 0.5023}, "islands_2000": {"spearman": 0.6568973168492285, "n": 1280, "share_by_fixed_bits": {"0": [0.317, 168], "1": [0.462, 459], "2": [0.872, 489], "3": [0.997, 164]}, "share_by_protection": {"prot_pub=True": [0.941, 639], "prot_priv=True": [0.982, 539], "prot_pub=False": [0.686, 240], "prot_priv=False": [0.697, 340]}}}

### R1priv-1-N50

- contract counters (all runs): {'draws': 255346, 'null': 172245, 'empty_menu': 0, 'guarded': 33985, 'refused': 0, 'installed': 83101, 'infeasible': 85432, 'overflow': 0}
- guard: {'guarded': 33985, 'went_through': 33985, 'carriers_present': 33874}
- settled transitions by trigger: {'contract': 11188, 'migration': 221, 'contract residue': 59}
- entries into V\* by trigger: {'contract': 2053, 'migration': 26, 'contract residue': 17}; exits from V\*: {'contract': 1509, 'migration': 2, 'contract residue': 2}; member-island generations 770784
- after a member exit, next member same / other: 495 / 937
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 93): member 0.086, member-mixed 0.011, other-mixed 0.161, unequal 0.269, wasteful 0.473 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 5930): disagreement 0.004, member 0.641, member-mixed 0.093, other-mixed 0.255, unequal 0.002, wasteful 0.003 | generator unequal 1.000
  - member-mixed (n = 6858): disagreement 0.001, member 0.371, member-mixed 0.379, other-mixed 0.247, unequal 0.001, wasteful 0.001 | generator 
  - other-mixed (n = 67887): disagreement 0.001, member 0.244, member-mixed 0.029, other-mixed 0.470, unequal 0.115, wasteful 0.142 | generator 
  - unequal (n = 887): member 0.114, other-mixed 0.256, unequal 0.329, wasteful 0.301 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 1446): member 0.222, member-mixed 0.009, other-mixed 0.221, unequal 0.268, wasteful 0.280 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'member>member': 227, 'wasteful>member': 32, 'unequal>member': 9, 'member>wasteful': 3, 'disagreement>member': 2, 'wasteful>unequal': 2, 'unequal>wasteful': 2, 'member>disagreement': 1, 'unequal>unequal': 1, 'wasteful>disagreement': 1}
- net circulation n(A→B) − n(B→A): {'member<>wasteful': -336, 'member<>unequal': -224, 'unequal<>wasteful': 34, 'disagreement<>member': 23, 'disagreement<>wasteful': 9, 'disagreement<>unequal': 12}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'M>M>M': 2677, 'M>M>M>M': 774, 'M>W>M': 207, 'M>W>M>M': 148, 'M>U>M': 126, 'M>M>W>M': 104, 'M>U>M>M': 81, 'M>M>U>M': 47, 'M>W>M>M>M': 41, 'M>U>W>M': 36}
- refusal: {"change": [0.44495833814144137, 0.3634552205353975, 0.4948915374279022], "below_half_2000": 0.05, "rising": 0.95, "traj": {"0": 0.4992, "250": 0.5252, "500": 0.5919, "1000": 0.7719, "2000": 0.9442}, "islands_2000": {"spearman": 0.31017402511946285, "n": 1280, "share_by_fixed_bits": {"0": [0.044, 2], "2": [0.043, 3], "3": [0.212, 1046]}, "share_by_protection": {"prot_pub=True": [0.249, 252], "prot_priv=True": [0.249, 252]}}}

### R1priv-0-N200

- contract counters (all runs): {'draws': 256238, 'null': 229942, 'empty_menu': 0, 'guarded': 11482, 'refused': 0, 'installed': 26296, 'infeasible': 85384, 'overflow': 0}
- guard: {'guarded': 11482, 'went_through': 11482, 'carriers_present': 9395}
- settled transitions by trigger: {'contract': 15860, 'contract residue': 1}
- entries into V\* by trigger: {'contract': 3879}; exits from V\*: {'contract': 3264, 'contract residue': 1}; member-island generations 1527679
- after a member exit, next member same / other: 944 / 1922
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 1065): member 0.146, unequal 0.348, wasteful 0.506 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 11404): disagreement 0.094, member 0.685, other-mixed 0.035, unequal 0.186 | generator unequal 1.000
  - member-mixed (n = 1): other-mixed 1.000 | generator 
  - other-mixed (n = 1509): member 0.191, other-mixed 0.052, unequal 0.318, wasteful 0.439 | generator 
  - unequal (n = 7505): member 0.343, unequal 0.324, wasteful 0.333 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 4812): member 0.278, unequal 0.470, wasteful 0.252 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'member>unequal': 1}
- net circulation n(A→B) − n(B→A): {'unequal<>wasteful': 202, 'disagreement<>wasteful': 392, 'disagreement<>unequal': 282, 'disagreement<>member': -678, 'member<>unequal': -223, 'member<>wasteful': -1069}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'long': 456, 'U>U>M>U': 241, 'M>U>U>M': 204, 'U>W>M>U': 184, 'U>U>U>U': 182, 'U>M>U>U': 180, 'U>M>U>M>U': 180, 'U>W>U>U': 161, 'U>U>W>U': 158, 'M>U>W>M': 149}
- refusal: {"change": [-0.001725265383720398, -0.02404739912599325, 0.021191148534417146], "below_half_2000": 0.55, "rising": 0.45, "traj": {"0": 0.5002, "250": 0.4994, "500": 0.4986, "1000": 0.4984, "2000": 0.4984}, "islands_2000": {"spearman": 0.6993042687971613, "n": 1280, "share_by_fixed_bits": {"0": [0.314, 177], "1": [0.482, 470], "2": [0.887, 455], "3": [1.0, 178]}, "share_by_protection": {"prot_pub=True": [0.955, 612], "prot_priv=True": [0.987, 547], "prot_pub=False": [0.661, 264], "prot_priv=False": [0.666, 329]}}}

### R1priv-1-N200

- contract counters (all runs): {'draws': 256208, 'null': 183388, 'empty_menu': 0, 'guarded': 28798, 'refused': 0, 'installed': 72820, 'infeasible': 85695, 'overflow': 0}
- guard: {'guarded': 28798, 'went_through': 28798, 'carriers_present': 28786}
- settled transitions by trigger: {'contract': 28418, 'migration': 89, 'contract residue': 32}
- entries into V\* by trigger: {'contract': 3892, 'migration': 53, 'contract residue': 24}; exits from V\*: {'contract': 3084, 'migration': 2}; member-island generations 1304118
- after a member exit, next member same / other: 975 / 2006
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 68): member 0.132, unequal 0.309, wasteful 0.559 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 18009): disagreement 0.005, member 0.708, member-mixed 0.039, other-mixed 0.243, unequal 0.003, wasteful 0.002 | generator unequal 1.000
  - member-mixed (n = 9049): disagreement 0.001, member 0.433, member-mixed 0.337, other-mixed 0.226, unequal 0.001, wasteful 0.001 | generator 
  - other-mixed (n = 37615): disagreement 0.002, member 0.304, member-mixed 0.015, other-mixed 0.306, unequal 0.186, wasteful 0.188 | generator 
  - unequal (n = 4204): member 0.137, other-mixed 0.001, unequal 0.500, wasteful 0.363 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 3875): member 0.251, other-mixed 0.001, unequal 0.338, wasteful 0.410 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'wasteful>member': 70, 'member>member': 23, 'wasteful>unequal': 15, 'unequal>member': 7, 'unequal>unequal': 3, 'member>unequal': 2, 'wasteful>wasteful': 1}
- net circulation n(A→B) − n(B→A): {'unequal<>wasteful': 532, 'member<>unequal': 85, 'member<>wasteful': -994, 'disagreement<>unequal': 10, 'disagreement<>wasteful': 14, 'disagreement<>member': -26}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'M>M>M': 4557, 'M>M>M>M': 1630, 'long': 573, 'U>U>U': 228, 'M>W>M': 174, 'U>W>U': 99, 'M>U>M': 97, 'M>W>M>M': 90, 'U>U>U>U': 69, 'M>U>M>M': 68}
- refusal: {"change": [0.37414192855358125, 0.30485225472599264, 0.4344075509905814], "below_half_2000": 0.0, "rising": 1.0, "traj": {"0": 0.499, "250": 0.5204, "500": 0.5388, "1000": 0.6536, "2000": 0.8731}, "islands_2000": {"spearman": 0.32506937801983365, "n": 1280, "share_by_fixed_bits": {"2": [0.478, 2], "3": [0.445, 500]}, "share_by_protection": {"prot_pub=True": [0.477, 254], "prot_priv=True": [0.477, 253], "prot_priv=False": [0.396, 1]}}}

### D3p-0

- contract counters (all runs): {'draws': 513011, 'null': 392070, 'empty_menu': 0, 'guarded': 26942, 'refused': 0, 'installed': 120941, 'infeasible': 171508, 'overflow': 0}
- guard: {'guarded': 26942, 'went_through': 26942}
- settled transitions by trigger: {'contract': 18964, 'contract residue': 25}
- entries into V\* by trigger: {'contract': 5158, 'contract residue': 13}; exits from V\*: {'contract': 4952, 'contract residue': 4}; member-island generations 1481102
- after a member exit, next member same / other: 1156 / 2387
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 67): other-mixed 1.000 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 10658): member 0.011, member-mixed 0.003, other-mixed 0.987 | generator unequal 1.000
  - member-mixed (n = 850): member 0.012, member-mixed 0.061, other-mixed 0.927 | generator 
  - other-mixed (n = 91175): member 0.002, member-mixed 0.001, other-mixed 0.993, unequal 0.004, wasteful 0.001 | generator 
  - unequal (n = 14009): other-mixed 0.989, unequal 0.011 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 4182): other-mixed 0.989, wasteful 0.011 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'wasteful>member': 7, 'unequal>member': 6, 'member>unequal': 4, 'wasteful>unequal': 3, 'member>member': 3, 'unequal>wasteful': 1, 'wasteful>wasteful': 1}
- net circulation n(A→B) − n(B→A): {'member<>unequal': 239, 'unequal<>wasteful': 288, 'member<>wasteful': -435, 'disagreement<>unequal': 23, 'disagreement<>wasteful': 1, 'disagreement<>member': 19}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'M>U>M': 408, 'U>U>U': 300, 'U>M>U': 260, 'M>U>U>M': 206, 'U>U>M>U': 152, 'U>M>U>U': 140, 'U>U>U>U': 108, 'U>W>U': 105, 'long': 97, 'M>M>M': 92}
- β < 1 fates by edge class: {'other-mixed>wasteful': {'superseded': 31399, 'one-sided': 3365, 'joint': 1765, 'lost': 1030, 'open': 353}, 'other-mixed>unequal': {'joint': 5590, 'superseded': 24892, 'lost': 858, 'one-sided': 1087, 'open': 349}, 'other-mixed>member': {'superseded': 15122, 'joint': 3940, 'one-sided': 796, 'lost': 421, 'open': 208}, 'disagreement>wasteful': {'superseded': 32, 'joint': 4, 'one-sided': 3}, 'wasteful>unequal': {'superseded': 1557, 'joint': 255, 'lost': 46, 'one-sided': 48, 'open': 23}, 'unequal>unequal': {'superseded': 3695, 'joint': 952, 'lost': 125, 'one-sided': 112, 'open': 48}, 'member>unequal': {'joint': 1117, 'superseded': 7528, 'lost': 560, 'one-sided': 614, 'open': 135}, 'unequal>wasteful': {'superseded': 3829, 'joint': 311, 'one-sided': 280, 'lost': 146, 'open': 66}, 'wasteful>wasteful': {'superseded': 966, 'one-sided': 58, 'joint': 93, 'lost': 26, 'open': 11}, 'unequal>member': {'superseded': 3490, 'one-sided': 192, 'joint': 585, 'lost': 116, 'open': 62}, 'wasteful>member': {'superseded': 894, 'joint': 144, 'one-sided': 34, 'open': 11, 'lost': 16}, 'member>member': {'superseded': 215, 'one-sided': 40, 'lost': 14, 'joint': 124, 'open': 2}, 'member-mixed>wasteful': {'superseded': 225, 'joint': 4, 'lost': 18, 'one-sided': 20, 'open': 2}, 'member>wasteful': {'superseded': 226, 'lost': 27, 'one-sided': 37, 'joint': 15, 'open': 4}, 'member-mixed>member': {'superseded': 146, 'joint': 40, 'lost': 9, 'one-sided': 23, 'open': 3}, 'member-mixed>unequal': {'superseded': 298, 'lost': 16, 'one-sided': 12, 'joint': 31, 'open': 3}, 'disagreement>unequal': {'joint': 3, 'superseded': 17}, 'disagreement>member': {'superseded': 8}}

### D3p-1

- contract counters (all runs): {'draws': 511127, 'null': 300948, 'empty_menu': 0, 'guarded': 47062, 'refused': 0, 'installed': 210179, 'infeasible': 170453, 'overflow': 0}
- guard: {'guarded': 47062, 'went_through': 47062}
- settled transitions by trigger: {'contract': 5418, 'migration': 18, 'contract residue': 9}
- entries into V\* by trigger: {'contract': 1499, 'migration': 9, 'contract residue': 5}; exits from V\*: {'contract': 1395, 'migration': 3, 'contract residue': 2}; member-island generations 491889
- after a member exit, next member same / other: 255 / 487
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 23): other-mixed 1.000 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 2995): member 0.102, member-mixed 0.019, other-mixed 0.879 | generator unequal 1.000
  - member-mixed (n = 1171): member 0.037, member-mixed 0.143, other-mixed 0.821 | generator 
  - other-mixed (n = 204246): member 0.003, member-mixed 0.002, other-mixed 0.993, unequal 0.002, wasteful 0.000 | generator 
  - unequal (n = 1385): other-mixed 0.891, unequal 0.109 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 359): other-mixed 0.900, wasteful 0.100 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'unequal>member': 7, 'wasteful>member': 7, 'member>member': 5, 'member>unequal': 4, 'wasteful>unequal': 2, 'unequal>unequal': 1, 'member>wasteful': 1}
- net circulation n(A→B) − n(B→A): {'member<>unequal': -81, 'member<>wasteful': -22, 'unequal<>wasteful': 12, 'disagreement<>member': 10, 'disagreement<>unequal': 4}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'M>M>M': 305, 'M>U>M': 186, 'M>M>U>M': 42, 'M>U>M>M': 34, 'M>M>M>M': 33, 'U>M>U': 32, 'M>W>M': 31, 'M>U>U>M': 25, 'U>U>U': 17, 'U>M>M>U': 13}
- β < 1 fates by edge class: {'other-mixed>wasteful': {'superseded': 80613, 'joint': 244, 'one-sided': 1984, 'lost': 1596, 'open': 887}, 'other-mixed>unequal': {'superseded': 66422, 'joint': 1155, 'lost': 1592, 'one-sided': 310, 'open': 805}, 'other-mixed>member': {'superseded': 44886, 'joint': 2415, 'lost': 461, 'one-sided': 298, 'open': 578}, 'member>unequal': {'superseded': 950, 'lost': 41, 'one-sided': 14, 'joint': 5, 'open': 8}, 'member>wasteful': {'superseded': 749, 'one-sided': 14, 'lost': 32, 'open': 9, 'joint': 1}, 'unequal>unequal': {'superseded': 572, 'joint': 71, 'open': 12, 'lost': 20, 'one-sided': 3}, 'member>member': {'joint': 190, 'superseded': 923, 'one-sided': 15, 'open': 21, 'lost': 23}, 'unequal>wasteful': {'superseded': 489, 'one-sided': 13, 'lost': 9, 'open': 9, 'joint': 3}, 'member-mixed>member': {'superseded': 364, 'joint': 52, 'lost': 7, 'one-sided': 7, 'open': 9}, 'member-mixed>wasteful': {'superseded': 336, 'lost': 21, 'one-sided': 7, 'open': 3}, 'member-mixed>unequal': {'superseded': 343, 'lost': 13, 'one-sided': 5, 'open': 3, 'joint': 1}, 'wasteful>wasteful': {'superseded': 125, 'joint': 17, 'one-sided': 3, 'lost': 1}, 'wasteful>unequal': {'superseded': 108, 'joint': 4, 'lost': 5, 'open': 1, 'one-sided': 1}, 'wasteful>member': {'superseded': 91, 'joint': 3}, 'unequal>member': {'superseded': 175, 'joint': 5, 'lost': 2, 'one-sided': 1, 'open': 1}, 'disagreement>wasteful': {'superseded': 9}, 'disagreement>unequal': {'superseded': 8}, 'disagreement>member': {'superseded': 6}}

### D2-0

- contract counters (all runs): {'draws': 51087, 'null': 44894, 'empty_menu': 0, 'guarded': 1212, 'refused': 0, 'installed': 6193, 'infeasible': 17063, 'overflow': 0}
- guard: {'guarded': 1212, 'went_through': 1212}
- settled transitions by trigger: {'contract': 5446, 'strict P': 23, 'other': 1}
- entries into V\* by trigger: {'contract': 1388, 'strict P': 9}; exits from V\*: {'contract': 1161}; member-island generations 1569009
- after a member exit, next member same / other: 72 / 234
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 158): member 0.158, unequal 0.373, wasteful 0.468 | generator member 0.167, unequal 0.333, wasteful 0.500
  - grand (n = 3): member 1.000 | generator member 1.000
  - member (n = 1180): member 0.003, unequal 0.994, wasteful 0.003 | generator unequal 1.000
  - member-mixed (n = 1): unequal 1.000 | generator 
  - other-mixed (n = 677): member 0.191, unequal 0.352, wasteful 0.458 | generator 
  - unequal (n = 2631): member 0.350, unequal 0.341, wasteful 0.309 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 1543): member 0.289, unequal 0.472, wasteful 0.238 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'disagreement>member': 8, 'disagreement>unequal': 8, 'disagreement>wasteful': 4, 'wasteful>unequal': 1, 'wasteful>member': 1, 'wasteful>wasteful': 1, 'unequal>wasteful': 1}
- net circulation n(A→B) − n(B→A): {'member<>unequal': 241, 'unequal<>wasteful': 83, 'disagreement<>unequal': 66, 'disagreement<>member': 32, 'disagreement<>wasteful': 74, 'member<>wasteful': -442, 'grand<>member': 3}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'U>U>M>U': 39, 'U>M>U>U': 36, 'M>U>U>M': 34, 'M>U>W>M': 33, 'U>W>U>U': 22, 'U>U>W>U': 21, 'U>U>U>U': 21, 'U>W>M>U': 19, 'U>W>W>U': 19, 'W>M>U>W': 16}

### D2-1

- contract counters (all runs): {'draws': 51038, 'null': 36019, 'empty_menu': 0, 'guarded': 5300, 'refused': 0, 'installed': 15019, 'infeasible': 17145, 'overflow': 0}
- guard: {'guarded': 5300, 'went_through': 5300}
- settled transitions by trigger: {'contract': 8583, 'migration': 3149, 'contract residue': 1652, 'conditional/none': 1, 'strict P': 1}
- entries into V\* by trigger: {'contract': 1639, 'migration': 1367, 'contract residue': 1093}; exits from V\*: {'contract': 2965, 'migration': 376, 'contract residue': 48}; member-island generations 2211416
- after a member exit, next member same / other: 1210 / 1409
- contract jump rows (class at the event → class one generation later), with the generator's rows:
  - disagreement (n = 7): other-mixed 0.143, unequal 0.571, wasteful 0.286 | generator member 0.167, unequal 0.333, wasteful 0.500
  - member (n = 2085): member 0.356, member-mixed 0.005, other-mixed 0.029, unequal 0.380, wasteful 0.230 | generator unequal 1.000
  - member-mixed (n = 893): member 0.362, member-mixed 0.002, other-mixed 0.035, unequal 0.283, wasteful 0.318 | generator 
  - other-mixed (n = 11450): member 0.266, member-mixed 0.002, other-mixed 0.032, unequal 0.347, wasteful 0.353 | generator 
  - unequal (n = 393): member 0.168, other-mixed 0.043, unequal 0.455, wasteful 0.333 | generator member 0.333, unequal 0.333, wasteful 0.333
  - wasteful (n = 191): member 0.309, member-mixed 0.005, other-mixed 0.042, unequal 0.251, wasteful 0.393 | generator member 0.250, unequal 0.500, wasteful 0.250
- non-contract settled transitions: {'member>member': 1554, 'unequal>member': 1261, 'wasteful>member': 1174, 'member>unequal': 388, 'wasteful>unequal': 169, 'unequal>unequal': 124, 'unequal>wasteful': 44, 'member>wasteful': 36, 'disagreement>member': 25, 'wasteful>wasteful': 16, 'disagreement>unequal': 9, 'disagreement>wasteful': 2}
- net circulation n(A→B) − n(B→A): {'member<>unequal': -167, 'unequal<>wasteful': 205, 'member<>wasteful': -497, 'disagreement<>unequal': 27, 'disagreement<>member': 46, 'disagreement<>wasteful': 20}
- most common minimal cycles (settled outcomes, classes M/U/W/D/G): {'M>M>M': 915, 'M>U>M': 519, 'M>W>M': 368, 'M>U>M>M': 135, 'U>M>U': 119, 'M>W>M>M': 111, 'M>M>W>M': 106, 'M>M>M>M': 96, 'M>M>U>M': 85, 'M>U>U>M': 75}

## Where the bit's rise comes from (decomposition added after the R1 cells; no prediction scored on it)

Change of the island mean bit per 50-generation window, summed per run and divided by 64 islands, by the island's state at the window start (classified member or member-mixed vs not) and the window's contract events (`src/dominance_contracts_refusal.py`).

- R1pub-1: member|guarded-through -0.001 (6315 windows), member|none -0.016 (74157 windows), member|refused -0.048 (151160 windows), member|unguarded-install -0.030 (53472 windows), non-member|guarded-through -0.013 (9194 windows), non-member|none +0.054 (49684 windows), non-member|refused +0.079 (103061 windows), non-member|unguarded-install +0.275 (64957 windows)
- R1priv-1: member|guarded-through +0.022 (18916 windows), member|none -0.004 (9008 windows), member|unguarded-install -0.008 (6622 windows), non-member|guarded-through +0.172 (27060 windows), non-member|none +0.077 (13933 windows), non-member|unguarded-install +0.200 (26861 windows)
- R1blind-1: member|guarded-through -0.008 (5221 windows), member|none +0.000 (2551 windows), member|unguarded-install -0.003 (1963 windows), non-member|guarded-through -0.007 (20271 windows), non-member|none +0.004 (17541 windows), non-member|unguarded-install +0.005 (54853 windows)
- R1priv-0: member|guarded-through -0.002 (18121 windows), member|none +0.001 (41141 windows), member|unguarded-install +0.000 (1 windows), non-member|guarded-through +0.000 (1375 windows), non-member|none -0.005 (21703 windows), non-member|unguarded-install -0.007 (20059 windows)

## Verdicts (scored against `predictions/2026-10-14-dominance-contracts.md`)

Occupancy below is the registered definition (islands classified ≥ 0.95 on a member, the baseline's 0.281 / 0.739);
"modal" is the spec's wording (argmax of the island's encounter distribution), reported because the two part at
mN = 1. **They agree at mN = 0 everywhere.** At mN = 1 contracts keep the islands on different outcomes, so every
migrant is mismatched and selection against it leaves a standing load of 5–25% of encounters: the island's modal play
is unchanged but the 0.95 test fails (other-mixed 0.5–0.95 of islands in the contract cells, 0.03 in the baseline,
where migration builds a consensus and migrants match). Disclosed here, after the run: the modal-play column was
added to the report when the D1 mN = 1 cell showed the split; no prediction was re-scored on it.

| # | prediction | outcome |
|---|---|---|
| **RS** | contracts deviating to dominating outcomes recover the vNM stable set (D1: occupancy ≥ 0.8 and support ⊆ V\* in ≥ 0.5 of runs, at mN = 0 or 1) | **failed at both mN, on both definitions.** mN = 0: 0.338 [0.318, 0.359] at 2,000, 0.315 at 10,000, support 0/40. mN = 1: 0.091 (modal 0.338) at 2,000, 0.084 (modal 0.324) at 10,000, support 0/40 (stable-sets definition 0/40). The occupancy is the exact proposal generator's 1/3. |
| RE 1 | D1 within 0.1 of the walk (0.2–0.4 at mN = 0); support ≤ 0.2; falsifier ≥ 0.6 | **held** (0.338 vs 1/3 at mN = 0; modal 0.338 at mN = 1; registered occupancy at mN = 1 is 0.091, outside the band by the migration load, not by the walk) |
| RE 2 | D1 at mN = 1 below the baseline's 0.74 because contracts break the consensus | **held** (0.091, paired Δ −0.65; modal 0.338 vs 0.843; consensus 0/40 vs 26/40) |
| RE 3 | D2 between the baseline and D1 | **held** (mN = 0: 0.345 [0.325, 0.366] against 0.281 and 0.338, within D1's uncertainty; mN = 1: 0.261 between 0.091 and 0.739; modal 0.679 between 0.338 and 0.843) |
| RE 4 | refusal lost where private (mean < 0.5 in ≥ 0.8 of runs at mN = 0), neutral where public; occupancy rises with the island's bit | **failed.** Public, mN = 0: neutral (change −0.007 [−0.017, 0.003]) and island member time-share rises with the bit (Spearman 0.63; 0.34 with no refusing slot, 1.0 with two or more): held. **Public, mN = 1: the bit rises in 40/40 runs, 0.50 → 0.80 by 10,000 (falsifier fired).** Private, mN = 0: mean < 0.5 in 0.60 of runs (change −0.011): clause failed. **Private, mN = 1: rises in 40/40 runs, 0.50 → 0.96 by 2,000 (falsifier fired).** The r-blind control does not move (−0.008 [−0.053, 0.036]). |
| RE 5 | R2: V\* reachable (contracts-only chain) and ≥ 0.9 occupancy, support ≥ 0.8 of runs | **held at mN = 0** (reachability a theorem of the generator; 1.000 occupancy, support 0.97 at 2,000 and 1.00 at 10,000); **falsifier fired at mN = 1 on the registered classifier** (0.331 / 0.316), read through the hazards: exits from V\* 3.8·10⁻⁵ per member-island-generation, modal occupancy 0.996 / 0.998, support (stable-sets definition) 0.95 / 1.00 of runs, coverage 1.00; the failure is the migration load between islands on different members (consensus 0/40), not leakage |
| RE 6 | D4 within 0.1 of the baseline at mN = 0 | **held** (0.220 vs 0.281, paired Δ −0.061); menus fall from 18.1 contracts to 0.40 by generation 100 and 0.29 by 250 |
| RE 7 (revised) | β\* > 0.5 for every member exit; fixation ≤ 0.05 at β = 0.25; D3 within uncertainty of the baseline; falsifier fixation ≥ 0.2 | **failed in two of three clauses; falsifier not fired.** β\*_static 0.76 (holds), β\*_flow 0.40 (fails); member-exit fixation at β = 0.25 = 0.13 (0.07 when the excluded constant is neutral, ≈ 0.7 when it already offers); D3 at mN = 0 is +0.117 [0.089, 0.144] above the paired baseline |
| Gemini (counter to RE 7) | fixation < 0.05 and D3 identical to the baseline | **failed** (0.13; +0.117) |
| RE 8 (Gemini's alternative, as a test) | if D1(mN = 1) > D1(mN = 0), entries into V\* at mN = 1 are carried by drift and migration | **premise false**: D1(mN = 1) is not above D1(mN = 0) (0.091 vs 0.338; modal 0.338 vs 0.338); 0.986 of entries into V\* at mN = 1 are contract-triggered. (At ν = 0.01, D2 at mN = 1, 0.60 of entries are not contract-triggered.) |
| S1 | D1 mN = 0 within 0.05 of 1/3 at 2,000 and 10,000; unequal 1/2, wasteful 1/6 | **held** (0.338 / 0.315; 0.505 / 0.517; 0.157 / 0.168) |
| S2 | RS fails in D1; mN = 1 occupancy in [0.45, 0.62] | RS clause **held**; the mN = 1 interval **failed** (0.091; modal 0.338); falsifier not fired |
| S3 | contract jumps follow the generator | **held** (member → unequal 1.000 of 62,791 contract jumps at mN = 0; unequal rows 0.333 / 0.334 / 0.333; wasteful 0.252 / 0.499 / 0.249) |
| S4 | same-member return 0.32 ± 0.06 at mN = 0, higher at mN = 1 | first clause **held** (0.326); second **failed** (0.326 at mN = 1) |
| S5 | ≥ 0.4 of entries into V\* not contract-triggered at mN = 1 | **failed, falsifier fired** (0.014) |
| S6 | member-exit fixation ≤ 0.05 at β = 0.25, ≥ 0.5 at 0.5; entries ≥ 3× exits; D3 − baseline ≥ 0.1 | **falsifier fired** (0.13 ≥ 0.1); 0.51 at β = 0.5 held; entries 1.6× exits failed; D3 − baseline +0.117 held |
| S7 | R1-public mN = 0: [0.75, 0.92] at 2,000, ≥ 0.85 at 10,000, support ≤ 0.1, bit change ≤ 0.05, protected islands ≥ 0.9, (0,0,0) ≈ 1/3 | **held** (0.845; 0.915; 0/40; −0.007; protected 1.000, unprotected-by-bits 0.36) |
| S8 | R1-private mN = 0 in [0.55, 0.78]; bit falls ≤ 0.05 at mN = 0, ≥ 0.05 at mN = 1 | first two **held** (0.675; −0.011); **falsifier fired** at mN = 1 (rises +0.46) |
| S9 | R2 ≥ 0.95 at mN = 0, [0.8, 0.95] at mN = 1, hazard ≤ 1/500 | mN = 0 **held** (1.000); **falsifier fired** at mN = 1 on the registered classifier (0.331; modal 0.996); hazard held (3.8·10⁻⁵) |
| S10 | D4 mN = 0 in [0.18, 0.34], menus ≤ 1 | **held** (0.220; 0.29) |
| S11 | D1 mN = 0: efficiency +≥ 0.05, occupancy +≤ 0.08 | **held** (+0.087; +0.057) |
| S12 | D1 mN = 0 within 0.05 of 1/3 at N = 50, 200 | **held** (0.352 / 0.355 at 2,000; 0.317 / 0.310 at 10,000) |
| S13 | no D cell meets the RS thresholds; R2 mN = 0 meets both by 10,000; R1-public meets occupancy, fails support | **held** (R2-0: 1.000, support 1.00; R1pub-0: 0.915, support 0) |

