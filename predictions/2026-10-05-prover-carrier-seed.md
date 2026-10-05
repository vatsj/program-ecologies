# Predictions: prover-carrier seed at b = 0, 2026-10-05

Spec: `specs/2026-10-05-prover-carrier-seed.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-05-prover-carrier-seed-gpt-6.1-sol.md`).
Committed before the static invasion diagnostics and before any seeded run. This is an invasion/establishment experiment
at finite sizes; finite-ε cells are about approach and establishment, not π, and nothing here is a large-population
efficiency claim.

## Measured before commit

- Type tables regenerated from `src/contracts_static.py` and `src/contracts_static_b0.py`; they match the committed
  static JSONs except for timing fields.
- **Establisher set** at n = 8 (free game: self-cooperates and defects on D): 118 canonical sources in 96 classes, μ mass
  0.0242 (canonical-normalized unit, as in `contracts_abm`). FairBot, `BOX1(THEM(ME))`, `BOX(THEM(THEM))` and
  `BOX1(THEM(THEM))` hold 0.2085 of it each (0.834 together); the probe-readers `BOX(THEM(^C))`, `BOX1(THEM(^C))` 0.063
  each. Every establisher's own carrier self-cooperates at b = 0 and defects on D.
- **Kernel.** `src/prover_carrier_seed.py` is `contracts_abm._run` with added counters and lineage tracking and an
  unchanged random-number sequence: a μ-seed b = 0 job (f₀ = 0.01, rep 0, σ ∈ {0, 1}, 1,000 generations) gives
  bit-identical P(C,C), carrier fraction and swap counts through both kernels.
- **Timing** (load average ≈ 12): 2,000 generations at N = 6,400 take 1.9 s at b = 0 (D sea) and 1.3 s at b = ∞, so a
  10⁵-generation cell is about 1.5–3 min and N = 25,600 about 6–12 min. No reduction of the N sweep or of replicates is
  needed; none is made.

## Design choices fixed before the run (where the spec leaves room)

1. **Seeds.** 'mix': iid μ, then exactly round(f₀·N) slots (uniform without replacement) are replaced by carriers whose
   sources are drawn from the 118 establisher sources ∝ μ, each carrying its own signature. 'fb': the same slots, every
   carrier FairBot. The initial population depends only on (seed, f₀, N, I, rep), so σ, b and the contract toggle are
   paired on identical populations and placements. f₀ ∈ {0.001, 0.003, 0.01, 0.03, 0.1} → 6 / 19 / 64 / 192 / 640
   carriers at N = 6,400.
2. **Finite ε main grid:** b = 0, s = 0, ε = 10⁻³, w = 0.3, PD, 10⁵ generations, statistics over the second half,
   samples every 20 generations, carriers counted every generation. {mix, fb} × 5 f₀ × σ ∈ {0, 1}; 5 seeds per cell and 20
   at f₀ ∈ {0.001, 0.003}.
3. **Success** in a finite-ε run = second-half P(C,C) ≥ 0.9 (the threshold in RE prediction 1). Success fractions carry
   Wilson 95% intervals; mean P(C,C) is reported with min–max over seeds.
4. **Carrier statistics.** Carrier = an agent carrying any contract. Reported: fraction over time, first generation at
   ≥ 10% and ≥ 50%, the carrier count at generations 10…10⁵, early growth rate log(k₂₀₀/k₀)/200, extinction (count hits 0;
   absorbing at s = 0 because no contract is created), carrier-conditional P(C,C) (pairs of carriers), contract and
   source composition. **Lineage:** each agent records its genealogical founder (initial slot) and its contract's founder;
   for the final carriers we report the number of founders, the share whose founder was a seed carrier, and the share
   whose contract came from another lineage (acquisition by swapping, as opposed to lineage expansion).
