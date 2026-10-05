# A semantic legibility gate (toward bounded provers), 2026-10-04

Spec `specs/2026-10-04-bounded-provers.md`; predictions `predictions/2026-10-04-bounded-provers.md`; code `src/bounded*.py`. The gate is semantic stabilization (essential atoms × settle world), not proof length; all results are finite-language (n = 6, 8) and specific to this gate. Adopted semantics: the world-indexed (online) gate; the spec's synchronous joint iteration is reported as a diagnostic (it cycles).

## Verdicts (cost proxy = semantic stabilization, not measured proof length; finite-language, gate-specific)

**Design deviation.** The spec's joint fixed point (free play → costs → gate → re-evaluate, synchronously) does not
converge: it falls into a period-2 cycle at every finite b at both n (except n = 6, b = 8). The pairs that flip are
mutual readers whose gates close and reopen together. The gate was redefined on the bounded trace, world by world:
at world n, x's boxes reading y are open iff k(y)·(1 + last change world of y's atoms toward x before n) ≤ b. Cost
only grows with n, so each gate closes at most once, box truth is monotone, and the trace settles (worlds 7–11) with no
fixed point to select. At the stable world the gate equals the cost of its own trace in every case; soundness holds on
every pair (0 violations); b = ∞ reproduces the free arm exactly.

| # | prediction | outcome |
|---|---|---|
| 1 | FairBot b* = 2, PrudentBot 4, P* 4; below threshold a prover still cooperates with ALLC | **Failed, falsifier fired.** b* = 1 for FairBot, `BOX1(THEM(ME))`, `BOX(THEM(THEM))` (self-cost 1·(1 + 0)); PrudentBot 2; P* 4 (held). 99.45% of n = 8 prover mass has b* = 1; b* is monotone for all 118 provers. Below threshold, 0.94 (b = 1), 0.68 (b = 2, 3), 1.00 (b = 4, 6) of that mass still cooperates with ALLC; PrudentBot and P* below threshold do not. |
| 2 | first drift-closed classes at b = 4; no legible sibling of a self-cooperator at b = 4 | **Failed, falsifier fired:** no drift-closed class (and no H-closed class) at any b at n = 6 or 8. The sibling clause held: no sibling is legible at any finite b ≤ 8 (cost ratio sibling/self ≥ 2). Closure fails through *cheaper* neighbours: P*'s suckerable mates (μ 3.1·10⁻³) are led by `not(BOX(THEM(ME)))` (k = 1), suckered by D. |
| 3 | FairBot exits neutrally at 1/N at every b, odds ∝ N^½; closed classes at b = 4 parochial | **Held** for FairBot: exit slope −1.00, all into ALLC, odds slope 0.43–0.48 at every b. The closed-class clause is vacuous (none). |
| 4 | π at b = 4 → closed prudent family, exit slope < −1.5, P(C,C) ≥ 0.9 at 10⁴, rival ≥ 0.5; b ≥ 8 within 0.05 of free; controls not closing | **Failed, falsifier fired:** at b = 4, n = 8 the top state is FairBot, exit slope −1.00, P(C,C) 0.620 at 10⁴, rival share 0.10. b ≥ 8 within 0.05: held (b = 8 equals free to 4 decimals). Controls: no slope steeper than −1.00 (held literally), but the random gate at b = 1, 3, 4 locks in P* (P(C,C) 0.98–1.00 at 10⁵) by cutting its cheap mates, which the legibility gate never does. |
| 5 | fixed support: π on the smallest closed b, not the largest | **Falsifier not fired; mechanism failed.** No family is closed. Prover π by b at n = 8, N = 10⁵: 0.235 / 0.223 / 0.189 / 0.184, a weak tilt to small b. Under the length penalty b = 1 dominates by prior (0.53 vs 0.07 / 0.01 / 0.002). |
| 6 | lottery: b ≥ 4 equivalent to free; b = 2 lower by 0.1–0.3 at I = 4, 1.00 at I ≥ 64; b = 1 zero | **Partly.** b ≥ 4: held (paired difference 0.00 at every cell). b = 2 lower: **failed** (+0.05 / −0.05 / 0.00 at I = 4). b = 2 at I ≥ 64 = 1.00: held. b = 1 zero: **failed** (0.20 / 0.53 / 0.80 / 1.00 / 1.00). Falsifier not fired. |
| 7 | budget decides closure under mutation; under seeding only via fragmentation near threshold | **Failed in its first half** (no closure, no parochialism); no fragmentation seen at b = 1–3. Falsifier not fired. |
| S1 | b* = 1 / 2 / 4 for FairBot / PrudentBot / P* | **Held** (also under both phases of the cycling iteration). |
| S2 | soundness by construction; no cycle | **Failed, falsifier fired** (cycle); soundness held. |
| S3 | no legible sibling at b ≤ 4; FairBot's sibling legible at b ≥ 8 | First clause **held**; second **failed** (FairBot's sibling costs 15 at b = 8 on the bounded trace, 9 on the free one). |

**Reading.** The gate excludes expensive readers of the resident and keeps cheap ones. Siblings are expensive, so
they are excluded; but the leaks that keep every class open in L_6 and L_8 run through cheap neighbours: ALLC (cost 0)
for FairBot, `BOX(THEM(THEM))` (cost 1) for PrudentBot, `not(BOX(THEM(ME)))` (cost ≤ 2) for P*. A budget can only cut
edges to programs that are costlier than the resident, so it cannot close a class whose suckerable mates are cheaper.
Under mutation the arm is the free arm with the P* block thinned (b ≤ 3 removes it; P(C,C) 0.847 vs 0.814 at
N = 10⁵); under seeding at n = 6 it is the free arm. A realizable prover is not tested here.

## 1. Semantics: joint iteration, online gate, soundness

| n | b | joint iteration: rounds / cycle | plays differing, cycle phase vs online | online: worlds | masked share of (k>0, k>0) pairs | final gate = cost of own trace | true open atoms checked | soundness violations | plays differing if the final gate is held fixed from world 0 | classes |
|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 1 | 5 / period 2 from round 3 | 311 | 9 | 0.918 | True | 400 | 0 | 0 | 26 |
| 6 | 2 | 5 / period 2 from round 3 | 423 | 9 | 0.597 | True | 692 | 0 | 299 | 35 |
| 6 | 3 | 5 / period 2 from round 3 | 313 | 9 | 0.241 | True | 868 | 0 | 285 | 47 |
| 6 | 4 | 4 / period 2 from round 2 | 25 | 9 | 0.072 | True | 973 | 0 | 96 | 51 |
| 6 | 6 | 2 / period 2 from round 0 | 0 | 8 | 0.001 | True | 994 | 0 | 0 | 51 |
| 6 | 8 | 0 / converged | 0 | 7 | 0.000 | True | 994 | 0 | 0 | 51 |
| 6 | inf | 0 / converged | 0 | 7 | 0.000 | True | 994 | 0 | 0 | 51 |
| 6 | ∞ check | free arm reproduced: plays True, payoff matrix True, class names True | | | | | | | | |
| 8 | 1 | 7 / period 2 from round 5 | 17909 | 11 | 0.753 | True | 59484 | 0 | 12776 | 148 |
| 8 | 2 | 7 / period 2 from round 5 | 28932 | 11 | 0.859 | True | 29024 | 0 | 12610 | 243 |
| 8 | 3 | 7 / period 2 from round 5 | 31318 | 11 | 0.673 | True | 39010 | 0 | 23563 | 368 |
| 8 | 4 | 6 / period 2 from round 4 | 32063 | 10 | 0.519 | True | 70862 | 0 | 17192 | 546 |
| 8 | 6 | 4 / period 2 from round 2 | 10080 | 10 | 0.215 | True | 120744 | 0 | 9154 | 543 |
| 8 | 8 | 4 / period 2 from round 2 | 1496 | 10 | 0.050 | True | 140041 | 0 | 2417 | 502 |
| 8 | inf | 0 / converged | 0 | 7 | 0.000 | True | 143269 | 0 | 0 | 471 |
| 8 | ∞ check | free arm reproduced: plays True, payoff matrix True, class names True | | | | | | | | |

