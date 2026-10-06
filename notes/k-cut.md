# K with cut and distribution (notes, 2026-10-05)

Spec `specs/2026-10-05-k-cut.md` (reviewed by gpt-6.1-sol); predictions `predictions/2026-10-05-k-cut.md`. Code: the
option `cut` in `src/bounded_k.py`, everything else in `src/k_cut.py`. Written incrementally. §1 is the deliverable
the spec puts first, and it changes what the rest of the experiment can find: distribution is **not** derivable from
cut (§1.3), so K_c needs it as a primitive rule; and a family of extension models (§1.7) shows that no sound
bounded rule of this kind can return P\*, P2, the level-2 ladder or any Gödel/Con-sentence faker while guards are
read at the reader's own budget or one above it.

## 1. K_c: definition, soundness, and what it cannot do

### 1.1 Language and model (unchanged from K, notes/proof-length.md §3 and notes/k-four.md §1.1)

Formulas: constants P_xy (x, y budgeted programs), ⊥, ⊤, ¬, ∧, ∨, →, indexed boxes □_b A. A budgeted program x_b
reads its atoms with budget b, its quoted arguments ^A are A_b, and its level-k guard is ¬□_{b+g}^k⊥ (g = 0 is K's
convention; g = 1 is the X-arm of "K with the 4-rule"). Sequents Γ ⊢ Δ with finite sets. The **standard model**
T_X of a rule set X: □_b A is true iff X derives ⊢ A (empty context) within b sequents; P_xy is true iff φ_x[y] is;
a sequent is true iff ∧Γ → ∨Δ is. φ_x[y] is a boolean combination of boxes (C ↦ ⊤, D ↦ ⊥), so once box truth is
fixed, the truth of every formula is defined outright by recursion; box truth is a fixed syntactic fact about X.
Size of a derivation = number of sequent nodes.

### 1.2 The reachable set R and the cut rule

**R.** Let Π be the finite set of budgeted programs of the catalogue closed under quotation (x_b quotes A_b; A is a
subterm of x's source, so the closure is finite). R is the set of subformulas of φ_x[y] for x, y ∈ Π, of the guards
¬□_{b+g}^k⊥ (k ≤ the catalogue's maximal level), and of their box contents, together with the constants P_xy
(x, y ∈ Π). Every constant's definition is in R (one unfolding per constant occurrence; no recursive re-unfolding is
needed because φ_x[y] mentions only constants P_uv with u, v ∈ Π). R is finite: Π is finite, the DSL syntax of each
source is finite, and the budgets occurring are those of Π and the guard offsets.

**Cut (with contexts).** From Γ ⊢ C, Δ (size s₁) and Γ, C ⊢ Δ (size s₂) infer Γ ⊢ Δ, size 1 + s₁ + s₂, C ∈ R.
K_cut = K + Cut. Cut is sound in any classical valuation in which P ↔ φ(P) holds, in particular in T_X.

### 1.3 Cut does not give distribution under a box (the spec's expected route fails)

**Theorem D0.** Let A = P[C, C] (φ = ⊤) and B = ⊥. For all budgets a, c, d the sequent
□_a A, □_c(A → B) ⊢ □_d B is not derivable in K_cut, nor in K_cut + 4m. (It is true in the standard model, because
□_c(A → ⊥) is false there.)

*Proof* (an extension model; the general form is §1.7). Let Std = {(Y, e) : K_cut ⊢ Y within e} and let B be the least
set of pairs containing Std ∪ {(A → ⊥, c)} and closed under the box-left rules of K_cut (BoxEq (i)–(iii); and 4m
for K_cut + 4m). Interpret □_e Y as true iff (Y, e) ∈ B, constants by their definitions. Every K_cut rule is sound in
this interpretation: initial sequents and BoxEq/4m because B is closed under them; propositional rules, unfolding and
Cut because the interpretation is a classical valuation in which P ↔ φ(P) holds; Nec because a derivation of ⊢ Y of
size s ≤ e puts (Y, e) in Std ⊆ B; JLöb because its instance D (size ≤ b) is a derivation of each ⊢ A_j, so
(A_j, b) ∈ Std ⊆ B, and by the induction hypothesis on the (smaller) premises each A_j is true. So every derivable
sequent is true. Now B's elements outside Std are BoxEq/4m images of (A → ⊥, c): contents A → ⊥ (A → ⊥ is not a
constant and is not the definition of one) and, under 4m, boxes □_e(A → ⊥). None is ⊥, and (⊥, d) ∉ Std by
soundness. So □_a A is true (K derives ⊢ P[C,C] in 2 sequents; take a ≥ 2, and for a < 2 put (A, a) in B too, which
changes nothing below), □_c(A → ⊥) is true, □_d ⊥ is false: the sequent is false in a model of K_cut. ∎

