# Predictions: annealed mutation (a decaying re-injection schedule along Λ_N → 0, N·Λ_N fixed at the curing exposure), 2026-10-16

Spec `specs/2026-10-16-annealed-mutation.md` (reviewed by gpt-6.1-sol and gemini-4-argon; the amendments supersede the
earlier text). Notes `notes/annealed.md` §1 (committed before any code). Written and committed before any code and
before any counted cell. Cells with re-injection are finite-ε approach-rate diagnostics at finite (N, I, horizon), never
π; ε = 0 cells are lottery statistics. The scaling claims are finite-size diagnostics over N = 200–1,600 at I = 8.

## The RS's statements (verbatim, registered first)

> I propose a model where mutation rate decreases over time. It starts at infinity, which generates the random
> seed, but the tail is light enough that islands can't drift (but heavy enough to prey on inefficiencies).

> drift should never colonize an island, only reintroduce fit programs.

**Scoring (declared now).** Drift and colonization as in notes §1.4 (a rain lineage holding ≥ 0.5 of an island at a
5-generation checkpoint; drift = neutral or deleterious against the island's majority at arrival). Exploitable rivals
and cures as in notes §1.5–1.6 and removing-rivals §1.6.
- *Statement 2 ("never colonize")* is read per run and per cell, on arm (i): it **holds at N** if every run of the cell
  is drift-free; it **holds in the limit** if the drift-free fraction of runs rises with N and reaches ≥ 0.9 at
  N = 1,600 (Wilson lower bound ≥ 0.7); it **fails** at N if the cell has any drift colonization.
- *Statement 1 ("can't drift but heavy enough to prey")* is the conjunction, at N = 1,600: drift-free runs ≥ 0.9 of the
  arm (i) cell **and** cure ≥ 0.8 of eligible exploitable rivals. Scored separately for the anti-punisher (AP) and
  detector (DET) classes of Part F, and for the natural mix (0.52 AP, 0.48 DET, the Part 0 proportions). *Supported*
  if both clauses hold for the natural mix; *contradicted* if drift-free < 0.7 or the mixed cure ≤ 0.5;
  *inconclusive* otherwise.

## The RE's predictions (verbatim from the spec, with the revision and withdrawal marks)

1. **Drift scales away along the path** [revised: on the amended path the expected slope is −1]: drift colonizations per island fall as N^(−1/2) within a factor 2 from
   N = 200 to 800, and the fraction of runs with zero drift colonizations rises with N. *Falsifier:* no decrease.
2. ~~Cures scale up to ≥ 0.8 at N = 800, Λ₀ = 0.03~~ [withdrawn after review by both: N·Λ_N = 12 arrivals per island
   needs predator mass ≥ 0.52 for a 0.8 cure, against ≈ 0.075]. **Revised (on the amended path):** with N·Λ_N held at
   K/(ρ·μ_pred) arrivals per island, the cure of exploitable rivals is ≥ 0.8 at every N. *Falsifier:* ≤ 0.5 at any N.
3. **The RS's criterion holds at the largest cell in a majority of runs** [revised: on the amended path]: no
   post-establishment drift colonization in ≥ 0.5 of runs at N = 1,600, with cures ≥ 0.8 there (uncertain).
   *Falsifier:* ≤ 0.2 of runs drift-free at N = 1,600.
4. **Annealing does not remove identity:** identity islands under (i) are ≥ the ε = 0 baseline's at every N;
   annealing plus sponsorship leaves uot below 0.85 at every N. *Falsifier:* uot ≥ 0.9 anywhere.
5. ~~Only Λ matters~~ [withdrawn after review by both: shadows take O(N) generations to form, so a front-loaded
   schedule meets fewer of them]. **Revised:** the schedule's shape matters for identity: constant rain gives more late
   identity takeovers of target islands than annealing at N ≥ 400, while drift colonization per island is equal within
   an equivalence margin of ±30% at matched total arrivals. *Falsifier:* identity takeovers equal within ±0.01 per
   island, or drift outside the margin.
6. **Counter-predictions registered.** *Gemini:* constant rain produces significantly more secondary takeovers of
   target shadows, and more late identity takeovers, than annealing at N ≥ 400; on the original path the cure of
   non-shadow exploitable rivals is < 0.5. *Sol:* outcomes are schedule-dependent in a direction not predictable
   before measuring state-conditioned hazards; identity effects are heterogeneous across founder regimes, not
   monotone in N.

Amendment 6 (verbatim): "the scaling claim is a finite-size diagnostic over 200–1,600 at I = 8, judged by the log-log
slope of drift per island against N (prediction 1: slope in [−1.3, −0.7])."

### Outcome regions for the RE's predictions and the counter-predictions (declared now, before any cell)

Slopes are Poisson-regression slopes of per-run drift counts on log N with a 95% run-bootstrap interval; arm (i) is
primary.
- **RE 1.** *Supported:* slope point estimate in [−1.3, −0.7] and drift-free fraction non-decreasing in N (one
  inversion within one run allowed). *Contradicted:* slope interval includes 0 or point ≥ −0.3 (no decrease), or the
  drift-free fraction at 1,600 below that at 200. *Inconclusive:* a decrease outside [−1.3, −0.7] (reported as "the
  amended slope missed") with the interval excluding 0.
- **RE 2.** Primary: Part F natural-mix cure per N (0.52·AP + 0.48·DET, cure = X island a target island at 12,000 for
  ≥ 25 generations). *Supported:* ≥ 0.8 at every N; *contradicted:* ≤ 0.5 at any N; *inconclusive:* otherwise. Also
  reported per class (AP, DET) with the same thresholds, and for natural exploitable rivals pooled over arms (i), (ii),
  (iv) and N (eligible at generation 200; too few for per-N verdicts).
- **RE 3.** *Supported:* arm (i) at N = 1,600 drift-free ≥ 0.5 of runs and the natural-mix Part F cure ≥ 0.8 at
  1,600; *contradicted:* drift-free ≤ 0.2; *inconclusive:* otherwise (including drift-free ≥ 0.5 with cure < 0.8,
  scored "drift clause held, cure clause failed").
- **RE 4.** Identity clause: identity islands per island at 12,000, (i) minus (iii) S-nonself, paired by replicate.
  *Supported:* difference ≥ 0 at every N; *contradicted:* < 0 at some N with the run-bootstrap interval excluding 0;
  *inconclusive:* a negative point estimate whose interval includes 0. uot clause: arm (ii) uot at 12,000.
  *Supported:* < 0.85 at every N; *contradicted (the falsifier):* ≥ 0.9 at some N; *inconclusive:* in [0.85, 0.9).
- **RE 5.** Identity takeovers of target islands per island, late (start ≥ 2,000), arms (iv) and (i), at N = 400, 800,
  1,600. Drift clause: ratio of drift colonizations per island (i)/(iv) at each N. *Supported:* (iv) − (i) ≥ +0.01 per
  island at every N ≥ 400 and the drift ratio in [0.7, 1.3] at every N ≥ 400; *contradicted (the falsifier):*
  |(iv) − (i)| < 0.01 at every N ≥ 400, or the drift ratio outside [0.7, 1.3] at some N ≥ 400; *inconclusive:*
  otherwise. The N = 200 drift ratio is reported beside it.
- **Gemini.** First clause: secondary takeovers of shadows and late identity takeovers, (iv) minus (i), pooled over
  N ≥ 400, paired by replicate; *held* if both are positive with run-bootstrap intervals excluding 0; *failed* if
  either point estimate ≤ 0; *inconclusive* otherwise. Second clause (original path, Λ₀ ∈ {0.01, 0.03}, i.e. 2–12
  arrivals per island): not run as cells; scored from the Part F AP and DET hazards (−ln(1 − cure)/arrivals, pooled
  over N) applied to 12 arrivals: *held* if the natural-mix extrapolated cure < 0.5.
- **Sol.** First clause *held* if any of drift per island, identity islands, uot or exploitable cure differs between
  (i) and (iv) at some N with a run-bootstrap interval excluding 0; second clause *held* if the identity effect
  ((i) − (iii), per island) is not monotone in N across the four N, or changes sign between S-nonself and sponsored
  founders.

## My predictions (with falsifiers and outcome regions)

A1. **Drift per island falls with N, more slowly under annealing than under constant rain.** Arm (i): drift
    colonizations per island over the run ≈ 0.08 / 0.05 / 0.03 / 0.015 at N = 200 / 400 / 800 / 1,600 (each within a
    factor 2.5), slope in [−1.1, −0.55] (point −0.8). Arm (iv): slope in [−1.3, −0.75] (point −1.0). *Falsifier:*
    arm (i) slope > −0.4 or < −1.4. *Inconclusive:* the slope interval wider than 1.2 (too few events).

A2. **Annealing beats constant rain on drift at small N, not at large N.** Ratio of drift per island (i)/(iv): in
    [0.3, 0.85] at N = 200 (the annealed schedule's early high rates suppress per-arrival lineage colonization), in
    [0.6, 1.3] at N = 1,600. *Falsifier:* ratio ≥ 1 at N = 200.

A3. **The RS's criterion per run.** Arm (i) drift-free runs ≈ 0.5 / 0.65 / 0.8 / 0.9 (each ± 0.2) at N = 200 / 400 /
    800 / 1,600; at least one drift colonization in every arm-(i) cell at N ≤ 800 (so "never" fails as a cell
    statement there); drift-free ≥ 0.75 at 1,600. *Falsifier:* drift-free < 0.5 at N = 1,600, or every run drift-free
    at N ≤ 400.

A4. **Most drift colonizations are shadows on target islands** (≥ 0.7 of drift colonizations had status target at
    arrival, in every rain cell with ≥ 5 drift colonizations), and most are later reversed or neutral: ≥ 0.5 of
    colonizing drift lineages do not hold the island at 12,000. *Falsifier:* shadow share < 0.5.

A5. **Cures in Part F are N-independent and class-split.** Annealed K = 3: AP cure ≥ 0.9 at every N; DET cure in
    [0.15, 0.6] at every N; neither class shows a monotone change > 0.25 from N = 200 to 1,600. K = 1: AP in
    [0.5, 0.9], DET ≤ 0.3. So RE 2 is supported for AP, contradicted for DET, and the natural mix is inconclusive
    (0.55–0.8). *Falsifier:* AP < 0.8 at some N, or DET ≥ 0.8 at some N, or a monotone trend > 0.25 in either class.

A6. **Single-arrival assays.** `C` into a FairBot island colonizes with probability within a factor 1.6 of 2/N and fixes
    within a factor 1.6 of 1/N at every N; the top predator of each class establishes with probability in [0.18, 0.34]
    at every N, and completes (island returned to target) in ≥ 0.85 of establishments within 400 generations. *Falsifier:*
    neutral colonization outside a factor 2.5 of 2/N at any N, or predator establishment trending with N by > 0.1.

A7. **Identity.** Identity islands per island at 12,000 under (iii) S-nonself are ≤ 0.05 at every N; arm (i) adds
    between −0.01 and +0.04 per island (rain feeds identity through shadows, but at I = 8 the migrant supply is small);
    identity takeovers of target islands are ≤ 0.03 per island in every rain cell, and late ones (≥ 2,000) ≤ 0.02 in
    both (i) and (iv), differing by < 0.01 at every N ≥ 400 (so RE 5's falsifier fires). *Falsifier:* takeovers
    ≥ 0.05 per island in some rain cell, or (iv) − (i) ≥ 0.02 at two N.

A8. **uot at I = 8.** (iii) S-nonself 0.45–0.85; (iii) sponsored ≥ (iii) S-nonself − 0.1 at every N and 0.55–0.95;
    annealing changes uot by ≤ 0.2 against the paired ε = 0 runs in each rule (it cures the rare exploitable rival
    and feeds the rare identity takeover). RE 4's uot falsifier (≥ 0.9 in arm (ii) somewhere) fires with probability
    about one half; my point estimate for arm (ii) is 0.7–0.85. *Falsifier:* a change ≥ 0.3 between annealed and
    ε = 0 in any cell.

A9. **Island efficiency** (P(C,C) ≥ 0.95) holds on ≥ 0.9 of islands at 12,000 in every natural cell, and the chase
    raises it relative to generation 10,000 by ≤ 0.03 in annealed cells (the tail at 10,000 is already near zero).
    *Falsifier:* < 0.85 in any cell.

A10. **Natural exploitable rivals** eligible at generation 200 number ≤ 6 per arm-(i) cell at N = 200 and ≤ 2 at
    N ≥ 800, and their pooled cure (arms (i), (ii), (iv), all N) is ≥ 0.5. *Falsifier:* ≥ 15 eligible in one cell (the
    Part F addition was unnecessary).

A11. **Fixing r changes nothing material.** If the native-r (400, 8) ε = 0 cell is run: uot, identity islands and
    held islands within the run-level interval of the r = 100 cell. *Falsifier:* uot differs by ≥ 0.3.
