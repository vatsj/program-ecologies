# Spec: legibility at founding in the fully realizable social organization game, 2026-10-14

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol and gemini-4-argon; to be run by an Opus subagent.
Follow-up to RESULTS "The social organization game, fully realizable" and DEFERRED 11 (the open item there).
REJECTED.md checked: nothing re-opened (the gate with a negative cache in "Provenance" was a production rule for
the PD carriers; here the mark is a cost fix, and its dynamic effect is measured, not assumed).

## Why

Under S-nonself₃ with `eq` the fair wage holds in 3 of 40 runs (zero wage 0.45), the ideal table does no better
(0/20), and 20 coalition founders per island give 0.70. The run engineer's reading, not isolated by any cell:
**legibility at founding**. Every founder starts with an empty certificate list, so militants strike uncertified
bosses and earn nothing while scabs work, and unconditional workers win the scramble before production makes the
coalition legible. If true, founders that carry the certificates they *could* write against the island's non-self
founders should restore the fair wage without seeding the coalition in numbers. If false, the bind is in the
language (the coalition's mass or its scramble), and the realizable claim on distribution must say so. Two cost
items ride along: the futile-retry overhead (≈ 4× the median encounter) and the fuel threshold (10⁶ vs 3·10⁶).

## Design

**Machinery.** `src/sog_full*.py` unchanged (import only): the realizable social organization game, K₃, c = 0.5,
`eq` in both roles, S-nonself₃ production, executed at K = 10⁶ (V = 2.5·10⁵), (100, 64), mN = 1, w = 0.3, horizon
2,000 with 10,000 on main cells (all runs), 40 runs on the paired founder streams of the S₃ + eq cell, whose stored
runs serve as the baseline (rerun bit-identically on a sample of 5).

**Cells.**
- **L1, legible founders:** at founding, each founder runs one S-nonself₃ production pass against the island's other
  founders (excluding copies of its own source, as the gate requires), under the same cap and fuel, and starts with
  the scripts it produced; play and later production as in S₃.
- **L2, the "cannot produce" mark:** S₃ + eq where a failed production for a set is recorded and inherited and not
  retried (a negative cache that is part of the program's state); natural founders.
- **L1 + L2.**
- **L3:** L1 at K = 3·10⁶.
- **L1 with the sham** in place of `eq` (paired), so that legibility's effect is read separately from identity's.
- **N panel:** L1 at (200, 64), 12 runs (the S₃ + eq cell had no fair run there).
- **Assay:** the isolated pure coalition (D\*, T₁, T₁) with L1-style founding lists: fair or not, and at what cost.

**Statistics.** Persistence, runs ≥ ½ fair, zero and ¼ wage shares, window establishment; holders (open militants,
greenbeards, closed shops); the worker-slot composition at generations 10, 50, 200 (the scramble: unconditional
workers' share), which tests the mechanism directly; production attempts by outcome (produced, NONE, timeout) and
the median per-encounter cost relative to play; paired contrasts against S₃ + eq with run-level uncertainty, keeping
in mind that outcomes are all-or-nothing by run.

**Scale guard.** ≤ 3 workers; sibling runs may use up to 3 each: check `ps` for their drivers before any
multi-worker step. The S₃ cells cost tens of minutes per run at (100, 64) and 86 minutes at (200, 64): report the
projected cost before the cells and drop L1 + L2 first, then L3, then the sham cell, disclosed.

## Required outputs

`src/founding_legibility.py` (+ `_run.py`, `_report.py`), `tests/test_founding_legibility.py` (founding production
respects the gate; the mark is inherited and suppresses only failed sets; ν-free reproduction of S₃ + eq on a
sample), `notes/founding-legibility.md` (§1 static: the founding lists' expected content under the length prior and
the coalition's legibility at t = 0; §2 costs), `runs/founding-legibility.md` and `.json`, predictions committed
before any counted cell, and the usual hand-back.

## RE predictions (with falsifiers)

1. **Legibility at founding is the mechanism where fuel does not bind** [revised after review by gemini-4-argon: with
   free full lists H gave 0.03 at K = 10⁶, so founding lists cannot beat fuel there]: L1 at 10⁶ ≤ 0.1; L1 on the
   ideal table ≥ 0.3 (against S₃ + eq ideal 0/20) and L1 at 3·10⁶ ≥ 0.3, each with the unconditional workers' share
   at generation 50 at least 0.1 below the matched natural-founding cell's. *Falsifier:* L1 ideal ≤ 0.1 (then the
   bind is not founding legibility; the candidates left are the coalition's demographic mass and the scramble).
   **Gemini's counter-prediction (registered):** L1 at 10⁶ ≤ 0.1 and L3 (3·10⁶) ≥ 0.3; if L1 fails even at 3·10⁶ the
   bind is the coalition's initial demographic mass.
2. **The mark is a cost fix, not a dynamic one:** L2 within 0.05 of S₃ + eq in persistence, with the median
   per-encounter cost falling to ≤ 1.5× play. *Falsifier:* a persistence change ≥ 0.15, or cost still ≥ 2×.
3. **Fuel and legibility compound:** L3 ≥ natural founding at 3·10⁶ + 0.2 [revised after review: the natural cell
   at 3·10⁶ is the matched control]. *Falsifier:* L3 within run-level uncertainty of it.
4. **Identity still decides nothing:** the sham cell within 0.1 of L1. *Falsifier:* a difference ≥ 0.2.
5. **Size still hurts:** L1 at (200, 64) below L1 at (100, 64) (uncertain). *Falsifier:* at least as high.
6. ~~The isolated coalition becomes fair with founding lists~~ [withdrawn after review by sol: in (D\*, T₁, T₁) the
   two workers are copies, so the S-nonself₃ gate refuses T₁'s production at founding as later]. **Revised:** a
   deterministic gate-and-production trace shows the gate binds, and the assay stays 0/40 with L1 lists.
   *Falsifier:* any fair run.

## Amendments after review (gpt-6.1-sol and gemini-4-argon; these supersede the text above where they conflict)

1. **The founding pass.** All founding lists are computed from one frozen empty-list snapshot (no founder-order
   bootstrapping): each founder runs S-nonself₃ production on M = 10 random non-self cross-role triples from its
   island's founders, each attempt under the ordinary cap and fuel, certificates capped as in play; the cost is
   reported. Notes §1 computes the expected yield (the probability that a naturally founded coalition is executable
   and certified at generation 0) before any cell.
2. **Cells, revised.** Natural founding at K = 3·10⁶ (the matched control both reviewers asked for); L1 at 10⁶, at
   3·10⁶ (L3) and on the ideal table (the decisive cell); **L1-withheld** (the same founding pass with its outputs
   withheld until after the first selection event: separates timely legibility from extra production); L1 with the
   sham at 3·10⁶; the N panel at 3·10⁶; L2 and L1 + L2 as below.
3. **L2, the mark, made safe.** It is keyed on the tuple of bare partner sources and invalidated whenever the
   program's own certificate list or fuel changes; NONE and timeouts are kept apart (only NONE is cached); a test
   verifies that production reads sources only, and a sample of cached failures is replayed against descendants
   (any success is reported). **Order:** a 5-run L2 pilot runs first; if its persistence and play match S₃ + eq on
   paired seeds, L2 becomes the base of the 3·10⁶ cells for speed (disclosed); otherwise it stays a separate cell.
4. **Manipulation checks.** Generation-0 certificate coverage of naturally founded coalitions, first-encounter
   strike/work decisions, militant lineage survival to generations 10 and 50, and certificate retention through first
   encounters, beside the worker-slot composition.
5. **Estimands fixed in advance.** Persistence at 2,000 and 10,000 (all runs), the establishment window as in the
   parent run, efficiency and fairness reported separately; intervals throughout, with "inconclusive" rather than
   "no effect" where intervals are wide; claims are finite-(N, I, horizon) statements.
6. **Drop order:** L1 + L2, then the N panel, then the sham cell, disclosed.
