# Spec: chicken and hawk–dove with fixed roles and without `ROLE`: do islands learn one-sided norms?, 2026-10-11

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol; to be run by an Opus subagent. Requested by the RS
(2026-10-11, DEFERRED 12): "straight in chicken is credible"; he predicts that with fixed roles some islands learn
norms where one role wins the straight play and the other is forced to swerve. One-population chicken without `ROLE`
is already run (RESULTS, the early tables: a conditional polymorphism with loss 0.74); with `ROLE` the ecology sits on
the sum-maximizing correlated outcome. Fixed roles have not been run in chicken.

## The RS's prediction (verbatim, registered)

> I'll predict (for chicken) that some islands will learn norms where one side "wins" the straight play and the
> other role is forced to swerve.

## Why

Chicken is the anti-coordination game whose pure equilibria are one-sided: (straight, swerve) and (swerve,
straight). With fixed roles each is a strict Nash equilibrium of the two-population game, so the ε→0 chain should
put π on the two conventions and the ε = 0 lottery should pick one per island; the questions are which, with what
share, whether source reading changes anything (a reader that plays straight iff the opponent would swerve is a
conditional straight; a committed constant straight is the Schelling commitment), whether islands disagree (a
patchwork of norms, which is the RS's picture), and whether migration between islands with opposite norms merges them
(a role-1-wins island and a role-2-wins island are rival conventions; the bridge question of RESULTS "Rival
networks"). Hawk–dove is the same game under the biological parametrization (resource V, fight cost C > V, so
mutual hawk is the worst outcome); chicken's crash payoff plays the same role; both run so the answer is not
parametrization-specific.

## Design

**Games.** Chicken with the repo's payoffs (`src/regret.py`'s `chicken` table); hawk–dove with V = 2, C = 3
(H–H = −1/2, H–D = 2, D–H = 0, D–D = 1), and a second hawk–dove with C = 6 (H–H = −2) as the "crash is terrible"
variant. Actions: straight/hawk, swerve/dove.

**Arms.** (a) Fixed roles, two populations (role 1 and role 2), weak arm at n = 6 (the standing DSL with `THEM`,
`ME`, constants; no `ROLE` atom, since the role is the population); (b) fixed roles, modal arm at n = 6 (sound box
atoms), to see whether provable commitment changes the norm; (c) one population without `ROLE` under the modal arm
(the weak-arm result exists); each at the three payoff tables.

**Static.** Class catalogues per role; the play tables; the two pure conventions and their basins; conditional
straights (`not(THEM(THEM))`-type readers) and what they do against a constant straight; the self-play of readers in
each role. [after review] **Program-space closure, not action-space:** a strict action equilibrium is not a strict
program equilibrium, since readers can match a constant's on-path action and enter neutrally, then change the other
role's incentives; the notes derive the invasion and drift closure of each convention *in program space*, retaining
distinct sources and neutral twins, using the audited closure-seeded log-domain solver (`src/chain_log.py`,
IMPLEMENTATION 4) with candidate traps verified without threshold pruning (the cut diagnostic). **Full bridge
tables:** before any bridge is named, the bridge–resident and bridge–bridge tables in both roles, including the
self-play of identical deterministic readers in opposite roles (which cannot anti-coordinate without a public
asymmetric signal; here the role *is* that signal, so the question is whether the grammar lets a reader condition on
it, which in the two-population game it does only through the population it sits in). **Outcome classification by
play, not genotype:** an island's outcome is classified by its role-conditioned action probabilities and payoffs
(convention tolerance: ≥ 0.95 of encounters at (straight, swerve) or (swerve, straight)), separately from its genotype
diversity, so that a polymorphic population implementing a perfect one-sided norm counts as that norm and two
monomorphic readers that crash count as crash. Mutual-dove is reported separately (in both hawk–dove tables it is
Pareto-efficient with the same total payoff as either pure convention; convention frequency is not an efficiency
statistic). The fitness map with negative payoffs is the repo's exponential map, stated.

**Chain** (ε→0, two-population Moran as in RESULTS "Three-player majority divide-the-dollar" with k = 2; N per
population ∈ {10², 10³, 10⁴}): π over outcome classes (role-1-wins, role-2-wins, crash, mutual swerve, polymorphic),
support, transition structure, the exit of each convention with its N-scaling, the decisive edges' Δ and N·Δ.

