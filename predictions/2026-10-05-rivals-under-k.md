# Predictions: rivals under the bounded prover K: does incompleteness remove the bridge-less obstruction? (2026-10-05)

Spec `specs/2026-10-05-rivals-under-k.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-05-rivals-under-k-gpt-6.1-sol.md`;
where the two differ the spec's [after review] text is the resolution). Code: `src/rivals_under_k.py` (kernel
`rival_islands._kern` unchanged; K tables `runs/k-at-n8/kval_n8_b{4,16,54}.npy` copied from a sibling worktree,
byte-identical in both siblings, not committed). Committed after the static screening (allowed by the brief, since the
forced rivals are chosen from it) and before any lottery run, including the m = 0 calibration runs. Finite-cutoff
(n = 8), finite-horizon evidence about the bridge-less obstruction relative to FairBot's pair.

## RE predictions (copied verbatim from the spec)

1. **Under K at b = 16 the direct-bridge-less hard rival mass is < 0.02 of rival mass** (against ≈ 0.25 under the
   free box at n = 8), with no new rival of mass ≥ 10⁻⁶ by source identity. *Falsifier:* share ≥ 0.1, or a new
   bridge-less rival of mass ≥ 10⁻⁵. Grey zone 0.02–0.1: inconclusive.
2. **Natural horizon separation under K is lower than under the free box at the same cutoff and the same mN, and
   no horizon separation under K involves a direct-bridge-less rival.** The RE expects 0–2 of 3,000 under K
   (one-sided 95% upper rate ≈ 0.0021 at two events, which is a *bound*, not a fivefold reduction) against 4–20
   under free (mostly P\*-family). *Falsifier:* K's count ≥ free's count at the common mN, or a direct-bridge-less
   rival among K's horizon separations. Grey zone: K below free but with ≥ 3 events.
