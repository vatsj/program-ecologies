# Prudent modal agents — answer (opus + sol)

FORMULA: (B(a) | B(~a)) -> B(F)
DEPTH: 1

i.e. φ = (□a ∨ □¬a) → □⊥ ≡ □⊥ ∨ (¬□a ∧ ¬□¬a).
Equivalent alternatives (also checked prudent): `(B(a) -> B(~a)) & (B(~a) -> B(a))` (□a ↔ □¬a, found by sol),
`B(F) | (~B(a & c & d) & ~B(~(a & c & d)))`.

`python3 check.py "(B(a) | B(~a)) -> B(F)"` →
`depth 1; vs CooperateBot D, vs DefectBot D, vs FairBot C, vs itself C; prudent: YES`

## 1. The agent and its outcome table

Reading: X cooperates iff either PA is inconsistent (□⊥, true only at world 0), or PA neither proves that the
opponent cooperates with X nor proves that it defects against X.

World-by-world actions of X (worlds 0,1,2,3,…; stable value is last):

| opponent      | X's actions | outcome | opponent's action vs X |
|---------------|-------------|---------|------------------------|
| CooperateBot  | 1,0,0,0,…   | **D**   | C                      |
| DefectBot     | 1,0,0,0,…   | **D**   | D                      |
| FairBot       | 1,0,0,1,1,… | **C**   | FairBot: 1,1,0,0,… → D |
| itself        | 1,0,1,1,…   | **C**   | C                      |

(Against FairBot, X cooperates but FairBot defects against X — prudence only constrains X's own action.)

Derivation. At world 0 every box is true, so X cooperates (□⊥). At world n ≥ 1, □⊥ is false and X cooperates iff
the opponent's action toward X at the worlds < n takes both values.
- CB: always C, so □a holds → D from world 1 on. DB: always D, so □¬a holds → D from world 1 on.
- FairBot: FB vs X at world n is □(X vs FB at worlds < n): 1 (world 0), X0=1 (world 1), X0∧X1=0 (world ≥2).
  X vs FB: world 0: 1; world 1: sees {1} → 0; world 2: sees {1,1} → 0; world ≥3: sees {1,1,0} → 1 forever.
  (Checker sequence 1,0,0,1,1,…; stable C.)
- Itself: a = X's own action. World 0: 1; world 1: sees {1} → 0; world ≥2: sees {1,0} → 1 forever. Stable C.

## 2. No agent of smaller depth (depth 0) is prudent

A fully modalized formula of modal depth 0 contains no box, hence (every atom must lie inside a box) no atom: it is
a Boolean combination of ⊤, ⊥, i.e. a constant. A constant agent takes the same action against every opponent, so it
cannot both defect against CooperateBot and cooperate with FairBot. Hence the minimal depth is exactly 1. ∎

## 3. Characterization of all prudent depth-1 agents, and minimal size

**Normal form.** A depth-1 fully modalized φ is a Boolean combination of constants and boxes □ψ with ψ propositional
in a, c, d (no atom may occur outside a box). On a linear frame, □ψ is true at world n iff ψ holds at every
valuation v_m = (a,c,d) at the worlds m < n. Hence the truth value of φ at world n depends only on the set
S_n = {v_m : m < n} ⊆ {0,1}³: φ(n) = f(S_n) for a function f : P({0,1}³) → {0,1}. Conversely every f is realized,
since S is determined by the boxes: v ∉ S iff □¬χ_v (χ_v the conjunction characterizing v); then
f = ⋁_{S: f(S)=1} (⋀_{v∉S} □¬χ_v ∧ ⋀_{v∈S} ¬□¬χ_v). (At world 0, S=∅ and all boxes are true, consistently.)

Write valuations as abc-strings `acd`, e.g. 110 = (a=1,c=1,d=0). Let v0 = f(∅) (X's action at world 0 against anyone).

- vs CB: valuations are 111 at every world, S_n = {111} for n ≥ 1, outcome f({111}).
- vs DB: valuations 000, outcome f({000}).
- vs FB: FB's atoms: c = FB vs CB = □⊤ = 1; d = FB vs DB = □⊥ = [n=0]; a = FB vs X = □(X vs FB at < n).
  World 0: 111. X(1) = f({111}) = 0 (needed for CB). World 1: a = X(0) = v0, so (v0,1,0). World n ≥ 2:
  a = X(0)∧X(1) = 0, so 010. Thus S_n = {111, v0 10, 010} for n ≥ 3 and the outcome is f({111, v0 10, 010}).
- vs itself: c_n = X vs CB at n, d_n = X vs DB at n, both = v0 at n=0 and 0 for n ≥ 1 (given prudence vs CB, DB).
  - If v0 = 0: world 0 valuation 000; then X(1) = f({000}) = 0 and c = d = 0, so every valuation is 000 and X
    defects with itself forever. So **v0 = 1 is necessary.**
  - If v0 = 1: world 0 valuation 111, world 1: X(1) = f({111}) = 0 → 000. S_2 = {111,000}. If f({111,000}) = 0
    the valuation stays 000 and S never changes → defect forever. If f({111,000}) = 1, then world 2 valuation is 100,
    S_n = {111,000,100} for n ≥ 3, and the outcome is f({111,000,100}).

**Theorem.** A depth-1 agent with function f is prudent iff
f(∅) = 1, f({111}) = 0, f({000}) = 0, f({111,110,010}) = 1, f({111,000}) = 1, f({111,000,100}) = 1;
the values of f on the other 250 subsets are arbitrary. (So there are 2^250 prudent depth-1 agents up to
equivalence.) For the answer formula, f(S) = 1 iff S = ∅ or S contains valuations with both a = 1 and a = 0, which
meets all six conditions; sol's □a ↔ □¬a gives the same f.

**Minimal size.** Counting symbols (atoms, T, F, ~, &, |, ->, B; parentheses free), the smallest prudent depth-1
formula has **9 symbols**, e.g. `(B(a) | B(~a)) -> B(F)`. Proof: by the theorem, prudence of a depth-1 formula
depends only on its values on the six sets above, which depend only on the truth tables of the boxed propositional
formulas on the five valuations 111, 000, 110, 010, 100. `/work/opus/minsize.py` does an exhaustive size-ordered
dynamic program over (i) propositional truth tables on those 5 valuations and (ii) top-level value vectors on the 6
sets, and finds no formula of ≤ 8 symbols with vector (1,0,0,1,1,1); the first hit is at 9. (Merging formulas with
equal truth tables only lowers sizes, so this is a valid lower bound.) In AST nodes counting B(F) etc., sol's
`(~B(a) -> B(~a)) -> B(F)` has 10; ours has 9.

Note on the problem's "Evidence": the enumeration of 801 formulas missed these because every prudent depth-1 agent
needs f(∅)=1 together with f({111})=f({000})=0, which requires distinguishing S=∅ from singletons (e.g. by □⊥ or by
□a ∧ □¬a), and the enumeration excluded constants and used only ≤ 7 symbols.
