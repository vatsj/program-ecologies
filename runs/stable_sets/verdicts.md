## Addendum cells (run after the first counted pass, disclosed; no prediction scored on them): the N trend at mN = 1

Fraction of islands and consensus runs (fair / unequal), L seeds, mN = 1, 20 runs (N = 100: 40):

| N | fair 2,000 | unequal 2,000 | fair 10,000 | unequal 10,000 | consensus at 10,000 (fair / unequal) | median generation to consensus |
|---|---|---|---|---|---|---|
| 50 | 0.84 | 0.15 | 0.83 | 0.15 | 16 / 3 of 20 | 660 |
| 100 | 0.74 | 0.14 | 0.81 | 0.17 | 31 / 7 of 40 | 1,496 |
| 150 | 0.64 | 0.14 | 0.67 | 0.25 | 11 / 5 of 20 | 2,284 |
| 200 | 0.50 | 0.22 | 0.15 | 0.75 | 2 / 15 of 20 | 3,765 |
| 300 | 0.47 | 0.09 | 0.24 | 0.69 | 3 / 10 of 20 | 5,496 |
| 400 | 0.47 | 0.06 | 0.37 | 0.42 | 1 / 4 of 20 (15 unresolved) | 6,743 |

The fair-pair consensus under migration is a small-island effect: from N = 200 the metapopulation ends on an unequal pair
in most runs that reach consensus, the direction of the chain (unfair 0.59 of π at N = 100).

## Forced residence, second measure

Time until a target island first *holds* (≥ 25 generations) a class other than the target (KM median, censored at
10,000), and what it holds: fair: not reached (0.70 censored), all 192 exits to unequal pairs; unequal: 638, to a
member 416 and to another unequal pair 224; wasteful: 723 (time spent mixed), to unequal 407, member 231; grand: 1,584,
to a member 560, unequal 79. First measure (first departure of ≥ 25 generations from the target, in the table above):
fair 776 (0.40 censored), unequal 121, grand 41, wasteful 26.

## Verdicts

Main cell L (length prior), N = 100, I = 64, 40 runs; horizon 2,000 unless stated; mN = 0 runs all close by
generation ≈ 300, so their 2,000 and 10,000 columns coincide.

**The RS's claim** ("each element of the stable set shows up on an island").

| cell | weak form (every element of V\* on some island) | strong form (island support inside a stable set) |
|---|---|---|
| L, mN = 0 | **40/40** (constants K: 40/40; the independence baseline at q = 0.28 gives 0.995) | **0/40** (0.72 of islands on outcomes in no stable set: unequal 0.42, wasteful 0.23, disagreement 0.07) |
| L, mN = 1 | **0/40** at 2,000 and 10,000 (the archipelago settles on one pair) | 33/40 (0.82) at 2,000 and 10,000, by consensus on *one* fair pair |
| L, mN = 1, N = 200 | 2/20 at 2,000, 0/20 at 10,000 | 0.40 at 2,000, **0.25** at 10,000 (15/20 runs end on one unequal pair) |

*Scored:* the weak form holds without migration, where it is a consequence of role symmetry and pairwise coordination
(constants alone give it; nothing in it tests stability), and fails under migration; the strong form fails without
migration, and holds under migration at N ≤ 150 only because one member takes over every island, which is selection
of a single element, not the set; at N ≥ 200 it fails. **The claim fails in both forms in the regimes that test it.**
The selection question among stable sets is empty: **V\* is the unique myopic stable set** on the game's outcomes, on
G6, G8 and on both extended grids.

