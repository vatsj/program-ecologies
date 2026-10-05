# Predictions: divide-the-dollar partitions across islands, with `ROLE`, without `ROLE`, and with fixed roles (2026-10-05)

Spec `specs/2026-10-05-dollar-partitions.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-05-dollar-partitions-gpt-6.1-sol.md`;
where the two differ the spec is the resolution). Code: `src/dollar_partitions.py` (on top of `src/dollar.py`).
Committed before any counted run (chains, joint simulation, lotteries, merges).

**Computed before this commit, and recorded in the static addendum `runs/dollar_partitions/static_dollar5.md`,
`runs/dollar_partitions/static_dollar3.md`:** the class tables of all three role structures (n = 5), the induced
priors, the pairwise contest table, the adjacent-move table with prior-weighted entry and exit rates (constant
conventions; direct moves and conceder paths), and a deterministic replicator from 400 multinomial(100) draws of the
prior per arm (no drift). Code checks that are not results: the fixed-role GTH solver agrees with a direct solve of
the generator on a random 5-class game to 2·10⁻¹⁶; the island kernel reproduces the one-mutant fixation probability
in one population (0.102 ± 0.005 vs 0.098) and with two slots (0.131 ± 0.005 vs 0.124) on a synthetic game; one
timing run per arm at (64, 100), mN = 0.1, 2,000 generations, and one timing run of the joint simulation; no outcome
of any timing run was looked at.

## Design as implemented (deviations from the spec stated)

- **Cutoff n = 5 in every arm (fallback).** `dollar5` at n = 6 has 19,036 programs with `ROLE` and 12,298 without;
  the evaluator's full value array alone would be 29 GB and 6 GB. n = 5 has 3,842 / 2,550 programs; the class counts
  are 78 (no `ROLE`) and the `ROLE` count in the static file. `dollar3` (control) also at n = 5 (1,586 / 902 programs;
  80 / 45 classes).
- **Arms:** (i) `role`: one population, `ROLE` in the grammar, role-averaged payoffs; (ii) `norole`: one population,
  the `--norole` grammar; (iii) `fixed`: two slot populations of the `--norole` grammar, a match draws one program from
  each; **N is per slot** in every fixed-role table. Weak arm (simulation, `THEM(^A)` probes, X), w = 0.3, f = exp(w·payoff).
- **Fixed-role chain** exactly as specified: joint states (a, b); a mutation event picks a slot with probability 1/2,
  draws q from that slot's prior (the n = 5 class prior, cut unit); q fixes with the constant-selection Moran
  probability at per-slot size N (a slot's fitness depends only on the other slot's resident). All K² states are
  solved by GTH on the embedded jump chain (entries below 10⁻²⁵ of a row dropped and reported) with π(s) =
  π_jump(s)/R(s) in log space. One-population chains use `src/chain.py`'s `Chain` (polymorphic attractors, Moran
  fixation, flow pruning θ = 10⁻⁷) on the class-level payoff matrix.
