# Predictions: almost all seeds give good outcomes? Persistence without mutation along N ≫ I and I ≫ N, 2026-10-04

Status: carries the RE predictions of `specs/2026-10-04-almost-all-seeds.md`, which was reviewed by gpt-6.1-sol
(`reviews/2026-10-04-almost-all-seeds-gpt-6.1-sol.md`) and revised before this commit. Committed before any computation
beyond language sizes and class counts, Object 1 included.

**Executions before this commit:** language sizes and behavioural class counts only.

| arm | n | programs | classes |
|---|---|---|---|
| modal (all four box kinds) | 6 / 7 / 8 / 9 | 1,020 / 4,542 / 19,544 / 89,842 | 51 / 172 / 471 / 863 |
| W0 (weak, no X, no `ROLE`) | 6 / 7 / 8 / 9 | 666 / 2,796 / 11,462 / 49,852 | 12 / 19 / (being evaluated) / — |
| L_n (weak, X and `ROLE`) | 6 / 7 | 3,994 / 23,776 | 112 / — |

The W0 n = 8 square evaluation was started for its class count. W0 n = 9 and L_7 with `ROLE` are not attempted in Object 1
(a square evaluation of 5·10⁴ or 2.4·10⁴ programs exceeds the budget; L_7 needs the sparse provider, which gives no full class matrix).

## RE predictions (Fable), verbatim from the spec

1. **Static, modal arm:** from x₀ = μ the replicator goes to an efficient persistent endpoint (a FairBot-family mixture)
   at every n, with P(C,C) ≥ 0.99 and no class in the language with positive growth rate. ALLC goes extinct first (D
   eats it), then D goes extinct. The endpoint is persistent under every prior listed except uniform-over-programs at
   n ≥ 8, where I expect it still to hold but with less margin. *Falsifier:* any listed prior at any n whose endpoint
   has P(C,C) < 0.9, or a class with positive growth rate at an efficient endpoint.
2. **Static, weak arms:** from μ the replicator goes to defection (P(C,C) ≤ 0.05) at every n and every prior, because
   `THEM(^D)` strictly invades `THEM(^C)` at any frequency. *Falsifier:* an efficient endpoint in either weak arm.
3. **Basin boundary, modal:** the endpoint stays efficient for all t ≤ 0.75 at n = 6. *Falsifier:* efficiency lost at
   t ≤ 0.5.
4. **Islands, modal, N ≫ I:** the certified-or-metastable efficient fraction rises with N: at least 0.5 at N = 400 and
   at least 0.9 at N = 6,400 (I = 4). Mechanism: ALLC is eaten in the first scramble and never returns; a FairBot island
   is uninvadable by D afterwards; a FairBot migrant into a D island is neutral at one copy and advantageous at two, so
   its fixation is ∝ N^(−1/2), not the pure-drift 1/N [sol predicts 1/N; the assay in control (b) decides].
   *Falsifier:* efficient fraction below 0.5 at N = 6,400, or the assay giving a slope of −1 over N.
5. **Islands, modal, I ≫ N:** the efficient fraction also rises with I, since more islands means a higher chance that some
   FairBot island survives the start and then seeds the rest; at least 0.6 at I = 256. The time to freeze grows with I.
   *Falsifier:* efficient fraction at I = 256 below its value at I = 4. [Sol predicts no guaranteed monotone increase,
   since takeover depends on directional migration rates; this is a live disagreement, and control (b) supplies the
   rates.]
6. **Islands, weak, both paths:** the efficient fraction is at most 0.15 everywhere and falls along I ≫ N, as before. Along
   N ≫ I it is at most 0.05 at N = 6,400, because every island carries both `THEM(^C)` and its fakers. *Falsifier:* weak
   efficient fraction at least 0.3 in any cell.
7. **Diagonal:** modal efficient fraction rises along the diagonal; weak falls or stays below 0.15.

