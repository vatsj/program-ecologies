# Spec: a path in (N, I, mN) on which islands nucleate independently and rival networks still resolve, 2026-10-05

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-05-island-path-gpt-6.1-sol.md`) and revised; changes marked
[after review]. To be run by an Opus subagent. Follow-up to RESULTS "Rival networks across islands, and the mN
rule" and "The demographic lemma" (DEFERRED 1, new open item).

## Why

The seed lottery's two halves now pull against each other. Independent nucleation needs the replacement fraction
during nucleation small, x = mN·T_nuc/N ≲ 0.3 (so mN ≲ 0.3·N/T_nuc(N) ∝ N^0.7); resolving rival networks needs
migration strong relative to the coordination barrier N·w/4, whose single-migrant hazard ρ_DD(N) falls exponentially
(1.85·10⁻⁵ at N = 100, 7·10⁻⁹ at 200). At N = 100 both can hold with mN ≈ 1 on a 10⁴-generation horizon; at N = 200
the patchwork effectively never resolves. The establishment formula says p(N) → 1 along N alone at fixed cutoff
(0.98 at N = 25,600), so the N ≫ I path does not need many islands at all; the I ≫ N path, which the RS proposed
(islands growing faster than their count is "sufficient but not necessary"), is where rivals are a risk. The
operating hypothesis is that island-level efficiency is the claim and metapopulation universality is not claimed
beyond N ≈ 100. This spec asks whether that concession is forced. [after review] Throughout, rival persistence,
universality and efficiency are three different outcomes: every cell reports island-level P(C,C) (within-island
encounters, the realized object) and the counterfactual cross-island P(C,C) under uniform mixing separately, and a
patchwork that fails to homogenize is not reported as inefficient.

Two mechanisms could resolve rivals without single-migrant fixation:
- **Clustered immigration.** k migrants arriving together fix with probability 0.0097 at k = 20 and 0.22 at k = 40 on
  an N = 100 island (RESULTS "Rival networks"). A migration rule that moves a *propagule* of size k drawn from one
  source island instead of one individual has a hazard that depends on k/N, not on e^{−N w/4} [after review: the
  scaling variable is k/N, so k/N-matched cells are included].
- **Nucleation-time asymmetry.** Rivals that nucleate later are rarer; if the first network to establish anywhere
  colonizes faster than the second can nucleate, the patchwork never forms. The rival run found 0.70 of majorities
  go to the network with more local establishments before the first immigrant-founded island.

And one object the rival run did not measure: the **bridge**, a class cooperating with both rivals, which gained
share from the conflict. A bridge-rich prior may resolve rivals by absorption rather than by fixation; absorption
and replacement are competing mechanisms and are reported separately [after review].

## Definitions [after review]

- **Nucleation event** of an island: the first generation at which its holder (the holder rule of the rival run:
  the class with the plurality of the island, provided it is a certified cooperator) is a cooperator. **T_nuc(N):**
  the median of that time over islands in **m = 0, iid** runs at each N (calibrated at N = 100, 200, 400 in this run,
  with the full distribution; the rival run's N^0.32 is an extrapolation and is not used for N = 200 without the
  calibration).
- **q:** the number of islands whose holder at the horizon has *local* ancestry (founded by a locally seeded copy,
  per the kernel's ancestry labels) divided by the same count in the m = 0 reference at the same (N, I, seeds).
  Measured on iid ancestry-tagged runs, never on pre-seeded ones.
- **Boundary path:** mN(N) = 0.3·N/T_nuc(N) with the calibrated T_nuc.
- **Both-present:** both rival networks hold at least one island (holder rule) at the horizon. **Successful
  invasion:** a migrant lineage becomes the holder of a recipient island. **Global resolution:** one network holds
  every cooperative island. The **separation-loss hazard** is per metapopulation-generation, with the exposure
  denominator the number of islands held by the minority network; the single-migrant reference is
  mN·ρ_DD(N) per recipient island-generation. Invasions and global resolution are reported separately.
- **Propagule migration:** at each migration event the kernel draws k individuals without replacement from one
  uniformly chosen source island (its composition, so propagules can be mixed) and replaces k uniformly chosen
  residents of the recipient simultaneously; donors do not lose individuals (migration is a birth of offspring
  copies, as in the single-migrant kernel, so k = 1 is exactly the current rule). Flux is matched: mN/k propagule
  events per island-generation. Validated against an unskipped reference implementation on small cells
  (N = 50, I = 4, 10³ generations, identical seeds), since the default-kernel regression does not validate the batch
  path.
- Recorded per island: first establishment time, first immigrant-founded island time, second rival's first
  establishment time, extinction times of each network, with binomial intervals on every fraction and predeclared
  verdicts for the gaps between prediction and falsifier thresholds.

## Design

Kernel `src/rival_islands.py` (exact skipping, lumping, ancestry), modal arm, n = 9, w = 0.3, ε = 0, iid seeds,
complete island graph, horizon 10⁵ generations.

0. **Calibration and statics.** m = 0 iid runs at N ∈ {100, 200, 400}, I = 16, 40 runs: T_nuc distributions.
   Static one-direction fixation probabilities of A into B, B into A, bridge into A, A into bridge, bridge into B,
   B into bridge, for single migrants and for propagules of k ∈ {10, 30, 60} at N ∈ {100, 200, 400} (10⁴ runs
   per cell on one island) [after review].
1. **The scaling path.** N ∈ {100, 200, 400}, I ∈ {16, 64}, mN on the calibrated boundary, with the separated
   pre-seed of pair 3 (P\*, no bridge) and pair 1 (bridge `BOX1(THEM(THEM))`), 40 runs per cell; plus iid
   ancestry-tagged runs at the same cells for q. Report q, the separation-loss hazard with KM survival, invasions,
   global resolution, both-present, and both P(C,C) objects.
2. **Propagule migration.** The pre-seeded cells at N = 200 and 400, I = 16, with k ∈ {1, 10, 30} and the
   k/N-matched k = 60 at N = 400, at the boundary flux, 40 runs per cell; q from matching iid tagged runs. Report
   q (clustering may help or hurt nucleation; bursts can destroy near-critical founders or import coordinated
   competitors, and migration-free intervals can help), the hazard against the static k-propagule fixation
   probability, invasions, and both-present.
3. **Natural separation along the path.** iid only, N ∈ {100, 200}, I ∈ {64, 256}, mN on the boundary, 300 runs
   per cell (100 at N = 200, I = 256): ever-separated and horizon-separated, the bridge's final share of islands, and
   the comparison sol asked for: the measured colonization time (first immigrant-founded island) against the
   interval between the first and the second rival's establishment.
4. **The bridge test.** Pre-seed one island with A, one with B and one with the bridge, N = 100, mN ∈ {0.1, 1},
   I = 16, 40 runs: the bridge's share of islands over time, its invasion probabilities in each direction (from 0),
   and whether it ends holding the majority; a control with the bridge pre-seeded alone against the iid background
   (its share without a conflict, to separate conflict mediation from intrinsic dominance or prior abundance).
   For runs of 1–2 ending with both present at N = 200, the merge test as in the rival run, reported as conditional
   on survival.

Cell priority fixed: 0 → 1 → 3 → 2 → 4; ≤ 3 workers; report hours per cell; stop where time runs out and say so.

## Required outputs

`runs/island-path.md` and `.json`, extensions of `src/rival_islands.py` (propagule migration as an option with the
default untouched and its validation cells rerun; the unskipped reference for the batch path), a predictions file
from the spec committed before any counted run, and the usual hand-back (draft RESULTS, REJECTED, THEORY §3 and
DEFERRED 1 edits, NOTATION, ≤ 5 lines, branch from `git branch --show-current`, commits).

## RE predictions (with falsifiers)

1. **On the boundary path, rivals resolve only at N = 100.** At N = 100: both-present at the horizon ≤ 0.2 for
   pair 1 and ≤ 0.5 for pair 3. At N = 200 and 400 on the boundary: both-present ≥ 0.8 for pair 3 and the hazard
   ≤ 10⁻⁵ per minority-island-generation, with q ≥ 0.75 everywhere on the path. *Falsifier:* both-present ≤ 0.5 for
   pair 3 at N = 400 on the boundary, or q < 0.6 on the boundary. Gap (0.5–0.8): inconclusive, predeclared.
2. **Propagules resolve rivals when k/N ≥ 0.15** (both-present ≤ 0.3 at k = 30, N = 200 and at k = 60, N = 400),
   **and not at k/N = 0.075** (k = 30, N = 400: both-present ≥ 0.6) [after review: k/N is the variable]; the effect
   on q is uncertain in sign and the RE predicts |Δq| ≤ 0.3 at matched flux. *Falsifier:* k/N = 0.15 leaves
   both-present ≥ 0.7 at N = 400, or |Δq| ≥ 0.4.
3. **Natural horizon separation stays below 0.05 at N = 100 on the boundary and grows with I at N = 200** (sol's
   point: more islands, more chances for a second rival to nucleate before colonization reaches it), reaching
   ≥ 0.05 at (200, 256); the colonization time is shorter than the first-to-second-rival interval at N = 100 and
   not at N = 200. *Falsifier:* horizon separation ≥ 0.1 at (100, 256), or separation at (200, 256) below (200, 64).
4. **The bridge grows during conflict** (its island share at the horizon exceeds its no-conflict control share by
   ≥ 0.1 at mN = 1) **but majority is not assured** (the RE predicts majority in 0.3–0.6 of runs at mN = 1 and
   ≤ 0.3 at mN = 0.1). *Falsifier:* the bridge's share not above its control at mN = 1, or majority ≥ 0.8.

The RS is invited to add predictions; the uncertain ones are 2's q clause and 3's growth with I.