So no derivation of K_cut, of any size, transports two boxed hypotheses into one boxed witness: the only K rules
with a box principal on the left are initial sequents (BoxEq, and 4m when present), which relate a box to a box of
the *same* content up to one unfolding; Cut composes them but cannot open a box. The spec's "JLöb or Nec on a cut
between the two witnesses" needs the witnesses inside an empty context, which a boxed hypothesis is not. Distribution
must therefore be a **primitive rule**, and its soundness is what needs cut.

### 1.4 K_c = K + Cut + Dist

**Dist_k** (the bounded K-rule, 1 ≤ k ≤ 3). From A_1, …, A_k ⊢ B (exactly these formulas on the left, nothing else;
size s) infer Γ, □_{a_1}A_1, …, □_{a_k}A_k ⊢ □_d B, Δ, provided d ≥ s + Σ_i a_i + k. Size 1 + s.
(Nec is the case k = 0. BoxEq (i) is subsumed only above its own bound, since A ⊢ A costs ≥ 1: Dist gives
□_a A ⊢ □_{a+2} A, BoxEq gives □_a A ⊢ □_a A.)

**Dist⁺_k** (the bounded K4-rule; exploratory, used only in the long-guard arm, §1.9). The premise's left side Π may
contain, for each i, A_i, the box □_{a_i}A_i itself, or both: from Π ⊢ B infer Γ, □_{a_1}A_1, …, □_{a_k}A_k ⊢ □_d B, Δ
provided d ≥ s + Σ_{A_i ∈ Π}(a_i + 1) + Σ_{□A_i ∈ Π}(a_i + 2). It contains the 4-axiom at a cost (□_a A ⊢ □_{a+3}□_a A).

**UnfId** (an initial sequent): Γ, P ⊢ φ(P), Δ, size 1. Needed only to keep Lemma W true once Cut can put a
constant on the left of a closed derivation (§1.5); sound because P ↔ φ(P) holds in every model considered.

**K_c = K + Cut + UnfId + Dist** (k ≤ 3); **K_c4 = K + Cut + UnfId + Dist⁺** (k ≤ 3); **K_cut = K + Cut + UnfId**.
All contain K's rules unchanged, so every K derivation is a K_c and a K_c4 derivation of the same size.

**Weakening** is admissible and size-preserving in K_c and K_c4 (add the extra formulas to every sequent of the
branch that keeps them): the only rules with a fixed premise context are Nec, JLöb and Dist(⁺), whose premises are
untouched and whose conclusions carry arbitrary Γ, Δ; Cut weakens both premises.

**Lemma C (witness composition).** If ⊢ A_i has a K_c derivation of size ≤ a_i (each i) and A_1, …, A_k ⊢ B one of
size s, then ⊢ B has a K_c derivation of size ≤ s + Σ a_i + k.
*Proof.* Induct on k. Cut on A_k: left premise A_1, …, A_{k−1} ⊢ A_k, B is a weakening of the derivation of ⊢ A_k
(size ≤ a_k); right premise A_1, …, A_k ⊢ B (size s); conclusion A_1, …, A_{k−1} ⊢ B of size ≤ s + a_k + 1. Repeat.
Each cut formula A_i is the content of a box occurring in a reachable sequent, so A_i ∈ R. ∎
For K_c4: a member □_{a_i}A_i of Π is discharged by Nec on the derivation of ⊢ A_i (size ≤ a_i + 1), then a cut
(+1): total a_i + 2, as charged; □_{a_i}A_i ∈ R.

*The spec's recurrence, corrected.* For ⊢ A (size a) and ⊢ A → B (size c), Lemma C with k = 2 on the premise
A, A → B ⊢ B gives ⊢ B within a + c + s + 2, where s = size of A, A → B ⊢ B = 1 + I(A) + I(B) (→L; I(F) = size of
the identity F ⊢ F, 1 for a constant or a box). So the bound is a + c + 5 for atomic A, B, not a + c + 1; it is a + c
when the derivation of ⊢ A → B ends in →R (invert it: A ⊢ B has size c − 1, one cut). The "+ 1" holds only for that
inverted form.

### 1.5 Soundness

**Theorem S.** Every K_c-derivable sequent is true in T_{K_c}; every K_c4-derivable sequent is true in T_{K_c4}.

