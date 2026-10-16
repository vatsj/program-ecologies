# Predictions: removing rival networks (sponsored PrudentBot donor; seed rain as a finite-ε diagnostic), 2026-10-15

Spec `specs/2026-10-15-removing-rivals.md` (reviewed by gpt-6.1-sol and gemini-4-argon; the amendments supersede the
earlier text). Notes `notes/removing-rivals.md` §1 (committed before any code). Written and committed before any code
and before any counted cell. Rain cells are finite-ε approach-rate diagnostics, never π.

## The RS's prediction (verbatim, registered first)

> "trickle and drift are distinguished only by scale - a small trickle over infinite time brings back the shadow. The
> divide I wanna draw is that drift should never colonize an island, only reintroduce fit programs."

Scored as notes §1.9: drift colonizations (a rain lineage that was neutral or deleterious against the island's majority
at arrival reaching ≥ 0.5 of an island) per island-generation at each rain rate, the shadow case on target islands,
and whether an admissible window (cures with zero drift colonizations) exists. *Read as a criterion and a claim:*
"drift should never colonize" is held at a rate if that rate's cells show zero drift colonizations over their horizon;
it fails at a rate with any.

**Scoring conventions (declared now).** Target, rival, identity, exploitable, closed, resolution, predator step and
losses as in notes §1.1–§1.6. *Rival islands* are target-relative (a held island whose holder is not mutual with the
PrudentBot reference unit); this is primary for every prediction below. The scaling run's classifier (failing
relative to the plurality open holder) is reported beside it as the *stored-classifier* reading, and where a verdict
differs between the two both are stated. B1 is scored at checkpoint + 10,000 generations, cures as differences between
matched branches (rain minus ε = 0 on the same checkpoint). Part A is scored at 2,000 and 10,000, the stated horizon
being 10,000 where a prediction does not name one; C-donor's comparison is at 2,000 (its stored horizon). Fractions are
over runs for run statistics and over islands pooled across runs for island statistics, with run-clustered intervals.

*Disclosure.* Before writing this file I had made the table lookups disclosed in notes §1 (spelling-level target
status of stored holders, showing many off-target open holders in stored universal-open runs). No Part 0 number, no
predator mass and no cell had been computed.

## RE predictions (verbatim from the spec)

1. **Most non-identity rivals are exploitable; identity cliques are closed:** ≥ 0.8 of non-identity rival islands
   have a predator with positive prior mass; 0 identity islands do. *Falsifier:* ≤ 0.5 exploitable.
2. **Rain cures exploitable rivals:** at εN = 0.1, ≥ 0.8 of exploitable rival islands join the target by 10,000
   generations, mostly by a predator step. *Falsifier:* ≤ 0.4.
3. **Rain does not cure cliques at N ≥ 200:** ≤ 0.1 of identity islands resolve at any rate. *Falsifier:* ≥ 0.3.
4. **Rain does not break the network:** target-island losses ≤ 0.01 per island over 10,000 generations at
   εN ≤ 0.1. *Falsifier:* ≥ 0.05.
5. **The sponsored donor prevents cliques:** identity islands ≤ 0.01 and universal-on-target ≥ 0.85 in every A cell,
   at least C-donor's. *Falsifier:* below 0.7 anywhere.
6. **Both together are universal on target:** B3 ≥ 0.95 at both geometries. *Falsifier:* ≤ 0.8.
7. **Counter-predictions registered after review.** *Sol:* cure at εN = 0.1 varies sharply with the accessible
   predator mass (80% of islands even receiving a predator needs accessible mass ≥ 0.0016) and many exploitable
   rivals stay unresolved; sponsorship reduces cliques but leaves geometry-dependent residual failures, so 5 and 6
   are too high; cliques resist far more strongly than exploitable rivals without necessarily meeting 3's bound.
   *Gemini:* the cure at εN = 0.1 is < 0.4 unless a simple high-prior program such as DefectBot is itself a predator.

*Scoring of 7 (mine, declared now):* Sol's first clause is scored as a positive rank correlation between μ(Pred_X) and
the per-island cure at εN = 0.1 (Spearman > 0.3 over exploitable rival islands) plus "many unresolved" = ≥ 0.2 of
exploitable rival islands unresolved; the second as RE 5 or 6 failing with residual failures differing between
geometries; the third as identity islands resolving less than exploitable ones at every rate. Gemini's as: cure at
εN = 0.1 < 0.4 iff no DefectBot-like (constant or near-constant) predator is in the top three by mass.

