# The gene arm: run report (2026-10-11)

Spec `specs/2026-10-11-gene-arm.md`; notes `notes/gene-arm.md`; predictions `predictions/2026-10-11-gene-arm.md`; code `src/gene_arm.py`, `src/gene_arm_run.py`, `src/gene_arm_report.py`, `tests/test_gene_arm.py`. Raw outputs in `runs/gene_arm/` (cell_*.json, static.json, chicken.json, lottery_*.json, coalition.json; tables_*.npz not committed).

**Scale guard.** At cap 2 the boss slot has ≥ 23206 behavioural classes (worker ≥ 571) > 3,000, so the SOG cells run at **cap 1** (136 worker and 1,323 boss programs), a different experiment from the spec's ≤ 2-gene arm; chicken at cap 2 (68 programs per role).

## Static

**Arms (cap 1):**

| arm | rule | genes W / B | programs B / W | classes B / W | refined units B / W | prior mass kept B / W (length; uniform) |
|---|---|---|---|---|---|---|
| base-CC | CC | 0 / 0 | 27 / 8 | 21 / 8 | 27 / 8 | 1.000 / 1.000; 1.000 / 1.000 |
| base-RC | RC | 0 / 0 | 27 / 8 | 7 / 8 | 27 / 8 | 1.000 / 1.000; 1.000 / 1.000 |
| base-RR | RR | 0 / 0 | 27 / 8 | 6 / 6 | 27 / 8 | 1.000 / 1.000; 1.000 / 1.000 |
| G-all | CC | 16 / 48 | 1323 / 136 | 706 / 80 | 931 / 99 | 1.000 / 1.000; 1.000 / 1.000 |
| G-all-RC | RC | 16 / 48 | 1323 / 136 | 112 / 57 | 447 / 76 | 1.000 / 1.000; 1.000 / 1.000 |
| G-cred | CC | 8 / 8 | 243 / 72 | 125 / 50 | 163 / 59 | 0.969 / 0.982; 0.184 / 0.529 |
| G-cred-ctl | CC | 8 / 8 | 81 / 72 | 7 / 38 | 9 / 47 | 0.323 / 0.982; 0.061 / 0.529 |
| G-cred-whole | RR | 16 / 48 | 1323 / 136 | 38 / 48 | 240 / 66 | 1.000 / 1.000; 1.000 / 1.000 |
| G-cred-whole-ctl | RR | 16 / 48 | 441 / 136 | 38 / 48 | 80 / 66 | 0.333 / 1.000; 0.333 / 1.000 |
| G-asym | CC | 16 / 32 | 891 / 136 | 482 / 80 | 643 / 99 | 0.987 / 1.000; 0.673 / 1.000 |
| G-asym-ctl | CC | 16 / 32 | 297 / 136 | 112 / 57 | 149 / 76 | 0.329 / 1.000; 0.224 / 1.000 |
| G-recip | CC | 6 / 4 | 135 / 56 | 77 / 36 | 99 / 45 | 0.965 / 0.978; 0.102 / 0.412 |
| G-recip-ctl | CC | 6 / 4 | 45 / 56 | 7 / 36 | 9 / 45 | 0.322 / 0.978; 0.034 / 0.412 |
| random | CC | 8 / 8 | 243 / 72 | 134 / 55 | 171 / 61 | 0.969 / 0.982; 0.184 / 0.529 |

**The override filter (G-cred) against the frozen reference catalogue (all cap-1 programs, CC):** admitted = `(BOX(s=0) -> work)`, `(BOX(s<=1/4) -> work)`, `(BOX(s=1/2) -> work)`, `(BOX(h=strike) -> work)`, `(BOX(h=source) -> work)`, `(BOX(OTHER=work) -> work)`, `(BOX(OTHER=strike) -> work)`, `(Q* -> work)`; `(BOX(W1=strike) -> whack none)`, `(BOX(W2=strike) -> whack none)`, `(BOX(W1=work) -> whack none)`, `(BOX(W2=work) -> whack none)`, `(P1(0) -> whack none)`, `(P2(0) -> whack none)`, `(P1(1/4) -> whack none)`, `(P2(1/4) -> whack none)`. No vacuous admission. Admitted-only iteration: converged, changes none. Random removal keeps W: (BOX(s=0) -> work), (BOX(s=1/2) -> work), (BOX(s=1/2) -> strike), (BOX(h=strike) -> work), (BOX(h=source) -> strike), (BOX(OTHER=work) -> strike), (BOX(OTHER=strike) -> strike), (Q* -> work); B: (BOX(W1=strike) -> wage 1/2), (BOX(W2=strike) -> whack source), (P1(0) -> wage 0), (P1(0) -> whack source), (P2(0) -> whack strike), (P1(1/4) -> wage 1/2), (P2(1/4) -> wage 1/2), (P2(1/4) -> whack strike).

| named gene | admitted | firing encounters | failing | heaviest failing witness (boss \| W1 \| W2: play; override vs alternatives) |
|---|---|---|---|---|
| whack w1 (BOX(W1=strike) -> whack strike) | False | 141408 | 141408 | (0,none,0)+(BOX(W1=strike) -> whack strike) \| striker \| scab: (0,strike) S W; 0.5 vs [0.5, 1.0, 1.0] |
| whack w2 (BOX(W2=strike) -> whack strike) | False | 139548 | 139548 | (0,none,0)+(BOX(W2=strike) -> whack strike) \| scab \| striker: (0,strike) W S; 0.5 vs [0.5, 1.0, 1.0] |
| quorum q (Q* -> strike) | False | 253584 | 165698 | (0,strike,0) \| scab+(Q* -> strike) \| striker: (0,strike) S S; -1.0 vs 0.0 |
| probe concession pi (P1(0) -> wage 1/2) | False | 231255 | 80487 | (0,none,0)+(P1(0) -> wage 1/2) \| striker \| scab: (1/2,none) S W; 0.5 vs [1.0, 0.75, 0.5] |
| de-escalation (BOX(W1=strike) -> whack none) | True | 121131 | 0 | – |
| threat accommodation (BOX(h=strike) -> work) | True | 369828 | 0 | – |

**Encoding invariance** (fraction of reference encounter mass, length prior, on which the two encodings play differently):

| pair | CC | RR |
|---|---|---|
| quorum q on scab vs union base | 0.000 | 0.000 |
| probe concession on (0,none,0) vs D0 | 0.000 | 0.000 |
| whack w1 on (0,none,0) vs (0,strike,0) | 0.497 | 0.000 |
| whack w1 on (1/2,none,0) vs (1/2,strike,0) | 0.512 | 0.000 |

Override-filter verdicts: gene encodings fail, base encodings are unfiltered (admitted) — invariance fails for every named gene under G-cred and G-recip; under G-cred-whole both encodings are rationalized identically.

**Named states** (play under the arm; gene-stable strict / weak; Nash; Pareto-dominated):

| state | G-all | G-cred | G-cred-whole | G-asym | G-recip | Nash (CC) | dominated |
|---|---|---|---|---|---|---|---|
| Z = (0,none,0) | scab | scab | (0,none) W W S/S | (0,none) W W S/S | (0,none) W W S/S | (0,none) W W S/S | (0,none) W W S/S | True | False |
| Z_w = (0,strike,0) | scab | scab | (0,strike) W W S/S | (0,strike) W W S/S | (0,none) W W S/S | (0,strike) W W S/S | (0,strike) W W S/S | True | False |
| S = (0,none,0) | striker | striker | (0,none) S S S/U | (0,none) S S S/U | (0,none) S S U/U | (0,none) S S S/U | (0,none) S S S/U | True | True |
| split = (0,none,0) | scab | striker | (0,none) W S S/U | (0,none) W S S/U | (0,none) W S U/U | (0,none) W S S/U | (0,none) W S S/U | True | True |
| F = (1/2,none,0) | militant | militant | (1/2,none) W W S/S | (1/2,none) W W S/S | (1/2,none) W W U/U | (1/2,none) W W S/S | (1/2,none) W W S/S | False | False |
| F_u = (1/2,none,0) | union | union | (1/2,none) W W S/S | (1/2,none) W W S/S | (1/2,none) W W U/U | (1/2,none) W W S/S | (1/2,none) W W S/S | False | False |
| I = (1/4,none,0) | T0 | T0 | (1/4,none) W W S/S | (1/4,none) W W S/S | (1/4,none) W W S/S | (1/4,none) W W S/S | (1/4,none) W W S/S | False | False |
| F* = (0,none,2) | militant | militant | (1/2,none) W W S/S | (1/2,none) W W S/S | (1/4,none) W W S/S | (1/2,none) W W S/S | (1/2,none) W W S/S | False | False |
| Z_D0 = (0,none,1) | scab | scab | (0,none) W W U/U | (0,none) W W S/S | (0,none) W W U/U | (0,none) W W U/U | (0,none) W W S/S | True | False |

**All program triples (cap 1): gene-stable triples by arm** (strict; weak = no admissible gene weakly improves its carrier and strictly improves someone):

| arm | version | triples | gene-stable | stable ∧ Nash | stable ∧ ¬Nash | Nash ∧ ¬stable | stable ∧ Pareto-dominated (prior mass) | stable by wage 0 / ¼ / ½ |
|---|---|---|---|---|---|---|---|---|
| G-all | strict | 24470208 | 3886919 | 709994 | 3176925 | 2419016 | 759149 (0.155) | 794403 / 435842 / 2656674 |
| G-all | weak | 24470208 | 3302375 | 372450 | 2929925 | 2756560 | 225530 (6.2e-04) | 392553 / 412176 / 2497646 |
| G-cred | strict | 1259712 | 686830 | 248897 | 437933 | 0 | 132839 (0.164) | 263468 / 185074 / 238288 |
| G-cred | weak | 1259712 | 587142 | 161952 | 425190 | 86945 | 33151 (5.0e-04) | 168507 / 184579 / 234056 |
| G-cred-whole | strict | 24470208 | 6474441 | 399129 | 6075312 | 5579397 | 0 (0.000) | 399129 / 6075312 / 0 |
| G-cred-whole | weak | 24470208 | 6474441 | 399129 | 6075312 | 5579397 | 0 (0.000) | 399129 / 6075312 / 0 |
| G-asym | strict | 16479936 | 2727008 | 545598 | 2181410 | 1789450 | 655432 (0.156) | 614730 / 308412 / 1803866 |
| G-asym | weak | 16479936 | 2220448 | 248011 | 1972437 | 2087037 | 196305 (6.2e-04) | 261868 / 285042 / 1673538 |
| G-recip | strict | 423360 | 246623 | 87807 | 158816 | 0 | 45014 (0.164) | 92126 / 67094 / 87403 |
| G-recip | weak | 423360 | 214349 | 59619 | 154730 | 28188 | 12740 (4.4e-04) | 62129 / 66523 / 85697 |
| G-recip-ctl | strict | 141120 | 105580 | 43610 | 61970 | 0 | 24305 (0.251) | 43610 / 26600 / 35370 |
| G-recip-ctl | weak | 141120 | 85675 | 24845 | 60830 | 18765 | 4400 (9.3e-04) | 24845 / 26460 / 34370 |

**G-recip: gene-stable Pareto-dominated states and the admissible genes that would leave them** (strict version, heaviest by prior):

- (0,source,0) | striker | striker (play (0,source) S S, mass 0.026): W1 (BOX(s=0) -> work) Δ=0.0 → (0,source) W S; W1 (BOX(s<=1/4) -> work) Δ=0.0 → (0,source) W S; W1 (BOX(OTHER=strike) -> work) Δ=0.0 → (0,source) W S; W2 (BOX(s=0) -> work) Δ=0.0 → (0,source) S W
- (0,source,0) | scab | striker (play (0,source) W S, mass 0.026): W2 (BOX(s=0) -> work) Δ=0.0 → (0,source) W W; W2 (BOX(s<=1/4) -> work) Δ=0.0 → (0,source) W W; W2 (BOX(OTHER=work) -> work) Δ=0.0 → (0,source) W W
- (0,none,0) | striker | scab (play (0,none) S W, mass 0.026): W1 (BOX(s=0) -> work) Δ=0.0 → (0,none) W W; W1 (BOX(s<=1/4) -> work) Δ=0.0 → (0,none) W W; W1 (BOX(OTHER=work) -> work) Δ=0.0 → (0,none) W W
- (0,none,0) | scab | striker (play (0,none) W S, mass 0.026): W2 (BOX(s=0) -> work) Δ=0.0 → (0,none) W W; W2 (BOX(s<=1/4) -> work) Δ=0.0 → (0,none) W W; W2 (BOX(OTHER=work) -> work) Δ=0.0 → (0,none) W W
- weak version: 12740 triples, e.g. (0,none,0) | striker | striker+(BOX(OTHER=strike) -> work) ((0,none) S W); (0,none,0) | striker | striker+(Q* -> work) ((0,none) S W) (no single admissible gene weakly improves its carrier and strictly improves anyone)
- Pareto-efficient states G-recip still admits as gene-stable: zero wage with everyone working (Z) and the fair and ¼ plays held by committed bases (F, F_u, I, F*): the filter cannot choose among the frontier's wages.

