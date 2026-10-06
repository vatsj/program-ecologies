# Spec: mixed-budget populations under K: do budget soft cliques become bridge-less rivals when budgets vary?, 2026-10-05

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-05-mixed-budgets-gpt-6.1-sol.md`) and revised; changes marked
[after review]. To be run by an Opus subagent. Follow-up to RESULTS "Rivals under the bounded prover K" (DEFERRED
1 and 2, "would settle it": the budget rule for mixed-budget populations). The cross-budget K catalogue at n = 8
exists over {4, 16} and extends to {4, 8, 16}; the screening and lottery machinery of the rivals-under-K run is
reused. [after review] The main result is **finite-horizon incidence** at n = 8, not large-population universality
or permanent isolation.

## Why

Under K at a single global budget b ≥ 12 the bridge-less obstruction to metapopulation universality is gone at
n = 8, and below the distinct-budget thresholds it returns as budget soft cliques (the budget grid: FairBot_b
cooperates with a distinct-budget FairBot iff min(b_x, b_y) ≥ 4, so FairBot₄ *is* compatible with FairBot₁₆;
`BOX1(THEM(ME))` iff min ≥ 7, so `BOX1(THEM(ME))`₄ defects on `BOX1(THEM(ME))`₁₆; FairBot vs `BOX1(THEM(ME))` iff
b_x ≥ 6 and b_y ≥ 5) [after review: corrected]. A real population of realizable readers will not share one budget,
so low-budget copies of core programs can be incompatible with high-budget copies *by budget alone*. Whether such
incompatible pairs are bridged decides whether the compatibility floor of RESULTS "Rivals under K" is a
population-level obstruction or only a per-program one. [after review] A missing edge is not bridge-lessness: the
thresholds give incompatible pairs, and only exhaustive enumeration over the budgeted catalogue says whether a
third program connects them.

## Definitions [after review]

- **Budgeted establisher:** a (source, budget) with budget in B that self-cooperates in K and defects on D.
- **Incompatible pair:** two budgeted establishers that mutually defect. This is the primary screening unit.
- **Pairwise bridge** of an incompatible pair: a budgeted cooperative class mutually cooperating with both; **mediator
  path:** a path of length ≤ 3 between them in the budgeted establisher mutual-cooperation graph;
  **direct-bridge-less / disconnected:** no pairwise bridge / no mediator path. **Structural bridge** (exists in the
  catalogue) is distinguished from a **seeded and surviving bridge** in a run.
- **A₁₆:** the reference clique {FairBot₁₆, `BOX1(THEM(ME))`₁₆}; "rival of A₁₆" is reported as a secondary
  statistic only.
- **Composition distance:** total variation between the budget distribution of cooperative holders (island-weighted,
  one vote per holding island) and the seed's budget prior, at the first checkpoint after every island is
  established (founder filtering) and at the horizon (subsequent selection).
- **Separation:** two certified islands whose cooperative holders are an incompatible pair, at the horizon
  (incidence), with run-level exact binomial intervals; **resolution hazard:** per exposure, with censoring.
- Efficiency denominators: island-level P(C,C) over certified islands, run-level efficient fraction over all
  islands, and the counterfactual cross-island P(C,C), all reported.

## Design

**Catalogue.** K at n = 8 over B = {4, 8, 16} (the K-at-n8 cross-budget machinery, {8} added), soundness check,
lumping validity on budgeted sources. Budget priors over B: *uniform* (1/3 each); *cheap-heavy* (0.6, 0.3, 0.1);
*above-threshold* (0, 0.5, 0.5). The induced class table under each; **homogeneous-budget controls** at 4, 8 and 16
with the same kernel and horizon [after review].

**Static screening.** All incompatible pairs of budgeted establishers, with exhaustive pairwise-bridge enumeration
and mediator paths; the direct-bridge-less and disconnected pair mass (product of the two masses, and the
per-pair co-seeding probability at N = 200) under each prior; which incompatible pairs are budget copies of one
source; the budgeted establisher compatibility graph (components; whether the budget-4 and budget-16 copies of
each core program share a component); for reference, the rivals of A₁₆ as before. Report masses normalized and
raw.

**Lottery** (kernel of rivals-under-K; N = 200, I = 64; horizon 10⁵; holder rule; hazards with exposure; paired
seeds across priors where the seed law allows) [after review: both migration rules, calibrated]:
- (a) natural iid runs, 3,000 per budget prior, at the **common mN** 1.091 and at each prior's **calibrated
  boundary** (T_nuc at m = 0 per prior, x = mN·T_nuc/N reported), every separation's pair (sources, budgets),
  structural bridge existence, bridge presence at seeding and fate recorded; composition distance at both
  checkpoints;
- (b) forced cells, 100 runs each with inert-defector and iid controls: the heaviest **direct-bridge-less
  incompatible pair** found (both members forced, on disjoint island halves) and the heaviest **incompatible but
  bridged pair**, the latter with bridge-present and bridge-absent seeds (bridge mass removed and renormalized)
  [after review];
- (c) a **scaling panel** for the decisive bridge-less forced pair: I ∈ {64, 256} and horizon {10⁵, 3·10⁵} at the
  declared migration scaling (boundary mN), 40 runs per cell, with exposure-conditioned resolution hazards and
  censoring [after review].
Priority: catalogue and screening → homogeneous controls → (a) cheap-heavy and above-threshold at the common mN →
(b) → (a) calibrated cells and uniform → (c). ≤ 3 workers; stop where time runs out and say so.

## Required outputs

`runs/mixed-budgets.md` and `.json`, code in `src/mixed_budgets.py` (reusing `src/rivals_under_k.py`,
`src/k_at_n8.py`, `src/bounded_k.py`; no core edits except bug fixes in their own commits), a predictions file from
the spec committed before any counted run (the screening may precede it as an addendum, since the forced pairs are
chosen from it), the usual hand-back (draft RESULTS, REJECTED, THEORY §3 and §9.2 edits, DEFERRED 1 and 2 edits,
NOTATION, ≤ 5 lines, branch from `git branch --show-current`, commits).

## RE predictions (with falsifiers) [after review: aligned; set-level claims replaced by pair-level ones]

1. **The pair (`BOX1(THEM(ME))`₄, `BOX1(THEM(ME))`₁₆) is incompatible and direct-bridge-less** (no budgeted class
   cooperates with both, since cooperating with the budget-4 copy needs a reader that proves it within 4 and the
   budget-16 copy's partners need ≥ 7), **and the direct-bridge-less incompatible-pair mass under cheap-heavy is
   ≥ 10× that under above-threshold**; the named core {FairBot, `BOX1(THEM(ME))`} at budgets ≥ 8 is one
   compatibility component, while catalogue-wide the above-threshold prior may still contain bridge-less pairs
   (PrudentBot's threshold is 11). *Falsifier:* the named pair has a pairwise bridge, or the cheap-heavy /
   above-threshold ratio < 3. Grey zone 3–10.
2. **Natural horizon separation under cheap-heavy exceeds above-threshold's at the common mN**, with the RE's point
   expectation ≥ 5 of 3,000 under cheap-heavy and ≤ 2 under above-threshold; separations are reported with exact
   intervals and the comparison is the paired count. *Falsifier:* cheap-heavy ≤ above-threshold. Grey zone: more
   under cheap-heavy but fewer than 3.
3. **Holder budgets are compatibility-biased, not prior-shaped** [after review: sol's reading adopted]: the
   composition distance at the horizon exceeds the distance at the first checkpoint by ≥ 0.1 under cheap-heavy, in
   the direction of higher budgets (more partners); the direction is the RE's guess, the magnitude uncertain.
   *Falsifier:* horizon distance within 0.03 of the first-checkpoint distance (no selection after founding).
   Grey zone 0.03–0.1.
4. **The bridged forced pair resolves with a seeded surviving bridge and separates without it** (mediation-before-loss
   ≥ 0.7 with the bridge, horizon separation ≥ 0.5 with it removed), and **the bridge-less forced pair's separation
   persists on the scaling panel** (≥ 0.5 at I = 256 and at 3·10⁵, hazard bound reported). *Falsifier:* bridged pair
   separating ≥ 0.4 with the bridge present, or bridge-less pair resolving to ≤ 0.2 at 3·10⁵.
5. **Island-level efficiency is unchanged** (island P(C,C) ≥ 0.97 in every cell) **and the homogeneous controls
   reproduce RESULTS "Rivals under K"** (b = 4 separated ≈ 0.8, b = 16 ≈ 0). *Falsifier:* island P(C,C) < 0.9, or
   b = 16 control ≥ 0.05 separated.

The RS is invited to add predictions; the uncertain one is 3.
