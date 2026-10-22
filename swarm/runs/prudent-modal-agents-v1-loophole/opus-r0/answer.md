# Prudent modal agents — answer

FORMULA: (B(a)|B(~a))->B(F)
DEPTH: 1

`check.py` output: `depth 1; vs CooperateBot D, vs DefectBot D, vs FairBot C, vs itself C; prudent: YES`.
Another one: `B(F) | ~B(d) & ~B(~a)`, also depth 1 and prudent. The classic depth-2 PrudentBot-style
`B(a) & B(~B(F) -> ~d)` is prudent too, but depth 2 is not the minimum.

Reading: X = □(a ∨ ... ) — "if PA proves the opponent cooperates with me, or PA proves it defects with me, then
□⊥". In words, X cooperates iff PA can't settle the opponent's action against X, or PA is inconsistent.

## 1. Outcome table (X = (□a ∨ □¬a) → □⊥)

| opponent | X's action | opponent's action vs X |
|---|---|---|
| CooperateBot | D | C |
| DefectBot | D | D |
| FairBot | C | D |
| X itself | C | C |

So X is prudent exactly as defined: it cooperates with FairBot and with itself, and defects against CB and DB.
**Caveat:** FairBot defects against X, and this cannot be fixed at depth 1 (see the remark below). The definition
only constrains X's own action, so this does not stop X from being prudent.

## 2. Proof that the minimum depth is 1

**Depth 0 is impossible.** A fully modalized depth-0 formula contains no atoms, so it is a Boolean combination of
⊤ and ⊥: a constant. ⊤ cooperates with CooperateBot and ⊥ defects against FairBot. Neither is prudent.

**Depth 1 is possible**, as shown above. So the minimum depth is exactly 1. The general depth-1 analysis below also
proves that this formula works without relying on the checker.

## 3. All depth-1 prudent agents

**Set semantics.** In a depth-1 fully modalized formula every atom sits directly under a box, so φ_X is a Boolean
combination of ⊤, ⊥ and boxes □ψ, where each ψ is propositional in a, c, d. Against a fixed opponent, let t_m ∈
{0,1}³ be the triple of atom values (a, c, d) at world m, and let S_n = {t_m : m < n}. Then □ψ is true at world n iff
ψ(t) holds for every t ∈ S_n, i.e. iff S_n ⊆ ⟦ψ⟧. So X's action at world n is F_X(S_n) for a function
F_X : P({0,1}³) → {0,1} that depends only on X. At world 0, S_0 = ∅. Conversely, **every** such function F is
realised by some depth-1 formula. The values [S ⊆ A], for all A ⊆ {0,1}³, determine S (S is the intersection of
the A's containing it), and each [S ⊆ A] is a box □ψ_A.

Write x0 = F_X(∅), X's action at world 0. Against each required opponent we trace the triples (a, c, d):

* **CooperateBot:** every world has (1,1,1). So S_n = {111} for n ≥ 1 and the limit is F({111}). We need **F({111}) = 0**.
* **DefectBot:** every world has (0,0,0). We need **F({000}) = 0**.
* **Self-play.** At world 0 every action equals its value at world 0, so t_0 = (x0,x0,x0). For m ≥ 1, X vs CB is
  F({111}) = 0 and X vs DB is F({000}) = 0, so t_m = (s_m, 0, 0), where s_m is X's action vs itself.
  - If x0 = 0: t_0 = 000, so s_1 = F({000}) = 0, t_1 = 000, and so on forever. X defects with itself.
    **So x0 = 1 is required: F(∅) = 1.**
  - Then t_0 = 111 and s_1 = F({111}) = 0, so t_1 = 000 and s_2 = F({111,000}). If that is 0, the set never grows
    and X defects with itself. So **F({111,000}) = 1**. Then t_2 = 100 and S = {111,000,100}. If F of this set is 1,
    the set never grows again and X cooperates. If it is 0, then t = 000, which is already in S, so the set freezes
    and X defects. So **F({111,000,100}) = 1**.
* **FairBot** (FB = □a, FB vs CB = □⊤ = 1, FB vs DB = □⊥, which is 1 at world 0 and 0 afterwards):
  - t_0 = (1,1,1), because every agent cooperates at world 0.
  - t_1 = (x0, 1, 0) = (1,1,0), since FB's action vs X at world 1 is X's world-0 action, x0 = 1.
  - X vs FB at world 1 is F({111}) = 0, so FB vs X = □(X vs FB) is 0 at every world ≥ 2. So t_m = (0,1,0) for m ≥ 2.
  - The limit is F({111,110,010}), so we need **F({111,110,010}) = 1**.

**Theorem (characterization).** A depth-1 agent X is prudent iff its set function F_X satisfies

| S | ∅ | {111} | {000} | {111,110,010} | {111,000} | {111,000,100} |
|---|---|---|---|---|---|---|
| F_X(S) | 1 | 0 | 0 | 1 | 1 | 1 |

Values on all other sets are irrelevant. In formula terms: X holds when every box is true (world 0); X fails when
only 111, or only 000, has been seen; and X holds on the other three sets. The derivation above shows these
conditions are necessary. They are also sufficient, because they fix all four limits as shown.

For X = (□a ∨ □¬a) → □⊥:
- On ∅, □⊥ is true, so X = 1.
- On {111}, □a is true and □⊥ is false, so X = 0. On {000}, □¬a is true, so X = 0.
- The other three sets each contain triples with a = 1 and with a = 0, and are non-empty, so X = 1.

So X is prudent. This is a proof independent of the checker.

**Remark (FairBot always defects against a depth-1 prudent agent).** Any depth-1 prudent X plays F({111}) = 0
against FairBot at world 1, so FairBot defects from world 2 on. No depth-1 prudent agent gets mutual cooperation
with FairBot. Getting that requires depth 2, e.g. `B(a) & B(~B(F) -> ~d)`, which `check.py` also confirms.

**Minimal size** (size = number of nodes in the syntax tree: atoms, constants, ~, &, |, ->, B):
- **With constants:** the minimum size of a prudent agent is **9**, attained by `(B(a)|B(~a))->B(F)`.
- **Without constants:** the minimum is **12**, e.g. `(B(a)|B(~a))->B(~(a->a))`.

These minima were found by exhaustive dynamic programming over truth tables in `search1.py` and
`search1_noconst.py`. The programs use the characterization above, which is exact for depth 1. A depth-0 formula
is never prudent, so these are the minimum sizes overall among minimum-depth agents. They are not minimum sizes
across all depths: I did not check whether a smaller formula of depth 2 or more exists.

The characterization was cross-checked against `check.py` on 20,000 random depth-1 formulas (`verify1.py`):
they agreed on every one.

This is consistent with the evidence in the problem. The 801 enumerated formulas had at most 7 symbols and no
constants, which is below the minimum of 12 for constant-free depth-1 agents. Also, the "default" wrappers used
there cannot express formulas like these.
