# Rewarding prudence: fission–fusion with a light post-merge tail under world K (notes, 2026-10-21)

Spec `specs/2026-10-21-prudence-world-k.md` (reviewed by gpt-6.1-sol and then gemini-4-argon; its two amendment sections
supersede the earlier text where they conflict, the later one winning). §1 is written by hand before any code of this
run and before any counted cell. §2 (code validation, costs) is appended after the code and before any counted cell.

Base, imported unchanged: provenance, realizable scaling, Pangaea (the fission–fusion cell `pg_L_100_128_r100_ff200`),
the removing-rivals target and annealed schedule machinery, and `src/world_k.py`'s world switch (L: `runs/provenance`
tables; K: `runs/detectors/K` tables with L's Q kept as `Q`). S-nonself, ε = 0 until the merge, w = 0.3, r = 100
production encounters per Moran event, calibrated mN = 1 on the 128 islands of 100, one population of 12,800 after the
merge at generation 200. Every number is an ε = 0 seed lottery followed by a **finite-(N, horizon) re-injection
diagnostic at N = 12,800, never π** (CLAUDE.md rule 5).

*Disclosure (before any code).* The cached static tables are untracked; they were copied read-only from the
`agent-a7781c…` worktree (detectors, provenance, world_k, removing_rivals, realizable_scaling, pangaea, annealed
directories; nothing modified at the source). Before writing this section I ran throwaway scripts (kept in the session
scratchpad, not in the repo) on those tables and on the stored world-K fission–fusion rows (`runs/world_k/cells_C.json.gz`,
cell `pg_L_100_128_r100_ff200`). What they printed is stated as *looked at* where it enters a prediction below
(statics: prior masses of the sets, the fixed-list edge, the identity of the sucker-depleted set in the two worlds;
stored A = 0 finals: guarded or unguarded winner by run). No post-merge arrival dynamics of any kind had been run.

## 1. Design

### 1.0 The object in one paragraph

The RS wants the dynamics to *reward prudence* (DEFERRED 1, 2026-10-17): a prudence premium is a good reason for
PrudentBot-type programs (those that refuse to cooperate with certified unconditional cooperators, "guarded" below) to
outcompete FairBot-type programs, proportional to the sucker supply set by the schedule. At ε = 0 the premium is spent
once the seed's suckers are eaten (at the merge, generation 200, the sucker share is 0 in both worlds), after which
guarded and unguarded members of the target network are neutral; the stored A = 0 winners are guarded in 5/20 (L) and
4/20 (K) runs. A light re-injection tail after the merge keeps supplying suckers, so a premium may keep paying; under
world K the former TwinD family (Q) are certified unconditional cooperators that pass PrudentBot's ⌜D⌝ guard, which the
spec suspected would shrink the premium. The run measures what the tail does to the guarded share, the target network,
the off-target FairBot variants and the whole-population loss rate, in both worlds, with a sucker-depleted control that
separates the premium from resilience to arriving predators.

### 1.1 Cells, schedule, pairing

- **Cells:** world ∈ {L, K} × arm ∈ {A0, A52, A156, SD52}, 20 runs each (replicates 0–19; 160 runs). A is the
  *delivered* number of fresh founders per 100 programs by the tail's end (amendment 1). SD52 is A = 52 with the
  sucker-depleted arrival stream (§1.4).
- **Phase 1 (identical in all arms of a world, and by construction the stored cells):** 128 islands of 100, ε = 0,
  generations 0–200 with the Pangaea kernel; replicate rep's founders are `PG.founders_pg` (same spellings in both
  worlds, units the world's E units). Merge at generation 200 (`PGRun.merge`, seed
  `kernel_seed_pg(12800, 1, rep) ^ 0x5DEECE66D`, as in the stored cells).
- **Phase 2 (tail):** one population of N = 12,800, generations 200 to 10,200 (t = g − 200 ∈ [0, 10,000)). Fresh
  founders arrive at the birth step: with probability ε_g per Moran event the victim is replaced by a founder drawn from
  the prior (empty lists, S-nonself), as in the annealed run's kernel. **ε_g N = λ_g, the expected arrivals in
  generation g:** λ_g = (A·128)·w_t / Σ_t w_t with w_t = (1 + t/1000)^(−2) (t₀ = 1,000, amendment 2.1). The sum is over
  the 10,000 discrete tail generations, so *the expected delivered total is exactly 128 A* (6,656 at A = 52, 19,968 at
  A = 156) and the realized count is binomial about it; realized counts are logged. The shape's mass within the first
  1,000 generations is 0.55, so the delivered fraction of the infinite-horizon integral is ≈ 0.91 by 10,000.
