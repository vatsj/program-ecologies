# An identity-resistant target: narrowing the PrudentBot network to members identity cannot exploit (notes, 2026-10-17)

Spec `specs/2026-10-17-identity-resistant-target.md` (reviewed by gpt-6.1-sol and gemini-4-argon; its "Amendments after
review" supersede the earlier text where they conflict). §1 is written by hand before any code of this run and before
any counted cell. §2 (code validation, the executed check of the partition, mechanism assays, projected costs) is
appended after the code and before any counted cell.

Base, imported unchanged: the removing-rivals machinery (target 𝒯, tracker, drift classifier), the Pangaea machinery
(fission–fusion merge, overlap-free kernel, network decomposition), the annealed machinery (schedules, paired founder
streams, takeover bookkeeping), on the realizable-scaling / provenance language (grammar P, n = 7, 12,546 spellings,
4,162 run trees, 17,394 units, prior L, S-nonself, lack rule, w = 0.3). r = 100 production encounters per Moran event
everywhere (at N = 200 this is the native r = N/2). Every number from an ε = 0 cell is a lottery statistic at finite
(N, I, horizon); every number from a rain cell is a finite-ε approach-rate diagnostic, never π. **R-move and the
R-proportional control are surgery on the mutation prior (amendment 1): they are counterfactual diagnostics that locate
the leak, not designs; the realizable claim is judged on the arms under L.**

*Disclosure (before this section).* Before writing it I read the spec, CLAUDE.md, RESULTS "Removing rival networks",
"Cliques on a Pangaea" and "Annealed mutation", the three notes and the code; cloned the untracked cached tables
(`runs/lt_genes/static/`, `runs/provenance/{static/, OSV.npy, SPO.npy, prod_exec.json}`) read-only from the
annealed worktree (copy-on-write, nothing modified at the source) and ran `tests/test_annealed.py` (5 passed: the clone
reproduces the stored kernels); and made static lookups with throwaway scripts on the tables and on stored rows (the
partition below, the syntactic test, prior masses, holder occupancy in stored runs, a timing probe of 24 executed
plays). No dynamics of any kind have been run.

## 1. Design

### 1.1 The object in one paragraph

The removing-rivals target 𝒯 (235 units: self-cooperating and mutual with PrudentBot's H unit u_PB) is frozen for
scoring (uot₂₃₅). Most of its members cooperate with identity holders that defect against them, which is how identity
enters target islands: as prey of a *selected* TwinD arrival (the annealed run's whole-run loss) or through exploitable
shadows drifting into target islands under rain. The run (a) partitions 𝒯 into members identity can exploit and members
it cannot, semantically, and tests a syntactic signature of resistance; (b) asks what each failure channel costs by
moving the prior mass of the exploitable members to the resistant ones (R-move), against a control that moves the same
mass to every non-identity spelling (R-proportional), under three regimes: ε = 0 fission–fusion (the Pangaea run's
remedy for the seed's cliques), ε = 0 islands (200, 64), and annealed / constant rain at I = 8; and (c) measures the
channel directly with forced TwinD challenges.

### 1.2 Semantic exploitability and the frozen challenge set (amendment 5)

- **Challenge set 𝒬** (frozen now): every identity unit of the table universe, i.e. provenance's `ident` (units that
  self-cooperate with their own quote, defect in twin play, and are mutual with no other unit of the universe): **21
  units in 14 run trees.** It contains the 8 identity units reachable by S-nonself production from the prior (the
  TwinD family Q: 10 spellings in 4 run trees, μ(Q) = 7.13·10⁻⁴; units 1312, 2712, 3879, 3881 and their C-listed
  variants 12603, 12997, 13497, 13499) and 13 units not reachable by S-nonself from any founder (zero prior mass as a
  founder state, reachable by production under other rules: e.g. 14312 = run tree 147
  `if(and(CHK(them,me,C),CHK(me,them,C)),C,D)` carrying script 7).
- **Exploitable target unit:** t ∈ 𝒯 with some q ∈ 𝒬 such that t cooperates with q and q defects against t
  (A[t, q] = 1, A[q, t] = 0), **on the ideal table or on executed plays** (the term evaluator `L.play` at the kernel's
  fuel K, a timeout counting as D; both directions, on the first two spellings of each run tree). The union is taken:
  a unit is exploitable if either judgement says so. **Resistant** otherwise. Distinct units only (an identity unit is
  never a target unit's own quote).
- **Ideal-table partition (lookup): 165 exploitable, 70 resistant.** It is the same with 𝒬 replaced by the 4 identity
  holders seen in the stored runs, by the 8 S-nonself-reachable identity units, or by the 21-unit universe. The
  executed check is code and is reported in §2 before any cell; if it moves a unit, the union rule above decides and the
  move is disclosed there.
- **By run tree.** The 235 units lie in 225 run trees (157 exploitable, 68 resistant); **no run tree has units in both
  classes**, so the partition lifts to spellings: a spelling is *exploitable-target* (E) if its run tree has an
  exploitable target unit, *resistant-target* (Res) if its run tree has a resistant one. μ_L(E) = **0.02788** (the
  removing-rivals "0.027"), μ_L(Res) = **0.01232**.
- **What the exploitable members are.** 0.0268 of E's 0.0279 is *suckers* at the H state (cooperating with
  DefectBot's H unit, e.g. `if(CHK(them,^D,D),C,D)`, which cooperates with anyone certified to defect against
  DefectBot, DefectBot and TwinD included); only 0.0011 are establishers. Of Res's 0.0123, 0.0118 are establishers.
  So "exploitable by identity" is, by mass, "exploitable by certified defectors"; R-move moves sucker mass to
  establisher mass, and is a large *founder boost* of the target's establishers (×3.26) as well as a removal of the
  channel. This is Gemini's caveat, and the R-proportional control and the per-founder statistics are there to
  separate the two.

### 1.3 The syntactic test

- **Signature:** a spelling is *guarded* if its program outputs D whenever the atom `CHK(them,me,C)` is false, for
  every assignment of the other atoms (atoms treated as independent; a variant treating `CHK(x,y,C)` and `CHK(x,y,D)`
  as exclusive gives the same counts). By soundness of the checker, a guarded unit cooperates only with partners that
  cooperate with it, so it is unexploitable by anyone, identity or not.
- **Lookup:** the guard is constant on run trees. **50 of the 70 resistant units are guarded (0.714); 0 of the 165
  exploitable units are.** The 20 unguarded resistant units are disjunctions or fall-throughs whose second way to
  cooperate is a condition no identity unit meets: `or(CHK(them,me,C), X)` with X ∈ {`CHK(them,them,D)`,
  `CHK(them,^C,C)`, `CHK(them,^D,C)`, `CHK(me,me,D)`, `CHK(me,them,C)`, `CHK(me,^C,C)`, `CHK(me,^C,D)`,
  `CHK(me,^D,C)`} in both orders, `if(CHK(them,me,C),C,if(CHK(me,them,D),D,C))`,
  `if(CHK(them,me,C),C,if(CHK(me,^D,D),D,C))`, `if(CHK(me,them,C),if(CHK(them,me,C),C,C),D)`,
  `if(CHK(me,^D,D),if(CHK(them,me,C),C,D),C)`, `if(CHK(them,me,C),C,if(CHK(me,me,C),D,C))`.
- **A sharper reading** (lookup over the 11,365 units of the universe): every guarded resistant unit is universally
  unexploitable (no unit at all defects against it while it cooperates), 13 unguarded resistant units are too, and 7
  are exploitable by some non-identity unit. **The guard is (on this grammar) a sufficient test of universal
  unexploitability; identity-resistance is a weaker, challenge-relative property**, which is why the syntax misses 20
  of 70. RE 1 is scored on these counts (verdict table); its outcome is fixed by this lookup, not by a cell.

### 1.4 Occupancy in the stored runs (lookup)

- Removing-rivals Part 0 (300 runs at N ≥ 200, generation 2,000): **22,723 target islands held by resistant units,
  355 by exploitable ones (0.015)**; 27 of 300 runs have an exploitable target island at all. Most-held: FairBot
  (unit 3, 2,185 islands), then `if(or(CHK(them,me,C),CHK(me,^D,C)),C,D)` (unguarded resistant, 916),
  `if(or(CHK(them,me,C),CHK(me,me,D)),C,D)` (unguarded resistant, 810), guarded PrudentBot-type programs.
- (200, 64) S-nonself calibrated at 2,000: target-resistant 1,056 islands, target-exploitable 13, closed-open rivals
  125, identity 72, exploitable rivals 14 (20 runs, uot 11).
- Annealed natural cells at 12,000: exploitable holders on 0–11% of target islands per cell (0 in the (800, 8)
  annealed S-nonself cell, 8 of 273 at (1,600, 8)).
- So the exploitable members carry 70% of the target's prior mass and hold ≈ 1.5% of its islands: they lose the
  scramble (they are suckers). Their role is as **shadows and prey**, not as holders.

### 1.5 Priors and the coupling (amendment 4)

- **L**: the length prior. **R-move (Rm)**: μ(s) = 0 for s ∈ E; μ(s) = μ_L(s)·(1 + μ_L(E)/μ_L(Res)) = 3.263·μ_L(s) for
  s ∈ Res; unchanged elsewhere. **R-proportional (Rp)**: μ(s) = 0 for s ∈ E; μ(s) = μ_L(s)·(1 + μ_L(E)/μ_L(W)) =
  1.0287·μ_L(s) for s ∈ W = every spelling outside E and Q (Res included, so Rp also adds 0.00035 to Res); Q
  unchanged. Totals are preserved exactly (tested).
- Seeded copies per island of 100 (fission–fusion): Res 1.23 (L) → 4.02 (Rm) → 1.27 (Rp); E 2.79 → 0 → 0; Q 0.071
  in all. Per island of 200: Res 2.5 → 8.0; per island of 800: 9.9 → 32.
- **Coupling.** Every founder slot and every rain arrival carries one uniform u. Under L it is mapped by L's inverse
  CDF in the catalogue's spelling order, exactly as the stored runs did (numpy's `choice` with p is `searchsorted` of
  the normalized cumulative sum on `random()`; the kernel's rain draw is a binary search on the cumulative sum), so the
  L arms reproduce the stored runs draw for draw. Under Rm and Rp, u is mapped through the *same* intervals: a u in the
  interval of an unchanged spelling (or of a Res / W spelling) gives that spelling; a u in the union of E's intervals,
  read at its position within that union, is mapped by the recipients' extra-mass quantile (recipients in catalogue
  order, weights μ_L). This is the inverse CDF of each prior on a common ordering in which every unchanged interval
  coincides, so each prior's marginal is exact and two arms differ only at the ≈ 2.8% of slots whose L draw was in E
  (a maximal coupling). Implemented as a piecewise table (boundaries, spelling of each piece) shared by the founder
  code and a copy of the annealed kernel whose rain draw reads the piece table (the only change; with the identity
  table it is the annealed kernel draw for draw). **Founding-prior and rain-prior interventions are not separated
  within an arm: rain draws from the same prior as the founders, in every arm (reported).**
- Seed streams: islands use the scaling run's stream [N, I, rep, SALT] (`random((I, N))`); fission–fusion uses the
  Pangaea run's 12,800 list [12800, rep, SALT_PG] (`random(12800)`) and its nested permutation; rain uses the annealed
  per-island counter draws ru(fseed, i·2²⁴ + n, 6). The sponsored PrudentBot founder (CBP4 spelling, rule H, unit u_PB,
  full list) replaces the founder at C-donor's donor slot of each island (removing-rivals' positions,
  [N, I, rep, SALT, 3]; for fission–fusion the positions of (100, 128)); it is the same slot in every prior.

### 1.6 Cells

| part | cells | priors | sponsor | runs | horizon |
|---|---|---|---|---|---|
| I, ε = 0 fission–fusion | (100, 128), mN = 1, merged into one population of 12,800 at 200 (Pangaea's merge and seed rule) | L, Rm, Rp | no / yes | 20 | 2,200 (2,000 after the merge) |
| II, ε = 0 islands | (200, 64), calibrated mN | L, Rm, Rp | no / yes | 20 | 10,000 (frozen runs stop early, as in removing-rivals) |
| III, rain | (800, 8) and (1,600, 8), S-nonself, annealed K = 3 schedule of "Annealed mutation" (onset 200, t₀ = N/2, cut at 10,000, chase to 12,000) and constant rain with the same delivered total | (800, 8): L, Rm, Rp; (1,600, 8): L, Rm | no | 40 | 12,000 |
| IV, assays | §1.8 | L (holders fixed by construction) | – | §1.8 | – |

The L arms reproduce stored cells: I-L-unsponsored = Pangaea `pg_L_100_128_r100_ff200` (to 2,200); II-L =
scaling `rs_Snon_200_64_cal` (to 2,000) and removing-rivals `rr_spon_200_64` (sponsored, to 10,000); III-L = annealed
`an_i_800`, `an_iv_800`, `an_i_1600`, `an_iv_1600`. They are rerun (not copied) so that every statistic below is
measured the same way in every arm; the reproduction is checked (§1.9).

**Drop order (amendment 2)**, applied only if §2's projection exceeds ≈ 24 hours on 3 workers and disclosed there
before any affected cell: (1) the (1,600, 8) rain cells; (2) the sponsored arms of Parts I and II. The (800, 8)
three-prior comparison is never dropped.

### 1.7 Statistics

- **uot₂₃₅** (islands): removing-rivals' universal-on-target (every island a target island, every pair of holders
  mutual). **uot₇₀**: the same with every holder a *resistant* target unit. **Universal-open** (provenance).
  **On the merged population** (Part I after the merge): the Pangaea decomposition's universal (the dominant compatible
  network M ≥ 0.95 of the population) and universal-open; **uot₂₃₅ = universal and ≥ 0.95 of the population on target
  units** (the T share counts individuals on units of 𝒯, self-cooperating and mutual with u_PB); **uot₇₀ = universal and
  ≥ 0.95 on resistant target units**. Before the merge (generation 200) the island statistics are reported.
