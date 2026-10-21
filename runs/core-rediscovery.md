# Verdicts: rediscovering the core, 2026-10-21

Spec `specs/2026-10-21-core-rediscovery.md`; predictions `predictions/2026-10-21-core-rediscovery.md` (committed before any code);
notes `notes/core-rediscovery.md` (§1 hand predictions, §2 deviations); code `src/core_auction*.py`, tests
`tests/test_core_auction.py` (22 pass); outputs `runs/core_auction/` (`statics.json`, `cell_*.json`, `rows_*.csv.gz`,
`tables.json`, `table_cells.csv`, `split_by_run.json`, `order_static.json`, `report_digest.txt`). All island numbers are ε = 0 (or
stated re-injection) seed-lottery statistics at finite (N = 100, I = 64, horizon 5,000 or 20,000 generations, 40 runs, w = 0.3),
never π. Fractions are pooled over 2,560 (run, island) pairs, with the run-level standard deviation where stated. At ε = 0
without migration every island is fixed at the horizon in every cell (`fixed` = 1.00), so there is no censoring there.

## Scorecard

| # | Prediction | Verdict | Number |
|---|---|---|---|
| 1 | Statics: efficient Nash revenues cover the whole core and nothing below (unrestricted); within two ticks of the minimum (no-overbid) | **partial** | no-overbid held (threshold 20..21, asymmetric 20..21); unrestricted threshold covers 20..28, not 29–30; the falsifier "an efficient equilibrium below the core" fires in the collusion instance (one equilibrium at revenue 9 against a minimum of 10, in both spaces) |
| 2 | Erosion ≥ 50% at ε = 0 (threshold, both spaces); the rest mostly inside the core, spread over it | **partial** | eroded 0.963 (unrestricted), 0.904 (no-overbid) held; of the non-eroded 0.037 and 0.096, in the core 0.0023 and 0.0098 (6% and 10%), the rest one tick below it (0.035, 0.087): second clause failed |
| 3 | Efficient allocation in ≥ 75% of end encounters (threshold, collusion); erosion mostly a transfer | **held** (second clause partial) | efficiency 0.792 / 0.872 (threshold), 0.875 / 0.866 (collusion); transfer share of the revenue shortfall 0.52 / 0.62 (threshold, held), 0.48 / 0.27 (collusion, not "mostly") |
| 4 | Annealed tail A = 3: ≥ 60% of islands end in the core | **failed** | 0.024 (unrestricted), 0.045 (no-overbid); time-averages 0.022 / 0.042; A = 1: 0.009 / 0.027. No transient restoration either (the series is flat from about 500 generations) |
| 5 | Responder, m = 0.2, ε = 0: ≥ 50% of islands in the core (counter-prediction: > 50% in the core but `PRU` holds P on < 40% of them) | **failed**, both | core 0.025 (m = 0.2), 0.020 (m = 0.05); 64 core islands, `PRU` a majority of P on none of them (P is 8% `PRU` at the end). Order-dependent: with the order B, A, P the core fraction is 0.711 and `PRU` holds P on every island; the order-free variant gives 0.023 |
| 6 | Split not Vickrey-nearest: asymmetric, at VN within a factor 2 of the grid baseline | **failed** | baseline 5/17 = 0.294 (bound 0.588); 40-run cells 1/4 and 8/8 edge islands at VN (9 of 12); 400-run cells 17/22 = 0.77 (unrestricted) and 69/80 = 0.86 (no-overbid); migration 856 of 864 and 64 of 64; but see §4: Vickrey-nearest, equal-surplus and the middle of the edge coincide in the spec's instances |
| 7 | Outbidder injection: establishes in ≥ 80% of eroded islands and restores the core | **partial** | establishment 0.919 / 0.863 (threshold), 0.944 / 0.876 (asymmetric) held; restoration 0.000 of 9,744 eroded islands (the outbidder wins: efficiency falls from about 0.8 to 0.03–0.10, revenue stays 16–18) |

Reported without a prediction: the collusion instance against the threshold instance (§3), migration (§5), the N sweep (§6).

## 1. Statics (committed before any island cell; `statics.json`, `nash_*.csv.gz`)

