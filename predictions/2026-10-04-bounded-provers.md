# Predictions: a semantic legibility gate (toward bounded provers), 2026-10-04

Spec: `specs/2026-10-04-bounded-provers.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-04-bounded-provers-gpt-6.1-sol.md`).
Run by an Opus subagent. Committed before any bounded evaluation: the only numbers measured so far are language sizes
and the free arm's class counts (below).

**Scope label for every verdict.** This is a *semantic legibility gate*, not a bounded-Löb implementation. The cost is
semantic stabilization (essential atoms × settle world), not measured proof length or proof-search work; every box is
charged the opponent-level cost whatever it proves; constants cost 0. All conclusions are finite-language (n = 6, 8)
and specific to this gate.

## Measured before the predictions (language sizes and class counts only)

| n | canonical functions | non-constant | programs | box atoms | essential atoms k: 0 / 1 / 2 | free behavioural classes | prior mass of non-constants |
|---|---|---|---|---|---|---|---|
| 6 | 66 | 64 | 1,020 | 48 | 2 / 64 / 0 | 51 | 0.062 |
| 8 | 610 | 608 | 19,544 | 144 | 2 / 256 / 352 | 471 | 0.067 |

Per-program budgets, length-penalized (size |p| + b; constants carry no annotation): non-constant canonical functions
with no program of size ≤ n − b, and their free-prior mass (normalized over L_n):

| n | b = 1 | b = 2 | b = 3 | b = 4 |
|---|---|---|---|---|
| 6 | 32 (0.0008) | 40 (0.0021) | 56 (0.0228) | 64 (0.0620): every prover gone, FairBot included |
| 8 | 392 (0.0005) | 544 (0.0013) | 576 (0.0023) | 584 (0.0041) |

So at n = 8 every size-8 family (PrudentBot, P*) is absent from the length-penalized variant at every b, and at n = 6
FairBot itself is absent at b = 4. The fixed-support variant has 4 × 64 + 2 = 258 genotypes at n = 6 and
4 × 608 + 2 = 2,434 at n = 8.

## Operational definitions (fixed now)

- **Cost.** v(x, y) = k(y)·(1 + settle(y, x)), where settle(y, x) is the last world at which the vector of y's atom
  values against x changes (`last` in `modal._evaluate_priced`), read off the *bounded* trace. Constants: k = 0, cost 0.
- **Gate.** x's boxes reading y are open iff v(x, y) ≤ b(x). A closed gate makes every box atom of x false at every
  world when x reads y (BOX_b, BOXD_b, BOX1_b, BOXD1_b alike).
- **Joint fixed point.** Start from the free play; compute v; gate; re-evaluate every pair on the GL chain with the
  gate fixed; recompute v from the bounded trace; repeat until the gate matrix repeats. Rounds and any cycle reported.
- **Soundness check.** On the final round, for every pair and every open atom that is true at the stable world, the
  proposition it names (opponent plays C, resp. D, against ME / THEM / ^A) holds in the stable bounded play. Same check
  for level-1 atoms.
- **Per-program budgets.** One budget per program, b ∈ {1, 2, 3, 4}, applied to all its boxes; a quoted argument ^A is
  evaluated as A with the reader's budget. Fixed support: each non-constant canonical function gets mass μ(f)/4 per
  budget. Length-penalized: the annotation adds b nodes, and the length prior is recomputed over the extended language.
