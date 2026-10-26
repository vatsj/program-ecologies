# Forfeit pricing, exact simulators and the security fallback (run report, 2026-10-26)

Spec `specs/2026-10-26-forfeit-pricing.md`; notes `notes/forfeit-pricing.md`; predictions `predictions/2026-10-26-forfeit-pricing.md`. LOTTERY objects at fixed geometry (N, I) = (100, 64), generation 2,000 (4,000 secondary), fresh run indices only (L_T runs 300-339, PD reps 300-339), world K. Never pi; finite-size mechanism test, no large-population or limit claim. Intervals: run-clustered percentile bootstrap (means), Wilson (PD counts); equivalence: 90% bootstrap interval inside +-0.05 (two one-sided tests).

## Cells present

- rps: A@0.03, Af+X@0.03, Af@0.03, Am+X@0.03, Am@0.03, A+X@0.1, A@0.1, Af+S@0.1, Af+X@0.1, Af@0.1, Am+X@0.1, Am@0.1, A@0.3, Af+X@0.3, Af@0.3, Am+X@0.3, Am@0.3, A+X@1, A@1, Af+S@1, Af+X@1, Af@1, Am+X@1, Am@1, A@10, Af+X@10, Af@10, Am+X@10, Am@10
- insp: A@0.03, Af+X@0.03, Af@0.03, A+X@0.1, A@0.1, Af+S@0.1, Af+X@0.1, Af@0.1, Am+X@0.1, Am@0.1, A@0.3, Af+X@0.3, Af@0.3, A+X@1, A@1, Af+S@1, Af+X@1, Af@1, Am+X@1, Am@1, A@10, Af+X@10, Af@10
- pd: Af@0.1, Af@1

## Band table (RPS, inspection, PD; (100, 64))

| cell | RPS e_prog (net) | e_gross (policy) | e_comp (completed) | forfeit / fallback share | by mixing | PRR modal | U modal | PB modal | SIMX modal | insp net eff | insp | PD (this run or carried) | classification |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A@0.03 | 0.041 [0.003, 0.101] | 0.042 [0.003, 0.104] | 0.042 [0.003, 0.104] | 0.000 [0.000, 0.000] | undetermined | 0.81 | 0.15 | 0.00 | 0.000 | 0.750 [0.625, 0.875] | met | met | unresolved |
| Af@0.03 | 0.030 [0.002, 0.082] | 0.031 [0.002, 0.085] | 0.031 [0.002, 0.085] | 0.000 [0.000, 0.000] | met | 0.83 | 0.14 | 0.00 | 0.000 | 0.694 [0.550, 0.825] | undetermined | met | unresolved |
| Af+X@0.03 | 0.002 [0.000, 0.006] | 0.002 [0.000, 0.006] | 0.002 [0.000, 0.006] | 0.057 [0.023, 0.104] | undetermined | 0.69 | 0.22 | 0.00 | 0.071 | 0.770 [0.639, 0.895] | met | - | - |
| Am@0.03 | 0.090 [0.042, 0.149] | 0.095 [0.044, 0.156] | 0.132 [0.066, 0.210] | 0.207 [0.118, 0.304] | failed | 0.31 | 0.35 | 0.23 | 0.000 | - | - | - | - |
| Am+X@0.03 | 0.027 [0.000, 0.078] | 0.028 [0.000, 0.081] | 0.039 [0.000, 0.098] | 0.230 [0.136, 0.335] | failed | 0.46 | 0.23 | 0.14 | 0.129 | - | - | - | - |
| A@0.1 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | met | 0.81 | 0.18 | 0.00 | 0.000 | 0.775 [0.648, 0.891] | met | met | confirmed |
| Af@0.1 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | met | 0.87 | 0.12 | 0.00 | 0.000 | 0.714 [0.582, 0.837] | undetermined | met | unresolved |
| Af+X@0.1 | 0.000 [0.000, 0.001] | 0.000 [0.000, 0.001] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | met | 0.78 | 0.22 | 0.00 | 0.000 | 0.745 [0.608, 0.870] | met | - | - |
| Am@0.1 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.100 [0.025, 0.200] | undetermined | 0.24 | 0.64 | 0.10 | 0.000 | 0.702 [0.562, 0.829] | undetermined | - | unresolved |
| Am+X@0.1 | 0.002 [0.000, 0.006] | 0.003 [0.000, 0.009] | 0.013 [0.000, 0.039] | 0.121 [0.025, 0.222] | undetermined | 0.28 | 0.56 | 0.12 | 0.006 | 0.825 [0.700, 0.925] | met | - | - |
| Af+S@0.1 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | met | 0.83 | 0.16 | 0.00 | 0.000 | 0.941 [0.866, 1.000] | met | - | - |
| A+X@0.1 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.471 [0.358, 0.587] | failed | 0.37 | 0.09 | 0.00 | 0.530 | 0.912 [0.821, 0.987] | met | - | - |
| A@0.3 | 0.027 [0.000, 0.068] | 0.038 [0.000, 0.097] | 0.000 [0.000, 0.000] | 0.034 [0.000, 0.086] | undetermined | 0.71 | 0.24 | 0.04 | 0.000 | 0.816 [0.693, 0.921] | met | met | unresolved |
| Af@0.3 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | met | 0.78 | 0.21 | 0.00 | 0.000 | 0.677 [0.539, 0.811] | undetermined | met | unresolved |
| Af+X@0.3 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | met | 0.71 | 0.29 | 0.00 | 0.000 | 0.875 [0.775, 0.975] | met | - | - |
| Am@0.3 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | met | 0.11 | 0.83 | 0.00 | 0.000 | - | - | - | - |
| Am+X@0.3 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.025 [0.000, 0.075] | undetermined | 0.21 | 0.70 | 0.03 | 0.000 | - | - | - | - |
| A@1 | 0.016 [0.004, 0.030] | 0.582 [0.491, 0.672] | 0.025 [0.006, 0.049] | 0.490 [0.398, 0.585] | failed | 0.08 | 0.28 | 0.58 | 0.000 | 0.786 [0.662, 0.893] | met | met | refuted |
| Af@1 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | met | 0.81 | 0.18 | 0.00 | 0.000 | 0.639 [0.501, 0.774] | undetermined | met | unresolved |
| Af+X@1 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | met | 0.73 | 0.25 | 0.00 | 0.000 | 0.900 [0.800, 0.975] | met | - | - |
| Am@1 | 0.014 [0.000, 0.035] | 0.014 [0.000, 0.035] | 0.014 [0.000, 0.035] | 0.000 [0.000, 0.000] | met | 0.55 | 0.42 | 0.00 | 0.000 | 0.795 [0.672, 0.904] | met | - | confirmed |
| Am+X@1 | 0.012 [0.000, 0.036] | 0.012 [0.000, 0.036] | 0.012 [0.000, 0.036] | 0.000 [0.000, 0.000] | met | 0.60 | 0.37 | 0.00 | 0.000 | 0.797 [0.672, 0.920] | met | - | - |
| Af+S@1 | 0.002 [0.000, 0.006] | 0.002 [0.000, 0.006] | 0.002 [0.000, 0.006] | 0.000 [0.000, 0.000] | met | 0.72 | 0.26 | 0.00 | 0.000 | 0.805 [0.697, 0.904] | met | - | - |
| A+X@1 | 0.000 [0.000, 0.000] | 0.410 [0.318, 0.505] | 0.000 [0.000, 0.000] | 0.703 [0.607, 0.788] | failed | 0.09 | 0.15 | 0.42 | 0.342 | 0.775 [0.648, 0.891] | met | - | - |
| A@10 | 0.104 [0.066, 0.145] | 0.807 [0.724, 0.880] | 0.241 [0.151, 0.339] | 0.623 [0.526, 0.715] | failed | 0.04 | 0.07 | 0.70 | 0.000 | 0.801 [0.696, 0.898] | met | met | refuted |
| Af@10 | 0.015 [0.000, 0.038] | 0.017 [0.000, 0.042] | 0.016 [0.000, 0.041] | 0.001 [0.000, 0.002] | met | 0.90 | 0.07 | 0.00 | 0.000 | 0.704 [0.590, 0.809] | undetermined | met | unresolved |
| Af+X@10 | 0.024 [0.000, 0.064] | 0.024 [0.000, 0.064] | 0.024 [0.000, 0.064] | 0.000 [0.000, 0.000] | met | 0.83 | 0.13 | 0.00 | 0.000 | 0.925 [0.825, 1.000] | met | - | - |
| Am@10 | 0.017 [0.000, 0.050] | 0.017 [0.000, 0.050] | 0.017 [0.000, 0.050] | 0.000 [0.000, 0.000] | met | 0.93 | 0.04 | 0.00 | 0.000 | - | - | - | - |
| Am+X@10 | 0.025 [0.000, 0.075] | 0.025 [0.000, 0.075] | 0.025 [0.000, 0.075] | 0.000 [0.000, 0.000] | met | 0.91 | 0.06 | 0.00 | 0.000 | - | - | - | - |

