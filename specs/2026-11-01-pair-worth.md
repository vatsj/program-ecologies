# Spec: the pair-worth-a game on islands: the easy case, the middle case, the glove market and the hard case with grand bids, 2026-11-01

Status: draft by the RE; to be reviewed by gemini-4-argon (folded [after review]), then gpt-6.1-sol (`--mode amended`,
folded [after second review]); to be run by a Sonnet subagent. Queue 72. Agreed by the RS:

> RS (2026-11-01), on the easy case: "I'd like to isolate the "easy case" where the core is externally stable and thus
> the unique stable set. I'm hoping the islands will yield exactly the core in this case - every core element shows up
> (with nonzero probability) and every island ends up in the core." On the running example: "K 1/3 sgtm".
> On grand bids at a = ⅚ (the RE's proposal of arms with and without bids, drawn from the prior and written by hooks):
> "I agree to fold that into the pair-worth spec alongside the a = ⅓ cells."

The OH doc's Theory tab (sections 0–3) is the static background and the source of truth for the operating hypotheses
used here: strict coalitions-map dominance (DEFERRED 15, 2026-11-01), the object = the seed lottery with the annealed
mutation tail (OH doc h01/h03; tail-free is the reference).

## Context

**The running example.** Three players; any pair is worth a, the grand coalition 1, a singleton 0. A slot names a
partner (one of the other two, or ALL) and a demand; two slots that name each other with demands summing to at most a
form a pair (the third gets 0), three slots naming ALL with demands summing to at most 1 form the grand coalition;
otherwise everyone gets 0. Waste is lost. The core is the set of grand splits giving no player more than 1 − a; it is
nonempty iff a ≤ ⅔. Static facts (Theory tab; `src/dominance_relations.py`, `src/dominance_hard_band.py`):

- **Easy (a ≤ ½).** In the continuum the core is externally stable, hence the unique stable set (proved boundary). On
  sixths at a = ⅓ the core proper is 19 grand splits. [after second review] On a grid under strict dominance a one-step
  *ring* of splits just outside the core and some wasteful splits are also undominated, so they belong to every stable
  set of the grid: the grid's stable set is not the core. The target scored here is the RS's, the **core proper**, with
  ring and undominated waste scored separately (OH doc, Theory §0); weak dominance or a sliver currency removes them.
- **Middle (½ < a ≤ ⅔).** The core is nonempty and not externally stable; at a = ⅔ it is the single equal split.
  The **glove monopolist** (R with L1, L2; v(R, Li) = 1, v(L1, L2) = 0, v(N) = 1) is the other middle-type test: core =
  competitive equilibrium = (1, 0, 0); its stable sets are curves that bound nothing; the strict grid ring is the one-tick
  Bertrand outcome (⅚, ⅙, 0). The RS's normative claim: outcomes dominated in the coalitions-map sense are not where
  islands end.
- **Hard (a > ⅔).** The core is empty; stable sets are grid- and relation-fragile below a = 1 (a = ⅚: none on sixths
  under strict, 15 grand splits on twelfths) and hold only grand splits (a stable-set member is never strictly
  Pareto-dominated; Theory tab §3). Efficiency and blocking conflict: every grand split is blocked by a pair that
  wastes 1 − a.

**Grand bids** (the RS's proposal, Theory tab §3 anticipations). A *bid* names the grand coalition at a full split on the
condition that the other two provably do, with a fallback. The fallback is the design variable. [after second review:
explicit action equations] For slot i with others j < k (slot indices), □ = PA provability on the encounter's GL chain
(`modal.py`), π(σ; i, j) = the *exclusion split* of the pair {i, j}: its worth split as equally as the grid allows, the
odd tick to the larger share in σ (no tie arises in the games below: every pair worth is an even number of ticks)
[after review: proportional rounding left a bidder at 0 on sixths]; in the glove market the R–L pair is split in
proportion to the two shares in σ, rounded down, the remainder to the larger share, and the L1–L2 pair (worth 0) at
(0, 0), which still excludes R. Programs are the conditionals below, read top to bottom; play is the modal fixed point:

- *exclusion bid* B(σ; c):
  `if □(j = (ALL, σ_j)) ∧ □(k = (ALL, σ_k)) then (ALL, σ_i)`
  `elif □(j = (i, π_j(σ; i, j))) then (j, π_i(σ; i, j))`
  `elif □(k = (i, π_k(σ; i, k))) then (k, π_i(σ; i, k))`
  `else c`.
  The second and third lines are Löbian pair handshakes: two bids facing a non-bidder pair with each other. With c equal
  to the slot's current action on an island (and c not itself the handshake's pair action), a bid is on-path identical
  to c and enters neutrally.
- *accept-pair bid* A(σ; c): the first line of B, then for each other slot in order j, k and each demand d of the
  partner on the grid (ascending): `elif □(partner = (i, d)) then (partner, worth − d)` when worth − d ≥ 0, then
  `else c`. It accepts any pair offer. In `dollar3` hand-built grand handshakes of this kind leaked faster than the
  constant grand coalition (RESULTS "Three-player majority divide-the-dollar": 0.7–1.1·10⁻⁴ against 2.7·10⁻⁶).
- *blocker* K(σ; c): `if □(j = (i, π_j(σ; i, j))) then (j, π_i(σ; i, j))`, `elif □(k = (i, π_k(σ; i, k))) then (k, …)`,
  `else B(σ; c)`. It tries the pair handshake first. Against bids its handshake fails only if the bid's own handshake
  line is not reached; whether K is on-path identical to B on a homogeneous bid island is a modal fixed-point question
  the engineer settles by evaluation (V4), and the spec's neutrality claim for K is conditional on it. Two blockers in
  different slots pair and gain π_i − σ_i each (1/12 at a = ⅚, equal split). The predicted exit from a grand-split
  island in the hard band.
- *grand constants* G(σ): the three constants (ALL, σ_i) as a non-reading coordination control at the same dose as B.

**Correction to the RE's reading in the doc** (to be made there with this spec's commit): the doc said that for a > ⅔
"the way in is uphill" because a pair member who switches to bidding gives up a/2 for ⅓. With a neutral fallback that
is wrong: on a pair island bids enter both pair slots neutrally; a bid in the excluded slot is then selected (+⅓ against
0 whenever it meets bids in both other slots), and once bids hold the excluded slot, the exclusion fallback makes
bidding selected in every slot (a non-bidding pair member meeting two bidders is excluded). So the way in is
drift-then-selection, like the way out through blockers (neutral blocker, then a selected second blocker, +(a/2 − ⅓)).
In the hard band the RE now expects grand ↔ pair *cycling*, with occupancy set by the neutral-entry masses of bids and
blockers; in the easy case blockers gain nothing (a pair pays at most a < ⅔ in total) and grand-split islands reached
by bids should be long-lived [after second review: not absorbing; the matching constant (ALL, σ_i) is on-path identical
to a bid and can drift in, after which coordination is fragile; escape hazards are measured directly].

