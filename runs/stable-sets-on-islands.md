# Stable sets on islands: run report (2026-10-13)

Spec `specs/2026-10-13-stable-sets-on-islands.md`; notes `notes/stable-sets-on-islands.md`; predictions `predictions/2026-10-13-stable-sets-on-islands.md`; code `src/stable_sets.py`, `src/stable_sets_run.py`, `src/stable_sets_report.py`. ε = 0 lottery (finite-size evidence); the chain is a separate object. Intervals: 95% over runs (t for fractions of islands, Wilson for fractions of runs).

## Static (enumeration)

- R (20 realizable outcomes): C = M: True; singleton commitments dominate: False; myopic stable sets (M = C): [['P12:3|3', 'P13:3|3', 'P23:3|3']]; with game effectiveness: [['P12:3|3', 'P13:3|3', 'P23:3|3']]; single-slot moves only: [['G(2,2,2)', 'P12:3|3', 'P13:3|3', 'P23:3|3']].
- Farsighted (TU): [['G(2,2,2)'], ['P12:4|2'], ['P12:3|3'], ['P12:2|4'], ['P13:4|2'], ['P13:3|3'], ['P13:2|4'], ['P23:4|2'], ['P23:3|3'], ['P23:2|4']]; LCS (TU) = all of R: True. Farsighted (game effectiveness): [['P12:4|2', 'P23:2|4'], ['P12:3|3', 'P13:3|3', 'P23:3|3'], ['P12:2|4', 'P13:2|4'], ['P13:4|2', 'P23:4|2']].
- G6= (28): stable sets [['P12:3|3', 'P13:3|3', 'P23:3|3']]; discriminatory sets 0.
- G6 (84): stable sets [['P12:3|3', 'P13:3|3', 'P23:3|3']]; discriminatory sets 0.
- G8= (45): stable sets [['P12:4|4', 'P13:4|4', 'P23:4|4']]; discriminatory sets 0.
- G8 (165): stable sets [['P12:4|4', 'P13:4|4', 'P23:4|4']]; discriminatory sets 0.
- R6x (66): stable sets [['P12:3|3', 'P13:3|3', 'P23:3|3']]; discriminatory sets 0.
- R8x (141): stable sets [['P12:4|4', 'P13:4|4', 'P23:4|4']]; discriminatory sets 0.
- Chicken under C: [['R1'], ['R2']].

## Island classes by cell (fraction of islands; mean [95%] over runs)

### Horizon 500

| cell | runs | fair (V\*) | unequal | wasteful | grand | disagree | member-mixed | other-mixed | coverage (runs) | RS strong (runs) | consensus | resolved | efficiency |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L0 | 40 | 0.281 [0.263, 0.300] | 0.417 [0.395, 0.439] | 0.23 [0.21, 0.24] | 0.003 | 0.070 | 0.000 | 0.000 | 1.00 [0.91, 1.00] | 0.00 [0.00, 0.09] | 0.00 | 1.00 | 0.886 |
| L1 | 40 | 0.286 [0.227, 0.346] | 0.014 [0.006, 0.023] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.104 | 0.594 | 0.17 [0.09, 0.32] | 0.60 [0.45, 0.74] | 0.00 | 0.00 | 0.928 |
| M0 | 40 | 0.283 [0.264, 0.302] | 0.413 [0.390, 0.436] | 0.23 [0.21, 0.24] | 0.003 | 0.072 | 0.000 | 0.000 | 1.00 [0.91, 1.00] | 0.00 [0.00, 0.09] | 0.00 | 0.95 | 0.884 |
| M1 | 40 | 0.294 [0.238, 0.350] | 0.023 [0.011, 0.036] | 0.00 [-0.00, 0.00] | 0.000 | 0.000 | 0.094 | 0.586 | 0.23 [0.12, 0.38] | 0.53 [0.37, 0.67] | 0.00 | 0.00 | 0.930 |
| K0 | 40 | 0.286 [0.268, 0.303] | 0.409 [0.387, 0.432] | 0.23 [0.22, 0.25] | 0.002 | 0.071 | 0.000 | 0.000 | 1.00 [0.91, 1.00] | 0.00 [0.00, 0.09] | 0.00 | 0.97 | 0.885 |
| K1 | 40 | 0.271 [0.219, 0.324] | 0.018 [0.010, 0.026] | 0.00 [-0.00, 0.00] | 0.000 | 0.000 | 0.092 | 0.618 | 0.30 [0.18, 0.45] | 0.45 [0.31, 0.60] | 0.00 | 0.00 | 0.924 |
| U0 | 40 | 0.005 [0.002, 0.008] | 0.014 [0.009, 0.019] | 0.01 [0.01, 0.01] | 0.000 | 0.971 | 0.000 | 0.000 | 0.00 [0.00, 0.09] | 0.00 [0.00, 0.09] | 0.30 | 1.00 | 0.027 |
| U1 | 40 | 0.242 [0.126, 0.358] | 0.190 [0.091, 0.288] | 0.01 [-0.01, 0.02] | 0.000 | 0.333 | 0.007 | 0.220 | 0.00 [0.00, 0.09] | 0.20 [0.10, 0.35] | 0.35 | 0.28 | 0.635 |
| A0 | 40 | 0.173 [0.162, 0.184] | 0.499 [0.480, 0.518] | 0.28 [0.26, 0.29] | 0.004 | 0.047 | 0.000 | 0.000 | 0.97 [0.87, 1.00] | 0.00 [0.00, 0.09] | 0.00 | 1.00 | 0.898 |
| A1 | 40 | 0.096 [0.043, 0.148] | 0.186 [0.138, 0.234] | 0.00 [-0.00, 0.00] | 0.000 | 0.000 | 0.004 | 0.713 | 0.00 [0.00, 0.09] | 0.07 [0.03, 0.20] | 0.00 | 0.00 | 0.939 |
| Fe-fair | 20 | 0.670 [0.641, 0.698] | 0.170 [0.150, 0.190] | 0.14 [0.12, 0.16] | 0.001 | 0.021 | 0.000 | 0.000 | 0.90 [0.70, 0.97] | 0.00 [0.00, 0.16] | 0.00 | 1.00 | 0.955 |
| Fe-unequal | 20 | 0.144 [0.122, 0.166] | 0.694 [0.662, 0.726] | 0.13 [0.11, 0.15] | 0.002 | 0.027 | 0.000 | 0.000 | 0.90 [0.70, 0.97] | 0.00 [0.00, 0.16] | 0.00 | 1.00 | 0.948 |
| Fe-wasteful | 20 | 0.179 [0.153, 0.205] | 0.498 [0.476, 0.520] | 0.30 [0.28, 0.33] | 0.000 | 0.020 | 0.000 | 0.000 | 1.00 [0.84, 1.00] | 0.00 [0.00, 0.16] | 0.00 | 0.95 | 0.916 |
| Fe-grand | 20 | 0.197 [0.181, 0.212] | 0.333 [0.309, 0.357] | 0.19 [0.17, 0.21] | 0.131 | 0.151 | 0.000 | 0.000 | 1.00 [0.84, 1.00] | 0.00 [0.00, 0.16] | 0.00 | 1.00 | 0.812 |
| Fr-fair | 20 | 0.939 [0.909, 0.969] | 0.003 [-0.000, 0.007] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.004 | 0.054 | 0.00 [0.00, 0.16] | 0.85 [0.64, 0.95] | 0.20 | 0.00 | 0.995 |
| Fr-unequal | 20 | 0.143 [0.058, 0.228] | 0.322 [0.223, 0.420] | 0.00 [-0.00, 0.00] | 0.000 | 0.000 | 0.000 | 0.534 | 0.00 [0.00, 0.16] | 0.10 [0.03, 0.30] | 0.00 | 0.00 | 0.956 |
| Fr-wasteful | 20 | 0.092 [0.018, 0.166] | 0.192 [0.121, 0.263] | 0.00 [-0.00, 0.00] | 0.000 | 0.000 | 0.001 | 0.713 | 0.00 [0.00, 0.16] | 0.00 [0.00, 0.16] | 0.00 | 0.00 | 0.915 |
| Fr-grand | 20 | 0.051 [0.036, 0.066] | 0.032 [0.023, 0.041] | 0.01 [0.00, 0.01] | 0.128 | 0.000 | 0.001 | 0.783 | 0.10 [0.03, 0.30] | 0.00 [0.00, 0.16] | 0.00 | 0.00 | 0.840 |
| L0-N50 | 20 | 0.171 [0.154, 0.188] | 0.312 [0.288, 0.335] | 0.26 [0.24, 0.28] | 0.003 | 0.253 | 0.000 | 0.000 | 1.00 [0.84, 1.00] | 0.00 [0.00, 0.16] | 0.00 | 1.00 | 0.696 |
| L1-N50 | 20 | 0.525 [0.356, 0.694] | 0.165 [0.021, 0.309] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.113 | 0.197 | 0.00 [0.00, 0.16] | 0.70 [0.48, 0.85] | 0.25 | 0.00 | 0.981 |
| L0-N200 | 20 | 0.406 [0.372, 0.440] | 0.471 [0.442, 0.500] | 0.12 [0.10, 0.14] | 0.001 | 0.003 | 0.000 | 0.002 | 1.00 [0.84, 1.00] | 0.00 [0.00, 0.16] | 0.00 | 0.55 | 0.976 |
| L1-N200 | 20 | 0.213 [0.176, 0.251] | 0.072 [0.055, 0.089] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.052 | 0.663 | 0.80 [0.58, 0.92] | 0.00 [0.00, 0.16] | 0.00 | 0.00 | 0.944 |
| X6-0 | 40 | 0.153 [0.139, 0.167] | 0.370 [0.350, 0.389] | 0.32 [0.30, 0.33] | 0.009 | 0.153 | 0.000 | 0.000 | 0.90 [0.77, 0.96] | 0.00 [0.00, 0.09] | 0.00 | 1.00 | 0.772 |
| X6-1 | 40 | 0.192 [0.132, 0.251] | 0.055 [0.037, 0.074] | 0.00 [-0.00, 0.00] | 0.000 | 0.000 | 0.043 | 0.709 | 0.05 [0.01, 0.17] | 0.17 [0.09, 0.32] | 0.00 | 0.00 | 0.906 |
| X8-0 | 40 | 0.087 [0.075, 0.098] | 0.312 [0.291, 0.334] | 0.40 [0.38, 0.42] | 0.011 | 0.190 | 0.000 | 0.000 | 0.62 [0.47, 0.76] | 0.00 [0.00, 0.09] | 0.00 | 0.97 | 0.724 |
| X8-1 | 40 | 0.150 [0.089, 0.212] | 0.087 [0.059, 0.114] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.013 | 0.749 | 0.00 [0.00, 0.09] | 0.12 [0.05, 0.26] | 0.00 | 0.00 | 0.902 |
| L1-N150 | 20 | 0.242 [0.195, 0.289] | 0.041 [0.027, 0.056] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.069 | 0.648 | 0.45 [0.26, 0.66] | 0.10 [0.03, 0.30] | 0.00 | 0.00 | 0.936 |
| L1-N300 | 20 | 0.293 [0.263, 0.323] | 0.134 [0.113, 0.155] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.061 | 0.512 | 0.95 [0.76, 0.99] | 0.00 [0.00, 0.16] | 0.00 | 0.00 | 0.962 |
| L1-N400 | 20 | 0.383 [0.358, 0.408] | 0.177 [0.157, 0.196] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.068 | 0.373 | 1.00 [0.84, 1.00] | 0.00 [0.00, 0.16] | 0.00 | 0.00 | 0.971 |

