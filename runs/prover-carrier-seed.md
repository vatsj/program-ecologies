# Prover-carrier seed at b = 0 (2026-10-05)

Spec `specs/2026-10-05-prover-carrier-seed.md`; predictions `predictions/2026-10-05-prover-carrier-seed.md` (with two
addenda committed before the seeded runs). Code: `src/prover_carrier_seed.py` (kernel = `contracts_abm._run` plus
transition counters and lineage tracking, RNG-identical), `src/prover_carrier_static.py`, `src/prover_carrier_report.py`,
`src/prover_carrier_pooled.py`. Rows: `runs/prover_carrier_seed_rows.json`; cell summaries and the static diagnostics:
`runs/prover-carrier-seed.json`, `runs/prover_carrier_static.json`; pooled statistics: `runs/prover-carrier-seed-pooled.txt`.
An invasion/establishment experiment at finite sizes; nothing here is π or a large-population efficiency claim.

**Deviations, all recorded before the runs they affect.** (1) Finite-ε window 2·10⁴ generations (second half
10⁴–2·10⁴), not 10⁵, because the lid was closed and workers got ~3% CPU; a 10⁵-generation check (mix, f₀ ∈ {0.01, 0.1},
σ ∈ {0, 1}, 3 seeds, the same populations as main reps 0–2) was run. (2) A b = 0, s = 0 finite-ε run stops when its
carriers go extinct: the rest is the no-contract b = 0 process (published 0.001–0.003); such runs count as failures.
(3) *Bug, fixed and rerun:* the first pass applied the extinction stop also to the b = ∞ control, where it is not valid
(sources are legible there). All 110 b = ∞ finite-ε rows were discarded and rerun without the stop; only the rerun is
reported. (4) N = 25,600 was cut to 3 seeds per σ in the addendum and restored to the spec's 5 once the machine woke.
(5) Lottery σ = 1 repeats every k ≥ 1 cell as a secondary check.

<!-- generated tables: src/prover_carrier_report.py -->
### Finite ε (10⁻³), b = 0 main grid and controls, N = 6,400 unless stated; 2·10⁴ generations except set long (10⁵)

Mean P(C,C) is over runs run to the end; runs stopped at carrier extinction (s = 0, the rest is the no-contract b = 0 process, published P(C,C) 0.001–0.003) count as failures and are listed under *extinct*.

