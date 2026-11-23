# Queue 81 notes: definitions as implemented, deviations, reuse

Spec `specs/2026-11-23-tiered-best-response.md` (both amendments folded); predictions
`predictions/2026-11-23-tiered-best-response.md` (committed 1ed5945 before stage 0; implementation definitions
committed 8d31983 before stage 2). Report `runs/tiered-best-response.md`.

## What was reused

- **Arms T and M**: `majority_tail.prepare` (published founders via `stable_sets_run.run_seed`, the arm-independent
  tail schedule, the universe and joint tables), the 27-program library at A_f with P_fail = 0.1 (arm T), the n ≤ 6
  modalPA DSL catalogue B6m with 1,305 classes per slot (arm M), the seed laws (`base_laws`). The kernel
  `src/tbr_kern.py` is generated from `src/majority_tail_kern.py` by `src/tbr_kern_gen.py` with observational
  additions only (`lastnew`, and the final `intro`, `arrf`, `t10` returned); `tests/test_tbr.py` checks it is draw
  for draw `kern_mt`, and every stage-1 run-cell at (Λ = 100, mN = 1) compares its V\* series (every N generations,
  0 … 120 N) and migration count with queue 74's stored row.
- **Arm P**: `bridgeless_rivals.seeds / build_init / a_ref / forced / boundary`, `rival_islands.restrict / _kern /
  cls(9)`. The class cache (`cache/spoiler-n{6,9,12}.npz`, gitignored) was rebuilt by `src/tbr_build_p.py`, which
  recompiles `moat_static_big` and `seeds_tail` kernels with `parallel=False` because numba 0.68 (the only build for
  Python 3.13 here; the repo pins 0.57) fails in its parfor pass on `_traces`. The parallel loop writes only bit 6 and
  reads only bits 0–5, so the serial table is identical; `build_main`'s own checks of n = 6 and 9 against
  `seeds_in_n` passed (names, masses to 2e-16, U equal).

## Definitions (as coded)

- **Fitness** exp(w·payoff), w = 0.3, in all arms, so P10's w/f = w: σ(p′) = w·Σ_{s′}Σ_q m_q T_q Δ_q.
- **World state**: full compositions at 30N, 60N, 90N, 120N (T, M; horizon 120 N, as queue 74's headline); arm P at
  25% and 100% of 10⁵ generations (exact), 50–75% from the strong-holder log only.
- **E(p; k)** (T, M): catalogue programs whose whole payoff vector, with the island's majority programs in the other
  slots, equals p's (tolerance 10⁻¹²). Arm P: u(p′,p) = u(p,p′) = u(p′,p′) = u(p,p). **E_comp**: equality against every
  combination of present programs (T, M) / every present class (P).
- **Native regret**: best catalogue payoff against the majority profile minus p's (P: a rare p′ among residents,
  max u(p′,p) − u(p,p)); composition version against the island's mix. Migrant claims are scored on residents with
  zero native regret.
- **Migrants**: other islands' majority programs per slot, island-count weights a_q = n_q/(I − 1) (the kernel's
  migration is uniform over the other islands; a migrant parent is drawn by fitness on its island, approximated by
  the majority). Arrival-weighted migrant payoff = ½ Σ_{s′} Σ_q a_q u_j(p′ | s′ ← q). T-weighted: σ with
  m_q = mN·a_q and T_q the exact single-arrival sojourn (copy-generations until extinction or N/2 copies) on the
  island's native profile.
- **Prior tier** (T, M only): the tail law, π_q (arrival) and π_q·T_q (T, unit dose), inside the T-argmax set of E
  (A-argmax for the arrival version); unconditional beside. Arm P has no tail.
- **Controls**: prior-matched = exact expectation over E under the seed law; founder = E weighted by the run's
  founder counts (summed over islands); arrival = E members with `lastnew` ≥ the residency start of the horizon profile
  (max over slots of the holder's N/2-crossing generation in its current presence episode), uniform weights.
- **Vacuous**: |E| = 1, or the statistic equal (≤ 10⁻⁹) over E; counted per statistic.
- **Diverse** world: ≥ 2 majority program profiles each on ≥ 5% of islands; consensus = not diverse.
- **Routes**: see the predictions file, item 9 (T, M) and `src/tbr_p.py` `routes_p` (P).
- **Costly threat carried with zero regret**: resident with zero T-migrant regret for which some p″ ∈ E earns more
  than p against a prior tester q while q also earns more against p″ than against p (p pays to punish q).

## Deviations from the spec

1. Stage 0a draws the testers met per birth event (Binomial(i, ε)) and simulates the embedded jump chain; it is
   compared with P10's finite-N formula (RE 1) and with the exact value for the realized event process.
2. Stage 0b: tester cases r_q ∈ {0.7, 0.9, 1.0 (neutral)}, each indifferent to the variant (scored), plus r_q = 0.9
   with ±0.1 feedback against variants (reported only). Burn-in 20 generations of the partner slot; a tester that
   establishes during burn-in is reset. 20,000 replicates per point.
3. Arm P runs with lumping off (see predictions item 7); environment checked draw for draw with lumping on.
4. Arm P mN = 1.091 (the published boundary) in place of 1; stage 2 doses {0.1, 1.091, 3, 10}. Arm P's stage 2 was
   first sent to Daytona with a wrongly quoted command (the tool joins its arguments, so `bash -c "..."` ran a bare
   python3); two 4-CPU sandboxes idled about 2 hours (about 16 sandbox-CPU-hours, no output), were interrupted and
   deleted (SDK listing empty afterwards), and stage 2 ran locally (`--out runs/tbr_rows/p_local`, then moved).
5. Λ = 1,000 uses its own tail stream (Lmax = 1,000); founders paired.
6. Supply control in arm P is founder-weighted (no arrival log); in T and M the arrival control is primary.
7. Stage 1b: migration into the focal slot switched off (arm P: only tester migrants arrive); on-path classes grouped;
   N = 200. A first arm P pass had a termination bug (resident extinction with testers present ended the replicate
   as a separate outcome) and was discarded; the diverse-world 1b for arm T is exploratory.
8. Stage 3: supply restricted to in-pair slots (otherwise the union of on-path equivalents is the whole catalogue);
   arm T run beside the registered arm M cell as exploratory.
9. The report is generated by `src/tbr_writeup.py` from the generated tables (repo convention for runs/*.md).
