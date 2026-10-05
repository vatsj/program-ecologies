# Predictions: does a co-seeded faker stop establishment? (2026-10-05)

Spec: `specs/2026-10-05-spoiler-conditioned.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-05-spoiler-conditioned-gpt-6.1-sol.md`).
Code: `src/spoiler_conditioned.py`. Committed before any run. Conclusions are finite-cell evidence at n ∈ {6, 9, 12},
N ∈ {100, 400}; nothing here establishes a uniform-in-n discount or a limit.

## Static numbers computed before the run (`runs/spoiler-conditioned-tables.json`)

- Class data: the modal language evaluated once at n = 12 (22,690 canonical functions); n = 6 and 9 are sub-blocks.
  Checked: at n = 6 and 9 the sub-block classes, masses and payoff matrices equal `modal.build(n)` exactly
  (51 and 863 classes; max |Δμ| 2·10⁻¹⁶). n = 12 has 13,514 classes.
- The local kernel (seeds_in_n `_run`, I = 1, m = 0, run on the seed's support plus ALLC and D, with logs that draw no
  random numbers) reproduces `seeds_in_n._run` on the full class set draw for draw (16 of 16 checks, n = 6 and 9).
- Targets (establishers with μ ≥ 10⁻⁴, μ in seeding units, i.e. cutoff-normalized): 8 at every n. FairBot and
  `BOX1(THEM(ME))` have no fakers; `BOX(THEM(THEM))` has none at n = 6 and fakers of mass 3–5·10⁻⁵ at n = 9, 12;
  `BOX1(THEM(THEM))` faker mass 0.0026–0.0031; the probe-readers `BOX(THEM(^C))`, `BOX1(THEM(^C))` 0.003–0.004; the two
  near-universal suckers `not(BOXD(THEM(^C)))`, `not(BOXD1(THEM(^C)))` 0.037–0.047.
- **The faker's play against D** is one of exactly three types in the PD (self-play is CC or DD; D always defects):
  *disadvantaged* (the faker cooperates with D), *neutral* (defects on D and on itself: identical to D inside {faker, D}),
  *advantaged* (defects on D, cooperates with itself: the faker is an establisher). No faker is "mixed". Over all fakers
  of the 8 targets (mass): disadvantaged 0.025 / 0.027 / 0.028, neutral 0.0033 / 0.0044 / 0.0049, advantaged
  0.023 / 0.024 / 0.025 at n = 6 / 9 / 12.
- **Forced pairs** (the 6 heaviest by μ(target)·μ(faker); the same six at every n):
  - `BOX1(THEM(THEM))` ← `not(BOX(THEM(ME)))` and ← `not(BOX(THEM(THEM)))`: **disadvantaged** (the faker self-cooperates,
    cooperates with D, defects on ALLC and on the target);
  - `BOX(THEM(^C))` and `BOX1(THEM(^C))` ← `BOX(THEM(^D))` and ← `BOX1(THEM(^D))`: **neutral** (the probe-fakers;
    cooperate with ALLC, defect on D, on themselves and on the target).
  - Supplement S (predeclared, outside the six, so that the advantaged type is tested): `not(BOXD(THEM(^C)))` ←
    FairBot, the same pair at every n (μ(target) 1.6–2.9·10⁻⁴).

## Operational choices (predeclared)

- *Timing:* one batch with a separate salt (outcomes not inspected): ≤ 3 ms per natural island and ≤ 45 ms per forced
  background (15 runs) at N = 400. **No reduction**: 4,000 natural islands per (n, N) and 1,000 backgrounds per pair,
  (n, N), as specified. Projected total under 30 minutes on 3 workers.
- *Success* (three definitions, reported separately): target survival (a target class in the certified terminal
  support); cooperative fixation (every pair in the terminal support mutually cooperates); efficiency (island
  P(C,C) ≥ 0.95). Islands unresolved at 10⁵ generations are censored (excluded from denominators, counted).
  "Establishment" without qualification means cooperative fixation.
- *Natural targets:* in cell (i) all present establishers; in (ii)–(iv) the present establishers that have a present
  faker. Fakers are resident-specific (fakers of a present establisher).
- *Treatment (c):* the spec's neutral program is "one with the target's own class", which in the class-level simulation
  is k more copies of the target class (target 2k). Because that also changes the target's dosage, I add **(cD)**:
  target + k and k copies of D, which neither exploits nor is exploited by an establisher (mutual defection). "Replacement
  alone" in prediction 4 is judged on (cD); (c) is reported. Treatments share background, replaced slots (target slots
  nested across k) and the simulation seed (common random numbers).
