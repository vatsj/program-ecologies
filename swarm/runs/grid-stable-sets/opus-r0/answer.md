# Stable sets of three-player majority division on the grid

## Answer

1. A stable set exists **if and only if K is even**.
2. For even K = 2h it is **unique**: V = {(h,h,0), (h,0,h), (0,h,h)}.
   For odd K there are none. (The continuum's discriminatory solutions have no counterpart on the grid.)

Computer check: `code/enum.py` is an exhaustive backtracking search over all subsets (it enumerates every kernel of the
domination digraph). For every K from 2 to 14 it found exactly the set above when K is even and nothing when K is odd.
The proof below covers all K ≥ 2.

## Proof

Write e_1, e_2, e_3 for the unit vectors. "x agrees with y in coordinate i" means x_i = y_i. If two allocations agree in
two coordinates they are equal, because the coordinates sum to K.

### Lemma 1 (internal stability ⇒ exactly one common coordinate)
Let x ≠ y both be in V. Let P = {i : x_i > y_i} and N = {i : x_i < y_i}. Both sets are nonempty because x ≠ y and the
coordinates have equal sums. Since x does not dominate y, |P| ≤ 1, and since y does not dominate x, |N| ≤ 1. So |P| = |N| = 1,
and x and y agree in **exactly one** coordinate.

### Lemma 2 (structure of V)
If V is internally stable, then either
- (A) V ⊆ L_{k,c} := {x : x_k = c} for some k and c (this includes |V| ≤ 2), or
- (B) V = {T − d e_1, T − d e_2, T − d e_3} for some integer vector T and integer d ≠ 0, with T_1+T_2+T_3 = K + d.

*Proof.* Suppose (A) fails. Then |V| ≥ 2, and we can pick x ≠ y in V. By Lemma 1 they agree in exactly one coordinate; after
relabeling players, x_3 = y_3 = c. Since V ⊄ L_{3,c}, some z ∈ V has z_3 ≠ c. By Lemma 1, z agrees with x in coordinate 1
or 2, and with y in coordinate 1 or 2. These cannot be the same coordinate, or else x and y would agree in two coordinates.
After swapping the names x and y if needed, z_1 = x_1 and z_2 = y_2. Write x = (a,b,c) and y = (a',b',c), with a ≠ a' and
b ≠ b'. Then z = (a, b', K−a−b').

*There is no fourth element.* Suppose w ∈ V \ {x,y,z}. Then w agrees with x in exactly one coordinate:
- w_3 = c. Then w agrees with y in coordinate 3, and z_3 ≠ c, so w agrees with z in coordinate 1 or 2. If w_1 = z_1 = x_1,
  then w = x. If w_2 = z_2 = y_2, then w = y. Contradiction.
- w_1 = a = z_1. Coordinate 1 cannot be the agreement with y, because y_1 = a' ≠ a. If w_3 = y_3 = x_3, then w = x. If
  w_2 = y_2 = z_2, then w = z. Contradiction.
- w_2 = b. The agreement with y cannot be coordinate 2 (b ≠ b') or coordinate 3 (that would give w = x), so w_1 = a'. The
  agreement with z cannot be coordinate 1 (a' ≠ a) or coordinate 2 (b ≠ b'), so w_3 = z_3 = K−a−b'. Then
  w_1+w_2+w_3 = K + (a'−a) + (b−b'). Since x_3 = y_3 we have a+b = a'+b', so this sum is K + 2(b−b') ≠ K. Contradiction.

So V = {x,y,z}. Put d = a − a' = b' − b ≠ 0 and T = (a, b', c). Then x = T − d e_2, y = T − d e_1, and z = T − d e_3,
using z_3 = K−a−b' = c−d. Also ΣT = K + d. ∎

### Theorem
For K ≥ 2, V is stable iff K = 2h and V = {(h,h,0),(h,0,h),(0,h,h)}.

*Sufficiency.* Let K = 2h. Any two elements of V agree in one coordinate, and each is larger than the other in exactly one
coordinate, so neither dominates the other. Now take y ∉ V. If two coordinates satisfy y_i < h and y_j < h, then the element
of V with h in positions i and j dominates y. Otherwise at least two coordinates are ≥ h. Their sum is ≥ K, so both equal h
and the third is 0, which means y ∈ V. Contradiction. So V is stable.

*Necessity.* Let V be stable. Then V ≠ ∅, since allocations exist and each must be dominated by something in V. Apply
Lemma 2.

**Case (A): V ⊆ L_{3,c}** (after relabeling players). Take y ∈ L_{3,c}. For any x ∈ V we have x_3 = y_3 and
x_1 + x_2 = y_1 + y_2, so x cannot be larger than y in both coordinates 1 and 2. Hence nothing in V dominates y, and
external stability forces y ∈ V. So V = L_{3,c}.
- If c < K, take y with y_3 = c+1. Any x ∈ V has x_3 = c < y_3, so x would have to beat y in coordinates 1 and 2. That
  needs x_1+x_2 ≥ y_1+y_2+2, but x_1+x_2 = K−c = y_1+y_2+1. So y is undominated and not in V. Contradiction.
- If c = K, then V = {(0,0,K)}. The allocation (1,0,K−1) exists because K ≥ 1, is not in V, and is not dominated: (0,0,K)
  is larger only in coordinate 3. Contradiction.

So case (A) is impossible.

**Case (B), d > 0.** Each element must be nonnegative, so T_i ≥ d for all i. Suppose some T_k > d; relabel so that k = 3.
Let y = (T_1+1, T_2, T_3−d−1). This is an allocation: its sum is K and T_3−d−1 ≥ 0. It is not in V, because
y_1 = T_1+1 is larger than the first coordinate of every element of V. Every element of V is ≤ T coordinatewise, so it is
not larger than y in coordinate 1 or coordinate 2. It can only be larger in coordinate 3, so it does not dominate y. This
contradicts external stability. Hence T = (d,d,d), so 3d = K + d, which gives K = 2d. Then V is exactly
{(d,d,0),(d,0,d),(0,d,d)}, the symmetric set.

**Case (B), d = −e < 0.** Here V = {S + e e_i}, where S = T satisfies S ≥ 0 and ΣS = K − e. The element S + e e_i equals
S_j in every coordinate j ≠ i.
- If e ≥ 2, let y = S + (e−1)e_1 + e_2. This is an allocation, and it is not in V because it is strictly above S in two
  coordinates. For every i and every j ≠ i, (S+e e_i)_j = S_j ≤ y_j. So each element of V is larger than y in at most one
  coordinate, and y is undominated. Contradiction.
- If e = 1, then ΣS = K−1 ≥ 1, so some S_k ≥ 1; relabel so that k = 3. Let y = S + e_1 + e_2 − e_3. This is an allocation.
  It is not in V, since y_3 = S_3−1 is smaller than the third coordinate of every element of V. Compare y with each element:
  S+e_1 is larger only in coordinate 3, S+e_2 is larger only in coordinate 3, and S+e_3 is larger only in coordinate 3. So y
  is undominated. Contradiction.

So every stable set is the symmetric one, and it requires K to be even. Combined with sufficiency, this proves the theorem
and answers questions 1–3 for every K ≥ 2. ∎

### Remark: why the discriminatory solutions fail
In the continuum, {x : x_3 = c} is stable for c < 1/2. On the grid, an allocation with y_3 = c + 1 can only be beaten by
improving both players 1 and 2. That needs two extra units, and only one is available. This is the c < K sub-case of
case (A).
