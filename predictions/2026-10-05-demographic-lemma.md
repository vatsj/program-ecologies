# Predictions: the demographic lemma, the factorized spoiler bound, and the establishment formula (2026-10-05)

Spec `specs/2026-10-05-demographic-lemma.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-05-demographic-lemma-gpt-6.1-sol.md`).
Written by the Opus subagent before any counted run. Code `src/demographic_lemma.py`; proofs `notes/demographic-lemma.md`;
results `runs/demographic-lemma.{md,json}`.

## RE predictions (copied verbatim from the spec)

1. **Lemma D holds with d_min ≥ 0.9 per generation for lineages that stay below N/20**, and the ghost control is within
   a factor 1.3 of 1/(1 + t) at every fixed t ≥ 5 at N = 400 and 1,600. *Falsifier:* measured ghost survival exceeds
   the proved bound at any (N, t) by more than its 95% interval, or the ratio to 1/(1 + t) is outside [0.5, 1.3] at
   some t ≥ 5.
2. **r_q ∈ [0.8, 1.6] in every cell, larger for ALLC-cooperating fakers than for D-cooperating ones** [after review:
   sol expects no universal interval; the RE keeps a numerical prediction so it can fail], and the recomputed
   empirical bound is **positive in all 18 cells** and extrapolates positive to N = 10⁴ for every member of P.
   *Falsifier:* any r_q outside [0.6, 2], or the bound non-positive in more than 2 of 18 cells, or the extrapolated sum
   exceeds 1 below N = 10⁴ for FairBot's family (which has no fakers and so should give 0 identically; that cell is
   the sanity check).
3. **The corrected establishment formula (curvature loss, broad k_τ, concave u_k) holds within a factor 1.25 at
   N = 100, 400, 1,600** (ratio measured/predicted in [0.8, 1.25]), the naive square-root formula overestimates by
   10–40% at N = 100–400, and the fitted exponent over N = 100–1,600 is in [0.45, 0.65]. The direct u₁ measurement is
   within a factor 1.2 of the diffusion value with the erf correction at every N, and the exact finite-N formula
   agrees with the simulation within intervals. *Falsifier:* corrected ratio outside [0.6, 1.6] at any N, or exponent
   outside [0.4, 0.7], or u₁ off by more than a factor 1.5.
4. **E[k_τ | E] per seeded copy is 0.75–0.95 for ALLC-cooperating establishers** (the curvature loss of about
   1 − 1/cosh(0.15) per generation over τ, partly offset because the loss shrinks as ALLC dies) **and > 1.2 for
   ALLC-exploiting ones.** *Falsifier:* the ALLC-cooperating value outside [0.6, 1.05].
5. [after review] **Saturation at N = 6,400 follows the independent-founder form (≈ 0.56 before scramble losses and
   spoilers) rather than the pooled-family form (≈ 0.69)**, because the seeded establisher copies are separate
   lineages that must each survive the scramble before they can pool. *Falsifier:* the (6,400, 1) cell above 0.66
   or below 0.35.

## Verdict rules (how each RE prediction is scored)

- **RE 1.** "Exceeds the proved bound": measured event-clock survival of the ghost (Wilson 95% lower end) above the
  event-clock Lemma D bound (notes §1.4) for the killed-at-K version, K = N/20 and N/4, at t = 5, 10, 20, 40 and
  N = 100, 400, 1,600. The ratio clause is judged on the unkilled ghost at N = 400 and 1,600 (the prediction's scope);
  N = 100 is reported. Point estimates decide the band; the interval is reported.
- **RE 2.** r_q is the per-founder correction P(tagged faker founder alive at τ | A, E)/P(tagged founder alive at τ | E),
  with A = {target class alive at τ}. "Every cell" = (N, n, faker type) with N ∈ {100, 400, 1,600}, n ∈ {6, 9, 12}, three
  types (27 cells). A cell counts against the band only if its point estimate is outside; cells with fewer than 10
  joint events (A and founder alive) are reported as underpowered and judged on the n-pooled cell instead. "ALLC-
  cooperating fakers larger than D-cooperating ones": neutral (probe-faker) pooled r above disadvantaged pooled r at
  each N. The 18 cells of the combined bound are (N ∈ {100, 400}) × 3 types × (n ∈ {6, 9, 12}) as in RESULTS
  "The scramble lemma"; the N = 1,600 cells are reported in addition. The bound uses Lemma D′'s q̄ (binned
  inf_φ form, notes §1.1, with the measured Φ_τ distribution) and the measured r and h, and is labelled a
  confidence-qualified empirical bound.
