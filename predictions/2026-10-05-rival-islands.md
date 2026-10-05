# Predictions: rival networks across islands along I ≫ N, and the mN scaling rule (2026-10-05)

Spec `specs/2026-10-05-rival-islands.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-05-rival-islands-gpt-6.1-sol.md`).
Committed before the static item and before any counted run. Code: `src/rival_islands.py`.

Before this commit the subagent ran (i) a kernel validation against `seeds_in_n._run` on identical seeds with
independent streams (salt 'val'; per-island p at N = 100 0.090 vs 0.085; (100, 4) mN = 1: 0.297 ± 0.019 reference,
0.327 ± 0.019 new, 0.305 ± 0.019 new without lumping, 600 runs each; (100, 16) mN = 0.1: 0.773 / 0.767 / 0.740, 300
runs each), and (ii) nine timing runs (salt 'time'), none counted. Three timing outcomes were seen and inform the
subagent's own predictions S1–S2 below (not the RE's): a one-island network among 255 homogeneous rival islands at
mN = 1 was lost at generation 2,014; a half/half patchwork at mN = 10, I = 256 lost one network at generation 139; a
pre-seeded A/B run at mN = 10, I = 256 lost B by generation 105. The single-migrant fixation probability for a
mutually-defecting pair (below) was computed before writing.

## Design as implemented

**Kernel.** The `seeds_in_n` dynamics (Moran birth-death; parent drawn with weight exp(w·mean payoff) on the source
island; with probability m = mN/N the parent comes from a uniformly chosen other island; victim uniform; complete island
graph; uniform replacement; a generation is I·N births; w = 0.3; ε = 0; iid seeds from the cutoff-normalized length
prior; class data from `spoiler_conditioned.cdata`, so n = 9 and n = 12 share one evaluation). Changes, none of which
alters the law of the process:
1. **Migration continues after certification; separation is never a stopping rule.** A run stops only when globally
   outcome-frozen (every present class pairwise payoff-identical, so no payoff can ever change again) or, at m = 0, when
   every island is locally frozen; otherwise it runs to the horizon of 10⁵ generations.
2. **Exact event skipping:** births that cannot change anything (monomorphic island, labels settled, no migrant) are
   skipped in one geometric draw.
3. **Exact lumping:** classes payoff-identical on the current global support (rows and columns), with the same
   cooperative flag and network tag, are merged (a lumpable Moran process).
4. **Ancestry labels:** on an island not yet established, each individual is local (lineage on the island since the
   seed) or immigrant; inherited within the island, immigrant on a migrant birth, victim's label drawn in proportion
   within its class. Recorded at establishment; frozen afterwards.
The validation above shows agreement with `seeds_in_n._run` within sampling error, with and without lumping.

**Definitions.**
- *Establisher:* self-cooperates, defects on D, not ALLC. *Cooperative class:* self-cooperates, not ALLC.
- *Island established (certified cooperative):* locally frozen and every present class cooperative; checked every 5
  generations to 2,000, every 25 to 10⁴, every 100 after. *Holder:* the largest class on the island.
- *Network tags* for a pair (A, B) of mutually-defecting establishers: A's network = cooperative classes mutually
  cooperating with A and not with B; B's network likewise; bridge = mutually cooperating with both; other.
- *Network lost:* its last individual dies (absorbing at ε = 0; exact birth time recorded). *Held islands:* islands
  whose holder carries the tag. Also recorded: first time a network holds no island.
- *Category at the horizon* (or at stopping), from holders, because at mN ≥ 1 islands carry transient migrants and
  are almost never monomorphic at an instant: **both present** (each network holds ≥ 1 island); **one lost**; **neither**
  (neither holds an island); **unresolved** (horizon reached and some island held by a non-cooperative class). Every run
  stays in every denominator; administratively censored runs (if any) are reported separately.
- *Hazard:* per-generation hazard of the first network loss = losses / total generations at risk (constant-hazard MLE,
  exact Poisson 95% interval), with Kaplan–Meier survival of min(T_A, T_B) and of each network, censored at the
  horizon; survival read at 10², 10³, 10⁴, 10⁵ generations.
- *Ancestry of an island's winner:* local if ≥ 0.5 of the holder class at establishment is local-labelled.
  *Arrival exposure:* migrant births into the island before its establishment. *Replacement fraction:* the immigrant-
  labelled share of the island at establishment.
- *Natural separation (item 3):* at the end of the run, two certified islands (P(C,C) ≥ 0.95) whose holders are
  cooperative and mutually defect.

