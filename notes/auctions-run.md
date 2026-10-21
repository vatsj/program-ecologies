# Coalition-proof auctions: the run (engineer, 2026-10-21)

Spec `specs/2026-10-21-coalition-proof-auctions.md`; theory `notes/coalition-proof-auctions.md`; predictions
`predictions/2026-10-21-coalition-proof-auctions.md` (committed before any code, with the scoring conventions fixed
in a second commit before any counted cell); verdicts `runs/auctions.md`. Code: `src/auctions.py` (rules, winner
determination, the notion kernel, ring, 2XL), `src/auctions_static.py` (Part A driver), `src/auction_islands.py`,
`src/auction_islands_run.py` (Part B), `src/auctions_report.py` (tables, verdict digest); tests
`tests/test_auctions.py`, `tests/test_auction_islands.py` (19 tests, all pass). Outputs `runs/auctions/` (summary JSON,
CSV tables, per-cell JSON; no arrays). One worker throughout. The note's decimal examples are scaled by 10 (integer
reports; values (2, .5, .5) are (20, 5, 5), the 2XL grid 0.1 is one unit on 0..200).

Seeded runs are deterministic: the second pass of the primary cells reproduced every first-pass number exactly.

## 1. Statics (Part A)

### 1.1 What was checked first (tests)
* Winner determination with the tie rule (more winners, then lowest index tuple): P = AB at 20 against A + B = 20 goes
  to A and B; substitutes with equal bids go to the lower index; zero reports win free items.
* AM VCG closed forms on 400 random profiles; Ausubel–Milgrom numbers: values (20, 5, 5): P wins, price 10; losers'
  overbid to 20 each: each nets +5 under VCG and −5 under the surcharge (payments 10 + 10); values (20, 15, 15):
  VCG pays 5 and 5, surcharge pays 10 and 10; bidder A shading to 12 gives payments 8.5 and 11.5, a gain of 1.5 (0.15
  in note units) for the shader taken from bidder B.
* The surcharge is in the core on every profile checked (all bidder sets, individual rationality, non-negative),
  equals VCG exactly when VCG is in the core, matches an independent LP + SLSQP implementation (generic path) on 240
  random profiles of the four families to 1e-4, and has the LP minimum revenue. At most two winners occur in the four
  families, where the minimum-revenue core with the VCG-nearest selection is exact in closed form (a segment on a
  line); the generic scipy path covers three or more winners and is not exercised by the families.
* 2XL: with ties against the leader the leader values at v = (10, 6) on the 0.1 grid are 6.9 (the high type) and
  5.0; with ties for the leader, 7.0 and 5.0; equal values give a symmetric pair.
* The notion kernel (numba) equals a plain-Python reference (R1 closure by the two graph rules, R2 maximizers, the five
  variants) on AM and a 4-bidder subsample at G = 3.

### 1.2 Truth-robustness (instances where no proper coalition profits), spec grid (reports 0..20)

AM (all 1,000 instances); AM+, substitutes and two packages on a fixed-seed subsample of 3,000 of 10,000
(`numpy.random.default_rng(20261021)`); no unresolved R1 instance occurred anywhere (the closure always contained an
equilibrium).

| family | VCG in core | mean surcharge | VCG robust (all 5 variants) | surcharge robust | VCG robust ignoring mixed coalitions (R1 T-weak) | surcharge robust ignoring mixed (R1 T-weak) |
|---|---|---|---|---|---|---|
| AM | 0.165 | 2.53 (3.03 when positive) | 0.385 | 0.000 | 0.385 | 1.000 |
| AM+ | 0.500 | 1.27 | 0.000 | 0.000 | 0.948 | 1.000 |
| substitutes (control) | 1.000 | 0 | 0.000 | 0.000 | 1.000 | 1.000 |
| two packages | 0.246 | 2.75 | 0.194 | 0.000 | 0.194 | 1.000 |

"Mixed" = a coalition containing a truthful winner and a truthful loser. Table: `runs/auctions/table_A_robust.csv` (all
variants, with the singleton / losers / winners / mixed breakdown).

