# Spec: the guard margin as a heritable trait: does selection buy Con-reading, and its fakers, by itself?, 2026-10-06

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-06-guard-trait-gpt-6.1-sol.md`) and revised; changes marked [after
review]. To be run by an Opus subagent. Follow-up to RESULTS "K with cut and distribution under a box" (DEFERRED 2,
"would settle it next"). Moderate compute: a full long-guard table at n = 8 is needed.

## Why

Within the class of sound bounded provers that compose witnesses, exactly one switch returns P\*-type cooperation
(cooperate iff provable from PA + Con but not PA): reading the consistency guard with a reflection margin of about
2b plus a 4-rule. The same switch returns the Gödel-sentence and Con-sentence fakers, and on a graft the net was
below K. That graft fixed the margin for the whole population. A realizable reader could carry its margin as a
heritable trait, like its budget, and selection would then decide whether the reflection margin is worth buying.
[after review] The statistic is not the stationary mass on g = long, most of which can be neutral drift between
behaviourally identical guard twins; it is the allocation among *behaviourally distinguishable* (source, g) pairs,
and the transition structure that produces it.

## Semantics and definitions [after review]

- **Genotype** (source, g), g ∈ {0, long}: the reader's own guard offset is part of its program semantics (its
  BOXk atoms read ¬□_b^k⊥ at g = 0 and ¬□_{2b+8}^k⊥ at g = long). An opponent's guard changes the proposition the
  reader proves about it (the opponent's unfolded definition contains the opponent's guard), so every cross-guard
  block (g = 0 reader vs g = long opponent and the converse) is **built from the mixed semantics**, never reused from
  a homogeneous table, and every newly derived content is replayed by the independent checker with the reader's
  budget and the opponent's identity. Lumpability is established across both guard populations jointly.
- **Guard twins:** (s, 0) and (s, long) whose rows and columns are identical in the full mixed table; their mass is
  **neutral guard mass**. **Active guard mass:** mass on (s, long) whose row or column differs from (s, 0)'s.
- **Mutation kernels** (both run): *joint* (a mutant redraws (source, g) from the product prior) and *separate* (a
  mutant changes either the source, with the guard inherited, or the guard, with the source inherited, each with
  probability 1/2). A **sham heritable bit** control: a label that changes neither proofs nor costs, under the same
  kernels, to calibrate neutral label allocation and twin handling.
- **Guard-induced action changes:** the complete set of (reader, opponent) plays that differ between g = 0 and
  g = long readers, weighted by source prior, split into newly enabled cooperation and newly enabled exploitation.
- **Price:** amortized, c·(2b + 8)/N per match for a g = long reader (the extra guard reading verified once per
  lifetime of ≈ N matches, as in the K-at-n8 amortized schedule), c ∈ {0, 0.01, 0.1, 1}, N = 10⁴; the zero-price
  cell is the reference; the schedule is imposed and says so.

## Design

**Catalogue.** K_c4 (K + Cut + UnfId + Dist⁺) at n = 8, b = 16, over (source, g): the full long-guard table (closure
size and time reported; the targeted-table method if the full closure does not fit) and both cross-guard blocks from
the mixed semantics, soundness checker (0 violations), witness replay, joint lumpability. Guard priors: uniform
over {0, long}, and 0.9/0.1; both applied to the chain and the lottery.

**Static.** Guard twins and active (source, g); the guard-induced action-change table; establishers, incompatible
pairs, rivals and bridges of the g = 0 core and the g = long core; which sources cooperate only at g = long
(P\*-type) and which fakers act only against g = long readers; for the core programs the four encounter payoffs
of a g = long mutant in a g = 0 resident of the same source (resident–resident, resident–mutant, mutant–resident,
mutant–mutant) and the exact N·ρ at N = 10³ and 10⁴ (neutrality is exact, N·ρ = 1, iff all four are identical).

**Chain** (seeded log-domain solver with audit outputs, independent deep-state discovery as in the solver audit's
`src/chain_log.py` if merged, else the K-cut audit): ε→0 over the (source, g) catalogue at N = 10³, 10⁴, 3·10⁴,
w = 0.3, PD, under both kernels and both priors: π on neutral and on active g = long mass separately, P(C,C),
support, transitions, the guard composition of the cooperative support, the entry and exit rates of the active
g = long genotypes and of the g = 0 core with their N-scaling (asymptotic bottlenecks estimated, not only three
finite N), against the g = 0-only (K) and g = long-only chains as references; the sham-bit control under both
kernels. **Attribution interventions** (N = 10⁴, uniform prior, joint kernel): delete the newly enabled fakers only;
delete the newly enabled cooperative partners only; other weights retained.

**Lottery** (ε = 0, (100, 64), mN = 1, 20 paired seeds, both priors): efficient fraction with paired differences
and intervals, the guard composition of holders, establishment, loss and coexistence times, separations by
(source, g) pairs.

**Price sweep** (chain at N = 10⁴, uniform prior, joint kernel): c ∈ {0, 0.01, 0.1, 1}; π on active g = long mass
and P(C,C) per c.

Priority: catalogue → static → chain at N = 10⁴ (both kernels, uniform prior) → sham control → attribution → chain
at 10³ and 3·10⁴ and the 0.9/0.1 prior → lottery → price sweep. ≤ 3 workers; stop where time runs out and say so.

## Required outputs

`runs/guard-trait.md` and `.json`, code in `src/guard_trait.py` (reusing `src/k_cut.py`, `src/bounded_k.py`,
`src/k_at_n8.py`; no core edits except bug fixes in their own commits), a predictions file from the spec committed
before any counted run, the usual hand-back (draft RESULTS, REJECTED, THEORY §9.2 and DEFERRED 2 edits, NOTATION,
≤ 5 lines, branch from `git branch --show-current`, commits).

## RE predictions (with falsifiers) [after review]

1. **Neutral guard mass is prior- and kernel-sensitive and uninformative; the active g = long mass is small:**
   π on active g = long genotypes ≤ 0.2 at N = 10⁴ under the uniform prior and both kernels, and the sham bit's
   allocation matches the neutral guard twins' within 0.05 under each kernel. *Falsifier:* active g = long π ≥ 0.4,
   or the sham allocation differing from the neutral twins' by ≥ 0.15. Grey zone 0.2–0.4.
2. **Displacement is explained by transition structure, not interpolation** (sol's reading adopted): the mixed
   chain's P(C,C) at N = 10⁴ need not lie between the homogeneous references, and the RE predicts it within 0.03 of
   K, with the attribution interventions showing the newly enabled fakers lowering P(C,C) by more than the newly
   enabled partners raise it. *Falsifier:* P(C,C) above K by ≥ 0.05 (the margin is worth buying), or the partner
   intervention's gain exceeding the faker intervention's loss by a factor ≥ 2. Grey zone between.
3. **A g = long FairBot mutant is exactly neutral in a g = 0 FairBot resident** (all four encounter payoffs
   identical, N·ρ = 1 to numerical error) **and g = long P\* strictly invades no g = 0 core program.** *Falsifier:*
   a payoff difference among the four, or P\*_long strictly invading a core program.
4. **The lottery's efficient fraction is unchanged within pairing** (paired difference's interval includes 0) and
   g = 0 holders are ≥ 0.5 of islands under the uniform prior. *Falsifier:* paired difference ≤ −0.15, or g = long
   holders ≥ 0.7.
5. **Under the amortized price the active g = long mass decreases monotonically in c and is ≤ 0.05 at c = 0.1.**
   *Falsifier:* non-monotone in c, or ≥ 0.2 at c = 0.1.

The RS is invited to add predictions; the uncertain one is 2's intervention ordering.