*Proof* (for K_c; K_c4 identical with Dist⁺). Strong induction on derivation size n; Claim(n): every derivation of
size ≤ n has a true end sequent. Box truth is not part of the induction: it is the fixed set of facts "K_c derives
⊢ A within b". The cases of K's rules are K's proof verbatim (notes/proof-length.md §3), given

**Lemma W in K_c.** If ⊢ P has a K_c derivation of size s, then ⊢ φ(P) has one of size ≤ s.
*Proof.* K's proof inspected the last rule; with Cut the root's P can be carried up as a side formula into both
premises, and a premise can acquire P on its left. Trace the root's occurrence of P upward (through every rule where it
is a side formula; the fixed-context premises of Nec, JLöb and Dist do not contain it) and replace it by φ(P)
everywhere along the trace. Where the traced P is principal: UnfR — delete the rule (size − 1); JLöb concluding P —
conclude φ(P) from the same premises; Ax Γ, P ⊢ P, Δ — becomes Γ, P ⊢ φ(P), Δ, an UnfId axiom (size 1). A Cut whose
cut formula is P itself has a left premise Γ ⊢ P, Δ that already derives the conclusion with fewer sequents; use it
and continue. No other rule has a constant as its principal right formula. Sizes never grow. ∎
- *Cut.* Both premises have size < n, so they are true by Claim(n − 1). If ∧Γ holds and ∨Δ fails, the left premise
  forces C and the right premise forces ¬C: contradiction. So the conclusion is true.
- *Dist.* If some □_{a_i}A_i is false, the conclusion is true. Otherwise each ⊢ A_i has a K_c derivation of size
  ≤ a_i; the premise derivation is a K_c derivation of A_1, …, A_k ⊢ B of size s; Lemma C gives ⊢ B within
  s + Σ a_i + k ≤ d, so □_d B is true. No induction hypothesis is used.
- *JLöb, with cut or Dist inside its premises (the Löb/cut interaction).* Let D be the instance, |D| ≤ b. A premise
  derivation may contain Cut and Dist nodes; it is still a closed derivation of its premise sequent (its root has
  exactly the context □_b S; cut and Dist do not import formulas from outside a derivation). D with its conclusion
  replaced by ⊢ A_j is a K_c derivation of ⊢ A_j of size ≤ b, so every □_b A_j is true; by Claim(n − 1) each premise
  is true; its left side is true; so each A_j, hence the conclusion, is true. A Dist node inside a premise whose
  hypothesis is □_b A_j is sound because □_b A_j is true by exactly this size argument, which uses no induction
  hypothesis; so the induction is not circular. ∎

So K_c is sound; the JLöb witness construction of notes/proof-length.md §3 is unchanged. Cut is used only in the
witnesses Lemma C builds: the soundness of Dist is the reason K_c contains Cut.

### 1.6 Finiteness, decidability, the search invariant, and the prune

- *Termination.* Every rule's premises are strictly smaller than its conclusion (size = 1 + Σ premises), so a
  derivation never contains its own end sequent and iterative deepening on size terminates; cyclic proofs are not
  admitted. Formulas in a derivation of a goal over R lie in R ∪ {boxes □_e Y : Y ∈ R, e ≤ cap} (Dist conclusions
  are right boxes of the sequent, Dist premises are contents of left boxes and the right box's content, Cut formulas
  are in R), so the set of sequents is finite and "K_c ⊢ A within b" is decidable.
- *The GL-erasure prune* (src/k_at_n8.py) stays valid **on every sequent of a derivation, not only on its end
  sequent**: each K_c rule erases to a GL+Def-sound sequent rule (Cut to cut; Dist to the K-rule "from ∧A → B infer
  □∧A → □B" with weakening; Dist⁺ to the K4-rule, GL-admissible because GL ⊢ □A → □□A; the others as in "K at
  n = 8"), so by induction on the derivation every sequent occurring in a K_c derivation erases to a GL-valid
  sequent. The search may therefore skip any sequent (including a Dist premise A_1, …, A_k ⊢ B) whose erasure is not
  GL-valid, and any closed goal whose erasure is not a GL theorem. The implementation checks Dist premises this way
  (an erased implication decided by the GL oracle).

### 1.7 Extension models: a structural certificate for every budget

Fix X ∈ {K_c, K_c + 4m, K_c4} and a program budget b. Let Std_X = {(Y, e) : X ⊢ Y within e}.

**Definition.** For a set E of formulas, B_E is the least set of pairs containing Std_X ∪ {(Y, b) : Y ∈ E} and closed
under X's box-left rules read as operations on pairs: BoxEq (i)–(iii), 4m (if present), and Dist(⁺) (if each
(A_i, a_i) ∈ B_E and X derives the premise within s, then (B, d) ∈ B_E for every d meeting the side condition). The
**extension model** I_E interprets □_e Y as (Y, e) ∈ B_E and constants by their definitions.