**The headline** is that truth is robust to almost nothing, and what breaks it is not what the note predicted.
Under both rules every family contains a profitable *mixed* coalition on essentially every instance: a loser lowers
its report to zero at no cost to itself and the winner's price falls (in the substitutes control, the winner and the
runner-up on the same item; in AM, P with an item bidder). That is the textbook Vickrey ring, available whenever a
loser's report is an input to a winner's price, and no core rule removes it, because the core only blocks coalitions
that include the seller. The substitutes control makes the point cleanly: VCG is in the core on 3,000 of 3,000
instances and truth is robust on none. Prediction 1 failed for this reason.

### 1.3 The spite readings (T-strict, T-weak, literal)

* **Literal reading** (strict-improvement graph for both ties; spite reachable only through strict improvements): identical
  to T-strict on every number. An indifferent loser never leaves its truthful bid, so spite never counts.
* **T-weak** (my reading: the best-reply graph admits any best reply, including a payoff-equal one): deters nothing at
  the instance level (every instance has a mixed coalition), and at the event level (break coalitions that T-strict
  breaks and T-weak does not) deters 0 of 1,515 (VCG) and 1,670 of 3,670 (surcharge) in AM; 25% and 33% in AM+, 3% in
  substitutes, 7% and 33% in two packages (`table_A_spite.csv`).
* **Where spite does and does not work.** Under the surcharge on the spec grid, T-weak deters *every* singleton, pure
  loser and pure winner break (surcharge robust ignoring mixed coalitions = 1.000 in all four families), the singleton
  shade included: the loser's raise is a best reply that costs it nothing and moves the shader's price against it. Under
  VCG on the spec grid it deters the singletons but not the pure-pair overbids (AM: losers 0.12 and winners 0.495 still
  break; AM+ 0.052 of losers), because **the grid cap lets the pair overbid to the cap**: with reports on 0..2G for
  everyone the pair bids 2G each and P's spite is capped at 2G < 4G. With responders on 0..4G and deviators on
  0..2G (`wide` sensitivity, AM only), T-weak VCG deters every same-side coalition too (robust ignoring mixed 1.000),
  deterred-only events 615 of 1,515 (41%) and the spiter's margin is exactly one tick (it bids one tick below winning).
  The note's section 5 claim therefore holds on an unbounded response grid and fails at a cap; it holds for every
  same-side coalition and for no mixed coalition.
* Spiter's margin (surcharge, AM, 400 sampled break events, 601 spiters): median 0 ticks; 67% of spiters sit at or above
  winning (they win at the spite bid, so the spite is not free for them). Under VCG with wide responders the margin is
  exactly 1 (400 of 400), so the spiter loses the auction by one tick and pays nothing.
* R2 (coalitional complement): R2 T-strict shows singleton breaks that R1 does not (AM VCG 0.46 of instances): when the
  deviating bidder is an item bidder, the complement {P, B} responds *jointly*, and its optimal joint response includes
  a costless bid reduction by the loser, which lowers the deviator's price too. The responding ring helps the deviator.
  Under T-weak R2 the singleton breaks disappear for VCG and persist for the surcharge (0.735).

### 1.4 Revenue, welfare and the ring (truthful reports)

| family | efficient welfare | revenue VCG / surcharge / first-price | bidder welfare VCG / surcharge / FP |
|---|---|---|---|
| AM | 11.33 | 2.64 / 5.17 / 11.33 | 8.69 / 6.16 / 0 |
| AM+ | 12.79 | 4.98 / 6.25 / 12.79 | 7.81 / 6.54 / 0 |
| substitutes | 14.37 | 7.71 / 7.71 / 14.37 | 6.66 / 6.66 / 0 |
| two packages | 11.54 | 4.06 / 6.81 / 11.54 | 7.48 / 4.73 / 0 |

