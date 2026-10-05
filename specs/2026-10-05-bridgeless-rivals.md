# Spec: bridge-less rivals, their prior mass in n, and mediation before loss at N ≥ 200, 2026-10-05

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-05-bridgeless-rivals-gpt-6.1-sol.md`) and revised; changes
marked [after review]. To be run by an Opus subagent. Follow-up to RESULTS "A path in (N, I, mN)" (DEFERRED 1,
"would settle it"). Finite-cutoff screening plus one enriched lottery with a small scaling panel; it bounds, it does
not settle, the asymptotic claim [after review].

## Why

On the calibrated boundary path, rival networks resolve iff the prior *bridges* them: a class mutually cooperating
with both rivals absorbs the minority polynomially, and its scramble survival becomes certain as I grows. The pair
whose rival is P\* never resolved at N ≥ 200, and the bridge of the other pair is P\*'s prey (P\* defects on it while
it cooperates with P\*), so P\* has no bridge in that language. "Metapopulation universality along the I ≫ N path"
now rests on two unmeasured numbers: the prior mass of rival establishers of the FairBot pair that have *no*
bridge as the cutoff grows, and how often such a rival establishes and holds islands in natural runs at N ≥ 200
(1,000 natural runs sampled none). [after review] The useful object is not a binary bridge label but the
**probability of successful mediation before rival loss or the horizon**, which depends on aggregate bridge mass,
demographic survival of bridge founders, and migration; this run measures its ingredients at finite cutoffs and
sizes.

## Definitions [after review]

- **Rival** of A = {FairBot, `BOX1(THEM(ME))`}: an establisher class R (self-cooperates, defects on D) that mutually
  defects with A.
- **Pairwise bridge** of (A, R): a class B that mutually cooperates with both A and R. Since all three are
  self-cooperators earning R against each other, two-type fixation between B and either is neutral; "exploitation" is
  not possible inside this table. **Prey** of R: a class that cooperates with R while R defects on it (the orientation
  the island-path run called "the bridge exploited by P\*"). **Mediator**: a class that is neutral or better against
  both A and R in pairwise fixation at N = 200 without being a pairwise bridge (multistep compatibility).
- **Bridge mass** of R: the total μ mass of its pairwise bridges; **safe bridge mass**: of those that are
  establishers. The threshold τ on the heaviest bridge is a *sensitivity parameter*, swept over
  {0, 10⁻⁵, 10⁻⁴, 10⁻³}; "literally bridge-less" (τ = 0) is reported separately from every threshold.
- **Compatibility connectivity**: whether A and R are connected in the mutual-cooperation graph over establishers,
  and the shortest path length.
- Masses are reported normalized (within the cutoff) and unnormalized (raw units of the infinite prior), with the
  omitted-tail bound < 1/(2n), and with a note on classes whose equivalence changes across cutoffs.
- **q** (holder form, as in the island-path run): horizon holders of local ancestry relative to the paired m = 0
  reference. **Both P(C,C) objects**: island-level (realized) and counterfactual cross-island under uniform mixing;
  separation threatens the second, not the first, and the write-up says so.

## Design

**Static screening (n = 9, 12, 15 if the class cache fits; report sizes).** For every rival R of A: μ mass; its
pairwise bridges with their masses, the heaviest, the total and the safe total; its prey among A's network and the
bridges; mediators; connectivity; one-migrant fixation of R into A and A into R at N = 200. Classify rivals by τ
and report the bridge-less mass, the bridged mass and their ratio at each τ and n; also for the probe-readers
`BOX(THEM(^C))`, `BOX1(THEM(^C))` for comparison. Report which rivals *gain* a bridge between cutoffs.

**Enriched lottery** (N = 200, I = 64, boundary mN = 1.09, n = 9, horizon 10⁵, holder rule, hazards per
minority-island-generation with the exposure reported so that a zero-loss cell gives its upper bound; 100 runs per
cell; runs are the independent units) [after review: several matched rivals, sparse seeding, bridge removal]:
- (a) *Forced rival, dense:* one copy of the rival on every island, the rest iid, for the three heaviest bridge-less
  rivals (τ = 10⁻⁴) and the three heaviest bridged rivals, matched on μ mass where possible;
- (b) *Forced rival, sparse:* one copy on 1/4 of the islands, same six rivals;
- (c) *Bridge removed:* the heaviest bridged rival as in (a), with its pairwise bridges removed from the seed prior
  (mass renormalized; removed mass reported), to compare the same rival with and without its bridges;
- (d) iid control;
- (e) *Scaling panel* [after review]: (a) for the heaviest bridge-less and the heaviest bridged rival at (400, 64)
  and at (200, 256), 40 runs each, and at (200, 64) with horizon 3·10⁵, to separate metastability from permanence
  on the observed scale.
Per cell: the rival's establishment per island (local ancestry), bridge founders and their establishment and
subsequent mediation events, ever-separated and horizon-separated, the loss hazard with its decomposition
(replacement / absorption / capture) and exposure, the mediation-before-loss probability, both P(C,C) objects, q
against (d).
- (f) *Unconditional:* 3,000 natural runs at (200, 64) on the boundary, with the rival type, bridge presence and
  bridge fate recorded for every separation (ever and at the horizon).
Priority: static → (a), (d) → (c) → (b) → (f) → (e); ≤ 3 workers; stop where time runs out and say so.

## Required outputs

`runs/bridgeless-rivals.md` and `.json`, code in `src/bridgeless_rivals.py` (reusing `src/island_path.py`,
`src/rival_islands.py`, `src/seeds_in_n.py`; no core edits except bug fixes in their own commits), a predictions
file from the spec committed before any counted run (the static screening may precede it as an addendum, since the
forced rivals are chosen from it), the usual hand-back (draft RESULTS, REJECTED, THEORY §3 and DEFERRED 1 edits,
NOTATION, ≤ 5 lines, branch from `git branch --show-current`, commits).

## RE predictions (with falsifiers) [after review]

1. **More rivals gain bridges at larger cutoffs, so literally bridge-less mass (τ = 0) falls as a fraction of rival
   mass from n = 9 to 15, while the τ = 10⁻⁴ ratio stays in [0.1, 0.5]** (sol's expectation adopted; the RE's
   first-draft monotonicity rationale was invalid). *Falsifier:* the τ = 0 fraction rising from n = 9 to 15, or the
   τ = 10⁻⁴ ratio outside [0.05, 0.6] at n = 15.
2. **A dense forced bridge-less rival separates the archipelago; the same treatment with a bridged rival does
   not:** in (a) the bridge-less rivals give horizon separation ≥ 0.5 of runs and the bridged ones ≤ 0.1; in (c)
   removing the bridges raises the bridged rival's horizon separation to ≥ 0.4; in (b) sparse seeding gives
   separation between the two. *Falsifier:* a bridge-less rival in (a) with horizon separation ≤ 0.2, or (c) not
   above (a)'s bridged value by ≥ 0.2.
3. **Unconditional natural separation at (200, 64) is rare, and bridge-less rivals are over-represented among
   horizon separations:** 1–15 of 3,000 runs separated at the horizon; bridged rivals may appear among them when
   their bridge failed to seed or died in the scramble (sol's point), but the bridge-less share of horizon
   separations is ≥ 0.5 while their share of rival mass is ≈ 0.25. *Falsifier:* 0 of 3,000 (which only bounds the
   rate; reported as such), or bridge-less share ≤ 0.25 with ≥ 4 separations.
4. **Local P(C,C) is robust to the forced rival and cross-island P(C,C) is not:** island-level P(C,C) ≥ 0.95 in every
   cell, the counterfactual cross-island P(C,C) ≤ 0.8 in separated runs, and |Δq| ≤ 0.1 against (d). *Falsifier:*
   island-level P(C,C) < 0.9, or |Δq| ≥ 0.2.
5. **Scaling panel:** the bridge-less rival's separation persists at (400, 64) and at horizon 3·10⁵ (≥ 0.5), and
   the bridged rival's resolution is faster at (200, 256) than at (200, 64) (horizon separation lower). *Falsifier:*
   bridge-less horizon separation ≤ 0.2 at 3·10⁵.

The RS is invited to add predictions; the uncertain one is 1.