- **Controls.** b = ∞ (gate all open) must equal the free arm exactly. Random gate: among pairs with k(x) > 0 and
  k(y) > 0 (the b-gate never masks a constant), mask uniformly at random as many pairs as the b-gate's final mask
  does, fixed seed, no iteration. Atom-count gate: mask iff k(y) > b. Clique arm: `build_priced(n, 0, m_cliques=1)`
  (one clique spelling at FairBot's prior mass).
- **Chain.** ε→0, PD, w = 0.3, `eager_poly=False`, n ∈ {6, 8}, N ∈ {10², 10³, 10⁴, 10⁵}. Exit slope: least-squares
  slope of log(total exit per mutation event from the top cooperative state) on log N over N ∈ {10³, 10⁴, 10⁵}, a
  fitted slope, not an asymptotic claim. Rival share: 1 − largest block's share of the mutual-cooperation graph over
  cooperative monomorphic states with π ≥ 10⁻³, ALLC excluded (`cert_limN.networks`).
- **Lottery.** n = 6, ε = 0, complete island graph, mN = 1, horizon 10⁵ generations, the stopping rules of
  `src/almost_all_seeds.py`. Seeding iid from μ at the level of canonical functions, then mapped to each arm's classes,
  so the same seed gives the same initial programs at every b (paired). 20 runs per cell, Wilson intervals; paired
  difference against b = ∞ with a bootstrap 95% interval; equivalence margin 0.15; adaptive replication to 40 runs where
  the paired difference is inside the margin but the interval is not; unresolved runs recorded as unresolved. No-
  migration cells (100, 64, mN = 0) and (400, 4, mN = 0) give the per-island chance.

## RE predictions (Fable), verbatim from the spec

1. **A threshold in b.** Bounded FairBot self-cooperates iff b ≥ 2 (k = 1 atom, settle world 1); PrudentBot needs
   b ≥ 4; P* needs b ≥ 4. Below its threshold a prover is not behaviourally D: it still cooperates with zero-cost ALLC
   (selective cooperation), so it is an exploitable class. *Falsifier:* FairBot self-cooperating at b = 1, or needing
   b > 3.
2. **Tight budgets give closure by proof length, at b = 4.** The sibling y = or(x, ψ_K) adds two essential atoms at
   level K, so its cost is at least (k(x) + 2)(1 + settle) and exceeds x's by at least 2(1 + settle). At b = 2
   FairBot's sibling is illegible but FairBot leaks through ALLC anyway; at b = 4 the prudent families (PrudentBot, P*)
   self-cooperate and their siblings cost ≥ 8, so the static map finds the first *drift-closed* classes in any modal
   arm at b = 4. *Falsifier:* no drift-closed class at b = 4, or a legible sibling of a self-cooperating prover at
   b = 4. Heterogeneous exclusion is consistent with this prediction only if every *closed* class's sibling is excluded.
3. **But ALLC is always legible** (cost 0), so bounded FairBot still tolerates ALLC and leaks through it by Corollary 1:
   under mutation, bounded FairBot's exit is neutral at 1/N and its odds grow like N^(1/2) at every b. The closed
   classes at b = 4 are the prudent ones that defect on ALLC-tolerators (P*-like), and they are parochial (old-sense
   universality 0). *Falsifier:* a drift-closed class at b = 4 with positive old-sense universality.
4. **Under mutation, π at b = 4 goes to the closed prudent family** at n = 8, with a fitted exit slope steeper than
   −1.5 over N ∈ [10³, 10⁵], P(C,C) ≥ 0.9 at N = 10⁴, rival share ≥ 0.5 (it defects on bounded FairBot). At b ≥ 8 the
   arm is within 0.05 of the free arm at every N. The random and atom-count gates at matched masking do *not* produce
   an exit slope steeper than −1.2. *Falsifier:* exit slope ≥ −1.1 at b = 4, b = 8 differing from free by more than
   0.1, or a control gate matching the closure.
5. **Per-program budgets: the fixed-support variant decides.** With fixed support, the π mass sits on the smallest b
   at which the resident family is closed (b = 4 for prudent, b = 2 for FairBot-like), not on larger b, because extra
   legibility admits siblings; with the length penalty the same holds and the penalty only sharpens it. *Falsifier:*
   most prover mass at the largest b in the fixed-support variant.
6. **The seeding lottery is unaffected for b ≥ 4, and weakened at b = 2.** At b ≥ 4 the efficient fraction is within
   the 0.15 equivalence margin of the free arm's at every cell (0.25 / 0.45 / 0.80 at I = 4; 1.00 at I ≥ 64); at b = 2
   it is lower by 0.1–0.3 at the I = 4 cells and still 1.00 at I ≥ 64; at b = 1 every cell is 0. *Falsifier:* b = 4
   outside the margin at any cell, or b = 2 at I = 256 below 0.9.
7. **The seeding/mutation split:** the budget decides closure and parochialism under mutation, and under seeding it
   matters only through core fragmentation near the threshold. *Falsifier:* b ≥ 4 changing the lottery outcome.

## Subagent predictions (made from reading the code, before any bounded evaluation)

- **S1 (arithmetic of prediction 1).** With settle read as `_evaluate_priced`'s last change world, FairBot's atom
  against a copy never changes (it is true at every world), so its self-cost is 1·(1 + 0) = 1 and b*(FairBot) = 1:
  prediction 1's falsifier fires on the instrument's arithmetic, not on substance. Hand trace: PrudentBot's atoms
  against a copy never change either (self-cost 2, b* = 2); P*'s `BOX(THEM(ME))` flips at world 1 (self-cost
  2·2 = 4, b* = 4). *Falsifier:* any of these three thresholds different.
- **S2 (soundness).** The gated evaluation with a fixed mask is an ordinary GL-chain evaluation, so soundness holds on
  every pair by construction once the joint iteration converges; the risk is non-convergence (a cycle), not unsound
  boxes. *Falsifier:* a soundness violation on a converged gate, or a cycle at any b.
- **S3 (siblings).** Every sibling of a bounded prover costs more than b to its original for b ≤ 4 (it carries
  k(x) + 2 ≥ 3 atoms and its ψ atoms against x move at least once), so siblings are excluded at b ≤ 4 and legible at
  b ≥ 8 for FairBot. *Falsifier:* a legible sibling of a self-cooperating prover at b ≤ 4.
