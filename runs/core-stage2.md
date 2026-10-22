# Verdicts: rediscovering the core, stage 2, 2026-10-21

Spec `specs/2026-10-21-core-stage2.md`; predictions `predictions/2026-10-21-core-stage2.md` (committed before any code, with
the scoring conventions fixed there); notes `notes/core-stage2.md` (§1 hand predictions, §2 deviations); code
`src/core_stage2.py`, `src/core_stage2_run.py`, `src/core_stage2_report.py`; tests `tests/test_core_stage2.py` (18 pass);
outputs `runs/core_stage2/` (`statics.json`, `static_*.csv.gz`, `cell_*.json`, `rows_*.csv.gz`, `tables.json`,
`table_cells.csv`, `report_digest.txt`). 98 cells, 40 runs each (3,920 runs), N = 100 per role unless stated, 64 islands,
w = 0.3, 5,000 generations (rain 20,000), a run stops early only when every island is frozen for good (no migration, no arrivals left). All
island numbers are finite-(N, I, horizon) lottery statistics at ε = 0 or stated re-injection, never π. Fractions are pooled
over (run, island) pairs. "core" in a table is the island-mean core fraction (stage 1's definition), "core_enc" the
encounter-level core probability (the spec's primary); at ε = 0 without migration every island is fixed at the horizon in all
three roles (`fixed_all` = 1.00), so the two coincide there to within 0.001.

## Scorecard

| # | Prediction | Verdict | Number |
|---|---|---|---|
| 1 | Statics: complementary pairs facing `TX(v_P)` have efficient revenue within two ticks of the core minimum; both orders agree | **held** | efficient complementary revenue offsets above the core minimum: threshold 1, 1, 2, 1, 1; asymmetric 2, 1, 1 (two exact ties at offset 0); skew 2, 1, 2, 1, 2 (one tie at 0); none more than 2 ticks off; 0 order differences over 3 × 202,500 triples, python against numba, both orders |
| 2 | ε = 0, threshold, no-overbid, m = 0.5: core 0.2–0.6; threat shift ≥ 3 ticks; matched-constants shift at most half | **partial (the headline claims failed)** | core_enc 0.082 (run sd 0.033), below the 0.1 falsifier; shift +2.61 (end threat 12.86 against a prior mean 10.25), below the claimed 3 and above the falsifier's 1; matched constants shift +0.83 = 0.32 of TX's, so that clause held |
| 3 | The shadow: on islands where followers fix and their bids sum above P's threat, `TX` wins under 1% after fixation | **held** | 1,764 qualifying islands of 2,560; `TX` wins 0.0000 of end encounters; time-averaged after the item roles fixed 1.6·10⁻⁵ (before: 0.145); 98% of the fixed follower pairs are δ-complementary |
| 4 | Rain gives ≥ 0.8 of threshold islands in the core; safe-follower rain below 0.6 | **failed** | full rain core 0.117 (core_enc 0.144) at m = 0.5, 0.222 at m = 0.2, 0.205 unrestricted; stage 1's constants-only rain reproduced on these seeds at 0.464. The safe-follower rain is 0.102, not below the full rain by enough to matter (the falsifier "rain below 0.6" fired) |
| 4c-g | Counter-prediction (gemini-4-argon): follower-only rain stays ≥ 0.6 | **failed** | 0.086 (core_enc 0.105) |
| 4c-s | Counter-prediction (gpt-6.1-sol): P-only rain at least item-only rain minus 0.05 | **partial** | m = 0.5: P-only 0.098 against items-only 0.064, supported; m = 0.2: 0.099 against 0.191, contradicted |
| 5 | Every cell's outcome identical under the two resolution orders | **held** | 0 differences in the statics (all triples, 3 instances); the first three runs of all 98 cells reproduced exactly (final counts) under the reverse-order tensor |
| 6 | Skew, modal split under migration is not the Vickrey-nearest one | **indeterminate as registered (partial)** | under migration there are 0 islands in the core with followers fixed, in all four skew migration cells, so the registered quantity does not exist; in the ε = 0 skew cell (post hoc), 183 core islands: A pays 11 (equal surplus) on 52%, 10 (Vickrey-nearest) on 25%, 7 or 8 on 8% |
| 7 | Bluffs: among tested `TX` at most 10% have t above v_P (ε = 0 primary cell) | **held** (permissive "tested"; fails under rain) | ε = 0: 1.7% (m = 0.5), 9.3% (m = 0.2); annealed tail 2.2% (m = 0.5), 10.8% and 10.2% (m = 0.2, threshold and asymmetric); untested bluffs 0 at ε = 0. Under rain the tested bluff share is 13–32% (reported, not the registered cell) |

The result in one line: **the certified threat fixes stage 1's artefact when the item roles do not follow (core_enc 0.65 at
ε = 0, 0.70 under rain, 0.98 under migration), and followers undo it (0.08, 0.14, 0.00)**. Followers fix the item roles in
about 20 generations, the threat is never tested again, and it freezes at the level the scramble left.

## 1. Statics (committed before any island cell; `statics.json`)

Exhaustive over t = 1..cap, δ_A, δ_B ∈ {0.1..0.9} (3,240 triples per instance and bid space), the bids resolved by the
numba resolver and by a pure-python source evaluator in both orders, seller outcomes by `core_auction.outcome`.
* `TX(v_P)` against the nine complementary pairs (δ_A + δ_B = 1), efficient outcomes (no bid space difference):
  * threshold (20, 15, 15), minimum revenue 20: T = 21, 21, 22, 21, 21 for (0.3, 0.7), (0.4, 0.6), (0.5, 0.5), (0.6, 0.4), (0.7, 0.3);
    (0.1, 0.9), (0.2, 0.8) and the mirrors are `TX` wins (T = 17, 19). Matches the hand derivation (notes §1.2).
  * asymmetric (20, 16, 12): efficient at T = 22, 21, 21; (0.4, 0.6) and (0.8, 0.2) are exact ties at T = 20 (`TX` wins half);
    the rest `TX` wins.
  * skew (14, 16, 8), minimum revenue 14: efficient at T = 16, 15, 16, 15, 16; (0.4, 0.6) a tie at T = 14; the rest `TX` wins.
    The maximum offset is exactly the two-tick limit.
* Over all t, 60% (threshold, no-overbid) of (t, δ_A, δ_B) triples are item wins and 31% `TX` wins, 9% ties; the unrestricted
  space has more `TX` wins (56%) because t above 20 is a bluff against any pair. `TX(t)` weakly dominates the constant t in
  P's payoff against every follower pair (mean advantage 0.94, minimum 0.0, maximum 15 in the threshold no-overbid grid).
* Order check: python in the two orders, and numba in the two orders, agree on all 202,500 triples per instance; the payoff,
  statistic and bid tensors are bit-identical across orders; the maximum call depth is 3 (item, certificate read, TX).
* Skew static map at t = 14 (R = 15): A's follower bids 2, 3, 5, 6, 8, 9, 11, 12, 14 for δ_A = 0.1..0.9 and B's the same capped
  at 8 (2, 3, 5, 6, 8, 8, 8, 8, 8). Of the 81 pairs, 35 are item wins outright, 9 ties; **no pair reproduces the Vickrey-nearest
  payments (10, 4) or the equal-payment point (7, 7)** (B has no bid 4, and A no bid 7), and the equal-surplus point (11, 3) occurs
  only at a tie. Prior-weighted split distribution before selection (A's payment among the 35 outright wins): 8 (5 pairs), 9 (6), 11 (7), 12 (8),
  14 (9); exact reference classes 0 of 35, mean L1 distance to the nearest reference 4.4. Over t uniform on 1..14: 690 outright wins, exact
  matches 4 (Vickrey-nearest), 1 (equal surplus), 7 (equal payment), mean distance 6.0. So gemini-4-argon's capped-B
  degeneracy is real in the static map (B at 8 in 45 of 81 pairs) and selection must be read against it.

## 2. ε = 0 (prediction 2, 3 and the controls)

**Primary cell (threshold, no-overbid, m = 0.5; 2,560 islands).**

| quantity | value |
|---|---|
| in the core (encounter-level / island-mean) | 0.082 / 0.082 (run sd 0.033) |
| eroded (revenue more than one tick below 20) | 0.875; mean revenue 14.05; efficiency 0.995 |
| P: `TX` share of the population | 0.74 (the rest constants) |
| items: follower share (each role) | 0.97 |
| P's threat: end mean 12.86 against prior 10.25 | shift +2.61; the fixed `TX(t)` have mean t 13.28, sd 3.84, quartiles 11/14/16 |
| item roles fixed on followers | median generation 20 (all islands); all three roles fixed median generation 81 |
| fixed follower pairs complementary (δ_A + δ_B = 1) | 1,727 of 1,765 (98%); T = R in 1,477, R + 1 in 249 |
| `TX` win probability before / after the item roles fix | 0.143 / 0.005 (qualifying islands: 0.145 / 0.00002) |
| TX payoff minus the matched constant's, per encounter | 1.16 at generation 0, 0.04 at 10, 0.002 at 50 |

* On the fixed follower pairs, the core is reached **iff the threat is high**: core_enc by the fixed `TX(t)` is 0.000 for every
  t ≤ 16, 0.034 at t = 17, 0.42 at t = 18, 0.986 at t = 19, 1.000 at t = 20, and only 13.5% of fixed `TX` have t ≥ 18 (7% have
  t ≥ 19). The followers price the pair at R = t + 1 whatever t is, so what decides the core is the threat's level.
* Same with m = 0.2: core 0.209, shift +5.60 (fixed `TX` mean t 15.8; the follower share is 0.74). Asymmetric 0.066 (shift
  +3.05), skew 0.090 (+1.61); unrestricted 0.051 (shift −9.08 against a prior mean 20.25: the unrestricted space selects the
  threat down and kills the bluffs). The annealed tail (A = 3) changes nothing: 0.080 (primary), 0.047–0.211 across cells.
* Matched constants (control vi): core 0.015, shift +0.83 (threshold no-overbid), 0.013 (+1.22) asymmetric, 0.048 (+0.94) skew,
  0.031 at m = 0.2: the same followers with constants in P do far worse than `TX`, and select the threat much less. The `TX`
  advantage is the exploitation payoff in the scramble (1.16 per encounter at generation 0), which is gone by generation 50.
* N panel (control vii): core_enc 0.105 / 0.082 / 0.066 at N = 50 / 100 / 200 (shift +2.72 / +2.61 / +2.54); unrestricted
  0.063 / 0.051 / 0.033. The shadow holds at every N.
* **Control (i), `TX` without followers (items constants only): core_enc 0.651 (island-mean 0.623), threat 18.59 (shift
  +8.34), `TX` wins 11% of end encounters.** Asymmetric 0.548, skew 0.679. This is the stage-1 artefact fixed: stage 1's
  constants-only ε = 0 cell had 0.010. The threat stays tested (at ties) because the item constants are underbidders it
  exploits and the pair that survives sits at T = t.
* **Control (ii), followers without `TX` (P constants): core 0.021** (asymmetric 0.010, skew 0.053).
* Follower mass in the item roles (post hoc, `x_fol*`; `TX` m = 0.5, threshold, no-overbid, ε = 0): core_enc 0.605 / 0.559 /
  0.487 / 0.395 / 0.251 at follower mass 0.01 / 0.02 / 0.05 / 0.10 / 0.20 (0.082 at 0.5); the followers' end share is 0.07 /
  0.12 / 0.28 / 0.47 / 0.74 (0.97 at 0.5). Followers are not neutral: they spread when seeded in numbers.

**Prediction 3 elsewhere.** `TX` wins 0.0000 of end encounters on qualifying islands in every ε = 0 and annealed cell
(threshold, asymmetric, skew; both spaces; m = 0.5 and 0.2), 431–1,956 qualifying islands per cell. Among fixed follower islands
that are not δ-complementary (all of them, not only those with T > t), `TX` is still tested in some cells: its win rate is 0.0 in
the threshold no-overbid cells (38 and 56 islands) and up to 0.066 in the asymmetric unrestricted m = 0.2 cell (98 islands), as the
spec's conditioning anticipated.

## 3. Rain, annealed tail and migration (prediction 4 and controls)

Island-mean core fraction (core_enc in brackets); rain is εN = 0.05 per role per island per generation over 20,000
generations (about 2,870 programs replaced per island), migration is mN = 1.

| cell (threshold, no-overbid, m = 0.5 unless stated) | rain | migration |
|---|---|---|
| `TX` + followers (primary) | 0.117 (0.144) | **0.000 (0.000)** |
| m = 0.2 | 0.222 (0.266) | 0.000 |
| unrestricted | 0.205 (0.238) | 0.000 |
| asymmetric / skew | 0.106 / 0.153 | 0.000 / 0.000 |
| (i) `TX` without followers | **0.633 (0.699)** | **0.701 (0.983)** |
| (ii) followers without `TX` | 0.102 (0.128) | 0.000 |
| (iii) constants only (stage 1 on these seeds) | 0.464 (0.517) | (stage 1: 0.454; unrestricted 0.183) |
| (iv) follower-only rain | 0.086 (0.105) | |
| (iv″) safe-follower rain (δ ≥ 0.5) | 0.102 (0.117) | |
| (iv′) P-only rain / item-only rain | 0.098 / 0.064 | |
| (vi) matched constants | 0.103 (0.129) | |
| follower mass 0.01 / 0.05 / 0.10 / 0.20 (post hoc) | 0.621 / 0.541 / 0.427 / 0.259 | |

* Control (iii) reproduces stage 1's constants-only rain (0.464 against 0.45–0.49), a check on the scheduled-arrival kernel.
* At m = 0.2 the controls are: (iv) 0.084, (iv″) 0.109, (iv′) P-only 0.099, item-only 0.191.
* Asymmetric (iv)/(iv″) 0.081 / 0.101, skew 0.126 / 0.152, against the full rain 0.106 / 0.153: the sucker-depleted arms are not below the
  full rain by more than 0.03 in any instance, and the safe-follower rain is above the follower-only rain in every instance.
* The threat under rain drifts toward the prior (12.9 at generation 100, 11.8 at generation 18,500; ε = 0: 12.86), because a frozen
  threat is neutral and rain replaces programs at random. Revenue is 12.8.
* Under migration the followers drive the threat down, not up (end 6.13 in the primary cell, revenue 7.2): even (ii) is at 0.000 and
  the `TX` + follower cells are at 0.000 in all 12 primary migration cells (both spaces, three instances, two masses);
  `TX` without followers reaches 0.98 at the encounter level (0.70 island-mean, a 0.28 gap: polymorphic islands).
* Encounter-level against island-mean core fractions: the gap is at most 0.045 in the ε = 0 cells, 0.007 under the annealed tail,
  0.073 under rain (0.034 on average) and 0.28 in (i)/migration (0.02 on average over the migration cells); the island mean is the
  more conservative.

## 4. The split (prediction 6, reported)

* Registered quantity (skew, migration, core islands with followers fixed in both item roles): none exist (all four skew
  migration cells have 0 core islands; the 337–442 fixed-follower islands with item wins there pay A 5–8 on over 90% of them, revenue
  well below 14).
* ε = 0, skew, no-overbid, m = 0.5, islands in the core with followers fixed (183): A pays 11 on 95 (52%), 10 on 46 (25%), 8 on
  13, 12 on 18; exact references: equal surplus 71, Vickrey-nearest 46, equal payment 0, other 66. m = 0.2 (133 core islands): A pays 10
  on 45, 11 on 44, equal surplus 30, Vickrey-nearest 45. Unrestricted m = 0.5 (169): Vickrey-nearest 35, equal surplus 26, equal
  payment 5, other 103. Rain, skew no-overbid m = 0.5 (182): equal surplus 35, Vickrey-nearest 34.
* A's modal payment among the core islands is 11 (equal surplus) in 4 of the 6 skew ε = 0 and rain cells listed, 10 (Vickrey-nearest)
  in the m = 0.2 cell (45 against 44) and 13 in the unrestricted rain cell (116 of 651; there the core is reached at revenue 15–16 by
  higher splits). Exact reference classes are a minority everywhere (the follower grid rarely hits them: 'other' 36–85%). Selection moves
  the split away from the pre-selection distribution (A pays 14 on the most static pairs, 11 or 10 after selection); the capped-B
  degeneracy (A pays 7–8) accounts for 8% of the core islands at ε = 0.

## 5. Bluffs (prediction 7, unrestricted)

At the horizon essentially every surviving `TX` has been tested at a generation boundary (the founding mixture tests all of them at
generation 0: `tested_pop` equals `tx_pop` in all but the annealed cells, where 0.2% are untested), and 1.7% of `TX` population
share has t above 20 at m = 0.5 (9.3% at m = 0.2, 2.2% / 10.8% under the annealed tail, 0.0% under migration). Untested bluffs: 0
at ε = 0 and 100 programs in the whole annealed skew cell. **Under rain the bluffs are not depleted**: the tested bluff share is 0.16 /
0.25 (threshold m = 0.5 / 0.2), 0.13 / 0.29 (asymmetric), 0.23 / 0.32 (skew), with 20–191 untested bluff programs per cell: arrivals
replace the selected population faster than the loss from a tested bluff removes them, and a bluff whose threat exceeds the followers'
capped total is not tested. The registered claim is the ε = 0 one. The "tested at least once" condition is permissive; the content is
that bluffs are depleted from the founding mixture's 50% (t above 20 is half of the unrestricted `TX` prior) to under 2.5% at m = 0.5.

## 6. What keeps the certified threat honest

As far as the controls identify it:
* **The policy, against non-following item programs.** `TX(t)` pays T + 1, not t, when it wins, so a high honest threat is not
  penalised in the scramble (payoff advantage over the matched constant 1.4 per encounter at generation 0); with constant items, the
  threat rises to 18.6 and the core is held at 0.65 (ε = 0), 0.63 (rain) and 0.98 encounter-level (migration), against 0.01 / 0.46 /
  0.45 for constants alone (stage 1, no-overbid).
* **A supply of item programs that do not follow, in numbers.** The threat stays tested only against item programs that can be
  exploited. The follower-mass sweep is monotone: core_enc 0.605 → 0.082 as the follower prior mass goes from 0.01 to 0.5. Followers
  spread by selection once seeded in numbers (the end share is 0.97 at m = 0.5), fix the item roles in about 20 generations, and
  after that `TX` wins 0.005 of encounters.
* **Not the rain's sucker supply, as built.** Rain with constants (suckers) arriving beside the followers gives 0.117; follower-only
  rain 0.086; safe-follower rain 0.102; P-only rain 0.098; item-only rain 0.064. The differences are within 0.05 and not ordered
  as predicted. A rare constant sucker arriving into an all-follower item role is a neutral program that followers read and
  accommodate, and it cannot restore testing alone.
* A frozen untested threat is neutral: its level is set by the scramble (mean t 13.3 at ε = 0, 11.5 under rain) and moves toward the
  prior under rain. With migration and followers it falls (6.1).

## Not done

* The unrestricted-space bluff condition is scored on a permissive "tested" definition (tested at any boundary); a stricter one
  (tested after the item roles fix) was not run.
* The ε→0 chain, a follower rule that conditions on whether the threat has been tested, and the Pareto-nearest follower were not
  run; the follower rule "bid enough to beat the certified threat" hard-codes the core constraint's arithmetic (spec).
* Rain at other rates, N-dependence under rain and migration, and mN other than 1.