### Horizon 2000

| cell | runs | fair (V\*) | unequal | wasteful | grand | disagree | member-mixed | other-mixed | coverage (runs) | RS strong (runs) | consensus | resolved | efficiency |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L0 | 40 | 0.281 [0.263, 0.300] | 0.417 [0.395, 0.439] | 0.23 [0.21, 0.24] | 0.003 | 0.070 | 0.000 | 0.000 | 1.00 [0.91, 1.00] | 0.00 [0.00, 0.09] | 0.00 | 1.00 | 0.886 |
| L1 | 40 | 0.739 [0.620, 0.858] | 0.138 [0.033, 0.242] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.097 | 0.026 | 0.00 [0.00, 0.09] | 0.82 [0.68, 0.91] | 0.65 | 0.10 | 1.000 |
| M0 | 40 | 0.283 [0.264, 0.302] | 0.413 [0.390, 0.436] | 0.23 [0.21, 0.24] | 0.003 | 0.072 | 0.000 | 0.000 | 1.00 [0.91, 1.00] | 0.00 [0.00, 0.09] | 0.00 | 1.00 | 0.884 |
| M1 | 40 | 0.641 [0.508, 0.775] | 0.228 [0.103, 0.352] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.072 | 0.059 | 0.00 [0.00, 0.09] | 0.70 [0.55, 0.82] | 0.72 | 0.20 | 0.999 |
| K0 | 40 | 0.286 [0.268, 0.303] | 0.409 [0.387, 0.432] | 0.23 [0.22, 0.25] | 0.002 | 0.071 | 0.000 | 0.000 | 1.00 [0.91, 1.00] | 0.00 [0.00, 0.09] | 0.00 | 1.00 | 0.885 |
| K1 | 40 | 0.658 [0.531, 0.786] | 0.195 [0.073, 0.318] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.135 | 0.012 | 0.00 [0.00, 0.09] | 0.78 [0.62, 0.88] | 0.62 | 0.15 | 1.000 |
| U0 | 40 | 0.005 [0.002, 0.008] | 0.014 [0.009, 0.019] | 0.01 [0.01, 0.01] | 0.000 | 0.971 | 0.000 | 0.000 | 0.00 [0.00, 0.09] | 0.00 [0.00, 0.09] | 0.30 | 1.00 | 0.027 |
| U1 | 40 | 0.254 [0.119, 0.389] | 0.380 [0.232, 0.529] | 0.00 [0.00, 0.00] | 0.000 | 0.324 | 0.000 | 0.041 | 0.00 [0.00, 0.09] | 0.25 [0.14, 0.40] | 0.88 | 0.50 | 0.673 |
| A0 | 40 | 0.173 [0.162, 0.184] | 0.499 [0.480, 0.518] | 0.28 [0.26, 0.29] | 0.004 | 0.047 | 0.000 | 0.000 | 0.97 [0.87, 1.00] | 0.00 [0.00, 0.09] | 0.00 | 1.00 | 0.898 |
| A1 | 40 | 0.422 [0.273, 0.571] | 0.398 [0.262, 0.533] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.034 | 0.146 | 0.00 [0.00, 0.09] | 0.45 [0.31, 0.60] | 0.60 | 0.20 | 0.996 |
| Fe-fair | 20 | 0.670 [0.641, 0.698] | 0.170 [0.150, 0.190] | 0.14 [0.12, 0.16] | 0.001 | 0.021 | 0.000 | 0.000 | 0.90 [0.70, 0.97] | 0.00 [0.00, 0.16] | 0.00 | 1.00 | 0.955 |
| Fe-unequal | 20 | 0.144 [0.122, 0.166] | 0.694 [0.662, 0.726] | 0.13 [0.11, 0.15] | 0.002 | 0.027 | 0.000 | 0.000 | 0.90 [0.70, 0.97] | 0.00 [0.00, 0.16] | 0.00 | 1.00 | 0.948 |
| Fe-wasteful | 20 | 0.179 [0.153, 0.205] | 0.498 [0.476, 0.520] | 0.30 [0.28, 0.33] | 0.000 | 0.020 | 0.000 | 0.000 | 1.00 [0.84, 1.00] | 0.00 [0.00, 0.16] | 0.00 | 1.00 | 0.916 |
| Fe-grand | 20 | 0.197 [0.181, 0.212] | 0.333 [0.309, 0.357] | 0.19 [0.17, 0.21] | 0.131 | 0.151 | 0.000 | 0.000 | 1.00 [0.84, 1.00] | 0.00 [0.00, 0.16] | 0.00 | 1.00 | 0.812 |
| Fr-fair | 20 | 0.700 [0.494, 0.906] | 0.300 [0.094, 0.506] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 [0.00, 0.16] | 0.70 [0.48, 0.85] | 1.00 | 0.35 | 1.000 |
| Fr-unequal | 20 | 0.600 [0.380, 0.820] | 0.400 [0.180, 0.620] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 [0.00, 0.16] | 0.60 [0.39, 0.78] | 1.00 | 0.70 | 1.000 |
| Fr-wasteful | 20 | 0.421 [0.206, 0.637] | 0.545 [0.323, 0.766] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.027 | 0.007 | 0.00 [0.00, 0.16] | 0.45 [0.26, 0.66] | 0.85 | 0.30 | 1.000 |
| Fr-grand | 20 | 0.673 [0.512, 0.833] | 0.147 [-0.007, 0.301] | 0.00 [0.00, 0.00] | 0.007 | 0.000 | 0.021 | 0.152 | 0.00 [0.00, 0.16] | 0.55 [0.34, 0.74] | 0.15 | 0.00 | 0.972 |
| L0-N50 | 20 | 0.171 [0.154, 0.188] | 0.312 [0.288, 0.335] | 0.26 [0.24, 0.28] | 0.003 | 0.253 | 0.000 | 0.000 | 1.00 [0.84, 1.00] | 0.00 [0.00, 0.16] | 0.00 | 1.00 | 0.696 |
| L1-N50 | 20 | 0.837 [0.677, 0.996] | 0.150 [-0.011, 0.311] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.013 | 0.000 | 0.00 [0.00, 0.16] | 0.85 [0.64, 0.95] | 0.90 | 0.35 | 1.000 |
| L0-N200 | 20 | 0.407 [0.373, 0.441] | 0.472 [0.443, 0.501] | 0.12 [0.10, 0.14] | 0.001 | 0.003 | 0.000 | 0.000 | 1.00 [0.84, 1.00] | 0.00 [0.00, 0.16] | 0.00 | 1.00 | 0.976 |
| L1-N200 | 20 | 0.500 [0.353, 0.647] | 0.216 [0.051, 0.381] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.144 | 0.141 | 0.10 [0.03, 0.30] | 0.40 [0.22, 0.61] | 0.00 | 0.00 | 0.988 |
| X6-0 | 40 | 0.153 [0.139, 0.167] | 0.370 [0.350, 0.389] | 0.32 [0.30, 0.33] | 0.009 | 0.153 | 0.000 | 0.000 | 0.90 [0.77, 0.96] | 0.00 [0.00, 0.09] | 0.00 | 1.00 | 0.772 |
| X6-1 | 40 | 0.595 [0.456, 0.734] | 0.289 [0.149, 0.428] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.098 | 0.018 | 0.00 [0.00, 0.09] | 0.68 [0.52, 0.80] | 0.70 | 0.17 | 0.999 |
| X8-0 | 40 | 0.087 [0.075, 0.098] | 0.312 [0.291, 0.334] | 0.40 [0.38, 0.42] | 0.011 | 0.190 | 0.000 | 0.000 | 0.62 [0.47, 0.76] | 0.00 [0.00, 0.09] | 0.00 | 1.00 | 0.724 |
| X8-1 | 40 | 0.480 [0.335, 0.625] | 0.384 [0.243, 0.526] | 0.00 [-0.00, 0.00] | 0.000 | 0.000 | 0.046 | 0.089 | 0.00 [0.00, 0.09] | 0.53 [0.37, 0.67] | 0.65 | 0.23 | 0.996 |
| L1-N150 | 20 | 0.641 [0.480, 0.803] | 0.136 [-0.008, 0.280] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.188 | 0.035 | 0.00 [0.00, 0.16] | 0.75 [0.53, 0.89] | 0.15 | 0.00 | 0.998 |
| L1-N300 | 20 | 0.466 [0.384, 0.547] | 0.091 [0.017, 0.164] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.234 | 0.210 | 0.50 [0.30, 0.70] | 0.05 [0.01, 0.24] | 0.00 | 0.00 | 0.982 |
| L1-N400 | 20 | 0.473 [0.441, 0.505] | 0.064 [0.041, 0.087] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.274 | 0.188 | 0.95 [0.76, 0.99] | 0.10 [0.03, 0.30] | 0.00 | 0.00 | 0.981 |