## 2. Thresholds b* (self-cooperation), selective cooperation below threshold

- n = 6: 16 free provers (self-cooperate, defect on D), μ 0.0229. Share of prover mass self-cooperating by b: 1: 1.0000, 2: 1.0000, 3: 1.0000, 4: 1.0000, 6: 1.0000, 8: 1.0000, inf: 1.0000. b* histogram (share of prover mass): 1: 1.0000. Non-monotone in b: 0. Below threshold, share of that mass that still cooperates with ALLC: b=1: none below (μ 0.0000), b=2: none below (μ 0.0000), b=3: none below (μ 0.0000), b=4: none below (μ 0.0000), b=6: none below (μ 0.0000), b=8: none below (μ 0.0000), b=inf: none below (μ 0.0000).
- n = 8: 118 free provers (self-cooperate, defect on D), μ 0.0242. Share of prover mass self-cooperating by b: 1: 0.9945, 2: 0.9993, 3: 0.9993, 4: 0.9995, 6: 0.9997, 8: 1.0000, inf: 1.0000. b* histogram (share of prover mass): 1: 0.9945, 2: 0.0048, 4: 0.0003, 6: 0.0001, 8: 0.0003. Non-monotone in b: 0. Below threshold, share of that mass that still cooperates with ALLC: b=1: 0.94 (μ 0.0055), b=2: 0.68 (μ 0.0007), b=3: 0.68 (μ 0.0007), b=4: 1.00 (μ 0.0005), b=6: 1.00 (μ 0.0003), b=8: none below (μ 0.0000), b=inf: none below (μ 0.0000).

| n | b | FairBot: self-coop (self-cost), coop ALLC | FB1: self-coop (self-cost), coop ALLC | BTT: self-coop (self-cost), coop ALLC | BTT1: self-coop (self-cost), coop ALLC | PrudentBot: self-coop (self-cost), coop ALLC | P*: self-coop (self-cost), coop ALLC |
|---|---|---|---|---|---|---|---|
| 6 | 1 | yes (1), yes | yes (1), yes | yes (1), yes | yes (1), yes | — | — |
| 6 | 2 | yes (1), yes | yes (1), yes | yes (1), yes | yes (1), yes | — | — |
| 6 | 3 | yes (1), yes | yes (1), yes | yes (1), yes | yes (1), yes | — | — |
| 6 | 4 | yes (1), yes | yes (1), yes | yes (1), yes | yes (1), yes | — | — |
| 6 | 6 | yes (1), yes | yes (1), yes | yes (1), yes | yes (1), yes | — | — |
| 6 | 8 | yes (1), yes | yes (1), yes | yes (1), yes | yes (1), yes | — | — |
| 6 | inf | yes (1), yes | yes (1), yes | yes (1), yes | yes (1), yes | — | — |
| 8 | 1 | yes (1), yes | yes (1), yes | yes (1), yes | yes (1), yes | no (2), no | no (2), no |
| 8 | 2 | yes (1), yes | yes (1), yes | yes (1), yes | yes (1), yes | yes (2), no | no (6), no |
| 8 | 3 | yes (1), yes | yes (1), yes | yes (1), yes | yes (1), yes | yes (2), no | no (6), no |
| 8 | 4 | yes (1), yes | yes (1), yes | yes (1), yes | yes (1), yes | yes (2), no | yes (4), no |
| 8 | 6 | yes (1), yes | yes (1), yes | yes (1), yes | yes (1), yes | yes (2), no | yes (4), no |
| 8 | 8 | yes (1), yes | yes (1), yes | yes (1), yes | yes (1), yes | yes (2), no | yes (4), no |
| 8 | inf | yes (1), yes | yes (1), yes | yes (1), yes | yes (1), yes | yes (2), no | yes (4), no |

## 3. Static map: components, drift-closure, universality, legibility

| n | b | classes | self-coop classes (μ) | components of G | drift-closed classes (μ) | H-closed (μ) | FairBot old-sense / within-budget universality | PrudentBot old / wb | P* old / wb | legible mass to FairBot / PB / P* |
|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 1 | 26 | 12 (0.497) | 1 | 0 (0) | 0 (0) | 0.795 / 1.000 | — / — | — / — | 0.962 / — / — |
| 6 | 2 | 35 | 14 (0.497) | 1 | 0 (0) | 0 (0) | 0.795 / 0.886 | — / — | — / — | 0.982 / — / — |
| 6 | 3 | 47 | 16 (0.497) | 2 | 0 (0) | 0 (0) | 0.795 / 0.795 | — / — | — / — | 1.000 / — / — |
| 6 | 4 | 51 | 18 (0.497) | 1 | 0 (0) | 0 (0) | 0.795 / 0.795 | — / — | — / — | 1.000 / — / — |
| 6 | 6 | 51 | 18 (0.497) | 1 | 0 (0) | 0 (0) | 0.795 / 0.795 | — / — | — / — | 1.000 / — / — |
| 6 | 8 | 51 | 18 (0.497) | 1 | 0 (0) | 0 (0) | 0.795 / 0.795 | — / — | — / — | 1.000 / — / — |
| 6 | inf | 51 | 18 (0.497) | 1 | 0 (0) | 0 (0) | 0.795 / 0.795 | — / — | — / — | 1.000 / — / — |
| 8 | 1 | 148 | 54 (0.497) | 1 | 0 (0) | 0 (0) | 0.768 / 1.000 | 0.017 / 0.017 | 0.000 / 0.000 | 0.958 / 0.999 / 0.999 |
| 8 | 2 | 243 | 110 (0.497) | 1 | 0 (0) | 0 (0) | 0.772 / 0.876 | 0.333 / 0.975 | 0.101 / 0.208 | 0.979 / 0.960 / 0.963 |
| 8 | 3 | 368 | 160 (0.497) | 1 | 0 (0) | 0 (0) | 0.772 / 0.780 | 0.333 / 0.603 | 0.101 / 0.123 | 0.999 / 0.984 / 0.993 |
| 8 | 4 | 546 | 243 (0.497) | 1 | 0 (0) | 0 (0) | 0.775 / 0.780 | 0.333 / 0.352 | 0.101 / 0.102 | 0.999 / 0.998 / 0.999 |
| 8 | 6 | 543 | 262 (0.497) | 1 | 0 (0) | 0 (0) | 0.779 / 0.779 | 0.334 / 0.336 | 0.102 / 0.102 | 1.000 / 1.000 / 1.000 |
| 8 | 8 | 502 | 251 (0.497) | 1 | 0 (0) | 0 (0) | 0.779 / 0.779 | 0.334 / 0.334 | 0.102 / 0.102 | 1.000 / 1.000 / 1.000 |
| 8 | inf | 471 | 237 (0.497) | 1 | 0 (0) | 0 (0) | 0.779 / 0.779 | 0.334 / 0.334 | 0.102 / 0.102 | 1.000 / 1.000 / 1.000 |

## 4. Siblings beyond n (y = or(x, ψ_K), z = BOX_K(THEM(^D)), built whatever their size)