The surcharge costs bidders 2.5 (AM), 1.3 (AM+), 0 (substitutes), 2.8 (two packages) of surplus on average and moves it to the
seller (P(VCG in core) 0.17, 0.50, 1.00, 0.25). Grand ring (the grand bidder coalition, best joint report optimized, ties
to the smaller total bid; `static_ring.json`): under VCG and the surcharge the ring reaches the efficient allocation at
zero payments on 100% of instances, so its gain equals the seller's revenue at truth on every instance in all four
families (max gain minus revenue = 0). Under first-price the ring is limited by the grid: efficient at the optimum on
96% (AM), 91% (AM+), 83% (substitutes), 95% (two packages), zero payments on 88%, 52%, 30%, 82%, and the gain is
99% (AM) of the seller's revenue at truth. So the seller's revenue at truth is the upper bound on every ring's gain, attained
exactly under the two Groves-like rules; no payment rule removes it (the note's proposition).

### 1.5 The Bernheim–Whinston comparison (first-price, AM, 1,000 instances)

Leader values v(S) by the two R1 ties and the two R2 ties (identical in first-price: the complement's best replies are
essentially unique). The set of reporting profiles with an efficient allocation giving every proper S at least v(S) is
**nonempty on all 1,000 instances** and contains a zero-revenue profile on 88% of them; the mean seller revenue over the
set is 0.34 against 2.64 for VCG at truth, and mean bidder welfare 10.99 against 8.69. Its bidder-payoff vectors are within one
tick of the bidder-optimal frontier of the true-value core for all vectors on 20.8% of instances (some vector 22.8%),
mean maximum distance 3.3 ticks; only 0.6% of the vectors lie in the true-value core; leader values exceed the joint
marginal contribution on 0 of 6,000 (instance, coalition) pairs. This is a comparison of two solution concepts, not a replication: the
one-round leader-value set with only proper bidder coalitions has no seller player and no bound on the bidders' total,
so the bidders' grand ring is unconstrained and the set contains the ring outcome. The Bernheim–Whinston result
holds with the seller as a player (or with the grand coalition's deviation counted); the notion as specified here does
not reproduce it.

## 2. The ecology (Part B)

### 2.1 Tensors (committed before any dynamics, `runs/auctions/partB_static.json`)

The AM roles (P, A, B), bids 0..40, values (P, A, B) = (20, 5, 5) collusion and (20, 15, 15) threshold; 12 (rule, instance,
audit) tensors of 4 × 4 × 3 triples. Pair joint report (each member individually gaining, ties to the smaller total
bid): VCG (20, 20) in both instances; surcharge no joint gain exists (pair = truthful (5, 5) and (15, 15): payments are
pinned by P's report); first-price collusion none (truthful), first-price threshold (6, 14) (+9 and +1 individually).
Singleton shades `SH`: truthful under VCG; 5 and 5 under the surcharge threshold and first-price; P's `SH` bids 11 under
first-price collusion. No strict Nash equilibrium exists in any tensor (neutral programs everywhere); weak
equilibria: 20 (VCG collusion; they include (PAIR, PAIR, T) and (PAIR, PAIR, SH) and exclude (PAIR, PAIR, POL)), 28 (VCG
threshold), 48 (surcharge collusion: every program is truthful), 24, 16, 16.

Tremble control (committed before the tremble; prediction 12): after P commits, each pair member fails to play its half
with probability 0.05. VCG collusion: `POL` commits 40, expected payoff −0.45; `T` 0.025; `SH` 0.025. No tremble: every
P program earns 0 against the pair. VCG threshold: POL −1.45, T 0.

Constant-bid invasion (`runs/auctions/partB_static.json`, `invasion`): in VCG collusion the pair (PAIR, PAIR, T) is not
invaded by any constant (each member's best constant earns 0 against the resident 5) and both members gain +5 over truthful, so
the pair is individually rational and constant-uninvadable; against `POL` the resident earns −15 and 20 of the 41
constants invade it. P is never invaded in VCG. In first-price P's `T` is invaded by 9 constants (a constant at 11 earns 9).
In the surcharge threshold the truthful pair is invaded by 10 constants (the shades).

### 2.2 The primary cells

N = 100 per role, 64 islands, w = 0.3, no mutation, 2,000 generations, 40 runs per cell, no migration; founders paired
across rules and the audit. Every island fixed (all roles monomorphic) in every cell (no censoring), at a median of 94
generations (VCG collusion U); payoff-frozen at a median of 15. Full table: `runs/auctions/table_B_cells.csv`.
Shares are pooled over 2,560 islands per cell; the run-level standard deviation is about 0.05.

| rule | instance | prior | audit | pair | items deviate | truthful | policed | efficiency | revenue |
|---|---|---|---|---|---|---|---|---|---|
| VCG | collusion | U | open | **0.303** | 0.303 | 0.697 | **0.334** | 0.697 | 7.69 |
| VCG | collusion | U | audit | 0 | 0 | 1 | 0 | 1 | 10.0 |
| VCG | collusion | U, no POL | open | **1.000** | 1.000 | 0 | 0 | 0 | 0 |
| VCG | collusion | S | open | 0.361 | 0.361 | 0.639 | 0.257 | 0.639 | 7.0 |
| VCG | collusion | M | open | **0.930** | 0.930 | 0.070 | 0.069 | 0.070 | 2.07 |
| VCG | threshold | U | open | 0.293 | 0.293 | 0.707 | 0.340 | 1 | 7.68 |
| VCG | threshold | U | audit | 0.061 | 0.461 | 0.539 | 0 | 1 | 7.39 |
| surcharge | collusion | U | open | 0 | 0 | 1 | 0.327 | 1 | 10.0 |
| surcharge | threshold | U | open | 0 | **0.787** | 0.213 | 0.330 | 0.480 | 15.6 |
| surcharge | threshold | U | audit | 0 | 1.000 | 0 | 0 | 0.275 | 12.75 |
| first-price | collusion | U | open | 0 | 0 (P shades) | 0 | 0 | 1 | 11.0 |
| first-price | threshold | U | open | 0.705 | 1.000 | 0 | 0.998 | 0.748 | 17.9 |

(items deviate = either item's bid differs from truth with probability at least 0.5; for the pair class the two coincide.)

What drives the numbers:
* **Rings are a demography-and-drift race, not a selection result on police.** In VCG collusion P's payoff is the same
  whatever it plays (it loses either way against a pair), so `POL` is a neutral shadow in role P: it fixes in 33% of
  islands by drift (856 of 2,560, equal to the 1/3 prior share). The pair earns +5 against `T` or `SH` and −15 against
  `POL`, so it is selected against while `POL` has at least a quarter of P (5(1 − s) − 15 s = 0 at s = 1/4) and gains
  otherwise. Islands go to the pair (30%) when `POL` drifts below a quarter before the pair is removed. The
  driven-out share of islands founded with both is 0.56 (POL founder share 0.2–0.3), 0.71 (0.3–0.4), 0.87 (≥ 0.4)
  in U, and 0.06–0.15 when POL is 6% of the founders (M): the police win by founder share. Removing `POL`: the pair
  takes every island (1.000; 0.996 at N = 50, 1.000 at 200).
* **The police are never tested.** Of the 856 policed islands (VCG collusion U) 94.5% never contained a deviating pair
  after `POL` became the only P program (5.5% tested); at founding every island held both. The N sweep is flat: pair
  0.288 (N = 50), 0.303 (100), 0.284 (200), police 0.325, 0.334, 0.320; pair without `POL` 0.996, 1.000, 1.000.
* **The audit** removes the reading programs: with the audit VCG collusion is all truthful (revenue 10 against 7.69, efficiency 1
  against 0.70). In the threshold instance the audit leaves the unenforced pair (PAIRU): pair 0.061, items deviating 0.461,
  revenue 7.39 (against 7.68 without the audit: lower, not scored).
* **The surcharge** has no joint gain for any pair, so every pair class is empty and the collusion instance is a
  neutral truthful lottery (all programs truthful; police 0.327 by drift). In the threshold instance the individual
  shade `SH` dominates `T` against a truthful partner (10 against 5) and ties it against a shader, and the pair of
  shaders destroys the item bidders' win (both shade to 5, P wins): items deviate on 0.787 of islands (0.977 by label:
  `SH` fixed in A or B), efficiency falls to 0.48 (1.0 under VCG), and the audit does not help (1.000, efficiency 0.275).
  The surcharge fixes the loser ring and opens a free-riding race that ends in an inefficient equilibrium.
* **First-price** is a comparison arm. In collusion P shades to 11 (revenue 11.0, efficient, bidders earn nothing); in
  the threshold instance `POL`, a best reply to the items' intended bids, exploits shaded items and fixes in 99.8% of
  islands (the prudence analogue of the note's section 6: it is selected because it earns 9 against shaders); the
  unenforced pair holds 0.705.
* **Migration** (mN = 1, N = 100, 4,000 generations, secondary): the metapopulation chooses globally. VCG collusion pair 0.568
  (per run: 10 of 40 runs at 0, 15 at 0.95 or above, the rest between), police 0.356, and the police are tested on 99%
  of policed islands; the VCG threshold 0.593; surcharge collusion truthful (all neutral); surcharge threshold items deviating 0.688,
  efficiency 0.47; first-price threshold pair and police both 1.000; without `POL` the pair takes everything. Migration
  makes the ring a coin flip per run (it is a global winner when `POL` is not).

## 3. Deviations from the spec, each stated

1. **T-weak reading.** The spec defines one best-reply graph ("strict improvements only") and two ties over the closure's
   equilibria. Taken literally, an indifferent loser never moves, the closure from the truthful profile has no spite
   equilibrium and T-weak equals T-strict. I read "spite counts" as the purpose and let the T-weak graph move to *any*
   best reply (lateral moves included), keeping the strict graph for T-strict. The literal reading is reported as the
   extra variant `R1_weak_literal` (identical to T-strict everywhere). Predictions 3 and 4 are scored on my reading.
2. **Report grid cap and the wide sensitivity.** Reports on 0..2G for all bidders let a pair overbid to the cap, out of
   reach of any responder. Added: deviators on 0..2G with responders on 0..4G (AM only), reported beside the spec-grid
   results; the verdicts are scored on the spec grid and both are given.
3. **Sample size.** AM is exhaustive (1,000); AM+, substitutes and two packages on a fixed-seed subsample of 3,000 of
   10,000 (the spec allows 3,000 for AM+; I applied it to the other two 4-bidder families). Leader values and the
   Bernheim–Whinston comparison are computed on AM only. The wide sensitivity is AM only.
4. **Deviations exclude the truthful report** (a coalition reporting truthfully has not deviated); leader values include it.
5. **T-strict ties**: among equilibria at the same L1 distance, the lexicographically smallest report vector.
6. **Unresolved R1 instances**: none occurred (0 in every family, rule and variant, first-price included).
7. **Prediction 6 convention**: all payoff vectors of the set within one tick (the some-vector version also reported);
   distance is L-infinity to the nearest Pareto-maximal *integer* point of the true-value core.
8. **Prediction 11, prior M**: item priors equal U; `POL` mass 1/16 = (1/4)², `T` and `SH` 15/32 each. Prior S: items 1/2 on `T`,
   1/6 on the rest; P 1/2 on `T`, 1/4 on `POL` and `SH`. The audit maps founders (PAIR → T, POL → T) so founders are paired
   across rules and the audit. The no-police cells put `POL`'s mass uniformly on `T` and `SH`.
9. **The island kernel is new.** `fixed_role_chicken.sim_two_pop` is two-population with pairwise payoffs, so a
   three-population numba kernel was written (`auction_islands.sim3`), reproducing its conventions: one island and
   one role per event, child sampled from the own island or (with probability m) another, fitness exp(w · expected payoff),
   uniform victim, 3NI events per generation, ε = 0, no mutation. "Random role triples per encounter" is implemented
   as the expectation over independent draws from the two other roles' island populations. No existing file in `src/` was edited.
10. **Fixation, not payoff-freezing, ends a run without migration.** The kernel stops when every role of every island is
    monomorphic ("fixed"); a payoff-frozen island keeps drifting among payoff-equivalent programs, so class shares
    are shares at fixation (including the neutral drift of P). Policed = `POL` the only P program. With migration the run
    stops at global payoff-freezing or 4,000 generations (censoring there = not payoff-frozen; `policed` = `POL`
    above half of P). The first pass of the migration cells reported censoring by fixation; it was corrected and the
    migration cells rerun.
11. **Tested**: after `POL` became the only P program, any generation boundary with `PAIR` in both item roles or
    `PAIRU` in both; the founding-state exposure is reported separately (1.000: every island held both at founding).
12. **Scoring of prediction 11**: a conjunction; the first part holds (pair islands rise 3.07×) and the second fails (7%), scored partial.
13. **Mixed coalitions dominate the Part A table** (§1.2), so the truth-robust fractions are near 0 in three of four
    families; the tables report the robust fraction ignoring mixed coalitions in addition to the spec's.
14. **The `batch_*.done` markers and `log_*.txt` files** in `runs/auctions/` are process logs; `tmp_*.npz` is gitignored.
