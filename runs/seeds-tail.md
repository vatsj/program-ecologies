# Seeds tail in n (static) and island merging at I = 4

Spec `specs/2026-10-05-seeds-tail.md`; predictions `predictions/2026-10-05-seeds-tail.md`; code `src/seeds_tail.py`, `src/seeds_tail_report.py`. Modal arm, PD, w = 0.3, ε = 0.

## Part A: static tail (modal arm, n = 6–12)

One evaluation at n = 12 (22690 canonical functions, stable at world 13, 51 s on 3 threads); every smaller cutoff is a sub-block (canonical ids are a prefix, checked; the n = 9 sub-block reproduces a direct `modal.build(9)` exactly: classes 863, μ_est, μ_core and μ_pf equal to 1e-15). n = 13 was not run: the machine was under memory pressure from sibling pools, and n = 12 is where the predictions are stated.

Units: **raw** (shell s has mass 1/(2s²); the infinite prior totals π²/12 ≈ 0.822, not 1), **inf** = raw/(π²/12), **cut** = raw/retained(n) (the seeding law). ω(n) = π²/12 − retained(n) is the omitted mass.

### Masses by cutoff

| n | classes | establisher / faker / core classes | retained | ω(n) | μ_est raw | μ_est cut | μ_est inf | bound on μ_est(∞) inf | μ_core cut | fakeable establishers cut | μ_pf cut (global union) | r = μ_pf/μ_est | μ-weighted faker exposure (cut) | FairBot, `BOX1(THEM(ME))` unfakeable |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 51 | 9 / 37 / 3 | 0.7457 | 0.0768 | 0.01706 | 0.02287 | 0.02074 | 0.1141 | 0.01485 | 0.00802 | 0.05256 | 2.30 | 0.00146 | True, True |
| 7 | 172 | 38 / 147 / 5 | 0.7559 | 0.0666 | 0.01798 | 0.02379 | 0.02187 | 0.1028 | 0.01018 | 0.01361 | 0.05518 | 2.32 | 0.00179 | True, True |
| 8 | 471 | 96 / 381 / 9 | 0.7637 | 0.0588 | 0.01848 | 0.02419 | 0.02247 | 0.0939 | 0.01024 | 0.01395 | 0.05951 | 2.46 | 0.00200 | True, True |
| 9 | 863 | 148 / 678 / 13 | 0.7699 | 0.0526 | 0.01895 | 0.02461 | 0.02304 | 0.0870 | 0.01035 | 0.01426 | 0.06084 | 2.47 | 0.00219 | True, True |
| 10 | 1752 | 319 / 1524 / 15 | 0.7749 | 0.0476 | 0.01927 | 0.02486 | 0.02342 | 0.0813 | 0.01036 | 0.01450 | 0.06181 | 2.49 | 0.00234 | True, True |
| 11 | 5545 | 1065 / 5106 / 38 | 0.7790 | 0.0435 | 0.01955 | 0.02510 | 0.02377 | 0.0766 | 0.01041 | 0.01469 | 0.06326 | 2.52 | 0.00246 | True, True |
| 12 | 13514 | 2505 / 12245 / 85 | 0.7825 | 0.0400 | 0.01977 | 0.02526 | 0.02404 | 0.0726 | 0.01044 | 0.01483 | 0.06395 | 2.53 | 0.00256 | True, True |

- Bound: μ_est(∞) ≤ (raw(12) + ω(12))/(π²/12) = 0.0726 (inf units); lower bound raw(12)/(π²/12) = 0.0240. 1/s²-tail extrapolation (mean shell fraction over s = 10–12, 0.0652, times ω(12)): μ_est(∞) ≈ 0.0272 (inf); μ_pf(∞) ≈ 0.0715; r(∞) ≈ 2.63.
- The global faker union is dominated by the fakers of two rare, highly exploitable establishers, `not(BOXD(THEM(^C)))` and `not(BOXD1(THEM(^C)))` (μ_cut 0.0003 each, faker mass 0.042–0.047 each, FairBot among their fakers). The μ-weighted exposure (the faker mass facing a μ-random establisher) is 20–25× smaller than the union.