| n | b | provers x (self-coop, defect on D) | sibling legible to x | sibling adjacent to x | adjacent and suckered by z | μ of x with adjacent sibling | min cost(x reads y) / self-cost(x) | FairBot: cost of its sibling | PrudentBot | P* |
|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 1 | 16 | 0 | 2 | 2 | 3.15e-04 | 3.0 | 9 | — | — |
| 6 | 2 | 16 | 0 | 2 | 2 | 3.15e-04 | 3.0 | 9 | — | — |
| 6 | 3 | 16 | 0 | 2 | 2 | 3.15e-04 | 3.0 | 15 | — | — |
| 6 | 4 | 16 | 0 | 2 | 2 | 3.15e-04 | 3.0 | 15 | — | — |
| 6 | 6 | 16 | 0 | 2 | 2 | 3.15e-04 | 3.0 | 15 | — | — |
| 6 | 8 | 16 | 0 | 2 | 2 | 3.15e-04 | 3.0 | 15 | — | — |
| 6 | inf | 16 | 16 | 16 | 16 | 2.29e-02 | 3.0 | 9 (legible) | — | — |
| 8 | 1 | 104 | 0 | 83 | 83 | 5.83e-04 | 2.0 | 9 | — | — |
| 8 | 2 | 122 | 0 | 63 | 63 | 5.56e-04 | 1.0 | 9 | 9 | — |
| 8 | 3 | 122 | 0 | 63 | 63 | 5.56e-04 | 1.0 | 15 | 15 | — |
| 8 | 4 | 118 | 0 | 62 | 62 | 5.56e-04 | 2.0 | 15 | 15 | 16 |
| 8 | 6 | 112 | 0 | 54 | 54 | 5.45e-04 | 3.0 | 15 | 15 | 16 |
| 8 | 8 | 118 | 0 | 54 | 54 | 5.45e-04 | 2.0 | 15 | 15 | 24 |
| 8 | inf | 118 | 118 | 118 | 118 | 2.42e-02 | 2.0 | 9 (legible) | 9 (legible) | 16 (legible) |

## 5. lim_N under rare mutation (ε→0 chain, PD, w = 0.3, eager_poly=False)

Exit slope: least-squares slope of log(total exit per mutation event from the top cooperative state) on log N over N = 10³–10⁵ (a fitted slope, not an asymptotic claim). Rival share: 1 − largest block share over cooperative states with π ≥ 10⁻³, ALLC excluded.

| arm | n | P(C,C) at N = 10² / 10³ / 10⁴ / 10⁵ | top cooperative state at 10⁵ (π) | top exits at 10⁵: strict / neutral / other | exit slope | rival share at 10³ / 10⁴ / 10⁵ | π(FB, PB, P*) at 10⁵ | classes | terminal / indeterminate / max cut flow |
|---|---|---|---|---|---|---|---|---|---|
| global 1 | 6 | 0.1719 / 0.3673 / 0.6271 / 0.8398 | `BOX(THEM(THEM))` (0.604) | 0.0e+00 / 4.8e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.000 | 0.234, 0.000, 0.000 | 26 | 1 / 0 / 4e-08 |
| global 2 | 6 | 0.1717 / 0.3667 / 0.6262 / 0.8392 | `BOX1(THEM(ME))` (0.303) | 0.0e+00 / 4.9e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.000 | 0.234, 0.000, 0.000 | 35 | 1 / 0 / 6e-07 |
| global 3 | 6 | 0.1705 / 0.3562 / 0.6072 / 0.8272 | `BOX1(THEM(ME))` (0.322) | 0.0e+00 / 4.9e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.000 | 0.250, 0.000, 0.000 | 47 | 1 / 0 / 1e-06 |
| global 4 | 6 | 0.1693 / 0.3454 / 0.5869 / 0.8136 | `BOX(THEM(THEM))` (0.271) | 0.0e+00 / 4.9e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.000 | 0.271, 0.000, 0.000 | 51 | 1 / 0 / 1e-06 |
| global 6 | 6 | 0.1693 / 0.3453 / 0.5869 / 0.8137 | `BOX(THEM(THEM))` (0.271) | 0.0e+00 / 4.9e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.000 | 0.271, 0.000, 0.000 | 51 | 1 / 0 / 1e-06 |
| global 8 | 6 | 0.1693 / 0.3453 / 0.5869 / 0.8137 | `BOX(THEM(THEM))` (0.271) | 0.0e+00 / 4.9e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.000 | 0.271, 0.000, 0.000 | 51 | 1 / 0 / 1e-06 |
| global inf | 6 | 0.1693 / 0.3453 / 0.5869 / 0.8137 | `BOX(THEM(THEM))` (0.271) | 0.0e+00 / 4.9e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.000 | 0.271, 0.000, 0.000 | 51 | 1 / 0 / 1e-06 |
| random 1 | 6 | 0.0737 / 0.1695 / 0.3404 / 0.3584 | `BOX(THEM(^C))` (0.345) | 1.3e-05 / 4.7e-06 / 0.0e+00 | -0.72 | 0.465 / 0.113 / 0.037 | 0.000, 0.000, 0.000 | 66 | 1 / 0 / 4e-10 |
| random 2 | 6 | 0.1483 / 0.2897 / 0.4003 / 0.6181 | `BOX(THEM(ME))` (0.594) | 0.0e+00 / 4.7e-06 / 0.0e+00 | -1.00 | 0.000 / 0.262 / 0.039 | 0.594, 0.000, 0.000 | 66 | 1 / 0 / 1e-08 |
| random 3 | 6 | 0.1355 / 0.2989 / 0.5596 / 0.7996 | `BOX(THEM(ME))` (0.510) | 0.0e+00 / 4.7e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.361 | 0.510, 0.000, 0.000 | 66 | 1 / 0 / 1e-06 |
| random 4 | 6 | 0.1668 / 0.3114 / 0.4999 / 0.7446 | `BOX(THEM(ME))` (0.371) | 0.0e+00 / 4.9e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.000 | 0.371, 0.000, 0.000 | 66 | 1 / 0 / 1e-06 |
| random 6 | 6 | 0.1698 / 0.3480 / 0.5880 / 0.8138 | `BOX(THEM(THEM))` (0.271) | 0.0e+00 / 4.9e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.000 | 0.270, 0.000, 0.000 | 52 | 1 / 0 / 1e-06 |
| random 8 | 6 | 0.1693 / 0.3453 / 0.5869 / 0.8137 | `BOX(THEM(THEM))` (0.271) | 0.0e+00 / 4.9e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.000 | 0.271, 0.000, 0.000 | 51 | 1 / 0 / 1e-06 |
| atom 1 | 6 | 0.1693 / 0.3453 / 0.5869 / 0.8137 | `BOX(THEM(THEM))` (0.271) | 0.0e+00 / 4.9e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.000 | 0.271, 0.000, 0.000 | 51 | 1 / 0 / 1e-06 |
| fixed - | 6 | 0.1709 / 0.3590 / 0.6124 / 0.8305 | `BOX(THEM(THEM))@1` (0.282) | 0.0e+00 / 4.9e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.000 | 0.246, 0.000, 0.000 | 109 | 1 / 0 / 7e-07 |
| penal - | 6 | 0.0566 / 0.1530 / 0.3348 / 0.5957 | `BOX(THEM(THEM))@1` (0.204) | 0.0e+00 / 5.0e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.000 | 0.179, 0.000, 0.000 | 42 | 1 / 0 / 4e-09 |
| clique - | 6 | 0.9990 / 1.0000 / 1.0000 / 1.0000 | `CLIQUE_1` (1.000) | 0.0e+00 / 0.0e+00 / 0.0e+00 | nan | 0.000 / 0.000 / 0.000 | 0.000, 0.000, 0.000 | 53 | 1 / 0 / 1e-09 |
| global 1 | 8 | 0.1811 / 0.3790 / 0.6395 / 0.8470 | `BOX1(THEM(ME))` (0.307) | 0.0e+00 / 4.8e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.000 | 0.232, 0.000, 0.000 | 148 | 1 / 0 / 2e-07 |
| global 2 | 8 | 0.1807 / 0.3806 / 0.6413 / 0.8481 | `BOX1(THEM(ME))` (0.300) | 0.0e+00 / 4.8e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.000 | 0.230, 0.006, 0.000 | 243 | 1 / 0 / 7e-07 |
| global 3 | 8 | 0.1792 / 0.3684 / 0.6184 / 0.8219 | `BOX1(THEM(ME))` (0.346) | 0.0e+00 / 4.8e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.000 | 0.268, 0.007, 0.000 | 368 | 1 / 0 / 1e-06 |
| global 4 | 8 | 0.1821 / 0.3709 / 0.6197 / 0.8227 | `BOX(THEM(ME))` (0.265) | 0.0e+00 / 4.9e-06 / 0.0e+00 | -1.00 | 0.068 / 0.100 / 0.122 | 0.265, 0.004, 0.033 | 546 | 1 / 0 / 1e-06 |
| global 6 | 8 | 0.1821 / 0.3709 / 0.6173 / 0.8135 | `BOX(THEM(ME))` (0.279) | 0.0e+00 / 4.9e-06 / 0.0e+00 | -1.00 | 0.068 / 0.100 / 0.126 | 0.279, 0.010, 0.034 | 543 | 1 / 0 / 1e-06 |
| global 8 | 8 | 0.1821 / 0.3708 / 0.6172 / 0.8135 | `BOX(THEM(ME))` (0.279) | 0.0e+00 / 4.9e-06 / 0.0e+00 | -1.00 | 0.067 / 0.100 / 0.125 | 0.279, 0.011, 0.067 | 502 | 1 / 0 / 1e-06 |
| global inf | 8 | 0.1821 / 0.3707 / 0.6172 / 0.8135 | `BOX(THEM(ME))` (0.279) | 0.0e+00 / 4.9e-06 / 0.0e+00 | -1.00 | 0.067 / 0.100 / 0.125 | 0.279, 0.011, 0.067 | 471 | 1 / 0 / 1e-06 |
| random 1 | 8 | 0.3026 / 0.9348 / 0.9968 / 0.9998 | `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` (0.999) | 0.0e+00 / 5.8e-11 / 0.0e+00 | -1.00 | 0.044 / 0.005 / 0.000 | 0.000, 0.000, 0.999 | 610 | 1 / 0 / 2e-07 |
| random 2 | 8 | 0.1926 / 0.4215 / 0.6804 / 0.8549 | `BOX(THEM(ME))` (0.260) | 0.0e+00 / 4.7e-06 / 0.0e+00 | -1.00 | 0.579 / 0.645 / 0.686 | 0.260, 0.140, 0.000 | 610 | 1 / 0 / 1e-07 |
| random 3 | 8 | 0.2917 / 0.9042 / 0.9804 / 0.9944 | `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` (0.974) | 0.0e+00 / 5.8e-11 / 0.0e+00 | -1.00 | 0.057 / 0.026 / 0.019 | 0.010, 0.000, 0.974 | 610 | 1 / 0 / 2e-07 |
| random 4 | 8 | 0.2840 / 0.8358 / 0.9497 / 0.9839 | `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` (0.917) | 0.0e+00 / 7.9e-11 / 0.0e+00 | -1.00 | 0.102 / 0.071 / 0.067 | 0.040, 0.001, 0.917 | 610 | 1 / 0 / 4e-07 |
| random 6 | 8 | 0.1965 / 0.4141 / 0.6364 / 0.8338 | `BOX(THEM(ME))` (0.440) | 0.0e+00 / 4.7e-06 / 0.0e+00 | -1.00 | 0.224 / 0.172 / 0.127 | 0.440, 0.028, 0.097 | 610 | 1 / 0 / 9e-07 |
| random 8 | 8 | 0.1818 / 0.3699 / 0.6048 / 0.8009 | `BOX(THEM(ME))` (0.298) | 0.0e+00 / 4.9e-06 / 0.0e+00 | -1.00 | 0.071 / 0.114 / 0.143 | 0.298, 0.012, 0.039 | 610 | 1 / 0 / 1e-06 |
| atom 1 | 8 | 0.1779 / 0.3533 / 0.5926 / 0.8016 | `BOX(THEM(ME))` (0.297) | 0.0e+00 / 4.8e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.000 | 0.297, 0.000, 0.000 | 340 | 1 / 0 / 1e-06 |
| fixed - | 8 | 0.1803 / 0.3740 / 0.6277 / 0.8307 | `BOX1(THEM(ME))@2` (0.166) | 0.0e+00 / 4.9e-06 / 0.0e+00 | -1.00 | 0.015 / 0.021 / 0.025 | 0.256, 0.003, 0.009 | 1838 | 1 / 0 / 8e-07 |
| penal - | 8 | 0.0605 / 0.1610 / 0.3477 / 0.6130 | `BOX1(THEM(ME))@1` (0.185) | 0.0e+00 / 5.0e-06 / 0.0e+00 | -1.00 | 0.000 / 0.000 / 0.000 | 0.180, 0.000, 0.000 | 198 | 1 / 0 / 1e-08 |
| clique - | 8 | 0.9990 / 1.0000 / 1.0000 / 1.0000 | `CLIQUE_1` (1.000) | 0.0e+00 / 0.0e+00 / 0.0e+00 | nan | 0.000 / 0.000 / 0.000 | 0.000, 0.000, 0.000 | 485 | 1 / 0 / 2e-09 |

