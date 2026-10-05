# Spec: an explicit proof system with measured proof length, in place of the stabilization proxy, 2026-10-05

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-05-proof-length-gpt-6.1-sol.md`) and revised; changes marked
[after review]. To be run by an Opus subagent. Queue item 5 (CLAUDE.md). Two parts: A measures lengths of actual GL
proofs on the free arm; B defines and runs a bounded prover. A is mandatory; B is run as far as time allows, in the
order given, and the hand-back says where it stopped.

## Why

The modal arm's box is a free sound oracle; every result that rests on it is an upper bound on what a realizable
source-reading program can do (CLAUDE.md, long-term goal). The one attempt to charge for proofs, the stabilization
proxy v(x, y) = k(y)·(1 + settle(y, x)) (RESULTS "Bounded provers"), found the gate harmless and closing nothing, but
the proxy is not a proof system: it never charges the Löb step, and its "length" is a world count. The RS has asked
for the asymptotics of *the cost of cooperation*. This spec replaces the proxy with lengths of actual proofs in a
calculus for the logic the arm already uses, GL, and asks: whether the proxy's cost ordering survives, what
cooperation costs as a function of program size and nesting depth, and whether budgets can be exploited (a budget
ladder) or only wasted.

Realizability caveat, to be stated in the write-up: GL decides the modal fragment, so proof search here is a decision
procedure with a measurable cost; for Turing-complete programs the relevant system is PA and lengths are unbounded.
GL proof length is the cost *inside the fragment the arm can express*; the Solovay translation carries provability,
not length, to PA.

## Part A: lengths in a definitional GL calculus (free arm)

**The calculus, GLS+Def** [after review: replaces "fixed-point sentences", whose representative is arbitrary].
Propositional constants P_{xy} ("x plays C against y") for every ordered pair of canonical sources; the definitional
axioms P_{xy} ↔ φ_x[P_{yx}, P_{yy}, P_{y,^A}, …] with φ_x the program's own formula as written in the DSL (boxes over
the play constants named by its atoms; `THEM(^A)` refers to the constant P_{y,A}); BOX1(s) is encoded as □(¬□⊥ → s),
which is the standard GL rendering of provability in PA + Con(PA) and needs no new atom [after review: sol's
objection was to an ad hoc constant; □⊥ is a sentence of GL, true exactly at world 0 of the chain]. Rules: a cut-free
sequent calculus for GL (GLS, Sambin–Valentini, with the Löb rule □Γ, Γ, □A ⊢ A / □Γ ⊢ □A) plus two unfolding rules
(replace P_{xy} by φ_x on either side; one step each). Every definition is guarded by a box, so by de Jongh–Sambin the
theory is conservative and decides nothing beyond GL; this is the same object as the fixed-point presentation, with
the representative frozen by the DSL syntax, so lengths are not representation-dependent beyond the DSL itself
[after review]. Report formula-symbol sizes of the φ_x as well.

**What is a theorem** [after review: the trichotomy]. The evaluator's `val[x, y]` is *truth* at the stable world
(the standard model), not provability; the evaluator's box facts hc[L, x, y] / hd[L, x, y] at the stable world are the
provability facts: hc[0, x, y] ⇔ GLS+Def ⊢ P_{xy}; hd[0, x, y] ⇔ ⊢ ¬P_{xy}; hc[1, x, y] ⇔ ⊢ ¬□⊥ → P_{xy}; likewise hd[1].
Pairs with neither a C-proof nor a D-proof exist (P\*'s cooperation is true but unprovable in PA, provable in
PA + Con(PA)); for them L = ∞ at that level. The **audit** is therefore of the four box-fact tables against
provability, on every (x, y) at n = 6 and on the n = 8 sample; an audit failure is first debugged and, if it survives,
reported as a result (the chain semantics and GL would differ), never silently classified either way.

**Lengths** [after review: certified minima versus upper bounds]. L_C(x, y) = size (number of sequents) of the
smallest GLS+Def derivation of ⊢ P_{xy}, found by iterative deepening on size, which certifies minimality; L_D for
⊢ ¬P_{xy}; L_C¹, L_D¹ at level 1. Λ = number of Löb-rule applications in the minimal derivation (report the minimum
over minimal-size derivations). At n = 8 the search is capped (size ≤ 400 or a wall-clock cap per pair); a capped
search reports an *upper bound* from the best derivation found if any, flagged uncertified, and is never regressed
as an exact length. Hand-check ALLC, D, FairBot, `BOX(THEM(^D))`, the □⊥ reader `BOXD(THEM(^C))`-type classes, one
nested pair and one PrudentBot pair, and include the derivations in the notes.

**Scale.** n = 6 (66 classes, 4,356 ordered pairs) exhaustively; n = 8 (610 classes): all pairs within the prover
family P, its siblings and fakers (the classes named in RESULTS "Conjecture 4" and "The scramble lemma"), plus a
μ-weighted random sample of 5,000 pairs. Report search time per pair and the fraction certified.

**Measurements.**
1. Distributions of L_C, L_D, Λ; the cost table for P, its siblings and fakers; L(x → sibling)/L(x → x), which the
   proxy put at ≥ 2.
2. Comparison with the proxy: Spearman over pairs with v > 0; a table of the largest disagreements with their
   derivations.
3. Scaling of the cost of cooperation among mutually cooperating establisher pairs: L_C against |x| + |y| (nodes)
   and against nesting depth; Λ against nesting depth. Report both the fit and the residual structure; compare
   tree-size with shared-DAG size of the derivation [after review].

## Part B: a bounded prover (operational) [after review: rewritten]

The bounded arm is not a lookup of unbounded lengths. A budgeted program x_b carries budget b and its box atoms are
*bounded* boxes □_b, read as "there is a derivation of size ≤ b in the bounded calculus K". K is GLS+Def with every
box annotated by a size and with accounting that makes it **sound by construction**:
- unfolding and propositional rules carry annotations through unchanged;
- the K axiom / distribution □(A → B), □_a A ⊢ □_{a+c₁} B, with c₁ the size of the distribution derivation;
- the bounded Löb rule: from a derivation of size s of ⊢ □_b A → A with b ≥ s + c₂, infer ⊢ A with the resulting
  derivation of size s + c₂ (c₂ the fixed overhead of the Löb construction in K). Its soundness is the statement that
  a derivation of A of size ≤ b now exists, which the rule's side condition guarantees. This is the parametric bounded
  Löb theorem (Critch 2016) at the calculus level, with the overhead made explicit.
- *Truth* of a bounded box □_b A is the existence of a K-derivation of A of size ≤ b (a decidable, purely syntactic
  fact), so a budgeted program's play is a function of the budgets and the sources with no fixed-point selection
  [after review]. The agent must (i) state K's rules in the notes, (ii) prove soundness of K for this truth
  definition (every derivable sequent is true at the stable world of the chain whose boxes are read as K-derivability)
  or exhibit the counterexample, and (iii) implement the search with iterative deepening, so bounded boxes are decided
  exactly up to the search cap.

Worked expectation (to be checked, not assumed): for FairBot_{b_x} against FairBot_{b_y}, the proof route that works
is the joint one, A = P_{xy} ∧ P_{yx}, ⊢ □_b A → A with b = min(b_x, b_y) − c₁, so mutual cooperation needs
min(b_x, b_y) ≥ s + c₁ + c₂; the nested route (one budget inside the other) needs b_x ≥ b_y + c and b_y ≥ b_x + c and
is impossible. If this is right, play is symmetric in every budget cell and the threshold is on the smaller budget.

**Runs, in order (stop where time runs out and say so):**
1. The budget grid for pairs of bounded FairBots and of bounded `BOX1(THEM(ME))`, b ∈ {2, …, 40}: the play matrix,
   payoffs, and whether any cell is (C, D).
2. The bounded arm at n = 6: every class at a global budget b, for b at 6 values spanning K's minimal lengths; the
   lim_N chain (support, transitions, P(C,C) at N = 10³, 10⁴, 3·10⁴) and the ε = 0 lottery ((100, 4), (100, 64), 20
   runs each, with Wilson intervals); the proxy control at masking matched by opponent type and cooperation status
   [after review], not by aggregate fraction. The leak test of RESULTS "Bounded provers": does any budget make a
   self-cooperating class drift-closed at n = 6?
3. A priced version: budget b costs c·b per match (c = 0.01, 0.1) in the chain at N = 10⁴; where π sits on the budget
   axis, and whether it sits on budgets that cooperate.

## Required outputs

`src/gl_proofs.py` (GLS+Def prover, audit), `src/bounded_k.py` (K), `src/proof_length_arm.py`, `notes/proof-length.md`
(the calculi, the soundness argument, the hand-checked derivations), `runs/proof-length.md` and `.json`,
`predictions/` from the spec committed before any counted run, and the usual hand-back (draft RESULTS, REJECTED,
THEORY / DEFERRED / NOTATION edits, ≤ 5 lines on what matters, branch name from `git branch --show-current`, commits).
≤ 3 worker processes. Work in small steps; commit the prover with its audit before any length table; write notes
incrementally rather than reasoning for long stretches without writing.

## RE predictions (with falsifiers)

1. **Audit:** 0 disagreements between the box-fact tables and GLS+Def provability at n = 6 and in the n = 8 sample,
   and the trichotomy is non-empty at both levels (some pairs have neither proof at level 0). *Falsifier:* a
   disagreement that survives debugging.
2. **The proxy's ordering survives:** Spearman ≥ 0.7 over pairs with v > 0, and L(x → sibling) ≥ 1.5·L(x → x) for
   every member of P. *Falsifier:* Spearman < 0.5, or a sibling cheaper than self for some member.
3. **The cost of cooperation is linear in the DSL's frozen syntax and Löb-light:** among mutually cooperating
   establisher pairs L_C is fitted by a + b·(|x| + |y|) with b ∈ [1, 4] sequents per node and residual sd < 0.3 of
   the mean, and Λ ≤ nesting depth + 1 with FairBot–FairBot at Λ = 1 [after review: stated for this calculus and this
   syntax, not as a GL invariant]. *Falsifier:* a quadratic term whose interval excludes 0 with AIC preferring it, or
   Λ ≥ nesting depth + 3 for any pair.
4. **Thresholds, plural** [after review]: conditional cooperation disappears in steps at distinct values of L (cheap
   readers such as `BOX(THEM(^D))`-type classes survive below FairBot's threshold), below L_C(FairBot → FairBot) the
   prover family P does not cooperate at all, and above max L over P the free arm's chain numbers return within 0.05.
   In between the arm is harmless and closes nothing (same verdict as the proxy). *Falsifier:* some budget closes a
   family at n = 6, or P(C,C) at N = 10⁴ differs from the free arm by > 0.1 at a budget above max L over P.
5. **No budget ladder in K:** every cell of the FairBot budget grid is symmetric (both C or both D), the threshold is
   on min(b_x, b_y), and under a price the chain puts ≥ 0.5 of π within 2 of the minimal cooperating budget at
   c = 0.1 [after review: sol predicts asymmetry is plausible and that pricing may favour zero-budget defectors; the
   RE's reason for symmetry is the worked expectation above]. *Falsifier:* a (C, D) cell, or π mass ≥ 0.3 on budgets
   above twice the minimal cooperating one, or π on non-cooperating budgets ≥ 0.5 at c = 0.01.

The RS is invited to add predictions; the genuinely uncertain ones are 4's "closes nothing" (the proxy never charged
the Löb step; here the cheapest neighbour of a class may no longer be cheaper) and 5 (sol and the RE disagree).