- **Phase 3 (chase):** 2,000 generations (to g = 12,200) without arrivals.
- **Pairing:** every arm of one (world, rep) shares the founders and the merge seed, so the arrival-event stream is
  nested (the arrival test is `u_5(seed, ev) < ε_g`, so the events at A = 52 are a subset of those at A = 156 when the
  schedules are proportional, which they are) and the n-th arrival draws its spelling from the same counter-based stream
  (`fseed` depends on rep only). Worlds share founders and `fseed`, so arriving spellings are identical in K and L.
  SD52 maps the *same uniform* through the depleted cumulative prior.
- **Stopping:** A0 may stop at the exact frozen stop (one type whose own encounters change nothing; later statistics are
  carried forward exactly). Arrival arms never stop before the tail ends; after generation 10,200 they may stop frozen.

### 1.2 Sets, fixed in advance (frozen to the tables, before any cell)

All of these are functions of the world's tables only; none is read off the population.

- **Target T (the PrudentBot network):** the unit-level set `RR.static(LS)['T']` = self-cooperating units mutual with
  PrudentBot-H (`if(CHK(them,me,C),if(CHK(them,^D,D),C,D),D)`, unit 123): **235 units in L, 298 in K** (looked at).
  This is the "frozen 235-unit target of Removing rival networks and its world-K counterpart from the detector run".
- **Prudent (guarded) target:** T members that **defect against certified CooperateBot** (`A[u, C-H] = 0`). **Unguarded
  target:** T members that cooperate with it (FairBot is in T and unguarded). By prior mass on H units, T spellings are
  0.0399 (L) / 0.0401 (K), of which guarded 0.0235 / 0.0226 and unguarded 0.0164 / 0.0175 (looked at). This split is my
  addition to the spec's list (declared here, before any cell): the spec's "PrudentBot's own share" is one tree among
  the guarded ones (prior mass 2.6·10⁻⁴, three spellings), and the premium's effect on *which* T members win is carried
  by the guard, not by the tree.
- **PrudentBot's own share:** individuals whose spelling's tree is PrudentBot's (`tau[tsp] == tPB`), any certificate
  state.
