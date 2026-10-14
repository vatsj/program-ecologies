# Spec: stable sets on islands: does each element of the vNM stable set show up on an island, and which stable set does the ecology select?, 2026-10-13

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol and gemini-4-argon; to be run by an Opus subagent.
Follow-up to DEFERRED 15 (the RS's equilibrium notion, the leader-value core, and the stable-set reading when the
core is empty) and to RESULTS "Three-player majority divide-the-dollar" and "Fixed-role chicken".

## The RS's claim (verbatim, registered)

> vNM stable sets lend themselves to a very natural claim on our island model: each element of the stable set shows
> up on an island.

## Why

When the leader-value core is empty (chicken, bargaining, majority division), the von Neumann–Morgenstern stable set
is the classical replacement: internally stable (no member dominates another) and externally stable (every
non-member is dominated by some member), with Anesi (2010) showing stable sets as limit sets of myopic dynamics. In
chicken the commitment-with-credible-response dominance relation gives exactly two singleton stable sets, the two
one-sided norms, and RESULTS "Fixed-role chicken" already shows every island landing in one of them by a coin flip.
Three-player majority division is the real test: its symmetric stable set is the three 50–50 pairs, the
rare-mutation chain found a rotating-pair chain (pairs 0.98 of π) with the fair and wasteful splits as transients,
and the island model asks two things the chain cannot: **coverage** (do all three pairs appear across one run's
islands?) and **selection** (the game also has infinitely many *discriminatory* stable sets, one player held at a
fixed small share; which solution does the ecology select?). Selection among stable sets is the analogue, for games
with an empty core, of selection among equilibria where the core is nonempty.

## Design

