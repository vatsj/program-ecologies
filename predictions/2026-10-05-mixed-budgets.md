# Predictions: mixed-budget populations under K: do budget soft cliques become bridge-less rivals when budgets vary? (2026-10-05)

Spec `specs/2026-10-05-mixed-budgets.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-05-mixed-budgets-gpt-6.1-sol.md`;
where the two differ the spec's [after review] text is the resolution). Code: `src/mixed_budgets.py` (a copy of the
kernel `rival_islands._kern` as `_kern_mb`, single-migrant only, carrying each (island, class)'s expected budget
composition; checked to give identical trajectories to `_kern` on the same inputs; core files unchanged). K tables
and cross-budget blocks in `runs/k-at-n8/` (b = 4, 8, 16 and (4, 16) copied from sibling worktrees; (4, 8) and
(8, 16) computed here with `k_at_n8._cross8`; none committed). **The main result is finite-horizon incidence at
n = 8 (N = 200, I = 64, horizon 10⁵), not large-population universality or permanent isolation.**

Written before the full {4, 8, 16} screening and before any lottery run (including m = 0 calibration). The subagent
had seen only a trial screening on the {4, 16} sub-catalogue (uniform prior over {4, 16}): `BOX1(THEM(ME))`@4 is an
establisher component of its own there, and (`BOX1(THEM(ME))`@4, `BOX1(THEM(ME))`@16) is incompatible with no
structural bridge. The full screening and the forced pairs chosen from it are recorded in the addendum below,
committed before any lottery run.

## RE predictions (copied verbatim from the spec)

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

## Subagent predictions (S1–S8)

Reasoning in one line: K's budget grid makes FairBot's copies compatible across {4, 8, 16} but `BOX1(THEM(ME))`@4
compatible with nothing but itself, so budget 4 creates one heavy soft clique that no budget-8 or -16 program can
bridge; above the thresholds the only incompatibilities are light ones.

- **S1 (static concentration).** Under cheap-heavy, ≥ 0.8 of the direct-bridge-less incompatible-pair mass has the
  class of `BOX1(THEM(ME))`@4 as one member; under above-threshold the direct-bridge-less pair mass is < 10⁻⁸ (cut,
  product units) and no direct-bridge-less pair has FairBot or `BOX1(THEM(ME))` at any budget as a member.
  *Falsifier:* share < 0.5, or above-threshold mass ≥ 10⁻⁷, or a FairBot/`BOX1(THEM(ME))` copy in an
  above-threshold bridge-less pair. Grey zone: share 0.5–0.8 or mass 10⁻⁸–10⁻⁷.
- **S2 (natural incidence, size).** At the common mN, cheap-heavy horizon separation is ≥ 0.3 of runs (point guess
  0.6), and ≥ 0.7 of separated cheap-heavy runs have `BOX1(THEM(ME))`@4's class as one member of a separated pair;
  above-threshold has ≤ 3 of 3,000. *Falsifier:* cheap-heavy < 0.1, or the `BOX1(THEM(ME))`@4 share < 0.4, or
  above-threshold ≥ 10 of 3,000. Grey zone between.
- **S3 (composition, against RE 3's direction).** Under cheap-heavy the mean budget of cooperative holders does not
  rise between the first checkpoint and the horizon by more than 0.5 budget units (it falls or stays: the
  budget-4 side of every bridged incompatibility is the heavier side, and `BOX1(THEM(ME))`@4 islands are permanent),
  and the TV change is < 0.1. *Falsifier:* a rise of ≥ 1.0 budget units with TV change ≥ 0.1 (RE 3 holding).
  Grey zone between.
- **S4 (homogeneous controls).** Horizon separation: b = 4 in [0.65, 0.92] (RESULTS "Rivals under K" had 0.80 on
  50 runs); b = 8 ≤ 0.01; b = 16 ≤ 0.005. *Falsifier:* b = 4 < 0.5, or b = 8 ≥ 0.03, or b = 16 ≥ 0.02.
- **S5 (forced bridge-less pair).** Given both members established, horizon separation ≥ 0.85 with 0 losses of
  either network after both are established, at (200, 64, 10⁵) and on every scaling-panel cell. *Falsifier:*
  < 0.6 at any cell, or a hazard estimate above 10⁻⁷ per minority-island-generation with ≥ 3 losses.
- **S6 (forced bridged pair).** With bridges present, horizon separation ≤ 0.15 and mediation-before-loss ≥ 0.75;
  with bridge classes removed from the seed law, horizon separation ≥ 0.6. *Falsifier:* ≥ 0.3 with bridges, or
  ≤ 0.3 without. Grey zone between.
- **S7 (efficiency denominators).** Island P(C,C) over certified islands ≥ 0.98 in every natural and homogeneous
  cell; run-level efficient fraction over all islands ≥ 0.95 averaged over runs; cf cross-island P(C,C) of separated
  cheap-heavy runs in [0.4, 0.85]. *Falsifier:* island P(C,C) < 0.95 in a cell, or run-level < 0.9.
- **S8 (calibration).** m = 0 T_nuc is 45–65 generations under every prior (the calibrated boundaries fall in
  [0.92, 1.33]), and cheap-heavy's horizon separation at its calibrated mN is within 0.1 of its common-mN value.
  *Falsifier:* a T_nuc outside 40–75, or a difference ≥ 0.2. Grey zone 0.1–0.2.

## Verdict rules

- Separation at the horizon = two certified islands (island P(C,C) ≥ 0.95) whose cooperative holders mutually defect
  (an incompatible pair), counted per run; intervals are exact (Clopper–Pearson) with runs as the units; paired
  comparisons over common reps (the source-level seed and the per-individual budget uniforms are shared by every
  prior at the same (N, I, rep)).
- Composition distance (RE 3, S3): per run, the island-weighted budget distribution of cooperative certified holders
  (one vote per island, the vote being the holder's expected budget composition on that island, exact given the
  lumped path) at the first check after every island is established and at the horizon (or the stop of a frozen run),
  TV against the prior over {4, 8, 16}; the statistic is the mean over runs with both checkpoints of (TV_end −
  TV_first), with a run-bootstrap interval, and the direction is the mean budget shift.
- Island-level P(C,C) is over certified islands; the run-level efficient fraction is over all islands; the cf
  cross-island P(C,C) is the global-composition counterfactual; all three are reported for every cell.
- A prediction's falsifier fires only on the stated statistic; a grey-zone outcome is reported as inconclusive;
  a cell that did not run leaves its clauses untested.
- Forced cells (RE 4, S5, S6): background seeds from cheap-heavy at the common mN; founders replace one uniformly
  chosen individual on every island of their half (pair members on disjoint halves); inert-defector control = D
  founders on both halves; iid control = no founders, same seeds. Mediation-before-loss = among runs in which both
  networks held a certified island, the fraction with an island of either network strongly taken by a bridge class
  before either network is lost (or the horizon).
