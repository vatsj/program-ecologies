# Spec: the inspection game's enforcer and its shadow, 2026-10-24

Status: draft by the RE; reviewed by gemini-4-argon (folded [after review]), then gpt-6.1-sol (`--mode amended`, folded [after second review]); to be run
by a Sonnet subagent. Requested by the RS (2026-10-24, "worth the confirmation"). Follows RESULTS "Mixed actions in
two-role games". REJECTED.md checked: nothing re-opened.

## Why

In the inspection game with both roles reading exactly, the seed lottery's modal island (0.65 at N = 100) is the
efficient outcome: a responsive inspector `cr(THEM(ME))` (inspect iff the inspectee would cheat) over compliant
constants. The whole-space chain does not hold it (inspector payoff −0.47 at N = 10⁴). The RE's reading is the PD's
mechanism: against compliant inspectees the never-inspecting constant `N` is a payoff twin of the responsive
inspector, drifts in neutrally, and is then exploited by cheaters `K`. This spec confirms or refutes that mechanism,
measures how it scales, and tests the PD's remedies.

## Design

[After second review] Two sets are distinguished throughout: **E**, the payoff-efficient states (both mean payoffs ≥
−0.05), and **R ⊂ E**, those where responsive enforcement is present (`cr(THEM(ME))` or another responsive class holds
the inspector role). Replacing `cr` by its twin `N` against `C` at c = 0 leaves E and enters E \ R; the efficiency exit
is what follows. At c = 0.01 `cr` pays to read and `N` does not, so `N`'s entry is selection, not drift: the charged
costs against `C` are tabulated and the entry classified accordingly.

Base: the inspection game, grammar (n = 8), exact arm, price c ∈ {0, 0.01}, chain and lottery of
`specs/2026-10-23-two-role-mixed.md`, reused by import from `src/mixed2*.py` (no edits).

1. **Exit decomposition (chain).** On the whole-space chain [after review: with the twin-expanded distribution,
   IMPLEMENTATION §4, since the mechanism is twin drift] at N ∈ {10², 10³, 10⁴, 10⁵}: identify the efficient states
   (both mean payoffs ≥ −0.05); decompose the stationary flow out of them by (mutant role, mutant class, fate:
   neutral drift or strict invasion) and record each exit's rate and its slope in N, with strict invasions by
   reading inspectees (possible fakers through mutual-reading forfeits) tracked apart from constant `K`; record the
   paths back, and [after review] the branching ratio from the shadow-exploited state (`N`, `K`) into the efficient set
   against committed or mixing inspector states. [After second review] Report separately: per-mutant fixation
   probabilities, prior-weighted transition rates, conditional exit hazards from R and from E, and stationary flux;
   mean first-passage times and occupation of the detours (committed and mixing states) on the way back, since return
   probability alone omits trapping time. The chain is the log-domain whole-space solve with closure-seeded
   exploration and support diagnostics, cross-checked against the exploration audit's positive control (queue 57).
   Report P(E), P(R) and their odds slopes in N.
2. **Lottery size path.** The seed lottery at (N, I) ∈ {(100, 64), (400, 16), (800, 8)}, mN = 1, 40 runs (20 at the two
   larger sizes), paired founders, c ∈ {0, 0.01}, [after review] horizon 20N generations (2,000 / 8,000 / 16,000) with
   the generation-2,000 snapshot reported beside it, since neutral drift takes O(N) generations; [after second
   review] plus a crossed cell (400, 64) so that N is varied at fixed I, trajectories reported at common t and t/N,
   and the size results described as path effects where N and I move together: efficient islands, committed-and-compliant
   islands, and the shares of `cr` inspectors, `N`, `K`, `C` and reading inspectees.
3. **Remedies** (each a cell at (100, 64) and (400, 16), and a chain at N = 10⁴ where the remedy is a prior change):
   - *Cheater fringe:* constant rain of `K` into the inspectee role at εN = 0.05 per generation (the modal arm's
     defector fringe, which pruned the shadow); paired with a matched rain of `C` as the control.
   - *Prudent inspectees:* [narrowed after review] the prior mass of the behavioural class of inspectees that comply
     against `cr(THEM(ME))` and cheat against `N` multiplied by 10 (they punish the shadow); the notes list the
     boosted programs and their behaviour before any cell; matched control: the same mass added to `C`. [After second
     review] The boost is renormalized and stated exactly: in the lottery it changes the founder distribution, in the
     chain the mutation prior; the added mass is taken proportionally from all other inspectee classes, identically
     in the control.
   - [After second review] *Direct starts:* paired islands started at (`cr`, `C`) and at (`N`, `C`) at N = 100 and
     400, with K at mutation rate 0 and then a single K arrival at generation 100: shadow fixation, cheater
     establishment and recovery measured directly.
   - *Migration:* mN ∈ {0, 1, 10} at (100, 64).