**Per-program budgets: prover π by budget (μ-weighted within merged classes) and the top state's budgets**

- fixed n=6 N=100: b=1 0.041, b=2 0.041, b=3 0.041, b=4 0.041; top state budgets [1, 2, 3, 4]
- fixed n=6 N=1000: b=1 0.092, b=2 0.092, b=3 0.088, b=4 0.085; top state budgets [1, 2, 3, 4]
- fixed n=6 N=10000: b=1 0.162, b=2 0.162, b=3 0.150, b=4 0.138; top state budgets [1, 2, 3, 4]
- fixed n=6 N=100000: b=1 0.221, b=2 0.221, b=3 0.203, b=4 0.186; top state budgets [1, 2, 3, 4]
- penal n=6 N=100: b=1 0.048, b=2 0.006, b=3 0.001; top state budgets [1, 2, 3]
- penal n=6 N=1000: b=1 0.134, b=2 0.016, b=3 0.003; top state budgets [1, 2, 3]
- penal n=6 N=10000: b=1 0.294, b=2 0.035, b=3 0.006; top state budgets [1, 2, 3]
- penal n=6 N=100000: b=1 0.523, b=2 0.062, b=3 0.011; top state budgets [1, 2, 3]
- fixed n=8 N=100: b=1 0.043, b=2 0.043, b=3 0.043, b=4 0.044; top state budgets [2, 3]
- fixed n=8 N=1000: b=1 0.095, b=2 0.095, b=3 0.091, b=4 0.092; top state budgets [2, 3]
- fixed n=8 N=10000: b=1 0.165, b=2 0.164, b=3 0.149, b=4 0.149; top state budgets [2, 3]
- fixed n=8 N=100000: b=1 0.235, b=2 0.223, b=3 0.189, b=4 0.184; top state budgets [2, 3]
- penal n=8 N=100: b=1 0.050, b=2 0.007, b=3 0.001, b=4 0.000; top state budgets [1]
- penal n=8 N=1000: b=1 0.138, b=2 0.018, b=3 0.003, b=4 0.000; top state budgets [1]
- penal n=8 N=10000: b=1 0.300, b=2 0.040, b=3 0.007, b=4 0.001; top state budgets [1]
- penal n=8 N=100000: b=1 0.530, b=2 0.070, b=3 0.012, b=4 0.002; top state budgets [1]

