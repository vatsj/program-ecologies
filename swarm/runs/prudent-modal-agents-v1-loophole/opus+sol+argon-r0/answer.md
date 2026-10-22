# Prudent modal agents — answer

FORMULA: B(a)|B(~a)->B(F)
DEPTH: 1

(Parsed as (□a ∨ □¬a) → □⊥. Equivalent, slightly longer: `B(F) | ~B(a) & ~B(~a)`, i.e. □a ↔ □¬a.)

check.py: `depth 1; vs CooperateBot D, vs DefectBot D, vs FairBot C, vs itself C; prudent: YES`

## 1. Outcome table (world-by-world)

Let X = (□a ∨ □¬a) → □⊥. At world 0 every box is true, so X = C at world 0 against everyone. For n ≥ 1, □⊥ is
false, so X cooperates at n iff neither □a nor □¬a holds, i.e. iff the opponent's `a` took **both** values at worlds < n.

| opponent | X's moves at worlds 0,1,2,3,… | stable |
|---|---|---|
| CooperateBot (a ≡ ⊤) | C, D, D, D, … | **D** |
| DefectBot (a ≡ ⊥) | C, D, D, D, … | **D** |
| FairBot (a_n = ∧_{m<n} X_m) | a: 1,1,0,0,…; X: C, D, D, C, C, … | **C** |
| itself (a_n = X_n) | C, D, C, C, … | **C** |

## 2. Minimality: no depth-0 agent is prudent

A depth-0 formula has no boxes; since it must be fully modalized it contains no atoms, so it is a Boolean
combination of ⊤, ⊥, i.e. equivalent to the constant ⊤ or ⊥. If ⊤, it cooperates with CooperateBot; if ⊥, it
defects against FairBot (and itself). Either way it is not prudent. Hence the minimal depth is exactly 1, attained
above. (The problem's "evidence" — no prudent agent among depth ≤ 2, ≤ 7 symbols — is consistent: our prudent formula has 9 symbols, see §3.)

## 3. Characterization of the depth-1 prudent agents, and minimal size

**Reduction to a set function.** A depth-1 fully modalized formula is a Boolean combination of ⊤, ⊥ and boxes □ψ
with ψ propositional in a, c, d. At world n, □ψ holds iff every triple (a,c,d) realised at worlds m < n satisfies ψ.
So X's move at world n is f(S_n), where S_n ⊆ {0,1}^3 is the set of triples (a_m, c_m, d_m) seen at worlds m < n
(S_0 = ∅), and f: P({0,1}^3) → {0,1} is determined by φ. Conversely every such f arises: S is determined by the
truth values of the boxes □¬χ_t (t ∉ S), χ_t the conjunction describing triple t, so f is a Boolean combination of them.

Write u = 111, v = 000, w = 100, h = 110, k = 010 (order a,c,d), and x0 = f(∅) (X's move at world 0, the same against everyone).

- **vs CooperateBot**: CB cooperates with everyone, so the triple is u at every world; S_n = {u} for n ≥ 1.
  Stable move f({u}). Need **f({u}) = 0**.
- **vs DefectBot**: triple v always; stable move f({v}). Need **f({v}) = 0**.
- **vs FairBot**: FB vs CB = □⊤ = 1 always; FB vs DB = □⊥ = 1 at world 0 only; FB vs X at n = ∧_{m<n} X_m.
  World 0 triple: u. X at world 1 = f({u}) = 0, so FB's `a` is 0 from world 2 on. World 1 triple (x0,1,0); worlds ≥ 2: k.
  Stable move f({u,(x0,1,0),k}).
- **vs itself**: X vs CB and X vs DB are x0 at world 0 and 0 afterwards (by the two conditions above). 
  - If x0 = 0: world-0 triple v, X_1 = f({v}) = 0, triple stays v forever, stable move 0 — not prudent. So **x0 = f(∅) = 1**.
  - With x0 = 1: triple u at world 0, X_1 = f({u}) = 0, triple v at world 1. X_2 = f({u,v}). If it is 0 the triple stays v
    and S stays {u,v}: stable 0. So **f({u,v}) = 1**; then the world-2 triple is w, and from world 3 on S = {u,v,w}
    whatever happens (the triple is w or v, both already seen), so the stable move is f({u,v,w}): need **f({u,v,w}) = 1**.
  - With x0 = 1 the FairBot condition reads **f({u,h,k}) = 1**.

**Theorem.** A depth-1 agent is prudent iff its set function f satisfies
f(∅)=1, f({111})=0, f({000})=0, f({111,000})=1, f({111,000,100})=1, f({111,110,010})=1.
(Necessity and sufficiency both follow from the case analysis above, which computes every relevant game exactly.)
The other 256 − 6 = 250 values of f are unconstrained, so there are exactly **2^250** prudent depth-1 agents up to
equivalence on finite linear GL frames. Example check for our formula f(S)= [S=∅] ∨ [S contains triples with a=1 and with a=0]:
values 1,0,0,1,1,1 as required.

**Minimal size.** Counting symbols (atoms, T, F, ~, &, |, ->, B; parentheses not counted), an exhaustive search over
depth-1 formulas using this characterization (`/work/sol_minsize.py`: computes for each relevant behaviour the
smallest formula, by size, over all propositional inner formulas and all Boolean outer combinations, sizes ≤ 13)
finds the minimum is **9 symbols**, attained by `B(a)|B(~a)->B(F)`. This size-minimality claim concerns depth 1 only; no size-minimality claim across all modal depths is needed.

Also found (depth 2, classical PrudentBot style): `B(a) & B(B(F) | ~d)` is prudent.

Credits: found independently by sol and opus; characterization cross-checked on the board.