- **Off-target FairBot variants** (the spec's "FairBot variants that PrudentBot would not certify"): the Pangaea class
  `CBo` at unit level: self-cooperating, mutual with FairBot-H, not mutual with PrudentBot-H (not in T) and not a sucker. Their prior mass is 0.0014 on spellings (looked at), so they are
  rare arrivals; their *residence* is dominated by the seed and drift, not by arrivals.
- **Suckers:** units that cooperate with DefectBot-H (`A[u, D-H] = 1`; the Pangaea `S`/`S-` classes, prior mass about
  0.5 on E units); **certified** if the unit holds a C certificate (`BLC[u, 0] ≥ 0`), else **uncertified**.
- **Identity and anti-punisher shares:** `decompose`'s `ident` and `APnet`; plus Q (the former TwinD family) by spelling.

### 1.3 Ancestry and decomposition (amendment 2)

Every individual carries a lineage id: 0 for a resident at the merge, and a fresh positive id for each arrival
(inherited by offspring, as in the annealed kernel; in the new kernel the parent is found by rejection sampling so the
cost is not O(N) per birth). At every checkpoint the shares above are split into *resident-descended* and
*arrival-descended*. Each arrival is logged with (generation, spelling, victim's type, majority type, lineage id, its
payoff against the population, the population's mean payoff). The change in a class share between checkpoints is
decomposed into **immigration** (arrivals into the class minus victims drawn from it, from the arrival log) and
**reproduction** (the remainder: births, certificate production, deaths). A **colonization** is the first checkpoint at
which one arrival lineage holds at least half of the population; it is *selected* if the arrival's initial payoff
exceeded the population mean (strictly) and *drift* otherwise, as a crude version of the annealed run's classifier
(disclosed: it classifies the arrival, not the lineage's later fate).

### 1.4 The sucker-depleted control (amendment 2.2)

Arrivals drawn from the prior with **uncertified unconditional cooperators removed, the same syntactic set in both
worlds**, renormalized, at the same rate: spellings whose *E-state unit* (no certificates, what a fresh founder is)
cooperates against all five probe units {CooperateBot-H, DefectBot-H, FairBot-H, AP-H, PrudentBot-H}, except Q (the
former TwinD family, so that identity arrivals are unchanged). This is 4,673 spellings, prior mass **0.3756**, identical
as a set in L and K (looked at). Realized as the same cumulative prior with the removed spellings' increments zeroed.
Predictions 1 and 2 are judged against SD52 as well as A0 (amendment 2.4).

### 1.5 The premium, measured two ways, plus the realized selection advantage (amendment 3)

- **Primary: the fixed-list payoff edge.** For a fixed list of opponent spellings (identical in K and L): CooperateBot
  `C`; the former TwinD family Q; `if(CHK(me,them,D),D,C)`; and the prior-weighted sets "uncertified suckers" (the E-state
  set above plus the sucker spellings of §1.2) and "certified suckers" (H-state): edge(x) = payoff(PrudentBot-H against
  x-H) − payoff(FairBot-H against x-H), payoffs 2 / 1 / 0 / −1 for (D vs C / C vs C / D vs D / C vs D), from the world's
  `A` matrix (twin quirks ignored: the references differ from x). The summary is the **edge per arriving
  uncertified-sucker founder**, edge averaged over the *realized* arriving spellings of that class, times the number of
  such arrivals, per 100 programs. Looked at: the prior-weighted edge over sucker spellings is 0.6828 in both worlds (L and
  K agree to every digit printed), and for H-state certified suckers 0.826 (L) / 0.824 (K); `C` itself has edge +1.
- **Secondary: the encounter-weighted edge** over the realized population at each checkpoint: Σ_j x_j [payoff(PB-H, u_j)
  − payoff(FB-H, u_j)] over the living sucker types j, and normalized per unit of sucker share; integrated over the tail
  and divided by A. (Inflated in K by certified suckers that survive: that is why it is secondary.)
- **Realized selection advantage:** the mean payoff of prudent target members minus that of unguarded ones (count-
  weighted, from the run's own payoff sums), at each checkpoint where both exist.

### 1.6 Statistics and endpoints

- **Over time** (every 10 generations to merge + 600, every 20 after): P(C,C), living types, T share, prudent and
  unguarded T shares, PB-own share, `CBo` (off-target) share, sucker shares (certified / uncertified), identity and AP
  shares, the arrival-descended share of each, the dominant network. Heavy statistics (closure, class composition) at
  snapshots t ∈ {0, 50, 100, 500, 1000, 2000, 5000, 10,000, 12,000}.
- **Composition at the merge** (generation 200, amendment 2.5): the same statistics at the instant of the merge, so the
  island-scramble premium is separated from the post-merge one.
- **Residence times** (population-share × generations): off-target (`CBo`), uncertified suckers, certified suckers,
  identity, over the tail (t ∈ [0, 10,000]); by the rectangle rule at the checkpoint spacing.
- **Endpoints at the tail's end (t = 10,000) and the chase's end (t = 12,000):** universal-open (the network
  `decompose`/`closure` already defines: M ≥ 0.95 and an open holder), universal-on-target (T share ≥ 0.95), prudent
  majority (prudent T ≥ 0.5), P(C,C) unconditionally, whole-population loss (closure status `lost`, or P(C,C) < 0.1),
  the winning network's identity (guarded or not, PB tree or not), and the support / transition structure (the number of
  distinct dominant networks at checkpoints and of dominant-network changes in the tail), not only means.
- **Drift and selected colonizations** counted as in §1.3.
- **Inference:** 20 paired runs per cell. Differences by paired bootstrap and exact McNemar / sign tests; claims of zero
  are read with their binomial upper bounds (0/20 ⇒ ≤ 0.14 at 95%). All claims are finite-horizon statements at
  N = 12,800 about this tail shape and this fission–fusion path.

### 1.7 Outcome regions for the headline (declared now)

The question is whether this tail rewards prudence. Write G(a, w) for the mean prudent-target share at the tail's end
(t = 10,000) in arm a, world w (paired over 20 runs).

- **R-reward:** G(A52) ≥ G(A0) + 0.25 **and** G(A52) ≥ G(SD52) + 0.20 in the world: prudence rises with the sucker
  supply, and the rise is not just resilience to arrivals.
- **R-resilience:** G(A52) ≥ G(A0) + 0.25 but G(A52) − G(SD52) < 0.10: arrivals raise the guarded share without a
  sucker supply (e.g. because guarded programs are better arriving predators, not because suckers pay).
- **R-null:** |G(A52) − G(A0)| < 0.10.
- **R-harm:** universal-open at the tail's end ≤ 0.75 at A = 52 (the spec's falsifier of prediction 4), or the guarded
  share falls.
Regions are per world; "the tail rewards prudence" needs R-reward in L and K. Intermediate cells are reported as such.

### 1.8 Hand predictions (they become numbered predictions with falsifiers in `predictions/2026-10-21-prudence-world-k.md`)

*My reading of the dynamics, before any arrival run.* After the merge the population is one type or a few, mostly
unguarded T members (stored winners: unguarded in 15/20 L, 16/20 K). A certified arriving sucker is mutual with an
unguarded resident (neutral, drifts in) and is exploited by a guarded one (dies at rate about w). So under a tail the
standing sucker share is roughly (sucker arrivals alive) / N in unguarded populations and about 0 in guarded ones. A
guarded arrival (prior mass about 0.023, i.e. roughly 160 at A = 52 and 470 at A = 156) invades an unguarded resident
population with advantage equal to the sucker share, so a first few percent of sucker share suffices for repeated
invasion attempts with the usual constant-selection fixation chance. Hence the guarded share should rise steeply with
A, and SD52 (which removes 0.376 of the arrival mass, essentially the unconditional cooperators) should not rise
(guarded programs would be neutral against unguarded ones with no suckers to eat). The world difference is carried only
by Q (0.0007 of the prior) and the AP-network mass moved by K (0.0126), so I expect the two worlds to agree on the
premium to within the noise of 20 runs; the spec's prediction 3 is, on the fixed-list measure, a tie. The risk side:
at A = 156 an unguarded population can accumulate sucker share of order 0.3 to 0.5 before guarded invaders arrive and
win, and defector arrivals (prior mass 0.38, class D) gain when the sucker share exceeds 1/2; I expect some
whole-population failures there, more than at A = 52, in both worlds.

Numbered (full text, falsifiers in the predictions file):
- **P1 (static).** The fixed-list edge per arriving uncertified sucker founder differs between K and L by less than 1%
  (looked at: identical). The spec's prediction 3 (K smaller) will not be supported.
- **P2.** G at the tail's end: A0 reproduces the stored 0.25 (L) and 0.20 (K) winner-guarded rates; A52 ≥ 0.60 and A156 ≥
  0.70 in both worlds; SD52 ≤ G(A0) + 0.15. R-reward in both worlds.
- **P3.** The target (T) share at the tail's end is not the right place to look for the premium: it is at its ceiling at
  A0 (mean ≥ 0.95 in both worlds), so the spec's prediction 1 read as "PrudentBot network share up by ≥ 0.1" must fail by
  the ceiling; PB's own tree share rises by less than 0.10 (its prior mass is 1/90 of the guarded set's).
- **P4.** Universal-open at the tail's end ≥ 0.90 at A52 in both worlds; at A156 in [0.70, 0.95] in both worlds
  (the spec's counter-prediction 7 holds in L if below 0.85).
- **P5.** Off-target residence: at A0 it is carried by the stored off-target runs (L's rep 5 only; K none), so in K the
  paired difference A52 − A0 is positive (transient arrivals) and in L it is ≤ 0 only if the tail cures rep 5; the spec's
  prediction 2 fails in K.
- **P6.** Ancestry: at A52 and A156, at least 0.8 of the tail-end prudent share is arrival-descended where the share rose
  (invasion, not resident reproduction).
- **P7.** Delivered counts within 3% of 128 A in every run.
- **P8 (validation).** A0 reproduces the stored fission–fusion cells state for state (pcc, living types, T share) in
  both worlds.

### 1.9 Validation plan (code, before any counted cell)

(a) A0 reproduces the stored `pg_L_100_128_r100_ff200` traces in both worlds (reps 0–2) at every stored checkpoint to
the stored precision; (b) the arrival kernel at ε = 0 equals the Pangaea kernel state for state over a merged
population; (c) the schedule's discrete sum equals 128 A (and the SD cumulative prior zeroes exactly the removed set);
(d) lineage conservation: every individual's lineage is 0 or an arrival id, arrival-descended counts equal the sum over
arrival lineages, arrivals are logged once; (e) paired streams: the arrival sequence of A52 equals the first 52/156 of
A156's events in spelling and order on a short run; (f) the cost probe on a discarded replicate (990) to 3,000
generations for A = 156 in both worlds. Drop order if the projected total exceeds ~12 hours on 3 workers
(amendment 5): A = 156 in L first, then the SD control in L; the chase and the other cells are never dropped.

## 2. Code, validation, probes and costs (appended after the code, before any counted cell)

### 2.1 Code

`src/prudence_kern.py` (the Pangaea island kernel with the annealed run's arrivals and lineage tracking by rejection
sampling, see its docstring), `src/prudence.py` (schedule, frozen sets, run object, statistics), `src/prudence_run.py`
(`statics`, `validate`, `probe`, `cells`), `src/prudence_report.py`, `tests/test_prudence.py` (5 tests, 70 s, pass).
Existing `src/` files are untouched; the Pangaea kernel's copier cache is dropped in the new kernel (C-donor only).

### 2.2 Validation (`runs/prudence-validate.json`; before any counted cell)

- **A = 0 reproduces the stored fission–fusion cells state for state in both worlds.** Replicates 0–2 in L and K
  (cell `pg_L_100_128_r100_ff200` of `runs/world_k/cells_C.json.gz`): at every stored checkpoint (every 10 generations
  to 500, every 50 after) P(C,C), the dominant network's share M, the target share and the number of living types agree
  to the stored 5-decimal precision (158 / 192 / 240 / 97 / 192 / 233 comparisons in K 0, L 1, L 0, L 2, K 1, K 2: 0
  differences in 6 of 6 runs), and the frozen stop falls at the stored generation (K 0 5,900; L 1 and K 1 7,600; L 2
  2,850; K 2 9,650; L 0 unfrozen at 10,000 as stored). This includes the merge and the post-merge arrival kernel at ε = 0.
- **Test (`test_arrival_kernel_equals…`):** after the merge, 40 generations of the new kernel at A = 0 equal the Pangaea
  kernel's slots, counts and type count exactly; at A = 52 and 156 the arrival log is consistent (one record per
  arrival, lineage ids 1..n unique, arrival-descended individuals ≤ n, counts sum to N), A = 52 delivers about a third
  of A = 156's arrivals over the same 40 generations, **A = 52's founder sequence is a prefix of A = 156's** (paired
  streams), and world K's arriving spellings equal world L's.
- **Statics (`runs/prudence-static.json`).** The schedule's discrete sums are 6,656 and 19,968 exactly (0.5501 of each
  within the first 1,000 generations; first-generation rate 7.3 and 22.0 arrivals, last 0.06 and 0.18). T has 235 units
  in L and 298 in K. The SD set is the **same 4,673 spellings, mass 0.3756**, in both worlds; Q is outside it.
  **The fixed-list edge per arriving uncertified-sucker founder is 0.6828 in both worlds** (0.8255 over the SD set),
  0.8261 (L) and 0.8244 (K) over H-state certified suckers (relative difference 0.2%), +1 for `C`, and 0 for the former
  TwinD family in both worlds' H-state; E-state edges are 0 (a fresh founder is uncertified, so neither PrudentBot nor
  FairBot cooperates with it and the payoffs are equal). This is the looked-at number of §1.5 now computed by the code.

