# Predictions: exploration-cap audit of the published ε → 0 chains, 2026-10-24

Spec `specs/2026-10-24-exploration-audit.md` (reviewed by gpt-6.1-sol, then gemini-4-argon in amended mode; both folded).
Inventory and triage: `notes/exploration-audit.md` §1 (committed first). Written and committed after the inventory and before
any re-solve. Predictions 1–4 are the RE's, copied verbatim from the spec; the registered counter-predictions are the
reviewers'. Section E below is the engineer's own, added before any re-solve and scored separately.

## The RE's predictions (verbatim from the spec; falsifiers in brackets)

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

## Scoring conventions fixed here (engineer, before any re-solve)

* **Prediction 1 count.** "Chain result" is an inventory group (I-nn). "Capped or thresholded" is status M or R of
  `notes/exploration-audit.md` §1.0. Inventory result: 45 groups, of which 15 monomorphic-restricted. Prediction 1 is scored
  from the inventory alone: **held** (45 ≥ 10). The prediction is nearly trivial because the early chain thresholds
  polymorphic targets everywhere; this is recorded rather than hidden.
* **Prediction 2 denominator.** Re-solved cells in one-population DSL arms = cells for which a stage (b) or later value
  exists in `runs/exploration-audit.json`, grouped by inventory group, counting each (group, N, parameter) cell once. A cell is
  "within 0.02" if the largest absolute difference between the published value and the final-stage value of the headline
  statistic is ≤ 0.02 on the scale of the spec (absolute for probabilities and shares; payoff divided by payoff range for
  payoffs). Cells whose final stage is only "stable under this enlargement" count with that value; cells *unconverged*
  by the frontier test (π mass on frontier states > 0.01 at stages (a) and (b)) are reported separately and are in the
  denominator. The counter-prediction is scored by tabulating for each moved cell the identified mechanism
  (neutral-network exit, polymorphic trap, cap truncation, prior-mass rare gateway, other) against one-population versus
  multi-role.
* **Prediction 3 value.** A published chain number "moves by more than 0.05" if, for any inventory group, any
  headline-level statistic (π share, P(C,C), efficiency, fair share, payoff/range) differs by > 0.05 between the published
  value and a stage (b)–(e) value, **in a cell whose published value was reproduced at stage (a)**. Moves that appear only
  when the transition model changes (stage (e), twin expansion) are labelled and counted separately, since the model
  change is a correction of a different kind. The two-sided scoring: the RE's version is scored on the named groups
  (I-38, I-45, I-46 (provenance/world K have no chain), I-48, I-49); gemini-4-argon's on I-24, I-36, I-44 and the RPS groups.
* **Prediction 4.** The lottery results are not re-run; the check is that no lottery number appears in any audit
  table. Interpretation changes of headlines that combine chain and lottery evidence are listed.
* **Stage labels** (spec): (a) reproduce, (b) enlarge every active restriction together, (c) full monomorphic space,
  (d) polymorphic states added from recurrent monomorphic classes, (e) twin-expanded (only for cells published under the
  lumped chain). Labels: *monomorphic-complete, polymorphism-search-limited*; *stable under this enlargement*;
  *unconverged* (frontier mass > 0.01); *unresolved* (not reached or not reproducible). None is called converged.
* **Tolerances.** Reproduction (stage a) is "reproduced" within the published precision (4 decimals for π shares, 3
  significant figures otherwise); a larger gap is a *reproduction failure*, reported before any stage (b) value is read.

## The engineer's own predictions (section E; added before any re-solve)

E1. The mixed2 positive control reproduces: capped chain at 1,500 states gives −0.009 ± 0.005 and the whole space gives
−0.471 ± 0.002 at c = 0, N = 10⁴; the negative control (blind inspection, 289 states, complete) changes by < 10⁻⁶.
[falsifier: either fails; then no later cell is trusted and the audit stops and reports]
E2. The cells that move by more than 0.05 will be monomorphic-restricted ones with a stored cap or large published cut, in
this order of likelihood: I-32 (modal fixed-role dollar), I-22 (three-player dollar), I-24C (enforcement), I-36 (concessions,
direction: fair lower), I-23 (union). [falsifier: none of these five moves by more than 0.05 while some M-status cell does]
E3. M-status cells (monomorphic complete) will not move by more than 0.02 at stages (b)–(d) except where a deep trap is
known (I-29 at N = 10², 10³, 3·10⁴; I-49 forfeit-only). [falsifier: any other M cell moves by more than 0.02]
E4. The two-role ultimatum arms I-05/I-06 (whole space 1,936 / 432 / 1,980 pairs) change their (M|M) and (L|L) shares by
< 0.02 when solved whole-space. [falsifier: > 0.02]
E5. The cut-corrected concession values are conservative: the re-solved P01 fair share at N = 10⁴ is ≤ the published
corrected 0.0020 + 0.01. [falsifier: larger]