### Horizon 10000

| cell | runs | fair (V\*) | unequal | wasteful | grand | disagree | member-mixed | other-mixed | coverage (runs) | RS strong (runs) | consensus | resolved | efficiency |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L0 | 40 | 0.281 [0.263, 0.300] | 0.417 [0.395, 0.439] | 0.23 [0.21, 0.24] | 0.003 | 0.070 | 0.000 | 0.000 | 1.00 [0.91, 1.00] | 0.00 [0.00, 0.09] | 0.00 | 1.00 | 0.886 |
| L1 | 40 | 0.805 [0.686, 0.925] | 0.175 [0.056, 0.294] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.020 | 0.000 | 0.00 [0.00, 0.09] | 0.82 [0.68, 0.91] | 0.95 | 0.80 | 1.000 |
| M0 | 40 | 0.283 [0.264, 0.302] | 0.413 [0.390, 0.436] | 0.23 [0.21, 0.24] | 0.003 | 0.072 | 0.000 | 0.000 | 1.00 [0.91, 1.00] | 0.00 [0.00, 0.09] | 0.00 | 1.00 | 0.884 |
| M1 | 40 | 0.691 [0.548, 0.834] | 0.285 [0.146, 0.425] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.009 | 0.015 | 0.00 [0.00, 0.09] | 0.70 [0.55, 0.82] | 0.95 | 0.82 | 1.000 |
| K0 | 40 | 0.286 [0.268, 0.303] | 0.409 [0.387, 0.432] | 0.23 [0.22, 0.25] | 0.002 | 0.071 | 0.000 | 0.000 | 1.00 [0.91, 1.00] | 0.00 [0.00, 0.09] | 0.00 | 1.00 | 0.885 |
| K1 | 40 | 0.771 [0.644, 0.897] | 0.200 [0.074, 0.326] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.029 | 0.000 | 0.00 [0.00, 0.09] | 0.80 [0.65, 0.90] | 0.90 | 0.68 | 1.000 |
| U0 | 40 | 0.005 [0.002, 0.008] | 0.014 [0.009, 0.019] | 0.01 [0.01, 0.01] | 0.000 | 0.971 | 0.000 | 0.000 | 0.00 [0.00, 0.09] | 0.00 [0.00, 0.09] | 0.30 | 1.00 | 0.027 |
| U1 | 40 | 0.275 [0.135, 0.415] | 0.382 [0.232, 0.533] | 0.00 [0.00, 0.00] | 0.000 | 0.325 | 0.000 | 0.018 | 0.00 [0.00, 0.09] | 0.28 [0.16, 0.43] | 0.97 | 0.78 | 0.675 |
| A0 | 40 | 0.173 [0.162, 0.184] | 0.499 [0.480, 0.518] | 0.28 [0.26, 0.29] | 0.004 | 0.047 | 0.000 | 0.000 | 0.97 [0.87, 1.00] | 0.00 [0.00, 0.09] | 0.00 | 1.00 | 0.898 |
| A1 | 40 | 0.457 [0.304, 0.609] | 0.475 [0.326, 0.623] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.018 | 0.050 | 0.00 [0.00, 0.09] | 0.47 [0.33, 0.63] | 0.82 | 0.72 | 1.000 |
| Fe-fair | 20 | 0.670 [0.641, 0.698] | 0.170 [0.150, 0.190] | 0.14 [0.12, 0.16] | 0.001 | 0.021 | 0.000 | 0.000 | 0.90 [0.70, 0.97] | 0.00 [0.00, 0.16] | 0.00 | 1.00 | 0.955 |
| Fe-unequal | 20 | 0.144 [0.122, 0.166] | 0.694 [0.662, 0.726] | 0.13 [0.11, 0.15] | 0.002 | 0.027 | 0.000 | 0.000 | 0.90 [0.70, 0.97] | 0.00 [0.00, 0.16] | 0.00 | 1.00 | 0.948 |
| Fe-wasteful | 20 | 0.179 [0.153, 0.205] | 0.498 [0.476, 0.520] | 0.30 [0.28, 0.33] | 0.000 | 0.020 | 0.000 | 0.000 | 1.00 [0.84, 1.00] | 0.00 [0.00, 0.16] | 0.00 | 1.00 | 0.916 |
| Fe-grand | 20 | 0.197 [0.181, 0.212] | 0.333 [0.309, 0.357] | 0.19 [0.17, 0.21] | 0.131 | 0.151 | 0.000 | 0.000 | 1.00 [0.84, 1.00] | 0.00 [0.00, 0.16] | 0.00 | 1.00 | 0.812 |
| Fr-fair | 20 | 0.700 [0.494, 0.906] | 0.300 [0.094, 0.506] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 [0.00, 0.16] | 0.70 [0.48, 0.85] | 1.00 | 0.60 | 1.000 |
| Fr-unequal | 20 | 0.600 [0.380, 0.820] | 0.400 [0.180, 0.620] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 [0.00, 0.16] | 0.60 [0.39, 0.78] | 1.00 | 0.95 | 1.000 |
| Fr-wasteful | 20 | 0.500 [0.275, 0.725] | 0.500 [0.275, 0.725] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 [0.00, 0.16] | 0.50 [0.30, 0.70] | 1.00 | 0.85 | 1.000 |
| Fr-grand | 20 | 0.750 [0.555, 0.945] | 0.250 [0.055, 0.445] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 [0.00, 0.16] | 0.75 [0.53, 0.89] | 1.00 | 0.75 | 1.000 |
| L0-N50 | 20 | 0.171 [0.154, 0.188] | 0.312 [0.288, 0.335] | 0.26 [0.24, 0.28] | 0.003 | 0.253 | 0.000 | 0.000 | 1.00 [0.84, 1.00] | 0.00 [0.00, 0.16] | 0.00 | 1.00 | 0.696 |
| L1-N50 | 20 | 0.826 [0.663, 0.989] | 0.150 [-0.011, 0.311] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.024 | 0.000 | 0.00 [0.00, 0.16] | 0.85 [0.64, 0.95] | 0.95 | 0.90 | 1.000 |
| L0-N200 | 20 | 0.407 [0.373, 0.441] | 0.472 [0.443, 0.501] | 0.12 [0.10, 0.14] | 0.001 | 0.003 | 0.000 | 0.000 | 1.00 [0.84, 1.00] | 0.00 [0.00, 0.16] | 0.00 | 1.00 | 0.976 |
| L1-N200 | 20 | 0.155 [0.015, 0.294] | 0.750 [0.555, 0.945] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.093 | 0.002 | 0.00 [0.00, 0.16] | 0.25 [0.11, 0.47] | 0.85 | 0.50 | 1.000 |
| X6-0 | 40 | 0.153 [0.139, 0.167] | 0.370 [0.350, 0.389] | 0.32 [0.30, 0.33] | 0.009 | 0.153 | 0.000 | 0.000 | 0.90 [0.77, 0.96] | 0.00 [0.00, 0.09] | 0.00 | 1.00 | 0.772 |
| X6-1 | 40 | 0.648 [0.503, 0.793] | 0.325 [0.178, 0.472] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.027 | 0.000 | 0.00 [0.00, 0.09] | 0.68 [0.52, 0.80] | 0.90 | 0.60 | 1.000 |
| X8-0 | 40 | 0.087 [0.075, 0.098] | 0.312 [0.291, 0.334] | 0.40 [0.38, 0.42] | 0.011 | 0.190 | 0.000 | 0.000 | 0.62 [0.47, 0.76] | 0.00 [0.00, 0.09] | 0.00 | 1.00 | 0.724 |
| X8-1 | 40 | 0.500 [0.343, 0.657] | 0.500 [0.343, 0.657] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.000 | 0.000 | 0.00 [0.00, 0.09] | 0.50 [0.35, 0.65] | 1.00 | 0.85 | 1.000 |
| L1-N150 | 20 | 0.674 [0.483, 0.866] | 0.250 [0.055, 0.445] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.076 | 0.000 | 0.00 [0.00, 0.16] | 0.75 [0.53, 0.89] | 0.80 | 0.60 | 1.000 |
| L1-N300 | 20 | 0.236 [0.063, 0.409] | 0.690 [0.489, 0.890] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.041 | 0.034 | 0.00 [0.00, 0.16] | 0.20 [0.08, 0.42] | 0.65 | 0.50 | 0.998 |
| L1-N400 | 20 | 0.368 [0.199, 0.537] | 0.421 [0.216, 0.626] | 0.00 [0.00, 0.00] | 0.000 | 0.000 | 0.155 | 0.055 | 0.00 [0.00, 0.16] | 0.15 [0.05, 0.36] | 0.25 | 0.05 | 0.997 |