### 2.3 Probes (discarded replicate 990; `runs/prudence/probe*.log`, `probe.json`)

K, A = 156, to the chase's end: 114 s, 19,943 arrivals (expected 19,968), frozen at generation 10,220 (one type) and
23,571 types created. L, SD52, 107 s, 6,579 arrivals, not frozen (a polymorphism of off-target variants to the end).
L A = 156 to generation 400: 30 s including compilation. The probes ran beside the sibling weak-wing run's 3 workers.
Sanity reads of the two kept probe rows (not counted, not scored): in K A156 the certified-sucker share rose to 0.2 within
the first 2,000 tail generations and a guarded type fixed near t = 7,000, resident-descended (the arrival-descended
share is 0 at the end), so the prudent winner need not be an arrival; in L SD52 no sucker share built up and the run
ended on an off-target FairBot variant.

### 2.4 Costs, plan and one declared extension

Per run about 100 s (A0 about 60 s, which stops at the exact frozen stop); 160 runs ≈ 4.5 worker-hours, ≈ 1.5 hours on
3 workers. Far below the 12-hour line, so **no drop-order step is applied**. Declared before any counted cell: the spec's
20 runs per cell (replicates 0–19) are the counted cells and carry the verdicts; because the endpoints are all-or-nothing
by run and the paired contrasts are small, **replicates 20–39 are run afterwards as a precision extension** (the annealed
run did the same). Every verdict is reported on 0–19 and on 0–39; where they disagree, both are said. The batches are
`python3 src/prudence_run.py cells --reps 20 --out main` and then `--rep0 20 --reps 20 --out ext`.

