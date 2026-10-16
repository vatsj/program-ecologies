# Verdicts: the realizable lottery along paths in (N, I, mN)

Predictions `predictions/2026-10-14-realizable-scaling.md` (scoring conventions there: main cells at T_ext, other S
cells at 10,000, C-donor and dense cells at 2,000 after the disclosed drop-order steps; 2,000 reported beside). Numbers
from `runs/realizable-scaling.md` / `.json`.

| # | prediction | outcome |
|---|---|---|
| RE 1 | q falls with N along P1 and P3, ≥ 0.95 efficient at the largest cell; P2 plateaus | **held on P1** (q 0.050 → 0.017 calibrated, 0.050 → 0.005 at mN = 1; ē 0.983 / 0.995 at (400, 64)); **failed on P3** (calibrated q 0.000 → 0.038 → 0.061, ē 0.939 at (200, 128)); P2 did not plateau (q fell to 0, all-island success rose with I); falsifier (P1) not fired |
| RE 2 | S-nonself ≤ 0.2 at (100, 256) and (200, 128) | **failed, falsifier fired** at (100, 256) (0.10 at 2,000, 0.30 at 10,000, 1.00 at T_ext); held at (200, 128) (0.20 calibrated, 0.10 at mN = 1, every horizon) |
| RE 3 | ablation ≥ 0.7 along P1 calibrated, failures non-identity | **held** (0.95 / 1.00 / 0.95 / 0.95; failures bridge-less rivals or scramble failures) |
| RE 4 | calibrated mN rescues ≥ half of mN = 1's bridged failures at N ≥ 200, no bridge-less ones | **untestable as worded** (no bridged failure under mN = 1 at N ≥ 200 by 10,000); the bridge-less clause failed in paired form (8 of 10 rescued by a different history, 5 lost) |
| RE 5 | collapse on copies on the calibrated path, crossings within 2× of 8 | **held at N = 200 and (100, 64)** (crossings 6.0 / 6.0 / 8.0, q_c 0.066–0.076); **failed at (100, 128)** (no crossing at T_ext); falsifier (spread > 4×) not fired; the mN = 1 clause untested (panel calibrated only) |
| RE 6 | C-donor ≥ 0.85 along P1; fails along P2 by identity | P1 clause **held** (0.90–1.00 at every N, 10/10 at (400, 64)); **P2 clause failed, falsifier fired** ((100, 256) 0.80; failures 3 non-identity rivals, 1 identity run) |
| G1 (Gemini) | matched copies: P1 more universal than P2 | **failed at T_ext** ((400, 64) 0.55 vs (100, 256) 1.00); held at 2,000 (0.55 vs 0.10); falsifier (both) not fired; the mechanism was not clustering but N (permanence and per-copy establishment) |
| G2 (Gemini) | C-donor (400, 64) < 0.75 | **failed, falsifier fired** (10/10, calibrated arm only) |
| S1 (sol) | no collapse on raw copies; establishment per copy varies with N, I | **held** (no crossing at (100, 128) with f₀ 0.95; own-island establishment per copy halves from N = 100 to 200) |
| R1 | ē ≥ 0.97 and all-island success ≥ 0.85 in every S cell at N ≥ 100; q(400) < q(50) | **failed, falsifier fired** ((100, 32) 0.787 by scramble failures; (200, 128) 0.939 by clique-border load); q(400) < q(50) held |
| R2 | 18-copy cells: (400, 64), (200, 128) in [0.1, 0.45]; (100, 256) rises ≥ 0.15 | (200, 128) and (100, 256) held (0.20; 0.10 → 1.00); (400, 64) 0.55 missed; falsifier not fired (edge) |
| R3 | identity failures absorbing at N ≥ 200, never bridged; coordination-unresolved at N = 50 | held at N ≥ 200 (1,192 / 1,192 absorbing, 0 bridged); the N = 50 clause failed (whole-metapopulation cliques are absorbing); falsifier not fired |
| R4 | C-donor identity ≤ 0.005; universal ≥ 0.85 everywhere; dense within 0.1 | identity and dense clauses held (≤ 0.004; +0.05); universal missed at (100, 256) and (50, 32) calibrated (0.80); falsifier (< 0.75) not fired |
| R5 | ablation − proportional ≤ 0.10; proportional − S-nonself ≥ 0.15 at four cells | second clause held (+0.25 / +0.40 / +0.60 / +0.45); first missed at (200, 64) (+0.15); falsifier not fired |
| R6 | panel: f(0) ≥ 0.75, q_c within 2×, crossings 8–20 | **failed, falsifier fired** (q_c 0.018 vs 0.076; crossings 6–8) |
| R7 | multi-copy islands ≥ 2× singles; total copies predict as well | **failed, falsifier fired** (ratio ≈ 1.0); second clause held |
| R8 | calibrated − mN = 1 within [−0.1, +0.2] at N ≥ 200, [−0.2, +0.1] at N = 50 | held |
| R9 | T_nuc 20–70 at N = 100, ≤ N^0.45, x flat in [0.15, 0.6] | held (35, N^0.38, 0.31–0.37) |
| R10 | half of the controls' failures at N ≥ 200 bridged | **failed, falsifier fired** (0: every one bridge-less) |

