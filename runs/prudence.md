# Prudence under world K: run report (`runs/prudence.json`, `runs/prudence-verdicts.md`, `runs/prudence-static.json`, `runs/prudence-validate.json`, `runs/prudence-extra.json`, rows `runs/prudence/cells_{main,ext}.json.gz`; notes `notes/prudence.md`; spec `specs/2026-10-21-prudence-world-k.md`; predictions `predictions/2026-10-21-prudence-world-k.md`)

Every number is an ε = 0 seed lottery (128 islands of 100, merged at generation 200) followed by a finite-(N = 12,800, horizon) re-injection diagnostic, never π. Cells: worlds L and K × arms A0, A52, A156 (fresh founders per 100 programs delivered by the tail's end) and SD52 (A52 with the sucker-depleted arrival prior), 20 runs per cell (replicates 0–19, the spec's cells) plus a declared precision extension (replicates 20–39), paired by founders and merge seed. The tail is 10,000 generations after the merge, the chase 2,000 without arrivals.

**Deviations.** (i) The first launch of the batch hung at 0% CPU from 12:33 on 21 October (a multiprocessing deadlock) with 5 of the 160 main runs unfinished; the RE killed it on 22 October and relaunched `batch.sh`, which reran the 5 missing main runs and then the extension. The runs are deterministic (counter-based draws), so rerun rows equal what the hung pool would have written; the hung log is kept as `runs/prudence/main.log.hung-2026-10-21`. (ii) Replicates 20–39 are a declared extension; verdicts are scored on 0–19 with 0–39 in brackets. (iii) The sucker-depleted control removes the uncertified unconditional cooperators the spec names (4,673 spellings, prior mass 0.3756) but leaves the rest of the sucker class (prior mass 0.5 before, 0.125 after), so it removes only part of the sucker residence (certified-sucker residence 0.10 against 0.14 in L, 0.11 against 0.33 in K at 40 runs); there is no sucker-depleted control at A = 156. (iv) My S7 second clause carried an arithmetic error (0.78 for 0.917). (v) `runs/prudence-extra.json` (post-hoc reads: identity after the merge, time-averaged sucker shares, the realized selection advantage, failures) is computed by `src/prudence_extra.py` after the first look at the tables and is descriptive.

**Reading of the post-hoc table** (`runs/prudence-extra.json`, 40 runs per cell): the time-averaged certified-sucker share over the tail is 0.014 (L A52), 0.033 (K A52), 0.044 and 0.042 (A156), 0.010 (SD52); uncertified suckers are about 0. The realized payoff advantage of prudent over unguarded target members, where both are present, is **negative** in every arm including A0 and SD52 (−0.01 to −0.04): membership in the target T (mutual with PrudentBot-H) is not pairwise compatibility. The premium is a fixed-list edge of 0.69 per arriving sucker, but suckers stand at a few percent of the population.

## Verdicts