**The core-only bid menu is a confound** [after second review]. Seeding bids only on core splits would make core
selection a property of the menu. On G⅓ the primary bid arm therefore bids on every grand split (B\*); the core-only
menu (B) is the contrast.

**Why it matters for the long-term goal.** The easy case is the cleanest test of whether the ecology selects a
solution concept at all: one stable set, the core, dominance-closed, no knife-edge symmetry. If islands do not land in
the core there, the stable-set targets elsewhere are not dynamic predictions. Bids are the source-reading lever: they
need a reader that resolves a three-way mutual condition, which Löb (the modal arm) and checked certificates (arm T)
supply and simulation does not.

REJECTED.md checked. Nearest entries: "Grand coalition entry is three neutral steps" and "The grand start decays into
pairs within 10⁴ generations" (`dollar3`, a = 1; entry ran through "join iff j joins" readers plus a strict step,
which is consistent with this spec's bid mechanism); "Myopic beats farsighted" and RE 1–4 of "Stable sets on islands"
(a = 1). Nothing is re-opened: this game varies a, which `dollar3` fixes at 1.

## The object

- **Islands.** The seed lottery of `src/churn_primary.py` / `src/migration_window_kernels.kern_mw` (three slot
  populations per island, mean-field expected payoffs, Moran birth-death with fitness exp(w·payoff), w = 0.3 per unit
  dollar as in `dollar3` (payoffs in dollars), migration m = mN/N per birth from a uniformly random other island,
  not payoff-weighted). N = 100 per slot, I = 64, one component. Founders drawn from the arm's seed law per slot.
