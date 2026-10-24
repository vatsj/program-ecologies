# Spec: deriving immigrant rejection for stable sets on islands, 2026-10-25

Status: draft by the RE; reviewed by gemini-4-argon (folded [after review]), then gpt-6.1-sol (`--mode amended`, folded [after second review]); to be run
by a Sonnet subagent. Queue item 61; the RS agreed to it on 2026-10-24 (the explainer "Stable Sets on Islands": "a
derived immigrant-rejection guard"). Follows RESULTS "A migration window for stable sets on islands", "Farsighted
refusal", "Dominance contracts and refusal on islands", "Every behavioural predicate as a hook key". REJECTED.md
checked: a reader of the island's guard composition (gKR-read) was neutral and did not keep coverage; this spec tests
different programs and re-opens nothing.

## Why

In one connected component the RS's target (every island efficient, all three fair pairs present) is met under
migration by the hand-written veto gV and not by the derived farsighted guard gKR(0.99), which only postpones the
one-member consensus (coverage-lost median ∝ roughly 1/mN). Without a guard, members switch into each other mostly by
neutral drift through member-mixed states: the excluded slot drifts to an offer of 1/2, then a pivot drifts across a
3-against-3 tie. The question is whether a guard that programs could hold for their own reasons keeps an island on its
member against immigrants and drift, as gV does.

## Design

Base: the migration-window kernels and arms (`src/migration_window*.py`, `src/farsighted_refusal*.py`), reused by import;
the stated and V\* targets, generation snapshots and statistics of that spec.

**Step 0, before any new arm: the mechanism of gV.** Decompose why gV keeps coverage under migration: per mN, the fate of
immigrants by type on member islands (fixation, loss), the member-to-member transitions that occur under the baseline
and are blocked under gV, and whether gV acts through contract refusal, through the refusal bit's selection on
immigrants, or through the tie step. The notes state the mechanism before any derived arm is built; the derived arms
target it. [After review] Step 0 includes two diagnostics that freeze only the excluded slot's offers, or only the
pivot's tie choice, to measure how much of each route carries the baseline's member-to-member flips, and [after second review] both
together, since the two routes may interact. **Step 0 is a
gate:** if it falsifies prediction 1 (gV acts mainly through contract refusal), the candidates are revised in a spec
addendum, reviewed again, before the main panel.

**Derived candidates** (each a heritable program trait, with matched prior mass and a matched inert control):
1. **Loyalty** (a history-keyed hook fill, admissible under the RS's behaviour-key ruling, DEFERRED 12): a member-slot
   program that, at a tie between its current partner's offer and another offer, keeps the partner it was paired with
   in its previous encounter. It reads only its own history, not the island. [After review] A variant with memory k = 5
   keeps the partner of the majority of its last five encounters, since one-step memory can be scrambled by a single
   immigrant encounter.
2. **Status-quo tie-breaking from farsighted consent:** gKR(0.99) extended from contracts to ties. [Redefined after
   review: the two fair pairs a pivot belongs to are symmetric under the default KR table, so their values W are equal
   and a plain comparison is still a tie.] The KR recursion is solved with a switching cost ε paid on any change of
   coalition, so the current pair has a strictly higher value than its symmetric alternative; ε ∈ {0, 0.05} sixths,
   where ε = 0 is the control that should equal gKR(0.99). [After second review] The recursion's state includes the
   incumbent coalition; the program's utility pays ε at every later switch too, with the same discount normalization
   as gKR; ties left after the recursion fall back to drift; ε = 0 is checked against the original transition kernel,
   not only by lifetimes. This is a **preference-modification arm** (it adds an incentive the game does not have); it
   is reported beside a **direct status-quo tie rule** (keep the current pair at every tie, no valuation) and a cell
   where the switching cost is charged in evolutionary payoffs.
3. **Conformity by local sampling** [redefined after review: an island-wide modal outcome is an environment oracle and
   undefined at the 3-against-3 tie]: before acting, the program observes one random completed encounter on its island;
   if that encounter formed a fair pair it plays its part of that pair, otherwise (or if it was excluded) it keeps its
   previous choice.
4. **References:** baseline, gKR(0.99), gV.

**State semantics** [after second review]. A program's history (its partners in its last k encounters, recorded as
partner *slots*, not sources) is personal: it starts empty at birth (not inherited), travels with a migrant, and an
encounter in which the program is excluded is recorded as no partner. Encounter order is the kernel's.

**Panel:** mN ∈ {0.01, 0.1, 1}; (100, 64), 40 runs, and (200, 64), 20 runs; one 16-island-component cell (C = 4) per
candidate at N = 200, mN = 0.1; 20,000 generations with the migration-window snapshots.

[After second review] **Scoring and scope.** Paired seeds, run-level 95% intervals and explicit censoring; "within 0.1"
is met only if the interval of the difference lies inside ±0.1, failed if outside, undetermined otherwise. Censored
survival curves and member-transition hazards are reported; conclusions are finite-time. Establishment from
uncoordinated founders is reported separately from maintenance of coverage already established.

## Predictions (the RE's; falsifiers in brackets)

1. *Step 0.* gV keeps coverage mainly by making mismatched immigrants on a member island lose, through the refusal bit
   carried by residents, not by blocking member-to-member contracts (none exist between members) [the decomposition
   attributes most blocked flips to contract refusal].
2. *Loyalty.* Loyalty meets the stated target in at least 0.8 of runs at mN = 0.1 and 1, N = 100 (gV 1.0 and 0.925)
   [below 0.5 at mN = 0.1]. *Counter-prediction (gemini-4-argon), registered:* one-step loyalty reaches 0.8 at mN = 0.1
   but falls below 0.6 at mN = 1, where immigrant encounters scramble the memory.
3. *Status-quo tie-breaking.* With ε = 0.05 it extends gKR's lifetime by at least 3× at mN = 0.1 but does not reach 0.8
   at mN = 1 [it reaches 0.8 at mN = 1]; with ε = 0 it equals gKR(0.99) within noise (lifetime ratio below 1.2) [above
   1.5].
4. *Conformity.* The conformity reader meets the target as well as gV at every mN (within 0.1) [more than 0.2 below gV
   at any mN]. *Counter-prediction (gpt-6.1-sol), registered:* sampling one encounter is copying, not rejection; it can
   amplify an immigrant's outcome and coarsen like a voter model, losing coverage in a connected component.
5. *Spread.* Every candidate that keeps coverage also rises in frequency under migration (as refusal did), and the
   inert controls do not [a coverage-keeping candidate that falls]. [After review] To separate selection from
   hitchhiking on long-lived islands, the within-island frequency change after immigrant arrivals is reported.
   [Replaced after second review: conditioning on member stability would condition on an outcome the trait causes.]
   Selection is measured by paired, randomized introductions of a rare candidate, and of its inert control, into
   identical resident islands, recording relative reproductive success and establishment, and by the reciprocal rare
   inert invasion of stabilized islands. *Counter-prediction (gpt-6.1-sol), registered:* a stabilizer can benefit
   non-carriers equally and stay neutral, so some effective stabilizers will not rise when rare.

## Required outputs

- `src/immigrant_rejection.py` (+ runner, report) importing the existing modules; no existing file edited.
- `tests/test_immigrant_rejection.py`: the candidates' choices at ties by hand; inert controls play identically to the
  baseline; the reference cells reproduce the stored migration-window rows.
- `notes/immigrant-rejection.md` (§1 hand predictions and Step 0's design, before code; §2 deviations; §3 the gV
  mechanism, before any derived arm's counted cell).
- `predictions/2026-10-25-immigrant-rejection.md`, before any counted cell, with the RS's agreement first.
- `runs/immigrant-rejection.md` and `.json`, `runs/immigrant_rejection/` (small files).
- Hand back RESULTS, REJECTED, THEORY and NOTATION drafts; do not edit the shared docs.

**Budget and scale guard.** Runs cost seconds to minutes; other subagents are running: check `ps` and free memory before
each batch; at most 2 workers while others are alive. One job per process; no `multiprocessing.Pool`; one background
wait per batch that exits at completion and fires if the log stops changing for 2 hours; never poll periodically. Cut
order (disclose): the component cell, N = 200 for the conformity reader, mN = 0.01.