**Support at N = 10⁵ (π ≥ 10⁻³, top 6) and top exit destinations**

- global 1 n=6: mono {BOX(THEM(THEM)):1} 0.604; mono {BOX(THEM(ME)):1} 0.234; mono {D:1} 0.160; mono {BOX1(THEM(THEM)):1} 0.002. Exits: `C` (neutral) 4.7e-06; `BOX(THEM(ME))` (neutral) 4.9e-08; `BOX1(THEM(THEM))` (neutral) 4.9e-08
- global 2 n=6: mono {BOX1(THEM(ME)):1} 0.303; mono {BOX(THEM(THEM)):1} 0.301; mono {BOX(THEM(ME)):1} 0.234; mono {D:1} 0.161; mono {BOX1(THEM(THEM)):1} 0.002. Exits: `C` (neutral) 4.7e-06; `BOX(THEM(THEM))` (neutral) 6.4e-08; `BOX(THEM(ME))` (neutral) 4.9e-08
- global 3 n=6: mono {BOX1(THEM(ME)):1} 0.322; mono {BOX(THEM(THEM)):1} 0.253; mono {BOX(THEM(ME)):1} 0.250; mono {D:1} 0.173; mono {BOX1(THEM(THEM)):1} 0.002. Exits: `C` (neutral) 4.7e-06; `BOX(THEM(THEM))` (neutral) 5.0e-08; `BOX(THEM(ME))` (neutral) 4.9e-08
- global 4 n=6: mono {BOX(THEM(THEM)):1} 0.271; mono {BOX(THEM(ME)):1} 0.271; mono {BOX1(THEM(ME)):1} 0.269; mono {D:1} 0.186; mono {BOX1(THEM(THEM)):1} 0.002. Exits: `C` (neutral) 4.7e-06; `BOX(THEM(ME))` (neutral) 5.0e-08; `BOX1(THEM(ME))` (neutral) 5.0e-08
- global 6 n=6: mono {BOX(THEM(THEM)):1} 0.271; mono {BOX(THEM(ME)):1} 0.271; mono {BOX1(THEM(ME)):1} 0.269; mono {D:1} 0.186; mono {BOX1(THEM(THEM)):1} 0.002. Exits: `C` (neutral) 4.7e-06; `BOX(THEM(ME))` (neutral) 5.0e-08; `BOX1(THEM(ME))` (neutral) 5.0e-08
- global 8 n=6: mono {BOX(THEM(THEM)):1} 0.271; mono {BOX(THEM(ME)):1} 0.271; mono {BOX1(THEM(ME)):1} 0.269; mono {D:1} 0.186; mono {BOX1(THEM(THEM)):1} 0.002. Exits: `C` (neutral) 4.7e-06; `BOX(THEM(ME))` (neutral) 5.0e-08; `BOX1(THEM(ME))` (neutral) 5.0e-08
- global inf n=6: mono {BOX(THEM(THEM)):1} 0.271; mono {BOX(THEM(ME)):1} 0.271; mono {BOX1(THEM(ME)):1} 0.269; mono {D:1} 0.186; mono {BOX1(THEM(THEM)):1} 0.002. Exits: `C` (neutral) 4.7e-06; `BOX(THEM(ME))` (neutral) 5.0e-08; `BOX1(THEM(ME))` (neutral) 5.0e-08
- random 1 n=6: mono {D:1} 0.642; mono {BOX(THEM(^C)):1} 0.345; mono {BOX1(THEM(THEM)):1} 0.013. Exits: `BOX(THEM(^BOX1(THEM(THEM))))` (strict) 6.4e-06; `BOX1(THEM(^BOX1(THEM(ME))))` (strict) 6.4e-06; `C` (neutral) 4.7e-06
- random 2 n=6: mono {BOX(THEM(ME)):1} 0.594; mono {D:1} 0.382; mono {BOX1(THEM(^C)):1} 0.008; mono {BOX1(THEM(THEM)):1} 0.008; mono {BOX(THEM(THEM)):1} 0.008. Exits: `C` (neutral) 4.7e-06; `not(BOXD(THEM(THEM)))` (neutral) 1.2e-08; `not(BOX1(THEM(THEM)))` (neutral) 1.2e-08
- random 3 n=6: mono {BOX(THEM(ME)):1} 0.510; mono {BOX1(THEM(ME)):1} 0.288; mono {D:1} 0.200. Exits: `C` (neutral) 4.7e-06; `BOX1(THEM(^C))` (neutral) 1.4e-08; `not(BOX(THEM(THEM)))` (neutral) 1.2e-08
- random 4 n=6: mono {BOX(THEM(ME)):1} 0.371; mono {BOX1(THEM(ME)):1} 0.363; mono {D:1} 0.255; mono {BOX1(THEM(THEM)):1} 0.005; mono {BOX1(THEM(^BOX(THEM(THEM)))):1} 0.002; mono {BOX(THEM(^BOX(THEM(ME)))):1} 0.001. Exits: `C` (neutral) 4.7e-06; `BOX(THEM(THEM))` (neutral) 4.9e-08; `BOX1(THEM(ME))` (neutral) 4.9e-08
- random 6 n=6: mono {BOX(THEM(THEM)):1} 0.271; mono {BOX(THEM(ME)):1} 0.270; mono {BOX1(THEM(ME)):1} 0.269; mono {D:1} 0.186; mono {BOX1(THEM(THEM)):1} 0.002. Exits: `C` (neutral) 4.7e-06; `BOX(THEM(ME))` (neutral) 5.0e-08; `BOX1(THEM(ME))` (neutral) 5.0e-08
- random 8 n=6: mono {BOX(THEM(THEM)):1} 0.271; mono {BOX(THEM(ME)):1} 0.271; mono {BOX1(THEM(ME)):1} 0.269; mono {D:1} 0.186; mono {BOX1(THEM(THEM)):1} 0.002. Exits: `C` (neutral) 4.7e-06; `BOX(THEM(ME))` (neutral) 5.0e-08; `BOX1(THEM(ME))` (neutral) 5.0e-08
- atom 1 n=6: mono {BOX(THEM(THEM)):1} 0.271; mono {BOX(THEM(ME)):1} 0.271; mono {BOX1(THEM(ME)):1} 0.269; mono {D:1} 0.186; mono {BOX1(THEM(THEM)):1} 0.002. Exits: `C` (neutral) 4.7e-06; `BOX(THEM(ME))` (neutral) 5.0e-08; `BOX1(THEM(ME))` (neutral) 5.0e-08
- fixed - n=6: mono {BOX(THEM(THEM))@1:1} 0.282; mono {BOX(THEM(ME))@1:1} 0.246; mono {BOX1(THEM(ME))@2:1} 0.220; mono {D:1} 0.169; mono {BOX1(THEM(ME))@1:1} 0.080; mono {BOX1(THEM(THEM))@1:1} 0.001. Exits: `C` (neutral) 4.7e-06; `BOX(THEM(ME))@1` (neutral) 4.9e-08; `BOX1(THEM(ME))@2` (neutral) 4.4e-08
- penal - n=6: mono {D:1} 0.404; mono {BOX(THEM(THEM))@1:1} 0.204; mono {BOX1(THEM(ME))@1:1} 0.179; mono {BOX(THEM(ME))@1:1} 0.179; mono {BOX1(THEM(ME))@2:1} 0.025; mono {BOX1(THEM(THEM))@1:1} 0.008. Exits: `C` (neutral) 4.9e-06; `BOX(THEM(ME))@1` (neutral) 1.6e-08; `BOX1(THEM(ME))@1` (neutral) 1.6e-08
- clique - n=6: mono {CLIQUE_1:1} 1.000. Exits: `C` (other) 0.0e+00; `D` (other) 0.0e+00; `BOX(THEM(ME))` (other) 0.0e+00
- global 1 n=8: mono {BOX1(THEM(ME)):1} 0.307; mono {BOX(THEM(THEM)):1} 0.306; mono {BOX(THEM(ME)):1} 0.232; mono {D:1} 0.153; mono {BOX1(THEM(THEM)):1} 0.002. Exits: `C` (neutral) 4.7e-06; `BOX(THEM(THEM))` (neutral) 6.7e-08; `BOX(THEM(ME))` (neutral) 5.1e-08
- global 2 n=8: mono {BOX1(THEM(ME)):1} 0.300; mono {BOX(THEM(ME)):1} 0.230; mono {BOX(THEM(THEM)):1} 0.230; mono {D:1} 0.152; mono {BOX(THEM(^C)):1} 0.069; mono {and(BOX(THEM(ME)),BOXD1(THEM(^D))):1} 0.006. Exits: `C` (neutral) 4.7e-06; `BOX(THEM(ME))` (neutral) 5.1e-08; `BOX(THEM(THEM))` (neutral) 5.1e-08
- global 3 n=8: mono {BOX1(THEM(ME)):1} 0.346; mono {BOX(THEM(ME)):1} 0.268; mono {BOX(THEM(THEM)):1} 0.185; mono {D:1} 0.178; mono {and(BOX(THEM(ME)),BOXD1(THEM(^D))):1} 0.007; mono {BOX1(THEM(^BOX(THEM(THEM)))):1} 0.003. Exits: `C` (neutral) 4.7e-06; `BOX(THEM(ME))` (neutral) 5.1e-08; `BOX(THEM(THEM))` (neutral) 5.0e-08
- global 4 n=8: mono {BOX(THEM(ME)):1} 0.265; mono {BOX1(THEM(ME)):1} 0.264; mono {BOX(THEM(THEM)):1} 0.179; mono {D:1} 0.177; mono {and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):1} 0.033; mono {and(BOX1(THEM(ME)),not(BOX(THEM(THEM)))):1} 0.033. Exits: `C` (neutral) 4.7e-06; `BOX1(THEM(ME))` (neutral) 5.1e-08; `BOX(THEM(THEM))` (neutral) 5.0e-08
- global 6 n=8: mono {BOX(THEM(ME)):1} 0.279; mono {BOX1(THEM(ME)):1} 0.277; mono {D:1} 0.186; mono {BOX(THEM(THEM)):1} 0.135; mono {and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):1} 0.034; mono {and(BOX1(THEM(THEM)),not(BOX(THEM(THEM)))):1} 0.034. Exits: `C` (neutral) 4.7e-06; `BOX1(THEM(ME))` (neutral) 5.1e-08; `BOX(THEM(THEM))` (neutral) 5.0e-08
- global 8 n=8: mono {BOX(THEM(ME)):1} 0.279; mono {BOX1(THEM(ME)):1} 0.277; mono {D:1} 0.186; mono {BOX(THEM(THEM)):1} 0.135; mono {and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):1} 0.067; mono {and(BOX1(THEM(ME)),not(BOX(THEM(THEM)))):1} 0.034. Exits: `C` (neutral) 4.7e-06; `BOX1(THEM(ME))` (neutral) 5.1e-08; `BOX(THEM(THEM))` (neutral) 5.1e-08
- global inf n=8: mono {BOX(THEM(ME)):1} 0.279; mono {BOX1(THEM(ME)):1} 0.277; mono {D:1} 0.186; mono {BOX(THEM(THEM)):1} 0.135; mono {and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):1} 0.067; mono {and(BOX1(THEM(ME)),not(BOX(THEM(THEM)))):1} 0.034. Exits: `C` (neutral) 4.7e-06; `BOX1(THEM(ME))` (neutral) 5.1e-08; `BOX(THEM(THEM))` (neutral) 5.1e-08
- random 1 n=8: mono {and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):1} 0.999. Exits: `not(BOX(THEM(^BOX(THEM(ME)))))` (neutral) 3.8e-11; `not(and(BOX(THEM(ME)),BOXD(THEM(ME))))` (neutral) 1.4e-11; `not(BOX(THEM(^not(BOXD(THEM(THEM))))))` (neutral) 6.8e-12
- random 2 n=8: mono {BOX(THEM(ME)):1} 0.260; mono {BOX1(THEM(ME)):1} 0.252; mono {BOX1(THEM(THEM)):1} 0.187; mono {D:1} 0.145; mono {and(BOX(THEM(ME)),BOXD1(THEM(^D))):1} 0.140; mono {BOX(THEM(THEM)):1} 0.017. Exits: `C` (neutral) 4.7e-06; `not(BOX(THEM(ME)))` (neutral) 1.3e-08; `not(BOXD(THEM(^D)))` (neutral) 2.3e-09
- random 3 n=8: mono {and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):1} 0.974; mono {BOX(THEM(ME)):1} 0.010; mono {BOX1(THEM(ME)):1} 0.009; mono {D:1} 0.006. Exits: `not(BOX(THEM(^BOX(THEM(ME)))))` (neutral) 3.8e-11; `not(and(BOX(THEM(ME)),BOXD(THEM(ME))))` (neutral) 1.4e-11; `not(BOX(THEM(^not(BOXD(THEM(THEM))))))` (neutral) 6.8e-12
- random 4 n=8: mono {and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):1} 0.917; mono {BOX(THEM(ME)):1} 0.040; mono {BOX1(THEM(ME)):1} 0.025; mono {D:1} 0.016. Exits: `not(BOX(THEM(^BOX(THEM(ME)))))` (neutral) 3.8e-11; `not(and(BOX(THEM(ME)),BOXD(THEM(ME))))` (neutral) 1.4e-11; `not(and(BOX(THEM(ME)),BOXD1(THEM(ME))))` (neutral) 1.4e-11
- random 6 n=8: mono {BOX(THEM(ME)):1} 0.440; mono {BOX1(THEM(ME)):1} 0.249; mono {D:1} 0.166; mono {and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):1} 0.097; mono {and(BOX(THEM(ME)),BOXD1(THEM(^D))):1} 0.028; mono {and(BOX1(THEM(THEM)),not(BOX(THEM(THEM)))):1} 0.008. Exits: `C` (neutral) 4.7e-06; `BOX1(THEM(ME))` (neutral) 5.0e-08; `BOX1(THEM(^C))` (neutral) 1.5e-08
- random 8 n=8: mono {BOX(THEM(ME)):1} 0.298; mono {BOX1(THEM(ME)):1} 0.296; mono {D:1} 0.199; mono {BOX(THEM(THEM)):1} 0.052; mono {and(BOX1(THEM(ME)),not(BOX(THEM(ME)))):1} 0.039; mono {and(BOX1(THEM(THEM)),not(BOX(THEM(THEM)))):1} 0.039. Exits: `C` (neutral) 4.7e-06; `BOX(THEM(THEM))` (neutral) 5.0e-08; `BOX1(THEM(ME))` (neutral) 5.0e-08
- atom 1 n=8: mono {BOX(THEM(ME)):1} 0.297; mono {BOX1(THEM(ME)):1} 0.295; mono {BOX(THEM(THEM)):1} 0.201; mono {D:1} 0.198; mono {BOX1(THEM(THEM)):1} 0.002; mono {BOX(THEM(^BOX(THEM(THEM)))):1} 0.002. Exits: `C` (neutral) 4.7e-06; `BOX1(THEM(ME))` (neutral) 5.1e-08; `BOX(THEM(THEM))` (neutral) 5.0e-08
- fixed - n=8: mono {D:1} 0.169; mono {BOX1(THEM(ME))@2:1} 0.166; mono {BOX(THEM(ME))@2:1} 0.128; mono {BOX1(THEM(ME))@1:1} 0.085; mono {BOX(THEM(THEM))@1:1} 0.084; mono {BOX(THEM(ME))@1:1} 0.064. Exits: `C` (neutral) 4.7e-06; `BOX(THEM(ME))@2` (neutral) 2.5e-08; `BOX1(THEM(THEM))@2` (neutral) 2.5e-08
- penal - n=8: mono {D:1} 0.387; mono {BOX1(THEM(ME))@1:1} 0.185; mono {BOX(THEM(THEM))@1:1} 0.183; mono {BOX(THEM(ME))@1:1} 0.156; mono {BOX1(THEM(ME))@2:1} 0.029; mono {BOX(THEM(ME))@2:1} 0.024. Exits: `C` (neutral) 4.9e-06; `BOX(THEM(THEM))@1` (neutral) 1.7e-08; `BOX(THEM(ME))@1` (neutral) 1.4e-08
- clique - n=8: mono {CLIQUE_1:1} 1.000. Exits: `D` (other) 0.0e+00; `C` (other) 0.0e+00; `BOX1(THEM(ME))` (other) 0.0e+00