PD statuses at 0.03, 0.3 and 10 are carried from the confirmation run (the PD has no forfeits, `ffe` recorder); inspection is run under every rule.

## Classification of A_f at each level

| level | RPS net | RPS by mixing | inspection (the A_f cell) | PD | A_f classification (registered: the cell) | inspection pooled over rules with identical tables | classification with the pooled inspection |
|---|---|---|---|---|---|---|---|
| 0.03 | met | met | undetermined 0.694 [0.550, 0.825] | met (carried from the confirmation run) | unresolved | met 0.722 [0.613, 0.819] (2 rules) | confirmed |
| 0.1 | met | met | undetermined 0.714 [0.582, 0.837] | met (this run) | unresolved | met 0.730 [0.658, 0.799] (3 rules) | confirmed |
| 0.3 | met | met | undetermined 0.677 [0.539, 0.811] | met (carried from the confirmation run) | unresolved | met 0.747 [0.670, 0.824] (2 rules) | confirmed |
| 1 | met | met | undetermined 0.639 [0.501, 0.774] | met (this run) | unresolved | met 0.740 [0.661, 0.816] (3 rules) | confirmed |
| 10 | met | met | undetermined 0.704 [0.590, 0.809] | met (carried from the confirmation run) | unresolved | met 0.752 [0.669, 0.829] (2 rules) | confirmed |

Concurrent A (forfeits free, fresh runs 300-339):

| level | RPS net | RPS by mixing | inspection | PD | A classification |
|---|---|---|---|---|---|
| 0.03 | undetermined | undetermined | met | met (carried from the confirmation run) | unresolved |
| 0.1 | met | met | met | met (this run) | confirmed |
| 0.3 | met | undetermined | met | met (carried from the confirmation run) | unresolved |
| 1 | met | failed | met | met (this run) | refuted |
| 10 | undetermined | failed | met | met (carried from the confirmation run) | refuted |

A_m (RPS only for the full set; inspection is reported in the band table):

| cell | RPS net | by mixing | fallback share | e_comp |
|---|---|---|---|---|
| Am@0.03 | undetermined | failed | 0.207 [0.118, 0.304] | 0.132 [0.066, 0.210] |
| Am+X@0.03 | met | failed | 0.230 [0.136, 0.335] | 0.039 [0.000, 0.098] |
| Am@0.1 | met | undetermined | 0.100 [0.025, 0.200] | 0.000 [0.000, 0.000] |
| Am+X@0.1 | met | undetermined | 0.121 [0.025, 0.222] | 0.013 [0.000, 0.039] |
| Am@0.3 | met | met | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| Am+X@0.3 | met | undetermined | 0.025 [0.000, 0.075] | 0.000 [0.000, 0.000] |
| Am@1 | met | met | 0.000 [0.000, 0.000] | 0.014 [0.000, 0.035] |
| Am+X@1 | met | met | 0.000 [0.000, 0.000] | 0.012 [0.000, 0.036] |
| Am@10 | met | met | 0.000 [0.000, 0.000] | 0.017 [0.000, 0.050] |
| Am+X@10 | met | met | 0.000 [0.000, 0.000] | 0.025 [0.000, 0.075] |

## Verdicts (predictions/2026-10-26-forfeit-pricing.md)

| # | verdict | detail |
|---|---|---|
| 1 | **held** | by mixing at A_f 0.3: met (e_gross 0.000 [0.000, 0.000], forfeit 0.000 [0.000, 0.000]); at 1: met (e_gross 0.000 [0.000, 0.000], forfeit 0.000 [0.000, 0.000]) |
| 2 | **partial** | 0.03 RPS e_gross: unresolved mean -0.0109 90% [-0.0721, 0.0497]; 0.03 RPS forfeit: equivalent mean 0.0000 90% [0.0000, 0.0000]; 0.03 RPS e_prog: unresolved mean -0.0105 90% [-0.0699, 0.0483]; 0.03 insp net: unresolved mean -0.0563 90% [-0.2125, 0.1000]; 0.1 RPS e_gross: equivalent mean 0.0000 90% [0.0000, 0.0000]; 0.1 RPS forfeit: equivalent mean 0.0000 90% [0.0000, 0.0000]; 0.1 RPS e_prog: equivalent mean 0.0000 90% [0.0000, 0.0000]; 0.1 insp net: unresolved mean -0.0609 90% [-0.2152, 0.0914]; statuses ok: False |
| 3 | **held** | A_f 10: by mixing met, forfeit 0.001 [0.000, 0.002], e_gross 0.017 [0.000, 0.042] |
| 4 | **failed** | SIMX modal share under A_f + X: 0.03: 0.071 [0.031, 0.126]; 0.1: 0.000 [0.000, 0.000]; 0.3: 0.000 [0.000, 0.000]; 1: 0.000 [0.000, 0.000]; 10: 0.000 [0.000, 0.000] |
| 5 | **partial** | 0.03: net with X 0.770, without 0.694, diff +0.076; 0.1: net with X 0.745, without 0.714, diff +0.030; 0.3: net with X 0.875, without 0.677, diff +0.198; 1: net with X 0.900, without 0.639, diff +0.261; 10: net with X 0.925, without 0.704, diff +0.221; SIMX_I modal share at 0.1: 0.369 [0.269, 0.476]; max paired static advantage of SIMX_I over SI100n against an inspectee class at P=0.1 (A_f): +3.100 |
| 5c-gemini | **failed** | modal share < 0.1: False; no class where SIMX_I beats SI100n by more than 0.05: False |
| 5c-gpt | **supported** | modal share SIMX_I (A_f+X) 0.369 against its counterpart-clone share in the sham cell 0.235 |
| 6 | **held** | 0.1: C 37/40 = 0.925 [0.801, 0.974], status met (confirmation A: 37/40), max steps 759079, forfeit runs 0; 1: C 39/40 = 0.975 [0.871, 0.996], status met (confirmation A: 36/40), max steps 750021, forfeit runs 0 |
| 6c-gpt | **failed** | a count more than 3 from the confirmation run at some level: False |
| 9 | **failed** | fallback share A_m: 0.1 no-X 0.100 [0.025, 0.200]; 0.1 X 0.121 [0.025, 0.222]; 0.3 no-X 0.000 [0.000, 0.000]; 0.3 X 0.025 [0.000, 0.075]; 1 no-X 0.000 [0.000, 0.000]; 1 X 0.000 [0.000, 0.000]; 10 no-X 0.000 [0.000, 0.000]; 10 X 0.000 [0.000, 0.000] |
| 9c-gpt | **held** | fallback share >= 0.05 at 0.1 in some arm: True |
| 10 | **failed** | 0.03: by mixing failed/met, e_comp 0.1323/0.0311; 0.03+X: by mixing failed/undetermined, e_comp 0.0388/0.0020; 0.1: by mixing undetermined/met, e_comp 0.0000/0.0000; 0.1+X: by mixing undetermined/met, e_comp 0.0129/0.0000; 0.3: by mixing met/met, e_comp 0.0000/0.0000; 0.3+X: by mixing undetermined/met, e_comp 0.0000/0.0000; 1: by mixing met/met, e_comp 0.0137/0.0000; 1+X: by mixing met/met, e_comp 0.0119/0.0000; 10: by mixing met/met, e_comp 0.0167/0.0161; 10+X: by mixing met/met, e_comp 0.0250/0.0242; insp 0.1: undetermined/undetermined; insp 1: met/undetermined |
| 10c-gpt | **held** | some status differs: True |
| 11 | **held** | SIMX mass at 0.1: A_m 0.00795, A_f 0.00000, ratio nan, 95% interval of the ratio of paired means [nan, nan] |
| 11c-gemini | **failed** | the interval of the ratio contains 1: False (A_f mass 0.00000, A_m mass 0.00795, founder mass 0.00095: A_m above the founder floor, A_f below it) |