- **Tail (main).** The annealed schedule of RESULTS "Annealed mutation" adapted to this kernel: prior arrivals per
  island per generation ε(t) = (Λ/t₀)(1 + (t − 200)/t₀)^(−2) from generation 200, t₀ = N/2 = 50, cut at generation
  10,000, then a 2,000-generation tail-free chase; each arrival replaces a uniformly random individual of a uniformly
  random slot with a program drawn from that slot's seed law. Λ = total arrivals per island: main Λ = 10, secondary
  Λ ∈ {1, 100}. **If queue 71 (annealed tail, mean field) reports Λ\* before launch, set the main Λ to 3·Λ\* (M natural,
  t₀ = 10²) and say so.** Reference: tail-free (Λ = 0), same founders.
- **Horizon.** 12,000 generations (10,000 + chase); runs not resolved at 12,000 are reported as censored, with the
  class occupancy over the last 2,000 generations.
- **Migration.** main mN = 1; secondary mN = 0 and 0.1.
- **Runs.** 20 per cell, founders paired across arms that share a base law, across tails, and across mN.

## Games and grids

| id | game | grid of demands | actions per slot |
|---|---|---|---|
| G⅓ | pair worth ⅓ | sixths, demands 0–6 | 21 |
| G⅔ | pair worth ⅔ | sixths | 21 |
| Ggl | glove monopolist (slot 0 = R) | sixths | 21 |
| G⅚ | pair worth ⅚ | twelfths, demands 0–12 [twelfths so that a/2 = 5/12 is on the grid] | 39 |
| G⅔′, Ggl′ | transfer cells | 24ths, demands 0–24 | 75 |

The grand coalition forms at any split summing to at most 1. The payoff table per game is built once (a joint table
over actions); every arm's joint table over programs is built from it.

## Arms

- **C (constants).** Seed law uniform over the slot's actions (the length prior on constants).
- **R (readers, secondary).** The `dollar3` modalPA grammar generalized to the game's actions, n ≤ 6 (one-atom
  conditionals `if(BOX(THEM_j = a), x, y)`), length prior, merged to canonical functions. Only on G⅓ and G⅚.
- **C+B (bids).** C plus the named bid family at dose δ (total seed mass per slot): exclusion bids B(σ; c) for σ in
  the game's bid set and every constant c, uniform within the family. Bid sets: G⅓ the 19 core splits (the core-only
  menu B, the contrast); G⅔ the 10 splits with every share ≥ ⅙; Ggl the 10 splits with R's share ≥ ½; G⅚ [after review: only] the equal split (4, 4, 4)/12, so that a blocker gains 1/12 in every slot (at (5, 4, 3)/12 the
  5/12 slot would gain nothing by blocking); transfer cells the same splits as their sixths cells. **Per-split dose**
  [after review]: δ is spread over 19 splits on G⅓ and 1 on G⅚, a 19× difference per split; the secondary cell G⅓
  C+B= seeds the equal split only, matching G⅚'s per-split dose. Doses: main δ = 0.05, secondary 0.01 and
  0.15.