5. **Transition counts per run:** mutations; mutations of carriers split into kept (contract valid for the new source) and
   lost (invalid, dropped); contracts created (0 by construction at s = 0); swaps accepted / same / rejected / donor
   without contract; accepted swaps onto a recipient with no contract; accepted swaps across lineages. Rates are per
   birth.
6. **ε = 0 twins** of every main cell: same populations, ε = 0, run until outcome-frozen (every present type pairwise
   payoff-identical, the lottery certification) or 10⁵ generations (then censored as metastable/unresolved, not counted
   as failure). 20 runs per twin cell (they stop early and are cheap). Efficient = P(C,C) ≥ 0.95 at the freeze.
7. **Controls.** (i) b = ∞, same populations, σ = 0; (ii) b = 0, same source multiset and placement, contracts removed,
   σ = 0 (σ has nothing to copy); both at the main grid's replicate counts, with ε = 0 twins (20 runs). (iii) the
   published μ-drawn f₀ = 0.01 b = 0 cell rerun at σ ∈ {0, 1}, reps 0–4, with contracts_abm's seeding; reps 0–2 are the
   published runs and must reproduce exactly.
8. **N sweep** at f₀ = 0.01, mix seed: N ∈ {1,600, 25,600} added to the N = 6,400 main cells, σ ∈ {0, 1}, 5 seeds at
   finite ε; plus ε = 0 twins at σ = 0 with 20 runs.
9. **Lottery.** `contracts_abm`'s lottery mode (the `almost_all_seeds` conventions: complete island graph, mN = 1 migrant
   per island per generation, N per island, iid μ seeding, outcome-frozen certification, 10⁵-generation horizon,
   censored runs reported separately), with exactly k carriers per island at uniform slots, sources drawn from the
   establishers ∝ μ, placement recorded. Cells (N, I, k): (100, 4, 0), (100, 4, 1), (100, 4, 3), (100, 4, 16),
   (100, 64, 0), (100, 64, 1), (100, 64, 3); 40 runs each. Fixed total of 64 carriers: (100, 4, 16) against (100, 64, 1).
   σ = 0 is primary; σ = 1 repeats every k ≥ 1 cell as a secondary check.
10. **Static diagnostics** (`src/prover_carrier_static.py`, before the runs): pairwise action and payoff matrix of the
    seeded carrier types against each other and against the μ background at b = 0; the Moran-replicator growth rate
    (per generation, fitness exp(w·payoff)) of a rare carrier of each seeded type at frequency 10⁻³ against three
    backgrounds: μ, the non-carrier flow at the moment ALLC first falls below 10⁻³, and the ε = 10⁻³ mutation–selection
    equilibrium of the non-carrier system; **f\*** = the smallest carrier frequency (mix composition, and FairBot alone) at
    which the carriers' fitness exceeds the background's mean fitness, against each background; and the deterministic
    threshold of the full type-level Moran-replicator(-mutator) flow started from each seeded state (with mutation
    stripping invalid contracts).

## RE predictions (Fable, from the spec)

1. **A prover-carrier seed spreads, above a threshold set by carrier–carrier encounters.** The static invasion fitness of
   a rare carrier in the μ background at b = 0 is negative or neutral while ALLC is present and positive once D has eaten
   ALLC and carriers meet each other at frequency above a threshold f*; f* ≈ 0.003–0.01 at N = 6,400. Second-half
   P(C,C) ≥ 0.9 at f₀ ≥ 0.03 in at least 4 of 5 seeds; at f₀ = 0.01 in at least 3 of 5; at f₀ ≤ 0.003 a drift lottery
   with 2–12 of 20 seeds. Where it succeeds, the carrier fraction passes 50% within 2·10⁴ generations. The homogeneous
   FairBot seed does at least as well as the mixture. *Falsifier:* f₀ = 0.03 below 0.5 in 3 or more seeds, or the static
   invasion fitness positive at every frequency (no threshold) with f₀ = 0.01 still failing.
