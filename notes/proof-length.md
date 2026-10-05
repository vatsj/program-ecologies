# Proof length: GLS+Def and the bounded calculus K (notes, 2026-10-05)

Spec `specs/2026-10-05-proof-length.md`; predictions `predictions/2026-10-05-proof-length.md`. Written incrementally.

## 1. GLS+Def

**Language.** Formulas over propositional constants P_{xy} (x, y programs: "x plays C against y"), ⊥, ⊤, ¬, ∧, ∨, →, □.
Sequents Γ ⊢ Δ with Γ, Δ finite *sets*.

**Definitions (frozen syntax).** For every program x and opponent y, φ_x[y] is x's source as written, with
C ↦ ⊤, D ↦ ⊥, not/and/or ↦ ¬/∧/∨ and the atoms
- BOX(THEM(ME)) ↦ □P_{yx}, BOX(THEM(THEM)) ↦ □P_{yy}, BOX(THEM(^A)) ↦ □P_{yA};
- BOXD(App) ↦ □¬P_{App};
- BOXk(App) ↦ □(¬□^k⊥ → P_{App}), BOXDk(App) ↦ □(¬□^k⊥ → ¬P_{App}) (k ≥ 1; □^k⊥ = k nested boxes over ⊥).

¬□^k⊥ is the GL rendering of Con(PA + Con^{k−1}): on the linear chain □^k⊥ holds exactly at worlds 0..k−1, so
□(¬□^k⊥ → s) at world n says s holds at every world m with k ≤ m < n, which is the evaluator's level-k box.

**Rules** (G3-style; size = number of sequents in the derivation tree).
- Initial sequents: Γ, A ⊢ A, Δ with A a constant P_{xy} or a boxed formula □B; Γ, ⊥ ⊢ Δ; Γ ⊢ ⊤, Δ.
- ¬L: Γ ⊢ A, Δ / Γ, ¬A ⊢ Δ.  ¬R: Γ, A ⊢ Δ / Γ ⊢ ¬A, Δ.
- ∧L: Γ, A, B ⊢ Δ / Γ, A∧B ⊢ Δ.  ∧R: Γ ⊢ A, Δ and Γ ⊢ B, Δ / Γ ⊢ A∧B, Δ.
- ∨L: Γ, A ⊢ Δ and Γ, B ⊢ Δ / Γ, A∨B ⊢ Δ.  ∨R: Γ ⊢ A, B, Δ / Γ ⊢ A∨B, Δ.
- →L: Γ ⊢ A, Δ and Γ, B ⊢ Δ / Γ, A→B ⊢ Δ.  →R: Γ, A ⊢ B, Δ / Γ ⊢ A→B, Δ.
- UnfL: Γ, φ_x[y] ⊢ Δ / Γ, P_{xy} ⊢ Δ.  UnfR: Γ ⊢ φ_x[y], Δ / Γ ⊢ P_{xy}, Δ.
- GLR (Löb): □Γ, Γ, □A ⊢ A / Σ, □Γ ⊢ □A, Δ.

(Premises contain the remaining context; the principal formula is removed. Sets absorb contraction; weakening is
admissible and size-preserving, so the search always takes □Γ = every boxed formula on the left.)

**Theorems and the trichotomy.** hc[0,x,y] ⇔ ⊢ P_{xy}; hd[0,x,y] ⇔ P_{xy} ⊢ ; hc[1,x,y] ⇔ ⊢ ¬□⊥ → P_{xy};
hd[1,x,y] ⇔ ⊢ ¬□⊥ → ¬P_{xy}.

**Why provability matches the chain (argument; the audit tests it).** *Soundness:* every rule is sound on any finite
transitive irreflexive Kripke frame on which the definitions hold at every world; the evaluator's linear chain with
P_{xy} true at world n iff val_n[x, y] = C is such a model (val_n is computed from box facts over worlds m < n, which
is the definition read at world n). So ⊢ P_{xy} implies P_{xy} at every world, i.e. hc[0, x, y]. *Completeness:* the
backward search is terminating (formulas lie in the finite unfolding/subformula closure; along a branch GLR only
fires on □A not already on the left, otherwise the sequent closes), and a failed search yields a finite irreflexive
transitive tree countermodel in the usual way, with the unfolding rules making each definition true at each node
for the constants that occur. By de Jongh–Sambin every P_{xy} is equivalent in GL+Def to a letterless sentence, and
letterless sentences take the same value at all nodes of the same depth in any GL model; so a countermodel node of
depth d gives val_d[x, y] = D on the chain, contradicting hc[0, x, y]. The same argument with the ¬□^k⊥ guard gives
the level-k tables. (Minimal sizes depend on the calculus; provability does not.)