**Game and dynamics** [after review by sol: the dynamic object registered]. The three-player majority
divide-the-dollar game of RESULTS "Three-player majority divide-the-dollar" (`src/dollar3*.py`: fixed roles, separate
slot populations, the n = 6 weak-arm grammar, demands on the 1/6 grid, a pair's agreement implemented by majority),
on islands: three slot populations of N = 100 per island, I = 64; iid seeds from the length prior (class masses
stated); **ε = 0, no mutation** (a founder type absent from a run can never appear in it; the object is absorption,
not a stationary distribution); Moran updating per slot with the repo's exponential fitness map, a generation = N
birth–death events per slot; migration on the complete island graph at mN ∈ {0, 1}, role-preserving, emigrants
unweighted; common observation horizons 500, 1,000, 2,000, with 10,000 on unresolved runs as a separate column and
unresolved dwell times censored; 40 runs per cell, run-level uncertainty; outcome classes by play (each island by
its modal realized division at tolerance 0.95: which pair at which split, the grand-coalition split, a wasteful
outcome, or mixed), with the exact payoff support and time-window frequencies reported beside the modal class, and
efficiency reported separately. A small **N panel** (N ∈ {50, 200}, 20 runs) on the main cell before any
large-population claim.

**The dominance relations and the stable sets, computed before any cell** [after review by sol: the relations are
specified and the solutions computed, never assumed to inherit the classical sets]. Two relations on the finite
outcome grid: **(M) strict majority dominance**, x ≻_S y iff S is a winning pair and *every* member of S is strictly
better off at x (the classical relation; under *weak* improvement the three equal pairs are not internally stable,
since {1, 2} weakly improves from (½, 0, ½) to (½, ½, 0)); **(C) commitment dominance**, x ≻_S y iff S's members can
change their demands so that, with the complement's credible response, every member of S is strictly better off,
with the commitment set, feasibility, the response (individual best reply, ties broken against the committers, and
improvement required for *every* best reply) all stated, and dominance defined on *policy profiles* (demand
vectors plus off-path responses) with outcome-level invariance established where it holds, since identical realized
divisions can arise from programs with different off-path responses. For each relation: all stable sets found by
exhaustive search on the grid (internal and external stability checked by enumeration), the symmetric set (the
three equal pairs) if it is one, the **discriminatory sets** correctly defined (one player's payoff fixed at c while
the others divide 1 − c in every way the grid allows: a line of three-positive-payoff allocations, not "the pairs
excluding that player"), and the farsighted stable set (Chwe 1994) as the contrast. Every exact payoff vector on the
grid is classified by computed membership in each stable set, with overlaps allowed; "dominated outcome" means
dominated under the relation, which is not the same as excluded from every stable set, and the report keeps the
two apart. [after review by gemini-4-argon] **The grid decides which sets exist:** on the 1/6 grid the discriminatory
line with c = 1/6 cannot split the remaining 5/6 equally, and (3/6, 2/6, 1/6) is dominated by (3/6, 3/6, 0) via the
pair {2, 3}, so a discriminatory stable set may not exist on this grid at all; the enumeration settles it before any
cell, and if none exists the asymmetric-prior cell is run anyway and reported as a test of what the tilted seed does
in the absence of a discriminatory set. If the dollar3 machinery admits it cheaply, a second grid with an even
remainder (demands on 1/8, c = 2/8) is run for the main cell, reported as a different experiment. **Unequal pairs**
(x, 1 − x, 0) are classified as their own category, separate from discriminatory-line elements (where the excluded
player gets c > 0) and from the symmetric set; under relation (M) they are dominated (e.g. (4/6, 2/6, 0) by
(0, 3/6, 3/6) via {2, 3}), and the chain's known result that π sits on mostly unfair pairs (the accommodator
ratchet) means the ecology may well sit on dominated outcomes, which is the informative possibility.

**Cells.** mN = 0 and mN = 1 under the length prior; a uniform-over-demands seed as the control [after review: this
changes demand marginals and prior masses, not only symmetry, and is reported as such]; a **modal-arm** cell at
n = 6 on a **matched grammar and prior** (same demand marginals and class masses as the weak arm) to see whether
source reading changes the solution selected; an **asymmetric-prior** cell (one slot's seed tilted toward the fixed
small demand c = 1/6, the seed most likely to populate a discriminatory line, with no claim that it must); and
[after review] **forced seeds** at each candidate member and at selected outsiders (the fair three-way, a wasteful
outcome, an unequal pair), measuring local entry, exit and residence times, so that coverage is read against basin
volume and founder availability rather than attributed to dominance by default; [after review by gemini-4-argon] a
**constants-only arm** at mN = 0 and 1 (the pure constant-demand subgrammar), since coverage of all three pairs at
mN = 0 follows from role symmetry plus pairwise coordination alone and does not test vNM stability, and the test of
the mechanism is at mN = 1: whether dominated states are actively replaced by external-stability coalitional moves.
At mN = 1 every flip is logged by its trigger: a single-slot migration exploiting a conditional program already
present, a two-slot coincidence of migrants, or drift; a flip from a member to another member needs two slots to
change, which a single migrant cannot do on a monomorphic constant island.

**Statistics.** Per run: the set of island outcomes at the horizon; **coverage** = whether every element of the
symmetric stable set (the three pairs at 50–50) is held by some island; the fraction of islands on each stable-set
element, on discriminatory elements (a pair with the excluded player at exactly c and the pair splitting the rest),
on discriminatory-line elements and on outcomes outside every stable set; **selection** = the list of *all* stable
sets containing the run's island support [after review: subset membership need not identify a unique set], with
role-symmetry across runs reported separately from within-run symmetric selection; the time an island spends on
non-member outcomes before reaching a member (transience, censored where unresolved); under migration, the full
intermediate invasion sequence of every flip between members (members of one stable set cannot dominate each other
directly, so a flip passes through an outsider; the question is whether each step out of the outsider is an
external-stability move) and whether migration produces consensus on one member through bridges, as it did in
chicken; the myopic vs farsighted contrast (any island held on an outcome that is farsightedly but not myopically
stable, or vice versa); and the chain's rotating-pair numbers rerun on the same grammar for comparison. The cited
myopic-dynamics result (Anesi 2010) has its assumptions listed against Moran program evolution in the notes.

**Scale guard.** The grammar and tables exist; the cost is the island kernel for three slots (report its cost before
the cells). ≤ 3 workers; the fully realizable social organization run is in flight with up to 3, so use at most 3
and check its pids (`sog_full_run`) before any multi-worker step. Kill pool children by pid before any driver.

## Required outputs

`src/stable_sets.py` (+ `_run.py`, `_report.py`, importing `dollar3*`), `tests/test_stable_sets.py` (the dominance
relation on hand cases; the symmetric set's internal and external stability on the grid; a discriminatory set's
stability; the island classifier on constructed islands; the seed laws), `notes/stable-sets-on-islands.md` (§1 the
dominance relations, the stable sets found, the chicken check as a sanity case, the hand predictions for coverage
under independent islands, before any cell; §2 costs), `runs/stable-sets-on-islands.md` and `.json`, a predictions
file from the spec with the RS's claim first, committed before any counted cell, the usual hand-back (draft RESULTS,
REJECTED, THEORY §3 / DEFERRED 15 edits, NOTATION, ≤ 5 lines, branch name, commits).

