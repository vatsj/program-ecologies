# The realizable language L_T and the calculus K_T (notes, 2026-10-06)

Spec `specs/2026-10-06-realizable-language.md` (reviewed by gpt-6.1-sol); predictions
`predictions/2026-10-06-realizable-language.md` (frozen terms, committed before this file). Code `src/lt.py`
(language, evaluator, calculus, prover, soundness checker), `src/lt_check.py` (independent evaluator and replay
checker). §1 is the gate the spec puts before any table: the rules with their cost recurrence, soundness, the
executable witness with size and runtime bounds, and the finiteness and completeness of the search. Written
incrementally.

## 1. K_T: rules, soundness, witness, search

### 1.1 The language and its two evaluations

**Terms** (de Bruijn): variables `v i`; `lam t`; `app f a`; constructors `con n` (n ∈ {C, D, T, F, TO}); `nat n`;
`pair a b`, `fst a`, `snd a`; `if c t e`; `fix t`; `quote t` (t closed); `eq a b`; formula builders
`mk k …` (k ∈ {plays, not, and, or, imp, box, bot, top}); `prove n f`; `sprove n f`; `run k x y`; and the runtime
forms `sim k t` and formula values. **Values:** lam, con, nat, pairs of values, quote, fix, formula values.
A **formula value** is a formula of F (§1.2) whose atoms are plays(⌜p⌝, ⌜q⌝, a).

**Step relation** σ → σ′ (call-by-value, left to right, substitution on closed terms; substitution never enters a
quote). The redex is found by the evaluation contexts `app(E, t)`, `app(v, E)`, `if(E, t, t)`, `pair(E, t)`,
`pair(v, E)`, `fst E`, `snd E`, `eq(E, t)`, `eq(v, E)`, `mk(…, v, E, t, …)`, `prove(E, t)`, `prove(v, E)`, the same for
`sprove` and `run`, and **sim frames**. Contractions (each one step): β `app(lam t, v) → t[0 := v]`; `app(fix t, v) →
app(t[0 := fix t], v)`; `if(T, a, b) → a`, `if(F, a, b) → b`; fst/snd of a pair (of a quote: its encoding
(tag, payload)); `eq(v, w) → T/F` (structural, quotes by encoding); `mk` of values → the formula value (or stuck on
ill-typed arguments); `sprove(n, f) → T` for n ≥ 1; `run(k, ⌜x⌝, ⌜y⌝) → sim(k, app(app(x, ⌜x⌝), ⌜y⌝))`. A sim frame
`sim(k, t)` steps as: t a value → t; else k = 0 or t stuck → TO; else t → t′ gives `sim(k − 1, t′)` (one step of the
whole state; every enclosing frame is charged because it is itself a sim whose inner term stepped). A state with no
redex that is not a value is **stuck**.

A **prove state** is a state whose next contraction is `prove(nat c, f)` with f a formula value (possibly inside sim
frames, all with fuel ≥ 1, since a frame with fuel 0 contracts to TO first). Write σ = E[prove(c, ψ)] and
σ_T = E⁻[T], σ_F = E⁻[F] for the two after-states, where E⁻ is E with every enclosing sim fuel decreased by 1. Every
other non-terminal state σ has a unique deterministic successor σ′; these are the **deterministic steps**.

**Idealized evaluation** (the semantics of the calculus): from σ, follow deterministic steps; at a prove state go to
σ_T if □_c ψ is true (§1.3) and to σ_F otherwise; no global bound. It reaches a value, gets stuck, or diverges.

**Actual evaluation** `eval_K` (the semantics of play): the same steps with a global counter of K steps; `prove`
costs one step and is answered by the host's exhaustive search (*primitive-assisted*), or costs W(ψ, c), the number
of node expansions of the frozen search (§1.6), charged to the global counter and every enclosing sim fuel; when W
exceeds the smallest remaining counter, the outermost exhausted frame times out (global: the play is ⊥, the prove is
a **timeout**; a sim: it returns TO) (*search-charged*). The play of p against q is `eval_K(app(app(p, ⌜p⌝), ⌜q⌝))`:
C, D, or ⊥ (out of steps, stuck, or another value), with ⊥ paying as D.