3. **Forced P\* under K has no cooperative establishment** (0 islands in 100 runs) **but may survive as a lineage**
   (the RE predicts lineage survival at the horizon in ≤ 0.1 of runs, no more than the inert-defector control's)
   and leaves q_est unchanged (|Δq_est| ≤ 0.1 against the iid control, and within 0.05 of the inert-defector
   control). *Falsifier:* a cooperative P\* establishment, or lineage survival exceeding the inert control's by
   ≥ 0.2. Grey zone between.
4. **Budget sensitivity:** the direct-bridge-less share under K is below 0.05 at b = 4, 16 and 54. *Falsifier:*
   ≥ 0.1 at some budget; grey zone 0.05–0.1.
5. **The positive control resolves** (mediation-before-loss ≥ 0.7 for the forced bridged rival under K) **and
   island-level efficiency is unchanged** (island P(C,C) ≥ 0.97 in every K cell; K's run-level efficient fraction
   not below the free box's by ≥ 0.05). *Falsifier:* mediation-before-loss ≤ 0.4, or K below free by ≥ 0.05.

## Subagent predictions (S1–S9)

Written after the static screening (addendum below), before any run.

- **S1 (free natural count).** Under the free box at n = 8 and its calibrated boundary mN, horizon separations are
  3–15 of 3,000 (static rate μ_bl·N·I·p₁ with μ_bl = 4.1·10⁻⁶ cut and p₁ ≈ 0.048 gives ≈ 7.5), and ≥ 0.6 of them
  involve a direct-bridge-less (P\*-family) rival. *Falsifier:* ≤ 1 or ≥ 25 horizon separations, or a P\*-family
  share ≤ 0.3 with ≥ 4 separations.
- **S2 (K natural count).** Under K at b = 16, at both its calibrated mN and the common mN, horizon separations are
  ≤ 1 of 3,000 each, and every K separation (ever or at the horizon) that involves A is with the PrudentBot pair
  (the only rivals of A at b = 16). *Falsifier:* ≥ 4 horizon separations in either K cell, or a K separation with an
  A-rival other than the PrudentBot pair.
- **S3 (calibration).** T_nuc at N = 200 (m = 0, I = 16, 120 runs) under K b = 16 is within ±20% of the free arm's
  (the establisher mass is 0.0242 in both), so the two boundary mN values differ by ≤ 20%. *Falsifier:* a
  difference > 35%.
- **S4 (K at b = 4, beyond the spec, declared here).** At b = 4 FairBot and `BOX1(THEM(ME))` are rivals of each
  other with no class bridging them (static); a 1,000-run natural cell at K b = 4's calibrated mN ends separated at
  the horizon in ≥ 0.5 of runs, while island P(C,C) stays ≥ 0.97. *Falsifier:* horizon separation < 0.2, or island
  P(C,C) < 0.9.
- **S5 (positive control).** PrudentBot `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` forced densely under K b = 16
  establishes in ≥ 0.8 of runs, ends separated in ≤ 0.05, with mediation-before-loss ≥ 0.85 (the free arm's H at n = 9:
  0.01 and 0.92). *Falsifier:* horizon separation ≥ 0.15 or mediation-before-loss ≤ 0.6.
- **S6 (P\* lineage under K).** Forced P\* under K b = 16 survives at the horizon in ≤ 0.05 of runs, and its
  survival is within 0.05 of the inert D control's; the lineages' median extinction generations are within a factor
  2 of each other. *Falsifier:* survival ≥ 0.2, or a survival difference ≥ 0.15.
- **S7 (P\* reference under free, beyond the spec, declared here).** The same forced P\* under the free box at n = 8
  establishes cooperatively (its lineage the certified holder of ≥ 1 island) in ≥ 0.9 of runs and ends separated
  in ≥ 0.8 (n = 9: 0.98 and 0.97). *Falsifier:* cooperative establishment ≤ 0.6.
- **S8 (efficiency).** In all three natural cells island P(C,C) ≥ 0.99 and the run-level efficient fraction (mean
  island P(C,C) ≥ 0.95) ≥ 0.98, with |K − free| ≤ 0.01 at the common mN. *Falsifier:* island P(C,C) < 0.97 in a
  natural cell, or |K − free| ≥ 0.03.
- **S9 (continuation).** ≥ 0.9 of the free arm's horizon-separated P\*-family runs are still separated at 3·10⁵
  generations, with 0 losses. *Falsifier:* ≤ 0.6 still separated.

## Verdict rules

A prediction **held** if every clause is true. It **failed, falsifier fired** if its falsifier condition is met;
**failed, falsifier not fired** if a clause is false but the falsifier is not met; **inconclusive** if the outcome is
in a predeclared grey zone. Counts use runs as the independent units with Wilson 95% intervals; hazards with exact
Poisson intervals, the one-sided 95% upper bound 3/exposure for zero-loss cells; resolution times right-censored
at the horizon (Kaplan–Meier). Island-level and counterfactual cross-island P(C,C), cooperative establishment and
lineage survival are reported separately; q_est (local establishments relative to the paired m = 0 reference) is the
nucleation statistic. "Common mN" is the free arm's calibrated boundary value at n = 8 (if K's calibrated value
equals it, the two K cells are one). Forced cell (d) is run only if the screening finds a direct-bridge-less rival
of A under K at b = 16.

## Addendum: static screening (ran before this commit)

`runs/rivals-under-k-static.json`, `python3 src/rivals_under_k.py static` (2 s). L_8 has 610 canonical sources.

**Checks.** The free class table built here from the GL+Def table equals the existing n = 8 free class table
(`modal.build(8)`, used by `almost_all_seeds.arm_data('modal', 8)` / `seeds_in_n`): 471 classes, identical names,
order, payoffs and masses (max |Δμ| 4·10⁻¹⁵). Lumping validity, every arm: every class has identical directed rows
and columns for all members (exhaustive, 0 violations); class masses equal summed source masses (error ≤ 6·10⁻¹⁷);
seed draws lumped from sources match class-level draws (2,000 islands each, max |z| ≤ 2.8 over all classes); the
establisher, rival and direct-bridge tests (existence and mass) agree between the class table and the source-level
table for **all 610 sources** (the spec's 1,000-source sample exceeds the language): 0 mismatches in every arm.

**Screening** (rival = establisher mutually defecting with FairBot or `BOX1(THEM(ME))`; masses cut, raw in brackets):

| arm | classes | establishers (μ) | rivals (full) | rival μ | direct-bridge-less share | hard share | no mediator path ≤ 3 | establisher graph |
|---|---|---|---|---|---|---|---|---|
| free | 471 | 96 (0.0242) | 12 (6) | 1.85·10⁻⁵ [1.41·10⁻⁵] | **0.221** (P\*, P\*′) | 0.221 | 0 | 1 component; path 1/2/3: 70/22/2 |
| K b = 16 | 476 | 93 (0.0242) | 2 (0) | 2.73·10⁻⁶ [2.08·10⁻⁶] | **0.000** | 0.000 | 0 | 1 component; path 1/2: 57/34 |
| K b = 54 | 255 | 52 (0.0242) | 2 (0) | 2.73·10⁻⁶ | 0.000 | 0.000 | 0 | 1 component |
| K b = 4 | 83 | 25 (0.0281) | 18 (5) | **1.68·10⁻²** | **1.000** | 0.906 | 0.091 | 4 components; 2 establishers unreachable |

- **b = 16 and 54:** the only rivals of A are the PrudentBot pair `and(BOX(THEM(ME)),BOXD1(THEM(^D)))`,
  `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))`, half-rivals (mutual defection with `BOX1(THEM(ME))`, mutual cooperation
  with FairBot), each bridged (9 / 17 bridges, mass 5.1·10⁻³, heaviest `BOX(THEM(THEM))`). **No new rival by source
  identity**; 11 free-arm rival sources (μ 1.6·10⁻⁵) are not rivals under K: the P\* family (self-defects), the
  B₁ family `BOX1(THEM(^not(…)))`, and the `not(BOXD1(THEM(^not(…))))` family.
- **P\* under K b = 16** is a singleton class that self-defects; its row equals D's (it defects on everything), but
  its column differs from D's in 175 classes: it has prey D lacks (μ 0.0058, including 40 light establishers
  `not(BOXD(THEM(^BOX(THEM(ME)))))`-type, μ 8.1·10⁻⁵, that cooperate unless they can prove the opponent defects,
  which K cannot for P\*), and D has prey P\* lacks (μ 0.0138). So P\* under K is not an inert defector.
- **b = 4 degenerates the definition:** FairBot and `BOX1(THEM(ME))` mutually defect at b = 4 (soft cliques at the
  copy threshold), so no class mutually cooperates with both and every rival is literally bridge-less, including
  each member of A as the other's rival (μ 5.0·10⁻³ each). Taken separately, FairBot's rivals at b = 4 have μ
  5.1·10⁻³ (share bridge-less 0.997) and `BOX1(THEM(ME))`'s μ 1.2·10⁻² (1.000). These are budget soft-clique
  rivalries, not the P\* family (which is gone at every K budget).
- One-migrant fixations between every rival and the A member it mutually defects with are positive at N = 200
  (≈ 7·10⁻⁹; no zero transitions, none below 10⁻¹²), and below 10⁻¹² at N = 400 for every rival in every arm.

**Verdicts decided by the static.** RE 1 **held** (share 0.000 < 0.02; no new rival). RE 4 **failed, falsifier
fired** at b = 4 (share 1.000 ≥ 0.1; the pair A itself is split at b = 4), held at b = 16 and 54 (0.000).
**Consequences for the design:** (d) is not run (no direct-bridge-less rival of A under K at b = 16); the positive
control (b) is PrudentBot `and(BOX(THEM(ME)),BOXD1(THEM(^D)))`, the heaviest bridged rival of A under K at b = 16;
S4 adds a K b = 4 natural cell beyond the spec.
