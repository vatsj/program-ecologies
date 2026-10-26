# Spec: charging forfeits like failed reads, and the option to simulate exactly, 2026-10-26

Status: draft by the RE; reviewed by gemini-4-argon (folded [after review]), then gpt-6.1-sol (`--mode amended`, folded
[after second review]); to be run by a Sonnet subagent. The RS (2026-10-26), on RESULTS "Confirming failure pricing as the default compute charge":

> "I think a forfeit should be charged, esp if our simulations do so implicitly. That way, opponents have the option to
> simulate an opponent EXACTLY, potentially at cost to themselves. I further propose that those 2 costs be equal, since
> they seem like the same failure."

## Why

Failure pricing (A) charges P_fail per timed-out read call but nothing for a forfeit (a play whose root fuel runs out
without a timed-out call). In the confirmation run the default was confirmed at P_fail = 0.03 and 0.1, unresolved at 0.3
and refuted at 1 and 10, where RPS was held by mutual non-play (forfeits 0.50–0.63), and the engineer suspected the
uncharged forfeit (a prover forfeiting most plays took 0.06 of islands at 0.3). Under the RS's rule a forfeit costs the
forfeiter P_fail, the same as a timed-out read. Then a capped read that times out and an uncapped (exact) read that
runs out of fuel cost the same charge, so a reader may simulate an opponent exactly at the price of a possible forfeit.

## Design

Code: `src/pricing_rules*.py` and `src/failure_pricing_confirm*.py` as merged (import; no existing file edited).
Fresh run indices throughout (none used before). Scores and classification as in the confirmation run (RPS net and
by-mixing, inspection net of charges, PD cost-inclusive; confirmed / refuted / unresolved).

- **Rule A_f:** P_fail per timed-out read call and P_fail per forfeit, the forfeit charged to the forfeiting program in
  addition to the game's own forfeit payoff. Nothing else changes. [After review] One failure, one charge: an uncapped
  read that exhausts the root fuel is charged once, as a forfeit, never as a timed-out read plus a forfeit. The RS's
  equality is read as equality of the charges; the game's own forfeit payoff (RPS: −1 against any action) is part of
  the game and stays (flagged for the RS in the notes). [After second review] Accounting is by the root's trace: each distinct failure
  event in the root's own execution is charged once (every capped read call that times out, and the forfeit if the
  root fuel runs out, but an uncapped read that exhausts the root counts only as the forfeit); failures inside a
  simulated execution are not charged to anyone (the simulator pays only for its own read's outcome).
- **Exact simulators (arm X)** ([after second review] precisely: uncapped, shared-fuel simulators; the simulated
  opponent runs on the caller's remaining fuel less the reserved response steps, which can differ from its own root
  budget, and a private tape is drawn fresh, so "exact" means exact for deterministic opponents that finish within
  that fuel): the RPS and inspection catalogues gain the exact simulators, `run` with the caller's
  whole remaining fuel and no default (if it runs out the caller forfeits): RPS `SIMX` (play what beats the simulated
  action; [after review] the fixed steps of its own response are reserved before the rest of the fuel is passed to
  `run`, so a simulation that finishes always leaves enough to answer; [after second review] the same reservation for
  `SIMX_I` and `SIMX_E`), inspection `SIMX_I` (inspect iff the simulated inspectee cheats) and `SIMX_E` (cheat iff the simulated
  inspector does not inspect). [After review] Each splits its capped counterpart's template mass equally with it, so
  the constants' mass is unchanged (masses stated in the notes). [After second review] A sham-split control (X-sham:
  the same split, with the second half a behaviourally identical capped simulator) separates the capability from the
  halved capped seeding.
- **Cells.** RPS and inspection at (100, 64), 40 runs, generation 2,000: A_f at 0.03, 0.1, 0.3, 1, 10, with and without
  X; A (forfeits free) with X at 0.1 and 1, so that X is read under both rules. [After second review] Concurrent A cells
  (no X) on the same fresh founders at 0.1, 0.3 and 1, so that A_f is compared with A paired, not against the
  confirmation run; X-sham at 0.1 and 1 under A_f. PD (world K, S-nonself, (100, 64), 40
  runs): A_f at 0.1 and 1 (the PD grammar has no exact simulator; its forfeits are rare, so this checks only that the
  rule leaves the PD alone).