| set | seed | b | ctl | N | f₀ | σ | success (P(C,C) ≥ 0.9) | mean P(C,C) [min, max] (full runs) | carriers | carrier P(C,C) | extinct | t₁₀ / t₅₀ med (max t₅₀) | growth₂₀₀ | lost-invalid / birth | accepted swaps (onto none) / birth | founders (med) | cross-lineage max |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ctl_inf | fb | inf | on | 6400 | 0.001 | 0 | 19/20 [0.76, 0.99] | 0.980 [0.831, 0.993] | 0.180 | 1.000 | 15 | 94.0 / 294.0 (1132) | -0.0124 | 1.8e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0.0 |
| ctl_inf | fb | inf | on | 6400 | 0.003 | 0 | 18/20 [0.70, 0.97] | 0.973 [0.801, 0.993] | 0.098 | 1.000 | 18 | 79.0 / 435.0 (1603) | -0.0182 | 1.1e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0 |
| ctl_inf | fb | inf | on | 6400 | 0.01 | 0 | 5/5 [0.57, 1.00] | 0.987 [0.980, 0.991] | 0.000 | – | 5 | None / None (None) | -0.0243 | 3.6e-08 | 0.0e+00 (0.0e+00) | None | 0 |
| ctl_inf | fb | inf | on | 6400 | 0.03 | 0 | 5/5 [0.57, 1.00] | 0.991 [0.988, 0.991] | 0.165 | 1.000 | 4 | 73.0 / 164.0 (925) | 0.0139 | 2.1e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0 |
| ctl_inf | fb | inf | on | 6400 | 0.1 | 0 | 5/5 [0.57, 1.00] | 0.990 [0.984, 0.992] | 0.570 | 1.000 | 1 | 1.0 / 35.0 (53) | 0.0100 | 6.1e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0.0 |
| ctl_inf | mix | inf | on | 6400 | 0.001 | 0 | 17/20 [0.64, 0.95] | 0.944 [0.546, 0.992] | 0.000 | – | 20 | 150.0 / 225.0 (301) | -0.0124 | 2.1e-06 | 0.0e+00 (0.0e+00) | None | 0 |
| ctl_inf | mix | inf | on | 6400 | 0.003 | 0 | 18/20 [0.70, 0.97] | 0.974 [0.814, 0.992] | 0.000 | – | 20 | 147.0 / 242.0 (1370) | -0.0182 | 2.7e-05 | 0.0e+00 (0.0e+00) | None | 0 |
| ctl_inf | mix | inf | on | 6400 | 0.01 | 0 | 5/5 [0.57, 1.00] | 0.990 [0.989, 0.992] | 0.403 | 1.000 | 2 | 83.5 / 110.0 (131) | 0.0217 | 4.1e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0 |
| ctl_inf | mix | inf | on | 6400 | 0.03 | 0 | 5/5 [0.57, 1.00] | 0.973 [0.903, 0.992] | 0.251 | 1.000 | 3 | 70.5 / 112.0 (124) | 0.0150 | 3.2e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0.0 |
| ctl_inf | mix | inf | on | 6400 | 0.1 | 0 | 5/5 [0.57, 1.00] | 0.987 [0.974, 0.991] | 0.272 | 1.000 | 3 | 1.0 / 29.0 (42) | 0.0103 | 3.1e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0.0 |
| ctl_mu | mu | 0 | on | 6400 | 0.01 | 0 | 0/5 [0.00, 0.43] | nan [nan, nan] | 0.000 | – | 5 | 185.5 / 1729.0 (1729) | 0.0095 | 1.9e-04 | 0.0e+00 (0.0e+00) | None | None |
| ctl_mu | mu | 0 | on | 6400 | 0.01 | 1 | 0/5 [0.00, 0.43] | 0.001 [0.000, 0.005] | 0.947 | – | 0 | 4.0 / 7.0 (7) | 0.0227 | 5.1e-04 | 6.0e-05 (6.0e-05) | None | None |
| ctl_off | fb | 0 | off | 6400 | 0.001 | 0 | 0/20 [0.00, 0.16] | 0.002 [0.000, 0.010] | 0.000 | – | 0 | None / None (None) | – | 0.0e+00 | 0.0e+00 (0.0e+00) | None | None |
| ctl_off | fb | 0 | off | 6400 | 0.003 | 0 | 0/20 [0.00, 0.16] | 0.002 [0.000, 0.008] | 0.000 | – | 0 | None / None (None) | – | 0.0e+00 | 0.0e+00 (0.0e+00) | None | None |
| ctl_off | fb | 0 | off | 6400 | 0.01 | 0 | 0/5 [0.00, 0.43] | 0.001 [0.000, 0.003] | 0.000 | – | 0 | None / None (None) | – | 0.0e+00 | 0.0e+00 (0.0e+00) | None | None |
| ctl_off | fb | 0 | off | 6400 | 0.03 | 0 | 0/5 [0.00, 0.43] | 0.002 [0.000, 0.006] | 0.000 | – | 0 | None / None (None) | – | 0.0e+00 | 0.0e+00 (0.0e+00) | None | None |
| ctl_off | fb | 0 | off | 6400 | 0.1 | 0 | 0/5 [0.00, 0.43] | 0.003 [0.002, 0.005] | 0.000 | – | 0 | None / None (None) | – | 0.0e+00 | 0.0e+00 (0.0e+00) | None | None |
| ctl_off | mix | 0 | off | 6400 | 0.001 | 0 | 0/20 [0.00, 0.16] | 0.002 [0.000, 0.008] | 0.000 | – | 0 | None / None (None) | – | 0.0e+00 | 0.0e+00 (0.0e+00) | None | None |
| ctl_off | mix | 0 | off | 6400 | 0.003 | 0 | 0/20 [0.00, 0.16] | 0.001 [0.000, 0.003] | 0.000 | – | 0 | None / None (None) | – | 0.0e+00 | 0.0e+00 (0.0e+00) | None | None |
| ctl_off | mix | 0 | off | 6400 | 0.01 | 0 | 0/5 [0.00, 0.43] | 0.001 [0.000, 0.005] | 0.000 | – | 0 | None / None (None) | – | 0.0e+00 | 0.0e+00 (0.0e+00) | None | None |
| ctl_off | mix | 0 | off | 6400 | 0.03 | 0 | 0/5 [0.00, 0.43] | 0.003 [0.000, 0.004] | 0.000 | – | 0 | None / None (None) | – | 0.0e+00 | 0.0e+00 (0.0e+00) | None | None |
| ctl_off | mix | 0 | off | 6400 | 0.1 | 0 | 0/5 [0.00, 0.43] | 0.001 [0.000, 0.004] | 0.000 | – | 0 | None / None (None) | – | 0.0e+00 | 0.0e+00 (0.0e+00) | None | None |
| long | mix | 0 | on | 6400 | 0.01 | 0 | 3/3 [0.44, 1.00] | 0.989 [0.989, 0.989] | 0.718 | 1.000 | 0 | 121.0 / 152.0 (177) | 0.0229 | 7.2e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0.0 |
| long | mix | 0 | on | 6400 | 0.01 | 1 | 0/3 [0.00, 0.56] | nan [nan, nan] | 0.000 | – | 3 | None / None (None) | – | 7.6e-06 | 2.9e-05 (2.9e-05) | None | None |
| long | mix | 0 | on | 6400 | 0.1 | 0 | 3/3 [0.44, 1.00] | 0.989 [0.989, 0.989] | 0.721 | 1.000 | 0 | 1.0 / 34.0 (38) | 0.0113 | 7.2e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0.0 |
| long | mix | 0 | on | 6400 | 0.1 | 1 | 3/3 [0.44, 1.00] | 0.989 [0.988, 0.990] | 0.721 | 1.000 | 0 | 2.0 / 30.0 (35) | 0.0113 | 7.2e-04 | 1.2e-06 (1.2e-06) | 1.0 | 1.0 |
| main | fb | 0 | on | 6400 | 0.001 | 0 | 3/20 [0.05, 0.36] | 0.988 [0.986, 0.991] | 0.107 | 1.000 | 17 | 123.0 / 158.0 (215) | 0.0348 | 7.2e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0.0 |
| main | fb | 0 | on | 6400 | 0.001 | 1 | 0/20 [0.00, 0.16] | nan [nan, nan] | 0.000 | – | 20 | None / None (None) | 0.0058 | 6.4e-06 | 4.5e-05 (4.5e-05) | None | None |
| main | fb | 0 | on | 6400 | 0.003 | 0 | 5/20 [0.11, 0.47] | 0.990 [0.988, 0.991] | 0.182 | 1.000 | 15 | 126.0 / 161.0 (255) | 0.0285 | 7.2e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0.0 |
| main | fb | 0 | on | 6400 | 0.003 | 1 | 5/20 [0.11, 0.47] | 0.988 [0.985, 0.991] | 0.175 | 1.000 | 15 | 96.0 / 126.0 (357) | 0.0289 | 7.0e-04 | 1.6e-06 (1.6e-06) | 1.0 | 0.0 |
| main | fb | 0 | on | 6400 | 0.01 | 0 | 3/5 [0.23, 0.88] | 0.989 [0.988, 0.991] | 0.430 | 1.000 | 2 | 99.0 / 130.0 (155) | 0.0229 | 7.2e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0.0 |
| main | fb | 0 | on | 6400 | 0.01 | 1 | 2/5 [0.12, 0.77] | 0.990 [0.988, 0.991] | 0.296 | 1.000 | 3 | 103.5 / 139.0 (160) | 0.0229 | 7.1e-04 | 1.6e-06 (1.6e-06) | 1.0 | 0.0 |
| main | fb | 0 | on | 6400 | 0.03 | 0 | 4/5 [0.38, 0.96] | 0.990 [0.989, 0.990] | 0.581 | 1.000 | 1 | 71.5 / 103.0 (134) | 0.0173 | 7.2e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0.0 |
| main | fb | 0 | on | 6400 | 0.03 | 1 | 5/5 [0.57, 1.00] | 0.990 [0.989, 0.991] | 0.730 | 1.000 | 0 | 59.0 / 101.0 (140) | 0.0174 | 7.2e-04 | 1.4e-06 (1.4e-06) | 1.0 | 0.0 |
| main | fb | 0 | on | 6400 | 0.1 | 0 | 5/5 [0.57, 1.00] | 0.990 [0.988, 0.991] | 0.730 | 1.000 | 0 | 1.0 / 34.0 (69) | 0.0112 | 7.3e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0.0 |
| main | fb | 0 | on | 6400 | 0.1 | 1 | 5/5 [0.57, 1.00] | 0.989 [0.985, 0.991] | 0.721 | 1.000 | 0 | 1.0 / 36.0 (40) | 0.0110 | 7.2e-04 | 1.6e-06 (1.6e-06) | 1.0 | 0.0 |
| main | mix | 0 | on | 6400 | 0.001 | 0 | 0/20 [0.00, 0.16] | 0.001 [0.000, 0.004] | 0.000 | – | 20 | None / None (None) | -0.0124 | 4.2e-08 | 0.0e+00 (0.0e+00) | None | None |
| main | mix | 0 | on | 6400 | 0.001 | 1 | 0/20 [0.00, 0.16] | nan [nan, nan] | 0.000 | – | 20 | None / None (None) | – | 7.7e-07 | 2.3e-06 (2.3e-06) | None | None |
| main | mix | 0 | on | 6400 | 0.003 | 0 | 4/20 [0.08, 0.42] | 0.989 [0.987, 0.991] | 0.144 | 1.000 | 16 | 161.0 / 197.0 (266) | 0.0254 | 7.1e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0.0 |
| main | mix | 0 | on | 6400 | 0.003 | 1 | 4/20 [0.08, 0.42] | 0.989 [0.988, 0.991] | 0.142 | 1.000 | 16 | 119.5 / 146.5 (202) | 0.0290 | 7.0e-04 | 1.6e-06 (1.6e-06) | 1.0 | 1.0 |
| main | mix | 0 | on | 6400 | 0.01 | 0 | 3/5 [0.23, 0.88] | 0.990 [0.989, 0.991] | 0.437 | 1.000 | 2 | 121.0 / 152.0 (177) | 0.0229 | 7.2e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0.0 |
| main | mix | 0 | on | 6400 | 0.01 | 1 | 2/5 [0.12, 0.77] | 0.988 [0.988, 0.988] | 0.281 | 1.000 | 3 | 54.0 / 81.5 (91) | 0.0227 | 7.1e-04 | 1.8e-06 (1.8e-06) | 1.0 | 0.0 |
| main | mix | 0 | on | 6400 | 0.03 | 0 | 3/5 [0.23, 0.88] | 0.990 [0.988, 0.991] | 0.446 | 1.000 | 2 | 139.0 / 179.0 (184) | 0.0174 | 7.2e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0.0 |
| main | mix | 0 | on | 6400 | 0.03 | 1 | 5/5 [0.57, 1.00] | 0.989 [0.987, 0.990] | 0.715 | 1.000 | 0 | 78.0 / 118.0 (213) | 0.0171 | 7.1e-04 | 2.1e-06 (2.1e-06) | 1.0 | 1.0 |
| main | mix | 0 | on | 6400 | 0.1 | 0 | 5/5 [0.57, 1.00] | 0.989 [0.987, 0.992] | 0.714 | 1.000 | 0 | 1.0 / 29.0 (38) | 0.0112 | 7.2e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0.0 |
| main | mix | 0 | on | 6400 | 0.1 | 1 | 5/5 [0.57, 1.00] | 0.989 [0.987, 0.991] | 0.714 | 1.000 | 0 | 2.0 / 35.0 (57) | 0.0113 | 7.1e-04 | 2.0e-06 (2.0e-06) | 1.0 | 1.0 |
| nsweep | mix | 0 | on | 1600 | 0.01 | 0 | 1/5 [0.04, 0.62] | 0.988 [0.988, 0.988] | 0.164 | 1.000 | 4 | 175.0 / 226.0 (226) | 0.0114 | 7.8e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0.0 |
| nsweep | mix | 0 | on | 25600 | 0.01 | 0 | 1/5 [0.04, 0.62] | 0.990 [0.990, 0.990] | 0.137 | 1.000 | 4 | 200.0 / 233.0 (233) | 0.0018 | 6.6e-04 | 0.0e+00 (0.0e+00) | 1.0 | 0.0 |
| nsweep | mix | 0 | on | 1600 | 0.01 | 1 | 1/5 [0.04, 0.62] | 0.985 [0.985, 0.985] | 0.154 | 1.000 | 4 | 102.0 / 134.0 (134) | 0.0230 | 7.7e-04 | 1.7e-06 (1.7e-06) | 1.0 | 0.0 |
| nsweep | mix | 0 | on | 25600 | 0.01 | 1 | 5/5 [0.57, 1.00] | 0.990 [0.989, 0.990] | 0.687 | 1.000 | 0 | 161.0 / 194.0 (657) | 0.0216 | 6.8e-04 | 2.8e-06 (2.8e-06) | 1.0 | 0.801259156123252 |

