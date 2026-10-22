# Behavioural hooks: notes (2026-10-21)

Spec `specs/2026-10-21-behavioural-hooks.md`; predictions `predictions/2026-10-21-behavioural-hooks.md` (committed 9d3bdb3,
before any code; addendum after the gate). **Status:** the launch gate failed at level PA, the RE chose option (a) (a level-1 box
in the grammar) and the gate then passed; the cells follow. Static numbers are static; every cell number is a finite-(N, I,
horizon) lottery statistic at eps = 0, not pi.

## 1. Hand predictions (before the solver)

Written in the predictions file (last section) and repeated: the five other hand statics agree with the RE; PrudentBot (key
box a and box not d, all boxes level PA) against FairBot is mutual defection, not mutual cooperation, because FairBot
cooperates with DefectBot at world 0. Mechanism hand expectations for Part M are the RE's in the spec (H1 contagion plus H2
inheritance as the leading guess); my own, registered in the predictions addendum: PrudentBot-equivalents are rarer than
FairBot-equivalents under this prior.

## 2. What was built, the gate, and every deviation

### 2.1 The family (after the RE's option (a): box1 admitted)

Atoms a, c, d; connectives not, and, or, box, box1 (box1: the level-1 box, PA + Con, ignores world 0, one node); every atom under a
box; modal depth <= 2 counting both kinds; size <= 7 nodes. Spellings a(2..7) = 6, 24, 90, 528, 2,814, 15,912 (ordered pairs
counted as in `modal.py`). Classes by truth on all words of length <= 6 (stable at 5, 6): **2,095 non-constant classes** for the
full family (sizes 2..7: 6, 18, 35, 137, 509, 1,390) and **730** for the a-free family (atoms c, d; stable at word lengths 5..8);
2 constants each, dropped. Prior: the arm's length prior bits(s) = log2 a(s) + 2 log2 s + 1, each class at its shortest member
(the six size-2 classes box a, box c, box d and their box1 forms carry about two thirds of the family's mass together; FairBot's key
box a alone about 0.11). The registry holds 1,026 boxed subformulas (identity by truth table at word length 5, checked equal at
6 and 7: `tools/beh_registry_check.py`); a key needs at most a few of them.

**Static finding kept (level PA only).** With box only (600 + 199 classes) the spec's PrudentBot (box a and box not d) is mutual
defection with FairBot and with itself, and **no one-fill program is prudent** (D against CooperateBot and DefectBot, C against
FairBot and a copy of itself) for either default, in either family (0 classes; `tools/beh_gate_extra2.py`, a test). **With box1
admitted:** prudent one-fill classes in the full family = **2** (box a and box1 not d; box (a and box1 not d)) on HOOK(t, D), prior
mass 1.0e-4 of the full-family key prior, and the two negations on HOOK(t, C) with mass < 1e-4; 0 in the a-free family.
FairBot-signature keys: 194 classes, prior mass 0.260 (D-default), 53 classes mass 0.030 (C-default).

**The gate (re-run).** `tools/beh_gate.py`: the solver and the independent pure-Python Kripke reference agree on all 49 entries
(seven programs); the spec's six hand entries all agree with PrudentBot read with box1 on d (PrudentBot against FairBot and
against itself: (C, C) from world 0). GATE PASSED.

### 2.2 The evaluator and kernel as built

`src/hooks_beh.py` (family, registry, evaluator `eval_match_beh`, packed specs, reference), `src/hooks_beh_kern.py` (kernel),
`src/hooks_beh_run.py` (cells, founders, runs), `src/hooks_beh_report.py` (verdicts), tests `tests/test_hooks_beh.py` (17) and
`tests/test_hooks_beh_kern.py` (20). No existing file edited. The kernel is `hooks_w2_kern` rebuilt on the new evaluator; with
the legacy keys (0-7 the beta classes, 8 and 9 the open keys) it is the same law, checked by **reproduction of the stored
`open-max` rows at the stored geometry (100, 64, 1,000 generations): runs 0 and 1 identical in island P(C,C), present types, held
fills at all 10 stored generations and in the final state statistics** (`runs/hooks-beh-validate.json`; a 25-generation version
is a test); the evaluator reproduces the stored solver's plays on 400 random legacy fill sets, and the registry programs agree
with direct Kripke semantics and with the reference on all keys of all 49 named pairs. Numba note: the compiled-function cache
is per file, so after editing `hooks_beh.py` the `hooks_beh*.nb*` cache files were removed (a stale cache would hide an edit).
Two optimizations that do not change the law (identical counters on a 120-generation probe before and after): only the node pairs
the two programs' references can reach are evaluated, and the stabilized registry state of a reading pair is folded from its letter
word (3 bits per world plus 6 repeats of the last letter; the state reaches its fixed point within depth + 1 repeats, a test).

