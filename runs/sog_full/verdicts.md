## Verdicts (hand-written from the tables above, `runs/sog-full-static.json`, the assays and the diagnostics)

Scored definitions as fixed in the predictions file and notes §1.8; "window" = the realizable run's 10-check
establishment window, reported beside the scored first-fair-check definition (notes §1.13 item 8).

| # | prediction | outcome |
|---|---|---|
| RS | identity's effect on the fair share is incremental: (i) establishment ≥ 0.9 in H ± eq and S ± eq; (ii) never 0 → positive or positive → 0; falsifier: a paired arm 0.2 → ≤ 0.05 or ≤ 0.05 → ≥ 0.2 | **(i) held** on the scored definition (40/40 in all four), window 34/37/29/28 of 40; **(ii) failed** in one arm: S + no eq 0.000 → S + eq 0.084 (and S + sham 0.002 → 0.073); **(iii) held**; **falsifier not fired** (largest change +0.084). Identity fills a few islands in one arm, it never decides the wage. |
| RE 1 | under S-nonself₃ establishment ≥ 0.8, delay ≤ 2×, timeouts ≤ 10% | **held on the scored definition** (40/40; median window end 150 vs 130 under H + eq, 1.15×; TO-changed checks 0.0075 of sampled encounters); on the window definition 28/40 = 0.70 < 0.8; falsifier not fired |
| RE 2 | greenbeard ≤ 0.05 under S, ≥ 0.2 under H | S clause held (0.023, all strike pacts; identity greenbeards 0); **H clause failed, falsifier fired** (0.005) |
| G (gemini) | U_eq < 0.05 of fair islands even in H + eq | **held** (no greenbeard-union island in any cell; identity mixtures 0.010 of H + eq fair islands) |
| RE 3 | |H + eq − H + sham| ≤ 0.1; the unread-slot assay leaves B_eq's wage unchanged, any effect through D\* (neutral cut after a scab) | **held** (−0.022 [−0.15, 0.11]; B_eq: neutral substitution → neutral cut, no strict cut; F\*: neutral substitution → neutral cut 0.36 of prior entrants) |
| RE 4 | S + eq persistence ≥ 0.3, zero-wage plurality ≤ 0.2, productive efficiency ≥ 0.9 | **failed, falsifier fired** (persistence 0.084 ≤ 0.15; zero wage 0.45; productive efficiency 0.963 held) |
| RE 5 | production adds ≤ 2× to the median per-encounter cost; failures in the top decile | **failed, falsifier fired on the realized encounters** (4.04× in S + eq, 4.8–4.9× in S + sham and S-opp; static 3.4×); the tail clause held only in part (the top cost decile holds 0.21–0.43 of failures, 2–4× its share, but the plurality, 0.50–0.68, sits in the third decile); the overhead is futile retries (0.97–0.99 of attempts after generation 50 return NONE), not failures (cap and fuel timeouts 0.14% of sampled attempts) |
| RE 6 | B_eq invasion positive on exact-T₁ islands, negative elsewhere; share > prior iff greenbeards ≥ 0.2 | **failed, falsifier fired** (on T₁-pair islands B_eq is neutral, 585 zero / 3 positive; its share is 2.4× its prior mass in S-opp, where greenbeards hold 0); greenbeards never reach 0.2, so the conditional form is vacuous |
| S1 | scale guard does not fire; ≤ 2,000 worker row classes reached in any S₃ cell | static clause held (603 grammar classes); **dynamic clause failed, falsifier fired**: one fresh S + eq run reaches 2,254 worker row classes (run tree × inventory × ⌜T₁⌝ bit; S-opp 2,267) and 25,176 boss row classes (`runs/sog_full/row_classes_reached.json`); under that reading the spec's guard would have fired and the named quote been dropped, which the eq-without-⌜T₁⌝ cell shows changes nothing under H (+0.002) |
| S2 | coalition masses (c) ∈ [0.0154, 0.0188], (a) ∈ [0.003, 0.014] | **failed, falsifier fired** ((c) 0.0200, (a) 0.0160: identity does not dilute coalitions, the prior is identity-blind in law) |
| S3 | H + no eq on the ideal table reproduces the realizable L cell | **held** (20/20 established, persistence 0.500 [0.30, 0.70]; realizable 0.53) |
| S4 | executable vs ideal under H + no eq within 0.05 | **failed, falsifier fired** (0.025 vs 0.500 on the same 20 seeds; Δ −0.475) |
| S5 | greenbeard holders ≤ 0.10 under H + eq | held (0.005) |
| S6 | ≤ 0.05 under S + eq, every greenbeard island under a boss that reads no worker certificate | number held (0.023); **falsifier fired on the clause** (the 10 greenbeard-classified islands are strike-pact mixtures under probe bosses; no identity greenbeard exists) |
| S7 | closed-shop share within [0.3, 3]× its prior share in every eq cell | **failed, falsifier fired** (forced preloaded cell 0; others 0.31–2.4×) |
| S8 | identity small: |eq − sham| ≤ 0.10, |eq − eqnoT| ≤ 0.05 under H | held (0.022, 0.002) |
| S9 | S₃ vs H with eq: establishment, delay ≤ 1.5×, persistence lower by 0–0.15 | held (40/40, 1.15×, +0.007) |
| S10 | isolated empty never fair, preloaded ≥ 38/40; lottery forced cells within 0.05 | isolated clauses **held** (0/40, 40/40); **lottery clause failed, falsifier fired** (0.702 vs 0.597, Δ −0.105, CI [−0.45, 0.24]) |
| S11 | composed costs exact on ≥ 99%; replays agree ≥ 98% | values and outcomes held (400/400 plays, 1,005/1,005 productions); **step exactness failed** (4% of plays exact; median error 1 step, 90th percentile 6%) |
| S12 | executable-TO ≤ 5% early and ≤ 1% late in every S₃ cell | **failed, falsifier fired** in S + sham at 2,000 (0.050); others ≤ 0.02 early, ≤ 0.009 late |
| S13 | no self-play-only script held under S₃ | held (0 individuals in every S cell, S-opp included) |
| S14 | zero-wage plurality ≤ 0.10 in every natural cell | **failed, falsifier fired** (0.45–0.59 in every S cell) |
| S15 | S + eq at (200, 64) ≥ its (100, 64) value − 0.05 | **missed the number** (0.000 on 12 runs, zero wage 0.10, ¼ wage 0.90, against 0.084); falsifier (lower by > 0.15) not fired |
| S16 | drift ≥ 0.6 of first exits; timeout + production failure ≤ 0.05 | **failed, falsifier fired** in the natural cells (drift 0.11–0.28: exits are boss cuts of scramble-fair islands); held in the forced cells (0.81–0.86); timeout-changed exits 0.12–0.13 of H exits (≤ 0.15) |
| S17 | productive efficiency ≥ 0.9 in every natural cell | held (0.963–1.000) |
| S18 | gate deadlock is a slot-1 loss | held (slot 1: deleterious −½ at entry, lost 200/200, never fixed; slot 2 neutral, 2/200 fixed under both gates); S-opp's neutral-rate clause inconclusive (0/200 fixed against ≈ 2 expected) |
| S19 | S-opp vs S₃ persistence within ±0.10; greenbeards higher under S-opp | persistence held (−0.073); greenbeard clause failed (S-opp has no fair island) |
| S20 | H + no eq at K = 3·10⁶ ≥ 0.35 | **held** (0.652 [0.45, 0.85]) |
| S21 | S + eq on the ideal table ≤ 0.15 | **held** (0.000 on 20 runs) |