**Theorem E.** Every X-derivable sequent is true in I_E, for every E.
*Proof.* As in §1.3, by induction on size: B_E ⊇ Std_X gives Nec and JLöb (their witnesses are X-derivations),
closure gives BoxEq, 4m and Dist(⁺), and the rest are classical. ∎

So **a formula F false in some I_E is not X-derivable at any size**: a certificate of structural failure that covers
every budget, every cut formula and every proof length at once, which a capped search cannot.

**Lemma E1 (what E adds at budgets ≤ b + 1).** Let E be a set of contents at budget b. Every element of B_E \ Std_X is
produced by a closure derivation with at least one E-leaf; every rule application increases the budget of its output
over that E-leaf, except BoxEq (i)/(ii). Precisely, the elements of B_E \ Std_X with budget ≤ b + 1 are exactly:
(Y, e ≥ b) with Y ∈ E or Y = φ(X) for a constant X ∈ E; (Q, e ≥ b + 1) for constants Q with φ(Q) one of those
contents; and, for X ⊇ 4m only, (□_f Y, e ≥ b + 1) with f ≥ b and Y one of those contents. Dist from any input
(Y, ≥ b) outputs at d ≥ s + b + 1 ≥ b + 2; 4m (iii) and (iv) at ≥ b + 2; Dist⁺ at ≥ b + 3.
*Proof.* Case analysis on the rule's side condition (BoxEq (iii): a + 1 ≤ c; 4m (i)/(ii): c ≥ a + 1; Dist: s ≥ 1,
k ≥ 1). ∎

**Lemma E2 (no 4-rule: E-derived contents are consequences of E).** If X = K_c (no 4m, Dist not Dist⁺), every
content Y with (Y, e) ∈ B_E \ Std_X satisfies K_c ⊢ ∧E → Y, hence GL+Def ⊢ erase(∧E → Y), at every budget e.
*Proof.* BoxEq images are provably equivalent to their source; a Dist output's content follows from its premise and
the inputs' contents, each implied by ∧E or a theorem (cuts). ∎

**The certificate actually computed** (`src/k_cut.py`, `certify`). Three-valued evaluation of F in I_E with
Std_X approximated from both sides: (Y, e) is *true* if the K search found a derivation of ⊢ Y within e
(K ⊆ X), *false* if GL+Def ⊬ erase(Y) or Y is already certified structural, *unknown* otherwise; E-membership is
Lemma E1's list (exact at budgets ≤ b + 1; queries above b + 1 are refused). F is certified structural when it
evaluates to *false* under Kleene's strong three-valued logic (false in every completion, hence in I_E itself, since
I_E is one completion). Certification iterates: a content certified structural is Std-false at every budget, which
can decide boxes in further formulas. E ranges over singletons and pairs of budget-b box contents occurring in F's
unfolding closure. For the guard offsets g ∈ {0, 1}, every box occurring in an atom has budget b or b + g ≤ b + 1.

**Corollary P (P\*, P2, the ladder, the fakers).** For X ∈ {K_c, K_c + 4m} and g ∈ {0, 1}, for every b:
- P\*_b's self-play content ¬□_{b+g}⊥ → P (P = □_b(¬□_{b+g}⊥ → P) ∧ ¬□_b P) is false in I_{{P}}: □_b P is true, so P is
  false, and □_{b+g}⊥ is false (Lemma E1: no E-derived content is ⊥ at budgets ≤ b + 1), so the guard holds. Not
  derivable at any size.
- P2_b: E = {P[P2, C]} (P2 against C, i.e. the content of its own ¬□_b P[·, C] atom): □_b P[P2,C] true, the self-play
  conjunct ¬□_b P[P2,C] false, guard true. Not derivable.
