# Predictions: the social organization game under the seed lottery (2026-10-06)

Spec: `specs/2026-10-06-social-organization-lottery.md` (reviewed by gpt-6.1-sol,
`reviews/2026-10-06-social-organization-lottery-gpt-6.1-sol.md`; where they differ the spec's [after review] text is
the resolution). Code: `src/sog_lottery.py`. Committed before any counted lottery run.

**What had been looked at when this was written.** (i) The static tables (`runs/sog-lottery-static.md`,
`runs/sog-lottery-static.json`; summarized below). (ii) The kernel validation against `src/union_abm.py`
(`runs/sog-lottery-validate.json`; passed, see below). (iii) Uncounted code-path runs: one main-cell-shaped run with
numpy seed 1 (strike-whacker share averaged over its 16 islands 0.35 → 0.15 (gen 10) → 0.19 (gen 100) → 0.11 (gen
500); zero wage on 12 of 16 islands at gen 2,000; globally closed at gen 3,500), four smoke runs at I = 4 for 3,000
generations (CC, RR, CC + pool, CC at mN = 0: all four islands at zero wage in each), and five timing runs (run
index 10⁶, only status and stop generation printed: CC main closed at 11,100; RR main closed at 11,600; mN = 1
closed at 1,292; N = 400 censored at 10⁵; I = 64 closed at 14,000). No counted run has been made.

## The game, matching and kernel as run (preregistered by the spec; reproduced here)

- **Game.** Three slots, separate populations, fixed roles: boss B (wage s ∈ {0, 1/4, 1/2} to each working worker,
  keeps 1 − s per working worker; whack policy h ∈ {strike targeting, none, source targeting}, cost c per whack,
  loss L = 1 to a whacked worker) and two workers W₁, W₂ (work or strike; a working worker produces 1). Encounter
  payoffs: `src/union.py`'s table (printed in full below). Programs: the union-game grammar at the union run's cutoffs
  (boss n = 6: 297 behavioural classes; workers n = 10: 364 classes; QUORUM arm), free box, level 0. Classes are
  re-lumped exactly under each evaluator (CC: 297 / 364; RR: 13 / 62, since a rational boss never whacks without the
  pool and all wage-equal bosses merge; QUORUM-disabled CC: 297 / 310).
- **Commitment arms.** CC: committed play (the union run's game). RR: both enforcement moves ex-post rational, from
  `src/union_enforcement.py` (tie rule 'whack'; off path without the pool).
- **Matching.** Each individual of each slot meets one member of each other slot of its island per encounter;
  fitness is the expected payoff over a uniform draw of those two members (the expectation of the spec's "matched
  once with a uniformly drawn individual of each other slot"; the single-draw matching noise is not simulated —
  `src/union_abm.py` and `src/rival_islands.py` use the same expectation).
- **Update kernel.** The island Moran birth–death of `src/rival_islands.py` per slot: a birth picks an (island,
  slot) unit uniformly; with probability m = mN/N the parent comes from the same slot of a uniformly chosen other
  island; the parent is drawn on the source island with weight count·exp(w·fitness), w = 0.3; the victim is uniform
  in the recipient unit. A generation is 3·I·N births (N births per slot per island). ε = 0. Exact event skipping
  (a birth in a monomorphic unit without a migrant changes nothing; geometric skip, law unchanged).
- **Seed.** Iid per slot per island from the slot's seed distribution (multinomial(N, p) per unit). Default p = the
  length prior over classes: boss constants 0.108 each (9 constants, 0.976 in all), conditional bosses 0.024;
  workers: scab 0.480, constant striker 0.480 (in the class masses: 0.4802 each), conditional workers 0.040 (the
  militant 1.2·10⁻³, the union 9.9·10⁻⁶).
- **Factorial seeds.** Constant-striker mass p_s with the conditional-worker mass held at the prior's (0.0397) and
  the scab taking the rest (1 − p_s − 0.0397). Boss seeds: *hostile* = the committed strike-targeting boss at
  s = 0 only; *mostly hostile* = the same at 0.9 and the non-whacking `(0, none)` at 0.1; *diverse* = the prior.
- **Stopping.** mN > 0: a run stops when closure is verified against the globally surviving classes of every slot:
  in every slot all globally present classes give the same realized play key (a₁, a₂, whacked₁, whacked₂, wage paid
  if anyone works) against every combination of globally present classes of the other two slots. This implies one
  play everywhere, payoff identity on the global support and no neutral transition that changes play against any
  surviving class; at ε = 0 nothing can change a payoff again. It follows that a wage patchwork (islands at
  different wages) can never be closure-verified at mN > 0: a patchwork is always horizon-censored. mN = 0: the run
  stops when every island is locally closed in the same sense. Otherwise the run is **horizon-censored** at 10⁵
  generations (3·10⁵ in the continuation) and reported as such. Checks every generation to 2,000, every 25 to
  10⁴, every 100 after.
- **Cells.** Main: CC, c = 0.5, N = 100 per slot, I = 16, mN = 0.1, prior seed, 40 runs. RR main. Factorial at the
  main cell's parameters: p_s ∈ {0.12, 0.48} × boss seed {hostile, mostly, diverse} ((0.48, diverse) = CC main).
  Striker sweep {0.06, 0.12, 0.24, 0.48} × diverse (0.12 and 0.48 shared with the factorial). QUORUM-disabled
  (the matched no-QUORUM grammar of `src/union.py`, same per-spelling weights), CC. N = 400. I = 64 (extra). mN ∈
  {0, 1}. CC + replacement pool. Continuation: the main cell's 40 seeds to 3·10⁵. c = 0.1 (CC and RR). Single-worker
  cell last, if time allows. Extras if time allows: RR at N = 400, QUORUM-disabled RR.

## Definitions used by the verdicts (fixed now)

- **Island label** at stop or horizon: the argmax of the 7 disjoint summaries (fair / intermediate / zero wage /
  strike / scab split / repression:strike / repression:source) of the island's encounter distribution (one uniform
  member per slot). A cell's share of a label = the mean over runs of the run's fraction of islands with that label;
  intervals are run-level (mean ± 1.96·SE over the 40 runs).