2. **Swapping is inert where measured transfer is negligible.** The accepted-swap rate onto non-carrier sources is below
   10⁻⁴ per birth in every cell, and σ = 1 changes second-half P(C,C) by less than 0.05 at every f₀. *Falsifier:* an
   accepted-transfer rate above 10⁻³ per birth, or a σ effect above 0.2.
3. **The contract is what spreads.** Control (ii) stays below 0.1 at every f₀; control (i) at b = ∞ is ≥ 0.9 at every
   f₀ ≥ 0.003. *Falsifier:* control (ii) above 0.5 at any f₀.
4. **Lottery.** k = 0 below 0.1 in both cells. With 64 carriers in total, 1 per island on (100, 64) beats 16 per island
   on (100, 4), each at least 0.2 above k = 0, with intervals. The direction of the I effect at fixed k is not predicted.
   *Falsifier:* 1-per-island on (100, 64) not above k = 0 by its interval.

## RS predictions (Jacob)

His standing intuition: a small seed spreads to every program that can carry it.

## Subagent predictions (Opus, from a hand calculation before the static diagnostics)

The hand calculation: for a FairBot-like carrier in a background of D (share d) and ALLC (share a), at b = 0 the carrier
gets R = 0 from carriers and ALLC and P = −1 from D, while D gets P from carriers, T = 1 from ALLC and P from D; so
carrier minus D = f − a in payoff. Under mutation at ε a carrier lineage also loses ≈ ε per generation (FairBot's contract
is valid for 7 sources of μ mass 0.005, so a mutated carrier almost always drops it). The deterministic threshold is
therefore f* ≈ a + ε/w: a ≈ 0.47 at μ, ≈ 0 after the scramble at ε = 0, and a ≈ ε·μ(ALLC)·(lifetime of an ALLC
mutant, ≈ 4 generations) ≈ 2·10⁻³ at ε = 10⁻³. Above f*, the advantage w(f − f*) is frequency-dependent, so the binding
barrier at small seeds is drift, with a diffusion fixation chance of about erf(f₀·√(wN/2)) at ε = 0.

- **S1 (static).** At the μ background the rare-carrier growth rate is negative for every seeded type. After ALLC's
  extinction at ε = 0, f* < 0.002 (no deterministic threshold beyond ALLC); at the ε = 10⁻³ equilibrium f* lies in
  [0.002, 0.015]. *Falsifier:* post-ALLC f* > 0.002 at ε = 0, or the ε = 10⁻³ f* outside [0.002, 0.015].
- **S2 (ε = 0 twins).** Efficient fractions roughly 0–0.15 / 0.05–0.3 / 0.2–0.6 / 0.6–0.95 / ≥ 0.95 at f₀ = 0.001 / 0.003
  / 0.01 / 0.03 / 0.1 (mix, σ = 0). *Falsifier:* f₀ = 0.01 outside [0.1, 0.75], or f₀ = 0.1 below 0.85.
- **S3 (finite ε).** Below the twins at f₀ ≤ 0.003 (the mutation-stripping threshold sits above those seeds): f₀ = 0.001
  succeeds in ≤ 1 of 20 seeds and f₀ = 0.003 in ≤ 4 of 20; f₀ = 0.01 in 1–4 of 5; f₀ = 0.03 in ≥ 4 of 5; f₀ = 0.1 in
  5 of 5. Successful runs reach second-half P(C,C) ≥ 0.97 with carrier-conditional P(C,C) ≥ 0.95. *Falsifier:* f₀ = 0.003
  succeeding in ≥ 8 of 20, or a successful run below 0.95.
- **S4 (N sweep).** At fixed f₀ = 0.01 success rises with N (f₀·√(wN/2) = 0.21 / 0.42 / 0.85). *Falsifier:* the ε = 0
  twin success fraction at N = 25,600 not above N = 1,600 by more than the intervals' overlap (i.e. the 25,600 interval's
  lower end below the 1,600 point estimate).