Engineer's predictions:

| # | verdict | detail |
|---|---|---|
| E1 | **held** | 1: PB modal A_f 0.000 [0.000, 0.000], A 0.581 [0.485, 0.675]; 10: PB modal A_f 0.002 [0.000, 0.005], A 0.697 [0.605, 0.782] |
| E2 | **failed** | 1: U modal 0.182 [0.114, 0.255], PRR modal 0.806 [0.734, 0.875]; 10: U modal 0.066 [0.029, 0.106], PRR modal 0.896 [0.833, 0.952] |
| E3 | **held** | concurrent A by mixing: 0.03: undetermined; 0.1: met; 0.3: undetermined; 1: failed; 10: failed |
| E4 | **held** | A 0.03: 0.00000; Af 0.03: 0.00000; A 0.1: 0.00000; Af 0.1: 0.00000 |
| E5 | **failed** | Af 0.03: mass 0.08364 present 0.238; Am 0.03: mass 0.14243 present 0.346; Af 0.1: mass 0.00000 present 0.000; Am 0.1: mass 0.00795 present 0.031; A 0.1: mass 0.52744 present 0.721; Af 0.3: mass 0.00000 present 0.000; Am 0.3: mass 0.00000 present 0.000; Af 1: mass 0.00000 present 0.000; Am 1: mass 0.00000 present 0.000; A 1: mass 0.34840 present 0.600; Af 10: mass 0.00000 present 0.000; Am 10: mass 0.00000 present 0.000 |
| E6 | **failed** | Af 0.1: diff +0.030, mass SIMX_I 0.36729 vs SI100n 0.17968; A 0.1: diff +0.137, mass SIMX_I 0.42134 vs SI100n 0.15594; Af 1: diff +0.261, mass SIMX_I 0.49332 vs SI100n 0.08124; A 1: diff -0.011, mass SIMX_I 0.56750 vs SI100n 0.07673 |
| E7 | **failed** | 0.1 RPS e_gross +0.0000; 0.1 RPS forfeit +0.0000; 0.1 insp net +0.2266; 1 RPS e_gross +0.0021; 1 RPS forfeit +0.0000; 1 insp net +0.1660 |
| E8 | **failed** | 0.1 A-Af +0.0609; 0.1 A-Am +0.0727; 0.1 Af-Am +0.0117; 1 A-Af +0.1473; 1 A-Am -0.0086; 1 Af-Am -0.1559 |
| E9 | **failed** | A_m against A_f without X: 0.03: e_comp 0.1012, fallback 0.2068; 0.1: e_comp 0.0000, fallback 0.1000; 0.3: e_comp 0.0000, fallback 0.0000; 1: e_comp 0.0137, fallback 0.0000; 10: e_comp 0.0005, fallback 0.0008 |
| E10 | **held** | 0.1: C 37/40, forfeit runs 0, max steps 759079; 1: C 39/40, forfeit runs 0, max steps 750021 |
| E12 | **failed** | 1: coin mass A_m 0.442 A_f 0.190, fallback excess +0.0000; 10: coin mass A_m 0.074 A_f 0.100, fallback excess -0.0008 |

## Exact simulators: mass, presence, modal share (RPS)

| cell | mass SIMX | mass SIM100u | mass SIM100u~ | islands with SIMX present | SIMX modal | SIM100u~ modal | SIM100u modal |
|---|---|---|---|---|---|---|---|
| Af+X@0.03 | 0.08364 | 0.00644 | 0.00000 | 0.238 | 0.071 | 0.000 | 0.006 |
| Am+X@0.03 | 0.14243 | 0.00020 | 0.00000 | 0.346 | 0.129 | 0.000 | 0.000 |
| A+X@0.1 | 0.52744 | 0.00000 | 0.00000 | 0.721 | 0.530 | 0.000 | 0.000 |
| Af+S@0.1 | 0.00000 | 0.00000 | 0.00000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Af+X@0.1 | 0.00000 | 0.00000 | 0.00000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Am+X@0.1 | 0.00795 | 0.00089 | 0.00000 | 0.031 | 0.006 | 0.000 | 0.001 |
| Af+X@0.3 | 0.00000 | 0.00000 | 0.00000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Am+X@0.3 | 0.00000 | 0.00000 | 0.00000 | 0.000 | 0.000 | 0.000 | 0.000 |
| A+X@1 | 0.34840 | 0.00000 | 0.00000 | 0.600 | 0.342 | 0.000 | 0.000 |
| Af+S@1 | 0.00000 | 0.00000 | 0.00000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Af+X@1 | 0.00000 | 0.00000 | 0.00000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Am+X@1 | 0.00000 | 0.00000 | 0.00000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Af+X@10 | 0.00000 | 0.00000 | 0.00000 | 0.000 | 0.000 | 0.000 | 0.000 |
| Am+X@10 | 0.00000 | 0.00000 | 0.00000 | 0.000 | 0.000 | 0.000 | 0.000 |

Inspection:

