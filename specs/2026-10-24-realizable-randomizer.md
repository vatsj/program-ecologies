# Spec: a private random tape in the realizable language, 2026-10-24

Status: draft by the RE; reviewed by gpt-6.1-sol (folded [after review]), then gemini-4-argon (`--mode amended`, folded [after second review]); to be run
by a Sonnet subagent. Queue item 59. The RS (2026-10-24): "1 sgtm as an experiment! A private random tape is an
acceptable primitive." Follows RESULTS "Rock–paper–scissors and mixed actions", "Rock–paper–scissors with a compute
price", "Mixed actions in two-role games", and DEFERRED 16. REJECTED.md checked: the shared coin `X` (one draw per
match) was dropped for the PD; this tape is private and per program, so nothing is re-opened.

## Why

Every mixed-action result so far used two idealizations: a free coin (`X`, `coin`) and a free exact reader (`cr`), in
a DSL that cannot tell a simulation from play. The realizable language L_T (RESULTS "The realizable language", milestones
1–5) has none of them: programs are deterministic λ-terms, reading is a sound bounded prover or a checked certificate,
and every step is charged. The question is whether the DSL findings survive: (1) under a compute price, the coin plays
RPS's mixed equilibrium; (2) in the inspection game, a responsive inspector over compliant inspectees makes the
efficient outcome the modal island, and commitment appears when only the inspectee reads.

## The primitive

**The private tape.** At the start of each root evaluation the runtime gives the evaluating program a fresh private
tape of m independent uniform digits over an alphabet of size r (r = 3 for RPS, r = 2 for inspection; m = 3 in the main
cells, m = 4 as a check). A new L_T primitive `tape i` returns digit i. The opponent can read the program's source,
including how it uses the tape, but never its tape. A bounded simulation (`run`) of another program gives the
simulated program its own fresh tape, independent of the real one, so simulation samples and cannot predict.
Pseudo-randomness computed from quotes is not a coin and is included as a control (below).

**Reasoning about it.** K_T is extended soundly in one of two ways, both implemented:
- *For-all-tapes atoms:* a box `□(x plays a against y)` is derivable only if it holds for every tape of every program
  whose tape the evaluation reads. This keeps K_T's soundness proof unchanged (tape digits are free variables).
