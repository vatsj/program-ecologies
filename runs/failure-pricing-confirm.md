# Confirming failure pricing as the default compute charge (run report, 2026-10-25)

Spec `specs/2026-10-25-failure-pricing-confirmation.md`; notes `notes/failure-pricing-confirm.md`; predictions `predictions/2026-10-25-failure-pricing-confirm.md`. LOTTERY objects at fixed geometry, fresh run indices only (RPS and inspection runs 100-139 at (100, 64) and (400, 16); PD reps 200-239, world K, S-nonself, (100, 64), up to 10,000 generations). Never pi; conclusions restricted to the tested geometries, grammars, caps and world K. Intervals: run-clustered bootstrap for means, Wilson for run counts.

## Headline

**Default (A at P_fail = 0.1) at (100, 64): CONFIRMED** (statuses RPS / inspection / PD: ['met', 'met', 'met']). 
At (400, 16), RPS and inspection: **confirmed** (['met', 'met']).


## Band table, fresh runs, (100, 64)

| cell | RPS e_prog (net) | RPS e_gross | RPS forfeits | by mixing | PRR modal share | RPS | insp gross eff | insp net eff | insp | PD (B) persistent | PD (C) cost-incl. | PD | classification |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Z (0) | 0.587 [0.497, 0.674] failed | 0.587 [0.497, 0.674] | 0.000 [0.000, 0.000] | failed | 0.15 [0.08, 0.22] | failed | 0.734 [0.600, 0.866] | 0.734 [0.600, 0.866] | met | 35/40 = 0.875 [0.739, 0.945] | 35/40 = 0.875 [0.739, 0.945] | met | refuted |
| A 0.03 | 0.002 [0.000, 0.003] met | 0.002 [0.000, 0.004] | 0.000 [0.000, 0.000] | met | 0.90 [0.83, 0.96] | met | 0.825 [0.700, 0.925] | 0.825 [0.700, 0.925] | met | 38/40 = 0.950 [0.835, 0.986] | 38/40 = 0.950 [0.835, 0.986] | met | confirmed |
| A 0.1 | 0.000 [0.000, 0.000] met | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | met | 0.85 [0.80, 0.90] | met | 0.834 [0.717, 0.934] | 0.825 [0.704, 0.929] | met | 37/40 = 0.925 [0.801, 0.974] | 37/40 = 0.925 [0.801, 0.974] | met | confirmed |
| A 0.3 | 0.043 [0.000, 0.095] met | 0.061 [0.000, 0.136] | 0.056 [0.000, 0.126] | undetermined | 0.69 [0.57, 0.79] | undetermined | 0.775 [0.625, 0.900] | 0.762 [0.623, 0.888] | met | 38/40 = 0.950 [0.835, 0.986] | 38/40 = 0.950 [0.835, 0.986] | met | unresolved |
| A 1 | 0.027 [0.007, 0.052] met | 0.595 [0.502, 0.691] | 0.502 [0.400, 0.609] | failed | 0.05 [0.00, 0.12] | failed | 0.827 [0.716, 0.930] | 0.789 [0.679, 0.896] | met | 36/40 = 0.900 [0.769, 0.960] | 36/40 = 0.900 [0.769, 0.960] | met | refuted |
| A 10 | 0.094 [0.057, 0.138] undetermined | 0.786 [0.701, 0.857] | 0.632 [0.533, 0.722] | failed | 0.05 [0.00, 0.12] | failed | 0.778 [0.655, 0.883] | 0.773 [0.651, 0.880] | met | 35/40 = 0.875 [0.739, 0.945] | 35/40 = 0.875 [0.739, 0.945] | met | refuted |
| A_s (0.2/0.5/0.3) | 0.000 [0.000, 0.000] met | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | met | 0.75 [0.64, 0.85] | met | 0.655 [0.505, 0.800] | 0.619 [0.475, 0.759] | undetermined | 38/40 = 0.950 [0.835, 0.986] | 38/40 = 0.950 [0.835, 0.986] | met | unresolved |


PD (B) persistent universal-open; (C) persistent with end-state charge per play <= 0.3 (0.1 of the range 3); threshold 0.70 by Wilson. Insp net: net-of-charge efficient islands >= 0.60.


## Verdicts

| # | verdict | detail |
|---|---|---|
| 1 | **held** | RPS met (net met, mixing met), inspection net met (0.825 [0.704, 0.929]), PD (C) met 37/40 = 0.925 [0.801, 0.974] |
| 1c (gpt-6.1-sol) | **failed** | inspection net at A 0.1: met 0.825 [0.704, 0.929]; gross met 0.834 [0.717, 0.934] |
| 2 | **held** | A 0.1 net met 0.814 [0.694, 0.919]; zero price 0.762 [0.631, 0.878]; clause1 True clause2 True; gross A 0.825 [0.700, 0.925] |
| 3 | **failed** | 3a RPS at 0.03: failed (met); 3b RPS mixing at 0.3: partial (undetermined, e_gross 0.061 [0.000, 0.136], forfeit 0.056 [0.000, 0.126]); 3c failed insp/PD levels: [] |
| 3c (gemini-4-argon) | **held** | by mixing at 0.3: undetermined, parts ('undetermined', 'undetermined') |
| 4 | **held** | mixing met at 0.1: met; PRR modal share 0.851 [0.802, 0.898]; failed at 1 (failed) and at 10 (failed) |
| 5 | **held** | 0.03: A 38 B 38 C 38; 0.1: A 37 B 37 C 37; 0.3: A 38 B 38 C 38; 1: A 36 B 36 C 36; 10: A 35 B 35 C 35; max B-C gap 0; priced runs with end-state charge >= 0.03: 0; F 1e-2 stored (C) 0/20 = 0.000 [0.000, 0.161] |
| 5c (gpt-6.1-sol) | **failed** | end-state charges tiny: True; levels whose paired persistent-UO difference excludes 0: []; {0.03: '0.075 [-0.050, 0.200]', 0.1: '0.050 [-0.050, 0.150]', 0.3: '0.075 [-0.050, 0.200]', 1.0: '0.025 [-0.100, 0.150]', 10.0: '0.000 [-0.150, 0.150]'} |
| E1 | **held** | gross 0.834 [0.717, 0.934] net 0.825 [0.704, 0.929] gap 0.008 |
| E2 | **held** | scramble charge/play A0.1 0.00077 [0.00052, 0.00112], A10 0.00034 [0.00017, 0.00060], ratio 0.4 |
| E3 | **held** | levels (A snapshot, B persistent): [(0.0, 36, 35), (0.03, 38, 38), (0.1, 37, 37), (0.3, 38, 38), (1.0, 36, 36), (10.0, 35, 35)] |
| E4 | **held** | {0.03: '0.075 [-0.050, 0.200]', 0.1: '0.050 [-0.050, 0.150]', 0.3: '0.075 [-0.050, 0.200]'} |
| E5 | **failed** | PRR modal share at 0.03: 0.902 [0.834, 0.960] |
| E6 | **failed** | A_s RPS 0.2 mixing met; insp 0.5 net 0.619 [0.475, 0.759] (fresh 0.3: 0.762 [0.623, 0.888], 1: 0.789 [0.679, 0.896]) |
| E7 | **held** | size A 0.1 RPS mixing met (e_gross 0.000 [0.000, 0.000], forfeit 0.000 [0.000, 0.000]); zero price mixing failed (e_gross 0.622 [0.543, 0.701]) |
| E8 | **held** | nested share of counted timeouts at generation 2,000: RPS 0.0000, inspection 0.0000 |
| E9 | **failed** | label confirmed; statuses (rps, insp, pd) ['met', 'met', 'met']; PD (C) 37/40 |
| E10 | **held** | 1: PD C 36/40 = 0.900 [0.769, 0.960], insp net met 0.789 [0.679, 0.896]; 10: PD C 35/40 = 0.875 [0.739, 0.945], insp net met 0.773 [0.651, 0.880] |