### 2.5 Deviations and conventions (declared before any cell)

- **Residences** use the rectangle (trapezoid) rule at the checkpoint spacing (10 generations to t = 600, then 20); after
  an exact frozen stop the values are carried forward exactly.
- **Ancestry** is the lineage of the individual (0 resident at the merge, else the arrival id), inherited at birth from a
  uniformly chosen parent individual of the chosen type; certificate production keeps the lineage. The decomposition into
  immigration and reproduction is **by lineage** (the change of the arrival-descended part of a class against the
  change of the resident-descended part), not by victim accounting; the log also stores each arrival's victim type.
- **Colonization classifier:** an arrival lineage that reaches half of the population; *selected* if the arrival's
  initial payoff against the population exceeded the mean (strictly), else *drift*.
- **"Universal-open" and "lost"** are `decompose`'s M ≥ 0.95 with an open holder, and closure status `lost` or P(C,C) < 0.1.
- **The tail's end is t = 10,000 (generation 10,200); the chase's end t = 12,000 (12,200).** A run that freezes after
  the tail's end carries its end state forward exactly.

### 2.6 Launch (written before the first counted cell)

`nohup bash runs/prudence/batch.sh &` from the worktree: `cells --reps 20 --out main` (replicates 0–19, 160 runs,
`runs/prudence/cells_main.json.gz`, log `main.log`) and then `cells --rep0 20 --reps 20 --out ext` (replicates 20–39,
`cells_ext.json.gz`, `ext.log`); `runs/prudence/batch.done` appears when both finish. Jobs are ordered by arm (A156, A52,
SD52, A0), then world, then replicate, three workers, one job per process (pool of 3, two jobs per child). The rows are
resumable (finished keys are skipped on relaunch). Then `python3 src/prudence_report.py --rows
runs/prudence/cells_main.json.gz` (and with `cells_ext.json.gz` appended for the 40-run tables) writes `runs/prudence.md`
and `runs/prudence.json`.

