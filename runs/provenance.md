# Provenance: who writes the first certificate, and against whom (run report, 2026-10-12)

Spec `specs/2026-10-12-provenance.md` (reviewed by gpt-6.1-sol); notes `notes/provenance.md` (§1 before any code;
§1.12 validation by code and its addendum before any counted cell; §2 costs); predictions
`predictions/2026-10-12-provenance.md`. Code: `src/provenance.py` (rules, counter RNG, island kernel, own-side
validity, term-level rules), `src/provenance_run.py` (static extension, OSV and the SPO audit, sets, gate closure,
hand pairs, validation, lottery), `src/provenance_report.py`, `tests/test_provenance.py` (10 tests). Summaries:
`runs/provenance.json` (all cells, costs, stages, contrasts, composition), `runs/provenance/{static_ext,osv,sets,
validate,gate_static}.json`, `runs/provenance/pairs.json`, `runs/provenance/lottery_{main,diag,size,gate}.json`. Raw
static arrays in `runs/provenance/static*/` (not committed).

Lottery numbers are ε = 0, finite-(N, I, horizon) evidence. Island-level efficiency (E3, island P(C,C)) and global
universality (universal-open) are reported separately. No chain was run (the spec drops it).

## 1. What was built, and what changed against the notes

- **Rules** as notes §1.2: S-self, S-nonself, S-self-delayed (shadow draws), S-2, S-3 (windows, own-side validity,
  safeguard score ≥ 2 with the earliest-candidate fallback), S-3 strict (extra), S-gate+cache, CS-nonself, C-donor,
  H-only. Quotes are code + list; mode and rule are metadata; the rules' source test reads the spelling.
- **Universe.** Milestone 5's 17,391 units plus 3 that S-k needs (a candidate written while the list was empty, kept
  after δ): 24,489 new host checks, 0 new production signatures.
- **Kernel.** Milestone 5's birth–death and encounter law with every draw a function of (replicate, event, draw)
  (splitmix64); encounters between *settled* individuals (H, or holding a C and a D entry under a lack rule) and
  *futile* ones (lacking an entry their rule can never produce) are skipped without consuming draws. Dynamics are
  unchanged: identical trajectories with and without the skip over 300 generations in 10 cells; the kernel's
  transitions equal term-executed encounters on 728/728 samples. Futile attempts are accounted in expectation
  (§5).
- **Corrections found by code before any cell (notes §1.12):** (i) the tactic's own output is not own-side valid at
  its would-be self in 468 of 19,102 signatures (F1), so such a candidate is inadmissible under the spec's rule;
  (ii) the signature reduction of own-side validity holds on 4,005/4,014 sampled pairs.
- **Process.** The first launch of the main batch was stopped after 18 runs (futile individuals made extensions too
  slow); those runs were set aside, not used. The second launch stalled on three 10,000-generation extensions in
  which E3 was recomputed every 10 generations; it was resumed with E3 every 500 generations past 2,000 (no 2,000
  number changes). Runs whose E3 failed by 2,000 are not extended (an all-defect metapopulation is absorbing at
  ε = 0); two C-donor failures were extended before that rule (8,000 more generations of all-D). Post-hoc diagnostic
  cells (not predicted, not scored) are labelled.

## 2. Static: the self-play-only audit and the ablation sets

