# Queue 78: notes (engineer's log; deviations, operations, budget). Appended as the run proceeds.

## Deviations and implementation choices
- The worktree base lacked the spec and queue 76's code; fast-forwarded to `main-t69lqz` (4194123) before starting.
- Catalogue K = 59: queue 76's 55 programs (T+, P, Q, O, F2) plus `Rnn`, `Rny`, `Rpn`, `Rpy` appended last (`src/patient_accepter.py`).
  `R<d><to>` reads partner d, names it at 1/2 if it names R at 1/2, else names the other partner at 1/3; `to` is T's timeout convention.
  The matched orientation for a victim whose bully is its prev (the seeded `Bn` islands) is `Rn*`.
- Dynamics use the two `n` variants at γδ/2 each (the spec's main arm); the `y` variants appear in the gates and step 0 only.
- Donor rule: in F+R, F+O+R and F+C⅓ the γδ comes uniformly out of the nine constants; F+C⅓ adds it to C3 and C0, the constants
  `Rnn` and `Rpn` play on path. Hence F+R and F+C⅓ differ only in the substituted family (checked in `tests/test_patient_accepter.py`).
- The F control rows are queue 75's stored 2a rows (`runs/lpt_rows/`), which were also queue 76's F control. V1 reruns 40 of them
  (N = 100, 200; β = 1, 3; δ = 0.01, 0.1; runs 0–4) with the 59-program catalogue.
- Step-0 assays are exact birth–death fixation probabilities over all named resident triples of each class. These are queue 76's
  method: frequency independent because the other two slots are monomorphic. The checks are a 10⁴-trial jump chain (60 assays) and the
  real kernel (16 assays, 3,000 islands).
- Seeded starts log the majority program of every slot at every generation (`src/patient_accepter_kern.py`, a generated copy of
  `kern_mt` with one extra record; draw-for-draw identical, tested). Exits are classified in `patient_accepter_dyn.classify_exits`.
  Transient flips are counted as exits; "lasted to 120N" marks the durable ones.
- Step 1: queue 75's targeted grammar search (`lt_prior_search.search`) rerun for R0 and R1 with the 59 programs as members. The
  family classifier labels R `other_cond`; the exact-member label is what is counted. The Monte Carlo upper bound is new draws with the extended members:
  R0 4 × 3·10⁶ locally, R1 4 × 1.5·10⁶ on Daytona. Queue 75's stored draws cannot give it, since R lies inside `other_cond`, most of R1's
  finite mass.

## Operations log
- 2026-11-14 ~19:20 UTC: main chunks g_0..g_9of10 (all stages except lps and v1; 4,700 cells) queued. Launched 025050dc = g_0of10,
  6e21fd10 = g_1of10, eb1088e7 = g_2of10, cd6fef12 = g_3of10, 6c3619a2 = g_4of10 (full ids in runs/pa_launch/launch.log, untracked).
  mcR1 queued ahead of g_5..g_9.
- Local: step-1 searches R0, R1; V1 stage (40 cells, one worker).

## Budget
- Cut order (spec, recorded before running): I = 256, then γ ∈ {0.3, 3}, then N = 400 for F+O+R. Projected total at launch:
  25,580 cost units ≈ 90 sandbox-CPU-hours for the grid. The first sandbox timing was 12.6 s per unit per CPU, against 9.2 s in queue 76.
  The length-prior series adds ≈ 20 and the R1 Monte Carlo ≈ 5. The projection is under the 200 ceiling, so no cut is applied.
- mcR1 (a8ab005f): two of the four shards (seeds 7801, 7802) were OOM-killed inside the sandbox, after 0.8·10⁶ and 1.45·10⁶ draws
  (the memory growth queue 75 noted). Kept: seeds 7800 and 7803, 2.0·10⁶ finite draws, 0 R hits, 95% upper bound 1.9·10⁻⁶. Not rerun:
  the bound is uninformative against the 10⁻¹⁰ lower bound either way. Cost ≈ 10.7 sandbox-CPU-hours (9,619 s × 4).
- ~21:15 UTC: exit classifier v1 gave undefined slot roles after migration mixed the rotated seeded triples (seen in the first five
  chunks). Classifier v2 committed; all 200 seeded cells rerun as series `seed2` (chunks s2_0of2, s2_1of2). The report uses `seed2` only.
  Disclosed in predictions addendum 2.
- Launches: 45d7789e = g_5of10, 0fdcd25e = g_6of10, 05d0ddc1 = g_7of10, 1272dce7 = g_8of10, 535e8603 = g_9of10, 33c153c3 = lps_0of4,
  75f22e85 = lps_1of4, 56cfc63e = lps_2of4, ac199ee2 = lps_3of4, 9cbc7774 = s2_0of2, 8813543c = s2_1of2. All exited 0 and were fetched;
  no container restart occurred.

## Budget and timing (final)
- Daytona: 17 sandbox runs (10 grid chunks, 4 lps, 2 seed2, mcR1). Sum of sandbox walls is 87,796 s × 4 CPUs ≈ 97.6 allocated
  sandbox-CPU-hours. Cell time (sum of job walls) is 85.7 CPU-hours. Local: gates, step 0 (25 s), step-1 searches (≈ 11 min),
  R0 Monte Carlo (≈ 10 CPU-min), V1 (40 cells, ≈ 25 min). Total ≈ 99 CPU-hours of the 200 ceiling; no cut applied.
- V1: 40 of 40 identical. seed vs seed2: 200 of 200 identical V\* series and fair shares (determinism check).
- `python3 tools/daytona_run.py list` is empty at hand-back.

## The model cannot express
- An offer from a reader that R can read. Mutual reading between readers always times out under the capped simulation, so R's
  patience is answerable only by non-reading ½ constants.
- A reader that stays a constant to its current partner. R's read makes it unreadable to the bully whenever a reader is near.
- A coordinated two-slot move (R and its offerer together); the dynamics are single-slot invasions.