- **Whacking boss** (prediction 1, the factorial): a *strike-whacker* = a boss class that realizes a whack on a
  constant striker in some encounter with workers from {scab, constant striker}² (strike targeting; 0.339 of the
  prior). *Any-whacker* adds the classes that realize a whack in some encounter with workers from {scab, striker,
  militant, union}² (source targeting; 0.673 of the prior), reported alongside. Source targeting costs nothing
  against the untagged constant striker, so the strike-whacker is the boss the spec's cost argument is about.
- **Early decline** (prediction 1): per island, strike-whacker share at generation 0 minus its minimum over
  generations 0–100 (also reported: share(0) − share(100)).
- **Realized repression on an island:** expected whacks per encounter > 10⁻³ at stop/horizon (the label
  repression:strike/source is reported as well). **Whacking policy on an island:** strike-whacker share > 0
  (any-whacker share > 0 reported alongside).
- **Non-whackers establish** (prediction 3, the sweep): the island's strike-whacker share at stop/horizon < 0.5.
  **Scab convergence:** label zero wage and constant-striker share 0. **Strikers surviving:** constant-striker share
  > 0 at stop/horizon.
- **Island wage** (patchwork, prediction 5): the offered wage with the largest encounter mass among encounters in
  which at least one worker works; islands with production < 0.05 have no wage. **Patchwork** = a run with ≥ 2
  distinct island wages at stop/horizon.
- **Distribution statistic.** Raw payoff vectors (boss, W₁, W₂), production, enforcement losses first; Pareto
  domination between cells on the mean payoff vectors. Eligible islands: three-slot total payoff > 0. Minimum share =
  min(u)/total; **three-role distribution threshold** = fraction of eligible islands with minimum share ≥ 1/6.
  Time-averaged shares over generations 5·10⁴–10⁵ (a closed run is frozen after its stop and is extended).

## RE predictions (copied verbatim from the spec)

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

Readings fixed now for the verdicts. Prediction 1: "whacking-boss share" = the strike-whacker share; the first
clause holds if the early decline is ≥ 0.3 on ≥ 0.7 of islands; "whacking policies survive on more islands than
realized repression" is checked as stated. Prediction 2: island labels in CC main. Prediction 3: "scab convergence"
and "strikers surviving" as defined; "non-whackers establish" = strike-whacker share < 0.5 at the end; "the diverse
seed's outcome" = the same establishment fraction. Prediction 4: QUORUM-disabled CC vs CC main; RR main.
Prediction 5: "≥ 0.9 of islands with whacking bosses retained" read as zero wage on ≥ 0.9 of islands in CC + pool,
with the fraction of those islands that keep a strike-whacker reported; patchwork at mN = 0.1 read on CC main; "no
patchwork at mN = 0.1 in ≥ 0.1 of runs" read as: the falsifier fires if fewer than 0.1 of CC-main runs are
patchworks. The mN = 1 clause is reported (patchwork fraction and the signs of the reciprocal invasion payoffs),
not given a verdict.