- **Occupancy:** target islands (or the population share) held by resistant vs exploitable units, every snapshot.
- **Identity:** identity islands, the maximum identity share, identity takeovers of target islands (annealed's
  definition: a target spell followed, before the island is target again, by an identity holder for ≥ 25
  generations; permanent if identity holds at the end), each attributed: *prey* if a TwinD (Q-spelling) rain lineage
  that arrived on that island colonized it within the episode and was classified *selected* at arrival, *arrival-drift*
  if such a lineage was classified neutral or deleterious, *migrant* otherwise. Reported in total, **per identity
  arrival** (Q-spelling rain founders, pooled over the cell), **per target island-generation** split by the holder's
  class (resistant / exploitable).
- **Exposure by class:** rain arrivals per run by class (Q, E, Res, unconditional cooperators = H unit cooperating with
  DefectBot's H unit, other), reported per prior.
- **Drift:** drift colonizations (removing-rivals §1.9 classifier) of target islands, split by the holder's class at
  arrival and by the colonizer's phenotype (an unconditional cooperator, an exploitable target unit, a resistant target
  unit, other); "drift from resistant islands to any unconditional cooperator" is the first cell of that split.
- **The target's own drift away:** runs that end universal-open but not on target (the Pangaea run's 4/34), and the
  non-target network that won.