Prediction 6 and 7 ("weak") apply to both weak arms in Object 2: L_6 with `ROLE` and X, and W0.

## Design as run (fixed here, before computing)

Code: `src/almost_all_seeds.py` (new). It reuses `chain.replicator`, `chain.fixation`, `modal.build`,
`matched_control.build('W0', n)` and `abm.load_or_evaluate` for L_6; the island dynamics are a copy of `islands._run`
restricted to what this experiment needs, with the stopping rules below.

**Arms.** `modal` = `modal.build(n)` (all four box kinds; 'modal6' in `src/islands.py`); `W0` = `matched_control.build('W0', n)`;
`L6R` = weak L_6 with X and `ROLE` (`islands._load('pd', False)`, as in `runs/islands_count.md`). Reciprocator R:
`BOX(THEM(ME))` (modal), `THEM(^C)` (weak arms). ALLC = the class of `C`.

**Priors (Object 1), each normalized to total mass 1 over the language at cutoff n, then summed per class:**
- `length`: as implemented, μ(p) = 2^(−bits(p)), bits = log2 a(|p|) + 2 log2 |p| + 1 (uniform within a length, Elias-gamma
  length code).
- `base b` (b ∈ {2, 4, 8}): per program μ(p) ∝ b^(−|p|), i.e. each node costs log2 b bits and there is no separate length
  code. At b = 2 this puts most mass on the longest programs; at b = 8 on the shortest. This is my reading of "per-node
  base"; the spec does not define it.
- `temper β` (β ∈ {0.5, 2}): per program μ(p)^β with μ the length prior.
- `uniform-programs`: every program of L_n equal mass.
- `uniform-classes`: every behavioural class equal mass.

**Replicator (Object 1).** `chain.replicator(U, x0)` with its defaults (atol 1e-5, ext_tol 1e-9, rest_tol 1e-8), on the full
class payoff matrix. "Extinct" in reports means share < 10⁻⁶ at the endpoint. Tolerance check: atol × 10 and ÷ 10 and
ext_tol × 10 and ÷ 10; residual growth rates reported. Growth rate of class q at endpoint x: (Ux)_q − xᵀUx, over every
class in the language; positive means > 10⁻⁹. Persistent iff no class is positive. Neutral = |rate| ≤ 10⁻⁹ and share
< 10⁻⁶. Perturbations: add 10⁻² of each neutral class in turn (ALLC first), of all neutral classes together (10⁻² total),
and of 5 random three-class mixtures (10⁻² total, seed fixed); re-integrate; "recovered" iff the new endpoint's P(C,C)
is within 10⁻³ of the old one and its support (share ≥ 10⁻⁶) has the same cooperative/defecting character. Basin
interpolation: x₀ = (1 − t)·μ + t·uniform, with uniform over classes (as the spec's end point) and, as a second line, over
programs; t ∈ {0, 0.25, 0.5, 0.75, 1}. Efficient endpoint = P(C,C) ≥ 0.95.

**Seeding (Object 2), a deviation from the spec's wording.** The spec says "seeding 'prior' (iid from μ)". The existing
`islands.py` 'prior' seeding is not iid: it seeds every program once and fills the rest from μ, which is infeasible here
(I·N = 400 < 1,020 programs) and is not the claim's object. I use a new seeding: each slot iid from μ (the length prior's
class masses), drawn per island as Multinomial(N, μ). Not comparable slot-for-slot with `runs/islands_count.md`, which
seeded uniform over programs.

**Island dynamics.** As `islands._run` at ε = 0, w_g = 0, complete island graph, w = 0.3, PD, mN = 1 (per-death
migration probability m = 1/N, so one migrant per island per generation), a generation = I·N births. Checks every 20
generations.

**Stopping and categories (never pooled).**
- *Certified, outcome-frozen:* every pair of surviving classes (globally) has the same payoff. Fitnesses are then equal for
  ever and the outcome cannot change (composition can still drift neutrally). Includes the single-class case.