*Agreement.* Under primitive-assisted charging the actual evaluation is the idealized one cut at K steps, provided
the host search decides box truth exactly (§1.6). Under search-charged charging they differ in two ways, both
reported per cell: a global timeout, and a sim frame that times out because it is charged a search the idealized
semantics charges one step. The second is not a soundness question about K_T (whose atoms are about the idealized
evaluation) but a gap between what a prover certifies and what a charged simulation does; §1.6 says why the
calculus cannot charge searches inside sims (the charge would be self-referential).

### 1.2 Formulas and the standard model T

**Atoms** ⟨σ⟩⇓a, σ a non-terminal state, a ∈ {C, D}; plays(⌜p⌝, ⌜q⌝, a) := ⟨app(app(p, ⌜p⌝), ⌜q⌝)⟩⇓a. The
**reading** ρ(σ, a) is ⊤ if σ is the constructor a, ⊥ if σ is any other value or stuck, and the atom ⟨σ⟩⇓a otherwise.
**Formulas:** atoms, ⊥, ⊤, ¬, ∧, ∨, →, □_c A (c ∈ ℕ). Sequents Γ ⊢ Δ with Γ, Δ finite sets.

**Catalogue universe.** K_T is used over a catalogue Cat (a finite set of closed programs closed under the sources
their formula builders and run calls mention). Reach(Cat) is the set of states on the idealized evaluation trees
(both branches at every prove state) of app(app(p, ⌜p⌝), ⌜q⌝), p, q ∈ Cat. Atoms range over Reach(Cat). For the
milestone catalogues every tree is finite (no `fix`; sim fuels decrease), so Reach(Cat) is finite; the code computes
it and records the number of **merges** (states with two deterministic predecessors). [Amended after the run:
merges occur (at most 1 per root closure, in SF's simulations of PB and P\*, where two inner branches reach the same
state); the completeness argument of §1.7 as amended does not use the merge count.]

**Truth in T.** □_c A is true iff K_T has a derivation of ⊢ A (empty context) with at most c sequents.
⟨σ⟩⇓a is true iff the idealized evaluation of σ reaches the constructor a. Connectives classically. A sequent is
true iff ∧Γ → ∨Δ is. Derivability in K_T is an inductively defined syntactic set whose side conditions (deterministic
steps, prove-state detection, sizes, the member condition of JLöb) are all syntactic; so box truth is a fixed fact,
the idealized evaluation is a well-defined deterministic process given it, and the truth of every formula is defined
outright: no fixed point and no selection, as in K.

**Basic equivalences in T.** (E1) If σ → σ′ is a deterministic step, ⟨σ⟩⇓a ↔ ρ(σ′, a). (E2) At a prove state
σ = E[prove(c, ψ)], ⟨σ⟩⇓a ↔ (□_c ψ ∧ ρ(σ_T, a)) ∨ (¬□_c ψ ∧ ρ(σ_F, a)). Both are the definition of the idealized
evaluation read one step.

### 1.3 Rules and the cost recurrence

Size |D| = number of sequent nodes. s, s₁, s₂, s_j are premise sizes. "A ≻_k B" means the atom A = ⟨σ⟩⇓x and
B = ρ(σ′, x) with σ →^k σ′ by k ≥ 1 deterministic steps (B is k steps **downstream** of A).

| rule | conclusion | premises | size | side condition |
|---|---|---|---|---|
| Ax | Γ, A ⊢ A, Δ (A an atom or a box); Γ, ⊥ ⊢ Δ; Γ ⊢ ⊤, Δ | — | 1 | — |
| BoxEq (i) | Γ, □_a A ⊢ □_c A, Δ | — | 1 | a ≤ c |
| BoxEq (ii) | Γ, □_a A ⊢ □_c B, Δ | — | 1 | A ≻_k B, a ≤ c |
| BoxEq (iii) | Γ, □_a B ⊢ □_c A, Δ | — | 1 | A ≻_k B, a + k ≤ c |
| ¬L, ¬R, ∧L, ∨R, →R | as in G3 | one | 1 + s | — |
| ∧R, ∨L, →L | as in G3 | two | 1 + s₁ + s₂ | — |
| EvR | Γ ⊢ ⟨σ⟩⇓a, Δ | Γ ⊢ ρ(σ′, a), Δ | 1 + s | σ → σ′ deterministic |
| EvL | Γ, ⟨σ⟩⇓a ⊢ Δ | Γ, ρ(σ′, a) ⊢ Δ | 1 + s | σ → σ′ deterministic |
| PrvR | Γ ⊢ ⟨σ⟩⇓a, Δ | Γ, □_c ψ ⊢ ρ(σ_T, a), Δ and Γ ⊢ □_c ψ, ρ(σ_F, a), Δ | 1 + s₁ + s₂ | σ = E[prove(c, ψ)] |
| PrvL | Γ, ⟨σ⟩⇓a ⊢ Δ | Γ, □_c ψ, ρ(σ_T, a) ⊢ Δ and Γ, ρ(σ_F, a) ⊢ □_c ψ, Δ | 1 + s₁ + s₂ | σ = E[prove(c, ψ)] |
| Nec(c) | Σ ⊢ □_c A, Δ | ⊢ A (empty context) | 1 + s | s ≤ c |
| JLöb(S, m) | Σ ⊢ X, Δ | □_m A_1, …, □_m A_k ⊢ A_j, one per j (nothing else on the left) | 1 + Σ_j s_j | 1 ≤ k ≤ 3; m ≥ 1 + Σ_j s_j; X = A_i or A_i ≻_k X for some A_i ∈ S |