**SG on hand states** (targeted proposals; kind):

- Z_D0: B: (BOX(W1=work) -> wage 0) conservative, (BOX(W2=work) -> wage 0) conservative; W1: (BOX(s=0) -> strike) strict, (BOX(s<=1/4) -> strike) strict, (BOX(OTHER=work) -> work) conservative; W2: (BOX(s=0) -> work) conservative, (BOX(s<=1/4) -> work) conservative, (BOX(OTHER=work) -> work) conservative
- Z: B: (BOX(W1=work) -> wage 0) conservative, (BOX(W2=work) -> wage 0) conservative; W1: (BOX(s=0) -> work) conservative, (BOX(s<=1/4) -> work) conservative, (BOX(OTHER=work) -> work) conservative; W2: (BOX(s=0) -> work) conservative, (BOX(s<=1/4) -> work) conservative, (BOX(OTHER=work) -> work) conservative
- S: B: (BOX(W1=strike) -> wage 0) conservative, (BOX(W2=strike) -> wage 0) conservative, (P1(0) -> wage 0) conservative, (P2(0) -> wage 0) conservative, (P1(1/4) -> wage 0) conservative, (P2(1/4) -> wage 0) conservative; W1: (BOX(s=0) -> strike) conservative, (BOX(s<=1/4) -> strike) conservative, (BOX(OTHER=strike) -> strike) conservative, (Q* -> strike) conservative; W2: (BOX(s=0) -> strike) conservative, (BOX(s<=1/4) -> strike) conservative, (BOX(OTHER=strike) -> strike) conservative, (Q* -> strike) conservative
- F: B: (BOX(W1=work) -> wage 1/4) strict, (BOX(W2=work) -> wage 1/4) strict, (P1(0) -> wage 1/4) strict, (P2(0) -> wage 1/4) strict; W1: (BOX(s=1/2) -> work) conservative, (BOX(OTHER=work) -> work) conservative; W2: (BOX(s=1/2) -> work) conservative, (BOX(OTHER=work) -> work) conservative

## Chain (ε → 0; cap 1; c = 0.5)

Fair = wage ½ with both working and no realized whack; ¼ = intermediate; split = one striker. "cut" = unexplored outflow / total outflow; "fair corr." = first-order cut-corrected fair share (dropped fair exits added to the fair escape) where the cut exceeds 2%.

**uniform prior** (N = 10³ → 10⁴):

| arm | kernel | fair | ¼ | zero | strike | split | worker payoff | boss | states | cut | fair corr. | strict-NE seeds |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base-CC | prior | 0.889 → 0.894 | 0.085 → 0.082 | 0.019 → 0.019 | 2.6e-04 → 2.0e-04 | 0.006 → 0.005 | 0.467 | 1.060 | 1344 / 1344 | 0.000 / 0.000 | – | 0 |
| base-RC | prior | 0.904 → 0.907 | 0.084 → 0.081 | 0.006 → 0.005 | 2.4e-04 → 1.9e-04 | 0.006 → 0.006 | 0.474 | 1.046 | 448 / 448 | 0.000 / 0.000 | – | 0 |
| base-RR | prior | 7.4e-04 → 7.5e-05 | 0.993 → 0.994 | 0.007 → 0.006 | 1.4e-05 → 1.4e-06 | 1.0e-04 → 1.0e-05 | 0.249 | 1.503 | 216 / 216 | 0.000 / 0.000 | – | 0 |
| G-all | prior | 0.030 → 0.012 | 0.022 → 0.003 | 0.880 → 0.924 | 0.009 → 0.008 | 0.059 → 0.053 | 0.007 | 1.908 | 68208 / 68208 | 0.000 / 0.000 | – | 0 |
| G-all | SG | 0.058 → 0.027 | 0.035 → 0.005 | 0.820 → 0.888 | 0.010 → 0.010 | 0.076 → 0.070 | 0.015 | 1.872 | 142188 / 142188 | 0.000 / 0.000 | – | 0 |
| G-all | local | 0.035 → 0.014 | 0.024 → 0.003 | 0.875 → 0.923 | 0.010 → 0.010 | 0.056 → 0.051 | 0.008 | 1.907 | 142188 / 142188 | 0.000 / 0.000 | – | 0 |
| G-all-RC | prior | 0.070 → 0.047 | 0.036 → 0.004 | 0.632 → 0.677 | 0.027 → 0.029 | 0.234 → 0.244 | 0.024 | 1.620 | 7935 / 7935 | 0.000 / 0.000 | – | 0 |
| G-cred | prior | 0.902 → 0.914 | 0.036 → 0.028 | 0.057 → 0.053 | 9.7e-05 → 2.9e-05 | 0.005 → 0.004 | 0.464 | 1.068 | 16940 / 16940 | 0.000 / 0.000 | – | 0 |
| G-cred | SG | 0.913 → 0.929 | 0.031 → 0.022 | 0.051 → 0.044 | 1.5e-04 → 3.3e-05 | 0.005 → 0.004 | 0.470 | 1.055 | 21780 / 21780 | 0.000 / 0.000 | – | 0 |
| G-cred | local | 0.922 → 0.936 | 0.025 → 0.016 | 0.049 → 0.044 | 9.6e-05 → 2.5e-05 | 0.004 → 0.004 | 0.472 | 1.052 | 21780 / 21780 | 0.000 / 0.000 | – | 0 |
| G-cred-ctl | prior | 0.965 → 0.973 | 0.028 → 0.022 | 0.004 → 0.002 | 1.3e-04 → 5.2e-05 | 0.002 → 0.002 | 0.492 | 1.013 | 2023 / 2023 | 0.000 / 0.000 | – | 0 |
| G-cred-whole | prior | 0.002 → 2.4e-04 | 0.568 → 0.484 | 0.424 → 0.515 | 1.0e-05 → 5.5e-07 | 0.005 → 6.2e-04 | 0.121 | 1.757 | 2352 / 2352 | 0.000 / 0.000 | – | 0 |
| G-cred-whole | SG | 0.003 → 2.9e-04 | 0.464 → 0.323 | 0.526 → 0.676 | 1.4e-05 → 9.0e-07 | 0.006 → 8.2e-04 | 0.081 | 1.837 | 31944 / 31944 | 0.000 / 0.000 | – | 0 |
| G-cred-whole | local | 0.003 → 2.5e-04 | 0.570 → 0.485 | 0.423 → 0.514 | 1.2e-05 → 7.7e-07 | 0.005 → 6.2e-04 | 0.121 | 1.757 | 31944 / 31944 | 0.000 / 0.000 | – | 0 |
| G-cred-whole-ctl | prior | 0.006 → 6.0e-04 | 0.665 → 0.504 | 0.318 → 0.493 | 4.7e-05 → 1.8e-06 | 0.011 → 0.002 | 0.126 | 1.746 | 2352 / 2352 | 0.000 / 0.000 | – | 0 |
| G-asym | prior | 0.024 → 0.010 | 0.018 → 0.002 | 0.895 → 0.933 | 0.008 → 0.007 | 0.055 → 0.048 | 0.005 | 1.918 | 46256 / 46256 | 0.000 / 0.000 | – | 0 |
| G-asym-ctl | prior | 0.067 → 0.037 | 0.044 → 0.007 | 0.566 → 0.624 | 0.035 → 0.037 | 0.287 → 0.294 | 0.020 | 1.544 | 7935 / 7935 | 0.000 / 0.000 | – | 0 |
| G-recip | prior | 0.931 → 0.941 | 0.047 → 0.040 | 0.015 → 0.013 | 1.2e-04 → 5.7e-05 | 0.006 → 0.006 | 0.480 | 1.033 | 7875 / 7875 | 0.000 / 0.000 | – | 0 |
| G-recip-ctl | prior | 0.953 → 0.960 | 0.039 → 0.034 | 0.004 → 0.003 | 1.1e-04 → 3.1e-05 | 0.003 → 0.003 | 0.488 | 1.020 | 1575 / 1575 | 0.000 / 0.000 | – | 0 |
| random | prior | 0.021 → 0.011 | 0.011 → 0.001 | 0.906 → 0.935 | 0.013 → 0.012 | 0.049 → 0.041 | 0.006 | 1.918 | 21168 / 21168 | 0.000 / 0.000 | – | 0 |

**length prior** (N = 10³ → 10⁴):

| arm | kernel | fair | ¼ | zero | strike | split | worker payoff | boss | states | cut | fair corr. | strict-NE seeds |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base-CC | prior | 0.067 → 0.093 | 0.036 → 0.033 | 0.433 → 0.424 | 0.115 → 0.111 | 0.349 → 0.340 | 0.054 | 1.329 | 748 / 597 | 5.6e-05 / 8.8e-04 | – | 0 |
| base-RC | prior | 0.090 → 0.123 | 0.054 → 0.049 | 0.299 → 0.289 | 0.122 → 0.118 | 0.434 → 0.421 | 0.074 | 1.196 | 395 / 356 | 2.1e-05 / 1.9e-04 | – | 0 |
| base-RR | prior | 5.2e-04 → 6.1e-05 | 0.777 → 0.781 | 0.217 → 0.218 | 2.6e-05 → 1.7e-06 | 0.005 → 4.8e-04 | 0.195 | 1.609 | 196 / 153 | 1.3e-05 / 1.5e-04 | – | 0 |
| G-all | prior | 0.018 → 0.015 | 0.016 → 0.006 | 0.463 → 0.477 | 0.124 → 0.124 | 0.378 → 0.377 | 0.009 | 1.356 | 14480 / 9416 | 0.008 / 0.040 | 0.010 | 0 |
| G-all-RC | prior | 0.034 → 0.016 | 0.032 → 0.012 | 0.322 → 0.343 | 0.134 → 0.136 | 0.478 → 0.493 | 0.012 | 1.211 | 8226 / 8057 | 0.003 / 0.013 | – | 0 |
| G-cred | prior | 0.011 → 0.023 | 0.013 → 0.012 | 0.457 → 0.452 | 0.130 → 0.128 | 0.389 → 0.385 | 0.014 | 1.330 | 3326 / 2080 | 0.001 / 0.006 | – | 0 |
| G-cred | SG | 0.013 → 0.018 | 0.005 → 0.005 | 0.622 → 0.618 | 0.053 → 0.054 | 0.307 → 0.307 | 0.010 | 1.566 | 6147 / 2475 | 0.004 / 0.014 | – | 0 |
| G-cred | local | 0.047 → 0.055 | 0.009 → 0.005 | 0.613 → 0.612 | 0.045 → 0.043 | 0.287 → 0.284 | 0.029 | 1.571 | 7719 / 3914 | 0.005 / 0.019 | – | 0 |
| G-cred-ctl | prior | 0.023 → 0.058 | 0.029 → 0.027 | 0.288 → 0.280 | 0.185 → 0.177 | 0.475 → 0.458 | 0.036 | 1.116 | 1039 / 802 | 6.8e-04 / 0.002 | – | 0 |
| G-cred-whole | prior | 2.3e-04 → 2.9e-05 | 0.764 → 0.762 | 0.231 → 0.238 | 2.2e-05 → 1.3e-06 | 0.005 → 5.1e-04 | 0.190 | 1.619 | 1681 / 1559 | 0.001 / 0.003 | – | 0 |
| G-cred-whole | SG | 2.1e-04 → 3.8e-05 | 0.798 → 0.767 | 0.200 → 0.233 | 9.4e-05 → 1.0e-05 | 0.001 → 1.4e-04 | 0.192 | 1.617 | 14066 / 9082 | 0.005 / 0.024 | 3.3e-05 | 0 |
| G-cred-whole | local | 5.9e-04 → 9.0e-05 | 0.792 → 0.785 | 0.203 → 0.214 | 9.8e-05 → 9.4e-06 | 0.005 → 4.9e-04 | 0.196 | 1.607 | 14908 / 8397 | 0.013 / 0.041 | 6.2e-05 | 0 |
| G-cred-whole-ctl | prior | 6.2e-04 → 7.0e-05 | 0.766 → 0.768 | 0.219 → 0.230 | 1.2e-04 → 4.5e-06 | 0.013 → 0.001 | 0.192 | 1.614 | 1429 / 1461 | 0.001 / 0.004 | – | 0 |
| G-asym | prior | 0.017 → 0.014 | 0.016 → 0.006 | 0.463 → 0.478 | 0.125 → 0.125 | 0.379 → 0.378 | 0.008 | 1.356 | 11789 / 7516 | 0.006 / 0.035 | 0.009 | 0 |
| G-asym-ctl | prior | 0.035 → 0.026 | 0.035 → 0.021 | 0.287 → 0.302 | 0.179 → 0.179 | 0.464 → 0.472 | 0.019 | 1.132 | 6805 / 3814 | 0.003 / 0.015 | – | 0 |
| G-recip | prior | 0.010 → 0.020 | 0.013 → 0.012 | 0.448 → 0.445 | 0.133 → 0.131 | 0.396 → 0.391 | 0.013 | 1.320 | 1874 / 1252 | 9.0e-04 / 0.005 | – | 0 |
| G-recip-ctl | prior | 0.020 → 0.044 | 0.027 → 0.026 | 0.289 → 0.283 | 0.186 → 0.181 | 0.478 → 0.466 | 0.029 | 1.115 | 869 / 669 | 5.7e-04 / 0.002 | – | 0 |
| random | prior | 0.013 → 0.014 | 0.013 → 0.009 | 0.456 → 0.463 | 0.131 → 0.129 | 0.387 → 0.384 | 0.009 | 1.339 | 4381 / 3931 | 0.002 / 0.013 | – | 0 |