- *Certified, separated:* every island monomorphic, and for every ordered pair of distinct island classes (q, a), a q
  migrant into an all-a island is strictly disadvantaged, u(q, a) < u(a, a). This is the spec's certified absorption.
  At finite w such a migrant still fixes with positive probability; I report the largest such Moran fixation
  probability per run.
- *Metastable:* at the horizon every island monomorphic, but some cross-island migrant is neutral or advantaged.
- *Unresolved:* some island polymorphic at the horizon. Its current P(C,C) is reported but counted as neither outcome.

Runs stop at the first certification. Outcome of a certified or metastable run: *efficient* if mean island P(C,C)
≥ 0.95; *defecting* if mean island P(C,C) ≤ 0.05 and mean payoff within 0.05 of P = −1; *other* otherwise.
"Efficient fraction" in predictions 4–7 = (certified or metastable, efficient) / runs in the cell.

**No-migration control (mN = 0).** Islands are independent; a run stops when every island is locally outcome-frozen
(its surviving classes pairwise payoff-identical). Reported per island.

**Cells.** N ≫ I: I = 4, N ∈ {100, 400, 1,600, 6,400}. I ≫ N: N = 100, I ∈ {4, 16, 64, 256} ((100, 4) shared with the
first path). Diagonal: (200, 8), (400, 16), (800, 32). 20 runs per cell, 40 at the end cells (N = 100 and 6,400 at
I = 4; I = 256 at N = 100). Controls (a) at (400, 4) and (100, 64), 20 runs. Three arms.

**Budget rule (declared now).** Horizon 10⁵ generations. Before the sweep I time one run of each arm at (N, I) =
(6,400, 4) (to horizon or certification). If a cell's projected wall time (runs × time per run ÷ 3 workers) exceeds 2 h,
its horizon is cut to the largest of 5·10⁴, 2·10⁴, 10⁴ that fits, the cut is recorded in the runs file, and the runs
not certified by then are unresolved. Timing runs are the first replicate of their cell and are kept.

**Mechanism traces (modal).** Per island: first generation at which ALLC is absent; global ALLC extinction generation.
"Cooperative island" = island with ≥ 90% of its agents in classes with self P(C,C) ≥ 0.95 other than ALLC. Count
islands that go from cooperative to < 50% cooperative, before and after global ALLC extinction.

**Seed-probability estimates (per cell, analytic from μ).** P(island seed has no FairBot) = (1 − μ_FB)^N, and the same
for the whole cooperative unfakeable family; P(island seed contains at least one faker of R) = 1 − (1 − μ_fakers)^N,
fakers = classes q with u(q, R) > u(R, R). Each reported with I times it.

**Control (b), assays.** Isolated island, two types, exact (`chain.fixation`) and Monte Carlo (Wilson 95%): one FairBot
into all-D and one D into all-FairBot (modal), and the same for `THEM(^C)` vs D (W0), at N ∈ {100, 400, 1,600}.
Slope = least squares of log ρ on log N over the three N.

## Subagent predictions (Opus RE, added; not Fable's)

S1. The assay slope for FairBot into all-D is −0.5 ± 0.05, matching the chain's ρ(FairBot | all-D) slope (RESULTS "Modal
    (Löbian) arm": −0.49 to −0.50, the same Moran process). D into all-FairBot is below 10⁻⁶ at N = 100.
S2. In the weak arms the per-island probability that the seed contains a faker of `THEM(^C)` tends to 1 as N grows (the
    bad configuration is not exponentially rare in N, it is typical), so I × P(bad) grows along both paths.
S3. In the modal arm, ALLC is globally extinct by generation 200 in every run with N ≥ 400, and no cooperative island is
    lost after that in any run.
*Falsifier of S1–S3:* assay slope outside [−0.6, −0.4]; the weak faker probability falling with N; a cooperative modal
island lost after global ALLC extinction.
