# Spec: almost all seeds give good outcomes? Persistence without mutation along N ≫ I and I ≫ N, 2026-10-04

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-04-almost-all-seeds-gpt-6.1-sol.md`) and revised; changes marked [after review]. Committed before launch. To be run by an Opus subagent.

## Why

The RS proposes a result of the form "almost all seeds give good outcomes": with probability → 1 under the complexity
prior, and ideally under a range of priors, an unmutated population seeded iid from the prior ends efficient. His proof
device is persistence: certain configurations persist forever without mutation, and the prior decides which ones tend to
arise. His structural claim: island population must grow faster than the island count, otherwise some island is seeded
with a clique or a faker lineage that then spreads.

**Re-opened REJECTED entry:** "Seeding randomness as a substitute for mutation" (2026-09-30). That verdict rested on the
weak arm (fakers present), uniform-over-programs seeding, and the I ≫ N regime (N = 100 fixed, I up to 1,024). None of
those is the regime proposed here, so the evidence does not bear on the claim.

## Precise statement

Seeds are iid draws of size N per island from the prior μ over programs at cutoff n. "Ends efficient" means the frozen
(absorbed) metapopulation has P(C,C) ≥ 0.95 averaged over islands. The claim is a limit along a path in (N, I):

    P_μ(seed ends efficient) → 1 as the seed grows along the path.

[after review] **The theorem target is a decomposition,** not persistence alone: (i) seed concentration (the iid seed's
composition concentrates at μ as N grows); (ii) deterministic basin robustness (μ lies in the basin of an efficient
endpoint of the replicator, with a margin); (iii) stochastic escape and spread bounds (neutral drift out of a non-strict
endpoint, and migration-driven spread between islands, bounded as N and I grow), uniform in the language cutoff. Object 1
tests (ii) and is a diagnostic; Object 2 tests (iii) at finite sizes. The order of limits matters: lim_N lim_t (fix N,
wait for absorption) is what Object 2 measures; lim_t lim_N (replicator) is Object 1. A persistent replicator endpoint does
not establish efficient absorption at finite N, because drift can leave a non-strict endpoint over long times.

[after review] **The regime boundary is a hypothesis about bad-seed probabilities,** not about I/N as such. If a bad island
seed (no reciprocator, or a persistent spoiler configuration) has probability about e^(−cN), its occurrence across the
metapopulation is governed by I·e^(−cN). The subagent should estimate, per cell, the per-island probability that the seed
contains no FairBot (modal) or contains a faker lineage (weak), and report I times that probability next to the outcome.

The regime split, which the experiment tests:
- **N ≫ I.** Each island's seed composition concentrates at μ by the law of large numbers, so the within-island dynamics
  approach the deterministic replicator started at μ. The claim then reduces to a static question: is μ in the basin of
  an efficient attractor that no program in the language can invade without mutation? "A range of priors" means that
  basin contains a neighbourhood of μ.
- **I ≫ N.** Rare compositions appear somewhere. Any persistent configuration that spreads by migration takes over
  however rare it is. This is where the old run found defection: a faker lineage always survived somewhere.

## Object 1: the replicator from μ (static, cheap)

`src/chain.py: replicator` on the full class payoff matrix of each arm, started at x₀ = μ (class masses under the length
prior), integrated to its ω-limit (rest point, or reported as a cycle under rule 4).
- Arms: the weak arm without X and `ROLE` (W0, `src/matched_control.py`), the full weak arm L_6 with `ROLE` and X (for
  comparability with the old island runs), and the modal arm (`src/modal.py: build`), each at n = 6, 7, 8, and 9 where
  feasible.
- Priors: the length prior as implemented; the length prior with its per-node base changed to 2, 4 and 8; tempered μ^β
  with β ∈ {0.5, 2}; uniform over programs; uniform over classes. State how each is normalized.
- Report per (arm, n, prior): the surviving set and its masses, P(C,C) at the endpoint, and **persistence**: the maximum
  growth rate at the endpoint over every class in the language, with the classes attaining it. An endpoint is persistent
  iff no class has positive growth rate; neutral classes (zero growth rate) are listed, since they are the drift roads
  that mutation would open but a seed without them does not. [after review] "Extinct" means share below 10⁻⁶ at the
  endpoint, stated as such; positive coordinates stay positive at finite time. Check endpoint stability under
  perturbation: add 10⁻² of each neutral class (ALLC first) and of small multi-class mixtures, re-integrate, and report
  whether the endpoint is recovered. Vary the integration tolerance by 10× and report residual growth rates.
- Basin boundary: interpolate x₀ = (1 − t)·μ + t·uniform for t ∈ {0, 0.25, 0.5, 0.75, 1} and report the largest t at
  which the endpoint is still efficient.

## Object 2: ε = 0 islands along the two paths (absorption lottery)

`src/islands.py` at ε = 0, seeding 'prior' (iid from μ), mN = 1, complete island graph, w = 0.3, PD, horizon 10⁵
generations with freeze detection, 20 runs per cell (40 at the two end cells of each path, for intervals). Arms: the
full weak arm L_6 with `ROLE` (as in `runs/islands_count.md`), the modal arm at n = 6 ('modal6'), and [after review] W0,
the weak arm without X and `ROLE`, whose grammar and prior match the modal arm's, so that the weak/modal contrast is not
confounded by X and `ROLE`.

[after review] **Freeze, certified.** A run is *certified absorbed* when every island is monomorphic and no migrant
between any two islands can change any island's composition (a migrant of class q into an all-a island with
u(q, a) ≤ u(a, a) and, if equal, the run is still reported as absorbed only if the neutral migrant's class is already a's
class). A run with islands monomorphic but neutral cross-island migrants possible is *metastable*. A run with any
polymorphic island at the horizon is *unresolved*. Report the three categories separately, never pooled. Migration is
mN = 1 migrant per island per generation, with a generation = I·N births; state this in the runs file.
- **N ≫ I path:** I = 4, N ∈ {100, 400, 1,600, 6,400}.
- **I ≫ N path:** N = 100, I ∈ {4, 16, 64, 256}.
- **Diagonal:** (N, I) ∈ {(200, 8), (400, 16), (800, 32)}, where N = 25·I.

Report per cell: the fraction of runs that freeze efficient, defecting, or other; mean final P(C,C); the median freeze
generation; the number of runs not frozen at the horizon (reported as unresolved, not as either outcome); and the
composition of the frozen states.

For the modal arm also report the mechanism along N ≫ I: time to extinction of ALLC within islands, and whether any
FairBot island was lost after ALLC was gone.

[after review] **Controls.** (a) A no-migration control (mN = 0) at (N, I) = (400, 4) and (100, 64) per arm, giving the
per-island lottery alone. (b) Single-migrant fixation assays: the probability that one FairBot migrant into an all-D
island of size N fixes, and one D migrant into an all-FairBot island, at N ∈ {100, 400, 1,600}, by Monte Carlo with
Wilson intervals. These measure the spread rates directly. (c) Wilson intervals on every fraction; 20 runs cannot show
a probability tending to one, so verdicts are about the ordering of cells and the end-cell fractions with intervals.

## RE predictions (Fable)

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
   its fixation is ∝ N^(−1/2), not the pure-drift 1/N [after review: sol predicts 1/N; the assay in control (b) decides].
   *Falsifier:* efficient fraction below 0.5 at N = 6,400, or the assay giving a slope of −1 over N.
5. **Islands, modal, I ≫ N:** the efficient fraction also rises with I, since more islands means a higher chance that some
   FairBot island survives the start and then seeds the rest; at least 0.6 at I = 256. The time to freeze grows with I.
   *Falsifier:* efficient fraction at I = 256 below its value at I = 4. [after review] Sol predicts no guaranteed
   monotone increase, since takeover depends on directional migration rates; this is a live disagreement, and control
   (b) supplies the rates.
6. **Islands, weak, both paths:** the efficient fraction is at most 0.15 everywhere and falls along I ≫ N, as before. Along
   N ≫ I it is at most 0.05 at N = 6,400, because every island carries both `THEM(^C)` and its fakers. *Falsifier:* weak
   efficient fraction at least 0.3 in any cell.
7. **Diagonal:** modal efficient fraction rises along the diagonal; weak falls or stays below 0.15.

**What it would mean.** If 1, 4 and 5 hold, "almost all seeds are good" holds for unfakeable programs in both regimes at
n = 6, and the RS's N ≫ I condition is sufficient but not necessary in a faker-free language. If 4 holds and 5 fails, the
condition is necessary: seeding many small islands lets rare bad configurations spread. If 2 and 6 hold, the claim fails
for fakeable languages in every regime, which places the result on the same footing as the lim_N results: unfakeability
is the condition, and mutation is not what makes the weak arm fail. The static persistence table is the candidate proof
object for the N ≫ I regime: the claim becomes "μ lies in the basin of a persistent efficient endpoint", checkable at
each n.

## RS predictions (Jacob, 2026-10-04, before results)

Along the N ≫ I path, cooperation should appear as islands grow. No claim is staked for few islands; the hope is about
large island populations, not about the small-N cells.

## Procedure for the subagent

Follow CLAUDE.md discipline. [after review] Write and commit `predictions/2026-10-04-almost-all-seeds.md` carrying the RE
predictions above *before any computation beyond language sizes and class counts*, Object 1 included. Predeclare any
budget reduction (horizon, runs per cell) in that file before running, and report censored cells as unresolved rather
than comparing shortened runs. Check that
`src/islands.py` supports 'prior' seeding for the 'modal6' game and ε = 0 freeze detection at these sizes; the largest
cell is 25,600 programs for 10⁵ generations, so measure one run's time first and reduce the horizon or runs per cell if
it exceeds the budget, stating the change. At most 3 workers; stop cells projected beyond 2 hours; do not edit
RESULTS.md, REJECTED.md, THEORY.md or CLAUDE.md; do not touch `runs/d8dcd7ee9a/row.json`; hand back draft RESULTS,
REJECTED and THEORY text, at most 5 lines on what matters, and the branch and commits.

## RE addendum after commit (2026-10-04, before results)

Back-of-envelope for the modal arm per island: copies of the unfakeable prover family in the seed ≈ 0.03·N; a fraction
≈ e^(−1.4) ≈ 0.25 survives the scramble while D eats ALLC (the prover earns R where D earns T); each survivor then fixes
in the D sea at ∝ N^(−1/2) (≈ 0.04 at N = 100, ≈ 0.005 at N = 6,400). So P(island ends cooperative) grows only like √N:
≈ 0.03 at N = 100 and ≈ 0.3–0.5 at N = 6,400. With I = 4 that is ≈ 0.1 and ≈ 0.5–0.8, below prediction 4's ≥ 0.9. Once
one island is cooperative the rest follow fast (D migrants die; prover migrants enter neutrally every generation), so
the outcome hinges on whether any island comes out cooperative, which islands raise linearly and N only as √N. Expected
split by arm: many islands help the unfakeable arm and hurt the fakeable ones. Prediction 4 stands as committed for
scoring; this note lowers the RE's expectation at (6,400, 4) to 0.5–0.8.