4. **Controls:** the blind arm (no responsive inspector exists) at each lottery size; [after review] the
   inspector-only-reading arm (`exact_er`) at (100, 64) and in the chain at N = 10⁴, which separates inspectee reading
   that punishes `N` from mutual-reading effects.

## Statistics

[After second review] Every effect-size prediction is scored *held* at or above its threshold, *partial* for a positive
effect below it, *failed* at or below zero. Action frequencies and forfeits are reported beside every payoff-threshold
statistic, so that forfeit artefacts cannot pass as efficiency. Efficient-island share and its trajectory; exit table (rates, slopes, shares of total outflow); P(efficient) and odds
slope in the chain; class shares; support, transitions and exits (CLAUDE.md rule 4); run-clustered intervals.

## Predictions (the RE's; falsifiers in brackets)

1. *Mechanism* [restated after second review]. In the chain at N ≥ 10³ at c = 0, the largest conditional exit from R
   is neutral drift of `N` (or another never-inspecting class), with hazard slope in N between −1.2 and −0.8, and the
   largest exit from E is strict invasion of `K` into (`N`, `C`)-type states [the largest exit from R is a strict
   invasion, the drift hazard's slope is outside the range, or the largest exit from E is not a cheater's invasion].
2. *Scaling* [finite-range claim only, after second review]. The odds slope of P(E) over N = 10³–10⁵ is below 0.5
   [above 0.5]. No asymptotic claim is registered: odds growing at any positive slope still go to 1, and the limit is
   set by how the return times scale. *Counter-prediction (gpt-6.1-sol), registered:* P(E) rises with N if escapes
   scale as 1/N and return times stay bounded.
   *Counter-prediction (gemini-4-argon), registered:* a 1/N shadow exit with O(1) return makes P(efficient) grow with
   N; if the slope is low it will be because returns bypass the efficient state into committed or mixing states.
3. *Lottery path.* Efficient islands fall with N along the lottery path: below 0.5 at (800, 8) at c = 0 [at or above
   0.65]. *Counter-prediction (gemini-4-argon), registered:* larger N lengthens the founding scramble, so founding
   cheaters purge `N` more thoroughly and later neutral fixation of `N` is slower; efficient islands stay at or above
   0.5, or rise.
4. *Cheater fringe.* K rain raises efficient islands against the matched C rain by at least 0.1 at (400, 16) [no
   increase, or a decrease].
5. *Prudent inspectees.* ×10 reading-inspectee mass raises chain P(efficient) at N = 10⁴ by at least 0.1 against the
   matched C control [no increase].
6. *Price.* At c = 0.01 the reading inspectee pays to read while `C` complies free, so prudent inspectees help less at
   c = 0.01 than at c = 0 [they help as much or more].

## Required outputs

- `src/inspection_shadow.py` (+ runner, report), importing `src/mixed2*.py`; no existing file edited.
- `tests/test_inspection_shadow.py`: the twin relation of `N` and `cr(THEM(ME))` against `C`, the exit decomposition
  on a toy chain, the rain controls' matching.
- `notes/inspection-shadow.md` (§1 hand predictions of the exits before code; §2 deviations).
- `predictions/2026-10-24-inspection-shadow.md`, before any counted cell.
- `runs/inspection-shadow.md` and `.json`, `runs/inspection_shadow/` (small files).
- Hand back RESULTS, REJECTED, THEORY and NOTATION drafts; do not edit the shared docs.

**Budget and scale guard.** At most 3 workers, capped by memory (the whole-space chain at 24,649 states took about
25 minutes per N); one job per process; no `multiprocessing.Pool`. Waiting: one background wait per batch that exits at
completion and fires if the log stops changing for 2 hours; never poll periodically. Another subagent (the
exploration audit) may be running: check `ps` before each batch and use at most 2 workers while it is alive. Cut order
if needed (disclose): N = 10⁵, (800, 8), the crossed (400, 64) cell, mN = 10, c = 0.01 remedy cells.