- *Counted-probability atoms:* a new atom `pr(x, y, a) ≥ k / r^M`. [Made precise after review] Randomness is indexed
  by (invocation, tape position): every root or nested evaluation is an invocation with its own m-digit tape, and
  repeated reads of one position return the same digit. The evaluation of x against y is a finite random decision
  tree over these digits; the probability is the weight of the leaves where x plays a, computed over a fixed padded
  assignment space (every invocation's full m digits, M = m × the number of invocations the budget allows), not a
  trace-dependent denominator. It is proved by enumeration or **checked from a carried count certificate**: the
  certificate is bound to both quotes, the checker version, the fuel budget and the evaluation context; it lists
  assignments with weights and outcomes; the checker replays exactly those assignments (never fresh draws), checks
  coverage, uniqueness and weights, and cannot certify an execution under a larger budget or different charging than
  actual play. Cost is charged per replayed assignment (a one-digit mixer certifies p = 1/2 with two). [After second
  review] For a `≥` atom, "coverage" means the listed assignments are disjoint prefixes that produce a and whose
  weights sum to at least k/r^M; the losing branches need not be listed. A program whose replay never reads the
  opponent's quote (a tape mixer) carries an **opponent-generic** certificate, bound to its own quote, the checker
  version and the budget, with the opponent a wildcard; the checker verifies that the replay never reads it (milestone
  4's opponent-generic certificates).

Soundness test before any cell: on every named pair, the derived atoms are true (0 false atoms), as in milestones 3–4.
[After review] Named-pair agreement is a regression test, not a soundness argument; the tests also cover adaptive and
nested cases (branch-dependent simulation, repeated tape reads) and adversarial certificates (malformed, duplicate or
omitted assignments, wrong weights, a certificate for another budget), all of which must be rejected.

## Games and programs

Both games use the conventions of the DSL runs: the RPS payoffs with forfeit (fuel exhausted) losing to every action;
the inspection payoffs (I, C) = (−1, 0), (I, K) = (−1, −3), (N, C) = (0, 0), (N, K) = (−4, 1). **Price:** c per evaluation
step, calibrated so that exhausting the fuel cap K costs 0.12 (the DSL's c·D at c = 0.01), and c = 0 as a control. One
population for RPS; fixed roles for inspection.

**Grammar.** A template grammar over L_T (milestone 2's approach) with a length prior over template spellings,
containing at least:
- constants (R, P, S; I, N; C, K);
- tape mixers: actions chosen by thresholds on the tape value (all probabilities k/r^m expressible at m = 3: in RPS the
  uniform mixer is one digit; in inspection 1/8 … 7/8, so 3/8 and 5/16 at m = 4 exist);
- the pseudo-random control: actions chosen from a hash of the opponent's quote (predictable by simulation);
- simulators: play what beats (RPS) or best-responds to (inspection) one `run` of the opponent against me;
- provers: FairBot-shaped responsive programs, for inspection the **responsive inspector** "inspect unless I can prove
  the inspectee complies against me" (FairBot with inspect as defect), and for the inspectee "comply iff I can prove
  the inspector inspects me with probability ≥ k/r^M" (a counted-probability reader, with its threshold in the
  template);
- certificate carriers: a tape mixer carrying a count certificate for its own probability, so that readers check
  rather than search (milestone 4's lever).

## Objects

The ε = 0 seed lottery (primary): RPS one population N = 100, 64 islands; inspection N = 100 per role, 64 islands;
mN = 1, 40 runs, horizon 2,000, paired founders across arms. Static tables (all pairs, exact values over tapes) before
any lottery. The ε → 0 chain only as a diagnostic, on the whole monomorphic class space where it fits in memory.

**Arms.** Full (all of the above); no-prover (constants, mixers and simulators kept; provers and carriers removed);
no-tape (deterministic programs only, the pure arm); pseudo-random-only (tape mixers replaced by quote hashes); for
inspection, inspector-only reading and inspectee-only reading. c ∈ {0, c₀} with c₀ the calibrated price. [After review]
Every arm keeps the full grammar's prior and disables a capability in place (a disabled template plays a fixed
default and keeps its prior mass), so founder abundances are matched across arms; [after second review] the defaults
are stated per class before any cell: in RPS disabled templates cycle R, P, S across spellings so no action gains
founder mass; in inspection disabled inspectors default to `N` and disabled inspectees to `C`, and the renormalized arm
is co-primary wherever the default shifts a founder share by more than 0.05; renormalized-grammar arms are
reported beside the primary ones. The grammar, template lengths, certificate encoding and costs, and evaluator
conventions are frozen in the notes before any cell. Selection uses exact expected payoffs over tapes (the tables);
a 10-run sampled-encounter check is run in the primary inspection cell. Raw game payoff is reported beside the
compute-adjusted payoff, and one cell varies the fuel cap K at fixed c, since recalibrating c·K = 0.12 alone confounds
more computation with cheaper computation. A size check (400, 16), 20 runs, in the primary inspection cell; the main
results are a transfer test at N = 100. Intervals are clustered by run; unresolved runs are extended, not counted as
absorbed. Hand-checked compliance thresholds: an inspectee prefers to comply iff 4p − 1 > 0, so certificates below,
at and above p = 1/4 are included.

## Statistics

As in the DSL runs: individual mixing, net exploitability (against the best program of the arm's grammar), forfeits
and fuel exhaustion, class shares (tape mixers, the pseudo-random control, simulators, provers, carriers), and for
inspection the efficient and committed-and-compliant island shares, inspector payoff, inspection and cheating rates;
the steps spent per encounter by route (proof search, certificate check, simulation); support, transitions and exits.

## Predictions (the RE's; falsifiers in brackets)

1. *Statics.* 0 false atoms over all named pairs and adversarial cases; on explicitly terminating hash fixtures under
   matched execution semantics the pseudo-random control is predicted exactly by a simulator and exploited by it (+1
   in RPS), while the uniform tape mixer is not (expected 0); a biased tape mixer is exploited only to the extent of
   its bias [a false atom, an accepted bad certificate, or a simulator that predicts a uniform tape mixer].
2. *RPS, c₀.* The uniform tape mixer holds at least 0.6 of the lottery population and forfeits are below 0.1 of plays
   (the DSL priced run: `X` 0.84–0.87) [tape mixers below 0.3]. In the pseudo-random-only arm individual
   programs are predictable (statewise exploitability ≥ 0.3) [≤ 0.1]. *Counter-prediction (gpt-6.1-sol),
   registered:* deterministic individuals can form a balanced aggregate, so population exploitability may be low
   even when individuals are predictable; both are reported.
3. *Inspection, full arm, c = 0.* Efficient islands are at least 0.3 (DSL free oracle 0.65), held by the responsive
   inspector over compliant constants [below 0.1]. [After review] At c = 0 steps matter only through the fuel cap, so
   any gap to the DSL is budget-dependent; the fuel-varying cell measures it.
4. *Inspection, inspectee-only reading, c = 0.* Committed-and-compliant islands are at least 0.5, carried by tape
   mixers with count certificates at probabilities above 1/4 (the DSL ablation: 0.91) [below 0.2].
5. *Cost of the two routes* [revised after review: the ratio is fixed from the hand table, not from enumeration size].
   The notes' hand table gives the per-encounter steps of the responsive inspector's proof and of the committed
   inspector's count-certificate check; the measured ratio is within a factor 2 of the hand table's [outside].
6. *Price.* At c₀ the route that the hand table makes cheaper survives the price better [the dearer route survives
   better]. [After second review] The hand table prices the responsive inspector's bounded search against a depth-1
   constant explicitly, beside a one-digit mixer's two-assignment check, since search may be the dearer route.

## Required outputs

- `src/lt_tape.py` (the tape primitive, K_T extensions, count certificates), `src/lt_tape_games.py` (grammar, tables,
  lottery), runner and report, importing `src/lt*.py`; no existing file edited.
- `tests/test_lt_tape.py`: tape privacy (a run draws a fresh tape), soundness on named pairs, the count certificate's
  check, the pseudo-random control's predictability, the price calibration.
- `notes/lt-tape.md` (§1 hand table before code; §2 deviations).
- `predictions/2026-10-24-realizable-randomizer.md`, before any counted cell, with the RS's statement first.
- `runs/lt-tape.md` and `.json`, `runs/lt_tape/` (small files).
- Hand back RESULTS, REJECTED, THEORY and NOTATION drafts; do not edit the shared docs.

**Budget and scale guard.** L_T evaluation is slow; measure one encounter's steps and wall time and one job's peak RSS
first, and size the lottery to fit (cut order, disclosed: m = 4 checks, the chain diagnostic, c = 0 in RPS, the
pseudo-random-only arm in inspection; never cut the full and inspectee-only inspection arms or the soundness test).
Other subagents may be running: check `ps` before each batch and use at most 2 workers while any is alive. One job per
process; no `multiprocessing.Pool`; one background wait per batch that exits at completion and fires if the log stops
changing for 2 hours; never poll periodically.