| cell | mass SIMX_I | mass SI100n | mass SI100n~ | SIMX_I present | SIMX_I modal | mass SIMX_E | mass SE100k | SIMX_E present | SIMX_E modal |
|---|---|---|---|---|---|---|---|---|---|
| Af+X@0.03 | 0.54096 | 0.22089 | 0.00000 | 0.794 | 0.546 | 0.00000 | 0.00000 | 0.000 | 0.000 |
| A+X@0.1 | 0.42134 | 0.15594 | 0.00000 | 0.685 | 0.430 | 0.00000 | 0.00000 | 0.000 | 0.000 |
| Af+S@0.1 | 0.00000 | 0.29262 | 0.23819 | 0.000 | 0.000 | 0.00000 | 0.00000 | 0.000 | 0.000 |
| Af+X@0.1 | 0.36729 | 0.17968 | 0.00000 | 0.637 | 0.369 | 0.00000 | 0.00000 | 0.000 | 0.000 |
| Am+X@0.1 | 0.57411 | 0.08137 | 0.00000 | 0.818 | 0.586 | 0.00000 | 0.00000 | 0.000 | 0.000 |
| Af+X@0.3 | 0.46671 | 0.14219 | 0.00000 | 0.696 | 0.471 | 0.00000 | 0.00000 | 0.000 | 0.000 |
| A+X@1 | 0.56750 | 0.07673 | 0.00000 | 0.780 | 0.578 | 0.00000 | 0.00000 | 0.000 | 0.000 |
| Af+S@1 | 0.00000 | 0.16222 | 0.10599 | 0.000 | 0.000 | 0.00000 | 0.00000 | 0.000 | 0.000 |
| Af+X@1 | 0.49332 | 0.08124 | 0.00000 | 0.696 | 0.493 | 0.00000 | 0.00000 | 0.000 | 0.000 |
| Am+X@1 | 0.46569 | 0.09768 | 0.00000 | 0.678 | 0.476 | 0.00000 | 0.00000 | 0.000 | 0.000 |
| Af+X@10 | 0.71832 | 0.05608 | 0.00000 | 0.823 | 0.723 | 0.00000 | 0.00000 | 0.000 | 0.000 |

The exact simulator's plays (SIMX holders, RPS): finished / forfeit / private tape inside the read, and the forfeit by opponent family:

| cell | SIMX weight (sum of island masses) | plays: exact read finished | forfeit (read ran out) | a private tape inside the read | forfeit by opponent family |
|---|---|---|---|---|---|
| rps_A+X_0.1_primary | 1350.2500 | 0.108 | 0.892 | 0.108 | sim 0.892 |
| rps_A+X_1_primary | 891.9100 | 0.066 | 0.934 | 0.066 | sim 0.812, prover 0.122 |
| rps_Af+X_0.03_primary | 214.1200 | 0.319 | 0.681 | 0.319 | sim 0.681 |
| rps_Af+X_0.1_primary | 0 | - | - | - | - |
| rps_Af+X_0.3_primary | 0 | - | - | - | - |
| rps_Af+X_10_primary | 0 | - | - | - | - |
| rps_Af+X_1_primary | 0 | - | - | - | - |
| rps_Am+X_0.03_primary | 364.6200 | 0.208 | 0.792 | 0.208 | sim 0.731, prover 0.061 |
| rps_Am+X_0.1_primary | 20.3600 | 0.052 | 0.948 | 0.052 | sim 0.559, prover 0.389 |
| rps_Am+X_0.3_primary | 0 | - | - | - | - |
| rps_Am+X_10_primary | 0 | - | - | - | - |
| rps_Am+X_1_primary | 0 | - | - | - | - |

Conditional on being founded (RPS; the exact simulator against its sham twin where the cell has one):

| cell | twin | islands founded with it | present at 2,000 | modal at 2,000 | mean founder mass (founded islands) | mean mass at 2,000 |
|---|---|---|---|---|---|---|
| rps_A+X_0.1_primary | SIMX | 227 | 0.749 | 0.551 | 0.011 | 0.547 |
| rps_A+X_1_primary | SIMX | 227 | 0.661 | 0.379 | 0.011 | 0.375 |
| rps_Af+S_0.1_primary | SIM100u~ | 227 | 0.000 | 0.000 | 0.011 | 0.000 |
| rps_Af+S_1_primary | SIM100u~ | 227 | 0.000 | 0.000 | 0.011 | 0.000 |
| rps_Af+X_0.03_primary | SIMX | 227 | 0.260 | 0.079 | 0.011 | 0.093 |
| rps_Af+X_0.1_primary | SIMX | 227 | 0.000 | 0.000 | 0.011 | 0.000 |
| rps_Af+X_0.3_primary | SIMX | 227 | 0.000 | 0.000 | 0.011 | 0.000 |
| rps_Af+X_10_primary | SIMX | 227 | 0.000 | 0.000 | 0.011 | 0.000 |
| rps_Af+X_1_primary | SIMX | 227 | 0.000 | 0.000 | 0.011 | 0.000 |
| rps_Am+X_0.03_primary | SIMX | 227 | 0.401 | 0.137 | 0.011 | 0.158 |
| rps_Am+X_0.1_primary | SIMX | 227 | 0.031 | 0.000 | 0.011 | 0.002 |
| rps_Am+X_0.3_primary | SIMX | 227 | 0.000 | 0.000 | 0.011 | 0.000 |
| rps_Am+X_10_primary | SIMX | 227 | 0.000 | 0.000 | 0.011 | 0.000 |
| rps_Am+X_1_primary | SIMX | 227 | 0.000 | 0.000 | 0.011 | 0.000 |

## Supplementary inspection runs (indices 340-419 pooled with 300-339, 120 runs per cell)

| level | A_f no X (120 runs) | A_f + X | X - none (paired) | A_f + sham | sham - none (paired) | X - sham (paired) | mass SIMX_I / SI100n in the X cell |
|---|---|---|---|---|---|---|---|
| 0.03 | 0.756 [0.679, 0.833] met | 0.814 [0.741, 0.881] met | 0.058 [-0.042, 0.155] | - | - | - | 0.478 / 0.193 |
| 0.1 | 0.769 [0.694, 0.838] met | 0.820 [0.749, 0.883] met | 0.051 [-0.043, 0.145] | 0.887 [0.834, 0.936] met | 0.118 [0.030, 0.208] | -0.067 [-0.149, 0.013] | 0.424 / 0.155 |
| 0.3 | 0.726 [0.651, 0.797] met | 0.864 [0.800, 0.919] met | 0.138 [0.043, 0.232] | - | - | - | 0.520 / 0.113 |
| 1 | 0.710 [0.635, 0.783] met | 0.867 [0.808, 0.925] met | 0.156 [0.057, 0.261] | 0.808 [0.744, 0.867] met | 0.098 [0.008, 0.183] | 0.058 [-0.027, 0.149] | 0.505 / 0.081 |
| 10 | 0.766 [0.703, 0.825] met | 0.825 [0.758, 0.892] met | 0.059 [-0.032, 0.151] | - | - | - | 0.728 / 0.035 |

## Charge per play, split into timed-out capped reads and forfeits (RPS)

