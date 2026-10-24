# A migration window for stable sets on islands (notes, 2026-10-24)

Spec `specs/2026-10-24-migration-window.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in `--mode amended`; the
[after review] text is the resolution). Follow-up to RESULTS "Stable sets on islands", "Dominance contracts and refusal
on islands", "Farsighted refusal". §1 is written by hand before any code of this experiment and before any counted
cell; §2 (deviations, choices where the spec is silent, costs) is appended as they arise.

## 1. Hand predictions and frozen parameters

### 1.1 The object, frozen now

Everything of `src/stable_sets.py` (kernel `kern`, game `dollar3`, tables, seed laws), `src/farsighted_refusal.py`
(kernel `fkern`, guards g0 / gV / gKR(0.99), `Setup`) and `src/dominance_contracts.py` (contracts, `tables`) is
imported, nothing edited. The two kernels are **copied by a generator** (`src/migration_window_gen.py`) into a new file
that records, in addition, each island's modal outcome, the mass on efficient outcomes and the mass on fair pairs at
every generation; no random draw is added, moved or removed, and the copies are tested to reproduce the originals
draw for draw (cls arrays, final counts, migrant counts). Components are run as independent sub-archipelagos (see 1.4).

- **Game:** `dollar3`, demands in {1/3, 1/2, 2/3}, outcomes in sixths, 20 realizable outcomes R (3 fair pairs, 6
  unequal pair outcomes, 9 wasteful, the grand coalition (2,2,2), disagreement).
- **L:** the length prior, `seed_law('L', slot)` over the 1,305 canonical functions of the weak arm; Moran with
  **w = 0.3** (`SS.W`); ε = 0 (no mutation); N per slot population (100 main, 200 second); I = 64 main.
- **Founding distribution:** each island and slot draws `multinomial(N, L)` from `np.random.default_rng(run_seed(base, r))`,
  island by island, slot by slot (`SS.draw_seeds`), so the first 16 C islands of any larger draw are a prefix of it.
  Common founders for every cell at a given N: `base = 'L1'` at N = 100 and `'L1-N200'` at N = 200, kernel seed
  `run_seed(base, r) % 2^31`. Hence the mN = 1 baseline cell and the mN = 1 U-gKR(0.99) and gV cells use exactly the
  founders and kernel seeds of the stored `L1`, `UKR99-1` and `R2r-1` / `R2-1` runs, and the mN = 1, N = 200 cells those
  of `L1-N200` and `UKR99-1-N200`. (The stored mN = 0 cells used the founder base `L0`; the counted mN = 0 cells use
  `L1` so that all mN are paired on founders; the stored mN = 0 runs are reproduced separately in the tests.)
- **Guards:** baseline = `kern` (no contracts); U-gKR(0.99) = `fkern` with guards ['g0', 'gKR0.99'], assignment
  ('bit', 1.0, 1) (every founder carries the guard); gV = ['g0', 'gV'], ('bit', 1.0, 1); both with **ν = 0.1** contract
  events per island per generation, **β = 1**, menu F, public consent, the static fixed-point table of
  `runs/farsighted-refusal-static.json`.
- **Topology:** complete graph within a component; no edges between components. A migrant birth in island i draws
  its parent's source island uniformly among the other islands of i's component.
- **Meaning of mN:** the kernel's definition, m = mN / N per birth, N births per slot-population per generation, so
  **mN is the expected number of migrant births per slot-population per generation** (for active, polymorphic
  populations; monomorphic populations are only touched by migrant births), 3·mN per island per generation. The realized
  count (`nmig`) is reported for runs that last the whole horizon.
- **Horizon:** 20,000 generations (cells that stop early on closure are forward-filled; closure is exact only at
  ν = 0, where the kernel stops on global play-closure, and for guard cells never). Per-generation records: every
  island's modal outcome (argmax of the encounter distribution), the encounter mass on efficient outcomes (total
  payoff 1) and on fair pairs. Snapshots at 1,000, 2,000, 5,000, 10,000, 20,000; modal outcomes also saved on a
  50-generation grid for the transition counts.
- **Code revision:** repository head `c09c425982e17e8629b0e769e91f49bc06c42a49` at the start of the work; the
  kernels are generated from the source of that revision (the generator asserts every anchor it patches).

### 1.2 Statistics, frozen now (choices where the spec leaves room)

Outcome classes of an island's modal outcome: **fair** (F_k, k = the excluded slot), **unequal**, **grand** ((2,2,2)),
**wasteful** (any pair outcome with total < 1), **disagreement**. *Efficient* = fair, unequal or grand (total payoff
1).

- **target (as stated):** every island's modal outcome is efficient *and* each of the three fair pairs is the modal
  outcome of at least one island. **target (V\*):** every island's modal outcome is a fair pair and all three are
  present. **High-purity versions:** every island has at least 0.95 of its encounter mass on efficient outcomes
  (resp. on fair pairs), and the three fair pairs are modal outcomes of at least one island each.
- **Per generation** (exact): the four indicators, the number of fair pairs present, the number of wasteful /
  disagreement islands, the mean inefficient mass (1 − efficient mass), the island counts by class.
- **Passage times** (generation index, from the per-generation records). *Waste cleared:* first generation g such
  that no island has a wasteful or disagreement modal outcome for the 25 generations g .. g + 24 (the repository's
  HELD = 25 convention; a flicker filter). *Coverage established:* first generation with all three fair pairs
  present (modal). *Coverage lost:* first generation g after coverage was established such that fewer than three
  fair pairs are present for the 25 generations g .. g + 24. Both are right-censored at 20,000 (a run that stops
  early on closure is censored there too); Kaplan–Meier medians. *Last observed waste:* the last generation in the
  horizon with a wasteful / disagreement modal island (horizon-dependent). *Target episodes:* maximal runs of the
  per-generation target indicator; first entry, number of episodes, the lengths of the episodes (and the number
  of episodes of at least 25 generations), cumulative generations in target.
- **Transitions:** on the 50-generation grid, for each island and consecutive grid points with different modal
  outcomes, a count by (from-class, to-class), by exact (from, to) outcome, and by whether the "to" outcome was
  present on another island of the component at the earlier grid point (colonization) or not (local).
- **Consensus:** all islands of a component have one modal outcome; the time it first holds for 25 generations.
- **Occupancy** (islands classified at least 0.95 on a fair pair, from the kernel's `cls`) and **modal occupancy**.

### 1.3 Scoring (fixed now)

*Held* at or past the stated threshold, *failed* at the falsifier, *partial* in between. All contrasts paired on
founders, with run-clustered percentile-bootstrap intervals (runs as clusters; 4,000 resamples; components are
resampled with their run). Predictions are scored on **target (as stated)** at **generation 10,000** unless the
prediction says otherwise, with target (V\*) and the 20,000 snapshot reported beside. Prediction 4's "its best mN":
scored as written (the mN at which U-gKR(0.99)'s share is largest, which may be mN = 0, where the baseline cannot meet
the target at all, so the clause is nearly free); the gain at the best mN > 0 is reported beside it and the verdict
says which one binds. Prediction 2's slopes: least squares of log median on log mN over all mN with an uncensored
Kaplan–Meier median, with the fit restricted to {0.03, 0.1, 0.3} reported beside it. Prediction 6's mechanism clause
("by preserving founding diversity rather than by migration") has no direct statistic in a design with migration on
inside every component; it is scored on the direction (4 × 4 above 4 × 64) and the component outcome distributions are
reported as the mechanism evidence, not scored (disclosed again in §2).

### 1.4 Components as independent sub-archipelagos

Components are independent in the model (no coupling except through migration, which stays inside a component), so a
C-component archipelago is run as C separate kernel runs of the component's islands, each with its own kernel seed
(`run_seed(base + '|comp%d|size%d', r)`) and with the founders of islands [16c, 16c + 16) of the common draw. The per-
generation records are concatenated into the archipelago's records. This differs from one kernel run over all islands
only in the clock coupling (the kernel allots a fixed number of births per generation to the whole archipelago, so
components would share a multinomial, not a fixed, split); the difference is a variance of the per-component clock of
order 1/sqrt(births per generation), recorded here as a disclosure. The panel of 16-island components is nested: the
C = 1, 2, 4 archipelagos are the first 1, 2, 4 components of the C = 8 archipelago (identical trajectories), so they
are one batch of 8 component runs per replicate. The size panel (C = 4 components of 4, 16 or 64 islands) shares its
16-island row with the main panel.

### 1.5 My own predictions (engineer's, derived by hand before any code; rough, with the reasoning)

Reasoning inputs: the stored mN = 1, N = 100 runs reach consensus 0.65 by 2,000 and 0.95 by 10,000 with 0.90 of
member flips by pure drift; an efficient immigrant that dominates a frozen wasteful island fixes with probability of
the order of 0.3; the frozen waste at mN = 0 is 0.30 of islands (about 19 of 64).

- **E1 (clearance is fast, about 6 / mN generations):** the median time to waste cleared is about ln(20) / (3 mN × 0.6 ×
  0.3), i.e. 4 / mN to 15 / mN: roughly 500–3,000 generations at mN = 0.01 and 15–50 at mN = 0.3. At mN = 0.003 it is
  below 10,000 in most runs.
- **E2 (coverage lasts longer, about 500 / mN):** the first loss of one of three types among 64 islands in a neutral
  voter-type process takes a fraction of the 2,000-generation consolidation time at mN = 1, so the median time to
  coverage lost is about 300–800 at mN = 1, about 5,000 at mN = 0.1 and censored (beyond 20,000) at mN ≤ 0.03. The ratio
  of the two medians is in the tens, so the RE's factor 5 holds where both are uncensored, and the slopes are near −1.
  I side with the RE against gemini's compression counter-prediction (flips are 0.90 pure drift in the stored runs).
- **E3 (the window is wide and low):** the baseline's target (as stated) share at generation 10,000 is 0 at mN = 0 (frozen
  waste), at least 0.8 for mN in {0.003, 0.01, 0.03}, about 0.3 at 0.1, about 0 at 0.3 and 1 (stored coverage 0/40 at
  mN = 1). The best mN is 0.01–0.03. Prediction 1 is held with room.
- **E4 (N = 200 narrows it):** from N = 200 an unequal pair takes over under migration, so the share at the best mN is
  about 0.4–0.6 against about 0.9. Prediction 3 held, but with a smaller N effect on the best low-mN cell than at
  mN = 1, because unequal pairs also count as efficient in the target as stated; the V\* version shows the larger drop.
- **E5 (guards):** U-gKR(0.99) at mN = 0 meets target (V\*) in all runs (stored occupancy 1.000); at mN > 0 it fixes the
  member each island holds and then spreads, so it meets the target no more often than the baseline in the
  low-mN plateau and loses to it at 0.1–0.3 by consolidating sooner (gemini's counter-prediction). The "at least 0.2 more at its best mN" clause is met only through mN = 0.
  Prediction 4's first clause ("at least as many at every mN") fails at one or more mN > 0 on the point estimates.
- **E6 (gV):** the stored R2 cell at mN = 1 has coverage 1.00 and modal occupancy 0.996 at 10,000, so gV holds
  at least 0.9 of runs at every mN ≥ 0.01 and Prediction 5 is held; gpt's counter-prediction (declining coverage) does
  not show in the stored cell and I expect it not to.
- **E7 (components):** at N = 100 and mN = 1 a 16-island component is at consensus long before 10,000, so the target
  shares are about 0 (C = 1), about 0 (C = 2), 0.2–0.35 (C = 4: the reference 0.444 times the chance that every
  component sits on a fair pair, roughly 0.8) and about 0.75 (C = 8). C = 4 is the borderline cell against the ±0.15
  band. At N = 200 below the reference (unequal pairs). In the size panel the 4 × 4 and 4 × 64 shares are close
  (within 0.1); I do not expect "founding diversity" to separate them.
- **E8 (controls):** the balanced start loses coverage on the same 1 / mN scale as the lottery (neutral drift), and the
  waste-seeded start clears on the E1 scale; a run of balanced-start islands under U-gKR / gV never loses coverage at
  mN = 0.1 within 20,000 for gV.

### 1.6 Hand-derived checks used by the tests

- The independent-uniform reference P(all three present) = 1 − 3 (2/3)^C + 3 (1/3)^C is 0, 0, 4/9, 0.8834 at C =
  1, 2, 4, 8 (0.9954 at C = 16); unit-tested against enumeration.
- Hand-built archipelagos: one with all 64 islands on fair pairs (21, 21, 22) meets both targets; the same with a
  single wasteful island meets neither; with one fair pair replaced by an unequal pair, the stated target holds if
  all three fair pairs are still present and the V\* target does not; with a fair pair missing, neither holds.

## 2. Choices where the spec is silent, deviations, validation, costs (appended as they arise)

### 2.1 Validation before any counted cell

- **Tests** (`tests/test_migration_window.py`, 10 passing): the generated kernels reproduce `stable_sets.kern` and
  `farsighted_refusal.fkern` draw for draw (classes, final counts, migrant counts, events) on small configurations at
  mN = 0 and 1 for the baseline, U-gKR(0.99) and gV; the stored baseline runs `L0` (runs 0-2) and `L1` (runs 0, 2), the
  stored `UKR99-1` run 0 and `R2r-1` run 0 are reproduced at the stored horizon in status, stop generation, migrant births
  and event counts; the reference formula against enumeration; the target statistic on hand-built archipelagos (both
  versions, high purity); passage-time helpers; the control starts (balanced: 20/20/20 fair-pair islands, waste-seeded:
  45 fair + 15 wasteful, the seeded outcome is the modal outcome at generation 0).
- **Re-verification of the stored cells** (`runs/migration-window-verify.json`): all 40 runs of the baseline `L1`, `UKR99-1`
  and gV (`R2r-1`) cells at mN = 1 were rerun through the generated kernels with the stored founders and seeds at the stored
  horizon 10,000 and compared with the stored per-run records: status, stop generation, migrant births and event counts
  identical in 40/40 in each cell; the modal outcome counts (guard cells), occupancy, consensus and coverage flags
  identical in 40/40. The stored gV cell at mN = 1, rederived: consensus 0/40, all three members present 40/40, modal
  occupancy 0.998 (the spec's 0.996 is the dominance-contracts `R2-1` figure; the farsighted rerun `R2r-1`, which is the
  stored cell used here, gives 0.998), and the spec's target as a statistic is **target (as stated) 0.925, target (V\*)
  0.850** at generation 10,000: one stray island (a non-fair modal outcome somewhere in 64) in 3 and 6 of 40 runs. So gV
  at mN = 1 is a good reference but not a certain 1.0; Prediction 5's 0.9 threshold is close at mN = 1 on this cell.

### 2.2 Choices and deviations

- **Components as independent sub-archipelagos** (§1.4): not a modification of the kernel. The 16-island prefix
  arrangement (C = 1, 2, 4, 8 from one batch of 8 components) means the C rows are nested, not independent draws.
- **Founders common across mN and guards.** The counted mN = 0 baseline cell uses founder base `L1`, not the stored `L0`
  (the stored mN = 0 runs are reproduced in the tests), so that every mN is paired on founders.
- **Event logs switched off.** `evcap` = 1000 and `cevcap` = 1000 in the copied kernels (the stored runs used 2·10⁶ /
  6·10⁵). They only bound the size of arrays that this experiment does not read; they do not enter the random stream
  (the identity tests run with the smaller values).
- **Hrec empty.** The kernels' snapshot arrays are unused; snapshots come from the per-generation records.
- **Prediction 6's mechanism clause** is not scored (see §1.3); component outcome distributions are reported.
- **Bootstrap sizes.** Percentile bootstrap with 4,000 resamples for shares and differences, 1,000 for Kaplan–Meier
  medians (cost), run-clustered.
- **Prediction 3** compares N = 200 with N = 100 unpaired (the founders differ by N); all within-N contrasts are paired.

### 2.3 After the counted cells (disclosures; nothing here changes a pre-registered rule)

- **All 72 counted cells ran to completion**; no cut from the cut order was needed (mN = 0.003, the (200, 64) guard
  cells, the 20,000 snapshot and the 64-island size panel are all in). 2,020 jobs, two workers throughout (other
  subagents were alive on the machine the whole time); peak job memory 0.77 GB; no failed job. The (200, 64) and size-
  panel cells use 20 runs (40 for N = 100 and the 4-island size cell), as planned in the runner.
- **The gV stray island** (§2.1) is one island per run in the 6 runs that miss the V\* target at mN = 1, N = 100:
  unequal in 3 runs, disagreement in 2, wasteful in 1; the stated target fails in the last 3.
- **Realized exposure** matches the definition: migrant births per slot-population per generation are 0.1000, 0.3000 and
  1.0004 at mN = 0.1, 0.3, 1 (full-horizon runs), at both N.
- **Prefix archipelagos.** The C = 1, 2, 4 rows are prefixes of the C = 8 archipelago; their migrant totals were
  recorded for the whole 8-component run, so exposure is not reported for them.
- **Waste is regenerated.** Reading the balanced and waste-seeded controls: even from a start with no waste, the baseline
  forms wasteful islands locally (fair → wasteful transitions with the destination absent from the rest of the
  component), at a rate comparable to their clearance by colonization; this is not in the spec's model of the window and
  it is why the all-islands target is hard for the baseline at every mN.
