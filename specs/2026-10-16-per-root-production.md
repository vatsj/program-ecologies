# Spec: a per-root production rule for the fully realizable social organization game, 2026-10-16

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol and gemini-4-argon; to be run by an Opus subagent.
Follow-up to RESULTS "Coverage components" (the deficit is second-path certification under the lack rule) and
DEFERRED 11. REJECTED.md checked: nothing re-opened (the gate with a negative cache in "Provenance" and the bare-source
mark in "Legibility at founding" are different rules; the invariant-key mark is kept).

## Why

Under the lack rule (S₃) a program produces a script for an outcome set only until it holds one, written on the first
path it meets; it is then uncertified on the paths partners later send it down (a militant certified against an
uncertified boss is not certified at a ¼ probe; a concession certified ≥¼ on its ¼ path is not certified on its ½
path). Granting exactly those second-path scripts recovered the free-certificate fair wage on the ideal table (0.30;
0.24 on fresh streams) where S₃ gives 0/20; both halves were needed (the producible second paths alone 0.10, the
Hyp-first tactic's shadowed F-branch alternatives alone 0.05). The remedy should therefore be a production rule, not a
grant.

## Design

**Machinery.** `src/sog_full*.py`, `src/founding_legibility*.py`, `src/coverage_components*.py` (import only; a new
module implements the rule). S-nonself₃ gate and `eq` in both roles unchanged; the invariant-key mark on, keyed on
everything production reads, including the root.

**Rules.** **R0 = S₃** (reference). **R1, per-root lack:** at an encounter, attempt production for a set A whenever no
held script for A is valid at the current root (instead of whenever no script for A is held); the produced script is
appended. **R2 = R1 + shadowed alternatives:** when the tactic produces a script whose derivation passes through a
Hyp-first branch, it also writes the shadowed F-branch alternative in the same attempt (one extra check). **R3 = R2
with a list cap** of k scripts per set (k = 2, 3; oldest evicted), the cost control.

**Cells.** On the stored S₃ + eq ideal-table founder streams (20 runs) and the 40 confirmation streams: R0, R1, R2,
R3 (k = 2, 3), and the H-full reference, on the **ideal table** first; then R2 (and the best R3) at **K = 3·10⁶** and
**K = 10⁶** executed, with the matched natural S₃ cells from earlier runs. (100, 64), mN = 1, horizon 10,000 primary.
A small (200, 64) panel for R2 on the ideal table (12 runs) if cost allows.

**Statistics.** Fair share and runs fair, zero and ¼ wage; production attempts per encounter, scripts per program per
set, the encounter cost relative to play (the futile-retry overhead must not return); the fraction of first fair
encounters at regrowth nuclei whose pivotal scripts were written by R1's per-root trigger versus R2's alternatives;
paired contrasts with run-level intervals, all-or-nothing outcomes kept in view.

**Scale guard.** ≤ 3 workers; the annealed-mutation run uses up to 3: check `ps` first. One job per process (the
coverage run's memory leak). Drop order: the (200, 64) panel, then R3 at k = 3, then K = 10⁶.

## Required outputs

`src/per_root.py` (+ `_run.py`, `_report.py`), `tests/test_per_root.py` (R1 never attempts a set with a script valid at
the root; R2 writes exactly the shadowed alternative; R0 reproduces stored S₃ ideal draw for draw; the mark is
invariant), `notes/per-root.md` (§1 static: per program, the scripts each rule can ever hold, against H's (b);
hand predictions; §2 costs), `runs/per-root.md` and `.json`, predictions committed before any counted cell, and the
usual hand-back.

## RE predictions (with falsifiers)

1. **R2 recovers the free-certificate fair wage on the ideal table:** within 0.1 of H-full on the paired streams (H-full
   0.30 / 0.30), and zero wage ≤ 0.05. *Falsifier:* R2 ≤ 0.1 on both stream sets.
2. **R1 alone is partial:** between S₃ and R2, near the producible-half grant (0.10). *Falsifier:* R1 ≥ R2.
3. **The cap is cheap** [revised after review: R2 writes two scripts per attempt, so the cap counts attempts]: R3 with
   k = 2 bundled attempts and LRU eviction within 0.05 of R2, cost ≤ 1.5× play. *Falsifier:* below R2 by ≥ 0.15.
4. **Fuel still binds when executed:** R2 at 10⁶ ≤ 0.1 (as free certificates gave 0.03) and at 3·10⁶ ≥ 0.4.
   *Falsifier:* R2 at 3·10⁶ ≤ 0.15.
5. **No overhead returns:** under the invariant mark, the median encounter cost under R2 ≤ 1.5× play [revised after
   review: the upper quantiles and cumulative charged work are reported too, and judged separately]. *Falsifier:* median
   ≥ 2×.
6. **Counter-predictions registered.** *Sol:* low median overhead can coexist with expensive regrowth encounters and
   fuel failures; k = 2 works only if a small validity cover exists; R2 improves on R0 but may stay well below matched
   H-full at 3·10⁶. *Gemini:* unbundled FIFO k = 2 drops ≥ 0.10 below R2; R2 at 3·10⁶ gives 0.25–0.35 under linear
   checking, ≥ 0.4 only with root-keyed dispatch; R2 may lag H-full by arrival timing (second scripts acquired after fair
   bosses die).

## Amendments after review (gpt-6.1-sol and gemini-4-argon; these supersede the text above where they conflict)

1. **Order of operations, fixed.** At an encounter: (i) validity of held scripts at the current root is checked; (ii)
   the mark is consulted, keyed on everything production reads (the root and the partners' lists included) but not on
   the program's own list, so appending or evicting does not restart failed attempts, and a failure is retried only when
   an input it read changes; (iii) production runs; (iv) the result is appended; (v) under a cap, eviction follows. Tests
   cover repeated failure, append, eviction and return to an earlier root; the retry bound is stated or reported absent.
2. **Realizability audit.** For R2, a source-executed trace on sample encounters shows that the shadowed alternative is
   constructed, located and checked by code within fuel, with no host-only branch information, and that soundness
   survives list changes; its steps are charged.
3. **Checking a list.** Held scripts are checked in list order (linear), the realistic default; a root-keyed dispatch
   variant runs beside it at 3·10⁶ only. Fuel exhaustion is recorded apart from uncertified failure.
4. **The cap counts attempts.** R3 bundles a primary script with its shadowed alternative as one entry; k ∈ {2, 3}
   bundles; LRU eviction (usage updated when a held script validates at the current root), with FIFO at k = 2 as a
   one-cell control.
5. **Factorial completed.** R0 + shadowed alternatives without the per-root trigger, on the ideal table (both stream
   sets), so the two changes and their interaction are separated.
6. **Matched references.** R0 and H-full are rerun at each executed fuel under the same implementation; "best R3" is
   chosen on the 20 development streams and evaluated on the untouched 40 confirmation streams.
7. **Outcomes.** "Fair share" is the terminal share at 10,000 (time averages reported beside it); each prediction has
   supported / contradicted / inconclusive regions in the predictions file; both stream sets are reported and the
   confirmation set decides. Wage-state occupancy and transitions, first-fair time and loss / regrowth counts are
   reported; a subset runs to 20,000.
8. **Mechanism checks.** Fixed encounter traces without evolutionary feedback (eligible roots, writes, coverage,
   checks, fuel exhaustion per rule); for up to five nucleation events per rescuing rule, a checkpoint replay
   suppressing each newly written script; the generation at which each second-path script is first acquired, against
   the fair bosses' extinction time.