## Selection, symmetry, farsighted contrast (horizon 2,000)

| cell | members present (of 3) | unequal / (fair+unequal) | in no stable set | far (TU) not myopic | far (game) not myopic | member shares P12/P13/P23 | modal member (runs) | slot-3 low rate | islands with non-member support |
|---|---|---|---|---|---|---|---|---|---|
| L0 | 3.00 | 0.596 [0.570, 0.623] | 0.719 | 0.420 | 0.417 | 0.34/0.35/0.31 | 0.31/0.45/0.25 | 0.328 | 0.719 |
| L1 | 1.00 | 0.154 [0.042, 0.265] | 0.138 | 0.138 | 0.138 | 0.41/0.22/0.38 | 0.35/0.20/0.30 | 0.000 | 0.168 |
| M0 | 3.00 | 0.592 [0.563, 0.620] | 0.717 | 0.416 | 0.413 | 0.34/0.35/0.31 | 0.30/0.46/0.24 | 0.330 | 0.717 |
| M1 | 0.85 | 0.272 [0.135, 0.409] | 0.228 | 0.228 | 0.228 | 0.48/0.12/0.40 | 0.33/0.10/0.33 | 0.131 | 0.291 |
| K0 | 3.00 | 0.587 [0.561, 0.614] | 0.714 | 0.411 | 0.409 | 0.35/0.35/0.30 | 0.39/0.40/0.21 | 0.329 | 0.714 |
| K1 | 1.02 | 0.200 [0.075, 0.326] | 0.195 | 0.195 | 0.195 | 0.45/0.23/0.31 | 0.35/0.20/0.25 | 0.242 | 0.211 |
| U0 | 0.28 | 0.744 [0.601, 0.888] | 0.995 | 0.014 | 0.014 | 0.25/0.17/0.58 | 0.07/0.03/0.15 | 0.370 | 0.995 |
| U1 | 0.28 | 0.607 [0.423, 0.791] | 0.705 | 0.380 | 0.380 | 0.12/0.39/0.49 | 0.05/0.10/0.12 | 0.201 | 0.751 |
| A0 | 2.98 | 0.741 [0.725, 0.758] | 0.827 | 0.503 | 0.499 | 0.42/0.27/0.31 | 0.49/0.26/0.25 | 0.628 | 0.827 |
| A1 | 0.57 | 0.529 [0.374, 0.683] | 0.398 | 0.398 | 0.398 | 0.00/0.57/0.43 | 0.00/0.30/0.23 | 0.190 | 0.547 |
| Fe-fair | 2.90 | 0.203 [0.180, 0.227] | 0.330 | 0.171 | 0.170 | 0.89/0.06/0.05 | 1.00/0.00/0.00 | 0.464 | 0.330 |
| Fe-unequal | 2.85 | 0.828 [0.801, 0.854] | 0.856 | 0.695 | 0.694 | 0.33/0.23/0.44 | 0.19/0.07/0.74 | 0.371 | 0.856 |
| Fe-wasteful | 3.00 | 0.738 [0.704, 0.772] | 0.821 | 0.498 | 0.498 | 0.50/0.24/0.26 | 0.78/0.12/0.10 | 0.404 | 0.821 |
| Fe-grand | 3.00 | 0.627 [0.597, 0.656] | 0.803 | 0.464 | 0.333 | 0.31/0.37/0.31 | 0.38/0.35/0.28 | 0.360 | 0.803 |
| Fr-fair | 0.70 | 0.300 [0.094, 0.506] | 0.300 | 0.300 | 0.300 | 1.00/0.00/0.00 | 0.70/0.00/0.00 | 1.000 | 0.300 |
| Fr-unequal | 0.60 | 0.400 [0.180, 0.620] | 0.400 | 0.400 | 0.400 | 0.00/0.00/1.00 | 0.00/0.00/0.60 | 0.368 | 0.400 |
| Fr-wasteful | 0.50 | 0.550 [0.326, 0.774] | 0.545 | 0.545 | 0.545 | 0.17/0.36/0.47 | 0.10/0.15/0.20 | 0.496 | 0.552 |
| Fr-grand | 1.00 | 0.154 [-0.005, 0.313] | 0.154 | 0.154 | 0.147 | 0.47/0.13/0.40 | 0.40/0.10/0.40 | 0.118 | 0.406 |
| L0-N50 | 3.00 | 0.644 [0.607, 0.681] | 0.829 | 0.315 | 0.312 | 0.32/0.35/0.33 | 0.25/0.42/0.33 | 0.359 | 0.829 |
| L1-N50 | 0.90 | 0.150 [-0.011, 0.311] | 0.150 | 0.150 | 0.150 | 0.29/0.59/0.12 | 0.25/0.50/0.10 | 0.072 | 0.150 |
| L0-N200 | 3.00 | 0.538 [0.504, 0.572] | 0.593 | 0.473 | 0.472 | 0.36/0.29/0.35 | 0.57/0.04/0.39 | 0.284 | 0.593 |
| L1-N200 | 1.30 | 0.251 [0.073, 0.429] | 0.216 | 0.216 | 0.216 | 0.37/0.29/0.34 | 0.25/0.30/0.30 | 0.238 | 0.478 |
| X6-0 | 2.90 | 0.708 [0.685, 0.732] | 0.847 | 0.376 | 0.370 | 0.30/0.34/0.35 | 0.32/0.33/0.35 | 0.398 | 0.847 |
| X6-1 | 0.85 | 0.301 [0.157, 0.445] | 0.289 | 0.289 | 0.289 | 0.38/0.26/0.36 | 0.33/0.15/0.23 | 0.181 | 0.310 |
| X8-0 | 2.55 | 0.780 [0.751, 0.810] | 0.913 | 0.316 | 0.312 | 0.36/0.33/0.31 | 0.34/0.27/0.39 | 0.405 | 0.913 |
| X8-1 | 0.68 | 0.451 [0.297, 0.604] | 0.385 | 0.384 | 0.384 | 0.18/0.41/0.41 | 0.12/0.25/0.20 | 0.220 | 0.488 |
| L1-N150 | 1.20 | 0.148 [-0.007, 0.303] | 0.136 | 0.136 | 0.136 | 0.44/0.25/0.30 | 0.35/0.15/0.40 | 0.004 | 0.202 |
| L1-N300 | 2.30 | 0.148 [0.053, 0.244] | 0.091 | 0.091 | 0.091 | 0.31/0.45/0.24 | 0.35/0.40/0.20 | 0.029 | 0.570 |
| L1-N400 | 2.95 | 0.120 [0.074, 0.166] | 0.064 | 0.064 | 0.064 | 0.36/0.36/0.28 | 0.42/0.40/0.17 | 0.100 | 0.611 |

## Transience and dwell

