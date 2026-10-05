## Bridge survival in pair-1 runs (added in analysis, not predeclared)

Every pair-1 run (path and propagule cells) that ends with both A and B present has lost the bridge class's last copy,
and early: median bridge extinction at generation 9–58, i.e. during the scramble. Runs ending both-present / runs with
the bridge extinct: (100, 16) 3 / 32; (100, 64) 4 / 12; (200, 16) 26 / 27; (200, 64) 6 / 9; (400, 16) 20 / 21;
(400, 64) 5 / 5 (40 runs per cell; at k = 10, 30, 60 on I = 16 the same pattern, 0 exceptions). A surviving bridge
absorbed B in every run in which it survived the scramble (2>3 is 63–1,223 events per cell against 2–234 replacements
2>1). At N = 100 coordination flips resolve rivals even without the bridge.

## Propagule stacking (added in analysis)

At (400, 60) the pair-3 hazard is 4.7·10⁻⁷ per minority-island-generation against the single-propagule reference
8.1·10⁻¹⁰ (×580); at (200, 30), 1.4·10⁻⁵ against 2.2·10⁻⁶ (×6). Two propagules arriving within the decay time of the
first act as one of size 2k: P(fix) from 120 of 400 at once is 9.6·10⁻⁴ (from 60, 2.8·10⁻⁸), from 60 of 200, 0.014.
Arrival intervals per island are k/mN = 35 generations at (400, 60) and 27 at (200, 30).

## Verdicts (predictions/2026-10-05-island-path.md)

| # | prediction | outcome |
|---|---|---|
| RE 1 | N = 100: both ≤ 0.2 (pair 1), ≤ 0.5 (pair 3); N = 200, 400: pair 3 both ≥ 0.8, hazard ≤ 10⁻⁵, q ≥ 0.75 | **Held.** N = 100: pair 1 0.07 / 0.10, pair 3 0.10 / 0.10 (I = 16 / 64). N ≥ 200 pair 3: 40/40 both in all four cells, 0 losses, hazard < 1.9·10⁻⁷ (upper 95%). q = 0.82–0.97 (lower bounds 0.69–0.84; within sampling error of 0.75 at (100, 64), (200, 16)). The headline "resolve only at N = 100" is wrong for pair 1, which resolves at N = 200 and 400 on I = 64 (both 0.15, 0.12) by bridge absorption; no clause covered it |
| RE 2 | both ≤ 0.3 at (200, 30) and (400, 60); ≥ 0.6 at (400, 30); abs(Δq) ≤ 0.3 | **Failed, falsifier fired** (within sampling error): (400, 60) pair 3 both 0.82 [0.68, 0.91] ≥ 0.7. Held: (200, 30) 0.00 [0, 0.09]; (400, 30) 1.00; max abs(Δq) 0.10. k/N is not the scaling variable: at k/N = 0.15 the static probability falls 2,000× from N = 200 to 400 |
| RE 3 | horizon separation < 0.05 at N = 100; grows with I at N = 200, ≥ 0.05 at (200, 256); colonization shorter than the rival interval at N = 100, not at N = 200 | **Failed, falsifier not fired.** Horizon separation 0 in all four cells (0/300, 0/300, 0/300, 0/100). Ever separated 2/300, 10/300 (N = 100); 4/300, 1/100 (N = 200), not growing with I at N = 200. Colonization vs rival interval: 25 vs 28 and 20 vs 20 at N = 100 (10 rival runs at I = 256: not shorter); N = 200 inconclusive (4 and 1 rival runs) |
| RE 4 | bridge share at mN = 1 above the bridge-alone control by ≥ 0.1; majority 0.3–0.6 at mN = 1, ≤ 0.3 at mN = 0.1 | **Failed, falsifier fired**: conflict share 0.619 = bridge-alone 0.619 (not above). Majority 0.65 [0.50, 0.78] at mN = 1 (gap) and 0.42 at mN = 0.1. Against the matched A, A, bridge control the conflict share is +0.32 (0.62 vs 0.30) at mN = 1 and +0.14 at mN = 0.1 |
| S1 | pair 1 both ≤ 0.2 in every path cell; replacement < 0.2 of B-island losses at N ≥ 200 | **Failed, falsifier fired** ((200, 16) both 0.65 ≥ 0.5; (400, 16) 0.50). The mechanism clause held: replacement is 2–16 of 70–910 B-island losses per cell at N ≥ 200, the rest absorption by the bridge (and 6–44 captures) |
| S2 | q ∈ [0.65, 0.95] in every path cell; the three N within 0.15 at each I | **Failed narrowly, falsifier not fired** ((400, 16) q = 0.97, within sampling error); agreement held (I = 16: 0.90 / 0.90 / 0.97; I = 64: 0.86 / 0.83 / 0.82) |
| S3 | pair 3 both ≥ 0.9 at N ≥ 200, B ≥ 3 islands, hazard ≤ 10⁻⁶ | **Held** (1.00; B holds 5.8–20.4 islands; 0 losses) |
| S4 | k/N-matched propagules do not resolve: pair 3 both ≥ 0.85 at every N = 400 cell, ≥ 0.6 at (200, 30); hazard within ×10 of (mN/k)·P_k | **Failed, falsifier not fired**: (200, 30) both 0.00; (400, 60) 0.82; hazard ×6 at (200, 30), ×580 at (400, 60) (stacking) |
| S5 | abs(Δq) ≤ 0.15 at matched flux | **Held** (−0.10 to +0.03; all intervals include 0) |
| S6 | horizon separation ≤ 0.05 at (200, 256), ever ∈ [0.01, 0.12]; more separations survive at N = 200; rival before the first immigrant island in ≥ 0.5 | **Failed, falsifier not fired.** First two clauses held (0/100; 1/100). No separation survived at either N (0/12, 0/5): every N = 200 rival in the sample had a bridge. Rival before the first immigrant-founded island 4/12 (N = 100) and 2/5 (N = 200) |
| S7 | conflict bridge share below bridge-alone, within ±0.15 of A, A, bridge; majority 0.2–0.5 | **Failed, falsifier fired** (conflict exceeds A, A, bridge by 0.32 ≥ 0.2; equal to bridge-alone, not below; majority 0.65 at mN = 1) |
