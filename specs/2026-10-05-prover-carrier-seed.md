# Spec: does a small seed of prover carriers spread where legibility is lost? 2026-10-05

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-05-prover-carrier-seed-gpt-6.1-sol.md`) and revised; changes marked [after review]. Committed before launch. To be run by an Opus subagent.

[after review] This is an *invasion/establishment* experiment at finite sizes. It distinguishes lineage expansion (carriers reproducing) from contract acquisition across source classes (which validity nearly forbids), and it does not establish large-population efficiency or spread "to every program that can carry it".

## Why

RESULTS "Proof-carrying contracts v1" found that where a gate removes legibility (b = 0, only constants legible from
source), carried contracts restore cooperation from 0.001 to 0.95–0.99, but a μ-drawn 1% carrier seed dies out at
every swap rate. The RS had expected a small seed to spread to every program that can carry it. The μ-drawn seed
conflates carrier rarity with prover rarity: 94% of it is ALLC and D, leaving about one prover carrier at N = 6,400.
This spec tests the RS's intuition with the design it needs: a seed of *prover* carriers.

## Design

`src/contracts_abm.py` (the contracts kernel, b = 0 gate, Löb contract reads), modal n = 8 sources, PD, w = 0.3.

[after review] **Transition rules, stated.** A birth copies the parent's source and contract. With probability ε the
child's source mutates to a μ-draw; the inherited contract is kept iff valid for the new source, else dropped; with
s = 0 no contract is ever created by search, so mutation cannot create carriers. A swap (probability σ at birth)
copies a payoff-weighted donor's contract iff valid for the child's source. Counts of contract creation, loss by
invalid inheritance, swap rejection and swap acceptance are reported per cell. A generation is N births.

[after review] **Static diagnostics first.** Before any long run: the pairwise action and payoff matrix of the seeded
carrier types against each other and against the μ background at b = 0; the deterministic invasion fitness of a rare
carrier of each type in the μ background (replicator growth rate at frequency 10⁻³, with the background at its μ
composition and after D has eaten ALLC); and the frequency at which carrier–carrier encounters make the carrier's
fitness exceed the background's. These say whether a threshold exists before the runs do.
- **Carrier seed:** the population is drawn iid from μ, then a fraction f₀ of slots is replaced by carriers whose
  sources are drawn from the *establisher* classes in proportion to μ, each carrying its own signature as contract.
  f₀ ∈ {0.001, 0.003, 0.01, 0.03, 0.1}; at N = 6,400 that is 6 / 19 / 64 / 192 / 640 carriers. [after review] Also a
  **homogeneous FairBot-carrier seed** at the same f₀, to separate transmissible legibility from a mixture effect.
- **Finite ε** (ε = 10⁻³ per birth, 10⁵ generations; 5 seeds per cell, 20 at the boundary cells f₀ = 0.001 and
  0.003): b = 0, s = 0, σ ∈ {0, 1}. Report P(C,C) over time and in the second half, carrier-conditional P(C,C), the
  carrier fraction over time, the times at which carriers first exceed 10% and 50%, early growth rate and extinction
  probability of the carrier lineage, contract and source composition, and lineage ancestry of the final carriers.
  [after review] **ε = 0 well-mixed twins** of every cell, to separate seed invasion from mutation-supported
  cooperation. **N sweep** at f₀ = 0.01: N ∈ {1,600, 6,400, 25,600}.
- **Controls:** (i) the same seeds at b = ∞; (ii) the *same source multiset and placement* at b = 0 with the contracts
  toggled off [after review: only the contract differs]; (iii) f₀ = 0.01 μ-drawn carriers at b = 0, the published
  failing cell, rerun with the same seeds.
- **ε = 0 lottery** (`src/almost_all_seeds.py` kernel with carriers; N per island, mN = 1 migrant per island per
  generation, certification and censoring as in the seeds runs): (N, I) ∈ {(100, 4), (100, 64)}, b = 0, with exactly
  k prover carriers per island, k ∈ {0, 1, 3}, 40 runs per cell. [after review] Plus a **fixed-total-carrier**
  comparison: 64 carriers in total, placed as 16 per island on (100, 4) or 1 per island on (100, 64), with placement
  recorded, so the island-number effect is not confounded with the number of seeded copies.

## RE predictions (Fable)

1. **A prover-carrier seed spreads, above a threshold set by carrier–carrier encounters** [after review]. The static
   invasion fitness of a rare carrier in the μ background at b = 0 is negative or neutral while ALLC is present (a
   carrier gets R from ALLC where D gets T) and positive once D has eaten ALLC and carriers meet each other at
   frequency above a threshold f* that the static diagnostic computes; I predict f* ≈ 0.003–0.01 at N = 6,400. So:
   second-half P(C,C) ≥ 0.9 at f₀ ≥ 0.03 in at least 4 of 5 seeds; at f₀ = 0.01 in at least 3 of 5; at f₀ ≤ 0.003
   success is a drift lottery with 2–12 of 20 seeds. The carrier fraction, where it succeeds, passes 50% within
   2·10⁴ generations. The homogeneous FairBot seed does at least as well as the mixture. *Falsifier:* f₀ = 0.03 below
   0.5 in 3 or more seeds, or the static invasion fitness positive at every frequency (no threshold) with f₀ = 0.01
   still failing.
2. **Swapping is inert where measured transfer is negligible** [after review: conditioned]. The accepted-swap rate
   onto non-carrier sources is below 10⁻⁴ per birth in every cell, and σ = 1 changes second-half P(C,C) by less than
   0.05 at every f₀. *Falsifier:* an accepted-transfer rate above 10⁻³ per birth, or a σ effect above 0.2.
3. **The contract is what spreads.** Control (ii), the same provers without contracts at b = 0, stays below 0.1 at
   every f₀, since illegible provers defect on each other. Control (i) at b = ∞ is ≥ 0.9 at every f₀ ≥ 0.003.
   *Falsifier:* control (ii) above 0.5 at any f₀.
4. **Lottery** [after review: restated with the fixed-total comparison]. With k = 0 both cells are below 0.1. With
   64 carriers in total, 1 per island on (100, 64) beats 16 per island on (100, 4) (more independent establishment
   trials), each by at least 0.2 over k = 0, with intervals. The direction of the I effect at fixed k is not
   predicted. *Falsifier:* 1-per-island on (100, 64) not above k = 0 by its interval.

**What it would mean.** If 1 and 3 hold, the RS's intuition is right for the seed it presupposes and above a
threshold: a small population of proof-carrying provers takes over a population that cannot read source, through
inheritance of the carried proof, once carriers meet each other often enough; legibility is a transmissible good at
the level of lineages, with an establishment threshold like any conditional cooperator's. The earlier failure was
about μ-drawn seeds, not about carrying. If 1 fails everywhere, carrying is not advantageous enough at b = 0 to
overcome drift from tens of copies, and contracts restore legibility only from an established carrier majority.
[after review] Alternatives the controls address: carrier enrichment selecting a prover clique rather than
transmissible legibility (the homogeneous seed and the composition say which); cooperation needing a
mutation-maintained defector fringe (the ε = 0 twins); metastability before shadow invasion (the time series).

## RS predictions (Jacob)

(His standing intuition: a small seed spreads to every program that can carry it.)

## Procedure for the subagent

Follow CLAUDE.md discipline. Commit `predictions/2026-10-05-prover-carrier-seed.md` carrying the RE and RS predictions
before any run. At most 3 workers; stop cells projected beyond 2 hours and say so; do not edit RESULTS.md,
REJECTED.md, THEORY.md, CLAUDE.md, DEFERRED.md or NOTATION.md; do not touch `runs/d8dcd7ee9a/row.json`; hand back draft
RESULTS, REJECTED, THEORY and DEFERRED text, at most 5 lines on what matters, and the branch (`git branch
--show-current`) and commits.