- **Outputs.** The confirmation run's tables for every cell; forfeits per play and who forfeits; the share of islands
  whose modal programme is an exact simulator, and the plays on which exact simulation finished, timed out of the root,
  or met a private tape; the charge per play split into timed-out reads and forfeits; [after review] for every forfeit
  of an exact simulator, the opponent's class.

## Predictions (the RE's; falsifiers in brackets)

1. *The leak closes.* Under A_f, RPS by mixing is met at 0.3 and 1 [not met at 0.3, or failed at 1].
2. *The lower end is unchanged.* At 0.03 and 0.1, A_f equals the concurrent A within an equivalence margin of 0.05 in
   each score (paired, run-clustered intervals) (forfeits are already 0 there): RPS by mixing
   met, inspection and the PD met [any of them not met at 0.1].
3. *High prices.* At 10, RPS by mixing is met or undetermined, not failed by non-play [forfeits above 0.05 by upper
   bound at 10].
4. *Exact simulation is rarely worth it in RPS.* Against a private-tape mixer an exact simulation predicts nothing (the
   simulated invocation draws its own tape), and against another reader it risks a forfeit, so `SIMX` is modal on fewer
   than 0.05 of RPS islands at every level under A_f [≥ 0.05 at any level].
5. *Exact simulation helps the inspector a little.* `SIMX_I` reads a compliant constant inspectee cheaply and exactly,
   so with X the inspection efficient share is within 0.10 of the A_f cell without X at every level, and `SIMX_I` is
   modal on at least 0.1 of inspector slots at 0.1 [outside 0.10, or below 0.1]. *Counter-prediction (gemini-4-argon),
   registered:* the capped simulator already reads a compliant constant within its cap at no charge, so `SIMX_I` has no
   advantage, is worse against deep inspectees, and is modal on fewer than 0.1 of inspector slots. gpt-6.1-sol agrees
   on the mechanism but expects its modal share to be prior- and drift-dependent.
6. *The PD is unaffected.* A_f at 0.1 and 1 keeps the PD met (cost-inclusive), and its count is within 6 of 40 of the
   confirmation run's A at the same level (a margin above sampling noise at these rates) [not met, or outside 6].
   *Counter-prediction (gpt-6.1-sol), registered:* a 3-run margin would be falsified by noise alone.

## [After second review] Further outputs and limits

- Paired payoff differences between capped and uncapped simulators against each opponent class, with charge totals
  and actual against simulated actions; recursive reader pairs tested at several nearby fuel budgets.
- Exact-simulator population mass beside modal-island frequency; uncertainty clustered by run; support and transition
  diagnostics; unresolved or high-forfeit cells extended to generation 4,000 before reading persistence.
- Whether reduced forfeiting comes with the removal of reader lineages, and whether RPS is carried by readers or by
  free randomizers (the coin's share).
- A finite-size mechanism test: no large-population or limit claim.

## Required outputs

- `src/forfeit_pricing.py` (+ runner, report), importing the merged pricing and confirmation code; no existing file
  edited.
- `tests/test_forfeit_pricing.py`: the forfeit charge on hand-built plays (a forfeit, a timed-out read, both, neither),
  including the single charge for an uncapped read that exhausts the root and the one-play net payoffs of `SIMX` against
  `SIMX` and `SIM` against `SIM` against the notes' hand table;
  the exact simulators' behaviour on hand-built opponents (a constant, a tape mixer, a reader that runs it out of
  fuel); A_f with no forfeits reproducing an A cell draw for draw; a fresh-index guard.
- `notes/forfeit-pricing.md` (§1 before code: the charge rule, the exact simulators' semantics and prior weights, hand
  payoffs of `SIMX` against the RPS catalogue at each level; §2 deviations).
- `predictions/2026-10-26-forfeit-pricing.md` before any counted cell, with the RS's message first.
- `runs/forfeit-pricing.md` and `.json`, `runs/forfeit_pricing/` (small files).
- Hand back RESULTS, REJECTED, THEORY and NOTATION drafts; do not edit the shared docs.

**Budget and scale guard.** Another subagent (encounter contracts) is running: at most 2 workers while it is alive, 3
after; check `ps` and free memory before each batch. One job per process; no `multiprocessing.Pool`; one background
wait per batch that exits at completion and fires if the log stops changing for 2 hours; never poll periodically. The
PD kernel needs the untracked world-K caches: copy them read-only (from `.claude/worktrees/agent-a77da45eb47c729f4`
if the main checkout lacks them), never commit them. Cut order (disclose): A with X at 1, the PD cells, A_f at 0.03.