## Static results (before any run; `runs/sog-lottery-static.md`)

- **Against the iid seed at gen 0** (CC, c = 0.5): constant bosses earn (0, none) 1.000, (0, source) 0.997,
  (0, strike) 0.500; (1/4, ·) 0.750 / 0.747 / 0.250; (1/2, ·) 0.500 / 0.497 / 0.000. **Whacking minus non-whacking
  at identical wage:** strike targeting −0.500 at every wage (= −c × the expected number of strikers per encounter: 0.96 constant strikers plus the
  conditional workers that strike), source targeting −0.003. At p_s = 0.24 / 0.12 / 0.06: −0.260 / −0.140 / −0.080.
  At c = 0.1: −0.100. With the pool: **+0.500 / +0.250 / 0.000** at s = 0 / 1/4 / 1/2.
- **Workers against the boss seed:** scab 0.250, constant striker −0.333, militant −0.055, union −0.233, union′
  0.100. Under RR every worker class earns 0.250 against the seed: the worker slots are exactly neutral in RR
  (a rational worker works at s > 0 and is indifferent at s = 0, where it follows its program), and the boss's best
  constant against the seed is s = 1/4 (1.500 against 1.000 at s = 0 and s = 1/2).
- **Replicator** (the deterministic per-generation mean of the kernel, from the seed), CC main: strike-whacker share
  0.339 → 0.156 (gen 10) → 0.020 (100) → 0.001 (500); fair bosses 0.333 → 0.003 (25); constant strikers 0.48 →
  0.05 (100); zero wage 0.93, scab split 0.07 of encounters at gen 500. At p_s ≤ 0.24 the strike-whacker share
  falls only to 0.20–0.31 and then **rises again** (0.45–0.57 at gen 500): once the constant strikers are gone, a
  residue of conditional workers that strike against non-whackers and work against whackers pays the whacker; the
  same happens at c = 0.1 (0.29 → 0.71) and with the pool (0.34 → 0.94). Mostly hostile: 0.90 → 0.81 → 0.99.
  QUORUM-disabled: identical to CC main to 10⁻³ in every column but the any-whacker share (source targeting has
  no target without the tag). RR: intermediate 0.998 of encounters by gen 100 with the worker shares unchanged.
- **Distribution arithmetic** (from the payoff table, no run needed): the three role payoffs at a both-working
  island are (2(1 − s), s, s); the minimum share s/2 is ≥ 1/6 iff s ≥ 1/3. **The three-role threshold can be met
  only at the fair wage**; the intermediate wage gives 1/8.

## Kernel validation (`runs/sog-lottery-validate.json`)

The three-slot island kernel was validated against `src/union_abm.py` (an independent implementation of the same
law without event skipping) on a small cell with identical initial islands (I = 4, N = 20, mN = 0.5, c = 0.5,
w = 0.3; islands seeded with four different monomorphic triples), comparing the island-level summary distribution
and payoffs at generations 15 and 150 over independent replicates: 3,000 replicates, 80 statistics, max |z| 2.26,
2.5% with |z| > 2; a targeted re-test at generation 15 with 15,000 replicates per side: max |z| 2.02 over 40
statistics, pooled payoff z = 0.12 / −0.96 / 0.45 (boss / W₁ / W₂).

## Subagent's own predictions (S), with falsifiers

- **S1 (CC main, wage).** Zero wage is the label on ≥ 0.75 of islands; fair on ≤ 0.02; intermediate ≤ 0.05. The
  remaining islands carry scab split or strike at s = 0 (strikers are neutral there beside a non-whacking boss).
  *Falsifier:* fair ≥ 0.1 or zero wage < 0.6.
