# Behavioural hooks: notes (2026-10-21)

Spec `specs/2026-10-21-behavioural-hooks.md`; predictions `predictions/2026-10-21-behavioural-hooks.md` (committed 9d3bdb3,
before any code). **Status: stopped at the launch gate; no counted cell was run.** The gate failed on one entry of the named
table (below). Every number here is a static computation; nothing is a lottery statistic.

## 1. Hand predictions (before the solver)

Written in the predictions file (last section) and repeated: the five other hand statics agree with the RE; PrudentBot (key
box a and box not d, all boxes level PA) against FairBot is mutual defection, not mutual cooperation, because FairBot
cooperates with DefectBot at world 0.

## 2. What was built, and the gate

Code (new files only; no existing file edited): `src/hooks_beh.py` (the key family, the quotient and prior, the registry
programs, the generalized evaluator `eval_match_beh`, packed specs `spec_of_beh`, the named programs, an independent
pure-Python Kripke reference `ref_match`), `tests/test_hooks_beh.py` (14 tests, all pass), `tools/beh_gate*.py`.
Not built: the kernel, runner and report (`hooks_beh_kern/_run/_report`), which wait on the gate.

**The family.** Atoms a, c, d; connectives not, and, or, box; every atom under a box; depth <= 2, size <= 7 nodes. Spellings
of size s (modalized, depth <= 2, ordered pairs counted as in `modal.py`): a(2..7) = 3, 9, 36, 174, 855, 4,437. Classes by
truth on all words of length <= 5 (stable at 4, 5, 6): **600 non-constant classes plus 2 constants (dropped)** for the full
family (sizes 2: 3, 3: 9, 4: 16, 5: 52, 6: 150, 7: 370), **199 classes** for the a-free family (atoms c, d). Prior: the
arm's length prior, bits(s) = log2 a(s) + 2 log2 s + 1, each class at its shortest member (box a, box c, box d: 0.2045 each;
not box a, box not a, box box a and the c, d analogues: 0.0303 each). The registry holds 320 boxed subformulas; a key needs at
most 3 of them. The evaluator needs only the specs' registry entries per match (all of them only when a stabilized reading is
wanted for a conditional write).

**The gate.** Solver (`eval_match_beh`, stabilized evaluation on finite linear GL frames, box vacuously true at world 0) and
the independent pure-Python reference agree on all 36 entries of the named table (0 mismatches). Against the RE's hand
derivation: five of six entries agree (FairBot vs TrustingBot: FairBot D, TrustingBot C; Godel predator vs itself: CC; FairBot
vs Godel predator: FairBot D, predator C, with the predator (F, F, T, T, ...) as derived; PrudentBot vs CooperateBot: D vs C;
PrudentBot vs TrustingBot: D vs C). **PrudentBot vs FairBot disagrees: the solver gives (D, D).** The convention is the spec's
(box vacuously true at world 0), so the disputed static (gemini-4-argon) is settled in the RE's favour on the predator
(FairBot exploits the predator) and the disagreement is elsewhere.

Why: PrudentBot's key box a and box not d at level PA. FairBot against DefectBot is (C, D, D, ...): it cooperates at world 0
because its box is vacuous there. So d = (C, D, D, ...) for FairBot, box not d is false from world 1, PrudentBot plays
(C, D, D, ...), FairBot (C, C, D, D, ...), stabilized (D, D). Likewise PrudentBot against itself is (D, D) and against
everyone it defects except when the partner is a provable non-cooperator with DefectBot (TrustingBot, which it exploits).
The standard PrudentBot reads the d-clause one level up (box1, PA + Con, ignoring world 0), the stored modal arm's BOX1.
With box1 on the d-clause the table matches the RE's hand derivation entry for entry (`tools/beh_gate_level1.py`:
PrudentBot (box1 d) against FairBot is (C, C) from world 0, and against itself (C, C)).

**A stronger consequence.** Over all 801 keys (the 600 full-family classes, the 199 a-free classes and the legacy open keys) and
both defaults (HOOK(0,D) + (key -> C), HOOK(0,C) + (key -> D)), no one-fill program is prudent, that is D against both
CooperateBot and DefectBot and C against FairBot and against a copy of itself (`tools/beh_gate_extra2.py`; a test pins it). So
in the level-PA grammar as specified there is no PrudentBot-equivalent at all, and predictions 3 (the PrudentBot clause) and 5
cannot be scored as stated. Under a box1 operator (one node) PrudentBot has six nodes and is in the family. FairBot-signature
keys (on HOOK(0,D) + (key -> C), signature against CooperateBot, DefectBot, FairBot, TrustingBot, predator, a copy of itself
= C D C D D C) are 116 of the 801 keys, 0.494 of the full family's prior mass.

**Choices made on ambiguous points (recorded now, before any run).**
1. *Quotient.* The spec says GL-equivalence; I quotiented by equivalence on finite *linear* frames (GL.3), which is the
   semantics the evaluator uses and is coarser than GL (every GL-equivalent pair is merged; the converse can fail on branching
   frames). Exact GL-equivalence of depth-2 types over three atoms is not enumerable (the type space is doubly exponential);
   the class count is stable under longer words (600 at word lengths 4, 5, 6).
2. *Prior.* "Geometric in nodes, the repo's ratio": taken as the arm's length prior (`modal.py`, `hooks-w.md` §1), which is
   what the repo calls its length prior. Per-spelling weight 1/(2 s^2 a(s)); a class carries its shortest member's weight.
3. *Hostile constructions* (cell 4) would be identified by (C-default, key = class of box not a, action D) and (C-default,
   key = box a, action D); C-default read from the base's shortest spelling containing HOOK(t,C) for the tag. Not exercised.
4. *Contract candidates* (cell 2 etc.): not decided; the design waits on the gate.

## 3. What the RE needs to decide before a re-launch

(a) Add a level-1 box (one node, ignoring world 0) to the key grammar, so PrudentBot is a six-node member and the spec's
hand table stands; the registry evaluator extends by one flag (a box1 entry skips world 0). Or (b) keep level PA and restate
predictions 1, 3, 5 (no prudent key exists; the prudence premium cannot be tested in this family). I recommend (a): the
prover arm's prudence is a level-up phenomenon, and the family without it has no prudent program by a computation.
