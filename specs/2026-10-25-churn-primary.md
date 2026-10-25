# Spec: does churn among the fair pairs happen in the primary object? 2026-10-25

Status: draft by the RE; reviewed by gemini-4-argon (folded [after review]), then gpt-6.1-sol (`--mode amended`, folded [after second review]); to be run
by a Sonnet subagent. The RS (2026-10-25): "I find it especially suspicious that the behavior as stated relies on the
veto, which I consider an experimental artifact rather than a core part of our equilibrium notion. Can we replicate the
dynamics in 'the primary object'? Extensional or Turing-complete would convince me." Follows RESULTS "Deriving
immigrant rejection for stable sets on islands, Step 0", "A migration window for stable sets on islands", "Stable sets
on islands" and "Three-player majority divide-the-dollar". REJECTED.md checked: nothing re-opened.

## Why

Under the contract layer with the hand-written veto (and with the weak-consent farsighted table), islands rotate among
the three fair pairs, because immigrants dent a member's realized share and the excluded slot's even split is then a
strict improvement; the rotation keeps all three pairs present under migration. Both mechanisms live in the contract
layer, which the RS regards as an experimental artifact. The primary object is the ε = 0 seed lottery of programs that
read each other and play encounter by encounter, with no contracts and no veto. The stored primary-object runs (weak
and modalPA arms, `dollar3`, n = 6) never kept coverage under migration (consensus 0.95 by 10,000 at mN = 1), and their
member-to-member flips were rare and by drift. This experiment asks, with richer grammars and a Turing-complete
language, whether encounter-level reading by programs produces the same churn and coverage.

## Design

**Game.** Three-player majority division as in `dollar3`: each slot names a partner (one of the others, or all) and a
demand in {1/3, 1/2, 2/3}; pairs form on mutual naming with demands summing to at most 1; the grand coalition at thirds.
Payoffs in sixths. V\* = the three fair pairs.

**Arm E (weakly extensional).** The `dollar3` DSL (`src/dollar3*.py`) in the modal arm, with the grammar enlarged to
n = 10 for the lottery (the chain is not needed; programs are sampled from the length prior), so that conditionals on
both other slots and nested reads exist, e.g. "name j iff j provably names me with demand 1/2, else name k iff k does,
else name j". The notes list the readers that can implement the churn step: take the excluded slot's fair offer when
the current partner does not name me. [After review] The notes report, before any cell, the prior mass at n = 10 of the
churn-capable readers and of the plain fair-pair establishers; a control arm **E-min** uses the n ≤ 6 grammar augmented
only with the minimal churn-capable reader templates, so prior dilution at n = 10 cannot explain a null result.

**Arm T (Turing-complete).** L_T (`src/lt*.py`) with a template grammar for majority division: constants; FairBot-style
pairing readers (name the slot that provably names me with a fair demand, by checked certificate or bounded proof,
with a fixed or tape-coin tie-break when both do); simulating readers (one capped `run` of each other slot); and the
private tape (RESULTS "A private random tape in the realizable language"). Capped simulation as the RS ruled; the
depth price at c = 0 and at the calibrated c₀ as a sensitivity. [After review] The template list and its prior weights
are fixed in the notes before launch, with the prior weight of symmetric two-partner readers stated beside constants
and single-partner readers; a compact prior that seeds islands with flexible readers could manufacture churn, so a
second prior (two-partner readers at one tenth of their weight) runs beside it.

**Lottery.** ε = 0, N = 100 per slot, I = 64, one connected component, mN ∈ {0, 0.01, 0.1, 1}, 40 runs, 10,000
generations (20,000 for runs not resolved), paired founders across mN; the migration-window statistics (modal outcome
per island every 50 generations, debounced member-to-member flips, coverage, consensus, efficiency, the stated and V\*
targets), and for comparison the stored contract-layer rows (baseline, gV, gKRw) at the same mN.