### Support, transitions and decisive edges (N = 10⁴)

**G-all, uniform prior** (99% of π on 1701 states; implemented whack {'strike': '0.749', 'none': '0.190', 'source': '0.062'}; strike-whacker bases 0.749; probe bosses 0.004):

- π 0.0147: (0,strike,0)+(BOX(W1=strike) -> wage 1/2) | T0+(Q* -> strike) | T0+(Q* -> strike) → (0,strike) W W [zero wage]
- π 0.0117: (0,strike,0)+(BOX(W1=strike) -> wage 1/2) | militant+(Q* -> strike) | T0+(Q* -> strike) → (0,strike) W W [zero wage]
- π 0.0117: (0,strike,0)+(BOX(W1=strike) -> wage 1/2) | T0+(Q* -> strike) | militant+(Q* -> strike) → (0,strike) W W [zero wage]
- π 0.0094: (0,strike,0)+(BOX(W1=strike) -> wage 1/2) | militant+(Q* -> strike) | militant+(Q* -> strike) → (0,strike) W W [zero wage]
- π 0.0088: (0,strike,0)+(BOX(W1=strike) -> wage 1/2) | T0+(Q* -> strike) | scab+(Q* -> strike) → (0,strike) W W [zero wage]
- π 0.0085: (0,strike,0)+(BOX(W1=strike) -> wage 1/2) | T0+(Q* -> strike) | scab+(BOX(s=0) -> strike) → (0,strike) W W [zero wage]
  - exits of (0,strike,0)+(BOX(W1=strike) -> wage 1/2) | T0+(Q* -> strike) | T0+(Q* -> strike) (π 0.0147): total 4.6e-05 per event; deleterious 0.000, neutral-change 1.8e-07, neutral-keep 4.6e-05; top: W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 2.8e-06; W2 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 2.8e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 2.1e-06
  - exits of (0,strike,0)+(BOX(W1=strike) -> wage 1/2) | militant+(Q* -> strike) | T0+(Q* -> strike) (π 0.0117): total 4.7e-05 per event; deleterious 0.000, neutral-change 1.8e-07, neutral-keep 4.7e-05; top: W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 3.5e-06; W2 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 2.8e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 2.1e-06
  - exits of (0,strike,0)+(BOX(W1=strike) -> wage 1/2) | T0+(Q* -> strike) | militant+(Q* -> strike) (π 0.0117): total 4.7e-05 per event; deleterious 0.000, neutral-change 1.8e-07, neutral-keep 4.7e-05; top: W2 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 3.5e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 2.8e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 2.1e-06

**G-cred, uniform prior** (99% of π on 1098 states; implemented whack {'strike': '0.483', 'none': '0.417', 'source': '0.100'}; strike-whacker bases 0.484; probe bosses 0.777):

- π 0.0077: (0,none,2) | tagged militant | scab → (1/2,none) W W [fair]
- π 0.0069: (0,none,2) | militant | scab → (1/2,none) W W [fair]
- π 0.0058: (0,none,2) | T0-union | T0-union → (1/2,none) W W [fair]
- π 0.0058: (0,none,2) | T0-union | tagged militant → (1/2,none) W W [fair]
- π 0.0058: (0,none,2) | T0-union | militant → (1/2,none) W W [fair]
- π 0.0057: (0,none,2) | T0-union | union → (1/2,none) W W [fair]
  - exits of (0,none,2) | tagged militant | scab (π 0.0077): total 1.8e-05 per event; neutral-change 3.2e-06, deleterious 0.000, neutral-keep 1.5e-05; top: B neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 1.1e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 6.9e-07; W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 6.9e-07
  - exits of (0,none,2) | militant | scab (π 0.0069): total 2.0e-05 per event; neutral-change 5.8e-06, deleterious 0.000, neutral-keep 1.5e-05; top: B neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 1.1e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 6.9e-07; W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 6.9e-07
  - exits of (0,none,2) | T0-union | T0-union (π 0.0058): total 8.8e-06 per event; deleterious 0.000, neutral-keep 6.3e-06, neutral-change 2.5e-06; top: B neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 1.1e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 6.9e-07; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 6.9e-07

**G-cred-whole, uniform prior** (99% of π on 370 states; implemented whack {'strike': '0.000', 'none': '1.000', 'source': '0.000'}; strike-whacker bases 0.000; probe bosses 0.171):

- π 0.0635: (0,none,0)+(BOX(W1=strike) -> wage 1/2) | T0+(Q* -> strike) | T0+(Q* -> strike) → (0,none) W W [zero wage]
- π 0.0404: (0,none,0)+(BOX(W1=strike) -> wage 1/2) | scab+(BOX(s=0) -> strike) | T0+(Q* -> strike) → (0,none) W W [zero wage]
- π 0.0404: (0,none,0)+(BOX(W1=strike) -> wage 1/2) | T0+(Q* -> strike) | scab+(BOX(s=0) -> strike) → (0,none) W W [zero wage]
- π 0.0257: (0,none,0)+(BOX(W1=strike) -> wage 1/2) | scab+(BOX(s=0) -> strike) | scab+(BOX(s=0) -> strike) → (0,none) W W [zero wage]
- π 0.0231: (0,none,0)+(BOX(W1=strike) -> wage 1/2) | T0+(Q* -> strike) | scab+(Q* -> strike) → (0,none) W W [zero wage]
- π 0.0222: (0,none,0)+(BOX(W1=strike) -> wage 1/2) | scab+(Q* -> strike) | T0+(Q* -> strike) → (0,none) W W [zero wage]
  - exits of (0,none,0)+(BOX(W1=strike) -> wage 1/2) | T0+(Q* -> strike) | T0+(Q* -> strike) (π 0.0635): total 5.1e-05 per event; deleterious 0.000, neutral-keep 3.5e-05, neutral-change 1.7e-05; top: W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 4.9e-06; W2 neutral-keep Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 4.9e-06; W1 neutral-change Δ=0.000 NΔ=0.0 → (0,none) S W (scab split) 3.5e-06
  - exits of (0,none,0)+(BOX(W1=strike) -> wage 1/2) | scab+(BOX(s=0) -> strike) | T0+(Q* -> strike) (π 0.0404): total 5.4e-05 per event; deleterious 0.000, neutral-keep 3.7e-05, neutral-change 1.7e-05; top: W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 7.6e-06; W2 neutral-keep Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 4.9e-06; W1 neutral-change Δ=0.000 NΔ=0.0 → (0,none) S W (scab split) 3.5e-06
  - exits of (0,none,0)+(BOX(W1=strike) -> wage 1/2) | T0+(Q* -> strike) | scab+(BOX(s=0) -> strike) (π 0.0404): total 5.4e-05 per event; deleterious 0.000, neutral-keep 3.7e-05, neutral-change 1.7e-05; top: W2 neutral-keep Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 7.6e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 4.9e-06; W1 neutral-change Δ=0.000 NΔ=0.0 → (0,none) S W (scab split) 3.5e-06

**G-asym, uniform prior** (99% of π on 1537 states; implemented whack {'strike': '0.779', 'none': '0.166', 'source': '0.055'}; strike-whacker bases 0.780; probe bosses 0.003):

- π 0.0149: (0,strike,0)+(BOX(W1=strike) -> wage 1/2) | T0+(Q* -> strike) | T0+(Q* -> strike) → (0,strike) W W [zero wage]
- π 0.0119: (0,strike,0)+(BOX(W1=strike) -> wage 1/2) | T0+(Q* -> strike) | militant+(Q* -> strike) → (0,strike) W W [zero wage]
- π 0.0119: (0,strike,0)+(BOX(W1=strike) -> wage 1/2) | militant+(Q* -> strike) | T0+(Q* -> strike) → (0,strike) W W [zero wage]
- π 0.0095: (0,strike,0)+(BOX(W1=strike) -> wage 1/2) | militant+(Q* -> strike) | militant+(Q* -> strike) → (0,strike) W W [zero wage]
- π 0.0090: (0,strike,0)+(BOX(W1=strike) -> wage 1/2) | T0+(Q* -> strike) | scab+(Q* -> strike) → (0,strike) W W [zero wage]
- π 0.0088: (0,strike,0)+(BOX(W1=strike) -> wage 1/2) | T0+(Q* -> strike) | scab+(BOX(s=0) -> strike) → (0,strike) W W [zero wage]
  - exits of (0,strike,0)+(BOX(W1=strike) -> wage 1/2) | T0+(Q* -> strike) | T0+(Q* -> strike) (π 0.0149): total 4.6e-05 per event; deleterious 0.000, neutral-change 1.8e-07, neutral-keep 4.6e-05; top: W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 2.8e-06; W2 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 2.8e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 2.1e-06
  - exits of (0,strike,0)+(BOX(W1=strike) -> wage 1/2) | T0+(Q* -> strike) | militant+(Q* -> strike) (π 0.0119): total 4.7e-05 per event; deleterious 0.000, neutral-change 1.8e-07, neutral-keep 4.7e-05; top: W2 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 3.5e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 2.8e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 2.1e-06
  - exits of (0,strike,0)+(BOX(W1=strike) -> wage 1/2) | militant+(Q* -> strike) | T0+(Q* -> strike) (π 0.0119): total 4.7e-05 per event; deleterious 0.000, neutral-change 1.8e-07, neutral-keep 4.7e-05; top: W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 3.5e-06; W2 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 2.8e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 2.1e-06

**G-recip, uniform prior** (99% of π on 784 states; implemented whack {'strike': '0.447', 'none': '0.449', 'source': '0.103'}; strike-whacker bases 0.449; probe bosses 0.740):

- π 0.0066: (0,none,2) | tagged militant | scab → (1/2,none) W W [fair]
- π 0.0060: (0,none,2) | militant | scab → (1/2,none) W W [fair]
- π 0.0059: (0,none,2) | T0-union | T0-union → (1/2,none) W W [fair]
- π 0.0059: (0,none,2) | T0-union | tagged militant → (1/2,none) W W [fair]
- π 0.0059: (0,none,2) | T0-union | militant → (1/2,none) W W [fair]
- π 0.0058: (0,none,2) | T0-union | union → (1/2,none) W W [fair]
  - exits of (0,none,2) | tagged militant | scab (π 0.0066): total 1.4e-05 per event; neutral-change 3.2e-06, deleterious 0.000, neutral-keep 1.1e-05; top: B neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 1.1e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 6.9e-07; W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 6.9e-07
  - exits of (0,none,2) | militant | scab (π 0.0060): total 1.7e-05 per event; neutral-change 5.8e-06, deleterious 0.000, neutral-keep 1.1e-05; top: B neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 1.1e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 6.9e-07; W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 6.9e-07
  - exits of (0,none,2) | T0-union | T0-union (π 0.0059): total 8.8e-06 per event; deleterious 0.000, neutral-keep 6.3e-06, neutral-change 2.5e-06; top: B neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 1.1e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 6.9e-07; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 6.9e-07