## 6. ε = 0 seeding lottery (n = 6, iid from μ, paired seeds across b)

Efficient fraction with Wilson 95% intervals; paired difference against b = ∞ (same seeds) with a bootstrap 95% interval; equivalence margin 0.15. Free-arm reference from "Almost all seeds?" (different seeds): 0.25 / 0.45 / 0.80 at I = 4 (N = 100 / 400 / 1,600); 1.00 at (100, 64) and (100, 256).

| arm | cell (N, I, mN) | runs | efficient | defecting | other / unresolved | efficient fraction [95%] | paired diff vs ∞ [95%] | equivalent within 0.15 | median ALLC extinction gen | cooperative-core count at ALLC extinction (median; runs with 0) |
|---|---|---|---|---|---|---|---|---|---|---|
| global 1 | (100, 4, 1.0) | 40 | 8 | 32 | 0 | 0.20 [0.10, 0.35] | +0.00 [-0.12, +0.12] (n=40) | yes | 40 | 0; 29 |
| global 1 | (400, 4, 1.0) | 40 | 21 | 19 | 0 | 0.53 [0.37, 0.67] | -0.03 [-0.20, +0.15] (n=40) | unresolved | 40 | 57; 14 |
| global 1 | (1600, 4, 1.0) | 40 | 32 | 8 | 0 | 0.80 [0.65, 0.90] | -0.03 [-0.17, +0.12] (n=40) | unresolved | 40 | 157; 1 |
| global 1 | (100, 64, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | +0.00 [+0.00, +0.00] (n=20) | yes | 40 | 864; 0 |
| global 1 | (100, 256, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | +0.00 [+0.00, +0.00] (n=20) | yes | 60 | 3570; 0 |
| global 1 | (400, 4, 0.0) | 20 | per island: 15 / 80 | | | per-island 0.188 [0.117, 0.287] | | | | |
| global 1 | (100, 64, 0.0) | 20 | per island: 106 / 1280 | | | per-island 0.083 [0.069, 0.099] | | | | |
| global 2 | (100, 4, 1.0) | 20 | 7 | 13 | 0 | 0.35 [0.18, 0.57] | +0.05 [+0.00, +0.15] (n=20) | yes | 40 | 0; 12 |
| global 2 | (400, 4, 1.0) | 40 | 20 | 20 | 0 | 0.50 [0.35, 0.65] | -0.05 [-0.20, +0.07] (n=40) | unresolved | 40 | 29; 13 |
| global 2 | (1600, 4, 1.0) | 40 | 33 | 7 | 0 | 0.82 [0.68, 0.91] | +0.00 [-0.12, +0.12] (n=40) | yes | 40 | 211; 1 |
| global 2 | (100, 64, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | +0.00 [+0.00, +0.00] (n=20) | yes | 40 | 760; 0 |
| global 2 | (100, 256, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | +0.00 [+0.00, +0.00] (n=20) | yes | 60 | 3791; 0 |
| global 2 | (400, 4, 0.0) | 20 | per island: 15 / 80 | | | per-island 0.188 [0.117, 0.287] | | | | |
| global 2 | (100, 64, 0.0) | 20 | per island: 98 / 1280 | | | per-island 0.077 [0.063, 0.092] | | | | |
| global 3 | (100, 4, 1.0) | 20 | 7 | 13 | 0 | 0.35 [0.18, 0.57] | +0.05 [+0.00, +0.15] (n=20) | yes | 40 | 0; 13 |
| global 3 | (400, 4, 1.0) | 40 | 19 | 21 | 0 | 0.47 [0.33, 0.63] | -0.07 [-0.25, +0.10] (n=40) | unresolved | 40 | 29; 15 |
| global 3 | (1600, 4, 1.0) | 40 | 32 | 8 | 0 | 0.80 [0.65, 0.90] | -0.03 [-0.12, +0.07] (n=40) | yes | 40 | 207; 1 |
| global 3 | (100, 64, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | +0.00 [+0.00, +0.00] (n=20) | yes | 40 | 756; 0 |
| global 3 | (100, 256, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | +0.00 [+0.00, +0.00] (n=20) | yes | 60 | 3561; 0 |
| global 3 | (400, 4, 0.0) | 20 | per island: 14 / 80 | | | per-island 0.175 [0.107, 0.273] | | | | |
| global 3 | (100, 64, 0.0) | 20 | per island: 101 / 1280 | | | per-island 0.079 [0.065, 0.095] | | | | |
| global 4 | (100, 4, 1.0) | 20 | 6 | 14 | 0 | 0.30 [0.15, 0.52] | +0.00 [+0.00, +0.00] (n=20) | yes | 40 | 0; 14 |
| global 4 | (400, 4, 1.0) | 20 | 10 | 10 | 0 | 0.50 [0.30, 0.70] | +0.00 [+0.00, +0.00] (n=20) | yes | 40 | 20; 8 |
| global 4 | (1600, 4, 1.0) | 20 | 15 | 5 | 0 | 0.75 [0.53, 0.89] | +0.00 [+0.00, +0.00] (n=20) | yes | 40 | 116; 1 |
| global 4 | (100, 64, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | +0.00 [+0.00, +0.00] (n=20) | yes | 40 | 748; 0 |
| global 4 | (100, 256, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | +0.00 [+0.00, +0.00] (n=20) | yes | 60 | 3733; 0 |
| global 4 | (400, 4, 0.0) | 20 | per island: 15 / 80 | | | per-island 0.188 [0.117, 0.287] | | | | |
| global 4 | (100, 64, 0.0) | 20 | per island: 101 / 1280 | | | per-island 0.079 [0.065, 0.095] | | | | |
| global 6 | (100, 4, 1.0) | 20 | 6 | 14 | 0 | 0.30 [0.15, 0.52] | +0.00 [+0.00, +0.00] (n=20) | yes | 40 | 0; 14 |
| global 6 | (400, 4, 1.0) | 20 | 10 | 10 | 0 | 0.50 [0.30, 0.70] | +0.00 [+0.00, +0.00] (n=20) | yes | 40 | 20; 8 |
| global 6 | (1600, 4, 1.0) | 20 | 15 | 5 | 0 | 0.75 [0.53, 0.89] | +0.00 [+0.00, +0.00] (n=20) | yes | 40 | 116; 1 |
| global 6 | (100, 64, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | +0.00 [+0.00, +0.00] (n=20) | yes | 40 | 748; 0 |
| global 6 | (100, 256, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | +0.00 [+0.00, +0.00] (n=20) | yes | 60 | 3733; 0 |
| global 6 | (400, 4, 0.0) | 20 | per island: 15 / 80 | | | per-island 0.188 [0.117, 0.287] | | | | |
| global 6 | (100, 64, 0.0) | 20 | per island: 101 / 1280 | | | per-island 0.079 [0.065, 0.095] | | | | |
| global 8 | (100, 4, 1.0) | 20 | 6 | 14 | 0 | 0.30 [0.15, 0.52] | +0.00 [+0.00, +0.00] (n=20) | yes | 40 | 0; 14 |
| global 8 | (400, 4, 1.0) | 20 | 10 | 10 | 0 | 0.50 [0.30, 0.70] | +0.00 [+0.00, +0.00] (n=20) | yes | 40 | 20; 8 |
| global 8 | (1600, 4, 1.0) | 20 | 15 | 5 | 0 | 0.75 [0.53, 0.89] | +0.00 [+0.00, +0.00] (n=20) | yes | 40 | 116; 1 |
| global 8 | (100, 64, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | +0.00 [+0.00, +0.00] (n=20) | yes | 40 | 748; 0 |
| global 8 | (100, 256, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | +0.00 [+0.00, +0.00] (n=20) | yes | 60 | 3733; 0 |
| global 8 | (400, 4, 0.0) | 20 | per island: 15 / 80 | | | per-island 0.188 [0.117, 0.287] | | | | |
| global 8 | (100, 64, 0.0) | 20 | per island: 101 / 1280 | | | per-island 0.079 [0.065, 0.095] | | | | |
| global inf | (100, 4, 1.0) | 40 | 8 | 32 | 0 | 0.20 [0.10, 0.35] | — | — | 40 | 0; 31 |
| global inf | (400, 4, 1.0) | 40 | 22 | 18 | 0 | 0.55 [0.40, 0.69] | — | — | 40 | 31; 11 |
| global inf | (1600, 4, 1.0) | 40 | 33 | 7 | 0 | 0.82 [0.68, 0.91] | — | — | 40 | 159; 1 |
| global inf | (100, 64, 1.0) | 40 | 40 | 0 | 0 | 1.00 [0.91, 1.00] | — | — | 40 | 670; 0 |
| global inf | (100, 256, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | — | — | 60 | 3733; 0 |
| global inf | (400, 4, 0.0) | 20 | per island: 15 / 80 | | | per-island 0.188 [0.117, 0.287] | | | | |
| global inf | (100, 64, 0.0) | 20 | per island: 101 / 1280 | | | per-island 0.079 [0.065, 0.095] | | | | |
| random 1 | (100, 4, 1.0) | 20 | 2 | 18 | 0 | 0.10 [0.03, 0.30] | -0.20 [-0.40, -0.05] (n=20) | no | 40 | 0; 18 |
| random 1 | (400, 4, 1.0) | 20 | 5 | 15 | 0 | 0.25 [0.11, 0.47] | -0.25 [-0.55, +0.05] (n=20) | no | 40 | 0; 14 |
| random 1 | (1600, 4, 1.0) | 20 | 7 | 13 | 0 | 0.35 [0.18, 0.57] | -0.40 [-0.60, -0.20] (n=20) | no | 40 | 20; 2 |
| random 1 | (100, 64, 1.0) | 40 | 35 | 5 | 0 | 0.88 [0.74, 0.95] | -0.12 [-0.25, -0.03] (n=40) | unresolved | 40 | 277; 4 |
| random 1 | (100, 256, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | +0.00 [+0.00, +0.00] (n=20) | yes | 60 | 1366; 0 |
| random 1 | (400, 4, 0.0) | 20 | per island: 11 / 80 | | | per-island 0.138 [0.079, 0.230] | | | | |
| random 1 | (100, 64, 0.0) | 20 | per island: 61 / 1280 | | | per-island 0.048 [0.037, 0.061] | | | | |
| random 2 | (100, 4, 1.0) | 20 | 5 | 15 | 0 | 0.25 [0.11, 0.47] | -0.05 [-0.15, +0.00] (n=20) | yes | 40 | 0; 15 |
| random 2 | (400, 4, 1.0) | 40 | 22 | 18 | 0 | 0.55 [0.40, 0.69] | +0.00 [-0.15, +0.15] (n=40) | yes | 40 | 42; 13 |
| random 2 | (1600, 4, 1.0) | 20 | 15 | 5 | 0 | 0.75 [0.53, 0.89] | +0.00 [-0.15, +0.15] (n=20) | yes | 40 | 156; 0 |
| random 2 | (100, 64, 1.0) | 20 | 19 | 1 | 0 | 0.95 [0.76, 0.99] | -0.05 [-0.15, +0.00] (n=20) | yes | 40 | 572; 1 |
| random 2 | (100, 256, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | +0.00 [+0.00, +0.00] (n=20) | yes | 60 | 3366; 0 |
| random 2 | (400, 4, 0.0) | 20 | per island: 16 / 80 | | | per-island 0.200 [0.127, 0.300] | | | | |
| random 2 | (100, 64, 0.0) | 20 | per island: 109 / 1280 | | | per-island 0.085 [0.071, 0.102] | | | | |
| random 3 | (100, 4, 1.0) | 20 | 5 | 15 | 0 | 0.25 [0.11, 0.47] | -0.05 [-0.15, +0.00] (n=20) | yes | 40 | 0; 15 |
| random 3 | (400, 4, 1.0) | 20 | 14 | 6 | 0 | 0.70 [0.48, 0.85] | +0.20 [-0.10, +0.50] (n=20) | no | 40 | 38; 6 |
| random 3 | (1600, 4, 1.0) | 40 | 27 | 13 | 0 | 0.68 [0.52, 0.80] | -0.15 [-0.28, -0.03] (n=40) | unresolved | 40 | 109; 0 |
| random 3 | (100, 64, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | +0.00 [+0.00, +0.00] (n=20) | yes | 40 | 584; 0 |
| random 3 | (100, 256, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | +0.00 [+0.00, +0.00] (n=20) | yes | 60 | 2700; 0 |
| random 3 | (400, 4, 0.0) | 20 | per island: 16 / 80 | | | per-island 0.200 [0.127, 0.300] | | | | |
| random 3 | (100, 64, 0.0) | 20 | per island: 97 / 1280 | | | per-island 0.076 [0.063, 0.092] | | | | |
| random 4 | (100, 4, 1.0) | 20 | 5 | 15 | 0 | 0.25 [0.11, 0.47] | -0.05 [-0.15, +0.00] (n=20) | yes | 40 | 0; 14 |
| random 4 | (400, 4, 1.0) | 20 | 14 | 6 | 0 | 0.70 [0.48, 0.85] | +0.20 [-0.10, +0.50] (n=20) | no | 40 | 40; 6 |
| random 4 | (1600, 4, 1.0) | 40 | 30 | 10 | 0 | 0.75 [0.60, 0.86] | -0.07 [-0.20, +0.05] (n=40) | unresolved | 40 | 161; 0 |
| random 4 | (100, 64, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | +0.00 [+0.00, +0.00] (n=20) | yes | 40 | 572; 0 |
| random 4 | (100, 256, 1.0) | 20 | 20 | 0 | 0 | 1.00 [0.84, 1.00] | +0.00 [+0.00, +0.00] (n=20) | yes | 60 | 3528; 0 |
| random 4 | (400, 4, 0.0) | 20 | per island: 19 / 80 | | | per-island 0.237 [0.158, 0.341] | | | | |
| random 4 | (100, 64, 0.0) | 20 | per island: 118 / 1280 | | | per-island 0.092 [0.078, 0.109] | | | | |