| item | value |
|---|---|
| own-side validity values (τ, script, code) | 28,283; signature reduction 4,005/4,014 |
| tactic output not own-side valid at its would-be self | 468 of 19,102 signatures (F1) |
| SPO (τ, s) pairs (valid at a self root, at no distinct-quote root) | 484 on 480 run trees, mass 0.111 (mostly trees ending C on both branches) |
| SPO pairs written at a non-self code | **0** (Claim N over the whole universe, copied scripts included) |
| units holding only SPO C entries | 782 |
| run trees whose only C script is the self-root one (the only-self class) | 97, mass 0.0178, 114 seeded copies per run |
| S-nonself closure / its identity units | 10,953 units / 8, all TwinD family |
| **Q** (seed's own clique set, frozen rule) | TwinD family: 4 run trees, 10 spellings, μ = 7.13·10⁻⁴, **4.56 seeded copies per run** |
| **R** (prudent open core analogue) | 11 run trees, 33 spellings, μ = 0.0024 |

The hand table of notes §1.4 holds by whole runs of the term (`pairs.json`): CB writes σCB against every partner;
CB1 and AND2 write ι against a copy and σCB1 otherwise; MM writes ι against a copy and nothing anywhere else;
CBP₄/CBPr write nothing at encounter 1 and σCBP/σCBPr from encounter 2 against δ-holders; TwinD writes τ₀ at the self
root and τ₁ elsewhere; S-nonself writes nothing against itself. In a window, CB1's ι scores 1 and σCB1 2, so S-2 keeps
σCB1; MM's single candidate ι is kept by the fallback and refused by S-3 strict.

## 3. The lottery at (100, 64), 40 runs, horizon 2,000 (runs unresolved at 2,000 continued to 10,000)

*Universal-open* = every island held, every pair of holders mutually cooperating, every holder mutual with CB-H.
*Identity islands* = held islands whose holder is an identity unit. *SPO islands* = held islands whose holder carries
only self-play-only C entries. Runs universal with E3 decided at 2,000 were not extended and are counted at their
2,000 state in the @10,000 columns.

| cell | E3 success / fail | universal / patchwork / unheld | **universal-open** [Wilson] | @10,000 | island P(C,C) | identity islands | SPO islands | cross P(C,C) | SPO share of held C instances |
|---|---|---|---|---|---|---|---|---|---|
| H-only | 38 / 2 | 31 / 7 / 2 | 31 [0.62, 0.88] | 35 | 0.947 | 0.024 | 0 | 0.910 | 0 |
| C-donor | 38 / 2 | 37 / 1 / 2 | **37** [0.80, 0.97] | 37 | 0.949 | 0.004 | 0 | 0.944 | 0 |
| **S-self** | 40 / 0 | 23 / 16 / 1 | **22** [0.40, 0.69] | 24 | 0.989 | **0.136** | 0.095 | 0.868 | 0.095 |
| **S-nonself** | 39 / 1 | 28 / 11 / 1 | **28** [0.55, 0.82] | 31 | 0.969 | **0.048** | 0 | 0.907 | **0** |
| **S-self-delayed** | 40 / 0 | 21 / 18 / 1 | **21** [0.37, 0.67] | 26 | 0.986 | **0.135** | 0.097 | 0.846 | 0.097 |
| S-2 | 40 / 0 | 13 / 27 / 0 | 13 [0.20, 0.48] | 20 | 0.985 | 0.141 | 0.142 | 0.822 | 0.141 |
| S-3 | 40 / 0 | 15 / 24 / 1 | 15 [0.24, 0.53] | 23 | 0.984 | 0.110 | 0.086 | 0.801 | 0.086 |
| S-3 strict (extra) | 40 / 0 | 25 / 13 / 2 | 25 [0.47, 0.76] | 33 | 0.992 | 0.052 | 0 | 0.904 | 0 |
| CS-nonself | 40 / 0 | 29 / 11 / 0 | 28 [0.55, 0.82] | 31 | 0.995 | 0.063 | 0 | 0.936 | 0 |
| mixed (¼ S-self, S-nonself, S-2, CS-nonself) | 40 / 0 | 18 / 22 / 0 | 17 [0.29, 0.58] | 25 | 0.990 | 0.100 | 0.013 | 0.899 | 0.013 |
| **ablation** (S-nonself, Q's mass onto R) | 40 / 0 | 34 / 6 / 0 | **34** [0.71, 0.93] | **40** | 0.999 | **0.000** | 0 | 0.995 | 0 |
| *diag: S-2 own-root* | 40 / 0 | 12 / 28 / 0 | 12 [0.18, 0.45] | 16 | 0.981 | 0.087 | 0.086 | 0.787 | 0.087 |
| *diag: S-2 timing* | 40 / 0 | 12 / 28 / 0 | 12 [0.18, 0.45] | 16 | 0.980 | 0.094 | 0.104 | 0.782 | 0.104 |
| *diag: S-self D-first* | 40 / 0 | 18 / 21 / 1 | 18 [0.31, 0.60] | 21 | 0.987 | 0.141 | 0.174 | 0.826 | 0.174 |

Establishment: every cell established in 39–40/40 runs, median first island at P(C,C) ≥ 0.9 at generation 30 (means
28.8–35.2); persistence 0.95–1.00. **Island-level efficiency is never at risk:** E3 succeeded on 38–40/40 in every
cell; the four failures (H-only 2, C-donor 2, one S-nonself) are all-defect metapopulations in which no establisher
survived the scramble (in C-donor the island donors died before any copier adopted). Mean island P(C,C) 0.947–0.999
(the failed runs alone pull H-only and C-donor below 0.95).

**Primary contrasts (paired on the same founders and streams; McNemar exact p; bootstrap 95% intervals):**

| contrast | universal-open | discordant (A only, B only) | paired difference | identity islands, paired difference |
|---|---|---|---|---|
| (a) S-nonself − S-self | 28 vs 22 | 9, 3 (p = 0.15) | +0.150 [0.000, +0.325] | **−0.087 [−0.175, −0.009]** |
| (b) S-nonself − S-self-delayed | 28 vs 21 | 11, 4 (p = 0.12) | +0.175 [0.000, +0.350] | **−0.086 [−0.173, −0.008]** |
| (c) S-nonself − C-donor | 28 vs 37 | 3, 12 (**p = 0.035**) | **−0.225 [−0.400, −0.050]** | +0.045 [+0.011, +0.091] |

Secondary: S-self-delayed − S-self −0.025 [−0.150, 0.100] (identity −0.001): **timing recovers nothing**; ablation −
S-nonself +0.150 [−0.025, 0.325] at 2,000 (identity −0.048 [−0.094, −0.015]), 40 vs 31 at 10,000; S-2 − S-self
−0.225 [−0.425, −0.025] (p = 0.049); S-3 − S-nonself −0.325 (p = 0.011); S-3 strict − S-nonself −0.075 [−0.275,
0.125]; CS-nonself − S-nonself 0.000; mixed − S-nonself −0.275 (p = 0.007); H − S-nonself +0.075.

**Who holds the islands** (mean islands per run at 2,000 held by open carriers / identity units / others):
H-only 59.0 / 1.5 / 0.2; C-donor 60.6 / 0.2 / 0.0; S-nonself 59.0 / 3.1 / 0.2; ablation 63.8 / 0 / 0.2; S-self
54.5 / 8.7 / 0.8; S-self-delayed 54.3 / 8.6 / 1.1; S-2 52.5 / 9.0 / 2.5; S-3 53.0 / 7.0 / 4.0; S-3 strict 59.0 / 3.3 /
1.7; mixed 56.8 / 6.4 / 0.8. The top identity holders are the only-self class with ι (`if(and(CHK(me,me,C),
CHK(me,them,C)),C,D)` and its order twin) under S-self, S-self-delayed and S-k, and the TwinD family under every rule.

## 4. The self-play-only audit in the populations, stage statistics and the mixed cell

- **Claim N held dynamically:** 0 SPO scripts written by any S-nonself or CS-nonself production; 0 SPO instances held
  in S-nonself, ablation, CS-nonself and S-3 strict at every checkpoint; 0 SPO scripts entered by copying in any cell.
- **Where SPO scripts live:** of the SPO C-script instances held at 2,000, 98.0% (S-self), 97.6% (S-2) and 99.1%
  (S-3) are on only-self run trees (the rest: TwinD's τ₀ written at a self root and kept). Under S-k every kept SPO
  script was kept by the fallback (S-2 3,649 of 3,649, S-3 3,578 of 3,578; 0 by the safeguard). The safeguard was met
  in 64% of S-2's and 78% of S-3's selections.
- **Stage statistics** (identity units / SPO-only units; entries = transitions into the group by production,
  pooled over 40 runs; islands at 2,000):

| cell | identity: entries → runs ever held → runs held at 2,000 → islands → per entry | SPO-only: entries → ever → end → islands → per entry |
|---|---|---|
| H-only | seeded 4.5 copies/run → 5 → 5 → 61 | – |
| S-self | 349 → 15 → 14 → 347 → 0.99 | 3,500 → 19 → 12 → 244 → 0.070 |
| S-self-delayed | 351 → 16 → 16 → 345 → 0.98 | 3,458 → 22 → 12 → 248 → 0.072 |
| S-nonself | 181 → 10 → 8 → 124 → 0.69 | 0 |
| S-2 | 356 → 19 → 19 → 361 → 1.01 | 3,649 → 20 → 17 → 364 → 0.100 |
| S-3 | 371 → 19 → 19 → 281 → 0.76 | 3,578 → 21 → 15 → 219 → 0.061 |
| S-3 strict | 180 → 13 → 13 → 133 → 0.74 | 0 |
| ablation | 0 | 0 |

  S-nonself's identity entries are the TwinD family producing τ₁ against non-self partners (the seed's own cliques,
  4.5 copies per run); S-self adds the only-self class's ι minted inside growing lineages (≈ 3,500 SPO entries per
  40 runs, ≈ 0.07 islands each).
- **Mixed cell** (rules iid ¼, heritable). Rule shares among cooperative individuals on held islands (S-self,
  S-nonself, S-2, CS-nonself): at establishment 0.305 / 0.219 / 0.229 / 0.247 (all individuals 0.243 / 0.259 / 0.234 /
  0.264); generation 200 0.256 / 0.213 / 0.280 / 0.251; 2,000 0.265 / 0.245 / 0.301 / 0.189 (no rule above 0.31).
  S-self is over-represented at establishment by 0.055 (founder effects: within a holder spelling the rule share is
  typically 0.6–1.0 of one rule, e.g. `if(CHK(them,^D,D),if(CHK(them,me,C),C,D),D)` held entirely by S-nonself
  lineages); SPO instances are held only by S-self (2,597) and S-2 (780) individuals, none copied by CS-nonself.
  Equality classes are not split by rules: distinct quotes per run equal distinct spellings at the horizon (3.3).
  Universal-open 17/40 is **below both** S-self (22) and S-nonself (28).

## 5. Costs, waiting and acquisition (modelled steps from milestone 5's term medians)

| rule (cell) | executed production steps per match | futile share of matches | C attempts → successes | cap timeouts | median steps per acquisition | capable producers waiting ≥ 20 encounters (near-monoclonal) |
|---|---|---|---|---|---|---|
| S-self | 14 | 0.063 | 1.19·10⁸ → 162,473 | 0.6% | 22,387 | 0.0% |
| S-nonself | 26 | 0.118 | 1.16·10⁸ → 158,107 | 4.1% | 22,387 (1.0×) | 0.25% (32.7% of 188,018) |
| S-self-delayed | 8 | 0.052 | 6.7·10⁷ → 162,402 | 0.8% | 22,387 | 0.14% (20.9%) |
| S-2 | 9 | 0.073 | 8.6·10⁷ → 160,264 | 0.1% | 89,125 (4.0×) | 0 |
| S-3 | 8 | 0.114 | 6.7·10⁷ → 159,840 | 0.3% | 177,828 (7.9×) | 0 |
| S-3 strict | 134 | 0.036 | 8.6·10⁸ → 150,198 | 0.05% | 177,828 | 0 |
| CS-nonself | 874 | 0 | 1.5·10⁹ → 149,304 | 0.6% | 44,668 | 3.9% (39.2%) |
| C (C-donor copiers) | 864 | 0 | – | – | – | – |

*Executed* steps are those of encounters the kernel processes; *futile* matches (an individual whose rule can never
produce its missing entry) retry a production at every match in the dynamics (no negative cache under the lack rule)
and cost one production attempt each (≥ 9,058 steps), so the full per-match cost is about futile share × 10⁴: ≈ 870
(S-self), ≈ 1,620 (S-nonself, whose only-self programs never acquire), ≈ 1,000–1,600 (S-k). Producer logs: of capable
producers (newborns lacking a C entry on run trees with a non-self production) 98.7–99.4% die before acquiring under
every rule (they are mostly newborns of lineages whose productions fail against the partners they meet); 0 are still
lacking at a 2,000 horizon except under S-3 strict (15,132, 0.008%). Waiting ≥ 20 encounters before the first attempt
is rare overall (≤ 0.25% under S-nonself) and common among the 0.7% of producers born into islands where their own
spelling is ≥ 90% (32.7%).

## 6. Size panel (finite-size; 20 runs each; r = N/2; unresolved runs continued to 10,000)

| cell | (100, 64) [40 runs] | (200, 64) @2,000 → @10,000 | (100, 128) @2,000 → @10,000 | identity islands (200, 64) / (100, 128) |
|---|---|---|---|---|
| S-self | 22/40 (0.55) | 6/20 → 6 | 4/20 → 8 | 0.163 / 0.126 |
| S-nonself | 28/40 (0.70) | 11/20 → 11 | 6/20 → 11 | 0.113 / 0.082 |
| C-donor | 37/40 (0.93) | **20/20** (no run unresolved) | 18/20 → 19/19 (one extension censored at its time cap) | 0 / 0 |
| ablation (extra, not predicted) | 34/40 → 40 | 17/20 → 18 | 14/20 → 16 | 0 / 0 |

Paired: S-nonself − S-self +5 runs at (200, 64) (5, 0 discordant; +0.25 [0.10, 0.45], p = 0.063) and +2 at (100, 128)
(+0.10 [−0.10, 0.30]); S-nonself − C-donor −9 (p = 0.004) and −12 (p = 0.002). Every run of every size cell kept
every island efficient (E3 20/20). At N = 200 no unresolved run of S-self or S-nonself changed between 2,000 and
10,000 (frozen patchworks, as in the identity run); at I = 128 about a third resolved. The seeded TwinD copies scale
with I·N (9.2–9.7 per run in both panels), and S-nonself's identity islands rise with N (0.048 → 0.113): the seed's
own cliques bind harder as islands grow; with them ablated the loss with size is smaller (17–18/20 and 14–16/20).

## 6b. The gate cell

(Filled below.)

## 7. Verdicts

(Filled below.)