**G-cred-ctl, uniform prior** (99% of π on 214 states; implemented whack {'strike': '0.000', 'none': '1.000', 'source': '0.000'}; strike-whacker bases 0.000; probe bosses 0.895):

- π 0.0218: (0,none,2) | militant | scab → (1/2,none) W W [fair]
- π 0.0218: (0,none,2) | tagged militant | scab → (1/2,none) W W [fair]
- π 0.0150: (0,none,2) | militant | T0+(BOX(s=1/2) -> work) → (1/2,none) W W [fair]
- π 0.0150: (0,none,2) | tagged militant | T0+(BOX(s=1/2) -> work) → (1/2,none) W W [fair]
- π 0.0150: (0,none,2) | tagged militant | T0-union+(BOX(s=1/2) -> work) → (1/2,none) W W [fair]
- π 0.0150: (0,none,2) | militant | T0-union+(BOX(s=1/2) -> work) → (1/2,none) W W [fair]
  - exits of (0,none,2) | militant | scab (π 0.0218): total 1.5e-05 per event; neutral-change 3.5e-07, deleterious 0.000, neutral-keep 1.5e-05; top: W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 1.4e-06; W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 1.4e-06; W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 1.4e-06
  - exits of (0,none,2) | tagged militant | scab (π 0.0218): total 1.5e-05 per event; neutral-change 3.5e-07, deleterious 0.000, neutral-keep 1.5e-05; top: W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 1.4e-06; W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 1.4e-06; W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 1.4e-06
  - exits of (0,none,2) | militant | T0+(BOX(s=1/2) -> work) (π 0.0150): total 1.5e-05 per event; deleterious 0.000, neutral-keep 1.5e-05; top: W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 2.1e-06; W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 1.4e-06; W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 1.4e-06

**base-CC, uniform prior** (99% of π on 235 states; implemented whack {'strike': '0.459', 'none': '0.451', 'source': '0.091'}; strike-whacker bases 0.459; probe bosses 0.662):

- π 0.0077: (1/2,source,0) | militant | militant → (1/2,source) W W [fair]
- π 0.0077: (1/2,source,0) | militant | T0 → (1/2,source) W W [fair]
- π 0.0076: (0,source,2) | militant | militant → (1/2,source) W W [fair]
- π 0.0073: (0,source,2) | militant | T0 → (1/2,source) W W [fair]
- π 0.0071: (1/2,source,0) | militant | scab → (1/2,source) W W [fair]
- π 0.0069: (1/4,none,0) | T0-union | T0 → (1/4,none) W W [intermediate]
  - exits of (1/2,source,0) | militant | militant (π 0.0077): total 3.9e-05 per event; deleterious 0.000, neutral-change 1.7e-05, neutral-keep 2.2e-05; top: W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,source) W W (fair) 4.2e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,source) W W (fair) 4.2e-06; W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,source) W W (fair) 4.2e-06
  - exits of (1/2,source,0) | militant | T0 (π 0.0077): total 3.9e-05 per event; deleterious 0.000, neutral-change 1.7e-05, neutral-keep 2.2e-05; top: W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,source) W W (fair) 4.2e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,source) W W (fair) 4.2e-06; W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,source) W W (fair) 4.2e-06
  - exits of (0,source,2) | militant | militant (π 0.0076): total 3.3e-05 per event; deleterious 0.000, neutral-change 1.7e-05, neutral-keep 1.6e-05; top: W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,source) W W (fair) 4.2e-06; W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,source) W W (fair) 4.2e-06; B neutral-change Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 3.7e-06

**base-RC, uniform prior** (99% of π on 109 states; implemented whack {'strike': '0.000', 'none': '1.000', 'source': '0.000'}; strike-whacker bases 0.000; probe bosses 0.647):

- π 0.0144: (1/4,none,0) | T0-union | T0 → (1/4,none) W W [intermediate]
- π 0.0141: (1/2,none,0) | militant | militant → (1/2,none) W W [fair]
- π 0.0141: (1/2,none,0) | tagged militant | militant → (1/2,none) W W [fair]
- π 0.0141: (1/2,none,0) | tagged militant | tagged militant → (1/2,none) W W [fair]
- π 0.0141: (1/2,none,0) | militant | tagged militant → (1/2,none) W W [fair]
- π 0.0140: (1/2,none,0) | tagged militant | T0-union → (1/2,none) W W [fair]
  - exits of (1/4,none,0) | T0-union | T0 (π 0.0144): total 2.4e-05 per event; deleterious 0.000, neutral-keep 2.4e-05; top: W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/4,none) W W (intermediate) 4.2e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/4,none) W W (intermediate) 4.2e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/4,none) W W (intermediate) 4.2e-06
  - exits of (1/2,none,0) | militant | militant (π 0.0141): total 5.6e-05 per event; deleterious 0.000, neutral-keep 5.6e-05; top: W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 4.2e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 4.2e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 4.2e-06
  - exits of (1/2,none,0) | tagged militant | militant (π 0.0141): total 5.6e-05 per event; deleterious 0.000, neutral-keep 5.6e-05; top: W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 4.2e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 4.2e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/2,none) W W (fair) 4.2e-06

**G-all, length prior** (99% of π on 1107 states; implemented whack {'strike': '0.241', 'none': '0.374', 'source': '0.384'}; strike-whacker bases 0.243; probe bosses 0.022):

- π 0.1924: (0,strike,0) | scab | scab → (0,strike) W W [zero wage]
- π 0.1166: (0,source,0) | scab | scab → (0,source) W W [zero wage]
- π 0.1082: (0,none,0) | scab | scab → (0,none) W W [zero wage]
- π 0.0938: (0,source,0) | striker | scab → (0,source) S W [scab split] Pareto-dominated
- π 0.0935: (0,source,0) | scab | striker → (0,source) W S [scab split] Pareto-dominated
- π 0.0859: (0,none,0) | striker | scab → (0,none) S W [scab split] Pareto-dominated
  - exits of (0,strike,0) | scab | scab (π 0.1924): total 8.2e-06 per event; neutral-change 7.4e-06, deleterious 0.000, neutral-keep 8.4e-07; top: B neutral-change Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 3.6e-06; B neutral-change Δ=0.000 NΔ=0.0 → (0,source) W W (zero wage) 3.6e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 5.3e-08
  - exits of (0,source,0) | scab | scab (π 0.1166): total 4.1e-05 per event; neutral-change 4.0e-05, deleterious 0.000, neutral-keep 4.9e-07; top: W1 neutral-change Δ=0.000 NΔ=0.0 → (0,source) S W (scab split) 1.6e-05; W2 neutral-change Δ=0.000 NΔ=0.0 → (0,source) W S (scab split) 1.6e-05; B neutral-change Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 3.6e-06
  - exits of (0,none,0) | scab | scab (π 0.1082): total 4.2e-05 per event; neutral-keep 8.1e-07, deleterious 0.000, neutral-change 4.1e-05; top: W1 neutral-change Δ=0.000 NΔ=0.0 → (0,none) S W (scab split) 1.6e-05; W2 neutral-change Δ=0.000 NΔ=0.0 → (0,none) W S (scab split) 1.6e-05; B neutral-change Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 3.6e-06

**G-cred, length prior** (99% of π on 205 states; implemented whack {'strike': '0.220', 'none': '0.389', 'source': '0.390'}; strike-whacker bases 0.222; probe bosses 0.014):

- π 0.1982: (0,strike,0) | scab | scab → (0,strike) W W [zero wage]
- π 0.1219: (0,source,0) | scab | scab → (0,source) W W [zero wage]
- π 0.1153: (0,none,0) | scab | scab → (0,none) W W [zero wage]
- π 0.0972: (0,source,0) | striker | scab → (0,source) S W [scab split] Pareto-dominated
- π 0.0970: (0,source,0) | scab | striker → (0,source) W S [scab split] Pareto-dominated
- π 0.0910: (0,none,0) | striker | scab → (0,none) S W [scab split] Pareto-dominated
  - exits of (0,strike,0) | scab | scab (π 0.1982): total 7.7e-06 per event; neutral-change 7.2e-06, neutral-keep 5.2e-07, deleterious 0.000; top: B neutral-change Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 3.6e-06; B neutral-change Δ=0.000 NΔ=0.0 → (0,source) W W (zero wage) 3.6e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 4.6e-08
  - exits of (0,source,0) | scab | scab (π 0.1219): total 3.9e-05 per event; neutral-change 3.9e-05, neutral-keep 2.6e-07, deleterious 0.000; top: W1 neutral-change Δ=0.000 NΔ=0.0 → (0,source) S W (scab split) 1.6e-05; W2 neutral-change Δ=0.000 NΔ=0.0 → (0,source) W S (scab split) 1.6e-05; B neutral-change Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 3.6e-06
  - exits of (0,none,0) | scab | scab (π 0.1153): total 4.1e-05 per event; neutral-change 4.0e-05, neutral-keep 4.3e-07, deleterious 0.000; top: W1 neutral-change Δ=0.000 NΔ=0.0 → (0,none) S W (scab split) 1.6e-05; W2 neutral-change Δ=0.000 NΔ=0.0 → (0,none) W S (scab split) 1.6e-05; B neutral-change Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 3.6e-06

**G-cred-whole, length prior** (99% of π on 115 states; implemented whack {'strike': '0.000', 'none': '1.000', 'source': '0.000'}; strike-whacker bases 0.000; probe bosses 0.017):

- π 0.2327: (1/4,none,0) | striker | striker → (1/4,none) W W [intermediate]
- π 0.2322: (1/4,none,0) | striker | scab → (1/4,none) W W [intermediate]
- π 0.2242: (1/4,none,0) | scab | striker → (1/4,none) W W [intermediate]
- π 0.2182: (0,none,0) | scab | scab → (0,none) W W [zero wage]
- π 0.0050: (0,none,2) | striker | scab → (1/4,none) W W [intermediate]
- π 0.0041: (0,none,2) | striker | striker → (1/4,none) W W [intermediate]
  - exits of (1/4,none,0) | striker | striker (π 0.2327): total 3.5e-05 per event; deleterious 0.000, neutral-keep 3.5e-05; top: W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/4,none) W W (intermediate) 1.6e-05; W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/4,none) W W (intermediate) 1.6e-05; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/4,none) W W (intermediate) 2.0e-07
  - exits of (1/4,none,0) | striker | scab (π 0.2322): total 3.5e-05 per event; deleterious 0.000, neutral-keep 3.5e-05; top: W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/4,none) W W (intermediate) 1.6e-05; W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/4,none) W W (intermediate) 1.6e-05; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/4,none) W W (intermediate) 2.0e-07
  - exits of (1/4,none,0) | scab | striker (π 0.2242): total 3.5e-05 per event; deleterious 0.000, neutral-keep 3.5e-05; top: W2 neutral-keep Δ=0.000 NΔ=0.0 → (1/4,none) W W (intermediate) 1.6e-05; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/4,none) W W (intermediate) 1.6e-05; W1 neutral-keep Δ=0.000 NΔ=0.0 → (1/4,none) W W (intermediate) 2.0e-07

**G-asym, length prior** (99% of π on 790 states; implemented whack {'strike': '0.241', 'none': '0.376', 'source': '0.384'}; strike-whacker bases 0.242; probe bosses 0.017):