- **Scramble:** unheld and all-defect islands at 200 and 2,000; runs lost (all-defect); **per-founder establishment**
  by class (§1.8, M2).
- **Island efficiency** (P(C,C) ≥ 0.95) reported, never used to select.
- **Uncertainty and comparisons (amendment 8):** runs are clusters. Paired run outcomes across priors (same founders
  up to the coupling, same kernel seed): differences in counts with exact McNemar tests on the discordant pairs and
  exact (Clopper–Pearson) intervals; rates per arrival or per island-generation with run-bootstrap intervals (2,000
  resamples, percentile); counts of runs with Clopper–Pearson intervals. Each prediction has supported / contradicted /
  inconclusive regions, declared in the predictions file before any counted cell. Only the decisive comparison is
  extended if inconclusive (declared there).

### 1.8 Mechanism assays (amendment 6)

- **M1, forced TwinD challenges.** One island of N ∈ {200, 800}, every individual holder X (its unit and spelling,
  S-nonself), ε = 0, I = 1; one fresh TwinD founder (the heaviest Q spelling `if(or(CHK(me,me,D),CHK(me,them,D)),D,C)`,
  empty lists, S-nonself) replaces a uniform slot; run until the lineage is lost, or identity holds the island (majority
  identity unit) for ≥ 25 generations ("takeover"), cap 3,000 generations. Holders: exploitable unit 31
  `if(CHK(them,^D,D),C,D)`, unit 87 `if(CHK(them,me,C),C,if(CHK(them,them,C),C,D))` (the annealed run's prey) and the
  most-held exploitable target holder in the stored runs; resistant FairBot (unit 3), PrudentBot (u_PB, the CBP4
  spelling), and the most-held unguarded resistant holder `if(or(CHK(them,me,C),CHK(me,^D,C)),C,D)`. Replicates set in
  §2 (target 1,000 per holder and N). **Neutral baselines:** 1/N (exact), and a fresh `C` (CooperateBot) arrival into
  each holder at N = 200 (the commonest drift colonizer; neutral where the holder cooperates with a certified `C`).
  Static relations first: the Q founder's phenotype against each holder, the drift class (selected / neutral /
  deleterious), and whether every Q spelling has the same class.