Scored on replicates 0–19 (the spec's cells) with replicates 0–39 in brackets. Numbers at the tail's end (t = 10,000) unless
stated; the chase's end (t = 12,000) agrees unless stated. All finite-(N = 12,800, horizon) diagnostics, never π.
G = mean prudent-target share.

| # | prediction | outcome |
|---|---|---|
| RE 1 | PrudentBot's share rises with A (A52 ≥ A0 + 0.1 in L); falsifier: no rise in either world | **failed at A = 52, falsifier fired as worded.** Network T share falls (L −0.153 [−0.065], K −0.101 [−0.073]); PB's own tree −0.011 [−0.039] (L), −0.020 [−0.029] (K); prudent share −0.036 [−0.014] (L), +0.012 [+0.025] (K). At A = 156 the prudent share is higher than at A0, +0.146 [+0.189, bootstrap above 0] (L), +0.169 [+0.110] (K), sign tests p 0.58 [0.13] and 0.42 [0.38]; there is no sucker-depleted control at A = 156, so this rise is not attributable to the premium |
| RE 2 | off-target residence falls at A52 against A0 (paired); also judged against SD52 | **failed (falsifier fired in K; L mixed).** Paired A52 − A0: K +0.668 [+0.129] share·10³ generations, 16 of 20 pairs up (p 0.012) [32 of 40, p < 0.001]; L +0.245 [−0.001], 17 of 20 up (p 0.003) [33 of 40], the mean difference indistinguishable from 0 because a few A0 runs hold large residences. Against SD52: L −0.405 [−0.189] (p 0.04 [0.15]), K +0.241 [+0.117] (p 0.26 [0.27]) |
| RE 3 | the premium per sucker encounter is smaller in K than in L | **failed, falsifier fired (tie).** Fixed-list edge per arriving uncertified-sucker founder 0.6855 in both worlds (static 0.6828 in both; 0.8261 L vs 0.8244 K over H-state certified suckers). The encounter-weighted edge is noisy and not ordered: A52 L 2.63 [2.04] vs K 2.11 [3.24]; A156 L 0.81 [0.71] vs K 1.01 [0.81] |
| RE 4 | universal-open ≥ 0.9 at every A in both worlds; falsifier ≤ 0.75 at A52 | **held.** 19–20 of 20 in every cell [38–40 of 40]; lowest 0.95 |
| RE 5 | no clique takes the merged population in K (identity share < 0.05 at the end) | **held.** Identity share 0 at the tail's and the chase's end in all 160 K runs; 0 of 160 K runs ever ≥ 0.05 |
| RE 6 (sol) | terminal off-target failures not zero; PB responds more to sucker exposure than to total A; L stays vulnerable to cliques | (i) **held:** T < 0.95 at the tail's end in 0–4 of 20 per cell (A0: L 2, K 0; arrival arms 1–4) [2–8 of 40]; (ii) **not supported:** SD52 vs A52 differ by −0.015 [−0.011] (L) and +0.062 [+0.078] (K), none significant, and SD52 still carries 0.4–0.7 of A52's certified-sucker residence (the control is partial); (iii) **not observed:** identity after generation 250 ≤ 0.0009 in every run of both worlds |
| RE 7 (argon) | L at A156: universal-open < 0.85 | **failed.** 20 of 20 [40 of 40] |
| S1 | fixed-list edge per arriving sucker equal in K and L within 1% | **held** (relative difference 0; certified H-state 0.2%) |
| S2 | G(A52) ≥ 0.60, G(A156) ≥ 0.70, G(SD52) ≤ G(A0) + 0.15; R-reward in both worlds | **failed, falsifier fired.** G(A0, A52, A156, SD52) = 0.267, 0.231, 0.412, 0.246 (L) and 0.231, 0.243, 0.400, 0.181 (K) [0.241, 0.227, 0.429, 0.238 and 0.192, 0.217, 0.302, 0.139]. The G(A0) clause (within 0.1 of 0.25 / 0.20) held. Region: R-null in K at both times; in L the letter of the rule gives R-harm because G(A52) < G(A0) by 0.036 (within noise); read as R-null |
| S3 | T share at ceiling at A0; PB own tree rises < 0.10; prudent rises ≥ 0.25 | (a) **held**: T at A0 0.983 (L), 1.000 (K) [0.954, 0.970] and it does not rise; (b) **held**: PB's own tree falls; (c) **failed** (see S2) |
| S4 | universal-open ≥ 0.90 at A52, in [0.70, 0.95] at A156; coin flip on argon 7 | A52 **held**; A156 **failed** (falsifier ≥ 0.95 in L fired: 20 of 20, K 20 of 20) |
| S5 | off-target residence up in K at A52 over A0; in L down only if rep 5 is cured | **held in K** (above); L: no decrease in the mean |
| S6 | ≥ 0.8 of a prudent gain is arrival-descended; immigration credited with ≥ half of the change over 2,000 generations | **failed, falsifier fired.** Arrival-descended fraction of the tail-end prudent share 0.04 (L A52), 0.00 (L A156), 0.07 and 0.13 (K) [0.02–0.09]; over t ≤ 2,000 arrivals give +0.00–0.04 and residents +0.00–0.19 |
| S7 | realized arrivals within 3% of 128 A; 0.78 ± 0.03 delivered by t = 5,000 | clause 1 **held on 0–19** (max deviation 1.9%), **exceeded on 0–39** (3.25% at A52, one run in 80 draws, ratio 1.0015, no offset); clause 2 **failed by my arithmetic error**: the shape's cumulative share by 5,000 is 1000(1 − 1/6)/909 = 0.917 (measured 0.916); 0.78 was wrong |
| S8 | no K run ≥ 0.05 identity; at least one non-SD L arrival run ≥ 0.05 at some time | K **held**. L: the clause as worded is true only through the merge composition (15 of 40 L runs hold identity ≥ 0.05 at generation 200, mean 0.0615, in every arm including A0); after the merge identity is ≤ 0.0009 in every run, so no arrival-caused takeover occurred: **failed in intent** |
| S9 | loss: 0 of 20 at A0, ≤ 2 at A52, 1–6 at A156 per world, more at A156 than A52 | A0 0 [0] **held**; A52 L 1, K 0 [1, 1] **held**; A156 0 and 0 [L 0, K 2] **failed (falsifier: 0 in both worlds at 20)**, and A156 does not exceed A52 at 20. Whole-population losses are 5 of 240 arrival-arm runs against 0 of 80 A0 runs (K reps 22 and 27 at A156, K rep 22 at A52, L rep 2 at A52, L rep 30 at SD52) |
| S10 | K − L within ±0.15 in every arm on every paired endpoint | **held** (prudent ≤ 0.065, universal-open ≤ 0.05, T ≤ 0.094) |
| S11 | SD52 not worse than A52 on universal-open; G(SD52) lowest of the arrival arms | universal-open clause **held**; lowest-G clause **held in K, failed in L** (SD52 0.246 vs A52 0.231) |
| S12 | validation: A0 reproduces the stored cells; kernel equals the Pangaea kernel at ε = 0 | **held** (6 of 6 runs, 0 differences; the test passes) |

**Headline.** The tail does not reward prudence at A = 52 in either world (R-null / noise), and the A = 156 rise in the
prudent share (+0.11 to +0.19) cannot be separated from resilience because the sucker-depleted control exists only at
A = 52 and is itself only a partial depletion. World K does not shrink the premium on its primary measure.


## Tables, replicates 0–19

#### Delivered exposure

| world | arm | runs | expected | mean realized | range | ratio | max |dev| | frac by 5,000 | frac by 1,000 |
|---|---|---|---|---|---|---|---|---|---|
| L | A52 | 20 | 6656 | 6658 | 6529-6775 | 1.0004 | 0.0191 | 0.916 | 0.549 |
| L | A156 | 20 | 19968 | 19954 | 19686-20202 | 0.9993 | 0.0141 | 0.916 | 0.550 |
| L | SD52 | 20 | 6656 | 6658 | 6529-6775 | 1.0004 | 0.0191 | 0.916 | 0.549 |
| K | A52 | 20 | 6656 | 6658 | 6529-6775 | 1.0004 | 0.0191 | 0.916 | 0.549 |
| K | A156 | 20 | 19968 | 19954 | 19686-20202 | 0.9993 | 0.0141 | 0.916 | 0.550 |
| K | SD52 | 20 | 6656 | 6658 | 6529-6775 | 1.0004 | 0.0191 | 0.916 | 0.549 |

#### Endpoints at the tail end (t = 10,000)

| world | arm | runs | universal-open | T ≥ 0.95 | prudent ≥ 0.5 | lost | P(C,C) | T share | prudent share | unguarded share | PB own | off-target share | identity share | runs with identity ≥ 0.05 at some time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L | A0 | 20 | 20 | 18 | 5 | 0 | 1.000 | 0.983 | 0.267 | 0.716 | 0.050 | 0.0170 | 0.0000 | 1 |
| L | A52 | 20 | 19 | 16 | 5 | 1 | 0.950 | 0.830 | 0.231 | 0.599 | 0.039 | 0.0944 | 0.0000 | 1 |
| L | A156 | 20 | 20 | 19 | 8 | 0 | 1.000 | 0.950 | 0.412 | 0.537 | 0.050 | 0.0394 | 0.0000 | 1 |
| L | SD52 | 20 | 20 | 17 | 5 | 0 | 1.000 | 0.856 | 0.246 | 0.609 | 0.039 | 0.1444 | 0.0000 | 1 |
| K | A0 | 20 | 20 | 20 | 4 | 0 | 1.000 | 1.000 | 0.231 | 0.769 | 0.085 | 0.0000 | 0.0000 | 0 |
| K | A52 | 20 | 20 | 17 | 4 | 0 | 1.000 | 0.899 | 0.243 | 0.657 | 0.065 | 0.0755 | 0.0000 | 0 |
| K | A156 | 20 | 20 | 18 | 8 | 0 | 1.000 | 0.917 | 0.400 | 0.516 | 0.150 | 0.0824 | 0.0000 | 0 |
| K | SD52 | 20 | 20 | 19 | 3 | 0 | 1.000 | 0.950 | 0.181 | 0.769 | 0.060 | 0.0500 | 0.0000 | 0 |

#### Endpoints at the chase end (t = 12,000)

| world | arm | runs | universal-open | T ≥ 0.95 | prudent ≥ 0.5 | lost | P(C,C) | T share | prudent share | unguarded share | PB own | off-target share | identity share | runs with identity ≥ 0.05 at some time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L | A0 | 20 | 20 | 19 | 6 | 0 | 1.000 | 0.990 | 0.283 | 0.707 | 0.050 | 0.0097 | 0.0000 | 1 |
| L | A52 | 20 | 19 | 16 | 4 | 1 | 0.950 | 0.810 | 0.224 | 0.587 | 0.048 | 0.0981 | 0.0000 | 1 |
| L | A156 | 20 | 20 | 19 | 7 | 0 | 1.000 | 0.950 | 0.385 | 0.565 | 0.050 | 0.0357 | 0.0000 | 1 |
| L | SD52 | 20 | 20 | 17 | 5 | 0 | 1.000 | 0.852 | 0.255 | 0.597 | 0.048 | 0.1481 | 0.0000 | 1 |
| K | A0 | 20 | 20 | 20 | 5 | 0 | 1.000 | 1.000 | 0.234 | 0.766 | 0.099 | 0.0000 | 0.0000 | 0 |
| K | A52 | 20 | 20 | 17 | 5 | 0 | 1.000 | 0.891 | 0.222 | 0.669 | 0.051 | 0.0674 | 0.0000 | 0 |
| K | A156 | 20 | 20 | 18 | 7 | 0 | 1.000 | 0.924 | 0.388 | 0.535 | 0.150 | 0.0765 | 0.0000 | 0 |
| K | SD52 | 20 | 20 | 19 | 3 | 0 | 1.000 | 0.950 | 0.179 | 0.771 | 0.054 | 0.0500 | 0.0000 | 0 |

#### Paired differences (same founders and merge seed)

| world | contrast | time | statistic | pairs | mean diff | 95% bootstrap | + | − | sign / McNemar p |
|---|---|---|---|---|---|---|---|---|---|
| L | A52 − A0 | t=10000 | prud | 20 | -0.036 | [-0.263, 0.189] | 3 | 5 | 0.727 |
| L | A52 − A0 | t=10000 | T | 20 | -0.153 | [-0.316, -0.014] | 1 | 5 | 0.219 |
| L | A52 − A0 | t=10000 | pb | 20 | -0.011 | [-0.033, 0.000] | 0 | 1 | 1.000 |
| L | A52 − A0 | t=10000 | pcc | 20 | -0.050 | [-0.150, 0.000] | 0 | 2 | 0.500 |
| L | A52 − A0 | t=10000 | universal-open (McNemar) | 20 | -0.050 | - | 0 | 1 | 1.000 |
| L | A52 − A0 | t=12000 | prud | 20 | -0.059 | [-0.290, 0.169] | 3 | 5 | 0.727 |
| L | A52 − A0 | t=12000 | T | 20 | -0.180 | [-0.368, -0.031] | 1 | 4 | 0.375 |
| L | A52 − A0 | t=12000 | pb | 20 | -0.002 | [-0.006, 0.000] | 0 | 1 | 1.000 |
| L | A52 − A0 | t=12000 | pcc | 20 | -0.050 | [-0.150, 0.000] | 0 | 1 | 1.000 |
| L | A52 − A0 | t=12000 | universal-open (McNemar) | 20 | -0.050 | - | 0 | 1 | 1.000 |
| L | A156 − A0 | t=10000 | prud | 20 | 0.146 | [-0.060, 0.339] | 8 | 5 | 0.581 |
| L | A156 − A0 | t=10000 | T | 20 | -0.033 | [-0.116, 0.017] | 1 | 9 | 0.021 |
| L | A156 − A0 | t=10000 | pb | 20 | -0.000 | [-0.000, 0.000] | 0 | 1 | 1.000 |
| L | A156 − A0 | t=10000 | pcc | 20 | -0.000 | [-0.000, -0.000] | 0 | 7 | 0.016 |
| L | A156 − A0 | t=10000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |
| L | A156 − A0 | t=12000 | prud | 20 | 0.102 | [-0.110, 0.295] | 6 | 2 | 0.289 |
| L | A156 − A0 | t=12000 | T | 20 | -0.040 | [-0.127, 0.006] | 1 | 1 | 1.000 |
| L | A156 − A0 | t=12000 | pb | 20 | 0.000 | [0.000, 0.000] | 0 | 0 | 1.000 |
| L | A156 − A0 | t=12000 | pcc | 20 | 0.000 | [0.000, 0.000] | 0 | 0 | 1.000 |
| L | A156 − A0 | t=12000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |
| L | A52 − SD52 | t=10000 | prud | 20 | -0.015 | [-0.210, 0.173] | 5 | 3 | 0.727 |
| L | A52 − SD52 | t=10000 | T | 20 | -0.025 | [-0.175, 0.125] | 2 | 3 | 1.000 |
| L | A52 − SD52 | t=10000 | pb | 20 | 0.000 | [0.000, 0.000] | 0 | 0 | 1.000 |
| L | A52 − SD52 | t=10000 | pcc | 20 | -0.050 | [-0.150, 0.000] | 2 | 2 | 1.000 |
| L | A52 − SD52 | t=10000 | universal-open (McNemar) | 20 | -0.050 | - | 0 | 1 | 1.000 |
| L | A52 − SD52 | t=12000 | prud | 20 | -0.031 | [-0.215, 0.141] | 3 | 3 | 1.000 |
| L | A52 − SD52 | t=12000 | T | 20 | -0.042 | [-0.200, 0.108] | 1 | 2 | 1.000 |
| L | A52 − SD52 | t=12000 | pb | 20 | 0.000 | [0.000, 0.000] | 0 | 0 | 1.000 |
| L | A52 − SD52 | t=12000 | pcc | 20 | -0.050 | [-0.150, 0.000] | 0 | 1 | 1.000 |
| L | A52 − SD52 | t=12000 | universal-open (McNemar) | 20 | -0.050 | - | 0 | 1 | 1.000 |
| L | SD52 − A0 | t=10000 | prud | 20 | -0.020 | [-0.178, 0.125] | 2 | 4 | 0.688 |
| L | SD52 − A0 | t=10000 | T | 20 | -0.127 | [-0.267, -0.000] | 0 | 6 | 0.031 |
| L | SD52 − A0 | t=10000 | pb | 20 | -0.011 | [-0.033, 0.000] | 0 | 1 | 1.000 |
| L | SD52 − A0 | t=10000 | pcc | 20 | -0.000 | [-0.000, 0.000] | 0 | 3 | 0.250 |
| L | SD52 − A0 | t=10000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |
| L | SD52 − A0 | t=12000 | prud | 20 | -0.028 | [-0.187, 0.131] | 2 | 3 | 1.000 |
| L | SD52 − A0 | t=12000 | T | 20 | -0.138 | [-0.288, 0.000] | 0 | 3 | 0.250 |
| L | SD52 − A0 | t=12000 | pb | 20 | -0.002 | [-0.006, 0.000] | 0 | 1 | 1.000 |
| L | SD52 − A0 | t=12000 | pcc | 20 | 0.000 | [0.000, 0.000] | 0 | 0 | 1.000 |
| L | SD52 − A0 | t=12000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |
| L | A156 − A52 | t=10000 | prud | 20 | 0.181 | [-0.090, 0.439] | 10 | 3 | 0.092 |
| L | A156 − A52 | t=10000 | T | 20 | 0.119 | [-0.061, 0.303] | 5 | 6 | 1.000 |
| L | A156 − A52 | t=10000 | pb | 20 | 0.011 | [0.000, 0.033] | 1 | 0 | 1.000 |
| L | A156 − A52 | t=10000 | pcc | 20 | 0.050 | [-0.000, 0.150] | 2 | 5 | 0.453 |
| L | A156 − A52 | t=10000 | universal-open (McNemar) | 20 | 0.050 | - | 1 | 0 | 1.000 |
| L | A156 − A52 | t=12000 | prud | 20 | 0.161 | [-0.101, 0.428] | 8 | 3 | 0.227 |
| L | A156 − A52 | t=12000 | T | 20 | 0.140 | [-0.052, 0.338] | 4 | 1 | 0.375 |
| L | A156 − A52 | t=12000 | pb | 20 | 0.002 | [0.000, 0.006] | 1 | 0 | 1.000 |
| L | A156 − A52 | t=12000 | pcc | 20 | 0.050 | [0.000, 0.150] | 1 | 0 | 1.000 |
| L | A156 − A52 | t=12000 | universal-open (McNemar) | 20 | 0.050 | - | 1 | 0 | 1.000 |
| K | A52 − A0 | t=10000 | prud | 20 | 0.012 | [-0.150, 0.178] | 6 | 3 | 0.508 |
| K | A52 − A0 | t=10000 | T | 20 | -0.101 | [-0.226, -0.000] | 0 | 5 | 0.062 |
| K | A52 − A0 | t=10000 | pb | 20 | -0.020 | [-0.059, 0.000] | 0 | 1 | 1.000 |
| K | A52 − A0 | t=10000 | pcc | 20 | -0.000 | [-0.000, 0.000] | 0 | 2 | 0.500 |
| K | A52 − A0 | t=10000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |
| K | A52 − A0 | t=12000 | prud | 20 | -0.012 | [-0.195, 0.160] | 4 | 3 | 1.000 |
| K | A52 − A0 | t=12000 | T | 20 | -0.109 | [-0.251, 0.000] | 0 | 3 | 0.250 |
| K | A52 − A0 | t=12000 | pb | 20 | -0.048 | [-0.143, 0.000] | 0 | 1 | 1.000 |
| K | A52 − A0 | t=12000 | pcc | 20 | 0.000 | [0.000, 0.000] | 0 | 0 | 1.000 |
| K | A52 − A0 | t=12000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |
| K | A156 − A0 | t=10000 | prud | 20 | 0.169 | [-0.040, 0.390] | 9 | 5 | 0.424 |
| K | A156 − A0 | t=10000 | T | 20 | -0.083 | [-0.215, -0.000] | 0 | 11 | 0.001 |
| K | A156 − A0 | t=10000 | pb | 20 | 0.065 | [-0.000, 0.180] | 2 | 1 | 1.000 |
| K | A156 − A0 | t=10000 | pcc | 20 | -0.000 | [-0.000, -0.000] | 0 | 6 | 0.031 |
| K | A156 − A0 | t=10000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |
| K | A156 − A0 | t=12000 | prud | 20 | 0.154 | [-0.065, 0.382] | 8 | 3 | 0.227 |
| K | A156 − A0 | t=12000 | T | 20 | -0.076 | [-0.203, 0.000] | 0 | 2 | 0.500 |
| K | A156 − A0 | t=12000 | pb | 20 | 0.051 | [0.000, 0.152] | 2 | 0 | 0.500 |
| K | A156 − A0 | t=12000 | pcc | 20 | 0.000 | [0.000, 0.000] | 0 | 0 | 1.000 |
| K | A156 − A0 | t=12000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |
| K | A52 − SD52 | t=10000 | prud | 20 | 0.062 | [-0.152, 0.281] | 6 | 5 | 1.000 |
| K | A52 − SD52 | t=10000 | T | 20 | -0.051 | [-0.201, 0.100] | 1 | 5 | 0.219 |
| K | A52 − SD52 | t=10000 | pb | 20 | 0.005 | [-0.104, 0.119] | 1 | 1 | 1.000 |
| K | A52 − SD52 | t=10000 | pcc | 20 | 0.000 | [-0.000, 0.000] | 2 | 1 | 1.000 |
| K | A52 − SD52 | t=10000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |
| K | A52 − SD52 | t=12000 | prud | 20 | 0.042 | [-0.201, 0.280] | 5 | 4 | 1.000 |
| K | A52 − SD52 | t=12000 | T | 20 | -0.059 | [-0.225, 0.100] | 1 | 3 | 0.625 |
| K | A52 − SD52 | t=12000 | pb | 20 | -0.003 | [-0.146, 0.139] | 1 | 1 | 1.000 |
| K | A52 − SD52 | t=12000 | pcc | 20 | 0.000 | [0.000, 0.000] | 0 | 0 | 1.000 |
| K | A52 − SD52 | t=12000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |
| K | SD52 − A0 | t=10000 | prud | 20 | -0.050 | [-0.245, 0.132] | 5 | 5 | 1.000 |
| K | SD52 − A0 | t=10000 | T | 20 | -0.050 | [-0.150, -0.000] | 0 | 4 | 0.125 |
| K | SD52 − A0 | t=10000 | pb | 20 | -0.024 | [-0.119, 0.046] | 1 | 1 | 1.000 |
| K | SD52 − A0 | t=10000 | pcc | 20 | -0.000 | [-0.000, 0.000] | 0 | 3 | 0.250 |
| K | SD52 − A0 | t=10000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |
| K | SD52 − A0 | t=12000 | prud | 20 | -0.055 | [-0.266, 0.161] | 4 | 5 | 1.000 |
| K | SD52 − A0 | t=12000 | T | 20 | -0.050 | [-0.150, 0.000] | 0 | 1 | 1.000 |
| K | SD52 − A0 | t=12000 | pb | 20 | -0.045 | [-0.139, 0.004] | 1 | 1 | 1.000 |
| K | SD52 − A0 | t=12000 | pcc | 20 | 0.000 | [0.000, 0.000] | 0 | 0 | 1.000 |
| K | SD52 − A0 | t=12000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |
| K | A156 − A52 | t=10000 | prud | 20 | 0.158 | [-0.075, 0.388] | 9 | 5 | 0.424 |
| K | A156 − A52 | t=10000 | T | 20 | 0.017 | [-0.157, 0.176] | 4 | 8 | 0.388 |
| K | A156 − A52 | t=10000 | pb | 20 | 0.085 | [-0.000, 0.220] | 2 | 1 | 1.000 |
| K | A156 − A52 | t=10000 | pcc | 20 | -0.000 | [-0.000, -0.000] | 1 | 5 | 0.219 |
| K | A156 − A52 | t=10000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |
| K | A156 − A52 | t=12000 | prud | 20 | 0.166 | [-0.081, 0.413] | 8 | 3 | 0.227 |
| K | A156 − A52 | t=12000 | T | 20 | 0.033 | [-0.135, 0.201] | 3 | 2 | 1.000 |
| K | A156 − A52 | t=12000 | pb | 20 | 0.099 | [0.000, 0.246] | 2 | 0 | 0.500 |
| K | A156 − A52 | t=12000 | pcc | 20 | 0.000 | [0.000, 0.000] | 0 | 0 | 1.000 |
| K | A156 − A52 | t=12000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |

#### World K minus world L (paired founders)

| arm | time | statistic | pairs | mean diff | 95% bootstrap | K>L | K<L | p |
|---|---|---|---|---|---|---|---|---|
| A0 | t=10000 | prud | 20 | -0.036 | [-0.248, 0.160] | 4 | 4 | 1.000 |
| A0 | t=10000 | T | 20 | 0.017 | [0.000, 0.045] | 2 | 0 | 0.500 |
| A0 | t=10000 | pcc | 20 | 0.000 | [0.000, 0.000] | 0 | 0 | 1.000 |
| A0 | t=10000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |
| A0 | t=12000 | prud | 20 | -0.049 | [-0.279, 0.176] | 4 | 4 | 1.000 |
| A0 | t=12000 | T | 20 | 0.010 | [0.000, 0.027] | 2 | 0 | 0.500 |
| A0 | t=12000 | pcc | 20 | 0.000 | [0.000, 0.000] | 0 | 0 | 1.000 |
| A0 | t=12000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |
| A52 | t=10000 | prud | 20 | 0.011 | [-0.199, 0.227] | 6 | 5 | 1.000 |
| A52 | t=10000 | T | 20 | 0.069 | [-0.125, 0.269] | 3 | 3 | 1.000 |
| A52 | t=10000 | pcc | 20 | 0.050 | [-0.000, 0.150] | 1 | 1 | 1.000 |
| A52 | t=10000 | universal-open (McNemar) | 20 | 0.050 | - | 1 | 0 | 1.000 |
| A52 | t=12000 | prud | 20 | -0.002 | [-0.244, 0.234] | 5 | 5 | 1.000 |
| A52 | t=12000 | T | 20 | 0.081 | [-0.104, 0.292] | 3 | 2 | 1.000 |
| A52 | t=12000 | pcc | 20 | 0.050 | [0.000, 0.150] | 1 | 0 | 1.000 |
| A52 | t=12000 | universal-open (McNemar) | 20 | 0.050 | - | 1 | 0 | 1.000 |
| A156 | t=10000 | prud | 20 | -0.012 | [-0.250, 0.233] | 7 | 6 | 1.000 |
| A156 | t=10000 | T | 20 | -0.033 | [-0.184, 0.117] | 2 | 4 | 0.688 |
| A156 | t=10000 | pcc | 20 | 0.000 | [-0.000, 0.000] | 2 | 1 | 1.000 |
| A156 | t=10000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |
| A156 | t=12000 | prud | 20 | 0.003 | [-0.234, 0.236] | 5 | 5 | 1.000 |
| A156 | t=12000 | T | 20 | -0.026 | [-0.179, 0.124] | 1 | 2 | 1.000 |
| A156 | t=12000 | pcc | 20 | 0.000 | [0.000, 0.000] | 0 | 0 | 1.000 |
| A156 | t=12000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |
| SD52 | t=10000 | prud | 20 | -0.065 | [-0.295, 0.169] | 5 | 5 | 1.000 |
| SD52 | t=10000 | T | 20 | 0.094 | [-0.100, 0.289] | 3 | 2 | 1.000 |
| SD52 | t=10000 | pcc | 20 | -0.000 | [-0.000, 0.000] | 0 | 1 | 1.000 |
| SD52 | t=10000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |
| SD52 | t=12000 | prud | 20 | -0.076 | [-0.311, 0.163] | 4 | 5 | 1.000 |
| SD52 | t=12000 | T | 20 | 0.098 | [-0.100, 0.294] | 3 | 1 | 0.625 |
| SD52 | t=12000 | pcc | 20 | 0.000 | [0.000, 0.000] | 0 | 0 | 1.000 |
| SD52 | t=12000 | universal-open (McNemar) | 20 | 0.000 | - | 0 | 0 | 1.000 |

#### Outcome regions (G = mean prudent-target share)

| world | time | G(A0) | G(A52) | G(A156) | G(SD52) | universal-open(A52) | region |
|---|---|---|---|---|---|---|---|
| L | t=10000 | 0.267 | 0.231 | 0.412 | 0.246 | 0.950 | R-harm |
| L | t=12000 | 0.283 | 0.224 | 0.385 | 0.255 | 0.950 | R-harm |
| K | t=10000 | 0.231 | 0.243 | 0.400 | 0.181 | 1.000 | R-null |
| K | t=12000 | 0.234 | 0.222 | 0.388 | 0.179 | 1.000 | R-harm |

#### Residence over the tail (share · 1,000 generations; runs with positive residence in brackets)

| world | arm | off-target (CBo) | certified suckers | uncertified suckers | identity | prudent target |
|---|---|---|---|---|---|---|
| L | A0 | 0.374 (8) | 0.000 (0) | 0.000 (0) | 0.000 (11) | 2.511 (17) |
| L | A52 | 0.619 (20) | 0.166 (20) | 0.008 (20) | 0.000 (16) | 2.259 (20) |
| L | A156 | 0.312 (20) | 0.592 (20) | 0.000 (20) | 0.000 (20) | 3.996 (20) |
| L | SD52 | 1.025 (20) | 0.028 (20) | 0.000 (20) | 0.000 (17) | 2.144 (20) |
| K | A0 | 0.094 (12) | 0.000 (1) | 0.000 (0) | 0.000 (0) | 2.273 (18) |
| K | A52 | 0.762 (20) | 0.348 (20) | 0.000 (20) | 0.000 (0) | 2.885 (20) |
| K | A156 | 0.645 (20) | 0.460 (20) | 0.000 (20) | 0.000 (0) | 3.987 (20) |
| K | SD52 | 0.522 (20) | 0.125 (20) | 0.000 (20) | 0.000 (0) | 1.881 (20) |

#### Paired off-target residence difference (share · 1,000 generations)

| world | contrast | pairs | mean | 95% bootstrap | + | − | sign p |
|---|---|---|---|---|---|---|---|
| L | A52 − A0 | 20 | 0.245 | [-0.252, 0.990] | 17 | 3 | 0.003 |
| L | A52 − SD52 | 20 | -0.405 | [-1.223, 0.028] | 5 | 15 | 0.041 |
| L | A156 − A0 | 20 | -0.062 | [-0.607, 0.452] | 15 | 5 | 0.041 |
| K | A52 − A0 | 20 | 0.668 | [0.008, 1.618] | 16 | 4 | 0.012 |
| K | A52 − SD52 | 20 | 0.241 | [-0.829, 1.292] | 7 | 13 | 0.263 |
| K | A156 − A0 | 20 | 0.551 | [-0.063, 1.402] | 14 | 6 | 0.115 |

#### The premium: fixed-list edge per arriving sucker (primary), encounter-weighted edge integrated over the tail per A (secondary)

| world | arm | edge per arriving uncertified-sucker founder (H-state) | sucker arrivals / run | edge per 100 programs | edge per arriving SD founder | encounter edge · generations / A | of which certified suckers |
|---|---|---|---|---|---|---|---|
| L | A52 | 0.6855 | 3332 | 34.316 | 0.8291 | 2.632 | 2.632 |
| L | A156 | 0.6854 | 9951 | 34.158 | 0.8275 | 0.815 | 0.815 |
| L | SD52 | 0.2555 | 1319 | 5.063 | 0.0000 | 0.108 | 0.108 |
| K | A52 | 0.6855 | 3332 | 34.316 | 0.8291 | 2.115 | 2.115 |
| K | A156 | 0.6854 | 9951 | 34.158 | 0.8275 | 1.014 | 1.014 |
| K | SD52 | 0.2555 | 1319 | 5.063 | 0.0000 | 0.121 | 0.121 |

Static fixed-list edges (`runs/prudence-static.json`): {"L": {"suckerE": {"H": 0.6828319502074689, "E": 0.0, "mass": 0.5}, "SD": {"H": 0.825479026411186, "E": 0.0, "mass": 0.3755835062240664}, "suckerH_cert": {"H": 0.8260671426401336, "E": 0.0, "mass": 0.42680238589211617}, "Q": {"H_mean": 0.0, "E_mean": 0.0, "n": 10}}, "K": {"suckerE": {"H": 0.6828319502074689, "E": 0.0, "mass": 0.5}, "SD": {"H": 0.825479026411186, "E": 0.0, "mass": 0.3755835062240664}, "suckerH_cert": {"H": 0.8244390539721043, "E": 0.0, "mass": 0.4276452282157676}, "Q": {"H_mean": 0.0, "E_mean": 0.0, "n": 10}}}

#### Ancestry of the prudent share (gain = tail-end prudent share minus its value at the merge ≥ 0.25)

| world | arm | runs with gain ≥ 0.25 | arrival-descended fraction of the tail-end prudent share | Δ prudent share from arrivals, t = 0 → 2,000 | Δ from residents |
|---|---|---|---|---|---|
| L | A52 | 5 | 0.039 | 0.004 | 0.014 |
| L | A156 | 8 | 0.000 | 0.036 | 0.161 |
| L | SD52 | 5 | 0.000 | 0.006 | 0.022 |
| K | A52 | 4 | 0.067 | 0.012 | 0.034 |
| K | A156 | 8 | 0.130 | 0.013 | 0.188 |
| K | SD52 | 3 | 0.000 | 0.016 | -0.020 |

#### Arrival lineages that reached half of the population

| world | arm | lineages | runs | selected (arrival payoff above the mean) | drift | prudent-target arrivals | Q arrivals | sucker arrivals |
|---|---|---|---|---|---|---|---|---|
| L | A52 | 6 | 4 | 2 | 4 | 1 | 0 | 4 |
| L | A156 | 3 | 3 | 0 | 3 | 3 | 0 | 2 |
| L | SD52 | 1 | 1 | 0 | 1 | 0 | 0 | 0 |
| K | A52 | 2 | 2 | 0 | 2 | 1 | 0 | 2 |
| K | A156 | 3 | 3 | 0 | 3 | 2 | 0 | 3 |
| K | SD52 | 1 | 1 | 0 | 1 | 1 | 0 | 1 |

#### Composition at the merge (generation 200; A0 rows, identical across arms)

| world | runs | P(C,C) | T | prudent | unguarded | PB own | off-target | certified suckers | uncertified suckers | identity | AP | living types |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L | 20 | 0.715 | 0.786 | 0.184 | 0.602 | 0.029 | 0.064 | 0.000 | 0.000 | 0.054 | 0.013 | 28 |
| K | 20 | 0.764 | 0.804 | 0.219 | 0.585 | 0.040 | 0.083 | 0.000 | 0.000 | 0.000 | 0.007 | 32 |

#### Plurality type at the chase's end, and plurality changes over the tail

| world | arm | runs | plurality in T | plurality guarded | plurality PB tree | mean plurality-spelling changes (samples) |
|---|---|---|---|---|---|---|
| L | A0 | 20 | 20 | 6 | 1 | 17.8 |
| L | A52 | 20 | 16 | 4 | 1 | 16.8 |
| L | A156 | 20 | 19 | 7 | 1 | 15.3 |
| L | SD52 | 20 | 17 | 5 | 1 | 18.6 |
| K | A0 | 20 | 20 | 5 | 2 | 18.4 |
| K | A52 | 20 | 18 | 5 | 1 | 21.9 |
| K | A156 | 20 | 18 | 7 | 3 | 20.4 |
| K | SD52 | 20 | 19 | 3 | 1 | 20.7 |


## Tables, replicates 0–39

#### Delivered exposure

| world | arm | runs | expected | mean realized | range | ratio | max |dev| | frac by 5,000 | frac by 1,000 |
|---|---|---|---|---|---|---|---|---|---|
| L | A52 | 40 | 6656 | 6666 | 6529-6872 | 1.0015 | 0.0325 | 0.916 | 0.550 |
| L | A156 | 40 | 19968 | 19966 | 19561-20417 | 0.9999 | 0.0225 | 0.916 | 0.550 |
| L | SD52 | 40 | 6656 | 6666 | 6529-6872 | 1.0015 | 0.0325 | 0.916 | 0.550 |
| K | A52 | 40 | 6656 | 6666 | 6529-6872 | 1.0015 | 0.0325 | 0.916 | 0.550 |
| K | A156 | 40 | 19968 | 19966 | 19561-20417 | 0.9999 | 0.0225 | 0.916 | 0.550 |
| K | SD52 | 40 | 6656 | 6666 | 6529-6872 | 1.0015 | 0.0325 | 0.916 | 0.550 |

#### Endpoints at the tail end (t = 10,000)

| world | arm | runs | universal-open | T ≥ 0.95 | prudent ≥ 0.5 | lost | P(C,C) | T share | prudent share | unguarded share | PB own | off-target share | identity share | runs with identity ≥ 0.05 at some time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L | A0 | 40 | 40 | 35 | 8 | 0 | 1.000 | 0.954 | 0.241 | 0.713 | 0.082 | 0.0459 | 0.0000 | 4 |
| L | A52 | 40 | 39 | 35 | 8 | 1 | 0.975 | 0.889 | 0.227 | 0.662 | 0.043 | 0.0722 | 0.0000 | 4 |
| L | A156 | 40 | 40 | 35 | 17 | 0 | 1.000 | 0.935 | 0.429 | 0.505 | 0.090 | 0.0508 | 0.0000 | 4 |
| L | SD52 | 40 | 39 | 35 | 9 | 1 | 0.975 | 0.878 | 0.238 | 0.640 | 0.044 | 0.0972 | 0.0000 | 4 |
| K | A0 | 40 | 40 | 38 | 7 | 0 | 1.000 | 0.970 | 0.192 | 0.778 | 0.061 | 0.0305 | 0.0000 | 0 |
| K | A52 | 40 | 39 | 32 | 8 | 1 | 0.975 | 0.897 | 0.217 | 0.680 | 0.033 | 0.0462 | 0.0000 | 0 |
| K | A156 | 40 | 38 | 33 | 12 | 2 | 0.950 | 0.876 | 0.302 | 0.574 | 0.075 | 0.0534 | 0.0000 | 0 |
| K | SD52 | 40 | 40 | 38 | 6 | 0 | 1.000 | 0.957 | 0.139 | 0.818 | 0.030 | 0.0426 | 0.0000 | 0 |

#### Endpoints at the chase end (t = 12,000)

| world | arm | runs | universal-open | T ≥ 0.95 | prudent ≥ 0.5 | lost | P(C,C) | T share | prudent share | unguarded share | PB own | off-target share | identity share | runs with identity ≥ 0.05 at some time |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L | A0 | 40 | 40 | 37 | 10 | 0 | 1.000 | 0.967 | 0.247 | 0.721 | 0.093 | 0.0325 | 0.0000 | 4 |
| L | A52 | 40 | 39 | 35 | 8 | 1 | 0.975 | 0.880 | 0.219 | 0.661 | 0.058 | 0.0740 | 0.0000 | 4 |
| L | A156 | 40 | 40 | 36 | 15 | 0 | 1.000 | 0.944 | 0.396 | 0.548 | 0.076 | 0.0455 | 0.0000 | 4 |
| L | SD52 | 40 | 39 | 35 | 9 | 1 | 0.975 | 0.876 | 0.231 | 0.645 | 0.049 | 0.0990 | 0.0000 | 4 |
| K | A0 | 40 | 40 | 38 | 8 | 0 | 1.000 | 0.972 | 0.190 | 0.782 | 0.072 | 0.0285 | 0.0000 | 0 |
| K | A52 | 40 | 39 | 33 | 9 | 1 | 0.975 | 0.902 | 0.212 | 0.690 | 0.026 | 0.0379 | 0.0000 | 0 |
| K | A156 | 40 | 38 | 34 | 11 | 2 | 0.950 | 0.885 | 0.297 | 0.588 | 0.075 | 0.0386 | 0.0000 | 0 |
| K | SD52 | 40 | 40 | 37 | 6 | 0 | 1.000 | 0.958 | 0.151 | 0.807 | 0.027 | 0.0417 | 0.0000 | 0 |

#### Paired differences (same founders and merge seed)

| world | contrast | time | statistic | pairs | mean diff | 95% bootstrap | + | − | sign / McNemar p |
|---|---|---|---|---|---|---|---|---|---|
| L | A52 − A0 | t=10000 | prud | 40 | -0.014 | [-0.129, 0.099] | 7 | 7 | 1.000 |
| L | A52 − A0 | t=10000 | T | 40 | -0.065 | [-0.170, 0.034] | 3 | 8 | 0.227 |
| L | A52 − A0 | t=10000 | pb | 40 | -0.039 | [-0.101, 0.008] | 1 | 4 | 0.375 |
| L | A52 − A0 | t=10000 | pcc | 40 | -0.025 | [-0.075, 0.000] | 0 | 3 | 0.250 |
| L | A52 − A0 | t=10000 | universal-open (McNemar) | 40 | -0.025 | - | 0 | 1 | 1.000 |
| L | A52 − A0 | t=12000 | prud | 40 | -0.028 | [-0.158, 0.101] | 5 | 7 | 0.774 |
| L | A52 − A0 | t=12000 | T | 40 | -0.087 | [-0.205, 0.016] | 3 | 5 | 0.727 |
| L | A52 − A0 | t=12000 | pb | 40 | -0.035 | [-0.113, 0.036] | 1 | 4 | 0.375 |
| L | A52 − A0 | t=12000 | pcc | 40 | -0.025 | [-0.075, 0.000] | 0 | 1 | 1.000 |
| L | A52 − A0 | t=12000 | universal-open (McNemar) | 40 | -0.025 | - | 0 | 1 | 1.000 |
| L | A156 − A0 | t=10000 | prud | 40 | 0.189 | [0.062, 0.320] | 15 | 7 | 0.134 |
| L | A156 − A0 | t=10000 | T | 40 | -0.019 | [-0.065, 0.012] | 2 | 17 | 0.001 |
| L | A156 − A0 | t=10000 | pb | 40 | 0.008 | [-0.060, 0.070] | 2 | 2 | 1.000 |
| L | A156 − A0 | t=10000 | pcc | 40 | -0.000 | [-0.000, -0.000] | 0 | 11 | 0.001 |
| L | A156 − A0 | t=10000 | universal-open (McNemar) | 40 | 0.000 | - | 0 | 0 | 1.000 |
| L | A156 − A0 | t=12000 | prud | 40 | 0.149 | [0.023, 0.281] | 12 | 3 | 0.035 |
| L | A156 − A0 | t=12000 | T | 40 | -0.023 | [-0.071, 0.002] | 1 | 3 | 0.625 |
| L | A156 − A0 | t=12000 | pb | 40 | -0.017 | [-0.075, 0.021] | 2 | 1 | 1.000 |
| L | A156 − A0 | t=12000 | pcc | 40 | 0.000 | [0.000, 0.000] | 0 | 0 | 1.000 |
| L | A156 − A0 | t=12000 | universal-open (McNemar) | 40 | 0.000 | - | 0 | 0 | 1.000 |
| L | A52 − SD52 | t=10000 | prud | 40 | -0.011 | [-0.166, 0.142] | 11 | 7 | 0.481 |
| L | A52 − SD52 | t=10000 | T | 40 | 0.011 | [-0.101, 0.125] | 6 | 6 | 1.000 |
| L | A52 − SD52 | t=10000 | pb | 40 | -0.001 | [-0.067, 0.055] | 2 | 1 | 1.000 |
| L | A52 − SD52 | t=10000 | pcc | 40 | 0.000 | [-0.075, 0.075] | 4 | 2 | 0.688 |
| L | A52 − SD52 | t=10000 | universal-open (McNemar) | 40 | 0.000 | - | 1 | 1 | 1.000 |
| L | A52 − SD52 | t=12000 | prud | 40 | -0.011 | [-0.164, 0.147] | 8 | 7 | 1.000 |
| L | A52 − SD52 | t=12000 | T | 40 | 0.004 | [-0.113, 0.125] | 3 | 3 | 1.000 |
| L | A52 − SD52 | t=12000 | pb | 40 | 0.009 | [-0.060, 0.074] | 2 | 1 | 1.000 |
| L | A52 − SD52 | t=12000 | pcc | 40 | 0.000 | [-0.075, 0.075] | 1 | 1 | 1.000 |
| L | A52 − SD52 | t=12000 | universal-open (McNemar) | 40 | 0.000 | - | 1 | 1 | 1.000 |
| L | SD52 − A0 | t=10000 | prud | 40 | -0.003 | [-0.144, 0.135] | 7 | 8 | 1.000 |
| L | SD52 − A0 | t=10000 | T | 40 | -0.076 | [-0.170, -0.000] | 2 | 8 | 0.109 |
| L | SD52 − A0 | t=10000 | pb | 40 | -0.038 | [-0.120, 0.030] | 1 | 3 | 0.625 |
| L | SD52 − A0 | t=10000 | pcc | 40 | -0.025 | [-0.075, -0.000] | 0 | 6 | 0.031 |
| L | SD52 − A0 | t=10000 | universal-open (McNemar) | 40 | -0.025 | - | 0 | 1 | 1.000 |
| L | SD52 − A0 | t=12000 | prud | 40 | -0.016 | [-0.162, 0.115] | 7 | 7 | 1.000 |
| L | SD52 − A0 | t=12000 | T | 40 | -0.091 | [-0.188, -0.018] | 1 | 4 | 0.375 |
| L | SD52 − A0 | t=12000 | pb | 40 | -0.044 | [-0.125, 0.013] | 1 | 3 | 0.625 |
| L | SD52 − A0 | t=12000 | pcc | 40 | -0.025 | [-0.075, 0.000] | 0 | 1 | 1.000 |
| L | SD52 − A0 | t=12000 | universal-open (McNemar) | 40 | -0.025 | - | 0 | 1 | 1.000 |
| L | A156 − A52 | t=10000 | prud | 40 | 0.202 | [0.042, 0.358] | 17 | 6 | 0.035 |
| L | A156 − A52 | t=10000 | T | 40 | 0.046 | [-0.073, 0.166] | 7 | 14 | 0.189 |
| L | A156 − A52 | t=10000 | pb | 40 | 0.047 | [-0.021, 0.131] | 4 | 1 | 0.375 |
| L | A156 − A52 | t=10000 | pcc | 40 | 0.025 | [-0.000, 0.075] | 3 | 9 | 0.146 |
| L | A156 − A52 | t=10000 | universal-open (McNemar) | 40 | 0.025 | - | 1 | 0 | 1.000 |
| L | A156 − A52 | t=12000 | prud | 40 | 0.177 | [0.017, 0.347] | 13 | 5 | 0.096 |
| L | A156 − A52 | t=12000 | T | 40 | 0.064 | [-0.057, 0.191] | 5 | 4 | 1.000 |
| L | A156 − A52 | t=12000 | pb | 40 | 0.018 | [-0.058, 0.108] | 3 | 2 | 1.000 |
| L | A156 − A52 | t=12000 | pcc | 40 | 0.025 | [0.000, 0.075] | 1 | 0 | 1.000 |
| L | A156 − A52 | t=12000 | universal-open (McNemar) | 40 | 0.025 | - | 1 | 0 | 1.000 |
| K | A52 − A0 | t=10000 | prud | 40 | 0.025 | [-0.116, 0.168] | 10 | 7 | 0.629 |
| K | A52 − A0 | t=10000 | T | 40 | -0.073 | [-0.173, 0.019] | 1 | 12 | 0.003 |
| K | A52 − A0 | t=10000 | pb | 40 | -0.029 | [-0.076, 0.000] | 0 | 2 | 0.500 |
| K | A52 − A0 | t=10000 | pcc | 40 | -0.025 | [-0.075, -0.000] | 0 | 4 | 0.125 |
| K | A52 − A0 | t=10000 | universal-open (McNemar) | 40 | -0.025 | - | 0 | 1 | 1.000 |
| K | A52 − A0 | t=12000 | prud | 40 | 0.022 | [-0.131, 0.180] | 8 | 7 | 1.000 |
| K | A52 − A0 | t=12000 | T | 40 | -0.070 | [-0.171, 0.024] | 1 | 7 | 0.070 |
| K | A52 − A0 | t=12000 | pb | 40 | -0.046 | [-0.116, 0.000] | 0 | 2 | 0.500 |
| K | A52 − A0 | t=12000 | pcc | 40 | -0.025 | [-0.075, 0.000] | 0 | 1 | 1.000 |
| K | A52 − A0 | t=12000 | universal-open (McNemar) | 40 | -0.025 | - | 0 | 1 | 1.000 |
| K | A156 − A0 | t=10000 | prud | 40 | 0.110 | [-0.034, 0.256] | 13 | 8 | 0.383 |
| K | A156 − A0 | t=10000 | T | 40 | -0.094 | [-0.206, 0.012] | 2 | 23 | 0.000 |
| K | A156 − A0 | t=10000 | pb | 40 | 0.014 | [-0.049, 0.083] | 2 | 2 | 1.000 |
| K | A156 − A0 | t=10000 | pcc | 40 | -0.050 | [-0.125, -0.000] | 0 | 11 | 0.001 |
| K | A156 − A0 | t=10000 | universal-open (McNemar) | 40 | -0.050 | - | 0 | 2 | 0.500 |
| K | A156 − A0 | t=12000 | prud | 40 | 0.107 | [-0.042, 0.255] | 12 | 5 | 0.143 |
| K | A156 − A0 | t=12000 | T | 40 | -0.087 | [-0.199, 0.020] | 2 | 6 | 0.289 |
| K | A156 − A0 | t=12000 | pb | 40 | 0.003 | [-0.066, 0.076] | 2 | 1 | 1.000 |
| K | A156 − A0 | t=12000 | pcc | 40 | -0.050 | [-0.125, 0.000] | 0 | 2 | 0.500 |
| K | A156 − A0 | t=12000 | universal-open (McNemar) | 40 | -0.050 | - | 0 | 2 | 0.500 |
| K | A52 − SD52 | t=10000 | prud | 40 | 0.078 | [-0.050, 0.211] | 12 | 6 | 0.238 |
| K | A52 − SD52 | t=10000 | T | 40 | -0.061 | [-0.159, 0.037] | 4 | 11 | 0.118 |
| K | A52 − SD52 | t=10000 | pb | 40 | 0.002 | [-0.052, 0.059] | 1 | 1 | 1.000 |
| K | A52 − SD52 | t=10000 | pcc | 40 | -0.025 | [-0.075, 0.000] | 3 | 2 | 1.000 |
| K | A52 − SD52 | t=10000 | universal-open (McNemar) | 40 | -0.025 | - | 0 | 1 | 1.000 |
| K | A52 − SD52 | t=12000 | prud | 40 | 0.060 | [-0.091, 0.212] | 10 | 5 | 0.302 |
| K | A52 − SD52 | t=12000 | T | 40 | -0.057 | [-0.153, 0.035] | 2 | 7 | 0.180 |
| K | A52 − SD52 | t=12000 | pb | 40 | -0.001 | [-0.073, 0.069] | 1 | 1 | 1.000 |
| K | A52 − SD52 | t=12000 | pcc | 40 | -0.025 | [-0.075, 0.000] | 0 | 1 | 1.000 |
| K | A52 − SD52 | t=12000 | universal-open (McNemar) | 40 | -0.025 | - | 0 | 1 | 1.000 |
| K | SD52 − A0 | t=10000 | prud | 40 | -0.053 | [-0.189, 0.080] | 8 | 8 | 1.000 |
| K | SD52 − A0 | t=10000 | T | 40 | -0.012 | [-0.091, 0.063] | 2 | 9 | 0.065 |
| K | SD52 − A0 | t=10000 | pb | 40 | -0.031 | [-0.090, 0.015] | 1 | 2 | 1.000 |
| K | SD52 − A0 | t=10000 | pcc | 40 | -0.000 | [-0.000, -0.000] | 0 | 5 | 0.062 |
| K | SD52 − A0 | t=10000 | universal-open (McNemar) | 40 | 0.000 | - | 0 | 0 | 1.000 |
| K | SD52 − A0 | t=12000 | prud | 40 | -0.039 | [-0.194, 0.108] | 7 | 8 | 1.000 |
| K | SD52 − A0 | t=12000 | T | 40 | -0.013 | [-0.088, 0.060] | 2 | 3 | 1.000 |
| K | SD52 − A0 | t=12000 | pb | 40 | -0.045 | [-0.114, 0.001] | 1 | 2 | 1.000 |
| K | SD52 − A0 | t=12000 | pcc | 40 | 0.000 | [0.000, 0.000] | 0 | 0 | 1.000 |
| K | SD52 − A0 | t=12000 | universal-open (McNemar) | 40 | 0.000 | - | 0 | 0 | 1.000 |
| K | A156 − A52 | t=10000 | prud | 40 | 0.085 | [-0.054, 0.221] | 11 | 10 | 1.000 |
| K | A156 − A52 | t=10000 | T | 40 | -0.021 | [-0.133, 0.089] | 7 | 17 | 0.064 |
| K | A156 − A52 | t=10000 | pb | 40 | 0.042 | [-0.000, 0.110] | 2 | 1 | 1.000 |
| K | A156 − A52 | t=10000 | pcc | 40 | -0.025 | [-0.075, -0.000] | 2 | 9 | 0.065 |
| K | A156 − A52 | t=10000 | universal-open (McNemar) | 40 | -0.025 | - | 0 | 1 | 1.000 |
| K | A156 − A52 | t=12000 | prud | 40 | 0.085 | [-0.071, 0.243] | 10 | 6 | 0.454 |
| K | A156 − A52 | t=12000 | T | 40 | -0.017 | [-0.135, 0.087] | 6 | 5 | 1.000 |
| K | A156 − A52 | t=12000 | pb | 40 | 0.049 | [0.000, 0.124] | 2 | 0 | 0.500 |
| K | A156 − A52 | t=12000 | pcc | 40 | -0.025 | [-0.075, 0.000] | 0 | 1 | 1.000 |
| K | A156 − A52 | t=12000 | universal-open (McNemar) | 40 | -0.025 | - | 0 | 1 | 1.000 |

#### World K minus world L (paired founders)

| arm | time | statistic | pairs | mean diff | 95% bootstrap | K>L | K<L | p |
|---|---|---|---|---|---|---|---|---|
| A0 | t=10000 | prud | 40 | -0.049 | [-0.199, 0.109] | 7 | 12 | 0.359 |
| A0 | t=10000 | T | 40 | 0.015 | [-0.057, 0.087] | 5 | 2 | 0.453 |
| A0 | t=10000 | pcc | 40 | 0.000 | [0.000, 0.000] | 0 | 0 | 1.000 |
| A0 | t=10000 | universal-open (McNemar) | 40 | 0.000 | - | 0 | 0 | 1.000 |
| A0 | t=12000 | prud | 40 | -0.057 | [-0.224, 0.112] | 7 | 12 | 0.359 |
| A0 | t=12000 | T | 40 | 0.004 | [-0.068, 0.077] | 4 | 2 | 0.688 |
| A0 | t=12000 | pcc | 40 | 0.000 | [0.000, 0.000] | 0 | 0 | 1.000 |
| A0 | t=12000 | universal-open (McNemar) | 40 | 0.000 | - | 0 | 0 | 1.000 |
| A52 | t=10000 | prud | 40 | -0.010 | [-0.161, 0.137] | 9 | 10 | 1.000 |
| A52 | t=10000 | T | 40 | 0.007 | [-0.114, 0.137] | 4 | 8 | 0.388 |
| A52 | t=10000 | pcc | 40 | -0.000 | [-0.075, 0.075] | 1 | 2 | 1.000 |
| A52 | t=10000 | universal-open (McNemar) | 40 | 0.000 | - | 1 | 1 | 1.000 |
| A52 | t=12000 | prud | 40 | -0.007 | [-0.164, 0.151] | 8 | 11 | 0.648 |
| A52 | t=12000 | T | 40 | 0.021 | [-0.098, 0.146] | 4 | 7 | 0.549 |
| A52 | t=12000 | pcc | 40 | 0.000 | [-0.075, 0.075] | 1 | 1 | 1.000 |
| A52 | t=12000 | universal-open (McNemar) | 40 | 0.000 | - | 1 | 1 | 1.000 |
| A156 | t=10000 | prud | 40 | -0.128 | [-0.290, 0.038] | 8 | 16 | 0.152 |
| A156 | t=10000 | T | 40 | -0.059 | [-0.176, 0.061] | 4 | 9 | 0.267 |
| A156 | t=10000 | pcc | 40 | -0.050 | [-0.125, 0.000] | 3 | 4 | 1.000 |
| A156 | t=10000 | universal-open (McNemar) | 40 | -0.050 | - | 0 | 2 | 0.500 |
| A156 | t=12000 | prud | 40 | -0.099 | [-0.271, 0.067] | 6 | 13 | 0.167 |
| A156 | t=12000 | T | 40 | -0.059 | [-0.185, 0.057] | 4 | 5 | 1.000 |
| A156 | t=12000 | pcc | 40 | -0.050 | [-0.125, 0.000] | 0 | 2 | 0.500 |
| A156 | t=12000 | universal-open (McNemar) | 40 | -0.050 | - | 0 | 2 | 0.500 |
| SD52 | t=10000 | prud | 40 | -0.098 | [-0.253, 0.057] | 8 | 11 | 0.648 |
| SD52 | t=10000 | T | 40 | 0.080 | [-0.036, 0.199] | 5 | 4 | 1.000 |
| SD52 | t=10000 | pcc | 40 | 0.025 | [-0.000, 0.075] | 1 | 1 | 1.000 |
| SD52 | t=10000 | universal-open (McNemar) | 40 | 0.025 | - | 1 | 0 | 1.000 |
| SD52 | t=12000 | prud | 40 | -0.079 | [-0.244, 0.086] | 7 | 11 | 0.481 |
| SD52 | t=12000 | T | 40 | 0.082 | [-0.036, 0.206] | 5 | 3 | 0.727 |
| SD52 | t=12000 | pcc | 40 | 0.025 | [0.000, 0.075] | 1 | 0 | 1.000 |
| SD52 | t=12000 | universal-open (McNemar) | 40 | 0.025 | - | 1 | 0 | 1.000 |

#### Outcome regions (G = mean prudent-target share)

| world | time | G(A0) | G(A52) | G(A156) | G(SD52) | universal-open(A52) | region |
|---|---|---|---|---|---|---|---|
| L | t=10000 | 0.241 | 0.227 | 0.429 | 0.238 | 0.975 | R-harm |
| L | t=12000 | 0.247 | 0.219 | 0.396 | 0.231 | 0.975 | R-harm |
| K | t=10000 | 0.192 | 0.217 | 0.302 | 0.139 | 0.975 | R-null |
| K | t=12000 | 0.190 | 0.212 | 0.297 | 0.151 | 0.975 | R-null |

#### Residence over the tail (share · 1,000 generations; runs with positive residence in brackets)

| world | arm | off-target (CBo) | certified suckers | uncertified suckers | identity | prudent target |
|---|---|---|---|---|---|---|
| L | A0 | 0.541 (17) | 0.000 (0) | 0.000 (0) | 0.000 (21) | 2.391 (35) |
| L | A52 | 0.539 (40) | 0.141 (40) | 0.004 (40) | 0.000 (32) | 2.269 (40) |
| L | A156 | 0.524 (40) | 0.434 (40) | 0.000 (40) | 0.000 (37) | 3.995 (40) |
| L | SD52 | 0.729 (40) | 0.104 (40) | 0.000 (40) | 0.000 (34) | 2.079 (40) |
| K | A0 | 0.456 (23) | 0.000 (1) | 0.000 (0) | 0.000 (0) | 1.875 (32) |
| K | A52 | 0.585 (40) | 0.332 (40) | 0.000 (40) | 0.000 (0) | 2.250 (40) |
| K | A156 | 0.497 (40) | 0.419 (40) | 0.000 (40) | 0.000 (0) | 3.035 (40) |
| K | SD52 | 0.468 (40) | 0.106 (40) | 0.000 (40) | 0.000 (0) | 1.512 (40) |

#### Paired off-target residence difference (share · 1,000 generations)

| world | contrast | pairs | mean | 95% bootstrap | + | − | sign p |
|---|---|---|---|---|---|---|---|
| L | A52 − A0 | 40 | -0.001 | [-0.625, 0.597] | 33 | 7 | 0.000 |
| L | A52 − SD52 | 40 | -0.189 | [-0.805, 0.421] | 15 | 25 | 0.154 |
| L | A156 − A0 | 40 | -0.016 | [-0.281, 0.243] | 32 | 8 | 0.000 |
| K | A52 − A0 | 40 | 0.129 | [-0.539, 0.772] | 32 | 8 | 0.000 |
| K | A52 − SD52 | 40 | 0.117 | [-0.473, 0.720] | 16 | 24 | 0.268 |
| K | A156 − A0 | 40 | 0.041 | [-0.676, 0.737] | 31 | 9 | 0.001 |

#### The premium: fixed-list edge per arriving sucker (primary), encounter-weighted edge integrated over the tail per A (secondary)

| world | arm | edge per arriving uncertified-sucker founder (H-state) | sucker arrivals / run | edge per 100 programs | edge per arriving SD founder | encounter edge · generations / A | of which certified suckers |
|---|---|---|---|---|---|---|---|
| L | A52 | 0.6859 | 3335 | 34.365 | 0.8277 | 2.041 | 2.041 |
| L | A156 | 0.6852 | 9980 | 34.247 | 0.8265 | 0.711 | 0.711 |
| L | SD52 | 0.2544 | 1327 | 5.074 | 0.0000 | 0.076 | 0.076 |
| K | A52 | 0.6859 | 3335 | 34.365 | 0.8277 | 3.242 | 3.242 |
| K | A156 | 0.6852 | 9980 | 34.247 | 0.8265 | 0.805 | 0.805 |
| K | SD52 | 0.2544 | 1327 | 5.074 | 0.0000 | 0.096 | 0.096 |

Static fixed-list edges (`runs/prudence-static.json`): {"L": {"suckerE": {"H": 0.6828319502074689, "E": 0.0, "mass": 0.5}, "SD": {"H": 0.825479026411186, "E": 0.0, "mass": 0.3755835062240664}, "suckerH_cert": {"H": 0.8260671426401336, "E": 0.0, "mass": 0.42680238589211617}, "Q": {"H_mean": 0.0, "E_mean": 0.0, "n": 10}}, "K": {"suckerE": {"H": 0.6828319502074689, "E": 0.0, "mass": 0.5}, "SD": {"H": 0.825479026411186, "E": 0.0, "mass": 0.3755835062240664}, "suckerH_cert": {"H": 0.8244390539721043, "E": 0.0, "mass": 0.4276452282157676}, "Q": {"H_mean": 0.0, "E_mean": 0.0, "n": 10}}}

#### Ancestry of the prudent share (gain = tail-end prudent share minus its value at the merge ≥ 0.25)

| world | arm | runs with gain ≥ 0.25 | arrival-descended fraction of the tail-end prudent share | Δ prudent share from arrivals, t = 0 → 2,000 | Δ from residents |
|---|---|---|---|---|---|
| L | A52 | 8 | 0.024 | 0.002 | 0.027 |
| L | A156 | 17 | 0.022 | 0.029 | 0.150 |
| L | SD52 | 9 | 0.000 | 0.018 | 0.003 |
| K | A52 | 8 | 0.080 | 0.010 | 0.004 |
| K | A156 | 12 | 0.087 | 0.030 | 0.102 |
| K | SD52 | 5 | 0.000 | 0.026 | -0.035 |

#### Arrival lineages that reached half of the population

| world | arm | lineages | runs | selected (arrival payoff above the mean) | drift | prudent-target arrivals | Q arrivals | sucker arrivals |
|---|---|---|---|---|---|---|---|---|
| L | A52 | 7 | 5 | 2 | 5 | 1 | 0 | 4 |
| L | A156 | 3 | 3 | 0 | 3 | 3 | 0 | 2 |
| L | SD52 | 4 | 3 | 1 | 3 | 1 | 0 | 2 |
| K | A52 | 5 | 4 | 1 | 4 | 1 | 0 | 3 |
| K | A156 | 11 | 8 | 1 | 10 | 4 | 0 | 5 |
| K | SD52 | 1 | 1 | 0 | 1 | 1 | 0 | 1 |

#### Composition at the merge (generation 200; A0 rows, identical across arms)

| world | runs | P(C,C) | T | prudent | unguarded | PB own | off-target | certified suckers | uncertified suckers | identity | AP | living types |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L | 40 | 0.687 | 0.766 | 0.190 | 0.575 | 0.032 | 0.061 | 0.000 | 0.000 | 0.061 | 0.011 | 30 |
| K | 40 | 0.766 | 0.800 | 0.190 | 0.610 | 0.031 | 0.082 | 0.000 | 0.000 | 0.000 | 0.006 | 33 |

#### Plurality type at the chase's end, and plurality changes over the tail

| world | arm | runs | plurality in T | plurality guarded | plurality PB tree | mean plurality-spelling changes (samples) |
|---|---|---|---|---|---|---|
| L | A0 | 40 | 39 | 10 | 4 | 17.3 |
| L | A52 | 40 | 35 | 8 | 3 | 20.3 |
| L | A156 | 40 | 38 | 15 | 3 | 18.2 |
| L | SD52 | 40 | 35 | 9 | 2 | 18.4 |
| K | A0 | 40 | 39 | 8 | 3 | 19.9 |
| K | A52 | 40 | 36 | 9 | 1 | 20.3 |
| K | A156 | 40 | 35 | 11 | 3 | 22.5 |
| K | SD52 | 40 | 39 | 6 | 1 | 22.9 |

