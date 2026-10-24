# Spec: zero-tolerance and sampling inspectors, 2026-10-24

Status: draft by the RE; reviewed by gemini-4-argon (folded [after review]), then gpt-6.1-sol (`--mode amended`, folded [after second review]); to be run
by a Sonnet subagent. The RS (2026-10-24) delegated the inspection thread to the RE ("I'd like u to manage that thread
autonomously"). Follows RESULTS "The inspection game's enforcer and its shadow". REJECTED.md checked: the cheater rain
and the prudent-inspectee boost were rejected as remedies; this tests different programs and re-opens nothing.

## Why

In the inspection chain the exact responsive inspector `cr(THEM(ME))` is eroded at N ≥ 10⁴ by light cheaters
(inspectee mixers cheating with probability q < 1/4, against whom not inspecting is its strict best reply) and by
exploiters of its bounded read; removing those 0.3% of the prior lifts π(E) at N = 10⁵ from 0.047 to 0.81. Two
inspector programs might close that gap without removing anything from the prior:

1. **Zero tolerance** `zt(THEM(ME))`: inspect iff the inspectee cheats against me with positive probability (exact
   read). Against a light cheater it inspects and pays −1 instead of −4q, so it gives up payoff (the inspection
   analogue of PrudentBot, which defects against CooperateBot), but light cheaters lose −3q·… against it and cannot
   invade.
2. **Sampling responder** `sr_k`: inspect iff any of k simulated draws of the inspectee against me cheats (k ∈ {1, 4,
   16}); detection probability 1 − (1 − q)^k, so it responds to light cheaters probabilistically and its read cannot
   be gamed through the bounded-read path that `cr` exposes.

## Design

[After review] The stored partial ablations are benchmarks for what each fix might do ([after second review] not ceilings:
deleting mutants and adding a program change different rates) (chain, c = 0, π(E) at N = 10⁴ / 10⁵): removing
only the non-reading light cheaters gives 0.396 / 0.239; removing only the bounded-read exploiters gives 0.174 / 0.036;
removing both gives 0.636 / 0.811. Zero tolerance addresses the first group only (benchmark about 0.24 at N = 10⁵). The bounded-read exploiters work because `cr` falls back to *not inspecting* when its read of the inspectee
times out; a **suspicious default** (inspect on timeout, FairBot's "defect unless proven") addresses the second group.

Base: the inspection game, n = 8, the exact arm and conventions of `specs/2026-10-24-inspection-shadow.md`, reused by
import from `src/inspection_shadow*.py` and `src/mixed2*.py` (no edits). Arms add the new inspector programs to the
grammar with matched prior mass (each enters at the prior mass `cr(THEM(ME))` has, taken proportionally from other
inspector classes; a matched control adds the same mass to `cr(THEM(ME))` itself):
- **ZT:** `zt(THEM(ME))` added; **SUS:** `cr_s(THEM(ME))`, the exact responsive inspector with the suspicious default,
  added; **ZT+SUS:** `zt_s(THEM(ME))`, zero tolerance with the suspicious default, added; **SR:** `sr_k` added for
  k ∈ {1, 4, 16} (separate arms); **control:** the same mass added to `cr(THEM(ME))`. [After review] Every arm adds the
  same total mass, split equally among its added programs, so no arm gains responsive-inspector mass over another.
- [After review] `sr_k` is stochastic: an inspectee reading it sees its exact action distribution (`cr` semantics), and
  payoffs are computed exactly over its draws (no Monte Carlo); it stops at the first cheating draw, so on path against
  compliant inspectees it pays all k levels. R is defined per arm to include the arm's added inspectors.
  [After second review] Each `sr_k` draw is an independent simulation with its own fresh coins, the same per-draw fuel
  and depth budget as `cr`'s read, and the same timeout action as the arm's default (not inspecting, or inspecting in
  the suspicious variant `sr_k,s`); exact averaging does not make a simulated opponent terminate, so the stored
  bounded-read exploiters are tested against every new inspector by hand. Under independent draws a light cheater with
  probability q earns q(1 − 4p) with p = 1 − (1 − q)^k, so it still profits when q < 1 − (3/4)^{1/k} (about 0.018 at
  k = 16); the notes list which grammar mixers fall below each threshold.
- [After second review] *Comparator:* an unconditional inspector (always I) at the same added mass, to separate
  detection from commitment. *Reporting:* resident-specific per-mutant fixation and exit rates (not only aggregates
  over a per-arm R), aggregates under fixed reference weights and under each arm's own stationary weights;
  behavioural-class membership and aggregated mutation mass of every added program; realized read costs and timeout
  frequencies; the chain's entry and exit scaling and support. Every contrast uses the newly computed control, with
  the stored 0.047 as context only. Lottery results are finite-horizon: unresolved islands and late transitions are
  reported, intervals are run-level.
- Prices c ∈ {0, 0.01} (`zt` and `sr_k` charged like `cr`: one level, `sr_k` k levels).
- **Chain:** whole space (float32 storage with the previous run's checks), N ∈ {10³, 10⁴, 10⁵}, with the exit
  decomposition (light cheaters, bounded-read exploiters, shadow, others) and P(E), P(R).
- **Lottery:** (100, 64) and (400, 64), 40 and 20 runs, horizon 20N, paired founders.
- **Ablation reference:** the stored "light cheaters and bounded-read exploiters removed" chain (0.452 / 0.636 / 0.811).

## Predictions (the RE's; falsifiers in brackets)

1. *Zero tolerance closes the light-cheater exit, and only that.* In the ZT arm at c = 0, the light-cheater exit hazard
   from R falls by at least 10× against the control at N = 10⁴ and 10⁵, and π(E) at N = 10⁵ lies between the control
   (0.047) and the light-cheaters-removed reference (0.239): at least 0.1 [below 0.07]. *Counter-prediction
   (gemini-4-argon), registered:* the bounded-read exit absorbs the flow and π(E) stays below 0.10.
2. *The suspicious default closes the other exit.* ZT+SUS reaches at least 0.5 at N = 10⁵ (both-removed reference 0.811)
   [below 0.3]; SUS alone lies near the reading-exploiters-removed reference (within 0.1 of 0.036) [above 0.2].
   *Counter-prediction (gpt-6.1-sol), registered:* targeted exit rates fall more reliably than stationary inefficiency;
   the flow moves to shadows and other routes, so 0.5 is overconfident.
3. *Sampling.* `sr_16` raises π(E) at N = 10⁵ above the control by at least 0.1; `sr_1` does not [`sr_16` gains under
   0.05]. *Counter-prediction (gpt-6.1-sol), registered:* sampling leaves a low-q escape channel (q below about 0.018
   at k = 16), so its benefit depends on the grammar's q grid.
4. *Price.* At c = 0.01, `sr_16` pays 16 levels per read on path and loses to `zt` (one level) [`sr_16` at least matches
   `zt`].
5. *Lottery.* Efficient islands change by less than 0.1 in every arm at (100, 64), since the lottery was not limited by
   light cheaters [any arm moves by more than 0.15].

## Required outputs

- `src/zero_tolerance.py` (+ runner, report) importing the existing modules; no existing file edited.
- `tests/test_zero_tolerance.py`: `zt` and `sr_k` payoffs against light cheaters and constants by hand; the matched
  prior; the exit categories.
- `notes/zero-tolerance.md` (§1 hand table before code; §2 deviations).
- `predictions/2026-10-24-zero-tolerance.md`, before any counted cell.
- `runs/zero-tolerance.md` and `.json`, `runs/zero_tolerance/` (small files).
- Hand back RESULTS, REJECTED, THEORY and NOTATION drafts; do not edit the shared docs.

**Budget and scale guard.** The whole-space chain matrix needs several GB; other subagents are running: check `ps` and
free memory before each chain job, run at most one chain job at a time and at most 2 workers in all while others are
alive. One job per process; no `multiprocessing.Pool`; one background wait per batch that exits at completion and fires
if the log stops changing for 2 hours; never poll periodically. Cut order (disclose): (400, 64), N = 10⁵ at c = 0.01,
`sr_4`.
