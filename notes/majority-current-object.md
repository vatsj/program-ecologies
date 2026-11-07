# Notes: majority division in the current object (queue 74)

Spec `specs/2026-11-07-majority-current-object.md`; predictions `predictions/2026-11-07-majority-current-object.md`; run record
`runs/majority-current-object.{md,json}`; rows `runs/majority_tail/rows/*.jsonl.gz` (one file per job, one JSON object per
cell). Code: `src/majority_tail_kern.py` (kernel), `src/majority_tail.py` (arms, laws, schedule, tables, statistics),
`src/majority_tail_run.py` (jobs and shards), `src/majority_tail_validate.py` (V1-V6), `src/majority_tail_report.py`
(aggregation, verdicts); tests `tests/test_majority_tail.py`.

## Deviations from the spec, with reasons

1. **Which series is "the modal outcome".** The spec's parenthesis defines it as "the outcome of the three modal
   programs"; the repository's `modal` (queue 64, 73, `kern_mw`) is the encounter-weighted argmax of the island's outcome
   distribution, and the majority-triple outcome is a separate record (`majo`). V1 reproduces queue 64, which uses `modal`, so
   the **primary V\* statistic is `modal`** and the majority-triple version is reported beside it in every cell
   ("V* (maj. triple)"). Transitions, consensus and class shares use `modal`; consensus is also counted on `majo`.
2. **Establishment is by presence episode, not lineage tag.** The spec allows the fallback ("if tagging is infeasible in
   the kernel, report genotype-frequency crossings instead"). Tagging needs one more random draw per birth (which parent
   copy is tagged) and would break the draw-for-draw reduction to `kern_mw` that V1 requires; the kernel logs the first
   generation a program holds more than N/2 of a slot on an island, with the flag of whether its current presence began
   with an arrival (and when). An arrival is credited if the episode it began crosses N/2; arrivals of programs already
   present, and later arrivals of a program, are not credited; an episode that began with an arrival and then spread by
   migration is credited to the arrival that began it on that island. The class-change test compares the island's modal
   class at g and g + 5N.
3. **Joint table is per-run, not the 1,305-class cube.** A 1,305³ table is 2.2·10⁹ entries. Each (arm, variant, N, run)
   builds the universe of founders plus every program of the Λ = 100 schedule (197 / 304 / 517 classes per slot at N = 100 /
   200 / 400, 15 MB to 160 MB as int16), so every program an arrival can bring has an entry against every pair that can
   be present (migrants copy residents). V3 checks the int16 table against the reference int32 builder on 54,000 triples of
   the universes and the lazy build against the reference on 10⁴ triples of the full catalogue (0 mismatches). All Λ and mN
   cells of a job share this universe; extra classes with zero counts do not change the kernel's stream (V1 passes with
   universe = founders only; Λ = 0 counted cells use the larger universe, which only appends zero-count classes).
4. **D4 removal is a mass-matched random subset, not exact.** The classes are indivisible and a few carry 3–6% of the
   prior, so no subset hits 0.2169 exactly. D4 draws a random order of the non-clean classes, removes classes that fit
   under target + 0.003 until the removed mass is within 0.003 of the target (0.2169), up to 5,000 orders (the
   closest if none is within); per slot and per draw, seeded by (draw, slot). The removed mass is verified per slot in the test.
5. **Arm T founders.** `churn_primary.founders` is used (a 31-class law with four stub classes at weight 0), then the first
   27 columns are taken, so T-main founders at N = 100 are the same individuals as queue 64's; T0 uses the constants-only law
   with the same generator. The arm T table is `many_islands_t.Tabs.payoff(0.1, 0.1)` (the A_f charge), deduplicated into
   types by (joint code, the three net payoffs) so the closure stop (play identity) is meaningful; the outcome totals in
   the surplus column are gross of the charge.
6. **V4.** There is no stored per-triple queue-69 table to compare with (queue 69 stored cell results, not tables); V4 checks
   the table against `Tabs.payoff(0.1, 0.1)` (max difference 3·10⁻¹³) and an independent counted re-evaluation of 300
   random triples through `many_islands_t.f_eval_counted` (0 mismatches). The table is the queue-69 table by construction.
7. **V1 environment.** V1 passes both locally (Python 3.13, newer numpy/numba) and in the pinned sandbox environment
   (numpy 1.24.3, numba 0.57.0): 240 of 240 stored rows (B6m and T-main, mN ∈ {0, 0.1, 1}, runs 0–39) and the `kern_mw` modal
   series exactly. All counted cells ran in the pinned sandbox environment.
8. **V6 tie-break.** The argmax's first-index tie-break is not rotation-equivariant. Rather than redefine the statistic,
   every snapshot records the number of islands whose top two outcome probabilities tie within 10⁻¹²; it is reported per
   cell (column `ties`), and the consensus statistics are not affected unless a tie occurs at 120N.
9. **Transitions.** Computed on the modal-outcome class series (5 × 5 over F, U, G, W, D) and on outcome ids for fair-to-fair
   flips, with the debounce applied to the whole series; a class change counts in the window if the first generation of the
   new class lies in it. Windows: tail [2N, 100N], chase [100N, 120N] (and [120N, 240N] for the ten long-chase runs).
10. **Long chase.** The ten runs 0–9 at (Λ = 100, mN = 1) are run in one kernel call to 240N; their 120N snapshot is the
    counted cell's (the stream is a prefix).
11. **Closure.** As in `kern_mw`, a global closure (status 1) ends a run once no arrivals are pending; the series is then
    frozen forward. Rows carry `status` and `stop`.
12. **Pilots.** Disclosed in the predictions file. A pipeline test ran one job (M, N = 100, run 0, all nine cells); only
    schema and wall times were read.
13. **Spec files.** The spec, its two reviews, `tools/daytona_run.py` and `tools/run_tests.sh` were uncommitted in the RE's
    checkout, so they were copied into the worktree (commits 1–2 of the branch).

## Timing and budget

(Filled after the run.)