## PD detail

| cell | (A) snapshot UO | (B) persistent UO | (C) cost-inclusive | late | censored | frozen | generations | P(C,C) | end-state charge/play | max run | scramble charge/play (g<=200) | cumulative charge/play | runs >= 0.03 | distinct holders | holder changes after 500 | wall s/run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Z (0) | 36/40 = 0.900 [0.769, 0.960] | 35/40 = 0.875 [0.739, 0.945] | 35/40 = 0.875 [0.739, 0.945] | 1 | 17 | 0.57 [0.42, 0.72] | 7084 [6003, 8100] | 0.998 [0.996, 1.000] | 0.00000 [0.00000, 0.00000] | 0.0000 | 0.00000 [0.00000, 0.00000] | 0.000000 [0.000000, 0.000000] | 0 | 1.4 [1.2, 1.6] | 1790 [1449, 2137] | 36 [32, 41] |
| A 0.03 | 38/40 = 0.950 [0.835, 0.986] | 38/40 = 0.950 [0.835, 0.986] | 38/40 = 0.950 [0.835, 0.986] | 0 | 18 | 0.55 [0.40, 0.70] | 7490 [6502, 8390] | 0.950 [0.875, 1.000] | 0.00000 [0.00000, 0.00000] | 0.0000 | 0.00035 [0.00023, 0.00049] | 0.000025 [0.000013, 0.000040] | 0 | 1.4 [1.2, 1.5] | 2017 [1681, 2349] | 71 [62, 80] |
| A 0.1 | 37/40 = 0.925 [0.801, 0.974] | 37/40 = 0.925 [0.801, 0.974] | 37/40 = 0.925 [0.801, 0.974] | 0 | 17 | 0.57 [0.42, 0.72] | 7378 [6373, 8311] | 0.999 [0.998, 1.000] | 0.00012 [0.00000, 0.00034] | 0.0039 | 0.00077 [0.00052, 0.00112] | 0.000175 [0.000034, 0.000436] | 0 | 1.4 [1.3, 1.6] | 1974 [1627, 2322] | 71 [61, 80] |
| A 0.3 | 38/40 = 0.950 [0.835, 0.986] | 38/40 = 0.950 [0.835, 0.986] | 38/40 = 0.950 [0.835, 0.986] | 0 | 16 | 0.60 [0.45, 0.75] | 8050 [7168, 8824] | 0.999 [0.997, 1.000] | 0.00000 [0.00000, 0.00000] | 0.0000 | 0.00089 [0.00063, 0.00119] | 0.000167 [0.000037, 0.000356] | 0 | 1.4 [1.2, 1.6] | 2012 [1697, 2311] | 73 [65, 80] |
| A 1 | 36/40 = 0.900 [0.769, 0.960] | 36/40 = 0.900 [0.769, 0.960] | 36/40 = 0.900 [0.769, 0.960] | 0 | 19 | 0.53 [0.38, 0.68] | 7142 [6026, 8208] | 0.999 [0.998, 1.000] | 0.00002 [0.00000, 0.00007] | 0.0009 | 0.00089 [0.00051, 0.00135] | 0.000145 [0.000048, 0.000267] | 0 | 1.5 [1.3, 1.7] | 1829 [1418, 2232] | 67 [57, 77] |
| A 10 | 35/40 = 0.875 [0.739, 0.945] | 35/40 = 0.875 [0.739, 0.945] | 35/40 = 0.875 [0.739, 0.945] | 0 | 19 | 0.53 [0.38, 0.68] | 7318 [6202, 8338] | 0.950 [0.875, 1.000] | 0.00000 [0.00000, 0.00000] | 0.0000 | 0.00034 [0.00017, 0.00060] | 0.000041 [0.000007, 0.000094] | 0 | 1.4 [1.2, 1.6] | 1619 [1240, 2016] | 65 [55, 74] |


Charge in stakes (range 3):

| cell | end-state charge | in range units | scramble charge | in range units | cumulative |
|---|---|---|---|---|---|
| A 0.03 | 0 | 0 | 0.000346 | 0.000115 | 2.53e-05 |
| A 0.1 | 0.000119 | 3.98e-05 | 0.000772 | 0.000257 | 0.000175 |
| A 0.3 | 0 | 0 | 0.000895 | 0.000298 | 0.000167 |
| A 1 | 2.32e-05 | 7.73e-06 | 0.000889 | 0.000296 | 0.000145 |
| A 10 | 0 | 0 | 0.000336 | 0.000112 | 4.11e-05 |