### Shell decomposition at n = 12 (shell fraction f(s) = shell contribution / (1/(2s²)))

| s | 1/(2s²) | μ_est contribution (raw) | f_est(s) | ratio to s − 1 | f_pf(s) | f_core(s) |
|---|---|---|---|---|---|---|
| 1 | 0.50000 | 0.000e+00 | 0.0000 | – | 0.0000 | 0.0000 |
| 2 | 0.12500 | 0.000e+00 | 0.0000 | – | 0.0000 | 0.0000 |
| 3 | 0.05556 | 1.235e-02 | 0.2222 | – | 0.4444 | 0.1111 |
| 4 | 0.03125 | 1.488e-03 | 0.0476 | 0.12 | 0.2619 | 0.0000 |
| 5 | 0.02000 | 2.376e-03 | 0.1188 | 1.60 | 0.2673 | 0.0495 |
| 6 | 0.01389 | 8.473e-04 | 0.0610 | 0.36 | 0.2347 | 0.0133 |
| 7 | 0.01020 | 9.271e-04 | 0.0909 | 1.09 | 0.2555 | 0.0324 |
| 8 | 0.00781 | 4.926e-04 | 0.0631 | 0.53 | 0.2230 | 0.0152 |
| 9 | 0.00617 | 4.703e-04 | 0.0762 | 0.95 | 0.2345 | 0.0241 |
| 10 | 0.00500 | 3.178e-04 | 0.0636 | 0.68 | 0.2181 | 0.0163 |
| 11 | 0.00413 | 2.849e-04 | 0.0689 | 0.90 | 0.2233 | 0.0201 |
| 12 | 0.00347 | 2.187e-04 | 0.0630 | 0.77 | 0.2142 | 0.0164 |

Odd shells carry more than even ones (parity of the grammar: a box costs 3, a binary connective 1); two-step ratios c(s+2)/c(s) at s = 6, 8, 10: 0.581, 0.645, 0.688, against (s/(s+2))²: 0.562, 0.640, 0.694. The tail is 1/s² with a parity oscillation, not geometric.

### Reclassification (n − 1 → n, raw masses)

| n | Δμ_est | from new shell | establisher status switches | Δμ_core | core → fakeable (old syntax, raw) | classes reclassified | Δμ_pf | from new shell | old syntax newly fakers |
|---|---|---|---|---|---|---|---|---|---|
| 7 | 9.27e-04 | 9.27e-04 | 0 | -3.38e-03 | 3.71e-03 | `BOX(THEM(THEM))`, `BOX(THEM(^BOX1(THEM(ME))))` … | 2.52e-03 | 2.40e-03 | 1.17e-04 |
| 8 | 4.93e-04 | 4.93e-04 | 0 | 1.24e-04 | 0.00e+00 |  | 3.74e-03 | 1.70e-03 | 2.04e-03 |
| 9 | 4.70e-04 | 4.70e-04 | 0 | 1.50e-04 | 0.00e+00 |  | 1.39e-03 | 1.39e-03 | 2.08e-06 |
| 10 | 3.18e-04 | 3.18e-04 | 0 | 5.70e-05 | 2.46e-05 | `BOX(THEM(^BOX(THEM(THEM))))`, `BOX(THEM(^BOX(THEM(^BOX1(THEM(ME))))))` … | 1.06e-03 | 1.06e-03 | 0.00e+00 |
| 11 | 2.85e-04 | 2.85e-04 | 0 | 8.29e-05 | 3.12e-08 | `and(BOX1(THEM(THEM)),BOX1(THEM(^BOX1(THEM(ME)))))` | 1.38e-03 | 9.21e-04 | 4.63e-04 |
| 12 | 2.19e-04 | 2.19e-04 | 0 | 5.70e-05 | 9.35e-08 | `and(BOX(THEM(THEM)),BOX(THEM(^BOX(THEM(ME)))))`, `and(BOX(THEM(THEM)),BOX1(THEM(^BOX(THEM(ME)))))` … | 7.59e-04 | 7.44e-04 | 1.48e-05 |