Design points the spec left open, each stated:
1. **Quotient.** Equivalence on finite linear frames (GL.3), coarser than GL (all GL-equivalent pairs are merged). Disclosed.
2. **Prior.** "Geometric in nodes, the repo's ratio": the arm's length prior (`modal.py`; `hooks-w.md` §1), per spelling
   2^-bits(s), a class at its shortest member. Normalized over the family.
3. **Seeding.** A seeded behaviour-scope fill draws its key from the family prior on a separate random stream (every other draw is
   the legacy one, so bases, tags, scopes and actions are common across cells). Under the hostile boost the (key, action) pair is
   drawn jointly with weights prior x 10 on the two hostile triples when the base's tag is C-default.
4. **C-default / D-default** of a base's tag = which of HOOK(t,C), HOOK(t,D) appears in its shortest spelling (neither or both: no
   default, never hostile).
5. **Written fills.** Thanks (mutual cooperation) and grudge (writer cooperated, partner defected) as in the follow-up's kernel;
   the key is drawn from the prior restricted to the keys true of the partner at the stabilized world of the pair, with the
   trigger's action; no true key: no write (counted). Tag draw, conflict rule (specific scope wins, ties by recency), capacity
   four with FIFO, in-place update on (tag, scope, key) as before; copying 0.1 per encounter, verbatim.