| cell | islands ever on a member | median gen to first member (if reached) | grand: visits/run, KM median dwell, censored | wasteful: visits/run, KM median dwell, censored | stop gen median (resolved runs) |
|---|---|---|---|---|---|
| L0 | 0.283 | 58.0 | 0.2, 2, 0.29 | 15.1, None, 0.60 | 280 (40/40) |
| L1 | 0.984 | 260.0 | 0.0, None, 0.00 | 9.5, 2, 0.00 | 5570 (32/40) |
| M0 | 0.284 | 58.0 | 0.2, 8, 0.43 | 14.9, None, 0.60 | 290 (40/40) |
| M1 | 0.993 | 269.0 | 0.0, 1, 0.00 | 9.9, 2, 0.00 | 4255 (33/40) |
| K0 | 0.286 | 57.0 | 0.1, 2, 0.40 | 15.3, None, 0.55 | 285 (40/40) |
| K1 | 0.998 | 274.0 | 0.0, 3, 0.00 | 10.1, 2, 0.00 | 4535 (27/40) |
| U0 | 0.005 | 64.0 | 0.0, None, 1.00 | 0.7, 3, 0.50 | 160 (40/40) |
| U1 | 0.407 | 352.0 | 0.0, 1, 0.00 | 6.0, 2, 0.00 | 1965 (31/40) |
| A0 | 0.174 | 63.0 | 0.2, None, 0.70 | 18.2, None, 0.54 | 300 (40/40) |
| A1 | 0.675 | 426.0 | 0.0, None, 0.00 | 11.4, 2, 0.00 | 3880 (29/40) |
| Fe-fair | 0.671 | 46.0 | 0.1, 1, 0.00 | 9.3, None, 0.63 | 285 (20/20) |
| Fe-unequal | 0.144 | 59.0 | 0.1, 1, 0.00 | 9.1, None, 0.57 | 290 (20/20) |
| Fe-wasteful | 0.180 | 65.0 | 0.0, None, 0.00 | 19.8, None, 0.58 | 285 (20/20) |
| Fe-grand | 0.199 | 55.0 | 8.4, None, 0.62 | 12.4, None, 0.59 | 270 (20/20) |
| Fr-fair | 0.997 | 0.0 | 0.0, None, 0.00 | 2.1, 2, 0.00 | 7255 (12/20) |
| Fr-unequal | 0.696 | 518.0 | 0.1, 1, 0.00 | 4.2, 2, 0.00 | 1305 (19/20) |
| Fr-wasteful | 0.793 | 586.0 | 0.0, None, 0.00 | 38.7, 7, 0.00 | 2960 (17/20) |
| Fr-grand | 0.942 | 1064.0 | 34.7, 5, 0.00 | 8.2, 2, 0.00 | 5645 (15/20) |
| L0-N50 | 0.171 | 36.0 | 0.2, None, 0.75 | 16.9, None, 0.72 | 150 (20/20) |
| L1-N50 | 0.920 | 237.0 | 0.0, None, 0.00 | 16.9, 2, 0.00 | 2640 (18/20) |
| L0-N200 | 0.409 | 84.0 | 0.1, None, 1.00 | 7.6, None, 0.54 | 500 (20/20) |
| L1-N200 | 0.955 | 255.0 | 0.0, None, 0.00 | 3.0, 2, 0.00 | 9445 (10/20) |
| X6-0 | 0.153 | 59.0 | 0.6, None, 0.62 | 20.3, None, 0.58 | 295 (40/40) |
| X6-1 | 0.918 | 358.0 | 0.1, 3, 0.00 | 12.8, 2, 0.00 | 6635 (24/40) |
| X8-0 | 0.087 | 58.0 | 0.7, None, 0.62 | 25.7, None, 0.58 | 290 (40/40) |
| X8-1 | 0.813 | 438.5 | 0.1, 1, 0.00 | 22.1, 2, 0.00 | 3580 (34/40) |
| L1-N150 | 0.990 | 251.0 | 0.1, 5, 0.00 | 5.3, 3, 0.00 | 8830 (12/20) |
| L1-N300 | 0.942 | 210.0 | 0.0, None, 0.00 | 1.5, 2, 0.00 | 9825 (10/20) |
| L1-N400 | 0.966 | 211.0 | 0.0, None, 0.00 | 0.7, 3, 0.00 | 10000 (1/20) |

## Flips under migration (mN = 1)

**L1**: flips per run 49.3 [15.3, 83.2]; by type {'member->member': 1350, 'member->unequal': 357, 'unequal->unequal': 164, 'unequal->member': 71, 'disagreement->member': 26, 'disagreement->unequal': 3}; triggers {'pure drift': 1219, 'two-slot coincidence': 445, 'single-slot strict': 102, 'conditional': 100, 'other': 66, 'drift-prepared': 39}; member→member 1350, via an outsider class 8, via other-mixed 134; steps out of a non-member following an M arrow 175/385; all steps following an arrow 529/2578.
  triggers by type: {'member->member': {'pure drift': 1219, 'two-slot coincidence': 92, 'other': 31, 'single-slot strict': 5, 'drift-prepared': 3}, 'disagreement->member': {'two-slot coincidence': 26}, 'member->unequal': {'two-slot coincidence': 217, 'single-slot strict': 86, 'other': 29, 'drift-prepared': 25}, 'disagreement->unequal': {'two-slot coincidence': 3}, 'unequal->member': {'two-slot coincidence': 60, 'drift-prepared': 5, 'single-slot strict': 4, 'other': 2}, 'unequal->unequal': {'conditional': 100, 'two-slot coincidence': 47, 'single-slot strict': 7, 'drift-prepared': 6, 'other': 4}}

**M1**: flips per run 47.5 [23.8, 71.3]; by type {'member->unequal': 722, 'member->member': 661, 'unequal->unequal': 385, 'unequal->member': 102, 'disagreement->member': 29, 'disagreement->unequal': 2, 'wasteful->unequal': 1}; triggers {'pure drift': 844, 'two-slot coincidence': 677, 'single-slot strict': 206, 'other': 100, 'drift-prepared': 54, 'conditional': 21}; member→member 661, via an outsider class 5, via other-mixed 103; steps out of a non-member following an M arrow 146/796; all steps following an arrow 906/2388.
  triggers by type: {'member->member': {'pure drift': 477, 'two-slot coincidence': 134, 'other': 24, 'conditional': 14, 'single-slot strict': 10, 'drift-prepared': 2}, 'disagreement->member': {'two-slot coincidence': 29}, 'member->unequal': {'two-slot coincidence': 424, 'single-slot strict': 185, 'other': 61, 'drift-prepared': 45, 'conditional': 7}, 'unequal->member': {'two-slot coincidence': 79, 'single-slot strict': 8, 'other': 8, 'drift-prepared': 7}, 'disagreement->unequal': {'two-slot coincidence': 2}, 'unequal->unequal': {'pure drift': 367, 'two-slot coincidence': 8, 'other': 7, 'single-slot strict': 3}, 'wasteful->unequal': {'two-slot coincidence': 1}}

**K1**: flips per run 77.9 [37.0, 118.7]; by type {'member->member': 2392, 'member->unequal': 573, 'unequal->member': 136, 'disagreement->member': 10, 'wasteful->member': 2, 'unequal->unequal': 1, 'disagreement->unequal': 1}; triggers {'pure drift': 2242, 'two-slot coincidence': 512, 'single-slot strict': 210, 'other': 86, 'drift-prepared': 65}; member→member 2392, via an outsider class 5, via other-mixed 166; steps out of a non-member following an M arrow 150/179; all steps following an arrow 737/4084.
  triggers by type: {'member->unequal': {'two-slot coincidence': 316, 'single-slot strict': 170, 'drift-prepared': 51, 'other': 36}, 'disagreement->member': {'two-slot coincidence': 10}, 'unequal->member': {'two-slot coincidence': 85, 'single-slot strict': 30, 'drift-prepared': 14, 'other': 7}, 'member->member': {'pure drift': 2242, 'two-slot coincidence': 98, 'other': 43, 'single-slot strict': 9}, 'wasteful->member': {'two-slot coincidence': 1, 'single-slot strict': 1}, 'unequal->unequal': {'two-slot coincidence': 1}, 'disagreement->unequal': {'two-slot coincidence': 1}}

**U1**: flips per run 72.8 [40.4, 105.2]; by type {'disagreement->unequal': 859, 'unequal->unequal': 836, 'disagreement->member': 764, 'member->unequal': 244, 'unequal->member': 107, 'wasteful->member': 50, 'disagreement->wasteful': 48, 'member->wasteful': 2, 'member->member': 2}; triggers {'two-slot coincidence': 2232, 'conditional': 604, 'drift-prepared': 44, 'other': 32}; member→member 2, via an outsider class 0, via other-mixed 2; steps out of a non-member following an M arrow 2097/3334; all steps following an arrow 2388/3757.
  triggers by type: {'disagreement->member': {'two-slot coincidence': 760, 'conditional': 2, 'other': 2}, 'member->unequal': {'two-slot coincidence': 205, 'conditional': 17, 'other': 11, 'drift-prepared': 11}, 'unequal->unequal': {'conditional': 583, 'two-slot coincidence': 210, 'drift-prepared': 27, 'other': 16}, 'disagreement->unequal': {'two-slot coincidence': 858, 'drift-prepared': 1}, 'disagreement->wasteful': {'two-slot coincidence': 47, 'drift-prepared': 1}, 'wasteful->member': {'two-slot coincidence': 49, 'other': 1}, 'member->wasteful': {'drift-prepared': 1, 'two-slot coincidence': 1}, 'member->member': {'two-slot coincidence': 2}, 'unequal->member': {'two-slot coincidence': 100, 'drift-prepared': 3, 'conditional': 2, 'other': 2}}

**A1**: flips per run 87.6 [45.2, 130.0]; by type {'unequal->unequal': 2241, 'member->member': 778, 'unequal->member': 275, 'member->unequal': 196, 'disagreement->unequal': 6, 'disagreement->member': 4, 'wasteful->unequal': 2, 'member->wasteful': 1, 'wasteful->member': 1}; triggers {'pure drift': 1907, 'two-slot coincidence': 1326, 'single-slot strict': 82, 'other': 75, 'conditional': 74, 'drift-prepared': 40}; member→member 778, via an outsider class 0, via other-mixed 35; steps out of a non-member following an M arrow 567/3374; all steps following an arrow 772/4707.
  triggers by type: {'unequal->unequal': {'pure drift': 1167, 'two-slot coincidence': 933, 'conditional': 60, 'other': 44, 'drift-prepared': 19, 'single-slot strict': 18}, 'unequal->member': {'two-slot coincidence': 256, 'single-slot strict': 8, 'drift-prepared': 7, 'other': 4}, 'disagreement->member': {'two-slot coincidence': 4}, 'disagreement->unequal': {'two-slot coincidence': 6}, 'member->unequal': {'two-slot coincidence': 103, 'single-slot strict': 55, 'conditional': 14, 'drift-prepared': 14, 'other': 10}, 'member->member': {'pure drift': 740, 'two-slot coincidence': 22, 'other': 16}, 'wasteful->unequal': {'two-slot coincidence': 2}, 'member->wasteful': {'other': 1}, 'wasteful->member': {'single-slot strict': 1}}