**Search.** Exact minima: the backward-reachable AND-OR graph of the roots, restricted to *provable* sequents (a
minimal derivation never contains an unprovable sequent, so the restriction is exact), and Knuth's generalized
Dijkstra on lexicographic (size, Λ). Provability of a sequent is decided by the standard terminating procedure
(invertible rules eagerly in a fixed order, then an OR over GLR on right boxes not already on the left); the
procedure is cross-checked against the unrestricted all-orders graph wherever that graph is small enough.

**Normal form (exact).** Call ¬A (either side), A∧B on the left, A∨B on the right and A→B on the right
*single-premise* formulas. Claim: for any sequent S with a single-premise formula f (take the canonical one, smallest
id), min(S) = min( min(S − f), 1 + min(S after decomposing f) ), and the same holds for (size, Λ) lexicographically.
*Proof.* ≤: both are valid derivations of S (weakening is size-preserving, so a derivation of S − f is one of S).
≥: take a minimal derivation of S. (i) If f's occurrence (or a descendant of it, not crossing a GLR, which drops
unboxed formulas) is decomposed somewhere, permute that decomposition to the root: the root gains one sequent, every
branch that decomposed it loses one, and branches that did not carry the products as unused context (weakening).
Size does not grow and Λ is unchanged. (ii) If it is never decomposed, f is unused: a compound non-boxed formula is
never principal in an initial sequent and GLR drops it, so deleting f everywhere leaves a derivation of S − f of the
same size and Λ. ∎ So the search applies "decompose f or delete f" (deletion costs 0 and is not a sequent of the
derivation) before any other rule, which removes the order freedom among single-premise rules. Two-premise rules,
unfolding (P can close an initial sequent unfolded or not) and GLR keep every choice. The normal-form graph is checked
against the all-orders graph on every n = 6 pair and on the n = 8 pairs where the latter fits.

## 2. Hand-checked derivations (GLS+Def)

Notation: F = ⊥, T = ⊤, [] = □. Every derivation below is the one the prover returns (`src/gl_proofs.py`,
`Graph.render`), checked by hand line by line; sizes are certified minima.

**ALLC against anything** (y arbitrary). φ_C = ⊤.
```
 |- P[C,y]        [UnfR]
   |- T           [Ax]
```
L_C = 2, Λ = 0. L_D = ∞ (P[C,y] ⊢ unfolds to T ⊢, which has no rule). Hand check: the only rule applicable to ⊢ P is
UnfR; ⊢ ⊤ is initial. Minimal.

**D against anything.** φ_D = ⊥. L_D: P[D,y] ⊢ ; UnfL; ⊥ ⊢ initial: 2, Λ = 0. L_C = ∞.

**FairBot against FairBot** (FB = BOX(THEM(ME))).
```
 |- P[FB,FB]                 [UnfR]
   |- []P[FB,FB]             [GLR]
    []P[FB,FB] |- P[FB,FB]   [UnfR]
      []P[FB,FB] |- []P[FB,FB]   [Ax]
```
L_C = 4, Λ = 1. Hand check: each line has exactly one applicable rule except the last, which is initial (a boxed
formula on both sides). The Löb step is the GLR: the diagonal □P on the left closes the leaf. Minimal.

## 3. The bounded calculus K (Part B)

