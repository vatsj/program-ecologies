# Spec: rival networks across islands along I ≫ N, and the mN scaling rule, 2026-10-05

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-05-rival-islands-gpt-6.1-sol.md`) and revised; changes marked [after review]. Committed before launch. To be run by an Opus subagent.

[after review] The object has three limits: island size, island count and observation time. A separated patchwork is *metastable*, not absorbing: deleterious migrants have positive fixation probability and arrive repeatedly, so the quantity is the network-loss *hazard* and its survival curve, not a freeze. Migration continues after certification; the topology is the complete island graph, replacement is uniform, time is in generations of I·N births, and unresolved runs stay in every denominator.

## Why

The seed lottery resolves compatibility *on* an island (RESULTS "compatibility among co-seeded establishers": two
self-cooperators cannot hold a stable mixture), but 2 of 100 runs at n = 9, (100, 256) froze certified-*separated*:
`BOX1(THEM(ME))` on 255 islands and a P*-family program on one, mutually defecting across islands yet every island
efficient. Along I ≫ N, with many independent establishment trials, rival networks on different islands become likely.
DEFERRED 1 lists two open items this spec addresses: whether migration merges rival networks, separates them, or lets
one win; and how mN should scale along the path so islands stay independent during nucleation (the merging pilot gave
mN·T_nuc ≈ 6 / 60 / 600 against N = 400 as independent / partly merged / merged).

Migration between two mutually-defecting networks is a conflict: a migrant from network A into an island held by B
gets P against B while B's residents get R among themselves, so it is deleterious and dies; the same the other way.
So separation should be stable under migration, and the metapopulation freezes into a patchwork whose island-level
P(C,C) is 1 but whose *cross-island* P(C,C) (if migrants' encounters are counted, or if the islands are later
merged) is not. Which network holds more islands is then decided at nucleation, by establishment rates and by the
first established island's spread, not by competition afterwards.

## Design

`src/seeds_in_n.py` kernel (modal arm, ε = 0, iid seeds, certification with the separated category), n ∈ {9, 12} so
that rival establishers exist (P*'s family and PrudentBot are absent at n = 6).
1. **Static:** the establisher pairs that mutually defect, their masses, and for each pair the per-mutant fixation
   probability of a migrant of one into an all-other island at N ∈ {100, 400} (deleterious, by how much), and the
   establishment rate of each from all-D.
2. **Separated-seed experiment** [after review: specified]. For each of the three heaviest mutually-defecting
   establisher pairs (A, B), its own cell: I islands of N = 100 seeded iid from μ, with two of them *replaced* by an
   all-A and an all-B island; I ∈ {16, 64, 256}, mN ∈ {0.1, 1, 10}; 40 runs per cell; horizon 10⁵. Report, with
   unresolved runs in the denominator: the category at the horizon (both networks present / one lost / neither /
   unresolved); the per-generation hazard of losing a network and its survival curve; the number of islands *held*
   (largest class in the network) by each at the horizon; which holds the majority; per-island establishment times and
   whether each island's winner descends from a local establisher or an immigrant (ancestry); and the counterfactual
   cross-island P(C,C) under uniform mixing, labelled as a counterfactual. Controls [after review]: m = 0; one-network
   pre-seeding (A only); and two homogeneous networks with no iid background.
3. **Natural separation rate:** iid seeds only, N = 100, I ∈ {64, 256, 1,024} [after review: several I, and a larger
   I/N point], n = 9 and 12, mN ∈ {0.1, 1}, 100 runs per cell and 200 more at any cell whose rate is below 0.05 (a 1–5%
   event needs them): the fraction of runs with two mutually-defecting networks present at the horizon, with binomial
   intervals, and the composition when so. Establishment rates of each rival are measured in the actual iid background
   (first-certified-island counts by network), not only from all-D.
4. **The mN rule** [after review: factorial, and the right clock]: N ∈ {100, 400} × I ∈ {16, 64} (plus (100, 256)) ×
   mN ∈ {0.03, 0.1, 0.3, 1, 3, 10}, 40 runs per cell, n = 9. Record *per-island* establishment times (not the
   first-island extreme), migrant arrivals at each island before its local establishment, the replacement fraction
   those arrivals represent, and local-versus-immigrant ancestry of each island's winner. Report the efficient fraction
   and the pairwise island-outcome correlation against two candidate controls, arrival exposure (migrants per island
   before local establishment) and replacement fraction, rather than assuming mN·T_nuc/N.
5. **Merge test:** take each separated frozen metapopulation and merge all islands into one well-mixed population of
   I·N at ε = 0; report which network wins and how fast (the within-population resolution, which the two-class
   argument says is bistable: the larger wins).

## RE predictions (Fable)

1. **Separation is long-lived under migration** [after review: a hazard, with falsifier aligned]. The per-generation
   hazard of losing a network is below 10⁻⁵ at mN ≤ 1 (median lifetime above the 10⁵ horizon), so both networks are
   present at the horizon in at least 0.8 of runs at mN ≤ 1 and at least 0.5 at mN = 10; lifetimes shorten with
   migration flux. *Falsifier:* both-present fraction below 0.6 at mN ≤ 1 at any I.
2. **Island counts are decided at nucleation, and track measured establishment-and-colonization rates.** The network
   with more locally established islands before the first immigrant-founded island holds the majority at the horizon
   in at least 0.8 of runs; my bet is that this is the heavier-prior network (FairBot's family) in at least 0.8 of runs,
   with the measured rates in the iid background as the predictor sol asks for. *Falsifier:* the P*-family holding the
   majority in more than 0.3 of runs, or majorities uncorrelated (rank correlation < 0.3) with measured rates.
3. **Natural separation grows with I toward 1** [after review: sol is right that with fixed positive establishment
   probabilities for both rivals, observing both tends to 1 as I grows; "enduring rarity" is withdrawn]. The
   both-present fraction is 0.01–0.05 at (100, 256), n = 9, higher at n = 12, and higher again at I = 1,024, consistent
   with 1 − (1 − p_B)^I for the rival's per-island establishment p_B measured in item 3; it is flat in mN at mN ≤ 1.
   *Falsifier:* a both-present fraction that falls from I = 256 to 1,024.
4. **The mN rule:** the efficient fraction is flat in mN while mN·T_nuc/N < 0.1 and falls once mN·T_nuc/N > 1, with
   the drop between those points; islands' outcomes are uncorrelated (pairwise correlation < 0.1) in the flat region.
   *Falsifier:* a fall of more than 0.2 while mN·T_nuc/N < 0.1.
5. **Merging resolves by size in clean two-type merges** [after review: restricted]. When the merged population holds
   essentially two homogeneous networks, the larger wins in at least 0.9 of cases; with family mixtures or near-ties no
   time bound is claimed, and the resolution time is reported. *Falsifier:* the minority network winning in more than
   0.3 of clean two-type merges.

**What it would mean.** If 1–2 hold, the I ≫ N path produces long-lived patchworks: efficient island by island, with
rival networks held apart by migration on the observed timescale and their proportions fixed at nucleation by
establishment rates. Since natural separation tends to 1 in I (3), "almost all seeds" holds for island-level efficiency
and fails for metapopulation-level universality along I ≫ N, unless the network-loss hazard makes the patchwork resolve
on a timescale the path can afford; [after review] growing separation lifetime and eventual universality can coexist
under different orders of the three limits, and the hazards are what decide which. 4 gives the rule DEFERRED 1 asks
for, in terms of arrival exposure or replacement fraction. If 1 fails and migration merges rival networks quickly, the
two-class argument extends across islands and patchworks resolve.

## RS predictions (Jacob)

(Optional.)

## Procedure for the subagent

Follow CLAUDE.md discipline. Commit `predictions/2026-10-05-rival-islands.md` carrying the RE predictions before any run;
static item 1 comes after that commit. At most 3 workers; the largest cells are I = 256 of N = 100 (25,600 programs) for
up to 10⁵ generations, which took seconds to a minute before; measure first and predeclare any reduction. Do not edit
RESULTS.md, REJECTED.md, THEORY.md, CLAUDE.md, DEFERRED.md or NOTATION.md; do not touch `runs/d8dcd7ee9a/row.json`;
hand back draft RESULTS, REJECTED, THEORY and DEFERRED text, at most 5 lines on what matters, and the branch
(`git branch --show-current`) and commits.
