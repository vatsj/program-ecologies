# Prudent modal agents — answer

FORMULA: B(a & (d -> B(F)))
DEPTH: 2

(Equivalent in GL to `B(a) & B(~d | B(F))`, i.e. □a ∧ □(¬□⊥ → ¬d): "PA proves the opponent cooperates with me, and
PA+Con(PA) proves the opponent defects against DefectBot" — the PrudentBot of Barasz et al. / LaVictoire et al.)

## 1. A prudent agent of depth 2

`python3 check.py "B(a & (d -> B(F)))"` prints:

```
depth 2; vs CooperateBot D, vs DefectBot D, vs FairBot C (FairBot replies C), vs itself C; prudent: YES
```

| opponent      | X's action | opponent's action vs X |
|---------------|-----------|-------------------------|
| CooperateBot  | D         | C                       |
| DefectBot     | D         | D                       |
| FairBot       | C         | C                       |
| itself        | C         | C                       |

Hand verification, with X = □(a ∧ (d → □⊥)); write x_Y(n) for X's action against Y at world n.
Note □⊥ is true only at world 0.

- **vs CooperateBot** (a=c=d=⊤): X = □□⊥, true at worlds 0,1 and false from world 2 on → **D**.
- **vs DefectBot** (all atoms ⊥): X = □⊥, false from world 1 on → **D**. So x_DB = 1,0,0,…
- **vs FairBot**: d(m) = "FairBot coops with DefectBot" = □⊥ at m, true only at m=0, where □⊥ is also true; so
  (d → □⊥) holds at every world, and X ≡ □a against FairBot, i.e. X and FairBot are both □(other cooperates). By
  induction both cooperate at every world (at n, both depend only on the other's values at worlds < n, all true)
  → **C/C**.
- **vs itself**: d(m) = x_DB(m) = [m=0], same as above, so (d → □⊥) always holds and X ≡ □a with a = X itself;
  by induction X is true at every world → **C**.

## 2. Proof that no agent of modal depth < 2 is prudent

Let X be any fully modalized formula of depth ≤ 1 (any size). Since boxes are not nested and every atom lies inside a
box, φ_X is a Boolean combination of constants and formulas □ψ_1, …, □ψ_k where each ψ_i is box-free, i.e. a
propositional formula in a, c, d, ⊤, ⊥. (Depth 0 means k = 0: φ_X is a constant.)

At world n ≥ 1, □ψ_i is true iff ψ_i is true at all worlds m < n. In particular **the value of φ_X at world 1 is
determined by the values of the atoms a, c, d at world 0**: □ψ_i is true at world 1 iff ψ_i(a(0), c(0), d(0)) is true.

*Against CooperateBot*: a = c = d = ⊤ at every world, so for every n ≥ 1, □ψ_i at n has the constant value
ψ_i(⊤,⊤,⊤). Hence x_CB(n) is the same for all n ≥ 1, and its stable value equals x_CB(1). Prudence requires the stable
value D, so x_CB(1) = false.

*Against FairBot*: at world 0 every box is true, so FairBot's actions at world 0 are all C:
- a(0) = FairBot's action vs X at 0 = □a at 0 = ⊤;
- c(0) = FairBot vs CooperateBot at 0 = ⊤;
- d(0) = FairBot vs DefectBot at 0 = □⊥ at world 0 = ⊤.

So the world-0 atom values against FairBot are (⊤,⊤,⊤), exactly those against CooperateBot. Therefore
x_FB(1) = x_CB(1) = false: X defects against FairBot at world 1.

*Consequence*: FairBot's action against X at world n is □(x_FB) at n, i.e. true iff x_FB(m) holds for all m < n. For
every n ≥ 2 this includes m = 1, where x_FB(1) is false; hence FairBot defects against X at every world n ≥ 2, and its
stable action against X is **D**. So X violates the condition "FairBot cooperates with X", and X is not prudent. ∎

(The argument uses only CooperateBot and FairBot: a depth-≤1 agent cannot distinguish FairBot from CooperateBot at
world 1, and any defection at a single world is fatal against FairBot.)

Hence the minimal modal depth of a prudent agent is exactly **2**.

## 3. Prudent agents of depth 2: structure and minimal size

### Necessary conditions (proved)

Let X have depth 2. At world n, φ_X depends only on atom values at worlds < n, and at world 1 only on world-0 atom
values (inner boxes are vacuously true at world 0). Then:

1. **φ_X must be true at world 0 and world 1 against FairBot**, since FairBot's cooperation (stable C) requires
   x_FB(m) true for *all* m. (FairBot vs X is □x_FB.) In fact x_FB(n) = C for every n.
2. As in §2, world-0 atoms against FairBot, CooperateBot and X itself are all (⊤,⊤,⊤) (for itself: a(0)=x_X(0),
   c(0)=x_CB(0), d(0)=x_DB(0), all equal to φ_X with every box true, which equals x_FB(0) = ⊤). Hence
   x_CB(1) = x_FB(1) = x_X(1) = ⊤. Against CooperateBot the depth-2 letterless value is constant from world 2 on, so
   **x_CB must be C, C, D, D, …** — X must defect against CooperateBot exactly from world 2.
3. At world 2, X sees atom histories over worlds 0,1: against CooperateBot (a,c,d) = (⊤⊤⊤),(⊤⊤⊤); against FairBot
   (⊤⊤⊤),(⊤⊤⊥) (FairBot vs DefectBot = □⊥ is false at world 1). Since X must output D on the first and C on the second,
   **the only distinguishing information is d at world 1**: every prudent depth-2 agent must test, under a nested box,
   whether the opponent cooperates with DefectBot — i.e. it necessarily contains the PrudentBot ingredient "□(… d … □…)".
   In particular atom d must occur essentially; agents over a and c alone (at depth 2) are never prudent.

### Minimal size (exhaustive computer search)

Size = number of symbols counting atoms, constants, ¬, ∧, ∨, →, and B (parentheses not counted).
`search/search_prudent.py` enumerates all syntax trees of depth ≤ 2 up to the given size (modulo commutativity of
∧/∨ and double negation, which cannot shrink a minimal formula), and tests prudence with a fast reimplementation of
the checker semantics; every hit was re-verified with `check.py`, and the fast test was cross-validated against
`check.py` on 21,495 formulas with zero disagreements (`search/xcheck.py`).

| size | prudent formulas found |
|------|------------------------|
| ≤ 6  | none |
| 7    | `B(a & (d -> B(F)))` (unique up to the symmetries above) |
| 8    | `B(a & (d -> B(~a)))`, `B(a & (d -> B(~c)))`, `B(a & (d -> B(~d)))`, `B(a & (d -> B(~T)))`, `B(a & (B(F) \| ~d))`, `B(a) & B(d -> B(F))` |

So the **minimal size of a prudent agent is 7 symbols** (`B(a & (d -> B(F)))`), and the minimal size **without
constants is 8** (e.g. `B(a & (d -> B(~d)))`, consistent with the given evidence that nothing of ≤ 7 symbols without
constants is prudent). All minimal examples are variants of PrudentBot: □(a ∧ (d → □(something false from world 1 on
against the relevant opponents))). The minimal-size claim is computational (exhaustive enumeration), not a
hand proof; a full characterization of all depth-2 prudent agents is not given — only the necessary conditions above.