- **Lottery kernel:** `src/islands.py`'s dynamics (uniform death; parent from the same island and slot with weight
  exp(w·mean payoff), or with probability m = mN/N from a uniformly chosen other island, fitness evaluated there;
  complete island graph), with S = 2 slot populations per island in the fixed arm (a birth picks the island and slot
  uniformly; a generation is I·S·N births), exact event skipping (a birth on a monomorphic island-slot without
  migration changes nothing), and the **verified-closed stop rule**: one population, every pair of present classes
  payoff-identical (`src/islands.py`'s rule; with self-exclusion nothing weaker freezes fitnesses); two slots, within
  each slot every present class earns the same against every present class of the other slot. At m = 0 a run stops
  when nothing can change (every island-slot monomorphic). Runs not closed at the horizon (10⁵ generations) are
  *censored*. Checks every 5 generations to 2,000, every 25 to 10⁴, every 100 after.
- **Island partition label:** the outcome category (efficient split, unordered with one population and ordered
  slot 1 | slot 2 with fixed roles; ineff; clash) holding ≥ 0.99 of the island's random-matching encounters, else
  *mixed* (unresolved or a stable polymorphism; the locally-closed flag separates them). *Partition-frozen*: the
  first check at which every island is locally closed; the *escape rate* is the number of island label changes per
  island-generation after it. *Loss hazard*: a label held by some island at one check and by none at the next, per
  generation after the partition-frozen time. *T_nuc*: median first locally-closed check per island at m = 0.
- **Statistics:** demand, realized payoff (demand if compatible, else 0), normalized share d_i/(d_i + d_j) of a
  compatible match. E[max share] = expected max realized payoff per encounter (the three-player convention; ex post);
  ex ante max share = the largest class-mean payoff in the state (1/2 on every symmetric efficient one-population
  convention, `ROLE` included); dwl = 1/2 − mean realized payoff per agent; P(efficient) = share of encounters on an
  efficient split. Benchmark: uniform over the five ordered efficient splits of `dollar5` gives 50–50 = 0.20 and
  E[max share] = 0.70 (in `dollar3`, three ordered splits: 1/3 and 0.611).
- **Run-level intervals** for every island statistic: 95% intervals from the across-run distribution of the run mean
  (t-interval on run means; Wilson for run-level binary outcomes).
- **Joint-simulation validation:** two slots of N = 50, ε = 10⁻³ per birth, 10 seeds, 2·10⁷ generations each (step 10),
  started at (S3 | S3); compared with the fixed-role chain at N = 50 on encounter-level ordered categories; persistent
  polymorphism = fraction of slot-checks whose largest class holds < 0.9.
- **Merges** (`role` arm): one population of N ∈ {100, 400}, 50–50 share ∈ {0.25, 0.3, 0.35, 0.375, 0.4, 0.45, 0.5},
  100 merges per point, pure S3 + `ROLE`, and sampled end states (one 1/2–1/2 island and one 1/6–5/6 island from the
  m = 0 lottery at (100, 64), resampled by composition), run to the verified-closed stop.

## Verdict rules

A prediction **holds** if every clause holds and its falsifier does not fire; **fails** if the falsifier fires
(reported as "falsifier fired"); **fails as stated** if a non-falsifier clause fails while the falsifier does not
fire. Interval-based clauses are judged on the point estimate, with the interval reported; where the 95% interval
straddles a threshold the verdict says so. Cells not run are "not tested". Chain clauses "at N = 10³" are judged at
N = 10³; "at N ≥ 10³" at both 10³ and 10⁴.

## RE predictions (copied verbatim from the spec)

1. **Mutation object with `ROLE`: 50–50 wins.** π on the 50–50 convention (constant S3 and its on-path shadows) is
   ≥ 0.5 at N ≥ 10³ and grows with N; the correlated splits (`ROLE`, `flip(ROLE)`, 1/3–2/3 via readers) hold ≤ 0.35
   together; P(efficient) ≥ 0.95. Reason: risk dominance (crossing 5/8) in the contest between the two 1-node
   conventions, which the RE expects to carry over to the full grammar because readers and shadows enter neutrally on
   both sides [after review: sol holds that mutation-entry weights and neutral paths can decide the large-N
   distribution, and predicts a fair advantage only in the restricted contest; the exit-rate table decides between
   the two readings]. *Falsifier:* correlated splits ≥ 0.5 at N = 10³, or 50–50 ≤ 0.3. **Control (ii), one
   population without `ROLE`:** 50–50 ≥ 0.7, since no correlated split is expressible and the unequal constants
   clash with themselves; *falsifier:* 50–50 ≤ 0.5.
2. **Seed lottery with `ROLE`: a patchwork, with 50–50 the modal convention but not dominant.** Across islands at
   (100, 64), mN = 0.1, the 50–50 convention holds 0.4–0.7 of islands, the `ROLE` (5/6, 1/6) split 0.1–0.4, and
   1/3–2/3 splits ≤ 0.2; ≥ 0.9 of islands are efficient at the horizon; at mN = 1 the patchwork resolves toward 50–50
   within 10⁵ generations in ≥ 0.5 of runs. *Falsifier:* 50–50 < 0.25 or `ROLE` > 0.5 of islands at mN = 0.1, or
   efficiency < 0.8.
3. **Merges go to the risk-dominant convention, not the larger one:** for pure-constant merges of 50–50 with `ROLE`,
   the 50–50 win probability crosses 1/2 at a 50–50 share in [0.35, 0.45] (the deterministic threshold is 3/8) and
   the crossing sharpens with N; at equal shares 50–50 wins ≥ 0.7 at N = 100 and ≥ 0.9 at N = 400. Sampled end
   states with shadows shift the crossing by < 0.05 [after review: sol notes the advantage at share 0.4 is small,
   0.35 against 1/3, so the prediction is about the crossing and its sharpening in N, not a universal probability].
   *Falsifier:* `ROLE` wins ≥ 0.5 of equal-share pure merges at N = 400, or the crossing lies outside [0.3, 0.5].
4. **Fixed roles: endpoint enrichment, not 50–50.** [after review: restated per ordered state against the
   uniform-over-ordered-splits benchmark, under which 50–50 already gets 1/5 and E[max share] already 0.70 in
   `dollar5`.] π is symmetric about 1/2 by relabeling (a check, not a prediction); per ordered split,
   π(1/6–5/6) ≥ 1.5·π(1/2–1/2) and π(1/3–2/3) ≥ π(1/2–1/2) at N ≥ 10³, so 50–50 ≤ 0.15 and E[max share] ≥ 0.72;
   the moves run through conceders (neutral drift of the losing side, then a strict move by the other), and the
   entry/exit-rate table shows the endpoints' *entry* rates are not smaller than the middle's, which is what the
   uniform-walk counterexample needs to fail. In `dollar3`, π(1/3–2/3) ≥ π(1/2–1/2) per ordered state (50–50 ≤ 1/3).
   *Falsifier:* π(1/6–5/6) ≤ π(1/2–1/2) per ordered state in `dollar5` at N = 10³, or E[max share] ≤ 0.70.
   (Young's adaptive-play result predicts the opposite; this is the prediction the RE is least sure of.)
5. **Fixed-role lottery:** per island, the 1/6–5/6 split is at least as frequent as 50–50 at (100, 64), m = 0 and
   mN = 0.1 (50–50 ≤ 0.2 of islands), the slot that gets more is decided per island by the scramble with no slot
   favoured in expectation (|mean slot payoff difference| < 0.05), and ≥ 0.8 of islands are efficient. *Falsifier:*
   50–50 ≥ 0.4 of islands, or 1/6–5/6 < 0.1.


## Subagent predictions

Written after the static tables for `norole` and `fixed` (both games) and `role` in `dollar3`; the `dollar5` `role`
evaluation was still running at commit time (its static table is added to the addendum afterwards and does not
change these). Reasoning in one line each.

- **S1 (fixed chain: endpoints, by entry and exit together).** In `dollar5` at N = 10³ and 10⁴, per ordered state
  π(1/6|5/6) ≥ 2·π(1/2|1/2), the two endpoints together hold ≥ 0.55, 50–50 ≤ 0.10, E[max share] ≥ 0.75. *Reason:* the
  static adjacent-move table gives the endpoints both the larger entry (5.8·10⁻⁷ vs 1.6·10⁻⁷ per event at N = 10³) and
  the smaller exit (2.2·10⁻⁷ vs 5.3·10⁻⁷): an accommodator in either slot lets the other slot jump straight to the
  largest compatible demand, and the larger jump has the larger fixation probability. *Falsifier:* π(1/6|5/6) <
  1.5·π(1/2|1/2) at N = 10³, or endpoints < 0.4.
- **S2 (fixed chain: mechanism).** At N ≥ 10³ ≥ 0.8 of the flux between distinct efficient ordered splits leaves
  from states with a non-constant slot (conceder paths), and the ordered-split distribution moves by < 0.05 (absolute,
  per split) from N = 10³ to 10⁴ (entry and exit both scale as 1/N). *Falsifier:* the conceder share < 0.5, or a
  split moves by > 0.1.
- **S3 (norole chain).** One population without `ROLE`: π(1/2–1/2) ≥ 0.9 at N = 10³ and 10⁴ and P(efficient) ≥ 0.9;
  the unequal constants have no efficient monomorphic convention and the Hawk–Dove polymorphisms are inefficient and
  strictly invadable by accommodators. *Falsifier:* π(1/2–1/2) < 0.7 at N = 10³.
- **S4 (role chain: risk dominance fades with N).** In `dollar5` with `ROLE` the direct S3 ↔ `ROLE` moves are
  e^(−Θ(N)) in both directions, so at large N the ratio of the two conventions is set by entry from inefficient
  states and by the exits through shadows, not by the 5/8 crossing (sol's reading): 50–50 lies in [0.35, 0.8] at
  N = 10³ and 10⁴, the correlated splits hold ≥ 0.15, and 50–50 does not grow by more than 0.05 from N = 10³ to
  10⁴. *Falsifier:* 50–50 > 0.9 at N = 10⁴, or 50–50 at N = 10⁴ exceeds N = 10³ by > 0.1.
- **S5 (lotteries: the scramble is fair in every role structure).** At (100, 64), m = 0 and mN = 0.1, 1/2–1/2 holds
  ≥ 0.6 of islands in `role` and `fixed` and ≥ 0.85 in `norole`; in `fixed` the two endpoints together hold ≤ 0.15 of
  islands. *Reason:* iid seeds from the prior are near-uniform over the five 1-node constants, against which S3 is the
  best reply (payoff 0.30 against a uniform demand, the next best 0.27); the deterministic two-population replicator
  from 400 such seeds ends at 1/2|1/2 in 0.92 of draws (one population: 0.99 without `ROLE`; 0.875 with `ROLE` in
  `dollar3`). So the lottery and the mutation object disagree under fixed roles. *Falsifier:* 1/2–1/2 < 0.4 of
  islands in `fixed` at m = 0, or the endpoints ≥ 0.3.
- **S6 (lotteries: no escape after partition-freeze at mN = 0.1).** At mN = 0.1 the post-partition-frozen escape rate
  is < 10⁻⁵ per island-generation in every arm, and runs with two or more conventions at the horizon are censored
  rather than resolved. *Falsifier:* escape rate > 10⁻⁴.
- **S7 (validation).** The joint two-slot simulation at N = 50, ε = 10⁻³ matches the fixed-role chain within total
  variation 0.1 over ordered categories; polymorphic slot-checks (largest class < 0.9) ≤ 0.3, all neutral standing
  variation. *Falsifier:* TV > 0.2.
- **S8 (merges).** Pure S3 + `ROLE` merges cross 1/2 at a 50–50 share in [0.33, 0.42] at both N, and at N = 400 the
  50–50 share 0.5 wins ≥ 0.98. *Falsifier:* crossing outside [0.3, 0.45] at N = 400.
- **S9 (`dollar3` control).** Fixed roles: per ordered state π(1/3|2/3) ≥ 2·π(1/2|1/2) at N ≥ 10³ (static entry/exit
  ratio 1.75 vs 0.30). *Falsifier:* π(1/3|2/3) < π(1/2|1/2) per ordered state.
