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