### 2.7 What happened to the batch (deviation, recorded after the fact)

The first launch hung at 0% CPU from 12:33 on 21 October (a multiprocessing deadlock in the pool) with 5 of the 160 main
runs unfinished and was killed by the RE on 22 October; the RE relaunched `runs/prudence/batch.sh`, which reran the 5 missing
main runs (finished keys are skipped) and then the extension. The runs are deterministic, so the rerun rows are those the
hung pool would have written. The hung log is `runs/prudence/main.log.hung-2026-10-21`. All 160 main and 160 extension rows
exist (`cells_main.json.gz`, `cells_ext.json.gz`, `batch.done`).

## 3. Results in one paragraph (details: `runs/prudence.md`, `runs/prudence-verdicts.md`)

At A = 52 the tail does not move the prudent (guarded) share in either world (G 0.267 → 0.231 in L, 0.231 → 0.243 in K,
within noise; sucker-depleted control 0.246 and 0.181), the network share falls, and universality stays 0.95–1.00. At
A = 156 the prudent share is higher (0.41 and 0.40; 0.43 and 0.30 on 40 runs) but there is no depleted control at that
exposure, the gain is resident-descended (arrival-descended 0.02–0.09), the standing sucker share is only a few percent,
and the realized payoff advantage of guarded over unguarded target members is negative where both are present. The fixed-list
premium per arriving sucker is identical in the two worlds (0.6855). The depleted control left part of the sucker class and
is a weak control. The RE's predictions 1, 2, 3 and 7 and my S2, S6 and the A156 clauses of S4 and S9 failed or fired their
falsifiers; RE 4, RE 5, S1, S10 and S12 held (full list in the verdicts); one failure is my arithmetic (S7 clause 2). Post hoc: `src/prudence_extra.py` (`runs/prudence-extra.json`).