**Fr-fair**: flips per run 19.1 [6.1, 32.1]; by type {'member->unequal': 379, 'disagreement->member': 3}; triggers {'two-slot coincidence': 176, 'single-slot strict': 139, 'drift-prepared': 43, 'other': 24}; member→member 0, via an outsider class 0, via other-mixed 0; steps out of a non-member following an M arrow 3/19; all steps following an arrow 394/411.
  triggers by type: {'disagreement->member': {'two-slot coincidence': 3}, 'member->unequal': {'two-slot coincidence': 173, 'single-slot strict': 139, 'drift-prepared': 43, 'other': 24}}

**Fr-unequal**: flips per run 54.3 [48.1, 60.5]; by type {'unequal->member': 656, 'unequal->unequal': 363, 'member->unequal': 64, 'disagreement->unequal': 2, 'disagreement->member': 1}; triggers {'two-slot coincidence': 826, 'single-slot strict': 111, 'drift-prepared': 83, 'other': 65, 'conditional': 1}; member→member 0, via an outsider class 0, via other-mixed 0; steps out of a non-member following an M arrow 1029/1094; all steps following an arrow 1097/1185.
  triggers by type: {'unequal->member': {'two-slot coincidence': 501, 'single-slot strict': 77, 'drift-prepared': 41, 'other': 36, 'conditional': 1}, 'unequal->unequal': {'two-slot coincidence': 274, 'drift-prepared': 40, 'single-slot strict': 25, 'other': 24}, 'disagreement->unequal': {'two-slot coincidence': 2}, 'disagreement->member': {'two-slot coincidence': 1}, 'member->unequal': {'two-slot coincidence': 48, 'single-slot strict': 9, 'other': 5, 'drift-prepared': 2}}

**Fr-wasteful**: flips per run 42.0 [29.1, 54.9]; by type {'unequal->member': 359, 'unequal->unequal': 219, 'member->unequal': 192, 'wasteful->unequal': 37, 'member->member': 19, 'wasteful->member': 14}; triggers {'two-slot coincidence': 611, 'single-slot strict': 97, 'drift-prepared': 54, 'other': 39, 'conditional': 28, 'pure drift': 11}; member→member 19, via an outsider class 1, via other-mixed 11; steps out of a non-member following an M arrow 576/702; all steps following an arrow 802/976.
  triggers by type: {'wasteful->member': {'two-slot coincidence': 13, 'single-slot strict': 1}, 'unequal->member': {'two-slot coincidence': 273, 'single-slot strict': 39, 'drift-prepared': 21, 'other': 14, 'conditional': 12}, 'member->member': {'pure drift': 10, 'two-slot coincidence': 7, 'single-slot strict': 1, 'drift-prepared': 1}, 'wasteful->unequal': {'two-slot coincidence': 37}, 'unequal->unequal': {'two-slot coincidence': 181, 'drift-prepared': 19, 'other': 12, 'single-slot strict': 6, 'pure drift': 1}, 'member->unequal': {'two-slot coincidence': 100, 'single-slot strict': 50, 'conditional': 16, 'drift-prepared': 13, 'other': 13}}

**Fr-grand**: flips per run 22.9 [13.8, 31.9]; by type {'grand-equal->member': 206, 'member->unequal': 182, 'disagreement->member': 25, 'grand-equal->unequal': 17, 'member->member': 13, 'disagreement->grand-equal': 6, 'unequal->member': 5, 'disagreement->unequal': 2, 'grand-equal->disagreement': 1}; triggers {'two-slot coincidence': 384, 'single-slot strict': 39, 'other': 20, 'drift-prepared': 13, 'pure drift': 1}; member→member 13, via an outsider class 0, via other-mixed 10; steps out of a non-member following an M arrow 254/315; all steps following an arrow 452/555.
  triggers by type: {'grand-equal->member': {'two-slot coincidence': 202, 'other': 4}, 'disagreement->member': {'two-slot coincidence': 25}, 'member->member': {'two-slot coincidence': 8, 'other': 2, 'single-slot strict': 2, 'pure drift': 1}, 'unequal->member': {'two-slot coincidence': 3, 'other': 2}, 'member->unequal': {'two-slot coincidence': 121, 'single-slot strict': 36, 'drift-prepared': 13, 'other': 12}, 'disagreement->grand-equal': {'two-slot coincidence': 5, 'single-slot strict': 1}, 'grand-equal->unequal': {'two-slot coincidence': 17}, 'grand-equal->disagreement': {'two-slot coincidence': 1}, 'disagreement->unequal': {'two-slot coincidence': 2}}

**L1-N50**: flips per run 14.9 [-5.9, 35.7]; by type {'member->member': 221, 'unequal->member': 56, 'disagreement->member': 14, 'disagreement->unequal': 5, 'member->unequal': 2}; triggers {'pure drift': 217, 'two-slot coincidence': 49, 'single-slot strict': 23, 'drift-prepared': 6, 'other': 3}; member→member 221, via an outsider class 0, via other-mixed 4; steps out of a non-member following an M arrow 81/87; all steps following an arrow 86/764.
  triggers by type: {'unequal->member': {'two-slot coincidence': 26, 'single-slot strict': 23, 'drift-prepared': 6, 'other': 1}, 'disagreement->member': {'two-slot coincidence': 14}, 'disagreement->unequal': {'two-slot coincidence': 5}, 'member->member': {'pure drift': 217, 'other': 2, 'two-slot coincidence': 2}, 'member->unequal': {'two-slot coincidence': 2}}

**L1-N200**: flips per run 128.2 [83.8, 172.6]; by type {'member->member': 1404, 'member->unequal': 897, 'unequal->member': 229, 'unequal->unequal': 31, 'wasteful->member': 3}; triggers {'two-slot coincidence': 1054, 'pure drift': 780, 'single-slot strict': 319, 'other': 223, 'drift-prepared': 104, 'conditional': 84}; member→member 1404, via an outsider class 35, via other-mixed 816; steps out of a non-member following an M arrow 242/347; all steps following an arrow 1127/2825.
  triggers by type: {'member->member': {'pure drift': 780, 'two-slot coincidence': 363, 'other': 109, 'conditional': 80, 'single-slot strict': 62, 'drift-prepared': 10}, 'unequal->member': {'two-slot coincidence': 178, 'other': 29, 'drift-prepared': 14, 'single-slot strict': 7, 'conditional': 1}, 'wasteful->member': {'two-slot coincidence': 3}, 'member->unequal': {'two-slot coincidence': 487, 'single-slot strict': 248, 'other': 81, 'drift-prepared': 79, 'conditional': 2}, 'unequal->unequal': {'two-slot coincidence': 23, 'other': 4, 'single-slot strict': 2, 'drift-prepared': 1, 'conditional': 1}}

**X6-1**: flips per run 55.2 [28.7, 81.7]; by type {'member->member': 1480, 'member->unequal': 436, 'unequal->member': 143, 'unequal->unequal': 76, 'disagreement->member': 55, 'disagreement->unequal': 17, 'wasteful->member': 1}; triggers {'pure drift': 1346, 'two-slot coincidence': 561, 'single-slot strict': 149, 'other': 91, 'drift-prepared': 61}; member→member 1480, via an outsider class 11, via other-mixed 168; steps out of a non-member following an M arrow 305/409; all steps following an arrow 764/2881.
  triggers by type: {'disagreement->member': {'two-slot coincidence': 55}, 'member->member': {'pure drift': 1339, 'two-slot coincidence': 87, 'other': 48, 'single-slot strict': 5, 'drift-prepared': 1}, 'unequal->unequal': {'two-slot coincidence': 58, 'other': 8, 'pure drift': 7, 'drift-prepared': 2, 'single-slot strict': 1}, 'unequal->member': {'two-slot coincidence': 103, 'single-slot strict': 24, 'other': 11, 'drift-prepared': 5}, 'member->unequal': {'two-slot coincidence': 240, 'single-slot strict': 119, 'drift-prepared': 53, 'other': 24}, 'disagreement->unequal': {'two-slot coincidence': 17}, 'wasteful->member': {'two-slot coincidence': 1}}

**X8-1**: flips per run 43.8 [34.1, 53.4]; by type {'member->unequal': 596, 'unequal->unequal': 510, 'unequal->member': 286, 'member->member': 223, 'disagreement->member': 72, 'disagreement->unequal': 54, 'wasteful->unequal': 6, 'wasteful->member': 1, 'member->wasteful': 1, 'disagreement->wasteful': 1}; triggers {'two-slot coincidence': 1045, 'single-slot strict': 287, 'pure drift': 239, 'other': 93, 'drift-prepared': 86}; member→member 223, via an outsider class 5, via other-mixed 73; steps out of a non-member following an M arrow 894/1167; all steps following an arrow 1529/2105.
  triggers by type: {'disagreement->member': {'two-slot coincidence': 72}, 'member->unequal': {'two-slot coincidence': 348, 'single-slot strict': 191, 'other': 29, 'drift-prepared': 28}, 'unequal->unequal': {'two-slot coincidence': 295, 'pure drift': 76, 'single-slot strict': 57, 'drift-prepared': 50, 'other': 32}, 'disagreement->unequal': {'two-slot coincidence': 53, 'other': 1}, 'wasteful->unequal': {'two-slot coincidence': 4, 'single-slot strict': 2}, 'unequal->member': {'two-slot coincidence': 228, 'single-slot strict': 35, 'other': 15, 'drift-prepared': 8}, 'member->member': {'pure drift': 163, 'two-slot coincidence': 42, 'other': 16, 'single-slot strict': 2}, 'wasteful->member': {'two-slot coincidence': 1}, 'member->wasteful': {'two-slot coincidence': 1}, 'disagreement->wasteful': {'two-slot coincidence': 1}}

