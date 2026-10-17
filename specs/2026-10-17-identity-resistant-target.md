# Spec: an identity-resistant target: narrowing the PrudentBot network to members identity cannot exploit, 2026-10-17

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol and gemini-4-argon; to be run by an Opus subagent.
Follow-up to RESULTS "Removing rival networks", "Cliques on a Pangaea" and "Annealed mutation", and DEFERRED 1 (the
RE's operating hypothesis after the 15-minute window: narrow the target). REJECTED.md checked: nothing re-opened
(the mass-matched ablation in "Provenance" moved clique mass to the prudent core; this moves exploitable *target* mass,
a different intervention, and says so).

## Why

Two failure channels run through target members that identity holders exploit (165 of the 235 target units; e.g.
`if(CHK(them,^D,D),C,D)` and `if(CHK(them,me,C),C,if(CHK(them,them,C),C,D))`): under rain they drift in as neutral
shadows and identity migrants invade through them; and a single *selected* TwinD arrival on an island held by one took
a whole 8-island run in 45 generations. At ε = 0 identity's main channel is different: clique islands establish from
the seed on their own islands, which fission–fusion erased (40/40 universal-open on the Pangaea test). So the
hypothesis is a two-part fix: fission–fusion for the seed's cliques, a resistant target for the entry channels.

## Design

**Machinery.** `src/pangaea*.py` (fission–fusion), `src/annealed*.py` (rain), `src/removing_rivals*.py` (target,
predators, drift classifier), `src/realizable_scaling*.py`, `src/provenance*.py` (import only). r = 100 per Moran
event; calibrated mN; cached tables copied read-only or rebuilt; reproduction verified first.

**Static (notes §1, before any cell).** Partition the 235 target units into *exploitable* (some identity holder in the
prior's TwinD family, or any identity unit with positive prior mass, cooperates-with-and-is-cooperated-by asymmetry:
the target unit cooperates with it while it defects) and *resistant*; state the syntactic signature of resistance
(cooperation guarded by a certified check of cooperation with oneself) and whether it is exactly that; report each
class's prior mass and how often each holds islands in the stored runs.

**Priors.** **L** (the length prior); **R-move**: the exploitable target units' prior mass moved to resistant target
units in proportion to their mass (a counterfactual: what a prior that points at resistant members buys);
**R-proportional control**: the same mass moved to all non-identity units in proportion (separates "less exploitable
mass" from "more resistant mass").

**Cells** (S-nonself, 20 runs, paired founders across priors):
- **ε = 0, fission–fusion:** 128 islands of 100 for 200 generations, then merged into one population of 12,800, under
  L, R-move and the control; with and without the sponsored PrudentBot founder. Horizon 2,000 after the merge.
- **ε = 0, islands:** (200, 64) under L, R-move and the control (does narrowing help without the merge?).
- **Rain:** the annealed schedule at K = 3 on (800, 8) and (1,600, 8), and constant rain at the same total, under L and
  R-move (the identity-prey channel and shadow takeovers of target islands).

**Statistics.** Universal-on-target (uot) and universal-open; identity share and identity islands; identity takeovers
of target islands by drift (shadows) and by selection (prey); the target's own drift to members PrudentBot would not
certify (4/34 runs on the Pangaea test); scramble failures; island efficiency (reported, never selected on).

**Scale guard.** ≤ 3 workers; the per-root run uses up to 3: check `ps` first; one job per process. Drop order: the
control under rain, then N = 1,600 rain, then the sponsored founder in fission–fusion.

## Required outputs

`src/identity_resistant.py` (+ `_run.py`, `_report.py`), `tests/test_identity_resistant.py` (the partition on the RE's
two examples; mass moves preserve totals; reproduction), `notes/identity-resistant.md` (§1 static, hand predictions;
§2 costs), `runs/identity-resistant.md` and `.json`, predictions committed before any counted cell, and the usual
hand-back.

## RE predictions (with falsifiers)

1. **Resistance is mostly a syntactic property** [revised after review: resistance is defined semantically; the
   syntax is a test of it]: the certified self-cooperation guard is sufficient for resistance, and ≥ 0.9 of resistant
   units carry it; exceptions are listed. *Falsifier:* < 0.7 carry it, or any guarded unit exploitable.
2. **Fission–fusion is universal-open in ≥ 0.95 of runs under every prior, and universal on target (235) in ≥ 0.9 with
   the sponsored founder under L** [revised after review: the Pangaea result was universal-open, and open rivals are not
   identity prey, so the sponsor carries the target]. *Falsifier:* universal-open ≤ 0.8, or sponsored uot under L ≤ 0.7.
3. **R-move alone on islands does little at ε = 0:** (200, 64) uot within 0.1 of L, because identity's main channel at
   ε = 0 is the seed's own islands. *Falsifier:* a gain ≥ 0.25.
4. **R-move closes the prey channel under rain** [revised after review: the combined bound and the cross-regime uot
   claim are dropped]: selected identity takeovers of target islands per identity arrival fall to ≤ 0.2 of L's.
   *Falsifier:* ≥ 0.5 of L's.
5. **The control does not do it:** the R-proportional control's identity takeovers under rain stay ≥ 0.5 of L's.
   *Falsifier:* ≤ 0.2.
6. **Counter-predictions registered.** *Sol:* semantic resistance is not captured by the syntax; under rain direct prey
   takeovers decline but the combined bounds fail; the sponsor matters materially and unsponsored R-move can be
   universal-open without being on target. *Gemini:* semantic resistance strictly contains the syntactic signature,
   violating it on > 10% of resistant units; R-move may work by founder boosting rather than channel closing.

## Amendments after review (gpt-6.1-sol and gemini-4-argon; these supersede the text above where they conflict)

1. **R-move is a diagnostic, not a design.** Moving prior mass is surgery on the mutation prior, which the RS's standing
   decision keeps at the length prior (2026-09-30); it is kept as a counterfactual that locates the leak. The realizable
   claim is judged on arms under L only: fission–fusion with and without the sponsored PrudentBot founder, and rain under
   L. The RS's later research question (a prior that points cheaply at good programs) is the bridge if R-move shows a
   large effect.
2. **Controls under rain kept.** The rain cell at (800, 8) runs all three priors (L, R-move, R-proportional) under the
   annealed schedule and under constant rain; the drop order becomes: N = 1,600 rain first, then the sponsored founder
   in the island cells; the (800, 8) three-prior comparison is never dropped.
3. **Scoring.** The original 235-unit target is frozen for scoring (uot₂₃₅), and the resistant-target score (uot₇₀) and
   the occupancy of resistant versus exploitable holders are reported beside it for every prior.
4. **Coupling.** Each founder slot carries one uniform draw mapped through each prior's inverse CDF, so priors are
   paired with correct marginals; founding-prior and rain-prior interventions are separated (rain draws from the same
   prior as the founders in each arm, reported).
5. **Resistance defined semantically.** A target unit is exploitable if some identity unit (in the frozen challenge
   set: the prior's identity units plus zero-prior units reachable by production) is cooperated with by it while
   defecting against it, judged on executed, fuel-limited outcomes as well as the ideal table; the syntactic guard is a
   test of this definition (prediction 1).
6. **Mechanism assays.** Forced TwinD challenges into established resistant and exploitable holders, with neutral
   fixation baselines; takeovers reported per identity arrival and per target-holder generation as well as in total;
   per-founder scramble establishment of resistant versus exploitable units (removing the latter may raise scramble
   failures); drift from resistant islands to *any* unconditional cooperator under rain.
7. **Rain timing.** The annealed schedule of "Annealed mutation" (onset at 200, t₀ = N/2, cut at 10,000, 2,000-generation
   chase); constant rain over the same window; cumulative exposure by program class reported.
8. **Statistics.** Paired differences with exact intervals, runs as clusters, predeclared supported / contradicted /
   inconclusive regions; only the decisive comparison is extended if inconclusive.