- **RE 3.** "Corrected formula" = the spec's (d) predictor: the measured post-scramble state of each lottery island
  (pooled count K_τ of the largest mutually-cooperating establisher block at ALLC extinction) mapped through the exact
  two-type escape u_K, averaged over islands. The closed-form compound model (p_corr below) is judged under S6.
  Exponent: least-squares slope of log p on log N over the three measured cells N = 100, 400, 1,600 (n = 9).
  "Naive overestimates by 10–40%": naive/measured − 1 at N = 100 and 400.
- **RE 4.** E[k_τ | E] per seeded copy measured on the tagged target founder of the forced runs (every target there
  cooperates with ALLC) and on every establisher founder in the n = 9 lottery; the falsifier is judged on each N
  separately. ALLC-exploiting establishers: reported if any are seeded (μ ≈ 0 at n ≤ 12, so likely untestable).
- **RE 5.** The (6,400, 1) lottery cell at n = 9, 200 runs, point estimate.

## Subagent predictions (S1–S9), with falsifiers

- **S1 (ghost at N = 100).** The unkilled ghost's survival at N = 100 exceeds 1/(1 + t) by more than 15% at t = 40,
  because its death rate is d = 1 − k/N < 1 for surviving lineages of size ~t and the neutral fixation floor is 1/N;
  at N = 1,600 the ratio is in [0.9, 1.1] at every t. *Falsifier:* N = 100, t = 40 ratio ≤ 1.15, or any N = 1,600
  ratio outside [0.9, 1.1].
