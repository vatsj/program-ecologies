# Spec: rock–paper–scissors with a compute price, 2026-10-23

Status: draft by the RE; reviewed by gpt-6.1-sol (folded [after review]), then gemini-4-argon (`--mode amended`, folded [after second review]); to be run
by a Sonnet subagent. Follows RESULTS "Rock–paper–scissors and mixed actions" and DEFERRED 16. The RS (2026-10-23):
"there's an old thread that considers compute costs nontrivial, so I'd lean against [counting mutual non-termination
as a free tie]. I'd call this a failure that shows a need for a random-action primitive … Opponents can see the coin
and simulate the flip, but they can't actually predict how the opponent flip will land." The RE's reply, accepted by
the RS ("go with your default price"): the coin primitive was already present (`X`, `coin`); what failed is that
non-play was free; the default price is a cost per application level, so a forfeit costs the whole cap. REJECTED.md
checked: atom pricing (2026-10-01) killed PD cooperation through an entry barrier and a price ladder; this spec prices
run time, not atoms, in a zero-sum game, and re-opens the runtime price that the RS left open on 2026-09-30 (its form
is fixed here by the RS's acceptance of the default).

## Why

Unpriced RPS reached the game's value by mutual non-play: readers like `next(THEM(ME))` forfeit against each other
and tie at 0, so the seed lottery was held by them (0.52–0.69 of plays forfeited in the coin arms) and unexploitable
individual mixing appeared only in the chain near N ≈ 10⁷. If computation costs something, two readers looping on
each other pay the whole cap, while `X` pays nothing and still earns 0 against everyone. The RE's prediction is that
the coin and coin-guarded readers then take the lottery, and the chain's slow approach (driven by cap residues of
size 2⁻⁷ to 2⁻¹³) becomes fast, since every forfeiting class is now beaten by a margin of order c·D.

## Design

**Base.** The object, grammar, arms, evaluator, depth cap D = 12, forfeit rule, classes, chain and lottery of
`specs/2026-10-23-rps-mixed.md`, reused by import from `src/rps*.py` (no edits).

**The price (a depth price; the RS accepted "a small cost per application level, so a forfeit costs the whole
cap").** [Made operational after both reviews.] Each player pays c times the application depth its own root
evaluation reaches: the length of the deepest chain of nested applications executed, including inside any opponent
evaluation it runs by simulation or reads exactly, as an expectation over its own coins (for `coin`, only the branch
taken; for `cr`, the deepest branch its exact computation explores). D caps depth, so a forfeit pays exactly c·D and
no evaluation pays more. `X`, constants and `coin` of constants pay 0. A player's payoff is the game payoff minus its
own cost; the opponent's cost does not enter. **Sensitivity: a work price** (c per application node executed, all
branches of a `cr` computation included) at c = 0.01 in the sample and exact arms, with the maximum node count over
the table reported; it separates the semantics of exact reading from the branching tax it would pay under work
pricing. The notes' hand table gives cases where depth and work differ (a `cr` reading a `coin` opponent; a reader of
a reader of a constant). The game is no longer zero-sum, so the chain may now
hold polymorphic states. [After review] Use `chain_log.LogChain` with closure-seeded exploration plus multi-start
replicator searches for attractors (support up to 6), with support-size diagnostics, a log-θ sensitivity (two values)
and twin-expanded results; any unresolved cycle or attractor is marked indeterminate (THEORY §5), not given a
stationary weight. **Classes are recomputed from the priced payoff rows and columns** (programs with equal game
payoffs can differ in work, also against third parties); the report says which unpriced classes split, and source
multiplicities, mutation masses and twin drift are kept.

**Price panel.** c ∈ {0.001, 0.01, 0.05} (forfeit cost 0.012, 0.12, 0.6), plus c = 0 from the stored run as the
reference.

**Arms.** pure, sample, sample-matched, exact (as before), each priced. Sensitivity: exact-br priced at c = 0.01.
[After review] Controls at the c = 0.01 forfeit charge: **forfeit-only** (only a forfeit is charged, c·D; successful
reading is free), which separates removing free non-play from taxing reading; and a **depth panel** holding c·D = 0.12
fixed at D ∈ {8, 16}, which separates the timeout penalty from changes in available reasoning (sample and exact
arms).

**Objects.** The ε → 0 chain at N ∈ {10², 10³, 10⁴, 10⁵}, w = 0.3; the ε = 0 seed lottery at (100, 64), mN = 1, 40
runs, generation 2,000, paired founders with the unpriced run (same seeds). Size cell (400, 16), 20 runs, at c = 0.01.
[After both reviews] An island's *support* is its set of classes with share ≥ 0.05. An island is *resolved* when its
support has not changed over the last 500 generations (a stable polymorphism counts as resolved), *cycling* when its
support revisits an earlier support within that window (reported as indeterminate, not extended), and otherwise
*unresolved*; runs with any unresolved island continue to 10,000 generations (rule fixed here). Founders are drawn at
the program level from the prior over spellings with the stored seeds and mapped to the priced classes after seeding,
so pairing with the unpriced run survives class splits. All lottery contrasts are paired and run-clustered (islands are not independent replicates).