- **M2, per-founder scramble establishment** (from Parts I and II, no extra runs): per seeded copy of a class (Res, E,
  Q, and FairBot alone), the probability that an island is held at 200 (Part I) or 2,000 (Part II) by a unit of a run
  tree of that class that was seeded on that island. Unheld and all-defect islands per prior.
- **M3, drift into unconditional cooperators** (from Part III): drift colonizations of target islands by unconditional
  cooperators, per target island-generation, split by the holder class at arrival.

### 1.9 Validation plan (code, before any counted cell)

1. The L coupling reproduces numpy's `choice` (Pangaea list, scaling founders) exactly; the Rm and Rp piece tables have
   the exact marginals (cumulative masses to 1e-12) and change a slot only when its L draw lies in E.
2. The kernel copy with the identity piece table equals the annealed kernel state for state (150 generations at
   (200, 8), rain on).
3. Reproduction: Part I-L-unsponsored against stored `pg_L_100_128_r100_ff200` (traces to 2,200, replicates 0–2);
   Part II-L against stored scaling traces to 2,000 (replicates 0–2) and removing-rivals `rr_spon_200_64` snapshots at
   2,000 (replicates 0–1); Part III-L against stored annealed `an_i_800` snapshots at 2,000 (replicate 0) and the
   arrival and colonization records to 2,000.
