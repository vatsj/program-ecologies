# Coverage components: verdicts (scored at generation 10,000 unless stated; 20 paired runs per cell)

Numbers from `runs/coverage-components.json`. H-full 0.300; S₃ 0 (stored `Ni`, reproduced draw for draw).

| # | prediction | outcome |
|---|---|---|
| RE 1 | untravelled paths carry regrowth: minus (a) ≤ 0.05 and plus (a) ≥ 0.2 | **failed, falsifier fired**: minus (a) 0.050 held, plus (a) 0.000 (0/20) |
| RE 2 | minus (b) and minus (d) within 0.1 of H-full | **failed, falsifier fired**: minus (b) 0.000; minus (d) 0.400 held |
| RE 3 | minus (c) within 0.1 of H-full | **held** (0.350) |
| RE 4 | no single component sufficient except (a): plus (b), (c), (d) ≤ 0.05 | **failed, falsifier fired**: plus (b) 0.300 (confirmed 0.237 on 40 fresh streams); plus (c) 0.050, plus (d) 0.000 held; plus (a) 0 |
| Gemini | minus (a) ≤ 0.05, plus (a) ≤ 0.10, plus (a)+(b) ≥ 0.25 | **failed**: first two held; plus (a)+(b) 0.100 |
| Sol | plus (a) < 0.2, and some combined grant beats every singleton | **failed**: plus (a) 0 held; both pairs 0.100 < plus (b) 0.300 |
| S1 | masks reproduce the references draw for draw | **held**: full = `Heq_i` 20/20; empty = `Ni` 5/5 with the mark (counters equal without it, rep 0) |
| S2 | (c) null: minus (c) within 0.05 of H-full, plus (c) ≤ 0.05 | **held** (+0.050 [−0.20, +0.30]; 0.050) |
| S3 | (d) small: minus (d) within 0.1, plus (d) ≤ 0.05 | **held** (0.400, +0.10 [−0.15, +0.35]; 0.000) |
| S4 | plus (b) − plus (a) ≥ 0 and plus (b) ≥ 0.15 | **held** (+0.300 [+0.10, +0.50], McNemar p = 0.031) |
| S5 | minus (b) ≤ 0.15 | **held** (0.000) |
| S6 | minus (a) ≤ 0.15 | **held** (0.050) |
| S7 | plus (a)+(b) ≥ 0.2 and plus (c)+(d) ≤ 0.05 | **failed** (0.100 and 0.100); neither falsifier fired (≤ 0.05; ≥ 0.2) |
| S8 | every cell ≤ 0.12 at generation 20 | **held** (max 0.048) |
| S9 | no minus cell exceeds H-full by ≥ 0.15 | **held** (largest minus (d), +0.10) |
| S10 | identity, not volume (conditional) | **split**: plus clause held for (b) (rand-plus (b) 0.050, −0.250 [−0.45, −0.10]); minus clause **failed, falsifier fired** for (a) and (b) (rand-minus (a) 0.000 vs 0.050; rand-minus (b) 0.050 vs 0.000) |
| (rand-(c)) | not scored (conditional cells not met) | rand-minus (c) 0.095, rand-plus (c) 0.050 |
| S11 | pivotal granted (b) scripts mostly "never written"; withheld replays regrow ≤ 2 of 5 | **failed, falsifier fired**: all 4 "pre-populated, here" by the pre-registered log (each blocked by the lack rule: own script held); 3/3 replays still regrow |
| S12 | 2,000 and 10,000 within 0.05 in every cell | **failed, falsifier fired**: minus (c) 0.476 → 0.350 |
| S13 | costs (H-type ≤ 8 min, plus-type 8–25 min) | **held** (4.7–6.5; 11.9–17.6) |
| D1 (addendum) | plus (b)∩S₃^static ≥ 0.2 | **failed**, falsifier (≤ 0.05) not fired: 0.101 |
| D2 (addendum) | plus (b)\S₃^static ≤ 0.05 | **held** (0.048) |