These are K's rules (notes/proof-length.md §3) with the definitional unfolding P ↦ φ(P) replaced by the evaluation
rules: EvR/EvL are the unfolding of a deterministic step, PrvR/PrvL are the unfolding of a prove step into its
**box obligation** (the cooperative branch under the hypothesis □_c ψ, the other branch with □_c ψ owed on the
right, discharged by Nec, by BoxEq from a JLöb hypothesis, or left undischarged when the branch is closed
otherwise), and BoxEq (ii)/(iii) are K's BoxEq (ii)/(iii) iterated along a deterministic chain. A computation of s
deterministic steps costs s sequents. There is no cut, no GLR context, and no rule that refutes a box: the
negative branch of a prove call is never closed by "the search failed"; the spec's "discharged by the refuted
search" is not a rule of K_T, because a refutation leaf at budget c is sound by the size induction only if charged
more than c sequents (the argument of Lemma G in notes/k-four.md), which would put it outside every box that could
use it. A program's not-found branch is entered in the *evaluation*, where the box is false in T; the calculus can
reason about it only through the Con antecedent, as in K (§1.5).

The **JLöb-disabled control** K_T⁻ is K_T without JLöb. Its standard model is T⁻ (boxes mean K_T⁻-derivability).

### 1.4 Soundness

**Lemma W_T (downstream readings never cost more).** If ⊢ ⟨σ⟩⇓x has a K_T derivation of size s and σ → σ′ is a
deterministic step, then ⊢ ρ(σ′, x) has one of size ≤ s. Hence the same for σ →^k σ′.
*Proof.* Look at the last rule of a derivation of ⊢ ⟨σ⟩⇓x with empty left side. It is not Ax (no left formula; the
right formula is not ⊤), not BoxEq or Nec (their right principal formula is a box), not a propositional rule (an
atom), not PrvR (σ has a deterministic step, so it is not a prove state). So it is EvR, whose premise ⊢ ρ(σ′, x)
has size s − 1, or JLöb concluding ⟨σ⟩⇓x, where ⟨σ⟩⇓x is a member A_i or downstream of one; then ρ(σ′, x) is also
downstream of A_i and the same instance (same premises, same size) may conclude it. ∎

**Theorem S (soundness).** Every K_T-derivable sequent is true in T. Every K_T⁻-derivable sequent is true in T⁻.

*Proof.* Strong induction on derivation size n. Claim(n): every derivation of size ≤ n has a true end sequent. Box
truth is not part of the induction: it is the fixed set of facts "K_T derives ⊢ A within c". Let D have size n and
look at its last rule; premises have size < n and are true by Claim(n − 1) where used.
- *Ax.* True sequents.
- *BoxEq (i):* a derivation within a ≤ c is one within c. *(ii):* if □_a A is true, Lemma W_T gives ⊢ B within
  a ≤ c. *(iii):* if □_a B is true, append k EvR steps (each premise is the reading of the next state, which is
  exactly the next node): ⊢ A within a + k ≤ c.
