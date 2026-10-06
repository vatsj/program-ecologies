# K with the 4-rule (notes, 2026-10-05)

Spec `specs/2026-10-05-k-four.md` (reviewed by gpt-6.1-sol); predictions `predictions/2026-10-05-k-four.md`. Code: the
option `four` in `src/bounded_k.py`, everything else in `src/k_four.py`. Written incrementally. §1 is the deliverable
the spec puts first: the encoding, the cost recurrence of every rule, and the inductive soundness proof.

## 1. K+4: encoding, cost recurrence, soundness

### 1.1 Language and model (unchanged from K, notes/proof-length.md §3)

Formulas: constants P_xy (x, y budgeted programs), ⊥, ⊤, ¬, ∧, ∨, →, and indexed boxes □_b A (b ∈ ℕ). A budgeted program
x_b reads its atoms with budget b; its quoted arguments ^A are A_b; its level-k guard is ¬□_b^k⊥ (k nested □_b over ⊥,
consistency asserted at the reader's own budget). Sequents Γ ⊢ Δ, Γ and Δ finite sets.

The standard model T_R of a rule set R: **□_b A is true iff R has a derivation of ⊢ A (empty context) with at most b
sequents**; P_xy is true iff φ_x[y] is true; a sequent is true iff ∧Γ → ∨Δ is. Derivability in R is an inductively
defined syntactic set whose side conditions (budgets, sizes) are syntactic, so box truth is a fixed fact about R and
the truth of every formula is defined outright by recursion on formulas plus finitely many unfoldings along the
(well-founded) nesting of quotations: no fixed point and no selection. Changing R changes the model: K+4's boxes
mean "K+4 derives within b".

### 1.2 Proof encoding and the cost recurrence

A derivation is a finite rooted tree; each node is a sequent labelled by the rule instance that concludes it, with the
instance's premises as its children. **Size |D| = number of sequent nodes.** Weakening is admissible and
size-preserving (a derivation of Γ ⊢ Δ is one of Γ, Γ' ⊢ Δ, Δ' after adding the extra formulas to every sequent of
the branch that keeps them, which no side condition below forbids: the only rules with an empty-context condition
are Nec and JLöb, whose *premises* are fixed and whose *conclusions* carry an arbitrary context). The search's
"deletion" of an unused single-premise formula (notes/proof-length.md §1, normal form) is weakening read backwards and
costs 0. Cost recurrence, with s, s₁, s₂, s_j the sizes of the premise derivations:

| rule | conclusion | premises | size | side condition |
|---|---|---|---|---|
| Ax | Γ, P ⊢ P, Δ; Γ, □_aA ⊢ □_aA, Δ; Γ, ⊥ ⊢ Δ; Γ ⊢ ⊤, Δ | — | 1 | — |
| BoxEq (i) | Γ, □_a A ⊢ □_c A, Δ | — | 1 | a ≤ c |
| BoxEq (ii) | Γ, □_a P ⊢ □_c φ(P), Δ | — | 1 | a ≤ c |
| BoxEq (iii) | Γ, □_a φ(P) ⊢ □_c P, Δ | — | 1 | a + 1 ≤ c |
| ¬L, ¬R, ∧L, ∨R, →R, UnfL, UnfR | as in G3 / GLS+Def | one | 1 + s | — |
| ∧R, ∨L, →L | as in G3 | two | 1 + s₁ + s₂ | — |
| Nec(c) | Σ ⊢ □_c A, Δ | ⊢ A (empty context) | 1 + s | s ≤ c |
| JLöb(S, b) | Σ ⊢ A_i, Δ (or Σ ⊢ φ(A_i), Δ for a constant A_i), A_i ∈ S | □_b A_1, …, □_b A_k ⊢ A_j, one per j (no other formula) | 1 + Σ_j s_j | 1 ≤ k ≤ 3, b ≥ 1 + Σ_j s_j |
| **4 (literal)** | Γ, □_a A ⊢ □_c □_a A, Δ | — | 1 | c ≥ a + 1 |
| **4m (i)** | Γ, □_a A ⊢ □_c □_d A, Δ | — | 1 | d ≥ a, c ≥ a + 1 |
| **4m (ii)** | Γ, □_a P ⊢ □_c □_d φ(P), Δ | — | 1 | d ≥ a, c ≥ a + 1 |
| **4m (iii)** | Γ, □_a φ(P) ⊢ □_c □_d P, Δ | — | 1 | d ≥ a + 1, c ≥ a + 2 |
| **4m (iv)** | Γ, □_a A ⊢ □_c Q, Δ with φ(Q) = □_d A′ | — | 1 | (A′, d) as in (i)–(iii) for (A, a), and c ≥ (that case's bound on c) + 1 |

"Indexed Nec" is Nec(c): its index is the box's budget, and its only obligation is that the premise derivation fit in
it. JLöb's budget b is the budget of its hypotheses and may be smaller than any program's budget. The **4-rule** is
an initial sequent (size 1) with a purely syntactic side condition; **K+4** = K + 4 (literal), **K+4m** = K + 4m
(i)–(iv). 4m (i) contains the literal rule (d = a). 4m is the literal rule closed under the monotonicity that K's
BoxEq already has at top level, and under one unfolding; K cannot derive 4m from 4 because it has no rule acting
under a box (□_{a+1}□_a A ⊢ □_c □_d A with d > a needs BoxEq under a box).

### 1.3 Two lemmas

**Lemma W (unfolding never costs on the right of an empty context), for K+4 and K+4m.** If ⊢ P (P a constant) has a
derivation of size s, then ⊢ φ(P) has one of size ≤ s. *Proof.* Look at the last rule of a derivation of ⊢ P with
empty left side. It is not an initial sequent: Ax needs P or ⊥ on the left or ⊤ on the right; BoxEq and 4/4m need a box
on the left. It is not a propositional rule (P is atomic) nor Nec (its right formula is a box). So it is UnfR, whose
premise ⊢ φ(P) has size s − 1, or JLöb concluding P (so P ∈ S), which may conclude φ(P) instead from the same premises
at the same size. ∎

**Lemma N (the Nec witness).** If □_a A is true in T_R (R ⊇ K's rules), then ⊢ □_d A has an R-derivation of size
≤ a + 1 for every d ≥ a. *Proof.* Truth gives a derivation D of ⊢ A with |D| ≤ a ≤ d; Nec(d) applied to D satisfies its
side condition and has size |D| + 1 ≤ a + 1. ∎

### 1.4 Soundness theorem

**Theorem.** Every K+4m-derivable sequent (hence every K+4-derivable one) is true in T_{K+4m}; every K+4-derivable
sequent is true in T_{K+4}.

*Proof* (written for K+4m; for K+4 drop cases (ii)–(iv) of the 4-rule and read R = K+4 throughout). Strong induction
on derivation size n. Claim(n): every R-derivation of size ≤ n has a true end sequent. Box truth is *not* part of the
induction: it is the fixed set of facts "R derives ⊢ A within b". Take a derivation D of size n and its last rule.

- *Ax.* P ⊢ P, □_aA ⊢ □_aA, ⊥ ⊢, ⊢ ⊤ are true.
- *BoxEq (i):* a derivation of ≤ a sequents has ≤ c. *(ii):* if □_a P is true, Lemma W gives ⊢ φ(P) within a ≤ c.
  *(iii):* if □_a φ(P) is true, append UnfR: ⊢ P within a + 1 ≤ c.
- *Propositional rules and unfolding.* The premises have size < n, so they are true by Claim(n − 1); G3's rules
  preserve truth; UnfL/UnfR preserve truth because P ↔ φ(P) holds in T_R by the definition of P's truth.
- *Nec(c).* The premise derivation itself witnesses □_c A (size s ≤ c), so the conclusion's right formula is true.
  (No induction hypothesis needed.)
- *JLöb(S, b).* |D| = 1 + Σ s_j ≤ b. For each j, D with its conclusion replaced by ⊢ A_j is an R-derivation of
  ⊢ A_j of size |D| ≤ b (the last rule's conclusion formula may be any member of S), so every □_b A_j is true. Each
  premise has size < n, so it is true by Claim(n − 1); its left side is all true, so every A_j is true, hence the
  conclusion's A_i (or φ(A_i), equivalent in T_R) is true.
- *4 (literal), 4m (i).* If □_a A is false the sequent is true. If it is true, Lemma N with d ≥ a gives an
  R-derivation of ⊢ □_d A of size ≤ a + 1 ≤ c, so □_c □_d A is true. **This is the case the review asked for: the
  witness for the outer box is Nec applied to the very derivation that makes the inner box true, and its size bound
  a + 1 is certified by Nec's cost recurrence (1 + s with s ≤ a).** No induction hypothesis is used, so the 4-rule
  cannot create a circularity in the induction.
- *4m (ii).* If □_a P is true, Lemma W gives ⊢ φ(P) within a ≤ d; Nec(d): ⊢ □_d φ(P) within a + 1 ≤ c.
- *4m (iii).* If □_a φ(P) is true, UnfR gives ⊢ P within a + 1 ≤ d; Nec(d): ⊢ □_d P within a + 2 ≤ c.
- *4m (iv).* The case (i)–(iii) argument gives ⊢ □_d A′ within its bound β; UnfR gives ⊢ Q (φ(Q) = □_d A′) within
  β + 1 ≤ c.

So Claim(n) holds for every n. ∎

*Remarks.* (a) The 4-rule's truth is the bounded form of provable Σ₁-completeness for the derivability predicate:
"if A has a short proof, then 'A has a short proof' has a proof one sequent longer". (b) The **GL-erasure prune** of
`src/k_at_n8.py` stays valid: every 4/4m instance erases to a GL+Def theorem (□A → □□A, □P → □□φ(P),
□φ(P) → □□P, □A → □Q with φ(Q) = □A), so K+4m ⊢ A still implies GL+Def ⊢ erase(A). (c) The normal form of the search
stays exact: the 4-rule's principal formulas are boxes, never a compound non-boxed formula. (d) The checker's
"0 violations" re-evaluates every derived closed formula in the computed model; it is a regression test of the
implementation against this proof, not the proof.

### 1.5 What the rule can and cannot do on the DSL (proved before any table)

**Lemma V (the literal rule is vacuous on DSL formulas).** In any table or catalogue of budgeted DSL programs (any
assignment of budgets), no instance of the literal 4-rule occurs in any derivation the search can build. *Proof.* The
right formula □_c □_a A of an instance is a box whose content is a box. Formulas reach a sequent from the root by
subformulas, unfolding and the rules' premises; Nec and JLöb premises introduce only the content of a right box and
boxes □_b(member of S) on the *left*. So a right formula is a subformula of some unfolded definition φ_x[y] (or of
the root, itself built from definitions and guards). In a definition, a box's content is a box only inside a level-k
guard, □_b^k⊥ with k ≥ 2, where every box carries the reader's own budget b; so c = a = b (and A = □_b^{k−2}⊥). The
side condition c ≥ a + 1 fails. ∎ **Corollary:** K+4 tables equal K tables at every budget and on every cross-budget
catalogue, so the literal rule re-arms nothing; the checker and tables below confirm this as a regression.

**Lemma V′ (where 4m can act on the DSL).** A 4m instance needs a left box □_a A and a right box □_c B whose content
is a box (a guard tower) or a constant unfolding to a box (a reader that is a single box atom, e.g. FairBot), with
c ≥ a + 1. At a fixed global budget b every program box has budget b, so a must be the budget of a JLöb hypothesis,
b′ ≤ b − 1 (case (iv) with (i) needs b′ ≤ b − 2). On a cross-budget catalogue a can be a lower-budget program's box:
the guard of x_c can absorb a left box of y_a when a < c.

**Lemma G (equal-budget guards).** The GL derivation of PB2 = `and(BOX(THEM(ME)),BOXD2(THEM(^D)))` against itself
needs, inside its BOXD2 atom, the sequent □_b P[D, PB2_b] ⊢ □_b □_b ⊥ (the 4-axiom instance □⊥ → □□⊥, with
φ(P[D, ·]) = ⊥). Its left box and its guard both carry PB2's own budget b, so 4m (ii) would need c = b ≥ b + 1.
No instance of 4 or 4m closes it at a fixed global budget. A sound rule closing □_a ⊥ ⊢ □_a □_a ⊥ outright does not
follow from Lemma N (the Nec witness has size a + 1, one more than the outer budget), and the alternative, a bounded
consistency leaf Γ, □_a ⊥ ⊢ Δ, is sound by the size induction only if it is charged more than a sequents (it needs
Claim(a)), so it cannot fit inside a box of budget a. The equal-budget guard is the bounded form of the second
incompleteness theorem: a budget-b box cannot certify the consistency of budget b. This predicts that PB2 is not
re-armed by K+4m at any fixed b (the sweep decides), and that it is re-armed when the guard is read one budget up,
¬□_{b+1}^k⊥ (4m (ii) with a = b, d = c = b + 1), an exploratory variant declared in the predictions. P\*, P2 and
the Gödel sentences need more than 4: refuting □_b P from Con needs distribution of the box over a conjunction
(□A, □(A → B) ⊢ □B under a box), which K has in no form.

## 2. The frozen classifier on K's label (n = 8)

Frozen in commit 6001721 with the predictions; evaluated afterwards (`runs/k-four/classify_n8.json`). 408 eligible
pairs (25 residents, 89 invader classes), 74 K-disarmed at b = 16 (37 classes).

- **C_spec: precision 1.00 (31/31), recall 0.42 (31/74)**; class level 16/16 and 16/37. Gödel part alone: 24 TP,
  0 FP; Con part alone: 15 TP, 0 FP. C_pair (either play of the invasion): precision 1.00, recall 0.65 (48/74).
- So the instrument is a sufficient sign of K-disarming on this catalogue (no false positive among 334 surviving
  invasions) but far from necessary. The 43 misses fall in three groups:
  1. *Level cap* (8 pairs, 4 of them caught by C_pair): readers of Gödel/Con sentences against
     `BOX1(THEM(^BOX1(THEM(THEM))))`, whose defection is first provable at level 3 (□□□⊥-type plays); the frozen
     classifier stops at level 2. 264 surviving invasions share the cap. **The cap is part of the precision:** the
     post-hoc variant with the cap at 6 (declared after the frozen result, descriptive) finds roots for all 408 pairs,
     gains no true positive and adds 21 false positives (precision 0.60; C_pair 0.70).
  2. *The failure is on the resident's side* (13 more caught by C_pair, 17 in all): the invader's defection is proved
     cleanly, but the resident's cooperation with the invader needs a Gödel hypothesis (e.g. `not(BOX(THEM(THEM)))` vs
     `BOX1(THEM(THEM))`).
  3. *Con sentences without a self-play hypothesis* (22 pairs): `not(BOX(THEM(^C)))` (self-play ≡ ¬□⊥), `not(BOX(THEM(^BOX(…))))`,
     the probe readers `BOX(THEM(^not(BOX(THEM(^C)))))`. K loses them because the resident must prove
     □P[z, C] → □⊥ where P[z, C] unfolds to ¬□⊤: box congruence under a provable equivalence, i.e. distribution
     (□(A → B), □A ⊢ □B), which K has in no form. Neither trigger sees it: the hypothesis is □P[z, C], a cross-play,
     and no guard sits under a box.

**Misclassifications** (`runs/k-four/misclass_n8_K16.json`). For all 74 K-disarmed pairs the lost atoms (GL-true atoms
of z vs x, x vs z, x vs x that are K-false at b = 16) are **structural**: none is K-derivable at any budget up to
2L + 10 (L ≤ 22, so up to 54). So there is no finite-budget counterexample of the kind RE 3 named; the 43 false
negatives are structural failures without a trigger. In the other direction, 6 of the 31 true positives have a GL
derivation of the invader's play with no used trigger within twice the minimal size (e.g.
`and(BOX1(THEM(THEM)),not(BOX(THEM(THEM))))` vs `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`: minimal 7, untriggered 7 —
a tie broken towards the triggered one). The trigger is a property of one derivation, not of the play. There are no
false positives to analyse. Held-out n = 6: 3 K-disarmed pairs (all against `BOX1(THEM(THEM))`); C_spec catches
`not(BOX(THEM(ME)))` only, C_pair adds `not(BOX(THEM(THEM)))`, neither catches the Con sentence `not(BOX(THEM(^C)))`.

## 3. Results in one paragraph

The literal 4-rule is vacuous on the DSL (Lemma V; K+4 = K at n = 6, b = 4, 16, 40 and n = 8, b = 16, 54). Its
monotone closure 4m is sound and acts, but only as a **finite-budget accelerator**: K+4m differs from K at n = 8 in
864 / 482 / 150 / 57 / 14 / 0 plays at b = 8 / 12 / 16 / 24 / 32 / 54 (0 at b = 4), every change at b ≥ 12 toward the
free arm, μ²-weight ≤ 3·10⁻⁶, and the chain at b = 16 and 54 is K's to 10⁻⁴. It re-arms none of PB2, P\*, P2, P12b,
P\*1b and no Gödel sentence at any b ≤ 54 (Lemma G). Reading the guard one budget up (X-arm) lets K+4m re-arm PB2 at
b\* = 11 with the same witness costs as PrudentBot (11 for the Löb step, 6 for the Con lemma), while K with the same
guard never does; P\*, P2 and the ladder stay disarmed (they need distribution under a box, not 4); no Gödel sentence
returns. At n = 8 the X-arm changes nothing beyond K+4m (PB2 is outside L_8). On the cross-budget catalogue {4, 16}
4m changes 126 + 248 plays (higher-budget readers now prove facts about lower-budget programs, Lemma V′) and closes
nothing. The frozen classifier is a perfect-precision, low-recall instrument (1.00 / 0.42; C_pair 1.00 / 0.65), and
its precision depends on the level cap; deleting its flagged classes from the free table recovers 0.39 of the
K − free gap.
