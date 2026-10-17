# Annealed mutation: run report (2026-10-16)

Spec `specs/2026-10-16-annealed-mutation.md` (the amendments supersede the earlier text); notes `notes/annealed.md`
(§1 design by hand, §2 validation, assays, costs and an extension declared before any cell); predictions
`predictions/2026-10-16-annealed-mutation.md` (the RS's two statements first, outcome regions declared before any
cell). Summary numbers in `runs/annealed.json`; validation in `runs/annealed-validate.json`; the post-hoc
identity-predator diagnostic in `runs/annealed-idprey.json`; rows in `runs/annealed/cells_*.json.gz` and
`runs/annealed/assay_*`. Cells with re-injection are finite-ε approach-rate diagnostics at finite (N, I = 8, horizon),
never π; ε = 0 cells are lottery statistics. uot = universal on the removing-rivals target 𝒯 (holders mutual with
PrudentBot's H unit, pairwise mutual).

**Design in one paragraph.** I = 8, calibrated mN, r = 100 production encounters per Moran event at every N. Seed at
generation 0; no arrivals before 200; then εN(t) = a(1 + (t − 200)/t₀)^(−2) with t₀ = N/2 and A = N·Λ_N = 3/(ρ·μ_AP)
= 156 arrivals per island (52 at K = 1), cut at 10,000, then a 2,000-generation mutation-free chase. Arm (iv) is
constant rain from 200 to 10,000 with the same delivered total. Arms share seed founders, kernel draws and the
per-island sequence of fresh-founder spellings. Part F: one forced rival island (anti-punisher AP or certified-defection
detector DET) among seven FairBot islands, under the same schedule.

## Deviations and process (all disclosed before the cells they affect, except the last two items)

- Part F (forced rivals) is an addition to the spec: natural exploitable rivals at I = 8 are too rare to measure a cure
  (notes §1.1; confirmed: 12 eligible in all rain cells, 7 in ε = 0 cells).
- 40 replicates in arms (i), (iii)-S-nonself, (iv) and Part F K = 3 (20 elsewhere); the native-r control at (400, 8)
  (notes §2.3). No drop-order step.
- Arm (iv) was run for S-nonself only (notes §1.5).
- *Process, after the fact:* the batch shell was twice restarted under new names (`cells2.sh`, `cells3.sh`) to keep
  workers busy while single slow runs held one worker; no job was run twice, no row was discarded, and no cell
  changed. Scramble-failure runs (all islands unheld) are slow under S-nonself (up to 10,600 s at N = 1,600) because
  their islands never settle.
- *Post hoc:* the identity-predator diagnostic (`src/annealed_idprey.py`) was written after seeing one whole-run
  identity takeover; it is labelled as such below.
- About 30 worker-hours in all (≈ 10.5 h wall on 2–3 workers).

## Validation (notes §2.1)

- ε = 0 equals the scaling and removing-rivals kernels draw for draw (states identical at (200, 8) and (400, 8));
  four stored (200, 64) runs reconstruct to 2,000 with 0 differences over 160 trace points (r = 100 is native there).
- In event-indexed mode the kernel reproduces removing-rivals' rain draw for draw; two stored B2 runs give identical
  snapshots and the same 6 + 6 colonizations with the same classes (the drift classifier agrees on stored lineages).
- Paired founder streams verified; the schedule integrates exactly (delivered 154.6 / 153.1 / 150.1 / 144.4 per island
  by 10,000; realized 153.3 / 152.4 / 149.1 / 143.8 in arm (i)).
- Native r at (400, 8), ε = 0, replicates 0–19: uot 14/20, 3 scramble failures, identity 0.044 per island; r = 100,
  same replicates: 13/20, 5, 0.10. Fixing r changed nothing beyond run-level noise.

## Single-arrival assays (notes §2.2)

- A neutral `C` arrival on a FairBot island colonizes (≥ 0.5) at 0.88–1.24 × 2/N and fixes at 0.76–1.36 × 1/N at
  N = 200–1,600 (10,000–40,000 replicates); the identity-exploitable shadow `if(CHK(them,^D,D),C,D)` likewise.
- The top predator of each class establishes with probability 0.22–0.28 at every N (exact ρ 0.26) and every
  establishment returns its island to the target within ≈ 110 generations (median 75–95).

## Drift along the path (natural cells)

Drift colonizations (a rain lineage, neutral or deleterious against the island's majority at arrival, holding ≥ 0.5 of
its arrival island at a 5-generation checkpoint), per island over the run, and drift-free runs:

| N | arm (i) annealed: drift / island [95% CI] | drift-free runs (i) [Wilson] | arm (iv) constant | drift-free (iv) | arm (ii) sponsored + annealed | drift-free (ii) |
|---|---|---|---|---|---|---|
| 200 | 0.29 [0.23, 0.36] | 4/40 = 0.10 [0.04, 0.23] | 0.32 | 7/40 | 0.16 | 8/20 |
| 400 | 0.16 [0.10, 0.23] | 14/40 = 0.35 [0.22, 0.51] | 0.14 | 17/40 | 0.05 | 15/20 |
| 800 | 0.034 [0.016, 0.056] | 30/40 = 0.75 [0.60, 0.86] | 0.059 | 29/40 | 0.025 | 17/20 |
| 1,600 | 0.022 [0.006, 0.044] | 35/40 = 0.875 [0.74, 0.95] | 0.013 | 36/40 | 0.013 | 18/20 |

- **Slopes** (Poisson regression of per-run counts on log N, run-bootstrap 95%): arm (i) **−1.28 [−1.61, −1.02]**,
  arm (iv) −1.33 [−1.71, −1.04], arm (ii) −1.35 [−2.18, −0.80], pooled −1.31 [−1.55, −1.12]; FairBot islands of Part F
  −1.23 [−1.49, −1.02]. Excluding scramble-failure runs, arm (i) −1.24 [−1.62, −0.95]; target-status arrivals only,
  −1.31.
- **Per arrival**, drift colonization × N is 0.30–0.42 at N = 200–400 in every rate bin (εN < 0.03 up to > 0.3), 0.17–0.28
  at 800 and 0.10–0.34 at 1,600: no rate dependence. The hand prediction that high early rates suppress per-arrival
  drift (and so make annealing drift less than constant rain at small N) is wrong; drift scales with arrivals (K = 1 at
  N = 200: 0.081 per island, 0.28 × the K = 3 value).
- **Where drift lands.** Arm (i): 53 / 18 / 7 / 5 drift colonizations on target islands, 5 / 4 / 1 / 1 on rivals, 35 /
  29 / 3 / 1 on unheld islands (mostly in scramble-failure runs) at N = 200 / 400 / 800 / 1,600. 93% are neutral at
  arrival. **They are transient:** 86 / 44 / 8 / 5 of the 93 / 51 / 11 / 7 drift lineages are lost by 12,000, 7 / 7 / 2 / 1
  fixed. Colonizing drift lineages also spread by migration: 187 / 172 / 50 / 31 further islands reached ≥ 0.5 by
  lineages that colonized as drift (most of them transient too).
- **The K = 1 exposure** at N = 800 is drift-free in 20/20 runs (arms (i) and (ii)).

## Cures (Part F: one rival island among seven FairBot islands)

| N | AP, K = 3 [Wilson] | DET, K = 3 | natural mix (0.52 AP + 0.48 DET) | AP, K = 1 | DET, K = 1 |
|---|---|---|---|---|---|
| 200 | 40/40 = 1.00 [0.91, 1.00] | 13/40 = 0.33 [0.20, 0.48] | 0.68 | 19/20 = 0.95 | 1/20 = 0.05 |
| 400 | 40/40 = 1.00 | 14/40 = 0.35 [0.22, 0.51] | 0.69 | – | – |
| 800 | 40/40 = 1.00 | 16/40 = 0.40 [0.26, 0.55] | 0.71 | 18/20 = 0.90 | 4/20 = 0.20 |
| 1,600 | 38/40 = 0.95 [0.83, 0.99] | 13/40 = 0.33 [0.20, 0.48] | 0.65 | – | – |

- **The cure is N-independent and class-split, as the path intends.** Per-arrival hazard, pooled over N:
  AP 0.029 (formula ρ·μ = 0.019), DET 0.0029 (formula 0.0015); about 1.5–2× the one-arrival formula, through selected
  exploiters that are not predators under the strict definition (8–13 of 38–40 AP cures per N; they self-cooperate or
  react) and a few migrant predators.
- Median time to cure (AP) 70 / 93 / 105 / 160 generations after onset; DET 185–1,220.
- **Extrapolated to the spec's original path** (12 arrivals per island): AP 0.30, DET 0.03, natural mix 0.17.
- Natural exploitable rivals at onset: 12 in all rain cells, 5 cured (0.42); 7 at ε = 0, 0 cured.

## Network outcomes (natural cells, generation 12,000)

| N | uot: (iii)-S / (i) / (iv) | (iii)-P / (ii) | identity islands per island: (iii)-S / (i) / (iv) | (iii)-P / (ii) | scramble-failure runs (iii)-S / (i) / (iv) | island efficiency (i), all runs / excluding scramble failures |
|---|---|---|---|---|---|---|
| 200 | 25 / 29 / 24 of 40 | 14 / 15 of 20 | 0.050 / 0.050 / 0.050 | 0.050 / 0.100 | 12 / 9 / 10 | 0.78 / 1.00 |
| 400 | 22 / 26 / 22 | 15 / 16 | 0.072 / 0.072 / 0.097 | 0.050 / 0.050 | 13 / 9 / 11 | 0.77 / 1.00 |
| 800 | 23 / 21 / 22 | 15 / 14 | 0.125 / 0.122 / 0.125 | 0.025 / 0.025 | 6 / 5 / 5 | 0.86 / 0.99 |
| 1,600 | 28 / 30 / 28 | 15 / 15 | 0.038 / 0.038 / 0.062 | 0.019 / 0.019 | 1 / 0 / 1 | 1.00 / 1.00 |

- **Annealing leaves identity where the seed put it.** Paired by replicate, identity islands (i) − (iii)-S are
  0 / 0 / −0.003 / 0 per island, and (ii) − (iii)-P +0.05 / 0 / 0 / 0 (one run at N = 200). Identity islands are all
  seeded establishments; none of the 170 identity islands present at onset in rain cells resolved.
- **Identity takeovers of target islands:** none in arms (i) and (ii); one event in arm (iv) at N = 1,600 (replicate 7):
  a single TwinD founder (`if(or(not(CHK(me,them,D)),CHK(me,me,D)),C,D)`) arrived at generation 6,341 on an island held
  by `if(CHK(them,me,C),C,if(CHK(them,them,C),C,D))` (unit 87, a target unit that cooperates with anyone certified to
  cooperate with itself), was **selected** under the drift classifier (it exploits the holder), fixed in 19 generations,
  and took all eight islands by migration within 45 generations: the whole run became an identity clique. *Post hoc
  diagnostic:* 0–9% of target islands are held by such identity-prey holders (identity-predator mass 2.6·10⁻⁴–7·10⁻⁴
  per holder), so ≈ 0.04–0.11 selected identity arrivals per prey island over the schedule; the paired annealed run
  had the same founder on the same island but at a time when the island was held by a non-prey holder.
- **Secondary takeovers of shadows** (a shadow-colonized target island later leaving target status for ≥ 25
  generations): 0.091 / 0.016 / 0.019 / 0.009 per island in (i), 0.106 / 0.016 / 0.022 / 0.006 in (iv); all to
  rivals or unheld, none to identity.
- **Rain rescues scramble failures.** Of 32 S-nonself scramble-failure runs at ε = 0, 13 are held under annealing
  (12 of them universal on target) and 7 under constant rain; 4 and 2 runs went the other way.
- uot changes with annealing by +0.10 / +0.10 / −0.05 / +0.05 (S-nonself, paired) and +0.05 / +0.05 / −0.05 / 0
  (sponsored), all intervals including 0; the sponsored arm's uot is 0.70–0.80 at every N.
- The commonest failure besides identity is closed-open rivals (0.05–0.12 of islands), as in removing-rivals; 89 of 176
  present at onset in rain cells changed holder by neutral drift, as at ε = 0 (49 of 108).

## Costs

Assays ≈ 0.4 worker-h; natural cells (40-run arms) ≈ 17 worker-h, sponsored ≈ 4, Part F ≈ 5, K = 1 and the native-r
control ≈ 1.3. The single slowest runs were scramble failures (10,618 s for one (1,600, 8) run under constant rain).

## Verdicts (scored as declared in the predictions file)

| # | prediction | outcome |
|---|---|---|
| RS 2 | "drift should never colonize an island, only reintroduce fit programs" | **fails at every N as a cell statement** (drift colonizations in every rain cell, 5 in 40 runs at N = 1,600); per run the drift-free fraction rises 0.10 → 0.35 → 0.75 → 0.875, short of the declared "holds in the limit" bar (≥ 0.9 at 1,600). Holds in the K = 1 cells at N = 800 (0/40 runs with drift), where the cure is 0.90 (AP) and 0.20 (DET). One *selected* arrival (an identity predator) did the worst damage of the run |
| RS 1 | "the tail is light enough that islands can't drift (but heavy enough to prey on inefficiencies)" | **inconclusive at N = 1,600** (drift-free 0.875 < 0.9; natural-mix cure 0.65); for anti-punishers both halves nearly hold (0.875, 0.95), for detectors the prey half fails (0.33) |
| RE 1 | drift falls along the path, slope in [−1.3, −0.7], drift-free rising | **supported** (slope −1.28 [−1.61, −1.02]; drift-free 0.10 / 0.35 / 0.75 / 0.875); the point is steeper than the expected −1 |
| RE 2 | cure of exploitable rivals ≥ 0.8 at every N | **inconclusive** on the natural mix (0.65–0.71 at every N); **supported for AP** (0.95–1.00), **falsifier fired for DET** (0.33–0.40) |
| RE 3 | ≥ 0.5 drift-free at 1,600, with cures ≥ 0.8 | drift clause **held** (0.875), cure clause **failed** (0.65): inconclusive by the declared region |
| RE 4 | identity under (i) ≥ ε = 0 at every N; (ii) uot < 0.85 | identity: **paired difference zero** at three N and −0.003 at N = 800 (one island in one run; interval includes 0): inconclusive by the declared region, the substance holds (annealing neither adds nor removes identity); uot clause **supported** (0.75 / 0.80 / 0.70 / 0.75); falsifier not fired |
| RE 5 | constant rain gives more late identity takeovers at N ≥ 400; drift equal ±30% | **falsifier fired**: drift ratio (i)/(iv) 1.16 / 0.58 / 1.75 at N = 400 / 800 / 1,600 (small counts); late identity takeovers 0 / 0 / 0.025 per island, the one event a whole-run takeover |
| Gemini | constant rain: more secondary shadow takeovers and late identity takeovers at N ≥ 400; original-path cure < 0.5 | first clause **failed** (secondary takeovers (iv) − (i) = 0.000 pooled; identity +0.008 [0, 0.025]); second clause **held** by extrapolation (0.17 natural mix, 0.30 AP at 12 arrivals) |
| Sol | schedule-dependent outcomes; heterogeneous identity effects | first clause **failed** as scored (no statistic differs between (i) and (iv) with an interval excluding 0; scramble rescue 13 vs 7 runs is suggestive); second clause **not supported** (identity effects are single-run events in both founder regimes) |
| A1 | drift 0.08 / 0.05 / 0.03 / 0.015 (× 2.5), slope [−1.1, −0.55] | **failed** at N ≤ 400 (0.29, 0.16: 3–4× too high, I took the per-arrival rate from εN ≥ 0.01 removing-rivals cells and assumed a rate suppression that does not exist) and on the slope (−1.28); falsifier (slope outside [−1.4, −0.4]) not fired |
| A2 | annealed/constant drift 0.3–0.85 at N = 200 | **failed** (0.91; no rate dependence of per-arrival drift); falsifier (≥ 1) not fired |
| A3 | drift-free ≈ 0.5 / 0.65 / 0.8 / 0.9 ± 0.2; ≥ 0.75 at 1,600 | **failed at N ≤ 400** (0.10, 0.35), held at 800 and 1,600; falsifier not fired |
| A4 | ≥ 0.7 of drift colonizations shadows on target; ≥ 0.5 transient | shadow share **failed** at N ≤ 800 (0.57, 0.35, 0.64; 0.71 at 1,600), falsifier (< 0.5) **fired at N = 400** (unheld islands of scramble-failure runs); transience **held** (0.71–0.92 lost by 12,000) |
| A5 | AP ≥ 0.9, DET 0.15–0.6, no trend; K = 1 AP 0.5–0.9, DET ≤ 0.3 | **held** at K = 3; K = 1 AP 0.95 at N = 200 above the range |
| A6 | neutral 2/N and 1/N within 1.6×; predator 0.18–0.34, completion ≥ 0.85 | **held** |
| A7 | identity ≤ 0.05 (iii); (i) adds −0.01 to +0.04; takeovers ≤ 0.03, late differ < 0.01 | identity level **failed** at 400 and 800 (0.072, 0.125); the rest held except (iv) late takeovers 0.025 at 1,600; falsifier not fired |
| A8 | uot (iii)-S 0.45–0.85, sponsored 0.55–0.95, annealing changes ≤ 0.2 | **held** |
| A9 | island efficiency ≥ 0.9 at 12,000 in every natural cell | **falsifier fired** (0.70–0.78 at N ≤ 400, scramble failures; ≥ 0.985 excluding them) |
| A10 | ≤ 6 natural exploitable rivals per cell at 200, pooled cure ≥ 0.5 | count **held** (1); pooled cure **failed** (5/12) |
| A11 | native r changes uot by < 0.3 | **held** (14 vs 13 of 20) |