- **C+B\* (bids on every split; primary on G⅓)** [after second review]. As C+B with σ ranging over all 28 grand
  splits on sixths, so that core selection cannot come from the menu.
- **C+B₂ (equal-mass control)** [after second review]. C+B at δ = 0.10, matching C+B+K's total named mass. G⅚.
- **C+G (non-reading coordination control)** [after second review]. C plus the grand constants (ALL, σ_i) for the
  same σ set as the bids, at dose δ. G⅓ (all 28 splits) and G⅚. Tests whether bids work by reading or by supplying
  coordination devices.
- **C+B+K (bids and blockers).** As C+B plus blockers K(σ; c) at the same dose as the bids (matched). Main on G⅚;
  secondary elsewhere.
- **C+A (accept-pair bids, control).** C plus accept-pair bids A(σ; c) at dose δ. G⅚ and G⅓ only.
- **R+B.** R plus the bid family at δ = 0.05. G⅓ and G⅚ (secondary).
- Evaluation of named programs: modal semantics (PA provability on the encounter's GL chain, `modal.py` /
  `dollar3.py` conventions) for every arm with conditionals; the bid conditions are conjunctions of two atoms,
  resolved jointly as in the `dollar3` grand handshakes. Compute the family's length-prior mass under R's grammar
  (static number; the RE expects it to be far below δ, which is why the family is seeded rather than drawn).