| cell | timed-out capped reads per play | forfeits per play | charge per play |
|---|---|---|---|
| A@0.03 | 0.0375 [0.0028, 0.0976] | 0.0000 [0.0000, 0.0000] | 0.0011 [0.0001, 0.0029] |
| Af@0.03 | 0.0316 [0.0032, 0.0852] | 0.0000 [0.0000, 0.0000] | 0.0009 [0.0001, 0.0026] |
| Af+X@0.03 | 0.0229 [0.0009, 0.0567] | 0.0569 [0.0226, 0.1036] | 0.0024 [0.0008, 0.0047] |
| Am@0.03 | 0.1228 [0.0642, 0.1947] | 0.2068 [0.1181, 0.3040] | 0.0099 [0.0064, 0.0135] |
| Am+X@0.03 | 0.0566 [0.0185, 0.1130] | 0.2305 [0.1359, 0.3351] | 0.0086 [0.0052, 0.0124] |
| A@0.1 | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] |
| A+X@0.1 | 0.0000 [0.0000, 0.0000] | 0.4707 [0.3576, 0.5873] | 0.0000 [0.0000, 0.0000] |
| Af@0.1 | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] |
| Af+X@0.1 | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0001] | 0.0000 [0.0000, 0.0000] |
| Am@0.1 | 0.0000 [0.0000, 0.0000] | 0.1000 [0.0250, 0.2000] | 0.0100 [0.0025, 0.0200] |
| Am+X@0.1 | 0.0040 [0.0000, 0.0109] | 0.1214 [0.0253, 0.2224] | 0.0125 [0.0026, 0.0226] |
| A@0.3 | 0.0000 [0.0000, 0.0000] | 0.0339 [0.0000, 0.0860] | 0.0000 [0.0000, 0.0000] |
| Af@0.3 | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] |
| Af+X@0.3 | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] |
| Am@0.3 | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] |
| Am+X@0.3 | 0.0000 [0.0000, 0.0000] | 0.0250 [0.0000, 0.0750] | 0.0075 [0.0000, 0.0225] |
| A@1 | 0.0000 [0.0000, 0.0000] | 0.4898 [0.3976, 0.5846] | 0.0000 [0.0000, 0.0000] |
| A+X@1 | 0.0000 [0.0000, 0.0000] | 0.7035 [0.6074, 0.7883] | 0.0000 [0.0000, 0.0000] |
| Af@1 | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] |
| Af+X@1 | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] |
| Am@1 | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] |
| Am+X@1 | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] |
| A@10 | 0.0000 [0.0000, 0.0000] | 0.6234 [0.5262, 0.7153] | 0.0000 [0.0000, 0.0000] |
| Af@10 | 0.0002 [0.0000, 0.0007] | 0.0008 [0.0000, 0.0025] | 0.0105 [0.0000, 0.0314] |
| Af+X@10 | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] |
| Am@10 | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] |
| Am+X@10 | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] | 0.0000 [0.0000, 0.0000] |

## Static paired payoffs: exact against capped simulators, by opponent class

| opponent | SIMX gross (A, A_f) | timeouts | forfeit | SIM100u gross | timeouts | opponent gross vs SIMX | SIMX - SIM100u net (A_f) at 0.1 / 1 | SIMX net A_m at 0.1 | predictability of the opponent (agreement of two draws) |
|---|---|---|---|---|---|---|---|---|---|
| R0 | +1.000 | 0 | 0 | +1.000 | 0 | -1.000 | +0.000 / +0.000 | +1.000 | 1.000 |
| P0 | +1.000 | 0 | 0 | +1.000 | 0 | -1.000 | +0.000 / +0.000 | +1.000 | 1.000 |
| S0 | +1.000 | 0 | 0 | +1.000 | 0 | -1.000 | +0.000 / +0.000 | +1.000 | 1.000 |
| U | +0.000 | 0 | 0 | +0.000 | 0 | +0.000 | +0.000 / +0.000 | +0.000 | 0.333 |
| B_RP | +0.333 | 0 | 0 | +0.333 | 0 | -0.333 | +0.000 / +0.000 | +0.333 | 0.556 |
| B_RS | +0.333 | 0 | 0 | +0.333 | 0 | -0.333 | +0.000 / +0.000 | +0.333 | 0.556 |
| B_PR | +0.333 | 0 | 0 | +0.333 | 0 | -0.333 | +0.000 / +0.000 | +0.333 | 0.556 |
| B_PS | +0.333 | 0 | 0 | +0.333 | 0 | -0.333 | +0.000 / +0.000 | +0.333 | 0.556 |
| B_SR | +0.333 | 0 | 0 | +0.333 | 0 | -0.333 | +0.000 / +0.000 | +0.333 | 0.556 |
| B_SP | +0.333 | 0 | 0 | +0.333 | 0 | -0.333 | +0.000 / +0.000 | +0.333 | 0.556 |
| CB_RP | +0.333 | 0 | 0 | +0.333 | 0 | -0.333 | +0.000 / +0.000 | +0.333 | 0.556 |
| CB_RS | +0.333 | 0 | 0 | +0.333 | 0 | -0.333 | +0.000 / +0.000 | +0.333 | 0.556 |
| CB_PR | +0.333 | 0 | 0 | +0.333 | 0 | -0.333 | +0.000 / +0.000 | +0.333 | 0.556 |
| CB_PS | +0.333 | 0 | 0 | +0.333 | 0 | -0.333 | +0.000 / +0.000 | +0.333 | 0.556 |
| CB_SR | +0.333 | 0 | 0 | +0.333 | 0 | -0.333 | +0.000 / +0.000 | +0.333 | 0.556 |
| CB_SP | +0.333 | 0 | 0 | +0.333 | 0 | -0.333 | +0.000 / +0.000 | +0.333 | 0.556 |
| H0 | +1.000 | 0 | 0 | +1.000 | 0 | -1.000 | +0.000 / +0.000 | +1.000 | 1.000 |
| H1 | +1.000 | 0 | 0 | +1.000 | 0 | -1.000 | +0.000 / +0.000 | +1.000 | 1.000 |
| H2 | +1.000 | 0 | 0 | +1.000 | 0 | -1.000 | +0.000 / +0.000 | +1.000 | 1.000 |
| SIM20R | +1.000 | 1 | 0 | +1.000 | 1 | -1.000 | +0.000 / +0.000 | +0.900 | 1.000 |
| SIM20P | +1.000 | 1 | 0 | +1.000 | 1 | -1.000 | +0.000 / +0.000 | +0.900 | 1.000 |
| SIM20S | +1.000 | 1 | 0 | +1.000 | 1 | -1.000 | +0.000 / +0.000 | +0.900 | 1.000 |
| SIM20u | +0.000 | 1 | 0 | +0.000 | 1 | +0.000 | +0.000 / +0.000 | -0.100 | 0.333 |
| SIM100R | +1.000 | 1 | 0 | +0.000 | 1 | -1.000 | +1.000 / +1.000 | +0.900 | 1.000 |
| SIM100P | +1.000 | 1 | 0 | +0.000 | 1 | -1.000 | +1.000 / +1.000 | +0.900 | 1.000 |
| SIM100S | +1.000 | 1 | 0 | +0.000 | 1 | -1.000 | +1.000 / +1.000 | +0.900 | 1.000 |
| SIM100u | +0.000 | 1 | 0 | +0.000 | 1 | +0.000 | +0.000 / +0.000 | -0.100 | 0.333 |
| PB | +0.000 | 0 | 1 | +1.000 | 1 | +0.000 | -1.000 / -1.000 | -0.100 | forfeit |
| PRR | +0.000 | 0 | 0 | +0.000 | 1 | +0.000 | +0.100 / +1.000 | +0.000 | 0.333 |
| CRR | +0.000 | 0 | 0 | +0.000 | 0 | +0.000 | +0.000 / +0.000 | +0.000 | 0.333 |