- **S5 (lineage).** Final carriers descend genealogically from seed carriers (share ≥ 0.99), and the share whose contract
  came from another lineage is < 0.01 at σ = 1: spread is lineage expansion, not acquisition. Accepted swaps onto
  contract-less recipients are < 10⁻⁵ per birth. *Falsifier:* cross-lineage share ≥ 0.05 in any successful σ = 1 run.
- **S6 (lottery).** k = 1 on (100, 64) and k = 16 on (100, 4) both ≥ 0.8, with their difference inside ±0.15 (the RE's
  ordering will not be resolved at 40 runs); k = 1 on (100, 4) ≈ 0.1–0.35. *Falsifier:* either fixed-total cell below 0.6.

## Addendum before any seeded run (2026-10-05, 01:40): reduction of the window, predeclared

Committed after the static diagnostics (`runs/prover_carrier_static.json`) and before any seeded run, except one 300-generation
smoke test of the kernel (mix seed, f₀ = 0.03, σ = 1, rep 0), which I disclose: its carriers passed 50% at generation 70
and P(C,C) over generations 160–300 was 0.99. The static diagnostics are reported with the results; they do not change
any prediction above.

**Why.** The machine's lid is closed (`AppleClamshellState = Yes`): the system sleeps between dark wakes, and a first
pool of 3 workers accumulated about 3 CPU-minutes each in 98 wall-minutes without finishing one job. The full grid
(470 finite-ε jobs at 10⁵ generations) is not feasible at that rate.

**Reductions (all predeclared, none conditioned on outcomes):**
1. Every finite-ε cell runs **2·10⁴ generations**, statistics over the second half (generations 10⁴–2·10⁴). The
   deterministic flow and the smoke test put takeover at 10²–10³ generations, so the 50%-within-2·10⁴ clause of RE
   prediction 1 stays testable; what is lost is the long-window metastability check (a shadow-driven collapse after
   2·10⁴ generations would be missed). A **long-window check** at 10⁵ generations (mix seed, f₀ ∈ {0.01, 0.1}, σ ∈ {0, 1},
   3 seeds) runs last if time allows; otherwise it is reported as not run.
2. **N sweep:** N = 1,600 at 5 seeds per σ; **N = 25,600 at 3 seeds per σ**, both at 2·10⁴ generations, run after the
   lottery. The ε = 0 N-sweep twins keep 20 runs.
3. Control (iii), the μ-drawn f₀ = 0.01 cell, runs at 2·10⁴ generations with the published seeds; exact reproduction of
   the published 10⁵-generation statistics is replaced by the kernel-equivalence check already recorded above
   (bit-identical through both kernels).
4. **Order:** main grid → ε = 0 twins → controls (i), (ii) and their twins → control (iii) → lottery → N sweep →
   long-window check. Any cell projected beyond about 2 hours of wall time is stopped and recorded as administratively
   censored with its completed generations.
5. The thresholds in every prediction are unchanged; "second half" now means generations 10⁴–2·10⁴.

## Addendum 2 (2026-10-05, 03:20): stop at carrier extinction

Five f₀ = 0.001 main runs (mix, σ = 0, reps 0–4) finished under the reduced window before this change; each took
2,000–2,400 wall-seconds with the lid closed, and their carriers died at generations 3–13. With s = 0 a contract is never
created, so once carriers are extinct the run is exactly the no-contract b = 0 process (published P(C,C) 0.001–0.003)
for the rest of its window. From here on a finite-ε run with s = 0 stops when the carrier count first reaches 0; it is
recorded as a failure with its extinction generation and its P(C,C) at that moment, and it is left out of mean-P(C,C)
statistics (which are over runs run to the end). The five finished runs are kept as they are. ε = 0 twins and lottery
runs are unchanged (they stop at the freeze). No prediction or threshold changes.