**Pairs (item 2), n = 9.** The literal three heaviest mutually-defecting establisher pairs are a four-way tie (to
0.04%) between {FairBot, `BOX1(THEM(ME))`} × {`BOX1(THEM(^not(BOX(THEM(ME)))))`, `BOX1(THEM(^not(BOX(THEM(THEM)))))`}
(product 2.75·10⁻⁸ each), which would make two of three cells near-replicates differing only in A. Predeclared instead:
the heaviest pair for each of the three heaviest rivals of the heaviest A = `BOX1(THEM(ME))`:
1. A = `BOX1(THEM(ME))`, B = R1 = `BOX1(THEM(^not(BOX(THEM(ME)))))` (μ_B 5.4·10⁻⁶; rank 1);
2. A = `BOX1(THEM(ME))`, B = R2 = `BOX1(THEM(^not(BOX(THEM(THEM)))))` (μ_B 5.4·10⁻⁶; rank 2);
3. A = `BOX1(THEM(ME))`, B = P* = `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` (μ_B 3.2·10⁻⁶; rank 5), the pair of the two
   certified-separated seeds-in-n runs.
R1 and R2 mutually cooperate with the bridge `BOX1(THEM(THEM))` (μ 0.0051); P* has no bridge and exploits ALLC and
`BOX1(THEM(THEM))`. This selection is ascertained by mass and observation, as sol warns.

**Cells.**
- *Item 2 (separated seed):* per pair, I ∈ {16, 64, 256} of N = 100, islands 0 and 1 replaced by all-A and all-B, the
  rest iid; mN ∈ {0.1, 1, 10}; 40 runs; horizon 10⁵.