- **S2 (CC main, the whacker race).** The early decline of the strike-whacker share is ≥ 0.3 on 0.15–0.55 of
  islands and < 0.1 on 0.2–0.5 (finite islands split: where strikers die first the whackers stop paying and drift).
  Strike-whacker policies survive at stop/horizon on ≥ 0.25 of islands and realized repression occurs on ≤ 0.05.
  *Falsifier:* decline ≥ 0.3 on ≥ 0.7 of islands, or realized repression on ≥ 0.2.
- **S3 (RR main).** The workers drift neutrally; the boss pays 1/4 wherever at least one worker slot is dominated
  by programs that strike at s = 0, so intermediate is the label on 0.5–0.9 of islands (the chain's 0.75 is the
  1 − (1/2)² of two independent neutral worker slots), fair ≤ 0.02, realized repression 0. *Falsifier:*
  intermediate < 0.3 or > 0.95.
- **S4 (factorial).** Hostile seed: scab convergence on ≥ 0.95 of islands and strikers extinct in every run at both
  masses. Mostly hostile: non-whackers establish on ≤ 0.3 of islands at both masses, with |high − low| < 0.1
  (the transient striker advantage of `(0, none)` is worth a log-odds of about c·w·∫2p_s dt ≈ 0.5, i.e. 0.1 → 0.15,
  then neutral drift) — i.e. **the RE's prediction 3 falsifier fires**. Diverse: non-whackers establish on ≥ 0.6
  of islands at both masses. *Falsifier:* mostly-hostile establishment ≥ 0.5 at high mass.
- **S5 (striker sweep, diverse).** The fraction of islands with strike-whacker share < 0.5 at the end is
  non-decreasing in p_s within 0.1 across {0.06, 0.12, 0.24, 0.48} and is ≥ 0.7 at 0.48. Zero wage ≥ 0.75 at every
  p_s. *Falsifier:* a decrease of more than 0.1 between adjacent p_s, or < 0.6 at 0.48.
- **S6 (QUORUM disabled).** Every label share within 0.05 of CC main (the union is seeded with expected count
  0.03 per slot per run; nothing reads QUORUM on path). *Falsifier:* any label share differing by ≥ 0.1.
- **S7 (pool).** Zero wage ≥ 0.9 of islands, and a strike-whacker share ≥ 0.5 on ≥ 0.6 of islands at the end
  (the pool makes strike targeting strictly better while strikers exist). *Falsifier:* zero wage < 0.8 or
  strike-whacker majority on < 0.3.
- **S8 (patchwork).** At mN = 0.1 fewer than 0.2 of CC-main runs are wage patchworks at stop/horizon (the non-zero
  wages die within ~25 generations); hence the RE's prediction-5 patchwork clause fails and its falsifier fires if
  the fraction is < 0.1. *Falsifier:* patchwork in ≥ 0.3 of runs.
- **S9 (censoring).** ≥ 0.85 of CC-main runs and ≥ 0.6 of RR-main runs are closure-verified before 10⁵; N = 400
  censors more (≥ 0.3 censored). *Falsifier:* CC main censored in > 0.3 of runs.
- **S10 (distribution).** The three-role threshold is met on ≤ 0.02 of eligible islands in every cell (only fair
  islands can meet it); the RE's RR guess (≤ 0.3) holds trivially. Time-averaged worker shares ≤ 0.05 each in CC,
  0.08–0.13 in RR (1/4 of 2 at an intermediate island, 0 at a zero-wage one). RR Pareto-dominates CC main on the
  cell-mean payoff vector. *Falsifier:* threshold met on > 0.05 of eligible islands in any CC cell.
- **S11 (c = 0.1).** Zero wage ≥ 0.75 of islands; strike-whacker majority on more islands than at c = 0.5 (by ≥
  0.15). *Falsifier:* fewer strike-whacker-majority islands than at c = 0.5.
- **S12 (N = 400, I = 64, mN).** N = 400 and I = 64: fair ≤ 0.02 and zero wage within 0.15 of CC main. mN = 0 and
  mN = 1: zero wage within 0.15 of CC main. *Falsifier:* fair ≥ 0.1 in any of these cells.

## Verdict rules

Each prediction is held, failed (falsifier fired) or inconclusive (grey zone, or censoring makes the measured
quantity a finite-horizon incidence that could still move). Island fractions are reported with run-level 95%
intervals; a threshold is judged on the cell mean, and a verdict whose interval straddles the threshold is called
"held (narrowly)" or "failed (narrowly)". Every number is a finite-horizon incidence unless the run is
closure-verified; closure-verified runs are frozen in play forever (ε = 0), censored runs are reported separately.
The chain's prediction for each cell (RESULTS "The union game", "Incentive-compatible enforcement") is quoted as
control (i).