**SIMX_I against SI100n (inspector payoffs, by inspectee class)**

| opponent | SIMX_I gross (A, A_f) | timeouts | forfeit | SI100n gross | timeouts | forfeit | net (A_f) difference at 0.1 / 1 | SIMX_I net A_m at 0.1 |
|---|---|---|---|---|---|---|---|---|
| C0 | +0.000 | 0 | 0 | +0.000 | 0 | 0 | +0.000 / +0.000 | +0.000 |
| K0 | -1.000 | 0 | 0 | -1.000 | 0 | 0 | +0.000 / +0.000 | -1.000 |
| Mc1 | -0.562 | 0 | 0 | -0.562 | 0 | 0 | +0.000 / +0.000 | -0.562 |
| Mc2 | -1.000 | 0 | 0 | -1.000 | 0 | 0 | +0.000 / +0.000 | -1.000 |
| Mc3 | -1.312 | 0 | 0 | -1.312 | 0 | 0 | +0.000 / +0.000 | -1.312 |
| Mc4 | -1.500 | 0 | 0 | -1.500 | 0 | 0 | +0.000 / +0.000 | -1.500 |
| Mc5 | -1.562 | 0 | 0 | -1.562 | 0 | 0 | +0.000 / +0.000 | -1.562 |
| Mc6 | -1.500 | 0 | 0 | -1.500 | 0 | 0 | +0.000 / +0.000 | -1.500 |
| Mc7 | -1.312 | 0 | 0 | -1.312 | 0 | 0 | +0.000 / +0.000 | -1.312 |
| HE0 | -1.000 | 0 | 0 | -1.000 | 0 | 0 | +0.000 / +0.000 | -1.000 |
| HE1 | +0.000 | 0 | 0 | +0.000 | 0 | 0 | +0.000 / +0.000 | +0.000 |
| SE20k | -1.000 | 1 | 0 | -1.000 | 1 | 0 | +0.000 / +0.000 | -1.100 |
| SE20c | +0.000 | 1 | 0 | +0.000 | 1 | 0 | +0.000 / +0.000 | -0.100 |
| SE100k | -1.000 | 1 | 0 | -4.000 | 1 | 0 | +3.000 / +3.000 | -1.100 |
| SE100c | +0.000 | 1 | 0 | +0.000 | 1 | 0 | +0.000 / +0.000 | -0.100 |
| PE | +0.000 | 0 | 0 | +0.000 | 1 | 0 | +0.100 / +1.000 | +0.000 |
| PEC | -1.000 | 0 | 0 | -4.000 | 1 | 0 | +3.100 / +4.000 | -1.000 |
| PR2 | +0.000 | 0 | 0 | +0.000 | 0 | 0 | +0.000 / +0.000 | +0.000 |
| PR3 | +0.000 | 0 | 0 | +0.000 | 0 | 0 | +0.000 / +0.000 | +0.000 |
| PR4 | +0.000 | 0 | 0 | +0.000 | 0 | 0 | +0.000 / +0.000 | +0.000 |
| CR2 | -1.000 | 0 | 0 | -1.000 | 0 | 0 | +0.000 / +0.000 | -1.000 |
| CR3 | -1.000 | 0 | 0 | -1.000 | 0 | 0 | +0.000 / +0.000 | -1.000 |
| CR4 | -1.000 | 0 | 0 | -1.000 | 0 | 0 | +0.000 / +0.000 | -1.000 |
| PCR3 | +0.000 | 0 | 0 | +0.000 | 0 | 0 | +0.000 / +0.000 | +0.000 |


**SIMX_E against SE100k (inspectee payoffs, by inspector class)**

| opponent | SIMX_E gross (A, A_f) | timeouts | forfeit | SE100k gross | timeouts | forfeit | net (A_f) difference at 0.1 / 1 | SIMX_E net A_m at 0.1 |
|---|---|---|---|---|---|---|---|---|
| I0 | +0.000 | 0 | 0 | +0.000 | 0 | 0 | +0.000 / +0.000 | +0.000 |
| N0 | +1.000 | 0 | 0 | +1.000 | 0 | 0 | +0.000 / +0.000 | +1.000 |
| M1 | +0.438 | 0 | 0 | +0.438 | 0 | 0 | +0.000 / +0.000 | +0.438 |
| M2 | +0.000 | 0 | 0 | +0.000 | 0 | 0 | +0.000 / +0.000 | +0.000 |
| M3 | -0.312 | 0 | 0 | -0.312 | 0 | 0 | +0.000 / +0.000 | -0.312 |
| M4 | -0.500 | 0 | 0 | -0.500 | 0 | 0 | +0.000 / +0.000 | -0.500 |
| M5 | -0.562 | 0 | 0 | -0.562 | 0 | 0 | +0.000 / +0.000 | -0.562 |
| M6 | -0.500 | 0 | 0 | -0.500 | 0 | 0 | +0.000 / +0.000 | -0.500 |
| M7 | -0.312 | 0 | 0 | -0.312 | 0 | 0 | +0.000 / +0.000 | -0.312 |
| CARR1 | +0.438 | 0 | 0 | +0.438 | 0 | 0 | +0.000 / +0.000 | +0.438 |
| CARR2 | +0.000 | 0 | 0 | +0.000 | 0 | 0 | +0.000 / +0.000 | +0.000 |
| CARR3 | -0.312 | 0 | 0 | -0.312 | 0 | 0 | +0.000 / +0.000 | -0.312 |
| CARR4 | -0.500 | 0 | 0 | -0.500 | 0 | 0 | +0.000 / +0.000 | -0.500 |
| CARR6 | -0.500 | 0 | 0 | -0.500 | 0 | 0 | +0.000 / +0.000 | -0.500 |
| HI0 | +1.000 | 0 | 0 | +1.000 | 0 | 0 | +0.000 / +0.000 | +1.000 |
| HI1 | +0.000 | 0 | 0 | +0.000 | 0 | 0 | +0.000 / +0.000 | +0.000 |
| SI20n | +1.000 | 1 | 0 | +1.000 | 1 | 0 | +0.000 / +0.000 | +0.900 |
| SI20i | +0.000 | 1 | 0 | +0.000 | 1 | 0 | +0.000 / +0.000 | -0.100 |
| SI100n | +1.000 | 1 | 0 | +1.000 | 1 | 0 | +0.000 / +0.000 | +0.900 |
| SI100i | +0.000 | 1 | 0 | -3.000 | 1 | 0 | +3.000 / +3.000 | -0.100 |
| RI | +0.000 | 0 | 0 | -3.000 | 1 | 0 | +3.100 / +4.000 | +0.000 |
| RIM | -3.000 | 0 | 1 | -1.000 | 1 | 0 | -2.000 / -2.000 | -0.100 |

## Recursive reader pairs at nearby fuel budgets (K = 9,000 / 10,000 / 11,000)