- *Effects:* the forced effect of a faker is reported both as the absolute paired difference (a) − (b) and as the
  relative reduction 1 − P(b)/P(a). Absolute base rates are a few percent, so an absolute threshold of 0.3 is vacuous;
  the 30% / 0.3 / 0.15 thresholds in predictions 1, 2 and 4 are judged on the **relative** reduction (target survival
  and cooperative fixation), with bootstrap intervals over backgrounds.
- *"Fixes"* in prediction 4(d): the faker is in the terminal support (the conservative reading, since a neutral faker
  freezes with D in a payoff-identical mixture); monomorphic fixation is reported too.
- *Mechanism logs:* category counts (target, faker, D, ALLC, other establisher, other) at the island's first ALLC
  extinction (just after the ALLC death) and every 20 generations to resolution. "Faker share falling after ALLC
  extinction while the target's rises" compares the ALLC-extinction snapshot with the first 20-generation row after it.
- *d(n, N)* = P(est | ii) / P(est | i), bootstrap 95% interval (2,000 resamples of islands within cells).
- *Held-out check:* cell probabilities and cell-conditional rates fitted on reps 0–1,999, p predicted for reps
  2,000–3,999. As sol noted, this is close to an identity in expectation; it tests stability, not mechanism.

## RE predictions (Fable, from the spec, unchanged)

1. Co-seeded non-establisher fakers rarely stop establishment, and the effect depends on the faker's play against D.
   Fakers strictly disadvantaged against D lower the target's establishment by less than 30% in the paired forced seeds
   at k = 1 (survival and cooperative fixation both); fakers that tie D are the harmful class and may lower it by more.
   Pooled, d(n, N) ≥ 0.7 at every (n, N), with its bootstrap interval. *Falsifier:* the pooled d's interval entirely
   below 0.5 at any cell.
2. The discount is flat in n, at the pair level. For each (target, faker) pair present at all three n, the paired
   forced-seed effect at k = 1 changes by less than 0.15 (absolute) from n = 6 to n = 12. *Falsifier:* a pair whose
   effect grows by more than 0.3 from n = 6 to 12.
3. Establisher-fakers leave a cooperative island. In cell (iii), cooperative fixation is at least 0.8 of cell (i)'s,
   even where target survival is lower; the winner is some establisher. *Falsifier:* cooperative fixation in (iii)
   below 0.6 of (i).
4. Forced seeds, the mechanism, at N = 400, k = 1: (a) − (b) below 0.3 for every pair whose faker is strictly
   disadvantaged against D; (a) − (c) within ±0.05; (d) alone never fixes a non-establisher faker in more than 5% of
   islands; the faker's share falls after ALLC extinction while the target's rises in at least 70% of (b) islands where
   the target survives. *Falsifier:* a strictly-D-disadvantaged non-establisher faker winning more than 10% of (b)
   islands at N = 400, k = 1.
5. The combined bound, held out: p = P(A)·Σ P(cell | A)·P(est | cell) (+ the no-A term), fitted on the first 2,000
   natural islands, predicts the second 2,000 within 15% at every (n, N). *Falsifier:* disagreement above 30%.

## Subagent predictions (mine, made before the run)

- **S1. The probe-fakers (neutral pairs) are strongly harmful.** In {target x, faker φ, D} after ALLC is gone, the
  payoff table gives f_φ − f_x = x + φ > 0 and f_x − f_D = x − φ: the faker beats the target whenever both are present
  and cancels the target's advantage over D. Forced, k = 1, N = 400: relative reduction of target survival ≥ 0.5 for all
  four neutral pairs. *Falsifier:* < 0.3 for any of them. (This is the RE's "may lower it by more", made quantitative;
  if it holds, prediction 4's mechanism clause will fail for these pairs, since the faker's share does not fall.)
- **S2. Disadvantaged fakers are eaten with ALLC.** Forced, k = 1: relative reduction < 0.15 for both disadvantaged pairs
  at both N; in natural cell (ii) islands whose fakers are all disadvantaged, the faker is extinct by the island's
  ALLC extinction in ≥ 80% of islands.
- **S3. Composition of cell (ii).** Most cell-(ii) islands carry only disadvantaged fakers (by faker mass), so the pooled
  d is ≥ 0.8 at N = 100 and lower at N = 400 than at N = 100 (more probe-faker copies per seed at larger N).
- **S4. Dosage.** For neutral pairs the relative reduction grows with k (k = 10 at N = 400 ≥ 0.8); for disadvantaged pairs
  it stays below 0.3 at k = 10.
- **S5. Held-out check.** Within 15% at both N = 400 cells at every n; at most one N = 100 cell misses 15% (sampling
  noise of ~10% on the held-out difference); the falsifier (> 30%) does not fire.
- **S6. Supplement S** (`not(BOXD(THEM(^C)))` ← FairBot): (b) raises cooperative fixation above (a) (the faker is a
  stronger establisher than the sucker target), while target survival falls.
