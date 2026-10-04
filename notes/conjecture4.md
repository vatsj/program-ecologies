# Conjecture 4: proof notes (2026-10-04)

Spec: `specs/2026-10-04-conjecture4.md`. Review: `reviews/2026-10-04-conjecture4-gpt-6.1-sol.md`.
Written incrementally. Ledger tags on every step:
- [SEM] a theorem about the evaluator semantics (linear GL chain, stable value), proved here;
- [ARITH] an arithmetic assumption or classical theorem used to lift [SEM] to PA;
- [BUDGET] a proof-budget condition (only in the transfer section);
- [EVAL] an evaluator-only observation (checked by running `src/modal.py` / `src/modal_lv.py`, not proved).

## 0. Semantic universe (the evaluator, written out)

Programs: A ::= C | D | not A | and A A | or A A | BOX_L(App) | BOXD_L(App), L = 0, 1, 2, ...
App ::= THEM(ME) | THEM(THEM) | THEM(^A).

Evaluation of x against y at world n = 0, 1, 2, ... (`modal._evaluate`, `modal_lv._evaluate_lv`):
- an atom of x is a statement about a pair (p, q) = "p plays a against q":
  THEM(ME) -> (y, x); THEM(THEM) -> (y, y); THEM(^A) -> (y, A);
- BOX_L(p, q) holds at world n iff p plays C against q at every world m with L <= m < n;
  BOXD_L(p, q) likewise with D. (Vacuously true for n <= L.)
- x's action at world n is its boolean formula on the atom values at n.
- the outcome is the stable value (the value at all sufficiently large n).

Inter-level principles the evaluator uses (and nothing else): the level-L box looks only at worlds >= L. In GL,
BOX_L s = □(◇^L ⊤ → s), i.e. provability in T_L = PA + ¬□^L⊥ (PA + Con^L(PA)). On the linear chain ◇^L⊤ holds
exactly at worlds >= L. So the evaluator is the linear-chain (letterless) semantics of these GL formulas.

Definitions (RESULTS "Universality against drift-closure"): x self-cooperates iff x(x) = C; x is suckerable iff some
y has x(y) = C and y(x) = D; G = mutual-cooperation graph on self-cooperators; K(x) = x's component; x drift-closed
iff no member of K(x) is suckerable. Evolutionary reading only in the rare-mutation monomorphic chain (Lemma 1).

## 1. Lemma A (finite settling) [SEM]

For any finite set of programs closed under fixed arguments, every pair's trace is eventually constant.
Proof: for n > L, BOX_L(p,q) at n+1 = BOX_L(p,q) at n AND [p plays C vs q at world n]; so each atom, once n > L, is
monotone non-increasing (true -> false at most once). The pairs reachable from (x, y) through atoms form a finite
set P(x,y) (opponent is always y, or a fixed argument; the left side is x, y, or a fixed argument). Finitely many
atoms, each flipping at most once after its level, so all values are constant from some world s(x, y) on.
Write settle(p, q) for the first world from which p's play against q is constant.

## 2. The sibling (main construction)

