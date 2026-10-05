# Spec: the seed lottery's tail in n (static) and island merging at I = 4, 2026-10-05

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-05-seeds-tail-gpt-6.1-sol.md`) and revised; changes marked [after review]. Committed before launch. To be run by an Opus subagent.

## Why

RESULTS "Almost all seeds: cutoff sensitivity in n" found the per-island chance flat at n = 6–9 and tracking μ_est(n),
the prior mass of self-cooperating classes that defect on D, not the unfakeable core. Uniformity in n therefore reduces
to two static questions about the prior as the cutoff grows, plus one small dynamical check that the review of that
spec raised.

## Part A: static tail (no runs)

[after review] **The prior is fixed and infinite.** The length prior gives length shell s total mass 1/(2s²) (as the
Conjecture 4 run established), split equally among the programs of that size, so the cutoff at n *retains*
Σ_{s≤n} 1/(2s²) and *omits* Σ_{s>n} 1/(2s²) < 1/(2n). All masses below are reported *raw* (unnormalized, under the
infinite prior) and the omitted mass is reported next to them, so every limit claim carries an explicit bound:
μ_est(∞) ≤ μ_est(n) + 1/(2n). Seeding at cutoff n draws from the renormalized prior; since the retained mass → 1, that
distinction vanishes in n and is noted, not corrected for. Reclassification is tracked separately from new syntax:
self-cooperation and defection on D are properties of a class's play against itself and against D, unchanged by
adding opponents (classes may split; their members keep both properties), so the raw μ_est is non-decreasing by
construction; what can change with n is *fakeability*, so the fakeable/unfakeable split is reported with the
reclassified mass at each step.

Over the modal arm at n = 6 … 12 (as far as `src/moat_static_big.py`'s enumeration allows within about an hour on 3
cores; n = 13 took 388 s and 2.7 GB there), compute per n:
1. μ_est(n): the prior mass of self-cooperating classes that defect on D (the lottery's establishment term).
2. μ_pf(n): the prior mass of *probe-fakers*, classes that strictly invade some D-entering self-cooperator's
   monomorphic world (these are the only spoilers the lottery saw).
3. The shell decomposition: the contribution of each length shell s ≤ n to μ_est and μ_pf, so monotonicity and
   convergence can be read off directly.
4. For each D-entering self-cooperator with μ ≥ 10⁻⁴: its establishment probability ρ(x | all-D) at N = 100, its
   fakers' total mass, and whether it is in the unfakeable core.
5. The ratio r(n) = μ_pf(n)/μ_est(n). [after review] Co-seeding, *conditioned correctly*: by drawing 10⁵ iid seeds of
   N = 100 per n and conditioning on the event A that the seed contains at least one D-entering self-cooperator,
   report E[K_pf | A] and P(K_pf > 0 | A), where K_pf counts fakers *of the specific establishers present* (resident-
   specific spoiler sets, not the global union).
6. [after review] The establishment-weighted mass Σ_x μ(x)·ρ(x | all-D) at N = 100, 400 and 1,600, next to the raw
   μ_est, since ρ differs across establishers only through their self-play and play against D.

## Part B: island merging at I = 4 (small ABM)

`src/seeds_in_n.py`, modal n = 6, four islands of N = 400 *each*, mN ∈ {0.1, 1, 10} migrants per island per
generation, 60 runs each [after review: raised from 40], horizon 10⁵ generations, certification as in the seeds runs,
censoring reported. [after review] **Benchmarks, with the events named.** "Efficient fraction" is *run-level*: the
whole metapopulation certified efficient. Two references, rerun with the same horizon and pipeline: (i) no migration,
where run-level efficiency is all four islands succeeding, ≈ p⁴, and the per-island rate p(400) is re-measured (0.158
before); (ii) a well-mixed control, one island of N = 1,600, whose efficient fraction is the "four islands as one"
benchmark (0.383 before, re-measured). The independent-trials benchmark 1 − (1 − p)^4 ≈ 0.50 assumes nucleation on at
least one island followed by spread within the horizon. Global P(C,C) is reported beside the run-level fraction.
Migration events are logged in two windows, before the first certified cooperative island and between it and
resolution, with founder and spoiler identities, island compositions, nucleation times and terminal support, so
"merging" is identified by the event counts, not by mN alone. The predeclared contrast is the difference between the
mN = 0.1 and mN = 10 fractions, with its 95% interval (60 runs each resolve a difference of about 0.17).

## RE predictions (Fable)

1. **μ_est(n) converges to a limit below 0.03, with a 1/s² shell tail** [after review: monotonicity is by
   construction, so it is not a prediction; geometric decay was wrong]. The shell contribution to μ_est is a roughly
   constant fraction (0.03–0.06) of the shell's own mass 1/(2s²), so successive ratios are (s/(s+1))² ≈ 0.75–0.85,
   not geometric, and μ_est(12) + 1/24 bounds the limit; the prediction is μ_est(12) ∈ [0.024, 0.028] and the shell
   fraction within ±50% of its s = 6 value at every s ≤ 12. *Falsifier:* the shell fraction of D-entering
   self-cooperators rising above 0.1 or falling below 0.01 at any s ≤ 12.
2. **Probe-faker mass grows but stays small:** μ_pf(n) ≤ 0.006 at n = 12 and r(n) ≤ 0.25 at every n; conditional on
   an establisher being seeded, E[K_pf | A] < 0.5 and P(K_pf > 0 | A) < 0.35 at N = 100 for every n ≤ 12, with the
   resident-specific count. *Falsifier:* r(12) > 0.4 or P(K_pf > 0 | A) > 0.5. [after review] Sol's theorem target, a
   resident-conditioned spoiler bound uniform in the cutoff plus a founder-establishment lower bound, is what 2 and 6
   measure the ingredients of; the spec does not claim the bound.
3. **FairBot and `BOX1(THEM(ME))` stay unfakeable at every n ≤ 12.** *Falsifier:* a strict invader of either.
   [after review] Such a finding is first a check of the evaluator's semantics and of the outcome-symmetry argument,
   and only then a soundness question.
4. **Merging at I = 4** [after review: a pilot with one predeclared contrast]. The run-level efficient fraction is
   0.50 ± 0.15 at mN = 0.1, 0.42 ± 0.12 at mN = 1, and 0.38 ± 0.12 at mN = 10, and the mN = 0.1 minus mN = 10 contrast
   is positive with a 95% interval excluding 0. Sol notes an intermediate maximum is plausible (migration spreads
   founders as well as importing spoilers); the event logs decide which timescale wins. *Falsifier:* the contrast's
   interval entirely below 0.

**What it would mean.** If 1–3 hold, the lottery's establishment term has a positive limit in n and its only spoiler
stays rare, which is the tail bound the seeding programme needs at the level of this language family; the remaining
gap to a theorem is a proof that D-entering self-cooperators only accumulate under the length prior. If 4 holds, the
"islands" of the I ≫ N path are independent trials only when migration is slow compared with nucleation, which fixes
how mN should scale when the path is taken seriously.

## RS predictions (Jacob)

(Optional.)

## Procedure for the subagent

Follow CLAUDE.md discipline. [after review] Commit `predictions/2026-10-05-seeds-tail.md` carrying the RE predictions
*before any static computation*, including class counts beyond those already published for n ≤ 9; then run Part A,
then Part B. At most 3 workers; stop anything projected beyond 2 hours and say so;
do not edit RESULTS.md, REJECTED.md, THEORY.md, CLAUDE.md or DEFERRED.md; do not touch `runs/d8dcd7ee9a/row.json`; hand
back draft RESULTS, REJECTED, THEORY and DEFERRED text, at most 5 lines on what matters, and the branch and commits.
