# The demographic lemma, the factorized spoiler bound, and the establishment formula (2026-10-05)

Spec `specs/2026-10-05-demographic-lemma.md` (reviewed by gpt-6.1-sol); predictions
`predictions/2026-10-05-demographic-lemma.md` (committed before any counted run, with two addenda); proofs
`notes/demographic-lemma.md`; code `src/demographic_lemma.py` (`static`, `test`, `dsea`, `forced`, `lottery`, `report`).
Aggregates in `runs/demographic-lemma.json`; raw rows: `runs/demographic-lemma-dsea.json`,
`runs/demographic-lemma-lottery.json.gz` (committed) and `runs/demographic-lemma-forced.npz` (270,000 rows, 38 MB,
gitignored by `runs/*.npz`; regenerate with `python3 src/demographic_lemma.py forced`, ≈ 11 minutes on 3 workers).

## What was run

- **Kernel.** `_dl_run` is the seeds_in_n kernel (birth–death Moran, parent ∝ e^{wπ}, victim uniform, I = 1, no
  migration) with instrumentation that draws no random numbers from the event stream: it reproduces
  `seeds_in_n._run` draw for draw (12/12 islands, `test`). Additions: a ghost class (fitness pinned to the mean), tagged
  duplicate classes for founders (class-level law unchanged), and per tracked lineage the Lemma D′ functional
  Φ = 1 + ∫ d e^{−R} on the event clock and on an independent Poisson clock, R, Λ, hitting times and fixed-time sizes.
- **D sea** (Task 3b): 10⁴ runs per (N, k) at N = 100, 400, 1,600 and 4,000 at 6,400; k = 1, 2, 4, 8, 16.
- **Forced** (Tasks 1–2): 10,000 backgrounds per (N, n, faker type), N = 100 / 400 / 1,600, n = 6 / 9 / 12 (the
  scramble-lemma pairs; the spec's 3,000 are the first block), each run twice with common random numbers (faker run to
  local freeze; ghost run to max(τ, 40 generations)). 270,000 backgrounds; 269,918 in E.
- **Lottery** (Task 3c–e): n = 9, iid seeds, every establisher founder tagged; 4,000 islands at N = 100, 400, 1,600,
  1,000 at 6,400, 400 at 25,600 (exploratory, declared before the run).
- **Stopping reasons.** Forced faker runs: τ by ALLC extinction in 99.1% (N = 100), 99.7% (400), 99.96% (1,600), the
  rest local freeze with ALLC present; no τ hit the 2,000-generation cap; final stop by local freeze in 269,986 runs and
  the 10⁵ horizon in 14 (5 at N = 400, 9 at 1,600; their outcome is read from the final state). Ghost runs end at 40
  generations (18,013) or when both tracked lineages are extinct after τ (251,987). Lottery: τ by ALLC extinction in
  3,984 / 3,990 / 3,997 / 1,000 / 400 islands at N = 100 / 400 / 1,600 / 6,400 / 25,600, local freeze otherwise, no
  cap; final stop by local freeze in every island but one (N = 1,600, rep 1,281: a stable anti-coordination mixture of
  `not(BOXD(THEM(ME)))` and `BOX1(THEM(^BOXD1(THEM(THEM))))`, each defecting on its own class and cooperating with the
  other, P(C,C) = 0.50; a rest point, not a cycle; counted as not cooperative). D sea: every run fixed or went extinct.

## Declared deviations

1. **Lemma D′ evaluation, corrected after the first report.** The first report used only the binned form
   Σ_i min{P(Φ ∈ bin_i), 1/φ_i}, which is valid but sums one cap per bin and came out vacuous (0.4–1.0, 12–50× the
   measured founder survival). The single-level form inf_φ [1/φ + P(Φ_τ < φ)] is Lemma D′ itself; the reported bound is
   the smaller of the two. Every Lemma D′ number below (and the combined bound and the extrapolation built on it) uses
   the corrected evaluation. Verdicts that depend on it (RE 2's positivity, S8, S9) are scored on the corrected numbers;
   with the binned-only form, 5 of the RE's 18 cells would have been non-positive.
2. **Kernel bug fix before the forced run** (commit c03a2f6): the first forced launch crashed on a division by zero when
   a neutral ghost took the whole island (N = 100), and hitting times after τ were not recorded in ghost runs. No rows
   were written by the crashed launch; the D-sea and lottery runs do not use either code path.
3. **p_corr2** (the establishment formula with the scramble's mean-field path computed from the full seed rather than
   from {ALLC, D} alone) was added after seeing that p_corr under-predicts. It is post hoc and has no fitted parameter.
4. The ghost check is pooled over the 7 pairs and 3 cutoffs (90,000 backgrounds per N) rather than "3,000 per pair".

## Headline numbers

- **Lemma D′ (proved, notes §1.1):** for any lineage and any stopping time, P(alive at τ, Φ_τ ≥ φ) ≤ 1 − (1 − 1/φ)^{k₀},
  Φ = 1 + ∫ d e^{−R}. It needs no sign condition on the lineage's fitness and dominates B1. **Lemma D** (fixed time,
  killed at K): ≤ k₀/(1 + d_min T), d_min = 1 − (K − 1)/N; the event-clock transfer costs ≤ 10%. The ghost check:
  the killed ghost never exceeds the bound in 24 of 24 (N, t, K) cells; the unkilled ghost / (1/(1 + t)) is
  1.005–1.036 at N = 400 and 1,600, and 1.015–1.173 at N = 100 (the clock slows as d = 1 − k/N).
- **Per-founder dependence r_q:** pooled over n, 1.15 / 1.39 / 1.66 (D-cooperating fakers), 1.09 / 0.93 / 0.94
  (probe-fakers), 0.80 / 0.85 / 1.13 (establisher-faker) at N = 100 / 400 / 1,600. The shared scramble duration
  explains little of it (r_env 1.01–1.16). r ≤ 1/P(A) always, so the 1/P(A) ≈ 7–20 loss of the scramble lemma is gone.