## 1. Payoff table (one encounter; L = 1; tags matter only under source targeting)

u_B = (1 - s) x #working - c x #whacks; a working worker gets s, a striker 0, a whacked worker loses L = 1; production = #working; enforcement loss = c x #whacks (boss) + L x #whacks (workers). With the pool a whacked striker is replaced by an outside scab: the boss gains 1 - s per replaced striker and the outside scab earns s.

| s | h | W1 | W2 | tags | u_B (c=0.5) | u_B (c=0.1) | u_W1 | u_W2 | production | whacks | loss: workers | loss: boss c=0.5 / 0.1 | summary | u_B pool c=0.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | strike | W | W | 00 | 2.00 | 2.00 | 0.00 | 0.00 | 2 | 0 | 0.0 | 0.00 / 0.00 | zero wage | 2.00 |
| 0 | strike | W | S | 00 | 0.50 | 0.90 | 0.00 | -1.00 | 1 | 1 | 1.0 | 0.50 / 0.10 | repression:strike | 1.50 |
| 0 | strike | S | W | 00 | 0.50 | 0.90 | -1.00 | 0.00 | 1 | 1 | 1.0 | 0.50 / 0.10 | repression:strike | 1.50 |
| 0 | strike | S | S | 00 | -1.00 | -0.20 | -1.00 | -1.00 | 0 | 2 | 2.0 | 1.00 / 0.20 | repression:strike | 1.00 |
| 0 | none | W | W | 00 | 2.00 | 2.00 | 0.00 | 0.00 | 2 | 0 | 0.0 | 0.00 / 0.00 | zero wage | 2.00 |
| 0 | none | W | S | 00 | 1.00 | 1.00 | 0.00 | 0.00 | 1 | 0 | 0.0 | 0.00 / 0.00 | scab split | 1.00 |
| 0 | none | S | W | 00 | 1.00 | 1.00 | 0.00 | 0.00 | 1 | 0 | 0.0 | 0.00 / 0.00 | scab split | 1.00 |
| 0 | none | S | S | 00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0.0 | 0.00 / 0.00 | strike | 0.00 |
| 0 | source | W | W | 00 | 2.00 | 2.00 | 0.00 | 0.00 | 2 | 0 | 0.0 | 0.00 / 0.00 | zero wage | 2.00 |
| 0 | source | W | W | 01 | 1.50 | 1.90 | 0.00 | -1.00 | 2 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 1.50 |
| 0 | source | W | W | 10 | 1.50 | 1.90 | -1.00 | 0.00 | 2 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 1.50 |
| 0 | source | W | W | 11 | 1.00 | 1.80 | -1.00 | -1.00 | 2 | 2 | 2.0 | 1.00 / 0.20 | repression:source | 1.00 |
| 0 | source | W | S | 00 | 1.00 | 1.00 | 0.00 | 0.00 | 1 | 0 | 0.0 | 0.00 / 0.00 | scab split | 1.00 |
| 0 | source | W | S | 01 | 0.50 | 0.90 | 0.00 | -1.00 | 1 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 1.50 |
| 0 | source | W | S | 10 | 0.50 | 0.90 | -1.00 | 0.00 | 1 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 0.50 |
| 0 | source | W | S | 11 | 0.00 | 0.80 | -1.00 | -1.00 | 1 | 2 | 2.0 | 1.00 / 0.20 | repression:source | 1.00 |
| 0 | source | S | W | 00 | 1.00 | 1.00 | 0.00 | 0.00 | 1 | 0 | 0.0 | 0.00 / 0.00 | scab split | 1.00 |
| 0 | source | S | W | 01 | 0.50 | 0.90 | 0.00 | -1.00 | 1 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 0.50 |
| 0 | source | S | W | 10 | 0.50 | 0.90 | -1.00 | 0.00 | 1 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 1.50 |
| 0 | source | S | W | 11 | 0.00 | 0.80 | -1.00 | -1.00 | 1 | 2 | 2.0 | 1.00 / 0.20 | repression:source | 1.00 |
| 0 | source | S | S | 00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0.0 | 0.00 / 0.00 | strike | 0.00 |
| 0 | source | S | S | 01 | -0.50 | -0.10 | 0.00 | -1.00 | 0 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 0.50 |
| 0 | source | S | S | 10 | -0.50 | -0.10 | -1.00 | 0.00 | 0 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 0.50 |
| 0 | source | S | S | 11 | -1.00 | -0.20 | -1.00 | -1.00 | 0 | 2 | 2.0 | 1.00 / 0.20 | repression:source | 1.00 |
| 1/4 | strike | W | W | 00 | 1.50 | 1.50 | 0.25 | 0.25 | 2 | 0 | 0.0 | 0.00 / 0.00 | intermediate | 1.50 |
| 1/4 | strike | W | S | 00 | 0.25 | 0.65 | 0.25 | -1.00 | 1 | 1 | 1.0 | 0.50 / 0.10 | repression:strike | 1.00 |
| 1/4 | strike | S | W | 00 | 0.25 | 0.65 | -1.00 | 0.25 | 1 | 1 | 1.0 | 0.50 / 0.10 | repression:strike | 1.00 |
| 1/4 | strike | S | S | 00 | -1.00 | -0.20 | -1.00 | -1.00 | 0 | 2 | 2.0 | 1.00 / 0.20 | repression:strike | 0.50 |
| 1/4 | none | W | W | 00 | 1.50 | 1.50 | 0.25 | 0.25 | 2 | 0 | 0.0 | 0.00 / 0.00 | intermediate | 1.50 |
| 1/4 | none | W | S | 00 | 0.75 | 0.75 | 0.25 | 0.00 | 1 | 0 | 0.0 | 0.00 / 0.00 | scab split | 0.75 |
| 1/4 | none | S | W | 00 | 0.75 | 0.75 | 0.00 | 0.25 | 1 | 0 | 0.0 | 0.00 / 0.00 | scab split | 0.75 |
| 1/4 | none | S | S | 00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0.0 | 0.00 / 0.00 | strike | 0.00 |
| 1/4 | source | W | W | 00 | 1.50 | 1.50 | 0.25 | 0.25 | 2 | 0 | 0.0 | 0.00 / 0.00 | intermediate | 1.50 |
| 1/4 | source | W | W | 01 | 1.00 | 1.40 | 0.25 | -0.75 | 2 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 1.00 |
| 1/4 | source | W | W | 10 | 1.00 | 1.40 | -0.75 | 0.25 | 2 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 1.00 |
| 1/4 | source | W | W | 11 | 0.50 | 1.30 | -0.75 | -0.75 | 2 | 2 | 2.0 | 1.00 / 0.20 | repression:source | 0.50 |
| 1/4 | source | W | S | 00 | 0.75 | 0.75 | 0.25 | 0.00 | 1 | 0 | 0.0 | 0.00 / 0.00 | scab split | 0.75 |
| 1/4 | source | W | S | 01 | 0.25 | 0.65 | 0.25 | -1.00 | 1 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 1.00 |
| 1/4 | source | W | S | 10 | 0.25 | 0.65 | -0.75 | 0.00 | 1 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 0.25 |
| 1/4 | source | W | S | 11 | -0.25 | 0.55 | -0.75 | -1.00 | 1 | 2 | 2.0 | 1.00 / 0.20 | repression:source | 0.50 |
| 1/4 | source | S | W | 00 | 0.75 | 0.75 | 0.00 | 0.25 | 1 | 0 | 0.0 | 0.00 / 0.00 | scab split | 0.75 |
| 1/4 | source | S | W | 01 | 0.25 | 0.65 | 0.00 | -0.75 | 1 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 0.25 |
| 1/4 | source | S | W | 10 | 0.25 | 0.65 | -1.00 | 0.25 | 1 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 1.00 |
| 1/4 | source | S | W | 11 | -0.25 | 0.55 | -1.00 | -0.75 | 1 | 2 | 2.0 | 1.00 / 0.20 | repression:source | 0.50 |
| 1/4 | source | S | S | 00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0.0 | 0.00 / 0.00 | strike | 0.00 |
| 1/4 | source | S | S | 01 | -0.50 | -0.10 | 0.00 | -1.00 | 0 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 0.25 |
| 1/4 | source | S | S | 10 | -0.50 | -0.10 | -1.00 | 0.00 | 0 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 0.25 |
| 1/4 | source | S | S | 11 | -1.00 | -0.20 | -1.00 | -1.00 | 0 | 2 | 2.0 | 1.00 / 0.20 | repression:source | 0.50 |
| 1/2 | strike | W | W | 00 | 1.00 | 1.00 | 0.50 | 0.50 | 2 | 0 | 0.0 | 0.00 / 0.00 | fair | 1.00 |
| 1/2 | strike | W | S | 00 | 0.00 | 0.40 | 0.50 | -1.00 | 1 | 1 | 1.0 | 0.50 / 0.10 | repression:strike | 0.50 |
| 1/2 | strike | S | W | 00 | 0.00 | 0.40 | -1.00 | 0.50 | 1 | 1 | 1.0 | 0.50 / 0.10 | repression:strike | 0.50 |
| 1/2 | strike | S | S | 00 | -1.00 | -0.20 | -1.00 | -1.00 | 0 | 2 | 2.0 | 1.00 / 0.20 | repression:strike | 0.00 |
| 1/2 | none | W | W | 00 | 1.00 | 1.00 | 0.50 | 0.50 | 2 | 0 | 0.0 | 0.00 / 0.00 | fair | 1.00 |
| 1/2 | none | W | S | 00 | 0.50 | 0.50 | 0.50 | 0.00 | 1 | 0 | 0.0 | 0.00 / 0.00 | scab split | 0.50 |
| 1/2 | none | S | W | 00 | 0.50 | 0.50 | 0.00 | 0.50 | 1 | 0 | 0.0 | 0.00 / 0.00 | scab split | 0.50 |
| 1/2 | none | S | S | 00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0.0 | 0.00 / 0.00 | strike | 0.00 |
| 1/2 | source | W | W | 00 | 1.00 | 1.00 | 0.50 | 0.50 | 2 | 0 | 0.0 | 0.00 / 0.00 | fair | 1.00 |
| 1/2 | source | W | W | 01 | 0.50 | 0.90 | 0.50 | -0.50 | 2 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 0.50 |
| 1/2 | source | W | W | 10 | 0.50 | 0.90 | -0.50 | 0.50 | 2 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 0.50 |
| 1/2 | source | W | W | 11 | 0.00 | 0.80 | -0.50 | -0.50 | 2 | 2 | 2.0 | 1.00 / 0.20 | repression:source | 0.00 |
| 1/2 | source | W | S | 00 | 0.50 | 0.50 | 0.50 | 0.00 | 1 | 0 | 0.0 | 0.00 / 0.00 | scab split | 0.50 |
| 1/2 | source | W | S | 01 | 0.00 | 0.40 | 0.50 | -1.00 | 1 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 0.50 |
| 1/2 | source | W | S | 10 | 0.00 | 0.40 | -0.50 | 0.00 | 1 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 0.00 |
| 1/2 | source | W | S | 11 | -0.50 | 0.30 | -0.50 | -1.00 | 1 | 2 | 2.0 | 1.00 / 0.20 | repression:source | 0.00 |
| 1/2 | source | S | W | 00 | 0.50 | 0.50 | 0.00 | 0.50 | 1 | 0 | 0.0 | 0.00 / 0.00 | scab split | 0.50 |
| 1/2 | source | S | W | 01 | 0.00 | 0.40 | 0.00 | -0.50 | 1 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 0.00 |
| 1/2 | source | S | W | 10 | 0.00 | 0.40 | -1.00 | 0.50 | 1 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 0.50 |
| 1/2 | source | S | W | 11 | -0.50 | 0.30 | -1.00 | -0.50 | 1 | 2 | 2.0 | 1.00 / 0.20 | repression:source | 0.00 |
| 1/2 | source | S | S | 00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0.0 | 0.00 / 0.00 | strike | 0.00 |
| 1/2 | source | S | S | 01 | -0.50 | -0.10 | 0.00 | -1.00 | 0 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 0.00 |
| 1/2 | source | S | S | 10 | -0.50 | -0.10 | -1.00 | 0.00 | 0 | 1 | 1.0 | 0.50 / 0.10 | repression:source | 0.00 |
| 1/2 | source | S | S | 11 | -1.00 | -0.20 | -1.00 | -1.00 | 0 | 2 | 2.0 | 1.00 / 0.20 | repression:source | 0.00 |

