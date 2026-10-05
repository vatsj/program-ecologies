# Predictions: an explicit proof system with measured proof length, 2026-10-05

Spec: `specs/2026-10-05-proof-length.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-05-proof-length-gpt-6.1-sol.md`,
and revised). Committed before the prover's audit, before any length table and before any run. Part A is static and
exact (certified minima, or flagged upper bounds); Part B's chain numbers are ε → 0 objects at stated N; its lottery
numbers are ε = 0 finite-(N, I) objects with Wilson intervals.

## Design choices fixed before the run (where the spec leaves room)

1. **GLS+Def, the exact calculus.** Sequents Γ ⊢ Δ of *sets* of formulas over P_{xy}, ⊥, ⊤, ¬, ∧, ∨, →, □.
   G3-style (context-sharing, invertible propositional rules, principal formula removed in the premise; weakening and
   contraction absorbed). Initial sequents: Γ, A ⊢ A, Δ for A *propositionally atomic* (a constant P_{xy} or a boxed
   formula □B); Γ, ⊥ ⊢ Δ; Γ ⊢ ⊤, Δ. Unfolding: replace P_{xy} by φ_x[y] on the left or on the right (one sequent each).
   GLR (the Löb rule, Sambin–Valentini): from □Γ, Γ, □A ⊢ A infer Σ, □Γ ⊢ □A, Δ; the backward search always carries
   *every* boxed formula of the left side into □Γ (weakening is size-preserving, so this loses no minimal derivation).
   Size = number of sequents in the derivation tree. Λ = number of GLR applications.