**Lottery** (ε = 0, primary). [after review] **Law, frozen in notes §1:** islands of two populations, N = 100 per
role (and a small-N panel N ∈ {25, 50}), I = 64; seeds iid from each role's class prior (the length prior, with class
masses stated), sampled with replacement, roles independent; Moran updating per role with the repo's exponential
fitness map; migration on the complete island graph at mN ∈ {0, 1}, role-preserving (a role-1 migrant replaces a
random role-1 resident), emigrants unweighted (the standing rule; payoff-weighted emigration is the island-selection
arm and is not used here); a generation = N birth–death events per role; horizon 2,000 with a doubled horizon 4,000
on every mN = 1 cell; endpoint E3 of milestone 2 adapted to outcome classes by play; runs not resolved by the horizon
are censored with resolution times reported; 40 runs per cell, run-level uncertainty. Report per run the fraction of
islands at each convention, mutual-dove and crash, the fraction of runs with islands at both conventions at the
horizon (a patchwork), **per-island establishment probabilities** (the RS's qualitative claim is scored on these: an
island learning a one-sided norm), whether patchworks resolve under migration and through which classes, the
establishment generation, and the crash rate on and between islands; cross-island expected loss, role-preserving
(role-1 holders of island A against role-2 holders of island B), against the benchmark of the one-sided conventions'
payoff, as the universality statistic. [after review] **Controls:** a constants-only two-population control (does
ordinary anti-coordination already produce the norms?); a matched grammar/prior control between the weak and modal
arms on paired seeds; forced opposite-convention islands with candidate bridges included versus removed at matched
founder mass; role-swapped runs (the payoff tables transposed) to detect implementation asymmetry.

**Scale guard.** The n = 6 catalogues are small (≤ 150 classes per role in the weak arm); report class counts and
chain sizes before the lottery. ≤ 3 workers; kill pool children by pid before any driver. [after review] The chain
(rare mutation) and the lottery (mutation-free absorption) are reported as separate objects, never pooled; the
lottery panel is finite-size evidence and is labelled so.

## Required outputs

`src/fixed_role_chicken.py` (+ `_run.py`, `_report.py`), `tests/test_fixed_role_chicken.py` (the three payoff
tables; the role catalogues; the two conventions strict in every table; the lottery seed law),
`notes/fixed-role-chicken.md` (§1 the conventions, the conditional straights and the hand-derived basins and
bridges, before any cell; §2 costs), `runs/fixed-role-chicken.md` and `.json`, a predictions file from the spec with
the RS's prediction verbatim first, committed before any counted cell, the usual hand-back (draft RESULTS, REJECTED,
THEORY §3 / DEFERRED 6 and 12 edits, NOTATION, ≤ 5 lines, branch name, commits).

## RE predictions (with falsifiers)

[after review: the RS's qualitative claim is scored on per-island establishment of a one-sided norm by play; my
numbers are bets on top of it, and success and falsifier ranges meet.]

1. **The RS's prediction holds in the lottery at mN = 0:** in every game and arm the per-island probability of
   ending at a one-sided convention (by play) is ≥ 0.6 (my bet ≥ 0.9), the role-1/role-2 split is within [0.25, 0.75],
   and the constants-only control already produces the norms (ordinary anti-coordination), with source reading
   changing the per-island probability by ≤ 0.1. *Falsifier:* per-island probability < 0.6, or a split outside
   [0.25, 0.75]; a reading effect ≥ 0.25 is a miss of the control clause. (Both conventions appearing somewhere among
   64 islands is near-automatic and is not scored.)
2. **Migration does not simply merge the norms** [revised after review]: at mN = 1 the two conventions are rival
   networks; identical readers in opposite roles anti-coordinate only through the role signal, so candidate bridges
   are role-specific; my bet is that ≥ 0.4 of runs are still patchworks at 4,000 generations, and that resolutions
   that do occur run through demographic takeover by the majority convention (migration-driven), not through reader
   mediation; the forced-island control with bridges removed changes the resolution rate by ≤ 0.1. *Falsifier:*
   ≤ 0.1 of runs patchworks at 4,000, or the bridges-removed control cutting resolutions by ≥ 0.4.
3. **Neutral neighbourhoods, exits by the full escape path** [revised after review]: π splits between the two
   conventions; each convention has a neutral neighbourhood (readers matching the on-path action) and its exit
   scaling is set by the complete escape path, which I bet is neutral entry then a strict switch (∝ 1/N) in chicken
   and may pass through a polymorphic trap in hawk–dove; no genuine limit cycle; crash states ≤ 0.05 of π.
   *Falsifier:* a cycle, a crash state ≥ 0.2, or an exit that is N-independent.
4. **Provable commitment does not change the norm:** on the matched grammar/prior control with paired seeds the
   modal arm's per-island convention probabilities are within 0.1 of the weak arm's. *Falsifier:* a difference
   ≥ 0.25.
5. **The crash parametrization lowers crash exposure, not convention frequency** [revised after review]: the C = 6
   hawk–dove has per-island convention probabilities within 0.1 of chicken's and a lower on-island crash rate; no
   claim on exit speed. *Falsifier:* a convention-probability difference ≥ 0.25, or a higher crash rate at C = 6.

The RS's prediction is registered above; the uncertain ones are 2 (whether anything bridges the two norms) and 4.
