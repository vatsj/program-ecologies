# Predictions: the seed lottery's tail in n (static) and island merging at I = 4 (2026-10-05)

Spec `specs/2026-10-05-seeds-tail.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-05-seeds-tail-gpt-6.1-sol.md`).
Committed before any static computation beyond the class counts published for n ≤ 9 and before any run. Code to come:
`src/seeds_tail.py` (static Part A and the Part B driver with its event-logging kernel).

## Units, fixed before computing (a correction to the spec's wording)

The length prior gives each program of size s the weight 1/(2·a(s)·s²), so shell s carries raw mass 1/(2s²) and the
infinite prior has total raw mass Σ_s 1/(2s²) = π²/12 ≈ 0.822, **not 1**. The spec's "retained mass → 1" is therefore
off by a constant: the retained raw mass at cutoff n is 0.746 (n = 6), 0.770 (9), 0.782 (12), and tends to 0.822. The
published masses (μ(ALLC) 0.469, μ_est 0.0229 → 0.0246) are *cutoff-normalized* (divided by the retained mass). Three
units are reported side by side for every mass:
- **raw**: unnormalized, shell mass 1/(2s²); the spec's bound is in these units: raw(∞) ≤ raw(n) + ω(n) with the
  omitted mass ω(n) = π²/12 − Σ_{s≤n} 1/(2s²) < 1/(2n), computed exactly;
- **infinite-normalized**: raw / (π²/12), a probability under the fixed infinite prior; its limit equals the limit
  of the cutoff-normalized mass;
- **cutoff-normalized**: raw / retained(n), the seeding law actually used by the islands.

Verdict rules fixed now:
- Prediction 1's numeric range μ_est(12) ∈ [0.024, 0.028] is evaluated in **cutoff-normalized** units, the units of the
  published 0.0229–0.0246 from which the range was evidently set. Raw values are also reported; in raw units the range
  would be a unit error, not a test.
- "Converges to a limit below 0.03" is evaluated in infinite-normalized units: **held** only if the rigorous upper
  bound (raw(12) + ω(12))/(π²/12) is below 0.03; **inconclusive (consistent)** if the bound is not below 0.03 but the
  1/s²-tail extrapolation (mean shell fraction over s = 10–12 times ω(12), added to raw(12)) is; **failed** if the lower
  bound raw(12)/(π²/12) already exceeds 0.03 or the extrapolation does.
- The shell fraction f(s) = (raw μ_est from programs of size s) / (1/(2s²)) is unit-free. Shells 1–2 contain no
  self-cooperator by construction (f = 0), so the ±50% clause and the falsifier are evaluated over **s = 6–12** (the
  spec's cutoff range); f(3)–f(5) are reported, and if the falsifier would fire there on a literal reading, that is
  stated beside the verdict.
- The μ ≥ 10⁻⁴ threshold in Part A item 4 is applied to the **raw** class mass.
- Reclassification: class identity across n is tracked at the level of canonical boolean functions over box atoms,
  whose ids are stable across cutoffs (checked); a canonical function present at n − 1 keeps its program counts in
  shells ≤ n − 1. D-entering self-cooperation is a property of self-play and play against D, so its reclassified mass
  must be exactly 0 (checked, not assumed). Fakeability (some class q with U(q, x) > U(x, x)) can switch from false to
  true when shell n adds an opponent; the mass so reclassified is reported per step, separately from the new shell's
  mass. Probe-faker status can likewise switch on for old syntax when a new establisher appears.

## Definitions

- *D-entering self-cooperator (establisher):* a behavioural class x ≠ ALLC with x playing C against itself and D
  against D (in the PD this is exactly "self-cooperating and defects on D"; every such x has the same 2×2 game against
  D, so the same ρ(x | all-D)).
- *Probe-faker μ_pf(n):* the mass of the union over establishers x of {q : U(q, x) > U(x, x)}, i.e. q defects on x
  while x cooperates with q. Reported both as the global union and per establisher. r(n) = μ_pf(n)/μ_est(n).
- *Unfakeable core:* self-cooperators x ≠ ALLC with no q in L_n having U(q, x) > U(x, x) (as `almost_all_seeds`).
- *Co-seeding (item 5):* per n, 10⁵ iid seeds of N = 100 from the cutoff-normalized prior (seeded RNG); A = at least
  one establisher present; K_pf = number of seed members (with multiplicity) that are fakers of at least one
  establisher present in that seed. Reported: P(A), E[K_pf | A], P(K_pf > 0 | A), with binomial standard errors.
- *Establishment-weighted mass (item 6):* Σ_x μ(x)·ρ(x | all-D, N) over establishers, with ρ = `chain.fixation` at
  w = 0.3 (the single-copy fixation probability, which gave 0.0421 at N = 100), at N = 100, 400, 1,600; also over all
  self-cooperators, for comparison.
- *Part B run-level efficient:* the run is certified (outcome-frozen or separated under migration; all islands locally
  frozen without migration) and the mean island P(C,C) ≥ 0.95, as in `seeds_in_n`. Runs that reach 10⁵ generations
  uncertified are *dynamically unresolved* and counted as not efficient in the fraction, reported separately;
  anything stopped for time is *administratively censored*, reported separately and excluded.
- *Part B cells:* n = 6, I = 4, N = 400 per island, mN ∈ {0.1, 1, 10}, 60 runs each; reference (i) no migration,
  (400, 4), 100 runs (400 islands; run-level efficiency = all four efficient; p(400) per island); reference (ii) one
  island of N = 1,600, mN = 0, 240 runs. Fresh seeds: a salt distinct from every earlier seeds run, so no earlier run
  is replayed. Horizon 10⁵ generations everywhere.
- *Event logs:* the kernel is `seeds_in_n._run` plus counters that consume no random numbers (checked draw for draw
  against `seeds_in_n._run`). Windows: W1 = before the first certified cooperative island, W2 = from it to resolution.
  Per window: migrant births by category of the migrant's class (establisher, probe-faker, D, ALLC, other
  self-cooperator, other) and by target state (target island ≥ 90% self-cooperators or not); introductions (a migrant
  of a class absent on the target island). Per island: first time ≥ 90% self-cooperators, first certified time,
  composition at first certification, and whether its largest cooperative class at that time was in the island's own
  seed (*local nucleation*) or arrived by migration (*import*). Losses with taker identities as in `seeds_in_n`.
  Founder = largest class of the first certified island; terminal support = classes present at the end.
