# Spec: a Turing-complete language with a bounded prover, milestone 1: FairBot by bounded proof cooperates with itself, 2026-10-06

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-06-realizable-language-gpt-6.1-sol.md`) and revised; changes marked
[after review]. To be run by an Opus subagent. Decision (RS, 2026-10-06, DEFERRED 11): a new small
Turing-complete language rather than the weak-arm DSL; the single-pair result as the first milestone; the stated end
state is that programs run their own proof search as code. [after review] The experiment is **gated on the
soundness-and-witness theorem of §1**: no table is computed until the notes contain the complete rules, the
executable witness construction with explicit proof-size and runtime bounds, and the finiteness-and-completeness
argument for the search.

## Why

Every realizability result so far lives in the modal fragment, where GL is decidable and the bounded prover K is
pruned by that decidability. The long-term goal is Turing-complete program classes with source access. The
generalization of K is mechanical in principle: K's definitional unfolding rule becomes the language's evaluation
rules, the joint bounded Löb rule stays, truth of a box is still "a derivation of the content exists within the
budget", and soundness follows from the soundness of the evaluation rules plus the Löb witness. What does not carry
over is the search (no decidability prune) and the cost (unfolding a computation costs its steps). The milestone is
to reproduce, in our own evaluator, Critch's result that bounded provers cooperate with each other above a budget
threshold, and to measure that threshold and the copy/distinct-budget structure K predicts. [after review]
Pairwise cooperation says nothing about population selection; milestone 2 is gated on milestone 1's audits.

## The language L_T [after review: executable specification]

- **Terms.** An untyped call-by-value λ-calculus with natural numbers, pairs, a fixed-point combinator, and quoted
  terms as data (de Bruijn syntax trees as nested pairs), with a step-counting evaluator `eval_K` (exactly K
  β/δ-steps; returns a value or ⊥). A **program** is a closed term p; its play against q is `eval_K(p ⌜p⌝ ⌜q⌝)`,
  read as C if the value is the constructor C, **D** if it is the constructor D, and **⊥ (timeout)** otherwise; the
  three outcomes are recorded separately everywhere, and the payoff treats ⊥ as D. Quining is supplied by the
  environment (the program receives its own source).
- **Primitives for milestone 1** (library code in milestone 3): `run_k(⌜p⌝, ⌜q⌝)` bounded simulation (C, D or ⊥);
  `eq` syntactic equality; `prove_b(φ)` bounded proof search in K_T (below), returning one of three values:
  **found** (a derivation of ⊢ φ of size ≤ b exists), **refuted** (the exhaustive search of size ≤ b completed
  without a derivation), or **⊥** (the search exceeded the program's remaining step budget under the charging
  semantics). A program's `if prove_b(φ)` branches on found vs not-found; the write-up reports which not-founds were
  refutations and which were timeouts.
- **Charging semantics** [after review], two arms run on every cell: *primitive-assisted* (`prove_b` costs one
  evaluator step; the search runs in the host; realizability caveat stated), and *search-charged* (`prove_b` costs
  the number of calculus nodes its iterative-deepening search visits, counted against the program's K). Global
  K ∈ {10⁴, 10⁵, 10⁶}; every cell reports search work, timeouts and the K at which the outcome stabilizes.
- **Formula language F** (finite per catalogue): atoms `plays(⌜p⌝, ⌜q⌝, a)` with p, q ranging over the **named
  catalogue** of this milestone (closed under the sources mentioned by the named programs, including ⌜C⌝ and
  ⌜D⌝) and a ∈ {C, D}; boolean connectives; `□_c φ` with c ≤ the outer budget. **Finiteness** [after review]: the
  candidate formulas at budget b are those built from this finite atom set with box budgets ≤ b and nesting depth
  ≤ b, and the JLöb sets S are subsets of size ≤ 3 of the box contents occurring in the reachable formulas; so the
  derivations of size ≤ b are finitely many, and **the search is exhaustive** (iterative deepening over all rule
  instances), with a completeness statement: if a derivation of ⊢ φ of size ≤ b exists in K_T, the search finds
  one; "refuted" is therefore a certified negative. Minimality is reported only when the exhaustive search at every
  lower size completed.
- **The calculus K_T.** Sequents over F. Rules: G3 propositional; **evaluation rules**: the atom
  `plays(⌜p⌝, ⌜q⌝, a)` is derivable from a derivation that the closed term `p ⌜p⌝ ⌜q⌝` reduces (by the evaluator's
  deterministic rules, one rule instance per step, so a computation of s steps gives a derivation of size s + O(1))
  to the constructor a, where a primitive call `prove_c(ψ)` encountered in the reduction is replaced by a **box
  obligation**: the step reduces to C's branch under the hypothesis □_c ψ and to the other branch under ¬□_c ψ, the
  hypothesis being discharged by a derivation of ⊢ ψ of size ≤ c (Nec) or by the refuted search; `run_k` calls
  reduce by their own evaluation; BoxEq, Nec and **JLöb(S, b)** exactly as in K (`notes/proof-length.md` §3) with the
  same cost recurrence and side condition b ≥ 1 + Σ premise sizes; no cut.
- **§1 theorem, to be written before any table** [after review]: (i) the complete rule list with the cost
  recurrence; (ii) **soundness** for the operational semantics by size induction (the evaluation case is the
  evaluator's determinism; the JLöb case is K's witness construction, re-done here with the obligation hypotheses);
  (iii) the **executable witness**: for each derivable □_b φ, an explicit derivation of ⊢ φ of size ≤ b and the
  **runtime bound** on the search that finds it under the search-charged semantics (so that a program whose box is
  true also *finds* it within K, or the K at which it does is stated); (iv) finiteness and completeness of the
  search as above. If (iii) cannot be bounded, the primitive-assisted arm is the only one that runs and the write-up
  says the result is primitive-assisted, not internalized.
- **Budgets.** K (evaluation steps) and b (proof size) per program; milestone 1 varies b on a grid and K over
  three values.

## Milestone 1: frozen named programs [after review: exact terms in the predictions file before any computation]

FairBot_b = `λ me them. if prove_b(plays(them, me, C)) then C else D`; FairBot1_b = the same with
`prove_b(¬□_b ⊥ → plays(them, me, C))` (the guard's budget index equal to the reader's own budget, the K convention);
PrudentBot_b = `λ me them. if prove_b(plays(them, me, C)) ∧ prove_b(¬□_b ⊥ → plays(them, ⌜D⌝, D)) then C else D`;
the Gödel-sentence program G_b = `λ me them. if prove_b(plays(them, me, C)) then D else C`; P\*_b =
`λ me them. if prove_b(¬□_b ⊥ → plays(them, me, C)) ∧ ¬prove_b(plays(them, me, C)) then C else D`; the constants
C and D; the **simulation FairBot** SF_k = `λ me them. if run_k(them, me) = C then C else D`; the **sloppy-checker
FairBot** SC_b, whose `prove` accepts the first candidate derivation whose end sequent matches the goal without
checking its rule applications (candidate generator: the same iterative deepening, truncated to end-sequent
matching; frozen in the predictions file); and [after review] two **harmless variants** of FairBot_b, a renamed
λ-variable spelling and a wrapper `λ me them. (λ x. x) (FairBot_b me them)`, to separate copy recognition from
cooperation.

Compute, with an independent witness replay (a second checker implemented separately from the prover) and
[after review] an **independently implemented evaluator** cross-checked on every reduction used: (i) the play
(C / D / ⊥) and the `prove` outcome (found / refuted / timeout) of every ordered pair of named programs at
b ∈ {2, …, 64} under both charging semantics and the three K; (ii) certified minimal derivation sizes and Λ where
cooperation holds; the self-cooperation threshold b\* of each program; the copy vs distinct-budget structure for
FairBot on the grid {4, 8, 16, 32}²; (iii) the soundness checker over every derived box (0 violations); (iv) the
**JLöb-disabled** calculus as a control (every cell recomputed; expected: no Löbian cooperation); (v) **tiny
hand-enumerated exhaustive proof spaces** (b ≤ 6) for FairBot–FairBot, checked by hand in the notes; (vi) the
harmless variants against FairBot_b and against each other.

## Milestone 2 (gated on milestone 1's audits; otherwise the next spec)

The length prior over L_T terms up to a node cutoff, enumeration, lumping at one global b, the cutoff at which
FairBot_b first appears, and the ε→0 chain at N = 10³ and 10⁴ with the audited solver.

## Milestone 3 (stated now, specified later): the prover as code

Replace `prove_b` by an L_T term (a derivation checker plus an iterative-deepening enumerator written in L_T), so the
proof budget is the program's own step count and the checker's source is visible; the sloppy checker becomes a
genuine program; selection acts on checkers.

## Required outputs

`src/lt.py` (language, evaluator, calculus, prover, checker), `src/lt_check.py` (the independent evaluator and
replay checker), `tests/test_lt.py`, `notes/realizable-language.md` (§1 theorem and the hand-enumerated spaces),
`runs/realizable-language.md` and `.json`, a predictions file (with the frozen terms) committed before any
counted computation, the usual hand-back (draft RESULTS, REJECTED, THEORY §9.2 and DEFERRED 2 and 11 edits,
NOTATION, ≤ 5 lines, branch from `git branch --show-current`, commits). ≤ 3 workers. Work in small steps; the §1
notes are the first commit after the predictions.

## RE predictions (with falsifiers) [after review: trichotomy respected; thresholds representation-dependent]

1. **K_T is sound and the witness is executable** (§1 proved; 0 checker violations; for every found box the
   search-charged arm finds it within K = 10⁶), **and FairBot_b cooperates with itself from a finite threshold** in
   the primitive-assisted arm with Λ = 1. The RE guesses b\* ≤ 64 but does not predict its value (representation-
   dependent, as sol says). *Falsifier:* a soundness gap, a found box the search-charged arm cannot find at any
   tested K, or no self-cooperation at any b ≤ 64 (reported as "threshold above the grid", with the certified
   lower bound).
2. **Budget structure:** no (C, D) cell on the FairBot grid under completed searches (soundness forbids
   exploitation), copies cooperate from a budget no higher than distinct budgets, and the RE guesses the distinct-
   budget condition is a threshold on min(b_x, b_y) but allows that source length enters. *Falsifier:* a (C, D) cell
   with both searches completed, or distinct budgets cooperating strictly below the copy threshold.
3. **The Gödel-sentence program is suckered, not disarmed** [after review: corrected]: FairBot_b defects on G_b
   (no derivation of G's cooperation exists, so the search refutes) and G_b then cooperates; FairBot1_b likewise;
   G_b's victim, if any, is a level-1 self-cooperation reader as in the modal arm. **The simulation FairBot pair
   mutually defects or times out at every k**, and **P\*_b never self-cooperates** (bounded Gödel II transfers).
   *Falsifier:* FairBot_b cooperating with G_b under a completed search, or P\*_b self-cooperating.
4. **PrudentBot_b self-cooperates at a finite threshold with Λ ≤ 5**, at most 8× FairBot's (K: 11 against 4).
   *Falsifier:* no self-cooperation at b ≤ 64 while FairBot's threshold is ≤ 16, or a threshold > 8× FairBot's.
5. **The sloppy checker is exploited by G_b** (SC cooperates while G defects) **and sound FairBot_b may defect on it
   while it cooperates** (sol's point: SC can cooperate before FairBot can certify it). **The JLöb-disabled control
   shows no cooperation between any two conditional programs**, and **the harmless variants cooperate with FairBot_b
   at FairBot's own threshold within +4** (cooperation is not copy recognition). *Falsifier:* SC not exploited by G,
   cooperation in the JLöb-disabled control, or a harmless variant needing > 2× FairBot's threshold.

The RS is invited to add predictions; the uncertain ones are 1's threshold and 2's min-rule.