- P12b, P\*1b: as P2 / P\* (their level-2 conjuncts do not help: the level-1 guard is false only if □_{b+g}⊥ is).
- PB2 at g = 0 (Lemma G of "K with the 4-rule" recovered): E = {P[D, PB2]}; the level-2 guard ¬□_b□_b⊥ needs
  (□_b ⊥, b) ∉ B_E, which holds (4m outputs at ≥ b + 1). At g = 1 with 4m: (□_{b+1}⊥, b + 1) ∈ B_E by 4m (ii) since
  φ(P[D, ·]) = ⊥: no certificate, consistent with PB2's re-arming at b\* = 11 in the X-arm of "K with the 4-rule". At
  g = 1 without 4m: certificate (consistent with "K, guard + 1: never").
- The Gödel sentence G = `not(BOX(THEM(ME)))` against a guarded reader (e.g. `BOX1(THEM(THEM))`): the reader needs
  ¬□_{b+g}⊥ → P[G, G] with P[G,G] = ¬□_b P[G,G]; E = {P[G,G]} falsifies it. The Con sentence `not(BOX(THEM(^C)))`:
  the resident's reading needs □_b P[z, C] → □_{b+g}⊥ with φ(P[z,C]) = ¬□_b⊤; E = {P[z, C]} falsifies it.
In each case the missing step is a boxed consequence at budget b + g of a hypothesis at budget b, and every sound
rule that composes witnesses pays at least one sequent per hypothesis plus one for the conclusion. **This is the
second incompleteness theorem in bounded form again (Lemma G), now for distribution: a budget-b reader cannot
conclude the inconsistency of budget b + g from a hypothesis of budget b for g ≤ 1.**

**Corollary T (tables).** If every GL-true atom content that K fails to derive at budget b is certified structural,
the K_c, K_c + 4m and K table at b coincide, without any K_c search. (Computed in §2 for n = 6 and n = 8.)

### 1.8 Hand-checked examples (tests/test_k_cut.py)

*Positive: the minimal distribution derivation.* A = P[FB_5, D], B = P[D, D] (FB = `BOX(THEM(ME))`; φ(A) = □_5 P[D, FB_5],
φ(B) = ⊥). Γ = {□_a A, □_c(A → B)}, goal Γ ⊢ □_d B. Derivation (size 4, contexts explicit):

    □_a A, □_c(A → B) ⊢ □_d B                    Dist_2, side condition d ≥ 3 + a + c + 2
      A, A → B ⊢ B                                →L
        A ⊢ A, B                                  Ax (A a constant)
        A, B ⊢ B                                  Ax (B a constant)

so d* = a + c + 5. *Negative:* at d = a + c + 4 the sequent is not derivable: A ⊢ B and A → B ⊢ B are not derivable
(I_{{φ(A)'s content}} makes A true and B false; and A → B ⊢ B is false in T_{K_c}, where A and B are both false), so
Dist_1 is impossible; Dist_2's premise A, A → B ⊢ B has no derivation of size ≤ 2 (no axiom; the only one-premise rules
are UnfL on A and UnfR on B, neither of which yields an axiom); using BoxEq images (φ(A), a) costs ≥ 1 more. Every
closure path to (B, ·) in I_{{A, A→B}} has budget ≥ a + c + 5. And in K_cut (no Dist) not at any d (Theorem D0's model).
*Witness replay.* For every Dist instance in a found derivation, the independent checker (`src/k_cut.py`, `replay`)
rebuilds the Lemma C witness — the k cuts on the closed derivations of the hypotheses' contents — checks every node's
rule and side condition from scratch, and confirms its size ≤ d.

### 1.9 What K_c can change, and the long-guard arm

By Corollaries P and T, at g ∈ {0, 1} K_c can change K's plays only where K's failure is *finite-budget* (derivable
at a larger budget): an accelerator, like 4m. Distribution can matter for Con-dependent cooperation only if the guard
is read at least two budgets above the reader (Lemma E1), and P\* needs more: inside its Löb branch it must conclude
□_{b+g}⊥ from □_b P, which by Lemma E2 is impossible without a 4-rule at any g, and with Dist⁺ costs
d ≥ s + (b + 1) + (b + 2) with s = 4 (P, □_b P ⊢ ⊥: UnfL, ∧L, ¬L, Ax), i.e. **b + g ≥ 2b + 7**. The Gödel sentences'
readers need the same: P[G,G], □_b P[G,G] ⊢ ⊥ (s = 3: UnfL, ¬L, Ax), **b + g ≥ 2b + 6**. So in every sound bounded
calculus of this family, **P\* and the Gödel-sentence fakers are restored together, by the same reflection margin**.
The exploratory long-guard arm (declared in the predictions, outside every RE verdict) reads the guard at 2b + 8
(g = b + 8) in K_c4 and measures what comes back.