- Establisher status never switches (0 at every step, checked), so μ_est raw grows only by new shells, as argued. The unfakeable core loses mass to reclassification once materially (n = 7, `BOX(THEM(THEM))` and its kin, 0.0037 raw) and then by ≤ 2.5·10⁻⁵ per step.

### Establishers with raw class mass ≥ 10⁻⁴ (item 4)

ρ(x | all-D) is the same for every establisher (same 2×2 game against D): 0.0421 / 0.0214 / 0.0108 at N = 100 / 400 / 1,600.

| class | μ cut (n = 6) | μ cut (n = 9) | μ cut (n = 12) | faker mass cut (n = 6 / 9 / 12) | core (n = 6 / 9 / 12) | top fakers at n = 12 |
|---|---|---|---|---|---|---|
| `BOX1(THEM(ME))` | 0.00495 | 0.00513 | 0.00518 | 0.00000 / 0.00000 / 0.00000 | yes / yes / yes | – |
| `BOX(THEM(ME))` | 0.00495 | 0.00513 | 0.00518 | 0.00000 / 0.00000 / 0.00000 | yes / yes / yes | – |
| `BOX(THEM(THEM))` | 0.00495 | 0.00510 | 0.00514 | 0.00000 / 0.00003 / 0.00005 | yes / no / no | `BOX1(THEM(^not(BOX(THEM(^C)))))`, `BOX1(THEM(^not(BOX(THEM(ME)))))` |
| `BOX1(THEM(THEM))` | 0.00490 | 0.00510 | 0.00514 | 0.00260 / 0.00293 / 0.00312 | no / no / no | `not(BOX(THEM(ME)))`, `not(BOX(THEM(^C)))` |
| `BOX1(THEM(^C))` | 0.00138 | 0.00158 | 0.00169 | 0.00295 / 0.00356 / 0.00389 | no / no / no | `BOX(THEM(^D))`, `BOX1(THEM(^D))` |
| `BOX(THEM(^C))` | 0.00138 | 0.00158 | 0.00168 | 0.00295 / 0.00359 / 0.00392 | no / no / no | `BOX(THEM(^D))`, `BOX1(THEM(^D))` |
| `not(BOXD1(THEM(^C)))` | 0.00016 | 0.00025 | 0.00029 | 0.03716 / 0.04055 / 0.04193 | no / no / no | `BOX(THEM(^C))`, `BOX(THEM(ME))` |
| `not(BOXD(THEM(^C)))` | 0.00016 | 0.00025 | 0.00029 | 0.04211 / 0.04583 / 0.04732 | no / no / no | `BOX(THEM(^C))`, `BOX(THEM(ME))` |

These 8 classes carry 97.3% of μ_est at n = 12.

### Co-seeding conditioned on an establisher (item 5) and establishment-weighted mass (item 6)

10⁵ iid seeds of N = 100 per n from the cutoff-normalized prior. A = some establisher present; K_pf = seed members that are fakers of an establisher present in that seed (resident-specific).

| n | P(A) | E[K_pf given A] | of which establishers | P(K_pf > 0 given A) | naive N·μ_pf | Σ μρ cut, N = 100 | 400 | 1,600 |
|---|---|---|---|---|---|---|---|---|
| 6 | 0.902 | 0.320 ± 0.003 | 0.065 | 0.189 ± 0.001 | 5.26 | 0.00096 | 0.00049 | 0.00025 |
| 7 | 0.909 | 0.404 ± 0.004 | 0.097 | 0.211 ± 0.001 | 5.52 | 0.00100 | 0.00051 | 0.00026 |
| 8 | 0.915 | 0.461 ± 0.004 | 0.110 | 0.233 ± 0.001 | 5.95 | 0.00102 | 0.00052 | 0.00026 |
| 9 | 0.918 | 0.512 ± 0.004 | 0.128 | 0.246 ± 0.001 | 6.08 | 0.00104 | 0.00053 | 0.00027 |
| 10 | 0.918 | 0.558 ± 0.004 | 0.143 | 0.260 ± 0.001 | 6.18 | 0.00105 | 0.00053 | 0.00027 |
| 11 | 0.922 | 0.580 ± 0.005 | 0.148 | 0.266 ± 0.001 | 6.33 | 0.00106 | 0.00054 | 0.00027 |
| 12 | 0.923 | 0.609 ± 0.005 | 0.156 | 0.274 ± 0.001 | 6.39 | 0.00106 | 0.00054 | 0.00027 |