- π 0.1950: (0,strike,0) | scab | scab → (0,strike) W W [zero wage]
- π 0.1175: (0,source,0) | scab | scab → (0,source) W W [zero wage]
- π 0.1095: (0,none,0) | scab | scab → (0,none) W W [zero wage]
- π 0.0944: (0,source,0) | striker | scab → (0,source) S W [scab split] Pareto-dominated
- π 0.0942: (0,source,0) | scab | striker → (0,source) W S [scab split] Pareto-dominated
- π 0.0868: (0,none,0) | striker | scab → (0,none) S W [scab split] Pareto-dominated
  - exits of (0,strike,0) | scab | scab (π 0.1950): total 8.1e-06 per event; neutral-change 7.3e-06, deleterious 0.000, neutral-keep 8.0e-07; top: B neutral-change Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 3.6e-06; B neutral-change Δ=0.000 NΔ=0.0 → (0,source) W W (zero wage) 3.6e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 5.3e-08
  - exits of (0,source,0) | scab | scab (π 0.1175): total 4.0e-05 per event; neutral-change 4.0e-05, deleterious 0.000, neutral-keep 4.6e-07; top: W1 neutral-change Δ=0.000 NΔ=0.0 → (0,source) S W (scab split) 1.6e-05; W2 neutral-change Δ=0.000 NΔ=0.0 → (0,source) W S (scab split) 1.6e-05; B neutral-change Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 3.6e-06
  - exits of (0,none,0) | scab | scab (π 0.1095): total 4.2e-05 per event; neutral-keep 7.7e-07, deleterious 0.000, neutral-change 4.1e-05; top: W1 neutral-change Δ=0.000 NΔ=0.0 → (0,none) S W (scab split) 1.6e-05; W2 neutral-change Δ=0.000 NΔ=0.0 → (0,none) W S (scab split) 1.6e-05; B neutral-change Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 3.6e-06

**G-recip, length prior** (99% of π on 148 states; implemented whack {'strike': '0.211', 'none': '0.396', 'source': '0.392'}; strike-whacker bases 0.212; probe bosses 0.011):

- π 0.1945: (0,strike,0) | scab | scab → (0,strike) W W [zero wage]
- π 0.1226: (0,source,0) | scab | scab → (0,source) W W [zero wage]
- π 0.1178: (0,none,0) | scab | scab → (0,none) W W [zero wage]
- π 0.0982: (0,source,0) | striker | scab → (0,source) S W [scab split] Pareto-dominated
- π 0.0980: (0,source,0) | scab | striker → (0,source) W S [scab split] Pareto-dominated
- π 0.0936: (0,none,0) | striker | scab → (0,none) S W [scab split] Pareto-dominated
  - exits of (0,strike,0) | scab | scab (π 0.1945): total 7.6e-06 per event; neutral-change 7.2e-06, neutral-keep 4.0e-07, deleterious 0.000; top: B neutral-change Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 3.6e-06; B neutral-change Δ=0.000 NΔ=0.0 → (0,source) W W (zero wage) 3.6e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 4.6e-08
  - exits of (0,source,0) | scab | scab (π 0.1226): total 3.9e-05 per event; neutral-change 3.9e-05, neutral-keep 1.8e-07, deleterious 0.000; top: W1 neutral-change Δ=0.000 NΔ=0.0 → (0,source) S W (scab split) 1.6e-05; W2 neutral-change Δ=0.000 NΔ=0.0 → (0,source) W S (scab split) 1.6e-05; B neutral-change Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 3.6e-06
  - exits of (0,none,0) | scab | scab (π 0.1178): total 4.0e-05 per event; neutral-change 4.0e-05, neutral-keep 4.1e-07, deleterious 0.000; top: W1 neutral-change Δ=0.000 NΔ=0.0 → (0,none) S W (scab split) 1.6e-05; W2 neutral-change Δ=0.000 NΔ=0.0 → (0,none) W S (scab split) 1.6e-05; B neutral-change Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 3.6e-06

**G-cred-ctl, length prior** (99% of π on 110 states; implemented whack {'strike': '0.000', 'none': '1.000', 'source': '0.000'}; strike-whacker bases 0.000; probe bosses 0.040):

- π 0.2710: (0,none,0) | scab | scab → (0,none) W W [zero wage]
- π 0.2218: (0,none,0) | striker | scab → (0,none) S W [scab split] Pareto-dominated
- π 0.2203: (0,none,0) | scab | striker → (0,none) W S [scab split] Pareto-dominated
- π 0.1745: (0,none,0) | striker | striker → (0,none) S S [strike] Pareto-dominated
- π 0.0151: (1/4,none,0) | T0-union | scab → (1/4,none) W W [intermediate]
- π 0.0097: (1/2,none,0) | tagged militant | scab → (1/2,none) W W [fair]
  - exits of (0,none,0) | scab | scab (π 0.2710): total 3.3e-05 per event; deleterious 0.000, neutral-keep 4.2e-07, neutral-change 3.3e-05; top: W1 neutral-change Δ=0.000 NΔ=0.0 → (0,none) S W (scab split) 1.6e-05; W2 neutral-change Δ=0.000 NΔ=0.0 → (0,none) W S (scab split) 1.6e-05; W1 neutral-change Δ=0.000 NΔ=0.0 → (0,none) S W (scab split) 1.6e-07
  - exits of (0,none,0) | striker | scab (π 0.2218): total 3.4e-05 per event; deleterious 0.000, neutral-change 3.3e-05, neutral-keep 8.3e-07; top: W1 neutral-change Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 1.6e-05; W2 neutral-change Δ=0.000 NΔ=0.0 → (0,none) S S (strike) 1.6e-05; W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,none) S W (scab split) 1.6e-07
  - exits of (0,none,0) | scab | striker (π 0.2203): total 3.4e-05 per event; deleterious 0.000, neutral-keep 8.4e-07, neutral-change 3.3e-05; top: W2 neutral-change Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 1.6e-05; W1 neutral-change Δ=0.000 NΔ=0.0 → (0,none) S S (strike) 1.6e-05; W1 neutral-change Δ=0.000 NΔ=0.0 → (0,none) S S (strike) 1.6e-07

**base-CC, length prior** (99% of π on 140 states; implemented whack {'strike': '0.248', 'none': '0.386', 'source': '0.366'}; strike-whacker bases 0.248; probe bosses 0.060):

- π 0.1933: (0,strike,0) | scab | scab → (0,strike) W W [zero wage]
- π 0.1101: (0,source,0) | scab | scab → (0,source) W W [zero wage]
- π 0.1058: (0,none,0) | scab | scab → (0,none) W W [zero wage]
- π 0.0861: (0,source,0) | striker | scab → (0,source) S W [scab split] Pareto-dominated
- π 0.0835: (0,source,0) | scab | striker → (0,source) W S [scab split] Pareto-dominated
- π 0.0820: (0,none,0) | striker | scab → (0,none) S W [scab split] Pareto-dominated
  - exits of (0,strike,0) | scab | scab (π 0.1933): total 8.0e-06 per event; neutral-change 7.4e-06, deleterious 0.000, neutral-keep 5.7e-07; top: B neutral-change Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 3.6e-06; B neutral-change Δ=0.000 NΔ=0.0 → (0,source) W W (zero wage) 3.6e-06; W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 2.2e-07
  - exits of (0,source,0) | scab | scab (π 0.1101): total 4.1e-05 per event; neutral-change 4.0e-05, deleterious 0.000, neutral-keep 1.3e-07; top: W1 neutral-change Δ=0.000 NΔ=0.0 → (0,source) S W (scab split) 1.6e-05; W2 neutral-change Δ=0.000 NΔ=0.0 → (0,source) W S (scab split) 1.6e-05; B neutral-change Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 3.6e-06
  - exits of (0,none,0) | scab | scab (π 0.1058): total 4.2e-05 per event; neutral-change 4.2e-05, deleterious 0.000, neutral-keep 5.7e-07; top: W1 neutral-change Δ=0.000 NΔ=0.0 → (0,none) S W (scab split) 1.6e-05; W2 neutral-change Δ=0.000 NΔ=0.0 → (0,none) W S (scab split) 1.6e-05; B neutral-change Δ=0.000 NΔ=0.0 → (0,strike) W W (zero wage) 3.6e-06

**base-RC, length prior** (99% of π on 81 states; implemented whack {'strike': '0.000', 'none': '1.000', 'source': '0.000'}; strike-whacker bases 0.000; probe bosses 0.076):

- π 0.2723: (0,none,0) | scab | scab → (0,none) W W [zero wage]
- π 0.2071: (0,none,0) | striker | scab → (0,none) S W [scab split] Pareto-dominated
- π 0.1962: (0,none,0) | scab | striker → (0,none) W S [scab split] Pareto-dominated
- π 0.1143: (0,none,0) | striker | striker → (0,none) S S [strike] Pareto-dominated
- π 0.0202: (1/4,none,0) | T0 | scab → (1/4,none) W W [intermediate]
- π 0.0194: (1/4,none,0) | T0-union | scab → (1/4,none) W W [intermediate]
  - exits of (0,none,0) | scab | scab (π 0.2723): total 3.5e-05 per event; deleterious 0.000, neutral-keep 8.3e-07, neutral-change 3.4e-05; top: W1 neutral-change Δ=0.000 NΔ=0.0 → (0,none) S W (scab split) 1.6e-05; W2 neutral-change Δ=0.000 NΔ=0.0 → (0,none) W S (scab split) 1.6e-05; B neutral-keep Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 3.0e-07
  - exits of (0,none,0) | striker | scab (π 0.2071): total 3.5e-05 per event; deleterious 0.000, neutral-change 3.4e-05, neutral-keep 9.9e-07; top: W1 neutral-change Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 1.6e-05; W2 neutral-change Δ=0.000 NΔ=0.0 → (0,none) S S (strike) 1.6e-05; W1 neutral-keep Δ=0.000 NΔ=0.0 → (0,none) S W (scab split) 2.2e-07
  - exits of (0,none,0) | scab | striker (π 0.1962): total 3.5e-05 per event; deleterious 0.000, neutral-keep 1.4e-06, neutral-change 3.4e-05; top: W1 neutral-change Δ=0.000 NΔ=0.0 → (0,none) S S (strike) 1.6e-05; W2 neutral-change Δ=0.000 NΔ=0.0 → (0,none) W W (zero wage) 1.6e-05; B neutral-keep Δ=0.000 NΔ=0.0 → (0,none) W S (scab split) 3.0e-07

## Execution rates of threat-type genes and commitments (prior kernel; the RS's second addition)

| cell | threat | carrier mass | on-path execution rate | cost / execution | carriers' mean payoff | non-carriers' |
|---|---|---|---|---|---|---|
| base-CC/uniform | whack | 0.549 | 4.0e-06 | 0.500 | 1.070 | 1.047 |
| base-CC/uniform | quorum strike | 0.559 | 0.0001 | 2.5e-05 | 0.480 | 0.451 |
| base-CC/uniform | costly strike | 0.742 | 3.0e-06 | 0.459 | 0.478 | 0.436 |
| base-RC/uniform | whack | 0.000 | – | – | – | 1.046 |
| base-RC/uniform | quorum strike | 0.627 | 0.0002 | 7.4e-05 | 0.485 | 0.456 |
| base-RC/uniform | costly strike | 0.745 | 2.9e-06 | 0.474 | 0.478 | 0.461 |
| G-all/uniform | whack | 0.814 | 7.5e-06 | 0.501 | 1.969 | 1.641 |
| G-all/uniform | quorum strike | 0.555 | 0.0004 | 3.6e-04 | 0.011 | 0.011 |
| G-all/uniform | costly strike | 0.879 | 0.0188 | 0.500 | 0.012 | 0.006 |
| G-cred/uniform | whack | 0.585 | 5.9e-06 | 0.501 | 1.102 | 1.019 |
| G-cred/uniform | quorum strike | 0.518 | 2.5e-05 | 4.1e-05 | 0.468 | 0.460 |
| G-cred/uniform | costly strike | 0.795 | 3.0e-06 | 0.467 | 0.476 | 0.417 |
| G-recip/uniform | whack | 0.553 | 7.4e-06 | 0.501 | 1.039 | 1.025 |
| G-recip/uniform | quorum strike | 0.527 | 4.8e-05 | 5.2e-05 | 0.485 | 0.475 |
| G-recip/uniform | costly strike | 0.794 | 3.9e-06 | 0.458 | 0.489 | 0.449 |
| base-CC/length | whack | 0.614 | 9.7e-07 | 0.500 | 1.434 | 1.160 |
| base-CC/length | quorum strike | 0.047 | 0.0187 | 3.8e-05 | 0.365 | 0.039 |
| base-CC/length | costly strike | 0.357 | 0.0003 | 0.362 | 0.094 | 0.033 |
| base-RC/length | whack | 0.000 | – | – | – | 1.196 |
| base-RC/length | quorum strike | 0.085 | 0.0195 | 1.1e-04 | 0.373 | 0.046 |
| base-RC/length | costly strike | 0.435 | 0.0004 | 0.370 | 0.107 | 0.048 |
| G-all/length | whack | 0.632 | 2.3e-06 | 0.500 | 1.466 | 1.167 |
| G-all/length | quorum strike | 0.024 | 0.0198 | 3.7e-04 | 0.239 | 0.004 |
| G-all/length | costly strike | 0.353 | 0.0013 | 0.431 | 0.022 | 0.003 |
| G-cred/length | whack | 0.614 | 1.4e-06 | 0.500 | 1.441 | 1.154 |
| G-cred/length | quorum strike | 0.021 | 0.0067 | 6.1e-05 | 0.355 | 0.007 |
| G-cred/length | costly strike | 0.349 | 0.0003 | 0.344 | 0.026 | 0.008 |
| G-recip/length | whack | 0.605 | 3.0e-07 | 0.500 | 1.431 | 1.152 |
| G-recip/length | quorum strike | 0.019 | 0.0079 | 6.1e-05 | 0.353 | 0.006 |
| G-recip/length | costly strike | 0.350 | 0.0003 | 0.339 | 0.023 | 0.008 |