**Stage 2 (gated; not part of this run unless the gate fires).** Gate: in G⅚ or G⅓, C+B core/grand occupancy exceeds
C's by ≥ 0.2 at mN = 1, Λ main, while the share of islands that ever hold a bid in all three slots is ≤ 0.3 (bids work
once present, supply is the bind). Then: (i) **arm T bids** with three-party checked certificates (the `L_T` milestone 4
checker and the three-player closure of RESULTS "The social organization game over the realizable language"; capped
simulation cannot read a mutual bid, so arm T's `churn_primary_t` frame is not usable); (ii) **hook-written bids**: a
`HOOK(t, c)` node whose fill (t, open key "both others provably bid σ", action (ALL, σ_me)) is written as "thanks" by a
slot that ends an encounter in the grand coalition at σ, inherited by offspring. Stage 2 gets its own spec and reviews.

## Design

1. **Static numbers (before any counted cell).** For each game and grid: the outcome set; the core proper; the strict
   undominated set and its decomposition (core proper, ring = undominated grand splits outside the core, undominated
   wasteful splits); weak undominated; stable sets under strict and weak (`src/dominance_hard_band.kernels`, report
   none where none); the length-prior mass of B, A and K under R; for the transfer cells the same with 24ths, checking
   the Theory tab's claim (strict undominated = core proper at a = ⅔ and in the glove market).
2. **Validation.** (V1) The generalized game at a = 1 on sixths restricted to `dollar3`'s 9 actions per slot reproduces
   `dollar3`'s payoff table exactly. (V2) The kernel with Λ = 0 reproduces a stored `churn_primary` baseline cell
   (constants, mN = 1) to its reported precision. (V3) The tail: on one cell, the realized number of arrivals per island
   against Λ (within 3 standard errors), and the arrival law against the seed law (χ² per slot). (V4) Bid semantics: on
   hand-built triples, B(σ; c)³ plays σ; B with one constant partner pairs the two bidders; K² with B in the third slot
   pairs the blockers; A accepts a pair offer; [after second review] K³, mixed-σ bid triples, incompatible bids, and
   constants that mimic a bid's output, each with the play the equations imply stated before evaluation. (V5) Modal evaluation of every named program against every constant and
   named program agrees with a direct GL-chain evaluation on a random 1,000 triples.
2b. **Invasion assays** [after second review]. Single islands (no migration, no tail), 2,000 replicates each, N = 100:
   (i) a pure pair island (the modal pair of G⅓ C and of G⅚ C) with one B(σ; c) introduced in a pair slot, c the
   slot's action: fixation probability against 1/N; then with B fixed in both pair slots, one B in the excluded slot;
   (ii) a homogeneous B³ grand island (G⅓ equal split, G⅚ equal split) with one matching grand constant, one blocker
   (G⅚), one accept-pair bid: fixation probabilities and, from 200 replicate homogeneous grand islands under the tail
   at Λ main, the escape hazard per generation; (iii) the same with K² fixed in two slots and B in the third. These
   measure neutrality and establishment directly rather than inferring them from island counts.
3. **Main cells (counted).** mN = 1, Λ main and Λ = 0:
   - G⅓: C, C+B\* (primary), C+B, C+G, C+A;
   - G⅔: C, C+B;
   - Ggl: C, C+B;
   - G⅚: C, C+B, C+B₂, C+B+K, C+G, C+A.
4. **Secondary cells.** mN ∈ {0, 0.1} for every main cell's C and C+B; doses 0.01 and 0.15 for C+B on G⅓ and G⅚; R and
   R+B on G⅓ and G⅚ at mN = 1; Λ ∈ {1, 100} for C and C+B on G⅓ and G⅚; G⅓ C+B= at mN ∈ {0, 1}; transfer cells G⅔′ and Ggl′ with C and C+B at
   mN = 1, both tails; N = 200 for C+B and C+B+K on G⅚; **easy case at larger N** [after second review]: G⅓ C and C+B\*
   at N = 200 and 400, horizon and tail scaled with N (t₀ = N/2, horizon 100·N generations plus a chase of 20·N, Λ
   unchanged), at mN = 1 (otherwise conclusions are labelled finite-N).
5. **Statistics per island**, from the modal outcome (the play of the island's majority triple, as in
   `stable_sets.py`), and [after second review] also the exact encounter-weighted outcome distribution (expected
   over the three slot compositions), the majority program's share per slot and the share of mixed-state time:
   - class at the end and occupancy over the last 2,000 generations: core proper / ring / other efficient grand
     (dominated) / undominated wasteful / dominated wasteful pair / disagreement; for G⅚: grand split / pair /
     disagreement, and membership of each stable set of that grid under each relation;
   - core coverage: how many core points are observed on any island at the end, pooled over runs, with frequencies,
     reported separately at mN = 0 and mN = 1 and stratified by minimum share (G⅓ has 10 core points with every share
     positive and 9 with a zero share, (4, 2, 0) and (3, 3, 0) and permutations; a zero-share bidder gains nothing over
     exclusion) [after review]; at mN = 1 also the number of runs reaching consensus on one split;
   - G⅚ and every cell with bids: grand ↔ pair switches per island per 10⁴ generations (debounced 25 generations),
     reported separately during the tail (generations 200–10,000) and the tail-free chase, and at mN = 0 against
     mN = 1 (local invasion against migration-driven turnover) [after second review],
     the share of islands that ever hold a bid in all three slots, and the transition structure (which program
     family is present at each switch: bid, blocker, constant) (discipline 4);
   - efficiency (share of the dollar paid out), mean payoff per slot; glove: R's mean share;
   - with the tail: the arrivals that fixed (≥ 10% of a slot) by family, and the arrivals that preceded a class change
     within 100 generations.
6. **Cut order** (cut from the end if the budget binds; report every cut): N = 400 of the easy case; N = 200 of G⅚;
   R and R+B; Λ ∈ {1, 100}; doses
   0.01 / 0.15; mN = 0.1; transfer cells; C+A on G⅓; G⅓ C+B=. Validation, static numbers, the invasion assays and
   the main cells are never cut. (V6) [after second review] Slot-permutation invariance: relabelling slots permutes
   every joint-table entry and every class share accordingly (0 mismatches on 10⁴ random triples per game; the glove
   only under permutations of L1, L2).

**Budget.** 3 workers. Pilot one C and one C+B run of G⅚ (the largest table) and report the per-run time before
launching; if the main cells exceed 24 hours at 3 workers, cut secondaries in the cut order before reducing runs.

## Required outputs

- `runs/pair-worth.md` and `.json`; rows under `runs/pair_worth/`; `notes/pair-worth.md` (engineer's notes, every
  deviation disclosed in the report too); `predictions/2026-11-01-pair-worth.md` from this spec with the static
  numbers, committed before any counted cell.
- Tables: static decomposition per game; end class shares and last-2,000 occupancy per cell with intervals over runs;
  core coverage (G⅓, G⅔, Ggl); switch rates and transition structure (G⅚); the tail's fixed arrivals by family.
- Drafts for RESULTS, REJECTED (every failed prediction, the RE's, the RS's and the engineer's), THEORY if a claim
  moves, NOTATION (B, A, K, δ, G⅓ … and the class names).

## Predictions, with falsifiers

**The RS's conjecture (the easy case), scored as stated.** In G⅓ every island ends in the core proper and every core
point appears with positive probability. Operationalized [after second review: a preregistered primary arm and a
minimum probability instead of positivity] in **C+B\***, Λ main: core proper ≥ 0.95 of islands at the end at mN = 1;
and at mN = 0 every core point has island frequency ≥ 1/76 (a quarter of uniform over 19), judged by run-clustered
simultaneous 95% intervals: the conjecture fails on a point whose upper bound is below 1/76. Coverage at mN = 1 is
reported, not scored (runs may reach consensus). Other arms are reported against the same criteria. *Falsifier:*
either clause fails in C+B\*.

**RE.**

1. **Constants do not reach the core from pairs.** G⅓, C: core proper < 0.8 at mN = 1 under both tails; pair and
   disagreement islands hold the rest (a pair member's switch to ALL costs its pair share and no single step is neutral
   into the grand coalition). *Falsifier:* core proper ≥ 0.8 in C.
2. **Bids carry the easy case, and dominance, not the menu, puts them in the core.** G⅓, C+B\* (δ = 0.05): core proper
   ≥ 0.8 at mN = 1, Λ main, at least 0.2 above C on paired founders, with dominated grand splits (outside core and
   ring) ≤ 0.05 (blocked non-core bids are left by a neutral step then a selected one); C+B (core-only menu) core
   proper ≥ 0.9. C+G (grand constants, no reading) at least 0.15 below C+B\* (bids work by reading, not by supplying
   coordination devices). *Falsifier:* any bound violated.
3. **The tail matters only with a neutral path.** G⅓: Λ main raises core proper over Λ = 0 by ≥ 0.05 in C+B and by
   < 0.05 in C. *Falsifier:* either inequality reversed.
4. **The ring is a grid effect that bids do not remove.** G⅓, C+B: ring islands ≤ 0.05; in C ring islands ≥ 0.02.
   Transfers (G⅔′, Ggl′ against G⅔, Ggl, arm C only [after review: C+B's bids sit on sixths splits and leave the
   24ths ring unseeded]): the share of non-core undominated islands (ring plus undominated wasteful) falls by ≥ 0.05. *Falsifier:* C has no ring islands (< 0.02), or the transfer cells do not lower it.
5. **The middle case keeps the coalitions-map claim only near the core.** G⅔, C+B: core proper (the equal split) plus
   ring ≥ 0.7 of islands; core proper alone ≥ 0.3. Glove, C and C+B: R's mean share ≥ ⅚ and islands on (1, 0, 0) or
   (⅚, ⅙, 0) ≥ 0.7 (Bertrand by neutral L moves and selected R switches), with (1, 0, 0) alone in [0.3, 0.8] (L
   players are indifferent at 0, so their drift keeps knocking R off the core). *Falsifier:* any bound violated.
6. **Hard case without bids: wasteful pairs.** G⅚, C: pair islands ≥ 0.7 at the end (mN = 1, both tails).
   *Falsifier:* pair islands < 0.7.
7. **Hard case with bids, no blockers: grand splits.** G⅚, C+B: grand-split islands ≥ 0.6 and at least 0.3 above C.
   *Falsifier:* either bound violated.
8. **Hard case with blockers: two-way switching while the tail supplies both families.** G⅚, C+B+K: grand occupancy
   over generations 200–10,000 in [0.15, 0.85] and at least 1 grand ↔ pair switch per island per 10⁴ generations
   during the tail, at mN = 0 as well as mN = 1, with both directions preceded by the named neutral-then-selected
   structure (bid or blocker present in two slots before the switch) in ≥ 0.6 of switches; in the tail-free chase the
   switch rate falls (the RE does not claim recurrent cycling without supply) [after second review]. *Falsifier:*
   occupancy outside the band, or fewer switches during the tail, or the structure in < 0.6. C+B₂ (equal mass, no
   blockers) has grand occupancy at least 0.2 above C+B+K, so the drop is the blockers', not dilution.
11. **Invasion assays.** (i) A bid in a pair slot fixes at 1/N within 2 standard errors (neutral); with bids in both
    pair slots, a bid in the excluded slot fixes at ≥ 3/N (selected). (ii) On a B³ grand island at G⅚ a blocker fixes
    at 1/N within 2 standard errors and, with K² in two slots, the third bid is lost; a matching grand constant fixes
    at 1/N (neutral). *Falsifier:* any of these off by more than the stated margin.
9. **Accept-pair bids do not help.** G⅚ and G⅓, C+A: grand / core share within 0.05 of C. *Falsifier:* C+A exceeds C
   by more than 0.05.
10. **Readers alone are not bids.** G⅓ and G⅚, R (n ≤ 6): within 0.1 of C on core / grand share (one-atom conditionals
    cannot express a two-sided bid). *Falsifier:* R exceeds C by more than 0.1.

**Reviewer counter-predictions, recorded and scored.** gpt-6.1-sol: grand states are long-lived rather than absorbing
(scored by the escape hazards of 2b), and G⅚ switching depends strongly on residual family supply, with genuine
recurrent cycling unestablished (scored by the chase switch rate against the tail's). gemini-4-argon: G⅓ C+B: core proper ≥ 0.9, but pooled coverage
at mN = 1 ≤ 15/19, the zero-share points missing, while mN = 0 shows all 19.

The RS is invited to add predictions, in particular on G⅚ (whether bids win against blockers) and on the glove market.

## Notes for the engineer

- Reuse `stable_sets.py` (game tables, classification), `migration_window_kernels.kern_mw` and `churn_primary.py`
  (catalogue, joint table, founders, summaries); add the tail as a new kernel variant, leaving the stored kernels
  unedited. The PD tail implementation (`src/annealed_kern.py`) shows the per-generation exact integration of ε(t).
- Catalogue sizes [after second review: recomputed]: G⅚ C+B+K has 39 + 39 + 39 = 117 programs per slot (one σ), a
  joint table of 1.6·10⁶ triples; G⅓ C+B\* has 21 + 28·21 = 609 (2.3·10⁸ triples) and G⅔ / Ggl C+B 21 + 210 = 231
  (1.2·10⁷); the transfer cells C+B 75 + 10·75 = 825. Where the full table is too large, evaluate the named families by
  a closed-form outcome rule over (σ, c, family) inside the kernel, or a table over behaviour classes; V5 validates the
  rule against modal evaluation on random triples including mixed σ, K³, incompatible bids and constants that mimic
  bid outputs.
- Use `dollar3.py`'s action encoding generalized: local action = (partner index ∈ {two others, ALL}, demand index).
- Payoffs in dollars; w = 0.3; check the sign and scale against `dollar3` in V1.
- Workers ≤ 3, BLAS threads 1. Do not read or source `.env`. No `.npz` / `.pkl` / large `.npy` committed.
- Commit `predictions/` before any counted cell; commit the notes' design section before code.