**Mechanism probe.** On islands sitting on a fair pair, inject single immigrants of each class into the member slots
and the excluded slot, and record whether the island switches pair and through which route (immigrant takes over,
excluded slot's offer accepted by a reader, drift). [After review] Stratified by the excluded slot's residents: (a)
forced to a fair offer toward a member, (b) the natural composition at mN > 0. Plus a **homogeneous-reader** cell: both
member slots and the excluded slot held entirely by churn-capable readers, with a 1–5% immigrant fraction injected into
one member slot, to separate "such readers are too rare to win the founding" from "even when resident, encounter-level
switching does not move the island".

**[After second review] Additions and freezes.**
- *Arm E′ (weak arm, behaviour reading by bounded simulation):* the `dollar3` weak (simulation) arm beside the modal
  arm, so that effects are not attributed to extensional reading when they come from the free provability oracle.
- *Churn-capable means executable:* a template counts as churn-capable only if a complete hand-checked three-program
  execution (branch priority, negative guards, reciprocal naming, timeouts) takes a fair-pair island to another fair
  pair; the notes give that path for each such template.
- *Homogeneous-reader cell:* its source composition, tie-breaks and verified resident outcome are stated before
  injection.
- *Prior controls:* E-min and the reduced two-partner prior move the changed mass to weight-matched inert or
  single-partner replacements, declared in the notes.
- *Arm T frozen before launch:* fuel caps, proof budgets, certificate production and checking, timeout actions and tape
  semantics, with executable (not idealized) payoffs.
- *Baselines:* a small matched rerun of the contract-free baseline (same founders, horizon, evaluator, denominators);
  flips are reported as hazards per fair-pair island-generation with intervals, not only as ratios; unresolved runs are
  censored.
- *Probe controls:* every injection paired with a sham replacement and a naming-preserving immigrant; a matched control
  with the reader's fallback branch disabled; reader frequencies, payoff differences and encounter redirections
  recorded through each switch; tape-driven action changes separated from evolutionary replacement.
- *Scaling:* the probe at N ∈ {50, 100, 200} (establishment probability and switch time); full-run conclusions are about
  finite-size persistence.
- *Scoring:* coverage, debounce (25 generations), injection replication and resolution rules fixed in the predictions;
  each prediction scored held / partial / failed with an intermediate band.

## Predictions (the RE's; falsifiers in brackets)

1. *No churn in arm E.* Member-to-member flips per run are within 3× of the stored contract-free baseline at every mN
   (no 20–60× churn), and coverage at mN = 1 is below 0.3 of runs [flips at least 10× the baseline with coverage at
   least 0.5]. [After review] Flips and coverage are reported beside the share of islands on V\*, so that islands off
   the set (dominated outcomes, as in the stored runs) are not read as an absence of churn.
2. *No churn in arm T at c = 0.* The same, in L_T [the same falsifier]. *Counter-prediction (gemini-4-argon),
   registered:* if the template prior gives symmetric two-partner readers substantial weight (≥ 0.05), islands establish
   with them resident, each immigrant in a partner slot redirects the readers' encounters to the excluded slot, and arm T
   churns. *Counter-prediction (gpt-6.1-sol), registered:* encounter-level redirection can be common while island
   flips stay rare; any threshold depends on the immigrant fraction and the resident composition.
3. *Readers do not take fair offers at the island level.* In the probe, an excluded slot's fair offer switches an island's
   pair in under 5% of injections, because a single reader in the member slot changes only its own encounters [at least
   20%].
4. *Coverage, where present, is founders'.* At mN = 0 and 0.01 coverage is high in both arms (founder diversity), and it
   falls with mN [it does not fall]. *Counter-prediction (gpt-6.1-sol), registered:* coverage depends jointly on
   establishment and island count, with no unconditional monotonicity in mN.

## Required outputs

- `src/churn_primary.py` (+ runner, report), importing `src/dollar3*.py`, `src/lt*.py`, `src/lt_tape*.py` and the
  migration-window statistics; no existing file edited.
- `tests/test_churn_primary.py`: payoffs of named readers by hand in both arms, the flip statistic on hand-built
  trajectories, the mN = 0 arm E cell reproducing the stored modalPA lottery at n = 6 when the grammar is restricted.
- `notes/churn-primary.md` (§1 hand predictions and the churn-capable readers in each grammar, before code; §2 deviations).
- `predictions/2026-10-25-churn-primary.md`, before any counted cell, with the RS's message first.
- `runs/churn-primary.md` and `.json`, `runs/churn_primary/` (small files).
- Hand back RESULTS, REJECTED, THEORY and NOTATION drafts; do not edit the shared docs.

**Budget and scale guard.** Other subagents are running: check `ps` and free memory before each batch; at most 2
workers while others are alive. One job per process; no `multiprocessing.Pool`; one background wait per batch that
exits at completion and fires if the log stops changing for 2 hours; never poll periodically. Cut order (disclose): the
c₀ sensitivity, mN = 0.01, 20,000-generation extensions.