## The proof device on the chain's support (99% of π)

| cell | gene-stable mass | weak | Pareto-dominated | dominated ∧ stable | Nash | heaviest dominated ∧ stable |
|---|---|---|---|---|---|---|
| G-all/length | 0.982 | 0.478 | 0.501 | 0.499 | 0.976 | (0,source,0) | striker | scab ((0,source) S W, π 0.0938) |
| G-all/uniform | 0.990 | 0.958 | 0.060 | 0.060 | 0.958 | (0,none,0)+(BOX(W1=strike) -> wage 1/2) | striker+(Q* -> strike) | T0+(Q* -> strike) ((1/2,none) S W, π 0.0021) |
| G-all-RC/length | 0.978 | 0.331 | 0.628 | 0.624 | 0.966 | (0,none,0) | striker | scab ((0,none) S W, π 0.2308) |
| G-all-RC/uniform | 0.990 | 0.862 | 0.269 | 0.269 | 0.862 | (0,none,0)+(BOX(W1=strike) -> wage 1/2) | T0+(Q* -> strike) | striker+(Q* -> strike) ((0,none) W S, π 0.0108) |
| G-asym/length | 0.983 | 0.479 | 0.502 | 0.500 | 0.977 | (0,source,0) | striker | scab ((0,source) S W, π 0.0944) |
| G-asym/uniform | 0.990 | 0.961 | 0.054 | 0.054 | 0.964 | (0,none,0)+(BOX(W1=strike) -> wage 1/2) | striker+(Q* -> strike) | T0+(Q* -> strike) ((1/2,none) S W, π 0.0019) |
| G-asym-ctl/length | 0.970 | 0.311 | 0.650 | 0.644 | 0.947 | (0,none,0) | striker | scab ((0,none) S W, π 0.2210) |
| G-asym-ctl/uniform | 0.989 | 0.815 | 0.330 | 0.329 | 0.831 | (0,none,0)+(BOX(W1=strike) -> wage 1/2) | striker+(Q* -> strike) | T0+(Q* -> strike) ((1/2,none) S W, π 0.0120) |
| G-cred/length | 0.990 | 0.480 | 0.511 | 0.511 | 0.960 | (0,source,0) | striker | scab ((0,source) S W, π 0.0972) |
| G-cred/uniform | 0.990 | 0.990 | 0.003 | 0.003 | 0.056 | (0,none,0) | militant | scab ((0,none) S W, π 0.0007) |
| G-cred-ctl/length | 0.990 | 0.360 | 0.632 | 0.632 | 0.910 | (0,none,0) | striker | scab ((0,none) S W, π 0.2218) |
| G-cred-ctl/uniform | 0.990 | 0.990 | 0.001 | 0.001 | 0.002 | (0,none,0) | militant | scab ((0,none) S W, π 0.0006) |
| G-cred-whole/length | 0.989 | 0.989 | 4.6e-04 | 0.000 | 0.236 |  |
| G-cred-whole/uniform | 0.990 | 0.990 | 0.000 | 0.000 | 0.514 |  |
| G-cred-whole-ctl/length | 0.987 | 0.987 | 0.001 | 0.000 | 0.230 |  |
| G-cred-whole-ctl/uniform | 0.990 | 0.990 | 0.000 | 0.000 | 0.493 |  |
| G-recip/length | 0.990 | 0.471 | 0.520 | 0.520 | 0.963 | (0,source,0) | striker | scab ((0,source) S W, π 0.0982) |
| G-recip/uniform | 0.990 | 0.990 | 0.004 | 0.004 | 0.016 | (0,none,0) | militant | scab ((0,none) S W, π 0.0009) |
| G-recip-ctl/length | 0.990 | 0.348 | 0.644 | 0.644 | 0.925 | (0,none,0) | striker | scab ((0,none) S W, π 0.2265) |
| G-recip-ctl/uniform | 0.990 | 0.990 | 0.002 | 0.002 | 0.003 | (0,none,0) | tagged militant | scab ((0,none) S W, π 0.0008) |
| base-CC/length | 0.990 | 0.990 | 0.451 | 0.451 | 0.874 | (0,source,0) | striker | scab ((0,source) S W, π 0.0861) |
| base-CC/uniform | 0.992 | 0.992 | 0.002 | 0.002 | 0.017 | (0,source,0) | militant | scab ((0,source) S W, π 0.0018) |
| base-RC/length | 0.990 | 0.990 | 0.539 | 0.539 | 0.827 | (0,none,0) | striker | scab ((0,none) S W, π 0.2071) |
| base-RC/uniform | 0.992 | 0.992 | 0.002 | 0.002 | 0.005 | (0,none,0) | militant | scab ((0,none) S W, π 0.0022) |
| base-RR/length | 0.991 | 0.991 | 0.000 | 0.000 | 0.218 |  |
| base-RR/uniform | 0.994 | 0.994 | 0.000 | 0.000 | 0.000 |  |
| random/length | 0.984 | 0.473 | 0.511 | 0.510 | 0.972 | (0,source,0) | striker | scab ((0,source) S W, π 0.0967) |
| random/uniform | 0.990 | 0.964 | 0.051 | 0.051 | 0.963 | (0,source,0) | striker | scab ((0,source) S W, π 0.0012) |

## SG and the uniform-local kernel: targeted proposals at the top states (N = 10⁴)

- G-all/SG/uniform: strict proposals at the 8 top states [0, 0, 0, 0, 0, 0, 0, 0]; strict whack proposals 0; conservative whack proposals 0
- G-all/local/uniform: strict proposals at the 8 top states [0, 0, 0, 0, 0, 0, 0, 0]; strict whack proposals 0; conservative whack proposals 0
- G-cred/SG/length: strict proposals at the 8 top states [0, 0, 0, 0, 0, 0, 0, 0]; strict whack proposals 0; conservative whack proposals 0
- G-cred/SG/uniform: strict proposals at the 8 top states [0, 0, 0, 0, 0, 0, 0, 0]; strict whack proposals 0; conservative whack proposals 0
- G-cred/local/length: strict proposals at the 8 top states [0, 0, 0, 0, 0, 0, 0, 0]; strict whack proposals 0; conservative whack proposals 0
- G-cred/local/uniform: strict proposals at the 8 top states [0, 0, 0, 0, 0, 0, 0, 0]; strict whack proposals 0; conservative whack proposals 0
- G-cred-whole/SG/length: strict proposals at the 8 top states [0, 0, 0, 0, 0, 0, 0, 0]; strict whack proposals 0; conservative whack proposals 0
- G-cred-whole/SG/uniform: strict proposals at the 8 top states [0, 0, 0, 0, 0, 0, 0, 0]; strict whack proposals 0; conservative whack proposals 0
- G-cred-whole/local/length: strict proposals at the 8 top states [0, 0, 0, 0, 0, 0, 0, 0]; strict whack proposals 0; conservative whack proposals 0
- G-cred-whole/local/uniform: strict proposals at the 8 top states [0, 0, 0, 0, 0, 0, 0, 0]; strict whack proposals 0; conservative whack proposals 0

## Coalition kernel (labelled cell)

- G-all/Z: coalition striker+(BOX(OTHER=work) -> work) + striker+(BOX(s=1/2) -> work) (μ-product 5.4e-07), pair play (0,none) S S, boss response (0,none,0)+(BOX(W1=work) -> wage 1/2); N=100: ρ₂ 1.0e-04 (N²ρ₂ 1.000), sequential ρ 0.010 then 0.010; N=1000: ρ₂ 1.0e-06 (N²ρ₂ 1.000), sequential ρ 0.001 then 0.001
- G-all/Z_D0: coalition striker+(BOX(OTHER=work) -> work) + striker+(BOX(s=1/2) -> work) (μ-product 5.4e-07), pair play (0,none) S S, boss response (0,none,0)+(BOX(W1=work) -> wage 1/2); N=100: ρ₂ 1.0e-04 (N²ρ₂ 1.000), sequential ρ 0.010 then 0.010; N=1000: ρ₂ 1.0e-06 (N²ρ₂ 1.000), sequential ρ 0.001 then 0.001
- G-cred-whole/Z: coalition striker + striker (μ-product 0.227), pair play (0,none) S S, boss response (0,none,0)+(BOX(W1=work) -> wage 1/4); N=100: ρ₂ 1.0e-04 (N²ρ₂ 1.000), sequential ρ 0.010 then 0.010; N=1000: ρ₂ 1.0e-06 (N²ρ₂ 1.000), sequential ρ 0.001 then 0.001
- G-cred-whole/Z_D0: coalition striker + striker (μ-product 0.227), pair play (1/2,none) W W, boss response (0,none,0)+(BOX(W1=work) -> wage 1/4); N=100: ρ₂ 0.001 (N²ρ₂ 13.929), sequential ρ 0.139 then 0.010; N=1000: ρ₂ 1.4e-04 (N²ρ₂ 139.292), sequential ρ 0.139 then 0.001

## Lottery (ε = 0; (N, I) = (100, 64), mN = 1, 40 runs, length-prior seeds, CC)

| arm | runs closed | fair islands | ¼ | zero | strike | split | strike-whacker share at closure | whacks / encounter (trajectory) | strikes at s > 0 / encounter | at s = 0 |
|---|---|---|---|---|---|---|---|---|---|---|
| G-all | 40/40 | 0.000 | 0.025 | 0.800 | 0.000 | 0.175 | 0.046 | 0.0031 | 0.0063 | 0.2014 |
| G-cred | 40/40 | 0.000 | 0.000 | 0.825 | 0.000 | 0.175 | 0.064 | 0.0026 | 0.0045 | 0.1746 |
| G-asym | 40/40 | 0.000 | 0.025 | 0.875 | 0.000 | 0.100 | 0.036 | 0.0023 | 0.0042 | 0.1816 |
| G-recip | 40/40 | 0.000 | 0.000 | 0.975 | 0.000 | 0.025 | 0.019 | 0.0024 | 0.0039 | 0.1745 |

**SG innovation in the lottery (a different object: finite-ε innovation, {'N': 100, 'I': 16, 'mN': 1.0, 'gens': 2000, 'runs': 10, 'u_inn_per_birth': 0.0001})**:

| cell | fair (end) | ¼ (end) | zero (end) | fair (2nd half) | ¼ (2nd half) | zero (2nd half) | innovations / run |
|---|---|---|---|---|---|---|---|
| G-all/SG-innovation | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 968 |
| G-all/no-innovation | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0 |
| G-cred/SG-innovation | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 954 |
| G-cred/no-innovation | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0 |

## Fixed-role chicken (cap 2)

Filter: (BOX(THEM=St) -> Straight) removed (fired 520, failed 520); (BOX(THEM=St) -> Swerve) admitted (fired 552, failed 0); (BOX(THEM=Sw) -> Straight) admitted (fired 644, failed 0); (BOX(THEM=Sw) -> Swerve) removed (fired 584, failed 584).

Named states: R1 (St,0)|(Sw,0): G-all stable, G-cred stable; R1' (St,1)|(Sw,0): G-all unstable [[2, '(BOX(THEM=Sw) -> Straight)', 3.0]], G-cred unstable [[2, '(BOX(THEM=Sw) -> Straight)', 3.0]]; crash: G-all unstable [[1, '(BOX(THEM=St) -> Swerve)', 9.0]], G-cred unstable [[1, '(BOX(THEM=St) -> Swerve)', 9.0]]; dove: G-all unstable [[1, '(BOX(THEM=Sw) -> Straight)', 2.0]], G-cred unstable [[1, '(BOX(THEM=Sw) -> Straight)', 2.0]].

Encoding: (St,1)+firm plays as (St,0) everywhere: True.