## RE predictions (with falsifiers)

1. **Coverage holds at mN = 0, and is a weak test** [revised after review: with member occupancy q the independence
   baseline is 1 − 3(1 − q/3)^64 + 3(1 − 2q/3)^64 − (1 − q)^64, near certain for modest q]: every element of the
   symmetric set is held by some island in ≥ 0.9 of runs, and the informative number is member occupancy, which I
   bet is ≥ 0.6 of islands at the horizon. *Falsifier:* coverage ≤ 0.7, or members ≤ 0.4 of islands.
2. **Role symmetry across runs is robust; within-run symmetric selection is not guaranteed** [revised after review]:
   across runs each pair is the modal member on ≈ ⅓ of runs under the symmetric seeds (within 0.1), while within a
   run the island support lies inside the symmetric set alone in my bet ≥ 0.5 of runs, inside some discriminatory
   set as well in the rest; under the tilted seed the support populates a discriminatory line (the tilted slot at
   c) on ≥ 0.3 of islands. *Falsifier:* role asymmetry ≥ 0.2 across runs under a symmetric seed, or the tilted seed
   leaving the discriminatory line at ≤ 0.1 of islands.
3. **Non-member outcomes are transient:** islands reaching the fair three-way or a wasteful outcome leave it within a
   median of 200 generations (censoring reported), and ≤ 0.1 of islands sit on a non-member at the horizon.
   *Falsifier:* a non-member holding ≥ 0.25 of islands at 10,000.
4. **Flips between members pass through an outsider, and migration can still produce consensus** [revised after
   review: members of one set cannot dominate each other directly]: every member-to-member flip traverses at least
   one non-member state, ≥ 0.8 of the steps out of that state are external-stability moves under relation (M), and
   consensus on one member across every island happens in ≤ 0.3 of runs at 10,000, through bridge classes as in
   chicken where it happens. *Falsifier:* ≤ 0.5 of exit steps following the arrows, or consensus in ≥ 0.6 of runs.
5. **Source reading changes nothing here:** the modal cell's coverage, selection and transience are within 0.1 of
   the weak arm's. *Falsifier:* a difference ≥ 0.25.
6. **Myopic beats farsighted:** where the farsighted and myopic sets differ on this grid, islands sit on the myopic
   set's elements. *Falsifier:* ≥ 0.2 of islands on farsightedly stable outcomes that are not myopically stable.

7. **Gemini's counter-prediction, registered** [after review by gemini-4-argon]: at mN = 0 the strict symmetric set
   holds < 0.4 of islands, all pairs combined (unequal ones included) hold > 0.7, because fixed-role scramble
   dynamics establish greedy demands against accommodators (the chain's rotating dictatorship); and at mN = 1 one
   pair or a two-pair cycle sweeps the metapopulation by 10,000 unless the three pairs re-invade each other. The
   RE's prediction 1 and this are scored against each other: if the symmetric set holds < 0.4 and unequal pairs
   dominate, the ecology sits on dominated outcomes and the RS's claim fails in its strong form (the stable set's
   elements may still each appear somewhere, which is the weak form, scored separately).

The RS's claim is registered above; the uncertain ones are 2 (selection), 6, and the contest between 1 and 7.