## RPS detail
| cell | U share | simulators | individual mixing | timeouts/play | PRR modal share |
|---|---|---|---|---|---|
| Z (0) | 0.022 [0.005, 0.044] | 0.831 [0.765, 0.895] | 0.363 [0.268, 0.465] | 0.824 [0.757, 0.888] | 0.15 [0.08, 0.22] |
| A 0.03 | 0.097 [0.045, 0.156] | 0.003 [0.001, 0.005] | 0.998 [0.996, 1.000] | 0.003 [0.001, 0.005] | 0.90 [0.83, 0.96] |
| A 0.1 | 0.163 [0.114, 0.214] | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] | 0.85 [0.80, 0.90] |
| A 0.3 | 0.244 [0.158, 0.342] | 0.000 [0.000, 0.000] | 0.939 [0.864, 1.000] | 0.000 [0.000, 0.000] | 0.69 [0.57, 0.79] |
| A 1 | 0.293 [0.220, 0.368] | 0.000 [0.000, 0.000] | 0.372 [0.280, 0.464] | 0.000 [0.000, 0.000] | 0.05 [0.00, 0.12] |
| A 10 | 0.078 [0.040, 0.123] | 0.000 [0.000, 0.000] | 0.128 [0.059, 0.212] | 0.000 [0.000, 0.000] | 0.05 [0.00, 0.12] |


## Inspection detail
| cell | inspector charge | inspectee charge | inspector game payoff | inspectee game payoff | timeouts/play | P(inspect) | P(cheat) |
|---|---|---|---|---|---|---|---|
| Z (0) | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | -0.147 [-0.223, -0.074] | 0.016 [0.008, 0.023] | 0.0980 [0.0556, 0.1495] | 0.037 [0.020, 0.056] | 0.031 [0.016, 0.047] |
| A 0.03 | 0.0002 [0.0000, 0.0005] | 0.0000 [0.0000, 0.0000] | -0.098 [-0.169, -0.042] | 0.011 [0.005, 0.019] | 0.0030 [0.0001, 0.0076] | 0.022 [0.009, 0.037] | 0.022 [0.009, 0.037] |
| A 0.1 | 0.0012 [0.0001, 0.0028] | 0.0000 [0.0000, 0.0000] | -0.092 [-0.155, -0.035] | 0.009 [0.003, 0.017] | 0.0060 [0.0005, 0.0139] | 0.021 [0.008, 0.035] | 0.021 [0.008, 0.035] |
| A 0.3 | 0.0022 [0.0004, 0.0048] | 0.0000 [0.0000, 0.0000] | -0.127 [-0.211, -0.056] | 0.014 [0.006, 0.023] | 0.0036 [0.0006, 0.0081] | 0.028 [0.013, 0.047] | 0.028 [0.013, 0.047] |
| A 1 | 0.0165 [0.0025, 0.0360] | 0.0000 [0.0000, 0.0000] | -0.085 [-0.146, -0.031] | 0.008 [0.002, 0.014] | 0.0083 [0.0013, 0.0180] | 0.030 [0.012, 0.053] | 0.016 [0.003, 0.028] |
| A 10 | 0.0031 [0.0003, 0.0068] | 0.0000 [0.0000, 0.0000] | -0.088 [-0.145, -0.041] | 0.003 [0.000, 0.008] | 0.0002 [0.0000, 0.0003] | 0.066 [0.032, 0.110] | 0.006 [0.000, 0.016] |


## Larger geometry (400, 16)
| (400, 16), 40 runs | RPS e_prog (net) | e_gross | forfeits | by mixing | RPS | insp gross | insp net | insp |
|---|---|---|---|---|---|---|---|---|
| Z (0) | 0.622 [0.543, 0.701] failed | 0.622 [0.543, 0.701] | 0.000 [0.000, 0.000] | failed | failed | 0.762 [0.631, 0.878] | 0.762 [0.631, 0.878] | met |
| A 0.1 | 0.000 [0.000, 0.000] met | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | met | met | 0.825 [0.700, 0.925] | 0.814 [0.694, 0.919] | met |


## Paired price-minus-zero differences (matched fresh founder sets)
| game | cell | statistic | price minus zero, paired (95%) |
|---|---|---|---|
| RPS | A 0.03 | e_gross | -0.585 [-0.672, -0.496] |
| RPS | A 0.03 | forfeit | 0.000 [0.000, 0.000] |
| RPS | A 0.03 | prr | 0.755 [0.663, 0.844] |
| inspection | A 0.03 | efficient fraction (gross) | 0.091 [-0.056, 0.234] |
| inspection | A 0.03 | efficient fraction (net) | 0.091 [-0.056, 0.234] |
| PD | A 0.03 | proportion (B) | 0.075 [-0.050, 0.200] |
| PD | A 0.03 | proportion (C) | 0.075 [-0.050, 0.200] |
| RPS | A 0.1 | e_gross | -0.587 [-0.674, -0.497] |
| RPS | A 0.1 | forfeit | 0.000 [0.000, 0.000] |
| RPS | A 0.1 | prr | 0.704 [0.623, 0.780] |
| inspection | A 0.1 | efficient fraction (gross) | 0.099 [-0.079, 0.266] |
| inspection | A 0.1 | efficient fraction (net) | 0.091 [-0.086, 0.257] |
| PD | A 0.1 | proportion (B) | 0.050 [-0.050, 0.150] |
| PD | A 0.1 | proportion (C) | 0.050 [-0.050, 0.150] |
| RPS | A 0.3 | e_gross | -0.526 [-0.639, -0.403] |
| RPS | A 0.3 | forfeit | 0.056 [0.000, 0.126] |
| RPS | A 0.3 | prr | 0.539 [0.437, 0.639] |
| inspection | A 0.3 | efficient fraction (gross) | 0.041 [-0.141, 0.209] |
| inspection | A 0.3 | efficient fraction (net) | 0.028 [-0.152, 0.198] |
| PD | A 0.3 | proportion (B) | 0.075 [-0.050, 0.200] |
| PD | A 0.3 | proportion (C) | 0.075 [-0.050, 0.200] |
| RPS | A 1 | e_gross | 0.007 [-0.120, 0.137] |
| RPS | A 1 | forfeit | 0.502 [0.400, 0.609] |
| RPS | A 1 | prr | -0.093 [-0.187, 0.009] |
| inspection | A 1 | efficient fraction (gross) | 0.093 [-0.063, 0.247] |
| inspection | A 1 | efficient fraction (net) | 0.055 [-0.105, 0.216] |
| PD | A 1 | proportion (B) | 0.025 [-0.100, 0.150] |
| PD | A 1 | proportion (C) | 0.025 [-0.100, 0.150] |
| RPS | A 10 | e_gross | 0.199 [0.077, 0.318] |
| RPS | A 10 | forfeit | 0.632 [0.533, 0.722] |
| RPS | A 10 | prr | -0.100 [-0.197, 0.002] |
| inspection | A 10 | efficient fraction (gross) | 0.043 [-0.147, 0.236] |
| inspection | A 10 | efficient fraction (net) | 0.039 [-0.152, 0.233] |
| PD | A 10 | proportion (B) | 0.000 [-0.150, 0.150] |
| PD | A 10 | proportion (C) | 0.000 [-0.150, 0.150] |


