# Spec: confirming failure pricing as the default compute charge, 2026-10-25

Status: draft by the RE; reviewed by gemini-4-argon (folded [after review]), then gpt-6.1-sol (`--mode amended`, folded
[after second review]); to be run by a Sonnet subagent. The RS (2026-10-25), on RESULTS "What compute should cost": "Next steps sg, happy to make this our working
hypothesis / default compute charge." DEFERRED 16 records the adoption and a circle-back after this run.

## Why

In "What compute should cost", failure pricing (A: P_fail per timed-out read, a raw payoff charge) at P_fail = 0.1 is
the only cell meeting all three targets (RPS net exploitability ≤ 0.10, inspection efficient islands ≥ 0.60, PD
universal-open runs ≥ 0.70), and only on pooled PD runs (35/40, the 20 registered runs undetermined). Inspection at
(400, 16) was undetermined (0.650 [0.450, 0.850], 20 runs), A at 1 and 10 met RPS's net target by mutual non-play, not
mixing, and the registered PD target is cost-blind. This run classifies the default as confirmed, refuted or unresolved on fresh runs ([after second review] confirmed
only if all three targets are met with the PD scored cost-inclusive; refuted if any game fails; unresolved otherwise), maps the
band's width around 0.1, and scores with the charge included.

## Design

Code: `src/pricing_rules*.py` as merged (import; no existing file edited). Every counted run uses run indices not used
before (fresh founders), so this is a confirmatory sample, not a pooling of the exploratory one.

- **PD** (world K, S-nonself, (100, 64), [after second review] stopping as in the stored cells, the universal-open
  verdict required to hold over the last 500 generations, censored runs kept and reported): A at 0.03, 0.1, 0.3, 1, 10 and the zero price, 40
  fresh runs each.
- **RPS and inspection** (L_T with the tape, (100, 64), 40 runs, generation 2,000): A at 0.03, 0.1, 0.3, 1, 10 and the
  zero price, fresh runs ([after review] 1, 10 and 0 added so every confirmatory comparison is on fresh runs); at
  (400, 16): A at 0.1 and the zero price, 40 runs each.
- [After review] **Stakes-normalized point control** (cut first; one point, not a band): A_s, P_fail = 0.1 × each game's payoff range (RPS 0.2,
  inspection 0.5, PD 0.3 by the notes' ranges), at (100, 64), 40 fresh runs per game, to test whether the band survives
  normalizing the charge by stakes rather than raw payoff.
- **Scores.** The three registered targets as before (met / failed / undetermined by run-level 95% intervals), plus:
  - *RPS by mixing:* gross exploitability ≤ 0.10 and forfeits ≤ 0.05 (so that mutual non-play cannot meet the target);
  - *PD cost-inclusive:* a run counts if it is universal-open and its end-state charge per play is at most 0.1 of the
    PD payoff range ([after review] end-state charge = the encounter-weighted mean charge per play over the final
    generation's population; the cumulative run-average charge and the mean charge per play over generations 1–200,
    the scramble, are reported beside it; the payoff range's value is fixed in the notes before code) (scored as a separate column, and also for the stored F, F+A, B and B-own cells from the stored rows,
    without rerunning them);
  - [after second review] *inspection net of charges:* each island's net payoff vector (game payoffs minus the charges
    each role paid per play), efficient if both net means are ≥ −0.05 as in the gross criterion, frozen in the notes;
  - [after review] the by-mixing and cost-inclusive scores (and inspection net of timeout charges) applied to every
    stored row of "What compute should cost" at no simulation cost, in one retrospective table (marked unavailable where a stored row lacks the needed charge
    or encounter fields);
  - the identity of the modal programme per island (RPS, inspection), to see whether the guarded mixer `PRR` holds
    RPS on the fresh runs.

## Predictions (the RE's; falsifiers in brackets)

1. *The default holds.* On fresh runs A at 0.1 meets the RPS and inspection targets at (100, 64), and the cost-inclusive
   PD is met or undetermined with a point estimate ≥ 0.75 (40 runs cannot separate 0.85 from the 0.70 line reliably;
   that outcome classifies the default as unresolved, not confirmed) [any game failed; or the PD undetermined with a
   point estimate below 0.75]. *Counter-prediction (gpt-6.1-sol), registered:* inspection at (100, 64) is
   undetermined, its interval straddling 0.60.
2. *Inspection at larger geometry.* At (400, 16) A at 0.1 is met or undetermined with a point estimate ≥ 0.60, and
   within 0.10 of the zero price [failed, or more than 0.10 below the zero price].
3. *Band width.* RPS fails at 0.03 (simulators survive, as at 0.01) and is met by mixing at 0.3; inspection and the PD
   are met or undetermined at every level from 0.03 to 0.3 [RPS met by mixing at 0.03, or failed at 0.3; or inspection
   or the PD failed at any level from 0.03 to 0.3].
   *Counter-prediction (gemini-4-argon), registered:* 0.3 is already costly enough for guarded reads during the
   scramble that by-mixing is borderline or fails at 0.3.
4. *Mixing, not non-play, at 0.1.* At P_fail = 0.1 the RPS by-mixing score is met and `PRR` is the modal programme on at
   least 0.8 of islands; at 1 and 10 the by-mixing score fails [by-mixing fails at 0.1, or is met at 1 or at 10].
5. *Cost-inclusive PD.* A keeps its PD verdicts with the charge included (the cost-inclusive count within 2 runs of the
   cost-blind count at every A level), and its end-state charge per play is below 0.01 of the range in every run;
   stored F at 10⁻² fails it [A's count drops by more than 2 at any level; or any A run's end-state charge ≥ 0.01 of
   the range; or F 10⁻² passes]. *Counter-prediction (gpt-6.1-sol), registered:* terminal charges may be tiny while
   the scramble's charges change which network establishes.

## [After second review] Further outputs and limits

- Paired price-minus-zero differences with intervals, using matched fresh founder sets where the kernel allows.
- Timeout counts by programme, stage (scramble, later) and nesting depth, with who pays for a nested failed read.
- Support and transition summaries per cell, not only modal programmes.
- Seed derivation documented; imported caches and code hashed; a check that the caches are semantic accelerators,
  not price-dependent tables.
- Conclusions restricted to the tested geometries (no island-size or large-N claim), and to these grammars, caps and
  world K.

## Required outputs

- `src/failure_pricing_confirm.py` (runner, report), importing the merged pricing code; no existing file edited.
- `tests/test_failure_pricing_confirm.py`: the new scores on hand-built rows (forfeits, charges); a fresh-index guard
  (no run index reused from the stored cells); one stored cell reproduced draw for draw.
- `notes/failure-pricing-confirm.md` (§1 before code: the score definitions with hand examples; §2 deviations).
- `predictions/2026-10-25-failure-pricing-confirm.md` before any counted cell, with the RS's message first.
- `runs/failure-pricing-confirm.md` and `.json`, `runs/failure_pricing_confirm/` (small files).
- Hand back RESULTS, REJECTED, THEORY and NOTATION drafts; do not edit the shared docs.

**Budget and scale guard.** Another subagent is running: at most 2 workers while it is alive, 3 after. Check `ps` and
free memory before each batch. One job per process; no `multiprocessing.Pool`; one background wait per batch that exits
at completion and fires if the log stops changing for 2 hours; never poll periodically. The PD kernel needs the
untracked world-K caches (`runs/provenance/static`, `runs/detectors/K/…`): copy them read-only from the main checkout
into the worktree, never commit them. Cut order (disclose): A_s, PD at 0.03 and 0.3, RPS and inspection at 0.03.