Fix a self-cooperating x. Let F(x) = x together with every program appearing as a fixed argument ^A anywhere inside
x, recursively (finite). Let K = max over P in F(x) of settle(P, D). Define

    psi_K  = and(not(BOX_K(THEM(^D))), not(BOXD_K(THEM(^D))))     "your play against DefectBot is undecided in T_K"
    y      = or(x, psi_K)          (x's source, with ME now referring to y)
    z      = BOX_K(THEM(^D))       (a faker of y)

Size: |y| = |x| + 12, |z| = 4.

**Lemma B (psi is silent on settled opponents) [SEM].** If settle(T, D) <= K then psi_K(T) is false at every world.
Proof: at n <= K, BOX_K is vacuously true, so not(BOX_K) is false. At n > K, T's play against D on [K, n) is one
constant value, so one of BOX_K, BOXD_K is true. Either way psi_K is false.

**Lemma C (mimicry) [SEM].** Let S = F(x) ∪ {D}. For every world n and every P in S:
 (i) y vs P at n = x vs P at n;  (ii) P vs y at n = P vs x at n;  (iii) y vs y at n = x vs x at n.
Proof by induction on n (all claims at once; at n the atoms read only worlds < n).
- (i) y vs P = or(x-formula with ME = y, psi_K)(P). The x-part's atoms are (P, y), (P, P), (P, A) for A in args(x)
  ⊆ F(x); by (ii) at earlier worlds, (P, y) has x's trace (P, x) there, so the x-part equals x vs P at n.
  psi_K(P): for P in F(x), settle(P, D) <= K by choice of K, so psi_K(P) is false (Lemma B); for P = D, D's play
  against D is constant D, so false. Hence y vs P = x vs P at n.
- (ii) P's atoms against y are (y, P), (y, y), (y, A) with A in args(P) ⊆ S (args of D: none; F(x) closed). By
  (i) and (iii) at earlier worlds these equal (x, P), (x, x), (x, A). So P vs y = P vs x at n.
- (iii) y vs y: the x-part reads (y, y), (y, y), (y, A), equal at earlier worlds to (x, x), (x, x), (x, A), so it
  equals x vs x at n. psi_K(y) reads y vs D, which equals x vs D at every earlier world by (i) with P = D, and
  settle(x, D) <= K, so by the argument of Lemma B (it only uses the trace on worlds < n) psi_K(y) is false.

**Theorem 1 (Conjecture 4, evaluator semantics, unbounded box levels) [SEM].** Every self-cooperating x has a
suckerable member of K(x) at distance at most 1. So no class is drift-closed.
Proof. Case 1: x plays C against D (stable). D defects on everything, so x is suckerable; distance 0.
Case 2: x defects on D (stable). Build y, z as above.
- y ∈ K(x): by Lemma C, y vs x = x vs x = C, x vs y = x vs x = C, y vs y = x vs x = C (stable values).
- z defects on y: z = BOX_K(THEM(^D)) plays C against y at n iff y plays C against D on all of [K, n). y vs D =
  x vs D (Lemma C (i)), which is stably D, so z plays D against y from some world on.
- y cooperates with z: z vs D is C at worlds <= K (vacuous box) and D at worlds > K (D never cooperates). So for
  n >= K + 2 the window [K, n) holds both values, psi_K(z) is true, and y = or(..., psi_K) plays C against z.
So y is suckerable and adjacent to x in G. QED.

Note what the proof uses: (a) closure of the grammar under `or`; (b) one non-monotone test, "undecided at level K"
(cooperation conditional on non-provability); (c) box levels up to K(x), which grows with x; (d) x's view of y is
*extensional through finitely many probes* (y vs x, y vs y, y vs fixed arguments). No Löb, no fixed-point
uniqueness, no linearity beyond the evaluator's definition. (d) is the step that fails with source access.

**Lemma D (one more Con level suffices) [SEM].** For any program P, settle(P, D) <= maxlevel(P) + 1.
Proof: against D every atom of P reads a pair (D, ·), and D's play is constant D. So BOXD_L is always true and
BOX_L is true iff n <= L. P's play at n depends on n only through the flags [n <= L], all false for
n > maxlevel(P). Hence K(x) <= maxlevel(F(x)) + 1, and:

**Corollary 2 [SEM].** Every self-cooperating x with boxes up to level k has a suckerable neighbour y (size
|x| + 12) with boxes up to level k + 1, and y's faker z = BOX_K(THEM(^D)) has size 4. In the language with all
levels (the union over k) no class is drift-closed. For a *fixed* level cap k, Theorem 1 does not apply; that
sub-language is the open case (static evidence only: G is one component at k = 1, n <= 11, and k = 2, n <= 9).

## 3. Evaluator check [EVAL]

`src/conj4.py` has its own trace evaluator (recursive, memoized, written from the definition in §0, independent of
`modal._evaluate`). Checks:
- the prudence ladder (FairBot, BOX1(TM), PrudentBot, P*, P2, P12b, P*1b, PB2, BOX(TT)): every sibling is in
  K(x) (mutual C with x, self-C), and z suckers it; mimicry holds trace-for-trace on F(x) ∪ {D}.
  K = 1 for FairBot and PrudentBot (y size 15 / 20), K = 2 for P*, P2, P12b (y size 20 / 21 / 26).
- every self-cooperating canonical function of L_n (levels <= lmax) for n/lmax = 6/1, 7/1, 8/1, 9/1, 6/2, 7/2, 8/2:
  y and z added to the `modal_lv` language and evaluated by `modal_lv._evaluate_lv`: 0 failures out of
  25 / 89 / 287 / 551 / 43 / 190 / 646 self-cooperators. Observed K <= lmax + 1, as Lemma D says.
- the two evaluators agree on 3,000 random pairs per language (0 disagreements).
- extended after the predictions commit (`runs/conjecture4.json`, key `sibling`): n/lmax = 10/1, 11/1, 9/2 also give
  0 failures (1,037 / 3,481 / 1,258 self-cooperators).

**Fixed level cap (the open sub-language) [EVAL].** Forcing K <= lmax (a level-preserving sibling, which Theorem 1
does not cover) still works for every self-cooperator at 9/1, 10/1, 8/2, 9/2, and even K = 0 works at 9/1, 10/1,
8/2, 9/2. It first fails at n = 11, lmax = 1: K = 1 fails for 4 classes, e.g.
`and(BOX(THEM(ME)),BOXD1(THEM(^not(BOX1(THEM(ME))))))`, and K = 0 for 8. The cause is exactly what Lemma B guards
against: the fixed argument `not(BOX1(THEM(ME)))` plays D, D, C, C, … against D, so ψ_1 fires on it from world 3,
the sibling cooperates with it, and x's BOXD1 probe sees the difference. These classes are *not* truncation-closed
candidates: G is one component at n = 11, so they reach suckerable classes by other paths inside L_11, and each has
the K = 2 sibling one level up. So the fixed-cap question stays open with no candidate counterexample.

## 4. Lifting Theorem 1 beyond the evaluator

**(a) Modal validity.** Each pairing of finitely many programs is a system of modal fixed points
p_{a,b} ↔ φ_a(boxed p's), every recursion guarded by a box. By de Jongh–Sambin each p_{a,b} has a unique (up to
GL-provable equivalence) letterless solution [ARITH-free, a GL theorem]. A letterless sentence's truth value at world
n of *any* GL frame depends only on the depth of n, and on the linear chain world n has depth n; so the evaluator's
trace is the letterless solution's trace and the stable value is its value at large depth. Lemmas A–D and Theorem 1
are statements about these traces, so they hold for the GL fixed points: "x and y mutually cooperate" means GL ⊢ the
corresponding letterless sentences are equivalent to formulas true at all large depths, i.e. to ¬□^k⊥ combinations
that are eventually true. [SEM + GL fixed-point theorem]

**(b) Arithmetic.** Realize □ as Prov_PA and BOX_L as provability in T_L = PA + ¬□^L⊥ (PA + Con^L(PA)). The fixed
points exist arithmetically by the diagonal lemma, and by the arithmetical soundness of GL together with uniqueness
of fixed points, the letterless solution is PA-provably equivalent to the sentence "a plays C against b" (Solovay's
completeness theorem is not needed). A letterless sentence is true in N iff
it holds at all sufficiently deep worlds, *provided* N ⊨ ¬□^k⊥ for every k, i.e. every T_k is consistent. That holds
because PA is sound. [ARITH: soundness of PA, or at least the consistency of PA + Con^k for all k]
So in the standard model: y and x actually cooperate with each other and with themselves, z actually defects on y and
y actually cooperates with z. The sibling is suckerable in the real program game, not only in the evaluator.

**(c) What is not claimed.** Nothing about modal validity on non-linear frames beyond the letterless reduction;
nothing about polymorphic residents (Lemma 1 is monomorphic); nothing about a fixed level cap k (Corollary 2).

## 5. Dependency ledger (per step)

| step | type | uses GL-specific structure? | needs only "programs can test provable behaviour"? |
|---|---|---|---|
| Lemma A (finite settling) | SEM | linear chain + monotone boxes (each flips once) | analogue: bounded search has finite traces trivially |
| Lemma B (ψ silent on settled opponents) | SEM | level-L boxes see worlds ≥ L | needs a *decidedness* test: "neither proof of C nor of D within T_K" |
| Lemma C (mimicry) | SEM | no: induction on worlds; uses only that x sees y through finitely many probes | the key step; fails if x reads source |
| Lemma D (K ≤ maxlevel + 1) | SEM | yes: D is constant, so traces vs D depend only on level flags | bounded analogue: decide x's play vs D within budget b_x |
| Theorem 1 | SEM | no beyond the above | yes, given the mimicry property |
| arithmetic lift (§4b) | ARITH | de Jongh–Sambin, letterless normal form | soundness of PA / consistency of all T_k |
| evaluator check (§3) | EVAL | n ≤ 9, lmax ≤ 2 | — |

No step uses Löb's theorem. Löb is what makes x self-cooperate in the first place (FairBot); Theorem 1 takes
self-cooperation as given and only needs y to inherit it, which mimicry supplies.

## 6. Transfer to bounded proof search over source

Setting: deterministic programs that read the opponent's source and search for PA-proofs of length ≤ k about its
play (Critch 2019). Write □_k φ for "a proof of φ of length ≤ k exists" (decidable).

**Lemma 1 and Corollary 1 (prediction 2a).** Lemma 1 uses only determinism, the four distinct PD payoffs and the
fixation rule. Corollary 1 uses only that FairBot cooperates with ALLC and that ALLC is suckerable. A bounded
FairBot_k cooperates with ALLC as soon as k exceeds the constant length of a proof that ALLC's source returns C.
So both transfer, with the single budget condition k ≥ c_ALLC. No step needs the linear chain or GL.

**Theorem 1 (prediction 2b).** The bounded sibling is y = or(x, ψ_b), with
ψ_b(opp) = ¬□_b[opp plays C vs D] ∧ ¬□_b[opp plays D vs D], and the faker z = "cooperate iff □_B[opp plays C vs D]".
- *z is a faker of y.* z defects on y because y defects on D (as x does) and PA is consistent. y cooperates with z
  when ψ_b(z) holds: "z defects on D" says "no proof ≤ B of a refutable sentence exists", essentially the finite
  consistency statement Con_B(PA). Pudlák (1986) shows its shortest PA-proofs have length between B^ε and B^c. So for
  B ≥ b^{1/ε}, no proof ≤ b decides z vs D, and ψ_b(z) holds. [BUDGET: B ≥ poly(b); ARITH: Pudlák's lower bound]
- *ψ_b is silent on x, y and x's probe opponents* if b ≥ b_x, where b_x is the longest proof that some program in
  F(x) ∪ {y} defects (or cooperates) with D. This replaces K ≥ settle(P, D). [BUDGET: b ≥ b_x]
- *Mimicry* is where the bounded case differs. x sees y through its own proof searches. For x to treat y as it
  treats itself, every probe "□_k[opp plays a vs Q]" that succeeds on x must also succeed on y, and vice versa.
  Proving "y plays C vs Q" costs the proof for x plus O(|y|) (unfold the `or`). Proving "y plays D vs Q" also
  needs ψ_b(Q) false, i.e. an explicit proof ≤ b that Q's play vs D is decided: by Σ1-completeness, a proof of
  length poly(b). The self-referential probes (y vs x, x vs y) need bounded Löb: Critch's theorem gives mutual
  cooperation once k exceeds the length of the Löbian argument, which is linear in |x| + |y| plus O(log k).
  So the sibling is in K(x) when every probe budget k_i of x satisfies
      k_i ≥ ℓ_i(x) + poly(b_x) + c·(|x| + |ψ_b| + log k_i),
  where ℓ_i(x) is the proof length the probe needs when x meets its own copy. [BUDGET]
- *When the threshold fails* (tight budgets: k_i just above ℓ_i(x)), x can reject its sibling, because the
  sibling's proofs are longer. That is a length fingerprint, a soft form of source recognition. Whether some other
  neighbour is then suckerable is open. With full source access the conjecture is simply false: CliqueBot
  ("cooperate iff the source equals mine") is unsuckerable and alone in its component (RESULTS "Priced arm",
  cliques absorbing).

So what transfers: the regress (Lemma 1, Corollary 1) unconditionally; the impossibility of drift-closure only for
readers whose observation of the opponent is extensional on finitely many probes with slack in their proof budgets.
Drift-closure is possible exactly when the reader can tell a sibling from a copy, by syntax (cliques) or by proof
length (tight budgets). Both are forms of incumbency or self-recognition.

## 7. The leak (Task 2) — see runs/conjecture4.md for the tables

- Uniform boundedness of leak/μ(FairBot) is trivial under the length prior: leak ≤ Σ_s 1/(2s²) = π²/12 and
  μ(FairBot) ≥ 1/324 unnormalized, so leak/μ ≤ 27π² ≈ 266 at every n. The content is the limit value.
- n = 12, 13 (`src/moat_static_big.py`, 54 s and 388 s): one component, no closed class, max drift distance 1;
  FairBot leak/μ 92.45 and 92.22, the minimum at both; runner-up `BOX1(THEM(ME))` 2·10⁻⁴ above.
- Shells: a near-constant fraction, 0.41–0.42 of every length shell s = 5–13, is a suckerable FairBot mate; FairBot's
  own class takes 0.007–0.009 of each shell. So the shell contributions decay like 1/s² (successive ratios 0.75 →
  0.856 at s = 13, tracking ((s−1)/s)²), not geometrically, and leak/μ drifts down slowly toward the ratio of the
  tail fractions. With constant fractions (0.42 and about 0.008) the limit is about 89–90 (extrapolated, [EVAL]).
  Shell contributions are stable across cutoffs (a shell's leak does not change once n ≥ s + 2).
- Lower bound from Theorem 1, for every unsuckerable x: leak(x) ≥ μ(class of or(x, ψ_K)) at cutoffs ≥ |x| + 12, which is
  ≥ μ(x)·min_s s²a(s)/((s+12)²a(s+12)) ≈ μ(x)·5^−12. Exact closure is defeated by a leak that can be ~10⁻⁹ of μ(x)
  for prudent x; the static map shows the actual leak is far larger (leak/μ ≥ 92 for every unsuckerable class).
