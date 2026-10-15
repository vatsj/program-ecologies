# Predictions: which part of the full certificate lists carries the fair wage's regrowth? (2026-10-15)

Spec `specs/2026-10-15-coverage-components.md` (reviewed by gpt-6.1-sol and gemini-4-argon; the "Amendments after
review" supersede the earlier text where they conflict). Committed after `notes/coverage-components.md` §1 (commit
8732351) and before any code of this run and any counted cell. Numbers are hand calculations from the notes, the
scratch classification disclosed in notes §1, readings of the stored `Heq_i` and `Ni` runs, or guesses (labelled).
Lottery results are ε = 0 evidence at finite (N, I, horizon); fairness is scored, productive efficiency is reported
beside it and selects nothing; outcomes are all-or-nothing by run, so contrasts rest on a few runs.

**Scoring conventions.** "Fair share" is the fraction of islands fair, scored at generation 10,000 (the primary
endpoint; 2,000 reported beside it). Components are those frozen in notes §1.0 item 4: (a) every script of a set that
S₃'s default root leaves uncovered, (b) every further script of a set the default root covers, (c) identity-true
scripts no tactic writes, (d) scripts written only beside a copy (the gate); canon is S₃'s first script. Cells: H-full,
S₃, minus X (granted H \ X, X barred), plus X (granted X, production on top), the pairs, and count-matched complement
controls (notes §1.0 item 7). Where the spec's wording of a component differs from the frozen definition, the
prediction is scored on the frozen definition and the difference is noted in the verdict.

## Frozen design (notes §1.0)

1. Base: S-nonself₃ + eq on the ideal table (K = 10¹²), (100, 64), mN = 1, w = 0.3, horizon 2,000 extended to 10,000,
   20 replicates on the stored founder streams 0–19, the invariant-key mark on wherever production runs.
2. Masks: a granted set and a barred set per (run tree, set); production on top of the grant (a set is attempted until
   the program has produced a script for it); reacquired and barred outcomes write nothing; minus and full cells are
   pure grants and run in H mode (Lemma P).
3. Cells, in this order: H-full, S₃ (validation reps), minus (a)–(d), plus (a)–(d), plus (a)+(b), plus (c)+(d),
   rand-minus and rand-plus for (a), (b), (d), then rand-(c); confirmations on replicates 20–59 for any plus, pair or
   random cell with fair share ≥ 0.2; mediation replays. Drops by cost only, in the order of notes §1.0 item 10.
4. ≤ 3 worker processes.

## RE predictions (verbatim from the spec)

1. **Untravelled paths carry regrowth:** minus (a) ≤ 0.05 and plus (a) ≥ 0.2; regrowth starts from a concession boss
   and militants whose first fair encounters use granted (a) scripts. *Falsifier:* minus (a) ≥ 0.2, or plus (a)
   ≤ 0.05.
2. **Second paths and gate copies matter little:** minus (b) and minus (d) within 0.1 of H-full. *Falsifier:* either
   ≤ 0.1.
3. **`EQ`-true scripts are not needed** (identity decided little everywhere): minus (c) within 0.1 of H-full.
   *Falsifier:* minus (c) ≤ 0.1.
4. **No single component is sufficient except (a)** (uncertain): plus (b), plus (c), plus (d) ≤ 0.05.
   *Falsifier:* any of them ≥ 0.2.

## Counter-predictions registered after review (verbatim from the spec)

5. *Gemini:* minus (a) ≤ 0.05 holds, but plus (a) alone ≤ 0.10 and recovery ≥ 0.25 needs plus (a)+(b) (a concession
   boss probes two worker slots, so one skeleton per lack-set blocks the three-way handshake). *Sol:* plus (a) alone
   < 0.2, and some combined grant beats every singleton (regrowth needs complementary certificates across coalition
   members).

*Scored:* Gemini holds iff minus (a) ≤ 0.05, plus (a) ≤ 0.10 and plus (a)+(b) ≥ 0.25. Sol holds iff plus (a) < 0.2
and max(plus (a)+(b), plus (c)+(d)) exceeds every plus singleton.

## Subagent predictions (mine), with falsifiers

**S1. The masks reproduce the references.** The full mask reproduces the stored H + eq ideal runs on 20/20 replicates
(every dynamic summary field identical; fair share 0.302 at 2,000 and 0.300 at 10,000), and the empty mask reproduces
the stored S₃ + eq ideal runs on the validation replicates (dynamics identical with the mark on; production counters
identical with the mark off). *Falsifier:* any difference in a dynamic field.

**S2. (c) is null.** minus (c) within 0.05 of H-full and plus (c) ≤ 0.05. *Falsifier:* |minus (c) − H-full| ≥ 0.15
or plus (c) ≥ 0.15.

**S3. (d) is small.** minus (d) within 0.1 of H-full; plus (d) ≤ 0.05. *Falsifier:* minus (d) ≤ H-full − 0.2, or
plus (d) ≥ 0.2.

**S4. Granting second paths helps at least as much as granting untravelled paths** (guess, probability about one
half). Paired mean plus (b) − plus (a) ≥ 0, and plus (b) ≥ 0.15. *Falsifier:* plus (a) − plus (b) ≥ 0.15.

**S5. (b) is necessary.** minus (b) ≤ 0.15. *Falsifier:* minus (b) ≥ 0.25.

**S6. (a) is necessary.** minus (a) ≤ 0.15 (barring (a) removes the probe concessions' certificates; only bosses
paying ½ on their default path keep a fair certificate). *Falsifier:* minus (a) ≥ 0.25.

**S7. The production-rule pair recovers H; the provenance pair does not.** plus (a)+(b) ≥ 0.2 and plus (c)+(d)
≤ 0.05. *Falsifier:* plus (a)+(b) ≤ 0.05, or plus (c)+(d) ≥ 0.2.

**S8. Collapse is grant-independent.** Every cell's fair share at generation 20 is ≤ 0.12 (H-full 0.03 in storage).
*Falsifier:* some cell ≥ 0.2 at generation 20.

**S9. No component is harmful.** No minus cell exceeds H-full by 0.15 or more (paired mean). *Falsifier:* one does.

**S10. Identity, not volume** (conditional). For every component X with plus X ≥ 0.2, its rand-plus control is at
least 0.15 lower; for every X with minus X ≤ H-full − 0.2, its rand-minus control is at least 0.15 higher than minus X.
*Falsifier:* a control within 0.05 of its cell in such a case. Unscored if no cell meets the condition.

**S11. What the rescue uses is never written by S₃.** In rescuing cells that grant (b), at least half of the pivotal
granted scripts at regrowth nuclei are "never written there" by the timing log, and replays with them withheld regrow
in at most 2 of 5. *Falsifier:* most pivotal granted scripts pre-populated (here or next), or ≥ 4 of 5 replays still
regrow. Unscored if no cell granting (b) rescues.

**S12. Endpoints agree.** Every cell's fair share at 10,000 is within 0.05 of its value at 2,000. *Falsifier:* a cell
moves by ≥ 0.1.

**S13. Costs.** Minus and full cells take ≤ 8 minutes per run (median, including the extension); plus, pair and
rand-plus cells 8–25 minutes. *Falsifier:* a plus-type median above 30 minutes.
