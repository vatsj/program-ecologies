# Predictions: majority division in the current object (queue 74), 2026-11-07

Spec: `specs/2026-11-07-majority-current-object.md` (reviewed by gemini-4-argon and gpt-6.1-sol, folded). Committed before
any counted cell is run. Verdicts are written into `runs/majority-current-object.md` against the rules below.

## Pilot runs made before this file (disclosure)

All pilots used the new code on founders and schedule of run index 0 only, at Lambda = 100, mN = 1, to time the kernel:

- arm M, N = 100, r = 0: every one of the 64 islands on fair pair F0 at 120N (V* share 1.0; snapshot at 2N: 36 F, 22 U, 4 W, 2 D of 64).
- arm M, N = 400, r = 0: all 64 islands on one unequal pair at 120N (V* share 0.0), kernel 128 s, closure at 39,760.
- arm T, N = 100, r = 0: all 64 islands on fair pair F1 at 120N (V* share 1.0).

A pipeline test ran all nine main-grid cells of arm M, N = 100, r = 0 as one job (`one M:main:100:0`); only the
schema of the rows and their wall times were read, no outcome value. No other counted-cell quantity was looked at.
Unit tests (two failed attempts at the arrival-law test's pooling rule and at the D4 matched-mass tolerance, both test
artefacts: expected counts below 5, class granularity) were run before. Validations V1-V6 all passed locally before any
counted cell (V1: 240 of 240 stored rows and kern_mw modal series reproduced exactly; V2 chi-squared p = 0.16 / 0.31, delivered
count within 0.4% of Lambda; V3, V4, V5, V6 pass; results in `runs/majority_tail/validation.json`); V1 is also run in the pinned
sandbox environment (numpy 1.24.3, numba 0.57.0), reported in `runs/majority_tail_sbx/`.

## The spec's predictions, verbatim

"Lands in V\*" for an arm and cell means V\* share ≥ 0.95 at 120N with the lower bootstrap bound ≥ 0.90.

- **RE 1 (the recorded arm-T prediction).** T at mN = 1, Λ = 10 and 100: V\* share ≥ 0.9 at N = 100 and at N = 200.
  Falsifier: mean < 0.9 in any of those four cells.
- **RE 2 (T at N = 400; recorded as unresolved, sharpened here).** T at mN = 1, N = 400, Λ = 10: V\* share ≥ 0.8.
  Falsifier: < 0.8.
- **RE 3 (the recorded DSL prediction, with the RS's).** M does not land in V\* at mN = 1 for any N and Λ, and its V\*
  share at N = 400 is below 0.5 with U the modal class. Falsifier: M lands in V\* in any mN = 1 cell, or V\* ≥ 0.5 at
  N = 400 (any Λ).
- **RE 4 (the prior's tail does not help M).** At mN = 1, V\*(Λ = 100) − V\*(Λ = 0) ≤ +0.05 for M at every N.
  Falsifier: a paired contrast > +0.10 with its interval excluding 0 at any N.
- **RE 5 (the tail cleans waste without migration).** At mN = 0, N = 100, the W share at 120N is lower at Λ = 100 than
  at Λ = 0 by ≥ 0.10 in both M and T (a wasteful island leaves by one selected step, a slot raising its demand, which
  arrivals supply). Falsifier: a reduction < 0.05 in either arm.
- **RE 6 (no arm lands without migration).** At mN = 0, no arm reaches V\* share ≥ 0.6 at any N and Λ ≤ 100 (unequal
  and disagreement islands persist in isolation). Falsifier: any mN = 0 cell ≥ 0.6.
- **RE 7 (equal likelihood across worlds in T).** [after review: one Λ only, since CRN founders make runs with the same
  index correlated across Λ] In T's mN = 1, Λ = 100 cell at each N, fair-consensus runs are spread over the three pairs
  uniformly (χ² p > 0.01). Falsifier: p < 0.01 at any N with ≥ 20 consensus runs; unscored at an N with fewer. Counts
  pooled over Λ are reported, not tested.
- **RE 8 (D1, diagnostic).** The clean tail raises M's V\* share at N = 100, mN = 1 by ≥ 0.15 over the full tail at the
  same Λ = 100. Falsifier: < 0.05. (If it holds, the mean-field finding of queue 71 survives finite N and I; if not, the
  finite-I migration consolidation dominates the tail's composition.) [after review] **RE 8b:** the same at N = 200, where
  M's tail-free baseline is expected to sit on U: a rise ≥ 0.15; falsifier < 0.05.
- **gemini-4-argon's counter (recorded, scored):** RE 8 fails (gain < 0.10), and fails at N = 200, because migration at
  mN = 1 consolidates the founding unequal convention by 10N–20N and over half of the tail's arrivals come later. (RE note: with t₀ = N/2 the share of Λ delivered by g − g₀ = 8N is 1 − 1/17 ≈ 0.94, so most arrivals
  come before 10N; the counter is scored as stated.) [after second review] Its timing mechanism is **refuted
  analytically before the run** (about 3% of delivered arrivals come after 15N); only its numerical outcome is scored.
- **gpt-6.1-sol's counters (recorded, scored):** (i) RE 8b fails: the clean tail's gain decreases with N and Λ = 100 is
  not enough at N = 200 (scored: gain at N = 200 < gain at N = 100, and < 0.05). (ii) RE 5's common bound fails in at
  least one arm (scored: reduction < 0.10 in M or in T).

The RS's recorded prediction is scored per arm: it holds for an arm if the arm does not land in V\* in the mN = 1, Λ > 0
cells at the largest N run, and fails for an arm that lands there.

## The engineer's own predictions (made after the three pilots above; E-numbers)

- **E1 (M's N-dependence at mN = 1).** M's V* share at mN = 1, Lambda = 100 falls with N: mean(100) > mean(200) > mean(400),
  with mean(400) < mean(100) - 0.3 (pilots: r = 0 fair at 100, unequal at 400; queue 31 put the fair/unequal crossover of
  migration's consensus between 150 and 200). Falsifier: the means are not strictly ordered, or the drop from 100 to 400 is
  under 0.3.
- **E2 (the validation gates).** V1 reproduces all 240 stored (arm x mN x run) rows and the kern_mw modal series exactly.
  Falsifier: any mismatch (which stops the cells the gate covers).
- **E3 (cost).** The whole counted grid runs in under 100 sandbox-CPU-hours with no cuts. Falsifier: more than 100, or any cut applied.
- **E4 (readers in T).** At mN = 1, Lambda = 100, N = 400, the number of runs in unequal consensus (>= 0.99 of islands on one unequal
  outcome at 120N) is at least 2 larger in T0 (constants only) than in T. Falsifier: T0 - T <= 1.
- **E5 (D4 vs D2).** At mN = 1, Lambda = 100, N = 200, D2's V* share exceeds the main cell's by at least 0.10 more than the mean of
  the three D4 draws' shares does (D4 mean gain smaller than D2 gain by >= 0.10). Falsifier: D2 gain - mean D4 gain < 0.10.
- **E6 (the tail changes M at N = 100, mN = 1).** The pilot cell is already at V* = 1.0; the tail-free baseline (queue 64) is 0.70 at generation
  10,000, so at N = 100, mN = 1, M's paired contrast V*(Lambda = 100) - V*(Lambda = 0) at 120N is > +0.10 with its interval excluding 0.
  Falsifier: contrast <= +0.10 or interval includes 0. (This is a prediction against RE 4's spirit at N = 100 only; RE 4 stays scored as written at every N.)