| cell | R1 | R2 | crash | dove | units | top state | top exits |
|---|---|---|---|---|---|---|---|
| const/prior/length/1000 | 0.500 | 0.500 | 0.000 | 2.4e-261 | 2 | (St,0) | (Sw,0) (0.500) | 5.4e-262 Δ=-2.000 → dove; 0.000 Δ=-9.000 → crash |
| const/prior/length/10000 | 0.500 | 0.500 | 0.000 | 0.000 | 2 | (St,0) | (Sw,0) (0.500) | 0.000 Δ=-2.000 → dove; 0.000 Δ=-9.000 → crash |
| const/prior/uniform/1000 | 0.500 | 0.500 | 0.000 | 2.4e-261 | 2 | (St,0) | (Sw,0) (0.500) | 5.4e-262 Δ=-2.000 → dove; 0.000 Δ=-9.000 → crash |
| const/prior/uniform/10000 | 0.500 | 0.500 | 0.000 | 0.000 | 2 | (St,0) | (Sw,0) (0.500) | 0.000 Δ=-2.000 → dove; 0.000 Δ=-9.000 → crash |
| base/prior/length/1000 | 0.500 | 0.500 | 0.000 | 2.3e-261 | 3 | (St,0) | (Sw,0) (0.474) | 6.8e-06 Δ=0.000 → R1; 6.8e-06 Δ=0.000 → R1 |
| base/prior/length/10000 | 0.500 | 0.500 | 0.000 | 0.000 | 3 | (St,0) | (Sw,0) (0.474) | 6.8e-07 Δ=0.000 → R1; 6.8e-07 Δ=0.000 → R1 |
| base/prior/uniform/1000 | 0.500 | 0.500 | 0.000 | 1.2e-261 | 3 | (St,0) | (Sw,0) (0.250) | 1.3e-04 Δ=0.000 → R1; 1.3e-04 Δ=0.000 → R1 |
| base/prior/uniform/10000 | 0.500 | 0.500 | 0.000 | 0.000 | 3 | (St,0) | (Sw,0) (0.250) | 1.2e-05 Δ=0.000 → R1; 1.2e-05 Δ=0.000 → R1 |
| G-all/prior/length/1000 | 0.500 | 0.500 | 0.000 | 1.0e-05 | 12 | (Sw,0) | (St,0) (0.476) | 3.2e-06 Δ=0.000 → R2; 3.2e-06 Δ=0.000 → R2 |
| G-all/SG/length/1000 | 0.500 | 0.500 | 0.000 | 1.3e-05 | 36 | (St,0)+(BOX(THEM=Sw) -> Straight) | (Sw,0)+(BOX(THEM=St) -> Swerve) (0.208) | 1.2e-04 Δ=0.000 → R1; 1.2e-04 Δ=0.000 → R1 |
| G-all/local/length/1000 | 0.500 | 0.500 | 0.000 | 2.5e-04 | 36 | (St,0) | (Sw,0) (0.091) | 6.3e-05 Δ=0.000 → R1; 6.3e-05 Δ=0.000 → R1 |
| G-all/prior/length/10000 | 0.500 | 0.500 | 0.000 | 4.5e-06 | 12 | (Sw,0) | (St,0) (0.477) | 3.2e-07 Δ=0.000 → R2; 3.2e-07 Δ=0.000 → R2 |
| G-all/SG/length/10000 | 0.500 | 0.500 | 0.000 | 4.8e-06 | 36 | (St,0)+(BOX(THEM=Sw) -> Straight) | (Sw,0)+(BOX(THEM=St) -> Swerve) (0.208) | 1.2e-05 Δ=0.000 → R1; 1.2e-05 Δ=0.000 → R1 |
| G-all/local/length/10000 | 0.500 | 0.500 | 0.000 | 1.1e-04 | 36 | (St,0) | (Sw,0) (0.091) | 6.3e-06 Δ=0.000 → R1; 6.3e-06 Δ=0.000 → R1 |
| G-all/prior/uniform/1000 | 0.493 | 0.493 | 0.000 | 0.013 | 12 | (St,0) | (Sw,0) (0.123) | 5.1e-05 Δ=0.000 → R1; 5.1e-05 Δ=0.000 → R1 |
| G-all/SG/uniform/1000 | 0.495 | 0.495 | 0.000 | 0.009 | 36 | (St,0)+(BOX(THEM=Sw) -> Straight) | (St,1)+(BOX(THEM=Sw) -> Straight) (0.032) | 1.1e-05 Δ=0.000 → R1; 1.1e-05 Δ=0.000 → R1 |
| G-all/local/uniform/1000 | 0.496 | 0.496 | 0.000 | 0.007 | 36 | (St,1)+(BOX(THEM=Sw) -> Straight) | (St,0)+(BOX(THEM=Sw) -> Straight) (0.029) | 1.1e-05 Δ=0.000 → R2; 1.1e-05 Δ=0.000 → R2 |
| G-all/prior/uniform/10000 | 0.494 | 0.494 | 0.000 | 0.013 | 12 | (St,0) | (Sw,0) (0.123) | 5.1e-06 Δ=0.000 → R1; 5.1e-06 Δ=0.000 → R1 |
| G-all/SG/uniform/10000 | 0.496 | 0.496 | 0.000 | 0.009 | 36 | (St,1)+(BOX(THEM=Sw) -> Straight) | (St,0)+(BOX(THEM=Sw) -> Straight) (0.032) | 1.1e-06 Δ=0.000 → R2; 1.1e-06 Δ=0.000 → R2 |
| G-all/local/uniform/10000 | 0.497 | 0.497 | 0.000 | 0.007 | 36 | (St,1)+(BOX(THEM=Sw) -> Straight) | (St,0)+(BOX(THEM=Sw) -> Straight) (0.030) | 1.1e-06 Δ=0.000 → R2; 1.1e-06 Δ=0.000 → R2 |
| G-cred/prior/length/1000 | 0.500 | 0.500 | 0.000 | 2.3e-08 | 6 | (St,0) | (Sw,0) (0.480) | 3.0e-06 Δ=0.000 → R1; 3.0e-06 Δ=0.000 → R1 |
| G-cred/SG/length/1000 | 0.500 | 0.500 | 0.000 | 2.3e-08 | 15 | (Sw,0)+(BOX(THEM=St) -> Swerve) | (St,0)+(BOX(THEM=Sw) -> Straight) (0.214) | 1.2e-04 Δ=0.000 → R2; 1.2e-04 Δ=0.000 → R2 |
| G-cred/local/length/1000 | 0.500 | 0.500 | 0.000 | 9.0e-07 | 15 | (St,0)+(BOX(THEM=Sw) -> Straight)+(BOX(THEM=St) -> Swerve) | (St,0) (0.091) | 1.3e-04 Δ=0.000 → R2; 1.2e-04 Δ=0.000 → R2 |
| G-cred/prior/length/10000 | 0.500 | 0.500 | 0.000 | 2.3e-09 | 6 | (St,0) | (Sw,0) (0.480) | 3.0e-07 Δ=0.000 → R1; 3.0e-07 Δ=0.000 → R1 |
| G-cred/SG/length/10000 | 0.500 | 0.500 | 0.000 | 2.3e-09 | 15 | (St,0)+(BOX(THEM=Sw) -> Straight) | (Sw,0)+(BOX(THEM=St) -> Swerve) (0.214) | 1.2e-05 Δ=0.000 → R1; 1.2e-05 Δ=0.000 → R1 |
| G-cred/local/length/10000 | 0.500 | 0.500 | 0.000 | 8.6e-08 | 15 | (St,0) | (St,0)+(BOX(THEM=Sw) -> Straight)+(BOX(THEM=St) -> Swerve) (0.091) | 1.3e-05 Δ=0.000 → R1; 1.2e-05 Δ=0.000 → R1 |
| G-cred/prior/uniform/1000 | 0.500 | 0.500 | 0.000 | 1.2e-04 | 6 | (St,0) | (St,0)+(BOX(THEM=Sw) -> Straight)+(BOX(THEM=St) -> Swerve) (0.182) | 3.7e-05 Δ=0.000 → R1; 2.9e-05 Δ=0.000 → R1 |
| G-cred/SG/uniform/1000 | 0.500 | 0.500 | 0.000 | 1.3e-04 | 15 | (St,1)+(BOX(THEM=Sw) -> Straight) | (St,0)+(BOX(THEM=Sw) -> Straight) (0.114) | 7.4e-06 Δ=0.000 → R2; 7.4e-06 Δ=0.000 → R2 |
| G-cred/local/uniform/1000 | 0.500 | 0.500 | 0.000 | 7.4e-05 | 15 | (St,0)+(BOX(THEM=Sw) -> Straight) | (St,0)+(BOX(THEM=Sw) -> Straight)+(BOX(THEM=St) -> Swerve) (0.214) | 7.4e-06 Δ=0.000 → R1; 7.4e-06 Δ=0.000 → R1 |
| G-cred/prior/uniform/10000 | 0.500 | 0.500 | 0.000 | 1.2e-05 | 6 | (St,0) | (St,0)+(BOX(THEM=Sw) -> Straight)+(BOX(THEM=St) -> Swerve) (0.183) | 3.7e-06 Δ=0.000 → R1; 2.9e-06 Δ=0.000 → R1 |
| G-cred/SG/uniform/10000 | 0.500 | 0.500 | 0.000 | 1.3e-05 | 15 | (St,1)+(BOX(THEM=Sw) -> Straight) | (St,0)+(BOX(THEM=Sw) -> Straight) (0.114) | 7.4e-07 Δ=0.000 → R2; 7.4e-07 Δ=0.000 → R2 |
| G-cred/local/uniform/10000 | 0.500 | 0.500 | 0.000 | 7.2e-06 | 15 | (St,0)+(BOX(THEM=Sw) -> Straight)+(BOX(THEM=St) -> Swerve) | (St,0)+(BOX(THEM=Sw) -> Straight) (0.219) | 7.4e-07 Δ=0.000 → R2; 7.4e-07 Δ=0.000 → R2 |
| G-cred-ctl/prior/length/1000 | 1.0e-128 | 1.0e-128 | 0.000 | 1.000 | 3 | (Sw,0)+(BOX(THEM=Sw) -> Straight) | (Sw,0)+(BOX(THEM=Sw) -> Straight) (1.000) | 4.4e-132 Δ=-1.000 → R2; 4.4e-132 Δ=-1.000 → R1 |
| G-cred-ctl/prior/length/10000 | 0.000 | 0.000 | 0.000 | 1.000 | 3 | (Sw,0)+(BOX(THEM=Sw) -> Straight) | (Sw,0)+(BOX(THEM=Sw) -> Straight) (1.000) | 0.000 Δ=-1.000 → R2; 0.000 Δ=-1.000 → R1 |
| G-cred-ctl/prior/uniform/1000 | 1.0e-130 | 1.0e-130 | 0.000 | 1.000 | 3 | (Sw,0)+(BOX(THEM=Sw) -> Straight) | (Sw,0)+(BOX(THEM=Sw) -> Straight) (1.000) | 5.3e-133 Δ=-1.000 → R2; 5.3e-133 Δ=-1.000 → R1 |
| G-cred-ctl/prior/uniform/10000 | 0.000 | 0.000 | 0.000 | 1.000 | 3 | (Sw,0)+(BOX(THEM=Sw) -> Straight) | (Sw,0)+(BOX(THEM=Sw) -> Straight) (1.000) | 0.000 Δ=-1.000 → R2; 0.000 Δ=-1.000 → R1 |
| random/prior/length/1000 | 0.500 | 0.500 | 0.000 | 2.3e-08 | 6 | (St,0) | (Sw,0) (0.480) | 3.0e-06 Δ=0.000 → R1; 3.0e-06 Δ=0.000 → R1 |
| random/prior/length/10000 | 0.500 | 0.500 | 0.000 | 2.3e-09 | 6 | (St,0) | (Sw,0) (0.480) | 3.0e-07 Δ=0.000 → R1; 3.0e-07 Δ=0.000 → R1 |
| random/prior/uniform/1000 | 0.500 | 0.500 | 0.000 | 1.2e-04 | 6 | (St,0) | (St,0)+(BOX(THEM=Sw) -> Straight)+(BOX(THEM=St) -> Swerve) (0.182) | 3.7e-05 Δ=0.000 → R1; 2.9e-05 Δ=0.000 → R1 |
| random/prior/uniform/10000 | 0.500 | 0.500 | 0.000 | 1.2e-05 | 6 | (St,0) | (St,0)+(BOX(THEM=Sw) -> Straight)+(BOX(THEM=St) -> Swerve) (0.183) | 3.7e-06 Δ=0.000 → R1; 2.9e-06 Δ=0.000 → R1 |

