# Spec: the social organization game under the seed lottery: do strikers who arrive in numbers beat a cheap credible threat?, 2026-10-06

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-06-social-organization-lottery-gpt-6.1-sol.md`) and revised;
changes marked [after review]. To be run by an Opus subagent. The RS's question (2026-10-06): costless credible
threats hold the wage at zero under rare mutation; the proposed normative goal is a Θ(1/n) share; how do we get
there? This is the first lever: change the object. [after review] Results are finite-horizon incidence unless
closure is verified against globally surviving classes; three fixed roles cannot establish Θ(1/n), and the
distribution statistic is a three-role threshold.

## Why

In the ε→0 chain a striker enters one copy at a time, so a boss whose source says "whack strikers" pays c once
against one mutant and the mutant dies: the threat is credible (source-visible) and cheap (executed only against
rare entrants), and it holds π at zero wage without a whack on path (RESULTS "The union game", "Incentive-compatible
enforcement"). Every worker-side institution failed against this, and only removing the boss's commitment moved the
wage. Under iid seeding the entrants are not rare: the constant striker has mass 0.48 of the worker prior, so
[after review: encounter size, not N] each encounter of a boss with two iid-seeded workers contains ≈ 0.96 expected
constant strikers before conditional responses, and a committed whacking boss pays c per striker in nearly every
encounter from generation 0, while the wage it keeps is the same as a non-whacking boss's at the same s. The seed
lottery is therefore the regime in which "arrive in numbers" is available, and it has never been run on this game.
[after review] Relative to rare mutation the lottery also changes boss diversity and the simultaneous availability
of conditional programs, so the design crosses these levers rather than assuming which one acts.

## The game, preregistered [after review]

Three slots, separate populations, fixed roles: a boss B (wage s ∈ {0, 1/4, 1/2} to each working worker, keeping
1 − s per working worker; whack policy h ∈ {strike targeting, none, source targeting}, cost c per whack, loss
L = 1 to a whacked worker) and two workers W₁, W₂ (work or strike); a working worker produces 1. **Encounter:** one
program from each slot; payoffs as in `src/union.py`'s table (to be printed in the predictions file: for every
(s, h, a₁, a₂) the three payoffs, the production and the enforcement loss). **Matching:** each generation every
individual of each slot is matched once with a uniformly drawn individual of each other slot on the same island;
fitness is the mean payoff over an individual's encounters; **update kernel:** the island Moran birth–death of
`src/rival_islands.py` per slot, migration mN per slot per generation with uniform replacement within the slot.
Programs: the union-game grammar at the union run's cutoffs (boss n = 6, workers n = 10; QUORUM arm), free box.
c ∈ {0.1, 0.5}. **Commitment arms:** (CC) committed policies and (RR) both enforcement moves ex-post rational, from
`src/union_enforcement.py`. **Static before any run:** for every boss class, its payoff against the seed
composition of the worker slots at generation 0 (0.48 strikers, 0.48 scabs, readers), and in particular the
whacking-minus-non-whacking payoff difference at identical wages; for every worker class, its payoff against the
boss seed; the replicator from the seed composition per slot.

## Design

**Seed lottery.** ε = 0; islands I ∈ {16, 64}; per-slot island size N ∈ {100, 400}; mN ∈ {0, 0.1, 1}; horizon 10⁵
with a continuation of 40 runs to 3·10⁵ to test censoring; **stopping** [after review]: a run stops only when
closure is verified against the globally surviving classes of every slot including migrants (payoff identity on
the global support, and no neutral transition that changes play against any surviving class); otherwise it is
horizon-censored and reported as such; 40 runs per cell, run-level intervals. Recorded per island and per run:
the wage, work pattern, policy and realized whacks at the horizon; the disjoint summaries fair / intermediate /
zero wage / strike / scab split / repression; raw payoff vectors (boss, W₁, W₂), production, enforcement losses,
cumulative whack costs, production lost to strikes, extinction times of the striker, militant, union, whacking-boss
and fair-boss lineages, and conditional-program lineages; the first-500-generation time series of the striker share
and the whacking-boss share per island; whether islands end at different wages (a wage patchwork, finite-horizon)
and the **reciprocal invasion payoffs between observed terminal island states** [after review].

**The factorial** [after review: isolate the lever], at c = 0.5, (100, 16), mN = 0.1, CC, 40 runs per cell:
constant-striker seed mass {low: 0.12, high: 0.48 (the prior)} × boss seed {monomorphic hostile: the committed
strike-targeting boss at s = 0 only; mostly hostile: the same at 0.9 with a fixed 0.1 of non-whacking bosses at
s = 0; diverse: iid}, with the conditional-worker mass held fixed at the prior's; plus a **striker-mass sweep**
{0.06, 0.12, 0.24, 0.48} under the diverse boss seed to find the threshold at which non-whacking bosses establish.

**Controls.** (i) The chain's prediction for each cell (the union run's π at the same c, CC and RR). (ii)
**Two workers with QUORUM disabled**, same seed weights [after review: replaces the single-worker variant as the
handshake control; the single-worker variant is kept as a secondary cell]. (iii) The **replacement-pool** variant at
c = 0.5. (iv) RR for the main cells.

**Distribution statistic** [after review]. Raw payoff vectors and Pareto domination are reported first. Share
eligibility: islands with positive total surplus; for those, the minimum share of total surplus, and the fraction of
islands with minimum share ≥ 1/6, called the **three-role distribution threshold** (not a Θ(1/n) test); the
time-averaged shares over the last half of the horizon as the fallback.

Priority: static → CC main cell → RR main cell → factorial → striker sweep → QUORUM-disabled → N = 400 → mN
sweep → pool → continuation → c = 0.1 → single worker. ≤ 3 workers; stop where time runs out and say so.

## Required outputs

`runs/social-organization-lottery.md` and `.json`, code in `src/sog_lottery.py` (reusing `src/union.py`'s evaluator
and class tables, `src/union_enforcement.py`'s rational-enforcement evaluator, and the island kernel of
`src/rival_islands.py` generalized to three slot populations; no core edits except bug fixes in their own commits),
a predictions file from the spec (with the printed payoff table) committed before any counted run, the usual
hand-back (draft RESULTS, REJECTED, THEORY §3 "Distribution" and §9.9 edits, DEFERRED 6 and 10 edits, NOTATION,
≤ 5 lines, branch from `git branch --show-current`, commits).

## RE predictions (with falsifiers) [after review: aligned, grey zones named]

1. **Early whacker decline, residual policies:** in the CC main cell the whacking-boss share falls by ≥ 0.3 within
   the first 100 generations on ≥ 0.7 of islands, but whacking *policies* survive at the horizon on more islands
   than realized repression occurs (sol's point: once strikers die, surviving whackers are neutral); the RE guesses
   realized repression on ≤ 0.2 of islands and whacking policies on 0.2–0.6. *Falsifier:* no early decline (share
   falls by < 0.1 on ≥ 0.5 of islands), or realized repression on ≥ 0.5 of islands. Grey zone between.
2. **The wage still goes to zero on most islands:** zero wage on ≥ 0.6 of islands and fair on ≤ 0.15 in CC, because
   scabs (0.48) work at any wage and the zero-wage boss earns most once the strike has been absorbed. *Falsifier:*
   fair ≥ 0.3. Grey zone 0.15–0.3. (The prediction the RE would most like to be wrong about.)
3. **The lever is boss diversity, not worker numbers alone:** in the factorial, the monomorphic hostile seed gives
   scab convergence on ≥ 0.9 of islands at both striker masses; the mostly-hostile seed lets non-whackers establish
   on ≥ 0.5 of islands at high striker mass and ≤ 0.2 at low; the diverse seed's outcome is within 0.15 of the
   mostly-hostile one at high mass. *Falsifier:* strikers surviving on ≥ 0.3 of islands under the monomorphic
   hostile seed, or non-whackers establishing equally at low and high striker mass (difference < 0.1).
4. **The handshake matters only at the intermediate wage:** QUORUM-disabled gives the same fair and zero-wage
   shares within 0.05, and differs only in the intermediate share (the union run's finding transferred). **RR
   raises the wage** (intermediate ≥ 0.3 of islands at c = 0.5). *Falsifier:* QUORUM-disabled fair share
   differing by ≥ 0.15, or RR intermediate ≤ 0.1.
5. **The pool restores zero wage** (≥ 0.9 of islands with whacking bosses retained), **and a wage patchwork is a
   finite-horizon object at mN = 0.1** (≥ 0.3 of runs with two wages at the horizon) **that resolves at mN = 1 only
   where the reciprocal invasion payoffs permit** (sol's reading; the RE guesses most do). *Falsifier:* pool fair
   ≥ 0.2, or no patchwork at mN = 0.1 in ≥ 0.1 of runs.

**Three-role distribution threshold, RE guess** (reported, not a verdict): ≤ 0.1 of eligible islands in CC, ≤ 0.3 in
RR; time-averaged worker shares ≤ 0.1 each in CC.

The RS is invited to add predictions; the one the RE is least sure of is 2.