4. The partition on the RE's two examples (`if(CHK(them,^D,D),C,D)` exploitable, `if(CHK(them,me,C),C,if(CHK(them,them,C),C,D))`
   exploitable), FairBot and PrudentBot resistant; the executed check over all 235 × 21 pairs, both directions.

### 1.10 Hand predictions (they become numbered predictions with falsifiers)

- *Static (already looked up):* RE 1's claim fails at 0.714 < 0.9 but its falsifier (< 0.7, or a guarded unit
  exploitable) does not fire: inconclusive. Sol's and Gemini's syntactic counter-predictions hold (20 of 70 = 29%
  resistant units unguarded). I expect the executed check to agree with the table on every pair.
- *Fission–fusion (ε = 0).* Universal-open 19–20/20 under every prior (the Pangaea result was 20/20 under L).
  Unsponsored uot₂₃₅: L 16–19 (the stored run's "target ≥ 0.9" was 18/20 at 2,000; target drift away is the failure),
  Rm 18–20, Rp 16–19. Sponsored uot₂₃₅ ≥ 19/20 under every prior. uot₇₀ = uot₂₃₅ in ≥ 0.9 of runs of every arm: the
  exploitable members are suckers, gone before the merge.
- *Islands (200, 64), ε = 0.* R-move boosts the target's establishers 3.3× against unchanged closed-open (0.0154) and
  identity (7·10⁻⁴) mass, so closed-open rival islands fall by ≥ 40% and identity islands by ≥ 30%; uot₂₃₅ at 10,000
  rises from 11/20 (stored) to 14–18/20 (gain +0.15 to +0.35): RE 3 more likely contradicted than supported, and by
  founder boosting (the gain is not tracked by the removal of exploitable occupancy, which is 13 islands of 1,280).
  Rp within ±2 runs of L. Sponsored: L 15/20 (stored), Rm 17–20.
- *Rain.* Under L, selected identity takeovers of target islands are rare: 0–3 in 160 (800, 8) runs, 0–3 in 80
  (1,600, 8) runs (the annealed run had 1 in all its natural cells); so RE 4 and RE 5 are likely inconclusive on
  counts and decided on the composite (§1.7 per-arrival exposure × M1 per-arrival takeover). Under Rm there are no
  exploitable target units anywhere, so its prey channel is 0 by construction; what remains is migrant export of seeded
  cliques. Drift colonizations of target islands: Rm ≥ L in total (3.3× more resistant neutral shadows), while drift
  into unconditional cooperators is unchanged within ×(0.7–1.3) (`C`'s mass is unchanged).
- *Assays.* TwinD into an exploitable holder is a self-cooperating predator (the holder cooperates with it, it defects,
  and its copies cooperate with each other): takeover ≥ 0.26 per arrival (the predator's ρ, plus self-cooperation) at
  both N. Into a resistant holder it is deleterious (mutual defection against residents that cooperate among
  themselves): takeover ≤ 1/1,000 at both N, guarded and unguarded alike.
