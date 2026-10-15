# Spec: which part of the full certificate lists carries the fair wage's regrowth?, 2026-10-15

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol and gemini-4-argon; to be run by an Opus subagent.
Follow-up to RESULTS "Legibility at founding" and "The social organization game, fully realizable"; DEFERRED 11's
open item. REJECTED.md checked: nothing re-opened (legibility at founding is dropped there and stays dropped).

## Why

On the ideal table, free full certificate lists with `eq` (H + eq) hold the fair wage on 0.30 of islands (6 of 20
runs), while S-nonself₃ production on the same seeds and grammar gives 0/20, with founding lists or without. Every
cell collapses to 0.03–0.08 fair by generation 20; only H regrows. Under H every founder lacks nothing, so the
deficit is what production never writes. Four candidate components: (a) **untravelled paths**: scripts for check
paths a program never meets in its own encounters; (b) **second paths**: a second script for a set the lack rule
treats as already held; (c) **`EQ`-true scripts**: scripts for paths where an identity atom reads true, which
S-nonself₃ refuses to produce beside a copy; (d) **gate copies**: what the S-nonself₃ gate forbids outright (T₁-type
production beside one's own source). Knowing which one carries regrowth says whether the fix is a production rule
(a, b), a provenance rule (c, d), or neither.

## Design

**Machinery.** `src/sog_full*.py` and `src/founding_legibility*.py` (import only); the S₃ + eq lottery on the ideal
table at (100, 64), mN = 1, the stored founder streams of the 20 ideal-table runs, horizon 2,000 and 10,000 for every
run; the invariant-key mark on for cost.

**Lists.** Founders and newborns receive a *granted list* = the H list restricted by a component mask; production
then runs as S₃ on top. Notes §1 defines each component exactly from the code (which scripts of a program's H list
fall in (a)–(d), with overlaps reported) before any cell, and gives each component's share of H-list scripts under
the length prior.

**Cells** (20 runs each, paired): **H-full** (= H + eq ideal; reference 0.30), **S₃** (reference 0); **minus-one**:
H minus (a), minus (b), minus (c), minus (d); **plus-one**: S₃ plus (a), plus (b), plus (c), plus (d). If a
plus-one cell reaches ≥ 0.2, a 40-run repeat of it and of H-full on fresh founder streams.

**Statistics.** Persistence, runs fair, zero and ¼ wage; the collapse-and-regrowth trajectory (fair share at
generations 5, 20, 200, 2,000); for regrowing islands the coalition that regrew it and which granted scripts its
first fair encounters used; held scripts by component at the horizon; paired contrasts with run-level intervals,
"inconclusive" where wide (outcomes are all-or-nothing by run).

**Scale guard.** ≤ 3 workers; the scaling run uses up to 3: check `ps` before any multi-worker step. Projected cost
first; drop the 40-run repeat, then the plus-one cells for components whose minus-one cell is within 0.05 of H-full.

## Required outputs

`src/coverage_components.py` (+ `_run.py`, `_report.py`), `tests/test_coverage_components.py` (the masks partition
or label every H-list script; the empty mask reproduces S₃ ideal draw for draw; the full mask reproduces H + eq ideal
draw for draw), `notes/coverage-components.md` (§1 definitions, shares, hand predictions; §2 costs),
`runs/coverage-components.md` and `.json`, predictions committed before any counted cell, and the usual hand-back.

## RE predictions (with falsifiers)

1. **Untravelled paths carry regrowth:** minus (a) ≤ 0.05 and plus (a) ≥ 0.2; regrowth starts from a concession boss
   and militants whose first fair encounters use granted (a) scripts. *Falsifier:* minus (a) ≥ 0.2, or plus (a)
   ≤ 0.05.
2. **Second paths and gate copies matter little:** minus (b) and minus (d) within 0.1 of H-full. *Falsifier:* either
   ≤ 0.1.
3. **`EQ`-true scripts are not needed** (identity decided little everywhere): minus (c) within 0.1 of H-full.
   *Falsifier:* minus (c) ≤ 0.1.
4. **No single component is sufficient except (a)** (uncertain): plus (b), plus (c), plus (d) ≤ 0.05.
   *Falsifier:* any of them ≥ 0.2.

5. **Counter-predictions registered after review.** *Gemini:* minus (a) ≤ 0.05 holds, but plus (a) alone ≤ 0.10
   and recovery ≥ 0.25 needs plus (a)+(b) (a concession boss probes two worker slots, so one skeleton per lack-set
   blocks the three-way handshake). *Sol:* plus (a) alone < 0.2, and some combined grant beats every singleton
   (regrowth needs complementary certificates across coalition members).

The RS is invited to add his own; the uncertain ones are 1 and 4.

## Amendments after review (gpt-6.1-sol and gemini-4-argon; these supersede the text above where they conflict)

1. **Static components.** Let S₃^static be every script S-nonself₃ can ever produce for a program on any encounter
   path (computed statically). The components are a static partition of H \ S₃^static, fixed in notes §1 before any
   cell, as properties of (program, script) pairs: (a) scripts for check-sets queried only on paths the program's own
   encounters never reach (off-role or off-path probe branches); (b) scripts beyond the canonical first one per
   lack-set; (c) scripts on paths where an identity atom reads true; (d) scripts the S-nonself₃ gate forbids. Overlaps
   are resolved by a stated priority order, and the joint membership classes are reported beside the marginal
   shares. A test checks that S₃^static ∪ (a) ∪ (b) ∪ (c) ∪ (d) = H for every program in the support.
2. **What a mask does.** Production is S-nonself₃ throughout, with its gate, copying, retry and cost rules frozen
   across cells. Every individual (founders, newborns and migrants alike) holds the granted part of its own source's
   H list: a supply policy, not seeding. In minus-one cells the removed component is also barred from production and
   copying, so it cannot be regenerated; in plus-one cells production runs on top of the grant. Grants, endogenous
   production, copying, lack-rule suppression and reacquisition are logged separately.
3. **Cells added.** Pairs: plus (a)+(b) (the production-rule pair) and plus (c)+(d) (the provenance-rule pair).
   Count-matched random grants and removals (stratified by host program and check set), one per singleton cell, so
   component identity is not confounded with coverage volume. Plus-one cells are kept regardless of the minus-one
   results (redundancy can make a component sufficient but unnecessary); pruning is by cost only. Any candidate
   reaching ≥ 0.2 is confirmed on 40 fresh founder streams with H-full beside it.
4. **Mediation and timing.** For up to five successful runs per rescuing cell, replay with the implicated granted
   script withheld just before its first use; and log, for every granted script used in a first fair encounter,
   whether S₃ would have produced it at that encounter or the next (separating "pre-populated" from "never written").
5. **Equivalence tests.** The empty mask reproduces S₃ ideal and the full mask reproduces H + eq ideal draw for draw,
   with the invariant-key mark on and off, over whole trajectories including production counters and charges.
6. **Estimands.** The fair-island share and the number of runs with any fair island are reported separately;
   generation 10,000 is the primary endpoint and 2,000 an intermediate one; observed-threshold verdicts are kept apart
   from statistical evidence (0/20 still allows a success probability near 0.14). Random streams are event-keyed where
   the kernel allows it, so that altered production does not shift demographic randomness; otherwise disclosed.