| pair set | opponent | law and events across K | play law (first K) | events | steps |
|---|---|---|---|---|---|
| rps | R0 | same | {'P': 1.0} | forf 0, capped TO 0 | K9000: 9 steps; K10000: 9 steps; K11000: 9 steps |
| rps | U | same | {'P': 0.3333333333333333, 'S': 0.3333333333333333, 'R': 0.3333333333333333} | forf 0, capped TO 0 | K9000: 16 steps; K10000: 16 steps; K11000: 16 steps |
| rps | B_RP | same | {'P': 0.6666666666666666, 'S': 0.3333333333333333} | forf 0, capped TO 0 | K9000: 13 steps; K10000: 13 steps; K11000: 13 steps |
| rps | H0 | DIFFERS | {'R': 1.0} | forf 0, capped TO 0 | K9000: 50 steps; K10000: 48 steps; K11000: 44 steps |
| rps | SIM20R | same | {'P': 1.0} | forf 0, capped TO 1 | K9000: 38 steps; K10000: 38 steps; K11000: 38 steps |
| rps | SIM100u | same | {'P': 0.3333333333333333, 'S': 0.3333333333333333, 'R': 0.3333333333333333} | forf 0, capped TO 1 | K9000: 125 steps; K10000: 125 steps; K11000: 125 steps |
| rps | PRR | same | {'P': 0.3333333333333333, 'S': 0.3333333333333333, 'R': 0.3333333333333333} | forf 0, capped TO 0 | K9000: 229 steps; K10000: 229 steps; K11000: 229 steps |
| rps | CRR | same | {'P': 0.3333333333333333, 'S': 0.3333333333333333, 'R': 0.3333333333333333} | forf 0, capped TO 0 | K9000: 22 steps; K10000: 22 steps; K11000: 22 steps |
| rps | PB | same | {'BOT': 1.0} | forf 1, capped TO 0 | K9000: 9000 steps; K10000: 10000 steps; K11000: 11000 steps |
| rps | SIMX | same | {'BOT': 1.0} | forf 1, capped TO 0 | K9000: 9000 steps; K10000: 10000 steps; K11000: 11000 steps |
| insp0 | C0 | same | {'N': 1.0} | forf 0, capped TO 0 | K9000: 11 steps; K10000: 11 steps; K11000: 11 steps |
| insp0 | K0 | same | {'I': 1.0} | forf 0, capped TO 0 | K9000: 9 steps; K10000: 9 steps; K11000: 9 steps |
| insp0 | Mc4 | same | {'I': 0.5, 'N': 0.5} | forf 0, capped TO 0 | K9000: 13 steps; K10000: 13 steps; K11000: 13 steps |
| insp0 | HE0 | DIFFERS | {'I': 1.0} | forf 0, capped TO 0 | K9000: 39 steps; K10000: 39 steps; K11000: 41 steps |
| insp0 | SE20k | same | {'I': 1.0} | forf 0, capped TO 1 | K9000: 33 steps; K10000: 33 steps; K11000: 33 steps |
| insp0 | SE100c | same | {'N': 1.0} | forf 0, capped TO 1 | K9000: 115 steps; K10000: 115 steps; K11000: 115 steps |
| insp0 | PE | same | {'N': 1.0} | forf 0, capped TO 0 | K9000: 5879 steps; K10000: 5879 steps; K11000: 5879 steps |
| insp0 | CR3 | same | {'I': 1.0} | forf 0, capped TO 0 | K9000: 11 steps; K10000: 11 steps; K11000: 11 steps |
| insp0 | PR3 | same | {'N': 1.0} | forf 0, capped TO 0 | K9000: 25 steps; K10000: 25 steps; K11000: 25 steps |
| insp0 | PCR3 | same | {'N': 1.0} | forf 0, capped TO 0 | K9000: 29 steps; K10000: 29 steps; K11000: 29 steps |
| insp0 | SIMX_E | same | {'BOT': 1.0} | forf 1, capped TO 0 | K9000: 9000 steps; K10000: 10000 steps; K11000: 11000 steps |
| insp1 | I0 | same | {'C': 1.0} | forf 0, capped TO 0 | K9000: 9 steps; K10000: 9 steps; K11000: 9 steps |
| insp1 | N0 | same | {'K': 1.0} | forf 0, capped TO 0 | K9000: 11 steps; K10000: 11 steps; K11000: 11 steps |
| insp1 | M4 | same | {'C': 0.5, 'K': 0.5} | forf 0, capped TO 0 | K9000: 13 steps; K10000: 13 steps; K11000: 13 steps |
| insp1 | CARR3 | same | {'C': 0.375, 'K': 0.625} | forf 0, capped TO 0 | K9000: 16 steps; K10000: 16 steps; K11000: 16 steps |
| insp1 | HI0 | DIFFERS | {'K': 1.0} | forf 0, capped TO 0 | K9000: 41 steps; K10000: 41 steps; K11000: 39 steps |
| insp1 | SI20n | same | {'K': 1.0} | forf 0, capped TO 1 | K9000: 35 steps; K10000: 35 steps; K11000: 35 steps |
| insp1 | SI100i | same | {'C': 1.0} | forf 0, capped TO 1 | K9000: 113 steps; K10000: 113 steps; K11000: 113 steps |
| insp1 | RI | same | {'C': 1.0} | forf 0, capped TO 0 | K9000: 5877 steps; K10000: 5877 steps; K11000: 5877 steps |
| insp1 | RIM | same | {'BOT': 1.0} | forf 1, capped TO 0 | K9000: 9000 steps; K10000: 10000 steps; K11000: 11000 steps |

## Support and transitions (RPS, share of islands whose modal programme changed)

| cell | modal changes 1500-2000 | 2000-4000 | support changes 2000-4000 |
|---|---|---|---|
| A@0.03 | 0.146 | 0.107 | 0.212 |
| Af+X@0.03 | 0.264 | 0.188 | 0.338 |
| Af@0.03 | 0.145 | 0.104 | 0.188 |
| Am+X@0.03 | 0.396 | 0.259 | 0.498 |
| Am@0.03 | 0.386 | 0.287 | 0.523 |
| A+X@0.1 | 0.289 | 0.293 | 0.433 |
| A@0.1 | 0.139 | 0.132 | 0.233 |
| Af+S@0.1 | 0.166 | 0.164 | 0.259 |
| Af+X@0.1 | 0.178 | 0.155 | 0.262 |
| Af@0.1 | 0.118 | 0.116 | 0.190 |
| Am+X@0.1 | 0.220 | 0.184 | 0.324 |
| Am@0.1 | 0.113 | 0.087 | 0.125 |
| A@0.3 | 0.195 | 0.213 | 0.312 |
| Af+X@0.3 | 0.263 | 0.255 | 0.370 |
| Af@0.3 | 0.157 | 0.157 | 0.215 |
| Am+X@0.3 | 0.245 | 0.256 | 0.381 |
| Am@0.3 | 0.148 | 0.130 | 0.216 |
| A+X@1 | 0.411 | 0.355 | 0.527 |
| A@1 | 0.364 | 0.314 | 0.506 |
| Af+S@1 | 0.264 | 0.251 | 0.370 |
| Af+X@1 | 0.260 | 0.258 | 0.373 |
| Af@1 | 0.220 | 0.199 | 0.282 |
| Am+X@1 | 0.306 | 0.257 | 0.382 |
| Am@1 | 0.336 | 0.346 | 0.461 |
| A@10 | 0.308 | 0.290 | 0.434 |
| Af+X@10 | 0.119 | 0.108 | 0.161 |
| Af@10 | 0.130 | 0.114 | 0.177 |
| Am+X@10 | 0.093 | 0.087 | 0.145 |
| Am@10 | 0.080 | 0.087 | 0.125 |