**Statistics.** As in the unpriced spec, with two definitions fixed in advance:
- **exploitability** is measured on the game payoff alone (the best game payoff any program of the arm's grammar earns
  against the class or population), so it is comparable with the unpriced run; [after review] **net exploitability**
  (the exploiter's game payoff minus its own cost) is reported beside it, since a costly exploiter need not be an
  evolutionary threat;
- **cost paid**: mean c × applications per play, the share of plays forfeited, and the aggregate net payoff (RPS's
  outcomes are all Pareto-efficient before pricing; this run tests waste and exploitability, not the efficiency
  conjecture).
[After second review] Predictions 2, 3, 5 and 7 are scored on **net** exploitability (equal to the game-payoff
measure at c = 0, so the unpriced comparisons stand); game-payoff exploitability is reported beside it.
Also: the named classes' shares (`X`, constants, `next(THEM(ME))`, `cr(THEM(ME))`, guarded readers), individual
mixing, the three readings (W, M, I) by island, support, transitions and exits (CLAUDE.md rule 4).

## Predictions (the RE's; falsifiers in brackets)

1. *Statics.* Under any c > 0, `X` invades, and dominates at every frequency of the two-type contest, every class
   whose self-play forfeits with positive probability (`X` pays 0 and earns at least 0 against everyone, +p_f against
   a program that forfeits against it with probability p_f; the reader pays at least c·D·p_f in self-play) [a
   forfeiting class that `X` does not dominate].
2. *Lottery, c = 0.01, sample and exact arms.* Forfeited plays ≤ 0.1 (unpriced 0.69 / 0.52); islands with individual
   mixing ≥ 0.6 (unpriced 0.22 / 0.25); islands with exploitability ≤ 0.05 ≥ 0.6 (unpriced 0.58 / 0.25) [forfeits
   ≥ 0.3, or mixing islands < 0.4].
3. *Chain, c = 0.01, N = 10⁴.* Exploitability ≤ 0.1 and mixing ≥ 0.6 in sample and exact (unpriced: 0.29 / 0.31 and
   0.43 / 0.31) [exploitability > 0.2 or mixing < 0.4]. The approach is fast: by N = 10³ the chain is within 0.1 of its
   N = 10⁵ values [it is not]. *Counter-prediction (gpt-6.1-sol), registered:* forfeits respond sooner than
   individual-mixing mass; free constants and `X` stay neutral with each other and entry rates still bind, so
   convergence by N = 10³ is far from secure.
4. *Dose.* c = 0.001 lies between unpriced and c = 0.01 on forfeits and mixing; c = 0.05 is at least as mixed as
   c = 0.01 [non-monotone in c on forfeits]. *Counter-prediction (gpt-6.1-sol), registered:* forfeits decline
   reliably but individual mixing need not be monotone, because a higher price also removes readers that exploit
   constants and can favour population-level mixtures of constants.
5. *Pure arm.* With no coin, the price removes the readers' free tie, but no program mixes: islands hold constants and
   readers, and statewise (individual) program exploitability stays ≥ 0.3 at every c [≤ 0.1 at any c]. [Revised after
   review] A balanced polymorphism of constants can have zero population exploitability; population exploitability is
   reported without a prediction.
6. *Who mixes.* At c = 0.01 the coin `X` holds more lottery mass than every source-reading class combined [readers
   hold more]. Low confidence: guarded readers also beat constants, and the chain at c = 0 gave them more mass than
   `X` at large N. *Counter-prediction (gemini-4-argon), registered:* a coin-guarded reader pays about c to read a
   constant and earns +½ to +1 against the constant-heavy founding scramble while avoiding most self-forfeits, so
   guarded readers hold more lottery mass than `X` at c = 0.01; `X` dominates only at c = 0.05 or in the large-N
   chain.
7. *Exact reading.* Exact − matched exploitability is not negative at c = 0.01 in either object [negative, with a
   run-clustered interval excluding 0]. Low confidence.

## Required outputs

- *Code:* `src/rps_priced.py`, `src/rps_priced_run.py`, `src/rps_priced_report.py`, importing `src/rps*.py`; no
  existing file edited.
- *Tests:* `tests/test_rps_priced.py`: level counts by hand for the named classes (constants 0; `next(THEM(ME))`
  against a constant 1; mutual readers D), the price at c = 0 reproducing the stored payoff tables exactly, and the
  statics of prediction 1.
- *Notes:* `notes/rps-priced.md` (§1 hand table of levels and priced payoffs before code; §2 deviations).
- *Predictions:* `predictions/2026-10-23-rps-priced.md`, committed before any counted cell, with the RS's statement
  first.
- *Runs:* `runs/rps_priced/` (small files; no `.npy`, `.npz`, `.pkl`), verdicts in `runs/rps-priced.md` and `.json`.
- *Hand back* RESULTS, REJECTED, THEORY and NOTATION drafts; do not edit the shared docs.

**Budget and scale guard.** At most 3 workers, capped by memory (one arm build peaked at 1.3 GB unpriced). One job per
process; no `multiprocessing.Pool`. Waiting: watch short commands; for long batches wait on one background command
that exits at completion and also fires if the log stops changing for 2 hours; never poll periodically. If the budget
forces cuts, cut in this order and disclose: the size cell, exact-br, the depth panel, c = 0.05, N = 10⁵.
