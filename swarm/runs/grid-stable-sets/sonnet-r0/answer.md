# Answer

1. A stable set exists **iff K is even**.
2. For K = 2h (h ≥ 1) the stable set is **unique**: V = {(0,h,h), (h,0,h), (h,h,0)}.
   For odd K there are none.

(Exhaustive search for K = 2..9, `bf.py`, agrees: one stable set for K = 2, 4, 6, 8 and none for K = 3, 5, 7, 9.)

## Proof

Notation: x dominates y iff x_i > y_i for at least two coordinates i. So x does **not** dominate y iff y_i ≥ x_i for at least two coordinates i. (*)

### Existence for K = 2h
V = {(0,h,h), (h,0,h), (h,h,0)}.
* Internal: two distinct elements, e.g. (0,h,h) and (h,0,h), each exceed the other in exactly one coordinate. Neither dominates the other.
* External: by (*), y is not dominated by (0,h,h) iff y_2 ≥ h or y_3 ≥ h, since y_1 ≥ 0 always. Likewise for the other two elements. If y is dominated by none of them, at least two coordinates of y are ≥ h. The sum is 2h, so those two equal h and the third is 0, so y ∈ V. Hence every y ∉ V is dominated.

### Necessity and uniqueness
Let V be stable.

**Step 1 (internal stability).** Let x ≠ y be in V. Neither dominates the other, so x exceeds y in at most one coordinate, and y exceeds x in at most one. The sums are equal and x ≠ y, so each exceeds the other in exactly one coordinate and they agree in exactly one coordinate. So any two distinct elements of V *agree in exactly one position* and differ in the other two. Label each pair by that position.

**Step 2 (all labels equal is impossible).** Suppose all pairs have the same label, say position 1, so every element has x_1 = c. This includes |V| ≤ 1; V = ∅ is not externally stable.
* If c = K, then V = {(K,0,0)}. The allocation (K−1,1,0) is not in V. It is not dominated, because (K,0,0) exceeds it only in coordinate 1.
* If c < K, take any y with y_1 = c+1. Then y ∉ V. An x ∈ V can dominate y only through coordinates 2 and 3, because x_1 = c < y_1. That needs x_2 + x_3 ≥ y_2 + y_3 + 2. But x_2 + x_3 = K−c and y_2 + y_3 = K−c−1, so this is impossible. So y is undominated, a contradiction.

**Step 3 (a triangle).** So the labels are not all equal. The complete graph on V is edge-coloured by labels with more than one colour and is connected. Hence some a ∈ V has two incident edges of different colours. (Otherwise each vertex has a single colour on all its edges, adjacent vertices share it, and so all edges have one colour.) Relabel coordinates so that a = (p,q,r), b ∈ V agrees with a in position 1, and c ∈ V agrees with a in position 2. Then b = (p, q+d, r−d) with d ≠ 0, and c = (p+e, q, r−e) with e ≠ 0. Now b_1 ≠ c_1 and b_2 ≠ c_2, so b and c must agree in position 3. That gives r−d = r−e, so e = d.

Thus a = (p,q,r), b = (p,q+d,r−d), c = (p+d,q,r−d).

**Step 4 (V = {a,b,c}).** Suppose e' ∈ V \ {a,b,c}. It agrees with a in exactly one position.
* Position 1 (e'_1 = p): e' agrees with b in position 1 already, so it must not agree with b elsewhere. It must agree with c somewhere, and e'_1 = p ≠ p+d. So e'_2 = q, which makes e' = a, or e'_3 = r−d, which makes e' = b. Contradiction.
* Position 2: this is symmetric, by swapping coordinates 1 and 2 and swapping b and c.
* Position 3 (e'_3 = r, with e'_1 ≠ p and e'_2 ≠ q): e' must agree with b, and b_3 = r−d ≠ r, so e'_1 = p or e'_2 = q+d. The first is excluded, so e'_2 = q+d and e'_1 = p−d. But e' = (p−d, q+d, r) agrees with c = (p+d, q, r−d) nowhere. Contradiction.

So V = {a,b,c}.

**Step 5 (d > 0, "up" triangle) is not stable.** Here r ≥ d. Exhibit y ∉ V that is dominated by none of a, b, c, using (*).
* d ≥ 2: take y = (p+1, q, r−1). Against a, coordinates 1 and 2 satisfy y ≥ a. Against b, coordinates 1 and 3 do (r−1 ≥ r−d). Against c, coordinates 2 and 3 do. Also y ∉ V: its third coordinate r−1 differs from r and r−d.
* d = 1, r ≥ 2: take y = (p+1, q+1, r−2). Coordinates 1 and 2 satisfy y ≥ x for each of a, b, c. The third coordinate r−2 differs from r and r−1, so y ∉ V.
* d = 1, r = 1: a = (p,q,1), b = (p,q+1,0), c = (p+1,q,0). Since K ≥ 2, p+q ≥ 1. If q ≥ 1, take y = (p+1, q−1, 1). Against a, coordinates 1 and 3 satisfy y ≥ a. Against b, coordinates 1 and 3 do. Against c, coordinates 1 and 3 do. The third coordinate is 1, which only a has, and y ≠ a, so y ∉ V. If p ≥ 1, take y = (p−1, q+1, 1) by symmetry.

In every case y is undominated, contradicting external stability.

**Step 6 (d = −h < 0, "down" triangle).** Here a = (p,q,r), b = (p,q−h,r+h), c = (p−h,q,r+h), with p,q ≥ h.
* If r ≥ 1, take y = (p+1, q, r−1). Against a, coordinates 1 and 2 satisfy y ≥ a. Against b, coordinates 1 and 2 do (q ≥ q−h). Against c, coordinates 1 and 2 do. The first coordinate p+1 is not p or p−h, so y ∉ V. y is undominated, a contradiction. Hence r = 0, K = p+q, and a = (p,q,0), b = (p,q−h,h), c = (p−h,q,h).
* If q > h, take y = (p, q−h−1, h+1). Against a, coordinates 1 and 3 satisfy y ≥ a. Against b, coordinates 1 and 3 do. Against c, coordinates 1 and 3 do. Its third coordinate h+1 is not 0 or h, so y ∉ V. y is undominated, a contradiction. So q = h.
* Symmetrically, p > h is impossible, so p = h.

Thus K = p+q = 2h, and V = {(h,h,0), (h,0,h), (0,h,h)}.

**Conclusion.** Any stable set equals the symmetric triple, which needs K = 2h. So there is no stable set for odd K, and exactly one for even K. ∎