**Language.** As GLS+Def, but every box carries a budget: □_b A, b ∈ ℕ. A budgeted program x_b reads its atoms with
budget b: BOX(App) ↦ □_b P_App, BOXD(App) ↦ □_b ¬P_App, BOXk(App) ↦ □_b(¬□_b^k⊥ → P_App) (□_b^k⊥ = k nested
□_b over ⊥; consistency is asserted at the reader's own budget), BOXDk likewise with ¬P. A quoted argument ^A of
x_b is A_b.

**Truth (the standard model T).** □_b A is true iff K has a derivation of ⊢ A (empty context) with at most b
sequents. P_{xy} is true iff φ_x[y] is true. Box truth is a fixed syntactic fact about K, so P's truth is defined
outright (no fixed point, no selection): a budgeted program's play is a function of the budgets and the sources.
A sequent Γ ⊢ Δ is true iff (∧Γ) → (∨Δ) is true in T.

**Rules** (size = number of sequents).
- G3 propositional rules and UnfL/UnfR exactly as in GLS+Def; initial sequents Γ, P ⊢ P, Δ; Γ, ⊥ ⊢ Δ; Γ ⊢ ⊤, Δ.
- *BoxEq* (initial): Γ, □_a A ⊢ □_c B, Δ when (A = B and a ≤ c), or (A = P a constant, B = φ(P), a ≤ c), or
  (A = φ(P), B = P, a + 1 ≤ c).
- *Nec*: from ⊢ A (empty context) of size s, infer Σ ⊢ □_c A, Δ, provided s ≤ c. Size s + 1.
- *JLöb(S, b)* (joint bounded Löb), S = {A_1, …, A_k} a set of formulas, 1 ≤ k ≤ 3: from the k premises
  □_b A_1, …, □_b A_k ⊢ A_j (sizes s_j), infer Σ ⊢ A_i, Δ for any A_i ∈ S — or Σ ⊢ φ(A_i), Δ when A_i is a
  constant P — provided b ≥ 1 + Σ_j s_j. Size 1 + Σ_j s_j.

In the spec's terms: c₂ = 1 (the JLöb sequent itself) and c₁ = 0, because there is no distribution step: the joint
rule takes the conjunction's members as separate hypotheses, so the spec's "□_b(A∧B) → □ A" projection never has
to be paid. There is no cut and no GLR context Γ; K is strictly weaker than GL, and how much weaker is measured.

**Soundness theorem.** Every K-derivable sequent is true in T.

*Proof,* by strong induction on derivation size n; the claim at n is "every K-derivation of size ≤ n has a true end
sequent". Box truth is not part of the induction: it is the fixed set of facts "some K-derivation of ⊢ A has
≤ b sequents".
- Initial sequents: P ⊢ P, ⊥ ⊢, ⊢ ⊤ are true. BoxEq: (a ≤ c) a derivation of ≤ a sequents has ≤ c. (A = P, B = φ(P))
  needs **Lemma W**: if ⊢ P has a K-derivation of size s, then ⊢ φ(P) has one of size ≤ s. Proof of W: the last rule
  of a derivation of ⊢ P with empty left side cannot be an initial sequent (P ≠ ⊤, nothing on the left), a
  propositional rule (P is atomic), Nec or BoxEq (their right formula is a box); so it is UnfR, whose premise ⊢ φ(P)
  has size s − 1, or JLöb concluding P, which may instead conclude φ(P) with the same premises and size. (A = φ(P),
  B = P, a + 1 ≤ c): append UnfR to a derivation of ⊢ φ(P).
- Propositional rules and unfolding: truth-preserving because P ↔ φ_x[y] holds in T by definition.
- Nec: the premise derivation itself witnesses □_c A (size s ≤ c), so the conclusion's right formula is true.
- JLöb: let D be the instance, |D| = 1 + Σ s_j ≤ b. For each j, D with its conclusion replaced by ⊢ A_j is a
  K-derivation of ⊢ A_j of size |D| ≤ b, so every □_b A_j is true. Each premise has size < |D|, so by the
  induction hypothesis each premise sequent is true; its left side is all true, so every A_j is true, hence the
  conclusion's A_i (or φ(A_i), equivalent in T) is true. ∎

The JLöb case is the bounded Löb theorem (Critch 2016) at the calculus level with the overhead explicit: the
derivation that discharges □_b A is the derivation of A itself, and it fits in the budget exactly when
b ≥ 1 + Σ s_j. The rule is sound only with an empty context on the premises' left beyond □_b S (a contextual
premise would not give a closed derivation of ⊢ A_j).

**Decidability.** "K ⊢ A within b" is decided exactly by a size-bounded search: JLöb's S ranges over subsets of
size ≤ 3 of the box contents reachable from A by unfolding (a member outside that set can only add premises, so it
never helps a minimal derivation), its b over [1, cap], and every other rule is analytic.