6. **Contracts (behavioural).** In an encounter that is not already (C, C) between two tagged parties, one key per party is drawn
   independently from the prior (not conditioned), action C, on each pair of carried tags (at most four candidates); accepted iff
   both parties are weakly better off and one strictly, judged jointly with both fills in force; one accepted candidate drawn
   uniformly. (The follow-up's open contract is the special case key = box a for both.)
7. **Sham writes (M5).** The conditioned key is drawn as in the cell above and then replaced by a key drawn uniformly from the full
   family's keys with the same size and the same applicability count, where the applicability count of a key is the number of the
   six named programs (FairBot, TrustingBot, PrudentBot, Godel predator, CooperateBot, DefectBot) of which it is true when read by
   a FairBot (stabilized). My reading of "matched in key length and in its pre-write applicability frequency across the panel".
8. **Ancestry (M3).** Behaviour fills carry in the key field bits 12-13 (0 seeded, 1 thanks, 2 grudge, 3 contract) and bit 14 (the
   fill has been copied at least once); the origin field is the latest transmission event. Flags only in the cells that need them
   (`anc=1`); a flagged fill is the same fill (same spec) but a different type, so flagged cells are statistically equivalent
   reruns, not draw-for-draw copies, of their unflagged versions. "Inherited-written" cannot be separated from "written" (types
   are structural: an offspring is the same type); inheritance's contribution is measured by the ablation M3a, as the spec says.
9. **M3a** strips every non-seeded fill from the child at birth (the stored kernel's `noinherit` stripped written fills only);
   **M3b** copying off; **M3c** both; **M3d** a write that would evict a fill is rejected (and counted; contract writes and copies
   likewise); **M3e** the founder-base prior restricted to bases whose truth function depends on each tag's hook atoms through a
   single leaf (hc-only or hd-only): "one hook node per tag" at the function level.
10. **M4** the window applies to creating fills (thanks and grudge writes and contracts); copying and inheritance continue outside it.
11. **M1** classes: FairBot, PrudentBot, CooperateBot-like, DefectBot-like, TrustingBot-like, predator-like, other, ambiguous
    (matches a named class on the six panel programs but differs on the stranger copy); the response signature is the individual's
    action against the six named programs and a stranger copy of itself (every context "no lineage"); equivalence is exact
    equality with the named program's signature. Two extra classes (TrustingBot-like, predator-like) beside the spec's six. The
    deciding fill of a type: the newest fill whose removal changes the signature; origin none / seeded / thanks / grudge / contract
    / several jointly, with the copied flag.
12. **M2** class-changing events logged per kind (thanks write, grudge write, copy, contract, birth: victim class to child class),
    by evicting or not and by multi-hook base or not, as counts over the whole run.
13. **Held/applicable/selected/executed statistics** (`enc_stats`) are reduced to "held" (the applicability of a behaviour fill needs
    the key's truth); the counter of encounters whose outcome a fill changes is kept.

### 2.3 Scale deviations (cost), declared before any counted cell

The behavioural family makes almost every write a new type (about 1.2 new types per sampled encounter, one per individual in steady
state), so a new type is matched against every resident type of its island; measured cost 0.4-0.9 ms per sampled encounter at
N = 100 (versus 5.6 microseconds in the legacy kernel), i.e. about 1.5 hours per run at the spec's (100, 64, 1,000 generations),
about 40 worker-hours for one cell of 40 runs. I therefore reduced the geometry of the counted cells, **declared and applied to
every cell alike so that all comparisons are paired at the same geometry**:
- PD island cells: **(N, I) = (100, 16), horizon 500 generations** (spec: (100, 64), 1,000). The stored rows show efficient-island
  share 0.95-0.99 by generation 200-500 in the legacy cells; the legacy comparison cells (`open-max`, thanks-only, grudge-only and
  all M3/M4 variants) are rerun at the same geometry. **The registered thresholds were set for I = 64; with I = 16 a universal-open
  run needs fewer islands to succeed, so baselines move up; I apply the thresholds literally and report the geometry-matched
  `open-max` beside every verdict.**
- Runs: 30 per behavioural cell (`beh-max`, `beh-max-noA`, `beh-max-hostile`, `beh-written-only`, `M5-sham`), 40 per legacy cell.
- Fission-fusion (`ff-beh-max`): **16 islands of 100 merged into 1,600 at generation 200, horizon 400, 10 runs** (spec: 32 x 100,
  merged 3,200, horizon 600, 20 runs).
- Secondary N = 200: **(200, 8), horizon 600, 10 runs** (spec: horizon 2,000, 20 runs; islands unspecified).
- The reproduction check of the legacy kernel stays at the stored geometry (100, 64, 1,000), 2 runs.
Drop order if time runs out: `beh-max-N200`, M3 on `open-max` (secondary), `ff-beh-max`, then runs per behavioural cell.

### 2.4 The family's prior (static note for the reader)

The six size-2 keys (box and box1 of a, c, d) hold about two thirds of the family's prior mass; a written key conditioned on being true
of a cooperating partner is box a or box1 a with high probability, so conditional writes concentrate on FairBot's guard, with a long
tail; the prudent classes (mass 1e-4) are reachable only through the tail, or through selection acting on seeded and written
mixtures of several keys.

### 2.5 Run record and changes after the declaration in 2.3 (all declared here, none changed a law)

- Counted cells: `beh-max` 30 runs; `beh-max-noA`, `beh-max-hostile`, `beh-written-only`, `M5-sham` **20 runs each** (cut from 30
  after seeing 8-10 minutes per run, before those cells started); `ff-beh-max` **6 runs** (10 planned; killed after the sixth, ~50
  minutes each; `runs/hooks_beh/cut_ff.sh`); `beh-max-N200` 10 runs; all legacy cells 40 runs; `inert` (Part W's inert-hooks control,
  every fill inert, lineage writes as stored, strict 0) **added** at this geometry after seeing that plain provers win many `beh-max`
  islands, so that "recovery" has a same-geometry reference (0.275 of 40 runs).
- Workers: 1 throughout. `runs/prudence/batch.done` never appeared; the prudence driver (pid 221) was alive but sleeping, its main
  log unchanged since 12:33 on 21 October and no worker children, so I held to the one-worker rule and report it.
- Diagnostics (not counted cells): `tools/beh_diag.py` re-runs a counted run deterministically to a generation and dumps the response
  signatures and the commonest types; one run (`beh-max` rep 0, generation 200) finished (`runs/hooks_beh/diag_beh-max_0_200.md`),
  the rest were stopped when the coordinator asked to finish. `tools/beh_types_from_rows.py` and `tools/beh_failed_islands.py` read
  the stored rows only. A `post` hook was added to `run_one` (diagnostics only; it does not touch the run).
- Code changes during the queue were confined to non-numba files (`hooks_beh_run.py`: `nrep`, `inert`, the `post` hook;
  `hooks_beh_report.py`); the compiled evaluator and kernel did not change after the first counted batch.
- Not done: the spec's (100, 64, 1,000) geometry for the behavioural cells (cost, 2.3); M1 snapshots are every 10 generations to 200
  and then 300, 500; the 15-minute RS/RE waiting rule did not arise.