## Timed-out calls: by depth and stage, then by programme
| game | cell | generation | timed-out calls/play | topmost | nested inside a timed-out call | issued from the opponent's code | nested share |
|---|---|---|---|---|---|---|---|
| rps | Z | 500 | 0.8283 | 0.8283 | 0.00000 | 0.0252 | 0.000 |
| rps | Z | 2000 | 0.8240 | 0.8240 | 0.00000 | 0.0137 | 0.000 |
| rps | A 0.03 | 500 | 0.5154 | 0.5154 | 0.00000 | 0.0112 | 0.000 |
| rps | A 0.03 | 2000 | 0.0028 | 0.0028 | 0.00000 | 0.0000 | 0.000 |
| rps | A 0.1 | 500 | 0.0102 | 0.0102 | 0.00000 | 0.0000 | 0.000 |
| rps | A 0.1 | 2000 | 0.0000 | 0.0000 | 0.00000 | 0.0000 | 0.000 |
| rps | A 0.3 | 500 | 0.0002 | 0.0002 | 0.00000 | 0.0000 | 0.000 |
| rps | A 0.3 | 2000 | 0.0000 | 0.0000 | 0.00000 | 0.0000 | 0.000 |
| rps | A 1 | 500 | 0.0007 | 0.0007 | 0.00000 | 0.0000 | 0.000 |
| rps | A 1 | 2000 | 0.0000 | 0.0000 | 0.00000 | 0.0000 | 0.000 |
| rps | A 10 | 500 | 0.0000 | 0.0000 | 0.00000 | 0.0000 | 0.000 |
| rps | A 10 | 2000 | 0.0000 | 0.0000 | 0.00000 | 0.0000 | 0.000 |
| insp | Z | 500 | 0.1415 | 0.1415 | 0.00000 | 0.0208 | 0.000 |
| insp | Z | 2000 | 0.0980 | 0.0980 | 0.00000 | 0.0137 | 0.000 |
| insp | A 0.03 | 500 | 0.0336 | 0.0336 | 0.00000 | 0.0035 | 0.000 |
| insp | A 0.03 | 2000 | 0.0030 | 0.0030 | 0.00000 | 0.0000 | 0.000 |
| insp | A 0.1 | 500 | 0.0109 | 0.0109 | 0.00000 | 0.0000 | 0.000 |
| insp | A 0.1 | 2000 | 0.0060 | 0.0060 | 0.00000 | 0.0000 | 0.000 |
| insp | A 0.3 | 500 | 0.0110 | 0.0110 | 0.00000 | 0.0000 | 0.000 |
| insp | A 0.3 | 2000 | 0.0036 | 0.0036 | 0.00000 | 0.0000 | 0.000 |
| insp | A 1 | 500 | 0.0087 | 0.0087 | 0.00000 | 0.0000 | 0.000 |
| insp | A 1 | 2000 | 0.0083 | 0.0083 | 0.00000 | 0.0000 | 0.000 |
| insp | A 10 | 500 | 0.0011 | 0.0011 | 0.00000 | 0.0000 | 0.000 |
| insp | A 10 | 2000 | 0.0002 | 0.0002 | 0.00000 | 0.0000 | 0.000 |

| game | cell | generation | role | top programmes by timed-out calls/play contributed (share-weighted) |
|---|---|---|---|---|
| rps | Z | 500 | role 0 | SIM100P 0.2431, SIM100S 0.2283, SIM100u 0.1443, SIM100R 0.1405 |
| rps | Z | 2000 | role 0 | SIM100P 0.2742, SIM100S 0.2330, SIM100u 0.1262, SIM100R 0.1254 |
| rps | A 0.1 | 500 | role 0 | SIM100S 0.0030, SIM100R 0.0026, SIM100u 0.0025, SIM100P 0.0017 |
| rps | A 0.1 | 2000 | role 0 |  |
| rps | A 1 | 500 | role 0 | SIM100R 0.0006, SIM20u 0.0001 |
| rps | A 1 | 2000 | role 0 |  |
| insp | Z | 500 | inspector | SI100n 0.1270, SI20i 0.0138, SI100i 0.0078, SI20n 0.0014 |
| insp | Z | 500 | inspectee | SE100c 0.0933, SE20c 0.0325, SE100k 0.0071 |
| insp | Z | 2000 | inspector | SI100n 0.0938, SI100i 0.0063, SI20i 0.0059, SI20n 0.0013 |
| insp | Z | 2000 | inspectee | SE100c 0.0641, SE20c 0.0228, SE100k 0.0020 |
| insp | A 0.1 | 500 | inspector | SI100n 0.0151, SI20n 0.0058, SI100i 0.0006, SI20i 0.0004 |
| insp | A 0.1 | 500 | inspectee | SE100k 0.0000 |
| insp | A 0.1 | 2000 | inspector | SI100n 0.0098, SI20n 0.0022 |
| insp | A 0.1 | 2000 | inspectee |  |
| insp | A 1 | 500 | inspector | SI100n 0.0098, SI20n 0.0062, SI100i 0.0009, SI20i 0.0005 |
| insp | A 1 | 500 | inspectee |  |
| insp | A 1 | 2000 | inspector | SI100n 0.0088, SI20n 0.0077 |
| insp | A 1 | 2000 | inspectee |  |


