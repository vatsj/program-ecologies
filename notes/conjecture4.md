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