Pure Nash equilibria of the constant-bid game (expected payoffs under the seller's revenue lottery), all checked against every
true-value core inequality:

| instance | space | Nash | efficient | in the core | revenue of efficient (min..max) | below the core |
|---|---|---|---|---|---|---|
| threshold (20, 15, 15) | unrestricted | 45 | 45 | 45 | 20..28 (9, 8, …, 1 per tick) | 0 |
| threshold | no-overbid | 17 | 17 | 17 | 20..21 | 0 |
| asymmetric (20, 16, 12) | unrestricted | 28 | 28 | 28 | 20..26 | 0 |
| asymmetric | no-overbid | 13 | 13 | 13 | 20..21 | 0 |
| collusion (20, 5, 5) | unrestricted | 66 | 66 | 65 | 9..19 | 1 (revenue 9) |
| collusion | no-overbid | 4 | 4 | 3 | 9..11 | 1 (revenue 9) |

Every efficient equilibrium in the threshold and asymmetric instances has the loser at one tick below the winners' total
(b_P = b_A + b_B − 1) and winners at most one tick below their values; so Nash spans the interior of the core (every split of the
total, every total from the minimum to about the top two ticks) and not only its bidder-optimal edge, as predicted, and the top
two ticks of the core are not equilibria because a winner at its value can tie for 0.5. In the collusion instance the losers can
only win jointly, so the single deviations that would restore the core are not available and an equilibrium sits one tick below
it. The hand predictions of notes §1.1–1.3 matched these tables exactly. Grid points near the Vickrey-nearest point (the split
baseline): threshold 5/21 = 0.238, asymmetric 5/17 = 0.294 (both spaces; an overbid cannot be in the core).

## 2. Erosion, efficiency, re-injection, responder, injection (primary and companion cells)

**Primary cells** (constants, U prior, ε = 0, 40 runs; `table_cells.csv`):

| cell | eroded | in core | at min-revenue edge | efficiency | mean revenue (min) |
|---|---|---|---|---|---|
| threshold, unrestricted | 0.963 (sd 0.024) | 0.002 | 0.002 | 0.792 | 15.9 (20) |
| threshold, no-overbid | 0.904 (0.028) | 0.010 | 0.010 | 0.872 | 17.0 (20) |
| asymmetric, unrestricted | 0.984 | 0.002 | 0.002 | 0.775 | 15.5 (20) |
| asymmetric, no-overbid | 0.956 | 0.003 | 0.003 | 0.847 | 16.7 (20) |
| collusion, unrestricted | 0.718 (0.067) | 0.096 | 0.093 | 0.875 | 7.75 (10) |
| collusion, no-overbid | 0.527 (0.072) | 0.103 | 0.102 | 0.866 | 8.42 (10) |

Ten-times-the-runs cells (post hoc, 400 runs): threshold 0.967 / 0.914 eroded, asymmetric 0.986 / 0.954, in the core 0.004 / 0.008
and 0.001 / 0.003.

* **Where the loser settles.** The losing bid is not a free threat at the end and not a drift outcome: P's median final bid is
  16 (10–90%: 12..17, unrestricted; 14..18 no-overbid), one tick below the winners' total (median P − total = −1 in both spaces; P is
  below the winners' total on 72% / 82% of islands, at or above it on the rest). Mechanism (hand computation, notes): against the
  uniform founding mixture of winners, P's best bid is 13 (expected payoff 2.68 against 0.72 at bid 19 and 0 at 20), so selection acts
  on P while the winners are still diverse and removes the high bids; the winners then ratchet to just above P's surviving maximum,
  and at ε = 0 the profitable outbid (a P bid at the winners' total plus one) has no founder left. The founding sets were not
  short of high bids: every island's founding set contained P bids at the top of the range (mean highest founding P bid 39.9
  unrestricted, 19.99 no-overbid; lowest about 0), so the erosion is not missing founders.
* **Time to first erosion.** In the no-overbid space every island is already eroded at generation 0 (the uniform founding mixture
  earns 16.6 against a minimum of 20), so the statistic is trivial there; in the unrestricted space founding revenue is 41.8 (random
  overbids win) and islands erode within a median of 2 generations after the start.
* **Re-injection** (`reinj` cells, threshold; extras on the other instances in `table_cells.csv`):

  | arm | unrestricted: in core / eroded | no-overbid: in core / eroded |
  |---|---|---|
  | ε = 0 | 0.002 / 0.963 | 0.010 / 0.904 |
  | annealed A = 1 | 0.009 / 0.957 | 0.027 / 0.878 |
  | annealed A = 3 | 0.024 / 0.929 | 0.045 / 0.834 |
  | rain εN = 0.05, 20,000 generations | 0.452 / 0.254 | 0.488 / 0.225 |

  The annealed tail's arrivals come after the islands have fixed (onset 200); the single P outbidder that arrives and wins wins
  inefficiently and the winners cannot answer without a matching arrival of their own. Constant rain restores slowly and
  partially: the in-core fraction rises 0.02 → 0.30 → 0.45 at 100, 2,000, 20,000 generations (unrestricted), revenue to 19.0–19.2,
  efficiency 0.92–0.95, and still 23–25% eroded; 61–81% of rain islands are fixed at the horizon, so this is not an absorbed state.
  On the responder prior (extra) the rain arm reaches 0.25 only (m = 0.2).
* **The responder** (1b, no-overbid, order P, A, B):

  | cell | in core | eroded | efficiency | `PRU` share of P at the end |
  |---|---|---|---|---|
  | threshold m = 0.05 | 0.020 | 0.786 | 0.808 | 0.098 |
  | threshold m = 0.2 | 0.025 | 0.780 | 0.761 | 0.083 |
  | asymmetric m = 0.05 / 0.2 | 0.015 / 0.025 | 0.835 / 0.807 | 0.774 / 0.757 | |
  | threshold m = 0.2, order B, A, P | **0.711** | 0.259 | 0.794 | 1.000 |
  | asymmetric m = 0.2, order B, A, P | 0.575 | 0.384 | 0.705 | 1.000 |
  | threshold m = 0.2, order-free (simultaneous reply to the defaults) | 0.023 | 0.927 | 0.721 | |

  The order is not innocuous. Triples with at most one responder resolve identically in both orders; triples with two responders
  differ in 85–86% of cases and cycle in 65%, and with three in 99% (`order_static.json`). The last mover wins those encounters
  (mean payoff of the roles in two-responder triples, order P, A, B: P 0.2, A 7.5, B 7.2; order B, A, P: P 3.5, A 3.5, B 3.9; three
  responders: P 0.03 against 6.7 under the reversed order), so the order decides which `PRU` is selected: under P, A, B the
  winners' responders take the last-mover advantage and `PRU` is selected against in P; under B, A, P a responding loser moves last,
  punishes underbidding winners by outbidding them, and fixes in P on every island, pulling the winners up to the core. The
  order-free rule is level-1 (replies to the defaults) and does not restore the core. So the prudent loser restores the core only
  when it is evaluated after the winners it reads; that is an assumption about the evaluator, not about the program, and a
  mutually reading pair of responders has no fixed-point selection (the regress of milestone 3 again).
* **Outbidder injection** (eroded end states of the four 1a item-winner cells; control: the same islands continued without
  injection): establishment (≥ half of P at the end; all establishing ones fixed) 0.919 / 0.863 (threshold unrestricted /
  no-overbid), 0.944 / 0.876 (asymmetric); in the core after 5,000 more generations: 0 of 9,744 eroded islands, as in the
  control (0 of 9,744, all still eroded). The injected outbidder wins the auction at the winners' total plus one: efficiency drops to
  0.03–0.10 (control 0.78–0.88) and revenue rises only to 16.1–17.5 (control 15.4–16.8), which is still below the core. A and B are
  fixed constants that cannot raise their bids, so the core needs a second, coordinated arrival; this is the double lottery that the
  rain arm eventually draws.

## 3. Collusion instance against the threshold instance (reported without a prediction)

Two independent threats erode less: eroded 0.72 / 0.53 against 0.96 / 0.90, in the core 0.10 against ≤ 0.01, efficiency about the
same (0.87), mean revenue 7.8 / 8.4 against a minimum of 10, and with an equilibrium at revenue 9 even the static benchmark is a
tick below the core. P pays the losers' total bid plus one tick, and the losers' bids settle low (the 10–90% range of the losing
roles' median bids is 1..4 unrestricted, 1..5 no-overbid, against a value of 5), since a loser's bid is neutral as long as it loses. The instances differ in more than the number of threats (one winner against two, and the losers' joint
deviation), so no attribution to the number of threats is made.

## 4. The split (prediction 6) and the skew control

In the spec's instances the Vickrey-nearest split, the equal-surplus split (Nash product) and the middle of the bidder-optimal edge
all coincide (the winners' VCG surpluses are both w(N) − v_P in this family when v_P exceeds both item values), so the statistic
cannot separate them. What the lottery does is concentrate on that point. At ε = 0 (400 runs) the winners' pA on the edge is
bell-shaped around the Vickrey-nearest value (asymmetric no-overbid: 10:6, 11:27, 12:30, 13:13, 14:4; threshold 0.82 at VN against a
0.238 baseline); under per-role migration every run that reaches the core lands on it (threshold 20 of 20 runs in the no-overbid
space and 8 of 8 unrestricted; asymmetric 15 of 15 and 1 of 1; 5,000 generations, 40 runs, mN = 1).

A post-hoc `skew` instance (v_P, v_A, v_B) = (14, 16, 8) separates the candidates: Vickrey-nearest payments (10, 4), equal surplus
(11, 3), equal payments (7, 7), edge middle 9.5. Under migration the core-reaching runs land on **Vickrey-nearest in 29 of 40
runs (no-overbid; 35 of 39 unrestricted) and on equal-surplus in the rest (11 of 40; 4 of 39), never on equal payments**; at ε =
0 the edge islands are 0.42 at (10, 4) and 0.36 at (11, 3) (no-overbid; mean pA 10.4); under rain mean pA 10.6. My
pre-registered guess for skew (equal surplus, probability 0.55) failed; neither pure candidate explains the run-level split, and
the mechanism is not established. The responder arms (order P, A, B) put the split at the last mover's corner (asymmetric
m = 0.2: pA = 14 on 46 of 63 core-edge islands, 0.06 at VN; skew pA 13–14), so the split under `PRU` is an evaluator artefact.

Prediction 6 is scored failed on the spec instance by its stated falsifier; read it with this paragraph: the run found a
strong, instance-wide concentration on the Vickrey-nearest point that the statics do not have (Nash puts every edge split on the
same footing), and the control shows it is not simply the middle of the edge or the equal-surplus point.

## 5. Migration (reported without a prediction; mN = 1, per-role, 5,000 generations)

Migration restores most of the core where nothing else at ε = 0 does and ends one tick short of it: threshold in the core 0.18
(unrestricted) / 0.45 (no-overbid), eroded 0.27 / 0.12, efficiency 0.995, revenue 19.1 / 19.5 against 20; asymmetric 0.025 / 0.34,
revenue 18.7 / 19.4; collusion 0.06 / 0.11, eroded 0.000 (revenue 9.1 against 10, one tick short, which is not "eroded" under the
more-than-one-tick rule); responder prior (threshold m = 0.2, order P, A, B) in the core 0.52 with the split at pA = 7 in 31 of 31
core-reaching runs (the responder's corner again). The mechanism is global selection among islands' loser bids: children arrive
from islands whose P population kept a higher bid, so the effect is a re-injection from the metapopulation (the loser's median bid
rises to 18.5 and the efficiency to 0.997). 0.31–0.57 of the islands are fixed at the horizon, so these are not absorbed states.
Only 8 of 40 (threshold) and 1 of 40 (asymmetric) runs reach the core at all in the unrestricted space.

## 6. N sweep (threshold, ε = 0, constants)

| N | unrestricted eroded / core | no-overbid eroded / core |
|---|---|---|
| 50 | 0.961 / 0.006 | 0.934 / 0.009 |
| 100 | 0.963 / 0.002 | 0.904 / 0.010 |
| 200 | 0.954 / 0.003 | 0.845 / 0.012 |

The in-core share does not rise with N; erosion falls slowly in the no-overbid space (0.93 → 0.85) and not at all in the
unrestricted space.

## 7. Caveats

* "Erosion" in the no-overbid space starts at generation 0 (§2); the statistic compares the end state with the core, not a drift
  away from a core start.
* In-core is evaluated on the island mean vector; with migration and rain, 31–70% of islands are polymorphic at the horizon, and
  the at-VN statistic averages over their encounters (mean payoffs of a symmetric polymorphism average to the symmetric split).
* The order of the responder's evaluation decides prediction 5; the registered order (P, A, B) is the one scored.
* The skew instance, the order-free rule, the x10 cells and the re-injection extras are post hoc and are labelled as such.
* Statistics are finite-(N, I, horizon) lottery statistics, not π; the migration and rain cells are about approach rates.