2. **Frozen syntax.** φ_x is the evaluator's representative source `rep[x]` (shortest source of the canonical class)
   translated literally: C ↦ ⊤, D ↦ ⊥, not/and/or ↦ ¬/∧/∨; BOX(THEM(ME)) ↦ □P_{yx}, BOX(THEM(THEM)) ↦ □P_{yy},
   BOX(THEM(^A)) ↦ □P_{yA}; BOXD(·) ↦ □¬P; level-k boxes BOXk(s) ↦ □(¬□^k⊥ → s), BOXDk(s) ↦ □(¬□^k⊥ → ¬s)
   (k = 1 is the DSL's BOX1; k = 2 is used only for the Conjecture-4 siblings and the prudence ladder, out of L_8).
3. **Roots.** L_C: ⊢ P_{xy}; L_D: P_{xy} ⊢ ; L_C¹: ⊢ ¬□⊥ → P_{xy}; L_D¹: ⊢ ¬□⊥ → ¬P_{xy} (the formula as written, so
   the level-1 lengths include the →R/¬ steps).
4. **Exact minima.** The full backward-reachable sequent graph of each root is built (finite: formulas lie in the
   unfolding/subformula closure) and minimal (size, Λ) — lexicographic, so Λ is the minimum over minimal-size
   derivations — is computed by Knuth's generalized Dijkstra over the AND-OR graph. This is equivalent to iterative
   deepening on size run to convergence and certifies minimality; an unreachable root (no finite cost) is a certified
   non-theorem. If a root's graph exceeds a cap (2·10⁶ sequents, or a wall-clock cap), the root is *uncertified*: an
   upper bound is reported from the best derivation found by a bounded search, flagged, and never regressed.
5. **Reader cost L(x → y)** for the proxy comparison (the proxy is v(x, y) = k(y)·(1 + settle(y, x)), x reading y).
   Primary: L_read(x, y) = Σ over x's essential box atoms against y that are true at the stable world of the minimal
   GLS+Def size of the atom formula itself (⊢ □P…, or ⊢ □(¬□⊥ → …)); false atoms contribute 0 (no proof exists).
   Secondary: L_out(x, y) = minimal size for x's actual outcome against y at level 0 (L_C if x plays C, L_D if D),
   ∞ when unprovable. Spearman is over pairs with v > 0 (and finite L for L_out).
6. **Nesting depth** of a pair = max DSL box-nesting depth of x and y (a box inside a quoted argument ^A adds 1;
   FairBot and PrudentBot have depth 1). **Establisher** = self-cooperating, defects on D (NOTATION).
   **Mutually cooperating establisher pairs**: ordered (x, y), both establishers, val[x,y] = val[y,x] = C, x = y included.
7. **The prover family P and named classes**: FairBot, `BOX1(THEM(ME))`, `BOX(THEM(THEM))`, `BOX1(THEM(THEM))`,
   `BOX(THEM(^C))`, `BOX1(THEM(^C))`, PrudentBot, P*, and the Conjecture-4 ladder (P2, P12b, P*1b, PB2); their
   siblings y = or(x, ψ_K) and fakers z = BOX_K(THEM(^D)) (`src/conj4.py`); the scramble-lemma fakers
   `not(BOX(THEM(ME)))`, `BOX1(THEM(^not(BOX(THEM(ME)))))`. Out-of-L_8 programs are checked against the independent
   trace evaluator `src/conj4.py` instead of the box-fact tables.
8. **K (Part B), fixed now so the grid is a prediction, not a fit.** Boxes carry budgets □_b. K = the propositional and
   unfolding rules of GLS+Def, atomic initial sequents, and three modal rules, all with the same size count:
   - *BoxEq* (initial sequent): Γ, □_a A ⊢ □_c B, Δ if (A = B, a ≤ c) or (A = P, B = φ(P), a ≤ c) or
     (A = φ(P), B = P, a + 1 ≤ c);
   - *Nec*: from ⊢ A (empty context, size s) infer Σ ⊢ □_c A, Δ if s ≤ c (size s + 1);
   - *joint bounded Löb* JLöb(S, b), S a set of 1–3 box contents: from □_b S ⊢ A_j for every A_j ∈ S (sizes s_j)
     infer Σ ⊢ A_i, Δ (or Σ ⊢ φ(A_i), Δ when A_i is a constant P), provided b ≥ 1 + Σ s_j; size 1 + Σ s_j
     (so c₂ = 1 per instance; there is no separate distribution rule, so c₁ = 0 and no cut).
   Truth of □_b A = existence of a K-derivation of ⊢ A of size ≤ b. Level-k bounded boxes: BOXk_b(s) ↦
   □_b(¬□_b^k⊥ → s) (consistency at the reader's own budget). Quoted arguments ^A of a program at budget b are at
   budget b (as `bounded.genotypes`). Soundness is proved in `notes/proof-length.md` by induction on derivation size
   (the JLöb witness is the instance itself, re-concluded at A_j). K is weaker than GL by design (no GLR context Γ,
   no cut); its incompleteness against GL is measured, not assumed away.

## RE predictions (verbatim from the spec)

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

## Subagent predictions (S1–S10), with falsifiers

- **S1 (audit beyond L_8).** GLS+Def provability (levels 0–2) agrees with `src/conj4.py`'s stable trace on every
  ordered pair among the named classes, their siblings and fakers. *Falsifier:* a surviving disagreement.
- **S2 (certification).** All n = 6 roots (4 × 4,356) are certified with the full graph; ≥ 95% of the provable n = 8
  sampled roots are certified within the cap. *Falsifier:* certified fraction < 0.95 at n = 8.
- **S3 (anchors in this calculus).** L_C(FairBot, FairBot) = 4 with Λ = 1; L_C(`BOX1(THEM(ME))`, itself) = 6 at level 0
  with Λ = 1. *Falsifier:* any other value.
- **S4 (siblings are additive).** L(x → sibling) − L(x → x) is a small constant (≤ 6 sequents for every member of P,
  ≤ 4 for FairBot): the dormant disjunct is weakened away, never unfolded. Hence the ratio is ≥ 1.5 only for the
  smallest provers and falls below 1.5 for PrudentBot and P* (RE 2's sibling clause fails without its falsifier
  firing, since no sibling is cheaper than self). *Falsifier:* ratio ≥ 1.5 for every member, or a difference > 6.
- **S5 (proxy agreement is moderate).** Spearman(v, L_read) over v > 0 lies in [0.2, 0.7) at n = 6 and at n = 8.
  *Falsifier:* ≥ 0.7 or < 0.2 at either size.
- **S6 (Λ counts consistency steps).** In GLS every box introduction is a GLR application, including the □⊥ steps of
  level-1 boxes; PrudentBot–PrudentBot has Λ ∈ {3, 4} (depth + 2 or + 3). *Falsifier:* Λ ≤ 2 or Λ ≥ 5.
- **S7 (K grid: copies are cheaper).** In K, FairBot_b against an exact copy (b_x = b_y) cooperates from b = 3, while
  distinct budgets need min(b_x, b_y) ≥ 5 (the joint Löb over {P_xy, P_yx}); `BOX1(THEM(ME))`: 5 on the diagonal,
  9 off it. Every cell is symmetric. So budgets 3–4 (resp. 5–8) are *soft cliques*: a proof-length fingerprint, as
  `notes/conjecture4.md` §6 anticipated. *Falsifier:* a (C, D) cell, or the diagonal threshold equal to the
  off-diagonal one in either family.
- **S8 (K is almost complete on L_6).** ≥ 0.9 of the n = 6 GL-true box atoms (μ-weighted over pairs) are K-provable
  at some budget ≤ 40; at a global budget above the largest K length over P, the n = 6 bounded arm's P(C,C) at
  N = 10⁴ is within 0.05 of the free arm. *Falsifier:* < 0.9, or a difference > 0.05.
- **S9 (cost of cooperation: monotone, not tight).** Among mutually cooperating establisher pairs at n = 8,
  Spearman(L_C, |x| + |y|) ≥ 0.5, but the linear fit's residual sd is ≥ 0.3 of the mean (the predictor that matters
  is the number of P constants unfolded, not node count). *Falsifier:* Spearman < 0.5, or residual sd < 0.3 of mean.
- **S10 (price ladder returns).** With budget priced at c·b per match against every opponent, ALLC (free) strictly
  invades every priced prover world, so at N = 10⁴ π on non-cooperating states is ≥ 0.5 at c = 0.1 and at c = 0.01,
  and P(C,C) < 0.3. *Falsifier:* P(C,C) ≥ 0.5 at c = 0.01.

## Verdict rules

- A prediction **holds** if every clause holds; **fails (falsifier fired)** if its falsifier fires; **partly** if some
  clause fails without the falsifier firing; **not run** if the run was not reached (Part B is run in the spec's
  order as far as time allows).
- Uncertified lengths (upper bounds) are never used as exact: regressions and Spearman use certified roots only, and
  the certified fraction is reported next to each statistic.
- Lottery cells report Wilson 95% intervals; chain cells report support and transition structure with π.