| lottery cell | per-island establishment (R1 or R2) | run sd | role-1 share | patchwork runs |
|---|---|---|---|---|
| lottery/const/mN0 | 1.000 | 0.000 | 0.511 | 1.000 |
| lottery/const/mN1 | 0.963 | 0.018 | 0.489 | 1.000 |
| lottery/base/mN0 | 1.000 | 0.000 | 0.485 | 1.000 |
| lottery/base/mN1 | 0.998 | 0.006 | 0.465 | 0.525 |
| lottery/G-all/mN0 | 1.000 | 0.000 | 0.505 | 1.000 |
| lottery/G-all/mN1 | 0.996 | 0.010 | 0.415 | 0.275 |
| lottery/G-cred/mN0 | 1.000 | 0.000 | 0.510 | 1.000 |
| lottery/G-cred/mN1 | 0.996 | 0.013 | 0.401 | 0.275 |
| lottery/G-cred-ctl/mN0 | 0.431 | 0.069 | 0.521 | 1.000 |
| lottery/G-cred-ctl/mN1 | 0.000 | 0.000 | 0.000 | 0.000 |
| lottery/random/mN0 | 1.000 | 0.000 | 0.495 | 1.000 |
| lottery/random/mN1 | 1.000 | 0.000 | 0.531 | 0.300 |

## Not finished

G-all with the SG and uniform-local kernels under the length prior (N = 10³, 10⁴): the hybrid exploration on 9·10⁶ refined
unit triples, capped at 6·10⁴ states and 20 rounds, had not converged after 70 minutes (round 3, outcome-changing cut
0.85) and was stopped. Every other planned cell ran (76 of 80 SOG chain cells, all chicken cells, all lottery cells,
the coalition cell). Coalition ε\* in `runs/gene_arm/coalition_eps.json` (ρ₂ at N = 10⁴ is the product of the sequential
fixations, exact for the neutral pairs).

## Verdicts (scored against `predictions/2026-10-11-gene-arm.md`; N = 10⁴ unless stated)

Reference numbers. Same-catalogue references (uniform over the named catalogue / length): base-CC fair 0.894 / 0.093,
base-RC 0.907 / 0.123, base-RR ¼ 0.994 / 0.781. The enforcement run's reduced-chain numbers quoted by RE 1 (CC 0.31,
RC 0.55) are over 9 constants × {scab, militant, union}; the gene arm's base catalogue contains the probe bosses D₀
and D\* (two thirds of the boss bases), which carry the fair share under a uniform prior (as in RESULTS "Concessions",
D\* family 0.977).

| # | prediction | outcome |
|---|---|---|
| RS (a) | the asymmetry: the union may special-case a quorum, the boss may not special-case a threat | **not derived by any filter.** The per-point test rejects a strike at s > 0 exactly as it rejects an executed whack (the quorum gene fails at (¼, none) and under strike targeting); whole-program credibility is the RR rule and selects ¼ (0.48 uniform, 0.76 length) and zero wage, fair ≤ 3·10⁻⁴. Declared (G-asym), it changes fair by ≤ 0.003 against G-all under both priors: the gene grammar's whack genes never deter (a `BOX(W_j = strike)` trigger dies at world 1 against an accommodating worker); the committed whack lives in the bases, and removing it (G-asym-ctl) gives fair 0.037 / 0.026 |
| RS (b) | the proof device: no credible (Pareto-improving) deviation exists, else it would have been adopted as a fit gene | **fails as stated.** Under the length prior strictly gene-stable, Pareto-dominated states (zero-wage splits and strikes) hold 0.50–0.64 of π in every CC-executed arm (G-all 0.499, G-cred 0.511, G-recip 0.520); the improving move (a striker switching to work) is neutral for its carrier, so it is adopted by drift, not selected. It holds under G-cred-whole (0 gene-stable dominated triples in the whole catalogue; dominated π 5·10⁻⁴), an arm that never selects the fair wage; with weak improvements counted, dominated π falls to 0.001–0.007 under the length prior but stays at 0.03–0.15 in the uniform G-all, G-asym and RC cells (wage-faker states), and the catalogue keeps weakly gene-stable dominated triples (coordination failures that need both workers) |
| RE 1 | G-cred within 0.1 of CC's 0.31; G-cred-ctl and G-cred-whole within 0.1 of RC's 0.55 | **failed, both falsifier clauses fired**: G-cred 0.914 (≥ 0.45) and G-cred-whole 2·10⁻⁴ (≤ 0.4); G-cred-ctl 0.973. Against the same catalogue G-cred is within 0.02 of base-CC (0.894) and G-cred-ctl within 0.07 of base-RC (0.907). Mechanism: the filter's effect (G-all 0.012 → G-cred 0.914) is the removal of stage-1 wage fakers (C₁ `(BOX(W1 = strike), wage ½)`, the wage cut), not of whacks (G-asym 0.010); whole-program credibility is RR, not RC (hand-predicted) |
| RE 2 | G-all is CC with more fakers; fair ≤ CC's; length prior: every gene arm zero wage ≥ 0.4 | **number held for the CC arms with committed bases** (G-all 0.477, G-cred 0.452, G-asym 0.478, G-recip 0.445, random 0.463), **missed** for the base-commitment controls (0.28–0.30), G-all-RC (0.34) and G-cred-whole (0.24); fair ≤ CC held (0.012 uniform, 0.015 length); falsifier (G-all > RC) not fired. "More fakers" held, but the fakers are wage fakers; "the whack gene deters as in CC" failed (the gene never deters) |
| RE 3 | (G-cred, SG) ≥ (G-cred, prior) under the length prior, uniform-local in between; targeted SG proposes quorum strikes and concessions, never whacks | **failed on the numbers, falsifier not fired**: SG 0.018 vs prior 0.023 (−0.005), local 0.056 above both; uniform: 0.929 / 0.914 / 0.936. At the chains' top states the targeted half makes 0 strict proposals and 0 whack proposals in every SG cell (the whack clause of the falsifier did not fire); quorum and concession genes are inadmissible under G-cred. Both local kernels move zero-wage mass from splits to both-working (zero wage 0.45 → 0.61–0.62) by putting accommodation genes next to strikers: a mutation-support effect, matched by the untargeted kernel |
| RE 4 | gene-stability and Nash incomparable; the fair state gene-stable under G-cred-whole and unstable under G-all | **failed, falsifier fired** on the fair-state clause: F (and F_u) is gene-stable under G-all and gene-unstable under G-cred-whole (witness `(BOX(W1 = work), wage ¼)`: the rational militant works at w0 and the cut sticks, 1.5 > 1). Incomparability held (G-all: 3.2·10⁶ stable ∧ ¬Nash, 2.4·10⁶ Nash ∧ ¬stable triples; G-cred-whole 5.6·10⁶ Nash ∧ ¬stable); under G-cred and G-recip every Nash triple is gene-stable |
| RE 5 | at G-cred-whole's top states no strict one-gene improvement; exit from zero wage sequential through a neutral intermediate; the coalition kernel faster | **first clause held** (gene-stable mass 0.989 length / 0.990 uniform of 0.99 covered); **the exit is sequential, mechanism different**: a lone constant striker enters (0, none) \| scab \| scab neutrally (1.6·10⁻⁵ per event per slot) and the boss strictly raises to ¼ (the rational striker works at ¼), no quorum gene involved; **the coalition clause failed**: ρ₂ = ρ₁ρ₂′ (= 1/N² for the neutral pair) and ε\* = 21 (G-cred-whole) and 250–420 (G-all), so the coalition kernel is never faster at ε ≤ 1. Falsifier not fired |
| RE 6 | chicken: the firm gene fails, the norm survives through constants; the base-commitment control forms the norm through readers; G-cred matches the constants arm within 0.1 | **held except the control clause**: firm removed (520/520 firings fail), bridge and yield admitted; G-cred chain π(R1) = π(R2) = 0.5 (conventions ≥ 1 − 10⁻⁴), lottery establishment 1.000 (mN = 0) and 0.996 (mN = 1) against 1.000 / 0.963. **On the control (bases (Sw, b)) no norm forms**: two bridge readers swerve against each other, mutual swerve holds π = 1.000 and is absorbing, and lottery establishment is 0.43 (mN = 0) and 0 (mN = 1) |
| RE 7 | encoding invariance fails somewhere | **held**: all four named genes (their base encodings are unfiltered); `w_1` is not play-equivalent to (0, strike, p) (0.50 of encounter mass); invariant under G-cred-whole |
| RE 8 | G-recip: every gene-stable state Pareto-efficient, top states gene-stable, fair ≥ RC's share (uniform) | **failed, falsifier fired**: 45,014 gene-stable Pareto-dominated triples (prior mass 0.16; e.g. (0, source, 0) \| striker \| striker, left only by neutral reciprocal work genes) and 0.52 of the length-prior π on dominated, strictly gene-stable states; top states gene-stable held (0.99); fair 0.941 ≥ 0.553 under the uniform prior held, 0.020 under the length prior. G-recip still admits Z (zero wage, everyone working) and the committed-base fair and ¼ states: a Pareto restriction cannot choose among wages |
| RE 9 | the RS's claim: the costly strike survives where its execution is repaid; the whack only where untested | **held as scored**, with the reading that both commitments are fit while essentially untested: G-all (length / uniform) costly-strike carriers 0.35 / 0.88 of π, execution rate 0.0013 / 0.019, cost 0.43 / 0.50 per execution, carriers' mean payoff 0.022 / 0.012 against 0.003 / 0.006; whack carriers 0.63 / 0.81, execution rate 2·10⁻⁶ / 8·10⁻⁶, carriers 1.47 / 1.97 against 1.17 / 1.64. Lottery trajectories: 0.002–0.003 whacks and 0.004–0.006 strikes at s > 0 per encounter. The strike's advantage comes from the encounters where it is not executed |
| S1 | filter composition | **held** exactly (8 work genes, 8 whack-none genes; nothing vacuous) |
| S2 | G-cred-whole: ¼ ≥ 0.4, fair ≤ 0.05 (uniform); ¼ ≥ 0.5 (length) | **held** (0.484, 2·10⁻⁴; 0.762) |
| S3 | \|G-cred − G-all\| ≤ 0.05 | **failed, falsifier fired** under the uniform prior (0.914 vs 0.012: the filter removes the wage fakers); held under the length prior (0.023 vs 0.015) |
| S4 | G-cred-ctl ≥ G-cred + 0.1 (uniform) | **missed the number** (+0.059); falsifier (< 0.05) not fired |
| S5 | length: CC arms zero ≥ 0.4, fair ≤ 0.05 | **missed for the controls** (G-cred-ctl zero 0.28, fair 0.058; G-asym-ctl 0.30; G-recip-ctl 0.28); falsifier (fair > 0.1) not fired |
| S6 | \|G-asym − G-all\| ≤ 0.05 | **held** (0.003, 0.002) |
| S7 | SG and local within 0.05 of the prior kernel (G-cred) | **held** (length −0.005 / +0.033; uniform +0.015 / +0.022) |
| S8 | chicken: conventions ≥ 0.95 in every arm | **failed, falsifier fired** (G-cred-ctl: mutual swerve 1.000) |
| S9 | SOG lottery: zero ≥ 0.6, fair ≤ 0.1 | **held** (zero 0.80–0.975, fair 0 on every arm) |
| S10 | coalition ε\* ≥ 10⁻³ | **held** (ε\* ≥ 21) |
| S11 | scale guard fires at cap 2 | **held** (≥ 23,206 boss classes) |
| S12 | a dominated top state (π ≥ 0.05) with no strict gene improvement | **held** (G-all length: (0, source, 0) \| striker \| scab, π 0.094) |
| S13 | G-recip ≈ G-cred (chain ≤ 0.05; lottery ≤ 0.1) | chain **held** (0.941 vs 0.914; 0.020 vs 0.023); lottery **falsifier fired** (zero wage 0.975 vs 0.825) |
| S14 | the weak version removes every dominated gene-stable state | **failed, falsifier fired** (12,740 weakly gene-stable dominated triples in G-recip) |
| S15 | strike execution ≤ 0.2, whack ≤ 0.01 (G-all) | **held** (0.0013 / 0.019; 2·10⁻⁶ / 8·10⁻⁶) |