## Support and transitions
| game | cell | modal programme(s), share of islands | mean support size (>= 5%) | modal changed: 500-1000 / 1000-1500 / 1500-2000 / 2000-4000 | support changed: 1500-2000 / 2000-4000 |
|---|---|---|---|---|---|
| rps | Z | SIM100P 0.28 SIM100S 0.24 PRR 0.15 SIM100R 0.13 | 1.70 | 0.65/0.59/0.49/0.43 | 0.68 / 0.63 |
| rps | A 0.03 | PRR 0.90 U 0.09 CRR 0.01 SIM100u 0.00 | 1.18 | 0.57/0.28/0.12/0.07 | 0.27 / 0.18 |
| rps | A 0.1 | PRR 0.85 U 0.15 CRR 0.00 | 1.32 | 0.22/0.22/0.22/0.23 | 0.32 / 0.33 |
| rps | A 0.3 | PRR 0.69 U 0.24 PB 0.06 CRR 0.01 | 1.34 | 0.24/0.23/0.22/0.19 | 0.32 / 0.30 |
| rps | A 1 | PB 0.57 U 0.29 PRR 0.05 CRR 0.02 | 1.52 | 0.41/0.40/0.35/0.32 | 0.49 / 0.45 |
| rps | A 10 | PB 0.71 U 0.07 PRR 0.05 B_RP 0.04 | 1.45 | 0.34/0.29/0.28/0.29 | 0.45 / 0.43 |
| insp | Z | SI100n/C0 0.39 SI100n/Mc1 0.23 SI20i/C0 0.07 SI100n/SE100c 0.06 | 2.68 | 0.62/0.43/0.40/0.36 | 0.59 / 0.52 |
| insp | A 0.03 | SI100n/C0 0.47 SI100n/Mc1 0.11 SI100i/C0 0.07 SI100n/PCR3 0.07 | 2.86 | 0.64/0.50/0.47/0.45 | 0.67 / 0.62 |
| insp | A 0.1 | SI100n/C0 0.29 SI20n/C0 0.13 SI100i/C0 0.12 SI20i/C0 0.09 | 3.11 | 0.72/0.64/0.60/0.57 | 0.81 / 0.80 |
| insp | A 0.3 | SI100n/C0 0.28 SI20n/C0 0.16 SI100i/C0 0.10 SI100n/Mc1 0.08 | 3.06 | 0.78/0.65/0.58/0.54 | 0.81 / 0.76 |
| insp | A 1 | SI100n/C0 0.22 SI20n/C0 0.15 SI100i/C0 0.12 SI100n/Mc1 0.06 | 3.23 | 0.78/0.70/0.66/0.64 | 0.83 / 0.84 |
| insp | A 10 | SI100n/C0 0.15 SI20i/C0 0.13 SI20n/C0 0.13 RIM/C0 0.12 | 3.13 | 0.77/0.71/0.63/0.57 | 0.80 / 0.75 |


## Retrospective: the new scores on the stored rows of "What compute should cost" (exploratory runs, not fresh)

RPS by mixing (stored e_gross and forfeit run values):

| rule | level | e_prog (net) | net | e_gross | forfeits | individual mixing | by mixing | net met but not by mixing |
|---|---|---|---|---|---|---|---|---|
| A | 0.01 | 0.310 [0.236, 0.391] | failed | 0.316 [0.241, 0.397] | 0.000 [0.000, 0.000] | 0.661 [0.564, 0.746] | failed |  |
| A | 0.1 | 0.000 [0.000, 0.000] | met | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | met |  |
| A | 10.0 | 0.093 [0.060, 0.129] | undetermined | 0.800 [0.696, 0.885] | 0.631 [0.533, 0.725] | 0.149 [0.065, 0.252] | failed |  |
| A | 1.0 | 0.029 [0.010, 0.052] | met | 0.515 [0.417, 0.613] | 0.418 [0.321, 0.523] | 0.444 [0.347, 0.544] | failed | yes |
| B | 0.0001 | 0.235 [0.156, 0.321] | failed | 0.236 [0.157, 0.322] | 0.000 [0.000, 0.000] | 0.760 [0.669, 0.842] | failed |  |
| B | 0.001 | 0.349 [0.264, 0.439] | failed | 0.357 [0.271, 0.447] | 0.000 [0.000, 0.000] | 0.635 [0.541, 0.725] | failed |  |
| B | 0.01 | 0.328 [0.228, 0.440] | failed | 0.389 [0.281, 0.510] | 0.000 [0.000, 0.000] | 0.594 [0.467, 0.709] | failed |  |
| B | 1e-05 | 0.235 [0.154, 0.328] | failed | 0.235 [0.154, 0.328] | 0.000 [0.000, 0.000] | 0.765 [0.672, 0.846] | failed |  |
| Bl | 0.0001 | 0.235 [0.156, 0.321] | failed | 0.236 [0.157, 0.322] | 0.000 [0.000, 0.000] | 0.760 [0.669, 0.842] | failed |  |
| Bl | 0.001 | 0.349 [0.264, 0.439] | failed | 0.357 [0.271, 0.447] | 0.000 [0.000, 0.000] | 0.635 [0.541, 0.725] | failed |  |
| Bl | 0.01 | 0.328 [0.228, 0.440] | failed | 0.389 [0.281, 0.510] | 0.000 [0.000, 0.000] | 0.594 [0.467, 0.709] | failed |  |
| Bl | 1e-05 | 0.235 [0.154, 0.328] | failed | 0.235 [0.154, 0.328] | 0.000 [0.000, 0.000] | 0.765 [0.672, 0.846] | failed |  |
| Bo | 0.0001 | 0.231 [0.151, 0.318] | failed | 0.232 [0.151, 0.319] | 0.000 [0.000, 0.000] | 0.756 [0.661, 0.842] | failed |  |
| Bo | 0.001 | 0.331 [0.228, 0.441] | failed | 0.340 [0.236, 0.449] | 0.000 [0.000, 0.000] | 0.660 [0.550, 0.763] | failed |  |
| Bo | 0.01 | 0.262 [0.162, 0.369] | failed | 0.314 [0.207, 0.428] | 0.000 [0.000, 0.000] | 0.675 [0.557, 0.789] | failed |  |
| Bo | 1e-05 | 0.244 [0.170, 0.323] | failed | 0.244 [0.170, 0.323] | 0.000 [0.000, 0.000] | 0.751 [0.668, 0.828] | failed |  |
| Bw | 0.0001 | 0.613 [0.544, 0.682] | failed | 0.613 [0.545, 0.682] | 0.000 [0.000, 0.000] | 0.340 [0.264, 0.422] | failed |  |
| Bw | 0.001 | 0.743 [0.672, 0.811] | failed | 0.752 [0.681, 0.820] | 0.000 [0.000, 0.000] | 0.212 [0.141, 0.288] | failed |  |
| Bw | 0.01 | 0.663 [0.580, 0.740] | failed | 0.746 [0.660, 0.827] | 0.000 [0.000, 0.000] | 0.200 [0.115, 0.294] | failed |  |
| Bw | 1e-05 | 0.653 [0.570, 0.729] | failed | 0.653 [0.570, 0.729] | 0.000 [0.000, 0.000] | 0.295 [0.212, 0.387] | failed |  |
| Bws | 0.0001 | 0.348 [0.261, 0.439] | failed | 0.349 [0.262, 0.439] | 0.000 [0.000, 0.000] | 0.644 [0.553, 0.735] | failed |  |
| Bws | 0.001 | 0.310 [0.230, 0.398] | failed | 0.318 [0.238, 0.406] | 0.000 [0.000, 0.000] | 0.659 [0.557, 0.751] | failed |  |
| FA | 0.0001 | 0.005 [-0.001, 0.017] | met | 0.006 [0.000, 0.017] | 0.000 [0.000, 0.000] | 0.992 [0.975, 1.000] | met |  |
| FA | 0.001 | 0.027 [-0.002, 0.080] | met | 0.029 [0.000, 0.083] | 0.000 [0.000, 0.000] | 0.971 [0.917, 1.000] | met |  |
| FA | 0.01 | 0.696 [0.607, 0.780] | failed | 0.734 [0.650, 0.814] | 0.000 [0.000, 0.000] | 0.002 [0.000, 0.005] | failed |  |
| FA | 1e-05 | 0.013 [-0.000, 0.039] | met | 0.015 [0.000, 0.046] | 0.000 [0.000, 0.000] | 0.985 [0.954, 1.000] | met |  |
| F | 0.0001 | 0.546 [0.460, 0.630] | failed | 0.554 [0.467, 0.639] | 0.000 [0.000, 0.000] | 0.379 [0.279, 0.481] | failed |  |
| F | 0.001 | -0.002 [-0.003, -0.001] | met | 0.001 [0.000, 0.002] | 0.000 [0.000, 0.000] | 0.999 [0.998, 1.000] | met |  |
| F | 0.01 | 0.380 [0.310, 0.445] | failed | 0.405 [0.335, 0.469] | 0.000 [0.000, 0.000] | 0.222 [0.125, 0.331] | failed |  |
| F | 1e-05 | 0.611 [0.540, 0.677] | failed | 0.612 [0.541, 0.678] | 0.000 [0.000, 0.000] | 0.305 [0.222, 0.393] | failed |  |
| Fs | 0.0001 | 0.187 [0.125, 0.260] | failed | 0.191 [0.128, 0.266] | 0.000 [0.000, 0.000] | 0.799 [0.717, 0.870] | failed |  |
| Fs | 0.001 | -0.003 [-0.003, -0.002] | met | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | met |  |
| T | 0.1 | 0.000 [0.000, 0.000] | met | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 1.000 [1.000, 1.000] | met |  |
| T | 1.0 | 0.669 [0.592, 0.748] | failed | 0.753 [0.666, 0.836] | 0.000 [0.000, 0.000] | 0.044 [0.013, 0.085] | failed |  |
| Z | 0.0 | 0.638 [0.561, 0.715] | failed | 0.638 [0.561, 0.715] | 0.000 [0.000, 0.000] | 0.330 [0.249, 0.413] | failed |  |
| Zs | 0.0 | 0.211 [0.137, 0.291] | failed | 0.211 [0.137, 0.291] | 0.000 [0.000, 0.000] | 0.789 [0.709, 0.864] | failed |  |


