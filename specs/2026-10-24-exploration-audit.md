# Spec: exploration-cap audit of the published ε → 0 chains, 2026-10-24

Status: draft by the RE; reviewed by gpt-6.1-sol (folded [after review]), then gemini-4-argon (`--mode amended`, folded [after second review]); to be run
by a Sonnet subagent. Requested by the RS (2026-10-24, "Audit as subagent?"). Corrective: no new science unless a
published number changes, and every discrepancy is reported. Follows the methods finding of RESULTS "Mixed actions in
two-role games": an exploration-capped chain (≤ 1,500 states, relative-inflow threshold 10⁻¹⁰) gave a mean inspector
payoff of −0.009 at N = 10⁴ where the whole-state-space solve gives −0.47, because the efficient state sits on a large
neutral network of behaviourally equivalent spellings and the capped exploration never reached the states that drain
it. REJECTED.md checked: the 2026-10-05 solver audit (RESULTS "Solver audit") tested θ-pruning and lumped residents
against deep polymorphic traps and found the published arithmetic sound; it did not test exploration caps against the
whole monomorphic state space. This audit re-opens nothing; it extends that check.

## Object

Every published ε → 0 chain number in RESULTS.md whose state space was explored lazily or under a cap: a θ threshold
on stationary inflow (`chain.Chain.explore`), a log-θ threshold (`chain_log.LogChain.explore_log`), a `max_states` or
`max_rounds` cap, a top-k invader restriction, or closure-seeded exploration with a cap. Chains solved on a complete
state space (closure complete, or every monomorphic state and every reachable polymorphic state expanded) are listed
and excluded.

## Design

1. **Inventory.** Read every RESULTS section that reports a chain number (π, P(C,C), shares, exits, slopes) and the
   code that produced it. For each, record: the section, the cells, the solver and its exploration settings, whether
   the reported run hit its cap or threshold (from stored logs or by re-running the stored configuration), the number
   of behavioural classes K, and the size of the complete monomorphic state space ([after second review] ∏_r K_r over
   the roles, K for one population). Commit the inventory before any re-solve.
2. **Triage.** [Revised after review] Every chain with restricted exploration is eligible (payoff-twin networks are
   one demonstrated failure; rare gateways and deep polymorphic traps are others). Twin networks only set the
   *order*: cells whose grammar has large payoff-twin networks, then by the size of the claim they support (a
   headline number first). Cells not reached are marked *unresolved*, never passed.
3. **Re-solve, in stages** [after review], so that each change is attributable:
   - (a) reproduce the published number with the published code revision, evaluator, prior, N, seeds and tolerances
     (frozen and recorded);
   - (b) enlarge exploration with the construction unchanged: every active restriction enlarged together (cap 10×,
     threshold lowered by 10⁴, invader top-k widened to all invaders where the original restricted it, rounds 10×);
   - (c) where feasible by *measured* transition count and memory (not a state-count rule; a dense matrix at 50,000
     states is about 20 GB), the full monomorphic state space with the same transition model, then
   - (d) polymorphic states added from the stored set plus a multi-start replicator search (supports up to 6)
     [bounded after second review: started from the recurrent monomorphic classes, or the states covering 0.999 of π,
     and their invaders], each retained state tested against every admissible invader, and
   - (e) the twin-expanded distribution (IMPLEMENTATION §4), [after second review] applied only to cells published
     under the lumped chain; stages (a)–(d) keep the published transition model (lumped or twin-expanded), so the
     model does not change silently between stages.
   [After second review] **Isolating the culprit:** a cell that moves by more than 0.02 in (b) and cannot reach (c)
   is rerun with each restriction enlarged alone (the cap and threshold alone; the invader top-k alone). **Frontier
   outflow:** at (a) and (b), record the π mass on explored states with unexpanded transitions or at the cap; a cell
   with frontier mass above 0.01 is *unconverged* even if (a) and (b) agree.
   Each stage's change is reported separately. Results are labelled *monomorphic-complete, polymorphism-search-
   limited* when (c)–(d) ran, and *stable under this enlargement* when only (b) ran; neither is called converged.
   "Closure complete" earns exclusion from the audit only if the closure is over all permitted transitions.
   **Solver check:** where the jump-chain GTH solver of `src/mixed2*.py` is used, stationary weights are converted to
   occupancy by exit rates (holding-time correction), reducible or absorbing classes are handled separately, and the
   solver is checked against the original solver on identical state sets and rates (small instances).
   **Controls:** the mixed2 inspection exact cell (c = 0, N = 10⁴) as a positive control (it must reproduce −0.009
   capped and −0.47 complete), and a small complete-chain cell as a negative control (no change). On two tractable
   cells, several caps and exploration seeds are compared against the complete reference.
4. **Report.** For every cell and stage: published value, reproduced value, re-solved value, the difference, whether a
   stated verdict or headline changes; [after review] the support and transition structure (recurrent classes,
   newly opened escape paths, state and SCC counts, mutation-prior mass and twin multiplicities), since equal
   aggregates can hide different supports.

## Predictions (the RE's; falsifiers in brackets)

1. The inventory finds at least 10 chain results with capped or thresholded exploration [fewer than 10].
2. [Metric fixed after review] For probabilities and shares (P(C,C), π shares, island fractions) the difference is
   absolute; for payoffs it is divided by the game's payoff range; slopes are compared in their own units with the
   published precision. At least two thirds of re-solved cells in one-population DSL arms (PD, divide-the-dollar,
   modal arm) are within 0.02 on these scales [fewer than two thirds]. *Counter-prediction (gpt-6.1-sol),
   registered:* corrections track missing transition structure (neutral-network exits, polymorphic traps) more than
   the one-population versus two-role distinction.
3. The cells at real risk are those whose grammar has large payoff-twin networks reached through reading programs:
   the realizable-language chains (milestones 2 and 5, provenance, world K) and the 2026-10-23 RPS chains. At least
   one published chain number moves by more than 0.05 [none does]. *Counter-prediction (gemini-4-argon), registered:*
   milestone 2's chain is absorbed by a strict CliqueBot and provenance and world K are mostly lottery results, so the
   shifts above 0.05 will be in multi-role games with large ∏_r K_r and capped exploration (incentive-compatible
   enforcement, concessions, the gene arm, coalition-proof auctions) and in the 2026-10-23 RPS chains.
4. No lottery measurement changes, since the lottery is not a chain [any lottery number changes: an audit error].
   [Revised after review] A headline that combines lottery and chain evidence may legitimately change its
   interpretation; such changes are listed, not counted as errors.

## Required outputs

- `notes/exploration-audit.md` (§1 inventory and triage, committed before any re-solve; §2 deviations).
- `predictions/2026-10-24-exploration-audit.md` (predictions 1–4 verbatim), committed before any re-solve.
- `src/exploration_audit.py` (and a runner), importing existing solvers; no existing file edited.
- `runs/exploration-audit.md` and `.json`: the per-cell table, verdicts, and a list of RESULTS sections that need an
  addendum, with the proposed addendum text for each.
- Hand back the addenda drafts and a REJECTED draft; do not edit the shared docs.

**Budget and scale guard.** At most 3 workers, capped by memory (measure first); one job per process; no
`multiprocessing.Pool`. Waiting: watch short commands; for long batches one background wait that exits at completion
and fires if the log stops changing for 2 hours; never poll periodically. If the full list is too large, audit the
at-risk cells in triage order and report what was not reached.
