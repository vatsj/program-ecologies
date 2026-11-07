# Spec: majority division in the current object (seed lottery with the annealed tail, finite N and islands), arms M and T, 2026-11-07

Status: reviewed by gemini-4-argon (folded [after review]) and gpt-6.1-sol (`--mode amended`, folded [after second
review]); to be run by a
Sonnet subagent on Daytona (`tools/daytona_run.py`). Queue 74. The RS said "Go" on 2026-11-07 to the RE's next-queue item
1: "majority division (pair worth a = 1) in the current object, arms M and T". The run is the one the OH doc's Theory tab
names under §3 a = 1: "Run majority division in the current object (seed lottery with the annealed tail, finite N and
islands, migration in the calibrated band; arms M and T) to score both predictions; after the tail-only run (queue 71)
reports."

## Context

The object (OH doc h01/h03, RS 2026-11-01): islands seeded i.i.d. from the prior, then selection and migration under a
light annealed mutation tail drawn from the founding prior (RS 2026-11-02: "the founding prior and the mutation prior
are both the length prior of the language; any other arrival law is overfitting"). The target (h11, RS 2026-10-29/31):
every island in V\* = the three fair pairs, each pair equally likely across independent worlds.

What exists, and what each lacks:

| run | finite N in-island | finite I | migration | tail | arm M | arm T |
|---|---|---|---|---|---|---|
| queue 64, "Churn among the fair pairs" | yes (N = 100) | 64 | mN ∈ {0, 0.01, 0.1, 1} | no (ε = 0) | B6m | T-lo/main/hi |
| queue 69, "Arm T under islands to infinity" | founding only | ∞ (ODE) and 64–65,536 (jump chain) | rare migration | founding only | – | yes |
| queue 71, "Annealing the unequal basin" | no (fixation table) | ∞ (ODE) | rare migration | yes | object P truncation | yes |
| queue 73, pair-worth along N | yes | 64 | mN ∈ {0, 1} | yes | – (other game) | – |

Tail-free at N = 100 (queue 64, V\* share at generation 10,000, 40 runs, mN = 0 / 0.1 / 1): B6m (arm M) 0.27 / 0.60 /
0.70; B6w (arm L) 0.27 / 0.56 / 0.82; T-main 0.53 / 0.97 / 1.00. Queue 31 ("Stable sets on islands") found migration
settling a fair pair at N ≤ 150 and an unequal pair at N ≥ 200 in the DSL. Queue 71 (mean field, I → ∞): the prior's own
tail leaves M's natural start unequal at every tested dose (to Λ = 10⁵), because it re-supplies the ⅓ constants and two
Trojan bullies per slot that hold the unequal basin; a tail without them flips M at Λ\* ≈ 35–55 (N = 100), with Λ\*
growing faster than N; arm T has no basin and the tail changes nothing.

Recorded predictions to be scored (Theory tab §3, 2026-11-01, before any run of the current object):
- **The RS:** "under the current operating hypotheses (finite N and islands, the annealed tail, the ⅓ – ½ – ⅔ grid),
  majority division does not land in V\*. No claim about the limit object."
- **The RE:** "agreed for the DSL arms under the length prior; for arm T, V\* on at least 0.9 of islands at N ≤ 200,
  unresolved at N = 400."

REJECTED.md checked. Does not re-open: farsighted clauses, contracts or the veto (out of the object; DEFERRED 15), the
clean tail as a remedy (RS 2026-11-02: clean-tail runs are diagnostics; it appears here only as diagnostic D1), equal
likelihood as within-world coverage (RS 2026-10-31: a lottery across worlds).

**What it is for.** It is the first run of majority division in the object as the RS now defines it. [after second
review: claims restricted to tested cells and schedules] If arm T meets the target in the tested cells while M fails,
the two recorded predictions are scored and the next question is the realizable prior (h03's exception); if T fails at
finite N and I, the mean-field result (queue 69) does not carry over to these sizes and schedules. A fixed I = 64 and
a horizon ∝ N cannot separate a basin from slow escape, and the M–T contrast compares two packages (library, prior,
evaluator, cost), not the causal value of reading.

## The object

- Game: `dollar3` (three-player majority division, nine actions per slot: name a partner or the grand coalition with
  demand ⅓, ½ or ⅔; Nash demand rule; `src/dollar3.py`). Outcome classes as `many_islands.CATMAP`: F fair pair, U unequal
  pair, G grand (sum = 1), W wasteful, D disagreement.
- Islands: three slot populations of N each, mean-field expected payoffs, Moran birth–death with fitness exp(w·payoff),
  w = 0.3, as queue 64 (`churn_primary.py`, `migration_window_kernels.kern_mw`).
- Founding: N founders per slot drawn i.i.d. from the arm's seed law, independently per island.
- Migration: m = mN/N per birth, the migrant a copy of a random same-slot individual from a uniformly random other island
  (one component, I = 64).
- **Annealed tail (new for `dollar3`):** from generation g₀ = 2N, arrivals per island and generation are Poisson with
  mean Λ[(1 + (g − g₀)/t₀)⁻¹ − (1 + (g + 1 − g₀)/t₀)⁻¹], t₀ = N/2 (queue 73's `tail_schedule`), each into a uniformly
  random slot, replacing a uniformly random resident; the arrival's program is drawn from **that slot's founding seed
  law** (the full law, no removals, in the main cells). Λ = total expected arrivals per island.
- Horizon: g_end = 100·N generations with the tail, then a 20·N tail-free chase (queue 73's geometry). Snapshots at
  g = 2N, 10N, 30N, 100N, 120N.
- Common random numbers: founders shared across Λ and mN within an arm, N and run index; tail arrival times shared
  across arms at equal (N, Λ, run).

## Arms

- **M (main):** the n ≤ 6 length-prior `dollar3` DSL under the modalPA (free sound box) evaluator, seed law
  `stable_sets.seed_law('M')` (B6m in queue 64; 1,305 canonical behaviour classes). No compute charge: the free oracle has
  no failed reads (as queues 70–71).
- **T (main):** the 27-program L_T^code library (`churn_primary_t.library()`, read cap 400, root fuel 1,200) at the
  `main` dose (constants 0.90, single-partner readers 0.06, two-partner 0.03, exploiters 0.01), at the default compute
  charge A_f, P_fail = 0.1 (h08), via `many_islands_t.Tabs.payoff`. The seed law is the library prior (h03's stated
  exception; noted as a caveat, not changed here).
- **L (reference):** the n ≤ 6 DSL under the weak evaluator (B6w), seed `seed_law('L')`, at N = 100 and 200 only.
- **D1 (diagnostic, M only):** the clean tail: arrivals drawn from M's seed law with the two ⅓-naming constants and the
  two Trojan-bully programs per slot removed and renormalized (queue 71's "clean tail" identities; founding unchanged).
  Λ = 100, mN ∈ {0.1, 1}, N = 100 and 200. Reported as a diagnostic of mechanism, never as a remedy.
- **D2 (diagnostic, M only) [after review]:** the same removals in the founding seed law *and* the tail (founders and
  arrivals both clean), Λ = 100, mN = 1, N = 100 and 200. [after second review] With **D3** (clean founding, full tail)
  the four cells (main, D1, D3, D2) form a 2 × 2 factorial of founding × tail composition at the same Λ, mN and N.
- **D4 (matched-mass control, M only) [after second review]:** remove programs of the same total prior mass per slot
  (0.217) chosen uniformly at random among the remaining classes, from founding and tail, renormalized; 3 independent
  removal draws × 20 runs, Λ = 100, mN = 1, N = 100 and 200. Renormalization raises every retained family's mass, so
  D2's effect is attributed to the ⅓ constants and bullies only beyond D4's.
- **T0 (constants-only control, T) [after second review]:** T's nine constants at their main-dose proportions
  (`many_islands_t.seed_law` dose '0'), mN = 1, Λ ∈ {0, 100}, N = 100, 200, 400. T against T0 is the readers' share of
  any T result.

## Grid and runs

| factor | values |
|---|---|
| N | 100, 200, 400 (L: 100, 200) |
| mN | 0, 0.1, 1 |
| Λ | 0 (tail-free reference), 10, 100 |
| runs | 40 at N = 100 and 200; 20 at N = 400 |

Main cells: M and T, 3 × 3 × 3 = 27 each; L 18; D1 4; D2–D3 4; D4 2 (× 3 draws); T0 6. **Long chase [after second
review]:** for M and T at mN = 1, Λ = 100, every N, runs 0–9 continue tail-free to 240N. **Cut order** if the budget (below) is exceeded: L at N = 200,
then Λ = 10 at N = 400, then mN = 0.1 at N = 400, then M/T at N = 400 down to 10 runs. Cuts are recorded before the cell
runs, never after seeing it.

**Budget.** The engineer times one run per arm at N = 100 and 400 (mN = 1, Λ = 100) and estimates the total before launch.
Run on Daytona: at most 5 sandboxes × 4 CPUs at once (`tools/daytona_run.py`; size pools from `DAYTONA_CPUS`). Ceiling:
400 sandbox-CPU-hours; above that, apply the cut order and say so.

## Measurements (per run unless noted)

1. **V\* share:** the fraction of islands whose modal outcome (the outcome of the three modal programs) is a fair pair, at
   every snapshot; primary at g = 120N (end of chase). [after second review] Also the **fair encounter probability**:
   the probability that a uniformly random encounter (one individual per slot, drawn by population frequency) forms a
   fair pair, averaged over islands; reported beside the modal share, with no nesting claimed.
1b. **Material surplus (evaluation, not target):** mean total payoff per encounter, so efficient states outside V\*
   (unequal pairs, grand splits) are distinguished from waste.
2. **Class shares** F / U / G / W / D at every snapshot.
3. **Consensus and pair identity:** a run is in fair consensus if ≥ 0.99 of islands sit on one fair pair at 120N, in
   unequal consensus likewise on one unequal pair. For fair-consensus runs, which pair, with the counts per (arm, N, mN,
   Λ); [after second review] the uniformity test is an exact multinomial test with simultaneous 95% intervals on the three
   pair probabilities (non-rejection is reported as "not distinguishable from uniform", not as equality).
4. **Transition structure (discipline 4):** debounced (25 generations) island-level transitions between classes F, U, W,
   D, G, and between fair pairs, per island-generation, in the tail window [2N, 100N] and in the chase. Report the 5 × 5
   matrix of rates per cell and the fair-to-fair flip rate. [after review] Report each at a fixed 25-generation debounce
   (comparable with queue 64) and at a 0.25·N debounce (comparable across N).
5. **Who holds the islands:** at 120N, the dominant program per slot on F and U islands, by family (M: constants by
   demand, Trojan bullies, fair readers, other conditionals; T: constants, single-partner, two-partner, exploiters).
6. **Tail accounting:** arrivals delivered per island (against Λ), the share by family, and for each family the number
   of arrivals that reach > N/2 copies in their slot (establishment) and whether the island's class changed within 5N
   generations after it [after second review: establishment is by **lineage**: each arrival carries a neutral lineage
   tag inherited through reproduction and migration, so copies of the same program already present or arriving later
   are not credited to it; if tagging is infeasible in the kernel, report genotype-frequency crossings instead and say
   so]; [after review] split by arrival time, early (g ∈ [2N, 15N]) and late (g ∈ (15N, 100N]).
7. **Without migration (mN = 0):** the W share at 2N (founding) and 120N, separately, to show what the tail cleans.

Statistics: means over runs with percentile-bootstrap 95% intervals over runs (islands within a run are correlated at mN
> 0). Paired contrasts (Λ = 100 minus Λ = 0; T minus M) use the CRN pairing. Every claim says whether it is a
finite-schedule statement (all of them are: discipline 5; nothing here is π).

## Validations (gates; a failed gate stops the cell family it covers)

- **V1 (tail-free reproduces queue 64):** Λ = 0, N = 100, mN ∈ {0, 0.1, 1}: the 100N = 10,000-generation snapshot of
  B6m and T-main runs 0–39 reproduces the stored `runs/churn_primary/` per-run records exactly (queue 64's endpoint is
  generation 10,000; the chase to 120N is beyond it). [after review] The arrival process uses its own RNG stream, so the
  birth and migration stream at Λ = 0 is draw for draw `kern_mw`'s. [after second review] Exact prefix reproduction is
  required; snapshots are observational and must not perturb the stream. No distributional fallback.
- **V2 (arrival law):** over 10⁵ simulated arrivals per arm, the empirical program law matches the seed law (χ² over the
  20 most common classes plus a pooled remainder, p > 0.01), and the delivered count per island matches Λ (mean within
  2%, Λ = 100; schedule integral checked analytically).
- **V3 (table coverage):** every program an arrival can bring has a joint payoff entry against every pair of programs
  that can be present (M: the full 1,305-class catalogue; T: 27). If M's joint table is built only over founding
  supports, extend it or compute missing entries lazily, and test the lazy path against the full table on 10⁴ random
  triples (0 mismatches).
- **V4 (A_f for T):** the charged table reproduces the stored queue-69 `Tabs` at P_fail = 0.1 on every triple.
- **V6 (slot symmetry) [after second review]:** the seed laws, the joint tables and the modal-outcome tie-break are
  equivariant under the rotation of slots (checked exhaustively for T, on 10⁴ random triples for M).
- **V5 (single-arrival assay):** a single ½-offer arrival in the excluded slot of a homogeneous unequal island (M's
  modal unequal triple) fixes with probability within the Moran neutral 1/N ± 3 s.e. over 10⁴ trials at N = 100 (the
  opener is neutral), and the subsequent switch of the underpaid member is selected (fixation > 3/N). [after second
  review] Neutrality also from k = 10 and k = N/2 starting copies (fixation within k/N ± 3 s.e.).

## Predictions (the RE's; the subagent copies them into `predictions/2026-11-07-majority-current-object.md` before any counted cell)

"Lands in V\*" for an arm and cell means V\* share ≥ 0.95 at 120N with the lower bootstrap bound ≥ 0.90.

- **RE 1 (the recorded arm-T prediction).** T at mN = 1, Λ = 10 and 100: V\* share ≥ 0.9 at N = 100 and at N = 200.
  Falsifier: mean < 0.9 in any of those four cells.
- **RE 2 (T at N = 400; recorded as unresolved, sharpened here).** T at mN = 1, N = 400, Λ = 10: V\* share ≥ 0.8.
  Falsifier: < 0.8.
- **RE 3 (the recorded DSL prediction, with the RS's).** M does not land in V\* at mN = 1 for any N and Λ, and its V\*
  share at N = 400 is below 0.5 with U the modal class. Falsifier: M lands in V\* in any mN = 1 cell, or V\* ≥ 0.5 at
  N = 400 (any Λ).
- **RE 4 (the prior's tail does not help M).** At mN = 1, V\*(Λ = 100) − V\*(Λ = 0) ≤ +0.05 for M at every N.
  Falsifier: a paired contrast > +0.10 with its interval excluding 0 at any N.
- **RE 5 (the tail cleans waste without migration).** At mN = 0, N = 100, the W share at 120N is lower at Λ = 100 than
  at Λ = 0 by ≥ 0.10 in both M and T (a wasteful island leaves by one selected step, a slot raising its demand, which
  arrivals supply). Falsifier: a reduction < 0.05 in either arm.
- **RE 6 (no arm lands without migration).** At mN = 0, no arm reaches V\* share ≥ 0.6 at any N and Λ ≤ 100 (unequal
  and disagreement islands persist in isolation). Falsifier: any mN = 0 cell ≥ 0.6.
- **RE 7 (equal likelihood across worlds in T).** [after review: one Λ only, since CRN founders make runs with the same
  index correlated across Λ] In T's mN = 1, Λ = 100 cell at each N, fair-consensus runs are spread over the three pairs
  uniformly (χ² p > 0.01). Falsifier: p < 0.01 at any N with ≥ 20 consensus runs; unscored at an N with fewer. Counts
  pooled over Λ are reported, not tested.
- **RE 8 (D1, diagnostic).** The clean tail raises M's V\* share at N = 100, mN = 1 by ≥ 0.15 over the full tail at the
  same Λ = 100. Falsifier: < 0.05. (If it holds, the mean-field finding of queue 71 survives finite N and I; if not, the
  finite-I migration consolidation dominates the tail's composition.) [after review] **RE 8b:** the same at N = 200, where
  M's tail-free baseline is expected to sit on U: a rise ≥ 0.15; falsifier < 0.05.
- **gemini-4-argon's counter (recorded, scored):** RE 8 fails (gain < 0.10), and fails at N = 200, because migration at
  mN = 1 consolidates the founding unequal convention by 10N–20N and over half of the tail's arrivals come later. (RE note: with t₀ = N/2 the share of Λ delivered by g − g₀ = 8N is 1 − 1/17 ≈ 0.94, so most arrivals
  come before 10N; the counter is scored as stated.) [after second review] Its timing mechanism is **refuted
  analytically before the run** (about 3% of delivered arrivals come after 15N); only its numerical outcome is scored.
- **gpt-6.1-sol's counters (recorded, scored):** (i) RE 8b fails: the clean tail's gain decreases with N and Λ = 100 is
  not enough at N = 200 (scored: gain at N = 200 < gain at N = 100, and < 0.05). (ii) RE 5's common bound fails in at
  least one arm (scored: reduction < 0.10 in M or in T).

The RS's recorded prediction is scored per arm: it holds for an arm if the arm does not land in V\* in the mN = 1, Λ > 0
cells at the largest N run, and fails for an arm that lands there.

## Required outputs

- `predictions/2026-11-07-majority-current-object.md` (committed before any counted cell; pilots disclosed).
- `src/majority_tail*.py` (the `dollar3` tail kernel: `churn_primary.prepare` outputs fed to `pair_worth_kern.kern_pw`
  or an equivalent, a `dollar3` arrival schedule and universe, the A_f table for T), tests in
  `tests/test_majority_tail.py`, run through `tools/run_tests.sh`.
- `runs/majority-current-object.md` and `.json` (every measurement above, per cell, with intervals; the transition
  matrices; validation results; the prediction table with verdicts), rows under `runs/majority_tail/` (no `.npz`/`.pkl`
  committed; compressed JSONL allowed).
- `notes/majority-current-object.md`: every deviation from this spec, with the reason, and the timing/budget record.
- Drafts handed back to the RE: a RESULTS section, REJECTED entries for failed predictions, and any NOTATION entries.

## Caveats known in advance

- Arm M uses the free sound oracle (a DSL approximation); T is a hand-built 27-program library under a library prior
  (h03's exception), not a length prior over the real syntax.
- One prior per arm; one grid (⅓ – ½ – ⅔); I = 64 in one component; finite schedules.
- The tail's form (t₀ = N/2, g₀ = 2N) is a modelling knob (h03); only Λ is varied.