PD persistent and cost-inclusive (registered rows; pooled with the supplementary rows where present):

| rule | level | (A) snapshot | (B) persistent | (C) cost-inclusive | status (C) | mean end-state charge | late | censored | pooled B / C |
|---|---|---|---|---|---|---|---|---|---|
| A | 0.01 | 19/20 = 0.950 [0.764, 0.991] | 19/20 = 0.950 [0.764, 0.991] | 19/20 = 0.950 [0.764, 0.991] | met | 0 | 0 | 7 |  |
| A | 0.1 | 17/20 = 0.850 [0.640, 0.948] | 17/20 = 0.850 [0.640, 0.948] | 17/20 = 0.850 [0.640, 0.948] | undetermined | 1.842e-05 | 0 | 9 | 35/40 C=35 (met) |
| A | 10.0 | 17/20 = 0.850 [0.640, 0.948] | 17/20 = 0.850 [0.640, 0.948] | 17/20 = 0.850 [0.640, 0.948] | undetermined | 0 | 0 | 10 | 32/40 C=32 (undetermined) |
| A | 1.0 | 15/20 = 0.750 [0.531, 0.888] | 15/20 = 0.750 [0.531, 0.888] | 15/20 = 0.750 [0.531, 0.888] | undetermined | 2.391e-05 | 0 | 13 | 33/40 C=33 (undetermined) |
| B | 0.0001 | 18/20 = 0.900 [0.699, 0.972] | 18/20 = 0.900 [0.699, 0.972] | 18/20 = 0.900 [0.699, 0.972] | undetermined | 0.0004 | 0 | 7 |  |
| B | 0.001 | 18/20 = 0.900 [0.699, 0.972] | 18/20 = 0.900 [0.699, 0.972] | 18/20 = 0.900 [0.699, 0.972] | undetermined | 0.004 | 0 | 7 |  |
| B | 0.01 | 18/20 = 0.900 [0.699, 0.972] | 18/20 = 0.900 [0.699, 0.972] | 18/20 = 0.900 [0.699, 0.972] | undetermined | 0.04 | 0 | 7 |  |
| B | 1e-05 | 18/20 = 0.900 [0.699, 0.972] | 18/20 = 0.900 [0.699, 0.972] | 18/20 = 0.900 [0.699, 0.972] | undetermined | 4e-05 | 0 | 7 |  |
| Bi | 0.0001 | 17/20 = 0.850 [0.640, 0.948] | 17/20 = 0.850 [0.640, 0.948] | 17/20 = 0.850 [0.640, 0.948] | undetermined | 0.0004 | 0 | 12 |  |
| Bi | 0.001 | 15/20 = 0.750 [0.531, 0.888] | 15/20 = 0.750 [0.531, 0.888] | 15/20 = 0.750 [0.531, 0.888] | undetermined | 0.004 | 0 | 10 |  |
| Bi | 0.01 | 14/20 = 0.700 [0.481, 0.855] | 14/20 = 0.700 [0.481, 0.855] | 14/20 = 0.700 [0.481, 0.855] | undetermined | 0.04 | 0 | 9 |  |
| Bi | 1e-05 | 20/20 = 1.000 [0.839, 1.000] | 20/20 = 1.000 [0.839, 1.000] | 20/20 = 1.000 [0.839, 1.000] | met | 4e-05 | 0 | 5 |  |
| Bo | 0.0001 | 20/20 = 1.000 [0.839, 1.000] | 20/20 = 1.000 [0.839, 1.000] | 20/20 = 1.000 [0.839, 1.000] | met | 0.0004 | 0 | 6 |  |
| Bo | 0.001 | 17/20 = 0.850 [0.640, 0.948] | 17/20 = 0.850 [0.640, 0.948] | 17/20 = 0.850 [0.640, 0.948] | undetermined | 0.004 | 0 | 7 |  |
| Bo | 0.01 | 12/20 = 0.600 [0.387, 0.781] | 12/20 = 0.600 [0.387, 0.781] | 12/20 = 0.600 [0.387, 0.781] | undetermined | 0.04 | 0 | 10 |  |
| Bo | 1e-05 | 20/20 = 1.000 [0.839, 1.000] | 20/20 = 1.000 [0.839, 1.000] | 20/20 = 1.000 [0.839, 1.000] | met | 4e-05 | 0 | 9 |  |
| Bow | 0.001 | 18/20 = 0.900 [0.699, 0.972] | 18/20 = 0.900 [0.699, 0.972] | 18/20 = 0.900 [0.699, 0.972] | undetermined | 0.004 | 0 | 4 |  |
| FA | 0.0001 | 0/20 = 0.000 [0.000, 0.161] | 0/20 = 0.000 [0.000, 0.161] | 0/20 = 0.000 [0.000, 0.161] | failed | 1.176 | 0 | 7 |  |
| FA | 0.001 | 12/20 = 0.600 [0.387, 0.781] | 12/20 = 0.600 [0.387, 0.781] | 0/20 = 0.000 [0.000, 0.161] | failed | 8.132 | 0 | 20 |  |
| FA | 0.01 | 20/20 = 1.000 [0.839, 1.000] | 20/20 = 1.000 [0.839, 1.000] | 0/20 = 0.000 [0.000, 0.161] | failed | 91.79 | 0 | 20 |  |
| FA | 1e-05 | 10/20 = 0.500 [0.299, 0.701] | 10/20 = 0.500 [0.299, 0.701] | 7/20 = 0.350 [0.181, 0.567] | failed | 0.2099 | 0 | 11 |  |
| F | 0.0001 | 0/20 = 0.000 [0.000, 0.161] | 0/20 = 0.000 [0.000, 0.161] | 0/20 = 0.000 [0.000, 0.161] | failed | 1.167 | 0 | 12 |  |
| F | 0.001 | 12/20 = 0.600 [0.387, 0.781] | 12/20 = 0.600 [0.387, 0.781] | 0/20 = 0.000 [0.000, 0.161] | failed | 8.696 | 0 | 20 | 24/40 C=0 (failed) |
| F | 0.01 | 20/20 = 1.000 [0.839, 1.000] | 20/20 = 1.000 [0.839, 1.000] | 0/20 = 0.000 [0.000, 0.161] | failed | 91.77 | 0 | 20 |  |
| F | 1e-05 | 9/20 = 0.450 [0.258, 0.658] | 9/20 = 0.450 [0.258, 0.658] | 7/20 = 0.350 [0.181, 0.567] | failed | 0.1884 | 0 | 10 |  |
| T | 0.1 | 19/20 = 0.950 [0.764, 0.991] | 19/20 = 0.950 [0.764, 0.991] | 19/20 = 0.950 [0.764, 0.991] | met | 0.115 | 0 | 4 |  |
| T | 1.0 | 0/20 = 0.000 [0.000, 0.161] | 0/20 = 0.000 [0.000, 0.161] | 0/20 = 0.000 [0.000, 0.161] | failed | 0.06724 | 0 | 20 |  |
| Z | 0.0 | 18/20 = 0.900 [0.699, 0.972] | 18/20 = 0.900 [0.699, 0.972] | 18/20 = 0.900 [0.699, 0.972] | undetermined | 0 | 0 | 7 | 37/40 C=37 (met) |