## Secondary: generation 4,000 (RPS by mixing, inspection net)

| cell | RPS by mixing (4000) | e_gross | forfeit share | insp net (4000) |
|---|---|---|---|---|
| A@0.03 | met | 0.025 [0.000, 0.075] | 0.000 [0.000, 0.000] | met 0.750 [0.625, 0.875] |
| Af+X@0.03 | met | 0.000 [0.000, 0.000] | 0.009 [0.000, 0.022] | met 0.775 [0.650, 0.900] |
| Af@0.03 | met | 0.025 [0.000, 0.075] | 0.000 [0.000, 0.000] | undetermined 0.700 [0.550, 0.825] |
| Am+X@0.03 | failed | 0.030 [0.000, 0.076] | 0.211 [0.100, 0.337] | - |
| Am@0.03 | failed | 0.048 [0.003, 0.112] | 0.181 [0.078, 0.302] | - |
| A+X@0.1 | failed | 0.000 [0.000, 0.000] | 0.458 [0.338, 0.585] | met 0.903 [0.812, 0.978] |
| A@0.1 | met | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | met 0.766 [0.637, 0.887] |
| Af+S@0.1 | met | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | met 0.932 [0.857, 1.000] |
| Af+X@0.1 | met | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | met 0.744 [0.607, 0.869] |
| Af@0.1 | met | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | undetermined 0.701 [0.569, 0.831] |
| Am+X@0.1 | undetermined | 0.009 [0.000, 0.028] | 0.116 [0.025, 0.216] | met 0.825 [0.700, 0.925] |
| Am@0.1 | undetermined | 0.000 [0.000, 0.000] | 0.100 [0.025, 0.200] | undetermined 0.680 [0.540, 0.809] |
| A@0.3 | undetermined | 0.037 [0.000, 0.093] | 0.032 [0.000, 0.080] | met 0.814 [0.691, 0.923] |
| Af+X@0.3 | met | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | met 0.875 [0.775, 0.975] |
| Af@0.3 | met | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | undetermined 0.701 [0.555, 0.836] |
| Am+X@0.3 | undetermined | 0.000 [0.000, 0.000] | 0.025 [0.000, 0.075] | - |
| Am@0.3 | met | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | - |
| A+X@1 | failed | 0.409 [0.288, 0.531] | 0.754 [0.644, 0.851] | met 0.782 [0.650, 0.900] |
| A@1 | failed | 0.585 [0.467, 0.700] | 0.527 [0.405, 0.647] | met 0.788 [0.662, 0.900] |
| Af+S@1 | met | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | met 0.813 [0.700, 0.913] |
| Af+X@1 | met | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | met 0.900 [0.800, 0.975] |
| Af@1 | met | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | undetermined 0.654 [0.512, 0.795] |
| Am+X@1 | met | 0.014 [0.000, 0.042] | 0.000 [0.000, 0.000] | met 0.800 [0.675, 0.925] |
| Am@1 | met | 0.019 [0.000, 0.048] | 0.000 [0.000, 0.000] | met 0.805 [0.679, 0.918] |
| A@10 | failed | 0.811 [0.718, 0.896] | 0.662 [0.546, 0.769] | met 0.846 [0.745, 0.936] |
| Af+X@10 | met | 0.021 [0.000, 0.054] | 0.000 [0.000, 0.000] | met 0.925 [0.825, 1.000] |
| Af@10 | met | 0.015 [0.000, 0.039] | 0.000 [0.000, 0.001] | undetermined 0.725 [0.589, 0.851] |
| Am+X@10 | met | 0.025 [0.000, 0.075] | 0.000 [0.000, 0.000] | - |
| Am@10 | met | 0.017 [0.000, 0.050] | 0.000 [0.000, 0.000] | - |

## PD (A_f; the recorder of maximum encounter steps)

| cell | cost-inclusive count (C) | status | censored runs | max end-state charge/play | max encounter steps | runs with a forfeit | forfeit weight |
|---|---|---|---|---|---|---|---|
| Af@0.1 | 37/40 = 0.925 [0.801, 0.974] | met | 15 | 0.00000 | 759079 | 0 | 0 |
| Af@1 | 39/40 = 0.975 [0.871, 0.996] | met | 18 | 0.00000 | 750021 | 0 | 0 |

## Deviations, crashes, retries, cuts

- **Code changes after the code commit (746d90a).** (1) `src/forfeit_pricing_batch.py` gained a `static` job (the nearby-budget check) between the L_T jobs and the PD jobs. (2) `src/forfeit_pricing_run.py` gained an `--ext first last` option and a `tag` argument (supplementary runs, files tagged `_ext`); the report module was written while the cells ran. No change to any code path that produced a registered cell after the first cell started (the `tag` default is empty).
- **Supplementary runs (not in the spec).** The run-level inspection statistic is nearly binary (run SD 0.37-0.46: the 64 islands with migration mostly end in one state), so 40 runs cannot resolve differences of 0.1-0.2 and the registered inspection statuses move between met and undetermined by dynamics-seed noise alone (A, A_f and A_m without X have identical tables yet differ by up to 0.15). Fresh run indices 340-419 were added for inspection: A_f without X, with X and with the sham at 0.1 and 1, and without X / with X at 0.03, 0.3 and 10 (12 cells x 80 runs), pooled with 300-339 in a separate section. The registered verdicts use the 40 runs only.
- **Extra cells** beyond the spec's list (disclosed in notes section 2): a concurrent A cell at 10, A_m + X in RPS at every level, A_m + X and A_m at 1 in inspection.
- **Shared tables in inspection.** The merged inspection catalogue has no forfeits, so inspection cells without X under A, A_f and A_m have identical tables; their differences are dynamics-seed noise (E8 failed: the noise floor is above 0.06; the classification pooled over the rules is reported beside the registered per-cell one).
- **PD under A_f** is the merged rule-A run with a read-only recorder (notes 2.7); no run recorded a forfeit (maximum encounter steps 759,079 against the budget 10^6); the PD statuses at 0.03, 0.3 and 10 are carried from the confirmation run. 15 (A_f 0.1) and 18 (A_f 1) of 40 runs had not frozen by generation 10,000 (censored); all kept, scored by the persistence rule.
- **Nearby budgets.** The hash programmes' actions differ across K because the exact simulator's term embeds K - 11 (a different quote, hence a different hash); every other pair has the same play law and failure events at K = 9,000, 10,000, 11,000.
- **No crash, retry or cut.** All registered cells ran to completion (RPS 29 cells, inspection 23, PD 2, static 3 budgets, 12 supplementary inspection cells); the batch driver recorded no retry. The cache digests (world-K) are identical before and after (`provenance_hashes.json`). At most 2 worker processes at a time (the encounter-contracts agent was alive throughout).
- **Clone.** The sham twins agree with their counterparts except against the hash programmes (a different spelling is a different quote); the sham therefore controls bookkeeping (class splitting), not the halving of the counterpart.