### ε = 0 twins (well-mixed, I = 1, run to the freeze)

| set | seed | b | ctl | N | I | f₀ / k | σ | efficient | outcomes | status | stop gen med (max) | carriers extinct | founders (med, eff.) | accepted onto none / birth |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| nsweep_twins | mix | 0 | on | 1600 | 1 | 0.01 | 0 | 3/20 [0.05, 0.36] | defecting 17, efficient 3 | frozen 20 | 35.0 (180) | 17 | 1.0 | 0.0e+00 |
| nsweep_twins | mix | 0 | on | 25600 | 1 | 0.01 | 0 | 19/20 [0.76, 0.99] | defecting 1, efficient 19 | frozen 20 | 237.5 (595) | 1 | 3.0 | 0.0e+00 |
| twins | fb | 0 | on | 6400 | 1 | 0.001 | 0 | 3/20 [0.05, 0.36] | defecting 17, efficient 3 | frozen 20 | 52.5 (200) | 17 | 2.0 | 0.0e+00 |
| twins | fb | 0 | on | 6400 | 1 | 0.001 | 1 | 0/20 [0.00, 0.16] | defecting 20, efficient 0 | frozen 20 | 42.5 (130) | 20 | None | 8.6e-07 |
| twins | fb | 0 | on | 6400 | 1 | 0.003 | 0 | 4/20 [0.08, 0.42] | defecting 16, efficient 4 | frozen 20 | 90.0 (365) | 16 | 1.5 | 0.0e+00 |
| twins | fb | 0 | on | 6400 | 1 | 0.003 | 1 | 5/20 [0.11, 0.47] | defecting 15, efficient 5 | frozen 20 | 55.0 (350) | 15 | 1.0 | 1.6e-05 |
| twins | fb | 0 | on | 6400 | 1 | 0.01 | 0 | 11/20 [0.34, 0.74] | defecting 9, efficient 11 | frozen 20 | 135.0 (235) | 9 | 1.0 | 0.0e+00 |
| twins | fb | 0 | on | 6400 | 1 | 0.01 | 1 | 13/20 [0.43, 0.82] | defecting 7, efficient 13 | frozen 20 | 142.5 (380) | 7 | 2.0 | 4.7e-05 |
| twins | fb | 0 | on | 6400 | 1 | 0.03 | 0 | 17/20 [0.64, 0.95] | defecting 3, efficient 17 | frozen 20 | 132.5 (235) | 3 | 4.0 | 0.0e+00 |
| twins | fb | 0 | on | 6400 | 1 | 0.03 | 1 | 18/20 [0.70, 0.97] | defecting 2, efficient 18 | frozen 20 | 112.5 (395) | 2 | 5.5 | 3.8e-05 |
| twins | fb | 0 | on | 6400 | 1 | 0.1 | 0 | 20/20 [0.84, 1.00] | efficient 20 | frozen 20 | 75.0 (95) | 0 | 21.5 | 0.0e+00 |
| twins | fb | 0 | on | 6400 | 1 | 0.1 | 1 | 20/20 [0.84, 1.00] | efficient 20 | frozen 20 | 75.0 (85) | 0 | 22.0 | 6.0e-05 |
| twins | mix | 0 | on | 6400 | 1 | 0.001 | 0 | 1/20 [0.01, 0.24] | defecting 19, efficient 1 | frozen 20 | 52.5 (295) | 19 | 1.0 | 0.0e+00 |
| twins | mix | 0 | on | 6400 | 1 | 0.001 | 1 | 2/20 [0.03, 0.30] | defecting 18, efficient 2 | frozen 20 | 57.5 (330) | 18 | 1.0 | 2.2e-05 |
| twins | mix | 0 | on | 6400 | 1 | 0.003 | 0 | 3/20 [0.05, 0.36] | defecting 17, efficient 3 | frozen 20 | 75.0 (235) | 17 | 1.0 | 0.0e+00 |
| twins | mix | 0 | on | 6400 | 1 | 0.003 | 1 | 0/20 [0.00, 0.16] | defecting 20, efficient 0 | frozen 20 | 52.5 (205) | 20 | None | 5.2e-06 |
| twins | mix | 0 | on | 6400 | 1 | 0.01 | 0 | 14/20 [0.48, 0.85] | defecting 6, efficient 14 | frozen 20 | 160.0 (310) | 6 | 2.0 | 0.0e+00 |
| twins | mix | 0 | on | 6400 | 1 | 0.01 | 1 | 14/20 [0.48, 0.85] | defecting 6, efficient 14 | frozen 20 | 140.0 (260) | 6 | 3.0 | 6.4e-05 |
| twins | mix | 0 | on | 6400 | 1 | 0.03 | 0 | 19/20 [0.76, 0.99] | defecting 1, efficient 19 | frozen 20 | 125.0 (240) | 1 | 4.0 | 0.0e+00 |
| twins | mix | 0 | on | 6400 | 1 | 0.03 | 1 | 18/20 [0.70, 0.97] | defecting 2, efficient 18 | frozen 20 | 117.5 (170) | 2 | 6.0 | 1.2e-04 |
| twins | mix | 0 | on | 6400 | 1 | 0.1 | 0 | 20/20 [0.84, 1.00] | efficient 20 | frozen 20 | 65.0 (85) | 0 | 28.0 | 0.0e+00 |
| twins | mix | 0 | on | 6400 | 1 | 0.1 | 1 | 20/20 [0.84, 1.00] | efficient 20 | frozen 20 | 72.5 (135) | 0 | 26.0 | 1.2e-04 |
| twins_ctl | fb | 0 | off | 6400 | 1 | 0.001 | 0 | 0/20 [0.00, 0.16] | defecting 20, efficient 0 | frozen 20 | 42.5 (115) | 0 | None | 0.0e+00 |
| twins_ctl | fb | 0 | off | 6400 | 1 | 0.003 | 0 | 0/20 [0.00, 0.16] | defecting 20, efficient 0 | frozen 20 | 57.5 (195) | 0 | None | 0.0e+00 |
| twins_ctl | fb | 0 | off | 6400 | 1 | 0.01 | 0 | 0/20 [0.00, 0.16] | defecting 20, efficient 0 | frozen 20 | 40.0 (260) | 0 | None | 0.0e+00 |
| twins_ctl | fb | 0 | off | 6400 | 1 | 0.03 | 0 | 0/20 [0.00, 0.16] | defecting 20, efficient 0 | frozen 20 | 45.0 (75) | 0 | None | 0.0e+00 |
| twins_ctl | fb | 0 | off | 6400 | 1 | 0.1 | 0 | 0/20 [0.00, 0.16] | defecting 20, efficient 0 | frozen 20 | 40.0 (145) | 0 | None | 0.0e+00 |
| twins_ctl | fb | inf | on | 6400 | 1 | 0.001 | 0 | 13/20 [0.43, 0.82] | defecting 7, efficient 13 | frozen 20 | 130.0 (260) | 18 | 1.5 | 0.0e+00 |
| twins_ctl | fb | inf | on | 6400 | 1 | 0.003 | 0 | 15/20 [0.53, 0.89] | defecting 5, efficient 15 | frozen 20 | 137.5 (250) | 14 | 1.0 | 0.0e+00 |
| twins_ctl | fb | inf | on | 6400 | 1 | 0.01 | 0 | 14/20 [0.48, 0.85] | defecting 6, efficient 14 | frozen 20 | 142.5 (245) | 11 | 2.0 | 0.0e+00 |
| twins_ctl | fb | inf | on | 6400 | 1 | 0.03 | 0 | 20/20 [0.84, 1.00] | efficient 20 | frozen 20 | 112.5 (270) | 0 | 4.5 | 0.0e+00 |
| twins_ctl | fb | inf | on | 6400 | 1 | 0.1 | 0 | 20/20 [0.84, 1.00] | efficient 20 | frozen 20 | 70.0 (175) | 0 | 23.5 | 0.0e+00 |
| twins_ctl | mix | 0 | off | 6400 | 1 | 0.001 | 0 | 0/20 [0.00, 0.16] | defecting 20, efficient 0 | frozen 20 | 45.0 (265) | 0 | None | 0.0e+00 |
| twins_ctl | mix | 0 | off | 6400 | 1 | 0.003 | 0 | 0/20 [0.00, 0.16] | defecting 20, efficient 0 | frozen 20 | 60.0 (265) | 0 | None | 0.0e+00 |
| twins_ctl | mix | 0 | off | 6400 | 1 | 0.01 | 0 | 0/20 [0.00, 0.16] | defecting 20, efficient 0 | frozen 20 | 35.0 (110) | 0 | None | 0.0e+00 |
| twins_ctl | mix | 0 | off | 6400 | 1 | 0.03 | 0 | 0/20 [0.00, 0.16] | defecting 20, efficient 0 | frozen 20 | 45.0 (310) | 0 | None | 0.0e+00 |
| twins_ctl | mix | 0 | off | 6400 | 1 | 0.1 | 0 | 0/20 [0.00, 0.16] | defecting 20, efficient 0 | frozen 20 | 50.0 (105) | 0 | None | 0.0e+00 |
| twins_ctl | mix | inf | on | 6400 | 1 | 0.001 | 0 | 18/20 [0.70, 0.97] | defecting 2, efficient 18 | frozen 20 | 155.0 (340) | 18 | 1.0 | 0.0e+00 |
| twins_ctl | mix | inf | on | 6400 | 1 | 0.003 | 0 | 16/20 [0.58, 0.92] | defecting 4, efficient 16 | frozen 20 | 167.5 (370) | 17 | 1.0 | 0.0e+00 |
| twins_ctl | mix | inf | on | 6400 | 1 | 0.01 | 0 | 16/20 [0.58, 0.92] | defecting 4, efficient 16 | frozen 20 | 147.5 (295) | 8 | 1.0 | 0.0e+00 |
| twins_ctl | mix | inf | on | 6400 | 1 | 0.03 | 0 | 19/20 [0.76, 0.99] | defecting 1, efficient 19 | frozen 20 | 105.0 (255) | 1 | 5.0 | 0.0e+00 |
| twins_ctl | mix | inf | on | 6400 | 1 | 0.1 | 0 | 20/20 [0.84, 1.00] | efficient 20 | frozen 20 | 65.0 (100) | 0 | 24.5 | 0.0e+00 |