Inspection: gross efficient fraction and the stored role charges; the island-level net score is unavailable for stored rows:

| rule | level | efficient (gross) | status | inspector charge | inspectee charge | net |
|---|---|---|---|---|---|---|
| A | 0.01 | 0.765 [0.640, 0.890] | met | 0.0003 [0.0001, 0.0006] | 0.0000 [0.0000, 0.0000] | unavailable (island counts not stored) |
| A | 0.1 | 0.925 [0.850, 1.000] | met | 0.0031 [0.0008, 0.0062] | 0.0000 [0.0000, 0.0000] | unavailable (island counts not stored) |
| A | 10.0 | 0.743 [0.624, 0.862] | met | 0.0030 [0.0001, 0.0076] | 0.0000 [0.0000, 0.0000] | unavailable (island counts not stored) |
| A | 1.0 | 0.851 [0.741, 0.949] | met | 0.0039 [0.0000, 0.0089] | 0.0000 [0.0000, 0.0000] | unavailable (island counts not stored) |
| B | 0.0001 | 0.622 [0.476, 0.766] | undetermined | 0.0004 [0.0004, 0.0004] | 0.0004 [0.0004, 0.0005] | unavailable (island counts not stored) |
| B | 0.001 | 0.725 [0.575, 0.850] | undetermined | 0.0040 [0.0040, 0.0040] | 0.0037 [0.0030, 0.0044] | unavailable (island counts not stored) |
| B | 0.01 | 0.899 [0.802, 0.975] | met | 0.0400 [0.0400, 0.0400] | 0.0247 [0.0212, 0.0292] | unavailable (island counts not stored) |
| B | 1e-05 | 0.874 [0.771, 0.969] | met | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | unavailable (island counts not stored) |
| Bl | 0.0001 | 0.622 [0.476, 0.766] | undetermined | 0.0004 [0.0004, 0.0004] | 0.0004 [0.0004, 0.0005] | unavailable (island counts not stored) |
| Bl | 0.001 | 0.725 [0.575, 0.850] | undetermined | 0.0040 [0.0040, 0.0040] | 0.0037 [0.0030, 0.0044] | unavailable (island counts not stored) |
| Bl | 0.01 | 0.899 [0.802, 0.975] | met | 0.0400 [0.0400, 0.0400] | 0.0247 [0.0212, 0.0292] | unavailable (island counts not stored) |
| Bl | 1e-05 | 0.874 [0.771, 0.969] | met | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | unavailable (island counts not stored) |
| Bo | 0.0001 | 0.702 [0.552, 0.827] | undetermined | 0.0004 [0.0004, 0.0004] | 0.0004 [0.0003, 0.0004] | unavailable (island counts not stored) |
| Bo | 0.001 | 0.731 [0.588, 0.856] | undetermined | 0.0040 [0.0040, 0.0040] | 0.0038 [0.0033, 0.0045] | unavailable (island counts not stored) |
| Bo | 0.01 | 1.000 [1.000, 1.000] | met | 0.0400 [0.0400, 0.0400] | 0.0201 [0.0200, 0.0202] | unavailable (island counts not stored) |
| Bo | 1e-05 | 0.600 [0.450, 0.750] | undetermined | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0001] | unavailable (island counts not stored) |
| Bw | 0.0001 | 0.825 [0.700, 0.925] | met | 0.0004 [0.0004, 0.0004] | 0.0003 [0.0003, 0.0004] | unavailable (island counts not stored) |
| Bw | 0.001 | 0.815 [0.690, 0.925] | met | 0.0040 [0.0040, 0.0040] | 0.0033 [0.0028, 0.0039] | unavailable (island counts not stored) |
| Bw | 0.01 | 0.975 [0.925, 1.000] | met | 0.0400 [0.0400, 0.0400] | 0.0214 [0.0201, 0.0239] | unavailable (island counts not stored) |
| Bw | 1e-05 | 0.900 [0.800, 0.975] | met | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | unavailable (island counts not stored) |
| Bws | 0.0001 | 0.537 [0.381, 0.692] | undetermined | 0.0004 [0.0004, 0.0004] | 0.0005 [0.0004, 0.0005] | unavailable (island counts not stored) |
| Bws | 0.001 | 0.877 [0.767, 0.965] | met | 0.0040 [0.0040, 0.0040] | 0.0029 [0.0025, 0.0034] | unavailable (island counts not stored) |
| FA | 0.0001 | 0.800 [0.675, 0.925] | met | 0.0012 [0.0011, 0.0013] | 0.0006 [0.0005, 0.0007] | unavailable (island counts not stored) |
| FA | 0.001 | 0.825 [0.700, 0.925] | met | 0.0090 [0.0084, 0.0096] | 0.0030 [0.0024, 0.0036] | unavailable (island counts not stored) |
| FA | 0.01 | 0.775 [0.650, 0.900] | met | 0.0380 [0.0290, 0.0470] | 0.0305 [0.0247, 0.0367] | unavailable (island counts not stored) |
| FA | 1e-05 | 0.750 [0.600, 0.875] | met | 0.0001 [0.0001, 0.0001] | 0.0001 [0.0001, 0.0001] | unavailable (island counts not stored) |
| F | 0.0001 | 0.711 [0.567, 0.842] | undetermined | 0.0012 [0.0011, 0.0013] | 0.0006 [0.0005, 0.0007] | unavailable (island counts not stored) |
| F | 0.001 | 0.789 [0.650, 0.914] | met | 0.0092 [0.0086, 0.0099] | 0.0032 [0.0026, 0.0039] | unavailable (island counts not stored) |
| F | 0.01 | 0.775 [0.650, 0.900] | met | 0.0260 [0.0215, 0.0320] | 0.0311 [0.0251, 0.0378] | unavailable (island counts not stored) |
| F | 1e-05 | 0.826 [0.701, 0.929] | met | 0.0002 [0.0001, 0.0002] | 0.0001 [0.0001, 0.0002] | unavailable (island counts not stored) |
| Fs | 0.0001 | 0.575 [0.424, 0.725] | undetermined | 0.0012 [0.0011, 0.0013] | 0.0006 [0.0005, 0.0007] | unavailable (island counts not stored) |
| Fs | 0.001 | 0.631 [0.482, 0.776] | undetermined | 0.0097 [0.0091, 0.0105] | 0.0037 [0.0031, 0.0045] | unavailable (island counts not stored) |
| T | 0.1 | 0.600 [0.450, 0.750] | undetermined | 0.0078 [0.0011, 0.0161] | 0.0004 [0.0000, 0.0011] | unavailable (island counts not stored) |
| T | 1.0 | 0.014 [0.007, 0.023] | failed | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | unavailable (island counts not stored) |
| Z | 0.0 | 0.875 [0.750, 0.975] | met | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | unavailable (island counts not stored) |
| Zs | 0.0 | 0.651 [0.502, 0.800] | undetermined | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | unavailable (island counts not stored) |