- Σ μρ is exactly ρ(N)·μ_est (every establisher has the same game against D), so item 6 adds only ρ(N) ∝ N^(−1/2) (ρ(400)/ρ(100) = 0.509, ρ(1600)/ρ(400) = 0.505).
- About a quarter of E[K_pf | A] is establishers faking other establishers (at n = 9, 73% of the μ×μ pair weight is the prover family (FairBot, `BOX1(THEM(ME))`, `BOX(THEM(THEM))`, `BOX1(THEM(THEM))`) exploiting `not(BOXD(THEM(^C)))` and `not(BOXD1(THEM(^C)))`, and 83% has one of those two as victim), whose takeover leaves a cooperative island.

## Part B: island merging at I = 4 (n = 6, N = 400 per island)

Fresh seeds (salt 20261005); horizon 10⁵ generations; the event kernel equals `seeds_in_n._run` draw for draw (15 of 15 checks). No run was censored or unresolved: every migration run was certified frozen, every no-migration run locally frozen.

### References (rerun)

- (i) No migration, (400, 4), 100 runs: per-island p(400) = 0.190 [0.155, 0.231] (published 0.158 [0.124, 0.198]); all four efficient in 0 of 100 runs (p⁴ = 0.0013). Independent-trials benchmark 1 − (1 − p)^4 = 0.570 [0.489, 0.651] (p's interval propagated).
- (ii) One island of N = 1,600, 240 runs: efficient 0.371 [0.312, 0.434] (published per-island 0.383 [0.336, 0.432]).

### Run-level efficient fraction

| mN | runs | efficient | fraction [95%] | per-island efficient | mean global P(C,C) | median / max stop generation |
|---|---|---|---|---|---|---|
| 0.1 | 60 | 37 | 0.617 [0.490, 0.729] | 0.617 [0.554, 0.676] | 0.617 | 690 / 2700 |
| 1 | 60 | 31 | 0.517 [0.393, 0.638] | 0.517 [0.454, 0.579] | 0.517 | 140 / 400 |
| 10 | 60 | 26 | 0.433 [0.316, 0.559] | 0.433 [0.372, 0.497] | 0.433 | 60 / 180 |

**Predeclared contrast** fraction(mN = 0.1) − fraction(mN = 10) = 0.183, 95% Newcombe interval [0.005, 0.346].

### Event logs

Windows: W1 before the first certified cooperative island, W2 from it to resolution. Migrant births by category of the migrant (per run, mean); "into coop" = target island ≥ 90% self-cooperators at the time.

| mN | window | runs | establisher | probe-faker | D | ALLC | other self-coop | other | introductions (new class on target) | of which establishers into non-coop islands | probe-fakers into coop islands |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.1 | W1 | 60 | 3.1 | 0.1 | 24.1 | 0.7 | 0.0 | 0.1 | 3.5 | 2.65 | 0.00 |
| 0.1 | W2 | 60 | 148.3 | 0.0 | 124.1 | 0.0 | 0.0 | 0.0 | 122.2 | 54.50 | 0.00 |
| 1 | W1 | 60 | 58.2 | 1.5 | 279.6 | 6.9 | 0.0 | 0.5 | 24.7 | 17.18 | 0.05 |
| 1 | W2 | 60 | 164.2 | 0.2 | 55.9 | 0.0 | 0.0 | 0.0 | 23.4 | 4.25 | 0.05 |
| 10 | W1 | 60 | 668.3 | 12.2 | 2206.2 | 78.5 | 1.0 | 4.9 | 31.2 | 18.77 | 0.00 |
| 10 | W2 | 60 | 212.8 | 0.0 | 0.3 | 0.0 | 0.0 | 0.0 | 0.5 | 0.00 | 0.00 |

| mN | first certified island, median gen | first certification within 20 gens of resolution / no certified island | islands reaching ≥ 90% coop per run: local / imported | efficient runs with ≥ 2 local nucleations | defecting runs that had a ≥ 90% coop island | losses (mechanism) | founders (efficient runs) | seeded establishers per run, efficient / defecting |
|---|---|---|---|---|---|---|---|---|
| 0.1 | 80 | 0 / 23 of 60 | 2.22 / 0.25 | 36 of 37 | 0 | 0 (–) | `BOX(THEM(THEM))` 14, `BOX(THEM(ME))` 11, `BOX1(THEM(THEM))` 5, `BOX1(THEM(^C))` 3 | 38.4 / 36.2 |
| 1 | 100 | 0 / 29 of 60 | 1.75 / 0.32 | 30 of 31 | 0 | 0 (–) | `BOX1(THEM(THEM))` 9, `BOX(THEM(THEM))` 7, `BOX1(THEM(ME))` 6, `BOX(THEM(ME))` 5 | 36.6 / 34.6 |
| 10 | 100 | 25 / 34 of 60 | 1.43 / 0.30 | 24 of 26 | 0 | 0 (–) | `BOX(THEM(ME))` 8, `BOX1(THEM(ME))` 7, `BOX(THEM(^C))` 5, `BOX(THEM(THEM))` 5 | 38.7 / 37.3 |

"Local" means the largest cooperative class at the island's first ≥ 90% check was in its own seed; with about 9 establishers seeded per island this label is weak, so nucleation is also identified by timing. Without migration every island that went ≥ 90% cooperative did so by generation 140 (median 60, 76 islands), so an island going ≥ 90% by generation 200 is counted as nucleated, a later one as reached by spread.

| mN | efficient runs | islands ≥ 90% coop by gen 200, per efficient run (1 / 2 / 3 / 4) | independent-trials expectation given ≥ 1 (1 / 2 / 3 / 4) | first → last island ≥ 90%, median gens | median resolution gen |
|---|---|---|---|---|---|
| 0.1 | 37 | 20 / 14 / 3 / 0 | 26.2 / 9.2 / 1.4 / 0.1 | 940 | 1020 |
| 1 | 31 | 1 / 6 / 7 / 17 | 22.0 / 7.7 / 1.2 / 0.1 | 120 | 220 |
| 10 | 26 | 0 / 0 / 0 / 26 | 18.4 / 6.5 / 1.0 / 0.1 | 20 | 120 |

Terminal support (efficient runs, most common sets):

- mN = 0.1: {`BOX(THEM(THEM))`} ×12; {`BOX(THEM(ME))`} ×9; {`BOX1(THEM(THEM))`} ×5; {`BOX(THEM(ME))`, `BOX(THEM(THEM))`} ×4; defecting: {`D`} ×19; {`D`, `not(BOXD1(THEM(ME)))`} ×1
- mN = 1: {`BOX1(THEM(ME))`} ×6; {`BOX1(THEM(THEM))`} ×5; {`BOX(THEM(ME))`} ×4; {`BOX(THEM(THEM))`} ×4; defecting: {`D`} ×24; {`BOX(THEM(^D))`, `D`} ×2
- mN = 10: {`BOX(THEM(ME))`} ×6; {`BOX(THEM(THEM))`, `BOX1(THEM(ME))`} ×4; {`BOX1(THEM(ME))`} ×3; {`BOX(THEM(^C))`} ×3; defecting: {`D`} ×29; {`D`, `not(BOXD(THEM(ME)))`} ×2

## Verdicts (rules predeclared in `predictions/2026-10-05-seeds-tail.md`)

| # | prediction | outcome |
|---|---|---|
| 1 | μ_est(n) converges below 0.03 with a 1/s² tail; μ_est(12) ∈ [0.024, 0.028]; shell fraction 0.03–0.06, within ±50% of s = 6 at every s ≤ 12 | **Held in substance; one clause failed narrowly; the limit is inconclusive.** μ_est(12) = 0.0253 (cut) is in range. The tail is 1/s²: two-step ratios are 0.58 / 0.65 / 0.69 against (s/(s+2))² = 0.56 / 0.64 / 0.69, with an odd–even oscillation. f(s) is within ±50% of f(6) = 0.061 at s = 6–12 (largest f(7) = 0.091, limit 0.092). The 0.03–0.06 band failed narrowly: f = 0.061–0.091, all above it. Falsifier not fired on s = 6–12; on a literal reading it fires at s = 3 (0.22), s = 5 (0.12) and s ≤ 2 (0). Limit below 0.03: **inconclusive (consistent)**. The extrapolation gives 0.027 (inf units), but the rigorous bound is 0.073. |
| 2 | μ_pf(12) ≤ 0.006, r ≤ 0.25; E[K_pf given A] < 0.5 and P(K_pf > 0 given A) < 0.35 for n ≤ 12 | **Failed, falsifier fired.** The global union μ_pf is 0.053 → 0.064 (cut) and r = 2.3 → 2.5, so r(12) > 0.4. E[K_pf given A] crosses 0.5 at n = 9 (0.61 at n = 12). P(K_pf > 0 given A) = 0.19 → 0.27 **held**. The union is the wrong quantity: it is dominated by the fakers of two rare establishers that are suckers of almost everything. The μ-weighted faker exposure is 0.0015 → 0.0026, and its increments fall like the 1/s² tail. |
| 3 | FairBot and `BOX1(THEM(ME))` unfakeable at every n ≤ 12 | **Held** (no strict invader at any n = 6–12). |
| 4 | I = 4 fractions 0.50 ± 0.15 / 0.42 ± 0.12 / 0.38 ± 0.12 at mN = 0.1 / 1 / 10; contrast positive with a 95% interval excluding 0 | **Contrast held:** 0.183 [0.005, 0.346], narrowly. **Bands inconclusive:** every point estimate is inside its band (0.617 / 0.517 / 0.433), but every Wilson interval straddles the upper edge. No intermediate maximum: the decline is monotone. Mechanism: merging during nucleation, not spoiler import (0 losses in 180 runs). |
| S1 | global faker union in [0.006, 0.02], r(12) in [0.2, 0.6] | **Failed** (0.064, r = 2.53). The direction was right and the size about 3× too small. |
| S2 | P(K_pf > 0 given A) in [0.15, 0.45] at every n, rising < 0.1 from n = 6 to 12 | **Held** (0.189 → 0.274, +0.085) |
| S3 | Σ μρ = ρ(N)·μ_est; ρ(400)/ρ(100) in 0.45–0.55 | **Held** (exact; 0.509) |
| S4 | mN = 0.1 in [0.38, 0.6], mN = 10 in [0.28, 0.48]; contrast interval includes 0; at mN = 10 first certification at resolution; at mN = 0.1 ≥ half of efficient runs with ≥ 2 local nucleations | **Mixed.** mN = 10 held. mN = 0.1 failed narrowly (0.617). The contrast interval excludes 0, so the "includes 0" claim **failed**. First certification at resolution: 25 of 26 efficient runs, **held**. Local nucleation: on the predeclared seed label 36 of 37, **held**, but that label is uninformative. By timing, 17 of 37 runs have ≥ 2 islands nucleated by generation 200, **failed** narrowly. |
| S5 | references reproduce | **Held:** p(400) = 0.190 [0.155, 0.231] against 0.158; one island of 1,600 gives 0.371 [0.312, 0.434] against 0.383. |