- *Propositional rules:* G3's rules preserve truth in any classical valuation.
- *EvR, EvL:* the principal atom and the premise's reading are equivalent in T by (E1).
- *PrvR:* suppose Γ true and Δ false. If □_c ψ is true, premise 1 gives ρ(σ_T, a); if false, premise 2 gives
  ρ(σ_F, a). Either way (E2) gives ⟨σ⟩⇓a. *PrvL:* suppose Γ and ⟨σ⟩⇓a true and Δ false. By (E2), either □_c ψ and
  ρ(σ_T, a) are true, contradicting premise 1, or □_c ψ is false and ρ(σ_F, a) true, contradicting premise 2.
- *Nec(c):* the premise derivation itself witnesses □_c A (size s ≤ c); no induction hypothesis.
- *JLöb(S, m).* |D| = 1 + Σ_j s_j ≤ m. For each j, D with its conclusion replaced by ⊢ A_j is a K_T derivation of
  ⊢ A_j (the rule may conclude any member) of size |D| ≤ m, so every □_m A_j is true. Each premise has size < n, so
  it is true; its left side is true, so every A_j is true; the conclusion X is A_i or downstream of A_i, true by (E1)
  iterated. ∎

For K_T⁻ drop the JLöb case; the BoxEq (ii) case uses Lemma W_T, whose JLöb case is vacuous.

**What soundness is about.** Theorem S says a found box is true of the *idealized* evaluation. Under
primitive-assisted charging and K above the play's step count, the actual play is the idealized one, so a sound
reader is never exploited. Under search-charged charging an actual play can be ⊥ (global timeout) or can differ by a
sim timeout; these are counted separately in every table, never as soundness violations, and never hidden.

### 1.5 What K_T can and cannot derive (the transfer of K's facts)

- **Löb for copies.** For FairBot_b (§2 hand derivation) the derivation is K's: a JLöb over the root atom (or its
  prove state), with the box obligation closed by BoxEq from the hypothesis. The cost is K's plus the deterministic
  steps to the prove state and from the cooperative branch to its value.
- **Distinct sources.** As in K, a joint JLöb over the two prove-state atoms, closed by BoxEq (iii), whose side
  condition charges the steps from each initial atom to its prove state.