## Deviations, retries, cuts and censoring (disclosed)

* **Nothing was cut; nothing crashed; no retries.** All registered cells ran: PD at the zero price and A at 0.03, 0.1, 0.3, 1, 10 (40 fresh reps each, 200-239); RPS and inspection at (100, 64) at the zero price and A at 0.03, 0.1, 0.3, 1, 10 and the stakes-normalized points (RPS 0.2, inspection 0.5), 40 fresh runs (100-139); RPS and inspection at (400, 16): zero price and A 0.1, 40 runs (100-139). The batch log (`runs/failure_pricing_confirm_batch.log`) shows no retry. Two workers throughout (a many-islands process was alive).
* **Caches** were copied from the pricing-rules engineer's worktree (`agent-a2a0df6470309b1aa`), not from the main checkout, which has none; untracked, never committed. The sha256 digests of every cache file and of the `static` directories are identical before and after the run. The code digests differ only by the report module, added after the pre-run digest.
* **The PD stakes-normalized point is the A 0.3 cell** (range 3, 0.1 x 3 = 0.3): no separate run (notes 1.4).
* **Censoring.** A PD run that has not frozen by generation 10,000 is censored (16-19 of 40 per cell); all are kept and scored by the persistence rule (an unfrozen run counts if universal-open at the end and the last indicator change is at least 500 generations earlier). The persistent count equals the snapshot count in every priced cell; at the zero price one run is late (36 snapshot, 35 persistent).
* **Scramble charge** uses the right-endpoint rule (notes 1.2b); the PD has only primitive reads (check or production caps, at most 2 per play, no nesting), so its timeouts are reported by stage only and not by programme or depth. Nested timed-out calls (inside another timed-out call) are exactly 0 in every RPS and inspection cell; a timed-out call issued from the opponent's code inside a simulation occurs (zero price 0.014-0.025 per play, at most 0.011 under A 0.03 and 0 from A 0.1).
* **Inspection net by island is unavailable for the stored rows**; the retrospective table gives gross fractions and the stored role charges.
* **The verdict logic was fixed in the predictions file before any counted cell**; the classification (confirmed iff all three games are met) uses the worst of each game's components. The exploratory sample is not pooled with the fresh runs anywhere in the headline.


## Provenance

Cache digests pre and post run identical: True (`runs/failure_pricing_confirm/provenance_hashes.json`).
