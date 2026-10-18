# Verdicts: per-root production (predictions/2026-10-16-per-root-production.md)

Scored on the confirmation streams 20–39 (all rules paired; R2, R0 and H-full also on 20–59), development streams
0–19 beside them; executed cells on the development streams. Fair share = fraction of islands fair at 10,000.

| # | prediction | numbers | verdict |
|---|---|---|---|
| RE 1 | R2 within 0.1 of H-full, zero wage ≤ 0.05 | conf 20–39: R2 0.402 vs H-full 0.398 (Δ +0.004 [−0.25, 0.30]); 20–59: 0.426 vs 0.299 (Δ +0.13 [−0.07, 0.31]); dev 0.339 vs 0.300; zero wage 0 everywhere | **supported** |
| RE 2 | R1 between S₃ and R2, near 0.10 | conf: R0 0.050 < R1 0.202 < R2 0.402; dev 0.000 / 0.200 / 0.339 | order held, not "near 0.10"; falsifier not fired; **inconclusive** (0.202 just above the region's 0.2) |
| RE 3 (revised) | R3 k = 2 within 0.05 of R2 at ≤ 1.5× play | R3 not run: the cap thrashes (class changes 16–48× R2's at founding); traces: k = 2 changes coverage little in 2,000 encounters | **not scored** (dropped as infeasible); the cost clause is contradicted by the diagnostic |
| RE 4 | R2 ≤ 0.1 at 10⁶ and ≥ 0.4 at 3·10⁶ | 10⁶: 0.050; 3·10⁶: 0.300 (H-full 0.347, R0 0.027) | first clause held, second failed; falsifier (≤ 0.15) not fired: **inconclusive** |
| RE 5 (revised) | median encounter cost under R2 ≤ 1.5× play | 3·10⁶: median 4.10×, p90 17×, p99 419×, cumulative 3.04×; validation 0.88 of non-play steps (0.98 after generation 50) | **contradicted, falsifier fired** (median ≥ 2×) |
| Sol (a) | low median overhead coexists with expensive tails | median 4.1× | **failed** (the median is not low) |
| Sol (b) | k = 2 works only with a small validity cover | not run | not scored |
| Sol (c) | R2 > R0 but ≤ H-full − 0.15 at 3·10⁶ | 0.300 vs 0.027 and 0.347 | **failed** (within 0.05 of H-full) |
| Gemini (d) | unbundled FIFO k = 2 ≥ 0.10 below R2 | not run | not scored |
| Gemini (e) | R2 linear 0.25–0.35 at 3·10⁶; ≥ 0.4 only with dispatch | linear 0.300; dispatch 0.199 | first clause held, second **failed** |
| Gemini (f) | R2 lags H-full by arrival timing | R2 ≥ H-full on every stream set; ½-paying bosses never vanish under R2 (minimum ≈ 10 islands, 0/20 runs extinct) | **failed** |
| S1 | R0 reproduces S₃ | 5/5 identical in every summary field | **held** |
| S2 | static reach and covers ≤ 2 for ≥ 0.9 of mass | R2 reaches 0.94 of (b) \ S₃; workers ≤ 2 bundles 0.96 (scripts 0.88), bosses 0.81 | workers held; bosses in the 0.8–0.9 band: **inconclusive** |
| S3 | R1 ≤ 0.10 on conf | 0.202 | **failed, falsifier fired** (≥ 0.2) |
| S4 | 0.10 ≤ R2 ≤ 0.30 on conf | 0.402 (20–39), 0.426 (20–59) | **failed, falsifier fired** (> 0.40; R2 did better) |
| S5 | R0 + alternatives ≤ 0.05; interaction > 0 | conf 0.050, dev 0.053; interaction +0.20 (conf), +0.09 (dev), intervals spanning 0 | **held** on the confirmation set |
| S6 | R2 zero wage ≤ 0.2 | 0.00 (R0 0.40) | **held** |
| S7 | median 1.3–2.5× at 3·10⁶, validation the overhead | median 4.10×; validation 0.98 of non-play steps after 50 | **failed, falsifier fired** (median > 3×); the validation clause held |
| S8 | R2 ≤ 0.05 at 10⁶; R0 ≤ R2 ≤ H-full at 3·10⁶ | 0.050; 0.027 ≤ 0.300 ≤ 0.347 | **held** |
| S9 | ≥ half of R2 nuclei have a per-root or alternative pivotal script | 1/7 (dev), 1/8 (conf) | **failed** (falsifier not fired) |
| S10 | the cap binds little | not run | not scored |
| S11 | second scripts by gen 10; fair bosses extinct in ≥ half the runs | per-root and alternatives held by generation 10 in 20/20 R1/R2 runs; fair bosses extinct by 200 in 0/20 under R1/R2, 2–5/20 under R0 | first clause held; second **failed** |
| S12 | PROD3A and soundness as code | primaries and alternatives 400/400 and 1,882/1,882; plays 450/450; 0 of 856 T checks unsound; model error 0.22% median | **held**, except exact step equality of plays (8/450; median 1 step, the parent's per-row-class approximation) |
| S13 | dispatch within 0.1 of linear at 3·10⁶ | 0.199 vs 0.300 (Δ −0.10 [−0.40, 0.20]) | **inconclusive** (0.001 outside; falsifier ≥ 0.2 not fired) |
| S14 | mark-sensitive 0 at ideal, < 1% at 3·10⁶ | 0; 1,838 of 1.2·10⁷ (0.015%) | **held** |
| D1 | boss second paths necessary: R2w fair on ≤ 2/7 | 0/7 | **held** |
| D2 | R2b fair on 2–5/7 | 3/7 | **held** |