- **No refutation of boxes.** No rule has ¬□ as a consequence except through ¬R from a left box, and a left box
  closes only by Ax/BoxEq against a right box. So K_T never derives ¬□_c A; a reader can use a not-found branch only
  under a Con antecedent ¬□_c⊥, where BoxEq (ii) with a downstream reading ⊥ closes □_c A ⊢ □_c ⊥ when A's evaluation
  reaches a value other than its target constructor without a prove call (PrudentBot's D-probe). This is K's
  mechanism with "φ(P) = ⊥" replaced by "the deterministic chain of A ends in the wrong value".
- **Gödel sentence G_b.** G's cooperation against a reader y is ⟨…⟩⇓C ↔ ¬□_b plays(y, G, C), which needs ¬□ on the
  right: underivable. So no reader proves G's cooperation, every reader's search refutes (or times out), and G
  cooperates with every reader that defects on refutation: suckered, not disarmed (sol's correction).
- **P\*_b.** Self-cooperation needs ⊢ ¬□_b⊥ → plays(P\*, P\*, C), whose truth requires ¬□_b plays(P\*, P\*, C): the
  same obstruction; and as in notes/k-cut.md Corollary P, no witness-composing rule would close it at the reader's
  own budget. So P\* never self-cooperates in K_T (bounded Gödel II, transferred).

### 1.6 The executable witness and the runtime bound (search-charged)

**The search** (frozen in the predictions). `minsize(Γ ⊢ Δ, cap)` returns the minimal size of a derivation if it is
≤ cap, else "> cap". It is a memoized recursion over **all** rule instances whose conclusion is the sequent (no
normal-form prune): axioms (size 1); each G3, EvR/EvL and PrvR/PrvL instance on each principal formula, with
premises called at the remaining cap (two premises: the first at cap − 2, the second at cap − 1 − s₁; exact because
premises are independent); Nec on each right box □_c A via minsize(⊢ A, min(c, cap − 1)); JLöb leaves on each
right formula X (§1.7 for the candidate sets), each tried at hypothesis budgets m from 2 upward with the jump
m := 1 + Σ s_j(m) (premise sizes are non-decreasing in m because a larger m is a weaker hypothesis, so the first
feasible m gives the minimal instance). The memo stores, per sequent, an exact value or a lower bound; a call is an
**expansion** when the memo cannot answer it. *Lower-bound rule* (fixed during implementation, before any table;
it does not change any outcome or minimal size, only W): a failed expansion at cap stores max(cap + 1, ℓ), where ℓ
is the minimum over the sequent's rule instances of the instance's lower bound (1 + the premises' bounds; Nec is
impossible, ℓ = ∞, when its premise's bound exceeds the box budget; a JLöb (S, m) instance's bound at the m reached is
a bound for every larger m, since premise sizes are non-decreasing in m). Every stored bound is a valid lower bound, so
the search stays exact; a sequent with bound ∞ is never expanded again. The prover runs **iterative deepening** n = 1, 2, …, b on ⊢ ψ with one
fresh memo per prove call, stops at the first n with a derivation (**found**, size n certified minimal) or after
n = b (**refuted**), and returns W(ψ, b) = the number of expansions. W is a deterministic function of (ψ, b) and the
catalogue.

**Witness.** For every true □_b ψ (a derivation of ⊢ ψ within b exists), the search returns a derivation of size
exactly the minimum n\* ≤ b, reconstructed from the memo's argmin instances (each node's rule, principal formula,
premises and, for JLöb, (S, m)); `src/lt_check.py` replays it from scratch (§3).

**Runtime bound.** Let U_b(ψ) be the finite universe of §1.7 (every formula that can occur in a derivation of ⊢ ψ of
size ≤ b explored by the search), u = |U_b(ψ)|. A sequent is a pair of subsets of U_b(ψ), so there are at most 4^u.
Each sequent is expanded at most once per cap value it is called with (after an expansion at cap the memo holds an
exact value or the lower bound cap + 1, the memo is shared by the passes of one prove call, and caps never exceed
b), so the whole prove call is bounded by **W(ψ, b) ≤ b·4^u expansions**; each expansion enumerates at most
r(u) = 2u + u·(1 + b·(1 + u + u²)) rule instances (one per principal formula, plus at most b hypothesis budgets per
JLöb candidate set of size ≤ 3). The bound is explicit and astronomically loose; what the experiment uses is the
measured W. Hence: **a program whose box □_b ψ is true finds it under search-charged charging iff its remaining
global budget (and every enclosing sim fuel) is at least W(ψ, b) when the prove call is reached**; every table
reports W and the smallest tested K at which each outcome stabilizes, and "a found box the search-charged arm
cannot find at any tested K" means W(ψ, b) > 10⁶ minus the play's other steps.

**Why the calculus does not charge searches inside sims.** If σ_T and σ_F inside a sim decreased the fuel by
W(ψ, c) instead of 1, the step relation would depend on W, which is the work of a search over derivations whose
evaluation rules depend on the step relation, including (for SF against FairBot) the very prove call being charged.
The definition would be circular. The calculus therefore describes the primitive-assisted idealization, and the
search-charged arm is the realizability test of that idealization.

### 1.7 Finiteness of the candidate set and completeness of the search

**The universe.** For a root ψ and cap b, U_b(ψ) is the least set containing ψ and closed under: subformulas; the
reading ρ(σ′, a) of each deterministic step of an atom; at a prove state, □_c ψ′, ρ(σ_T, a) and ρ(σ_F, a); the
content of each box; the **member candidates** Mem(ψ) = the box contents in this closure, every atom deterministically
upstream or downstream of an atom box content within Reach(Cat), and every atom in the closure; and the hypothesis
boxes □_m Y for Y ∈ Mem(ψ) and 1 ≤ m ≤ b. Over a catalogue with finite evaluation trees, Reach(Cat) is finite, so the
closure is finite, Mem is finite, and U_b(ψ) is finite (at most |closure| + b·|Mem| formulas). Box budgets in U_b(ψ)
are those written by the programs (≤ the catalogue's maximum) or hypothesis budgets ≤ b; nesting depth is that of the
formula values the programs build, plus one for a hypothesis box. This is the spec's finiteness: a finite atom set,
budgets ≤ b, bounded nesting, JLöb sets of size ≤ 3 over the box contents (and their chains). The derivations of size
≤ b over U_b(ψ) are finitely many.

**Every derivation of size ≤ b lives in U_b(ψ) up to unused members.** Induct on the derivation from the root: each
rule's premises contain only formulas of its conclusion, subformulas, deterministic or prove-branch readings, the
box □_c ψ′ of a prove state, a right box's content (Nec), or a JLöb instance's members and hypothesis boxes. The
only formulas not forced into the closure are JLöb members. A member A_j whose hypothesis □_m A_j is never principal
in the other premises' derivations can be deleted from S with its premise: the remaining premises are still
derivations (they did not use it), the instance shrinks, and m may stay (the side condition only gets easier), so
size does not grow. Iterating, keep the least set S_used containing the concluded member A_i and every member whose
hypothesis is used in a premise of S_used. A used hypothesis □_m Y is principal only in Ax or BoxEq against a right
box □_c B of that derivation, so Y = B (Ax, BoxEq (i)) or Y and B are atoms on one deterministic chain (BoxEq (ii),
(iii)). Right boxes of a premise derivation are boxes of the closure of its right formula (prove obligations and
subformulas) or Nec conclusions over them, so by induction on size every used member is a box content of the closure
or on a deterministic chain through one, i.e. in Mem(ψ) or upstream of a member of Mem(ψ).
**Lemma U (upstream members outside the closure)** [amended after the run; replaces an argument that assumed 0
merges]. The root closure is closed downstream (under deterministic and prove-branch successors), and every right
box of a derivation of ⊢ ψ has its content in it: right boxes come from the root's subformulas, from prove
obligations of closure states, from Nec over closure contents, and from the premise derivations of JLöb members,
whose prove obligations lie downstream of the member and hence, once the member's chain enters the closure, inside
it (a deterministic segment carries no box). Let Y be a member (or the concluded member) outside the closure, Y
upstream of a closure state, and let X′ be the first closure state on Y's chain. A right box □_c B that □_m Y closes
has B in the closure, so B is downstream of Y and the BoxEq used is (ii), with side condition m ≤ c and no distance
charge. Replace Y by X′ in S: the premise for X′ is at most the premise for Y (that premise must travel from Y to X′
by EvR steps, or end in a nested JLöb leaf on the segment, which may conclude X′ instead, by induction on size), so the
instance and m do not grow; every use of □_m Y becomes a use of □_m′ X′ by BoxEq (ii) with m′ ≤ m ≤ c; and the
conclusion, downstream of Y, is downstream of X′ or of a state between, still derivable at the same size. So
**if ⊢ ψ has a K_T derivation of size ≤ b, it has one of size ≤ b all of whose formulas lie in U_b(ψ)**, with
concluded members drawn from the closure's own upstream map, merges or not.

**Completeness of the search.** `minsize` enumerates every rule instance over U_b(ψ) with every premise-size split
and every JLöb (S, m) with S ⊆ Mem(ψ), |S| ≤ 3, containing a member whose downstream reduct (or itself) is the right
formula. By the previous paragraph, if a derivation of size ≤ n exists, one over U_b(ψ) exists, and the
recursion's value is ≤ n by induction on its size (each node's instance is enumerated, with each premise's value at
most the premise's size). Conversely every value returned is witnessed by a derivation (the argmin instances). So
iterative deepening returns found at the minimal n, and **"refuted" at b is a certified negative**: no K_T
derivation of ⊢ ψ of size ≤ b exists. Minimality is reported only from completed passes.

*Implementation note.* For a JLöb leaf on X the concluded member A_i ranges over X and its upstream states in the
root closure (all deterministic predecessors, so merges are covered), and the extras over Mem(A_i) = the atoms and box
contents of closure(A_i) plus A_i's upstream states, |E| ≤ 2 (`Search.members`). Two empirical checks that the
restriction is not binding: the brute-force prover of `src/lt_check.py` (members = every atom and box content of the
root closure, no lower bounds) at b ≤ 8, and the main prover with Mem = the whole root closure at b ∈ {16, 25, 32}.

### 1.8 The hand-checked exhaustive space at small b: FairBot against FairBot

FB_b = `λme. λthem. if prove_b(plays(them, me, C)) then C else D`, q = ⌜FB_b⌝, A = plays(q, q, C).
Deterministic chain: A₀ = ⟨app(app(FB, q), q)⟩⇓C → (β) A₁ = ⟨app(λ. if prove_b(PL(v0, q, C)) …, q)⟩⇓C → (β)
A₂ = ⟨if(prove(b, PL(q, q, C)), C, D)⟩⇓C → (mk) A₃ = ⟨if(prove(b, A), C, D)⟩⇓C, a prove state with ψ = A.
After-states: if(T, C, D) → C (reading ⊤), if(F, C, D) → D (reading ⊥ for C). Nothing in Reach(Cat) steps into A₀
(an application of a program to two quotes is never a contractum in this catalogue: checked, 0 merges).

**Claim: the minimal K_T derivation of ⊢ A has size 8 at every b ≥ 8, and none of size ≤ 7 exists at any b.**

*Enumeration.* A derivation of ⊢ A₀ (empty left) begins with a run of EvR steps through A₁, A₂, A₃ (the only other
rule for an atom with empty left is a JLöb leaf; Ax needs a left formula; BoxEq, Nec, G3 do not apply) and must
then either close a state A_k by a JLöb leaf or apply PrvR at A₃. PrvR at A₃ has premises
P₁ = Γ, □_b A ⊢ ⟨if(T, C, D)⟩⇓C, minimal size 2 (EvR, then ⊢ ⊤), and P₂ = Γ ⊢ □_b A, ⟨if(F, C, D)⟩⇓C. In P₂ the atom
can only step to ⊥, which no rule removes from the right (a JLöb leaf concluding it would need a premise deriving
⊥ from boxes alone, and a left box closes only against a right box), so P₂ needs ⊢ □_b A from Γ: by Nec (which
contains a derivation of ⊢ A strictly inside), by a JLöb leaf concluding □_b A (its premise for the member □_b A has
no axiom unless A or a chain atom of A is also a member: □_m □_b A ⊢ □_b A fails BoxEq, the contents □_b A and A
being different and not on one chain), or by Ax/BoxEq from a left hypothesis □_m Y in Γ, which exists only above a
JLöb. So a derivation without a JLöb instance having a chain member A_i (i ≤ 3) contains a derivation of ⊢ A
strictly inside itself, impossible for a finite tree; members off the chain are unused and deleted (§1.7).
*Cost.* Claim: every JLöb instance with a chain member A_i has size ≥ 8 − i. Its premise □_m S ⊢ A_i must go from
A_i to A₃ by EvR steps or end earlier in a nested JLöb concluding some A_k (k ≥ i) from a chain member A_{i′}
(i′ ≤ k), of size ≥ 8 − i′ by induction, hence premise ≥ (k − i) + 8 − i′ ≥ 8 − i; on the EvR route it pays
3 − i steps, PrvR (1), P₁ (2) and P₂ (≥ 1: Ax/BoxEq from a hypothesis), so premise ≥ 7 − i and instance ≥ 8 − i.
Then either the root's chain ends in a JLöb leaf concluding A_k (size ≥ k + 8 − i ≥ 8, since k ≥ i: a JLöb concludes
a member or a *downstream* reduct), or the root applies PrvR at A₃ and the instance sits inside P₂ (size
≥ 3 + 1 + 2 + 5 = 11). Extra members add premises of size ≥ 1. Hence size ≥ 8 everywhere, and **at every b ≤ 7 the
search refutes**.
*Attained at 8.* S = {A₀}, m = 8: premise □₈A ⊢ A: EvR, EvR, EvR, PrvR [P₁: □₈A, □_bA ⊢ ⟨if(T,C,D)⟩⇓C: EvR, ⊢⊤ (2);
P₂: □₈A ⊢ □_bA, ⟨if(F,C,D)⟩⇓C: BoxEq (i), 8 ≤ b (1)] = 3 + 1 + 2 + 1 = 7; instance 8 ≤ m. Also S = {A₃}, m = 5: premise
PrvR [P₁ (2); P₂: □₅A₃ ⊢ □_bA by BoxEq (iii), A₀ ≻₃ A₃, 5 + 3 ≤ b (1)] = 4, instance 5, and ⊢ A = EvR³ + JLöb = 8.
Both need b ≥ 8. **b\*(FB) = 8, Λ = 1.**

**Distinct budgets FB_x, FB_y.** A_xy = plays(FB_x, FB_y, C) has its prove state A₃^xy with ψ = A_yx (budget x). A
joint JLöb with S = {A₃^xy, A₃^yx}, m = 9: each premise is PrvR + P₁ (2) + P₂ (BoxEq (iii): □₉A₃^yx ⊢ □_x A_yx needs
9 + 3 ≤ x) = 4; instance 9; ⊢ A_yx = 3 + 9 = 12 ≤ x and ⊢ A_xy = 12 ≤ y. With S over the initial atoms the instance
is 15 and needs m = 15 ≤ min(x, y). A lower bound as above (each premise ≥ 4 + upstream distance, both members
needed because each box obligation names the other atom) gives **cooperation iff min(x, y) ≥ 12**; copies are
cheaper (8) because S is a singleton.

The search's own visit of this space at b = 2…7 (every sequent it expands, with its value) is listed in §2 and was
checked against this enumeration line by line.

## 2. The search's own visit of the FairBot space, checked by hand

Names: A0 = plays(FB_b, FB_b, C), A1, A2 its deterministic successors, A3 the prove state, AT/AF the after-states
⟨if(T, C, D)⟩⇓C / ⟨if(F, C, D)⟩⇓C, T/F the readings ⊤/⊥. The root closure has these 9 formulas plus □_b A0, with 0
merges; Mem(A0) = {A0, A1, A2, A3, AT, AF}.

**b = 4** (refuted, W = 55 expansions, 34 sequents, 3 JLöb entries). The complete memo at the end of the search, every
entry a lower bound (no sequent is derivable within its cap):

```
>= 5   |- A0            >= 4   |- A1            >= 3   |- A2            >= 2   |- A3
>= 4   [2]A0 |- A0      >= 3   [2]A0 |- A1      >= 2   [2]A0 |- A2
>= 3   [2]A1 |- A1      >= 2   [2]A1 |- A2      >= 2   [2]A2 |- A2
>= 3   [3]A0, [3]Y |- A0   and   >= 2  [3]A0, [3]Y |- A1      for Y in {A1, A2, A3, AF, AT}
>= 2   [3]A1, [3]Y |- A1     for Y in {A2, A3, AF, AT}
>= 2   [4]A0, [4]Y, [4]Z |- A0   for the ten pairs {Y, Z} of {A1, A2, A3, AF, AT}
J(A0) >= 5    J(A1) >= 4    J(A2) >= 3
```

*Hand check.* By §1.8 the true minima are ⊢ A0 = 8, ⊢ A_k = 8 − k (k ≤ 3), and a JLöb premise □_m S ⊢ A_i has size
≥ 7 − i (and needs m + 3 − (position of the hypothesis on the chain) ≤ b to close P₂ by BoxEq, otherwise more). Every
stored bound is at most the corresponding true minimum (e.g. [2]A0 ⊢ A0: true minimum 7 at b = 4, since □_2 A0 ⊢ □_4 A0
closes P₂; stored ≥ 4), so the memo contradicts nothing, and the root's bound 5 > 4 is the certified refutation. The
pattern of the visit is the hand enumeration: EvR down the chain from A0, JLöb candidates at each of A0, A1, A2
(A3's J is never reached at cap ≤ 4, because a JLöb concluding A3 below A0 costs ≥ 3 + 2), singletons, pairs and
triples drawn from Mem, with hypothesis budget m = 1 + |S| (the smallest admissible), each failing inside its cap.
The sequents [m]S ⊢ A_i with S ∌ A3 never reach the prove state within the cap; none with AT or AF as an extra member
can use it (no right box has content AT or AF, and they are downstream of the prove state only through a branch, not
a deterministic step).

**b = 5, 6, 7** (refuted): W = 125, 229, 359 expansions; 66, 100, 126 sequents; again only lower bounds, root bound
b + 1. **b = 8** (found, size 8, W = 378): the exact entries are

```
= 8   |- A0        = 7   |- A1        = 6   |- A2        = 5   |- A3        J(A3) = 5
= 4   [5]A3 |- A3          = 1   [5]A3 |- AF, [8]A0     (BoxEq (iii): A0 >_3 A3, 5 + 3 <= 8)
= 2   [5]A3, [8]A0 |- AT   = 1   [5]A3, [8]A0 |- T
= 4   [2]A3 |- A3          (the m = 2 attempt: premise 4 > 2, so the instance jumps to m = 5)
```

which is the second derivation of §1.8 (S = {A3}, m = 5, ⊢ A0 = EvR³ + JLöb), line for line. The brute-force prover of
`src/lt_check.py` (no lower bounds, members = the whole closure) returns the same minimum 8 and refutes at every b ≤ 7.
