# Spec: a semantic legibility gate (toward bounded provers), 2026-10-04

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-04-bounded-provers-gpt-6.1-sol.md`) and revised; changes marked [after review]. Committed before launch. To be run by an Opus subagent.

[after review] **What this is.** This arm is a *semantic legibility gate*, not a bounded-Löb implementation: the cost is semantic stabilization (atoms × settle world), not proof length or proof-search work, all boxes are charged the opponent-level cost whatever proposition they prove, and constants cost 0, which builds in a computational exemption. Conclusions are finite-language and about this gate. A realizability claim would need an explicit proof system, a resource measure and a sound checker, which is the follow-up, not this run.

## Why

The long-term goal is cooperation among Turing-complete programs with source access. The modal arm gets its results
from a free, sound provability oracle. The step toward realizability is a *bounded* sound prover: a program that
cooperates iff it can verify, within a budget, that the opponent cooperates with it, and otherwise defects. Critch's
parametric bounded Löb theorem (2019) says two such programs cooperate when their budgets exceed the lengths of the
proofs involved, which depend on the opponents' source lengths. So a budget creates a *legibility* cutoff: opponents
whose cooperation is too expensive to verify are treated as defectors.

This arm tests three things at once, under both objects of DEFERRED.md entry 1:
- whether a budget creates *closure by proof length* (the "soft clique" the sibling theorem's transfer analysis
  predicted: a sibling costs one more level, so a tight budget excludes it);
- what that closure costs in universality (the budget also excludes legitimate but expensive cooperators);
- whether a bounded sound core still survives the ε = 0 scramble, which is the condition the seeding programme needs.

## The instrument

Build on `_evaluate_priced` (`src/modal.py`), which already returns, per pair, the number of essential box atoms k(x)
and the settle world. Define the **verification cost** of x reading y as v(x, y) = k(y)·(1 + settle(y, x)): the work
to establish y's stable play toward x, which is the same proxy the priced arm used (semantic stabilization, a stand-in
for proof length; say so). Constants cost 0.

**Bounded box.** `BOX_b(φ)` is true iff `BOX(φ)` is true *and* the verification cost of the opponent toward the reader
is at most b. Otherwise it is false, and likewise for `BOXD_b`, `BOX1_b`, `BOXD1_b`. So a bounded FairBot
`BOX_b(THEM(ME))` cooperates iff the opponent provably cooperates with it *and* is legible at budget b.

[after review] **Semantics, made precise.** Costs and plays are mutually dependent, so the bounded game is a joint fixed
point: start from the free play table, compute v(x, y) from it, apply the gates and re-evaluate every pair, recompute
costs from the *bounded* play, and iterate until the play table is stable. Report the number of rounds and whether the
iteration cycles. Then verify **soundness on every pair**: whenever `BOX_b(THEM(ME))` is true for x reading y, y's
actual bounded play toward x is C (and the analogous check for `BOXD_b`, `BOX1_b`, `BOXD1_b` against their intended
propositions). Any violation is reported, and if violations exist the gate is redefined on the bounded trace before any
chain run. The free-game cost is reported alongside as a diagnostic, not used for the gate.

**Self-cooperation needs the budget to cover the self-proof.** `BOX_b(THEM(ME))` against itself: the cost is its own
k·(1 + settle), so there is a threshold b* below which bounded FairBot defects on itself. That is the bounded-Löb
threshold in this instrument; report it for each prover.

Three ways to assign budgets, run all [after review: fixed-support variant added]:
- **Global b:** every bounded box in the arm uses the same b ∈ {1, 2, 3, 4, 6, 8, ∞}; ∞ is the free arm.
- **Per-program b, fixed support:** the budget is an annotation on each box, b ∈ {1, …, 4}, at *no* node cost, so the
  genotype support and prior are identical across budgets and only the gate differs.
- **Per-program b, length-penalized:** as above but costing 1 node per unit of b. Report which prover families drop out
  of the cutoff at each n because of the penalty, with their total prior mass, so legibility is not confounded with
  language support.

## What to measure

1. **Static map** at n = 6 and 8 for each b: which classes self-cooperate; the legible set of each prover; thresholds
   b*; the mutual-cooperation graph; drift-closure per class (as in `src/moat_static.py`); the sibling check
   (`src/conj4.py`): does the sibling y = or(x, ψ_K) of each bounded prover exceed the budget, so that x defects on it?
   Universality of each closed class in the old sense (μ-weighted share of free FairBot's component) and in the
   within-budget sense (share of the legible self-cooperators).
2. **lim_N under mutation:** ε→0 chain, PD, w = 0.3, `eager_poly=False`, n ∈ {6, 8}, N ∈ {10², 10³, 10⁴, 10⁵}, per b:
   P(C,C); support and transitions; exits from the top state split strict/neutral/deleterious with the fitted exit
   slope in N; rival share (block definition from "Certificate pricing"); which family holds the mass.
3. **ε = 0 seeding lottery** (`src/almost_all_seeds.py`, iid from μ): per b, the cells (N, I) ∈ {(100, 4), (400, 4),
   (1,600, 4), (100, 64), (100, 256)}, 20 runs each with Wilson intervals; the efficient fraction; the per-island
   chance; and whether the bounded core survives the scramble (ALLC phase) as the free core did.
4. **Controls:** b = ∞ reproduces the free arm exactly; the clique arm at matched prior. [after review] Also two
   budget-matched gates that are *not* legibility: a random gate (each box is masked with the same overall frequency as
   the b-gate, at random over pairs, fixed seed) and an atom-count-only gate (mask iff k(y) > b, ignoring settle), to
   separate structured legibility from generic pruning of interactions.
5. **Sibling enumeration beyond n** [after review]: for each bounded prover, construct its sibling directly
   (`src/conj4.py`) whatever its size, and report its cost and legibility, so closure is not an artifact of neutral
   mutants being pushed past the cutoff.
6. **Lottery statistics** [after review]: paired seeds across b (same seed → same initial populations), an equivalence
   margin of 0.15 on the efficient fraction, adaptive replication up to 40 runs where the paired difference is within
   the margin but the interval is not, and unresolved runs recorded as unresolved.

## RE predictions (Fable)

1. **A threshold in b.** Bounded FairBot self-cooperates iff b ≥ 2 (k = 1 atom, settle world 1); PrudentBot needs
   b ≥ 4; P* needs b ≥ 4. [after review] Below its threshold a prover is not behaviourally D: it still cooperates with
   zero-cost ALLC (selective cooperation), so it is an exploitable class. *Falsifier:* FairBot self-cooperating at b = 1,
   or needing b > 3.
2. **Tight budgets give closure by proof length, at b = 4** [after review: corrected from b = 2, which conflicted with
   the prudent thresholds in 1]. The sibling y = or(x, ψ_K) adds two essential atoms at level K, so its cost is at least
   (k(x) + 2)(1 + settle) and exceeds x's by at least 2(1 + settle). At b = 2 FairBot's sibling is illegible but FairBot
   leaks through ALLC anyway; at b = 4 the prudent families (PrudentBot, P*) self-cooperate and their siblings cost ≥ 8,
   so the static map finds the first *drift-closed* classes in any modal arm at b = 4. *Falsifier:* no drift-closed class
   at b = 4, or a legible sibling of a self-cooperating prover at b = 4. Sol expects heterogeneous exclusion; that is
   consistent with this prediction only if every *closed* class's sibling is excluded.
3. **But ALLC is always legible** (cost 0), so bounded FairBot still tolerates ALLC and leaks through it by Corollary
   1: under mutation, bounded FairBot's exit is neutral at 1/N and its odds grow like N^(1/2) at every b. The closed
   classes at b = 4 are the prudent ones that defect on ALLC-tolerators (P*-like), and they are parochial (old-sense
   universality 0). *Falsifier:* a drift-closed class at b = 4 with positive old-sense universality.
4. **Under mutation, π at b = 4 goes to the closed prudent family** at n = 8, with a fitted exit slope steeper than
   −1.5 over N ∈ [10³, 10⁵] (closure beats the shadow; a fitted slope, not an asymptotic claim), P(C,C) ≥ 0.9 at
   N = 10⁴, rival share ≥ 0.5 (it defects on bounded FairBot). At b ≥ 8 the arm is within 0.05 of the free arm at every
   N. The random and atom-count gates at matched masking do *not* produce an exit slope steeper than −1.2. *Falsifier:*
   exit slope ≥ −1.1 at b = 4, b = 8 differing from free by more than 0.1, or a control gate matching the closure.
5. **Per-program budgets: the fixed-support variant decides.** [after review] With fixed support (no node cost), the
   π mass sits on the smallest b at which the resident family is closed (b = 4 for prudent, b = 2 for FairBot-like), not
   on larger b, because extra legibility admits siblings; with the length penalty the same holds and the penalty only
   sharpens it. *Falsifier:* most prover mass at the largest b in the fixed-support variant.
6. **The seeding lottery is unaffected for b ≥ 4, and weakened at b = 2.** [after review: sol's point that a tight
   gate fragments the core is right: at b = 2 the `BOX1` and `THEM(THEM)` provers are illegible to bounded FairBot, so
   the core's members defect on each other and the per-island survival falls.] Predictions: at b ≥ 4 the efficient
   fraction is within the 0.15 equivalence margin of the free arm's at every cell (0.25 / 0.45 / 0.80 at I = 4; 1.00 at
   I ≥ 64); at b = 2 it is lower by 0.1–0.3 at the I = 4 cells and still 1.00 at I ≥ 64; at b = 1 every cell is 0.
   *Falsifier:* b = 4 outside the margin at any cell, or b = 2 at I = 256 below 0.9.
7. **The seeding/mutation split:** the budget decides closure and parochialism under mutation, and under seeding it
   matters only through core fragmentation near the threshold. *Falsifier:* b ≥ 4 changing the lottery outcome.

**What it would mean.** If 2–4 hold, a proof budget is the first mechanism that closes a network without a copy
subsidy, and it does so by making siblings illegible, as the transfer analysis predicted; the price is parochialism,
as Corollary 1 requires, and the closure only matters under mutation. If 6–7 hold, the seeding programme is robust to
realizability at this level of idealization: a bounded sound core suffices. If 6 fails, bounded provers lose the
scramble, and the uniformity-in-n question has a negative answer at the budget level, which would redirect the
programme. If 2 fails, proof length does not separate siblings in this instrument and the "soft clique" needs a
different cost proxy.

## RS predictions (Jacob)

(Optional.)

## Procedure for the subagent

Follow CLAUDE.md discipline. Commit `predictions/2026-10-04-bounded-provers.md` carrying the RE predictions above after
measuring only language sizes and class counts; then the joint fixed-point semantics and the soundness check, then the
static map, then the chain, then the lottery. Label every conclusion finite-language and gate-specific. At most 3
workers; stop cells projected beyond 2 hours; do not edit RESULTS.md, REJECTED.md, THEORY.md or CLAUDE.md; do not touch
`runs/d8dcd7ee9a/row.json`; hand back draft RESULTS, REJECTED and THEORY text, at most 5 lines on what matters, and the
branch and commits. Note in every verdict that the cost proxy is semantic stabilization, not measured proof length.