- **Combined bound** (confidence-qualified empirical): positive in 27 of 27 cells, point and conservative (it was
  non-positive in 16 of 18 with B1's q̄). The extrapolated spoiler sum for the probe-readers is 0.04 / 0.08 / 0.14 at
  N = 100 / 400 / 1,600 (0.02 / 0.05 / 0.09 with the measured q̄), growing ≈ N^0.45, 0.34 at N = 10⁴ (extrapolated);
  0 for FairBot's pair.
- **Escape from a D sea:** exact birth–death formula inside the 95% interval in 20 of 20 (N, k) cells; pooled u_k is
  nearly linear in k (u₁₆ = 0.61 at N = 100 against 0.50 for independent copies).
- **E[k_τ]/k₀ for ALLC-cooperating establishers is 1.26–1.55 at every N, not 0.93**: the family's own advantage
  (π_E − π̄ = x_D x_E) beats the fitness curvature, and at small N a survivor's own frequency adds more.
- **p(N):** 0.087 / 0.195 / 0.383 / 0.686 / 0.980 at N = 100 / 400 / 1,600 / 6,400 / 25,600 (n = 9, I = 1). The
  post-scramble state mapped through the pooled two-type escape predicts it within 0–4% at every N. The closed form
  with the curvature-only scramble under-predicts by 1.21–1.27; with the full-seed mean field (post hoc, no fitted
  parameter) by 1.17 / 1.16 / 1.07 / 1.01 / 1.02. Saturation follows the pooled-family form (0.719 / 0.969 at 6,400 /
  25,600), not the independent-founder form (0.577 / 0.821). Exponent over 100–1,600: 0.533 [0.495, 0.571].

## Verdicts

| # | prediction | outcome |
|---|---|---|
| RE 1 | Lemma D with d_min ≥ 0.9 below N/20; ghost within 1.3 of 1/(1 + t) at N = 400, 1,600 | **Held** (d_min ≥ 0.95 proved; 0/24 bound exceedances; ratios 1.005–1.036) |
| RE 2 | r_q ∈ [0.8, 1.6] everywhere, larger for ALLC-cooperating fakers; bound positive in 18/18; positive extrapolation to 10⁴ | **Failed, falsifier fired narrowly**: r = 2.01 [1.22, 2.74] at (1,600, D-cooperating, n = 9) with 11 joint events; 5 of 27 cells outside [0.8, 1.6]; the ordering is reversed (D-cooperating fakers have the larger r). Positivity **held** (18/18, and 27/27, point and conservative); extrapolated sums ≤ 0.34 at 10⁴; FairBot's pair 0 |
| RE 3 | corrected formula within 1.25; naive over by 10–40%; exponent 0.45–0.65; u₁ within 1.2; exact agrees | **Held** on the spec's (d) predictor (ratios 1.017 / 0.999 / 1.036; naive over by 23% / 11%; exponent 0.533; u₁ ratio 0.87–0.99; 20/20). The closed form p_corr would have missed the 1.25 band at N = 100 and 400 (1.26, 1.27), inside the falsifier |
| RE 4 | E[k_τ] per copy 0.75–0.95 (ALLC-cooperating), > 1.2 (ALLC-exploiting) | **Failed, falsifier fired** at every N: 1.41 / 1.55 / 1.36 / 1.26 / 1.32 (lottery), 1.36 / 1.45 / 1.17 (forced targets). ALLC-exploiting founders are too rare to test (5–114 per N, intervals spanning 0) |
| RE 5 | (6,400, 1) follows the independent-founder form (≈ 0.56) | **Failed, falsifier fired**: 0.686 [0.657, 0.714] on 1,000 islands (the spec's 200: 0.660 [0.592, 0.722], at the boundary); 25,600: 0.980 against 0.82 (independent) and 0.97 (pooled) |
| S1 | ghost at N = 100 above 1/(1+t) by > 15% at t = 40; N = 1,600 within [0.9, 1.1] | **Held** (1.173 [1.129, 1.219]; 1.005–1.032) |
| S2 | E[k_τ]/k₀ > 1.05 at N = 100, decreasing in N, in [0.88, 1.08] at 1,600 | **Failed** (first clause held; 1.41 → 1.55 → 1.36 is not decreasing; 1.36 / 1.17 at 1,600) |
| S3 | D-sea simulation matches the exact formula; u₁₆ above the independent-copies form | **Held** (20/20; u₁₆ above at every N ≤ 1,600) |
| S4 | pooled r ∈ [0.9, 1.6]; r_env ≥ 1 and explains ≥ half of r − 1 | **Failed** (0.80 at (100, establisher-faker), 1.66 at (1,600, D-cooperating); r_env ≥ 1 everywhere but 1.07 against r = 1.39 at (400, D-cooperating)) |
| S5 | semi-empirical predictor within [0.85, 1.15] | **Held** (0.999–1.036) |
| S6 | closed-form p_corr under-predicts by 1.1–1.45 | **Held** (1.257 / 1.267 / 1.212) |
| S7 | (6,400, 1) ≥ 0.66 and within 0.1 of the semi-empirical value | **Held** (0.686; 0.674) |
| S8 | Lemma D′ within 2× of measured faker-founder survival in every (N, type) | **Failed** (2.06–3.25 at N = 100; 4.45 and 7.87 for D-cooperators at 400 and 1,600; 1.5–1.9 for the others at N ≥ 400) |
| S9 | bound positive in all 27 cells; h^rel(1,600) < 0.15 for probe-reader pairs | **Failed on h** (positivity held; h^rel = 0.40) |
| S10 | (25,600, 1) above 0.85 | **Held** (0.980 [0.961, 0.990]) |

## Reading

- **Demography and selection are one martingale.** Lemma D′ bounds a lineage's survival at any stopping time by
  1/φ + P(Φ_τ < φ), with Φ = 1 + ∫ d e^{−R}. For a neutral lineage Φ = 1 + t, which is the critical-branching law; for a
  disadvantaged one e^{−R} grows inside the integral. B1 was the special case that dropped the "1 + ∫ d" part, which is
  why it was vacuous for probe-fakers. On data it is within 1.5–2× for near-neutral founders at N ≥ 400; what it loses
  is the spread of the scramble duration, which a single φ cannot track.
- **The 1/P(A) loss was an artefact of the union step.** Charging each faker founder its survival *given the target
  survives* costs a factor r_q = 0.8–1.7, not 1/P(A) = 7–20, and the per-island bound becomes positive in every cell.
  The association is not mainly the shared scramble length; a direct-interaction term (the faker earns T against a
  surviving target) is the likely remainder, strongest for D-cooperating fakers.
- **Probe-readers' spoiler term still grows** (≈ N^0.45 in the bound), so the clean statement stays on FairBot's pair;
  the fakeable provers are a bonus whose bound would reach 1 only far beyond N = 10⁴ on this extrapolation.
- **The establishment chance has a formula, and it saturates.** Each establisher founder survives the scramble like a
  near-critical branching lineage (≈ 1/(1 + τ), size ≈ 1 + τ given survival); the survivors pool into one family; the
  family escapes the D sea by the exact two-type birth–death formula. The post-scramble part is exact to within 4% and
  calibrated; the scramble part is a Kendall approximation whose mean is set by a mean-field family advantage the spec
  had left out. **At fixed cutoff the per-island chance tends to 1** (0.98 at N = 25,600), following the pooled-family
  form erf(μ_est ℓ √(Nc/2)), so the N ≫ I path is "almost all seeds" for a single island.
- **sol was right about saturation.** Independent-founder escape under-predicts by 11–13% at large N; pooling after the
  scramble is the mechanism. The RE's argument that founders must each survive the scramble is true, but the survivors
  then pool, and E[k_τ] > 1 offsets the scramble loss.

# Tables (generated by `python3 src/demographic_lemma.py report`)

## Task 3(a)-(b): escape from a D sea (u_k)

Seeds_in_n kernel on {prover k, D N − k}, run to local freeze (no unresolved run). Exact = birth–death formula;
diffusion = erf form; independent copies = 1 − (1 − u₁)^k.

| N | k | runs | measured u_k [95%] | exact | diffusion | 1 − (1 − u₁)^k | k·u₁ | exact in interval | median fixation gen |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 1 | 10000 | 0.0402 [0.0365, 0.0442] | 0.0421 | 0.0437 | 0.0421 | 0.0421 | yes | 40 |
| 100 | 2 | 10000 | 0.0831 [0.0778, 0.0887] | 0.0841 | 0.0872 | 0.0823 | 0.0841 | yes | 40 |
| 100 | 4 | 10000 | 0.1682 [0.1610, 0.1757] | 0.1677 | 0.1734 | 0.1579 | 0.1682 | yes | 40 |
| 100 | 8 | 10000 | 0.3271 [0.3180, 0.3364] | 0.3295 | 0.3387 | 0.2909 | 0.3365 | yes | 40 |
| 100 | 16 | 10000 | 0.6120 [0.6024, 0.6215] | 0.6083 | 0.6192 | 0.4972 | 0.6729 | yes | 40 |
| 400 | 1 | 10000 | 0.0216 [0.0189, 0.0246] | 0.0214 | 0.0218 | 0.0214 | 0.0214 | yes | 80 |
| 400 | 2 | 10000 | 0.0429 [0.0391, 0.0471] | 0.0428 | 0.0437 | 0.0424 | 0.0428 | yes | 80 |
| 400 | 4 | 10000 | 0.0893 [0.0839, 0.0950] | 0.0856 | 0.0872 | 0.0829 | 0.0856 | yes | 80 |
| 400 | 8 | 10000 | 0.1664 [0.1592, 0.1738] | 0.1704 | 0.1734 | 0.1590 | 0.1713 | yes | 80 |
| 400 | 16 | 10000 | 0.3251 [0.3160, 0.3343] | 0.3337 | 0.3387 | 0.2927 | 0.3425 | yes | 80 |
| 1600 | 1 | 10000 | 0.0101 [0.0083, 0.0123] | 0.0108 | 0.0109 | 0.0108 | 0.0108 | yes | 140 |
| 1600 | 2 | 10000 | 0.0220 [0.0193, 0.0251] | 0.0216 | 0.0218 | 0.0215 | 0.0216 | yes | 140 |
| 1600 | 4 | 10000 | 0.0433 [0.0395, 0.0475] | 0.0432 | 0.0437 | 0.0425 | 0.0432 | yes | 140 |
| 1600 | 8 | 10000 | 0.0891 [0.0837, 0.0948] | 0.0864 | 0.0872 | 0.0833 | 0.0865 | yes | 140 |
| 1600 | 16 | 10000 | 0.1713 [0.1640, 0.1788] | 0.1718 | 0.1734 | 0.1596 | 0.1730 | yes | 140 |
| 6400 | 1 | 4000 | 0.0047 [0.0030, 0.0074] | 0.0054 | 0.0055 | 0.0054 | 0.0054 | yes | 220 |
| 6400 | 2 | 4000 | 0.0110 [0.0082, 0.0147] | 0.0109 | 0.0109 | 0.0108 | 0.0109 | yes | 260 |
| 6400 | 4 | 4000 | 0.0180 [0.0143, 0.0226] | 0.0217 | 0.0218 | 0.0216 | 0.0217 | yes | 260 |
| 6400 | 8 | 4000 | 0.0480 [0.0418, 0.0551] | 0.0435 | 0.0437 | 0.0426 | 0.0435 | yes | 240 |
| 6400 | 16 | 4000 | 0.0930 [0.0844, 0.1024] | 0.0868 | 0.0872 | 0.0835 | 0.0869 | yes | 240 |

Exact value inside the 95% interval in 20 of 20 cells. u₁ measured/diffusion: 0.920 (N = 100), 0.989 (N = 400), 0.924 (N = 1600), 0.870 (N = 6400).

## Task 1: Lemma D against the ghost (fitness pinned to the mean), fixed time and stopped

Ghost runs: the faker founder of every forced background replaced by a ghost (plays as the faker, fitness =
population mean, so r ≡ 0 and d = 1 − k/N exactly), common random numbers with the faker run, all 7 pairs and
3 cutoffs pooled (the ghost's survival does not depend on its payoffs except through others), in E.
Bound = event-clock Lemma D (notes §1.4) for the process killed at K; "killed alive" = alive at t and K not hit by t.

| N | t | backgrounds | alive (unkilled) | ratio to 1/(1+t) | killed at N/20: alive | bound | killed at N/4: alive | bound | P(hit N/4 by t) | k₀/K (N/4) |
|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 5 | 89918 | 0.1692 [0.1667, 0.1716] | 1.015 [1.000, 1.030] | 0.0234 | 0.1896 | 0.1661 | 0.2282 | 0.0031 | 0.0400 |
| 100 | 10 | 89918 | 0.0945 [0.0926, 0.0964] | 1.039 [1.019, 1.061] | 0.0006 | 0.1019 | 0.0770 | 0.1253 | 0.0175 | 0.0400 |
| 100 | 20 | 89918 | 0.0511 [0.0497, 0.0526] | 1.073 [1.043, 1.104] | 0.0000 | 0.0525 | 0.0199 | 0.0655 | 0.0339 | 0.0400 |
| 100 | 40 | 89918 | 0.0286 [0.0275, 0.0297] | 1.173 [1.129, 1.219] | 0.0000 | 0.0265 | 0.0014 | 0.0333 | 0.0399 | 0.0400 |
| 400 | 5 | 90000 | 0.1688 [0.1663, 0.1712] | 1.013 [0.998, 1.027] | 0.1588 | 0.1829 | 0.1688 | 0.2208 | 0.0000 | 0.0100 |
| 400 | 10 | 90000 | 0.0940 [0.0921, 0.0959] | 1.034 [1.013, 1.055] | 0.0624 | 0.0991 | 0.0940 | 0.1222 | 0.0000 | 0.0100 |
| 400 | 20 | 90000 | 0.0493 [0.0479, 0.0508] | 1.036 [1.007, 1.066] | 0.0105 | 0.0515 | 0.0489 | 0.0643 | 0.0005 | 0.0100 |
| 400 | 40 | 90000 | 0.0252 [0.0242, 0.0262] | 1.033 [0.992, 1.076] | 0.0002 | 0.0262 | 0.0214 | 0.0329 | 0.0038 | 0.0100 |
| 1600 | 5 | 90000 | 0.1675 [0.1651, 0.1700] | 1.005 [0.990, 1.020] | 0.1675 | 0.1788 | 0.1675 | 0.2162 | 0.0000 | 0.0025 |
| 1600 | 10 | 90000 | 0.0924 [0.0905, 0.0943] | 1.016 [0.996, 1.037] | 0.0923 | 0.0974 | 0.0924 | 0.1202 | 0.0000 | 0.0025 |
| 1600 | 20 | 90000 | 0.0487 [0.0473, 0.0501] | 1.023 [0.994, 1.053] | 0.0467 | 0.0508 | 0.0487 | 0.0635 | 0.0000 | 0.0025 |
| 1600 | 40 | 90000 | 0.0252 [0.0242, 0.0262] | 1.032 [0.991, 1.075] | 0.0173 | 0.0260 | 0.0251 | 0.0326 | 0.0000 | 0.0025 |

**Stopped version** (ghost alive at its own run's τ = ALLC extinction ∧ freeze ∧ 2,000 generations), by stopping
reason; Lemma D′ bound from the measured Φ_τ (Poisson clock, binned); lower-tail decomposition
inf_t₁ [Lemma D(t₁, K = N/4) + P(hit N/4 by t₁) + P(τ < t₁)] with the measured lower tail of τ.

| N | reason | islands | ghost alive at τ | median τ | E[1/(1+τ)] | Lemma D′ bound | lower-tail bound |
|---|---|---|---|---|---|---|---|
| 100 | all | 89918 | 0.0747 [0.0730, 0.0764] | 13.6 | 0.0723 | 0.1596 | 0.2334 |
| 100 | ALLC extinct | 89200 | 0.0750 [0.0733, 0.0767] | 13.5 | 0.0727 | 0.1598 | 0.2336 |
| 100 | frozen | 718 | 0.0404 [0.0283, 0.0574] | 40.0 | 0.0270 | 0.0610 | 0.1017 |
| 100 | cap | 0 | – | – | – | – | – |
| 400 | all | 90000 | 0.0521 [0.0507, 0.0536] | 19.1 | 0.0506 | 0.0944 | 0.1284 |
| 400 | ALLC extinct | 89739 | 0.0522 [0.0508, 0.0537] | 19.0 | 0.0507 | 0.0944 | 0.1284 |
| 400 | frozen | 261 | 0.0153 [0.0060, 0.0387] | 60.0 | 0.0176 | 0.0256 | 0.0425 |
| 400 | cap | 0 | – | – | – | – | – |
| 1600 | all | 90000 | 0.0393 [0.0381, 0.0406] | 24.6 | 0.0391 | 0.0636 | 0.0840 |
| 1600 | ALLC extinct | 89969 | 0.0393 [0.0381, 0.0406] | 24.6 | 0.0392 | 0.0636 | 0.0840 |
| 1600 | frozen | 31 | 0.0000 [0.0000, 0.1103] | 80.0 | 0.0139 | 0.0167 | 0.0351 |
| 1600 | cap | 0 | – | – | – | – | – |

## Task 2: per-founder dependence r_q, Lemma D′ on faker founders, and the combined bound

Forced backgrounds (one tagged target founder, one tagged faker founder; scramble-lemma pairs), in E.
A = target class alive at τ; F_j = the tagged faker founder alive at τ; r = P(F_j | A)/P(F_j) (bootstrap 95%);
r_env = the τ-binned shared-background value; Lemma D′ = binned bound on P(F_j) from the measured Φ_τ (Poisson
clock); B1 = the exponential-martingale bound of the scramble lemma, for comparison; ghost = P(ghost alive at τ).

| N | type | n | bgs | stop 1/2/3 | P(A) | P(F_j) | joint events | r [95%] | r_env | Lemma D′ (×) | B1 | ghost |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | disadvantaged | 6 | 9990 | 9920/70/0 | 0.107 | 0.0343 | 39 | 1.07 [0.79, 1.39] | 1.141 | 0.1186 (3.45×) | 0.403 | 0.0813 |
| 100 | disadvantaged | 9 | 9991 | 9925/66/0 | 0.108 | 0.0391 | 48 | 1.13 [0.85, 1.44] | 1.174 | 0.1179 (3.01×) | 0.407 | 0.0846 |
| 100 | disadvantaged | 12 | 9989 | 9902/87/0 | 0.107 | 0.0364 | 48 | 1.24 [0.94, 1.55] | 1.154 | 0.1208 (3.32×) | 0.412 | 0.0804 |
| 100 | disadvantaged | pooled | 29970 | 29747/223/0 | 0.107 | 0.0366 | 135 | 1.15 [0.98, 1.33] | 1.159 | 0.1192 (3.25×) | 0.407 | 0.0821 |
| 100 | neutral | 6 | 9994 | 9920/74/0 | 0.080 | 0.0647 | 61 | 1.18 [0.95, 1.45] | 1.069 | 0.1539 (2.38×) | 1.000 | 0.0673 |
| 100 | neutral | 9 | 9995 | 9883/112/0 | 0.077 | 0.0706 | 52 | 0.96 [0.73, 1.21] | 1.061 | 0.1547 (2.19×) | 1.000 | 0.0740 |
| 100 | neutral | 12 | 9985 | 9900/85/0 | 0.081 | 0.0708 | 66 | 1.15 [0.90, 1.40] | 1.083 | 0.1541 (2.18×) | 1.000 | 0.0746 |
| 100 | neutral | pooled | 29974 | 29703/271/0 | 0.079 | 0.0687 | 179 | 1.09 [0.94, 1.24] | 1.070 | 0.1542 (2.24×) | 1.000 | 0.0720 |
| 100 | advantaged | 6 | 9994 | 9898/96/0 | 0.069 | 0.0778 | 51 | 0.95 [0.72, 1.18] | 1.057 | 0.1596 (2.05×) | 1.000 | 0.0697 |
| 100 | advantaged | 9 | 9985 | 9901/84/0 | 0.062 | 0.0800 | 40 | 0.80 [0.59, 1.06] | 1.070 | 0.1584 (1.98×) | 1.000 | 0.0732 |
| 100 | advantaged | 12 | 9995 | 9895/100/0 | 0.066 | 0.0738 | 31 | 0.64 [0.43, 0.85] | 1.045 | 0.1584 (2.15×) | 1.000 | 0.0671 |
| 100 | advantaged | pooled | 29974 | 29694/280/0 | 0.066 | 0.0772 | 122 | 0.80 [0.67, 0.94] | 1.055 | 0.1589 (2.06×) | 1.000 | 0.0700 |
| 400 | disadvantaged | 6 | 10000 | 9974/26/0 | 0.143 | 0.0084 | 16 | 1.33 [0.76, 1.93] | 1.083 | 0.0441 (5.25×) | 0.154 | 0.0539 |
| 400 | disadvantaged | 9 | 10000 | 9973/27/0 | 0.142 | 0.0112 | 19 | 1.19 [0.73, 1.67] | 1.049 | 0.0446 (3.98×) | 0.155 | 0.0561 |
| 400 | disadvantaged | 12 | 10000 | 9958/42/0 | 0.152 | 0.0101 | 25 | 1.62 [1.06, 2.24] | 1.086 | 0.0437 (4.32×) | 0.155 | 0.0572 |
| 400 | disadvantaged | pooled | 30000 | 29905/95/0 | 0.146 | 0.0099 | 60 | 1.39 [1.08, 1.71] | 1.073 | 0.0441 (4.45×) | 0.155 | 0.0557 |
| 400 | neutral | 6 | 10000 | 9970/30/0 | 0.078 | 0.0473 | 38 | 1.03 [0.75, 1.34] | 1.024 | 0.0893 (1.89×) | 0.999 | 0.0509 |
| 400 | neutral | 9 | 10000 | 9975/25/0 | 0.079 | 0.0484 | 35 | 0.91 [0.63, 1.22] | 1.005 | 0.0896 (1.85×) | 1.000 | 0.0506 |
| 400 | neutral | 12 | 10000 | 9964/36/0 | 0.080 | 0.0464 | 32 | 0.86 [0.59, 1.16] | 1.020 | 0.0885 (1.91×) | 0.999 | 0.0507 |
| 400 | neutral | pooled | 30000 | 29909/91/0 | 0.079 | 0.0474 | 105 | 0.93 [0.77, 1.09] | 1.014 | 0.0892 (1.88×) | 0.999 | 0.0507 |
| 400 | advantaged | 6 | 10000 | 9969/31/0 | 0.046 | 0.0494 | 19 | 0.83 [0.49, 1.22] | 1.000 | 0.0916 (1.85×) | 1.000 | 0.0476 |
| 400 | advantaged | 9 | 10000 | 9971/29/0 | 0.049 | 0.0545 | 20 | 0.75 [0.45, 1.07] | 1.019 | 0.0922 (1.69×) | 1.000 | 0.0522 |
| 400 | advantaged | 12 | 10000 | 9974/26/0 | 0.054 | 0.0524 | 27 | 0.96 [0.62, 1.33] | 1.021 | 0.0927 (1.77×) | 1.000 | 0.0499 |
| 400 | advantaged | pooled | 30000 | 29914/86/0 | 0.050 | 0.0521 | 66 | 0.85 [0.65, 1.05] | 1.015 | 0.0922 (1.77×) | 1.000 | 0.0499 |
| 1600 | disadvantaged | 6 | 10000 | 9997/3/0 | 0.291 | 0.0023 | 9 | 1.34 [0.65, 2.10] | 1.080 | 0.0151 (6.55×) | 0.052 | 0.0407 |
| 1600 | disadvantaged | 9 | 10000 | 9993/7/0 | 0.304 | 0.0018 | 11 | 2.01 [1.22, 2.74] | 1.070 | 0.0157 (8.72×) | 0.052 | 0.0385 |
| 1600 | disadvantaged | 12 | 10000 | 9997/3/0 | 0.310 | 0.0017 | 9 | 1.71 [0.95, 2.44] | 1.080 | 0.0147 (8.62×) | 0.052 | 0.0394 |
| 1600 | disadvantaged | pooled | 30000 | 29987/13/0 | 0.302 | 0.0019 | 29 | 1.66 [1.21, 2.07] | 1.070 | 0.0152 (7.87×) | 0.052 | 0.0395 |
| 1600 | neutral | 6 | 10000 | 9999/1/0 | 0.118 | 0.0380 | 47 | 1.04 [0.76, 1.34] | 1.014 | 0.0588 (1.55×) | 1.000 | 0.0378 |
| 1600 | neutral | 9 | 10000 | 9993/7/0 | 0.130 | 0.0374 | 45 | 0.93 [0.70, 1.19] | 1.010 | 0.0590 (1.58×) | 1.000 | 0.0409 |
| 1600 | neutral | 12 | 10000 | 9997/3/0 | 0.135 | 0.0355 | 41 | 0.85 [0.63, 1.09] | 1.008 | 0.0587 (1.65×) | 1.000 | 0.0399 |
| 1600 | neutral | pooled | 30000 | 29989/11/0 | 0.128 | 0.0370 | 133 | 0.94 [0.80, 1.08] | 1.010 | 0.0588 (1.59×) | 1.000 | 0.0395 |
| 1600 | advantaged | 6 | 10000 | 9998/2/0 | 0.039 | 0.0435 | 16 | 0.95 [0.55, 1.43] | 1.007 | 0.0629 (1.45×) | 1.000 | 0.0399 |
| 1600 | advantaged | 9 | 10000 | 9995/5/0 | 0.051 | 0.0426 | 26 | 1.19 [0.77, 1.64] | 1.011 | 0.0631 (1.48×) | 1.000 | 0.0383 |
| 1600 | advantaged | 12 | 10000 | 9991/9/0 | 0.049 | 0.0397 | 24 | 1.24 [0.77, 1.73] | 1.020 | 0.0633 (1.60×) | 1.000 | 0.0383 |
| 1600 | advantaged | pooled | 30000 | 29984/16/0 | 0.046 | 0.0419 | 66 | 1.13 [0.88, 1.41] | 1.013 | 0.0633 (1.51×) | 1.000 | 0.0388 |

### The combined per-island bound (confidence-qualified empirical bound, not a theorem)

P(Est | E) ≥ ρ̃·[1 − E[K_q]·q̄·r·h^rel] (notes §3.1). Est = target class in the final support (faker runs, to
local freeze); F = faker class alive at τ (for h); E[K_q] = 1 + mean bg_q; q̄ = Lemma D′ bound on the founder;
point = all at estimates; cons = ρ̃ lower 95%, q̄ with Wilson-upper bins, r and h^rel upper 95%. "old" = the
scramble lemma's form ρ̃ − P(F)·h⁺ with P(F) measured (its best case). P(Est) measured for comparison.

| N | type | n | P(Est) | ρ̃ | h^rel | E[K_q] | q̄ (D′) | r | bound (point) | bound (cons) | bound, measured q̄ | old (measured P(F)) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | disadvantaged | 6 | 0.0554 | 0.0564 | 0.42 | 1.12 | 0.1186 | 1.07 | 0.0530 | 0.0450 | 0.0554 | 0.0476 |
| 100 | disadvantaged | 9 | 0.0533 | 0.0548 | 0.51 | 1.13 | 0.1179 | 1.13 | 0.0506 | 0.0435 | 0.0534 | 0.0435 |
| 100 | disadvantaged | 12 | 0.0571 | 0.0585 | 0.47 | 1.14 | 0.1208 | 1.24 | 0.0538 | 0.0454 | 0.0571 | 0.0477 |
| 100 | disadvantaged | pooled | 0.0553 | 0.0566 | 0.47 | 1.13 | 0.1192 | 1.15 | 0.0524 | 0.0480 | 0.0553 | 0.0463 |
| 100 | neutral | 6 | 0.0401 | 0.0425 | 0.69 | 1.13 | 0.1539 | 1.18 | 0.0365 | 0.0302 | 0.0400 | 0.0159 |
| 100 | neutral | 9 | 0.0387 | 0.0407 | 0.60 | 1.16 | 0.1547 | 0.96 | 0.0365 | 0.0306 | 0.0387 | 0.0154 |
| 100 | neutral | 12 | 0.0393 | 0.0421 | 0.72 | 1.17 | 0.1541 | 1.15 | 0.0358 | 0.0297 | 0.0392 | 0.0119 |
| 100 | neutral | pooled | 0.0394 | 0.0418 | 0.67 | 1.15 | 0.1542 | 1.09 | 0.0363 | 0.0329 | 0.0393 | 0.0142 |
| 100 | advantaged | 6 | 0.0296 | 0.0325 | 0.85 | 1.50 | 0.1596 | 0.95 | 0.0262 | 0.0212 | 0.0294 | -0.0126 |
| 100 | advantaged | 9 | 0.0256 | 0.0282 | 0.93 | 1.52 | 0.1584 | 0.80 | 0.0232 | 0.0185 | 0.0257 | -0.0197 |
| 100 | advantaged | 12 | 0.0256 | 0.0274 | 0.78 | 1.52 | 0.1584 | 0.64 | 0.0241 | 0.0196 | 0.0259 | -0.0100 |
| 100 | advantaged | pooled | 0.0270 | 0.0294 | 0.86 | 1.51 | 0.1589 | 0.80 | 0.0245 | 0.0215 | 0.0270 | -0.0142 |
| 400 | disadvantaged | 6 | 0.0659 | 0.0662 | 0.22 | 1.49 | 0.0441 | 1.33 | 0.0649 | 0.0568 | 0.0659 | 0.0648 |
| 400 | disadvantaged | 9 | 0.0678 | 0.0681 | 0.24 | 1.53 | 0.0446 | 1.19 | 0.0668 | 0.0594 | 0.0678 | 0.0663 |
| 400 | disadvantaged | 12 | 0.0714 | 0.0715 | 0.10 | 1.55 | 0.0437 | 1.62 | 0.0708 | 0.0615 | 0.0714 | 0.0709 |
| 400 | disadvantaged | pooled | 0.0684 | 0.0686 | 0.18 | 1.52 | 0.0441 | 1.39 | 0.0675 | 0.0628 | 0.0684 | 0.0673 |
| 400 | neutral | 6 | 0.0324 | 0.0341 | 0.69 | 1.57 | 0.0893 | 1.03 | 0.0308 | 0.0253 | 0.0324 | 0.0126 |
| 400 | neutral | 9 | 0.0373 | 0.0391 | 0.66 | 1.62 | 0.0896 | 0.91 | 0.0356 | 0.0299 | 0.0372 | 0.0132 |
| 400 | neutral | 12 | 0.0352 | 0.0368 | 0.64 | 1.68 | 0.0885 | 0.86 | 0.0338 | 0.0281 | 0.0352 | 0.0140 |
| 400 | neutral | pooled | 0.0350 | 0.0367 | 0.66 | 1.62 | 0.0892 | 0.93 | 0.0334 | 0.0301 | 0.0349 | 0.0133 |
| 400 | advantaged | 6 | 0.0147 | 0.0168 | 0.88 | 2.99 | 0.0916 | 0.83 | 0.0134 | 0.0094 | 0.0150 | -0.0292 |
| 400 | advantaged | 9 | 0.0121 | 0.0137 | 0.89 | 3.06 | 0.0922 | 0.75 | 0.0111 | 0.0080 | 0.0122 | -0.0242 |
| 400 | advantaged | 12 | 0.0158 | 0.0171 | 0.62 | 3.08 | 0.0927 | 0.96 | 0.0142 | 0.0096 | 0.0155 | -0.0111 |
| 400 | advantaged | pooled | 0.0142 | 0.0159 | 0.79 | 3.04 | 0.0922 | 0.85 | 0.0129 | 0.0106 | 0.0142 | -0.0213 |
| 1600 | disadvantaged | 6 | 0.1238 | 0.1239 | 0.06 | 2.96 | 0.0151 | 1.34 | 0.1234 | 0.1111 | 0.1238 | 0.1237 |
| 1600 | disadvantaged | 9 | 0.1359 | 0.1364 | 0.40 | 3.12 | 0.0157 | 2.01 | 0.1310 | 0.1162 | 0.1358 | 0.1352 |
| 1600 | disadvantaged | 12 | 0.1348 | 0.1352 | 0.36 | 3.20 | 0.0147 | 1.71 | 0.1313 | 0.1167 | 0.1347 | 0.1343 |
| 1600 | disadvantaged | pooled | 0.1315 | 0.1318 | 0.28 | 3.09 | 0.0152 | 1.66 | 0.1289 | 0.1214 | 0.1315 | 0.1310 |
| 1600 | neutral | 6 | 0.0450 | 0.0466 | 0.30 | 3.18 | 0.0588 | 1.04 | 0.0439 | 0.0372 | 0.0448 | 0.0338 |
| 1600 | neutral | 9 | 0.0489 | 0.0516 | 0.44 | 3.52 | 0.0590 | 0.93 | 0.0472 | 0.0401 | 0.0488 | 0.0306 |
| 1600 | neutral | 12 | 0.0525 | 0.0559 | 0.43 | 3.68 | 0.0587 | 0.85 | 0.0515 | 0.0446 | 0.0533 | 0.0336 |
| 1600 | neutral | pooled | 0.0488 | 0.0514 | 0.40 | 3.46 | 0.0588 | 0.94 | 0.0475 | 0.0433 | 0.0489 | 0.0326 |
| 1600 | advantaged | 6 | 0.0055 | 0.0075 | 0.91 | 8.94 | 0.0629 | 0.95 | 0.0039 | 0.0010 | 0.0050 | -0.0458 |
| 1600 | advantaged | 9 | 0.0088 | 0.0106 | 0.60 | 9.23 | 0.0631 | 1.19 | 0.0062 | 0.0020 | 0.0076 | -0.0278 |
| 1600 | advantaged | 12 | 0.0070 | 0.0092 | 0.82 | 9.28 | 0.0633 | 1.24 | 0.0037 | 0.0001 | 0.0058 | -0.0389 |
| 1600 | advantaged | pooled | 0.0071 | 0.0091 | 0.76 | 9.15 | 0.0633 | 1.13 | 0.0046 | 0.0023 | 0.0061 | -0.0371 |

### Target founder: E[k_τ | E] per seeded copy (all forced targets cooperate with ALLC)

| N | n | founders | P(alive at τ) | E[k_τ] [95%] | E[k_τ | alive] | median R_τ | E[k e^{Λ}] (martingale) |
|---|---|---|---|---|---|---|---|
| 100 | 6 | 29978 | 0.0705 | 1.413 [1.328, 1.504] | 20.0 | -0.124 | 1.014 |
| 100 | 9 | 29971 | 0.0674 | 1.325 [1.238, 1.410] | 19.7 | -0.125 | 1.105 |
| 100 | 12 | 29969 | 0.0692 | 1.327 [1.235, 1.406] | 19.2 | -0.126 | 0.925 |
| 100 | pooled | 89918 | 0.0691 | 1.355 [1.304, 1.403] | 19.6 | -0.125 | 1.014 |
| 400 | 6 | 30000 | 0.0495 | 1.474 [1.347, 1.613] | 29.8 | -0.087 | 0.989 |
| 400 | 9 | 30000 | 0.0476 | 1.431 [1.295, 1.570] | 30.1 | -0.087 | 0.986 |
| 400 | 12 | 30000 | 0.0512 | 1.444 [1.322, 1.566] | 28.2 | -0.084 | 0.988 |
| 400 | pooled | 90000 | 0.0494 | 1.449 [1.368, 1.534] | 29.3 | -0.086 | 0.988 |
| 1600 | 6 | 30000 | 0.0365 | 1.154 [1.038, 1.273] | 31.6 | -0.028 | 0.974 |
| 1600 | 9 | 30000 | 0.0396 | 1.175 [1.078, 1.278] | 29.7 | -0.018 | 1.032 |
| 1600 | 12 | 30000 | 0.0386 | 1.181 [1.076, 1.294] | 30.6 | -0.015 | 0.989 |
| 1600 | pooled | 90000 | 0.0382 | 1.170 [1.105, 1.233] | 30.6 | -0.021 | 0.998 |

### Extrapolated spoiler sum for the members of P (natural seeding, n = 12)

S_x(N) = N·Σ_type μ_type(x)·q̄_type(N)·r_type(N)·h^rel_type(N), with q̄ = Lemma D′ bound, r and h^rel measured
(pooled over n) at N = 100, 400, 1,600 and extrapolated as power laws in N (r held at its N = 1,600 value if its
fit is unstable). Non-positive h^rel counts as 0. FairBot's pair has no fakers, so S ≡ 0 (the sanity check).

Fits: disadvantaged q̄ ∝ N^-0.74, h^rel ∝ N^-0.18 (h^rel = 0.47/0.18/0.28); neutral q̄ ∝ N^-0.35, h^rel ∝ N^-0.19 (h^rel = 0.67/0.66/0.40); advantaged q̄ ∝ N^-0.33, h^rel ∝ N^-0.04 (h^rel = 0.86/0.79/0.76)

| target x | μ fakers (disadv. / neutral / advant.) | S(100) | S(400) | S(1,600) | S(10⁴) extrapolated | with measured q̄: S(100 / 400 / 1,600) |
|---|---|---|---|---|---|---|
| `BOX(THEM(ME))` | 0.0000 / 0.0000 / 0.0000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 / 0.000 / 0.000 |
| `BOX1(THEM(ME))` | 0.0000 / 0.0000 / 0.0000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 / 0.000 / 0.000 |
| `BOX(THEM(THEM))` | 0.0000 / 0.0000 / 0.0000 | 0.001 | 0.001 | 0.002 | 0.005 | 0.000 / 0.000 / 0.001 |
| `BOX1(THEM(THEM))` | 0.0031 / 0.0000 / 0.0000 | 0.023 | 0.026 | 0.030 | 0.038 | 0.006 / 0.003 / 0.006 |
| `BOX(THEM(^C))` | 0.0000 / 0.0039 / 0.0000 | 0.041 | 0.077 | 0.145 | 0.339 | 0.020 / 0.046 / 0.086 |
| `BOX1(THEM(^C))` | 0.0000 / 0.0038 / 0.0000 | 0.040 | 0.076 | 0.144 | 0.336 | 0.020 / 0.045 / 0.085 |

## Task 3(c)-(e): the iid lottery with per-founder tags (n = 9, I = 1, no migration)

Every establisher founder is its own payoff-identical tagged class. Outcome = cooperative fixation (every final
pair mutually cooperates); efficient = final P(C,C) ≥ 0.95. τ = ALLC extinction ∧ local freeze ∧ 2,000; final
stop = local freeze (5) or the 10⁵ horizon (6). μ_est = 0.0246 (n = 9).

| N | islands | coop. fixation [95%] | efficient | τ stop 1/2/3 | final 5/6 | median τ [10–90%] | founders/island |
|---|---|---|---|---|---|---|---|
| 100 | 4000 | 0.0872 [0.0789, 0.0964] | 0.0872 | 3984/16/0 | 4000/0 | 13.4 [8.4, 22.0] | 2.5 |
| 400 | 4000 | 0.1945 [0.1825, 0.2071] | 0.1945 | 3990/10/0 | 4000/0 | 19.0 [13.9, 26.9] | 9.9 |
| 1600 | 4000 | 0.3825 [0.3676, 0.3977] | 0.3825 | 3997/3/0 | 3999/1 | 24.5 [19.5, 32.6] | 39.3 |
| 6400 | 1000 | 0.6860 [0.6566, 0.7140] | 0.6860 | 1000/0/0 | 1000/0 | 30.1 [25.2, 38.4] | 157.6 |
| 25600 | 400 | 0.9800 [0.9610, 0.9898] | 0.9800 | 400/0/0 | 400/0 | 36.0 [30.9, 42.5] | 629.5 |

(6,400, 1): first 200 islands (the spec's cell) 0.6600 [0.5919, 0.7221].
(1,600, 1): first 2,000 islands (the spec's cell) 0.3835 [0.3624, 0.4050].

### Establisher founders through the scramble (per seeded copy; islands in E, ALLC-extinction stops)

| N | group | founders | P(alive at τ) | E[k_τ] [95%, islands resampled] | E[k_τ | alive] | P(max ≥ N/4 before τ) | E[u(k_τ)] / (u₁·E[k_τ]) |
|---|---|---|---|---|---|---|---|
| 100 | all | 9799 | 0.0687 | 1.408 [1.261, 1.578] | 20.5 | 0.0280 | 0.590 |
| 100 | coopALLC | 9794 | 0.0686 | 1.408 [1.259, 1.577] | 20.5 | 0.0280 | 0.590 |
| 100 | exploitALLC | 5 | 0.2000 | 1.600 [0.000, 4.805] | 8.0 | 0.0000 | 0.979 |
| 100 | BOX(THEM(ME)) | 2095 | 0.0726 | 1.514 [1.191, 1.876] | 20.9 | 0.0320 | 0.588 |
| 100 | BOX1(THEM(ME)) | 2101 | 0.0681 | 1.485 [1.140, 1.891] | 21.8 | 0.0295 | 0.563 |
| 100 | BOX(THEM(THEM)) | 1962 | 0.0632 | 1.212 [0.921, 1.531] | 19.2 | 0.0250 | 0.621 |
| 100 | BOX(THEM(^C)) | 619 | 0.0711 | 1.514 [0.821, 2.268] | 21.3 | 0.0210 | 0.520 |
| 400 | all | 39344 | 0.0521 | 1.552 [1.439, 1.670] | 29.8 | 0.0034 | 0.661 |
| 400 | coopALLC | 39329 | 0.0521 | 1.553 [1.440, 1.671] | 29.8 | 0.0034 | 0.661 |
| 400 | exploitALLC | 15 | 0.0000 | 0.000 [0.000, 0.000] | nan | 0.0000 | nan |
| 400 | BOX(THEM(ME)) | 8176 | 0.0532 | 1.717 [1.441, 1.984] | 32.3 | 0.0042 | 0.618 |
| 400 | BOX1(THEM(ME)) | 8132 | 0.0499 | 1.405 [1.191, 1.647] | 28.1 | 0.0026 | 0.680 |
| 400 | BOX(THEM(THEM)) | 8226 | 0.0532 | 1.609 [1.355, 1.864] | 30.2 | 0.0033 | 0.656 |
| 400 | BOX(THEM(^C)) | 2509 | 0.0602 | 1.622 [1.264, 1.993] | 26.9 | 0.0024 | 0.736 |
| 1600 | all | 156897 | 0.0395 | 1.355 [1.285, 1.432] | 34.3 | 0.0001 | 0.801 |
| 1600 | coopALLC | 156843 | 0.0395 | 1.355 [1.284, 1.431] | 34.3 | 0.0001 | 0.801 |
| 1600 | exploitALLC | 54 | 0.0741 | 3.426 [0.365, 7.923] | 46.2 | 0.0000 | 0.887 |
| 1600 | BOX(THEM(ME)) | 32815 | 0.0393 | 1.308 [1.192, 1.435] | 33.3 | 0.0001 | 0.818 |
| 1600 | BOX1(THEM(ME)) | 32952 | 0.0395 | 1.390 [1.247, 1.569] | 35.2 | 0.0002 | 0.789 |
| 1600 | BOX(THEM(THEM)) | 32422 | 0.0406 | 1.389 [1.257, 1.519] | 34.2 | 0.0001 | 0.819 |
| 1600 | BOX(THEM(^C)) | 9883 | 0.0384 | 1.337 [1.097, 1.631] | 34.8 | 0.0003 | 0.779 |
| 6400 | all | 157587 | 0.0327 | 1.260 [1.201, 1.321] | 38.5 | 0.0000 | 0.926 |
| 6400 | coopALLC | 157515 | 0.0327 | 1.260 [1.200, 1.321] | 38.5 | 0.0000 | 0.926 |
| 6400 | exploitALLC | 72 | 0.0278 | 2.347 [0.000, 6.418] | 84.5 | 0.0000 | 0.942 |
| 6400 | BOX(THEM(ME)) | 32800 | 0.0327 | 1.180 [1.065, 1.307] | 36.1 | 0.0000 | 0.925 |
| 6400 | BOX1(THEM(ME)) | 33067 | 0.0337 | 1.262 [1.158, 1.373] | 37.5 | 0.0000 | 0.945 |
| 6400 | BOX(THEM(THEM)) | 32707 | 0.0344 | 1.385 [1.267, 1.508] | 40.3 | 0.0000 | 0.917 |
| 6400 | BOX(THEM(^C)) | 9915 | 0.0308 | 1.167 [0.977, 1.361] | 38.0 | 0.0000 | 0.928 |
| 25600 | all | 251816 | 0.0286 | 1.319 [1.264, 1.375] | 46.2 | 0.0000 | 0.974 |
| 25600 | coopALLC | 251702 | 0.0286 | 1.320 [1.265, 1.375] | 46.1 | 0.0000 | 0.974 |
| 25600 | exploitALLC | 114 | 0.0088 | 0.561 [0.000, 1.829] | 64.0 | 0.0000 | 0.992 |
| 25600 | BOX(THEM(ME)) | 52302 | 0.0289 | 1.342 [1.240, 1.445] | 46.4 | 0.0000 | 0.974 |
| 25600 | BOX1(THEM(ME)) | 52482 | 0.0289 | 1.360 [1.269, 1.456] | 47.0 | 0.0000 | 0.975 |
| 25600 | BOX(THEM(THEM)) | 52373 | 0.0286 | 1.346 [1.251, 1.445] | 47.0 | 0.0000 | 0.975 |
| 25600 | BOX(THEM(^C)) | 16239 | 0.0283 | 1.265 [1.102, 1.433] | 44.8 | 0.0000 | 0.979 |

### Predicting p(N)

- **semi-empirical** (RE 3, spec (d)): each island's state at τ mapped through the exact two-type escape u_K of
  the pooled count K of the largest mutually-cooperating establisher block (remainder treated as D); islands
  frozen before ALLC extinction count at their (determined) outcome;
- **independent founders after the scramble**: 1 − Π_j (1 − u_{k_j}) over the block's surviving founder lineages;
- **p_corr** (closed-form compound model, S6): each island's founder count and τ, each founder alive with
  probability 1/Φ(τ) and geometric with mean e^{R(τ)}Φ(τ) given alive (mean-field curvature path), pooled escape
  u_K (40 Monte Carlo draws per island);
- **naive** μ_est√(2cN/π); **independent-founder form** 1 − exp(−naive); **pooled-family form**
  erf(μ_est√(Nc/2))/erf(√(Nc/2)).

| N | measured | semi-empirical | ratio [95%] | indep. founders | p_corr | ratio | p_corr2 (post hoc) | ratio | naive | 1 − e^{−naive} | pooled erf |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.0872 | 0.0858 | 1.017 [0.963, 1.065] | 0.0854 | 0.0694 | 1.257 | 0.0743 | 1.174 | 0.1076 | 0.1020 | 0.1072 |
| 400 | 0.1945 | 0.1947 | 0.999 [0.962, 1.039] | 0.1918 | 0.1535 | 1.267 | 0.1673 | 1.163 | 0.2151 | 0.1935 | 0.2125 |
| 1600 | 0.3825 | 0.3692 | 1.036 [1.006, 1.064] | 0.3531 | 0.3157 | 1.212 | 0.3592 | 1.065 | 0.4302 | 0.3496 | 0.4102 |
| 6400 | 0.6860 | 0.6742 | 1.018 [0.982, 1.052] | 0.6106 | 0.5969 | 1.149 | 0.6822 | 1.006 | 0.8604 | 0.5770 | 0.7191 |
| 25600 | 0.9800 | 0.9566 | 1.024 [1.010, 1.037] | 0.8740 | 0.9029 | 1.085 | 0.9616 | 1.019 | 1.7209 | 0.8211 | 0.9690 |

Calibration of the semi-empirical predictor (islands binned by predicted u; measured rate | mean prediction):

- N = 100: [0, 1e-09): 3377 islands, 0.000 | 0.000; [1e-09, 0.1): 77 islands, 0.117 | 0.061; [0.1, 0.3): 128 islands, 0.188 | 0.201; [0.3, 0.6): 126 islands, 0.492 | 0.441; [0.6, 0.9): 120 islands, 0.708 | 0.738; [0.9, 1): 172 islands, 0.983 | 0.981
- N = 400: [0, 1e-09): 2412 islands, 0.000 | 0.000; [1e-09, 0.1): 191 islands, 0.047 | 0.053; [0.1, 0.3): 406 islands, 0.214 | 0.199; [0.3, 0.6): 389 islands, 0.419 | 0.443; [0.6, 0.9): 319 islands, 0.777 | 0.751; [0.9, 1): 283 islands, 0.958 | 0.975
- N = 1600: [0, 1e-09): 895 islands, 0.000 | 0.000; [1e-09, 0.1): 440 islands, 0.066 | 0.053; [0.1, 0.3): 725 islands, 0.214 | 0.197; [0.3, 0.6): 798 islands, 0.474 | 0.440; [0.6, 0.9): 666 islands, 0.757 | 0.747; [0.9, 1): 476 islands, 0.975 | 0.970
- N = 6400: [0, 1e-09): 8 islands, 0.000 | 0.000; [1e-09, 0.1): 14 islands, 0.071 | 0.055; [0.1, 0.3): 93 islands, 0.258 | 0.200; [0.3, 0.6): 247 islands, 0.518 | 0.460; [0.6, 0.9): 370 islands, 0.732 | 0.762; [0.9, 1): 268 islands, 0.978 | 0.968
- N = 25600: [0, 1e-09): 0 islands, – | –; [1e-09, 0.1): 0 islands, – | –; [0.1, 0.3): 1 islands, 1.000 | 0.262; [0.3, 0.6): 3 islands, 0.000 | 0.544; [0.6, 0.9): 49 islands, 0.980 | 0.817; [0.9, 1): 347 islands, 0.988 | 0.982

Fitted exponent of p over N = 100–1,600: measured 0.533 [0.495, 0.571]; semi-empirical 0.526; p_corr 0.546; p_corr2 0.568; naive 0.500.