### ε = 0 lottery on islands (mN = 1)

| set | seed | b | ctl | N | I | f₀ / k | σ | efficient | outcomes | status | stop gen med (max) | carriers extinct | founders (med, eff.) | accepted onto none / birth |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lottery | mix | 0 | on | 100 | 4 | k=0 | 0 | 0/40 [0.00, 0.09] | defecting 40, efficient 0 | frozen 40 | 25.0 (100) | 0 | None | 0.0e+00 |
| lottery | mix | 0 | on | 100 | 64 | k=0 | 0 | 5/40 [0.05, 0.26] | defecting 35, efficient 5 | frozen 40 | 215.0 (425) | 0 | None | 0.0e+00 |
| lottery | mix | 0 | on | 100 | 4 | k=1 | 0 | 12/40 [0.18, 0.45] | defecting 28, efficient 12 | frozen 40 | 30.0 (180) | 31 | 1.0 | 0.0e+00 |
| lottery | mix | 0 | on | 100 | 64 | k=1 | 0 | 37/40 [0.80, 0.97] | defecting 3, efficient 37 | frozen 40 | 260.0 (450) | 4 | 3.0 | 0.0e+00 |
| lottery | mix | 0 | on | 100 | 4 | k=1 | 1 | 9/40 [0.12, 0.38] | defecting 31, efficient 9 | frozen 40 | 25.0 (165) | 35 | 1.0 | 2.9e-05 |
| lottery | mix | 0 | on | 100 | 64 | k=1 | 1 | 38/40 [0.83, 0.99] | defecting 2, efficient 38 | frozen 40 | 260.0 (44790) | 3 | 3.0 | 4.5e-06 |
| lottery | mix | 0 | on | 100 | 4 | k=3 | 0 | 14/40 [0.22, 0.50] | defecting 26, efficient 14 | frozen 40 | 35.0 (210) | 26 | 1.0 | 0.0e+00 |
| lottery | mix | 0 | on | 100 | 64 | k=3 | 0 | 40/40 [0.91, 1.00] | efficient 40 | frozen 40 | 230.0 (290) | 0 | 7.5 | 0.0e+00 |
| lottery | mix | 0 | on | 100 | 4 | k=3 | 1 | 24/40 [0.45, 0.74] | defecting 16, efficient 24 | frozen 40 | 87.5 (215) | 18 | 1.0 | 2.1e-05 |
| lottery | mix | 0 | on | 100 | 64 | k=3 | 1 | 40/40 [0.91, 1.00] | efficient 40 | frozen 40 | 232.5 (325) | 0 | 8.0 | 2.3e-05 |
| lottery | mix | 0 | on | 100 | 4 | k=16 | 0 | 38/40 [0.83, 0.99] | defecting 2, efficient 38 | frozen 40 | 85.0 (200) | 2 | 3.0 | 0.0e+00 |
| lottery | mix | 0 | on | 100 | 4 | k=16 | 1 | 34/40 [0.71, 0.93] | defecting 6, efficient 34 | frozen 40 | 85.0 (205) | 6 | 2.0 | 4.6e-05 |

