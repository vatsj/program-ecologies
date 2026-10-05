# Spec: does a co-seeded faker stop establishment? The spoiler half of "almost all seeds", 2026-10-05

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-05-spoiler-conditioned-gpt-6.1-sol.md`) and revised; changes marked [after review]. Committed before launch. To be run by an Opus subagent.

[after review] Conclusions are finite-cell evidence at n ∈ {6, 9, 12} and N ∈ {100, 400}; nothing here establishes a uniform-in-n discount or a limit. The path the seeding claim needs is stated in THEORY §3 and DEFERRED 1; this run measures one ingredient of it.

## Why

RESULTS "the tail in n" made the establishment half of the seed lottery rigorous (μ_est ≥ 0.0207 uniformly in the
cutoff) and left one open ingredient: the resident-conditioned spoiler exposure, P(K_pf > 0 | A) = 0.27 at n = 12.
That number is an *exposure*, not a loss rate. The question that decides "almost all seeds" is conditional: given that
an island's seed contains an establisher *and* one of its fakers, how often does the island still establish? If the
answer is "usually", the spoiler half is a bounded multiplicative discount on p and the result goes through; if a
co-seeded faker reliably kills establishment, exposure growing in n would eventually bite.

Mechanism to test: a faker of establisher x exploits x only while x is present, and is itself eaten by D once x is
gone, or else it must also beat D on its own. In the scramble, D eats ALLC first and the establisher is a small
minority; the faker's advantage over x is proportional to x's frequency, so it is tiny during the scramble, and the
faker is deleterious against D unless it is itself an establisher. So I expect co-seeded fakers to matter only when
they are *themselves* establishers (the prover family exploiting the two near-universal suckers), which leaves a
cooperative island anyway.

## Design (no migration, so each island is one trial)

`src/seeds_in_n.py` kernel, modal arm, ε = 0, iid seeds, single islands (I = 1), no migration, horizon 10⁵, certified
outcomes. n ∈ {6, 9, 12} (n = 12 needs the one-off evaluation from `src/seeds_tail.py`; reuse it), N ∈ {100, 400}.
- [after review] **Payoff tables first.** Before any run, extract for every (target, faker) pair with μ(target) ≥ 10⁻⁴
  the 4×4 table over {target, faker, D, ALLC}, and classify the faker's play against D as strictly disadvantaged,
  neutral (tie), or advantaged. The predictions below distinguish these.
- [after review] **Success, defined three ways,** reported separately: *target survival* (the inserted or seeded target
  class is in the certified terminal support), *cooperative fixation* (the terminal support is a mutually cooperating
  set), and *efficiency* (island P(C,C) ≥ 0.95). Unresolved islands at the horizon are censored, not losses. Terminal
  support, transition structure (the order of extinctions) and P(C,C) are reported, not only the winning class.
- **Natural seeds:** 4,000 islands per (n, N), iid from μ. For each island record: the establishers present (class,
  count), the fakers of those establishers present (resident-specific, class, count), whether each faker is itself an
  establisher, the three outcomes, the terminal support, the time of ALLC extinction, and [after review] the
  target / faker / D frequencies at ALLC extinction and every 20 generations until resolution.
- **Conditioning cells** [after review: four disjoint categories] on the natural seeds, given an establisher present:
  (i) no faker of any present establisher; (ii) non-establisher fakers only; (iii) establisher-fakers only; (iv) both.
  Report each cell's establishment with a Wilson interval and its count, stratified by target identity and target
  count where counts allow (minimum 50 islands per stratum, otherwise pooled and labelled). The spoiler discount
  d(n, N) is (ii)/(i), with a bootstrap 95% interval on the ratio (Wilson intervals do not cover ratios). These are
  descriptive: faker presence correlates with target identity and background; the causal estimate comes from the
  forced seeds.
- **Forced seeds** [after review: target–faker *pairs*, paired backgrounds, dosage]. For each of the 6 heaviest
  (target, faker) pairs at each n (the faker must actually exploit that target, verified from the payoff table), draw
  1,000 iid-μ backgrounds per (n, N) and, on the *same* background, run four treatments by replacement at fixed N:
  (a) target + k copies inserted; (b) target + k and faker + k inserted; (c) target + k and k copies of a *neutral*
  program (one with the target's own class, so replacement without exploitation) inserted; (d) faker + k alone.
  Dosage k ∈ {1, 3, 10} at N = 400 and k ∈ {1, 3} at N = 100, so single-copy insertion is not taken to represent
  natural multiplicities. Existing copies of the inserted classes in the background are counted and left in place.
  Report, per pair and dosage, target survival, cooperative fixation and efficiency in (a)–(d), the paired difference
  (a) − (b) with its interval, and which class wins.
- **The discount's trend in n:** d(6), d(9), d(12) at both N.

## RE predictions (Fable)

1. **Co-seeded non-establisher fakers rarely stop establishment, and the effect depends on the faker's play against
   D** [after review]. Fakers strictly disadvantaged against D lower the target's establishment by less than 30% in the
   paired forced seeds at k = 1 (survival and cooperative fixation both); fakers that *tie* D are the harmful class and
   may lower it by more. Pooled, d(n, N) ≥ 0.7 at every (n, N), with its bootstrap interval. *Falsifier:* the pooled d's
   interval entirely below 0.5 at any cell. Sol predicts heterogeneity by payoff profile and target abundance; the
   pair-level table is the test, and the pooled d is my bet.
2. **The discount is flat in n, at the pair level** [after review: weakened]. For each (target, faker) pair present at
   all three n, the paired forced-seed effect at k = 1 changes by less than 0.15 (absolute) from n = 6 to n = 12; the
   pooled d may move with composition. *Falsifier:* a pair whose effect grows by more than 0.3 from n = 6 to 12.
3. **Establisher-fakers leave a cooperative island** [after review: weakened]. In cell (iii), *cooperative fixation* is
   at least 0.8 of cell (i)'s, even where *target survival* is lower; the winner is some establisher. *Falsifier:*
   cooperative fixation in (iii) below 0.6 of (i).
4. **Forced seeds: the mechanism.** In the paired forced seeds at N = 400, k = 1: (a) − (b) is below 0.3 for every
   pair whose faker is strictly disadvantaged against D; (a) − (c) is within ±0.05 (replacement alone does nothing);
   (d) alone never fixes a non-establisher faker in more than 5% of islands; and the frequency logs show the faker's
   share falling after ALLC extinction while the target's rises, in at least 70% of (b) islands where the target
   survives. *Falsifier:* a strictly-D-disadvantaged non-establisher faker winning more than 10% of (b) islands at
   N = 400, k = 1.
5. **The combined bound, as a held-out prediction** [after review]. Estimand: the unconditional per-island
   establishment probability p(n, N) of a natural seed. Decomposition: p = P(A)·Σ_cells P(cell | A)·P(est | cell),
   with the four cells of the conditioning table. Fit the cell probabilities on the first 2,000 natural islands and
   predict p on the second 2,000; prediction within 15% of the held-out measured p at every (n, N). *Falsifier:*
   disagreement above 30% on held-out seeds.

**What it would mean.** If 1–2 hold, the spoiler half is a bounded discount at these cells, and "almost all seeds"
has both halves measured for this language family: a rigorous establishment bound and a spoiler discount that is
flat at the pair level. The remaining step is a lemma; [after review] sol's framing of it is the right one: it must
compare the *integrated* target–faker selection through the scramble against drift, uniformly over backgrounds and
cutoffs, not merely bound the instantaneous advantage by target frequency. The frequency logs are the data for that
lemma.
If 1 fails, co-seeded fakers kill establishment and the growth of exposure in n is the term that could defeat the
limit, which would make a prior that suppresses fakers, or structure that separates them, necessary.

## RS predictions (Jacob)

(Optional.)

## Procedure for the subagent

Follow CLAUDE.md discipline. Commit `predictions/2026-10-05-spoiler-conditioned.md` carrying the RE predictions before
any run; then run. At most 3 workers; stop anything projected beyond 2 hours and say so; do not edit RESULTS.md,
REJECTED.md, THEORY.md, CLAUDE.md or DEFERRED.md; do not touch `runs/d8dcd7ee9a/row.json`; hand back draft RESULTS,
REJECTED, THEORY and DEFERRED text, at most 5 lines on what matters, and the branch and commits.