| # | prediction | outcome |
|---|---|---|
| RE 1 | coverage ≥ 0.9 at mN = 0; member occupancy ≥ 0.6 | coverage **held** (1.00); occupancy **failed, falsifier fired** (0.281 [0.263, 0.300] ≤ 0.4) |
| RE 2 | role symmetry across runs within 0.1; support inside V\* alone in ≥ 0.5 of runs; tilted seed on a discriminatory line ≥ 0.3 | symmetry held on the falsifier (pooled member shares 0.34 / 0.35 / 0.31; modal-member shares 0.31 / 0.45 / 0.25, one band miss of 0.12, falsifier 0.2 not fired); within-run clause **failed at mN = 0** (0/40), held at mN = 1 (0.82); tilted clause **failed, falsifier fired** (0 islands: no discriminatory element is realizable in this game, as registered) |
| RE 3 | non-members transient (median ≤ 200); ≤ 0.1 of islands on non-members | grand visits short (KM median 2 generations, 0.18 visits per run); wasteful islands **absorbed** at mN = 0 (0.60 censored) but transient at mN = 1 (median 2); ≤ 0.1 **failed** (0.72 at mN = 0; 0.14 / 0.18 at mN = 1); **falsifier fired at mN = 0** (unequal pairs 0.42 ≥ 0.25 at 10,000) and at mN = 1, N = 200 (0.75); not at mN = 1, N = 100 |
| RE 4 | member flips via an outsider; ≥ 0.8 of exit steps on M arrows; consensus ≤ 0.3 at 10,000, through bridges | **failed, both falsifier clauses fired**: 8 of 1,350 member → member flips pass through an outsider class (the rest through member-mixed states, 0.90 by pure drift); 175 / 385 = 0.45 of steps out of a non-member follow an M arrow; consensus in 38/40 runs at 10,000 (0.95); constants alone reach it (K1 0.90), so no bridge is needed |
| RE 5 | modal = weak within 0.1 | **held at mN = 0** (paired, Δ fair 0.002 ± 0.007); at mN = 1 the band missed narrowly on selection (strong form 0.70 vs 0.82, Δ fair −0.11 ± 0.16, paired, not significant); falsifier (≥ 0.25) not fired |
| RE 6 | islands on myopic, not farsighted-only, outcomes | **falsifier fired at mN = 0** (0.42 of islands on outcomes farsightedly stable under TU effectiveness but in no myopic stable set: the six unequal pairs and (2, 2, 2)); not fired at mN = 1, N = 100 (0.14 / 0.18); fired at N = 200 (0.75 at 10,000). The farsighted sets on R are every efficient singleton (TU), or V\* plus three held-player pairs (game effectiveness) |
| RE 7 (Gemini) | V\* < 0.4 and all pairs > 0.7 at mN = 0; a sweep by 10,000 at mN = 1 | **held** on every number: V\* 0.28, all pairs 0.93 (fair + unequal alone 0.698), unequal > fair; consensus 0.95 at 10,000. Its mechanism (greed against accommodators) is not what happens: the constants arm reproduces mN = 0 exactly, and the unequal share of efficient pair islands (0.60) is below the two-orientation count (2/3); at mN = 1 the sweep is to a *fair* pair at N ≤ 150 and to an unequal pair at N ≥ 200. **Scored against RE 1: Gemini's prediction wins.** |
| S1 | V\* the unique stable set on R | **held** |
| S2 | V\* stable on the grids; no discriminatory set on G6 | **held** (none on G8 either) |
| S3 | mN = 0: q ∈ [0.2, 0.45], unequal ∈ [0.3, 0.55], pairs > 0.7, coverage ≥ 0.95, strong ≤ 0.05 | **held** (0.28, 0.42, 0.93, 1.00, 0) |
| S4 | mN = 1 at 2,000: fair ∈ [0.2, 0.45], unequal ≥ 0.5 of pair islands | **failed, falsifier fired** (fair 0.74; unequal 0.15 of pair islands); at N ≥ 200 by 10,000 the unequal clause holds |
| S5 | member flips: ≥ 0.8 no outsider, ≥ 0.7 pure drift | **held** (0.994; 0.90) |
| S6 | member → unequal flips ≥ 0.7 drift-prepared | **failed, falsifier fired** (0.07; 0.61 concurrent, 0.24 single-slot strict: under migration the second slot's new class is usually already present at ≥ 10%) |
| S7 | K and M within 0.05 of L at mN = 0 | **held** (0.004, 0.002) |
| S8 | tilted slot 3 is the low member ≥ 0.5 of its pair islands | **held** (0.63 vs L's 0.33); 0 discriminatory islands |
| S9 | U more mixed or in disagreement than L by ≥ 0.1 | **held** (0.97 disagreement vs 0.07) |
| S10 | forced entry: member and unequal ≥ 0.5, wasteful ≤ 0.3, grand ≤ 0.4 | **held** (0.60, 0.51, 0.07, 0.13) |
| S11 | residence wasteful < unequal < member; grand longest | order **held** (26 < 121 < 776); grand clause **failed** (41); falsifier not fired |
| S12 | C = M on R; chicken {R1}, {R2} | **held** |
| S13 | ≥ 0.8 unresolved at 2,000; ≤ 0.3 consensus at 10,000 | first clause **held** (0.90 unresolved); second **failed** (0.95) |
| S14 | extended grids: grand ≤ 0.1, pairs ≥ 0.7 | **held** (grand 0.009 / 0.011; pairs 0.84 / 0.80; discriminatory-line elements 0.006 / 0.004 of islands) |
| S15 | a singleton fair pair is farsighted stable; RE 6 void on R | first clause **held**; "void" **failed** (unequal pairs and (2, 2, 2) are farsightedly stable too) |

**Chain (separate object).** The weak-arm chain at N = 100 rerun on the same grammar reproduces the published numbers
to four decimals (fair 0.373, unfair 0.590, wasteful 0.026, grand 0.010; E[max share] 0.596; P12 = P13 = P23 = 0.330;
circulation 10⁻¹⁹): π puts 0.627 on outcomes in no stable set. The lottery and the chain are not pooled.