### Composition (main grid, mean second-half shares)

- main fb f₀ = 0.001 σ = 0 N = 6400: contracts `<BOX(THEM(ME))>` 1.00; sources `BOX(THEM(ME))` 0.71, `C` 0.28, `D` 0.01, `BOXD1(THEM(ME))` 0.00; FairBot-contract share 1.000; source-ALLC load 0.284; P(C,C) by seed ['ext@18', 'ext@65', 'ext@93', 'ext@4', 'ext@5', 0.986, 'ext@13', 'ext@82', 'ext@9', 'ext@15', 'ext@11', 'ext@4', 'ext@36', 'ext@8', 'ext@4', 'ext@3', 'ext@4', 'ext@27', 0.987, 0.991]
- main fb f₀ = 0.001 σ = 1 N = 6400: contracts ; sources ; FairBot-contract share 0.000; source-ALLC load 0.000; P(C,C) by seed ['ext@42', 'ext@209', 'ext@60', 'ext@3', 'ext@8', 'ext@11', 'ext@10', 'ext@71', 'ext@184', 'ext@32', 'ext@8', 'ext@13', 'ext@11', 'ext@5', 'ext@8', 'ext@6', 'ext@11', 'ext@5', 'ext@6', 'ext@4']
- main fb f₀ = 0.003 σ = 0 N = 6400: contracts `<BOX(THEM(ME))>` 1.00; sources `BOX(THEM(ME))` 0.73, `C` 0.27, `D` 0.00, `BOXD(THEM(ME))` 0.00; FairBot-contract share 1.000; source-ALLC load 0.267; P(C,C) by seed ['ext@13', 'ext@19', 'ext@114', 'ext@60', 'ext@12', 'ext@16', 'ext@6', 'ext@15', 'ext@34', 0.99, 'ext@30', 'ext@36', 'ext@66', 0.991, 'ext@10', 0.988, 'ext@109', 'ext@12', 0.99, 0.99]
- main fb f₀ = 0.003 σ = 1 N = 6400: contracts `<BOX(THEM(ME))>` 1.00; sources `BOX(THEM(ME))` 0.70, `C` 0.30, `D` 0.01, `BOXD1(THEM(ME))` 0.00; FairBot-contract share 1.000; source-ALLC load 0.297; P(C,C) by seed ['ext@32', 'ext@38', 'ext@174', 'ext@10', 'ext@103', 0.99, 'ext@29', 'ext@57', 'ext@9', 'ext@76', 'ext@13', 'ext@86', 'ext@21', 'ext@14', 'ext@50', 0.991, 'ext@14', 0.986, 0.987, 0.985]
- main fb f₀ = 0.01 σ = 0 N = 6400: contracts `<BOX(THEM(ME))>` 1.00; sources `BOX(THEM(ME))` 0.72, `C` 0.28, `D` 0.01, `BOXD(THEM(THEM))` 0.00; FairBot-contract share 1.000; source-ALLC load 0.279; P(C,C) by seed [0.988, 'ext@122', 'ext@98', 0.991, 0.989]
- main fb f₀ = 0.01 σ = 1 N = 6400: contracts `<BOX(THEM(ME))>` 1.00; sources `BOX(THEM(ME))` 0.74, `C` 0.26, `D` 0.00, `BOXD1(THEM(THEM))` 0.00; FairBot-contract share 1.000; source-ALLC load 0.257; P(C,C) by seed ['ext@116', 'ext@41', 'ext@75', 0.988, 0.991]
- main fb f₀ = 0.03 σ = 0 N = 6400: contracts `<BOX(THEM(ME))>` 1.00; sources `BOX(THEM(ME))` 0.73, `C` 0.27, `D` 0.00, `BOXD(THEM(ME))` 0.00; FairBot-contract share 1.000; source-ALLC load 0.270; P(C,C) by seed ['ext@98', 0.99, 0.99, 0.989, 0.99]
- main fb f₀ = 0.03 σ = 1 N = 6400: contracts `<BOX(THEM(ME))>` 1.00; sources `BOX(THEM(ME))` 0.73, `C` 0.26, `D` 0.00, `BOXD(THEM(ME))` 0.00; FairBot-contract share 1.000; source-ALLC load 0.266; P(C,C) by seed [0.989, 0.989, 0.99, 0.991, 0.991]
- main fb f₀ = 0.1 σ = 0 N = 6400: contracts `<BOX(THEM(ME))>` 1.00; sources `BOX(THEM(ME))` 0.73, `C` 0.26, `D` 0.00, `BOXD1(THEM(THEM))` 0.00; FairBot-contract share 1.000; source-ALLC load 0.266; P(C,C) by seed [0.99, 0.99, 0.989, 0.991, 0.988]
- main fb f₀ = 0.1 σ = 1 N = 6400: contracts `<BOX(THEM(ME))>` 1.00; sources `BOX(THEM(ME))` 0.72, `C` 0.27, `D` 0.01, `BOXD(THEM(ME))` 0.00; FairBot-contract share 1.000; source-ALLC load 0.275; P(C,C) by seed [0.989, 0.985, 0.99, 0.991, 0.987]
- main mix f₀ = 0.001 σ = 0 N = 6400: contracts ; sources `D` 0.96, `BOX(THEM(THEM))` 0.01, `BOX(THEM(ME))` 0.01, `BOX1(THEM(THEM))` 0.01; FairBot-contract share 0.000; source-ALLC load 0.897; P(C,C) by seed [0.0, 0.0, 0.004, 0.0, 0.001, 0.003, 'ext@9', 'ext@2', 'ext@28', 'ext@9', 'ext@2', 'ext@3', 'ext@15', 'ext@40', 'ext@14', 'ext@4', 'ext@5', 'ext@2', 'ext@66', 'ext@256']
- main mix f₀ = 0.001 σ = 1 N = 6400: contracts ; sources ; FairBot-contract share 0.000; source-ALLC load 0.000; P(C,C) by seed ['ext@4', 'ext@5', 'ext@14', 'ext@5', 'ext@8', 'ext@12', 'ext@5', 'ext@6', 'ext@10', 'ext@2', 'ext@6', 'ext@3', 'ext@4', 'ext@7', 'ext@24', 'ext@60', 'ext@8', 'ext@3', 'ext@4', 'ext@14']
- main mix f₀ = 0.003 σ = 0 N = 6400: contracts `<BOX1(THEM(THEM))>` 0.75, `<BOX(THEM(^C))>` 0.25; sources `BOX1(THEM(THEM))` 0.54, `C` 0.28, `BOX(THEM(^C))` 0.18, `D` 0.01; FairBot-contract share 0.000; source-ALLC load 0.277; P(C,C) by seed ['ext@11', 'ext@35', 'ext@21', 'ext@50', 0.987, 'ext@80', 'ext@29', 'ext@8', 0.991, 'ext@29', 'ext@18', 0.988, 'ext@10', 'ext@64', 'ext@16', 'ext@85', 'ext@20', 'ext@50', 'ext@21', 0.99]
- main mix f₀ = 0.003 σ = 1 N = 6400: contracts `<BOX1(THEM(ME))>` 0.50, `<BOX(THEM(THEM))>` 0.25, `<BOX(THEM(ME))>` 0.25; sources `BOX1(THEM(ME))` 0.36, `C` 0.28, `BOX(THEM(THEM))` 0.18, `BOX(THEM(ME))` 0.17; FairBot-contract share 0.250; source-ALLC load 0.287; P(C,C) by seed ['ext@10', 'ext@108', 'ext@70', 'ext@85', 'ext@29', 'ext@46', 'ext@27', 'ext@8', 'ext@5', 0.988, 'ext@165', 0.991, 'ext@59', 'ext@9', 'ext@45', 'ext@14', 'ext@26', 'ext@55', 0.989, 0.988]
- main mix f₀ = 0.01 σ = 0 N = 6400: contracts `<BOX1(THEM(ME))>` 0.33, `<BOX(THEM(ME))>` 0.33, `<BOX(THEM(THEM))>` 0.33; sources `C` 0.27, `BOX(THEM(THEM))` 0.25, `BOX(THEM(ME))` 0.24, `BOX1(THEM(ME))` 0.24; FairBot-contract share 0.333; source-ALLC load 0.268; P(C,C) by seed [0.989, 0.99, 'ext@191', 'ext@14', 0.991]
- main mix f₀ = 0.01 σ = 1 N = 6400: contracts `<BOX(THEM(ME))>` 1.00; sources `BOX(THEM(ME))` 0.70, `C` 0.29, `D` 0.01, `BOXD(THEM(THEM))` 0.00; FairBot-contract share 1.000; source-ALLC load 0.294; P(C,C) by seed ['ext@79', 'ext@72', 'ext@35', 0.988, 0.988]
- main mix f₀ = 0.03 σ = 0 N = 6400: contracts `<BOX(THEM(THEM))>` 0.67, `<BOX1(THEM(ME))>` 0.33; sources `BOX(THEM(THEM))` 0.50, `C` 0.25, `BOX1(THEM(ME))` 0.24, `D` 0.00; FairBot-contract share 0.000; source-ALLC load 0.254; P(C,C) by seed [0.989, 0.988, 'ext@134', 'ext@62', 0.991]
- main mix f₀ = 0.03 σ = 1 N = 6400: contracts `<BOX(THEM(ME))>` 0.20, `<BOX1(THEM(THEM))>` 0.20, `<BOX1(THEM(ME))>` 0.20; sources `C` 0.28, `BOX(THEM(ME))` 0.15, `BOX1(THEM(THEM))` 0.14, `BOX1(THEM(ME))` 0.14; FairBot-contract share 0.200; source-ALLC load 0.281; P(C,C) by seed [0.99, 0.989, 0.987, 0.988, 0.989]
- main mix f₀ = 0.1 σ = 0 N = 6400: contracts `<BOX1(THEM(ME))>` 0.60, `<BOX(THEM(ME))>` 0.20, `<BOX1(THEM(THEM))>` 0.19; sources `BOX1(THEM(ME))` 0.42, `C` 0.28, `BOX(THEM(ME))` 0.15, `BOX1(THEM(THEM))` 0.13; FairBot-contract share 0.200; source-ALLC load 0.282; P(C,C) by seed [0.988, 0.989, 0.992, 0.99, 0.987]
- main mix f₀ = 0.1 σ = 1 N = 6400: contracts `<BOX1(THEM(THEM))>` 0.60, `<BOX(THEM(^C))>` 0.20, `<BOX(THEM(THEM))>` 0.20; sources `BOX1(THEM(THEM))` 0.42, `C` 0.28, `BOX(THEM(^C))` 0.15, `BOX(THEM(THEM))` 0.14; FairBot-contract share 0.000; source-ALLC load 0.282; P(C,C) by seed [0.991, 0.99, 0.988, 0.99, 0.987]
- nsweep mix f₀ = 0.01 σ = 0 N = 1600: contracts `<BOX1(THEM(ME))>` 1.00; sources `BOX1(THEM(ME))` 0.82, `C` 0.17, `D` 0.01, `BOXD1(THEM(THEM))` 0.00; FairBot-contract share 0.000; source-ALLC load 0.177; P(C,C) by seed ['ext@41', 'ext@38', 'ext@9', 'ext@8', 0.988]
- nsweep mix f₀ = 0.01 σ = 0 N = 25600: contracts `<BOX(THEM(ME))>` 1.00, `<BOX(THEM(THEM))>` 0.00; sources `BOX(THEM(ME))` 0.68, `C` 0.31, `D` 0.00, `BOX(THEM(THEM))` 0.00; FairBot-contract share 0.996; source-ALLC load 0.310; P(C,C) by seed ['ext@127', 'ext@325', 'ext@131', 'ext@90', 0.99]
- nsweep mix f₀ = 0.01 σ = 1 N = 1600: contracts `<BOX(THEM(ME))>` 1.00; sources `BOX(THEM(ME))` 0.77, `C` 0.22, `D` 0.01, `BOXD(THEM(THEM))` 0.00; FairBot-contract share 1.000; source-ALLC load 0.226; P(C,C) by seed ['ext@4', 'ext@16', 'ext@9', 'ext@14', 0.985]
- nsweep mix f₀ = 0.01 σ = 1 N = 25600: contracts `<BOX1(THEM(^C))>` 0.31, `<BOX1(THEM(ME))>` 0.20, `<BOX(THEM(THEM))>` 0.20; sources `C` 0.31, `BOX1(THEM(^C))` 0.21, `BOX1(THEM(ME))` 0.14, `BOX1(THEM(THEM))` 0.14; FairBot-contract share 0.085; source-ALLC load 0.310; P(C,C) by seed [0.99, 0.99, 0.99, 0.989, 0.99]

