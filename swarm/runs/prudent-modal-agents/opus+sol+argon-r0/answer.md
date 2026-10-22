# Prudent modal agents — answer

FORMULA: B(a & (d -> B(F)))
DEPTH: 2

(i.e. φ_X = □(a ∧ (d → □⊥)) — "PrudentBot": cooperate iff PA proves the opponent cooperates with me and
PA+Con(PA) proves the opponent defects against DefectBot.)

## 1. Existence and outcome table

`python3 check.py "B(a & (d -> B(F)))"` →
`depth 2; vs CooperateBot D, vs DefectBot D, vs FairBot C (FairBot replies C), vs itself C; prudent: YES`

| opponent Y   | X vs Y | Y vs X |
|--------------|--------|--------|
| CooperateBot | D      | C      |
| DefectBot    | D      | D      |
| FairBot      | C      | C      |
| X itself     | C      | C      |

Trace proof (worlds n = 0,1,2,…; □ψ at n means ψ at all m<n). Write ψ = a ∧ (d → □⊥); note □⊥ is true only at world 0.
- vs CB: atoms a=c=d=⊤ always. ψ(m) = □⊥(m), true at m=0 only. So X = □ψ is C at n=0,1 and D for n≥2. Stable D.
- vs DB: a=⊥ always, so ψ false at every m, X is C at 0 and D for n≥1. Stable D.
- vs FB: FB's d-atom is "FB vs DB" = □⊥, true only at 0, where □⊥ is also true; so d→□⊥ holds at every world, and
  ψ ≡ a = "FB cooperates with X" = □x. Induction: x_0 = f_0 = 1; if x_m = f_m = 1 for all m<n then f_n = 1 and x_n = 1.
  Both C forever.
- vs itself: d-atom = "X vs DB" = C only at world 0, where □⊥ is true, so d→□⊥ holds everywhere; ψ ≡ a = x, and
  x_n = all x_m (m<n), which by induction is 1 forever. C.
Other depth-2 prudent agents (all checked): `B(a) & B(~B(F) -> ~d)`, `B(a) & B(B(F) | ~d)`, `B(a) & (B(B(F)) | ~B(d))` (sol).

## 2. No agent of modal depth < 2 is prudent (any size)

Depth 0: a fully modalized formula of depth 0 contains no atoms, so it is a constant. ⊤ cooperates with CooperateBot;
⊥ defects against FairBot. Neither is prudent.

Depth 1: φ_X = g(□ψ_1, …, □ψ_k) for a Boolean function g and propositional formulas ψ_i in a, c, d (and constants).
Key fact: the value of a fully modalized formula at world n depends only on the atom values at worlds m < n.

(a) Against CooperateBot, the atoms (CB cooperates with X / with CB / with DB) are ⊤ at every world. So for n ≥ 1,
□ψ_i(n) = ψ_i(1,1,1), independent of n; hence X's action vs CB is the same at every world n ≥ 1 and equals the stable
value. Prudence requires it to be D: g(ψ_1(1,1,1), …, ψ_k(1,1,1)) = 0.

(b) Against FairBot, at world 0 the opponent atoms are a = FB-vs-X(0) = □x(0) = ⊤, c = FB-vs-CB(0) = □⊤ = ⊤,
d = FB-vs-DB(0) = □⊥(0) = ⊤ (all boxes are vacuously true at world 0). So at world 1, each □ψ_i(1) = ψ_i(1,1,1), and
X's action vs FB at world 1 equals g(ψ_1(1,1,1), …) = 0 by (a): X defects against FB at world 1.

(c) Then FairBot's action against X, □(X cooperates with FB), is false at every world n ≥ 2 (world 1 < n is a
counterexample), so FairBot's stable action against X is D, violating prudence.

Hence no agent of depth ≤ 1 is prudent, and the minimal depth is exactly 2. (Same argument found independently by sol.)
More generally the argument shows: any agent whose action vs CB is already stable at world 1 cannot be prudent; depth 2
is needed so that X can see at world 2 the world-1 difference between FairBot (d false: FB defects vs DB) and
CooperateBot (d true).

## 3. Minimal size and characterization

Counting AST nodes (each atom, constant, ¬, ∧, ∨, →, □ counts 1):
- **Exact exhaustive verification (`verify_min_size.py`)**: testing every single fully modalized syntax tree without heuristic deduplication proves:
  - **With constants (`T, F`)**: out of all 10,476 ASTs of size ≤ 6, **0** are prudent; at size 7 (63,272 ASTs), **only 2** ASTs are prudent: `B(a & (d -> B(F)))` and `B((d -> B(F)) & a)` (both depth 2). Thus the minimal size with constants is **7**.
  - **Without constants (`a, c, d` only)**: out of all 11,754 ASTs of size ≤ 7, **0** are prudent (which explains the negative result in `problem.md` for constant-free formulas up to 7 symbols); at size 8 (63,885 ASTs), **only 6** ASTs are prudent: `B(a & (d -> B(~a)))`, `B(a & (d -> B(~c)))`, `B(a & (d -> B(~d)))` and their `&`-commuted variants (all depth 2). Thus the minimal size without constants is **8**.
- **Analytical necessity of `d`**: when FairBot cooperates with X, the atoms `a` and `c` are `⊤` at every world $m \ge 0$ against both CooperateBot and FairBot, so any formula not containing `d` evaluates identically against CooperateBot and FairBot and cannot be prudent.
- **Exact characterization of the canonical depth-2 family**: for any propositional formula $q(a, c, d)$, the depth-2 agent $\varphi_q = \square(a \wedge (d \to \square q))$ is prudent **if and only if** $q(\top, \top, \top) = \bot$ (yielding 128 pairwise-inequivalent Boolean functions $q$ over $a, c, d$). More generally, $\square(a \wedge (d \to \theta))$ is prudent for any $\square$-formula $\theta$ (which is vacuously true at world 0) that evaluates to false at some world $m \ge 1$ against CooperateBot (such as $\square\bot, \square\neg a, \square\neg c, \square\neg d$).
- Semantic deduplication search (`opus/enum.py`) up to size 8 agrees completely with these exact results.