**L1-N150**: flips per run 95.8 [45.1, 146.6]; by type {'member->member': 1584, 'member->unequal': 297, 'unequal->member': 32, 'disagreement->member': 3, 'wasteful->member': 1}; triggers {'pure drift': 869, 'conditional': 417, 'two-slot coincidence': 407, 'other': 108, 'single-slot strict': 93, 'drift-prepared': 23}; member→member 1584, via an outsider class 15, via other-mixed 392; steps out of a non-member following an M arrow 34/61; all steps following an arrow 346/2169.
  triggers by type: {'member->member': {'pure drift': 869, 'conditional': 411, 'two-slot coincidence': 189, 'other': 89, 'single-slot strict': 25, 'drift-prepared': 1}, 'disagreement->member': {'two-slot coincidence': 3}, 'unequal->member': {'two-slot coincidence': 31, 'other': 1}, 'member->unequal': {'two-slot coincidence': 183, 'single-slot strict': 68, 'drift-prepared': 22, 'other': 18, 'conditional': 6}, 'wasteful->member': {'two-slot coincidence': 1}}

**L1-N300**: flips per run 146.6 [121.6, 171.5]; by type {'member->member': 1230, 'member->unequal': 1003, 'unequal->member': 563, 'unequal->unequal': 130, 'wasteful->member': 2, 'wasteful->unequal': 2, 'unequal->wasteful': 1}; triggers {'two-slot coincidence': 1278, 'single-slot strict': 550, 'other': 521, 'pure drift': 343, 'drift-prepared': 136, 'conditional': 103}; member→member 1230, via an outsider class 27, via other-mixed 1047; steps out of a non-member following an M arrow 669/763; all steps following an arrow 1637/3063.
  triggers by type: {'unequal->member': {'two-slot coincidence': 339, 'other': 100, 'single-slot strict': 67, 'drift-prepared': 47, 'conditional': 10}, 'member->member': {'two-slot coincidence': 403, 'pure drift': 333, 'other': 235, 'single-slot strict': 164, 'conditional': 85, 'drift-prepared': 10}, 'member->unequal': {'two-slot coincidence': 462, 'single-slot strict': 310, 'other': 159, 'drift-prepared': 66, 'conditional': 6}, 'unequal->unequal': {'two-slot coincidence': 70, 'other': 27, 'drift-prepared': 13, 'pure drift': 10, 'single-slot strict': 8, 'conditional': 2}, 'unequal->wasteful': {'two-slot coincidence': 1}, 'wasteful->member': {'single-slot strict': 1, 'two-slot coincidence': 1}, 'wasteful->unequal': {'two-slot coincidence': 2}}

**L1-N400**: flips per run 153.0 [128.9, 177.1]; by type {'member->member': 1714, 'member->unequal': 658, 'unequal->member': 591, 'unequal->unequal': 92, 'wasteful->member': 3, 'unequal->wasteful': 1, 'disagreement->unequal': 1}; triggers {'two-slot coincidence': 910, 'other': 714, 'single-slot strict': 691, 'pure drift': 499, 'drift-prepared': 132, 'conditional': 114}; member→member 1714, via an outsider class 12, via other-mixed 1281; steps out of a non-member following an M arrow 656/709; all steps following an arrow 1325/3116.
  triggers by type: {'unequal->member': {'two-slot coincidence': 274, 'other': 155, 'single-slot strict': 108, 'drift-prepared': 50, 'conditional': 4}, 'member->member': {'pure drift': 499, 'other': 391, 'two-slot coincidence': 377, 'single-slot strict': 332, 'conditional': 107, 'drift-prepared': 8}, 'member->unequal': {'single-slot strict': 234, 'two-slot coincidence': 212, 'other': 140, 'drift-prepared': 70, 'conditional': 2}, 'unequal->unequal': {'two-slot coincidence': 46, 'other': 26, 'single-slot strict': 16, 'drift-prepared': 4}, 'unequal->wasteful': {'other': 1}, 'wasteful->member': {'single-slot strict': 1, 'other': 1, 'conditional': 1}, 'disagreement->unequal': {'two-slot coincidence': 1}}

## Forced seeds

- Fe-fair: {"500": [0.5984375, 0.5680471157921189, 0.628827884207881], "1000": [0.5984375, 0.5680471157921189, 0.628827884207881], "2000": [0.5984375, 0.5680471157921189, 0.628827884207881], "10000": [0.5984375, 0.5680471157921189, 0.628827884207881]}
- Fe-unequal: {"500": [0.51328125, 0.48312116877350436, 0.5434413312264956], "1000": [0.51328125, 0.48312116877350436, 0.5434413312264956], "2000": [0.51328125, 0.48312116877350436, 0.5434413312264956], "10000": [0.51328125, 0.48312116877350436, 0.5434413312264956]}
- Fe-wasteful: {"500": [0.0671875, 0.05520228604202574, 0.07917271395797426], "1000": [0.0671875, 0.05520228604202574, 0.07917271395797426], "2000": [0.0671875, 0.05520228604202574, 0.07917271395797426], "10000": [0.0671875, 0.05520228604202574, 0.07917271395797426]}
- Fe-grand: {"500": [0.13125, 0.11678287529021676, 0.14571712470978326], "1000": [0.13125, 0.11678287529021676, 0.14571712470978326], "2000": [0.13125, 0.11678287529021676, 0.14571712470978326], "10000": [0.13125, 0.11678287529021676, 0.14571712470978326]}
- Fr-fair: {"residence_km_median": 776, "residence_censored": 0.4046875, "residence_mean_uncensored": 273.59580052493436, "entry_km_median": 172, "entry_censored": 0.00625, "exits_to": {"P12:3|3": 318, "P23:4|2": 40, "P13:4|2": 23}}
- Fr-unequal: {"residence_km_median": 121, "residence_censored": 0.0, "residence_mean_uncensored": 193.4015625, "entry_km_median": 261, "entry_censored": 0.3484375, "exits_to": {"P12:4|2": 402, "P23:3|3": 165, "P23:4|2": 73}}
- Fr-wasteful: {"residence_km_median": 26, "residence_censored": 0.0, "residence_mean_uncensored": 29.746875, "entry_km_median": null, "entry_censored": 1.0, "exits_to": {"P12:4|2": 131, "P12:2|4": 122, "P13:4|2": 92, "P12:3|3": 84, "P23:3|3": 78, "P13:3|3": 68, "P23:4|2": 60, "P12:2|2": 3}}
- Fr-grand: {"residence_km_median": 41, "residence_censored": 0.0, "residence_mean_uncensored": 56.26875, "entry_km_median": null, "entry_censored": 0.9671875, "exits_to": {"G(2,2,2)": 189, "P12:3|3": 174, "P23:3|3": 153, "P13:3|3": 60, "P12:4|2": 47, "P23:4|2": 16, "P12:2|4": 1}}

## Chain (ε→0, weak arm, N = 100; a separate object)

- published: {"mass_by_type": {"grand": 0.010053318270056077, "fair pair": 0.373218689886767, "unfair pair": 0.5904507728765568, "wasteful pair": 0.025843852400184372, "disagreement": 0.0004333665664357875}, "mass_by_coalition": {"G": 0.010053318270056077, "P12": 0.3298377717211697, "P13": 0.3298377717211693, "P23": 0.3298377717211692, "X": 0.0004333665664357875}, "E_max_share": 0.5963556585203563, "efficiency": 0.9950987574026866, "P_some_slot_zero": 0.9899466817299675, "circulation": {"C": 1.3552527156068805e-20, "total_pair_to_pair": 0.0004411332305783853}, "pair_to_pair_by_mover": {"excluded_bids_in": 1.7835642729020536e-06, "pivot_switches": 0.00043934931325033047, "dropped_slot_moves": 3.5305420609222004e-10}, "dwell_events": {"G": 207503.29132532567, "P12": 2213.9716268531115, "P13": 2213.971626853113, "P23": 2213.971626853113, "X": 74.20509232514108}, "lumped_relaxation_events": 206626.64880477, "states": 32259, "cut_flow": 1.2505149545806348e-05, "time_s": 741.9388120174408}
- rerun: {"mass_by_type": {"grand": 0.010045988191906769, "fair pair": 0.37324284806159, "unfair pair": 0.590450663312875, "wasteful pair": 0.025827669768028378, "disagreement": 0.0004328306656000095}, "mass_by_coalition": {"G": 0.010045988191906769, "P12": 0.3298403937141643, "P13": 0.3298403937141644, "P23": 0.3298403937141647, "X": 0.0004328306656000095}, "E_max_share": 0.5963577723434379, "efficiency": 0.9951026328625104, "P_some_slot_zero": 0.989954011808125, "circulation": {"C": 1.3552527156068805e-19, "total_pair_to_pair": 0.00044104021609038714}, "pair_to_pair_by_mover": {"excluded_bids_in": 1.783391156849051e-06, "pivot_switches": 0.00043925647191299155, "dropped_slot_moves": 3.5302037727808974e-10}, "dwell_events": {"G": 207493.04883330152, "P12": 2214.479836173689, "P13": 2214.479836173687, "P23": 2214.479836173689, "X": 74.18996573757043}, "lumped_relaxation_events": 206618.20939621486, "states": 31989, "cut_flow": 1.2964644832801775e-05, "time_s": 1246.439785003662}