- *Controls:* (a) m = 0, A/B pre-seeded, per pair and I, 40 runs; (b) A only pre-seeded (all three pairs share A, so
  run once with pair 1's tags), I × mN as item 2, 40 runs; (c) two homogeneous networks without background, run once
  (the 2×2 game inside every mutually-defecting establisher pair is identical, so pairs differ only by labels): half
  all-A / half all-B, and one all-B island among I − 1 all-A, I ∈ {16, 64, 256}, mN ∈ {0.1, 1, 10}, 40 runs.
- *Item 3 (natural):* iid only, N = 100, I ∈ {64, 256, 1,024}, n ∈ {9, 12}, mN ∈ {0.1, 1}, 100 runs; 200 more at any
  cell whose both-present fraction is below 0.05; Wilson intervals. Rival establishment rate p_B: the fraction of
  islands whose holder at establishment is local-ancestry and a cooperative class mutually defecting with
  `BOX1(THEM(ME))` or FairBot, measured in these runs (the actual iid background).
- *Item 4 (mN rule):* n = 9, N ∈ {100, 400} × I ∈ {16, 64} plus (100, 256), mN ∈ {0.03, 0.1, 0.3, 1, 3, 10}, 40
  runs; plus (an addition, needed for T_nuc and the independent-trials reference) m = 0 at (100, 16) and (400, 16), 40
  runs each. T_nuc(N) = median per-island establishment time at m = 0; p_N = per-island establishment fraction at
  m = 0; reference R(N, I) = 1 − (1 − p_N)^I.
- *Item 5 (merge):* every run that ends at the horizon with two networks present (items 2, 3, control c) is merged into
  one well-mixed island of I·N at ε = 0 (m = 0, stops when locally frozen; horizon 10⁵ generations). *Clean two-type
  merge:* the two largest (lumped) classes hold ≥ 0.98 of the merged population and mutually defect.
- No reduction of the spec's design is needed: timing gave 0.1–15 s per run at the largest cells. Administrative cap:
  any cell projected beyond about 2 hours of wall time on 3 workers is stopped and reported as censored with completed
  generations.

## RE predictions (Fable, from the spec, verbatim in substance) with verdict rules

1. **Separation is long-lived under migration.** The per-generation hazard of losing a network is below 10⁻⁵ at
   mN ≤ 1 (median lifetime above the 10⁵ horizon), so both networks are present at the horizon in at least 0.8 of runs
   at mN ≤ 1 and at least 0.5 at mN = 10; lifetimes shorten with migration flux. *Falsifier:* both-present fraction
   below 0.6 at mN ≤ 1 at any I.
   *Rules:* evaluated on the item-2 cells, per pair and I. Held = every mN ≤ 1 cell ≥ 0.8, every mN = 10 cell ≥ 0.5,
   pooled mN ≤ 1 hazard upper bound below 10⁻⁵, and hazard increasing in mN. Failed (falsifier) = some mN ≤ 1 cell
   below 0.6. Otherwise failed on the numerical clauses that miss, falsifier not fired.
2. **Island counts are decided at nucleation, and track measured establishment-and-colonization rates.** The network
   with more locally established islands before the first immigrant-founded island holds the majority at the horizon
   in at least 0.8 of runs; the bet is that this is the heavier-prior network (FairBot's family, A) in at least 0.8 of
   runs. *Falsifier:* the rival (B) holding the majority in more than 0.3 of runs, or majorities uncorrelated (rank
   correlation < 0.3) with measured rates.
   *Rules:* majority = more held islands at the horizon (a lost network holds none; ties reported and counted as not a
   majority for either). "Measured rates": per cell, the predicted A share (1 + Ê_A)/(2 + Ê_A + Ê_B), with Ê_X the
   number of locally established islands of network X in the iid background observed in the m = 0 control of that
   (pair, I); Spearman correlation over the 27 item-2 cells between this and the observed fraction of runs with an A
   majority. Pooled over all item-2 runs and also reported per pair.
3. **Natural separation grows with I toward 1.** The both-present fraction is 0.01–0.05 at (100, 256), n = 9, higher
   at n = 12, higher again at I = 1,024, consistent with 1 − (1 − p_B)^I for the measured p_B; flat in mN at mN ≤ 1.
   *Falsifier:* a both-present fraction that falls from I = 256 to 1,024.
   *Rules:* "consistent" = 1 − (1 − p̂_B)^I inside the Wilson 95% interval of the observed fraction; "higher" and
   "falls" = point estimates in that direction, called significant when a two-proportion 95% interval excludes 0; the
   falsifier fires on a significant fall; "flat in mN" = the mN = 0.1 vs 1 difference not significant at 95%.
4. **The mN rule.** The efficient fraction is flat in mN while mN·T_nuc/N < 0.1 and falls once mN·T_nuc/N > 1, the
   drop between those points; islands' outcomes are uncorrelated (pairwise correlation < 0.1) in the flat region.
   *Falsifier:* a fall of more than 0.2 while mN·T_nuc/N < 0.1.
   *Rules:* the fall is measured against R(N, I) (the m = 0 independent-trials reference). Island outcome X_i = 1 if
   island i establishes with a local-ancestry winner; pairwise correlation = the intraclass correlation of X across the
   runs of a cell, ρ̂ = (Var(ΣX)/(I·p̂(1 − p̂)) − 1)/(I − 1). Also reported: efficient fraction and ρ̂ against arrival
   exposure and replacement fraction, and which of the three candidate controls (mN·T_nuc/N, exposure, replacement
   fraction) collapses N = 100 and N = 400 best (lowest deviance of a pooled logistic fit of the relative efficient
   fraction on the log control).
5. **Merging resolves by size in clean two-type merges.** The larger network wins in at least 0.9 of clean two-type
   merges; with family mixtures or near-ties no time bound is claimed and the resolution time is reported.
   *Falsifier:* the minority network winning in more than 0.3 of clean two-type merges.

## Subagent's own predictions (written after the three timing outcomes above and the fixation numbers)

Mutual defection between two self-cooperators is a symmetric coordination game (each earns R = 0 at home and P = −1
across); a single migrant of one into an all-other island of N fixes with probability ρ_DD(N) = 1.85·10⁻⁵ (N = 100),
7.2·10⁻⁹ (200), 1.6·10⁻¹⁵ (400) (`chain.fixation`, w = 0.3), against ρ(est | all-D) = 0.042 / 0.030 / 0.021 and
ρ(D | all-FairBot) = 1.7·10⁻⁸ / 3.8·10⁻¹⁵ / 2.5·10⁻²⁸. So separation at N = 100 is shallow: the barrier is about
N·w/4, not the D-into-FairBot barrier.
- **S1.** In control (c) "one all-B island among I − 1 all-A", the hazard of losing B at mN ≤ 1 is within a factor 3 of
  mN·ρ_DD(100) = 1.85·10⁻⁵·mN per generation (single-island regime); B also gains islands at a comparable rate, so its
  survival curve has a heavy tail, not an exponential.
- **S2.** At mN = 10, N = 100 the metapopulation behaves as one coordination population: one network is lost within
  10³ generations in at least 0.8 of item-2 and control (c) runs, the larger network surviving. This contradicts
  prediction 1's mN = 10 clause.
- **S3.** At mN ≤ 1 in item 2, the network-loss hazard is dominated by the nucleation phase (first 10³ generations,
  while the iid background is still being colonized), with a lower post-nucleation hazard; both-present fractions
  at mN = 0.1 are at least 0.8 in every item-2 cell.

## Addendum (committed before running it; after seeing partial item-2 data at N = 100)

Partial item-2 data show one network lost in every run so far at N = 100 (hazard ~7·10⁻⁴ at mN = 1). The static
barrier says the lifetime should grow exponentially in N. One extra control, not in the spec, labelled as an addition:
control (c) at **N = 200**, I = 64, mN ∈ {1, 10}, half/half and one-minority-island presets, 40 runs each.
- **S4.** At N = 200, mN = 1, no network is lost within 10⁵ generations in either preset (S1's rate mN·ρ_DD(200) =
  7·10⁻⁹ per generation); at mN = 10 the half/half preset still loses a network in at least 0.5 of runs (strong
  coupling), the minority preset in at most 0.2.
