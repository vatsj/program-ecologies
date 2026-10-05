# Spec: proof-carrying contracts v1, legibility as a shared precomputed guarantee, 2026-10-04

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-04-proof-carrying-contracts-gpt-6.1-sol.md`) and revised; the instrument and predictions sections were rewritten after review, as marked. Committed before launch. To be run by an Opus subagent.

## Why

The RS's pitch: a contract is a precomputed guarantee about a program's behaviour, carried with the program and checked
cheaply by anyone. The search cost is paid once; checking is cheap; the guarantee is shared across every program it is
true of; and contracts can be transmitted between fit programs ("swapping") as a second operator beside, or instead of,
mutation. The general form (DEFERRED.md, operating definition): a contract is (pre, post, proof), "whenever *pre* holds
my action satisfies *post*", with *pre* ranging over the opponent's *contracts* and over population state, never over
source. This v1 implements *pre* over contracts only; the population-state hook is built but unused, for the union game.

Three results already fix parts of the picture, so v1 is aimed at what is new:
- Amortized checking is the α = 1 price path and behaves as free proofs (THEORY §9.2), so checking cost is not the
  question.
- A legibility gate (spec 2026-10-04-bounded-provers, running) limits whom a bounded reader can verify *from source*.
  A contract is exactly what restores legibility: a reader that cannot afford to derive your behaviour can still check
  your proof.
- Corollary 1 says the universal network leaks under mutation through ALLC, whatever the channel; at ε = 0 it does not.

So v1 asks: **does carrying contracts restore cooperation that a legibility gate removed, and when contracts spread by
swapping, which contract wins: the one with the most prior mass, or the one valid for the most sources?**

## The instrument [rewritten after review]

- **Sources** are modal programs p at n = 8 (471 classes; n = 8 so that P* exists). **Contracts** are elements of a
  finite contract alphabet C: a contract is an *exact policy over contracts*, a map c: C ∪ {none} → {C, D} giving the
  carrier's action against an opponent by the opponent's contract. This is the behavioural signature of a source over
  the contract alphabet, so there is no ambiguity between implication and policy, and no unspecified cases: against a
  contract-less opponent the carrier's play is whatever its source does, and the contract says nothing about it. C is
  the set of signatures realized by some source in L_8 (computed statically); its size is reported.
- **One evaluator for (p, c).** A reader p meeting an opponent y computes its action from its own source, where every
  box atom about y is evaluated against y's *contract* if y carries one (the contract gives y's guaranteed action
  toward p's contract class, or toward "none" if p carries no contract) and against y's *source* otherwise, through
  the legibility gate with budget b (illegible ⇒ the atom is false). Mutual self-reference between contracts is
  resolved as in the certificates-only Löb arm: contract-level statements are provability atoms. Certified
  implications are tested exhaustively against actual pairwise play for every (p, c, y, c_y) including mixed
  certified/uncertified encounters, before any run.
- **Validity.** (p, c) is valid iff, for every opponent source y and every contract c_y ∈ C ∪ {none}, the evaluator's
  action of p against (y, c_y) equals c(c_y) whenever c_y ≠ none. Validity is computed against the whole alphabet, not
  only against valid opponents, so it is not recursive. Only valid pairs exist: search assigns a source its own
  signature (unique, so there is no choice to preregister), inheritance copies the parent's contract, a source mutation
  whose inherited contract is invalid for the new source drops the contract, and a swap is refused when invalid. The
  full source–contract compatibility matrix is reported.
- **Carriers at start.** The initial carrier frequency f₀ ∈ {0, 0.01, 1} is an independent variable (at f₀ = 0 with
  s = 0, contracts can never arise, which is now a control, not a cell that could succeed).
- **Search.** A mutant source is born with its signature as contract with probability s ∈ {0, 1}.
- **Swapping.** At each birth, after inheritance, with probability σ ∈ {0, 0.1, 1} the newborn copies the contract of a
  donor drawn with probability ∝ exp(w·payoff) over the population, if valid for its source. **Control:** a uniform-donor
  variant, to separate breadth from donor fitness. **Neutral-label control:** the same copying applied to a label with
  no behavioural effect, to separate copying dynamics from selection. Accepted and rejected swaps are counted by
  contract.
- **Population-state hook:** present, set to true in v1.

## Objects [rewritten after review]

Swapping is a second operator, so the ε→0 chain does not represent it. These are finite-size mechanism results, not
limits, and are labelled as such.
1. **Finite-ε agent-based runs**, well-mixed, ε = 10⁻³ per birth, PD, w = 0.3, 3 seeds per cell, 10⁵ generations.
   Main grid at N = 6,400: b ∈ {2, 4, ∞} × s ∈ {0, 1} × f₀ ∈ {0, 0.01, 1} × σ ∈ {0, 0.1, 1}, minus cells that are
   controls by construction (s = 0, f₀ = 0). Start from all-D sources with carriers placed at random, and from a
   uniform-μ seed. **N path:** for the key cell (b = 2, s = 0, f₀ = 0.01, σ = 1) and its σ = 0 twin, N ∈ {1,600, 6,400,
   25,600}. Report composition time series (support), the transitions between dominant contract types, second-half
   P(C,C), carrier fraction, contract composition, swap routes, and the source-ALLC and contract-ALLC loads separately.
2. **The ε = 0 seeding lottery** (`src/almost_all_seeds.py`): sources and contracts seeded with carrier frequency f₀;
   cells (N, I) ∈ {(100, 4), (400, 4), (100, 64), (100, 256)}; **40 runs** per cell with Wilson intervals; b ∈ {2, ∞},
   σ ∈ {0, 1}, f₀ ∈ {0.01, 1}. Censoring (cells stopped for time) is recorded explicitly.
3. **Baselines:** the source oracle (b = ∞, no contracts); an unbounded reader using the contract evaluator (b = ∞,
   f₀ = 1), to show what contracts lose or change relative to source.

## RE predictions (Fable) [restated after review]

1. **Contracts restore legibility, where they are behaviourally matched.** At b = 2 with f₀ = 0, s = 0 (no contracts
   ever) the well-mixed run is below 0.3; with f₀ = 1 it is within 0.1 of the unbounded-reader-with-contracts baseline,
   which is itself within 0.05 of the source oracle (≈ 0.99 from E3), because a signature over the contract alphabet
   carries everything a modal reader uses. *Falsifier:* b = 2, f₀ = 1 below 0.6, or the contract-evaluator baseline more
   than 0.1 below the source oracle.
2. **Under swapping the FairBot-contract wins, and the uniform-donor control shows whether it is breadth or fitness.**
   With σ = 1 and payoff-weighted donors, the FairBot-contract holds ≥ 0.6 of carrying mass in the second half and the
   P*-contract < 0.1; with uniform donors the FairBot-contract still holds ≥ 0.5, which would show breadth (it is valid
   for the most sources) rather than donor fitness. With σ = 0 the composition tracks the prior mass of the carrying
   sources. *Falsifier:* P*-contract or a tag above the FairBot-contract at σ = 1, payoff-weighted. Sol predicts
   population dependence; the uniform-donor control is the test.
3. **Swapping spreads a contract from a small seed.** At (b = 2, s = 0, f₀ = 0.01): σ = 1 reaches second-half P(C,C)
   ≥ 0.8 at N = 6,400 and σ = 0 stays below 0.3, because swapping carries the contract from the 1% carriers to the whole
   core while inheritance alone cannot outrun the gate. Along the N path the σ = 1 value does not fall with N.
   *Falsifier:* σ = 1 below 0.6 at the key cell, or falling by more than 0.2 from N = 1,600 to 25,600.
4. **Source-ALLC and contract-ALLC loads.** Under mutation the source-ALLC load inside the cooperative mass is
   0.2–0.35 at every σ (Corollary 1's leak is unchanged by contracts), while the contract-ALLC load can differ: ALLC
   sources can carry only the all-C signature, so the two coincide when f₀ = 1 and diverge when f₀ < 1. *Falsifier:*
   source-ALLC load below 0.1 at b = ∞.
5. **Seeding lottery:** with f₀ = 1 the efficient fractions at b = 2 are within 0.15 of the free arm's at every cell
   (40 runs give ±0.15 near 0.5); with f₀ = 0.01, σ = 0 at b = 2 they are at least 0.3 lower at the I = 4 cells; σ = 1
   restores them to within 0.15. *Falsifier:* f₀ = 1, b = 2 more than 0.15 below the free arm at any cell.
6. **Neutral-label control:** the neutral label's composition under σ = 1 tracks donor abundance × fitness and does not
   concentrate on any label beyond 0.4; the FairBot-contract's concentration in 2 exceeds the neutral label's by at
   least 0.2. *Falsifier:* the neutral label concentrating as strongly as the FairBot-contract.

**What it would mean.** If 1–3 hold, a contract is the mechanism by which bounded readers recover the free arm:
legibility becomes a shared, transmissible good, and transmission from a small seed selects the broadest valid
guarantee, which would be the first result where *which* cooperative network wins is decided by something other than
prior mass or a moat; 2's uniform-donor control says whether it is breadth or donor fitness. If 2 fails toward tags or
P*, swapping selects narrow guarantees and the RS's "hide your strength" concern applies to contracts too. 4 is the
reminder that contracts solve legibility, not re-injection.

## RS predictions (Jacob)

(From the pitch, recorded before the run: with a rich enough contract set this limits to the free-proof case; the one
unfit component is the program that defects on anyone whose cooperation it can prove, and he predicts it does poorly.)

## Procedure for the subagent

Follow CLAUDE.md discipline. Commit `predictions/2026-10-04-proof-carrying-contracts.md` carrying the RE and RS
predictions above after measuring only language sizes and the contract-class count; then compute validity breadth
(static), then run. At most 3 workers; stop cells projected beyond 2 hours; do not edit RESULTS.md, REJECTED.md,
THEORY.md, CLAUDE.md or DEFERRED.md; do not touch `runs/d8dcd7ee9a/row.json`; hand back draft RESULTS, REJECTED,
THEORY and DEFERRED text, at most 5 lines on what matters, and the branch and commits.