<!-- end generated -->

## Static invasion diagnostics (`runs/prover_carrier_static.json`)

- Establishers at n = 8: 118 sources, 96 classes, μ 0.0242; FairBot, `BOX1(THEM(ME))`, `BOX(THEM(THEM))`,
  `BOX1(THEM(THEM))` 0.21 of the seed each. As carriers they mutually cooperate with μ-weighted P(C,C) 0.963 inside the
  mixture; the misses are mostly prover × `not(BOXD(THEM(^C)))`. PrudentBot's carrier cooperates only with
  FairBot/`BOX(THEM(THEM))` carriers and itself; P*'s only with itself.
- Against the non-carrier background at b = 0 every main carrier gets R from ALLC, P from D, P from (illegible) non-carrier
  provers, and T from a *sucker fringe*: non-carrier programs whose literal or THEM(THEM) atoms are answered by the
  carrier's contract (so they cooperate with carriers) while the carrier, unable to read their source, defects
  (`BOX(THEM(THEM))`, `BOX1(THEM(THEM))`, `BOX(THEM(^C))`, `BOXD1(THEM(^D))`, …; μ mass 0.024 for FairBot's carrier).
  Nothing in the background exploits a FairBot carrier.
- Moran-replicator growth of a rare carrier (frequency 10⁻³) per generation: **μ background −0.006 (mix), −0.005
  (FairBot)**, positive only for 6 rare ALLC-exploiting types (PrudentBot and P\* families, 0.06% of the seed);
  **after ALLC's extinction (the non-carrier flow drops ALLC below 10⁻³ at generation 24): +0.010 (mix and FairBot)**;
  at the ε = 0 endpoint +0.010; at the ε = 10⁻³ mutation–selection equilibrium (standing ALLC 0.0019) +0.009 net of
  contract stripping (99.5% of carrier mutations drop the contract; FairBot's contract is valid for μ 0.005).
- **f\*** (carrier fitness exceeds the background's mean): **0.033 (mix) / 0.028 (FairBot) at the μ background; 0 at
  every post-scramble background, with or without mutation.** The post-scramble advantage is ≈ 0.010 per generation at
  every frequency (0.010 / 0.011 / 0.013 / 0.018 / 0.035 at f = 0.001 / 0.003 / 0.01 / 0.03 / 0.1), so it comes from the
  sucker fringe (≈ 2% of the D sea), not from carrier–carrier encounters (w·f = 3·10⁻⁴ at f = 10⁻³).
- The deterministic type-level flow from every seeded state with f₀ ≥ 10⁻⁴ ends in carrier takeover (P(C,C) 0.99–1.00),
  at ε = 0 and 10⁻³, mix and FairBot: carriers dip by 1–3% in generations 1–7 and then grow. **No deterministic
  threshold exists**; the binding barrier is drift during and just after the scramble.

## Results in brief

- **Outcome is lineage survival.** In every finite-ε b = 0 run, either the carriers went extinct (then P(C,C) is the
  no-contract value) or they took over (second-half P(C,C) 0.985–0.992, carrier-conditional P(C,C) 1.000); there were 0
  surviving-but-unsuccessful runs. Extinction comes early: median generation 8 / 29 / 77 / 98 at f₀ = 0.001 / 0.003 /
  0.01 / 0.03 (max 256). Surviving lineages grow at 0.011–0.035 per generation over the first 200 generations and pass
  50% by generation 29–357.
- **Success by f₀, finite ε (pooled mix + FairBot, σ ∈ {0, 1})**: 3/80 [0.01, 0.10], 18/80 [0.15, 0.33], 10/20 [0.30,
  0.70], 17/20 [0.64, 0.95], 20/20 [0.84, 1.00] at f₀ = 0.001 / 0.003 / 0.01 / 0.03 / 0.1 (6 / 19 / 64 / 192 / 640
  carriers). ε = 0 twins: 6/80 [0.03, 0.15], 12/80 [0.09, 0.24], 52/80 [0.54, 0.75], 72/80 [0.81, 0.95], 80/80 [0.95,
  1.00]. Mutation at ε = 10⁻³ creates no threshold; finite ε and twins agree within intervals.
- **Homogeneous FairBot vs mixture:** 37/110 vs 31/110 at finite ε, 111/200 vs 111/200 in the twins: no difference.
  Successful finite-ε runs end on one founder's lineage (founders median 1 after 2·10⁴ generations; 3–5 at the ε = 0
  freeze), so the final composition is a lottery among founders. Pooled over successes the sources are FairBot 0.46, ALLC
  0.27, `BOX1(THEM(ME))` 0.08, `BOX1(THEM(THEM))` 0.08, `BOX(THEM(THEM))` 0.06, `BOX(THEM(^C))` 0.03, D 0.005. Carriers
  are 0.72 of the population; the rest is a contract-less ALLC shadow (source-ALLC load 0.28) fed by mutation, which
  strips contracts at ≈ ε per birth (lost-invalid 7.2·10⁻⁴ per birth; 0.49% of carrier mutations keep the contract).
- **Long window (10⁵ generations, 12 runs, the populations of main reps 0–2):** all 9 established runs stay established
  (sampled P(C,C) ≥ 0.91 throughout, second half 0.988–0.990); 3 runs (f₀ = 0.01, σ = 1) went extinct early, as in the
  2·10⁴ window. No metastable collapse seen.
- **Swapping.** σ = 1 vs σ = 0: finite ε 33/110 vs 35/110 (paired discordances 12 vs 14); twins 110/200 vs 112/200 (16
  vs 18). Accepted swaps are always onto contract-less recipients: 1.8·10⁻⁶ per birth over the finite-ε grid (max per
  run 1.1·10⁻⁴), 5.3·10⁻⁵ over the twins (per cell up to 1.2·10⁻⁴, per run up to 4·10⁻⁴), 7.4·10⁻⁶ over the lottery;
  about 20% of finite-ε swap attempts are rejected as invalid. Recipients are non-carrier copies of prover sources (an
  illegible `BOX(THEM(ME))` acquiring FairBot's contract). **Acquisition across lineages is real:** among σ = 1
  successes the final carriers' contract came from another lineage for > 5% of carriers in 52 of 110 twins, > 50% in 9,
  and for all of them in 3 (the winning lineage was a non-seed acquirer); in the finite-ε grid in 3 of 33. It changes
  which lineage wins, not whether carriers win.
- **Controls.** (ii) Same sources and placement with contracts off: P(C,C) 0.001–0.003 in every cell; every ε = 0 twin
  defecting (0/200). (i) b = ∞: finite ε 36/40, 36/40, 10/10, 10/10, 10/10 at f₀ = 0.001 … 0.1 (mean P(C,C)
  0.944–0.991); ε = 0 twins 31/40, 31/40, 30/40, 39/40, 40/40: the free arm establishes from μ with or without a seed.
  (iii) μ-drawn f₀ = 0.01 at b = 0: 0/10 (σ = 0: the carriers die, P(C,C) ≤ 0.005; σ = 1: P(C,C) 0.0002–0.005 with 0.93–0.97
  of agents carrying `<D>` on D sources), reproducing the published failure.
- **N sweep at f₀ = 0.01 (mix):** finite ε 2/10, 5/10, 6/10 at N = 1,600 / 6,400 / 25,600; ε = 0 twins (σ = 0) 3/20
  [0.05, 0.36], 14/20 [0.48, 0.85], 19/20 [0.76, 0.99]. At fixed f₀ establishment rises with N: more copies against a
  drift barrier set by a per-copy advantage that does not scale with N.
- **Lottery (ε = 0, mN = 1, b = 0; σ = 0 / σ = 1):** (100, 4): k = 0 0/40; k = 1 12/40 [0.18, 0.45] / 9/40; k = 3 14/40
  [0.22, 0.50] / 24/40 [0.45, 0.74]; k = 16 38/40 [0.83, 0.99] / 34/40. (100, 64): k = 0 5/40 [0.05, 0.26], all five
  non-carrier monocultures of `not(BOXD1(THEM(ME)))`, `not(BOXD(THEM(THEM)))` and kin (they cooperate with the illegible
  and defect on D; the published b = 0 lottery had 2/40 of these); k = 1 37/40 [0.80, 0.97] / 38/40; k = 3 40/40 / 40/40.
  **Fixed total of 64 carriers: 16 per island on (100, 4) 0.95 [0.83, 0.99] against 1 per island on (100, 64) 0.925
  [0.80, 0.97]: not resolved.** Every run froze (one σ = 1 run at generation 44,790). The σ = 1 lift at (100, 4), k = 3
  (14 → 24 of 40) is the one σ contrast nominally outside noise (Fisher p ≈ 0.04, one of about 20 σ contrasts) and is unexplained.

## Verdicts

| # | prediction | outcome |
|---|---|---|
| RE 1 | spreads above a carrier–carrier threshold f* ≈ 0.003–0.01; ≥ 4/5 at f₀ ≥ 0.03, ≥ 3/5 at 0.01, 2–12/20 at ≤ 0.003; 50% within 2·10⁴; FairBot ≥ mix | **Partly held, mechanism failed.** Success rises steeply with f₀, t₅₀ ≤ 357 everywhere, FairBot ≈ mix. But there is no carrier–carrier threshold: f* = 0 after ALLC's extinction (0.03 at the μ background), and the post-scramble advantage comes from a sucker fringe. Numeric clauses failed in 6 of 20 cells (f₀ = 0.03 mix σ = 0: 3/5; f₀ = 0.01 σ = 1: 2/5 twice; f₀ = 0.001: 0/20 three times). Falsifier not fired |
| RE 2 | swapping inert: onto-non-carrier acceptance < 10⁻⁴ per birth in every cell; σ effect < 0.05 at every f₀ | **Failed as stated; inert in outcome.** Acceptance 1.8·10⁻⁶ per birth over the finite-ε grid but 1.2·10⁻⁴ in two ε = 0 twin cells; the σ effect on mean P(C,C) at f₀ = 0.03 is 0.30 (7/10 vs 10/10), which fires the > 0.2 falsifier, while pooled over cells σ has no effect (33/110 vs 35/110; discordant pairs 12 vs 14). Swaps do move contracts across lineages |
| RE 3 | control (ii) < 0.1 everywhere; control (i) ≥ 0.9 at f₀ ≥ 0.003 | **Held** (ii ≤ 0.003; i mean 0.944–0.991) |
| RE 4 | k = 0 < 0.1 in both cells; 1/island on (100, 64) beats 16/island on (100, 4), each ≥ 0.2 above k = 0 | **Failed on two clauses:** k = 0 on (100, 64) is 0.125; the fixed-total comparison is unresolved, point estimates reversed (0.925 vs 0.95). Each is ≥ 0.2 above k = 0; falsifier not fired |
| RS | a small seed spreads to every program that can carry it | **Partly.** A prover-carrier seed takes over a b = 0 population with probability ≈ 0.85 at 3% and 0.5 at 1%, mostly dies in the scramble at ≤ 0.3%, and the chance rises with N at fixed f₀. Where it wins, the winner is one founder's lineage (occasionally an acquirer's), not every program that can carry the contract, and 28% of the final population is a contract-less ALLC shadow |
| S1 | μ growth negative for every type; post-ALLC f* < 0.002; ε = 10⁻³ f* in [0.002, 0.015] | **Failed, falsifier fired:** f* = 0 at ε = 10⁻³ (the sucker fringe outweighs standing ALLC and stripping); 6 rare ALLC-exploiting types grow at μ; the post-ALLC clause held |
| S2 | twins 0–0.15 / 0.05–0.3 / 0.2–0.6 / 0.6–0.95 / ≥ 0.95 | **Mostly held:** 0.05 / 0.15 / 0.70 / 0.95 / 1.00 (mix, σ = 0); the f₀ = 0.01 band missed; falsifier not fired |
| S3 | finite ε below twins at f₀ ≤ 0.003; ≤ 1/20, ≤ 4/20, 1–4/5, ≥ 4/5, 5/5; successes ≥ 0.97 | **Partly:** premise failed (finite ε 18/80 vs twins 12/80 at 0.003); FairBot cells exceeded the small-f₀ bounds (3/20, 5/20) and mix f₀ = 0.03 σ = 0 fell short (3/5); success levels held (≥ 0.985, carrier P(C,C) 1.000); falsifier not fired |
| S4 | success rises with N at f₀ = 0.01 | **Held** (twins 0.15 → 0.70 → 0.95) |
| S5 | final carriers from seed founders ≥ 0.99; cross-lineage < 0.01 | **Failed, falsifier fired:** cross-lineage share ≥ 0.05 in 52 of 110 σ = 1 twin successes and 3 of 33 finite-ε ones |
| S6 | fixed-total cells both ≥ 0.8, difference within ±0.15; k = 1 on (100, 4) 0.1–0.35 | **Held** (0.95, 0.925; 0.30) |