8. **RE (added 2026-10-15 with the RS's criterion), the admissible window.** Per island, cures / drift colonizations
   ≈ 2·s·N·μ_pred; a window exists (cures with no drift colonization at some εN ≤ 0.1) iff the operational predators'
   prior mass μ_pred ≳ 1/(2sN), which holds if DefectBot-like predators are among them. *Falsifier:* at every rate
   either no cure or at least one drift colonization per 64 islands over the horizon, with μ_pred ≥ 1%.

## My predictions (with falsifiers)

M1. **The target is strict.** Among stored runs at N ≥ 200 (S-nonself, proportional, ablation), fewer than half of the
    universal-open runs at generation 2,000 are universal-on-target. *Falsifier:* ≥ 0.75 of them on target.

M2. **The commonest non-identity rival is closed and open.** Among non-identity target-relative rival islands at
    generation 2,000 in the stored failing runs, ≥ 0.5 are closed-open (S-guarded holders bridged to the target through
    FairBot-type units) and < 0.5 are exploitable, so RE 1 fails on the target definition. On the stored-classifier
    rivals (certificate-reading rivals such as the anti-punisher), ≥ 0.6 are exploitable. *Falsifier:* exploitable
    ≥ 0.8 on the target definition, or < 0.4 on the stored-classifier rivals.

M3. **Predator mass.** For the anti-punisher in the RE's example, μ(Pred) is in [0.005, 0.1], DefectBot is not among
    the predators, and the certified-table count exceeds the accessible count by ≥ 10× in units. *Falsifier:*
    μ(Pred) < 0.001 or DefectBot a predator.

M4. **Cure rates (B1, exploitable rival islands, matched-branch differences).** Cure by 10,000 generations ≈ 1 −
    exp(−2,600·εN·μ(Pred_X)) within ±0.2 pooled per rate, i.e. at εN = 0.1 ≥ 0.6 where μ ≥ 0.004; ≥ 0.7 of cures by a
    predator step; ≤ 0.05 of exploitable rival islands resolve in the ε = 0 branches. *Falsifier:* pooled cure at
    εN = 0.1 outside the band, or fewer than half of cures by predator steps.

M5. **Closed rivals.** Identity islands resolve ≤ 0.02 at every rate (and 0 at ε = 0); closed-open rival islands
    resolve ≤ 0.15 at εN = 0.1 by 10,000 generations. *Falsifier:* identity ≥ 0.1 at any rate, or closed-open
    ≥ 0.3 at εN = 0.1.

M6. **No losses, but shadows.** Target-island losses ≤ 0.002 per island at εN ≤ 0.1; at least one drift
    colonization of a target island (a neutral FairBot-family shadow) per run in some cell at εN = 0.1, so the RS's
    "drift should never colonize" fails at εN = 0.1 over 10,000 generations at 64–128 islands. *Falsifier:* losses
    ≥ 0.01, or zero drift colonizations in every εN = 0.1 cell.

M7. **Sponsored donor.** Identity islands ≤ 0.03 in every A cell (below S-nonself's 0.03–0.13 at N ≥ 200) but not
    ≤ 0.01 everywhere; universal-on-target in [0.35, 0.8] at 10,000 in every A cell, above S-nonself's and above
    C-donor's at every cell; the remaining failures mostly closed-open rivals. The empty-list control is within ±0.15
    of S-nonself on universal-on-target. *Falsifier:* universal-on-target ≥ 0.85 everywhere (RE 5 holds) or ≤ 0.2
    somewhere; or the empty control ≥ 0.25 above S-nonself.

M8. **B3 (sponsor + rain at εN = 0.1)** is universal-on-target in [0.5, 0.9] at both geometries and within +0.15 of A
    at the same geometry. *Falsifier:* ≥ 0.95 at both (RE 6 holds) or below A's value by more than 0.1.

M9. **B2 natural.** At εN ≤ 0.1, rain from generation 0 changes universal-on-target by ≤ 0.15 against the paired ε = 0
    runs at 10,000 (it removes exploitable rivals only, which are a minority); at εN = 1 identity islands do not
    increase. *Falsifier:* a change ≥ 0.3 at εN ≤ 0.1.

M10. **Per-arrival probabilities.** A predator arrival on its rival island colonizes with probability within a factor
    2 of the exact ρ ≈ 0.26 (not 2s = 0.6); a neutral arrival with probability within a factor 3 of 1/N.
    *Falsifier:* outside those factors at N = 200.

M11. **Injection assays.** The injected predator colonizes its rival island in ≥ 0.15 of replicates and its island
    ends on target in ≥ 0.8 of those; the matched non-predator colonizes in ≤ 0.02. *Falsifier:* predator colonization
    < 0.1 (establishment failure, not arrival scarcity, limits the cure).
