# Spec: divide-the-dollar partitions across islands, with `ROLE` and with fixed roles, 2026-10-05

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-05-dollar-partitions-gpt-6.1-sol.md`) and revised; changes marked
[after review]. To be run by an Opus subagent. Queue item 6
(CLAUDE.md), the RS's request of 2026-10-02: "I'm curious what set of partitions we see amongst islands in the weakly
extensional regime for divide-the-dollar. I see no reason why 50–50 would be preferred." Partial code exists:
`games/dollar3.yaml`, `games/dollar5.yaml`, `src/dollar.py` (evaluation, classes, partition statistics),
`src/dollar_static.py` (basins, conventions, pairwise contests), carried over unrun from a paused worktree.

## Why

Distribution is an evaluation, not a selector (CLAUDE.md 3), and the program's normative target for it is an open
DEFERRED item (6): Θ(1/n) fair partition as a stochastically stable *state*, with anonymity deliberately violable by
slot asymmetry. The fixed-role results so far select the asymmetric split: the ultimatum game selects the
subgame-perfect split, and three-player majority divide-the-dollar selects rotating, mostly unfair pairs with
E[max share] 0.60, because the selected outcome is the one whose deviations are generous rather than self-punishing
(RESULTS "Three-player majority divide-the-dollar"; THEORY §9.11). The two-player Nash demand game is the cleanest
distribution question: every efficient split (d, 1 − d) is a strict equilibrium, nothing in the payoffs prefers
50–50, and the literature does prefer it: under adaptive play with uniform mistakes the stochastically stable
convention is the Nash bargaining solution (Young 1993, "An evolutionary model of bargaining"; Binmore, Samuelson and
Young 2003), 50–50 for symmetric players. Our dynamics differ (Moran fixation with a length prior over source-reading
programs; islands with iid seeds and no mutation), so the question is open here, and the RS expects no preference.

Two features of our setting give concrete reasons either way, and the experiment is designed to tell them apart:
- *With `ROLE`* (one population, the environment's correlating signal), the 1-node program `ROLE` *is* the most
  unequal correlated split, (5/6, 1/6) in `dollar5`, at the same prior mass as the 1-node constant `S3` (1/2). Each
  earns 1/2 against itself. Between them the mismatch payoffs make a coordination game between conventions whose
  interior crossing is at a `ROLE`-frequency of 5/8 (S3 earns 1/2 − x/4, ROLE earns 1/12 + 5x/12), so 50–50 is
  risk-dominant with the larger basin, and the standard stochastic-stability argument favours it in the mutation
  object. In the seed lottery, which convention wins an island is decided in the scramble, where the constants S1–S5
  and ROLE all have equal 1-node mass and the conditionals are a third of μ.
- *With fixed roles* (two slot populations, no `ROLE`; DEFERRED 3's operating hypothesis for social-choice questions),
  every efficient split is strict for both slots and moves run through neutral drift of the side that will lose into
  a *conceder* (on-path identical to its constant, conceding to the other side's new demand), followed by the other
  side's strict move: the three-player mechanism. The number of such exits from a split is the number of neighbouring
  splits, so the extremes have fewer exits than the middle. That predicts mass at the extremes, against Young.

## Design

**Games.** `dollar5` (demands 1/6 … 5/6; efficient splits 1/6–5/6, 1/3–2/3, 1/2–1/2; incompatible pairs pay 0;
compatible-inefficient pairs pay their demands) as the main game; `dollar3` (1/3, 1/2, 2/3) as the control with no
intermediate inequality. Level order is ascending demand, so `ROLE` plays (S1 | S5) and `flip` maps d → 1 − d.

**Arms** [after review: the role comparison must not change several things at once]. The *weak* arm (the RS's
"weakly extensional regime": simulation-based reading, `THEM(^A)` probes, `X`), at one matched cutoff n for every
arm (n = 6 for `dollar5` if the class count allows the chain; report it; fall back to n = 5 everywhere and say so),
in three role structures: (i) **one population with `ROLE`**; (ii) **one population without `ROLE`** (symmetric, no
signal; the `--norole` grammar); (iii) **two fixed slot populations without `ROLE`** (as in `src/dollar3*.py` for
three slots: each slot its own population; a match draws one program from each). (ii) separates the signal from
the population structure. Constants-only baselines for all three. Report the induced prior over behavioural classes
(constants, `ROLE`-splits, readers, shadows) in every arm.

**The fixed-role chain** [after review: specified before it runs]. States are *joint* resident configurations
(one class per slot); a mutation event picks a slot uniformly, draws a mutant from that slot's μ, and the mutant
fixes or dies in that slot by the Moran fixation probability with fitness exp(w · mean payoff against the other
slot's resident) at per-slot size N; the other slot is held fixed during the fixation. This is the sequential-fixation
reduction already used for three slots (RESULTS "Three-player majority divide-the-dollar"); validate it here against
a small joint-population simulation (two slots of N = 50, ε = 10⁻³, 10 seeds) by comparing π over partitions, and
report any persistent polymorphism, which would invalidate the monomorphic reduction. Say whether N is per slot
(it is) in every table.

**Objects.**
1. *Mutation object:* the ε→0 chain (`src/chain.py` through `run.py` / `limN.py` conventions) at N = 10², 10³, 10⁴,
   w = 0.3: π by partition (each efficient split, compatible-inefficient, clash), support (which programs: constants,
   `ROLE`-splits such as `ROLE`, `flip(ROLE)`, readers), transition structure between conventions (the exits of each
   split, and whether moves run through conceders as in the three-player game), E[max share], deadweight loss, and
   P(efficient). Report the pairwise contest table of conventions (mismatch payoffs, crossing frequencies, Moran
   fixation of one mutant) from `src/dollar_static.py` first, before any chain run. [after review] For every
   efficient split, tabulate its *adjacent* moves under the actual grammar (direct constant-to-constant transitions
   and conceder paths alike) with prior-weighted entry and exit rates, so π can be read against the rates rather than
   against an exit count; compare the measured π over splits with the uniform-over-ordered-splits benchmark (in
   `dollar5` five ordered efficient splits, four of them unequal, so "unequal ≥ 0.5 of π" is not evidence of an
   inequality preference).
2. *Seed lottery:* ε = 0, iid seeds from μ, islands (100, 64) and (400, 16), mN ∈ {0, 0.1, 1} [after review: m = 0
   separates seed-basin selection from migration] (the mN rule of RESULTS "Rival networks" puts x = mN·T_nuc/N ≲ 0.3
   for independent islands; report T_nuc here), 40 runs per cell, horizon 10⁵ generations. [after review] The stop
   rule is the kernel's verified closed class (every pair of surviving classes payoff-identical on the present
   support, `src/islands.py`'s rule, under which fitnesses are equal for ever), *not* a partition-frozen state:
   on-path shadows can drift without changing the partition and later enable another convention, and migration can
   restart change. Runs not closed at the horizon are censored and reported as such, with the post-"partition-frozen"
   escape rate measured. Kernel as in `src/rival_islands.py` / `src/seeds_in_n.py` adapted to the weak arm's class
   tables (`src/islands.py` already handles weak-arm games and `ROLE`; reuse it). Record per island the partition at
   the horizon (split, inefficient, clash, unresolved), the holder's class, and per run the distribution of partitions
   across islands, the number of distinct conventions, whether islands with different conventions coexist (a
   rival-convention patchwork, with the loss hazard as in RESULTS "Rival networks"), and the deadweight loss.
   Uncertainty intervals are **run-level** (islands within a run are not independent replicates). With `ROLE`, a
   `ROLE`-split island is efficient and unequal *ex post* but equal *ex ante*; report both views, and define demand,
   realized payoff and normalized share separately [after review].
3. *Merge test:* separated end states merged into one population: does the larger convention win, or the
   risk-dominant one? Sweep the 50–50 share around the predicted threshold 3/8 (shares 0.25, 0.3, 0.35, 0.375, 0.4,
   0.45, 0.5), with both pure constant representatives and sampled island end states (which carry shadows), 100 merges
   per point, at N = 100 and 400 [after review].
4. *Fixed roles:* the chain (specified above) and the lottery with two slot populations; the lottery's per-island
   partition is a genuine unequal split between slots; report which slot gets more per island, the mean slot payoff
   (equal between slots by relabeling symmetry only in expectation, and equal to 1/2 only if every island is
   efficient [after review]), and E[max share].

**Scale guard** [after review: the primary comparison runs early]. Static tables for all three role structures;
then the N = 10² chains for all three (with the joint-simulation validation of the fixed-role reduction); then matched
lotteries at (100, 64), mN = 0.1, for all three; then N = 10³, 10⁴ chains, the other lottery cells, merges, and the
`dollar3` control. ≤ 3 workers. Stop where time runs out and say where.

## Required outputs

`runs/dollar-partitions.md` and `.json` (every table with intervals; support and transitions for every π), the
static tables as a section, code under `src/dollar*.py` (extend the carried-over files), a predictions file written
from the spec before any counted run, and the usual hand-back (draft RESULTS, REJECTED, THEORY §3 "Distribution" and
§9.11 edits, DEFERRED 3 and 6 edits, NOTATION, ≤ 5 lines on what matters, branch from `git branch --show-current`,
commits).

## RE predictions (with falsifiers)

1. **Mutation object with `ROLE`: 50–50 wins.** π on the 50–50 convention (constant S3 and its on-path shadows) is
   ≥ 0.5 at N ≥ 10³ and grows with N; the correlated splits (`ROLE`, `flip(ROLE)`, 1/3–2/3 via readers) hold ≤ 0.35
   together; P(efficient) ≥ 0.95. Reason: risk dominance (crossing 5/8) in the contest between the two 1-node
   conventions, which the RE expects to carry over to the full grammar because readers and shadows enter neutrally on
   both sides [after review: sol holds that mutation-entry weights and neutral paths can decide the large-N
   distribution, and predicts a fair advantage only in the restricted contest; the exit-rate table decides between
   the two readings]. *Falsifier:* correlated splits ≥ 0.5 at N = 10³, or 50–50 ≤ 0.3. **Control (ii), one
   population without `ROLE`:** 50–50 ≥ 0.7, since no correlated split is expressible and the unequal constants
   clash with themselves; *falsifier:* 50–50 ≤ 0.5.
2. **Seed lottery with `ROLE`: a patchwork, with 50–50 the modal convention but not dominant.** Across islands at
   (100, 64), mN = 0.1, the 50–50 convention holds 0.4–0.7 of islands, the `ROLE` (5/6, 1/6) split 0.1–0.4, and
   1/3–2/3 splits ≤ 0.2; ≥ 0.9 of islands are efficient at the horizon; at mN = 1 the patchwork resolves toward 50–50
   within 10⁵ generations in ≥ 0.5 of runs. *Falsifier:* 50–50 < 0.25 or `ROLE` > 0.5 of islands at mN = 0.1, or
   efficiency < 0.8.
3. **Merges go to the risk-dominant convention, not the larger one:** for pure-constant merges of 50–50 with `ROLE`,
   the 50–50 win probability crosses 1/2 at a 50–50 share in [0.35, 0.45] (the deterministic threshold is 3/8) and
   the crossing sharpens with N; at equal shares 50–50 wins ≥ 0.7 at N = 100 and ≥ 0.9 at N = 400. Sampled end
   states with shadows shift the crossing by < 0.05 [after review: sol notes the advantage at share 0.4 is small,
   0.35 against 1/3, so the prediction is about the crossing and its sharpening in N, not a universal probability].
   *Falsifier:* `ROLE` wins ≥ 0.5 of equal-share pure merges at N = 400, or the crossing lies outside [0.3, 0.5].
4. **Fixed roles: endpoint enrichment, not 50–50.** [after review: restated per ordered state against the
   uniform-over-ordered-splits benchmark, under which 50–50 already gets 1/5 and E[max share] already 0.70 in
   `dollar5`.] π is symmetric about 1/2 by relabeling (a check, not a prediction); per ordered split,
   π(1/6–5/6) ≥ 1.5·π(1/2–1/2) and π(1/3–2/3) ≥ π(1/2–1/2) at N ≥ 10³, so 50–50 ≤ 0.15 and E[max share] ≥ 0.72;
   the moves run through conceders (neutral drift of the losing side, then a strict move by the other), and the
   entry/exit-rate table shows the endpoints' *entry* rates are not smaller than the middle's, which is what the
   uniform-walk counterexample needs to fail. In `dollar3`, π(1/3–2/3) ≥ π(1/2–1/2) per ordered state (50–50 ≤ 1/3).
   *Falsifier:* π(1/6–5/6) ≤ π(1/2–1/2) per ordered state in `dollar5` at N = 10³, or E[max share] ≤ 0.70.
   (Young's adaptive-play result predicts the opposite; this is the prediction the RE is least sure of.)
5. **Fixed-role lottery:** per island, the 1/6–5/6 split is at least as frequent as 50–50 at (100, 64), m = 0 and
   mN = 0.1 (50–50 ≤ 0.2 of islands), the slot that gets more is decided per island by the scramble with no slot
   favoured in expectation (|mean slot payoff difference| < 0.05), and ≥ 0.8 of islands are efficient. *Falsifier:*
   50–50 ≥ 0.4 of islands, or 1/6–5/6 < 0.1.

The RS is invited to add predictions; his stated expectation is "no reason why 50–50 would be preferred", and the
RE's predictions 1 and 4 disagree with each other on that across the two role conventions, so this is a case where
his guess is wanted before the run.