- **S2 (E[k_τ] above the curvature value at small N).** E[k_τ | E]/k₀ for ALLC-cooperating establishers exceeds 1.05
  at N = 100 (so RE 4's falsifier fires there), decreases with N, and is in [0.88, 1.08] at N = 1,600. The mean-field
  curvature alone gives 0.93; the family's own advantage and a survivor's own frequency push it up, more at small N.
  *Falsifier:* N = 100 value ≤ 1.05, or not decreasing from N = 100 to 1,600, or the N = 1,600 value outside
  [0.88, 1.08].
- **S3 (u_k).** The direct D-sea simulation agrees with the exact birth–death formula at every (N, k) within its 95%
  interval (at most 1 of 20 cells outside, as chance allows), and for k = 16 the measured u₁₆ exceeds
  1 − (1 − u₁)¹⁶ by more than the interval at every N ≤ 1,600. *Falsifier:* 2 or more cells outside the interval of
  the exact value, or u₁₆ not above the independent-copies form at some N ≤ 1,600.
- **S4 (r_q decomposition).** Pooled over n, r_q ∈ [0.9, 1.6] for each type at each N, and the shared-background part
  r_env = E[s_A(τ)s_F(τ)]/(E[s_A(τ)]E[s_F(τ)]) (conditional survivals binned on τ) is ≥ 1 and accounts for at least
  half of r − 1 whenever r − 1 > 0.1. *Falsifier:* a pooled r outside [0.9, 1.6], or r_env < 1, or r_env − 1 < (r − 1)/2
  in a cell with r − 1 > 0.1 and ≥ 30 joint events.
- **S5 (post-scramble escape is two-type).** The semi-empirical predictor (RE 3's) is within [0.85, 1.15] of the measured
  per-island chance at N = 100, 400, 1,600. *Falsifier:* outside [0.85, 1.15] at any of the three.
- **S6 (closed-form compound model underpredicts).** p_corr — founders Bin(N, μ_est), τ from the measured island
  distribution, each founder alive with probability 1/Φ(τ) and geometric with mean e^{R(τ)}Φ(τ) given alive (R, Φ from
  the mean-field curvature path), escape u_exact(K) of the pooled count — underpredicts measured p by a factor in
  [1.1, 1.45] at every N ∈ {100, 400, 1,600}, because it omits the family and own-frequency advantages during the
  scramble. *Falsifier:* measured/p_corr outside [1.1, 1.45] at any of the three.
- **S7 (saturation).** The (6,400, 1) cell is at or above 0.66 (point estimate): pooling after the scramble wins over
  independent founders, so RE 5's falsifier fires; and it lies within 0.1 of the semi-empirical predictor computed on
  the same islands. *Falsifier:* point estimate below 0.66, or |measured − semi-empirical| > 0.1.
- **S8 (Lemma D′ is sharp for fakers).** The binned Lemma D′ bound on the tagged faker founder's survival at τ is within
  a factor 2 of the measured survival for every faker type at every N (pooled over n), against B1's vacuous bound for
  probe-fakers. *Falsifier:* bound/measured > 2 in any (N, type) cell with ≥ 30 surviving founders.
- **S9 (combined bound).** The recomputed empirical bound is positive in all 27 cells (not just the RE's 18), and the
  extrapolated spoiler sum Σ_q N μ_q q̄_q r_q h_q for the probe-reader targets stays below 1 to N = 10⁴ only if h keeps
  falling (I predict h at N = 1,600 below 0.15). *Falsifier:* any non-positive cell, or h(1,600) ≥ 0.15 for the
  probe-reader pairs.

## Design notes (declared before the runs)

- Forced runs (Tasks 1–2): the scramble-lemma forced pairs (`spoiler_conditioned.forced_pairs`, 7 per n; types
  disadvantaged = pairs 0–1, neutral = 2–5, advantaged = 6), fresh background salt, one target copy and one faker copy
  inserted as in treatment (b) k = 1, each inserted copy a *tagged* duplicate class (payoff-identical, so the law of the
  process is unchanged) so that per-founder survival is observable. 3,000 backgrounds per (N, n, type) at N = 100 and
  400 (disadvantaged 1,500 per pair, neutral 750 per pair, advantaged 3,000); at N = 1,600 the same allocation scaled to
  1,000 per (n, type) if the timing batch projects more than 3 hours on 3 workers, else 3,000. Each background is run
  twice with common random numbers: (i) faker run, to τ = ALLC extinction ∧ local freeze ∧ 2,000 generations and then
  on to local freeze (horizon 10⁵) for the outcome; (ii) ghost run (the faker founder replaced by a ghost, fitness
  pinned to the mean) to t = 40 generations, recording the ghost at t = 5, 10, 20, 40, at τ, its first hitting times of
  N/20 and N/4, and Φ on both clocks.
- D-sea runs (Task 3b): the seeds_in_n kernel on {FairBot k, D N − k}, k = 1, 2, 4, 8, 16, 10⁴ runs per cell at
  N = 100, 400, 1,600 and 2,000 at N = 6,400.
- Lottery (Task 3c–e): n = 9, I = 1, no migration, iid seeds from μ, every establisher founder its own tagged class;
  N = 100 (4,000 islands), 400 (4,000), 1,600 (2,000), 6,400 (200); horizon 10⁵ generations; outcome = cooperative
  fixation (every final pair mutually cooperates), with efficiency reported.
- Intervals: Wilson 95% for proportions, bootstrap (2,000 resamples) for ratios and means.

## Addendum: static and exact numbers computed before the simulations (`python3 src/demographic_lemma.py static`)

- Exact u₁ (birth–death formula, self-excluded payoffs): 0.04206 / 0.02141 / 0.01081 / 0.00543 at N = 100 / 400 /
  1,600 / 6,400; diffusion with erf correction 0.04368 / 0.02185 / 0.01093 / 0.00546 (ratio exact/diffusion 0.963 /
  0.980 / 0.990 / 0.995; the erf correction is < 10⁻⁷ at these N).
- Pooled u_k is nearly linear in k for k ≤ √N: u₁₆ = 0.608 / 0.334 / 0.172 / 0.087 against 16u₁ = 0.673 / 0.343 / 0.173 /
  0.087 and the independent-copies form 1 − (1 − u₁)¹⁶ = 0.497 / 0.293 / 0.160 / 0.084. The spec's concavity example
  (0.49 vs 0.65 at N = 100, k ≈ 15) uses the independent-copies form; the pooled value is ≈ 0.58.
- Mean-field curvature factor e^R for a payoff-neutral ALLC-cooperating establisher over the {ALLC, D} scramble:
  0.926–0.928 at every N (not 0.8–0.9).
- Lemma D event-clock bound / Poisson-clock 1/(1 + d_min T): 1.10–1.05 (N = 100), 1.05–1.02 (400), 1.03–1.01 (1,600)
  over T = 5–40.
- Rough compound-model values (τ = medians 13.4 / 19 / 24.5 / 30, ℓ = e^R = 0.93, μ_est = 0.0246): p_corr ≈ 0.072 /
  0.157 / 0.323 / 0.60 at N = 100 / 400 / 1,600 / 6,400, against measured 0.090 / 0.185 / 0.412 (seeds-in-n, n = 9).
  This motivated S6. The naive form is 0.108 / 0.215 / 0.430 / 0.86; the independent-founder saturation form
  1 − exp(−naive) is 0.577 at 6,400 and the pooled-family form erf(μ_est√(Nc/2))/erf(√(Nc/2)) is 0.719 (μ_est = 0.0246
  at n = 9; the spec's 0.56 / 0.69 used 0.023).

## Addendum 2: design extensions declared before any counted run (timing batch, separate salt, outcomes not used)

Timing: 0.002–0.02 s per forced background (both runs) at N = 100–1,600; 0.01–0.2 s per lottery island at N = 1,600,
0.1 s at 6,400, 1–3 s at 25,600. Because the runs are cheap, the design is enlarged now, before any counted run:
- **Forced runs:** 10,000 backgrounds per (N, n, type) at every N (allocation per pair ALLOC × 10/3: disadvantaged
  5,000 per pair, neutral 2,500 per pair, advantaged 10,000). The spec's 3,000 are the first block (rep < ALLOC);
  verdicts use all 10,000; the 3,000 block is reported for RE 2 in addition.
- **D sea:** 10⁴ runs per (N, k) at N = 100, 400, 1,600 and 4,000 at 6,400.
- **Lottery (n = 9):** 4,000 islands at N = 100, 400 and 1,600 (the spec's new 1,600 cell asked for 2,000: the first
  2,000 reps are that cell), 1,000 at 6,400 (the first 200 are the spec's cell; RE 5 and S7 are judged on all 1,000,
  the 200 reported too), and an exploratory **400 islands at N = 25,600**, where the independent-founder and pooled
  forms differ most (1 − e^{−μ√(2cN/π)} = 0.82 against erf(μ√(Nc/2))/erf(√(Nc/2)) = 0.97 at μ_est = 0.0246).
  S10 (added now): the 25,600 cell is above 0.85 (pooled side). *Falsifier:* point estimate ≤ 0.85.
- Raw forced rows are saved as `runs/demographic-lemma-forced.npz` (gitignored by the repo's `runs/*.npz` rule; 270,000
  rows); aggregates and every reported number go to `runs/demographic-lemma.json`.