- *Contrast:* fraction(mN = 0.1) − fraction(mN = 10), 95% Newcombe hybrid-score interval (Wilson-based, method 10).
  Single fractions: Wilson 95%.
- Outcome of a prediction: **held** if the claimed quantity's interval lies inside the claim, **failed** if it lies
  outside or a falsifier fires, **inconclusive** if intervals straddle a boundary. Static quantities are exact (no
  interval) except the co-seeding Monte Carlo, whose standard error is reported.

## Cutoff range and budget

n = 6 … 12 for the static table, with n = 12 evaluated once and the smaller cutoffs taken as sub-blocks (checked
against a direct evaluation at n = 9). n = 13 only if n = 12 finishes well inside the budget and memory allows
(2.7 GB before, with sibling pools running). Anything projected beyond about 2 hours is stopped and reported as
administratively censored.

## RE predictions (Fable), carried verbatim from the spec

1. **μ_est(n) converges to a limit below 0.03, with a 1/s² shell tail.** The shell contribution to μ_est is a roughly
   constant fraction (0.03–0.06) of the shell's own mass 1/(2s²), so successive ratios are (s/(s+1))² ≈ 0.75–0.85,
   not geometric, and μ_est(12) + 1/24 bounds the limit; the prediction is μ_est(12) ∈ [0.024, 0.028] and the shell
   fraction within ±50% of its s = 6 value at every s ≤ 12. *Falsifier:* the shell fraction of D-entering
   self-cooperators rising above 0.1 or falling below 0.01 at any s ≤ 12.
2. **Probe-faker mass grows but stays small:** μ_pf(n) ≤ 0.006 at n = 12 and r(n) ≤ 0.25 at every n; conditional on
   an establisher being seeded, E[K_pf | A] < 0.5 and P(K_pf > 0 | A) < 0.35 at N = 100 for every n ≤ 12, with the
   resident-specific count. *Falsifier:* r(12) > 0.4 or P(K_pf > 0 | A) > 0.5. Sol's theorem target, a
   resident-conditioned spoiler bound uniform in the cutoff plus a founder-establishment lower bound, is what 2 and 6
   measure the ingredients of; the spec does not claim the bound.
3. **FairBot and `BOX1(THEM(ME))` stay unfakeable at every n ≤ 12.** *Falsifier:* a strict invader of either. Such a
   finding is first a check of the evaluator's semantics and of the outcome-symmetry argument, and only then a
   soundness question.
4. **Merging at I = 4.** The run-level efficient fraction is 0.50 ± 0.15 at mN = 0.1, 0.42 ± 0.12 at mN = 1, and
   0.38 ± 0.12 at mN = 10, and the mN = 0.1 minus mN = 10 contrast is positive with a 95% interval excluding 0. Sol
   notes an intermediate maximum is plausible; the event logs decide which timescale wins. *Falsifier:* the contrast's
   interval entirely below 0.

μ_pf in prediction 2 is evaluated in cutoff-normalized units (the units of the published 0.0030–0.0036), on the
global union as defined above; the per-establisher maximum is reported beside it.

## Subagent's own predictions (Opus RE), made before computing

- **S1 (the global faker union is larger than the published per-prover figure).** The published 0.0030–0.0036 is the
  faker mass of one prover, `BOX(THEM(^C))`. The union over all fakeable establishers is larger and rises with n:
  μ_pf(12) in [0.006, 0.02] (cutoff-normalized) and r(12) in [0.2, 0.6], so RE 2's static bounds (≤ 0.006, ≤ 0.25)
  are at risk while its falsifier (r(12) > 0.4) may or may not fire.
- **S2 (resident-conditioned co-seeding stays moderate).** Because the two heaviest establishers (FairBot,
  `BOX1(THEM(ME))`) are unfakeable, conditioning on the residents present cuts the faker exposure well below N·μ_pf:
  P(K_pf > 0 | A) in [0.15, 0.45] at every n ≤ 12, rising by less than 0.1 from n = 6 to 12.
- **S3 (establishment-weighted mass is μ_est times a constant).** Every establisher has the same 2×2 game against D,
  so Σ μ ρ = ρ(N)·μ_est exactly at every N; the item-6 column carries no new information beyond ρ(N) ∝ N^(−1/2)
  (ρ(400)/ρ(100) within 0.45–0.55).
- **S4 (Part B: contrast positive, not resolved).** Point estimates: mN = 0.1 in [0.38, 0.6], mN = 10 in [0.28, 0.48];
  the contrast's point estimate is positive but its 95% interval includes 0 (60 runs per arm resolve about ±0.17).
  At mN = 10 the first certified island coincides with resolution in most runs (islands do not freeze separately), and
  at mN = 0.1 at least half the efficient runs have two or more islands with local nucleation.
- **S5 (references reproduce).** p(400) re-measured within the published interval around 0.158 (Wilson on 400
  islands overlapping [0.12, 0.20]); the one-island N = 1,600 efficient fraction overlaps 0.383's interval
  [0.34, 0.43].