## Addendum cells (run after the first counted pass, disclosed; no prediction scored on them): the N trend at mN = 1

Fraction of islands and consensus runs (fair / unequal), L seeds, mN = 1, 20 runs (N = 100: 40):

| N | fair 2,000 | unequal 2,000 | fair 10,000 | unequal 10,000 | consensus at 10,000 (fair / unequal) | median generation to consensus |
|---|---|---|---|---|---|---|
| 50 | 0.84 | 0.15 | 0.83 | 0.15 | 16 / 3 of 20 | 660 |
| 100 | 0.74 | 0.14 | 0.81 | 0.17 | 31 / 7 of 40 | 1,496 |
| 150 | 0.64 | 0.14 | 0.67 | 0.25 | 11 / 5 of 20 | 2,284 |
| 200 | 0.50 | 0.22 | 0.15 | 0.75 | 2 / 15 of 20 | 3,765 |
| 300 | 0.47 | 0.09 | 0.24 | 0.69 | 3 / 10 of 20 | 5,496 |
| 400 | 0.47 | 0.06 | 0.37 | 0.42 | 1 / 4 of 20 (15 unresolved) | 6,743 |

The fair-pair consensus under migration is a small-island effect: from N = 200 the metapopulation ends on an unequal pair
in most runs that reach consensus, the direction of the chain (unfair 0.59 of π at N = 100).

## Forced residence, second measure

Time until a target island first *holds* (≥ 25 generations) a class other than the target (KM median, censored at
10,000), and what it holds: fair: not reached (0.70 censored), all 192 exits to unequal pairs; unequal: 638, to a
member 416 and to another unequal pair 224; wasteful: 723 (time spent mixed), to unequal 407, member 231; grand: 1,584,
to a member 560, unequal 79. First measure (first departure of ≥ 25 generations from the target, in the table above):
fair 776 (0.40 censored), unequal 121, grand 41, wasteful 26.

## Verdicts

Main cell L (length prior), N = 100, I = 64, 40 runs; horizon 2,000 unless stated; mN = 0 runs all close by
generation ≈ 300, so their 2,000 and 10,000 columns coincide.

**The RS's claim** ("each element of the stable set shows up on an island").

| cell | weak form (every element of V\* on some island) | strong form (island support inside a stable set) |
|---|---|---|
| L, mN = 0 | **40/40** (constants K: 40/40; the independence baseline at q = 0.28 gives 0.995) | **0/40** (0.72 of islands on outcomes in no stable set: unequal 0.42, wasteful 0.23, disagreement 0.07) |
| L, mN = 1 | **0/40** at 2,000 and 10,000 (the archipelago settles on one pair) | 33/40 (0.82) at 2,000 and 10,000, by consensus on *one* fair pair |
| L, mN = 1, N = 200 | 2/20 at 2,000, 0/20 at 10,000 | 0.40 at 2,000, **0.25** at 10,000 (15/20 runs end on one unequal pair) |

*Scored:* the weak form holds without migration, where it is a consequence of role symmetry and pairwise coordination
(constants alone give it; nothing in it tests stability), and fails under migration; the strong form fails without
migration, and holds under migration at N ≤ 150 only because one member takes over every island, which is selection
of a single element, not the set; at N ≥ 200 it fails. **The claim fails in both forms in the regimes that test it.**
The selection question among stable sets is empty: **V\* is the unique myopic stable set** on the game's outcomes, on
G6, G8 and on both extended grids.

| # | prediction | outcome |
|---|---|---|
| RE 1 | coverage ≥ 0.9 at mN = 0; member occupancy ≥ 0.6 | coverage **held** (1.00); occupancy **failed, falsifier fired** (0.281 [0.263, 0.300] ≤ 0.4) |
| RE 2 | role symmetry across runs within 0.1; support inside V\* alone in ≥ 0.5 of runs; tilted seed on a discriminatory line ≥ 0.3 | symmetry held on the falsifier (pooled member shares 0.34 / 0.35 / 0.31; modal-member shares 0.31 / 0.45 / 0.25, one band miss of 0.12, falsifier 0.2 not fired); within-run clause **failed at mN = 0** (0/40), held at mN = 1 (0.82); tilted clause **failed, falsifier fired** (0 islands: no discriminatory element is realizable in this game, as registered) |
| RE 3 | non-members transient (median ≤ 200); ≤ 0.1 of islands on non-members | grand visits short (KM median 2 generations, 0.18 visits per run); wasteful islands **absorbed** at mN = 0 (0.60 censored) but transient at mN = 1 (median 2); ≤ 0.1 **failed** (0.72 at mN = 0; 0.14 / 0.18 at mN = 1); **falsifier fired at mN = 0** (unequal pairs 0.42 ≥ 0.25 at 10,000) and at mN = 1, N = 200 (0.75); not at mN = 1, N = 100 |
| RE 4 | member flips via an outsider; ≥ 0.8 of exit steps on M arrows; consensus ≤ 0.3 at 10,000, through bridges | **failed, both falsifier clauses fired**: 8 of 1,350 member → member flips pass through an outsider class (the rest through member-mixed states, 0.90 by pure drift); 175 / 385 = 0.45 of steps out of a non-member follow an M arrow; consensus in 38/40 runs at 10,000 (0.95); constants alone reach it (K1 0.90), so no bridge is needed |
| RE 5 | modal = weak within 0.1 | **held at mN = 0** (paired, Δ fair 0.002 ± 0.007); at mN = 1 the band missed narrowly on selection (strong form 0.70 vs 0.82, Δ fair −0.11 ± 0.16, paired, not significant); falsifier (≥ 0.25) not fired |
| RE 6 | islands on myopic, not farsighted-only, outcomes | **falsifier fired at mN = 0** (0.42 of islands on outcomes farsightedly stable under TU effectiveness but in no myopic stable set: the six unequal pairs and (2, 2, 2)); not fired at mN = 1, N = 100 (0.14 / 0.18); fired at N = 200 (0.75 at 10,000). The farsighted sets on R are every efficient singleton (TU), or V\* plus three held-player pairs (game effectiveness) |
| RE 7 (Gemini) | V\* < 0.4 and all pairs > 0.7 at mN = 0; a sweep by 10,000 at mN = 1 | **held** on every number: V\* 0.28, all pairs 0.93 (fair + unequal alone 0.698), unequal > fair; consensus 0.95 at 10,000. Its mechanism (greed against accommodators) is not what happens: the constants arm reproduces mN = 0 exactly, and the unequal share of efficient pair islands (0.60) is below the two-orientation count (2/3); at mN = 1 the sweep is to a *fair* pair at N ≤ 150 and to an unequal pair at N ≥ 200. **Scored against RE 1: Gemini's prediction wins.** |
| S1 | V\* the unique stable set on R | **held** |
| S2 | V\* stable on the grids; no discriminatory set on G6 | **held** (none on G8 either) |
| S3 | mN = 0: q ∈ [0.2, 0.45], unequal ∈ [0.3, 0.55], pairs > 0.7, coverage ≥ 0.95, strong ≤ 0.05 | **held** (0.28, 0.42, 0.93, 1.00, 0) |
| S4 | mN = 1 at 2,000: fair ∈ [0.2, 0.45], unequal ≥ 0.5 of pair islands | **failed, falsifier fired** (fair 0.74; unequal 0.15 of pair islands); at N ≥ 200 by 10,000 the unequal clause holds |
| S5 | member flips: ≥ 0.8 no outsider, ≥ 0.7 pure drift | **held** (0.994; 0.90) |
| S6 | member → unequal flips ≥ 0.7 drift-prepared | **failed, falsifier fired** (0.07; 0.61 concurrent, 0.24 single-slot strict: under migration the second slot's new class is usually already present at ≥ 10%) |
| S7 | K and M within 0.05 of L at mN = 0 | **held** (0.004, 0.002) |
| S8 | tilted slot 3 is the low member ≥ 0.5 of its pair islands | **held** (0.63 vs L's 0.33); 0 discriminatory islands |
| S9 | U more mixed or in disagreement than L by ≥ 0.1 | **held** (0.97 disagreement vs 0.07) |
| S10 | forced entry: member and unequal ≥ 0.5, wasteful ≤ 0.3, grand ≤ 0.4 | **held** (0.60, 0.51, 0.07, 0.13) |
| S11 | residence wasteful < unequal < member; grand longest | order **held** (26 < 121 < 776); grand clause **failed** (41); falsifier not fired |
| S12 | C = M on R; chicken {R1}, {R2} | **held** |
| S13 | ≥ 0.8 unresolved at 2,000; ≤ 0.3 consensus at 10,000 | first clause **held** (0.90 unresolved); second **failed** (0.95) |
| S14 | extended grids: grand ≤ 0.1, pairs ≥ 0.7 | **held** (grand 0.009 / 0.011; pairs 0.84 / 0.80; discriminatory-line elements 0.006 / 0.004 of islands) |
| S15 | a singleton fair pair is farsighted stable; RE 6 void on R | first clause **held**; "void" **failed** (unequal pairs and (2, 2, 2) are farsightedly stable too) |

**Chain (separate object).** The weak-arm chain at N = 100 rerun on the same grammar reproduces the published numbers
to four decimals (fair 0.373, unfair 0.590, wasteful 0.026, grand 0.010; E[max share] 0.596; P12 = P13 = P23 = 0.330;
circulation 10⁻¹⁹): π puts 0.627 on outcomes in no stable set. The lottery and the chain are not pooled.

