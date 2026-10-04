# Spec: Conjecture 4 (no drift-closed class in the unbounded modal language) and the leak bound, 2026-10-04

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-04-conjecture4-gpt-6.1-sol.md`) and revised; changes marked [after review]. Committed before launch. To be run by an Opus subagent. Mostly theory, with a static-map extension.

## Background

THEORY §9.2 now has: Lemma 1 (fates of a single mutant from a cooperative world), Corollary 1 (universality and
drift-closure exclude each other), Propositions 2–3 (β = 1/2 derived; prices with free constants beat 1/N only through
incumbency), and Conjecture 4: no drift-closed self-cooperating class exists in the unbounded modal language. Static
evidence: none at n ≤ 11 with boxes up to PA + Con(PA), and n ≤ 9 up to PA + Con². FairBot's leak/μ (the μ-mass of its
neutral exploitable entrants divided by its own μ) is 93–96 at n = 6–11, the smallest of any unsuckerable class.

Definitions, from RESULTS "Universality against drift-closure": a class x is *suckerable* if it cooperates with some y
that defects on it; x's *neutral closure* is its component in the graph of mutual cooperation among self-cooperators;
x is *drift-closed* iff no member of its closure is suckerable.

## Task 1: settle Conjecture 4

Prove or refute, over GL on the linear Kripke chain, with box levels PA + Con^k for every k and applications THEM(ME),
THEM(THEM), THEM(^A). Make every assumption explicit. [after review] **Semantic universe.** State the result first for the
*evaluator semantics* of `src/modal.py` (linear chain, stable value as the outcome, box levels as implemented, with the
inter-level principles the evaluator uses written out), and only then say whether it lifts to modal validity or to
arithmetic provability. Keep a dependency ledger for every step: semantic theorem, arithmetic assumption, proof-budget
condition, or evaluator-only observation. The evolutionary reading of drift-closure is restricted to the rare-mutation
monomorphic chain, where pairwise mutual cooperation is exactly neutral entry; it is not claimed for polymorphic residents.

[after review] **What counts as evidence.** A class with no suckerable closure member at n ≤ 13 is a *truncation-closed
candidate*, not a refutation: it may acquire a suckerable neighbour at greater length or box depth. For each candidate,
search for a larger or deeper witness directly rather than enumerating the whole larger universe. Nonexistence at
successive cutoffs is evidence for the conjecture, not proof. If it holds only for a sub-language, say which. If false, give the
counterexample and check it with the evaluator (`src/modal.py`, `src/modal_lv.py`).

Route to try first: a sibling construction. For a self-cooperating x, consider x′ = or(x, φ) where φ is a provable-
cooperation test that members of x's closure tolerate, so that x′ is in the closure and is suckerable. The question is
whether such a φ exists for every x, in particular for prudent families such as P\* that defect on ALLC-cooperators.

Say, for every step, whether it uses GL-specific structure (Löb, unique fixed points, the linear chain) or only
"programs can test provable cooperation", which bounded proof search over arbitrary source also provides (Critch 2019,
bounded Löb). The project's long-term goal is cooperation among Turing-complete programs with source access, so the
transfer question matters as much as the theorem.

## Task 2: the leak bound

Is FairBot leak/μ-optimal among unsuckerable classes at every n, and is leak/μ bounded uniformly in n? Extend
`src/moat_static.py` to the largest n that fits in about an hour on 3 cores (n = 12 and 13 are the targets). Report, per
n: the number of classes, the unsuckerable classes, each one's leak, μ and leak/μ, and the minimum.

[after review] **Measure specification.** Define leak exactly as `src/moat_static.py` computes it: the μ-mass, at cutoff
n, of classes that are neutral entrants into all-x (mutual cooperation with x, self-cooperating) and are suckerable
(direct leak), and separately the mass of the whole closure's suckerable members (closure-reachable leak). μ is the
length prior over programs at cutoff n, summed over the behavioural class after the evaluator's deduplication; state the
equivalence relation. Reproduce the n ≤ 11 numbers before extending. Report program counts and prior mass by length and by
box depth, and the leak contributed by each new length shell, since a uniform bound needs a summable tail: the test is
whether the shell-n contribution to FairBot's direct leak decays geometrically in n.

## RE predictions (Fable)

1. **Conjecture 4 holds** for the full language. The proof goes through a sibling construction, and the sibling exists
   because the grammar is closed under `or` with a provable-cooperation atom: for every x there is an x′ in its closure
   that cooperates with some program that provably cooperates with ALLC-tolerators, and that program's own sibling
   defects on x′. [after review] Sol's point, which I accept: the bottleneck is *closure membership*, showing that x′
   still mutually cooperates with x (a prudent x may reject the sibling), not constructing the disjunction. *Falsifier:*
   a counterexample proved closed against the full language and checked by the evaluator. A truncation-closed candidate
   at n = 12 or 13 is evidence against, not a falsification.
2a. **Lemma 1 and Corollary 1 transfer** to deterministic programs with bounded proof search over source: they use only
   determinism, the fixation rule, and the existence of a cooperate-with-everyone program that is honest and suckerable.
   *Falsifier:* a step in either proof that needs the linear chain or full GL.
2b. **The sibling construction transfers only under budget assumptions** [after review: split from 2a at sol's
   suggestion]. It needs the source language closed under disjunction with a provability test *and* a proof budget large
   enough that the sibling's self-cooperation proof fits, which bounded Löb (Critch 2019) gives above an explicit
   threshold. The subagent should state that threshold in terms of the proof lengths involved. *Falsifier:* a step with no
   bounded analogue at any budget.
3. **FairBot is leak/μ-optimal at n = 12 and 13,** with direct leak/μ in [85, 105], and the shell contribution to its
   direct leak decays geometrically (ratio of successive shells below 0.7 from n = 10 on). *Falsifier:* another
   unsuckerable class with smaller leak/μ at either n, FairBot's ratio outside the interval, or shell contributions that
   do not decay. [after review] Sol expects the plateau to be weakly diagnostic without the tail argument; the shell
   decay is that argument's empirical half.
4. **No drift-closed class at n = 12 or 13** (the static form of 1).

## RS predictions (Jacob)

(Optional.)

## Procedure for the subagent

[after review] Beyond this task, the program needs a quantitative theorem relating witness complexity and mutation mass to
escape rates as N grows: a tiny leak defeats exact closure without necessarily defeating efficient concentration. Note
in the write-up what the static map says about that, but do not attempt it here.

Work in small steps and make a tool call at least every few minutes; write proof attempts incrementally to
`notes/conjecture4.md` with Write and Edit. Earlier attempts at this task stalled by reasoning for long stretches with no
tool call. Write and commit `predictions/2026-10-04-conjecture4.md` carrying the RE predictions above before the extended
static runs. At most 3 workers; stop runs projected beyond about 2 hours; do not edit RESULTS.md, REJECTED.md, THEORY.md
or CLAUDE.md; do not touch `runs/d8dcd7ee9a/row.json`. Hand back the proof or counterexample, draft RESULTS, REJECTED and
THEORY text, at most 5 lines on what matters, and the branch and commits.
